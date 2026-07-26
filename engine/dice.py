"""Deterministic double-dice dealer selection."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DiceResult:
    d1: int
    d2: int
    total: int
    dealer_seat: int

    def to_dict(self) -> dict:
        return {
            "d1": self.d1,
            "d2": self.d2,
            "total": self.total,
            "dealer_seat": self.dealer_seat,
        }

    @classmethod
    def from_dict(cls, data: dict) -> DiceResult:
        try:
            d1 = int(data["d1"])
            d2 = int(data["d2"])
            total = int(data["total"])
            dealer_seat = int(data["dealer_seat"])
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"invalid dice dict: {data!r}") from e
        if d1 + d2 != total:
            raise ValueError(f"dice total mismatch: {data!r}")
        return cls(d1=d1, d2=d2, total=total, dealer_seat=dealer_seat)


def roll_dice(dice_seed: int, num_players: int) -> DiceResult:
    """Roll two dice from dice_seed; dealer_seat = (total - 1) % num_players."""
    if num_players < 2:
        raise ValueError(f"num_players must be >= 2, got {num_players}")
    rng = random.Random(dice_seed)
    d1 = rng.randint(1, 6)
    d2 = rng.randint(1, 6)
    total = d1 + d2
    dealer_seat = (total - 1) % num_players
    return DiceResult(d1=d1, d2=d2, total=total, dealer_seat=dealer_seat)
