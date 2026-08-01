from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.model001_dataset_validator import validate_dataset


def _write_dataset(path: Path, *, split_a: str = "train", provenance: bool = False) -> None:
    path.mkdir(parents=True, exist_ok=True)
    features = [{"sample_id": "s1", "game_id": "g1", "split": split_a, "policy_features": {"phase": "play"}}]
    labels = [{"sample_id": "s1", "shape": "other", "label_source": "SIMULATOR_TRUTH"}]
    manifest = {"generator_version": "test", "feature_schema_version": "1", "label_schema_version": "1", "validation_scope": "SIMULATION", "data_origin": "SIMULATION"}
    if provenance:
        manifest["provenance"] = {"source": "approved-test-fixture", "consent": "test"}
    for name, rows in (("features.jsonl", features), ("labels.jsonl", labels)):
        (path / name).write_text("\n".join(json.dumps(row) for row in rows) + "\n")
    (path / "manifest.json").write_text(json.dumps(manifest))


def test_simulation_dataset_validates() -> None:
    result = validate_dataset(Path("data/model001/model001-sim-v1"), minimum_samples=10000)
    assert result["valid"] and result["samples"] >= 10000
    assert result["external_validity"] == "NOT_EVALUATED"


def test_formal_dataset_requires_provenance(tmp_path: Path) -> None:
    _write_dataset(tmp_path)
    with pytest.raises(ValueError, match="provenance"):
        validate_dataset(tmp_path, require_provenance=True)


def test_group_leakage_rejected(tmp_path: Path) -> None:
    _write_dataset(tmp_path)
    rows = [
        {"sample_id": "s2", "game_id": "g1", "split": "train", "policy_features": {}},
        {"sample_id": "s3", "game_id": "g1", "split": "test", "policy_features": {}},
    ]
    (tmp_path / "features.jsonl").write_text("\n".join(json.dumps(row) for row in rows) + "\n")
    (tmp_path / "labels.jsonl").write_text("\n".join(json.dumps({"sample_id": key}) for key in ("s2", "s3")) + "\n")
    with pytest.raises(ValueError, match="group leakage"):
        validate_dataset(tmp_path)


def test_data_origin_is_explicit(tmp_path: Path) -> None:
    _write_dataset(tmp_path)
    assert validate_dataset(tmp_path)["data_origin"] == "SIMULATION"
    manifest = json.loads((tmp_path / "manifest.json").read_text())
    manifest.pop("data_origin")
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="data_origin"):
        validate_dataset(tmp_path)
