"""NDJSON wire codec for human subprocess protocol."""

from __future__ import annotations

import json
from typing import Any

from engine.action import Action
from protocols.messages import ActionRequest, Decision, Observation

PROTOCOL_VERSION = 1


def encode_line(obj: dict[str, Any]) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n"


def decode_line(line: str) -> dict[str, Any]:
    line = line.strip()
    if not line:
        raise ValueError("empty wire line")
    data = json.loads(line)
    if not isinstance(data, dict) or "type" not in data:
        raise ValueError(f"invalid wire message: {line[:80]!r}")
    return data


def msg_hello(seat: int, pid: int) -> dict:
    return {
        "type": "hello",
        "seat": seat,
        "version": PROTOCOL_VERSION,
        "pid": pid,
    }


def msg_window_ready(
    seat: int, *, x: int, y: int, w: int, h: int, title: str = ""
) -> dict:
    """Seat → main: pygame window is mapped and titled."""
    return {
        "type": "window_ready",
        "seat": int(seat),
        "x": int(x),
        "y": int(y),
        "w": int(w),
        "h": int(h),
        "title": str(title or ""),
    }


def msg_observation(obs: Observation) -> dict:
    return {"type": "observation", **obs.to_dict()}


def msg_action_request(req: ActionRequest, hints: dict | None = None) -> dict:
    d = {"type": "action_request", **req.to_dict()}
    if hints is not None:
        d["hints"] = hints
    return d


def msg_decision(dec: Decision) -> dict:
    return {"type": "decision", **dec.to_dict()}


def msg_game_end(result: dict) -> dict:
    return {"type": "game_end", "result": result}


def msg_ready_request(
    *,
    round_index: int = 1,
    game_id: str = "",
    num_players: int = 4,
    num_rounds: int = 1,
) -> dict:
    """Main → seat: ask player window to confirm starting this hand."""
    return {
        "type": "ready_request",
        "round": int(round_index),
        "game_id": str(game_id or ""),
        "num_players": int(num_players),
        "num_rounds": int(num_rounds),
    }


def msg_ready(seat: int, *, auto: bool = False) -> dict:
    """Seat → main: confirm start for this hand."""
    return {
        "type": "ready",
        "seat": int(seat),
        "auto": bool(auto),
    }


def msg_set_geometry(*, x: int, y: int, w: int, h: int) -> dict:
    """Main → seat: re-position / resize the Tk seat window (multi-monitor fix)."""
    return {
        "type": "set_geometry",
        "x": int(x),
        "y": int(y),
        "w": int(w),
        "h": int(h),
    }


def msg_seat_settings(
    seat: int,
    *,
    auto_start: bool | None = None,
    ai_type: str | None = None,
    predict_opponents: bool | None = None,
) -> dict:
    """Seat → main: update auto-start / AI / predict prefs for this seat."""
    d: dict = {"type": "seat_settings", "seat": int(seat)}
    if auto_start is not None:
        d["auto_start"] = bool(auto_start)
    if ai_type is not None:
        d["ai_type"] = str(ai_type)
    if predict_opponents is not None:
        d["predict_opponents"] = bool(predict_opponents)
    return d


def msg_shutdown() -> dict:
    return {"type": "shutdown"}


def msg_error(message: str) -> dict:
    return {"type": "error", "message": message}


def parse_decision(data: dict) -> Decision:
    if data.get("type") != "decision":
        raise ValueError(f"expected decision, got {data.get('type')}")
    action = Action.from_dict(data["action"])
    return Decision(
        request_id=str(data["request_id"]),
        action=action,
        reason=str(data.get("reason") or "human"),
        analysis=data.get("analysis"),
        think_ms=data.get("think_ms"),
    )


def parse_observation(data: dict) -> Observation:
    return Observation(
        game_id=str(data["game_id"]),
        self_seat=int(data["self_seat"]),
        phase=str(data["phase"]),
        view=dict(data.get("view") or {}),
    )


def parse_action_request(data: dict) -> tuple[ActionRequest, dict | None]:
    legal = [Action.from_dict(a) for a in data.get("legal_actions") or []]
    req = ActionRequest(
        request_id=str(data["request_id"]),
        seat=int(data["seat"]),
        phase=str(data["phase"]),
        legal_actions=legal,
        deadline_ms=data.get("deadline_ms"),
    )
    hints = data.get("hints")
    return req, hints if isinstance(hints, dict) else None
