"""M10 — crash policy tests."""

from __future__ import annotations

import pytest

from engine.action import Action, ActionType
from engine.crash import AbortGame, CrashConfig, CrashHandler, CrashPolicy
from engine.session import build_ready_game
from engine.blood_battle import start_play
from engine.legal import legal_actions
from players.random_player import RandomPlayer
from protocols.messages import ActionRequest, Decision
from engine.tile import Suit, Tile


class BoomPlayer(RandomPlayer):
    def decide(self, request: ActionRequest) -> Decision:
        raise RuntimeError("boom")


def test_c01_force_pass() -> None:
    state = build_ready_game("m10-fp", num_players=2)
    start_play(state)
    seat = state.current_seat
    legal = legal_actions(state, seat)
    req = ActionRequest.create(seat, "discard", legal)
    h = CrashHandler(CrashConfig(policy=CrashPolicy.FORCE_PASS))
    players = [RandomPlayer(seed=1), RandomPlayer(seed=2)]
    for i, p in enumerate(players):
        p.on_join(i, {})
    dec = h.handle(state, seat, RuntimeError("x"), req, legal, players)
    assert action_in_legal_safe(dec.action, legal)
    assert "force" in dec.reason


def action_in_legal_safe(action, legal) -> bool:
    from engine.legal import action_in_legal

    return action_in_legal(action, legal)


def test_c02_replace_player() -> None:
    state = build_ready_game("m10-rep", num_players=2)
    start_play(state)
    seat = 0
    legal = legal_actions(state, seat) or [Action(ActionType.PASS)]
    req = ActionRequest.create(seat, state.phase, legal)
    players: list = [BoomPlayer(seed=1), RandomPlayer(seed=2)]
    for i, p in enumerate(players):
        p.on_join(i, {})
    h = CrashHandler(
        CrashConfig(policy=CrashPolicy.REPLACE_PLAYER, fallback_player="random")
    )
    dec = h.handle(state, seat, RuntimeError("boom"), req, legal, players)
    assert not isinstance(players[0], BoomPlayer)
    assert action_in_legal_safe(dec.action, legal) or dec.action.type in (
        ActionType.PASS,
        ActionType.DISCARD,
    )


def test_c03_abort() -> None:
    state = build_ready_game("m10-ab", num_players=2)
    start_play(state)
    seat = 0
    legal = legal_actions(state, seat) or [Action(ActionType.PASS)]
    req = ActionRequest.create(seat, "discard", legal)
    players = [RandomPlayer(seed=1), RandomPlayer(seed=2)]
    h = CrashHandler(CrashConfig(policy=CrashPolicy.ABORT_RESTART))
    with pytest.raises(AbortGame):
        h.handle(state, seat, RuntimeError("x"), req, legal, players)
    assert len(h.crash_log) == 1


def test_illegal_force() -> None:
    state = build_ready_game("m10-ill", num_players=2)
    start_play(state)
    seat = state.current_seat
    legal = legal_actions(state, seat)
    req = ActionRequest.create(seat, "discard", legal)
    bad = Decision(
        request_id=req.request_id,
        action=Action(ActionType.PASS),
        reason="bad",
    )
    h = CrashHandler(CrashConfig())
    dec = h.handle_illegal(state, seat, req, legal, bad)
    assert action_in_legal_safe(dec.action, legal)
