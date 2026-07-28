"""F0007: main table uniform tiles + control panel."""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def test_layout_uniform_tile_sizes():
    from display.layout import MIN_TABLE_TW, Layout

    ly = Layout.from_window(1280, 720, panel_w=216)
    assert ly.tile_w == ly.tile_small_w == ly.tile_tiny_w
    assert ly.tile_w >= MIN_TABLE_TW

    narrow = Layout.from_window(800, 500, panel_w=216)
    assert narrow.tile_w >= MIN_TABLE_TW
    assert narrow.tile_w == narrow.tile_tiny_w


def test_layout_never_below_min():
    from display.layout import MIN_TABLE_TW, Layout

    tiny = Layout.from_window(400, 300, panel_w=200)
    assert tiny.tile_w >= MIN_TABLE_TW


def test_pack_fixed_fits_area_may_shrink():
    from display.table_view import _pack_fixed

    # Tall enough: keep requested cell
    per, lines, cw, ch = _pack_fixed(14, 300, 120, 36, 50, gap=3, horizontal=True)
    assert cw == 36 and ch == 50
    assert per * lines >= 14
    # Short area: shrink cells to fit zone height
    per2, lines2, cw2, ch2 = _pack_fixed(14, 300, 40, 36, 50, gap=3, horizontal=True)
    assert cw2 <= 36 and ch2 <= 50
    assert per2 * lines2 >= 14


def test_main_hand_bands_frame_and_equal_face_size():
    """L/R hands use full table height; face size matches T/B for 14 tiles."""
    from display.layout import Layout
    from display.table_view import _pack_fixed

    ly = Layout.from_window(885, 498)
    bot = ly.bottom_band()
    top = ly.top_band()
    left = ly.left_band()
    right = ly.right_band()
    # Frame: L/R full height, T/B inset (no corner hand overlap)
    assert left[3] == 498 and right[3] == 498
    assert left[2] == right[2]  # same thickness
    assert bot[2] == top[2]
    assert bot[0] == left[0] + left[2]
    assert bot[0] + bot[2] == right[0]
    # No hand-hand AABB overlap
    def overlap(a, b) -> bool:
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return not (
            ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay
        )

    hands = {"b": bot, "t": top, "l": left, "r": right}
    keys = list(hands)
    for i, k1 in enumerate(keys):
        for k2 in keys[i + 1 :]:
            assert not overlap(hands[k1], hands[k2]), f"{k1} overlaps {k2}"

    gap = 3
    n = 14
    # T/B pack (horizontal cell tw×th)
    cw0, ch0 = ly.cell_size(rotate=0)
    _, _, cw_tb, ch_tb = _pack_fixed(n, bot[2], bot[3], cw0, ch0, gap=gap, horizontal=True)
    # L/R pack (rotated cell th×tw)
    cw1, ch1 = ly.cell_size(rotate=90)
    _, _, cw_lr, ch_lr = _pack_fixed(
        n, left[2], left[3], cw1, ch1, gap=gap, horizontal=False
    )
    draw_tb = min(ly.tile_w, cw_tb)
    draw_lr = min(ly.tile_w, ch_lr)  # post-rot height = face width
    assert draw_tb == draw_lr == ly.tile_w, (draw_tb, draw_lr, ly.tile_w)
    assert cw_lr >= ch_tb - 1  # rotated face height ≈ upright face height


def test_control_panel_toggles():
    import pygame

    pygame.init()
    from display.control_panel import ControlPanel

    panel = ControlPanel()
    screen = pygame.display.set_mode((960, 540))
    panel.draw(screen, num_players=4)
    # click inference toggle region roughly
    assert panel.options.show_inference is True
    # use hit keys after draw
    key = "infer"
    assert key in panel._hits
    center = panel._hits[key].center
    assert panel.handle_click(center, num_players=4)
    assert panel.options.show_inference is False
    panel.handle_click(panel._hits["faces_none"].center, num_players=4)
    assert all(not panel.options.face_visible(s) for s in range(4))
    pygame.quit()


def test_river_areas_non_overlapping():
    """F0015: four ZONE_DISC strips sit outside DICE and do not overlap each other."""
    from display.layout import Layout

    ly = Layout.from_window(1280, 720)
    rects = {s: ly.river_area(s) for s in ("bottom", "top", "left", "right")}
    mi = ly.ensure_interior()
    dice = mi.dice.as_tuple()
    dx, dy, dw, dh = dice
    for s, (x, y, w, h) in rects.items():
        assert w > 0 and h > 0, s
        # disc strip is outside DICE (may touch edge)
        # not fully contained inside dice
        inside = (
            x >= dx and y >= dy and x + w <= dx + dw and y + h <= dy + dh
        )
        assert not inside, f"{s} should not be inside DICE"

    def overlap(a, b) -> bool:
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return not (
            ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay
        )

    slots = list(rects.keys())
    for i, s1 in enumerate(slots):
        for s2 in slots[i + 1 :]:
            assert not overlap(rects[s1], rects[s2]), f"{s1} overlaps {s2}"


def test_main_interior_80_20_from_layout():
    from display.layout import Layout

    ly = Layout.from_window(885, 498)
    assert abs(ly.content_w / 885 - 0.80) < 0.02
    regions = ly.side_regions()
    assert regions["mid"][3] > 0
    assert regions["top"][3] + regions["mid"][3] + regions["bot"][3] == 498


def test_table_view_draw_smoke():
    import pygame

    pygame.init()
    from display.asset_manager import AssetManager
    from display.control_panel import ControlPanel
    from display.table_view import TableView
    from engine.session import build_ready_game
    from engine.blood_battle import start_play

    screen = pygame.display.set_mode((1100, 700))
    am = AssetManager(theme="green")
    panel = ControlPanel()
    tv = TableView(am, control_panel=panel, show_hud=True)
    st = build_ready_game("f0007-smoke", num_players=4)
    start_play(st)
    tv.draw(screen, st)
    assert tv.layout.tile_w >= 12  # F0019 floor
    assert tv.layout.tile_w == tv.layout.tile_tiny_w
    pygame.quit()
