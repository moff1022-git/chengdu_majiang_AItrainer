"""Replay humanlike decisions from private Audit v1 PlayerView snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from engine.action import Action
from engine.audit import AuditError, canonical_json_bytes, load_audit, verify_audit
from players.humanlike.player import HumanlikeV2Player
from protocols.messages import ActionRequest, Observation


@dataclass(frozen=True, slots=True)
class PolicyReplayResult:
    game_id: str
    replayed: int
    skipped: int
    matched: bool


def _same(left: Any, right: Any) -> bool:
    return canonical_json_bytes(left) == canonical_json_bytes(right)


def replay_humanlike_audit(
    path: Path | str,
    *,
    config_path: Path | str | None = None,
) -> PolicyReplayResult:
    verification = verify_audit(path, strict=True)
    records = load_audit(path)
    players: dict[int, HumanlikeV2Player] = {}
    replayed = 0
    skipped = 0
    trace_fields = (
        "selected_action",
        "stop_reason",
        "checked_actions",
        "rng_used",
        "rng_index_before",
        "rng_index_after",
        "memory",
        "attention",
        "plan",
        "think_time_ms",
        "plan_restarted",
        "restart_reasons",
    )
    for row in records:
        if row.get("kind") != "decision":
            continue
        if row.get("policy") != "humanlike_v2_cognitive":
            skipped += 1
            continue
        seat = int(row["seat"])
        player = players.get(seat)
        if player is None:
            player = HumanlikeV2Player(seed=0, config_path=config_path)
            player.on_join(seat, {})
            players[seat] = player
        view = row["player_view"]
        observation = Observation(
            game_id=str(view["game_id"]),
            self_seat=int(view["self_seat"]),
            phase=str(view["phase"]),
            view=dict(view["view"]),
        )
        player.observe(observation)
        legal = [Action.from_dict(action) for action in row["legal_actions"]]
        request = ActionRequest(
            request_id=f"audit-{row['decision_index']}",
            seat=seat,
            phase=str(row["phase"]),
            legal_actions=legal,
            deadline_ms=None,
        )
        decision = player.decide(request)
        if not _same(decision.action.to_dict(), row["selected_action"]):
            raise AuditError(f"policy replay action mismatch at decision {row['decision_index']}")
        expected = row["decision_trace"]
        for field in trace_fields:
            if not _same(decision.analysis.get(field), expected.get(field)):
                raise AuditError(f"policy replay trace mismatch at decision {row['decision_index']}: {field}")
        replayed += 1
    return PolicyReplayResult(verification.game_id, replayed, skipped, True)


__all__ = ["PolicyReplayResult", "replay_humanlike_audit"]
