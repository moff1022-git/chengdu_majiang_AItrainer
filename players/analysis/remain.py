"""Visible tile counts and remaining estimates."""

from __future__ import annotations

from collections import Counter

from engine.hand_utils import melds_from_raw
from engine.state import GameState
from engine.tile import all_tile_faces


def _all_face_ids() -> list[str]:
    return [t.id for t in all_tile_faces()]


def visible_counts_for_seat(state: GameState, seat: int) -> Counter:
    """
    Public info + self hand only (no other players' private hands).
    """
    c: Counter = Counter()
    for p in state.players:
        # self hand
        if p.seat == seat:
            for t in p.hand:
                c[t.id] += 1
        # all melds and discards public
        for t in p.discard_pile:
            c[t.id] += 1
        for m in melds_from_raw(p.melds):
            n = 4 if m.is_gang else 3
            c[m.tile.id] += n
    return c


def remain_map(state: GameState, seat: int) -> dict[str, int]:
    vis = visible_counts_for_seat(state, seat)
    out: dict[str, int] = {}
    for tid in _all_face_ids():
        out[tid] = max(0, 4 - int(vis.get(tid, 0)))
    return out


def ukeire_count(ukeire_ids: list[str], remain: dict[str, int]) -> int:
    return sum(remain.get(tid, 0) for tid in ukeire_ids)
