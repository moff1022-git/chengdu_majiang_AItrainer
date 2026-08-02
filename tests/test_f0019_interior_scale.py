"""F0019: interior element scale from 1080p baseline."""

from __future__ import annotations

from display.interior_scale import (
    AI_REF_H,
    AI_REF_W,
    HUMAN_REF_H,
    HUMAN_REF_W,
    MAIN_REF_H,
    MAIN_REF_W,
    main_scale,
    scale_factor,
    seat_scale,
)
from display.layout import Layout


def test_scale_factor_main_baseline_and_double():
    assert abs(scale_factor(MAIN_REF_W, MAIN_REF_H, "main") - 1.0) < 1e-9
    assert abs(scale_factor(MAIN_REF_W * 2, MAIN_REF_H * 2, "main") - 2.0) < 1e-9
    # larger only in one axis → limited by the smaller ratio
    assert abs(scale_factor(MAIN_REF_W * 2, MAIN_REF_H, "main") - 1.0) < 1e-9


def test_scale_factor_seat_roles():
    assert abs(scale_factor(HUMAN_REF_W, HUMAN_REF_H, "play") - 1.0) < 1e-9
    assert abs(scale_factor(AI_REF_W, AI_REF_H, "watch") - 1.0) < 1e-9
    assert scale_factor(AI_REF_W * 2, AI_REF_H * 2, "watch") == 2.0


def test_main_scale_tiles_grow():
    s1 = main_scale(MAIN_REF_W, MAIN_REF_H)
    s2 = main_scale(MAIN_REF_W * 2, MAIN_REF_H * 2)
    assert s1.s == 1.0
    assert s1.tile_w == 28
    assert s2.tile_w == 56
    # body font grows with window but seat typography is capped separately
    assert s2.font_body >= s1.font_body


def test_layout_uses_f0019_scale():
    ly = Layout.from_window(MAIN_REF_W, MAIN_REF_H)
    assert abs(ly.scale - 1.0) < 1e-9
    assert ly.tile_w == 28
    ly2 = Layout.from_window(MAIN_REF_W * 2, MAIN_REF_H * 2)
    assert ly2.tile_w == 56
    # ratios unchanged
    assert abs(ly.content_w / ly.width - 0.80) < 0.02
    assert abs(ly2.content_w / ly2.width - 0.80) < 0.02


def test_seat_scale_play_vs_ai():
    p = seat_scale(HUMAN_REF_W, HUMAN_REF_H, mode="play")
    a = seat_scale(AI_REF_W, AI_REF_H, mode="watch")
    assert p.s == 1.0 and a.s == 1.0
    assert p.hand_tw == 26
    assert a.hand_tw == 16
    assert p.font <= 12 and p.font_lg <= 14
    p2 = seat_scale(HUMAN_REF_W * 2, HUMAN_REF_H * 2, mode="play")
    # tiles may grow; fonts capped at S=1 for balance
    assert p2.hand_tw >= p.hand_tw
    assert p2.font == p.font


def test_actions_above_settings_geometry():
    from players.seat_layout_play import compute_seat_interior

    li = compute_seat_interior(885, 498, expanded=True, view_mode="full")
    # OP order: info → status → play → settings
    assert li.op_info.y < li.op_status.y < li.op_play.y < li.op_settings.y
    # action bar at bottom of play, immediately above settings
    assert li.play_actions.y + li.play_actions.h <= li.op_settings.y + 1


def test_plan_windows_never_exceed_1080p_full():
    """Complete-mode outer sizes: min for fit, never enlarge past 1080p §8.2."""
    from display.window_geometry import FULL_AI_H, FULL_AI_W, FULL_MAIN_H, FULL_MAIN_W, compute_window_plan

    for desk in ((1920, 1080), (2560, 1440), (3840, 2160)):
        plan = compute_window_plan(4, desktop=desk, origin=(0, 0), human_seats=[0])
        assert plan.main.w <= FULL_MAIN_W and plan.main.h <= FULL_MAIN_H
        for s, r in plan.players.items():
            if s == 0:
                assert r.w <= FULL_MAIN_W and r.h <= FULL_MAIN_H
            else:
                assert r.w <= FULL_AI_W and r.h <= FULL_AI_H
    # 1080p equals complete size
    p1080 = compute_window_plan(4, desktop=(1920, 1080), origin=(0, 0), human_seats=[0])
    assert p1080.main.w == FULL_MAIN_W and p1080.main.h == FULL_MAIN_H
