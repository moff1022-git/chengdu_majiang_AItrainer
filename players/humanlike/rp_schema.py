"""F0037 RP envelope validation and backward-compatible migration helpers."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

RP_IDS = tuple(f"RP-{i:03d}" for i in range(1, 34))
SCHEMA_VERSION = "F0037-RP-1.0"
VISIBILITIES = {"private", "public_exact", "public_partial", "audit_only"}
STATUSES = {"absent", "active", "final", "invalidated"}


class RPSchemaError(ValueError):
    pass


def canonical_payload_hash(payload: Any, extensions: Mapping[str, Any] | None = None) -> str:
    data = {"payload": payload, "extensions": dict(extensions or {})}
    raw = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def make_envelope(parameter_id: str, payload: Any, *, event_index: int, owner_seat: int | None = None,
                  lifecycle: str = "event", visibility: str = "private", status: str = "active",
                  source: str = "engine", extensions: Mapping[str, Any] | None = None) -> dict[str, Any]:
    if parameter_id not in RP_IDS:
        raise RPSchemaError(f"unknown RP: {parameter_id}")
    if not isinstance(event_index, int) or not 0 <= event_index <= 1_000_000:
        raise RPSchemaError("event_index must be in 0..1000000")
    if owner_seat is not None and owner_seat not in range(4):
        raise RPSchemaError("owner_seat must be 0..3 or null")
    if visibility not in VISIBILITIES or status not in STATUSES:
        raise RPSchemaError("invalid visibility or status")
    ext = deepcopy(dict(extensions or {}))
    return {"schema_version": SCHEMA_VERSION, "parameter_id": parameter_id, "lifecycle": lifecycle,
            "event_index": event_index, "owner_seat": owner_seat, "visibility": visibility,
            "status": status, "payload": deepcopy(payload), "extensions": ext,
            "source": source, "updated_at_event": event_index,
            "payload_hash": canonical_payload_hash(payload, ext)}


def validate_envelope(value: Mapping[str, Any], parameter_id: str | None = None) -> dict[str, Any]:
    required = {"schema_version", "parameter_id", "lifecycle", "event_index", "owner_seat", "visibility", "status", "payload", "extensions", "source", "updated_at_event", "payload_hash"}
    if set(value) != required or value["schema_version"] != SCHEMA_VERSION:
        raise RPSchemaError("invalid RP envelope fields or schema version")
    if parameter_id and value["parameter_id"] != parameter_id:
        raise RPSchemaError("RP parameter_id mismatch")
    expected = make_envelope(value["parameter_id"], value["payload"], event_index=value["event_index"], owner_seat=value["owner_seat"], lifecycle=value["lifecycle"], visibility=value["visibility"], status=value["status"], source=value["source"], extensions=value["extensions"])
    if value["updated_at_event"] != value["event_index"] or value["payload_hash"] != expected["payload_hash"]:
        raise RPSchemaError("RP payload hash or updated event mismatch")
    if value["visibility"] in {"public_exact", "public_partial"} and _contains_forbidden_hidden(value["payload"]):
        raise RPSchemaError("hidden fields cannot enter public RP payload")
    return deepcopy(dict(value))


def _contains_forbidden_hidden(value: Any) -> bool:
    if isinstance(value, Mapping):
        if any(str(key).lower() in {"hidden_hand", "server_hand", "private_hand", "concealed_tiles"} for key in value):
            return True
        return any(_contains_forbidden_hidden(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return any(_contains_forbidden_hidden(item) for item in value)
    return False


def migrate_legacy(parameter_id: str, payload: Any, *, event_index: int = 0, owner_seat: int | None = None) -> dict[str, Any]:
    """Wrap Task 19's legacy bare payload without changing its semantic data."""
    return make_envelope(parameter_id, payload, event_index=event_index, owner_seat=owner_seat, lifecycle="event", status="active", source="legacy")
