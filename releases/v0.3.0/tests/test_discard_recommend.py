"""F0012 discard recommendation display rules."""

from __future__ import annotations

from players.analysis.discard_recommend import (
    build_discard_recommendations,
    recommendation_order_map,
    sort_ukeire_tile_ids,
    ukeire_for_focus,
)
from players.analysis.types import DiscardAdvice


def test_ukeire_face_tw_readable_range() -> None:
    """F0012: ukeire faces stay in 32–40px (not the old ≤22 mini)."""
    from players.seat_window import TkSeatApp

    class _Stub:
        def _content_width(self):
            return 640

    tw = TkSeatApp._ukeire_face_tw(_Stub())  # type: ignore[arg-type]
    assert 32 <= tw <= 40
    assert tw % 2 == 0


def test_sort_ukeire_wan_tong_tiao() -> None:
    ids = ["tiao_3", "wan_9", "tong_1", "wan_2", "tiao_1"]
    assert sort_ukeire_tile_ids(ids) == [
        "wan_2",
        "wan_9",
        "tong_1",
        "tiao_1",
        "tiao_3",
    ]


def test_non_tenpai_max_three() -> None:
    ranks = [
        DiscardAdvice("wan_1", 1, 2, 0, "safe", 1.0, "best", []),
        DiscardAdvice("wan_2", 2, 2, 0, "safe", 0.9, "second", []),
        DiscardAdvice("wan_3", 3, 3, 0, "safe", 0.8, "none", []),
        DiscardAdvice("wan_4", 4, 3, 0, "safe", 0.7, "none", []),
    ]
    rec = build_discard_recommendations(ranks)
    assert len(rec) == 3
    assert [r["tile_id"] for r in rec] == ["wan_1", "wan_2", "wan_3"]
    assert [r["order"] for r in rec] == [1, 2, 3]
    assert all(not r["is_tenpai"] for r in rec)


def test_tenpai_recommends_all_tenpai_discards() -> None:
    ranks = [
        DiscardAdvice("wan_1", 1, 1, 0, "safe", 1.0, "best", []),
        DiscardAdvice(
            "tong_5", 2, 0, 2, "safe", 0.95, "second", ["wan_3", "tiao_2"]
        ),
        DiscardAdvice("wan_2", 3, 2, 0, "safe", 0.5, "none", []),
        DiscardAdvice(
            "tiao_9", 4, 0, 1, "low", 0.4, "none", ["tong_1"]
        ),
    ]
    rec = build_discard_recommendations(ranks)
    assert len(rec) == 2
    assert [r["tile_id"] for r in rec] == ["tong_5", "tiao_9"]
    assert all(r["is_tenpai"] for r in rec)
    assert rec[0]["ukeire_tiles"] == ["wan_3", "tiao_2"]
    assert rec[1]["ukeire_tiles"] == ["tong_1"]
    m = recommendation_order_map(rec)
    assert m["tong_5"] == 1 and m["tiao_9"] == 2
    assert ukeire_for_focus(rec, "tong_5") == ["wan_3", "tiao_2"]
    assert ukeire_for_focus(rec, "wan_1") == []


def test_strategy_ranks_include_ukeire_tiles() -> None:
    from engine.config import EngineConfig
    from engine.deal import create_dealt_game
    from players.analysis.opponent_model import estimate_opponents
    from players.analysis.strategy import rank_discards

    st = create_dealt_game("f0012-uke", config=EngineConfig(num_players=4))
    p = st.players[0]
    ops = estimate_opponents(st, 0)
    ranks = rank_discards(st, 0, list(p.hand), p.melds, p.dingque, ops)
    assert ranks
    # field exists on advice
    assert hasattr(ranks[0], "ukeire_tiles")
    assert isinstance(ranks[0].ukeire_tiles, list)
