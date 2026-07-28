from __future__ import annotations

import json
from pathlib import Path

import pytest

from players.humanlike.config import ConfigValidationError, GP_IDS, load_config
from players.humanlike.traceability import PARAMETER_TRACES, TRACE_BY_ID

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
    assert tuple(first.global_parameters.values) == GP_IDS
    assert tuple(profile.player_id for profile in first.players) == (0, 1, 2, 3)
    assert len(first.config_hash) == 64
    assert first.config_hash == second.config_hash
    with pytest.raises(TypeError):
        first.global_parameters.values["GP-001"] = {}  # type: ignore[index]


def test_hash_ignores_json_format_and_key_order(tmp_path: Path) -> None:
    data = _raw()
    reordered = {key: data[key] for key in reversed(data)}
    assert load_config(_write(tmp_path, reordered), COMPATIBILITY).config_hash == load_config(DEFAULT).config_hash


@pytest.mark.parametrize("missing", ["GP-001", "GP-014", "GP-027"])
def test_missing_gp_fails(tmp_path: Path, missing: str) -> None:
    data = _raw()
    del data["global_parameters"][missing]
    with pytest.raises(ConfigValidationError, match="exactly GP-001 through GP-027"):
        load_config(_write(tmp_path, data), COMPATIBILITY)


def test_unknown_version_fails(tmp_path: Path) -> None:
    data = _raw()
    data["implementation_version"] = "CDMJ-AI-IMPL 9.9.9"
    with pytest.raises(ConfigValidationError, match="unsupported"):
        load_config(_write(tmp_path, data), COMPATIBILITY)


def test_invalid_range_fails(tmp_path: Path) -> None:
    data = _raw()
    data["global_parameters"]["GP-026"]["search_depth"] = 9
    with pytest.raises(ConfigValidationError, match="search_depth"):
        load_config(_write(tmp_path, data), COMPATIBILITY)


def test_non_normalized_weights_fail(tmp_path: Path) -> None:
    data = _raw()
    data["global_parameters"]["GP-027"]["weights"]["risk"] = 0.5
    with pytest.raises(ConfigValidationError, match="sum to 1"):
        load_config(_write(tmp_path, data), COMPATIBILITY)


def test_traceability_has_all_60_unique_parameters() -> None:
    assert len(PARAMETER_TRACES) == 60
    assert len(TRACE_BY_ID) == 60
    assert set(TRACE_BY_ID) == {f"GP-{i:03d}" for i in range(1, 28)} | {f"RP-{i:03d}" for i in range(1, 34)}
    assert all(trace.schema_path and trace.consumer and trace.test_anchor for trace in PARAMETER_TRACES)
