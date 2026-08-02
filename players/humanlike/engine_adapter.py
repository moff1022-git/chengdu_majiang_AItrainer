"""Read-only projection from validated F0028 GP values to legacy engine inputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from engine.config import EngineConfig
from players.humanlike.config import HumanlikeConfig


class EngineConfigConflict(ValueError):
    pass


_EXCHANGE_DIRECTIONS = {
    "left": "counterclockwise",
    "right": "clockwise",
    "opposite": "across",
    "dice": "auto_dice",
    "random": "auto_dice",
}


@dataclass(frozen=True, slots=True)
class HumanlikeEngineAdapter:
    config: HumanlikeConfig

    def engine_config(self) -> EngineConfig:
        gp = self.config.global_parameters
        return EngineConfig(
            num_players=4,
            initial_score=int(gp["GP-003"]["starting_score"]),
            exchange_dir=_EXCHANGE_DIRECTIONS[str(gp["GP-005"]["direction"])],
            fan_cap=int(gp["GP-013"]["fan_cap"]),
            multi_ron=bool(gp["GP-008"]["multi_hu"]),
            base_score=int(gp["GP-013"]["base_score"]),
            force_discard_dingque=bool(gp["GP-006"]["force_discard_missing_suit"]),
            enable_exchange=bool(gp["GP-005"]["enabled"]),
        )

    def visibility_policy(self) -> Mapping[str, str]:
        return self.config.global_parameters["GP-021"]

    def require_compatible(self, existing: EngineConfig) -> EngineConfig:
        projected = self.engine_config()
        conflicts = {
            field: (getattr(existing, field), getattr(projected, field))
            for field in projected.__dataclass_fields__
            if getattr(existing, field) != getattr(projected, field)
        }
        if conflicts:
            raise EngineConfigConflict(f"EngineConfig conflicts with validated GP: {conflicts}")
        return projected
