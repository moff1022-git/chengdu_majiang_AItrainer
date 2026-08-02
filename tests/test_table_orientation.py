"""Main table: left/right seats orient tiles toward center."""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def test_slot_tile_rotation_toward_center():
    from display.table_view import TableView

    assert TableView._slot_tile_rotation("left") == -90
    assert TableView._slot_tile_rotation("right") == 90
    assert TableView._slot_tile_rotation("bottom") == 0
    assert TableView._slot_tile_rotation("top") == 0


def test_blit_tile_left_right_swaps_aspect():
    import pygame

    pygame.init()
    from display.asset_manager import AssetManager
    from display.table_view import TableView

    screen = pygame.display.set_mode((640, 480))
    tv = TableView(AssetManager(theme="green"))
    # upright
    w0, h0 = tv._blit_tile(screen, "wan_1", 10, 10, 32, rotate=0)
    assert w0 <= 34 and h0 > w0
    # left seat orientation
    wL, hL = tv._blit_tile(screen, "wan_1", 10, 100, 32, rotate=-90)
    assert hL <= 34 and wL > hL  # wider than tall after -90
    # right
    wR, hR = tv._blit_tile(screen, "tong_5", 10, 200, 32, rotate=90)
    assert hR <= 34 and wR > hR
    pygame.quit()
