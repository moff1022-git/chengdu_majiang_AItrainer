"""STATE-004 guarded, versioned phase transition facade."""

from __future__ import annotations

from dataclasses import dataclass
from copy import deepcopy
from enum import Enum
from threading import RLock
from typing import Any, Mapping

from engine.audit import canonical_hash


class RoundPhase(str, Enum):
    CONFIGURED = "CONFIGURED"
    DEALT = "DEALT"
    EXCHANGE = "EXCHANGE"
    DINGQUE = "DINGQUE"
    READY = "READY"
    DRAW = "DRAW"
    DISCARD = "DISCARD"
    RESPONSE = "RESPONSE"
    FINISHED = "FINISHED"
    SETTLED = "SETTLED"


LEGACY_PHASES = {phase.value.lower(): phase for phase in RoundPhase if phase is not RoundPhase.CONFIGURED and phase is not RoundPhase.SETTLED}


class RoundStateError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class TransitionRequest:
    event_id: str
    expected_state_version: int
    event_type: str
    actor: str
    payload: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class RoundSnapshot:
    phase: RoundPhase
    state_version: int
    active_seats: tuple[int, ...]
    wall_remaining: int
    settlement_hash: str | None = None
    authority_hash: str | None = None
    pending_claim_seats: tuple[int, ...] = ()
    current_seat: int | None = None


@dataclass(frozen=True, slots=True)
class TransitionResult:
    accepted: bool
    snapshot: RoundSnapshot
    error_code: str | None
    audit_ref: str
    notify: tuple[str, ...] = ()


def phase_from_legacy(value: str, *, end_settled: bool = False) -> RoundPhase:
    if value == "finished" and end_settled:
        return RoundPhase.SETTLED
    try:
        return LEGACY_PHASES[value]
    except (KeyError, TypeError) as exc:
        raise RoundStateError("SCHEMA_INVALID", f"unknown legacy phase: {value!r}") from exc


def phase_to_legacy(value: RoundPhase) -> tuple[str, bool]:
    if value is RoundPhase.CONFIGURED:
        raise RoundStateError("SCHEMA_INVALID", "CONFIGURED has no persisted GameState v5 representation")
    if value is RoundPhase.SETTLED:
        return "finished", True
    return value.value.lower(), False


_EVENT_EDGES: dict[tuple[RoundPhase, str], RoundPhase] = {
    (RoundPhase.CONFIGURED, "DEAL_COMMITTED"): RoundPhase.DEALT,
    (RoundPhase.DEALT, "EXCHANGE_STARTED"): RoundPhase.EXCHANGE,
    (RoundPhase.DEALT, "EXCHANGE_SKIPPED"): RoundPhase.DINGQUE,
    (RoundPhase.EXCHANGE, "EXCHANGE_RESOLVED"): RoundPhase.DINGQUE,
    (RoundPhase.DINGQUE, "DINGQUE_RESOLVED"): RoundPhase.READY,
    (RoundPhase.READY, "PLAY_STARTED"): RoundPhase.DISCARD,
    (RoundPhase.DRAW, "DRAW_COMPLETED"): RoundPhase.DISCARD,
    (RoundPhase.DISCARD, "DISCARD_COMMITTED"): RoundPhase.RESPONSE,
    (RoundPhase.RESPONSE, "CLAIMS_PASSED"): RoundPhase.DRAW,
    (RoundPhase.RESPONSE, "PONG_COMMITTED"): RoundPhase.DISCARD,
    (RoundPhase.RESPONSE, "GANG_COMMITTED"): RoundPhase.DRAW,
    (RoundPhase.DISCARD, "GANG_COMMITTED"): RoundPhase.DRAW,
    (RoundPhase.FINISHED, "SETTLEMENT_COMMITTED"): RoundPhase.SETTLED,
}


class RoundStateMachine:
    def __init__(self, snapshot: RoundSnapshot, *, outbox=None):
        self._snapshot = snapshot
        self._events: dict[str, tuple[str, TransitionResult]] = {}
        self._lock = RLock()
        self._outbox = outbox
        self.audit_records: list[Mapping[str, Any]] = []

    @property
    def snapshot(self) -> RoundSnapshot:
        return self._snapshot

    def transition(self, request: TransitionRequest) -> TransitionResult:
        with self._lock:
            return self._transition_locked(request)

    def _transition_locked(self, request: TransitionRequest) -> TransitionResult:
        if not request.event_id or not request.actor or request.expected_state_version < 0:
            return self._reject("SCHEMA_INVALID", request)
        payload_hash = canonical_hash({"event_id": request.event_id, "version": request.expected_state_version, "event_type": request.event_type, "actor": request.actor, "payload": dict(request.payload)})
        old = self._events.get(request.event_id)
        if old:
            return old[1] if old[0] == payload_hash else self._reject("EVENT_PHASE_MISMATCH", request)
        if self._snapshot.phase is RoundPhase.SETTLED:
            return self._remember(payload_hash, request, self._reject("TERMINAL_STATE", request))
        if request.expected_state_version != self._snapshot.state_version:
            return self._remember(payload_hash, request, self._reject("VERSION_CONFLICT", request))
        try:
            target, active, wall, settlement_hash = self._resolve(request)
        except RoundStateError as exc:
            return self._remember(payload_hash, request, self._reject(exc.code, request))
        authority_hash = request.payload.get("authority_hash", self._snapshot.authority_hash)
        pending = tuple(sorted(int(x) for x in request.payload.get("pending_claim_seats", self._snapshot.pending_claim_seats)))
        current = request.payload.get("current_seat", self._snapshot.current_seat)
        phase_before = self._snapshot.phase
        updated = RoundSnapshot(target, self._snapshot.state_version + 1, active, wall, settlement_hash, authority_hash, pending, current)
        audit = canonical_hash({"unit_id": "STATE-004", "accepted": True, "before": phase_before.value, "after": target.value, "version": updated.state_version, "event": payload_hash})
        result = TransitionResult(True, updated, None, audit, ("STATE-002", "STATE-009", "TRAIN-001"))
        self._snapshot = updated
        record = {"unit_id": "STATE-004", "event_id": request.event_id, "phase_before": phase_before.value, "phase_after": target.value, "state_version_after": updated.state_version, "input_hash": payload_hash, "result_hash": audit, "accepted": True}
        self.audit_records.append(record)
        remembered = self._remember(payload_hash, request, result)
        if self._outbox is not None:
            try:
                self._outbox(remembered)
            except Exception:
                pass
        return remembered

    def _resolve(self, req: TransitionRequest) -> tuple[RoundPhase, tuple[int, ...], int, str | None]:
        phase = self._snapshot.phase
        active = self._snapshot.active_seats
        wall = self._snapshot.wall_remaining
        settlement = self._snapshot.settlement_hash
        if req.event_type == "HU_RESOLVED" and phase in {RoundPhase.DISCARD, RoundPhase.RESPONSE}:
            hu = tuple(sorted(set(int(x) for x in req.payload.get("hu_seats", ()))))
            if not hu or any(seat not in active for seat in hu):
                raise RoundStateError("GUARD_FAILED", "hu seats are not active")
            active = tuple(seat for seat in active if seat not in hu)
            return (RoundPhase.FINISHED if len(active) <= 1 or wall <= 0 else RoundPhase.DRAW, active, wall, settlement)
        if req.event_type == "WALL_EXHAUSTED" and phase in {RoundPhase.DRAW, RoundPhase.DISCARD, RoundPhase.RESPONSE}:
            return RoundPhase.FINISHED, active, 0, settlement
        if req.event_type == "GAME_FINISHED" and phase in {RoundPhase.DRAW, RoundPhase.DISCARD, RoundPhase.RESPONSE}:
            return RoundPhase.FINISHED, active, wall, settlement
        target = _EVENT_EDGES.get((phase, req.event_type))
        if target is None:
            raise RoundStateError("ILLEGAL_TRANSITION", f"{phase.value} cannot consume {req.event_type}")
        if req.event_type == "GANG_COMMITTED" and wall <= 0:
            target = RoundPhase.FINISHED
        if req.event_type == "SETTLEMENT_COMMITTED":
            raw_hash = req.payload.get("settlement_hash")
            if not isinstance(raw_hash, str) or len(raw_hash) != 64:
                raise RoundStateError("INVARIANT_FAILED", "settlement hash required")
            settlement = raw_hash
        return target, active, wall, settlement

    def _reject(self, code: str, req: TransitionRequest) -> TransitionResult:
        audit = canonical_hash({"unit_id": "STATE-004", "accepted": False, "phase": self._snapshot.phase.value, "version": self._snapshot.state_version, "event_id": req.event_id, "error": code})
        return TransitionResult(False, self._snapshot, code, audit)

    def _remember(self, payload_hash: str, req: TransitionRequest, result: TransitionResult) -> TransitionResult:
        self._events[req.event_id] = (payload_hash, result)
        return result

    def observe_legacy_commit(self, state: Any, *, event_id: str) -> TransitionResult:
        """Record an already-committed v5 authority state at the compatibility boundary."""
        phase = phase_from_legacy(state.phase, end_settled=bool(getattr(state, "end_settled", False)))
        active = tuple(sorted(player.seat for player in state.players if player.status == "active"))
        pending = tuple(sorted((state.pending_claims or {}).keys()))
        authority_hash = canonical_hash(state.to_dict())
        with self._lock:
            before = self._snapshot
            if before.phase is phase and before.authority_hash == authority_hash:
                return TransitionResult(True, before, None, canonical_hash({"unit_id": "STATE-004", "event_id": event_id, "unchanged": authority_hash}))
            updated = RoundSnapshot(phase, before.state_version + 1, active, len(state.wall), before.settlement_hash, authority_hash, pending, state.current_seat)
            audit = canonical_hash({"unit_id": "STATE-004", "event_id": event_id, "before": before.phase.value, "after": phase.value, "version": updated.state_version, "authority_hash": authority_hash})
            result = TransitionResult(True, updated, None, audit, ("STATE-002", "STATE-009", "TRAIN-001"))
            self._snapshot = updated
            self.audit_records.append({"unit_id": "STATE-004", "event_id": event_id, "phase_before": before.phase.value, "phase_after": phase.value, "state_version_before": before.state_version, "state_version_after": updated.state_version, "result_hash": audit, "authority_hash": authority_hash, "accepted": True})
            if self._outbox is not None:
                try:
                    self._outbox(result)
                except Exception:
                    pass
            return result

    def apply_legacy_transaction(self, state: Any, *, event_id: str, mutation) -> TransitionResult:
        """Atomically apply one legacy authority mutation and commit its STATE-004 projection."""
        before_data = deepcopy(state.to_dict())
        before_snapshot = self._snapshot
        try:
            mutation()
            state.validate()
        except Exception:
            restored = type(state).from_dict(before_data)
            for name in state.__dataclass_fields__:
                setattr(state, name, deepcopy(getattr(restored, name)))
            return self._reject_transaction(event_id, "INVARIANT_FAILED", before_snapshot)

        try:
            phase = phase_from_legacy(state.phase, end_settled=bool(getattr(state, "end_settled", False)))
            active = tuple(sorted(player.seat for player in state.players if player.status == "active"))
            pending = tuple(sorted((state.pending_claims or {}).keys()))
            authority_hash = canonical_hash(state.to_dict())
        except Exception:
            restored = type(state).from_dict(before_data)
            for name in state.__dataclass_fields__:
                setattr(state, name, deepcopy(getattr(restored, name)))
            return self._reject_transaction(event_id, "INVARIANT_FAILED", before_snapshot)

        with self._lock:
            updated = RoundSnapshot(phase, before_snapshot.state_version + 1, active, len(state.wall), before_snapshot.settlement_hash, authority_hash, pending, state.current_seat)
            audit = canonical_hash({"unit_id": "STATE-004", "event_id": event_id, "before": canonical_hash(before_data), "after": authority_hash, "version": updated.state_version})
            result = TransitionResult(True, updated, None, audit, ("STATE-002", "STATE-009", "TRAIN-001"))
            self._snapshot = updated
            self.audit_records.append({"unit_id": "STATE-004", "event_id": event_id, "phase_before": before_snapshot.phase.value, "phase_after": phase.value, "state_version_before": before_snapshot.state_version, "state_version_after": updated.state_version, "input_hash": canonical_hash(before_data), "result_hash": audit, "authority_hash": authority_hash, "accepted": True})
            if self._outbox is not None:
                try:
                    self._outbox(result)
                except Exception:
                    pass
            return result

    def _reject_transaction(self, event_id: str, code: str, snapshot: RoundSnapshot) -> TransitionResult:
        audit = canonical_hash({"unit_id": "STATE-004", "event_id": event_id, "accepted": False, "error": code, "version": snapshot.state_version})
        return TransitionResult(False, snapshot, code, audit)
