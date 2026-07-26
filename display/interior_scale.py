"""Interior element scale from 1080p baseline (F0019).

Layout ratios unchanged; pixel sizes scale with client area:

    S = min(Cw/Cw0, Ch/Ch0)

Baseline client sizes (UI_DESIGN_STANDARD §8.2, complete mode):
    MAIN / human Full: 885×498
    AI Full:           442×249
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

WindowRole = Literal["main", "play", "watch"]

# --- 1080p default client sizes (also application minsize) ---
MAIN_REF_W, MAIN_REF_H = 885, 498
HUMAN_REF_W, HUMAN_REF_H = 885, 498
AI_REF_W, AI_REF_H = 442, 249

# --- Base element sizes at S=1 (chosen to fit full content in baseline) ---
MAIN_BASE_TILE_W = 28
MAIN_TILE_FLOOR = 12
MAIN_TILE_CEIL = 96

PLAY_BASE_HAND_TW = 26
PLAY_BASE_DISC_TW = 20
# Keep fonts modest so 885×498 zones stay balanced (user: 部分字体过大)
PLAY_BASE_FONT = 9
PLAY_BASE_FONT_LG = 11
PLAY_BASE_PAD = 4
PLAY_TILE_FLOOR = 10
PLAY_DISC_FLOOR = 8

AI_BASE_HAND_TW = 16
AI_BASE_DISC_TW = 12
AI_BASE_FONT = 8
AI_BASE_FONT_LG = 9
AI_BASE_PAD = 2
AI_TILE_FLOOR = 10
AI_DISC_FLOOR = 8

FONT_FLOOR = 7
FONT_LG_FLOOR = 8
FONT_CEIL = 12
FONT_LG_CEIL = 14


def ref_size(role: WindowRole) -> tuple[int, int]:
    if role == "main":
        return MAIN_REF_W, MAIN_REF_H
    if role == "play":
        return HUMAN_REF_W, HUMAN_REF_H
    return AI_REF_W, AI_REF_H


def scale_factor(
    client_w: int,
    client_h: int,
    role: WindowRole = "main",
) -> float:
    """S = min(Cw/Cw0, Ch/Ch0); always > 0."""
    rw, rh = ref_size(role)
    cw = max(1, int(client_w))
    ch = max(1, int(client_h))
    return min(cw / float(rw), ch / float(rh))


def scale_px(base: float, s: float, *, floor: int = 1, ceil: int | None = None) -> int:
    v = int(round(float(base) * float(s)))
    v = max(int(floor), v)
    if ceil is not None:
        v = min(int(ceil), v)
    return v


@dataclass(frozen=True, slots=True)
class MainScale:
    s: float
    tile_w: int
    tile_h: int
    font_title: int
    font_body: int
    font_small: int
    row_h: int
    pad: int
    gap: int


def main_scale(client_w: int, client_h: int) -> MainScale:
    s = scale_factor(client_w, client_h, "main")
    tw = scale_px(MAIN_BASE_TILE_W, s, floor=MAIN_TILE_FLOOR, ceil=MAIN_TILE_CEIL)
    th = max(1, int(round(tw * 1.4)))
    return MainScale(
        s=s,
        tile_w=tw,
        tile_h=th,
        font_title=scale_px(15, s, floor=FONT_LG_FLOOR),
        font_body=scale_px(12, s, floor=FONT_FLOOR),
        font_small=scale_px(11, s, floor=FONT_FLOOR),
        row_h=scale_px(24, s, floor=16),
        pad=scale_px(6, s, floor=2),
        gap=scale_px(3, s, floor=1),
    )


@dataclass(frozen=True, slots=True)
class SeatScale:
    s: float
    role: WindowRole
    hand_tw: int
    hand_tw_max: int
    disc_tw: int
    font: int
    font_lg: int
    pad: int
    gap: int
    btn_h: int
    settings_h: int


def seat_scale(client_w: int, client_h: int, *, mode: str) -> SeatScale:
    role: WindowRole = "play" if mode == "play" else "watch"
    s = scale_factor(client_w, client_h, role)
    # Cap S for typography so oversized client never blows up text
    s_font = min(s, 1.0)
    if role == "play":
        hand = scale_px(PLAY_BASE_HAND_TW, s, floor=PLAY_TILE_FLOOR, ceil=40)
        disc = scale_px(PLAY_BASE_DISC_TW, s, floor=PLAY_DISC_FLOOR, ceil=32)
        font = scale_px(PLAY_BASE_FONT, s_font, floor=FONT_FLOOR, ceil=FONT_CEIL)
        font_lg = scale_px(
            PLAY_BASE_FONT_LG, s_font, floor=FONT_LG_FLOOR, ceil=FONT_LG_CEIL
        )
        pad = scale_px(PLAY_BASE_PAD, s, floor=2)
        # Single-row action strip height
        btn_h = scale_px(28, s, floor=22, ceil=34)
        settings_h = scale_px(40, s, floor=28, ceil=52)
    else:
        hand = scale_px(AI_BASE_HAND_TW, s, floor=AI_TILE_FLOOR, ceil=28)
        disc = scale_px(AI_BASE_DISC_TW, s, floor=AI_DISC_FLOOR, ceil=22)
        font = scale_px(AI_BASE_FONT, s_font, floor=FONT_FLOOR, ceil=FONT_CEIL)
        font_lg = scale_px(
            AI_BASE_FONT_LG, s_font, floor=FONT_LG_FLOOR, ceil=FONT_LG_CEIL
        )
        pad = scale_px(AI_BASE_PAD, s, floor=1)
        btn_h = scale_px(26, s, floor=20, ceil=32)
        settings_h = scale_px(32, s, floor=24, ceil=40)
    gap = max(1, scale_px(3, s, floor=1))
    return SeatScale(
        s=s,
        role=role,
        hand_tw=hand,
        hand_tw_max=max(hand, int(round(hand * 1.15))),
        disc_tw=disc,
        font=font,
        font_lg=font_lg,
        pad=pad,
        gap=gap,
        btn_h=btn_h,
        settings_h=settings_h,
    )
