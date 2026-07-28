"""M06 — observation view filter privacy."""

from __future__ import annotations

from engine.session import build_ready_game
from protocols.view_filter import filter_state_for_seat


def test_p01_hides_opponent_hands() -> None:
    state = build_ready_game("m06-vf", num_players=4)
    view = filter_state_for_seat(state, 0)
    assert "wall" not in view
    assert "wall_remaining" in view
    for p in view["players"]:
        if p["seat"] == 0:
            assert "hand" in p
            assert len(p["hand"]) == p["hand_count"]
        else:
            assert "hand" not in p
            assert p["hand_count"] in (13, 14)
