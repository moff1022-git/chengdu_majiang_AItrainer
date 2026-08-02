"""M11: ChengduMahjongEnv tests."""

from __future__ import annotations

import pytest

from engine.action import Action, ActionType
from engine.deal import create_dealt_game
from training.env import ChengduMahjongEnv, EnvError, smoke_random_episode
from training.spaces import encode_obs_vector


def test_e01_reset_returns_obs_with_legals():
    env = ChengduMahjongEnv(opponent_spec="random", seed=1)
    obs = env.reset(game_id="e01-reset")
    assert "legal_actions" in obs
    assert isinstance(obs["legal_actions"], list)
    assert len(obs["legal_actions"]) >= 1
    assert obs["seat"] == 0
    assert obs["phase"] in ("exchange", "dingque", "discard", "response")
    assert env.legal_actions()
    env.close()


def test_e02_random_policy_to_done():
    summary = smoke_random_episode(
        game_id="e02-random",
        opponent_spec="random",
        seed=2,
    )
    assert summary["terminated"] is True
    assert summary["truncated"] is False
    assert summary["scores"] is not None
    assert summary["steps"] >= 1


def test_e03_illegal_action_raises():
    env = ChengduMahjongEnv(opponent_spec="random", seed=3)
    env.reset(game_id="e03-illegal")
    with pytest.raises(EnvError):
        env.step(99999)
    with pytest.raises(EnvError):
        env.step(Action(ActionType.PASS))
    env.close()


def test_e04_same_game_id_dealt_hands():
    """Same game_id → same dealt hands at first learner decision (exchange)."""
    env1 = ChengduMahjongEnv(opponent_spec="rule_ai", seed=0)
    env2 = ChengduMahjongEnv(opponent_spec="rule_ai", seed=0)
    obs1 = env1.reset(game_id="e04-repro")
    obs2 = env2.reset(game_id="e04-repro")
    assert obs1["game_id"] == obs2["game_id"]
    dealt = create_dealt_game("e04-repro", num_players=4)
    # At exchange, hands not yet swapped
    assert env1.state.phase == "exchange"
    h1 = [t.id for t in env1.state.players[0].hand]
    h2 = [t.id for t in env2.state.players[0].hand]
    hd = [t.id for t in dealt.players[0].hand]
    assert h1 == h2 == hd
    env1.close()
    env2.close()


def test_e05_reward_is_float():
    env = ChengduMahjongEnv(opponent_spec="random", seed=5)
    env.reset(game_id="e05-reward")
    legal = env.legal_actions()
    obs, reward, terminated, truncated, info = env.step(legal[0])
    assert isinstance(reward, float)
    assert isinstance(info.get("score"), int)
    env.close()


def test_e06_env_no_display_import():
    import training.env as env_mod

    src = open(env_mod.__file__, encoding="utf-8").read()
    assert "display" not in src
    assert "pygame" not in src
    # import path works without needing GUI
    from training.env import ChengduMahjongEnv as E

    e = E(opponent_spec="random", num_players=2, seed=0)
    e.reset("e06")
    e.close()


def test_step_index_and_dict_action():
    env = ChengduMahjongEnv(opponent_spec="random", seed=7)
    env.reset(game_id="e-index")
    obs, r, term, trunc, info = env.step(0)
    assert isinstance(r, float)
    if not (term or trunc):
        d = env.legal_action_dicts()[0]
        env.step(d)
    env.close()


def test_encode_obs_vector_length():
    env = ChengduMahjongEnv(opponent_spec="random", seed=8)
    obs = env.reset(game_id="e-vec")
    vec = encode_obs_vector(obs)
    # 27 faces + wall + 8 phase one-hot
    assert len(vec) == 27 + 1 + 8
    env.close()


def test_smoke_rule_ai_opponents():
    summary = smoke_random_episode(
        game_id="e-rule",
        opponent_spec="rule_ai",
        seed=9,
        num_players=3,
    )
    assert summary["terminated"] is True
    assert summary["scores"] is not None
