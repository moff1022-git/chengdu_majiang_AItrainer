from __future__ import annotations

import json
from pathlib import Path

from training.model001.generate import ALLOWED_STYLES, generate_dataset
from training.model001.train import TARGETS, predict, train_and_evaluate, visible_tokens


def test_train_artifact_probabilities_and_no_truth_features(tmp_path: Path) -> None:
    dataset, output = tmp_path / "data", tmp_path / "artifact"
    generate_dataset(100, list(ALLOWED_STYLES), 314159, dataset)
    metrics = train_and_evaluate(dataset, output)
    artifact = json.loads((output / "model.json").read_text(encoding="utf-8"))
    feature = json.loads((dataset / "features.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert all(abs(sum(predict(artifact, feature, target)) - 1.0) < 1e-12 for target in TARGETS)
    assert all("truth" not in token and "label" not in token for token in visible_tokens(feature))
    assert metrics["external_validity"] == "NOT_EVALUATED"
    assert metrics["calibration_conclusion"].endswith("WITHOUT_APPROVED_THRESHOLDS")


def test_model_training_is_reproducible(tmp_path: Path) -> None:
    dataset = tmp_path / "data"
    generate_dataset(100, list(ALLOWED_STYLES), 2718, dataset)
    train_and_evaluate(dataset, tmp_path / "a")
    train_and_evaluate(dataset, tmp_path / "b")
    assert (tmp_path / "a/model.json").read_bytes() == (tmp_path / "b/model.json").read_bytes()
    assert (tmp_path / "a/metrics.json").read_bytes() == (tmp_path / "b/metrics.json").read_bytes()
