"""Shanten (distance to tenpai/win) with dingque handling."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Sequence

from engine.hand_utils import (
    MeldView,
    NUM_FACES,
    copy_counts,
    index_to_tile,
    melds_from_raw,
    suit_indices,
    tiles_to_counts,
)
from engine.tile import Suit, Tile
from engine.win_check import is_seven_pairs_form, is_standard_form, is_winning_hand

_INF = 99


@dataclass(frozen=True, slots=True)
class ShantenResult:
    shanten: int
    standard: int
    seven_pairs: int
    ukeire: frozenset[Tile] | None


def _seven_pairs_shanten(counts: Sequence[int]) -> int:
    c = list(counts)
    total = sum(c)
    if total == 14 and is_seven_pairs_form(c):
        return -1
    pairs = sum(x // 2 for x in c)
    s = 6 - pairs
    if total == 14:
        # one away from pairs structure if almost
        return max(s, 0)
    return max(s, 0)


def _is_tenpai_standard(counts: list[int], open_melds: int) -> bool:
    """13-tile (or equivalent) hand is tenpai if some +1 tile completes."""
    need = 4 - open_melds
    target = 3 * need + 2
    if sum(counts) != target - 1:
        return False
    c = counts
    for i in range(NUM_FACES):
        if c[i] >= 4:
            continue
        c[i] += 1
        ok = is_standard_form(c, open_melds)
        c[i] -= 1
        if ok:
            return True
    return False


def _dfs_mentsu_shanten(counts: tuple[int, ...], need: int) -> int:
    """
    Classic left-tile decomposition shanten (standard form).
    need = number of melds still required from closed hand (4 - open).
    """

    @lru_cache(maxsize=None)
    def search(state: tuple[int, ...], melds: int, taatsu: int, pair: int) -> int:
        arr = list(state)
        i = 0
        while i < NUM_FACES and arr[i] == 0:
            i += 1
        if i >= NUM_FACES:
            m = melds
            t = taatsu
            p = pair
            if m > need:
                return _INF
            # Cap useful taatsu / pair (standard formula)
            # containers: need melds + 1 pair head
            max_taatsu = need - m
            if max_taatsu < 0:
                max_taatsu = 0
            t = min(t, max_taatsu)
            # total blocks m+t+p should not exceed need+1
            if m + t + p > need + 1:
                t = max(0, need + 1 - m - p)
            s = 2 * (need - m) - t - p
            return max(s, -1)

        best = _INF
        n = arr[i]

        # isolated / discard one
        if n >= 1:
            arr[i] -= 1
            best = min(best, search(tuple(arr), melds, taatsu, pair))
            arr[i] += 1

        # pair head
        if n >= 2 and pair == 0:
            arr[i] -= 2
            best = min(best, search(tuple(arr), melds, taatsu, 1))
            arr[i] += 2

        # pong
        if n >= 3:
            arr[i] -= 3
            best = min(best, search(tuple(arr), melds + 1, taatsu, pair))
            arr[i] += 3

        # chow
        rank = i % 9
        if rank <= 6 and arr[i] and arr[i + 1] and arr[i + 2]:
            arr[i] -= 1
            arr[i + 1] -= 1
            arr[i + 2] -= 1
            best = min(best, search(tuple(arr), melds + 1, taatsu, pair))
            arr[i] += 1
            arr[i + 1] += 1
            arr[i + 2] += 1

        # adjacent taatsu
        if rank <= 7 and arr[i] and arr[i + 1]:
            arr[i] -= 1
            arr[i + 1] -= 1
            best = min(best, search(tuple(arr), melds, taatsu + 1, pair))
            arr[i] += 1
            arr[i + 1] += 1

        # kanchan taatsu
        if rank <= 6 and arr[i] and arr[i + 2]:
            arr[i] -= 1
            arr[i + 2] -= 1
            best = min(best, search(tuple(arr), melds, taatsu + 1, pair))
            arr[i] += 1
            arr[i + 2] += 1

        # dual pair as taatsu (shanpon component) when pair head already chosen
        if n >= 2 and pair == 1:
            arr[i] -= 2
            best = min(best, search(tuple(arr), melds, taatsu + 1, pair))
            arr[i] += 2

        return best

    return search(tuple(counts), 0, 0, 0)


def _standard_shanten(counts: list[int], open_melds: int) -> int:
    need = 4 - open_melds
    if need < 0:
        return _INF
    target = 3 * need + 2
    total = sum(counts)
    c = copy_counts(counts)

    if total == target and is_standard_form(c, open_melds):
        return -1

    # Exact tenpai for one-tile-short hands
    if total == target - 1 and _is_tenpai_standard(c, open_melds):
        return 0

    # 14-tile non-winning: min shanten after one discard
    if total == target:
        best = _INF
        for i in range(NUM_FACES):
            if c[i] <= 0:
                continue
            c[i] -= 1
            best = min(best, _standard_shanten(c, open_melds))
            c[i] += 1
        return best

    # General DFS (works for 1-shanten+ and odd sizes)
    return _dfs_mentsu_shanten(tuple(c), need)


def _apply_dingque_mask(
    counts: list[int], dingque: Suit | None
) -> tuple[list[int], int]:
    if dingque is None:
        return counts, 0
    c = copy_counts(counts)
    dq = 0
    for i in suit_indices(dingque):
        dq += c[i]
        c[i] = 0
    return c, dq


def compute_shanten(
    hand: list[Tile],
    melds: Sequence | None = None,
    dingque: Suit | None = None,
) -> ShantenResult:
    meld_views = melds_from_raw(melds or [])
    open_n = len(meld_views)
    counts = tiles_to_counts(hand)

    win = is_winning_hand(hand, meld_views, dingque)
    if win.ok:
        sp = -1 if win.form and win.form.value == "seven_pairs" else _INF
        std = -1 if win.form and win.form.value == "standard" else _INF
        return ShantenResult(-1, std if std < _INF else -1, sp if sp < _INF else -1, frozenset())

    masked, dq_n = _apply_dingque_mask(counts, dingque)
    std = _standard_shanten(masked, open_n)
    if dq_n and std < _INF:
        std = std + dq_n

    if open_n == 0:
        sp_counts = copy_counts(counts)
        if dingque is not None:
            dq_tiles = sum(counts[i] for i in suit_indices(dingque))
            for i in suit_indices(dingque):
                sp_counts[i] = 0
            sp = _seven_pairs_shanten(sp_counts)
            if dq_tiles:
                sp = sp + dq_tiles if sp < _INF else _INF
        else:
            sp = _seven_pairs_shanten(sp_counts)
    else:
        sp = _INF

    overall = min(std, sp)
    if overall >= _INF:
        overall = 8

    ukeire: frozenset[Tile] | None
    if overall == 0:
        ukeire = _compute_ukeire(hand, meld_views, dingque)
    else:
        ukeire = None

    return ShantenResult(
        shanten=overall,
        standard=std if std < _INF else 8,
        seven_pairs=sp if sp < _INF else 8,
        ukeire=ukeire,
    )


def _compute_ukeire(
    hand: list[Tile],
    melds: list[MeldView],
    dingque: Suit | None,
) -> frozenset[Tile]:
    open_n = len(melds)
    need_len = 14 - 3 * open_n
    total = len(hand)
    if total != need_len - 1:
        return frozenset()

    base_counts = tiles_to_counts(hand)
    useful: set[Tile] = set()
    for i in range(NUM_FACES):
        if base_counts[i] >= 4:
            continue
        t = index_to_tile(i)
        if dingque is not None and t.suit == dingque:
            continue
        trial = hand + [t]
        if is_winning_hand(trial, melds, dingque).ok:
            useful.add(t)
    return frozenset(useful)


def shanten(
    hand: list[Tile],
    melds: Sequence | None = None,
    dingque: Suit | None = None,
) -> ShantenResult:
    return compute_shanten(hand, melds, dingque)
