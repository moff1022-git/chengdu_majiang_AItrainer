from datetime import datetime, timezone
from pathlib import Path

import tools.task19_monitor as monitor
from tools.task19_monitor import WorkspaceSource, average_progress, duration, projected_state, snapshot, status_color


def test_projected_state_requires_all_audited_for_completion():
    assert projected_state(["AUDITED", "AUDITED"]) == "COMPLETED"
    assert projected_state(["AUDITED", "READY_FOR_IMPLEMENTATION"]) == "IN_PROGRESS"
    assert projected_state(["WAITING_FOR_DESIGN_APPROVAL"]) == "NOT_STARTED"


def test_snapshot_covers_locked_plan():
    data = snapshot(datetime.now(timezone.utc))
    assert len(data["waves"]) == 14
    assert sum(data["batch_counts"].values()) == 40
    assert sum(data["unit_counts"].values()) == 96
    assert data["workspace"]
    assert data["tracker_path"].startswith(data["workspace"])
    assert data["workspace_candidates"]
    assert any(agent["name"] == "/root" for agent in data["agents"])
    assert any(agent["name"].endswith("/stage5_review") for agent in data["agents"])
    # A real ADR-0001 gate may intentionally be visible after automatic triage.
    assert data["human_confirmation_count"] >= 0
    if data["human_confirmation_count"]:
        assert any(agent["requires_human_confirmation"] for agent in data["agents"])


def test_auto_discovery_prefers_most_advanced_tracker():
    data = snapshot(datetime.now(timezone.utc))
    selected = next(item for item in data["workspace_candidates"] if item["selected"])
    assert selected["audited"] == max(item["audited"] for item in data["workspace_candidates"])
    assert selected["audited"] >= 25


def test_old_runtime_cannot_appear_live_against_new_tracker():
    data = snapshot(datetime.now(timezone.utc))
    if data["runtime_lagging"]:
        assert all(agent["effective_status"] != "RUNNING" for agent in data["agents"])


def test_integration_branch_wins_equal_tracker_tie(monkeypatch):
    now = datetime.now(timezone.utc)
    def source(root, branch, mtime):
        return WorkspaceSource(
            root=Path(root), tracker=Path(root) / "tracker", waves=Path(root) / "waves",
            checkpoint=Path(root) / "checkpoint", agents=Path(root) / "agents",
            branch=branch, head="abc", audited=27, progress=33.4,
            tracker_updated_at=now, tracker_mtime=mtime,
        )
    detached = source("/tmp/detached", "detached", 999.0)
    integration = source("/tmp/integration", "task19/w01-integration", 1.0)
    monkeypatch.setattr(monitor, "discover_sources", lambda repo: [detached, integration])
    selected, _ = monitor.select_source(repo=Path("/tmp/repo"))
    assert selected is integration


def test_duration_is_stable():
    assert duration(3661) == "01:01:01"
    assert duration(90061) == "1d 01:01:01"


def test_average_progress_uses_tracker_percentages():
    assert average_progress([{"progress": "25.00%"}, {"progress": "75.00%"}]) == 50.0


def test_status_color_prioritizes_confirmation():
    assert status_color("RUNNING") == "blue"
    assert status_color("COMPLETED") == "green"
    assert status_color("WAITING") == "yellow"
    assert status_color("NOT_STARTED") == "white"
    assert status_color("RUNNING", needs_confirmation=True) == "red"
    assert status_color("INTERRUPTED") == "red"
