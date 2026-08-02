"""Persistence and dual-view helpers for RP envelopes."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Mapping
from players.humanlike.rp_schema import RP_IDS, migrate_legacy, validate_envelope

def envelope_view(values: Mapping[str, Any]) -> dict[str, Any]:
    return {key: dict(value) if isinstance(value, Mapping) and value.get("schema_version") else value for key, value in values.items()}

def payload_view(values: Mapping[str, Any], *, include_audit: bool = False) -> dict[str, Any]:
    out = {}
    for key, value in values.items():
        if isinstance(value, Mapping) and value.get("schema_version"):
            if value.get("visibility") == "audit_only" and not include_audit:
                continue
            out[key] = value["payload"]
        else:
            out[key] = value
    return out

def save_envelopes(path: str | Path, values: Mapping[str, Any]) -> None:
    Path(path).write_text(json.dumps(envelope_view(values), ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

def load_envelopes(path: str | Path) -> dict[str, Any]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    out = {}
    for key in RP_IDS:
        value = raw.get(key)
        if value is None:
            out[key] = None
        elif isinstance(value, Mapping) and value.get("schema_version"):
            out[key] = validate_envelope(value, key)
        else:
            out[key] = migrate_legacy(key, value)
    return out

def dual_view(values: Mapping[str, Any], *, include_audit: bool = False) -> dict[str, Any]:
    """Return UI/audit-friendly envelope and payload projections together."""
    return {"envelope": envelope_view(values), "payload": payload_view(values, include_audit=include_audit)}
