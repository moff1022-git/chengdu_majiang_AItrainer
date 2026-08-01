"""Satisficing selection, bounded noise and reproducible think-time."""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Any, Mapping

from engine.action import Action, ActionType
from players.humanlike.candidates import stable_action_key
from players.humanlike.cognition import (
    CognitiveState,
    LEVEL_FACTORS,
    effective_candidate_capacity,
    effective_satisfaction_threshold,
)
from players.humanlike.evaluator import EvaluationResult, ScoredCandidate
from players.humanlike.view import DecisionContext


@dataclass(frozen=True, slots=True)
class CognitiveDecision:
    selected: Action
    trace: Mapping[str, Any]


def _u64(parts: tuple[object, ...]) -> float:
    payload = "\x1f".join(str(part) for part in parts).encode("utf-8")
    value = int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")
    return value / 2**64


def _plan_affinity(action: Action, plan: str | None, context: DecisionContext) -> float:
    if plan == "defend" and action.type in {ActionType.PASS, ActionType.DISCARD}:
        return context.profile.defense_awareness
    if plan == "value_hand" and action.type in {ActionType.PONG, ActionType.GANG_AN, ActionType.GANG_JIA, ActionType.GANG_MING}:
        return context.profile.big_hand_preference
    if plan in {"fast_win", "clear_dingque"} and action.type in {ActionType.DISCARD, ActionType.HU}:
        return 1.0
    return 0.0


def _cognitive_order(
    context: DecisionContext,
    evaluation: EvaluationResult,
    state: CognitiveState,
    gp026: Mapping[str, Any],
) -> list[ScoredCandidate]:
    plan = state.inertial_plan or state.primary_plan
    best_score = max(item.score for item in evaluation.scored)
    inertia_window = 0.05 * float(gp026["research_threshold"])
    attention_weights = {item.key: item.weight for item in state.attention if item.category == "action"}

    def modifier(item: ScoredCandidate) -> float:
        if best_score - item.score > inertia_window + 1e-12:
            return 0.0
        return (
            _plan_affinity(item.action, plan, context) * context.profile.plan_persistence
            + attention_weights.get(f"action:{stable_action_key(item.action)}", 0.0)
            + (max(0.0, state.emotion) * context.profile.defense_awareness if item.action.type in {ActionType.PASS, ActionType.DISCARD} else 0.0)
            + (max(0.0, -state.emotion) * context.profile.big_hand_preference if item.action.type in {ActionType.PONG, ActionType.GANG_AN, ActionType.GANG_JIA, ActionType.GANG_MING} else 0.0)
        )

    return sorted(
        evaluation.scored,
        key=lambda item: (
            not item.mandatory,
            -round(modifier(item), 8),
            -item.score,
            stable_action_key(item.action),
        ),
    )


def select_cognitively(
    context: DecisionContext,
    evaluation: EvaluationResult,
    state: CognitiveState,
    *,
    gp022: Mapping[str, Any],
    gp025: Mapping[str, Any],
    gp026: Mapping[str, Any],
    config_seed: int,
    plan_restarted: bool,
    restart_reasons: tuple[str, ...],
) -> CognitiveDecision:
    rng_before = state.rng_index
    order = _cognitive_order(context, evaluation, state, gp026)
    mandatory = [item for item in order if item.mandatory]
    threshold = effective_satisfaction_threshold(context.profile.level, context.profile.style, float(gp026["satisfaction_threshold"]))
    checked: list[ScoredCandidate] = []
    stop_reason = "best_checked"
    if mandatory:
        checked = mandatory
        base = sorted(mandatory, key=lambda item: (-item.score, stable_action_key(item.action)))[0]
        stop_reason = "mandatory"
    else:
        capacity = effective_candidate_capacity(context.profile.level, int(gp026["min_candidates"]), int(gp026["max_candidates"]))
        if plan_restarted:
            capacity = max(capacity, int(gp026["min_candidates"]))
        base = order[0]
        for item in order[:capacity]:
            checked.append(item)
            satisfaction = max(0.0, min(1.0, (item.score + 0.25) / 1.5))
            base = item
            if satisfaction >= threshold:
                stop_reason = "satisficing"
                break
        else:
            base = sorted(checked, key=lambda item: (-item.score, stable_action_key(item.action)))[0]

    selected = base
    near_threshold = 0.05 * float(gp025["near_equal_randomness"])
    noise_pool = [item for item in checked if not item.mandatory and abs(base.score - item.score) <= near_threshold + 1e-12]
    noise_probability = float(gp025["max_error_probability"]) * LEVEL_FACTORS[context.profile.level]["noise"]
    rng_used = False
    if len(noise_pool) > 1 and noise_probability > 0:
        sample_parts = (
            config_seed,
            gp025["random_seed"],
            state.game_id,
            context.seat,
            context.event_index,
            state.decision_index,
            state.rng_index,
            "bounded_noise_gate",
        )
        gate = _u64(sample_parts)
        state.rng_index += 1
        rng_used = True
        if gate < noise_probability:
            temperature = max(0.005, near_threshold or 0.005)
            weights = [math.exp((item.score - base.score) / temperature) for item in noise_pool]
            draw = _u64(sample_parts[:-1] + (state.rng_index, "bounded_noise_pick")) * sum(weights)
            state.rng_index += 1
            cumulative = 0.0
            for item, weight in zip(noise_pool, weights):
                cumulative += weight
                if draw <= cumulative:
                    selected = item
                    break

    max_delay = int(gp022["max_performance_delay_ms"])
    complexity = min(1.0, len(checked) / max(1, int(gp026["max_candidates"])))
    closeness = 1.0 if len(noise_pool) > 1 else 0.0
    base_delay = max_delay * (0.15 + 0.45 * complexity + 0.2 * closeness + (0.15 if plan_restarted else 0.0))
    jitter = _u64((config_seed, state.game_id, context.seat, context.event_index, state.decision_index, "think_time"))
    think_time = round(min(max_delay, base_delay * (1.15 - 0.75 * context.profile.thinking_speed) + jitter * max_delay * 0.08))
    trace = dict(evaluation.trace)
    trace.update(
        {
            "trace_version": 2,
            "policy": "humanlike_v2_cognitive",
            "selected_action": selected.action.to_dict(),
            "cognitive_order": [stable_action_key(item.action) for item in order],
            "checked_count": len(checked),
            "checked_actions": [item.action.to_dict() for item in checked],
            "satisfaction_threshold": round(threshold, 8),
            "stop_reason": stop_reason,
            "rng_used": rng_used,
            "rng_index_before": rng_before,
            "rng_index_after": state.rng_index,
            "noise_pool_size": len(noise_pool),
            "near_threshold": round(near_threshold, 8),
            "think_time_ms": think_time,
            "plan_restarted": plan_restarted,
            "restart_reasons": list(restart_reasons),
        }
    )
    state.decision_index += 1
    return CognitiveDecision(selected.action, trace)
