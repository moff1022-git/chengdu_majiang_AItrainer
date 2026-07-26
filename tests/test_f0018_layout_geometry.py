"""F0018 P0–P3 geometry: canvas 85%, plan A/B/C, main interior 80/20, seat 67/33."""

from __future__ import annotations

from display.main_interior import compute_main_interior
from display.play_event_log import PlayEventLog
from display.window_geometry import (
    LAYOUT_CAP_H,
    LAYOUT_CAP_W,
    compute_window_plan,
    layout_canvas,
    plan_layout_abc,
    plan_mode_A,
    plan_mode_B,
    plan_mode_C,
    resolve_layout_mode,
    to_compact,
    window_sizes,
    windows_overlap,
)
from players.seat_layout_play import compute_seat_interior


def test_layout_canvas_area_ratio_and_cap():
    for W, H, expect_lw, expect_lh in (
        (1280, 720, 1180, 664),
        (1920, 1080, 1770, 996),
        (3840, 2160, 3540, 1991),
    ):
        c = layout_canvas(W, H, origin=(0, 0))
        assert c.w == expect_lw and c.h == expect_lh, (W, H, c)
        area_ratio = (c.w * c.h) / float(W * H)
        assert 0.84 <= area_ratio <= 0.86

    # >2160p: cap before 85%
    big = layout_canvas(7680, 4320, origin=(100, 50))
    capped = layout_canvas(LAYOUT_CAP_W, LAYOUT_CAP_H, origin=(100, 50))
    assert big.w == capped.w and big.h == capped.h


def test_window_sizes_percentages():
    sz = window_sizes(1770, 996)
    assert sz["Wm"] == 885 and sz["Hm"] == 498
    assert sz["Wa"] == 442 and sz["Ha"] == 249
    assert abs((885 * 498) / (1770 * 996) - 0.25) < 0.001
    assert abs((442 * 249) / (1770 * 996) - 0.0625) < 0.001


def test_resolve_layout_mode():
    assert resolve_layout_mode(1, 3) == "A"
    assert resolve_layout_mode(2, 2) == "B"
    assert resolve_layout_mode(0, 4) == "C"
    assert resolve_layout_mode(3, 1) is None


def test_plan_mode_a_b_c_1080p_no_overlap():
    canvas = layout_canvas(1920, 1080)
    main_a, pl_a = plan_mode_A(canvas, human_seats=[0], ai_seats=[1, 2, 3])
    assert main_a.w == 885 and main_a.h == 498
    assert main_a.x == canvas.x and main_a.y == canvas.y + 498
    assert pl_a[0].x == canvas.x + 885
    assert set(pl_a) == {0, 1, 2, 3}
    for s, r in pl_a.items():
        if s != 0:
            assert r.w == 442 and r.h == 249
        assert not windows_overlap(r, main_a)

    main_b, pl_b = plan_mode_B(canvas, human_seats=[0, 1], ai_seats=[2, 3])
    assert pl_b[0].y == canvas.y + 498  # bottom-right human
    assert pl_b[1].y == canvas.y  # top-right human
    assert len([s for s in pl_b if s in (2, 3)]) == 2

    main_c, pl_c = plan_mode_C(canvas, ai_seats=[0, 1, 2, 3])
    assert set(pl_c) == {0, 1, 2, 3}
    assert all(r.w == 442 for r in pl_c.values())


def test_compute_window_plan_default_is_mode_a():
    plan = compute_window_plan(4, desktop=(1920, 1080), origin=(0, 0))
    assert plan.layout_mode == "A"
    assert plan.main.w == 885
    assert 0 in plan.players
    assert plan.players[0].w >= 885  # Wm2 may equal Wm


def test_plan_layout_abc_all_ai():
    plan = plan_layout_abc(4, human_seats=[], desktop=(1920, 1080), origin=(10, 20))
    assert plan is not None
    assert plan.layout_mode == "C"
    assert set(plan.players) == {0, 1, 2, 3}


def test_to_compact_left_anchor():
    from display.window_geometry import WindowRect

    r = WindowRect(100, 50, 442, 249)
    c = to_compact(r)
    assert c.x == 100 and c.y == 50
    assert c.w == 221 and c.h == 249


def test_main_interior_80_20_dice_strips():
    mi = compute_main_interior(885, 498, tile_w=44)
    assert mi.table.w + mi.side.w == 885
    assert abs(mi.table.w / 885 - 0.80) < 0.02
    assert mi.side_top.h + mi.side_mid.h + mi.side_bot.h == 498
    # DICE concentric
    cx_t = mi.table.x + mi.table.w // 2
    cy_t = mi.table.y + mi.table.h // 2
    cx_d, cy_d = mi.dice.center()
    assert abs(cx_t - cx_d) <= 1
    assert abs(cy_t - cy_d) <= 1
    # strips order bottom: disc.y < meld.y < hand.y (outer lower)
    bot = mi.strips["bottom"]
    assert bot.disc.y <= bot.meld.y <= bot.hand.y
    assert bot.hand.h > 0 and bot.meld.h > 0 and bot.disc.h > 0


def test_seat_interior_67_33_and_fold():
    exp = compute_seat_interior(885, 498, expanded=True, view_mode="full")
    assert exp.ext is not None
    assert abs(exp.op.w / 885 - 0.67) < 0.03
    assert exp.op.w + exp.ext.w == 885
    assert exp.ext_top is not None and exp.ext_bot is not None
    assert exp.ext_top.h + exp.ext_bot.h == 498
    # STATUS:PLAY ≈ 20:60 within flex
    flex = exp.op_status.h + exp.op_play.h
    assert abs(exp.op_status.h / flex - 0.20 / 0.80) < 0.05
    assert abs(exp.op_play.h / flex - 0.60 / 0.80) < 0.05
    # actions strip is bottom of OP_PLAY, above settings
    assert exp.play_actions.y + exp.play_actions.h == exp.op_play.y + exp.op_play.h
    assert exp.op_settings.y >= exp.op_play.y + exp.op_play.h - 1

    col = compute_seat_interior(885, 498, expanded=False)
    assert col.ext is None
    assert col.op.w == 885

    compact = compute_seat_interior(885, 498, expanded=True, view_mode="compact")
    assert compact.ext_bot is not None and compact.ext_bot.h == 0


def test_play_event_log_ring():
    log = PlayEventLog(capacity=5)
    for i in range(8):
        log.append("info", f"line{i}")
    assert len(log) == 5
    texts = log.texts()
    assert texts[0] == "line3"
    assert texts[-1] == "line7"
