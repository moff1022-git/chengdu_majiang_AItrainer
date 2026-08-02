"""Training-only complete information, deliberately separate from Observation."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from engine.state import GameState


@dataclass(frozen=True, slots=True)
class TrainingTruth:
    game_id: str
    hands: Mapping[int, tuple[int, ...]]
    wall_tile_ids: tuple[int, ...]


def build_training_truth(state: GameState) -> TrainingTruth:
    return TrainingTruth(
        game_id=state.game_id,
        hands=MappingProxyType(
            {player.seat: tuple(tile.tile_id for tile in player.hand) for player in state.players}
        ),
        wall_tile_ids=tuple(tile.tile_id for tile in state.wall),
    )
