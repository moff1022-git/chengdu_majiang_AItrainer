"""M03 — win check and fan tests."""

from __future__ import annotations

import pytest

from engine.fan import FanError, WinContext, apply_fan_cap, compute_fan
from engine.hand_utils import MeldView
from engine.tile import Suit, Tile
from engine.win_check import WinForm, is_winning_hand


def T(suit: str, rank: int) -> Tile:
    return Tile(Suit(suit), rank)


def expand(*groups: tuple[str, list[int]]) -> list[Tile]:
    out: list[Tile] = []
    for suit, ranks in groups:
        for r in ranks:
            out.append(T(suit, r))
    return out


def standard_ping_hu() -> list[Tile]:
    # 123m 456m 789m 123p 11p, dingque=tiao
    return expand(
        ("wan", [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ("tong", [1, 2, 3, 1, 1]),
    )


def test_w01_standard_win() -> None:
    hand = standard_ping_hu()
    r = is_winning_hand(hand, [], Suit.TIAO)
    assert r.ok and r.form == WinForm.STANDARD


def test_w02_seven_pairs() -> None:
    hand = expand(
        ("wan", [1, 1, 2, 2, 3, 3, 4, 4]),
        ("tong", [5, 5, 6, 6, 7, 7]),
    )
    r = is_winning_hand(hand, [], Suit.TIAO)
    assert r.ok and r.form == WinForm.SEVEN_PAIRS


def test_w03_dingque_blocks() -> None:
    hand = standard_ping_hu()
    r = is_winning_hand(hand, [], Suit.WAN)
    assert not r.ok and r.reason == "HAS_DINGQUE"


def test_w04_no_dingque() -> None:
    hand = standard_ping_hu()
    r = is_winning_hand(hand, [], None)
    assert not r.ok and r.reason == "NO_DINGQUE"


def test_w05_not_complete() -> None:
    hand = expand(("wan", [1, 2, 3, 4, 5, 6, 7, 8, 9]), ("tong", [1, 2, 3, 4, 5]))
    r = is_winning_hand(hand, [], Suit.TIAO)
    assert not r.ok


def test_f01_ping_hu() -> None:
    hand = standard_ping_hu()
    fr = compute_fan(hand, [], Suit.TIAO, fan_cap=0)
    assert fr.fan_raw == 0
    assert "ping_hu" in fr.yaku


def test_f02_dui_dui_hu() -> None:
    # 333m 555m 777m 999p 11p
    hand = expand(
        ("wan", [3, 3, 3, 5, 5, 5, 7, 7, 7]),
        ("tong", [9, 9, 9, 1, 1]),
    )
    r = is_winning_hand(hand, [], Suit.TIAO)
    assert r.ok
    fr = compute_fan(hand, [], Suit.TIAO)
    assert "dui_dui_hu" in fr.yaku
    assert fr.fan_raw >= 1


def test_f03_qing_yi_se() -> None:
    # 123 456 789 111 22 万
    hand = expand(("wan", [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 1, 1, 2, 2]))
    assert len(hand) == 14
    assert is_winning_hand(hand, [], Suit.TIAO).ok
    fr = compute_fan(hand, [], Suit.TIAO)
    assert "qing_yi_se" in fr.yaku
    assert fr.details.get("qing_yi_se", 0) == 2


def test_f04_qing_dui_stack() -> None:
    # 全是万: 111 333 555 777 99
    hand = expand(("wan", [1, 1, 1, 3, 3, 3, 5, 5, 5, 7, 7, 7, 9, 9]))
    assert is_winning_hand(hand, [], Suit.TIAO).ok
    fr = compute_fan(hand, [], Suit.TIAO)
    assert "qing_yi_se" in fr.yaku
    assert "dui_dui_hu" in fr.yaku
    assert fr.fan_raw >= 3


def test_f05_seven_pairs_fan() -> None:
    hand = expand(
        ("wan", [1, 1, 2, 2, 3, 3, 4, 4]),
        ("tong", [5, 5, 6, 6, 7, 7]),
    )
    fr = compute_fan(hand, [], Suit.TIAO)
    assert "qi_dui" in fr.yaku
    assert fr.details["qi_dui"] == 2
    assert "dui_dui_hu" not in fr.yaku


def test_f06_gen() -> None:
    # 1111m as part of hand with pairs structure — standard: 1111 222 333 444 55 m
    hand = expand(("wan", [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5]))
    # not winning. Use 1111 222 333 444 55:
    hand = expand(("wan", [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5]))
    # 14 tiles but 5 single — fix pair 55:
    hand = expand(("wan", [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5]))
    assert is_winning_hand(hand, [], Suit.TIAO).ok
    fr = compute_fan(hand, [], Suit.TIAO)
    assert fr.details.get("gen", 0) >= 1


def test_f07_fan_cap() -> None:
    hand = expand(("wan", [1, 1, 1, 3, 3, 3, 5, 5, 5, 7, 7, 7, 9, 9]))
    fr = compute_fan(hand, [], Suit.TIAO, fan_cap=2)
    assert fr.fan_raw >= 3
    assert fr.fan == 2
    assert apply_fan_cap(5, 0) == 5
    assert apply_fan_cap(5, 3) == 3


def test_f08_gang_shang_hua() -> None:
    hand = standard_ping_hu()
    fr = compute_fan(
        hand, [], Suit.TIAO, context=WinContext(is_gang_shang_hua=True)
    )
    assert "gang_shang_hua" in fr.yaku
    assert fr.fan_raw >= 1


def test_f09_fan_on_non_win() -> None:
    hand = expand(("wan", [1, 2, 3, 4, 5, 6, 7, 8, 9]), ("tong", [1, 2, 3, 4, 5]))
    with pytest.raises(FanError):
        compute_fan(hand, [], Suit.TIAO)


def test_jin_gou_diao() -> None:
    melds = [
        MeldView("pong", T("wan", 1)),
        MeldView("pong", T("wan", 3)),
        MeldView("pong", T("wan", 5)),
        MeldView("ming_gang", T("wan", 7)),
    ]
    hand = [T("tong", 2), T("tong", 2)]
    r = is_winning_hand(hand, melds, Suit.TIAO)
    assert r.ok
    fr = compute_fan(hand, melds, Suit.TIAO)
    assert "jin_gou_diao" in fr.yaku
