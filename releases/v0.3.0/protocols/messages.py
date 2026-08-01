"""Observation / ActionRequest / Decision message types."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Optional
from uuid import uuid4

from engine.action import Action


@dataclass
class Observation:
    game_id: str
    self_seat: int
    phase: str
    view: dict

    def to_dict(self) -> dict:
        return {
            "game_id": self.game_id,
            "self_seat": self.self_seat,
            "phase": self.phase,
            "view": self.view,
        }


@dataclass
class ActionRequest:
    request_id: str
    seat: int
    phase: str
    legal_actions: list[Action]
    deadline_ms: int | None = None

    @staticmethod
    def create(
        seat: int,
        phase: str,
        legal_actions: list[Action],
        deadline_ms: int | None = None,
    ) -> ActionRequest:
        return ActionRequest(
            request_id=uuid4().hex[:12],
            seat=seat,
            phase=phase,
            legal_actions=list(legal_actions),
            deadline_ms=deadline_ms,
        )

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "seat": self.seat,
            "phase": self.phase,
            "legal_actions": [a.to_dict() for a in self.legal_actions],
            "deadline_ms": self.deadline_ms,
        }


@dataclass
class Decision:
    request_id: str
    action: Action
    reason: str
    analysis: dict | None = None
    think_ms: int | None = None

    def to_dict(self) -> dict:
        d: dict[str, Any] = {
            "request_id": self.request_id,
            "action": self.action.to_dict(),
            "reason": self.reason,
        }
        if self.analysis is not None:
            d["analysis"] = self.analysis
        if self.think_ms is not None:
            d["think_ms"] = self.think_ms
        return d
