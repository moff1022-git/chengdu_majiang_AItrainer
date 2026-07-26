"""Lightweight domain events for play loop."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class GameEvent:
    type: str
    payload: dict[str, Any] = field(default_factory=dict)
    turn_index: int = 0

    def to_dict(self) -> dict:
        return asdict(self)
