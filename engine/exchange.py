"""Exchange-three direction, validation, and hand multiset ops."""

from __future__ import annotations

from collections import Counter
from typing import Iterable, Literal

from engine.config import EngineConfig
from engine.state import GameState
from engine.tile import Suit, Tile

ResolvedDir = Literal["clockwise", "counterclockwise", "across"]

_VALID_RESOLVED = frozenset({"clockwise", "counterclockwise", "across"})


class ExchangeError(ValueError):
    """Invalid exchange selection or resolve failure."""


def across_offset(num_players: int) -> int:
    if num_players == 4:
        return 2
    return 1  # 2p and 3p


def destination_seat(seat: int, direction: ResolvedDir, num_players: int) -> int:
    if direction == "clockwise":
        return (seat + 1) % num_players
    if direction == "counterclockwise":
        return (seat - 1) % num_players
    if direction == "across":
        return (seat + across_offset(num_players)) % num_players
    raise ExchangeError(f"invalid direction: {direction!r}")


def resolve_exchange_direction(
    state: GameState, config: EngineConfig | None = None
) -> ResolvedDir:
    """Resolve configured direction; auto_dice uses dice.total % 3."""
    if config is None:
        config = EngineConfig.from_dict(state.config) if state.config else EngineConfig()
    mode = config.exchange_dir
    if mode in _VALID_RESOLVED:
        return mode  # type: ignore[return-value]
    if mode == "auto_dice":
        r = state.dice.total % 3
        if r == 0:
            return "clockwise"
        if r == 1:
            return "across"
        return "counterclockwise"
    raise ExchangeError(f"invalid exchange_dir: {mode!r}")


def validate_exchange_tiles(hand: list[Tile], tiles: list[Tile]) -> list[Tile]:
    """
    Ensure exactly 3 tiles, same suit, multiset-subset of hand.
    Returns the 3 tiles (same objects/values as given).
    """
    if len(tiles) != 3:
        raise ExchangeError(f"exchange requires exactly 3 tiles, got {len(tiles)}")
    suits = {t.suit for t in tiles}
    if len(suits) != 1:
        raise ExchangeError("exchange tiles must be the same suit")

    hand_counts = Counter(t.id for t in hand)
    offer_counts = Counter(t.id for t in tiles)
    for tid, need in offer_counts.items():
        if hand_counts[tid] < need:
            raise ExchangeError(f"hand missing tiles for exchange: {tid}")
    return list(tiles)


def remove_tiles_from_hand(hand: list[Tile], tiles: Iterable[Tile]) -> list[Tile]:
    """Return new hand list with multiset of tiles removed."""
    remaining = list(hand)
    for tile in tiles:
        for i, h in enumerate(remaining):
            if h.id == tile.id:
                del remaining[i]
                break
        else:
            raise ExchangeError(f"cannot remove {tile.id} from hand")
    return remaining


def hand_has_same_suit_triple(hand: list[Tile]) -> bool:
    by_suit: dict[Suit, int] = {}
    for t in hand:
        by_suit[t.suit] = by_suit.get(t.suit, 0) + 1
    return any(c >= 3 for c in by_suit.values())


def pick_same_suit_triple(hand: list[Tile]) -> list[Tile]:
    """
    Deterministic helper for tests: pick first suit (wan/tong/tiao order)
    that has >=3 tiles, take first 3 of that suit in hand order.
    """
    for suit in Suit:
        chosen = [t for t in hand if t.suit == suit]
        if len(chosen) >= 3:
            return chosen[:3]
    raise ExchangeError("hand has no same-suit triple")
