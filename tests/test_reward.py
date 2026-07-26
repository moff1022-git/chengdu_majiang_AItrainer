"""M05 — reward calculator tests."""

from __future__ import annotations

from engine.blood_battle import GameResult
from engine.reward import RewardCalculator, RewardConfig
from engine.score import ScoreTransfer
from engine.state import GameState, PlayerState
from engine.dice import DiceResult
from engine.tile import Suit, Tile


def test_rw01_deal_in_penalty() -> None:
    calc = RewardCalculator(
        RewardConfig(hu_fan_scale=1.0, deal_in_penalty=2.0, use_engine_score_as_reward=False)
    )
    tr = [
        ScoreTransfer(reason="hu_dianpao", from_seat=1, to_seat=0, amount=4, fan=2)
    ]
    r = calc.on_transfers(tr)
    assert r[0] > 0
    assert r[1] < 0


def test_rw02_rank_bonus() -> None:
    calc = RewardCalculator(RewardConfig(rank_bonus=[3, 1, -1, -3], final_score_scale=0))
    result = GameResult(
        game_id="r",
        rankings=[2, 0, 1, 3],
        scores={0: 0, 1: 0, 2: 0, 3: 0},
        hu_sequence=[],
        finished_reason="last_one",
        wall_remaining=0,
    )
    state = GameState(
        game_id="r",
        master_seed=0,
        phase="finished",
        num_players=4,
        dice=DiceResult(1, 1, 2, 0),
        dealer_seat=0,
        wall=[],
        players=[
            PlayerState(seat=i, hand=[Tile(Suit.WAN, 1)], score=0)
            for i in range(4)
        ],
    )
    r = calc.on_game_end(result, state)
    assert r[2] == 3.0
    assert r[3] == -3.0


def test_rw03_engine_score_mode() -> None:
    calc = RewardCalculator(
        RewardConfig(use_engine_score_as_reward=True, final_score_scale=0.01)
    )
    tr = [ScoreTransfer(reason="hu_dianpao", from_seat=1, to_seat=0, amount=100, fan=0)]
    r = calc.on_transfers(tr)
    assert abs(r[0] - 1.0) < 1e-9
    assert abs(r[1] + 1.0) < 1e-9
