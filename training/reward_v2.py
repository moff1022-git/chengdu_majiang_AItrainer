"""Versioned training configuration and PlayerView-only potential shaping."""

from __future__ import annotations

from dataclasses import dataclass, field

from engine.shanten import shanten
from engine.tile import Suit, parse_tile


@dataclass(frozen=True, slots=True)
class ShapingWeights:
    shanten: float = 0.5
    live: float = 0.15
    dingque: float = 0.25
    risk: float = 0.1


@dataclass(frozen=True, slots=True)
class TrainingContractConfig:
    contract_version: int = 1
    illegal_action_mode: str = "raise"
    illegal_action_penalty: float = -1.0
    shaping_enabled: bool = False
    shaping_gamma: float = 0.99
    shaping_weights: ShapingWeights = field(default_factory=ShapingWeights)
    include_cognitive: bool = False

    def __post_init__(self) -> None:
        if self.contract_version not in (1, 2):
            raise ValueError("contract_version must be 1 or 2")
        if self.illegal_action_mode not in ("raise", "terminate"):
            raise ValueError("illegal_action_mode must be raise or terminate")
        if self.illegal_action_penalty > 0:
            raise ValueError("illegal_action_penalty must be <= 0")
        if not 0 <= self.shaping_gamma <= 1:
            raise ValueError("shaping_gamma must be in [0, 1]")


def visible_potential(view: dict, weights: ShapingWeights | None = None) -> tuple[float, dict[str, float]]:
    weights = weights or ShapingWeights()
    players = view.get("players") or []
    own = next((p for p in players if "hand" in p), {})
    hand = []
    for raw in own.get("hand") or []:
        try:
            hand.append(parse_tile(str(raw)))
        except ValueError:
            pass
    dq = Suit(own["dingque"]) if own.get("dingque") else None
    try:
        result = shanten(hand, [], dq)
        shanten_value = max(0.0, min(1.0, (8 - max(-1, result.shanten)) / 9.0))
        live = min(1.0, len(result.ukeire or ()) / 12.0)
    except Exception:
        shanten_value = live = 0.0
    dq_count = sum(tile.suit == dq for tile in hand) if dq else 0
    dingque = 1.0 - dq_count / max(1, len(hand)) if dq else 0.0
    visible = sum(len(p.get("discard_pile") or []) for p in players)
    risk = max(0.0, 1.0 - visible / 108.0)
    parts = {"shanten": shanten_value, "live": live, "dingque": dingque, "risk": risk}
    total = sum(parts[name] * getattr(weights, name) for name in parts)
    return float(total), parts


def shaping_delta(before: float, after: float, *, gamma: float, terminal: bool = False) -> float:
    return gamma * (0.0 if terminal else after) - before
