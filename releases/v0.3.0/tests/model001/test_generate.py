from __future__ import annotations

import json
import socket
from pathlib import Path

import pytest

from training.model001.generate import (
    ALLOWED_STYLES,
    _walk_validate_features,
    generate_dataset,
    stable_split,
)


def _rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


@pytest.fixture(scope="module")
def generated(tmp_path_factory: pytest.TempPathFactory) -> tuple[dict, list[dict], list[dict]]:
    out = tmp_path_factory.mktemp("model001-shared")
    manifest = generate_dataset(20, list(ALLOWED_STYLES), 20260730, out)
    return manifest, _rows(out / "features.jsonl"), _rows(out / "labels.jsonl")


def test_small_generation_and_contract(tmp_path: Path) -> None:
    out = tmp_path / "dataset"
    manifest = generate_dataset(20, list(ALLOWED_STYLES), 20260730, out)
    features, labels = _rows(out / "features.jsonl"), _rows(out / "labels.jsonl")
    assert manifest["actual_samples"] >= 20
    assert manifest["valid"] and manifest["illegal_actions"] == 0
    assert {row["style_id"] for row in features} == set(ALLOWED_STYLES)
    assert {row["sample_id"] for row in features} == {row["sample_id"] for row in labels}
    assert all(row["label_source"] == "SIMULATOR_TRUTH" for row in labels)
    assert len({row["split"] for row in features if row["game_id"] == features[0]["game_id"]}) == 1


def test_same_seed_is_byte_reproducible_and_different_seed_changes_game(tmp_path: Path) -> None:
    a, b, c = tmp_path / "a", tmp_path / "b", tmp_path / "c"
    generate_dataset(20, list(ALLOWED_STYLES), 7, a)
    generate_dataset(20, list(ALLOWED_STYLES), 7, b)
    generate_dataset(20, list(ALLOWED_STYLES), 8, c)
    for name in ("features.jsonl", "labels.jsonl", "manifest.json"):
        assert (a / name).read_bytes() == (b / name).read_bytes()
    assert _rows(a / "features.jsonl")[0]["game_id"] != _rows(c / "features.jsonl")[0]["game_id"]


def test_feature_label_separation_and_poison_rejection(tmp_path: Path) -> None:
    out = tmp_path / "dataset"
    generate_dataset(20, list(ALLOWED_STYLES), 99, out)
    features = _rows(out / "features.jsonl")
    assert all(not ({"shape", "dominant_suit", "cleared_dingque", "label_source"} & row.keys()) for row in features)
    with pytest.raises(ValueError, match="forbidden feature field"):
        _walk_validate_features({"nested": {"wall_order": [1, 2, 3]}})


def test_generator_does_not_use_network_or_model_artifact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def denied(*args, **kwargs):
        raise AssertionError("network access attempted")
    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(socket.socket, "connect", denied)
    manifest = generate_dataset(20, list(ALLOWED_STYLES), 123, tmp_path / "dataset")
    assert manifest["valid"]
    assert "model" not in manifest and "artifact" not in manifest


def test_samples_minimum_is_honored(generated) -> None:
    manifest, _, _ = generated
    assert manifest["actual_samples"] >= manifest["requested_samples"] == 20


def test_all_games_are_complete(generated) -> None:
    manifest, features, _ = generated
    assert len({row["game_id"] for row in features}) == manifest["games"]


def test_illegal_action_rate_is_zero(generated) -> None:
    manifest, _, _ = generated
    assert manifest["illegal_actions"] == 0


def test_feature_ids_are_unique(generated) -> None:
    _, features, _ = generated
    ids = [row["sample_id"] for row in features]
    assert len(ids) == len(set(ids))


def test_label_ids_are_unique(generated) -> None:
    _, _, labels = generated
    ids = [row["sample_id"] for row in labels]
    assert len(ids) == len(set(ids))


def test_game_split_has_no_cross_partition(generated) -> None:
    _, features, _ = generated
    by_game: dict[str, set[str]] = {}
    for row in features:
        by_game.setdefault(row["game_id"], set()).add(row["split"])
    assert all(len(value) == 1 for value in by_game.values())
    assert all(next(iter(value)) == stable_split(game_id) for game_id, value in by_game.items())


def test_labels_use_approved_enums(generated) -> None:
    _, _, labels = generated
    assert {row["cleared_dingque"] for row in labels} <= {0, 1}
    assert {row["dominant_suit"] for row in labels} <= {"wan", "tong", "tiao", "mixed"}
    assert {row["shape"] for row in labels} <= {"seven_pairs", "pure_suit", "all_pongs", "standard", "other"}


def test_manifest_records_approved_targets(generated) -> None:
    manifest, _, _ = generated
    assert manifest["cleared_target"] == "CURRENT_HIDDEN_STATE"
    assert manifest["dominant_suit_target"] == "CURRENT_HIDDEN_STATE"
    assert manifest["shape_target"] == "EVENTUAL_TERMINAL_OUTCOME"
