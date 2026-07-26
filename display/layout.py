"""Layout helpers — TABLE 80%/SIDE 20% + sector strips (F0015/F0018/F0019)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from display.interior_scale import MAIN_REF_H, MAIN_REF_W, main_scale
from display.main_interior import MainInteriorLayout, compute_main_interior

# Legacy labels (F0007); actual tile size from F0019 scale
SCREEN_W = MAIN_REF_W
SCREEN_H = MAIN_REF_H

# Floors used by table_view asserts / callers
MIN_TABLE_TW = 12
MAX_TABLE_TW = 96
BASE_TABLE_TW = 28

SCREEN_SLOTS = ("bottom", "right", "top", "left")


@dataclass
class Layout:
    width: int = SCREEN_W
    height: int = SCREEN_H
    tile_w: int = BASE_TABLE_TW
    # Kept for backward compat; F0007 forces them equal to tile_w
    tile_small_w: int = BASE_TABLE_TW
    tile_tiny_w: int = BASE_TABLE_TW
    panel_w: int = 216
    content_w: int = SCREEN_W - 216
    scale: float = 1.0
    interior: MainInteriorLayout | None = field(default=None, repr=False)

    @classmethod
    def from_window(
        cls,
        width: int,
        height: int,
        *,
        panel_w: int | None = None,
        side_collapsed: bool = False,
    ) -> Layout:
        """80/20 interior; tile_w from F0019 scale vs 885×498 baseline."""
        width = max(200, int(width))
        height = max(160, int(height))
        ms = main_scale(width, height)
        tw = ms.tile_w

        if panel_w is None:
            interior = compute_main_interior(
                width, height, tile_w=tw, side_collapsed=side_collapsed
            )
            panel_w = interior.side.w
            content_w = interior.table.w
        else:
            panel_w = max(0, int(panel_w))
            content_w = max(80, width - panel_w)
            interior = compute_main_interior(
                width,
                height,
                tile_w=tw,
                side_collapsed=side_collapsed or panel_w <= 40,
                collapsed_side_w=panel_w if panel_w <= 40 else 28,
            )
            if not side_collapsed and panel_w > 40:
                panel_w = interior.side.w
                content_w = interior.table.w

        return cls(
            width=width,
            height=height,
            tile_w=tw,
            tile_small_w=tw,
            tile_tiny_w=tw,
            panel_w=panel_w,
            content_w=content_w,
            scale=ms.s,
            interior=interior,
        )

    def ensure_interior(self) -> MainInteriorLayout:
        if self.interior is None:
            self.interior = compute_main_interior(
                self.width, self.height, tile_w=self.tile_w
            )
        return self.interior

    @property
    def tile_h(self) -> int:
        return max(1, int(round(self.tile_w * 1.4)))

    def cell_size(self, *, rotate: int = 0) -> tuple[int, int]:
        """Drawn cell (w, h) after optional ±90 rotation."""
        tw, th = self.tile_w, self.tile_h
        if abs(int(rotate)) % 180 == 90:
            return th, tw
        return tw, th

    def center(self) -> tuple[int, int]:
        mi = self.ensure_interior()
        return mi.dice.center()

    def margin(self) -> int:
        return max(10, min(24, self.content_w // 48))

    def _strip(self, slot: str, which: str) -> tuple[int, int, int, int]:
        mi = self.ensure_interior()
        st = mi.strips.get(slot)
        if st is None:
            return (0, 0, 40, 40)
        r = getattr(st, which)
        return r.as_tuple()

    def top_band(self) -> tuple[int, int, int, int]:
        """Hand strip for top seat (outer edge)."""
        return self._strip("top", "hand")

    def bottom_band(self) -> tuple[int, int, int, int]:
        return self._strip("bottom", "hand")

    def left_band(self) -> tuple[int, int, int, int]:
        return self._strip("left", "hand")

    def right_band(self) -> tuple[int, int, int, int]:
        return self._strip("right", "hand")

    def center_band(self) -> tuple[int, int, int, int]:
        mi = self.ensure_interior()
        return mi.dice.as_tuple()

    def river_area(self, slot: str) -> tuple[int, int, int, int]:
        """Discard zone (inner strip toward DICE)."""
        return self._strip(slot, "disc")

    def meld_area(self, slot: str) -> tuple[int, int, int, int]:
        return self._strip(slot, "meld")

    def hand_area(self, slot: str) -> tuple[int, int, int, int]:
        """Legacy API: x, y, max_span, align."""
        if slot == "bottom":
            x, y, w, h = self.bottom_band()
            return (x, y, w, 0)
        if slot == "top":
            x, y, w, h = self.top_band()
            return (x, y, w, 0)
        if slot == "left":
            x, y, w, h = self.left_band()
            return (x, y, w, 1)
        x, y, w, h = self.right_band()
        return (x, y, w, 1)

    def avatar_pos(self, slot: str) -> tuple[int, int]:
        m = self.margin()
        if slot == "bottom":
            x, y, w, h = self.bottom_band()
            return (x, max(m, y - 40))
        if slot == "top":
            x, y, w, h = self.top_band()
            return (x + max(0, w - 70), max(4, y + h + 2))
        if slot == "left":
            x, y, w, h = self.left_band()
            return (max(0, x + w + 2), y)
        x, y, w, h = self.right_band()
        return (max(0, x - 64), y)

    def score_pos(self, slot: str) -> tuple[int, int]:
        ax, ay = self.avatar_pos(slot)
        if slot in ("left", "right"):
            return (ax, ay + 48)
        return (ax + 64, ay + 8)

    def side_regions(self) -> dict[str, tuple[int, int, int, int]]:
        mi = self.ensure_interior()
        return {
            "side": mi.side.as_tuple(),
            "top": mi.side_top.as_tuple(),
            "mid": mi.side_mid.as_tuple(),
            "bot": mi.side_bot.as_tuple(),
        }


def seat_to_slot(seat: int, focus_seat: int, num_players: int) -> str:
    """Map logical seat to screen slot; focus_seat appears at bottom."""
    if num_players == 2:
        return "bottom" if seat == focus_seat else "top"
    if num_players == 3:
        rel = (seat - focus_seat) % num_players
        return ("bottom", "right", "left")[rel]
    rel = (seat - focus_seat) % 4
    return ("bottom", "right", "top", "left")[rel]
