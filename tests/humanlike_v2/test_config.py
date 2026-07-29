from __future__ import annotations

import json
from pathlib import Path

import pytest

from players.humanlike.config import COGNITIVE_GP_IDS, GLOBAL_GP_IDS, ConfigValidationError, load_config
from players.humanlike.engine_adapter import EngineConfigConflict, HumanlikeEngineAdapter
from players.humanlike.traceability import PARAMETER_TRACES, TRACE_BY_ID
from engine.config import EngineConfig

ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "configs" / "humanlike_v2" / "default.json"
COMPATIBILITY = ROOT / "configs" / "humanlike_v2" / "compatibility.json"


def _raw() -> dict:
    return json.loads(DEFAULT.read_text(encoding="utf-8"))


def _write(tmp_path: Path, data: dict) -> Path:
    path = tmp_path / "config.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


def test_default_has_all_gp_profiles_and_stable_hash() -> None:
    first = load_config(DEFAULT)
    second = load_config(DEFAULT)
    assert tuple(first.global_parameters.values) == GLOBAL_GP_IDS
    assert tuple(first.players[0].cognitive_parameters) == COGNITIVE_GP_IDS
    assert tuple(profile.player_id for profile in first.players) == (0, 1, 2, 3)
    assert len(first.config_hash) == 64
    assert first.config_hash == second.config_hash
    with pytest.raises(TypeError):
        first.global_parameters.values["GP-001"] = {}  # type: ignore[index]


def test_hash_ignores_json_format_and_key_order(tmp_path: Path) -> None:
    data = _raw()
    reordered = {key: data[key] for key in reversed(data)}
    assert load_config(_write(tmp_path, reordered), COMPATIBILITY).config_hash == load_config(DEFAULT).config_hash


@pytest.mark.parametrize("missing", ["GP-001", "GP-014"])
def test_missing_gp_fails(tmp_path: Path, missing: str) -> None:
    data = _raw()
    del data["global_parameters"][missing]
    with pytest.raises(ConfigValidationError, match="exactly GP-001 through GP-023"):
        load_config(_write(tmp_path, data), COMPATIBILITY)


def test_unknown_version_fails(tmp_path: Path) -> None:
    data = _raw()
    data["implementation_version"] = "CDMJ-AI-IMPL 9.9.9"
    with pytest.raises(ConfigValidationError, match="unsupported"):
        load_config(_write(tmp_path, data), COMPATIBILITY)


def test_invalid_range_fails(tmp_path: Path) -> None:
    data = _raw()
    data["players"][0]["cognitive_parameters"]["GP-026"]["search_depth"] = 9
    with pytest.raises(ConfigValidationError, match="search_depth"):
        load_config(_write(tmp_path, data), COMPATIBILITY)


def test_non_normalized_weights_fail(tmp_path: Path) -> None:
    data = _raw()
    data["players"][0]["cognitive_parameters"]["GP-027"]["weights"]["risk"] = 0.5
    with pytest.raises(ConfigValidationError, match="sum to 1"):
        load_config(_write(tmp_path, data), COMPATIBILITY)


def test_missing_player_cognitive_gp_fails(tmp_path: Path) -> None:
    data = _raw()
    del data["players"][2]["cognitive_parameters"]["GP-027"]
    with pytest.raises(ConfigValidationError, match="GP-024 through GP-027"):
        load_config(_write(tmp_path, data), COMPATIBILITY)


def test_player_cognitive_parameters_are_independent() -> None:
    cfg = load_config(DEFAULT)
    assert cfg.players[0].cognitive_parameters is not cfg.players[1].cognitive_parameters
    assert cfg.players[0].cognitive_parameters["GP-026"] is not cfg.players[1].cognitive_parameters["GP-026"]


def test_legacy_global_cognition_migrates_to_four_independent_players(tmp_path: Path) -> None:
    data = _raw()
    cognitive = data["players"][0].pop("cognitive_parameters")
    for item in data["players"][1:]:
        item.pop("cognitive_parameters")
    data["global_parameters"].update(cognitive)
    data["parameter_version"] = "CDMJ-AI-PARAMS 1.0.0"
    data["implementation_version"] = "CDMJ-AI-IMPL 2.0.0"
    data["global_parameters"]["GP-001"]["parameter_version"] = "CDMJ-AI-PARAMS 1.0.0"
    cfg = load_config(_write(tmp_path, data), COMPATIBILITY)
    assert cfg.parameter_version == "CDMJ-AI-PARAMS 1.1.0"
    assert all(dict(player.cognitive_parameters["GP-026"]) == dict(cfg.players[0].cognitive_parameters["GP-026"]) for player in cfg.players)
    assert len({id(player.cognitive_parameters) for player in cfg.players}) == 4


def test_traceability_has_all_60_unique_parameters() -> None:
    assert len(PARAMETER_TRACES) == 60
    assert len(TRACE_BY_ID) == 60
    assert set(TRACE_BY_ID) == {f"GP-{i:03d}" for i in range(1, 28)} | {f"RP-{i:03d}" for i in range(1, 34)}
    assert all(trace.schema_path and trace.consumer and trace.test_anchor for trace in PARAMETER_TRACES)


def test_engine_adapter_is_read_only_and_conflicts_fail() -> None:
    adapter = HumanlikeEngineAdapter(load_config(DEFAULT))
    projected = adapter.engine_config()
    assert projected.num_players == 4
    assert projected.exchange_dir == "auto_dice"
    assert adapter.require_compatible(projected) == projected
    with pytest.raises(EngineConfigConflict, match="conflicts"):
        adapter.require_compatible(EngineConfig(num_players=3))
