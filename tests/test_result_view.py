"""F0008 — ResultView scoreboard draws with full ledger (dummy display)."""

from __future__ import annotations

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from display.asset_manager import AssetManager
from display.result_view import ResultView
from engine.blood_battle import GameResult


def test_format_cumulative_board() -> None:
    from display.result_view import format_cumulative_board

    s = format_cumulative_board({0: 12, 1: -3, 2: 0, 3: 5}, rankings=[0, 3, 2, 1])
    assert "累计得分" in s
    assert "S0:+12" in s
    assert "S3:+5" in s


def test_result_view_draw_with_details() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1100, 720))
    am = AssetManager(theme="green")
    rv = ResultView(am)
    result = GameResult(
        game_id="rv-test",
        rankings=[0, 2, 1, 3],
        scores={0: 16, 1: -8, 2: -2, 3: -6},
        hu_sequence=[{"seat": 0, "fan": 1, "zimo": True}],
        finished_reason="last_one",
        wall_remaining=12,
        settle_tags={"hua_zhu": [], "ting": [1], "not_ting": [2, 3]},
        score_events=[
            {
                "type": "score",
                "turn_index": 3,
                "transfers": [
                    {
                        "reason": "hu_zimo",
                        "from_seat": 1,
                        "to_seat": 0,
                        "amount": 2,
                        "fan": 1,
                    },
                    {
                        "reason": "hu_zimo",
                        "from_seat": 2,
                        "to_seat": 0,
                        "amount": 2,
                        "fan": 1,
                    },
                    {
                        "reason": "hu_zimo",
                        "from_seat": 3,
                        "to_seat": 0,
                        "amount": 2,
                        "fan": 1,
                    },
                ],
            }
        ],
    )
    rv.draw(
        screen,
        result,
        round_index=2,
        num_rounds=4,
        session_scores={0: 16, 1: -8, 2: -2, 3: -6},
        hand_start_scores={0: 10, 1: -6, 2: 0, 3: -4},
    )
    # hit tests after draw (buttons may be placed)
    assert isinstance(rv.hit_lobby((0, 0)), bool)
    assert isinstance(rv.hit_again((0, 0)), bool)
    pygame.quit()


def test_result_view_draw_empty_events() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    am = AssetManager(theme="green")
    rv = ResultView(am)
    result = GameResult(
        game_id="rv-empty",
        rankings=[0, 1],
        scores={0: 0, 1: 0},
        hu_sequence=[],
        finished_reason="wall_empty",
        wall_remaining=0,
        settle_tags={},
        score_events=[],
    )
    rv.draw(screen, result)
    pygame.quit()
