"""F0008 — per-seat score ledger from score_events."""

from __future__ import annotations

from engine.blood_battle import build_game_result
from engine.config import EngineConfig
from engine.score import (
    ScoreService,
    ScoreTable,
    build_score_ledger,
    format_score_line,
    ledger_net,
    reason_label,
)
from engine.state import GameState, PlayerState
from engine.dice import DiceResult
from engine.tile import Suit, Tile


def _state() -> GameState:
    players = [
        PlayerState(
            seat=i,
            hand=[Tile(Suit.WAN, 1)] * 13,
            score=0,
            dingque=Suit.TIAO,
            status="active",
            is_dealer=(i == 0),
        )
        for i in range(4)
    ]
    return GameState(
        game_id="ledger-test",
        master_seed=1,
        phase="discard",
        num_players=4,
        dice=DiceResult(1, 1, 2, 0),
        dealer_seat=0,
        wall=[],
        players=players,
        current_seat=0,
    )


def test_reason_labels_zh() -> None:
    assert reason_label("hu_zimo") == "自摸"
    assert reason_label("hu_dianpao") == "点炮胡"
    assert reason_label("gang_an") == "暗杠"
    assert reason_label("hua_zhu") == "花猪"
    assert reason_label("cha_jiao") == "查叫"


def test_format_score_line() -> None:
    assert format_score_line(delta=4, reason="hu_dianpao", counterparty=1, fan=2) == (
        "+4 点炮胡(2番) ←S1"
    )
    assert format_score_line(delta=-2, reason="gang_jia", counterparty=0) == (
        "-2 补杠 →S0"
    )


def test_ledger_matches_balances() -> None:
    state = _state()
    svc = ScoreService(EngineConfig(), ScoreTable(base_score=1))
    svc.apply_hu_dianpao(state, [0], loser=1, fans={0: 2})  # +4 / -4
    svc.apply_gang(state, "gang_an", gang_seat=2)  # +6 to S2 from 0,1,3 each 2

    ledger = build_score_ledger(
        [e for e in state.score_events if e.get("type") == "score"]
    )
    for p in state.players:
        assert ledger_net(ledger.get(p.seat, [])) == p.score

    # S0: +4 from dianpao, -2 to an gang
    s0_texts = [x["text"] for x in ledger[0]]
    assert any("点炮胡" in t and "+4" in t for t in s0_texts)
    assert any("暗杠" in t and "-2" in t for t in s0_texts)


def test_build_game_result_includes_score_events() -> None:
    state = _state()
    svc = ScoreService(EngineConfig())
    svc.apply_hu_zimo(state, winner=0, fan=0)
    state.phase = "finished"
    state.finished_reason = "last_one"
    state.end_settled = True  # skip settle_end side effects for isolation
    result = build_game_result(state)
    assert result.score_events
    assert all(e.get("transfers") for e in result.score_events)
    d = result.to_dict()
    assert "score_events" in d
    ledger = build_score_ledger(result.score_events)
    assert ledger_net(ledger[0]) == result.scores[0]
