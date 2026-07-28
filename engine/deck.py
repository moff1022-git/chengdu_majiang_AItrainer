"""108-tile wall: build, shuffle, deal."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from engine.physical_tile import PhysicalTile, build_physical_wall


def build_full_wall() -> list[PhysicalTile]:
    """Fixed physical-id order, preserving the historical face sequence."""
    return build_physical_wall()


def shuffle_wall(wall: list[PhysicalTile], shuffle_seed: int) -> list[PhysicalTile]:
    """Return a new shuffled list (does not mutate input)."""
    out = list(wall)
    random.Random(shuffle_seed).shuffle(out)
    return out


@dataclass
class Deck:
    """Wall with draw pointer; remaining tiles are ``tiles[index:]``."""

    tiles: list[PhysicalTile] = field(default_factory=build_full_wall)
    index: int = 0

    @classmethod
    def create_shuffled(cls, shuffle_seed: int) -> Deck:
        return cls(tiles=shuffle_wall(build_full_wall(), shuffle_seed), index=0)

    @property
    def remaining(self) -> int:
        return len(self.tiles) - self.index

    def draw(self) -> PhysicalTile:
        if self.index >= len(self.tiles):
            raise ValueError("wall is empty")
        tile = self.tiles[self.index]
        self.index += 1
        return tile

    def remaining_tiles(self) -> list[PhysicalTile]:
        return list(self.tiles[self.index :])


def deal_hands(
    deck: Deck,
    *,
    num_players: int,
    dealer_seat: int,
) -> list[list[PhysicalTile]]:
    """
    Deal 13 tiles each starting from dealer, then one extra to dealer.

    Order each round: seat = (dealer_seat + k) % num_players for k in 0..n-1.
    """
    if num_players < 2:
        raise ValueError(f"num_players must be >= 2, got {num_players}")
    if not 0 <= dealer_seat < num_players:
        raise ValueError(f"dealer_seat out of range: {dealer_seat}")

    hands: list[list[PhysicalTile]] = [[] for _ in range(num_players)]
    for _ in range(13):
        for k in range(num_players):
            seat = (dealer_seat + k) % num_players
            hands[seat].append(deck.draw())
    hands[dealer_seat].append(deck.draw())
    return hands
