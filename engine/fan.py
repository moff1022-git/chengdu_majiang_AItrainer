"""Chengdu blood-battle fan calculation with configurable table and cap."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

from engine.hand_utils import (
    MeldView,
    NUM_FACES,
    melds_from_raw,
    tile_index,
    tiles_to_counts,
)
from engine.tile import Suit, Tile
from engine.win_check import (
    WinForm,
    can_form_all_koutsu,
    is_winning_hand,
)

_DEFAULT_TABLE_PATH = (
    Path(__file__).resolve().parent.parent / "configs" / "fan_table.json"
)


class FanError(ValueError):
    """Fan computation on non-winning hand or invalid input."""


@dataclass(frozen=True, slots=True)
class WinContext:
    is_zimo: bool = False
    is_gang_shang_hua: bool = False
    is_gang_shang_pao: bool = False
    is_qiang_gang: bool = False
    is_hai_di: bool = False
    root_extra: int = 0


@dataclass(frozen=True, slots=True)
class FanResult:
    fan: int
    fan_raw: int
    yaku: list[str]
    details: dict[str, int]


@dataclass
class FanTable:
    version: int
    yaku: dict[str, int]

    def get(self, key: str, default: int = 0) -> int:
        return int(self.yaku.get(key, default))

    @classmethod
    def from_dict(cls, data: dict) -> FanTable:
        return cls(version=int(data.get("version", 1)), yaku=dict(data.get("yaku") or {}))

    @classmethod
    def load(cls, path: Path | str | None = None) -> FanTable:
        p = Path(path) if path else _DEFAULT_TABLE_PATH
        with p.open(encoding="utf-8") as f:
            return cls.from_dict(json.load(f))


_default_table: FanTable | None = None


def default_fan_table() -> FanTable:
    global _default_table
    if _default_table is None:
        _default_table = FanTable.load()
    return _default_table


def apply_fan_cap(raw: int, cap: int) -> int:
    if cap is None or cap <= 0:
        return raw
    return min(raw, cap)


def _all_tiles(hand: list[Tile], melds: list[MeldView]) -> list[Tile]:
    out = list(hand)
    for m in melds:
        if m.is_gang:
            out.extend([m.tile] * 4)
        elif m.kind == "pong":
            out.extend([m.tile] * 3)
        else:
            out.append(m.tile)
    return out


def _count_gen(hand: list[Tile], melds: list[MeldView]) -> int:
    """Roots: each 4-of-a-kind in hand+melds (gang counts once)."""
    counts = tiles_to_counts(hand)
    gen = 0
    for m in melds:
        if m.is_gang:
            gen += 1
            # gang tiles not in hand; already counted
        elif m.kind == "pong":
            # pong + 1 in hand could make gen — include pong as 3 in pool
            counts[tile_index(m.tile)] += 3
    for c in counts:
        if c >= 4:
            gen += 1
    return gen


def _is_yao(tile: Tile) -> bool:
    return tile.rank in (1, 9)


def _is_qing_yi_se(hand: list[Tile], melds: list[MeldView]) -> bool:
    tiles = _all_tiles(hand, melds)
    if not tiles:
        return False
    s0 = tiles[0].suit
    return all(t.suit == s0 for t in tiles)


def _is_duan_yao(hand: list[Tile], melds: list[MeldView]) -> bool:
    return all(not _is_yao(t) for t in _all_tiles(hand, melds))


def _is_dai_yao_standard(
    hand: list[Tile], melds: list[MeldView], counts: list[int]
) -> bool:
    """
    带幺九: every meld and the pair includes a terminal (1/9).
    Approximate: all open melds yao-based; closed hand pure yao structure check
    via requiring every tile group involves 1/9 — strict: no middle-only melds.
    """
    for m in melds:
        if m.kind == "chow":
            return False
        if not _is_yao(m.tile):
            return False
    # For closed part: all tiles must be 1 or 9 for pure 带幺 (common digital rule
    # for 带幺九 often means 全带幺: every set contains 幺九)
    # Check via decomposition: only use 1/9 tiles and chows that include them
    # Simplified strong rule used by many apps: every tile in hand+melds is 1 or 9
    # for 老头 / 更严; 带幺九 allows 123, 789 chows.
    # We implement 全带幺: try to verify structure with yao constraint in melds.
    return _all_sets_contain_yao(hand, melds)


def _all_sets_contain_yao(hand: list[Tile], melds: list[MeldView]) -> bool:
    """True if there exists a standard decomposition where each set has a terminal."""
    for m in melds:
        if m.kind == "chow":
            # chow tile is leftmost stored — not enough info; reject chow melds for dai yao unless tile is 1 or 7
            if m.tile.rank not in (1, 7):
                return False
            # 123 has 1, 789 has 9 when leftmost 7
        elif not _is_yao(m.tile):
            return False

    counts = tiles_to_counts(hand)
    need = 4 - len(melds)
    return _decomp_all_yao(counts, need, False)


def _decomp_all_yao(counts: list[int], melds_left: int, has_pair: bool) -> bool:
    if melds_left == 0:
        if has_pair:
            return sum(counts) == 0
        # need pair of yao
        for i in range(NUM_FACES):
            if counts[i] >= 2 and index_is_yao(i):
                counts[i] -= 2
                ok = sum(counts) == 0
                counts[i] += 2
                if ok:
                    return True
        return False

    if not has_pair:
        for i in range(NUM_FACES):
            if counts[i] >= 2 and index_is_yao(i):
                counts[i] -= 2
                if _decomp_all_yao(counts, melds_left, True):
                    counts[i] += 2
                    return True
                counts[i] += 2

    i = next((j for j in range(NUM_FACES) if counts[j] > 0), None)
    if i is None:
        return False

    if counts[i] >= 3 and index_is_yao(i):
        counts[i] -= 3
        if _decomp_all_yao(counts, melds_left - 1, has_pair):
            counts[i] += 3
            return True
        counts[i] += 3

    rank = i % 9
    # chow containing yao: 123 (left 1) or 789 (left 7)
    if rank == 0 and counts[i] and counts[i + 1] and counts[i + 2]:
        counts[i] -= 1
        counts[i + 1] -= 1
        counts[i + 2] -= 1
        if _decomp_all_yao(counts, melds_left - 1, has_pair):
            counts[i] += 1
            counts[i + 1] += 1
            counts[i + 2] += 1
            return True
        counts[i] += 1
        counts[i + 1] += 1
        counts[i + 2] += 1
    if rank == 6 and counts[i] and counts[i + 1] and counts[i + 2]:
        counts[i] -= 1
        counts[i + 1] -= 1
        counts[i + 2] -= 1
        if _decomp_all_yao(counts, melds_left - 1, has_pair):
            counts[i] += 1
            counts[i + 1] += 1
            counts[i + 2] += 1
            return True
        counts[i] += 1
        counts[i + 1] += 1
        counts[i + 2] += 1

    return False


def index_is_yao(i: int) -> bool:
    r = i % 9
    return r == 0 or r == 8


def _is_dui_dui(
    hand: list[Tile], melds: list[MeldView], form: WinForm
) -> bool:
    if form != WinForm.STANDARD:
        return False
    for m in melds:
        if m.kind == "chow":
            return False
        if not m.is_pong_or_gang:
            return False
    return can_form_all_koutsu(tiles_to_counts(hand), len(melds))


def compute_fan(
    hand: list[Tile],
    melds: Sequence | None,
    dingque: Suit | None,
    win_tile: Tile | None = None,
    context: WinContext | None = None,
    *,
    fan_table: FanTable | None = None,
    fan_cap: int | None = 0,
) -> FanResult:
    meld_views = melds_from_raw(melds or [])
    check = is_winning_hand(hand, meld_views, dingque)
    if not check.ok or check.form is None:
        raise FanError(f"not a winning hand: {check.reason}")

    table = fan_table or default_fan_table()
    ctx = context or WinContext()
    details: dict[str, int] = {}
    yaku: list[str] = []

    def add(key: str, mult: int = 1) -> None:
        pts = table.get(key, 0) * mult
        if key not in details:
            details[key] = 0
            yaku.append(key)
        details[key] += pts

    form = check.form

    if form == WinForm.SEVEN_PAIRS:
        add("qi_dui")
    else:
        if _is_dui_dui(hand, meld_views, form):
            add("dui_dui_hu")
        if len(hand) == 2 and len(meld_views) == 4:
            add("jin_gou_diao")

    if _is_qing_yi_se(hand, meld_views):
        add("qing_yi_se")

    if form == WinForm.STANDARD:
        if _is_duan_yao(hand, meld_views):
            add("duan_yao_jiu")
        elif _is_dai_yao_standard(hand, meld_views, tiles_to_counts(hand)):
            add("dai_yao_jiu")

    gen = _count_gen(hand, meld_views) + ctx.root_extra
    if gen > 0:
        add("gen", gen)

    if ctx.is_gang_shang_hua:
        add("gang_shang_hua")
    if ctx.is_gang_shang_pao:
        add("gang_shang_pao")
    if ctx.is_qiang_gang:
        add("qiang_gang")
    if ctx.is_hai_di:
        add("hai_di")

    # ping_hu only if no other hand yaku with points (context/gen may still apply)
    hand_yaku_points = sum(
        v
        for k, v in details.items()
        if k
        not in (
            "gen",
            "gang_shang_hua",
            "gang_shang_pao",
            "qiang_gang",
            "hai_di",
        )
    )
    if form == WinForm.STANDARD and hand_yaku_points == 0:
        add("ping_hu")

    raw = sum(details.values())
    capped = apply_fan_cap(raw, fan_cap if fan_cap is not None else 0)
    return FanResult(fan=capped, fan_raw=raw, yaku=yaku, details=details)
