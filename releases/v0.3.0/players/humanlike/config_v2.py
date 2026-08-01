"""ALGO-009 versioned migration and CDMJ canonical-jcs-nfc-v2 profile."""

from __future__ import annotations

import hashlib
import json
import math
import unicodedata
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping

PARAMS_V1 = "CDMJ-AI-PARAMS 1.1.0"
PARAMS_V2 = "CDMJ-AI-PARAMS 2.0.0"
CONTRACTS_V2 = "CDMJ-CONTRACTS 2.0.0"
CANONICAL_V2 = "CDMJ canonical-jcs-nfc-v2 profile"
INT64_MIN, INT64_MAX = -(2**63), 2**63 - 1


class ConfigV2Error(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _normalize(value: Any) -> Any:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        if not INT64_MIN <= value <= INT64_MAX:
            raise ConfigV2Error("PARAM_RANGE", "integer outside int64")
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ConfigV2Error("NON_FINITE", "non-finite number")
        return 0 if value == 0 else value
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ConfigV2Error("SCHEMA_INVALID", "object keys must be strings")
            normalized = unicodedata.normalize("NFC", key)
            if normalized in result:
                raise ConfigV2Error("SCHEMA_INVALID", "NFC key collision")
            result[normalized] = _normalize(item)
        return result
    raise ConfigV2Error("PARAM_TYPE", f"unsupported type: {type(value).__name__}")


def canonical_v2_bytes(value: Any) -> bytes:
    normalized = _normalize(value)
    return json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


@dataclass(frozen=True, slots=True)
class FrozenConfigV2:
    value: Mapping[str, Any]
    canonical_bytes: bytes
    config_hash: str
    source_hash: str | None
    parameter_version: str = PARAMS_V2
    contract_version: str = CONTRACTS_V2
    canonical_version: str = CANONICAL_V2
    formula_version: str = "ALGO-009/v2"
    baseline_version: str = "legacy-json-v1"
    schema_before_after: tuple[str, str] = (PARAMS_V1, PARAMS_V2)
    migration_steps: tuple[str, ...] = ("MIG-CONFIG-110-200",)
    defaults: tuple[str, ...] = ()


def migrate_1_1_to_2_0(raw: Mapping[str, Any], *, source_hash: str | None = None) -> dict[str, Any]:
    if raw.get("parameter_version") == PARAMS_V2 and raw.get("contract_version") == CONTRACTS_V2:
        return deepcopy(dict(raw))
    if raw.get("parameter_version") != PARAMS_V1:
        raise ConfigV2Error("MIGRATION_FAILED", "only the explicit 1.1 to 2.0 edge is supported")
    candidate = deepcopy(dict(raw))
    candidate["parameter_version"] = PARAMS_V2
    candidate["contract_version"] = CONTRACTS_V2
    candidate["canonical_version"] = CANONICAL_V2
    gp001 = candidate.get("global_parameters", {}).get("GP-001")
    if isinstance(gp001, Mapping):
        gp001["parameter_version"] = PARAMS_V2
    if source_hash is not None:
        candidate["source_hash"] = source_hash
    return candidate


def migrate_1_0_to_1_1(raw: Mapping[str, Any]) -> dict[str, Any]:
    if raw.get("parameter_version") != "CDMJ-AI-PARAMS 1.0.0" or raw.get("implementation_version") != "CDMJ-AI-IMPL 2.0.0":
        raise ConfigV2Error("MIGRATION_FAILED", "only the explicit 1.0/2.0 to 1.1/2.1 edge is supported")
    candidate = deepcopy(dict(raw))
    gp = candidate.get("global_parameters")
    players = candidate.get("players")
    if not isinstance(gp, dict) or not isinstance(players, list) or len(players) != 4:
        raise ConfigV2Error("MIGRATION_FAILED", "legacy cognitive parameters or players missing")
    try:
        cognitive = {pid: gp.pop(pid) for pid in ("GP-024", "GP-025", "GP-026", "GP-027")}
    except KeyError as exc:
        raise ConfigV2Error("MIGRATION_FAILED", "legacy cognitive parameter missing") from exc
    for player in players:
        player["cognitive_parameters"] = deepcopy(cognitive)
    candidate["parameter_version"] = PARAMS_V1
    candidate["implementation_version"] = "CDMJ-AI-IMPL 2.1.0"
    return candidate


def freeze_v2(raw: Mapping[str, Any], *, source_hash: str | None = None) -> FrozenConfigV2:
    candidate = deepcopy(dict(raw))
    allowed_meta = {"rule_version", "parameter_version", "implementation_version", "contract_version", "canonical_version", "ruleset", "seed", "global_parameters", "players", "source_hash"}
    unknown = set(candidate) - allowed_meta
    if unknown:
        raise ConfigV2Error("PARAM_UNKNOWN", f"unknown fields: {sorted(unknown)}")
    gp = candidate.get("global_parameters")
    if not isinstance(gp, Mapping):
        raise ConfigV2Error("SCHEMA_INVALID", "global_parameters required")
    if candidate.get("parameter_version") != PARAMS_V2 or candidate.get("contract_version") != CONTRACTS_V2:
        raise ConfigV2Error("SCHEMA_VERSION_UNSUPPORTED", "v2 versions required")
    for pid in ("GP-002", "GP-004"):
        ext = gp.get(pid, {}).get("extensions") if isinstance(gp.get(pid), Mapping) else None
        if ext != []:
            raise ConfigV2Error("PARAM_UNKNOWN", f"{pid}.extensions must be empty")
    encoded = canonical_v2_bytes(candidate)
    return FrozenConfigV2(_normalize(candidate), encoded, hashlib.sha256(encoded).hexdigest(), source_hash)


def load_v2_bytes(raw: bytes) -> FrozenConfigV2:
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ConfigV2Error("SCHEMA_INVALID", "invalid v2 JSON") from exc
    if not isinstance(value, Mapping):
        raise ConfigV2Error("SCHEMA_INVALID", "v2 root must be object")
    frozen = freeze_v2(value, source_hash=value.get("source_hash"))
    if canonical_v2_bytes(value) != raw.strip():
        raise ConfigV2Error("SCHEMA_INVALID", "v2 file is not canonical")
    return frozen


class ConfigActivator:
    def __init__(self) -> None:
        self.active: FrozenConfigV2 | None = None

    def activate(self, raw: Mapping[str, Any], *, startup: bool = False) -> FrozenConfigV2:
        try:
            candidate = freeze_v2(raw)
        except ConfigV2Error:
            if startup or self.active is None:
                raise
            raise
        self.active = candidate
        return candidate


def validate_and_freeze(raw: Mapping[str, Any], *, source_hash: str | None = None) -> tuple[FrozenConfigV2, tuple[str, ...]]:
    """Observable fixed pipeline used by settings and audit oracles."""
    stages = ("parse", "version", "migration", "defaults", "type_range", "cross_constraint", "unknown", "canonical_hash")
    candidate = migrate_1_1_to_2_0(raw, source_hash=source_hash) if raw.get("parameter_version") == PARAMS_V1 else deepcopy(dict(raw))
    frozen = freeze_v2(candidate, source_hash=source_hash)
    return frozen, stages
