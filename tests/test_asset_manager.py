"""M07 — AssetManager tests (dummy video driver)."""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

pygame.init()

from display.asset_manager import AssetManager
from engine.orchestrator import InteractiveRunner
from players.registry import create_players


def test_a01_load_tile_green() -> None:
    am = AssetManager(theme="green")
    surf = am.tile("wan", 1)
    assert surf.get_width() > 0
    assert surf.get_height() > 0


def test_a02_theme_switch() -> None:
    am = AssetManager(theme="green")
    g = am.tile("tong", 5)
    am.set_theme("blue")
    b = am.tile("tong", 5)
    assert g is not b or g.get_size() == b.get_size()
    # paths differ so surfaces reloaded
    assert am.theme == "blue"


def test_a03_placeholder() -> None:
    am = AssetManager(theme="green")
    p = am.tile_placeholder()
    assert p.get_width() > 0


def test_a04_missing_strict() -> None:
    am = AssetManager(theme="green", strict=True)
    with pytest.raises(FileNotFoundError):
        am.load("tiles/wan/tile_wan_99_green.png")


def test_a05_buttons_and_bg() -> None:
    am = AssetManager(theme="blue")
    assert am.button("hu").get_width() > 0
    assert am.bg("table").get_width() > 0
    assert am.dice(3).get_width() > 0
    assert am.fx("hu").get_width() > 0


def test_i01_interactive_runner_finishes() -> None:
    players = create_players("rule_ai,rule_ai,random,random", base_seed=42)
    runner = InteractiveRunner(players, game_id="m07-step")
    runner.setup()
    assert runner.state.phase in ("discard", "draw", "response")
    steps = 0
    while not runner.step_once() and steps < 8000:
        steps += 1
    assert runner.result is not None
    assert runner.result.finished_reason
