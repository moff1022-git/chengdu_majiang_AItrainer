#!/usr/bin/env python3
"""Read-only live dashboard for the Task 19 authoritative tracker."""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import time
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK19 = ROOT / "docs/spec-v3/task19"
TRACKER = TASK19 / "task19_progress_tracker.md"
WAVES = TASK19 / "task19_parallel_wave_plan.csv"
CHECKPOINT = TASK19 / "checkpoint/task19_checkpoint_final_authorization.json"
AGENTS = ROOT / "docs/status/task19_agent_runtime.json"
ORCHESTRATOR = ROOT / "docs/status/task19_orchestrator_state.json"
ACTIVE = {
    "READY_FOR_IMPLEMENTATION",
    "IMPLEMENTING",
    "IMPLEMENTED_PENDING_EVIDENCE",
    "IMPLEMENTED_PENDING_INDEPENDENT_AUDIT",
    "AUDIT_REMEDIATION",
    "BLOCKED",
}


@dataclass(frozen=True)
class WorkspaceSource:
    root: Path
    tracker: Path
    waves: Path
    checkpoint: Path
    agents: Path
    branch: str
    head: str
    audited: int
    progress: float
    tracker_updated_at: datetime
    tracker_mtime: float


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def tracker_rows(path: Path = TRACKER) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    marker = next(i for i, line in enumerate(lines) if line.startswith("| unit_id |"))
    header = [part.strip() for part in lines[marker].strip("|").split("|")]
    rows = []
    for line in lines[marker + 2 :]:
        if not line.startswith("|"):
            break
        values = [part.strip() for part in line.strip("|").split("|")]
        if len(values) == len(header):
            rows.append(dict(zip(header, values)))
    if len(rows) != 96:
        raise ValueError(f"expected 96 tracker rows, found {len(rows)}")
    return rows


def wave_rows(path: Path = WAVES) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 14:
        raise ValueError(f"expected 14 waves, found {len(rows)}")
    return rows


def projected_state(statuses: list[str]) -> str:
    if statuses and all(status == "AUDITED" for status in statuses):
        return "COMPLETED"
    if any(status in ACTIVE for status in statuses):
        return "IN_PROGRESS"
    return "NOT_STARTED"


def average_progress(rows: list[dict[str, str]]) -> float:
    if not rows:
        return 0.0
    return round(sum(float(row["progress"].removesuffix("%")) for row in rows) / len(rows), 2)


def default_started_at(source: WorkspaceSource) -> datetime:
    try:
        payload = json.loads(source.checkpoint.read_text(encoding="utf-8"))
        for key in ("authorized_at", "created_at", "timestamp"):
            if payload.get(key):
                return parse_time(str(payload[key]))
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        pass
    return datetime.fromtimestamp(source.tracker.stat().st_mtime, timezone.utc)


def git_worktrees(repo: Path = ROOT) -> list[tuple[Path, str, str]]:
    proc = subprocess.run(
        ["git", "worktree", "list", "--porcelain"], cwd=repo, text=True,
        capture_output=True, check=True,
    )
    result = []
    current: dict[str, str] = {}
    for line in [*proc.stdout.splitlines(), ""]:
        if not line:
            if current.get("worktree"):
                branch = current.get("branch", "detached").removeprefix("refs/heads/")
                result.append((Path(current["worktree"]).resolve(), branch, current.get("HEAD", "unknown")))
            current = {}
        elif " " in line:
            key, value = line.split(" ", 1)
            current[key] = value
        else:
            current[line] = "true"
    return result


def workspace_source(root: Path, branch: str = "explicit", head: str = "unknown") -> WorkspaceSource:
    task19 = root / "docs/spec-v3/task19"
    tracker = task19 / "task19_progress_tracker.md"
    units = tracker_rows(tracker)
    # A partially merged tracker can temporarily shift a row's trailing
    # columns; keep the worktree discoverable and fall back to file mtime.
    timestamps = []
    for row in units:
        try:
            timestamps.append(parse_time(row["last_updated"]))
        except (KeyError, ValueError):
            continue
    latest = max(timestamps) if timestamps else datetime.fromtimestamp(tracker.stat().st_mtime, timezone.utc)
    return WorkspaceSource(
        root=root, tracker=tracker, waves=task19 / "task19_parallel_wave_plan.csv",
        checkpoint=task19 / "checkpoint/task19_checkpoint_final_authorization.json",
        agents=root / "docs/status/task19_agent_runtime.json", branch=branch, head=head,
        audited=sum(row["task19_current_status"] == "AUDITED" for row in units),
        progress=average_progress(units), tracker_updated_at=latest, tracker_mtime=tracker.stat().st_mtime,
    )


def discover_sources(repo: Path = ROOT) -> list[WorkspaceSource]:
    sources = []
    for root, branch, head in git_worktrees(repo):
        try:
            source = workspace_source(root, branch, head)
            wave_rows(source.waves)
            sources.append(source)
        except (OSError, ValueError, StopIteration):
            continue
    if not sources:
        raise ValueError("no valid Task 19 workspace with 96 tracker rows was found")
    return sources


def select_source(workspace: Path | None = None, repo: Path = ROOT) -> tuple[WorkspaceSource, list[WorkspaceSource]]:
    if workspace is not None:
        selected = workspace_source(workspace.resolve())
        return selected, [selected]
    sources = discover_sources(repo)
    selected = max(
        sources,
        key=lambda item: (
            "task19/" in item.branch and "integration" in item.branch,
            item.tracker_updated_at, item.audited, item.progress,
            item.tracker_mtime,
        ),
    )
    return selected, sources


def select_agent_snapshot(selected: WorkspaceSource, sources: list[WorkspaceSource]) -> tuple[Path, bool]:
    if selected.agents.exists():
        return selected.agents, False
    candidates = [source.agents for source in sources if source.agents.exists()]
    if not candidates:
        return selected.agents, False
    def updated(path: Path) -> datetime:
        try:
            return parse_time(json.loads(path.read_text(encoding="utf-8")).get("updated_at", "1970-01-01T00:00:00Z"))
        except (OSError, ValueError, json.JSONDecodeError):
            return datetime.fromtimestamp(0, timezone.utc)
    return max(candidates, key=updated), True


def snapshot(started_at: datetime | None = None, workspace: Path | None = None) -> dict[str, object]:
    source, sources = select_source(workspace)
    units = tracker_rows(source.tracker)
    waves = wave_rows(source.waves)
    now = datetime.now(timezone.utc)
    start = started_at or default_started_at(source)
    unit_by_batch: dict[str, list[dict[str, str]]] = {}
    for unit in units:
        unit_by_batch.setdefault(unit["batch_id"], []).append(unit)

    wave_views = []
    batch_counts: Counter[str] = Counter()
    for wave in waves:
        batch_views = []
        for batch_id in wave["batch_ids"].split("|"):
            members = unit_by_batch.get(batch_id, [])
            state = projected_state([row["task19_current_status"] for row in members])
            batch_counts[state] += 1
            batch_views.append({"id": batch_id, "state": state, "units": len(members)})
            batch_views[-1]["progress"] = average_progress(members)
        state = projected_state(
            [row["task19_current_status"] for batch in batch_views for row in unit_by_batch.get(batch["id"], [])]
        )
        wave_members = [row for batch in batch_views for row in unit_by_batch.get(batch["id"], [])]
        wave_views.append(
            {
                "id": wave["parallel_wave_id"],
                "state": state,
                "progress": average_progress(wave_members),
                "batches": batch_views,
            }
        )

    status_counts = Counter(row["task19_current_status"] for row in units)
    latest = max(parse_time(row["last_updated"]) for row in units)
    agent_path, runtime_fallback = select_agent_snapshot(source, sources)
    agent_payload = json.loads(agent_path.read_text(encoding="utf-8")) if agent_path.exists() else {"agents": []}
    agent_snapshot_updated = parse_time(agent_payload["updated_at"]) if agent_payload.get("updated_at") else None
    orchestrator_path = ROOT / "docs/status/task19_orchestrator_state.json"
    orchestrator_payload = json.loads(orchestrator_path.read_text(encoding="utf-8")) if orchestrator_path.exists() else {"work_items": []}
    runtime_lagging = (
        agent_snapshot_updated is None
        or (now - agent_snapshot_updated).total_seconds() > 60
    )
    agent_views = []
    for agent in agent_payload.get("agents", []):
        needs_confirmation = agent.get("requires_human_confirmation", False)
        if not isinstance(needs_confirmation, bool):
            raise ValueError("requires_human_confirmation must be boolean")
        if needs_confirmation and not agent.get("confirmation_reason"):
            raise ValueError("confirmation_reason is required when human confirmation is needed")
        heartbeat = parse_time(agent["last_heartbeat"]) if agent.get("last_heartbeat") else None
        agent_start = parse_time(agent["started_at"]) if agent.get("started_at") else None
        age = max(0, int((now - heartbeat).total_seconds())) if heartbeat else None
        status = str(agent["status"])
        heartbeat_stale = status == "RUNNING" and (age is None or age > 60)
        agent_views.append(
            {
                **agent,
                "effective_status": "STALE" if status == "RUNNING" and (heartbeat_stale or runtime_lagging) else status,
                "heartbeat_stale": heartbeat_stale,
                "heartbeat_age_seconds": age,
                "elapsed_seconds": max(0, int((now - agent_start).total_seconds())) if agent_start else None,
                "requires_human_confirmation": needs_confirmation,
            }
        )

    # Design work legitimately leaves tracker units waiting for approval. Project
    # the live wave as running when an active agent explicitly names that wave.
    active_wave_ids: set[str] = set()
    for agent in agent_views:
        if agent["effective_status"] not in {"RUNNING", "IN_PROGRESS"}:
            continue
        active_wave_ids.update(re.findall(r"\bW(?:0[1-9]|1[0-4])\b", str(agent["current_work"]), re.IGNORECASE))
    active_work_states = {"DISPATCHED", "RUNNING", "REMEDIATING"}
    active_wave_ids.update(
        str(item["wave"]) for item in orchestrator_payload.get("work_items", [])
        if item.get("state") in active_work_states
    )
    for wave in wave_views:
        if wave["id"].upper() in {item.upper() for item in active_wave_ids} and wave["state"] != "COMPLETED":
            wave["state"] = "IN_PROGRESS"
    return {
        "workspace": str(source.root),
        "branch": source.branch,
        "head": source.head,
        "tracker_path": str(source.tracker),
        "agent_runtime_path": str(agent_path),
        "runtime_fallback": runtime_fallback,
        "runtime_lagging": runtime_lagging,
        "workspace_candidates": [
            {"workspace": str(item.root), "branch": item.branch, "head": item.head,
             "audited": item.audited, "progress": item.progress,
             "selected": item.root == source.root}
            for item in sorted(sources, key=lambda item: str(item.root))
        ],
        "now": now.isoformat(),
        "started_at": start.isoformat(),
        "elapsed_seconds": max(0, int((now - start).total_seconds())),
        "tracker_updated_at": latest.isoformat(),
        "tracker_age_seconds": max(0, int((now - latest).total_seconds())),
        "unit_counts": dict(sorted(status_counts.items())),
        "overall_progress": average_progress(units),
        "batch_counts": dict(batch_counts),
        "wave_counts": dict(Counter(wave["state"] for wave in wave_views)),
        "waves": wave_views,
        "agents": agent_views,
        "agent_snapshot_updated_at": agent_snapshot_updated.isoformat() if agent_snapshot_updated else None,
        "agent_snapshot_age_seconds": (
            max(0, int((now - agent_snapshot_updated).total_seconds())) if agent_snapshot_updated else None
        ),
        "human_confirmation_count": sum(agent["requires_human_confirmation"] for agent in agent_views),
        "orchestrator_path": str(orchestrator_path),
        "orchestrator_items": orchestrator_payload.get("work_items", []),
    }


def duration(seconds: int) -> str:
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{days}d {hours:02d}:{minutes:02d}:{secs:02d}" if days else f"{hours:02d}:{minutes:02d}:{secs:02d}"


def colorize(text: str, color: str, enabled: bool) -> str:
    codes = {"red": "31", "green": "32", "yellow": "33", "blue": "34", "white": "37"}
    return f"\033[{codes[color]}m{text}\033[0m" if enabled else text


def status_color(status: str, needs_confirmation: bool = False) -> str:
    if needs_confirmation or status in {"INTERRUPTED", "STALE", "BLOCKED", "FAIL"}:
        return "red"
    if status in {"RUNNING", "IN_PROGRESS"}:
        return "blue"
    if status in {"COMPLETED", "AUDITED", "DONE"}:
        return "green"
    if status == "WAITING":
        return "yellow"
    return "white"


def render(data: dict[str, object], color: bool = False) -> str:
    symbols = {"COMPLETED": "[DONE]", "IN_PROGRESS": "[RUN ]", "NOT_STARTED": "[WAIT]"}
    wave_counts = data["wave_counts"]
    batch_counts = data["batch_counts"]
    lines = [
        "Task 19 Live Monitor (read-only)",
        f"Source: {data['workspace']}  branch={data['branch']}  HEAD={str(data['head'])[:12]}",
        f"Tracker: {data['tracker_path']}",
        f"Agent runtime: {data['agent_runtime_path']}  fallback={'YES' if data['runtime_fallback'] else 'NO'}",
        f"Elapsed: {duration(int(data['elapsed_seconds']))}  Tracker age: {duration(int(data['tracker_age_seconds']))}",
        "Waves: " + "  ".join(f"{key}={wave_counts.get(key, 0)}" for key in symbols),
        "Batches: " + "  ".join(f"{key}={batch_counts.get(key, 0)}" for key in symbols),
        "Units: " + "  ".join(f"{key}={value}" for key, value in data["unit_counts"].items()),
        f"Overall evidence-gate progress: {data['overall_progress']:.2f}%",
        "",
        "Agents:",
        f"Registered agents: {len(data['agents'])}  Human confirmation required: {data['human_confirmation_count']}",
    ]
    if data["agent_snapshot_age_seconds"] is not None:
        lines.append(f"Agent snapshot age: {duration(data['agent_snapshot_age_seconds'])}")
    if data["runtime_lagging"]:
        lines.append(colorize("WARNING: Agent runtime snapshot lags the selected tracker; RUNNING entries are shown as STALE.", "red", color))
    for agent in data["agents"]:
        elapsed = duration(agent["elapsed_seconds"]) if agent["elapsed_seconds"] is not None else "unknown"
        heartbeat = duration(agent["heartbeat_age_seconds"]) if agent["heartbeat_age_seconds"] is not None else "unknown"
        agent_line = (
            f"[{agent['effective_status']:^11}] {agent['name']}  elapsed={elapsed}  heartbeat={heartbeat} ago  "
            f"confirm={'YES' if agent['requires_human_confirmation'] else 'NO'}"
        )
        lines.append(
            colorize(
                agent_line,
                status_color(agent["effective_status"], agent["requires_human_confirmation"]),
                color,
            )
        )
        lines.append(f"             {agent['current_work']}")
        if agent["requires_human_confirmation"]:
            lines.append(f"             CONFIRMATION: {agent['confirmation_reason']}")
        if agent["heartbeat_stale"]:
            lines.append(colorize("             HEARTBEAT STALE: status snapshot is not real-time.", "red", color))
    lines.append("")
    if data["orchestrator_items"]:
        lines.append("Orchestrator:")
        for item in data["orchestrator_items"]:
            lines.append(
                f"[{item['state']:^17}] {item['wave']}/{item['batch_id']} gate={item['gate']} "
                f"owner={item['owner']} next={item.get('next_action', 'UNKNOWN')}"
            )
        lines.append("")
    for wave in data["waves"]:
        batches = " ".join(
            f"{symbols[item['state']]} {item['id']}({item['units']}) {item['progress']:.2f}%"
            for item in wave["batches"]
        )
        wave_line = f"{symbols[wave['state']]} {wave['id']} {wave['progress']:.2f}%: {batches}"
        lines.append(colorize(wave_line, status_color(wave["state"]), color))
    if int(data["tracker_age_seconds"]) > 3600:
        lines.extend(["", "WARNING: authoritative tracker is over one hour old; live agent work may be ahead."])
    alternatives = [item for item in data["workspace_candidates"] if not item["selected"]]
    if alternatives:
        lines.append("Other tracker sources: " + "; ".join(
            f"{item['branch']} audited={item['audited']}/96 progress={item['progress']:.2f}% @ {item['workspace']}"
            for item in alternatives
        ))
    lines.append("Press Ctrl-C to exit. This monitor never changes task state.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true", help="print once instead of refreshing")
    parser.add_argument("--json", action="store_true", help="emit one JSON snapshot")
    parser.add_argument("--interval", type=float, default=2.0, help="refresh interval in seconds")
    parser.add_argument("--started-at", type=parse_time, help="override elapsed-time origin (ISO-8601)")
    parser.add_argument("--workspace", type=Path, help="use an explicit Task 19 worktree instead of auto-discovery")
    args = parser.parse_args(argv)
    if args.interval <= 0:
        parser.error("--interval must be positive")
    try:
        while True:
            data = snapshot(args.started_at, args.workspace)
            use_color = sys.stdout.isatty() and not args.json and "NO_COLOR" not in os.environ
            output = json.dumps(data, ensure_ascii=False, indent=2) if args.json else render(data, color=use_color)
            if not (args.once or args.json) and sys.stdout.isatty():
                sys.stdout.write("\033[2J\033[H")
            print(output, flush=True)
            if args.once or args.json:
                return 0
            time.sleep(args.interval)
    except KeyboardInterrupt:
        return 0
    except (OSError, ValueError, StopIteration) as exc:
        print(f"task19_monitor: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
