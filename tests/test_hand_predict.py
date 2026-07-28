"""F0010: opponent hand Top-K prediction v2 + multiset F1 accuracy."""

from __future__ import annotations

from collections import Counter

from engine.config import EngineConfig
from engine.deal import create_dealt_game
from players.analysis.hand_predict import (
    DUMP_COMPLY_EMPTY,
    EARLY_MMR,
    LATE_BLEND_FAST,
    LATE_BLEND_SHANTEN,
    LATE_CONF_TEMPERATURE,
    LATE_MMR,
    LATE_STRUCTURE_MULT,
    MID_CONF_TEMPERATURE,
    MID_MMR,
    TARGET_SHANTEN_BY_DISC,
    TARGET_SHANTEN_MELD_RELIEF,
    _dump_compliance_mult,
    _structure_score,
    _target_shanten,
    apply_oracle_accuracy,
    assert_mutual_exclusion,
    discard_fingerprint,
    expected_hand_count,
    multiset_f1,
    predict_joint_scenes,
    predict_opponent_hands,
    score_accuracy,
    OpponentHandForecast,
    OpponentHandHypothesis,
)
from players.analysis.remain import remain_map


def test_multiset_f1_basic() -> None:
    assert multiset_f1([], []) == 1.0
    assert multiset_f1(["wan_1"], []) == 0.0
    a = ["wan_1", "wan_1", "tong_2"]
    b = ["wan_1", "tong_2", "tiao_3"]
    # inter: wan_1 x1 + tong_2 = 2; |a|+|b|=6; f1=4/6
    assert abs(multiset_f1(a, b) - 4 / 6) < 1e-6


def test_predict_top_k_sorted_and_normalized() -> None:
    st = create_dealt_game("pred-test-1", config=EngineConfig(num_players=4))
    forecasts = predict_opponent_hands(st, self_seat=0, top_k=5, seed=42)
    assert len(forecasts) == 3
    for fc in forecasts:
        assert fc.seat != 0
        assert 1 <= len(fc.hypotheses) <= 5
        confs = [h.confidence for h in fc.hypotheses]
        assert confs == sorted(confs, reverse=True)
        s = sum(confs)
        assert 0.98 <= s <= 1.02
        ranks = [h.rank for h in fc.hypotheses]
        assert ranks == list(range(1, len(ranks) + 1))
        need = expected_hand_count(st, fc.seat)
        for h in fc.hypotheses:
            assert len(h.tiles) == need
            assert h.tiles == sorted(h.tiles)
            assert h.scene_id >= 1


def test_score_accuracy_picks_best_rank() -> None:
    true = ["wan_1", "wan_2", "wan_3"]
    hyps = [
        OpponentHandHypothesis(1, ["tong_1", "tong_2", "tong_3"], 0.5),
        OpponentHandHypothesis(2, ["wan_1", "wan_2", "wan_3"], 0.3),
        OpponentHandHypothesis(3, ["wan_1", "tiao_9", "tiao_8"], 0.2),
    ]
    fc = OpponentHandForecast(seat=1, hypotheses=hyps)
    scored = score_accuracy(fc, true)
    assert scored.accuracy == 1.0
    assert scored.accuracy_detail.get("best_rank") == 2
    assert scored.accuracy_detail.get("exact_set") is True


def test_apply_oracle_and_fingerprint() -> None:
    st = create_dealt_game("pred-test-2", config=EngineConfig(num_players=4))
    fcs = predict_opponent_hands(st, 0, top_k=5, seed=1)
    oracle = {str(p.seat): [t.id for t in p.hand] for p in st.players if p.seat != 0}
    scored = apply_oracle_accuracy(fcs, oracle)
    assert all(s.accuracy is not None for s in scored)
    view = {"last_discard": "wan_5", "last_discard_seat": 2}
    assert discard_fingerprint(view) == "2:wan_5"
    assert discard_fingerprint({"discard_seq": 7}) == "seq:7"


def test_predict_from_view_dict_no_oracle_param() -> None:
    """Contract: public API only takes state/view + self_seat (no oracle)."""
    st = create_dealt_game("pred-test-3", config=EngineConfig(num_players=4))
    from protocols.view_filter import filter_state_for_seat

    view = filter_state_for_seat(st, 0)
    fcs = predict_opponent_hands(view, 0, top_k=3, seed=0)
    assert len(fcs) >= 1


def test_joint_mutual_exclusion_respects_remain() -> None:
    """E: within each scene, sum of tile counts across opponents ≤ remain."""
    st = create_dealt_game("pred-mutex-1", config=EngineConfig(num_players=4))
    remain = remain_map(st, 0)
    scenes = predict_joint_scenes(st, self_seat=0, top_k=5, seed=7)
    assert scenes
    for sc in scenes:
        used: Counter = Counter()
        for h in sc.hands.values():
            used.update(h)
        for tid, n in used.items():
            assert n <= int(remain.get(tid, 0)), (
                f"scene {sc.scene_id} overuses {tid}: {n} > remain {remain.get(tid)}"
            )
    fcs = predict_opponent_hands(st, 0, top_k=5, seed=7)
    assert assert_mutual_exclusion(fcs, remain, rank=1)


def test_joint_scene_alignment_across_seats() -> None:
    """Same scene_id / confidence across seats (joint display)."""
    st = create_dealt_game("pred-align-1", config=EngineConfig(num_players=4))
    fcs = predict_opponent_hands(st, 0, top_k=5, seed=11)
    assert len(fcs) == 3
    # ranks map to same scene confidences
    by_rank: dict[int, list[float]] = {}
    for fc in fcs:
        for h in fc.hypotheses:
            by_rank.setdefault(h.rank, []).append(h.confidence)
            assert h.scene_id == h.rank or h.scene_id >= 1
    for rank, confs in by_rank.items():
        assert len(set(round(c, 4) for c in confs)) == 1, (
            f"rank {rank} conf mismatch across seats: {confs}"
        )


def test_continuity_prev_joints_and_hard_c1() -> None:
    """C1: after a seat discards d, continuity evolves prior hand that held d."""
    st = create_dealt_game("pred-cont-1", config=EngineConfig(num_players=4))
    scenes0 = predict_joint_scenes(st, 0, top_k=5, seed=3)
    assert scenes0
    # Pick a tile from seat 1's top scene hand and pretend they discarded it
    s1_hand = scenes0[0].hands.get(1) or []
    assert s1_hand
    disc = s1_hand[0]
    scenes1 = predict_joint_scenes(
        st,
        0,
        top_k=5,
        prev_joints=scenes0,
        last_discarder=1,
        last_discard_tile=disc,
        seed=4,
    )
    assert scenes1
    remain = remain_map(st, 0)
    for sc in scenes1:
        used: Counter = Counter()
        for h in sc.hands.values():
            used.update(h)
        for tid, n in used.items():
            assert n <= int(remain.get(tid, 0))
    # At least one evolved scene should retain substantial overlap with prior
    # non-discarder hands (continuity soft/hard path)
    prev_other = {s: scenes0[0].hands[s] for s in scenes0[0].hands if s != 1}
    best_overlap = 0.0
    for sc in scenes1:
        for s, prev_h in prev_other.items():
            if s not in sc.hands:
                continue
            best_overlap = max(best_overlap, multiset_f1(sc.hands[s], prev_h))
    assert best_overlap >= 0.3


def test_dh_combo_and_dingque_exempt() -> None:
    from players.analysis.hand_predict import (
        _combo_association,
        _tenpai_association,
        _discard_hand_assoc_penalty,
    )

    hand = ["wan_2", "wan_3", "wan_4", "tong_1", "tong_9"]
    # strong combo with wan_3
    assert _combo_association("wan_3", hand, None) > _combo_association(
        "tiao_5", hand, None
    )
    # dingque discard → 0 assoc
    assert _combo_association("wan_5", hand, "wan") == 0.0
    assert _tenpai_association("wan_5", hand, 0, "wan") == 0.0
    # early penalty applies for high combo
    p_hi = _discard_hand_assoc_penalty(
        hand,
        ["tong_9", "wan_3"],
        ban_suit=None,
        n_melds=0,
        phase="early",
    )
    p_lo = _discard_hand_assoc_penalty(
        hand,
        ["tong_9", "tiao_5"],
        ban_suit=None,
        n_melds=0,
        phase="early",
    )
    assert p_hi < p_lo


def test_m2_dumped_suits_and_streak() -> None:
    from players.analysis.hand_predict import (
        _dumped_suits,
        _streak_dumped_suits,
        DUMP_SUIT_COUNT_MID,
        DUMP_SUIT_COUNT_LATE,
        DUMP_SUIT_RECENT_MIN,
    )

    # mid K=3 + ≥ RECENT_MIN wan in recent window
    mid_disc = [
        "wan_1",
        "wan_2",
        "tong_5",
        "wan_3",
        "wan_4",
        "wan_5",
        "tiao_1",
    ]
    assert "wan" in _dumped_suits(mid_disc, "mid")
    assert "tong" not in _dumped_suits(mid_disc, "mid")
    # late: need K=3 + recent≥3 wan
    late_disc = ["tong_9", "wan_1", "wan_2", "tong_2", "wan_9", "wan_8"]
    assert "wan" in _dumped_suits(late_disc, "late")
    # only 2 wan total → not dump even in late
    assert "wan" not in _dumped_suits(["tong_1", "wan_1", "wan_2"], "late")
    assert _dumped_suits(late_disc, "early") == set()
    # trailing streak only
    streak = ["tong_1", "wan_1", "wan_2", "wan_3"]
    assert "wan" in _streak_dumped_suits(streak)
    assert "wan" not in _streak_dumped_suits(["wan_1", "wan_2", "wan_3", "tiao_9"])
    assert DUMP_SUIT_COUNT_MID == 3
    assert DUMP_SUIT_COUNT_LATE == 3
    assert DUMP_SUIT_RECENT_MIN == 3


def test_l2_target_shanten_table() -> None:
    """L2.1 C5b: empirical table decreases with discards; melds relieve; clamp ≥0."""
    assert _target_shanten(0, 0) == TARGET_SHANTEN_BY_DISC[0]
    assert _target_shanten(7, 0) == TARGET_SHANTEN_BY_DISC[7]
    assert _target_shanten(20, 0) == TARGET_SHANTEN_BY_DISC[-1]
    assert _target_shanten(7, 1) == max(
        0.0, TARGET_SHANTEN_BY_DISC[7] - TARGET_SHANTEN_MELD_RELIEF
    )
    assert _target_shanten(12, 4) >= 0.0
    assert _target_shanten(12, 10) == 0.0
    # roughly monotonic in n_disc for meld0
    prev = _target_shanten(0, 0)
    for nd in range(1, len(TARGET_SHANTEN_BY_DISC)):
        cur = _target_shanten(nd, 0)
        assert cur <= prev + 1e-9
        prev = cur
    # late targets well below early (old formula was too low early)
    assert _target_shanten(0, 0) >= 6.5
    assert _target_shanten(10, 0) <= 2.5


def test_l2_structure_mult_constant() -> None:
    """L2.4: late structure amplifies bonus; base score is ≥1."""
    tiles = ["wan_1", "wan_1", "wan_2", "wan_3", "tong_5", "tong_5"]
    base = _structure_score(tiles)
    assert base >= 1.0
    amplified = 1.0 + LATE_STRUCTURE_MULT * (base - 1.0)
    assert amplified >= base - 1e-9
    assert LATE_STRUCTURE_MULT == 1.2


def test_l3_ranking_constants() -> None:
    """L3.1–L3.3: temperature / MMR / blend locked to plan."""
    assert LATE_CONF_TEMPERATURE == 0.35
    assert MID_CONF_TEMPERATURE == 0.50
    assert EARLY_MMR == 0.55
    assert MID_MMR == 0.40
    assert LATE_MMR == 0.15
    assert abs(LATE_BLEND_FAST + LATE_BLEND_SHANTEN - 1.0) < 1e-9
    assert LATE_BLEND_SHANTEN == 0.24
    assert LATE_BLEND_FAST == 0.76


def test_s2_trust_and_j4_constants() -> None:
    from players.analysis.hand_predict import (
        J4_SHANTEN_WORSEN_TOL,
        J4_WORSEN_SOFT,
        LATE_BLEND_SHANTEN,
        S2_FAKE_NEAR_EXTRA,
        S_TRUST_OUTSIDE_SCALE,
        S_TRUST_TAU,
    )

    assert J4_SHANTEN_WORSEN_TOL == 1
    assert J4_WORSEN_SOFT == 0.40
    assert S_TRUST_TAU == 1.5
    assert S_TRUST_OUTSIDE_SCALE == 0.35
    assert S2_FAKE_NEAR_EXTRA == 0.55
    assert LATE_BLEND_SHANTEN == 0.24  # S2.4: do not raise blend


def test_s1_fake_near_gate_late_only() -> None:
    from players.analysis.hand_predict import (
        StrategyBelief,
        _is_suspicious_fake_near,
        _target_shanten,
    )

    bel = StrategyBelief()
    # late discards: many tong dumps
    disc = [f"tong_{i}" for i in range(1, 9)]
    # weak mixed hand claiming low shanten
    tiles = ["wan_1", "tong_2", "tiao_3", "wan_9", "tong_8", "tiao_7", "wan_5"]
    assert _target_shanten(len(disc), 0) >= 2.0
    assert _is_suspicious_fake_near(
        tiles,
        sh=0,
        n_disc=len(disc),
        n_melds=0,
        discards=disc,
        ban_suit=None,
        strategy=bel,
        phase="late",
    )
    # mid should not flag
    assert not _is_suspicious_fake_near(
        tiles,
        sh=0,
        n_disc=4,
        n_melds=0,
        discards=disc[:4],
        ban_suit=None,
        strategy=bel,
        phase="mid",
    )


def test_discard_accuracy_scoring_shape() -> None:
    """Discard accuracy returns top1/top3 fields and baseline 1/n_legal."""
    from engine.action import Action, ActionType
    from engine.config import EngineConfig
    from engine.deal import create_dealt_game
    from players.analysis.discard_accuracy import score_discard_decision

    st = create_dealt_game("disc-acc-1", config=EngineConfig(num_players=4))
    # force discard phase-like hand
    seat = 0
    hand = list(st.players[seat].hand)
    if len(hand) < 2:
        return
    tid = hand[0].id
    legal = [Action(ActionType.DISCARD, tiles=(t,)) for t in hand]
    # pick a legal actual
    row = score_discard_decision(st, seat, legal, tid)
    assert row["n_legal"] >= 1
    assert 0.0 < row["random_baseline"] <= 1.0
    assert "top1_hit" in row and "top3_hit" in row
    assert row["pred_top1"] is not None
    assert row["rank"] is not None and row["rank"] >= 1


def test_l3_dump_compliance_independent() -> None:
    """L3.4: empty dump-suit hold scores higher than excess hold."""
    # 3+ wan discards with recent window → dumped wan in late
    disc = [
        "wan_1",
        "wan_2",
        "wan_3",
        "tong_1",
        "wan_4",
        "wan_5",
        "wan_6",
        "tiao_1",
    ]
    clean = ["tong_2", "tong_3", "tong_4", "tiao_5", "tiao_6"]
    dirty = ["wan_7", "wan_8", "wan_9", "tong_2", "tiao_5"]
    m_clean = _dump_compliance_mult(clean, disc, "late")
    m_dirty = _dump_compliance_mult(dirty, disc, "late")
    m_none = _dump_compliance_mult(clean, ["tong_1", "tiao_2"], "late")
    assert m_none == 1.0
    assert m_clean > m_dirty
    assert m_clean >= DUMP_COMPLY_EMPTY  # at least empty bonus path


def test_strategy_hint_present() -> None:
    st = create_dealt_game("pred-strat-1", config=EngineConfig(num_players=4))
    # add discards to make strategy non-empty path
    from engine.tile import parse_tile

    st.players[1].discard_pile.extend(
        [parse_tile("wan_1"), parse_tile("wan_2"), parse_tile("tong_9")]
    )
    fcs = predict_opponent_hands(st, 0, top_k=3, seed=2)
    fc1 = next(f for f in fcs if f.seat == 1)
    assert isinstance(fc1.strategy_hint, str)
    # shanten_est may be int or None depending on engine; at least field exists
    assert any(hasattr(h, "shanten_est") for h in fc1.hypotheses)
