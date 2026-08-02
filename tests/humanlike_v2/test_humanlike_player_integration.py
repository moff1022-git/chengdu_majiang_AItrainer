from __future__ import annotations

import pytest

from engine.orchestrator import PlayerGameRunner
from players.humanlike.player import HumanlikeV2Player
from players.registry import PLAYER_REGISTRY, create_player, create_players


def test_registry_exposes_humanlike_without_changing_old_defaults() -> None:
    assert PLAYER_REGISTRY["humanlike_v2"] is HumanlikeV2Player
    assert isinstance(create_player("humanlike_v2", seat=0, seed=7), HumanlikeV2Player)
    assert create_player("rule_ai", seat=0).__class__.__name__ == "RuleAIPlayer"
    assert create_player("rule_ai_plus", seat=0).__class__.__name__ == "RuleAIPlayer"


@pytest.mark.parametrize("num_players", [2, 3, 4])
def test_humanlike_self_play_has_no_policy_crash_or_full_state_channel(num_players: int) -> None:
    players = create_players(["humanlike_v2"] * num_players, base_seed=31)
    runner = PlayerGameRunner(players, game_id=f"f28-self-{num_players}")
    result = runner.run()
    assert result.finished_reason
    assert runner.crash.crash_log == []
    assert all(not hasattr(player, "_engine_state") for player in players)
    assert all(player.runtime is not None for player in players)


def test_same_game_produces_same_decision_histories() -> None:
    histories = []
    for _ in range(2):
        players = create_players(["humanlike_v2"] * 4, base_seed=11)
        runner = PlayerGameRunner(players, game_id="f28-repeat")
        result = runner.run()
        assert runner.crash.crash_log == []
        histories.append([
            [record["selected_action"] for record in (player.runtime.snapshot().values["RP-029"] or [])]
            for player in players
        ])
        assert result.finished_reason
    assert histories[0] == histories[1]

