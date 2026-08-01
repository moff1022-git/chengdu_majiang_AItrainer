"""Validate MODEL-001 datasets before training or formal calibration.

The validator is deliberately independent of the model implementation.  It
checks the feature/label boundary, grouped split integrity, provenance, and
canonical hashes, while never upgrading external-validity status.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

REQUIRED_MANIFEST = ("generator_version", "feature_schema_version", "label_schema_version", "validation_scope")
DATA_ORIGINS = {"SIMULATION", "HUMAN"}
GROUP_KEYS = ("player_id", "match_id", "game_id", "seed_family")
FORBIDDEN_FEATURE_KEYS = {"label", "truth", "oracle", "restricted_label_zone", "future_event", "raw_seed"}


def canonical_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _walk(value: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_FEATURE_KEYS:
                raise ValueError(f"forbidden feature field: {'.'.join(path + (str(key),))}")
            _walk(child, path + (str(key),))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            _walk(child, path + (str(i),))


def validate_dataset(dataset: Path, *, minimum_samples: int = 1, require_provenance: bool = False) -> dict[str, Any]:
    feature_path, label_path, manifest_path = (dataset / name for name in ("features.jsonl", "labels.jsonl", "manifest.json"))
    if not all(path.is_file() for path in (feature_path, label_path, manifest_path)):
        raise ValueError("dataset requires features.jsonl, labels.jsonl, and manifest.json")
    features, labels = _rows(feature_path), _rows(label_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if len(features) < minimum_samples:
        raise ValueError(f"sample count {len(features)} below minimum {minimum_samples}")
    fids, lids = [row.get("sample_id") for row in features], [row.get("sample_id") for row in labels]
    if None in fids or len(set(fids)) != len(fids) or fids != lids:
        raise ValueError("feature/label sample_id parity or ordering failed")
    groups: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for row in features:
        if "policy_features" not in row:
            raise ValueError("feature row missing policy_features")
        _walk(row["policy_features"])
        # game_id is mandatory; optional fields become empty so old simulation
        # data remains valid while formal data can enforce richer grouping.
        group = tuple(str(row.get(key, "")) for key in GROUP_KEYS)
        groups[group].add(str(row.get("split", "")))
    if any(len(splits) != 1 or "" in splits for splits in groups.values()):
        raise ValueError("group leakage or missing split detected")
    missing = [key for key in REQUIRED_MANIFEST if not manifest.get(key)]
    if missing:
        raise ValueError("manifest missing: " + ", ".join(missing))
    origin = str(manifest.get("data_origin", "")).upper()
    if origin not in DATA_ORIGINS:
        raise ValueError("manifest data_origin must be SIMULATION or HUMAN")
    if require_provenance and not manifest.get("provenance"):
        raise ValueError("formal dataset requires manifest.provenance")
    result = {
        "valid": True,
        "samples": len(features),
        "groups": len(groups),
        "split_counts": {split: sum(1 for row in features if row.get("split") == split) for split in ("train", "validation", "test")},
        "external_validity": manifest.get("external_validity", "NOT_EVALUATED"),
        "data_origin": origin,
        "sha256": {name: canonical_sha256(dataset / name) for name in ("features.jsonl", "labels.jsonl", "manifest.json")},
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--minimum-samples", type=int, default=1)
    parser.add_argument("--require-provenance", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate_dataset(args.dataset, minimum_samples=args.minimum_samples, require_provenance=args.require_provenance), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
