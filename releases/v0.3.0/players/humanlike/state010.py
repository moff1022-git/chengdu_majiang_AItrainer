"""STATE-010 parameter registry and atomic lifecycle primitives."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

GP_IDS = tuple(f"GP-{i:03d}" for i in range(1, 28))
RP_IDS = tuple(f"RP-{i:03d}" for i in range(1, 34))
PARAMETER_IDS = GP_IDS + RP_IDS


class ParameterErrorCode(str, Enum):
    DUPLICATE_PARAMETER = "DUPLICATE_PARAMETER"
    SCHEMA_INVALID = "SCHEMA_INVALID"
    MISSING_REQUIRED = "MISSING_REQUIRED"
    PARAM_NULL = "PARAM_NULL"
    OUT_OF_RANGE = "OUT_OF_RANGE"
    UNKNOWN_PARAMETER = "UNKNOWN_PARAMETER"
    LIFECYCLE_VIOLATION = "LIFECYCLE_VIOLATION"
    VERSION_CONFLICT = "VERSION_CONFLICT"


class ParameterStateError(ValueError):
    def __init__(self, code: ParameterErrorCode, message: str):
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class ParameterDefinition:
    parameter_id: str
    scope: str
    required: bool
    nullable: bool
    owner_scoped: bool
    name: str
    type_and_range: str
    lifecycle: str
    visibility: str
    source_reference: str


_registry_path = Path(__file__).with_name("parameter_registry_v2.json")
_registry_rows = json.loads(_registry_path.read_text(encoding="utf-8"))
PARAMETER_REGISTRY = MappingProxyType({row["parameter_id"]: ParameterDefinition(
    row["parameter_id"], row["scope"], True, False, row["parameter_id"].startswith("RP-"),
    row["parameter_name"], row["data_type_and_range"], row["lifecycle_or_update"],
    row["visibility"], f'{row["authoritative_source"]} {row["source_section"]}',
) for row in _registry_rows})
if tuple(PARAMETER_REGISTRY) != PARAMETER_IDS or len(PARAMETER_REGISTRY) != 60:
    raise RuntimeError("STATE-010 registry must contain 60 unique IDs")


@dataclass(frozen=True, slots=True)
class State010Result:
    accepted: bool
    version: int
    error_code: str | None = None
    result: Mapping[str, Any] | None = None


def build_registry(rows: list[Mapping[str, Any]]) -> Mapping[str, ParameterDefinition]:
    ids = [str(row.get("parameter_id")) for row in rows]
    if len(ids) != len(set(ids)):
        raise ParameterStateError(ParameterErrorCode.DUPLICATE_PARAMETER, "duplicate parameter ID")
    if set(ids) != set(PARAMETER_IDS):
        raise ParameterStateError(ParameterErrorCode.SCHEMA_INVALID, "registry must contain exact 60-ID closure")
    return PARAMETER_REGISTRY


def resolve_parameters(source: Mapping[str, Any], *, phase: str, owner_seat: int | None = None, parameter_version: str = "CDMJ-AI-PARAMS 2.0.0", ruleset_hash: str = "", config_hash: str = "") -> State010Result:
    unknown = set(source) - set(PARAMETER_IDS)
    if unknown:
        return State010Result(False, 0, ParameterErrorCode.UNKNOWN_PARAMETER.value, None)
    if phase not in {"match_create", "round_start", "event", "decision", "round_end"}:
        return State010Result(False, 0, ParameterErrorCode.LIFECYCLE_VIOLATION.value, None)
    if owner_seat is not None and owner_seat not in range(4):
        return State010Result(False, 0, ParameterErrorCode.OUT_OF_RANGE.value, None)
    payload = MappingProxyType({"phase": phase, "owner_seat": owner_seat, "parameter_version": parameter_version, "ruleset_hash": ruleset_hash, "config_hash": config_hash, "values": deepcopy(dict(source))})
    return State010Result(True, 1, None, payload)


class FrozenGlobalParameters:
    """One-time GP commit; failed commits leave the previous snapshot untouched."""

    def __init__(self) -> None:
        self._values: Mapping[str, Any] | None = None
        self._version = 0

    @property
    def snapshot(self) -> Mapping[str, Any] | None:
        return self._values

    def commit(self, values: Mapping[str, Any], expected_version: int = 0) -> State010Result:
        if self._values is not None:
            return State010Result(False, self._version, ParameterErrorCode.LIFECYCLE_VIOLATION.value)
        if expected_version != self._version:
            return State010Result(False, self._version, ParameterErrorCode.VERSION_CONFLICT.value)
        unknown = set(values) - set(GP_IDS)
        missing = set(GP_IDS) - set(values)
        if unknown:
            return State010Result(False, self._version, ParameterErrorCode.UNKNOWN_PARAMETER.value)
        if missing:
            return State010Result(False, self._version, ParameterErrorCode.MISSING_REQUIRED.value)
        if any(values[pid] is None for pid in GP_IDS):
            return State010Result(False, self._version, ParameterErrorCode.PARAM_NULL.value)
        candidate = MappingProxyType(deepcopy(dict(values)))
        self._values = candidate
        self._version = 1
        return State010Result(True, self._version)


@dataclass(frozen=True, slots=True)
class SeatRuntimeArchive:
    round_id: str
    owner_seat: int
    state_version: int
    values: Mapping[str, Any]


class SeatRuntimeStore:
    """Four isolated RP stores with CAS updates and immutable round archives."""

    def __init__(self, round_id: str):
        if not round_id:
            raise ValueError("round_id must be non-empty")
        self.round_id = round_id
        self._values = [{pid: None for pid in RP_IDS} for _ in range(4)]
        self._versions = [0, 0, 0, 0]
        self._finalized = [False] * 4

    def snapshot(self, seat: int) -> Mapping[str, Any]:
        self._check_seat(seat)
        return MappingProxyType(deepcopy(self._values[seat]))

    def version(self, seat: int) -> int:
        self._check_seat(seat)
        return self._versions[seat]

    def update(self, *, actor_seat: int, owner_seat: int, changes: Mapping[str, Any], expected_version: int) -> State010Result:
        self._check_seat(owner_seat)
        if actor_seat != owner_seat or self._finalized[owner_seat]:
            return State010Result(False, self._versions[owner_seat], ParameterErrorCode.LIFECYCLE_VIOLATION.value)
        if expected_version != self._versions[owner_seat]:
            return State010Result(False, self._versions[owner_seat], ParameterErrorCode.VERSION_CONFLICT.value)
        if set(changes) - set(RP_IDS):
            return State010Result(False, self._versions[owner_seat], ParameterErrorCode.UNKNOWN_PARAMETER.value)
        candidate = deepcopy(self._values[owner_seat])
        candidate.update(deepcopy(dict(changes)))
        self._values[owner_seat] = candidate
        self._versions[owner_seat] += 1
        return State010Result(True, self._versions[owner_seat])

    def finalize(self, seat: int) -> SeatRuntimeArchive:
        self._check_seat(seat)
        if self._finalized[seat]:
            raise ParameterStateError(ParameterErrorCode.LIFECYCLE_VIOLATION, "seat already finalized")
        self._finalized[seat] = True
        return SeatRuntimeArchive(self.round_id, seat, self._versions[seat], self.snapshot(seat))

    @staticmethod
    def _check_seat(seat: int) -> None:
        if seat not in range(4):
            raise ValueError("seat must be 0..3")
