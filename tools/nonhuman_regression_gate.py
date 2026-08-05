"""Offline paired-result regression gate for Nonhuman versus Expert."""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from statistics import mean


def _games(path: Path) -> dict[str, dict]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    result = {row["game_id"]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"duplicate game_id in {path}")
    return result


def _metric(row: dict, name: str) -> int:
    if name == "score":
        return int(row["scores"]["0"])
    if name == "hu":
        return sum(event.get("seat") == 0 for event in row.get("hu_sequence", []))
    if name == "zimo":
        return sum(event.get("seat") == 0 and event.get("zimo") for event in row.get("hu_sequence", []))
    if name == "hua_zhu":
        return int(0 in row.get("settle_tags", {}).get("hua_zhu", []))
    if name == "dianpao":
        return sum(event.get("loser") == 0 and not event.get("zimo") for event in row.get("hu_sequence", []))
    raise KeyError(name)


def evaluate(spec: dict) -> dict:
    policy = spec["policy"]
    iterations = int(policy.get("bootstrap_iterations", 10_000))
    rng = random.Random(str(policy.get("bootstrap_seed", "F0066-REGRESSION-V1")))
    datasets, combined = [], []
    seen_sha: set[str] = set()
    errors: list[str] = []
    for item in spec["datasets"]:
        dataset_id, sha = item["test_id"], item["dataset_sha256"]
        if sha in seen_sha:
            errors.append(f"duplicate dataset SHA: {sha}")
        seen_sha.add(sha)
        try:
            candidate, baseline = _games(Path(item["nonhuman_games"])), _games(Path(item["expert_games"]))
            if set(candidate) != set(baseline):
                raise ValueError("game_id sets differ")
            if len(candidate) != int(item["requested_games"]):
                raise ValueError("paired count differs from requested_games")
            deltas = [_metric(candidate[g], "score") - _metric(baseline[g], "score") for g in sorted(candidate)]
            metrics = {name: sum(_metric(candidate[g], name) - _metric(baseline[g], name) for g in candidate)
                       for name in ("score", "hu", "zimo", "hua_zhu", "dianpao")}
            datasets.append({"test_id": dataset_id, "dataset_sha256": sha, "paired_games": len(deltas),
                             "score_delta": sum(deltas), "mean_delta": mean(deltas), "metric_deltas": metrics,
                             "better_equal_worse": [sum(x > 0 for x in deltas), sum(x == 0 for x in deltas), sum(x < 0 for x in deltas)]})
            combined.extend(deltas)
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{dataset_id}: {exc}")
    if errors or not combined:
        return {"status": "ERROR", "errors": errors or ["no paired games"], "datasets": datasets}
    samples = sorted(mean(rng.choices(combined, k=len(combined))) for _ in range(iterations))
    lo, hi = samples[int(iterations * .025)], samples[min(iterations - 1, int(iterations * .975))]
    failures = []
    if policy.get("require_each_dataset_positive", True):
        failures += [f"{d['test_id']}: non-positive score delta" for d in datasets if d["score_delta"] <= 0]
    if mean(combined) <= float(policy.get("minimum_mean_delta", 0)):
        failures.append("combined mean delta below threshold")
    if lo <= float(policy.get("minimum_ci_lower", 0)):
        failures.append("bootstrap CI lower bound below threshold")
    totals = {name: sum(d["metric_deltas"][name] for d in datasets) for name in ("hu", "zimo", "hua_zhu", "dianpao")}
    guards = policy.get("metric_guardrails", {})
    for name in ("hu", "zimo"):
        if totals[name] < -int(guards.get(f"max_{name}_decrease", 0)):
            failures.append(f"{name} guardrail failed")
    for name in ("hua_zhu", "dianpao"):
        if totals[name] > int(guards.get(f"max_{name}_increase", 0)):
            failures.append(f"{name} guardrail failed")
    return {"status": "FAIL" if failures else "PASS", "failures": failures, "datasets": datasets,
            "combined": {"paired_games": len(combined), "score_delta": sum(combined), "mean_delta": mean(combined),
                         "bootstrap_95_ci": [lo, hi], "metric_deltas": totals}, "policy": policy}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        result = evaluate(json.loads(args.spec.read_text(encoding="utf-8")))
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        result = {"status": "ERROR", "errors": [str(exc)]}
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return {"PASS": 0, "FAIL": 1, "ERROR": 2}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
