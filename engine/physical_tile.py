"""Unique physical tiles for the 108-tile Chengdu Mahjong wall."""

from __future__ import annotations

from dataclasses import dataclass

from engine.tile import Suit, Tile

PHYSICAL_TILE_COUNT = 108
COPIES_PER_FACE = 4


@dataclass(frozen=True, slots=True, eq=False)
class PhysicalTile:
    """One concrete tile while preserving the legacy face-level interface."""

    tile_id: int
    face: Tile

    def __post_init__(self) -> None:
        if not isinstance(self.tile_id, int) or isinstance(self.tile_id, bool):
            raise ValueError("tile_id must be an integer")
        if not 0 <= self.tile_id < PHYSICAL_TILE_COUNT:
            raise ValueError(f"tile_id must be 0..107, got {self.tile_id}")
        if self.face != face_from_physical_id(self.tile_id):
            raise ValueError(
                f"tile_id {self.tile_id} does not match face {self.face.id}"
            )

    @property
    def id(self) -> str:
        """Legacy face id used by actions, UI and face-level algorithms."""
        return self.face.id

    @property
    def face_id(self) -> str:
        return self.face.id

    @property
    def suit(self) -> Suit:
        return self.face.suit

    @property
    def rank(self) -> int:
        return self.face.rank

    @property
    def copy_index(self) -> int:
        return self.tile_id % COPIES_PER_FACE

    def to_asset_parts(self) -> tuple[str, int]:
        return self.face.to_asset_parts()

    def _sort_key(self) -> tuple[int, int, int]:
        return (self.suit.sort_key, self.rank, self.tile_id)

    def __lt__(self, other: object) -> bool:
        if isinstance(other, PhysicalTile):
            return self._sort_key() < other._sort_key()
        if isinstance(other, Tile):
            return (self.suit.sort_key, self.rank) < (other.suit.sort_key, other.rank)
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PhysicalTile):
            return self.tile_id == other.tile_id
        if isinstance(other, Tile):
            return self.face == other
        return False

    def __hash__(self) -> int:
        return hash(self.tile_id)

    def __str__(self) -> str:
        return self.face_id


def tile_type_from_face(face: Tile) -> int:
    return face.suit.sort_key * 9 + (face.rank - 1)


def physical_id_for(face: Tile, copy_index: int) -> int:
    if not isinstance(copy_index, int) or not 0 <= copy_index < COPIES_PER_FACE:
        raise ValueError(f"copy_index must be 0..3, got {copy_index!r}")
    return tile_type_from_face(face) * COPIES_PER_FACE + copy_index


def face_from_physical_id(tile_id: int) -> Tile:
    if not isinstance(tile_id, int) or isinstance(tile_id, bool) or not 0 <= tile_id < PHYSICAL_TILE_COUNT:
        raise ValueError(f"tile_id must be 0..107, got {tile_id!r}")
    tile_type = tile_id // COPIES_PER_FACE
    suit = (Suit.WAN, Suit.TONG, Suit.TIAO)[tile_type // 9]
    return Tile(suit, tile_type % 9 + 1)


def physical_tile(tile_id: int) -> PhysicalTile:
    return PhysicalTile(tile_id=tile_id, face=face_from_physical_id(tile_id))


def build_physical_wall() -> list[PhysicalTile]:
    return [physical_tile(tile_id) for tile_id in range(PHYSICAL_TILE_COUNT)]


def face_of(tile: Tile | PhysicalTile) -> Tile:
    return tile.face if isinstance(tile, PhysicalTile) else tile
