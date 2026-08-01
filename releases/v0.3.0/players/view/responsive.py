"""Responsive layout math for seat windows (F0006 / F0019).

Shared by Tk seat_window and pygame PlayerView.

Policy (F0019):
  - Caller supplies ``min_tw`` / ``max_tw`` already scaled from 1080p baseline.
  - Prefer fitting in area: if one row cannot hold all tiles at ``min_tw``,
    wrap to more rows (may still use min_tw; further shrink is caller's job).
  - When area is wide, tiles may grow up to ``max_tw``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# Defaults = F0019 play S=1 baseline (not hard floors; seat_window passes scaled)
DEFAULT_MIN_HAND_TW = 28
DEFAULT_MAX_HAND_TW = 36


@dataclass(frozen=True, slots=True)
class TileGrid:
    """How to place ``n`` tiles in a horizontal band of ``area_width``."""

    tw: int
    th: int
    per_row: int
    rows: int
    gap: int
    n: int

    @property
    def total_height(self) -> int:
        if self.n <= 0 or self.rows <= 0:
            return 0
        return self.rows * self.th + max(0, self.rows - 1) * self.gap

    def cell(self, index: int, *, origin_x: int = 0, origin_y: int = 0) -> tuple[int, int]:
        """Top-left of tile at index (row-major, left→right, top→bottom)."""
        if self.per_row <= 0:
            return origin_x, origin_y
        row = index // self.per_row
        col = index % self.per_row
        x = origin_x + col * (self.tw + self.gap)
        y = origin_y + row * (self.th + self.gap)
        return x, y

    def cell_bottom_up(
        self, index: int, *, origin_x: int = 0, bottom_y: int = 0
    ) -> tuple[int, int]:
        """
        Place rows stacked upward from ``bottom_y`` (bottom edge of last row).

        Used by PlayerView hand strip above the action bar.
        """
        if self.per_row <= 0 or self.n <= 0:
            return origin_x, bottom_y - self.th
        row_from_top = index // self.per_row
        col = index % self.per_row
        row_from_bottom = (self.rows - 1) - row_from_top
        x = origin_x + col * (self.tw + self.gap)
        y = bottom_y - self.th - row_from_bottom * (self.th + self.gap)
        return x, y


def compute_tile_grid(
    n: int,
    area_width: int,
    *,
    min_tw: int = DEFAULT_MIN_HAND_TW,
    max_tw: int = DEFAULT_MAX_HAND_TW,
    gap: int = 3,
    margin: int = 16,
    label_w: int = 0,
    aspect: float = 1.4,
    max_rows: int = 12,
    max_height: int | None = None,
    cell_extra: int = 0,
    allow_shrink_below_min: bool = False,
) -> TileGrid:
    """
    Choose tile width and wrap so all ``n`` tiles fit in ``area_width``.

    Default: never use ``tw < min_tw``. If one row is insufficient at
    ``min_tw``, add rows. Optional ``max_height`` only forces more rows /
    smaller *growth*, never below ``min_tw`` unless
    ``allow_shrink_below_min`` (legacy/tests only).
    """
    n = max(0, int(n))
    min_tw = max(8, int(min_tw))  # F0019: allow small AI / scaled floors
    max_tw = max(min_tw, int(max_tw))
    gap = max(0, int(gap))
    cell_extra = max(0, int(cell_extra))
    W = max(40, int(area_width) - int(margin) - int(label_w))

    if n == 0:
        tw = max_tw
        return TileGrid(tw=tw, th=int(tw * aspect), per_row=1, rows=0, gap=gap, n=0)

    def _cell(tw: int) -> int:
        return max(1, tw + cell_extra + gap)

    def _pack(tw: int) -> tuple[int, int]:
        pr = max(1, W // _cell(tw))
        r = max(1, math.ceil(n / pr))
        return pr, r

    # 1) Largest tw in [min_tw, max_tw] that still fits on **one** row
    chosen_tw = min_tw
    for tw in range(max_tw, min_tw - 1, -1):
        per, rows = _pack(tw)
        if n <= per:
            chosen_tw = tw
            per_row, rows = per, 1
            break
    else:
        # 2) Cannot fit one row at min_tw → wrap at min_tw (do NOT shrink)
        chosen_tw = min_tw
        per_row, rows = _pack(chosen_tw)

    # 3) Height budget: only wrap more / reduce *above*-min size, never below min
    if max_height is not None and max_height > 0:
        def _h(tw: int, r: int) -> int:
            th = int(tw * aspect)
            return r * th + max(0, r - 1) * gap

        if _h(chosen_tw, rows) > max_height:
            # Prefer more rows at same tw (already at wrap); if still too tall
            # and we grew above min, step down toward min_tw only.
            for tw in range(chosen_tw, min_tw - 1, -1):
                pr, r = _pack(tw)
                if r <= max_rows and _h(tw, r) <= max_height:
                    chosen_tw, per_row, rows = tw, pr, r
                    break
            else:
                # Stay at min_tw and accept scroll (seat canvas) rather than shrink
                chosen_tw = min_tw
                per_row, rows = _pack(chosen_tw)

    if rows > max_rows and allow_shrink_below_min:
        # Legacy escape hatch only
        for tw in range(min_tw - 1, 11, -1):
            pr, r = _pack(tw)
            if r <= max_rows:
                chosen_tw, per_row, rows = tw, pr, r
                break

    # Final: never report tw below min unless allow_shrink
    if not allow_shrink_below_min and chosen_tw < min_tw:
        chosen_tw = min_tw
        per_row, rows = _pack(chosen_tw)

    th = max(1, int(chosen_tw * aspect))
    return TileGrid(
        tw=chosen_tw, th=th, per_row=per_row, rows=rows, gap=gap, n=n
    )


def compute_button_rows(
    n_buttons: int,
    area_width: int,
    *,
    btn_w: int = 108,
    gap: int = 10,
    margin: int = 24,
) -> tuple[int, int]:
    """Return (per_row, rows) for action buttons (fixed button size, wrap only)."""
    n = max(0, int(n_buttons))
    if n == 0:
        return 1, 0
    W = max(btn_w, int(area_width) - int(margin))
    per = max(1, W // (btn_w + gap))
    rows = max(1, math.ceil(n / per))
    return per, rows
