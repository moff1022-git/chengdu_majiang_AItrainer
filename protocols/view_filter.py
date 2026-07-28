"""Seat-perspective state filtering for observations."""

from __future__ import annotations

import copy
from typing import Any

from engine.state import GameState
from protocols.messages import Observation


def filter_state_for_seat(state: GameState, seat: int) -> dict[str, Any]:
    """
    Build a JSON-compatible view: own hand full; others hand_count only;
    wall only remaining count.
    """
    raw = state.to_dict()
    view = copy.deepcopy(raw)

    # Wall: hide tile list
    wall = view.get("wall") or []
    view["wall_remaining"] = len(wall)
    view.pop("wall", None)

    # Players
    for p in view.get("players") or []:
        p_seat = int(p.get("seat", -1))
        if p_seat == seat:
            p["hand_count"] = len(p.get("hand") or [])
            # keep hand
        else:
            hand = p.pop("hand", None) or []
            p["hand_count"] = len(hand)
            # never expose hand tiles

    # pending_exchange: only own tiles; others submitted flag
    pe = view.get("pending_exchange")
    if pe is not None:
        filtered: dict[str, Any] = {}
        submitted = {}
        for k, tiles in (pe or {}).items():
            sk = str(k)
            submitted[sk] = tiles is not None and len(tiles) > 0
            if int(k) == seat:
                filtered[sk] = tiles
        view["pending_exchange"] = filtered
        view["exchange_submitted"] = submitted

    # Hide other seats' pending claims action details? public ok for training
    # Keep last_discard public
    return view


def build_observation(
    state: GameState,
    seat: int,
    *,
    include_oracle_hands: bool = False,
    discard_seq: int | None = None,
) -> Observation:
    view = filter_state_for_seat(state, seat)
    if discard_seq is not None:
        view["discard_seq"] = int(discard_seq)
    if include_oracle_hands:
        # Training-only ground truth for accuracy metrics (not for prediction).
        oracle: dict[str, list[str]] = {}
        for p in state.players:
            if p.seat == seat:
                continue
            oracle[str(p.seat)] = [t.id for t in p.hand]
        view["oracle_hands"] = oracle
    return Observation(
        game_id=state.game_id,
        self_seat=seat,
        phase=state.phase,
        view=view,
    )
