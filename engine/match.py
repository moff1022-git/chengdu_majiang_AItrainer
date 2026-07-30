"""STATE-001 atomic match creation and multi-round control facade."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from threading import RLock
from typing import Any, Callable, Mapping, Sequence

from engine.audit import canonical_hash


class MatchError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class SeatBinding:
    seat: int
    player_id: str
    profile_id: str
    style_id: str = "balanced"


@dataclass(frozen=True, slots=True)
class MatchCreateRequest:
    event_id: str
    match_id: str
    expected_state_version: int
    ruleset_hash: str
    config_hash: str
    seed_trace_ref: str
    bindings: tuple[SeatBinding, ...]
    total_rounds: int
    starting_scores: Mapping[int, int]
    dealer_policy: str = "dice"
    rules_version: str = "CDMJ-AI-RULES 1.0.0"
    parameter_version: str = "CDMJ-AI-PARAMS 2.0.0"
    contract_version: str = "CDMJ-CONTRACTS 2.0.0"
    canonical_version: str = "CDMJ canonical-jcs-nfc-v2 profile"
    rng_version: int = 2
    frozen_config: Any | None = None

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "MatchCreateRequest":
        allowed = set(cls.__dataclass_fields__)
        if set(raw) != allowed - {"frozen_config"} and set(raw) != allowed:
            raise MatchError("SCHEMA_INVALID", "request fields do not match schema")
        try:
            values = dict(raw)
            values["bindings"] = tuple(SeatBinding(**item) if isinstance(item, Mapping) else item for item in values["bindings"])
            return cls(**values)
        except (KeyError, TypeError, ValueError) as exc:
            raise MatchError("SCHEMA_INVALID", "invalid match request") from exc


@dataclass(frozen=True, slots=True)
class MatchContext:
    match_id: str
    state_version: int
    ruleset_hash: str
    config_hash: str
    seed_trace_ref: str
    bindings: tuple[SeatBinding, ...]
    total_rounds: int
    current_round: int
    starting_scores: Mapping[int, int]
    dealer_policy: str
    rules_version: str
    parameter_version: str
    contract_version: str
    canonical_version: str
    rng_version: int
    fingerprint: str
    config_canonical_bytes: bytes = b""

    def public_projection(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "match_id": self.match_id,
            "state_version": self.state_version,
            "total_rounds": self.total_rounds,
            "current_round": self.current_round,
            "scores": dict(self.starting_scores),
            "ruleset_hash": self.ruleset_hash,
            "config_hash": self.config_hash,
            "seed_trace_ref": self.seed_trace_ref,
        })


@dataclass(frozen=True, slots=True)
class MatchResult:
    match_id: str
    status: str
    state_version: int
    rounds_completed: int
    scores: Mapping[int, int]
    rankings: tuple[int, ...]
    fingerprint: str


@dataclass(frozen=True, slots=True)
class MatchOperationResult:
    accepted: bool
    context: MatchContext | None = None
    match_result: MatchResult | None = None
    error_code: str | None = None
    next_state_version: int | None = None
    audit_ref: str | None = None


def _request_payload(req: MatchCreateRequest) -> dict[str, Any]:
    return {
        "event_id": req.event_id, "match_id": req.match_id,
        "expected_state_version": req.expected_state_version,
        "ruleset_hash": req.ruleset_hash, "config_hash": req.config_hash,
        "seed_trace_ref": req.seed_trace_ref,
        "bindings": [
            {"seat": b.seat, "player_id": b.player_id, "profile_id": b.profile_id, "style_id": b.style_id}
            for b in sorted(req.bindings, key=lambda item: item.seat)
        ],
        "total_rounds": req.total_rounds,
        "starting_scores": {str(k): int(v) for k, v in sorted(req.starting_scores.items())},
        "dealer_policy": req.dealer_policy,
        "versions": [req.rules_version, req.parameter_version, req.contract_version, req.canonical_version, req.rng_version],
    }


class MatchController:
    """Single-writer controller; failed operations publish no partial context."""

    def __init__(self) -> None:
        self._context: MatchContext | None = None
        self._scores: dict[int, int] = {}
        self._rounds_completed = 0
        self._events: dict[str, tuple[str, MatchOperationResult]] = {}
        self._lock = RLock()
        self._prepared_players: tuple[Any, ...] = ()

    @property
    def context(self) -> MatchContext | None:
        return self._context

    def create(
        self,
        request: MatchCreateRequest,
        *,
        player_factories: Mapping[int, Callable[[], Any]] | None = None,
    ) -> MatchOperationResult:
        with self._lock:
            return self._create_locked(request, player_factories=player_factories)

    def _create_locked(
        self,
        request: MatchCreateRequest,
        *,
        player_factories: Mapping[int, Callable[[], Any]] | None = None,
    ) -> MatchOperationResult:
        try:
            payload_hash = canonical_hash(_request_payload(request))
        except Exception:
            return MatchOperationResult(False, error_code="SCHEMA_INVALID", next_state_version=0)
        old = self._events.get(request.event_id)
        if old:
            return old[1] if old[0] == payload_hash else MatchOperationResult(False, error_code="INVALID_MATCH_REQUEST", next_state_version=self._version)
        if self._context is not None or request.expected_state_version != 0:
            return MatchOperationResult(False, error_code="VERSION_CONFLICT", next_state_version=self._version)
        error = self._validate(request)
        if error:
            result = MatchOperationResult(False, error_code=error, next_state_version=0)
            self._events[request.event_id] = (payload_hash, result)
            return result

        prepared: list[Any] = []
        try:
            if player_factories is not None:
                if set(player_factories) != {b.seat for b in request.bindings}:
                    raise MatchError("INVALID_MATCH_REQUEST", "factory seats mismatch")
                prepared = [player_factories[b.seat]() for b in sorted(request.bindings, key=lambda x: x.seat)]
                if any(item is None for item in prepared):
                    raise MatchError("INVALID_MATCH_REQUEST", "factory returned no player")
        except Exception as exc:
            for item in prepared:
                close = getattr(item, "close", None)
                if callable(close):
                    close()
            code = exc.code if isinstance(exc, MatchError) else "INVARIANT_FAILED"
            result = MatchOperationResult(False, error_code=code, next_state_version=0)
            self._events[request.event_id] = (payload_hash, result)
            return result

        scores = {int(k): int(v) for k, v in sorted(request.starting_scores.items())}
        bindings = tuple(sorted(request.bindings, key=lambda item: item.seat))
        config_bytes = bytes(getattr(request.frozen_config, "canonical_bytes", b""))
        context_data = {**_request_payload(request), "state_version": 1, "current_round": 0}
        context = MatchContext(
            match_id=request.match_id, state_version=1,
            ruleset_hash=request.ruleset_hash, config_hash=request.config_hash,
            seed_trace_ref=request.seed_trace_ref, bindings=bindings,
            total_rounds=request.total_rounds, current_round=0,
            starting_scores=MappingProxyType(scores.copy()), dealer_policy=request.dealer_policy,
            rules_version=request.rules_version, parameter_version=request.parameter_version,
            contract_version=request.contract_version, canonical_version=request.canonical_version,
            rng_version=request.rng_version, fingerprint=canonical_hash(context_data),
            config_canonical_bytes=config_bytes,
        )
        # Publication is the sole commit point. on_join is deliberately left to
        # the legacy adapter after every factory has prepared successfully.
        self._scores = scores
        self._context = context
        self._prepared_players = tuple(prepared)
        result = MatchOperationResult(True, context=context, next_state_version=1, audit_ref=canonical_hash({"unit_id": "STATE-001", "event": payload_hash, "result": context.fingerprint}))
        self._events[request.event_id] = (payload_hash, result)
        return result

    @property
    def _version(self) -> int:
        return self._context.state_version if self._context else 0

    @staticmethod
    def _validate(req: MatchCreateRequest) -> str | None:
        if not all(isinstance(x, str) and x for x in (req.event_id, req.match_id, req.ruleset_hash, req.config_hash)):
            return "SCHEMA_INVALID"
        if not req.seed_trace_ref:
            return "SEED_MISSING"
        if req.rng_version not in (1, 2):
            return "VERSION_CONFLICT"
        if req.frozen_config is not None:
            if getattr(req.frozen_config, "config_hash", None) != req.config_hash:
                return "CONFIG_MUTATION"
            if getattr(req.frozen_config, "parameter_version", None) != req.parameter_version:
                return "VERSION_CONFLICT"
            if getattr(req.frozen_config, "contract_version", None) != req.contract_version:
                return "VERSION_CONFLICT"
            if getattr(req.frozen_config, "canonical_version", None) != req.canonical_version:
                return "VERSION_CONFLICT"
        if not 1 <= req.total_rounds <= 10_000:
            return "INVALID_MATCH_REQUEST"
        if len(req.bindings) not in (2, 3, 4):
            return "INVALID_MATCH_REQUEST"
        seats = [b.seat for b in req.bindings]
        if len(set(seats)) != len(seats):
            return "DUPLICATE_SEAT"
        profiles = [b.profile_id for b in req.bindings]
        if len(set(profiles)) != len(profiles):
            return "INVALID_MATCH_REQUEST"
        if set(seats) != set(range(len(seats))) or set(req.starting_scores) != set(seats):
            return "INVALID_MATCH_REQUEST"
        if any(not b.player_id or not b.profile_id for b in req.bindings):
            return "INVALID_MATCH_REQUEST"
        if req.dealer_policy not in {"dice", "rotate", "fixed"}:
            return "INVALID_MATCH_REQUEST"
        return None

    def complete_round(self, *, event_id: str, expected_state_version: int, scores: Mapping[int, int]) -> MatchOperationResult:
        with self._lock:
            return self._complete_round_locked(event_id=event_id, expected_state_version=expected_state_version, scores=scores)

    def _complete_round_locked(self, *, event_id: str, expected_state_version: int, scores: Mapping[int, int]) -> MatchOperationResult:
        if self._context is None:
            return MatchOperationResult(False, error_code="INVALID_MATCH_REQUEST", next_state_version=0)
        payload_hash = canonical_hash({"event_id": event_id, "version": expected_state_version, "scores": {str(k): v for k, v in sorted(scores.items())}})
        old = self._events.get(event_id)
        if old:
            return old[1] if old[0] == payload_hash else MatchOperationResult(False, error_code="INVALID_MATCH_REQUEST", next_state_version=self._version)
        if self._rounds_completed >= self._context.total_rounds:
            return MatchOperationResult(False, error_code="TERMINAL_STATE", next_state_version=self._version)
        if expected_state_version != self._version:
            return MatchOperationResult(False, error_code="VERSION_CONFLICT", next_state_version=self._version)
        if set(scores) != {b.seat for b in self._context.bindings}:
            return MatchOperationResult(False, error_code="INVARIANT_FAILED", next_state_version=self._version)
        self._scores = {int(k): int(v) for k, v in scores.items()}
        self._rounds_completed += 1
        version = self._version + 1
        ctx = self._context
        updated = MatchContext(
            match_id=ctx.match_id, state_version=version, ruleset_hash=ctx.ruleset_hash,
            config_hash=ctx.config_hash, seed_trace_ref=ctx.seed_trace_ref, bindings=ctx.bindings,
            total_rounds=ctx.total_rounds, current_round=self._rounds_completed,
            starting_scores=MappingProxyType(self._scores.copy()), dealer_policy=ctx.dealer_policy,
            rules_version=ctx.rules_version, parameter_version=ctx.parameter_version,
            contract_version=ctx.contract_version, canonical_version=ctx.canonical_version,
            rng_version=ctx.rng_version, fingerprint=canonical_hash({"previous": ctx.fingerprint, "round": self._rounds_completed, "scores": self._scores}),
            config_canonical_bytes=ctx.config_canonical_bytes,
        )
        self._context = updated
        final = None
        if self._rounds_completed == ctx.total_rounds:
            ranking = tuple(sorted(self._scores, key=lambda seat: (-self._scores[seat], seat)))
            final = MatchResult(ctx.match_id, "COMPLETED", version, self._rounds_completed, MappingProxyType(self._scores.copy()), ranking, updated.fingerprint)
        result = MatchOperationResult(True, context=updated, match_result=final, next_state_version=version, audit_ref=canonical_hash({"unit_id": "STATE-001", "event": payload_hash, "version": version}))
        self._events[event_id] = (payload_hash, result)
        return result

    @property
    def prepared_players(self) -> tuple[Any, ...]:
        return self._prepared_players
