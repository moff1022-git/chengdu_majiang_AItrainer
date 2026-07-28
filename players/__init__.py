"""Pluggable player modules."""

from players.base_player import BasePlayer
from players.human_proxy import HumanPlayerProxy
from players.humanlike.player import HumanlikeV2Player
from players.random_player import RandomPlayer
from players.registry import PLAYER_REGISTRY, create_player, create_players
from players.rule_ai_player import RuleAIPlayer

__all__ = [
    "BasePlayer",
    "HumanPlayerProxy",
    "HumanlikeV2Player",
    "PLAYER_REGISTRY",
    "RandomPlayer",
    "RuleAIPlayer",
    "create_player",
    "create_players",
]
