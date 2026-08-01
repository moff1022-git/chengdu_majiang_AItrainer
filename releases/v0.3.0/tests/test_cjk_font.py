"""CJK UI font resolution (macOS / Windows / Linux)."""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def test_resolve_ui_font_renders_chinese() -> None:
    import pygame

    pygame.init()
    pygame.font.init()
    from display.hud_common import _font_supports_cjk, draw_text, resolve_ui_font

    font = resolve_ui_font(24)
    assert font is not None
    assert _font_supports_cjk(font)
    surf = font.render("开始游戏 万筒条 碰杠胡", True, (255, 255, 255))
    assert surf.get_width() > 150

    screen = pygame.Surface((400, 60))
    draw_text(screen, "本局结算", (8, 12), size=28)
    # non-black pixels present
    arr = pygame.surfarray.array3d(screen)
    assert (arr.sum(axis=2) > 0).any()
    pygame.quit()


def test_resolve_ui_font_survives_reinit() -> None:
    import pygame

    from display.hud_common import resolve_ui_font

    pygame.init()
    pygame.font.init()
    f1 = resolve_ui_font(18)
    assert f1 is not None
    w1 = f1.render("胡牌", True, (255, 255, 255)).get_width()
    pygame.quit()

    pygame.init()
    pygame.font.init()
    f2 = resolve_ui_font(18)
    assert f2 is not None
    w2 = f2.render("胡牌", True, (255, 255, 255)).get_width()
    assert w2 >= w1 * 0.8
    pygame.quit()
