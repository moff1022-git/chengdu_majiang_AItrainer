"""Controlled RP-001..RP-033 lifecycle for one humanlike-v2 round."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any

RP_IDS = tuple(f"RP-{index:03d}" for index in range(1, 34))


class RuntimeStateError(ValueError):
    """Raised for invalid RP identifiers or lifecycle transitions."""


class RoundLifecycle(str, Enum):
    CREATED = "created"
    ACTIVE = "active"
    DECIDING = "deciding"
    FINALIZED = "finalized"


@dataclass(frozen=True, slots=True)
class RuntimeSnapshot:
    lifecycle: RoundLifecycle
    event_index: int
    values: Mapping[str, Any]


@dataclass(slots=True)
class RoundRuntime:
    """Owns all 33 RP slots while leaving their domain payloads slice-local."""

    _values: dict[str, Any] = field(default_factory=lambda: dict.fromkeys(RP_IDS))
    lifecycle: RoundLifecycle = RoundLifecycle.CREATED
    event_index: int = 0

    def __post_init__(self) -> None:
        if tuple(self._values) != RP_IDS:
            raise RuntimeStateError("round runtime must contain exactly RP-001 through RP-033")

    @classmethod
    def create_round(
        cls,
        *,
        round_id: str,
        round_index: int,
        dealer_id: int,
        self_seat: int,
        scores: tuple[int, int, int, int],
    ) -> "RoundRuntime":
        if not round_id:
            raise RuntimeStateError("round_id must be non-empty")
        if round_index < 1:
            raise RuntimeStateError("round_index must be >= 1")
        if dealer_id not in range(4) or self_seat not in range(4):
            raise RuntimeStateError("dealer_id and self_seat must be in 0..3")
        if len(scores) != 4 or any(not isinstance(score, int) for score in scores):
            raise RuntimeStateError("scores must contain four integers")
        runtime = cls()
        runtime._values["RP-001"] = {"round_id": round_id, "round_index": round_index, "event_index": 0, "status": "active"}
        runtime._values["RP-002"] = {"dealer_id": dealer_id, "self_seat": self_seat, "active_seats": [0, 1, 2, 3]}
        runtime._values["RP-003"] = {"match_score_before_round": list(scores), "round_ledger": [0, 0, 0, 0]}
        runtime.lifecycle = RoundLifecycle.ACTIVE
        return runtime

    def _ensure_mutable(self) -> None:
        if self.lifecycle is RoundLifecycle.FINALIZED:
            raise RuntimeStateError("finalized round runtime is immutable")

    def set_parameter(self, parameter_id: str, value: Any) -> None:
        self._ensure_mutable()
        if parameter_id not in self._values:
            raise RuntimeStateError(f"unknown round parameter: {parameter_id}")
        self._values[parameter_id] = deepcopy(value)

    def apply_event(self, event: Mapping[str, Any]) -> int:
        self._ensure_mutable()
        if self.lifecycle is RoundLifecycle.DECIDING:
            raise RuntimeStateError("cannot apply an event while a decision is open")
        self.event_index += 1
        self._values["RP-001"]["event_index"] = self.event_index
        self._values["RP-013"] = deepcopy(dict(event)) | {"event_index": self.event_index}
        self.lifecycle = RoundLifecycle.ACTIVE
        return self.event_index

    def begin_decision(self, *, legal_actions: list[Mapping[str, Any]], deadline_ms: int) -> None:
        self._ensure_mutable()
        if self.lifecycle is not RoundLifecycle.ACTIVE:
            raise RuntimeStateError("decision can only begin from active state")
        if not legal_actions:
            raise RuntimeStateError("legal_actions must not be empty")
        if deadline_ms < 0:
            raise RuntimeStateError("deadline_ms must be >= 0")
        self._values["RP-014"] = {"legal_actions": deepcopy(legal_actions), "deadline_ms": deadline_ms}
        self._values["RP-023"] = None
        self._values["RP-026"] = None
        self._values["RP-027"] = {"deadline_ms": deadline_ms}
        self.lifecycle = RoundLifecycle.DECIDING

    def append_decision(self, record: Mapping[str, Any]) -> None:
        self._ensure_mutable()
        if self.lifecycle is not RoundLifecycle.DECIDING:
            raise RuntimeStateError("decision record requires an open decision")
        history = self._values["RP-029"]
        if history is None:
            history = []
            self._values["RP-029"] = history
        history.append(deepcopy(dict(record)) | {"event_index": self.event_index})
        self.lifecycle = RoundLifecycle.ACTIVE

    def finalize_round(self, *, round_result: tuple[int, int, int, int], learning_output: Mapping[str, Any]) -> RuntimeSnapshot:
        self._ensure_mutable()
        if self.lifecycle is RoundLifecycle.DECIDING:
            raise RuntimeStateError("cannot finalize while a decision is open")
        if len(round_result) != 4 or any(not isinstance(score, int) for score in round_result):
            raise RuntimeStateError("round_result must contain four integers")
        self._values["RP-032"] = {"round_result": list(round_result)}
        self._values["RP-033"] = deepcopy(dict(learning_output))
        self._values["RP-001"]["status"] = "finalized"
        self.lifecycle = RoundLifecycle.FINALIZED
        return self.snapshot()

    def snapshot(self) -> RuntimeSnapshot:
        return RuntimeSnapshot(self.lifecycle, self.event_index, MappingProxyType(deepcopy(self._values)))
