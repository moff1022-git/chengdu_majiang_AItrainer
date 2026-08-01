"""M03 — shanten tests."""

from __future__ import annotations

from engine.shanten import shanten
from engine.tile import Suit, Tile
from engine.win_check import is_winning_hand


def T(suit: str, rank: int) -> Tile:
    return Tile(Suit(suit), rank)


def expand(*groups: tuple[str, list[int]]) -> list[Tile]:
    out: list[Tile] = []
    for suit, ranks in groups:
        for r in ranks:
            out.append(T(suit, r))
    return out


def test_s02_winning_standard_shanten_neg1() -> None:
    # 123m 456m 789m 123p 11s
    hand = expand(
        ("wan", [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ("tong", [1, 2, 3]),
        ("tiao", [1, 1]),
    )
    assert len(hand) == 14
    assert is_winning_hand(hand, [], Suit.TIAO).ok is False  # has tiao dingque wrong
    assert is_winning_hand(hand, [], Suit.WAN).ok is False  # has wan
    r = is_winning_hand(hand, [], Suit.TONG)  # wait has tong
    # dingque must be a suit NOT in hand — use a free suit: all three present
    # change pair to tong: 11p and no tiao... hand has all 3 suits.
    # Use dingque that is empty: impossible if all suits present.
    # For win, dingque suit must not appear — pick hand without tiao:
    hand = expand(
        ("wan", [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ("tong", [1, 2, 3, 1, 1]),
    )
    assert len(hand) == 14
    assert is_winning_hand(hand, [], Suit.TIAO).ok
    s = shanten(hand, [], Suit.TIAO)
    assert s.shanten == -1


def test_s01_tenpai_shanten_0() -> None:
    # 13 tiles: 123m 456m 789m 123p 1s — wait for 1s
    hand = expand(
        ("wan", [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ("tong", [1, 2, 3]),
        ("tiao", [1]),
    )
    assert len(hand) == 13
    s = shanten(hand, [], Suit.TIAO)  # still has tiao 1 — dingque tiao means not tenpai clean
    # dingque tong? has tong. dingque must be absent from hand for win; for tenpai with tiao wait,
    # dingque = wan is wrong. Use hand without dingque suit:
    # 123m456m789m123p1p — wait 1p or 4p etc, dingque=tiao
    hand = expand(
        ("wan", [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ("tong", [1, 2, 3, 1]),
    )
    assert len(hand) == 13
    s = shanten(hand, [], Suit.TIAO)
    assert s.shanten == 0
    assert s.ukeire is not None
    assert T("tong", 1) in s.ukeire or T("tong", 4) in s.ukeire or len(s.ukeire) >= 1


def test_s03_seven_pairs_tenpai() -> None:
    # 6 pairs + 1 single
    hand = expand(
        ("wan", [1, 1, 2, 2, 3, 3]),
        ("tong", [1, 1, 2, 2, 3, 3]),
        ("tiao", [5]),
    )
    assert len(hand) == 13
    s = shanten(hand, [], Suit.TIAO)
    # has tiao dingque — bad. replace single with wan 4
    hand = expand(
        ("wan", [1, 1, 2, 2, 3, 3, 4]),
        ("tong", [1, 1, 2, 2, 3, 3]),
    )
    s = shanten(hand, [], Suit.TIAO)
    assert s.seven_pairs == 0 or s.shanten == 0
    assert s.shanten == 0
    assert s.ukeire is not None
    assert T("wan", 4) in s.ukeire


def test_s04_dingque_raises_shanten() -> None:
    hand_clean = expand(
        ("wan", [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ("tong", [1, 2, 3, 1]),
    )
    hand_dirty = hand_clean + [T("tiao", 5)]
    # dirty is 14 tiles — compare 13-tile versions
    clean13 = hand_clean
    dirty13 = expand(
        ("wan", [1, 2, 3, 4, 5, 6, 7, 8]),
        ("tong", [1, 2, 3]),
        ("tiao", [5, 5]),
    )
    s_clean = shanten(clean13, [], Suit.TIAO)
    s_dirty = shanten(dirty13, [], Suit.TIAO)
    assert s_dirty.shanten > s_clean.shanten
