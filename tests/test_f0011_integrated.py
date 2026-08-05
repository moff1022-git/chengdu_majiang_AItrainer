"""F0011 integrated discard advisor A1–A5 smoke tests."""

from __future__ import annotations

from engine.action import ActionType
from engine.config import EngineConfig
from engine.deal import create_dealt_game
from engine.legal import legal_actions
from players.analysis.integrated_discard import (
    build_f0010_context,
    fan_proxy_after,
    rank_discards_f0011,
    s_fei,
)
from players.analysis.opponent_model import estimate_opponents
from players.analysis.pipeline import analyze_for_seat
from players.analysis.strategy import rank_discards


def test_build_f0010_context_and_rank() -> None:
    st = create_dealt_game("f0011-t1", config=EngineConfig(num_players=4))
    # force discard-like hand size: already 13; add nothing
    ctx = build_f0010_context(st, 0, top_k=2, seed=1)
    assert ctx.remain_eff
    assert isinstance(ctx.dumps, dict)
    ops = estimate_opponents(st, 0)
    p = st.players[0]
    # may have 13 tiles — rank still works on unique ids
    ranks = rank_discards_f0011(
        st, 0, list(p.hand), p.melds, p.dingque, ops, f0010_top_k=2, seed=1
    )
    assert ranks
    assert ranks[0].rank == 1
    assert ranks[0].danger in (
        "critical",
        "high",
        "medium",
        "low",
        "safe",
        "unknown",
    )
    det = getattr(ranks[0], "f0011_detail", None)
    assert det is not None
    assert "s_gong" in det and "s_fang" in det and "s_fei" in det


def test_pipeline_legacy_f0011_flag_cannot_reenable_retired_human_recommendation() -> None:
    st = create_dealt_game("f0011-t2", config=EngineConfig(num_players=4))
    snap0 = analyze_for_seat(st, 0, use_f0011=False)
    snap1 = analyze_for_seat(st, 0, use_f0011=True, f0011_top_k=2)
    assert getattr(snap0, "use_f0011", False) is False
    assert getattr(snap1, "use_f0011", False) is False
    # both may have empty ranks if hand not discard-size; still ok
    assert snap1.generated_ms >= 0


def test_fan_proxy_and_baseline_compat() -> None:
    st = create_dealt_game("f0011-t3", config=EngineConfig(num_players=4))
    p = st.players[0]
    fp = fan_proxy_after(list(p.hand), p.melds, p.dingque)
    assert 0.0 <= fp <= 6.0
    ops = estimate_opponents(st, 0)
    base = rank_discards(st, 0, list(p.hand), p.melds, p.dingque, ops)
    assert isinstance(base, list)


def test_s_fei_present() -> None:
    st = create_dealt_game("f0011-t4", config=EngineConfig(num_players=4))
    ctx = build_f0010_context(st, 0, top_k=2, seed=0)
    # any face id
    tid = "wan_5"
    v = s_fei(tid, ctx)
    assert v >= 0.0
