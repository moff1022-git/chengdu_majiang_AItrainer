"""Public-projection-only RP derivations; never accepts engine hidden truth."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from engine.hand_utils import melds_from_raw, tile_index
from engine.shanten import shanten
from engine.tile import Suit, parse_tile
from players.humanlike.belief import model_001_rule_baseline

FORBIDDEN = {"hidden_hand", "server_hand", "private_hand", "concealed_tiles", "wall_order", "rng_state"}


class PublicDerivationError(ValueError):
    pass


def _guard(value: Any) -> None:
    if isinstance(value, Mapping):
        if any(str(key).lower() in FORBIDDEN for key in value):
            raise PublicDerivationError("hidden truth is forbidden in public RP derivation")
        for item in value.values():
            _guard(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _guard(item)


def derive_public_rps(view: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    _guard(view)
    counts = [0] * 27
    for tile in _visible_tile_indices(view):
        if 0 <= tile < 27:
            counts[tile] = min(4, counts[tile] + 1)
    unseen = [4 - value for value in counts]
    wall = view.get("wall_remaining")
    wall_value = int(wall) if isinstance(wall, int) else None
    ratio = max(0.0, min(1.0, wall_value / 55.0)) if wall_value is not None else None
    phase = "unknown" if ratio is None else ("early" if ratio > .70 else "middle" if ratio > .35 else "late" if ratio > .10 else "endgame")
    active = max(1, len(view.get("active_seats") or [0, 1, 2, 3]))
    draws = None if wall_value is None else max(0, (wall_value + active - 1) // active)
    opponents = view.get("other_players") or []
    normalized_opponents = []
    for opponent in opponents:
        if not isinstance(opponent, Mapping):
            continue
        melds = [item for item in opponent.get("melds", ()) if isinstance(item, Mapping) and "tile_id" in item]
        discards = [str(item) for item in opponent.get("discard_pile", opponent.get("discards", ())) if isinstance(item, str)]
        normalized_opponents.append({**opponent, "melds": melds, "discard_pile": discards})
    model_hypotheses = list(model_001_rule_baseline(tuple(normalized_opponents)))
    hypotheses = [{**item, "ready_probability": _public_ready_probability(opponents[index])} for index, item in enumerate(model_hypotheses)]
    aggregate = 1.0
    for item in hypotheses:
        aggregate *= 1.0 - item["ready_probability"]
    risk = round(1.0 - aggregate, 8)
    waits, live_counts, live_total, probability = _wait_state(view, unseen)
    return {
        "RP-010": {"visible_counts": counts, "unseen_upper": unseen},
        "RP-018": {"wait_tiles": waits, "live_counts": live_counts, "live_total": live_total, "probability": probability, "dead_wait": bool(waits and live_total == 0)},
        "RP-019": {"hypotheses": hypotheses, "evidence_source": "public_only"},
        "RP-020": {"aggregate_risk": risk, "risk_kind": "public_estimate"},
        "RP-021": {"remaining_draws": wall_value, "self_draws_estimate": draws, "time_pressure": 0.0 if ratio is None else round(1.0-ratio,8)},
        "RP-022": {"phase": phase, "phase_strength": 0.0 if ratio is None else round(1.0-ratio,8), "wall_ratio": ratio},
    }


def _visible_tile_indices(view: Mapping[str, Any]):
    for key in ("self_hand_indices", "public_tile_indices", "discard_indices", "meld_tile_indices"):
        for value in view.get(key) or []:
            if isinstance(value, int):
                yield value


def _public_ready_probability(player: Mapping[str, Any]) -> float:
    melds = len(player.get("melds") or [])
    discards = len(player.get("discards") or [])
    return round(max(0.0, min(1.0, 0.08 * melds + 0.01 * discards)), 8)


def _wait_state(view: Mapping[str, Any], unseen: list[int]) -> tuple[list[str], list[int], int, float]:
    own = view.get("self_player")
    if not isinstance(own, Mapping) or not own.get("hand"):
        return [], [0] * 27, 0, 0.0
    hand = [parse_tile(str(value)) for value in own.get("hand", ())]
    melds = melds_from_raw([dict(item) for item in own.get("melds", ())])
    dingque = Suit(own["dingque"]) if own.get("dingque") else None
    result = shanten(hand, melds, dingque)
    waits = [tile.id for tile in result.ukeire] if result.shanten == 0 else []
    live = [0] * 27
    for tile in result.ukeire if result.shanten == 0 else ():
        idx = tile_index(tile)
        live[idx] = unseen[idx]
    total = sum(live)
    denominator = sum(unseen)
    return waits, live, total, round(total / denominator, 8) if denominator else 0.0
