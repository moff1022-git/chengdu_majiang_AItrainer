"""108-tile wall: build, shuffle, deal."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from engine.tile import Suit, Tile


def build_full_wall() -> list[Tile]:
    """Fixed order: suit (wan, tong, tiao) × rank 1..9 × 4 copies."""
    wall: list[Tile] = []
    for suit in Suit:
        for rank in range(1, 10):
            face = Tile(suit=suit, rank=rank)
            wall.extend([face, face, face, face])
    return wall


def shuffle_wall(wall: list[Tile], shuffle_seed: int) -> list[Tile]:
    """Return a new shuffled list (does not mutate input)."""
    out = list(wall)
    random.Random(shuffle_seed).shuffle(out)
    return out


@dataclass
class Deck:
    """Wall with draw pointer; remaining tiles are ``tiles[index:]``."""

    tiles: list[Tile] = field(default_factory=build_full_wall)
    index: int = 0

    @classmethod
    def create_shuffled(cls, shuffle_seed: int) -> Deck:
        return cls(tiles=shuffle_wall(build_full_wall(), shuffle_seed), index=0)

    @property
    def remaining(self) -> int:
        return len(self.tiles) - self.index

    def draw(self) -> Tile:
        if self.index >= len(self.tiles):
            raise ValueError("wall is empty")
        tile = self.tiles[self.index]
        self.index += 1
        return tile

    def remaining_tiles(self) -> list[Tile]:
        return list(self.tiles[self.index :])


def deal_hands(
    deck: Deck,
    *,
    num_players: int,
    dealer_seat: int,
) -> list[list[Tile]]:
    """
    Deal 13 tiles each starting from dealer, then one extra to dealer.

    Order each round: seat = (dealer_seat + k) % num_players for k in 0..n-1.
    """
    if num_players < 2:
        raise ValueError(f"num_players must be >= 2, got {num_players}")
    if not 0 <= dealer_seat < num_players:
        raise ValueError(f"dealer_seat out of range: {dealer_seat}")

    hands: list[list[Tile]] = [[] for _ in range(num_players)]
    for _ in range(13):
        for k in range(num_players):
            seat = (dealer_seat + k) % num_players
            hands[seat].append(deck.draw())
    hands[dealer_seat].append(deck.draw())
    return hands
