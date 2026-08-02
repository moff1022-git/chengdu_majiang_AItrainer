"""PlayerView-only observation encoder for training contract v2."""

from __future__ import annotations

from typing import Any

from engine.tile import Suit, parse_tile
from training.action_codec_v2 import ACTION_SPACE_SIZE
from training.spaces import PHASE_ONE_HOT, TILE_FACE_ORDER

TRAINING_CONTRACT_VERSION = 2
_FACE_INDEX = {face: i for i, face in enumerate(TILE_FACE_ORDER)}


def _face(value: Any) -> int | None:
    try:
        return _FACE_INDEX[parse_tile(str(value)).id]
    except (KeyError, TypeError, ValueError):
        return None


def encode_observation_v2(obs: dict[str, Any], action_mask: tuple[int, ...] | list[int], cognitive: dict[str, Any] | None = None) -> dict[str, Any]:
    if len(action_mask) != ACTION_SPACE_SIZE or any(v not in (0, 1) for v in action_mask):
        raise ValueError(f"action_mask must contain {ACTION_SPACE_SIZE} binary values")
    view = obs.get("view") or {}
    seat = int(obs.get("seat", 0))
    players = list(view.get("players") or [])
    by_seat = {int(p.get("seat", -1)): p for p in players if isinstance(p, dict)}
    own = by_seat.get(seat, {})
    hand = [0] * 27
    for raw in own.get("hand") or []:
        idx = _face(raw)
        if idx is not None:
            hand[idx] += 1
    dingque = [[0, 0, 0, 0] for _ in range(4)]
    discards = [[0] * 27 for _ in range(4)]
    active = [0] * 4
    scores = [0.0] * 4
    public_melds: list[dict[str, Any]] = []
    own_melds: list[dict[str, Any]] = []
    for player_seat, player in by_seat.items():
        if not 0 <= player_seat < 4:
            continue
        dq = player.get("dingque")
        dingque[player_seat][0 if dq is None else tuple(Suit).index(Suit(dq)) + 1] = 1
        active[player_seat] = int(player.get("status") == "active")
        scores[player_seat] = max(-10.0, min(10.0, float(player.get("score", 0)) / 100.0))
        for raw in player.get("discard_pile") or []:
            idx = _face(raw)
            if idx is not None:
                discards[player_seat][idx] += 1
        for meld in player.get("melds") or []:
            safe = {k: meld[k] for k in ("kind", "tile_id", "suit", "tile_count") if k in meld}
            safe["seat"] = player_seat
            public_melds.append(safe)
            if player_seat == seat:
                own_melds.append(dict(safe))
    sequence = []
    for event in sorted(view.get("discard_history") or [], key=lambda e: int(e.get("event_index", 0))):
        idx = _face(event.get("face_id"))
        if idx is not None:
            sequence.append((int(event.get("seat", -1)), idx, int(event.get("claimed_by") is not None)))
    current = [0] * 4
    dealer = [0] * 4
    if isinstance(view.get("current_seat"), int) and 0 <= view["current_seat"] < 4:
        current[view["current_seat"]] = 1
    if isinstance(view.get("dealer_seat"), int) and 0 <= view["dealer_seat"] < 4:
        dealer[view["dealer_seat"]] = 1
    exact = view.get("wall_remaining")
    wall = {"visibility": "exact" if exact is not None else "hidden", "exact": exact, "lower": exact, "upper": exact}
    phase = str(obs.get("phase") or view.get("phase") or "")
    result: dict[str, Any] = {
        "game_id": obs.get("game_id"), "seat": seat, "phase": phase,
        "observation_version": TRAINING_CONTRACT_VERSION,
        "hand_counts": hand, "own_melds": own_melds, "dingque_one_hot": dingque,
        "discard_counts": discards, "discard_sequence": sequence, "public_melds": public_melds,
        "active_seats": active, "current_seat_one_hot": current, "dealer_seat_one_hot": dealer,
        "wall": wall, "scores": scores,
        "phase_one_hot": [int(phase == name) for name in PHASE_ONE_HOT],
        "action_mask": list(action_mask), "action_space_size": ACTION_SPACE_SIZE,
        "legal_actions": list(obs.get("legal_actions") or []), "request_id": obs.get("request_id", ""),
    }
    if cognitive is not None:
        allowed = {"plan", "memory_counts", "attention_weights", "emotion", "rng_index"}
        result["cognitive"] = {key: cognitive[key] for key in allowed if key in cognitive}
    return result


def flatten_observation_v2(obs: dict[str, Any]) -> list[float]:
    meld_counts = [0.0] * (4 * 27)
    for meld in obs.get("public_melds") or []:
        idx = _face(meld.get("tile_id"))
        seat = int(meld.get("seat", -1))
        if idx is not None and 0 <= seat < 4:
            meld_counts[seat * 27 + idx] += 1.0
    wall = obs.get("wall") or {}
    values = [*obs["hand_counts"]]
    values += [float(x) for row in obs["dingque_one_hot"] for x in row]
    values += [float(x) for row in obs["discard_counts"] for x in row]
    values += meld_counts + [*map(float, obs["active_seats"]), *map(float, obs["current_seat_one_hot"]), *map(float, obs["dealer_seat_one_hot"])]
    values += [float(wall.get("exact") or 0), float(wall.get("lower") or 0), float(wall.get("upper") or 0)]
    values += [*map(float, obs["scores"]), *map(float, obs["phase_one_hot"]), *map(float, obs["action_mask"])]
    return values

