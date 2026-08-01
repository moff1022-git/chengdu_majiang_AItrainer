import json

import pytest

from tools.task19_agent_runtime import (
    read_orchestrator, read_payload, record_finding, set_confirmation, sync_agents,
    update_work_item, upsert_agent, validate_agent,
)


def agent(name="/root/worker", status="WAITING", work="Waiting for dependency"):
    return {
        "name": name,
        "status": status,
        "current_work": work,
        "started_at": None,
        "last_heartbeat": None,
        "requires_human_confirmation": False,
        "confirmation_reason": None,
    }


def test_sync_replaces_complete_tree_atomically(tmp_path):
    path = tmp_path / "runtime.json"
    sync_agents(path, [agent(), agent("/root/worker/reviewer", "COMPLETED", "Review completed")])
    payload = read_payload(path)
    assert [item["name"] for item in payload["agents"]] == ["/root/worker", "/root/worker/reviewer"]
    assert json.loads(path.read_text())["schema_version"] == 1


def test_upsert_preserves_tree_and_sets_running_times(tmp_path):
    path = tmp_path / "runtime.json"
    sync_agents(path, [agent()])
    payload = upsert_agent(path, {"name": "/root/new", "status": "RUNNING", "current_work": "Implementing"})
    assert len(payload["agents"]) == 2
    running = next(item for item in payload["agents"] if item["name"] == "/root/new")
    assert running["started_at"] and running["last_heartbeat"]


def test_upsert_does_not_reset_existing_start_time(tmp_path):
    path = tmp_path / "runtime.json"
    original = agent("/root", "RUNNING", "Implementing")
    original["started_at"] = "2026-07-30T23:00:30+08:00"
    sync_agents(path, [original])
    payload = upsert_agent(path, {"name": "/root", "status": "RUNNING", "current_work": "Reviewing"})
    assert payload["agents"][0]["started_at"] == "2026-07-30T23:00:30+08:00"


def test_confirmation_and_waiting_require_reasons():
    with pytest.raises(ValueError, match="confirmation_reason"):
        validate_agent({**agent(), "requires_human_confirmation": True})
    with pytest.raises(ValueError, match="waiting for"):
        validate_agent(agent(work="Idle"))


def test_confirmation_lifecycle_is_visible_and_reversible(tmp_path):
    path = tmp_path / "runtime.json"
    sync_agents(path, [agent("/root", "RUNNING", "Orchestrating")])
    opened = set_confirmation(path, "/root", True, "Approve elevated full regression")
    assert opened["agents"][0]["requires_human_confirmation"] is True
    assert opened["agents"][0]["confirmation_reason"] == "Approve elevated full regression"
    closed = set_confirmation(path, "/root", False)
    assert closed["agents"][0]["requires_human_confirmation"] is False
    assert closed["agents"][0]["confirmation_reason"] is None


def test_confirmation_rejects_unknown_agent(tmp_path):
    path = tmp_path / "runtime.json"
    sync_agents(path, [agent()])
    with pytest.raises(ValueError, match="unknown agent"):
        set_confirmation(path, "/root/missing", True, "Approve")


def test_orchestrator_persists_ready_and_dispatched_states(tmp_path):
    path = tmp_path / "orchestrator.json"
    update_work_item(path, {"batch_id": "T19-D05", "wave": "W04", "gate": "IMPLEMENT",
                            "state": "READY_TO_DISPATCH", "owner": "/root", "next_action": "DISPATCH_IMPLEMENTER"})
    update_work_item(path, {"batch_id": "T19-D05", "wave": "W04", "gate": "IMPLEMENT",
                            "state": "DISPATCHED", "owner": "/root/worker", "next_action": "WAIT_FOR_AGENT"})
    item = read_orchestrator(path)["work_items"][0]
    assert item["state"] == "DISPATCHED" and item["owner"] == "/root/worker"


def test_third_same_finding_requires_human_confirmation(tmp_path):
    path = tmp_path / "orchestrator.json"
    for _ in range(3):
        payload = record_finding(path, "T19-D14", "W04", "DESIGN_REVIEW", "P1-SAME", "/root/fixer")
    item = payload["work_items"][0]
    assert item["state"] == "BLOCKED"
    assert item["requires_human_confirmation"] is True
    assert item["remediation_counts"]["P1-SAME"] == 3
