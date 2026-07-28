"""Main-window dice roll presentation (F0023).

Engine still rolls via game_id seeds; this module only animates & holds
the faces for TableView.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field


# Default show time: rolling phase + settle hold before engine continues
DEFAULT_ROLL_S = 1.6
DEFAULT_SETTLE_S = 0.5
DEFAULT_TOTAL_S = DEFAULT_ROLL_S + DEFAULT_SETTLE_S


@dataclass
class DiceRollFx:
    """One hand's dice animation keyed by final result."""

    d1: int
    d2: int
    dealer_seat: int
    total: int = 0
    started_at: float = field(default_factory=time.monotonic)
    roll_s: float = DEFAULT_ROLL_S
    total_s: float = DEFAULT_TOTAL_S
    game_id: str = ""
    round_index: int = 0
    log_emitted: bool = False

    def __post_init__(self) -> None:
        self.d1 = max(1, min(6, int(self.d1)))
        self.d2 = max(1, min(6, int(self.d2)))
        if not self.total:
            self.total = self.d1 + self.d2
        self.dealer_seat = int(self.dealer_seat)

    @classmethod
    def from_dice(
        cls,
        dice,
        *,
        game_id: str = "",
        round_index: int = 0,
        total_s: float = DEFAULT_TOTAL_S,
    ) -> DiceRollFx:
        return cls(
            d1=int(dice.d1),
            d2=int(dice.d2),
            total=int(getattr(dice, "total", 0) or (int(dice.d1) + int(dice.d2))),
            dealer_seat=int(dice.dealer_seat),
            game_id=str(game_id or ""),
            round_index=int(round_index),
            total_s=float(total_s),
            roll_s=min(DEFAULT_ROLL_S, max(0.4, float(total_s) * 0.75)),
        )

    def elapsed(self) -> float:
        return max(0.0, time.monotonic() - self.started_at)

    def progress(self) -> float:
        return min(1.0, self.elapsed() / max(0.05, self.total_s))

    def is_rolling(self) -> bool:
        return self.elapsed() < self.roll_s

    def is_done(self) -> bool:
        return self.elapsed() >= self.total_s

    def faces(self) -> tuple[int, int]:
        """Faces to draw: scramble while rolling, final after."""
        if not self.is_rolling():
            return self.d1, self.d2
        # Deterministic flicker from time (no extra RNG — final already fixed)
        t = self.elapsed()
        tick = int(t * 14)
        f1 = (tick * 3 + self.d1 + self.dealer_seat) % 6 + 1
        f2 = (tick * 5 + self.d2 * 2 + 1) % 6 + 1
        return f1, f2

    def caption(self) -> str:
        if self.is_rolling():
            f1, f2 = self.faces()
            return f"掷骰定庄中…  {f1}  {f2}"
        return (
            f"掷骰 {self.d1}+{self.d2}={self.total}  ·  庄家 S{self.dealer_seat}"
        )

    def log_line(self) -> str:
        return (
            f"掷骰 {self.d1}+{self.d2}={self.total} → 庄家 S{self.dealer_seat}"
        )


def preview_dice_for_game(
    game_id: str,
    num_players: int,
) -> object:
    """Same dice the engine will use for this game_id (no full deal)."""
    from engine.dice import roll_dice
    from engine.game_id import derive_seeds, normalize_game_id

    gid = normalize_game_id(game_id)
    seeds = derive_seeds(gid)
    return roll_dice(seeds.dice_seed, max(2, int(num_players)))
