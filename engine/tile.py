"""Mahjong tile types for Chengdu / Sichuan (wan, tong, tiao only)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class Suit(str, Enum):
    WAN = "wan"
    TONG = "tong"
    TIAO = "tiao"

    @property
    def sort_key(self) -> int:
        return _SUIT_ORDER[self]


_SUIT_ORDER: dict[Suit, int] = {
    Suit.WAN: 0,
    Suit.TONG: 1,
    Suit.TIAO: 2,
}

_SUIT_BY_NAME: dict[str, Suit] = {s.value: s for s in Suit}


@dataclass(frozen=True, slots=True)
class Tile:
    """Face value only (no instance id). Equal tiles are interchangeable."""

    suit: Suit
    rank: int  # 1..9

    def __post_init__(self) -> None:
        if not isinstance(self.suit, Suit):
            raise ValueError(f"invalid suit: {self.suit!r}")
        if self.rank < 1 or self.rank > 9:
            raise ValueError(f"rank must be 1..9, got {self.rank}")

    @property
    def id(self) -> str:
        return f"{self.suit.value}_{self.rank}"

    def to_asset_parts(self) -> tuple[str, int]:
        """Return (suit, rank) for AssetManager path building."""
        return self.suit.value, self.rank

    def _sort_key(self) -> tuple[int, int]:
        return (self.suit.sort_key, self.rank)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Tile):
            return NotImplemented
        return self._sort_key() < other._sort_key()

    def __str__(self) -> str:
        return self.id


def parse_tile(tile_id: str) -> Tile:
    """Parse ``wan_3`` style id into Tile."""
    if not isinstance(tile_id, str) or not tile_id:
        raise ValueError(f"invalid tile id: {tile_id!r}")
    parts = tile_id.split("_")
    if len(parts) != 2:
        raise ValueError(f"invalid tile id: {tile_id!r}")
    suit_name, rank_s = parts
    suit = _SUIT_BY_NAME.get(suit_name)
    if suit is None:
        raise ValueError(f"invalid tile suit in id: {tile_id!r}")
    try:
        rank = int(rank_s)
    except ValueError as e:
        raise ValueError(f"invalid tile id: {tile_id!r}") from e
    return Tile(suit=suit, rank=rank)


def tiles_to_ids(tiles: Iterable[Tile]) -> list[str]:
    return [t.id for t in tiles]


def ids_to_tiles(ids: Iterable[str]) -> list[Tile]:
    return [parse_tile(i) for i in ids]


def all_tile_faces() -> list[Tile]:
    """27 unique faces: 3 suits × ranks 1..9."""
    return [Tile(suit=s, rank=r) for s in Suit for r in range(1, 10)]


def sorted_tiles(tiles: Iterable[Tile]) -> list[Tile]:
    return sorted(tiles)
