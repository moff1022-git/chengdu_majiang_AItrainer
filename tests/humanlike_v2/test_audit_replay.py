from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.action import Action, ActionType
from engine.audit import (
    AuditError,
    DecisionAuditWriter,
    canonical_hash,
    canonical_json_bytes,
    load_audit,
    verify_audit,
)
from engine.deal import create_dealt_game
from engine.orchestrator import PlayerGameRunner
from players.humanlike.audit_replay import replay_humanlike_audit
from players.registry import create_players
from protocols.view_filter import build_observation


def test_canonical_hash_is_order_independent_and_rejects_nan() -> None:
    assert canonical_hash({"b": 2, "a": [1, 3]}) == canonical_hash({"a": [1, 3], "b": 2})
    with pytest.raises(AuditError, match="canonical JSON"):
        canonical_json_bytes({"bad": float("nan")})


def _manual_audit(path: Path) -> Path:
    state = create_dealt_game("f28-audit-unit", num_players=2)
    state.phase = "dingque"
    observation = build_observation(state, 0)
    observation.phase = "dingque"
    observation.view["phase"] = "dingque"
    legal = [Action(ActionType.DINGQUE, suit=suit) for suit in state.players[0].hand[0].suit.__class__]
    selected = legal[0]
    trace = {
        "trace_version": 2,
        "policy": "humanlike_v2_cognitive",
        "config_hash": "a" * 64,
        "selected_action": selected.to_dict(),
        "rng_used": False,
        "rng_index_before": 0,
        "rng_index_after": 0,
        "memory": {},
        "attention": [],
        "plan": {},
        "checked_actions": [selected.to_dict()],
        "stop_reason": "mandatory",
        "think_time_ms": 10,
    }
    writer = DecisionAuditWriter(
        path,
        game_id=state.game_id,
        engine_config={"num_players": 2},
        initial_state=state.to_dict(),
    )
    writer.record_decision(
        seat=0,
        phase="dingque",
        state_before=state.to_dict(),
        state_after=state.to_dict(),
        player_view=observation.to_dict(),
        legal_actions=[action.to_dict() for action in legal],
        selected_action=selected.to_dict(),
        reason="fixture",
        decision_trace=trace,
    )
    writer.finish(final_state=state.to_dict(), finished_reason="fixture")
    return path


def test_writer_verifier_and_footer_contract(tmp_path: Path) -> None:
    path = _manual_audit(tmp_path / "unit.audit.jsonl")
    result = verify_audit(path)
    assert result.complete is True
    assert result.decision_count == 1
    assert len(result.final_record_hash) == 64
    records = load_audit(path)
    assert [record["kind"] for record in records] == ["header", "decision", "footer"]
    assert records[1]["player_view_hash"] == canonical_hash(records[1]["player_view"])


def test_tampering_and_truncation_are_detected(tmp_path: Path) -> None:
    path = _manual_audit(tmp_path / "tampered.audit.jsonl")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    rows[1]["reason"] = "changed"
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
    with pytest.raises(AuditError, match="record hash mismatch"):
        verify_audit(path)

    truncated = _manual_audit(tmp_path / "truncated.audit.jsonl")
    lines = truncated.read_text(encoding="utf-8").splitlines()[:-1]
    truncated.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(AuditError, match="requires a footer"):
        verify_audit(truncated)
    assert verify_audit(truncated, strict=False).complete is False


def test_writer_rejects_opponent_hand_leak_and_illegal_action(tmp_path: Path) -> None:
    state = create_dealt_game("f28-audit-leak", num_players=2)
    state.phase = "dingque"
    observation = build_observation(state, 0).to_dict()
    observation["phase"] = "dingque"
    observation["view"]["phase"] = "dingque"
    other = next(player for player in observation["view"]["players"] if player["seat"] == 1)
    other["hand"] = ["wan_1"]
    writer = DecisionAuditWriter(
        tmp_path / "leak.audit.jsonl",
        game_id=state.game_id,
        engine_config={"num_players": 2},
        initial_state=state.to_dict(),
    )
    with pytest.raises(AuditError, match="opponent concealed hand"):
        writer.record_decision(
            seat=0,
            phase="dingque",
            state_before=state.to_dict(),
            state_after=state.to_dict(),
            player_view=observation,
            legal_actions=[{"type": "dingque", "suit": "wan"}],
            selected_action={"type": "dingque", "suit": "tong"},
            reason="bad",
            decision_trace=None,
        )
    writer.close()


def _run_audited(path: Path, game_id: str) -> tuple[PlayerGameRunner, Path]:
    players = create_players(["humanlike_v2", "humanlike_v2"], base_seed=45)
    runner = PlayerGameRunner(
        players,
        game_id=game_id,
        save_dir=path,
        save_every_decision=True,
    )
    runner.run()
    return runner, path / f"{game_id}.audit.jsonl"


def test_runner_audit_verifies_and_policy_replays(tmp_path: Path) -> None:
    runner, path = _run_audited(tmp_path, "f28-audit-e2e")
    verification = verify_audit(path)
    replay = replay_humanlike_audit(path)
    assert verification.decision_count > 10
    assert replay.matched and replay.replayed == verification.decision_count
    assert verification.final_state_hash == canonical_hash(runner.state.to_dict())
    assert (tmp_path / "f28-audit-e2e.steps.jsonl").exists()


def test_same_game_produces_identical_audit_hash_chain(tmp_path: Path) -> None:
    _, first = _run_audited(tmp_path / "a", "f28-audit-repeat")
    _, second = _run_audited(tmp_path / "b", "f28-audit-repeat")
    first_hashes = [record["record_hash"] for record in load_audit(first)]
    second_hashes = [record["record_hash"] for record in load_audit(second)]
    assert first_hashes == second_hashes

