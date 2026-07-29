from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from players.humanlike.config import ConfigValidationError
from players.humanlike.settings_service import read_raw, save_raw, validate_raw


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

