"""Streaming, public-information-only F0057 candidate correlation audit."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


FIELDS = ("shanten", "dingque_tiles", "ukeire_public_count")


def _bucket(field: str, value: float) -> str:
    value = int(value)
    if field == "shanten": return str(value) if value <= 3 else "4+"
    if field == "dingque_tiles": return str(value) if value <= 2 else "3+"
    return "0" if value == 0 else ("1-3" if value <= 3 else "4+")


def audit(trace_root: Path, games_path: Path) -> dict:
    games = {row["game_id"]: row for row in map(json.loads, games_path.read_text(encoding="utf-8").splitlines())}
    hua_zhu = {gid for gid, row in games.items() if 0 in row.get("settle_tags", {}).get("hua_zhu", [])}
    records = candidates = 0
    coverage = {field: 0 for field in FIELDS}
    strata: dict[tuple, list[float]] = defaultdict(lambda: [0, 0.0, 0.0])
    for path in trace_root.glob("*/*.audit.jsonl"):
        for line in path.open(encoding="utf-8"):
            row = json.loads(line)
            if row.get("seat") != 0: continue
            ranked = row.get("decision_trace", {}).get("candidates") or []
            if not ranked: continue
            records += 1; candidates += len(ranked)
            ranked = sorted(ranked, key=lambda c: float(c.get("score", 0)), reverse=True)
            margin = float(ranked[0].get("score", 0)) - float(ranked[1].get("score", 0)) if len(ranked) > 1 else 0.0
            features = ranked[0].get("features", {})
            outcome = "hua_zhu" if row.get("game_id") in hua_zhu else "non_hua_zhu"
            for field in FIELDS:
                if field not in features: continue
                coverage[field] += 1
                key = (outcome, field, _bucket(field, features[field]))
                cell = strata[key]; cell[0] += 1; cell[1] += margin; cell[2] += float(features[field])
    return {"audit_scope": "seat0 public decision_trace candidates only", "decision_records": records,
            "candidate_records": candidates, "field_coverage": {f: {"count": coverage[f], "rate": coverage[f] / records if records else 0} for f in FIELDS},
            "strata": [{"outcome": k[0], "field": k[1], "bucket": k[2], "count": v[0],
                        "mean_top2_margin": v[1] / v[0], "mean_feature_value": v[2] / v[0]} for k, v in sorted(strata.items())],
            "causal_claim": False, "limitations": ["observational association only", "candidate score scales are policy-specific"]}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("trace_root", type=Path); parser.add_argument("games", type=Path); parser.add_argument("output", type=Path)
    args = parser.parse_args(argv); result = audit(args.trace_root, args.games)
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("decision_records", "candidate_records", "field_coverage")}, ensure_ascii=False))
    return 0


if __name__ == "__main__": raise SystemExit(main())
