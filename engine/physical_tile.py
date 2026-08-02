"""Unique physical tiles for the 108-tile Chengdu Mahjong wall."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
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
    wall = [physical_tile(tile_id) for tile_id in range(PHYSICAL_TILE_COUNT)]
    regions = {name: [] for name in PHYSICAL_REGIONS}
    regions["wall"] = [tile.tile_id for tile in wall]
    validate_physical_ownership(regions)
    return wall


def face_of(tile: Tile | PhysicalTile) -> Tile:
    return tile.face if isinstance(tile, PhysicalTile) else tile


class PhysicalOwnershipError(ValueError):
    """Stable ALGO-001 validation failure carrying a specification error code."""

    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        super().__init__(f"{code}: {detail}" if detail else code)


PHYSICAL_REGIONS = (
    "wall", *(f"hand:S{i}" for i in range(4)), *(f"discard:S{i}" for i in range(4)),
    *(f"meld:S{i}" for i in range(4)), *(f"exchange_pool:S{i}" for i in range(4)),
    "pending_discard", "pending_gang", "removed",
)


def validate_physical_ownership(regions: Mapping[str, Sequence[int]]) -> dict[str, object]:
    """ALGO-001 canonical ownership projection and 108-tile conservation check."""
    if not isinstance(regions, Mapping):
        raise PhysicalOwnershipError("SCHEMA_INVALID")
    unknown = sorted(set(regions) - set(PHYSICAL_REGIONS))
    if unknown:
        raise PhysicalOwnershipError("REGION_UNKNOWN", ",".join(unknown))
    missing_regions = sorted(set(PHYSICAL_REGIONS) - set(regions))
    if missing_regions:
        raise PhysicalOwnershipError("REGION_MISSING", ",".join(missing_regions))
    owners: dict[int, str] = {}
    face_counts = [0] * 27
    region_counts: dict[str, int] = {}
    for region in sorted(regions):
        values = regions[region]
        if not isinstance(region, str) or not isinstance(values, (list, tuple)):
            raise PhysicalOwnershipError("SCHEMA_INVALID")
        region_counts[region] = len(values)
        for tile_id in values:
            if not isinstance(tile_id, int) or isinstance(tile_id, bool) or not 0 <= tile_id < 108:
                raise PhysicalOwnershipError("PHYSICAL_ID_RANGE", repr(tile_id))
            if tile_id in owners:
                raise PhysicalOwnershipError("OWNERSHIP_DUPLICATE", str(tile_id))
            owners[tile_id] = region
            face_counts[tile_id // 4] += 1
    missing = sorted(set(range(108)) - owners.keys())
    if missing:
        raise PhysicalOwnershipError("OWNERSHIP_MISSING", ",".join(map(str, missing)))
    if any(count > 4 for count in face_counts):
        raise PhysicalOwnershipError("FACE_COUNT_EXCEEDED")
    return {"conserved": True, "region_counts": region_counts, "face_counts": tuple(face_counts), "owner_by_id": tuple(owners[i] for i in range(108))}
