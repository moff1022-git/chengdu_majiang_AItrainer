"""Legal-only deterministic candidate construction."""

from __future__ import annotations

from dataclasses import dataclass

from engine.action import Action, ActionType
from players.humanlike.view import DecisionContext, PolicyInputError


_ACTION_ORDER = {
    ActionType.HU: 0,
    ActionType.GANG_AN: 1,
    ActionType.GANG_JIA: 2,
    ActionType.GANG_MING: 3,
    ActionType.PONG: 4,
    ActionType.DISCARD: 5,
    ActionType.EXCHANGE: 6,
    ActionType.DINGQUE: 7,
    ActionType.PASS: 8,
}


def stable_action_key(action: Action) -> tuple[int, str, tuple[str, ...]]:
    return (_ACTION_ORDER[action.type], action.suit.value if action.suit else "", tuple(sorted(tile.id for tile in action.tiles)))


@dataclass(frozen=True, slots=True)
class Candidate:
    action: Action
    mandatory: bool


@dataclass(frozen=True, slots=True)
class CandidateSet:
    candidates: tuple[Candidate, ...]


def _mandatory(action: Action, context: DecisionContext) -> bool:
    if len(context.legal_actions) == 1:
        return True
    if action.type != ActionType.HU:
        return False
    gp009 = context.view.payload.get("policy_gp009")
    # GP is normally supplied by the evaluator/player; absent public metadata is
    # handled conservatively: discard-phase HU is self-draw and cannot pass.
    if context.phase == "discard":
        return True
    return bool(gp009 and not gp009.get("discard_hu_can_pass", True))


def build_candidates(
    context: DecisionContext,
    *,
    max_candidates: int,
    pre_scores: dict[tuple[int, str, tuple[str, ...]], float] | None = None,
) -> CandidateSet:
    if max_candidates < 1:
        raise PolicyInputError("max_candidates must be positive")
    ordered = sorted(context.legal_actions, key=stable_action_key)
    mandatory = [Candidate(action, True) for action in ordered if _mandatory(action, context)]
    ordinary = [Candidate(action, False) for action in ordered if not _mandatory(action, context)]
    scores = pre_scores or {}
    ordinary.sort(key=lambda item: (-scores.get(stable_action_key(item.action), 0.0), stable_action_key(item.action)))
    kept = mandatory + ordinary[:max_candidates]
    if not kept:
        raise PolicyInputError("candidate set must not be empty")
    return CandidateSet(tuple(kept))
