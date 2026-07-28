"""Deterministic Q(action) evaluation and trace construction."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN
from typing import Any, Mapping

from engine.action import Action, ActionType
from engine.hand_utils import tile_index
from engine.tile import Suit
from players.humanlike.belief import PublicBelief
from players.humanlike.candidates import CandidateSet, stable_action_key
from players.humanlike.hand_analyzer import HandFeatures, analyze_action, visible_hand
from players.humanlike.plan import PlanSnapshot, choose_plan
from players.humanlike.view import DecisionContext


@dataclass(frozen=True, slots=True)
class ScoredCandidate:
    action: Action
    mandatory: bool
    features: HandFeatures
    score: float


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    selected: Action
    plan: PlanSnapshot
    scored: tuple[ScoredCandidate, ...]
    trace: Mapping[str, Any]


def _q8(value: float) -> float:
    return float(Decimal(str(value)).quantize(Decimal("0.00000001"), rounding=ROUND_HALF_EVEN))


def _adjustment(context: DecisionContext, action: Action) -> float:
    profile = context.profile
    if action.type == ActionType.HU:
        return 1.0
    if action.type in {ActionType.GANG_AN, ActionType.GANG_JIA, ActionType.GANG_MING}:
        return 0.12 * profile.gang_preference
    if action.type == ActionType.PONG:
        return 0.08 * profile.peng_preference
    if action.type == ActionType.PASS:
        return 0.04 * profile.defense_awareness
    return 0.0


def _dingque_score(action: Action, hand) -> float:
    if action.suit is None:
        return -1.0
    count = sum(1 for tile in hand if tile.suit == action.suit)
    structural = sum(1 for tile in hand if tile.suit == action.suit and 2 <= tile.rank <= 8)
    return _q8(1.0 - count / 14.0 - structural / 140.0)


def evaluate_candidates(
    context: DecisionContext,
    candidates: CandidateSet,
    belief: PublicBelief,
    weights: Mapping[str, float],
) -> EvaluationResult:
    hand, _, dingque = visible_hand(context)
    scored: list[ScoredCandidate] = []
    for candidate in candidates.candidates:
        action = candidate.action
        features = analyze_action(context, action, belief)
        if context.phase == "dingque":
            score = _dingque_score(action, hand)
        else:
            score = sum(float(weights[key]) * float(getattr(features, key)) for key in ("speed", "hand_value", "defense", "flexibility"))
            score += _adjustment(context, action)
            if action.type == ActionType.DISCARD and action.tiles and dingque is not None:
                has_dingque = any(tile.suit == dingque for tile in hand)
                if has_dingque and action.tiles[0].suit != dingque:
                    score -= 2.0
            if context.phase == "exchange" and action.tiles:
                danger = sum(belief.danger_by_face[tile_index(tile)] for tile in action.tiles) / len(action.tiles)
                score += 0.1 * danger
        scored.append(ScoredCandidate(action, candidate.mandatory, features, _q8(score)))

    mandatory = [item for item in scored if item.mandatory]
    pool = mandatory or scored
    ranked = sorted(pool, key=lambda item: (-item.score, stable_action_key(item.action)))
    selected = ranked[0].action
    representative = ranked[0].features
    plan = choose_plan(representative)
    all_ranked = sorted(scored, key=lambda item: (-item.score, stable_action_key(item.action)))
    trace = {
        "trace_version": 1,
        "policy": "humanlike_v2_deterministic",
        "view_version": 2,
        "config_hash": context.config_hash,
        "event_index": context.event_index,
        "phase": context.phase,
        "plan": plan.to_dict(),
        "belief_summary": belief.summary(),
        "candidates": [
            {"action": item.action.to_dict(), "mandatory": item.mandatory, "features": {key: getattr(item.features, key) for key in ("speed", "hand_value", "defense", "flexibility")}, "score": item.score}
            for item in all_ranked
        ],
        "selected_action": selected.to_dict(),
        "stop_reason": "deterministic_argmax",
        "rng_used": False,
    }
    return EvaluationResult(selected, plan, tuple(all_ranked), trace)

