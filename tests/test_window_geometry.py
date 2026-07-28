"""Window geometry: screen detect, grid layout, no off-screen seats."""

from __future__ import annotations

import sys

from display.layout import Layout
from display.window_geometry import (
    MAX_WORK_H,
    MAX_WORK_W,
    ScreenInfo,
    compute_window_plan,
    detect_screen,
    find_hwnds_for_pid,
    force_hwnd_placement,
    force_placement_by_pid,
    force_placement_by_title,
    plan_for_screen,
    plan_to_dict,
    rect_from_plan_dict,
    seat_slot,
    windows_overlap,
    work_area,
)


def _bbox(plan) -> tuple[int, int, int, int]:
    xs = [plan.main.x, plan.main.right]
    ys = [plan.main.y, plan.main.bottom]
    for r in plan.players.values():
        xs.extend([r.x, r.right])
        ys.extend([r.y, r.bottom])
    return min(xs), min(ys), max(xs), max(ys)


def test_work_area_capped_to_2k():
    wa = work_area(desktop=(3840, 2160))
    assert wa.w == MAX_WORK_W
    assert wa.h == MAX_WORK_H


def test_work_area_on_1080p():
    wa = work_area(desktop=(1920, 1080))
    assert wa.w == 1920
    assert wa.h == 1080


def test_plan_fits_inside_2k_work():
    plan = compute_window_plan(4, include_main=True, desktop=(2560, 1440))
    x0, y0, x1, y1 = _bbox(plan)
    # F0018: plan fits inside given desktop work (may use 85% canvas)
    assert x0 >= plan.work.x
    assert y0 >= plan.work.y
    assert x1 <= plan.work.x + plan.work.w
    assert y1 <= plan.work.y + plan.work.h
    assert x1 - x0 <= plan.work.w
    assert y1 - y0 <= plan.work.h


def test_all_seats_inside_and_no_overlap_main():
    for desk in ((1440, 852), (1920, 1080), (1366, 768), (2560, 1440)):
        plan = compute_window_plan(4, desktop=desk)
        assert set(plan.players) == {0, 1, 2, 3}
        for seat, r in plan.players.items():
            assert r.x >= plan.work.x
            assert r.y >= plan.work.y
            assert r.right <= plan.work.x + plan.work.w
            assert r.bottom <= plan.work.y + plan.work.h
            assert not windows_overlap(r, plan.main), f"{desk} S{seat} overlaps main"


def test_seat_slots_mapping():
    assert seat_slot(0) == "bottom"
    assert seat_slot(1) == "right"
    assert seat_slot(2) == "top"
    assert seat_slot(3) == "left"


def test_force_placement_by_title_no_crash():
    """API exists and returns False when no matching window (headless)."""
    from display.window_geometry import force_placement_by_title, reassert_plan_windows

    ok = force_placement_by_title("___no_such_window___", 10, 10, 200, 200)
    assert ok is False
    plan = compute_window_plan(4, desktop=(1440, 852), origin=(0, 0))
    # Default: seats only (safe from background threads)
    res = reassert_plan_windows(plan, include_main=False)
    assert res.get("main") is False
    assert "S0" in res and "S1" in res and "S2" in res and "S3" in res


def test_grid_relative_positions_1440():
    """F0018 layout A: MAIN bottom-left; human S0 bottom-right; AI on top band."""
    plan = compute_window_plan(4, desktop=(1440, 852), human_seats=[0])
    assert plan.layout_mode == "A"
    # MAIN left of human
    assert plan.main.x <= plan.players[0].x
    assert plan.main.y >= plan.players[1].y  # AI above MAIN band
    # human bottom-right of canvas-ish
    assert plan.players[0].x >= plan.main.x
    # AI seats share top band y (top-aligned)
    ys = {plan.players[s].y for s in (1, 2, 3)}
    assert len(ys) == 1
    # MAIN and human same height
    assert plan.main.h == plan.players[0].h
    # AI bottom clear of MAIN (decoration pad)
    from display.window_geometry import DECORATION_PAD_Y, GAP

    for s in (1, 2, 3):
        assert plan.players[s].bottom + DECORATION_PAD_Y + GAP <= plan.main.y
        assert not windows_overlap(plan.players[s], plan.main)
        assert not windows_overlap(plan.players[s], plan.players[0])


def test_layout_a_main_human_equal_height_and_ai_clear():
    for desk in ((1920, 1080), (1512, 982), (2560, 1440)):
        plan = compute_window_plan(4, desktop=desk, human_seats=[0])
        assert plan.main.h == plan.players[0].h
        assert plan.main.y == plan.players[0].y
        for s in (1, 2, 3):
            assert plan.players[s].y <= plan.main.y
            assert plan.players[s].bottom <= plan.main.y
            assert not windows_overlap(plan.players[s], plan.main)


def test_macos_sdl_pos_aligns_with_outer_plan():
    """SDL POS is content-top; helper offsets by chrome so outer aligns with Tk."""
    import sys
    from display.window_geometry import platform_frame_chrome_y, set_sdl_window_pos
    import os

    set_sdl_window_pos(100, 500)
    env = os.environ.get("SDL_VIDEO_WINDOW_POS", "")
    x_s, y_s = env.split(",")
    assert int(x_s) == 100
    if sys.platform == "darwin":
        assert int(y_s) == 500 + platform_frame_chrome_y()
    else:
        assert int(y_s) == 500


def test_detect_screen_and_plan_for_screen():
    sc = detect_screen()
    assert sc.width >= 640 and sc.height >= 480
    assert isinstance(sc.origin_x, int) and isinstance(sc.origin_y, int)
    plan = plan_for_screen(
        4, screen=ScreenInfo(1440, 900, "test", origin_x=1920, origin_y=0)
    )
    assert plan.screen_w == 1440 and plan.screen_h == 900
    assert plan.work.x >= 1920
    assert plan.main.x >= 1920
    d = plan_to_dict(plan)
    r0 = rect_from_plan_dict(d, 0)
    assert r0 is not None
    assert r0.w == plan.players[0].w


def test_pick_layout_stays_on_current_screen():
    """pick_layout_screen / plan keep preferred — including portrait secondary."""
    from display.window_geometry import pick_layout_screen, plan_for_screen

    primary = ScreenInfo(
        1920, 1052, "macos_main", origin_x=0, origin_y=28, monitor_index=0
    )
    secondary = ScreenInfo(
        1440,
        2532,
        "macos_cursor",
        origin_x=1920,
        origin_y=-812,
        monitor_index=1,
    )
    chosen = pick_layout_screen([primary, secondary], preferred=secondary)
    assert chosen.origin_x == 1920
    plan = plan_for_screen(4, screen=chosen)
    assert plan.work.x >= 1920
    assert plan.main.x >= 1920
    # All seats on same work area as main (no split across monitors)
    for s, r in plan.players.items():
        assert r.x >= plan.work.x
        assert r.right <= plan.work.x + plan.work.w
    chosen2 = pick_layout_screen([primary, secondary], preferred=primary)
    assert chosen2.origin_x == 0


def test_force_placement_does_not_crash():
    """Placement uses set_mode + env pos; must not SEGV (no _sdl2 writes)."""
    from display.window_geometry import force_window_placement
    import pygame

    pygame.display.init()
    try:
        pygame.display.set_mode((320, 240))
        ok = force_window_placement(80, 60, 320, 240)
        assert ok in (True, False)
        surf = pygame.display.get_surface()
        assert surf is not None
        # Draw must still work after placement (regression for lobby SEGV)
        pygame.draw.rect(surf, (8, 28, 22), pygame.Rect(10, 10, 40, 40), border_radius=4)
        pygame.display.flip()
        for _ in range(5):
            pygame.event.get()
    finally:
        pygame.display.quit()


def test_format_tk_geometry_preserves_negative_y():
    """Negative Y must stay absolute (…+x+-y), not “from bottom” (…+x-y)."""
    from display.window_geometry import format_tk_geometry, plan_cli_args, WindowRect

    g = format_tk_geometry(469, 708, 1928, -724)
    assert g == "469x708+1928+-724"
    assert "+-" in g  # absolute negative Y marker for Tk
    assert "1928-724" not in g.replace("1928+-", "")  # avoid from-bottom form
    cli = plan_cli_args(WindowRect(1928, -724, 469, 708))
    assert any(a.startswith("--y=") and "-724" in a for a in cli)


def test_detect_screen_platform_source_sane():
    """F0005: platform-native detect must not claim the wrong OS source."""
    sc = detect_screen()
    assert sc.width >= 640 and sc.height >= 480
    if sys.platform == "darwin":
        assert sc.source.startswith("macos") or sc.source in ("pygame", "default")
        assert not sc.source.startswith("win32")
    elif sys.platform == "win32":
        assert sc.source.startswith("win32") or sc.source in ("pygame", "default")
        assert not sc.source.startswith("macos")


def test_win32_placement_apis_safe_on_non_windows():
    """HWND helpers must no-op without crashing off Windows."""
    if sys.platform == "win32":
        return
    assert force_hwnd_placement(1, 0, 0, 200, 200) is False
    assert force_placement_by_title("___none___", 0, 0, 200, 200) is False
    assert force_placement_by_pid(1, 0, 0, 200, 200, timeout_s=0.05) is False
    assert find_hwnds_for_pid(1) == []


def test_layout_from_window_scales_tiles():
    # F0019: scale vs 885×498; larger client → larger tiles
    base = Layout.from_window(885, 498)
    big = Layout.from_window(1770, 996)
    small = Layout.from_window(800, 480)
    assert base.tile_w == 28
    assert big.tile_w == 56
    assert small.tile_w <= base.tile_w
    assert small.tile_w >= 12  # F0019 floor


def test_pack_fixed_fits_and_center_origin():
    from display.table_view import _center_origin, _pack_fixed

    per, lines, cw, ch = _pack_fixed(14, 200, 40, 36, 50, gap=2, horizontal=True)
    assert per * cw + max(0, per - 1) * 2 <= 200 + 2
    assert lines * ch + max(0, lines - 1) * 2 <= 40 + 2 or cw <= 12
    ox, oy = _center_origin(
        10, 20, 200, 60, n=6, per=6, lines=1, cell_w=20, cell_h=28, gap=2, horizontal=True
    )
    # content width = 6*20+5*2 = 130 → ox = 10 + (200-130)//2 = 45
    assert ox == 45 and oy == 20 + (60 - 28) // 2
    # Short hand with large capacity must still center on actual n (not per)
    ox2, _ = _center_origin(
        0, 0, 400, 50, n=5, per=20, lines=1, cell_w=20, cell_h=28, gap=0, horizontal=True
    )
    # content_w = 5*20 = 100 → ox = (400-100)//2 = 150
    assert ox2 == 150
