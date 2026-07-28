"""Selectable deterministic PlayerView-v2 humanlike baseline player."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app_paths import configs_dir
from players.base_player import BasePlayer
from players.humanlike.belief import build_public_belief
from players.humanlike.candidates import build_candidates, stable_action_key
from players.humanlike.config import HumanlikeConfig, load_config
from players.humanlike.evaluator import evaluate_candidates
from players.humanlike.hand_analyzer import analyze_action
from players.humanlike.runtime import RoundRuntime
from players.humanlike.view import PolicyInputError, build_decision_context
from protocols.messages import ActionRequest, Decision, Observation


def default_humanlike_config_path() -> Path:
    return configs_dir() / "humanlike_v2" / "default.json"


class HumanlikeV2Player(BasePlayer):
    """F0028-3 policy: deterministic and limited to its received player view."""

    def __init__(self, *args: Any, config_path: str | Path | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._config_path = Path(config_path) if config_path else default_humanlike_config_path()
        self.humanlike_config: HumanlikeConfig | None = None
        self.profile = None
        self.runtime: RoundRuntime | None = None
        self._round_game_id: str | None = None

    def on_join(self, seat: int, config: dict) -> None:
        if seat not in range(4):
            raise PolicyInputError("humanlike_v2 seat must be in 0..3")
        self.seat = seat
        self.config = dict(config or {})
        self.humanlike_config = load_config(self._config_path)
        self.profile = self.humanlike_config.players[seat]
        if not self.name or self.name in {"HumanlikeV2Player", "humanlike_v2"}:
            self.name = f"HumanlikeV2-{seat}"
        self.runtime = None
        self._round_game_id = None

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
            self._round_game_id = observation.game_id

    def decide(self, request: ActionRequest) -> Decision:
        if self.seat is None or self.humanlike_config is None or self.profile is None:
            raise PolicyInputError("humanlike_v2 must join before deciding")
        if self.runtime is None:
            raise PolicyInputError("decision requires an observed round")
        context = build_decision_context(
            self.last_observation,
            request,
            bound_seat=self.seat,
            profile=self.profile,
            config_hash=self.humanlike_config.config_hash,
        )
        gp026 = self.humanlike_config.global_parameters["GP-026"]
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

        self.runtime.set_parameter("RP-015", {"view_version": 2, "event_index": context.event_index})
        self.runtime.set_parameter("RP-016", belief.summary())
        selected_scored = next(item for item in evaluation.scored if item.action.to_dict() == evaluation.selected.to_dict())
        self.runtime.set_parameter("RP-017", selected_scored.features.to_dict())
        self.runtime.set_parameter("RP-018", evaluation.plan.to_dict())
        self.runtime.set_parameter("RP-023", {"count": len(candidates.candidates), "actions": [item.action.to_dict() for item in candidates.candidates]})
        self.runtime.set_parameter("RP-026", {"selected_action": evaluation.selected.to_dict(), "score": selected_scored.score})
        self.runtime.append_decision(evaluation.trace)
        return Decision(
            request_id=request.request_id,
            action=evaluation.selected,
            reason=f"humanlike_v2:deterministic:{evaluation.selected.type.value}",
            analysis=dict(evaluation.trace),
        )
