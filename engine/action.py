"""Player/engine actions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from engine.tile import Suit, Tile, parse_tile


class ActionType(str, Enum):
    EXCHANGE = "exchange"
    DINGQUE = "dingque"
    DISCARD = "discard"
    PASS = "pass"
    PONG = "pong"
    GANG_MING = "gang_ming"
    GANG_AN = "gang_an"
    GANG_JIA = "gang_jia"
    HU = "hu"


@dataclass(frozen=True, slots=True)
class Action:
    type: ActionType
    tiles: tuple[Tile, ...] = ()
    suit: Optional[Suit] = None

    def to_dict(self) -> dict:
        d: dict = {"type": self.type.value}
        if self.tiles:
            d["tiles"] = [t.id for t in self.tiles]
        if self.suit is not None:
            d["suit"] = self.suit.value
        return d

    @classmethod
    def from_dict(cls, data: dict) -> Action:
        typ = ActionType(data["type"])
        tiles_raw = data.get("tiles") or []
        tiles = tuple(parse_tile(t) if isinstance(t, str) else t for t in tiles_raw)
        suit_raw = data.get("suit")
        suit = Suit(suit_raw) if suit_raw else None
        return cls(type=typ, tiles=tiles, suit=suit)

    def __str__(self) -> str:
        extra = ""
        if self.tiles:
            extra = ":" + ",".join(t.id for t in self.tiles)
        if self.suit:
            extra += f":{self.suit.value}"
        return f"{self.type.value}{extra}"
