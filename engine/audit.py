"""Versioned private decision audit with a canonical SHA-256 hash chain."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from engine.action import Action

AUDIT_FORMAT_VERSION = 1
HASH_HEX_LENGTH = 64


class AuditError(ValueError):
    """An audit record is malformed, inconsistent, or tampered with."""


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise AuditError(f"value is not canonical JSON: {exc}") from exc


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _record_hash(row: Mapping[str, Any]) -> str:
    return canonical_hash({key: value for key, value in row.items() if key != "record_hash"})


def _is_hash(value: Any) -> bool:
    return isinstance(value, str) and len(value) == HASH_HEX_LENGTH and all(char in "0123456789abcdef" for char in value)


def _action_is_legal(selected: Mapping[str, Any], legal: Iterable[Mapping[str, Any]]) -> bool:
    selected_bytes = canonical_json_bytes(selected)
    return any(canonical_json_bytes(action) == selected_bytes for action in legal)


def _validate_player_view(view: Mapping[str, Any], *, seat: int, phase: str) -> None:
    if view.get("self_seat") != seat or view.get("phase") != phase:
        raise AuditError("player_view seat/phase does not match decision")
    raw = view.get("view")
    if not isinstance(raw, Mapping) or raw.get("view_version") != 2:
        raise AuditError("audit requires PlayerView version 2")
    if raw.get("wall") not in (None, [], ()):
        raise AuditError("player_view must not contain wall order")
    for player in raw.get("players") or []:
        if not isinstance(player, Mapping):
            raise AuditError("player_view players must be objects")
        if player.get("seat") != seat and player.get("hand") not in (None, [], ()):
            raise AuditError("player_view leaks an opponent concealed hand")
        if player.get("seat") != seat and player.get("physical_hand") not in (None, [], ()):
            raise AuditError("player_view leaks opponent physical tiles")


@dataclass(frozen=True, slots=True)
class AuditVerification:
    game_id: str
    decision_count: int
    final_state_hash: str
    final_record_hash: str
    complete: bool


class DecisionAuditWriter:
    def __init__(
        self,
        path: Path | str,
        *,
        game_id: str,
        engine_config: Mapping[str, Any],
        initial_state: Mapping[str, Any],
        implementation_version: str = "CDMJ-AI-IMPL 2.0.0",
        state_schema_version: int = 5,
        player_view_version: int = 2,
    ) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fp = self.path.open("w", encoding="utf-8")
        self.game_id = game_id
        self.engine_config_hash = canonical_hash(engine_config)
        self._previous_hash: str | None = None
        self._decision_index = 0
        self._finished = False
        self._append(
            {
                "audit_format_version": AUDIT_FORMAT_VERSION,
                "kind": "header",
                "game_id": game_id,
                "implementation_version": implementation_version,
                "state_schema_version": state_schema_version,
                "player_view_version": player_view_version,
                "engine_config_hash": self.engine_config_hash,
                "initial_state_hash": canonical_hash(initial_state),
                "previous_record_hash": None,
            }
        )

    @property
    def decision_count(self) -> int:
        return self._decision_index

    def record_decision(
        self,
        *,
        seat: int,
        phase: str,
        state_before: Mapping[str, Any],
        state_after: Mapping[str, Any],
        player_view: Mapping[str, Any],
        legal_actions: Iterable[Mapping[str, Any]],
        selected_action: Mapping[str, Any],
        reason: str,
        decision_trace: Mapping[str, Any] | None,
        applied: bool = True,
    ) -> Mapping[str, Any]:
        if self._finished:
            raise AuditError("cannot append after audit footer")
        _validate_player_view(player_view, seat=seat, phase=phase)
        legal = [dict(action) for action in legal_actions]
        selected = dict(selected_action)
        if not _action_is_legal(selected, legal):
            raise AuditError("selected action is not in legal_actions")
        trace = dict(decision_trace) if decision_trace is not None else None
        policy = trace.get("policy") if trace else None
        if policy == "humanlike_v2_cognitive":
            if trace.get("trace_version") != 2:
                raise AuditError("humanlike cognitive audit requires trace version 2")
            if canonical_json_bytes(trace.get("selected_action")) != canonical_json_bytes(selected):
                raise AuditError("trace selected_action does not match outer action")
        rng = {
            "used": bool(trace and trace.get("rng_used", False)),
            "index_before": int(trace.get("rng_index_before", 0)) if trace else 0,
            "index_after": int(trace.get("rng_index_after", 0)) if trace else 0,
        }
        if rng["index_after"] < rng["index_before"]:
            raise AuditError("RNG index must not move backwards")
        if not rng["used"] and rng["index_before"] != rng["index_after"]:
            raise AuditError("unused RNG must not advance")
        cognitive = None
        if trace:
            cognitive = {
                "memory": trace.get("memory"),
                "attention": trace.get("attention"),
                "plan": trace.get("plan"),
                "personality": trace.get("personality"),
                "checked_actions": trace.get("checked_actions"),
                "stop_reason": trace.get("stop_reason"),
                "think_time_ms": trace.get("think_time_ms"),
                "plan_state": trace.get("plan_state"),
                "hu_rule": trace.get("hu_rule"),
                "parameter_snapshot": trace.get("parameter_snapshot"),
            }
        row = {
            "audit_format_version": AUDIT_FORMAT_VERSION,
            "kind": "decision",
            "game_id": self.game_id,
            "decision_index": self._decision_index,
            "seat": seat,
            "phase": phase,
            "state_hash_before": canonical_hash(state_before),
            "state_hash_after": canonical_hash(state_after),
            "player_view": dict(player_view),
            "player_view_hash": canonical_hash(player_view),
            "legal_actions": legal,
            "policy": policy,
            "policy_config_hash": trace.get("config_hash") if trace else None,
            "decision_trace": trace,
            "rng": rng,
            "cognitive_snapshot": cognitive,
            "selected_action": selected,
            "reason": str(reason),
            "applied": bool(applied),
            "previous_record_hash": self._previous_hash,
        }
        written = self._append(row)
        self._decision_index += 1
        return written

    def finish(self, *, final_state: Mapping[str, Any], finished_reason: str | None) -> Mapping[str, Any]:
        if self._finished:
            raise AuditError("audit footer already written")
        row = self._append(
            {
                "audit_format_version": AUDIT_FORMAT_VERSION,
                "kind": "footer",
                "game_id": self.game_id,
                "decision_count": self._decision_index,
                "final_state_hash": canonical_hash(final_state),
                "final_chain_hash": self._previous_hash,
                "finished_reason": finished_reason,
                "previous_record_hash": self._previous_hash,
            }
        )
        self._finished = True
        self.close()
        return row

    def close(self) -> None:
        if not self._fp.closed:
            self._fp.close()

    def _append(self, row: dict[str, Any]) -> Mapping[str, Any]:
        row["record_hash"] = _record_hash(row)
        self._fp.write(canonical_json_bytes(row).decode("utf-8") + "\n")
        self._fp.flush()
        self._previous_hash = row["record_hash"]
        return dict(row)


def load_audit(path: Path | str) -> tuple[Mapping[str, Any], ...]:
    source = Path(path)
    if not source.exists():
        raise AuditError(f"audit path not found: {source}")
    records = []
    for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise AuditError(f"invalid JSON at line {line_number}: {exc}") from exc
        if not isinstance(row, Mapping):
            raise AuditError(f"audit line {line_number} must be an object")
        records.append(dict(row))
    if not records:
        raise AuditError("audit is empty")
    return tuple(records)


def verify_audit(path: Path | str, *, strict: bool = True) -> AuditVerification:
    records = load_audit(path)
    header = records[0]
    if header.get("kind") != "header" or header.get("audit_format_version") != AUDIT_FORMAT_VERSION:
        raise AuditError("audit must start with a supported header")
    game_id = header.get("game_id")
    previous = None
    decision_index = 0
    rng_by_seat: dict[int, int] = {}
    for index, row in enumerate(records):
        if row.get("audit_format_version") != AUDIT_FORMAT_VERSION or row.get("game_id") != game_id:
            raise AuditError(f"version/game_id mismatch at record {index}")
        if row.get("previous_record_hash") != previous:
            raise AuditError(f"hash chain predecessor mismatch at record {index}")
        if not _is_hash(row.get("record_hash")) or _record_hash(row) != row.get("record_hash"):
            raise AuditError(f"record hash mismatch at record {index}")
        kind = row.get("kind")
        if index == 0 and kind != "header":
            raise AuditError("first audit record must be header")
        if index > 0 and kind == "header":
            raise AuditError(f"unexpected header at record {index}")
        if kind == "footer" and index != len(records) - 1:
            raise AuditError(f"footer must be the final record, got {index}")
        if kind not in {"header", "decision", "footer"}:
            raise AuditError(f"unknown audit record kind at {index}: {kind!r}")
        if row.get("kind") == "decision":
            if row.get("decision_index") != decision_index:
                raise AuditError(f"non-contiguous decision index at record {index}")
            for key in ("state_hash_before", "state_hash_after", "player_view_hash"):
                if not _is_hash(row.get(key)):
                    raise AuditError(f"invalid {key} at record {index}")
            view = row.get("player_view")
            if not isinstance(view, Mapping) or canonical_hash(view) != row.get("player_view_hash"):
                raise AuditError(f"player view hash mismatch at record {index}")
            _validate_player_view(view, seat=int(row.get("seat", -1)), phase=str(row.get("phase")))
            legal = row.get("legal_actions")
            selected = row.get("selected_action")
            if not isinstance(legal, list) or not isinstance(selected, Mapping) or not _action_is_legal(selected, legal):
                raise AuditError(f"illegal selected action at record {index}")
            trace = row.get("decision_trace")
            if row.get("policy") == "humanlike_v2_cognitive":
                if not isinstance(trace, Mapping) or trace.get("trace_version") != 2:
                    raise AuditError(f"invalid humanlike trace at record {index}")
                if canonical_json_bytes(trace.get("selected_action")) != canonical_json_bytes(selected):
                    raise AuditError(f"trace action mismatch at record {index}")
            rng = row.get("rng")
            if not isinstance(rng, Mapping) or int(rng.get("index_after", -1)) < int(rng.get("index_before", 0)):
                raise AuditError(f"invalid RNG position at record {index}")
            if not rng.get("used") and rng.get("index_before") != rng.get("index_after"):
                raise AuditError(f"unused RNG advanced at record {index}")
            seat = int(row["seat"])
            if int(rng.get("index_before", 0)) < rng_by_seat.get(seat, 0):
                raise AuditError(f"RNG index regressed for seat {seat} at record {index}")
            rng_by_seat[seat] = int(rng.get("index_after", 0))
            policy_hash = row.get("policy_config_hash")
            if policy_hash is not None and not _is_hash(policy_hash):
                raise AuditError(f"invalid policy_config_hash at record {index}")
            decision_index += 1
        previous = row["record_hash"]
    footer = records[-1]
    complete = footer.get("kind") == "footer"
    if strict and not complete:
        raise AuditError("strict verification requires a footer")
    if complete:
        if footer.get("decision_count") != decision_index:
            raise AuditError("footer decision_count mismatch")
        if footer.get("final_chain_hash") != footer.get("previous_record_hash"):
            raise AuditError("footer final_chain_hash mismatch")
        if not _is_hash(footer.get("final_state_hash")):
            raise AuditError("footer final_state_hash is invalid")
    final_state_hash = str(footer.get("final_state_hash", "")) if complete else ""
    return AuditVerification(str(game_id), decision_index, final_state_hash, str(records[-1]["record_hash"]), complete)


__all__ = [
    "AUDIT_FORMAT_VERSION",
    "AuditError",
    "AuditVerification",
    "DecisionAuditWriter",
    "canonical_hash",
    "canonical_json_bytes",
    "load_audit",
    "verify_audit",
]
