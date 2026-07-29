"""Lobby layout: human-chrome style, no footer/body overlap."""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from display.asset_manager import AssetManager
from display.lobby_view import CTL_HUMANLIKE, CTL_HUMANLIKE_SETTINGS, CTL_START, LobbyView


def test_lobby_draw_buttons_in_footer() -> None:
    pygame.init()
    for size in ((885, 498), (1100, 720), (640, 400)):
        screen = pygame.display.set_mode(size)
        am = AssetManager(theme="green")
        lv = LobbyView(am)
        lv.draw(
            screen,
            theme="green",
            num_players=4,
            players_spec="human,rule_ai,rule_ai,rule_ai",
            spectator="full",
            num_rounds=2,
        )
        w, h = size
        assert lv.start_rect.bottom <= h
        assert lv.start_rect.top >= int(h * 0.55)  # footer half
        assert lv.hit_start(lv.start_rect.center)
        assert lv.hit_control(lv.start_rect.center) == CTL_START
        # settings rows exist
        assert "players" in lv._hit
        if w >= 800 and h >= 498:
            assert CTL_HUMANLIKE in lv._hit
            assert CTL_HUMANLIKE_SETTINGS in lv._hit
        for r in lv._hit.values():
            assert r.bottom <= h
            assert r.top >= 0
    pygame.quit()
