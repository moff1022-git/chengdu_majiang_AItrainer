"""Hand counting and meld views for shanten / win / fan."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Sequence

from engine.tile import Suit, Tile, parse_tile

NUM_FACES = 27  # 3 suits × 9 ranks

MeldKind = Literal["pong", "chow", "ming_gang", "an_gang", "jia_gang"]

_GANG_KINDS = frozenset({"ming_gang", "an_gang", "jia_gang"})


@dataclass(frozen=True, slots=True)
class MeldView:
    kind: MeldKind
    tile: Tile

    @property
    def is_gang(self) -> bool:
        return self.kind in _GANG_KINDS

    @property
    def is_pong_or_gang(self) -> bool:
        return self.kind == "pong" or self.is_gang


def tile_index(tile: Tile) -> int:
    return tile.suit.sort_key * 9 + (tile.rank - 1)


def index_to_tile(idx: int) -> Tile:
    suit = (Suit.WAN, Suit.TONG, Suit.TIAO)[idx // 9]
    rank = (idx % 9) + 1
    return Tile(suit, rank)


def tiles_to_counts(tiles: Iterable[Tile]) -> list[int]:
    counts = [0] * NUM_FACES
    for t in tiles:
        counts[tile_index(t)] += 1
    return counts


def counts_to_tiles(counts: Sequence[int]) -> list[Tile]:
    out: list[Tile] = []
    for i, c in enumerate(counts):
        t = index_to_tile(i)
        out.extend([t] * c)
    return out


def suit_indices(suit: Suit) -> range:
    base = suit.sort_key * 9
    return range(base, base + 9)


def count_suit_tiles(counts: Sequence[int], suit: Suit) -> int:
    return sum(counts[i] for i in suit_indices(suit))


def has_suit(tiles: Iterable[Tile], suit: Suit) -> bool:
    return any(t.suit == suit for t in tiles)


def melds_have_suit(melds: Sequence[MeldView], suit: Suit) -> bool:
    return any(m.tile.suit == suit for m in melds)


def melds_from_raw(raw: Sequence) -> list[MeldView]:
    """Accept MeldView or dict {kind, tile|tile_id}."""
    out: list[MeldView] = []
    for item in raw or []:
        if isinstance(item, MeldView):
            out.append(item)
            continue
        if not isinstance(item, dict):
            raise ValueError(f"invalid meld: {item!r}")
        kind = item["kind"]
        if "tile" in item:
            tile = item["tile"]
            if isinstance(tile, str):
                tile = parse_tile(tile)
            elif not isinstance(tile, Tile):
                raise ValueError(f"invalid meld tile: {tile!r}")
        elif "tile_id" in item:
            tile = parse_tile(str(item["tile_id"]))
        else:
            raise ValueError(f"meld missing tile: {item!r}")
        out.append(MeldView(kind=kind, tile=tile))
    return out


def expected_hand_len(num_melds: int) -> int:
    """Closed-hand length including win tile: 14 - 3 * num_melds."""
    return 14 - 3 * num_melds


def copy_counts(counts: Sequence[int]) -> list[int]:
    return list(counts)
