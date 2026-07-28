"""Stable Top-K attention over visible cognitive objects."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

from engine.action import ActionType
from players.humanlike.candidates import CandidateSet, stable_action_key
from players.humanlike.memory import MemoryStore
from players.humanlike.view import DecisionContext


@dataclass(frozen=True, slots=True)
class AttentionItem:
    key: str
    category: str
    salience: float
    weight: float

    def to_dict(self) -> dict[str, object]:
        return {"key": self.key, "category": self.category, "salience": self.salience, "weight": self.weight}


def _action_salience(action_type: ActionType, mandatory: bool) -> float:
    if mandatory:
        return 4.0
    return {
        ActionType.HU: 3.5,
        ActionType.GANG_AN: 3.0,
        ActionType.GANG_JIA: 3.0,
        ActionType.GANG_MING: 3.0,
        ActionType.PONG: 2.8,
        ActionType.DISCARD: 1.8,
        ActionType.EXCHANGE: 1.7,
        ActionType.DINGQUE: 1.7,
        ActionType.PASS: 1.2,
    }[action_type]


def select_attention(
    context: DecisionContext,
    candidates: CandidateSet,
    memory: MemoryStore,
    *,
    capacity: int,
) -> tuple[AttentionItem, ...]:
    raw: dict[str, tuple[str, float]] = {}
    for candidate in candidates.candidates:
        key = f"action:{stable_action_key(candidate.action)}"
        multiplier = 0.75 + 0.25 * context.profile.defense_awareness if candidate.action.type in {ActionType.PASS, ActionType.DISCARD} else 1.0
        raw[key] = ("action", min(4.0, _action_salience(candidate.action.type, candidate.mandatory) * multiplier))
    for item in memory.ranked_items():
        category_multiplier = 0.75 + 0.5 * context.profile.defense_awareness if item.category in {"meld", "status", "recent"} else 1.0
        raw[item.key] = (item.category, min(4.0, item.strength * item.salience * category_multiplier))
    ranked = sorted(raw.items(), key=lambda pair: (-pair[1][1], pair[0]))[: max(1, int(capacity))]
    if not ranked:
        return ()
    peak = max(value[1] for _, value in ranked)
    exps = [math.exp(value[1] - peak) for _, value in ranked]
    total = sum(exps)
    return tuple(
        AttentionItem(key, value[0], round(value[1], 8), round(exp_value / total, 8))
        for (key, value), exp_value in zip(ranked, exps)
    )

