"""Stable Top-K attention over visible cognitive objects."""

from __future__ import annotations

import math
from decimal import Decimal, ROUND_HALF_EVEN
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
    explanation: dict[str, object] | None = None

    def to_dict(self) -> dict[str, object]:
        return {"key": self.key, "category": self.category, "salience": self.salience, "weight": self.weight, "explanation": self.explanation}


def rank_attention_cues(cues: Iterable[dict[str, object]], *, capacity: int) -> tuple[dict[str, object], ...]:
    """HEUR-019 normative baseline for generic visible cues (ranking, not choice)."""
    if not 1 <= capacity <= 64:
        raise ValueError("CAPACITY_RANGE")
    ranked = []
    q = Decimal("0.00000001")
    for cue in cues:
        key = cue.get("candidate_key")
        if not isinstance(key, str) or not key:
            raise ValueError("FEATURE_SCHEMA")
        vals = []
        for name in ("salience", "freshness", "memory_strength"):
            value = cue.get(name)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)) or not 0 <= float(value) <= 1:
                raise ValueError("FEATURE_RANGE")
            vals.append(Decimal(str(value)))
        mandatory = bool(cue.get("mandatory", False))
        score = (Decimal(int(mandatory)) + Decimal("0.7") * vals[0] + Decimal("0.4") * vals[1] + Decimal("0.3") * vals[2]).quantize(q, rounding=ROUND_HALF_EVEN)
        ranked.append((not mandatory, -score, key, {"candidate_key": key, "mandatory": mandatory, "raw_features": {"salience": float(vals[0]), "freshness": float(vals[1]), "memory_strength": float(vals[2])}, "score_components": {"mandatory": int(mandatory), "salience": float(Decimal("0.7")*vals[0]), "freshness": float(Decimal("0.4")*vals[1]), "memory": float(Decimal("0.3")*vals[2])}, "corrections": {"style": 0.0, "level": 0.0, "phase": 0.0}, "final_score": float(score), "selected": False, "filtered_reason": None, "abandon_reason": None, "stop_reason": None}))
    ranked.sort(key=lambda row: row[:3])
    mandatory_rows = [row[3] for row in ranked if not row[0]]
    ordinary = [row[3] for row in ranked if row[0]][:capacity]
    return tuple({**row, "rank": index + 1} for index, row in enumerate((*mandatory_rows, *ordinary)))


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
    mandatory_keys={f"action:{stable_action_key(c.action)}" for c in candidates.candidates if c.mandatory}
    cues=({"candidate_key":key,"mandatory":key in mandatory_keys,"salience":min(1.0,value[1]/4.0),"freshness":1.0,"memory_strength":min(1.0,value[1]/4.0)} for key,value in raw.items())
    normative=rank_attention_cues(cues,capacity=max(1,int(capacity)))
    ranked=[(str(item["candidate_key"]),raw[str(item["candidate_key"])]) for item in normative]
    if not ranked:
        return ()
    peak = max(value[1] for _, value in ranked)
    exps = [math.exp(value[1] - peak) for _, value in ranked]
    total = sum(exps)
    return tuple(
        AttentionItem(key, value[0], round(value[1], 8), round(exp_value / total, 8), {"candidate_key": key, "generated_by": value[0], "legal": True, "raw_features": {"salience": round(value[1],8)}, "score_components": {"softmax_input": round(value[1],8)}, "corrections": {"style_level_phase": 0.0}, "final_score": round(value[1],8), "rank": i+1, "selected": True, "filtered_reason": None, "abandon_reason": None, "stop_reason": "top_k"})
        for i, ((key, value), exp_value) in enumerate(zip(ranked, exps))
    )
