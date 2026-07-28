"""Frozen, versioned player-perspective view."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

PLAYER_VIEW_VERSION = 2


def freeze_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    def freeze(item: Any) -> Any:
        if isinstance(item, Mapping):
            return MappingProxyType({str(key): freeze(child) for key, child in item.items()})
        if isinstance(item, list):
            return tuple(freeze(child) for child in item)
        if isinstance(item, tuple):
            return tuple(freeze(child) for child in item)
        return item

    return freeze(value)


def thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: thaw(child) for key, child in value.items()}
    if isinstance(value, tuple):
        return [thaw(child) for child in value]
    return value


@dataclass(frozen=True, slots=True)
class PlayerViewV2:
    game_id: str
    self_seat: int
    phase: str
    event_index: int
    payload: Mapping[str, Any]
    view_version: int = PLAYER_VIEW_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", freeze_mapping(self.payload))

    def to_legacy_dict(self) -> dict[str, Any]:
        result = thaw(self.payload)
        result.pop("wall", None)
        own = result.pop("self_player")
        others = result.pop("other_players")
        players = sorted([own, *others], key=lambda player: player["seat"])
        result["players"] = players
        result["exchange_dir_resolved"] = result.pop("exchange_direction_public", None)
        for player in players:
            player.pop("physical_hand", None)
            player.pop("revealed_hand", None)
            player.pop("revealed_hand_count", None)
        result["view_version"] = self.view_version
        result["game_id"] = self.game_id
        result["phase"] = self.phase
        return result
