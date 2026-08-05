"""Persistent private cognitive state for one humanlike player instance."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Mapping

from players.humanlike.attention import AttentionItem
from players.humanlike.memory import MemoryStore, MemorySummary, extract_visible_tokens
from players.humanlike.plan import PlanSnapshot
from players.humanlike.view import DecisionContext


LEVEL_FACTORS: Mapping[str, Mapping[str, float]] = {
    "novice": {"candidate": 0.55, "threshold": -0.15, "attention": 0.60, "noise": 1.00},
    "normal": {"candidate": 0.75, "threshold": -0.05, "attention": 0.80, "noise": 0.70},
    "skilled": {"candidate": 0.90, "threshold": 0.00, "attention": 0.95, "noise": 0.40},
    "expert": {"candidate": 1.00, "threshold": 0.05, "attention": 1.00, "noise": 0.20},
}


@dataclass(slots=True)
class CognitiveState:
    game_id: str
    memory: MemoryStore
    decision_index: int = 0
    rng_index: int = 0
    attention: tuple[AttentionItem, ...] = ()
    primary_plan: str | None = None
    inertial_plan: str | None = None
    backup_plan: str | None = None
    plan_age: int = 0
    previous_phase: str | None = None
    previous_public_event: str = ""
    emotion: float = 0.0
    opponent_impressions: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def create(cls, game_id: str, gp024: Mapping[str, Any]) -> "CognitiveState":
        return cls(
            game_id=game_id,
            memory=MemoryStore(
                initial_strength=float(gp024["initial_strength"]),
                forget_rate=float(gp024["forget_rate"]),
                salience_boost=float(gp024["salience_boost"]),
                capacity=32,
            ),
        )

    def begin_new_round(self, game_id: str, gp024: Mapping[str, Any], *, attention_capacity: int) -> None:
        if game_id == self.game_id:
            return
        history_limit = int(gp024["cross_round_history"])
        if history_limit:
            categories: dict[str, int] = {}
            for item in self.memory.items.values():
                if item.category in {"meld", "status", "discard"}:
                    categories[item.category] = categories.get(item.category, 0) + 1
            if categories:
                self.opponent_impressions.append({"round": self.game_id, "public_categories": categories})
                self.opponent_impressions = self.opponent_impressions[-history_limit:]
        self.game_id = game_id
        self.memory = MemoryStore(
            initial_strength=float(gp024["initial_strength"]),
            forget_rate=float(gp024["forget_rate"]),
            salience_boost=float(gp024["salience_boost"]),
            capacity=max(8, int(attention_capacity) * 4),
        )
        self.decision_index = 0
        self.rng_index = 0
        self.attention = ()
        self.primary_plan = None
        self.inertial_plan = None
        self.backup_plan = None
        self.plan_age = 0
        self.previous_phase = None
        self.previous_public_event = ""
        self.emotion = 0.0

    def update_memory(self, context: DecisionContext) -> MemorySummary:
        return self.memory.update(context.event_index, extract_visible_tokens(context.view.payload))

    def update_plan(self, context: DecisionContext, plan: PlanSnapshot) -> tuple[bool, tuple[str, ...]]:
        public_event = json.dumps(context.view.payload.get("last_public_event") or {}, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
        reasons = []
        if self.previous_phase is not None and self.previous_phase != context.phase:
            reasons.append("phase_changed")
        if self.previous_public_event and public_event != self.previous_public_event:
            reasons.append("public_event_changed")
        if self.primary_plan is not None and self.primary_plan != plan.primary:
            reasons.append("plan_changed")
        restarted = bool(reasons)
        previous_plan = self.primary_plan
        if not restarted and previous_plan == plan.primary:
            self.plan_age += 1
        else:
            self.plan_age = 0
        self.inertial_plan = previous_plan if not restarted else None
        self.primary_plan = plan.primary
        self.backup_plan = plan.backup
        self.previous_phase = context.phase
        self.previous_public_event = public_event
        return restarted, tuple(reasons)

    def update_emotion(self, context: DecisionContext, emotional_stability: float) -> float:
        players = [context.view.payload.get("self_player")] + list(context.view.payload.get("other_players") or [])
        scores = [float(item.get("score", 0)) for item in players if isinstance(item, Mapping)]
        own = context.view.payload.get("self_player")
        own_score = float(own.get("score", 0)) if isinstance(own, Mapping) else 0.0
        opponent_scores = [score for index, score in enumerate(scores) if index != 0]
        gap = own_score - (sum(opponent_scores) / len(opponent_scores) if opponent_scores else own_score)
        target = max(-1.0, min(1.0, gap / 20.0)) * (1.0 - float(emotional_stability))
        self.emotion = max(-1.0, min(1.0, self.emotion * 0.75 + target * 0.25))
        return self.emotion


def effective_attention_capacity(level: str, configured: int) -> int:
    return max(1, round(configured * LEVEL_FACTORS[level]["attention"]))


def effective_candidate_capacity(level: str, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, round(maximum * LEVEL_FACTORS[level]["candidate"])))


def effective_satisfaction_threshold(level: str, style: str, configured: float, *, preset_id: str | None = None) -> float:
    if preset_id == "nonhuman_optimized":
        return max(0.0, min(1.0, float(configured)))
    style_delta = {"conservative": -0.04, "balanced": 0.0, "aggressive": 0.04}[style]
    return max(0.45, min(0.95, configured + LEVEL_FACTORS[level]["threshold"] + style_delta))
