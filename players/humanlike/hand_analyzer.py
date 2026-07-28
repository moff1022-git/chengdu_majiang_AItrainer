"""Deterministic hand features computed from the player's visible hand."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from engine.action import Action, ActionType
from engine.hand_utils import melds_from_raw, tile_index
from engine.shanten import shanten
from engine.tile import Suit, Tile, parse_tile
from players.humanlike.belief import PublicBelief
from players.humanlike.view import DecisionContext, PolicyInputError


@dataclass(frozen=True, slots=True)
class HandFeatures:
    shanten: int
    speed: float
    hand_value: float
    defense: float
    flexibility: float
    dingque_tiles: int

    def to_dict(self) -> dict[str, float | int]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}


def visible_hand(context: DecisionContext) -> tuple[list[Tile], list, Suit | None]:
    own = context.view.payload["self_player"]
    try:
        hand = [parse_tile(str(item)) for item in own.get("hand", ())]
        melds = melds_from_raw([dict(item) for item in own.get("melds", ())])
        dingque = Suit(own["dingque"]) if own.get("dingque") else None
    except (KeyError, TypeError, ValueError) as exc:
        raise PolicyInputError(f"invalid self hand projection: {exc}") from exc
    return hand, melds, dingque


def _remove_action_tiles(hand: list[Tile], action: Action) -> list[Tile]:
    result = list(hand)
    if action.type == ActionType.DISCARD and action.tiles:
        target = action.tiles[0].id
        for index, tile in enumerate(result):
            if tile.id == target:
                del result[index]
                break
    return result


def analyze_action(context: DecisionContext, action: Action, belief: PublicBelief) -> HandFeatures:
    hand, melds, dingque = visible_hand(context)
    trial = _remove_action_tiles(hand, action)
    result = shanten(trial, melds, dingque)
    counts = Counter(tile.id for tile in trial)
    dq_n = sum(1 for tile in trial if dingque is not None and tile.suit == dingque)

    useful = 0
    if result.ukeire:
        useful = sum(belief.unseen_counts[tile_index(tile)] for tile in result.ukeire)
    speed = max(0.0, min(1.0, (8 - max(-1, result.shanten)) / 9.0 + min(useful, 16) / 64.0))
    if action.type == ActionType.DISCARD and action.tiles and dingque is not None:
        if action.tiles[0].suit == dingque:
            speed = min(1.0, speed + 0.25)

    pairs = sum(1 for value in counts.values() if value >= 2)
    triples = sum(1 for value in counts.values() if value >= 3)
    suit_counts = Counter(tile.suit for tile in trial)
    dominant = max(suit_counts.values(), default=0) / max(1, len(trial))
    hand_value = min(1.0, 0.12 * pairs + 0.16 * triples + 0.45 * dominant)

    if action.tiles:
        idx = tile_index(action.tiles[0])
        defense = 1.0 - belief.danger_by_face[idx]
    else:
        defense = 0.5
    distinct = len(counts)
    neighbor_links = sum(1 for tile in set(trial) if any(other.suit == tile.suit and abs(other.rank - tile.rank) in (1, 2) for other in set(trial)))
    flexibility = min(1.0, 0.6 * distinct / 14.0 + 0.4 * neighbor_links / 14.0)
    return HandFeatures(result.shanten, round(speed, 8), round(hand_value, 8), round(defense, 8), round(flexibility, 8), dq_n)
