"""Winning hand form check (standard + seven pairs) with dingque."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from engine.hand_utils import (
    MeldView,
    NUM_FACES,
    copy_counts,
    expected_hand_len,
    melds_from_raw,
    melds_have_suit,
    tiles_to_counts,
)
from engine.tile import Suit, Tile


class WinForm(str, Enum):
    STANDARD = "standard"
    SEVEN_PAIRS = "seven_pairs"


@dataclass(frozen=True, slots=True)
class WinCheckResult:
    ok: bool
    form: WinForm | None
    reason: str | None = None


def _extract_melds(counts: list[int], n: int) -> bool:
    """Whether counts can be partitioned into exactly n melds (pong/chow)."""
    if n == 0:
        return all(c == 0 for c in counts)

    i = next((j for j in range(NUM_FACES) if counts[j] > 0), None)
    if i is None:
        return False

    # Pong / kezi
    if counts[i] >= 3:
        counts[i] -= 3
        if _extract_melds(counts, n - 1):
            counts[i] += 3
            return True
        counts[i] += 3

    # Chow / shuntsu (i as leftmost)
    rank = i % 9
    if rank <= 6 and counts[i] >= 1 and counts[i + 1] >= 1 and counts[i + 2] >= 1:
        counts[i] -= 1
        counts[i + 1] -= 1
        counts[i + 2] -= 1
        if _extract_melds(counts, n - 1):
            counts[i] += 1
            counts[i + 1] += 1
            counts[i + 2] += 1
            return True
        counts[i] += 1
        counts[i + 1] += 1
        counts[i + 2] += 1

    return False


def is_standard_form(counts: Sequence[int], num_open_melds: int) -> bool:
    need = 4 - num_open_melds
    if need < 0:
        return False
    c = copy_counts(counts)
    total = sum(c)
    if total != 3 * need + 2:
        return False
    for i in range(NUM_FACES):
        if c[i] >= 2:
            c[i] -= 2
            if _extract_melds(c, need):
                c[i] += 2
                return True
            c[i] += 2
    return False


def is_seven_pairs_form(counts: Sequence[int]) -> bool:
    if sum(counts) != 14:
        return False
    pairs = 0
    for x in counts:
        if x % 2 != 0:
            return False
        pairs += x // 2
    return pairs == 7


def _has_chow_meld(melds: Sequence[MeldView]) -> bool:
    return any(m.kind == "chow" for m in melds)


def is_winning_hand(
    hand: list[Tile],
    melds: Sequence | None,
    dingque: Suit | None,
    *,
    allow_seven_pairs: bool = True,
) -> WinCheckResult:
    meld_views = melds_from_raw(melds or [])
    if _has_chow_meld(meld_views):
        return WinCheckResult(False, None, "CHOW_NOT_ALLOWED")

    if dingque is None:
        return WinCheckResult(False, None, "NO_DINGQUE")

    if any(t.suit == dingque for t in hand) or melds_have_suit(meld_views, dingque):
        return WinCheckResult(False, None, "HAS_DINGQUE")

    n_melds = len(meld_views)
    exp = expected_hand_len(n_melds)
    if len(hand) != exp:
        return WinCheckResult(False, None, "BAD_HAND_LEN")

    counts = tiles_to_counts(hand)

    if n_melds == 0 and allow_seven_pairs and is_seven_pairs_form(counts):
        return WinCheckResult(True, WinForm.SEVEN_PAIRS, None)

    if is_standard_form(counts, n_melds):
        return WinCheckResult(True, WinForm.STANDARD, None)

    return WinCheckResult(False, None, "NOT_COMPLETE")


def can_form_all_koutsu(counts: Sequence[int], num_open_melds: int) -> bool:
    """True if standard win with only pongs/gangs + pair (对对胡 shape in closed)."""
    need = 4 - num_open_melds
    c = copy_counts(counts)
    if sum(c) != 3 * need + 2:
        return False
    # pair + only pongs
    for i in range(NUM_FACES):
        if c[i] >= 2:
            c[i] -= 2
            ok = True
            rem = list(c)
            melds = 0
            for j in range(NUM_FACES):
                while rem[j] >= 3:
                    rem[j] -= 3
                    melds += 1
                if rem[j] != 0:
                    ok = False
                    break
            c[i] += 2
            if ok and melds == need:
                return True
    return False
