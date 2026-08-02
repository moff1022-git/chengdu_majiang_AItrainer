"""Heuristic opponent tenpai / wait model."""

from __future__ import annotations

from engine.hand_utils import melds_from_raw
from engine.state import GameState
from players.analysis.types import OpponentHint


def estimate_opponents(state: GameState, self_seat: int) -> list[OpponentHint]:
    # late game if wall small
    late = 1.0 if len(state.wall) < 30 else 0.0
    mid = 1.0 if len(state.wall) < 50 else 0.0
    hints: list[OpponentHint] = []
    for p in state.players:
        if p.seat == self_seat or p.status != "active":
            continue
        n_melds = len(melds_from_raw(p.melds))
        n_disc = len(p.discard_pile)
        prob = min(
            1.0,
            0.12 * n_melds + 0.015 * n_disc + 0.25 * late + 0.1 * mid,
        )
        # crude waits: last few non-dingque discards' "neighbors" not used;
        # use empty or tiles near recent discards by suit
        likely: list[str] = []
        for t in p.discard_pile[-3:]:
            # suggest same suit middle ranks as weak signal inversion
            if t.rank >= 2:
                likely.append(f"{t.suit.value}_{t.rank - 1}")
            if t.rank <= 8:
                likely.append(f"{t.suit.value}_{t.rank + 1}")
        # unique preserve order
        seen = set()
        waits = []
        for tid in likely:
            if tid not in seen:
                seen.add(tid)
                waits.append(tid)
            if len(waits) >= 5:
                break
        level = "active" if prob >= 0.5 else "unknown"
        hints.append(
            OpponentHint(
                seat=p.seat,
                tenpai_prob=round(prob, 3),
                tenpai_level=level,
                likely_waits=waits,
            )
        )
    return hints
