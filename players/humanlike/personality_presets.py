"""Immutable F0037 personality presets over existing profile/GP-025/GP-026 fields."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping


LEVEL_PRESETS: Mapping[str, Mapping[str, Any]] = {
    "novice": {"min_candidates": 2, "max_candidates": 6, "search_depth": 1, "attention_capacity": 8, "satisfaction_threshold": 0.62, "max_error_probability": 0.060, "near_equal_randomness": 0.12},
    "normal": {"min_candidates": 3, "max_candidates": 8, "search_depth": 2, "attention_capacity": 12, "satisfaction_threshold": 0.72, "max_error_probability": 0.040, "near_equal_randomness": 0.08},
    "skilled": {"min_candidates": 4, "max_candidates": 10, "search_depth": 3, "attention_capacity": 16, "satisfaction_threshold": 0.77, "max_error_probability": 0.025, "near_equal_randomness": 0.05},
    "expert": {"min_candidates": 5, "max_candidates": 12, "search_depth": 4, "attention_capacity": 20, "satisfaction_threshold": 0.82, "max_error_probability": 0.015, "near_equal_randomness": 0.03},
}

STYLE_PRESETS: Mapping[str, Mapping[str, Any]] = {
    "conservative": {"peng_preference": 0.35, "gang_preference": 0.30, "big_hand_preference": 0.25, "defense_awareness": 0.80, "plan_persistence": 0.70, "thinking_speed": 0.50, "emotional_stability": 0.85, "habit_strength": 0.65, "decision_weights": {"speed": 0.25, "hand_value": 0.20, "defense": 0.40, "flexibility": 0.15}},
    "balanced": {"peng_preference": 0.50, "gang_preference": 0.50, "big_hand_preference": 0.45, "defense_awareness": 0.55, "plan_persistence": 0.55, "thinking_speed": 0.55, "emotional_stability": 0.70, "habit_strength": 0.55, "decision_weights": {"speed": 0.35, "hand_value": 0.25, "defense": 0.25, "flexibility": 0.15}},
    "aggressive": {"peng_preference": 0.70, "gang_preference": 0.75, "big_hand_preference": 0.75, "defense_awareness": 0.35, "plan_persistence": 0.45, "thinking_speed": 0.65, "emotional_stability": 0.55, "habit_strength": 0.45, "decision_weights": {"speed": 0.40, "hand_value": 0.35, "defense": 0.10, "flexibility": 0.15}},
}

NONHUMAN_PRESET = {
    "min_candidates": 14, "max_candidates": 14, "search_depth": 8,
    "attention_capacity": 64, "satisfaction_threshold": 1.0,
    "max_error_probability": 0.0, "near_equal_randomness": 0.0,
    "peng_preference": 0.70, "gang_preference": 0.85,
    "big_hand_preference": 0.80, "defense_awareness": 0.45,
    "plan_persistence": 0.05, "thinking_speed": 1.0,
    "emotional_stability": 1.0, "habit_strength": 0.0,
    "decision_weights": {"speed": 0.20, "hand_value": 0.45, "defense": 0.25, "flexibility": 0.10},
}

PRESET_IDS = tuple(f"{level}_{style}" for level in LEVEL_PRESETS for style in STYLE_PRESETS) + ("nonhuman_optimized",)


@dataclass(frozen=True, slots=True)
class PresetDiff:
    path: str
    before: Any
    after: Any


def _preset_values(preset_id: str) -> tuple[str, str, Mapping[str, Any], Mapping[str, Any]]:
    if preset_id not in PRESET_IDS:
        raise ValueError(f"unknown personality preset: {preset_id}")
    if preset_id == "nonhuman_optimized":
        return "expert", "nonhuman_optimized", NONHUMAN_PRESET, NONHUMAN_PRESET
    level, style = preset_id.split("_", 1)
    return level, style, LEVEL_PRESETS[level], STYLE_PRESETS[style]


def apply_personality_preset(player: Mapping[str, Any], preset_id: str) -> dict[str, Any]:
    level, style, level_values, style_values = _preset_values(preset_id)
    result = deepcopy(dict(player))
    profile = result["profile"]
    gp025 = result["cognitive_parameters"]["GP-025"]
    gp026 = result["cognitive_parameters"]["GP-026"]
    profile["level"] = level
    profile["style"] = style
    if preset_id == "nonhuman_optimized":
        for key in ("peng_preference", "gang_preference", "big_hand_preference", "defense_awareness", "plan_persistence", "thinking_speed"):
            profile[key] = NONHUMAN_PRESET[key]
        for key in ("emotional_stability", "habit_strength", "max_error_probability", "near_equal_randomness"):
            gp025[key] = NONHUMAN_PRESET[key]
        for key in ("min_candidates", "max_candidates", "search_depth", "attention_capacity", "satisfaction_threshold"):
            gp026[key] = NONHUMAN_PRESET[key]
        gp026["decision_weights"] = deepcopy(NONHUMAN_PRESET["decision_weights"])
        # Keep schema enums valid; the preset identity is carried by preset_id.
        profile["level"], profile["style"] = "expert", "aggressive"
        return result
    for key in ("peng_preference", "gang_preference", "big_hand_preference", "defense_awareness", "plan_persistence", "thinking_speed"):
        profile[key] = style_values[key]
    for key in ("emotional_stability", "habit_strength"):
        gp025[key] = style_values[key]
    for key in ("max_error_probability", "near_equal_randomness"):
        gp025[key] = level_values[key]
    for key in ("min_candidates", "max_candidates", "search_depth", "attention_capacity", "satisfaction_threshold"):
        gp026[key] = level_values[key]
    gp026["decision_weights"] = deepcopy(style_values["decision_weights"])
    return result


def detect_personality_preset(player: Mapping[str, Any]) -> str:
    for preset_id in PRESET_IDS:
        expected = apply_personality_preset(player, preset_id)
        if _controlled_values(expected) == _controlled_values(player):
            return preset_id
    return "custom"


def personality_preset_diff(player: Mapping[str, Any], preset_id: str) -> tuple[PresetDiff, ...]:
    target = apply_personality_preset(player, preset_id)
    before = _controlled_values(player)
    after = _controlled_values(target)
    return tuple(PresetDiff(path, before[path], value) for path, value in after.items() if before[path] != value)


def _controlled_values(player: Mapping[str, Any]) -> dict[str, Any]:
    profile = player["profile"]
    gp025 = player["cognitive_parameters"]["GP-025"]
    gp026 = player["cognitive_parameters"]["GP-026"]
    paths = {
        "profile.level": profile["level"], "profile.style": profile["style"],
        **{f"profile.{key}": profile[key] for key in ("peng_preference", "gang_preference", "big_hand_preference", "defense_awareness", "plan_persistence", "thinking_speed")},
        **{f"GP-025.{key}": gp025[key] for key in ("emotional_stability", "habit_strength", "max_error_probability", "near_equal_randomness")},
        **{f"GP-026.{key}": gp026[key] for key in ("min_candidates", "max_candidates", "search_depth", "attention_capacity", "satisfaction_threshold")},
        "GP-026.decision_weights": gp026["decision_weights"],
    }
    return paths


def effective_search_depth(level: str, configured: int) -> int:
    if level not in LEVEL_PRESETS:
        raise ValueError(f"unknown personality level: {level}")
    return min(int(configured), int(LEVEL_PRESETS[level]["search_depth"]))
