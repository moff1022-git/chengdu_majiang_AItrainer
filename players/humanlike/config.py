"""Immutable, validated F0028 humanlike-v2 configuration."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

RULE_VERSION = "CDMJ-AI-RULES 1.0.0"
PARAMETER_VERSION = "CDMJ-AI-PARAMS 1.1.0"
IMPLEMENTATION_VERSION = "CDMJ-AI-IMPL 2.1.0"
RULESET = "chengdu_xuezhan_daodi"
WEIGHT_TOLERANCE = 1e-6

GP_IDS = tuple(f"GP-{index:03d}" for index in range(1, 28))
GLOBAL_GP_IDS = GP_IDS[:23]
COGNITIVE_GP_IDS = GP_IDS[23:]
GP_FIELDS = {
    "GP-001": {"rule_version", "parameter_version", "locked"},
    "GP-002": {"ruleset", "platform_ruleset_id", "extensions"},
    "GP-003": {"total_rounds", "starting_score", "ranking", "early_end_score"},
    "GP-004": {"suits", "ranks", "copies_per_type", "tile_types", "total_tiles", "extensions"},
    "GP-005": {"enabled", "exchange_count", "same_suit_required", "direction"},
    "GP-006": {"enabled", "force_discard_missing_suit", "allow_hu_before_cleared"},
    "GP-007": {"draw", "discard", "peng", "ming_gang", "an_gang", "bu_gang", "qiang_gang_hu", "chi"},
    "GP-008": {"priority_mode", "multi_hu", "seat_priority"},
    "GP-009": {"pass_hu_mode", "discard_hu_can_pass", "self_draw_can_pass", "qiang_gang_hu_can_pass", "forced_hu_wall_threshold"},
    "GP-010": {"total_tiles", "standard_wall_after_deal", "terminal_winners", "tail_reserved", "gang_draw_source"},
    "GP-011": {"patterns"}, "GP-012": {"relations"},
    "GP-013": {"base_score", "fan_cap", "gang_outside_cap"},
    "GP-014": {"mode", "bonus_fan", "fixed_bonus", "payers"},
    "GP-015": {"ming_gang_score", "an_gang_score", "bu_gang_score", "payment", "settlement"},
    "GP-016": {"enabled", "scope", "multi_hu_mode"},
    "GP-017": {"enabled", "penalty_fan", "fixed_score", "payees"},
    "GP-018": {"enabled", "dead_wait", "valuation"},
    "GP-019": {"enabled", "scope"},
    "GP-020": {"dealer_mode", "dealer_bonus_fan", "dealer_fixed_bonus", "continuations"},
    "GP-021": {"wall_remaining", "draw_source", "exchange_source", "concealed_gang_tiles", "hu_hand", "draw_round_hand", "thinking_time", "cancel_action"},
    "GP-022": {"discard_timeout_ms", "response_timeout_ms", "max_performance_delay_ms", "timeout_action"},
    "GP-023": {"profile_count"},
    "GP-024": {"initial_strength", "forget_rate", "salience_boost", "cross_round_history", "learn_hidden_information"},
    "GP-025": {"emotional_stability", "habit_strength", "max_error_probability", "near_equal_randomness", "random_seed"},
    "GP-026": {"min_candidates", "max_candidates", "search_depth", "attention_capacity", "satisfaction_threshold", "research_threshold", "decision_weights"},
    "GP-027": {"weights", "target_rank", "lead_gap", "trail_gap"},
}


class ConfigValidationError(ValueError):
    """Raised when a humanlike-v2 configuration violates the specification."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ConfigValidationError(message)


def _number(value: Any, path: str, low: float, high: float) -> float:
    _require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{path} must be numeric")
    result = float(value)
    _require(low <= result <= high, f"{path} must be in [{low}, {high}]")
    return result


def _integer(value: Any, path: str, low: int, high: int) -> int:
    _require(isinstance(value, int) and not isinstance(value, bool), f"{path} must be an integer")
    _require(low <= value <= high, f"{path} must be in [{low}, {high}]")
    return value


def _enum(value: Any, path: str, allowed: set[str]) -> str:
    _require(isinstance(value, str) and value in allowed, f"{path} must be one of {sorted(allowed)}")
    return value


def _weights(value: Any, path: str, keys: Sequence[str]) -> None:
    _require(isinstance(value, Mapping), f"{path} must be an object")
    _require(set(value) == set(keys), f"{path} keys must be {sorted(keys)}")
    total = sum(_number(value[key], f"{path}.{key}", 0.0, 1.0) for key in keys)
    _require(abs(total - 1.0) <= WEIGHT_TOLERANCE, f"{path} weights must sum to 1 (got {total})")


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class PlayerProfile:
    player_id: int
    name: str
    level: str
    style: str
    peng_preference: float
    gang_preference: float
    big_hand_preference: float
    defense_awareness: float
    plan_persistence: float
    thinking_speed: float
    cognitive_parameters: Mapping[str, Mapping[str, Any]]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any], path: str, cognitive_parameters: Mapping[str, Any]) -> "PlayerProfile":
        expected = {
            "player_id", "name", "level", "style", "peng_preference", "gang_preference",
            "big_hand_preference", "defense_awareness", "plan_persistence", "thinking_speed",
        }
        _require(set(data) == expected, f"{path} fields must be {sorted(expected)}")
        _require(isinstance(data["name"], str) and bool(data["name"]), f"{path}.name must be non-empty")
        return cls(
            player_id=_integer(data["player_id"], f"{path}.player_id", 0, 3),
            name=data["name"],
            level=_enum(data["level"], f"{path}.level", {"novice", "normal", "skilled", "expert"}),
            style=_enum(data["style"], f"{path}.style", {"conservative", "balanced", "aggressive"}),
            peng_preference=_number(data["peng_preference"], f"{path}.peng_preference", 0, 1),
            gang_preference=_number(data["gang_preference"], f"{path}.gang_preference", 0, 1),
            big_hand_preference=_number(data["big_hand_preference"], f"{path}.big_hand_preference", 0, 1),
            defense_awareness=_number(data["defense_awareness"], f"{path}.defense_awareness", 0, 1),
            plan_persistence=_number(data["plan_persistence"], f"{path}.plan_persistence", 0, 1),
            thinking_speed=_number(data["thinking_speed"], f"{path}.thinking_speed", 0, 1),
            cognitive_parameters=_freeze(cognitive_parameters),
        )


@dataclass(frozen=True, slots=True)
class GlobalParameters:
    values: Mapping[str, Mapping[str, Any]]

    def __getitem__(self, parameter_id: str) -> Mapping[str, Any]:
        return self.values[parameter_id]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "GlobalParameters":
        _require(set(data) == set(GLOBAL_GP_IDS), "global_parameters must contain exactly GP-001 through GP-023")
        for parameter_id in GLOBAL_GP_IDS:
            _require(isinstance(data[parameter_id], Mapping), f"global_parameters.{parameter_id} must be an object")
        _validate_global_parameters(data)
        return cls(_freeze(data))


@dataclass(frozen=True, slots=True)
class HumanlikeConfig:
    rule_version: str
    parameter_version: str
    implementation_version: str
    ruleset: str
    global_parameters: GlobalParameters
    players: tuple[PlayerProfile, ...]
    seed: int
    config_hash: str

    def normalized_dict(self) -> dict[str, Any]:
        return {
            "implementation_version": self.implementation_version,
            "parameter_version": self.parameter_version,
            "players": [
                {
                    "player_id": profile.player_id,
                    "profile": {field: getattr(profile, field) for field in profile.__dataclass_fields__ if field not in {"player_id", "cognitive_parameters"}},
                    "cognitive_parameters": _thaw(profile.cognitive_parameters),
                }
                for profile in self.players
            ],
            "rule_version": self.rule_version,
            "ruleset": self.ruleset,
            "seed": self.seed,
            "global_parameters": _thaw(self.global_parameters.values),
        }


def canonical_json_bytes(data: Mapping[str, Any]) -> bytes:
    try:
        return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ConfigValidationError(f"configuration is not canonical JSON: {exc}") from exc


def _validate_global_parameters(gp: Mapping[str, Mapping[str, Any]]) -> None:
    for parameter_id in GLOBAL_GP_IDS:
        expected_fields = GP_FIELDS[parameter_id]
        _require(set(gp[parameter_id]) == expected_fields, f"{parameter_id} fields must be {sorted(expected_fields)}")
    _require(gp["GP-001"] == {"rule_version": RULE_VERSION, "parameter_version": PARAMETER_VERSION, "locked": True}, "GP-001 version lock mismatch")
    _require(gp["GP-002"].get("ruleset") == RULESET, "GP-002.ruleset mismatch")
    platform_id = gp["GP-002"].get("platform_ruleset_id")
    _require(isinstance(platform_id, str) and 1 <= len(platform_id) <= 128, "GP-002.platform_ruleset_id length must be 1..128")
    extensions = gp["GP-002"].get("extensions")
    _require(isinstance(extensions, list) and len(extensions) <= 64, "GP-002.extensions length must be 0..64")
    _integer(gp["GP-003"].get("total_rounds"), "GP-003.total_rounds", 1, 10000)
    _integer(gp["GP-003"].get("starting_score"), "GP-003.starting_score", -10**9, 10**9)
    _enum(gp["GP-003"].get("ranking"), "GP-003.ranking", {"total_score", "rank_points", "custom"})
    if gp["GP-003"].get("early_end_score") is not None:
        _integer(gp["GP-003"]["early_end_score"], "GP-003.early_end_score", -10**9, 10**9)
    _require(gp["GP-004"] == {"suits": ["wan", "tong", "tiao"], "ranks": 9, "copies_per_type": 4, "tile_types": 27, "total_tiles": 108, "extensions": []}, "GP-004 fixed deck mismatch")
    _enum(gp["GP-005"].get("direction"), "GP-005.direction", {"left", "right", "opposite", "dice", "random"})
    if gp["GP-005"].get("enabled"):
        _require(gp["GP-005"].get("exchange_count") == 3 and gp["GP-005"].get("same_suit_required") is True, "GP-005 enabled exchange must use three same-suit tiles")
    _require(gp["GP-006"].get("enabled") is True and gp["GP-006"].get("allow_hu_before_cleared") is False, "GP-006 locked dingque values mismatch")
    _require(all(isinstance(value, bool) for value in gp["GP-006"].values()), "GP-006 fields must be boolean")
    _require(gp["GP-007"].get("chi") is False, "GP-007.chi must be false")
    _require(all(isinstance(value, bool) for value in gp["GP-007"].values()), "GP-007 action switches must be boolean")
    _enum(gp["GP-008"].get("priority_mode"), "GP-008.priority_mode", {"hu_gang_peng_pass", "hu_seat_peng_gang_pass"})
    _require(isinstance(gp["GP-008"].get("multi_hu"), bool), "GP-008.multi_hu must be boolean")
    _enum(gp["GP-008"].get("seat_priority"), "GP-008.seat_priority", {"nearest_from_discarder", "platform_deterministic"})
    _enum(gp["GP-009"].get("pass_hu_mode"), "GP-009.pass_hu_mode", {"none", "until_self_draw", "until_value_increase", "platform_custom"})
    _require(all(isinstance(gp["GP-009"].get(key), bool) for key in ("discard_hu_can_pass", "self_draw_can_pass", "qiang_gang_hu_can_pass")), "GP-009 pass switches must be boolean")
    _integer(gp["GP-009"].get("forced_hu_wall_threshold"), "GP-009.forced_hu_wall_threshold", 0, 4)
    _require(gp["GP-010"].get("total_tiles") == 108 and gp["GP-010"].get("standard_wall_after_deal") == 55 and gp["GP-010"].get("terminal_winners") == 3, "GP-010 locked wall values mismatch")
    _integer(gp["GP-010"].get("tail_reserved"), "GP-010.tail_reserved", 0, 16)
    _enum(gp["GP-010"].get("gang_draw_source"), "GP-010.gang_draw_source", {"wall_tail", "platform_position"})
    patterns = gp["GP-011"].get("patterns")
    _require(isinstance(patterns, list) and 1 <= len(patterns) <= 128, "GP-011.patterns length must be 1..128")
    pattern_ids = [item.get("id") for item in patterns if isinstance(item, Mapping)]
    _require(len(pattern_ids) == len(patterns) and len(pattern_ids) == len(set(pattern_ids)), "GP-011 pattern ids must be unique")
    _require(all(isinstance(item.get("id"), str) and 1 <= len(item["id"]) <= 64 and isinstance(item.get("enabled"), bool) and set(item) == {"id", "enabled"} for item in patterns), "GP-011 patterns must have id/enabled fields")
    _require(isinstance(gp["GP-012"].get("relations"), list), "GP-012.relations must be an array")
    _integer(gp["GP-013"].get("base_score"), "GP-013.base_score", 1, 1_000_000)
    _integer(gp["GP-013"].get("fan_cap"), "GP-013.fan_cap", 0, 64)
    _require(isinstance(gp["GP-013"].get("gang_outside_cap"), bool), "GP-013.gang_outside_cap must be boolean")
    _enum(gp["GP-014"].get("mode"), "GP-014.mode", {"add_base", "add_fan", "fixed_bonus", "none"})
    _integer(gp["GP-014"].get("bonus_fan"), "GP-014.bonus_fan", 0, 16)
    _integer(gp["GP-014"].get("fixed_bonus"), "GP-014.fixed_bonus", 0, 1_000_000)
    _enum(gp["GP-014"].get("payers"), "GP-014.payers", {"all_active_opponents", "platform_set"})
    for key in ("ming_gang_score", "an_gang_score", "bu_gang_score"):
        _integer(gp["GP-015"].get(key), f"GP-015.{key}", 0, 1_000_000)
    _enum(gp["GP-015"].get("payment"), "GP-015.payment", {"discarder_only", "all_active_opponents", "custom"})
    _enum(gp["GP-015"].get("settlement"), "GP-015.settlement", {"immediate", "round_end"})
    _require(isinstance(gp["GP-016"].get("enabled"), bool), "GP-016.enabled must be boolean")
    _enum(gp["GP-016"].get("scope"), "GP-016.scope", {"latest_gang_only", "all_related_gang_score", "custom"})
    _enum(gp["GP-016"].get("multi_hu_mode"), "GP-016.multi_hu_mode", {"copy_to_each_winner", "split", "custom"})
    _require(isinstance(gp["GP-017"].get("enabled"), bool), "GP-017.enabled must be boolean")
    _integer(gp["GP-017"].get("penalty_fan"), "GP-017.penalty_fan", 0, 64)
    _integer(gp["GP-017"].get("fixed_score"), "GP-017.fixed_score", 0, 1_000_000)
    _enum(gp["GP-017"].get("payees"), "GP-017.payees", {"all_non_hu_non_huazhu", "all_eligible", "custom"})
    _require(isinstance(gp["GP-018"].get("enabled"), bool), "GP-018.enabled must be boolean")
    _enum(gp["GP-018"].get("dead_wait"), "GP-018.dead_wait", {"valid", "invalid"})
    _enum(gp["GP-018"].get("valuation"), "GP-018.valuation", {"actual_live_wait", "maximum_possible_fan", "custom"})
    _require(isinstance(gp["GP-019"].get("enabled"), bool), "GP-019.enabled must be boolean")
    _enum(gp["GP-019"].get("scope"), "GP-019.scope", {"all_gang_income", "untransferred_gang_income", "selected_events", "custom"})
    _enum(gp["GP-020"].get("dealer_mode"), "GP-020.dealer_mode", {"dice", "rotate", "winner", "custom"})
    _integer(gp["GP-020"].get("dealer_bonus_fan"), "GP-020.dealer_bonus_fan", 0, 16)
    _integer(gp["GP-020"].get("dealer_fixed_bonus"), "GP-020.dealer_fixed_bonus", 0, 1_000_000)
    _integer(gp["GP-020"].get("continuations"), "GP-020.continuations", 0, 10000)
    visibility = gp["GP-021"]
    _require(visibility and all(value in {"hidden", "public_exact", "public_partial"} for value in visibility.values()), "GP-021 visibility values invalid")
    discard_timeout = _integer(gp["GP-022"].get("discard_timeout_ms"), "GP-022.discard_timeout_ms", 250, 600000)
    _integer(gp["GP-022"].get("response_timeout_ms"), "GP-022.response_timeout_ms", 250, 600000)
    _integer(gp["GP-022"].get("max_performance_delay_ms"), "GP-022.max_performance_delay_ms", 0, int(discard_timeout * 0.8))
    _enum(gp["GP-022"].get("timeout_action"), "GP-022.timeout_action", {"auto_pass", "auto_hu", "safe_discard", "platform_default"})
    _require(gp["GP-023"].get("profile_count") == 4, "GP-023.profile_count must be 4")
def _validate_cognitive_parameters(gp: Mapping[str, Mapping[str, Any]], path: str) -> None:
    _require(set(gp) == set(COGNITIVE_GP_IDS), f"{path} must contain exactly GP-024 through GP-027")
    for parameter_id in COGNITIVE_GP_IDS:
        _require(set(gp[parameter_id]) == GP_FIELDS[parameter_id], f"{path}.{parameter_id} fields mismatch")
    for key in ("initial_strength", "forget_rate", "salience_boost"):
        _number(gp["GP-024"].get(key), f"GP-024.{key}", 0, 1)
    _require(gp["GP-024"].get("learn_hidden_information") is False, "GP-024.learn_hidden_information must be false")
    _integer(gp["GP-024"].get("cross_round_history"), "GP-024.cross_round_history", 0, 10000)
    for key in ("emotional_stability", "habit_strength", "max_error_probability", "near_equal_randomness"):
        _number(gp["GP-025"].get(key), f"GP-025.{key}", 0, 1)
    _integer(gp["GP-025"].get("random_seed"), "GP-025.random_seed", 0, 2**64 - 1)
    cognition = gp["GP-026"]
    minimum = _integer(cognition.get("min_candidates"), "GP-026.min_candidates", 1, 14)
    maximum = _integer(cognition.get("max_candidates"), "GP-026.max_candidates", 1, 14)
    _require(minimum <= maximum, "GP-026 min_candidates must not exceed max_candidates")
    _integer(cognition.get("search_depth"), "GP-026.search_depth", 0, 8)
    _integer(cognition.get("attention_capacity"), "GP-026.attention_capacity", 1, 64)
    for key in ("satisfaction_threshold", "research_threshold"):
        _number(cognition.get(key), f"GP-026.{key}", 0, 1)
    _weights(cognition.get("decision_weights"), "GP-026.decision_weights", ("speed", "hand_value", "defense", "flexibility"))
    objective = gp["GP-027"]
    _weights(objective.get("weights"), "GP-027.weights", ("round_score", "match_score", "rank", "risk", "stability"))
    _integer(objective.get("target_rank"), "GP-027.target_rank", 1, 4)
    _integer(objective.get("lead_gap"), "GP-027.lead_gap", 0, 10**9)
    _integer(objective.get("trail_gap"), "GP-027.trail_gap", 0, 10**9)


def _load_compatibility(path: Path) -> set[tuple[str, str, str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigValidationError(f"cannot load compatibility file {path}: {exc}") from exc
    combinations = raw.get("supported") if isinstance(raw, Mapping) else None
    _require(isinstance(combinations, list), "compatibility.supported must be an array")
    return {(item["rule_version"], item["parameter_version"], item["implementation_version"]) for item in combinations}


def load_config(path: str | Path, compatibility_path: str | Path | None = None) -> HumanlikeConfig:
    source = Path(path)
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigValidationError(f"cannot load configuration {source}: {exc}") from exc
    _require(isinstance(raw, Mapping), "configuration root must be an object")
    required = {"rule_version", "parameter_version", "implementation_version", "ruleset", "global_parameters", "players", "seed"}
    _require(set(raw) == required, f"configuration root fields must be {sorted(required)}")
    versions = (raw["rule_version"], raw["parameter_version"], raw["implementation_version"])
    compatibility = Path(compatibility_path) if compatibility_path else source.with_name("compatibility.json")
    _require(versions in _load_compatibility(compatibility), f"unsupported RULES/PARAMS/IMPL combination: {versions}")
    raw = json.loads(json.dumps(raw))
    if versions[1:] == ("CDMJ-AI-PARAMS 1.0.0", "CDMJ-AI-IMPL 2.0.0"):
        legacy = {key: raw["global_parameters"].pop(key) for key in COGNITIVE_GP_IDS}
        for item in raw["players"]:
            item["cognitive_parameters"] = json.loads(json.dumps(legacy))
        raw["parameter_version"] = PARAMETER_VERSION
        raw["implementation_version"] = IMPLEMENTATION_VERSION
        raw["global_parameters"]["GP-001"]["parameter_version"] = PARAMETER_VERSION
        versions = (raw["rule_version"], raw["parameter_version"], raw["implementation_version"])
    _require(raw["ruleset"] == RULESET, f"ruleset must be {RULESET}")
    global_parameters = GlobalParameters.from_dict(raw["global_parameters"])
    _require(isinstance(raw["players"], list) and len(raw["players"]) == 4, "players must contain exactly four profiles")
    players_list = []
    for index, item in enumerate(raw["players"]):
        _require(set(item) == {"player_id", "profile", "cognitive_parameters"}, f"players[{index}] fields invalid")
        _validate_cognitive_parameters(item["cognitive_parameters"], f"players[{index}].cognitive_parameters")
        players_list.append(PlayerProfile.from_dict(item["profile"] | {"player_id": item["player_id"]}, f"players[{index}]", item["cognitive_parameters"]))
    players = tuple(players_list)
    _require(tuple(profile.player_id for profile in players) == (0, 1, 2, 3), "player ids must be exactly 0,1,2,3 in seat order")
    seed = _integer(raw["seed"], "seed", 0, 2**64 - 1)
    provisional = HumanlikeConfig(versions[0], versions[1], versions[2], raw["ruleset"], global_parameters, players, seed, "")
    digest = hashlib.sha256(canonical_json_bytes(provisional.normalized_dict())).hexdigest()
    return HumanlikeConfig(
        rule_version=provisional.rule_version,
        parameter_version=provisional.parameter_version,
        implementation_version=provisional.implementation_version,
        ruleset=provisional.ruleset,
        global_parameters=provisional.global_parameters,
        players=provisional.players,
        seed=provisional.seed,
        config_hash=digest,
    )
