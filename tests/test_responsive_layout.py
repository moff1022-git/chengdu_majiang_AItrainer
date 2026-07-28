"""F0006: responsive tile grid + PlayerView multi-row hand."""

from __future__ import annotations

import os

import pytest

from players.view.responsive import compute_button_rows, compute_tile_grid

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def test_wide_window_single_row_large_tiles():
    g = compute_tile_grid(5, 800, min_tw=36, max_tw=48, gap=3, margin=16)
    assert g.rows == 1
    assert g.per_row >= 5
    assert g.tw >= 36
    assert g.n == 5


def test_narrow_window_wraps_at_min_not_shrink():
    """Below min size → more rows, never tw < min_tw."""
    min_tw = 36
    g = compute_tile_grid(14, 320, min_tw=min_tw, max_tw=48, gap=3, margin=16)
    assert g.per_row * g.rows >= 14
    assert g.rows >= 2
    assert g.tw >= min_tw
    for i in range(14):
        x, _y = g.cell(i, origin_x=0, origin_y=0)
        assert x + g.tw <= 320 + min_tw  # last col may approach edge


def test_cell_extra_forces_wrap_before_clip():
    """Button/Label chrome must be counted or 14 tiles overflow a 400px seat."""
    bare = compute_tile_grid(14, 400, min_tw=36, max_tw=44, gap=4, margin=4, cell_extra=0)
    with_chrome = compute_tile_grid(
        14, 400, min_tw=36, max_tw=44, gap=4, margin=4, cell_extra=6
    )
    assert with_chrome.per_row <= bare.per_row
    assert with_chrome.tw >= 36
    assert with_chrome.per_row * with_chrome.rows >= 14


def test_bottom_up_hand_rows_stack_upward():
    g = compute_tile_grid(14, 200, min_tw=36, max_tw=40, gap=2, margin=8)
    assert g.rows >= 2
    assert g.tw >= 36
    bottom = 400
    coords = [g.cell_bottom_up(i, origin_x=0, bottom_y=bottom) for i in range(14)]
    assert coords[-1][1] >= coords[0][1]
    for _x, y in coords:
        assert y + g.th <= bottom + 1


def test_default_hand_min_is_f0019_baseline():
    from players.view.responsive import DEFAULT_MIN_HAND_TW, compute_tile_grid

    # F0019 play S=1 baseline (was 36 under F0006 hard floor)
    assert DEFAULT_MIN_HAND_TW == 28
    g = compute_tile_grid(13, 280)  # defaults
    assert g.tw >= DEFAULT_MIN_HAND_TW
    assert g.rows >= 2


def test_button_rows_wrap():
    per, rows = compute_button_rows(6, 240, btn_w=108, gap=10, margin=24)
    assert per >= 1
    assert rows >= 2
    assert per * rows >= 6


def test_discard_grid_multi_row_narrow_ext():
    """AI/human EXT discard column (~33% width) must wrap many discards."""
    # ~442*0.33 AI watch, 24 discards, compact chrome cell_extra=4
    g = compute_tile_grid(
        24,
        140,
        min_tw=12,
        max_tw=16,
        gap=1,
        margin=4,
        max_rows=16,
        cell_extra=4,
    )
    assert g.rows >= 2
    assert g.per_row * g.rows >= 24
    assert g.tw >= 12
    # wide human EXT still wraps when n is large
    g2 = compute_tile_grid(
        30, 280, min_tw=18, max_tw=22, gap=1, margin=4, max_rows=16, cell_extra=4
    )
    assert g2.rows >= 2
    assert g2.per_row * g2.rows >= 30


def test_player_view_hand_rects_match_count_and_bounds():
    import pygame

    pygame.init()
    from display.asset_manager import AssetManager
    from players.view.player_view import PlayerView

    screen = pygame.display.set_mode((360, 520))
    am = AssetManager(theme="green")
    pv = PlayerView(am, seat=0)
    pv.mode = "play"
    hand = [f"wan_{i}" for i in range(1, 10)] + [f"tong_{i}" for i in range(1, 6)]
    view = {
        "wall_remaining": 50,
        "players": [
            {
                "seat": 0,
                "score": 0,
                "hand": hand,
                "melds": [],
                "discard_pile": [f"tiao_{i}" for i in range(1, 10)],
                "status": "playing",
                "hand_count": len(hand),
            },
            {
                "seat": 1,
                "score": 0,
                "hand_count": 13,
                "melds": [],
                "status": "playing",
            },
        ],
    }
    pv.draw(screen, view, "discard", [], status_note="")
    assert len(pv.hand_rects) == len(hand)
    w, h = screen.get_size()
    for tid, rect in pv.hand_rects:
        assert rect.x >= 0
        assert rect.right <= w + 2
        assert rect.y >= 0
        assert rect.bottom <= h
    # Narrower → more or equal rows effect: all still present
    screen2 = pygame.display.set_mode((280, 520))
    pv.draw(screen2, view, "discard", [], status_note="")
    assert len(pv.hand_rects) == len(hand)
    pygame.quit()
