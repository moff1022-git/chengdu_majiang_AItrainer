"""Selectable deterministic PlayerView-v2 humanlike baseline player."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from app_paths import configs_dir
from players.base_player import BasePlayer
from players.humanlike.belief import build_public_belief
from players.humanlike.attention import select_attention
from players.humanlike.candidates import build_candidates, stable_action_key
from players.humanlike.cognition import CognitiveState, effective_attention_capacity
from players.humanlike.config import HumanlikeConfig, load_config
from players.humanlike.evaluator import evaluate_candidates
from players.humanlike.hand_analyzer import analyze_action
from players.humanlike.policy import select_cognitively
from players.humanlike.personality_presets import effective_search_depth
from players.humanlike.public_derivation import derive_public_rps
from players.humanlike.runtime import RoundRuntime
from players.humanlike.state010 import SeatRuntimeStore
from players.humanlike.view import PolicyInputError, build_decision_context
from protocols.messages import ActionRequest, Decision, Observation


def default_humanlike_config_path() -> Path:
    return configs_dir() / "humanlike_v2" / "default.json"


class HumanlikeV2Player(BasePlayer):
    """F0028-4 cognitive policy limited to its received PlayerView sequence."""

    def __init__(self, *args: Any, config_path: str | Path | None = None, preset_id: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._config_path = Path(config_path) if config_path else default_humanlike_config_path()
        self.preset_id = preset_id
        self.humanlike_config: HumanlikeConfig | None = None
        self.profile = None
        self.runtime: RoundRuntime | None = None
        self.cognitive_state: CognitiveState | None = None
        self._round_game_id: str | None = None
        self.state010_store: SeatRuntimeStore | None = None

    def on_join(self, seat: int, config: dict) -> None:
        if seat not in range(4):
            raise PolicyInputError("humanlike_v2 seat must be in 0..3")
        self.seat = seat
        self.config = dict(config or {})
        if self.preset_id:
            import tempfile
            from players.humanlike.personality_presets import apply_personality_preset
            raw = json.loads(self._config_path.read_text(encoding="utf-8"))
            raw["players"][seat] = apply_personality_preset(raw["players"][seat], self.preset_id)
            with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
                json.dump(raw, handle, ensure_ascii=False)
                override_path = Path(handle.name)
            try:
                self.humanlike_config = load_config(override_path, self._config_path.with_name("compatibility.json"))
            finally:
                override_path.unlink(missing_ok=True)
        else:
            self.humanlike_config = load_config(self._config_path)
        self.profile = self.humanlike_config.players[seat]
        player_payload = self.humanlike_config.normalized_dict()["players"][seat]
        self.player_config_hash = hashlib.sha256(json.dumps(player_payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if not self.name or self.name in {"HumanlikeV2Player", "humanlike_v2"}:
            self.name = f"HumanlikeV2-{seat}"
        self.runtime = None
        self.cognitive_state = None
        self._round_game_id = None
        self.state010_store = None

    def observe(self, observation: Observation) -> None:
        super().observe(observation)
        if self.seat is None or self.humanlike_config is None:
            raise PolicyInputError("humanlike_v2 must join before observing")
        if observation.self_seat != self.seat:
            raise PolicyInputError("observation seat does not match player seat")
        if self._round_game_id != observation.game_id:
            scores = [0, 0, 0, 0]
            for item in observation.view.get("players") or []:
                seat = int(item.get("seat", -1))
                if seat in range(4):
                    scores[seat] = int(item.get("score", 0))
            self.runtime = RoundRuntime.create_round(
                round_id=observation.game_id,
                round_index=1,
                dealer_id=int(observation.view.get("dealer_seat", 0)),
                self_seat=self.seat,
                scores=tuple(scores),
            )
            self.state010_store = SeatRuntimeStore(observation.game_id)
            self._round_game_id = observation.game_id
            gp024 = self.profile.cognitive_parameters["GP-024"]
            gp026 = self.profile.cognitive_parameters["GP-026"]
            if self.cognitive_state is None:
                self.cognitive_state = CognitiveState.create(observation.game_id, gp024)
                self.cognitive_state.memory.capacity = max(8, int(gp026["attention_capacity"]) * 4)
            else:
                self.cognitive_state.begin_new_round(
                    observation.game_id,
                    gp024,
                    attention_capacity=int(gp026["attention_capacity"]),
                )

    def decide(self, request: ActionRequest) -> Decision:
        if self.seat is None or self.humanlike_config is None or self.profile is None:
            raise PolicyInputError("humanlike_v2 must join before deciding")
        if self.runtime is None or self.cognitive_state is None:
            raise PolicyInputError("decision requires an observed round")
        context = build_decision_context(
            self.last_observation,
            request,
            bound_seat=self.seat,
            profile=self.profile,
            config_hash=self.humanlike_config.config_hash,
        )
        public_projection = dict(context.view.payload)
        for parameter_id, payload in derive_public_rps(public_projection).items():
            self._set_rp(parameter_id, payload)
        gp026 = self.profile.cognitive_parameters["GP-026"]
        gp022 = self.humanlike_config.global_parameters["GP-022"]
        gp025 = self.profile.cognitive_parameters["GP-025"]
        self.runtime.begin_decision(
            legal_actions=[action.to_dict() for action in request.legal_actions],
            deadline_ms=int(request.deadline_ms or 0),
        )
        belief = build_public_belief(context)
        weights = gp026["decision_weights"]
        pre_scores = {}
        for action in context.legal_actions:
            features = analyze_action(context, action, belief)
            pre_scores[stable_action_key(action)] = sum(
                float(weights[key]) * float(getattr(features, key))
                for key in ("speed", "hand_value", "defense", "flexibility")
            )
        candidates = build_candidates(
            context,
            max_candidates=int(gp026["max_candidates"]),
            pre_scores=pre_scores,
        )
        evaluation = evaluate_candidates(context, candidates, belief, weights)
        memory_summary = self.cognitive_state.update_memory(context)
        self.cognitive_state.update_emotion(context, float(gp025["emotional_stability"]))
        plan_restarted, restart_reasons = self.cognitive_state.update_plan(context, evaluation.plan)
        attention = select_attention(
            context,
            candidates,
            self.cognitive_state.memory,
            capacity=effective_attention_capacity(
                context.profile.level,
                int(gp026["attention_capacity"]),
            ),
        )
        self.cognitive_state.attention = attention
        decision = select_cognitively(
            context,
            evaluation,
            self.cognitive_state,
            gp022=gp022,
            gp025=gp025,
            gp026=gp026,
            config_seed=self.humanlike_config.seed,
            plan_restarted=plan_restarted,
            restart_reasons=restart_reasons,
            preset_id=self.preset_id,
        )
        trace = dict(decision.trace)
        trace["configured_search_depth"] = int(gp026["search_depth"])
        trace["effective_search_depth"] = effective_search_depth(
            context.profile.level,
            int(gp026["search_depth"]),
            preset_id=self.preset_id,
        )
        trace["preset_id"] = self.preset_id
        trace["memory"] = memory_summary.to_dict()
        trace["attention"] = [item.to_dict() for item in attention]
        trace["personality"] = {
            "level": context.profile.level,
            "style": context.profile.style,
            "plan_persistence": context.profile.plan_persistence,
            "emotion": round(self.cognitive_state.emotion, 8),
        }
        trace["parameter_snapshot"] = {
            "preset_id": self.preset_id,
            "cognitive_7": {k: gp026.get(k) for k in ("min_candidates", "max_candidates", "search_depth", "attention_capacity", "satisfaction_threshold", "research_threshold")},
            "behavior": {k: gp025.get(k) for k in ("max_error_probability", "near_equal_randomness", "emotional_stability", "habit_strength")},
            "style_8": {k: getattr(context.profile, k) for k in ("peng_preference", "gang_preference", "big_hand_preference", "defense_awareness", "plan_persistence", "thinking_speed")},
            "decision_weights": dict(gp026.get("decision_weights", {})),
            "gp009": dict(self.humanlike_config.global_parameters["GP-009"]),
            "config_hash": self.player_config_hash,
        }
        trace["plan_state"] = {
            "primary_plan": self.cognitive_state.primary_plan,
            "inertial_plan": self.cognitive_state.inertial_plan,
            "plan_age": self.cognitive_state.plan_age,
            "plan_restarted": plan_restarted,
        }
        trace["hu_rule"] = {
            "pass_hu_mode": self.humanlike_config.global_parameters["GP-009"].get("pass_hu_mode"),
            "discard_hu_can_pass": self.humanlike_config.global_parameters["GP-009"].get("discard_hu_can_pass"),
            "self_draw_can_pass": self.humanlike_config.global_parameters["GP-009"].get("self_draw_can_pass"),
            "forced_hu_wall_threshold": self.humanlike_config.global_parameters["GP-009"].get("forced_hu_wall_threshold"),
            "hu_candidates": [item.action.to_dict() for item in candidates.candidates if item.action.type.value == "hu"],
            "mandatory_hu": any(item.action.type.value == "hu" and item.mandatory for item in candidates.candidates),
        }
        trace["cross_round_impressions"] = len(self.cognitive_state.opponent_impressions)
        trace["player_config_hash"] = self.player_config_hash

        self._set_rp("RP-015", {"view_version": 2, "event_index": context.event_index})
        self._set_rp("RP-016", belief.summary())
        selected_scored = next(item for item in evaluation.scored if item.action.to_dict() == decision.selected.to_dict())
        self._set_rp("RP-017", selected_scored.features.to_dict())
        self._set_rp("RP-018", evaluation.plan.to_dict())
        self._set_rp("RP-023", {"count": len(candidates.candidates), "actions": [item.action.to_dict() for item in candidates.candidates]})
        self._set_rp("RP-024", memory_summary.to_dict() | {"cross_round_impressions": len(self.cognitive_state.opponent_impressions)})
        self._set_rp("RP-025", [item.to_dict() for item in attention])
        self._set_rp("RP-026", {"selected_action": decision.selected.to_dict(), "score": selected_scored.score, "checked_count": trace["checked_count"], "stop_reason": trace["stop_reason"], "configured_search_depth": trace["configured_search_depth"], "effective_search_depth": trace["effective_search_depth"]})
        self._set_rp("RP-027", {"deadline_ms": int(request.deadline_ms or 0), "think_time_ms": trace["think_time_ms"], "time_pressure": bool(request.deadline_ms and trace["think_time_ms"] >= request.deadline_ms)})
        self._set_rp("RP-028", {"personality": trace["personality"], "plan_restarted": plan_restarted, "restart_reasons": list(restart_reasons)})
        self.runtime.append_decision(trace)
        return Decision(
            request_id=request.request_id,
            action=decision.selected,
            reason=f"humanlike_v2:cognitive:{decision.selected.type.value}:{trace['stop_reason']}",
            analysis=trace,
        )

    def _set_rp(self, parameter_id: str, value: Any) -> None:
        assert self.runtime is not None and self.state010_store is not None and self.seat is not None
        self.runtime.set_enveloped_parameter(parameter_id, value, role="player_policy", owner_seat=self.seat)
        version = self.state010_store.version(self.seat)
        result = self.state010_store.update(actor_seat=self.seat, owner_seat=self.seat, changes={parameter_id: value}, expected_version=version)
        if not result.accepted:
            raise PolicyInputError(f"STATE-010 update failed: {result.error_code}")
