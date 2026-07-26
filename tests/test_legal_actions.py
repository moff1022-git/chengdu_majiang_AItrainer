"""M04 — legal actions unit tests."""

from __future__ import annotations

from engine.action import ActionType
from engine.blood_battle import start_play
from engine.legal import legal_actions
from engine.session import build_ready_game


def test_l01_discard_phase_has_discards() -> None:
    state = build_ready_game("m04-l01", num_players=4)
    start_play(state)
    seat = state.current_seat
    acts = legal_actions(state, seat)
    assert any(a.type == ActionType.DISCARD for a in acts)
    # non-current has no discard actions
    other = (seat + 1) % 4
    assert legal_actions(state, other) == []


def test_response_has_pass() -> None:
    state = build_ready_game("m04-l02", num_players=2)
    start_play(state)
    seat = state.current_seat
    from engine.blood_battle import apply_action
    from engine.action import Action

    disc = next(
        a for a in legal_actions(state, seat) if a.type == ActionType.DISCARD
    )
    apply_action(state, seat, disc)
    other = 1 - seat
    acts = legal_actions(state, other)
    assert any(a.type == ActionType.PASS for a in acts)
