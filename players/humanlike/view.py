"""Validated, read-only decision context derived only from PlayerView v2 messages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engine.action import Action
from players.humanlike.config import PlayerProfile
from protocols.messages import ActionRequest, Observation
from protocols.player_view_v2 import PLAYER_VIEW_VERSION, PlayerViewV2


class PolicyInputError(ValueError):
    """Raised when a policy message violates the approved F0028-3 contract."""


@dataclass(frozen=True, slots=True)
class DecisionContext:
    request_id: str
    seat: int
    phase: str
    event_index: int
    view: PlayerViewV2
    legal_actions: tuple[Action, ...]
    profile: PlayerProfile
    config_hash: str


def _legacy_to_v2(observation: Observation) -> PlayerViewV2:
    raw = observation.view
    if not isinstance(raw, Mapping):
        raise PolicyInputError("observation.view must be a mapping")
    if raw.get("view_version") != PLAYER_VIEW_VERSION:
        raise PolicyInputError(f"humanlike_v2 requires PlayerView version {PLAYER_VIEW_VERSION}")
    players = raw.get("players")
    if not isinstance(players, (list, tuple)):
        raise PolicyInputError("PlayerView v2 projection is missing players")
    own = [dict(item) for item in players if isinstance(item, Mapping) and item.get("seat") == observation.self_seat]
    if len(own) != 1:
        raise PolicyInputError("PlayerView must contain exactly one self player")
    others = [dict(item) for item in players if isinstance(item, Mapping) and item.get("seat") != observation.self_seat]
    payload: dict[str, Any] = {
        "dealer_seat": raw.get("dealer_seat"),
        "turn_index": raw.get("turn_index", 0),
        "current_seat": raw.get("current_seat"),
        "exchange_direction_public": raw.get("exchange_dir_resolved"),
        "wall": raw.get("wall"),
        "wall_remaining": raw.get("wall_remaining"),
        "self_player": own[0],
        "other_players": others,
        "discard_history": list(raw.get("discard_history") or []),
        "legal_actions": list(raw.get("legal_actions") or []),
        "deadline_ms": raw.get("deadline_ms"),
        "last_public_event": dict(raw.get("last_public_event") or {}),
    }
    return PlayerViewV2(
        game_id=observation.game_id,
        self_seat=observation.self_seat,
        phase=observation.phase,
        event_index=int(raw.get("turn_index", 0) or 0),
        payload=payload,
    )


def build_decision_context(
    observation: Observation | None,
    request: ActionRequest,
    *,
    bound_seat: int,
    profile: PlayerProfile,
    config_hash: str,
) -> DecisionContext:
    if observation is None:
        raise PolicyInputError("decision requires a prior observation")
    if not request.legal_actions:
        raise PolicyInputError("legal_actions must not be empty")
    if request.phase not in {"exchange", "dingque", "response", "discard"}:
        raise PolicyInputError(f"unsupported decision phase: {request.phase!r}")
    if request.seat != bound_seat or observation.self_seat != bound_seat:
        raise PolicyInputError("request, observation and bound player seats must match")
    if request.phase != observation.phase:
        raise PolicyInputError("request and observation phases must match")
    view = _legacy_to_v2(observation)
    return DecisionContext(
        request_id=request.request_id,
        seat=bound_seat,
        phase=request.phase,
        event_index=view.event_index,
        view=view,
        legal_actions=tuple(request.legal_actions),
        profile=profile,
        config_hash=config_hash,
    )

