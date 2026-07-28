"""Discard deal-in danger heuristics."""

from __future__ import annotations

from engine.state import GameState
from engine.tile import Tile
from players.analysis.types import OpponentHint

_LEVELS = ("critical", "high", "medium", "low", "safe", "unknown")

DANGER_PENALTY = {
    "critical": 3.0,
    "high": 2.0,
    "medium": 1.0,
    "low": 0.3,
    "safe": 0.0,
    "unknown": 0.5,
}


def _all_discards(state: GameState) -> set[str]:
    s: set[str] = set()
    for p in state.players:
        for t in p.discard_pile:
            s.add(t.id)
    return s


def rate_discard_danger(
    tile_id: str,
    state: GameState,
    opponents: list[OpponentHint],
    *,
    f0010_ctx=None,
) -> str:
    """A1: optional F0010-weighted waits via f0010_ctx (F0011)."""
    if f0010_ctx is not None:
        from players.analysis.integrated_discard import rate_danger_f0011

        return rate_danger_f0011(tile_id, f0010_ctx, opponents)

    disc = _all_discards(state)
    in_disc = tile_id in disc

    # critical/high if matches high-tenpai opponent waits
    max_prob = 0.0
    in_wait = False
    for op in opponents:
        if tile_id in op.likely_waits:
            in_wait = True
            max_prob = max(max_prob, op.tenpai_prob)
        else:
            max_prob = max(max_prob, op.tenpai_prob * 0.3)

    if in_wait and max_prob >= 0.6:
        return "critical"
    if in_wait and max_prob >= 0.4:
        return "high"
    if max_prob >= 0.55 and not in_disc:
        return "medium"
    if in_disc:
        return "safe" if max_prob < 0.35 else "low"
    if max_prob < 0.25:
        return "low"
    return "unknown"


def danger_map_for_tiles(
    tile_ids: list[str],
    state: GameState,
    opponents: list[OpponentHint],
    *,
    f0010_ctx=None,
) -> dict[str, str]:
    return {
        tid: rate_discard_danger(
            tid, state, opponents, f0010_ctx=f0010_ctx
        )
        for tid in tile_ids
    }
