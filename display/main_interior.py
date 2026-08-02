"""Main window interior geometry — TABLE 80% / SIDE 20% + DICE + sectors (F0015/F0018)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Slot = Literal["bottom", "right", "top", "left"]

SIDE_TOP_RATIO = 0.35
SIDE_MID_RATIO = 0.30
SIDE_BOT_RATIO = 0.35
TABLE_RATIO = 0.80
DICE_K = 0.28


@dataclass(frozen=True, slots=True)
class Rect:
    x: int
    y: int
    w: int
    h: int

    @property
    def right(self) -> int:
        return self.x + self.w

    @property
    def bottom(self) -> int:
        return self.y + self.h

    def as_tuple(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.w, self.h

    def center(self) -> tuple[int, int]:
        return self.x + self.w // 2, self.y + self.h // 2


@dataclass(frozen=True, slots=True)
class ZoneStrips:
    """From table-edge outward inward: hand → meld → discard (toward DICE)."""

    hand: Rect
    meld: Rect
    disc: Rect


@dataclass(frozen=True, slots=True)
class MainInteriorLayout:
    client_w: int
    client_h: int
    table: Rect
    side: Rect
    side_top: Rect
    side_mid: Rect
    side_bot: Rect
    dice: Rect
    tile_w: int
    tile_h: int
    # sector outer AABB by slot (bottom/right/top/left)
    sectors: dict[str, Rect]
    strips: dict[str, ZoneStrips]

    @property
    def panel_w(self) -> int:
        return self.side.w

    @property
    def content_w(self) -> int:
        return self.table.w


def compute_main_interior(
    Cw: int,
    Ch: int,
    *,
    tile_w: int = 44,
    dice_k: float = DICE_K,
    side_collapsed: bool = False,
    collapsed_side_w: int = 28,
) -> MainInteriorLayout:
    """
    Pure geometry for MAIN client area.

    - TABLE 80% / SIDE 20% (SIDE absorbs remainder)
    - SIDE vertical: top 35% / mid 30% / bot 35%
    - DICE: concentric square k*min(Tw,Th)
    - Four sector AABBs + hand/meld/disc strips (outer→inner)
    """
    Cw = max(200, int(Cw))
    Ch = max(160, int(Ch))
    tw = max(24, int(tile_w))
    th = max(1, int(round(tw * 1.4)))

    if side_collapsed:
        Sw = max(0, int(collapsed_side_w))
        Tw = max(80, Cw - Sw)
    else:
        # Strict 80/20: TABLE absorbs floor, SIDE gets remainder (=20%±1px)
        Tw = int(Cw * TABLE_RATIO)
        Sw = Cw - Tw
        if Sw < 40 and Cw >= 200:
            Sw = max(40, int(round(Cw * 0.20)))
            Tw = Cw - Sw

    table = Rect(0, 0, Tw, Ch)
    side = Rect(Tw, 0, Sw, Ch)

    sh_top = int(Ch * SIDE_TOP_RATIO)
    sh_mid = int(Ch * SIDE_MID_RATIO)
    sh_bot = Ch - sh_top - sh_mid
    side_top = Rect(Tw, 0, Sw, sh_top)
    side_mid = Rect(Tw, sh_top, Sw, sh_mid)
    side_bot = Rect(Tw, sh_top + sh_mid, Sw, sh_bot)

    D = max(24, int(min(Tw, Ch) * float(dice_k)))
    Dx = Tw // 2 - D // 2
    Dy = Ch // 2 - D // 2
    dice = Rect(Dx, Dy, D, D)

    # Sector AABBs: TABLE minus DICE, four sides
    # bottom (south): full width, from dice.bottom to table.bottom
    bottom = Rect(0, dice.bottom, Tw, max(1, Ch - dice.bottom))
    top = Rect(0, 0, Tw, max(1, dice.y))
    left = Rect(0, dice.y, max(1, dice.x), D)
    right = Rect(dice.right, dice.y, max(1, Tw - dice.right), D)
    sectors = {
        "bottom": bottom,
        "top": top,
        "left": left,
        "right": right,
    }

    pad = max(2, tw // 12)
    strips: dict[str, ZoneStrips] = {}
    for slot, sec in sectors.items():
        strips[slot] = _sector_strips(sec, slot, tile_h=th, pad=pad)

    # Frame hands: L/R use full table height (same tile face budget as T/B for 14 tiles);
    # T/B hands inset by L/R thickness so four hand bands do not overlap at corners.
    strips = _frame_hand_strips(strips, table_w=Tw, table_h=Ch)

    return MainInteriorLayout(
        client_w=Cw,
        client_h=Ch,
        table=table,
        side=side,
        side_top=side_top,
        side_mid=side_mid,
        side_bot=side_bot,
        dice=dice,
        tile_w=tw,
        tile_h=th,
        sectors=sectors,
        strips=strips,
    )


def _frame_hand_strips(
    strips: dict[str, ZoneStrips],
    *,
    table_w: int,
    table_h: int,
) -> dict[str, ZoneStrips]:
    """
    Place ZONE_HAND as a non-overlapping frame:

    - left/right: full table height, thickness from sector strip
    - top/bottom: full remaining width between L/R hands, thickness from sector strip

    Meld/disc for top/bottom are inset to the same horizontal span so they do not
    sit under L/R hands. L/R meld/disc stay mid-sector (toward DICE).
    """
    top = strips["top"]
    bot = strips["bottom"]
    left = strips["left"]
    right = strips["right"]

    w_lr = max(8, left.hand.w)
    h_tb = max(8, top.hand.h)
    # Prefer matching thicknesses from opposite seats when slightly different
    w_lr = max(w_lr, right.hand.w)
    h_tb = max(h_tb, bot.hand.h)

    x0 = w_lr
    x1 = max(x0 + 1, table_w - w_lr)
    span_tb = max(1, x1 - x0)

    left_hand = Rect(0, 0, w_lr, table_h)
    right_hand = Rect(table_w - w_lr, 0, w_lr, table_h)
    top_hand = Rect(x0, 0, span_tb, h_tb)
    bot_hand = Rect(x0, table_h - h_tb, span_tb, h_tb)

    def _inset_x(r: Rect) -> Rect:
        nx = max(r.x, x0)
        nr = min(r.right, x1)
        return Rect(nx, r.y, max(1, nr - nx), r.h)

    return {
        "top": ZoneStrips(
            hand=top_hand,
            meld=_inset_x(top.meld),
            disc=_inset_x(top.disc),
        ),
        "bottom": ZoneStrips(
            hand=bot_hand,
            meld=_inset_x(bot.meld),
            disc=_inset_x(bot.disc),
        ),
        "left": ZoneStrips(
            hand=left_hand,
            meld=left.meld,
            disc=left.disc,
        ),
        "right": ZoneStrips(
            hand=right_hand,
            meld=right.meld,
            disc=right.disc,
        ),
    }


def _sector_strips(sec: Rect, slot: str, *, tile_h: int, pad: int) -> ZoneStrips:
    """
    Outer (table edge) → inner (toward DICE): HAND (1 row) / MELD (2 rows) / DISC (rest).
    """
    H_hand = tile_h + pad
    H_meld = 2 * tile_h + pad
    H_disc_min = max(tile_h // 2, tile_h + pad // 2)

    if slot in ("bottom", "top"):
        span = sec.h
        h_hand = min(H_hand, max(8, span // 4))
        h_meld = min(H_meld, max(8, span // 3))
        if h_hand + h_meld + H_disc_min > span:
            h_hand = min(h_hand, max(8, span // 3))
            h_meld = min(h_meld, max(8, span // 3))
        h_disc = max(H_disc_min, span - h_hand - h_meld)
        # rebalance if overshoot
        if h_hand + h_meld + h_disc > span:
            h_disc = max(4, span - h_hand - h_meld)
        if slot == "bottom":
            # outer at bottom of sector
            y_hand = sec.y + sec.h - h_hand
            y_meld = y_hand - h_meld
            y_disc = sec.y
            h_disc = max(4, y_meld - y_disc)
            return ZoneStrips(
                hand=Rect(sec.x, y_hand, sec.w, h_hand),
                meld=Rect(sec.x, y_meld, sec.w, h_meld),
                disc=Rect(sec.x, y_disc, sec.w, h_disc),
            )
        # top: outer at top
        y_hand = sec.y
        y_meld = y_hand + h_hand
        y_disc = y_meld + h_meld
        h_disc = max(4, sec.bottom - y_disc)
        return ZoneStrips(
            hand=Rect(sec.x, y_hand, sec.w, h_hand),
            meld=Rect(sec.x, y_meld, sec.w, h_meld),
            disc=Rect(sec.x, y_disc, sec.w, h_disc),
        )

    # left / right — thickness along horizontal
    span = sec.w
    h_hand = min(H_hand, max(8, span // 4))
    h_meld = min(H_meld, max(8, span // 3))
    if h_hand + h_meld + H_disc_min > span:
        h_hand = min(h_hand, max(8, span // 3))
        h_meld = min(h_meld, max(8, span // 3))
    if slot == "left":
        # outer = left edge
        x_hand = sec.x
        x_meld = x_hand + h_hand
        x_disc = x_meld + h_meld
        w_disc = max(4, sec.right - x_disc)
        return ZoneStrips(
            hand=Rect(x_hand, sec.y, h_hand, sec.h),
            meld=Rect(x_meld, sec.y, h_meld, sec.h),
            disc=Rect(x_disc, sec.y, w_disc, sec.h),
        )
    # right: outer = right edge
    x_hand = sec.right - h_hand
    x_meld = x_hand - h_meld
    x_disc = sec.x
    w_disc = max(4, x_meld - x_disc)
    return ZoneStrips(
        hand=Rect(x_hand, sec.y, h_hand, sec.h),
        meld=Rect(x_meld, sec.y, h_meld, sec.h),
        disc=Rect(x_disc, sec.y, w_disc, sec.h),
    )


def slot_tile_rotation(slot: str) -> int:
    if slot == "left":
        return -90
    if slot == "right":
        return 90
    if slot == "top":
        return 180
    return 0
