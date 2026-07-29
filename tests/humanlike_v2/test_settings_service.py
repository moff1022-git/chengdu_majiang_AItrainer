from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from players.humanlike.config import ConfigValidationError
from players.humanlike.settings_service import read_raw, save_raw, validate_raw
from players.humanlike.settings_window import ENUMS, RANGES, SCOPE_ENUMS, _help


ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "configs" / "humanlike_v2" / "default.json"
COMPAT = ROOT / "configs" / "humanlike_v2" / "compatibility.json"


def _target(tmp_path):
    target = tmp_path / "default.json"
    target.write_text(DEFAULT.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "compatibility.json").write_text(COMPAT.read_text(encoding="utf-8"), encoding="utf-8")
    return target


def test_validate_and_atomic_save_with_backup(tmp_path):
    target = _target(tmp_path)
    data = read_raw(target)
    data["players"][0]["profile"]["thinking_speed"] = 0.66
    config = save_raw(data, target)
    assert config.players[0].thinking_speed == 0.66
    assert target.with_suffix(".json.bak").exists()
    assert read_raw(target)["players"][0]["profile"]["thinking_speed"] == 0.66


def test_invalid_or_locked_value_is_rejected_without_write(tmp_path):
    target = _target(tmp_path)
    before = target.read_bytes()
    data = read_raw(target)
    data["global_parameters"]["GP-004"]["total_tiles"] = 109
    with pytest.raises(ConfigValidationError):
        save_raw(data, target)
    assert target.read_bytes() == before


def test_all_gp_and_profiles_are_present():
    data = read_raw(DEFAULT)
    assert set(data["global_parameters"]) == {f"GP-{i:03d}" for i in range(1, 28)}
    assert len(data["players"]) == 4
    assert validate_raw(copy.deepcopy(data), target=DEFAULT).config_hash


def test_form_metadata_has_explicit_ranges_and_all_validator_enums():
    for key in ("total_rounds", "starting_score", "forced_hu_wall_threshold", "tail_reserved", "base_score", "fan_cap", "discard_timeout_ms", "response_timeout_ms", "max_performance_delay_ms", "cross_round_history", "random_seed", "min_candidates", "max_candidates", "search_depth", "attention_capacity", "target_rank", "lead_gap", "trail_gap", "seed"):
        assert key in RANGES and "范围：" in _help(key, 1)
    for key in ("ranking", "direction", "priority_mode", "seat_priority", "pass_hu_mode", "gang_draw_source", "mode", "payers", "payment", "settlement", "multi_hu_mode", "payees", "dead_wait", "valuation", "dealer_mode", "timeout_action", "level", "style"):
        assert len(ENUMS[key]) >= 2
    assert set(SCOPE_ENUMS) == {"GP-016", "GP-019"}
