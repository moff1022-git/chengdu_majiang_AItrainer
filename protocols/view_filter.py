"""Legacy-compatible API backed by the PlayerView v2 whitelist builder."""

from __future__ import annotations

from typing import Any

from engine.state import GameState
from protocols.messages import Observation
from protocols.player_view_builder import PlayerViewBuilder


def filter_state_for_seat(state: GameState, seat: int) -> dict[str, Any]:
    return PlayerViewBuilder().build_legacy_dict(state, seat)


def build_observation(
    state: GameState,
    seat: int,
    *,
    discard_seq: int | None = None,
) -> Observation:
    view = filter_state_for_seat(state, seat)
    if discard_seq is not None:
        view["discard_seq"] = int(discard_seq)
    return Observation(game_id=state.game_id, self_seat=seat, phase=state.phase, view=view)
