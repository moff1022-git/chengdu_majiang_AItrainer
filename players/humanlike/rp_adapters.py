"""Role-scoped RP writes for the F0037 runtime schema."""

from __future__ import annotations

from typing import Any

from players.humanlike.rp_schema import make_envelope
from players.humanlike.runtime import RoundRuntime, RuntimeStateError

ENGINE_RPS = {"RP-001", "RP-002", "RP-003", "RP-004", "RP-005", "RP-006", "RP-007", "RP-008", "RP-009", "RP-010", "RP-011", "RP-012", "RP-013", "RP-014", "RP-030", "RP-031", "RP-032"}
POLICY_RPS = {"RP-010", *{f"RP-{i:03d}" for i in range(15, 30)}}
AUDIT_RPS = {"RP-029", "RP-030", "RP-031", "RP-033"}


def write_rp(runtime: RoundRuntime, parameter_id: str, payload: Any, *, role: str, event_index: int | None = None, owner_seat: int | None = None, visibility: str = "private", lifecycle: str = "event") -> None:
    allowed = {"engine": ENGINE_RPS, "player_policy": POLICY_RPS, "audit": AUDIT_RPS}.get(role)
    if allowed is None:
        raise RuntimeStateError(f"unknown RP writer role: {role}")
    if parameter_id not in allowed:
        raise RuntimeStateError(f"role {role} cannot write {parameter_id}")
    envelope = make_envelope(parameter_id, payload, event_index=runtime.event_index if event_index is None else event_index, owner_seat=owner_seat, visibility=visibility, lifecycle=lifecycle, source=role)
    runtime.set_parameter(parameter_id, envelope)
