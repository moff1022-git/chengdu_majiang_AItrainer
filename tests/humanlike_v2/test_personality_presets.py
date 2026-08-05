from __future__ import annotations

from copy import deepcopy

from players.humanlike.config import load_config
from players.humanlike.personality_presets import (
    LEVEL_PRESETS,
    PRESET_IDS,
    STYLE_PRESETS,
    apply_personality_preset,
    detect_personality_preset,
    effective_search_depth,
    personality_preset_diff,
)
from players.humanlike.player import default_humanlike_config_path


def _raw_player() -> dict:
    config = load_config(default_humanlike_config_path()).normalized_dict()
    return deepcopy(config["players"][0])


def test_all_twelve_presets_apply_and_detect() -> None:
    assert len(PRESET_IDS) == 13
    player = _raw_player()
    for preset_id in PRESET_IDS:
        updated = apply_personality_preset(player, preset_id)
        assert detect_personality_preset(updated) == preset_id
        assert abs(sum(updated["cognitive_parameters"]["GP-026"]["decision_weights"].values()) - 1.0) < 1e-9


def test_apply_preserves_fields_outside_personality_contract() -> None:
    player = _raw_player()
    updated = apply_personality_preset(player, "expert_aggressive")
    assert updated["player_id"] == player["player_id"]
    assert updated["profile"]["name"] == player["profile"]["name"]
    assert updated["cognitive_parameters"]["GP-024"] == player["cognitive_parameters"]["GP-024"]
    assert updated["cognitive_parameters"]["GP-027"] == player["cognitive_parameters"]["GP-027"]
    assert updated["cognitive_parameters"]["GP-025"]["random_seed"] == player["cognitive_parameters"]["GP-025"]["random_seed"]


def test_manual_override_is_custom_and_diff_is_bounded() -> None:
    player = apply_personality_preset(_raw_player(), "normal_balanced")
    player["profile"]["peng_preference"] = 0.51
    assert detect_personality_preset(player) == "custom"
    diffs = personality_preset_diff(player, "normal_balanced")
    assert [(item.path, item.before, item.after) for item in diffs] == [("profile.peng_preference", 0.51, 0.5)]


def test_level_and_style_presets_are_monotonic() -> None:
    levels = list(LEVEL_PRESETS.values())
    assert [item["search_depth"] for item in levels] == sorted(item["search_depth"] for item in levels)
    assert [item["attention_capacity"] for item in levels] == sorted(item["attention_capacity"] for item in levels)
    assert [item["max_error_probability"] for item in levels] == sorted((item["max_error_probability"] for item in levels), reverse=True)
    styles = list(STYLE_PRESETS.values())
    assert [item["peng_preference"] for item in styles] == sorted(item["peng_preference"] for item in styles)
    assert [item["gang_preference"] for item in styles] == sorted(item["gang_preference"] for item in styles)
    assert [item["defense_awareness"] for item in styles] == sorted((item["defense_awareness"] for item in styles), reverse=True)


def test_effective_search_depth_uses_level_cap() -> None:
    assert effective_search_depth("novice", 8) == 1
    assert effective_search_depth("normal", 8) == 2
    assert effective_search_depth("skilled", 2) == 2
    assert effective_search_depth("expert", 8) == 4
    assert effective_search_depth("expert", 8, preset_id="nonhuman_optimized") == 8


def test_nonhuman_optimized_uses_promoted_multidataset_stack() -> None:
    player = apply_personality_preset(_raw_player(), "nonhuman_optimized")
    assert player["profile"]["gang_preference"] == 0.50
    assert player["cognitive_parameters"]["GP-026"]["decision_weights"] == {
        "speed": 0.40,
        "hand_value": 0.20,
        "defense": 0.25,
        "flexibility": 0.15,
    }
    assert detect_personality_preset(player) == "nonhuman_optimized"
