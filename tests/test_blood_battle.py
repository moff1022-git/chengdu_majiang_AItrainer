"""M04 — blood battle play loop tests."""

from __future__ import annotations

import random

import pytest

from engine.action import Action, ActionType
from engine.blood_battle import PlayError, apply_action, player_at, start_play
from engine.config import EngineConfig
from engine.legal import legal_actions
from engine.session import GameSession, build_ready_game, play_random_game
from engine.tile import Suit


def test_b01_start_play() -> None:
    state = build_ready_game("m04-b01", num_players=4)
    assert state.phase == "ready"
    start_play(state)
    assert state.phase == "discard"
    assert state.current_seat == state.dealer_seat


def test_b02_discard_pass_cycle() -> None:
    state = build_ready_game("m04-b02", num_players=2)
    start_play(state)
    dealer = state.dealer_seat
    acts = legal_actions(state, dealer)
    disc = next(a for a in acts if a.type == ActionType.DISCARD)
    apply_action(state, dealer, disc)
    assert state.phase == "response"
    other = 1 - dealer
    apply_action(state, other, Action(ActionType.PASS))
    # after pass → draw → discard for other
    assert state.phase == "discard"
    assert state.current_seat == other
    assert len(player_at(state, other).hand) in (13, 14)


def test_b08_force_discard_dingque() -> None:
    state = build_ready_game(
        "m04-b08",
        num_players=2,
        config=EngineConfig(num_players=2, force_discard_dingque=True),
        dingque_plan={0: Suit.WAN, 1: Suit.TONG},
    )
    start_play(state)
    seat = state.current_seat
    assert seat is not None
    p = player_at(state, seat)
    # if has dingque tiles, legal discards only those
    ding = [t for t in p.hand if t.suit == p.dingque]
    acts = [a for a in legal_actions(state, seat) if a.type == ActionType.DISCARD]
    if ding:
        for a in acts:
            assert a.tiles[0].suit == p.dingque


def test_force_complete_response_unblocks() -> None:
    """Missing response claims must not freeze the hand forever."""
    from engine.action import Action, ActionType
    from engine.blood_battle import force_complete_response, start_play
    from engine.config import EngineConfig
    from engine.legal import legal_actions
    from engine.session import build_ready_game

    st = build_ready_game(
        "bb-force-resp",
        num_players=4,
        config=EngineConfig(num_players=4, enable_exchange=False),
    )
    start_play(st)
    seat = st.current_seat
    assert seat is not None
    acts = legal_actions(st, seat)
    disc = next(a for a in acts if a.type == ActionType.DISCARD)
    from engine.blood_battle import apply_action

    apply_action(st, seat, disc)
    assert st.phase == "response"
    # Only one seat answers; rest missing → force complete
    s0 = st.response_seats[0]
    apply_action(st, s0, Action(ActionType.PASS))
    assert st.phase == "response"
    assert force_complete_response(st) is True
    assert st.phase in ("draw", "discard", "finished")


def test_blood_battle_continues_after_first_hu() -> None:
    """First hu must not end the hand while ≥2 players remain active (血战)."""
    import random

    from engine.action import Action, ActionType
    from engine.blood_battle import apply_action, do_draw, player_at, start_play
    from engine.config import EngineConfig
    from engine.legal import legal_actions
    from engine.session import build_ready_game

    found = False
    for seed in range(80):
        rng = random.Random(seed)
        st = build_ready_game(
            f"bb-cont-{seed}",
            num_players=4,
            config=EngineConfig(num_players=4, enable_exchange=False),
        )
        start_play(st)
        saw_hu = False
        for _ in range(6000):
            if st.phase == "finished":
                break
            if st.phase == "draw":
                do_draw(st)
                continue
            if st.phase == "discard":
                seat = st.current_seat
                assert seat is not None
                acts = legal_actions(st, seat)
                hu = [a for a in acts if a.type == ActionType.HU]
                if hu and not saw_hu:
                    apply_action(st, seat, hu[0])
                    saw_hu = True
                    active = [p.seat for p in st.players if p.status == "active"]
                    finished = [p.seat for p in st.players if p.status == "finished"]
                    assert len(finished) >= 1
                    if len(active) >= 2:
                        assert st.phase != "finished", (
                            f"seed={seed} ended after first hu with "
                            f"active={active} reason={st.finished_reason}"
                        )
                        assert st.phase in ("draw", "discard", "response")
                        found = True
                        # play a few more steps to ensure engine still moves
                        for __ in range(5):
                            if st.phase == "finished":
                                break
                            if st.phase == "draw":
                                do_draw(st)
                            elif st.phase == "discard":
                                s2 = st.current_seat
                                assert player_at(st, s2).status == "active"
                                acts2 = legal_actions(st, s2)
                                assert acts2, "no legal after first hu"
                                d = [a for a in acts2 if a.type == ActionType.DISCARD]
                                apply_action(st, s2, rng.choice(d or acts2))
                            elif st.phase == "response":
                                for s3 in list(st.response_seats or []):
                                    if s3 in (st.pending_claims or {}):
                                        continue
                                    if st.phase != "response":
                                        break
                                    a3 = legal_actions(st, s3)
                                    apply_action(
                                        st,
                                        s3,
                                        next(
                                            (
                                                a
                                                for a in a3
                                                if a.type == ActionType.PASS
                                            ),
                                            a3[0],
                                        ),
                                    )
                        break
                    continue
                d = [a for a in acts if a.type == ActionType.DISCARD]
                apply_action(st, seat, rng.choice(d or acts))
                continue
            if st.phase == "response":
                for s in list(st.response_seats or []):
                    if s in (st.pending_claims or {}):
                        continue
                    if st.phase != "response":
                        break
                    acts = legal_actions(st, s)
                    hu = [a for a in acts if a.type == ActionType.HU]
                    if hu and not saw_hu:
                        apply_action(st, s, hu[0])
                        saw_hu = True
                    else:
                        apply_action(st, s, Action(ActionType.PASS))
                if saw_hu:
                    active = [p.seat for p in st.players if p.status == "active"]
                    if len(active) >= 2 and st.phase != "finished":
                        found = True
                    break
                continue
        if found:
            break
    assert found, "could not find a first-hu position with ≥2 active players"


def test_b10_random_games_terminate() -> None:
    for i in range(20):
        result = play_random_game(
            f"m04-rand-{i}",
            num_players=4,
            rng=random.Random(i),
            max_steps=5000,
        )
        assert result.finished_reason in (
            "last_one",
            "wall_empty",
            "max_steps",
        )
        assert len(result.rankings) == 4


def test_b11_more_random() -> None:
    # 50 games light
    ok = 0
    for i in range(50):
        result = play_random_game(
            f"m04-r50-{i}",
            num_players=3,
            rng=random.Random(100 + i),
            max_steps=8000,
        )
        assert result.game_id.startswith("m04")
        ok += 1
    assert ok == 50


def test_illegal_action() -> None:
    state = build_ready_game("m04-ill", num_players=2)
    start_play(state)
    seat = state.current_seat
    with pytest.raises(PlayError):
        apply_action(state, seat, Action(ActionType.PASS))


def test_session_wrapper() -> None:
    state = build_ready_game("m04-sess", num_players=2)
    sess = GameSession(state)
    sess.start_play()
    seat = sess.state.current_seat
    acts = sess.legal_actions(seat)
    disc = next(a for a in acts if a.type == ActionType.DISCARD)
    sess.apply(seat, disc)
    assert sess.state.phase in ("response", "discard", "draw", "finished")
