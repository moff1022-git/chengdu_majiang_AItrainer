from __future__ import annotations

import copy

import pytest

from engine.action import Action, ActionType
from engine.tile import Suit, Tile
from training.action_codec_v2 import ACTION_SPACE_SIZE, EXCHANGE_TUPLES, ActionCodecError, decode_action, encode_action, legal_action_mask
from training.env import ChengduMahjongEnv, EnvError
from training.observations_v2 import flatten_observation_v2
from training.reward_v2 import TrainingContractConfig


def test_codec_is_fixed_unique_and_roundtrips():
    assert ACTION_SPACE_SIZE == 635
    assert len(EXCHANGE_TUPLES) == 495
    decoded = [decode_action(index) for index in range(ACTION_SPACE_SIZE)]
    assert [encode_action(action) for action in decoded] == list(range(ACTION_SPACE_SIZE))
    assert len({str(action) for action in decoded}) == ACTION_SPACE_SIZE
    assert all(len({tile.suit for tile in triple}) == 1 for triple in EXCHANGE_TUPLES)


def test_codec_rejects_mixed_exchange_and_mask_is_exact():
    with pytest.raises(ActionCodecError):
        encode_action(Action(ActionType.EXCHANGE, tiles=(Tile(Suit.WAN, 1), Tile(Suit.WAN, 2), Tile(Suit.TONG, 3))))
    actions = [Action(ActionType.PASS), Action(ActionType.DINGQUE, suit=Suit.TIAO)]
    mask = legal_action_mask(actions)
    assert len(mask) == ACTION_SPACE_SIZE
    assert [i for i, value in enumerate(mask) if value] == [0, 634]


@pytest.mark.parametrize("players", [2, 3, 4])
def test_v2_observation_shapes_and_no_hidden_fields(players):
    env = ChengduMahjongEnv(num_players=players, opponent_spec="random", seed=players, contract_version=2)
    obs = env.reset(game_id=f"f28-v2-obs-{players}")
    assert len(obs["hand_counts"]) == 27
    assert len(obs["dingque_one_hot"]) == 4
    assert len(obs["discard_counts"]) == 4
    assert len(obs["action_mask"]) == ACTION_SPACE_SIZE
    assert "physical_hand" not in repr(obs)
    assert len(flatten_observation_v2(obs)) == 921
    env.close()


def test_v2_fixed_index_and_shaping_off():
    env = ChengduMahjongEnv(opponent_spec="random", seed=8, contract_version=2)
    obs = env.reset(game_id="f28-v2-index")
    index = next(i for i, bit in enumerate(obs["action_mask"]) if bit)
    _, reward, _, _, info = env.step(index)
    assert reward == info["base_reward"]
    assert info["shaping_reward"] == 0
    env.close()


def test_v2_shaping_is_separate_from_true_score():
    cfg = TrainingContractConfig(contract_version=2, shaping_enabled=True, shaping_gamma=0.9)
    env = ChengduMahjongEnv(opponent_spec="random", seed=18, training_contract=cfg)
    obs = env.reset(game_id="f28-v2-shaping")
    index = next(i for i, bit in enumerate(obs["action_mask"]) if bit)
    _, reward, _, _, info = env.step(index)
    assert reward == pytest.approx(info["base_reward"] + info["shaping_reward"])
    assert info["true_score_delta"] == info["score_delta"]
    assert info["true_score"] == info["score"]
    env.close()


def test_illegal_raise_preserves_state_and_terminate_penalizes():
    env = ChengduMahjongEnv(opponent_spec="random", seed=9, contract_version=2)
    obs = env.reset(game_id="f28-v2-illegal-raise")
    before = copy.deepcopy(env.state.to_dict())
    illegal = next(i for i, bit in enumerate(obs["action_mask"]) if not bit)
    with pytest.raises(EnvError):
        env.step(illegal)
    assert env.state.to_dict() == before
    env.close()

    cfg = TrainingContractConfig(contract_version=2, illegal_action_mode="terminate", illegal_action_penalty=-7)
    env = ChengduMahjongEnv(opponent_spec="random", seed=9, training_contract=cfg)
    obs = env.reset(game_id="f28-v2-illegal-term")
    illegal = next(i for i, bit in enumerate(obs["action_mask"]) if not bit)
    terminal, reward, terminated, truncated, info = env.step(illegal)
    assert (reward, terminated, truncated) == (-7, True, False)
    assert info["illegal_action"] is True
    assert sum(terminal["action_mask"]) == 0
    env.close()


def test_v1_integer_semantics_remain_legal_list_index():
    env = ChengduMahjongEnv(opponent_spec="random", seed=4)
    obs = env.reset(game_id="f28-v1-compatible")
    expected = env.legal_actions()[0]
    env.step(0)
    assert obs["legal_actions"][0] == expected.to_dict()
    env.close()
