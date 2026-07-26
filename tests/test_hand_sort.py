"""Hand order: wan → tong → tiao, rank ascending."""

from __future__ import annotations

from engine.deal import create_dealt_game
from engine.tile import Suit, Tile, sorted_tiles
from players.view.player_view import _sort_hand_ids


def test_sorted_tiles_order() -> None:
    hand = [
        Tile(Suit.TIAO, 3),
        Tile(Suit.WAN, 9),
        Tile(Suit.TONG, 1),
        Tile(Suit.WAN, 2),
        Tile(Suit.TIAO, 1),
    ]
    assert [t.id for t in sorted_tiles(hand)] == [
        "wan_2",
        "wan_9",
        "tong_1",
        "tiao_1",
        "tiao_3",
    ]


def test_dealt_hands_sorted() -> None:
    st = create_dealt_game("sort-hand-001", num_players=4)
    for p in st.players:
        ids = [t.id for t in p.hand]
        assert ids == [t.id for t in p.sorted_hand()]


def test_player_view_sort_hand_ids() -> None:
    raw = ["tiao_5", "wan_1", "tong_9", "wan_3"]
    assert _sort_hand_ids(raw) == ["wan_1", "wan_3", "tong_9", "tiao_5"]


def test_to_dict_hand_sorted() -> None:
    st = create_dealt_game("sort-hand-dict", num_players=2)
    # scramble then export
    p = st.players[0]
    p.hand = list(reversed(p.hand))
    d = p.to_dict()
    assert d["hand"] == [t.id for t in p.sorted_hand()]
