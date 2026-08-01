"""Stateless deterministic plan labels for the F0028-3 baseline."""

from __future__ import annotations

from dataclasses import dataclass

from players.humanlike.hand_analyzer import HandFeatures


@dataclass(frozen=True, slots=True)
class PlanSnapshot:
    primary: str
    backup: str

    def to_dict(self) -> dict[str, str]:
        return {"primary": self.primary, "backup": self.backup}


def choose_plan(features: HandFeatures) -> PlanSnapshot:
    if features.dingque_tiles:
        return PlanSnapshot("clear_dingque", "fast_win")
    if features.defense < 0.35:
        return PlanSnapshot("defend", "balanced")
    if features.shanten <= 1 or features.speed >= 0.72:
        return PlanSnapshot("fast_win", "balanced")
    if features.hand_value >= 0.62:
        return PlanSnapshot("value_hand", "balanced")
    return PlanSnapshot("balanced", "fast_win")

