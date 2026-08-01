"""F0023: main-window dice roll presentation."""

from __future__ import annotations

import time

from display.dice_fx import DiceRollFx, preview_dice_for_game
from engine.deal import create_dealt_game
from engine.dice import DiceResult


def test_preview_matches_dealt_game() -> None:
    gid = "f0023-dice-match"
    st = create_dealt_game(gid, num_players=4)
    prev = preview_dice_for_game(gid, 4)
    assert prev.d1 == st.dice.d1
    assert prev.d2 == st.dice.d2
    assert prev.dealer_seat == st.dealer_seat
    assert prev.total == st.dice.total


def test_dice_fx_faces_settle() -> None:
    dice = DiceResult(d1=2, d2=5, total=7, dealer_seat=2)
    fx = DiceRollFx.from_dice(dice, game_id="x", round_index=1, total_s=0.2)
    fx.started_at = time.monotonic()
    # Immediately may still be rolling depending on timing
    f1, f2 = fx.faces()
    assert 1 <= f1 <= 6 and 1 <= f2 <= 6
    fx.started_at = time.monotonic() - 1.0  # past roll_s
    assert not fx.is_rolling()
    assert fx.faces() == (2, 5)
    assert "庄家 S2" in fx.caption()
    assert "2+5=7" in fx.log_line()


def test_dice_fx_done() -> None:
    fx = DiceRollFx(d1=1, d2=1, total=2, dealer_seat=0, total_s=0.05, roll_s=0.02)
    fx.started_at = time.monotonic() - 1.0
    assert fx.is_done()
    assert fx.progress() >= 1.0
