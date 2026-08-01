"""M05 — scoring tests."""

from __future__ import annotations

from engine.config import EngineConfig
from engine.score import ScoreService, ScoreTable, hu_points
from engine.state import GameState, PlayerState
from engine.dice import DiceResult
from engine.tile import Suit, Tile


def _minimal_state(scores: dict[int, int] | None = None) -> GameState:
    scores = scores or {0: 0, 1: 0, 2: 0, 3: 0}
    players = [
        PlayerState(
            seat=i,
            hand=[Tile(Suit.WAN, 1)] * 13,
            score=scores.get(i, 0),
            dingque=Suit.TIAO,
            status="active",
            is_dealer=(i == 0),
        )
        for i in range(4)
    ]
    return GameState(
        game_id="score-test",
        master_seed=1,
        phase="discard",
        num_players=4,
        dice=DiceResult(1, 1, 2, 0),
        dealer_seat=0,
        wall=[],
        players=players,
        current_seat=0,
    )


def test_sc01_dianpao_fan2() -> None:
    state = _minimal_state()
    cfg = EngineConfig(base_score=1)
    svc = ScoreService(cfg, ScoreTable(base_score=1))
    svc.apply_hu_dianpao(state, [0], loser=1, fans={0: 2})
    assert hu_points(2, 1) == 4
    assert state.players[0].score == 4
    assert state.players[1].score == -4


def test_sc02_multi_ron() -> None:
    state = _minimal_state()
    svc = ScoreService(EngineConfig(), ScoreTable(base_score=1))
    svc.apply_hu_dianpao(state, [0, 2], loser=1, fans={0: 1, 2: 0})
    # 0 gets 2, 2 gets 1 from seat 1
    assert state.players[0].score == 2
    assert state.players[2].score == 1
    assert state.players[1].score == -3


def test_sc03_zimo() -> None:
    state = _minimal_state()
    svc = ScoreService(EngineConfig(), ScoreTable(base_score=1))
    svc.apply_hu_zimo(state, winner=0, fan=1)
    # each of 1,2,3 pays 2
    assert state.players[0].score == 6
    assert state.players[1].score == -2


def test_sc04_an_gang() -> None:
    state = _minimal_state()
    svc = ScoreService(EngineConfig(), ScoreTable(base_score=1, gang_an_mult=2))
    svc.apply_gang(state, "gang_an", gang_seat=0)
    assert state.players[0].score == 6  # 2*3
    assert state.players[1].score == -2


def test_sc05_hua_zhu() -> None:
    state = _minimal_state()
    # seat 0 holds dingque tiao
    state.players[0].hand = [Tile(Suit.TIAO, 1)] * 13
    state.players[0].dingque = Suit.TIAO
    # others clean
    for i in range(1, 4):
        state.players[i].hand = [Tile(Suit.WAN, 2)] * 13
        state.players[i].dingque = Suit.TIAO
    state.phase = "finished"
    state.finished_reason = "wall_empty"
    svc = ScoreService(EngineConfig(), ScoreTable(base_score=1, hua_zhu_fan=3))
    tr = svc.settle_end(state)
    assert any(t.reason == "hua_zhu" for t in tr)
    # pig pays 8 to each of 3 => -24
    assert state.players[0].score == -24


def test_score_events_written() -> None:
    state = _minimal_state()
    svc = ScoreService(EngineConfig())
    svc.apply_hu_dianpao(state, [0], 1, {0: 0})
    assert any(e.get("type") == "score" for e in state.score_events)
