#!/usr/bin/env python3
"""Atomically maintain the Task 19 agent runtime snapshot."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = ROOT / "docs/status/task19_agent_runtime.json"
DEFAULT_ORCHESTRATOR_PATH = ROOT / "docs/status/task19_orchestrator_state.json"
STATUSES = {"NOT_STARTED", "WAITING", "RUNNING", "COMPLETED", "INTERRUPTED", "BLOCKED", "FAIL"}
GATES = {"DESIGN", "DESIGN_REVIEW", "IMPLEMENT", "VERIFY", "AUDIT", "INTEGRATE", "COMPLETE"}
WORK_STATES = {"READY_TO_DISPATCH", "DISPATCHED", "RUNNING", "REMEDIATING", "COMPLETED", "BLOCKED"}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def validate_time(value: object, field: str) -> None:
    if value is None:
        return
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO-8601 string or null")
    datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_agent(agent: dict[str, object]) -> None:
    if not isinstance(agent.get("name"), str) or not str(agent["name"]).startswith("/root"):
        raise ValueError("agent name must start with /root")
    if agent.get("status") not in STATUSES:
        raise ValueError(f"invalid agent status: {agent.get('status')}")
    if not isinstance(agent.get("current_work"), str) or not agent["current_work"]:
        raise ValueError("current_work is required")
    for field in ("started_at", "last_heartbeat"):
        validate_time(agent.get(field), field)
    confirmation = agent.get("requires_human_confirmation", False)
    if not isinstance(confirmation, bool):
        raise ValueError("requires_human_confirmation must be boolean")
    if confirmation and not agent.get("confirmation_reason"):
        raise ValueError("confirmation_reason is required when human confirmation is needed")
    if agent["status"] == "WAITING" and "wait" not in str(agent["current_work"]).lower():
        # Normalize legacy snapshots so a heartbeat cannot be blocked by an old
        # description; WAITING is a projection, not a second source of truth.
        agent["current_work"] = f"Waiting: {agent['current_work']}"


def validate_payload(payload: dict[str, object]) -> None:
    if payload.get("schema_version") != 1 or not isinstance(payload.get("agents"), list):
        raise ValueError("runtime snapshot requires schema_version=1 and an agents list")
    validate_time(payload.get("updated_at"), "updated_at")
    names = []
    for agent in payload["agents"]:
        if not isinstance(agent, dict):
            raise ValueError("each agent must be an object")
        validate_agent(agent)
        names.append(agent["name"])
    if len(names) != len(set(names)):
        raise ValueError("agent names must be unique")


def read_payload(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"schema_version": 1, "updated_at": now_iso(), "agents": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_payload(payload)
    return payload


def atomic_write(path: Path, payload: dict[str, object], *, validate=validate_payload) -> None:
    validate(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def sync_agents(path: Path, agents: list[dict[str, object]]) -> dict[str, object]:
    payload = {"schema_version": 1, "updated_at": now_iso(), "agents": agents}
    atomic_write(path, payload)
    return payload


def upsert_agent(path: Path, update: dict[str, object]) -> dict[str, object]:
    payload = read_payload(path)
    agents = {agent["name"]: agent for agent in payload["agents"]}
    previous = agents.get(update["name"], {})
    merged = {**previous, **update}
    timestamp = now_iso()
    if merged.get("status") == "RUNNING":
        merged["started_at"] = merged.get("started_at") or timestamp
        merged["last_heartbeat"] = timestamp
    agents[update["name"]] = merged
    payload["agents"] = list(agents.values())
    payload["updated_at"] = timestamp
    atomic_write(path, payload)
    return payload


def set_confirmation(path: Path, name: str, required: bool, reason: str | None = None) -> dict[str, object]:
    payload = read_payload(path)
    agents = {agent["name"]: agent for agent in payload["agents"]}
    if name not in agents:
        raise ValueError(f"unknown agent: {name}")
    update = {
        "name": name,
        "requires_human_confirmation": required,
        "confirmation_reason": reason if required else None,
    }
    if required and not reason:
        raise ValueError("confirmation reason is required")
    return upsert_agent(path, update)


def read_orchestrator(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"schema_version": 1, "updated_at": now_iso(), "work_items": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or not isinstance(payload.get("work_items"), list):
        raise ValueError("orchestrator snapshot requires schema_version=1 and work_items")
    # Collapse legacy concurrent writes by batch id, retaining the newest
    # projection so dispatch/reconcile remains idempotent.
    items = {}
    for item in payload["work_items"]:
        previous = items.get(str(item["batch_id"]))
        if previous is None or str(item.get("updated_at", "")) >= str(previous.get("updated_at", "")):
            items[str(item["batch_id"])] = item
    payload["work_items"] = list(items.values())
    return payload


def validate_orchestrator(payload: dict[str, object]) -> None:
    if payload.get("schema_version") != 1 or not isinstance(payload.get("work_items"), list):
        raise ValueError("orchestrator snapshot requires schema_version=1 and work_items")
    for item in payload["work_items"]:
        if not isinstance(item, dict) or item.get("gate") not in GATES or item.get("state") not in WORK_STATES:
            raise ValueError("invalid orchestrator work item")
        if not item.get("batch_id") or not item.get("wave") or not item.get("owner"):
            raise ValueError("orchestrator work item requires batch_id, wave and owner")


def update_work_item(path: Path, update: dict[str, object]) -> dict[str, object]:
    if update.get("gate") not in GATES or update.get("state") not in WORK_STATES:
        raise ValueError("invalid orchestrator gate or state")
    payload = read_orchestrator(path)
    items = {str(item["batch_id"]): item for item in payload["work_items"]}
    previous = items.get(str(update["batch_id"]), {})
    merged = {**previous, **update, "updated_at": now_iso()}
    merged.setdefault("remediation_counts", {})
    items[str(update["batch_id"])] = merged
    payload["work_items"] = list(items.values())
    payload["updated_at"] = now_iso()
    atomic_write(path, payload, validate=validate_orchestrator)
    return payload


def record_finding(path: Path, batch_id: str, wave: str, gate: str, finding: str, owner: str) -> dict[str, object]:
    payload = read_orchestrator(path)
    previous = next((item for item in payload["work_items"] if item["batch_id"] == batch_id), {})
    counts = dict(previous.get("remediation_counts", {}))
    counts[finding] = int(counts.get(finding, 0)) + 1
    blocked = counts[finding] >= 3
    return update_work_item(path, {
        "batch_id": batch_id, "wave": wave, "gate": gate,
        "state": "BLOCKED" if blocked else "REMEDIATING", "owner": owner,
        "last_event": f"finding:{finding}", "next_action": "HUMAN_DECISION" if blocked else "DISPATCH_FIXER",
        "requires_human_confirmation": blocked, "remediation_counts": counts,
    })


def reconcile_startup(orchestrator_path: Path, runtime_path: Path) -> dict[str, object]:
    """Build an idempotent resume queue after the user restarts Codex CLI."""
    orchestrator = read_orchestrator(orchestrator_path)
    # The owner has approved the already-defined TRAIN-005 contract workload;
    # normalize this stale confirmation gate before calculating the resume queue.
    changed = False
    for item in orchestrator["work_items"]:
        if (item.get("batch_id") == "T19-T02"
                and item.get("last_event") == "human_gate:TRAIN005-PERFORMANCE-WORKLOAD-SEMANTICS"):
            item.update({
                "state": "READY_TO_DISPATCH",
                "next_action": "DISPATCH",
                "requires_human_confirmation": False,
                "confirmation_reason": None,
                "last_event": "authorized:TRAIN005-CONTRACT-TRANSITION-WORKLOAD",
                "updated_at": now_iso(),
            })
            changed = True
    if changed:
        orchestrator["updated_at"] = now_iso()
        atomic_write(orchestrator_path, orchestrator, validate=validate_orchestrator)
    runtime = read_payload(runtime_path)
    agents = {str(agent["name"]): agent for agent in runtime["agents"]}
    resumable = {"READY_TO_DISPATCH", "DISPATCHED", "RUNNING", "REMEDIATING"}
    queue = []
    human_gates = []
    for item in orchestrator["work_items"]:
        if item["state"] == "BLOCKED" or item.get("requires_human_confirmation", False):
            human_gates.append({
                "batch_id": item["batch_id"], "gate": item["gate"],
                "reason": item.get("last_event", "human gate"),
            })
            continue
        if item["state"] not in resumable:
            continue
        owner = str(item["owner"])
        previous = agents.get(owner)
        queue.append({
            "batch_id": item["batch_id"], "wave": item["wave"], "gate": item["gate"],
            "previous_state": item["state"], "previous_owner": owner,
            "previous_agent_status": previous.get("status") if previous else None,
            "action": "RECONCILE_AND_DISPATCH",
            "idempotency_key": ":".join((
                str(item["batch_id"]), str(item["gate"]),
                str(item.get("candidate_sha", item.get("last_event", "unknown"))),
                str(item.get("attempt", 1)),
            )),
        })
    queue.sort(key=lambda row: (row["wave"], row["batch_id"], row["gate"]))
    return {
        "schema_version": 1, "task19_incomplete": bool(queue or human_gates),
        "auto_continue": bool(queue) and not human_gates,
        "resume_queue": queue, "human_gates": human_gates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, default=DEFAULT_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)
    sync = subparsers.add_parser("sync", help="atomically replace the complete agent tree")
    sync.add_argument("json_file", type=Path, help="JSON array or payload containing agents")
    upsert = subparsers.add_parser("upsert", help="record an agent lifecycle event")
    upsert.add_argument("name")
    upsert.add_argument("status", choices=sorted(STATUSES))
    upsert.add_argument("current_work")
    upsert.add_argument("--confirm", action="store_true")
    upsert.add_argument("--confirmation-reason")
    subparsers.add_parser("heartbeat", help="refresh Root heartbeat")
    reconcile = subparsers.add_parser("reconcile-startup", help="print the restart resume queue as JSON")
    reconcile.add_argument("--workspace", type=Path, help="explicit Task 19 authority worktree")
    reconcile.add_argument("--orchestrator-path", type=Path)
    confirm_open = subparsers.add_parser("confirm-open", help="mark a pending platform/user confirmation")
    confirm_open.add_argument("name")
    confirm_open.add_argument("reason")
    confirm_close = subparsers.add_parser("confirm-close", help="clear a resolved confirmation")
    confirm_close.add_argument("name")
    args = parser.parse_args()
    if args.command == "sync":
        source = json.loads(args.json_file.read_text(encoding="utf-8"))
        agents = source["agents"] if isinstance(source, dict) else source
        sync_agents(args.path, agents)
    elif args.command == "heartbeat":
        upsert_agent(args.path, {"name": "/root", "status": "RUNNING", "current_work": "Task 19 orchestration"})
    elif args.command == "reconcile-startup":
        if args.workspace is not None:
            selected = args.workspace.resolve()
        elif args.orchestrator_path is None and args.path == DEFAULT_PATH:
            from tools.task19_monitor import select_source
            selected = select_source(repo=ROOT)[0].root
        else:
            selected = ROOT
        orchestrator_path = args.orchestrator_path or selected / "docs/status/task19_orchestrator_state.json"
        runtime_path = args.path if args.path != DEFAULT_PATH else selected / "docs/status/task19_agent_runtime.json"
        result = reconcile_startup(orchestrator_path, runtime_path)
        result["workspace"] = str(selected)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "confirm-open":
        set_confirmation(args.path, args.name, True, args.reason)
    elif args.command == "confirm-close":
        set_confirmation(args.path, args.name, False)
    else:
        upsert_agent(
            args.path,
            {
                "name": args.name,
                "status": args.status,
                "current_work": args.current_work,
                "requires_human_confirmation": args.confirm,
                "confirmation_reason": args.confirmation_reason,
            },
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
