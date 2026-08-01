"""Train and evaluate a small local categorical MODEL-001 simulation model."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

TARGETS = {
    "cleared_dingque": (0, 1),
    "dominant_suit": ("wan", "tong", "tiao", "mixed"),
    "shape": ("seven_pairs", "pure_suit", "all_pongs", "standard", "other"),
}
MODEL_VERSION = "MODEL001-SIM-NB 1.0.0"


def _rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def visible_tokens(feature: dict) -> list[str]:
    """Extract bounded categorical evidence from PlayerView, never restricted truth."""
    view = feature["policy_features"]
    opponent_seat = int(feature["opponent_seat"])
    player = next((p for p in view.get("players", []) if int(p.get("seat", -1)) == opponent_seat), {})
    tokens = [
        f"phase={view.get('phase','unknown')}",
        f"dingque={player.get('dingque') or 'none'}",
        f"hand_count={int(player.get('hand_count', 0))}",
        f"status={player.get('status','unknown')}",
        f"turn_bin={min(9, int(view.get('turn_index', 0)) // 10)}",
        f"style={feature.get('style_id','unknown')}",
    ]
    discards = Counter(str(tile).split("_")[0] for tile in player.get("discard_pile", []))
    melds = Counter()
    for meld in player.get("melds", []):
        raw = meld.get("tile_id") or meld.get("suit") or "unknown"
        melds[str(raw).split("_")[0]] += int(meld.get("tile_count", 1))
    for suit in ("wan", "tong", "tiao"):
        tokens.append(f"discard_{suit}={min(9, discards[suit])}")
        tokens.append(f"meld_{suit}={min(12, melds[suit])}")
    return tokens


def fit(features: list[dict], labels: dict[str, dict]) -> dict:
    artifact: dict[str, Any] = {"model_version": MODEL_VERSION, "alpha": 1.0, "targets": {}}
    train = [row for row in features if row["split"] == "train"]
    vocab = sorted({token for row in train for token in visible_tokens(row)})
    for target, classes in TARGETS.items():
        class_counts = Counter(labels[row["sample_id"]][target] for row in train)
        token_counts: dict[Any, Counter] = defaultdict(Counter)
        totals = Counter()
        for row in train:
            cls = labels[row["sample_id"]][target]
            for token in visible_tokens(row):
                token_counts[cls][token] += 1
                totals[cls] += 1
        artifact["targets"][target] = {
            "classes": list(classes), "class_counts": {str(k): class_counts[k] for k in classes},
            "token_counts": {str(cls): dict(token_counts[cls]) for cls in classes},
            "token_totals": {str(cls): totals[cls] for cls in classes}, "vocab_size": len(vocab),
        }
    artifact["training_samples"] = len(train)
    return artifact


def predict(artifact: dict, feature: dict, target: str) -> list[float]:
    head = artifact["targets"][target]
    classes = head["classes"]
    total_classes = sum(head["class_counts"].values())
    vocab_size = max(1, int(head["vocab_size"]))
    scores = []
    for cls in classes:
        key = str(cls)
        prior = (head["class_counts"][key] + 1.0) / (total_classes + len(classes))
        score = math.log(prior)
        denominator = head["token_totals"][key] + vocab_size
        counts = head["token_counts"][key]
        for token in visible_tokens(feature):
            score += math.log((counts.get(token, 0) + 1.0) / denominator)
        scores.append(score)
    peak = max(scores)
    values = [math.exp(value - peak) for value in scores]
    total = sum(values)
    return [value / total for value in values]


def _metrics(probs: list[list[float]], truths: list[int]) -> dict:
    if not truths:
        return {"samples": 0, "status": "NOT_EVALUATED_EMPTY_SPLIT"}
    n, k = len(truths), len(probs[0])
    brier = sum(sum((p[j] - int(j == y)) ** 2 for j in range(k)) for p, y in zip(probs, truths)) / n
    log_loss = -sum(math.log(max(1e-15, p[y])) for p, y in zip(probs, truths)) / n
    correct = sum(max(range(k), key=lambda j: probs[i][j]) == y for i, y in enumerate(truths)) / n
    buckets = [[] for _ in range(10)]
    for p, y in zip(probs, truths):
        guess = max(range(k), key=lambda j: p[j])
        confidence = p[guess]
        buckets[min(9, int(confidence * 10))].append((confidence, int(guess == y)))
    ece = sum(len(bucket) / n * abs(sum(x[0] for x in bucket) / len(bucket) - sum(x[1] for x in bucket) / len(bucket)) for bucket in buckets if bucket)
    return {"samples": n, "brier": brier, "log_loss": log_loss, "ece_10_bin": ece, "accuracy": correct, "threshold_status": "NOT_EVALUATED_NO_APPROVED_THRESHOLD"}


def train_and_evaluate(dataset: Path, output: Path) -> dict:
    features = _rows(dataset / "features.jsonl")
    label_rows = _rows(dataset / "labels.jsonl")
    labels = {row["sample_id"]: row for row in label_rows}
    if {row["sample_id"] for row in features} != set(labels):
        raise ValueError("feature/label sample sets differ")
    artifact = fit(features, labels)
    metrics: dict[str, Any] = {"model_version": MODEL_VERSION, "validation_scope": "SIMULATION", "external_validity": "NOT_EVALUATED", "splits": {}}
    for split in ("validation", "test"):
        subset = [row for row in features if row["split"] == split]
        metrics["splits"][split] = {}
        for target, classes in TARGETS.items():
            probs = [predict(artifact, row, target) for row in subset]
            truths = [list(classes).index(labels[row["sample_id"]][target]) for row in subset]
            metrics["splits"][split][target] = _metrics(probs, truths)
    output.mkdir(parents=True, exist_ok=True)
    model_bytes = json.dumps(artifact, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    (output / "model.json").write_bytes(model_bytes)
    metrics["model_sha256"] = hashlib.sha256(model_bytes).hexdigest()
    metrics["calibration_conclusion"] = "SIMULATION_METRICS_RECORDED_NOT_PASSED_WITHOUT_APPROVED_THRESHOLDS"
    (output / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(train_and_evaluate(args.dataset, args.output), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
