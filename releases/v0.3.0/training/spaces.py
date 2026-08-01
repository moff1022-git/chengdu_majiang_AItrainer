"""Observation / action helpers for ChengduMahjongEnv (M11)."""

from __future__ import annotations

from itertools import combinations
from typing import Any

from engine.action import Action, ActionType
from engine.tile import Suit, Tile, parse_tile

# Stable observation keys returned by ChengduMahjongEnv
OBS_KEYS = (
    "game_id",
    "seat",
    "phase",
    "view",
    "legal_actions",
    "request_id",
)

PHASE_ONE_HOT = (
    "dealt",
    "exchange",
    "dingque",
    "ready",
    "draw",
    "discard",
    "response",
    "finished",
)

TILE_FACE_ORDER: list[str] = [
    f"{s.value}_{r}" for s in Suit for r in range(1, 10)
]  # 27 faces


def enumerate_exchange_actions(hand: list[Tile]) -> list[Action]:
    """All unique same-suit triples from hand as EXCHANGE actions."""
    seen: set[tuple[str, ...]] = set()
    actions: list[Action] = []
    for suit in Suit:
        suit_tiles = [t for t in hand if t.suit == suit]
        if len(suit_tiles) < 3:
            continue
        for combo in combinations(range(len(suit_tiles)), 3):
            tiles = tuple(suit_tiles[i] for i in combo)
            key = tuple(sorted(t.id for t in tiles))
            if key in seen:
                continue
            seen.add(key)
            actions.append(Action(ActionType.EXCHANGE, tiles=tiles))
    return actions


def opening_dingque_actions() -> list[Action]:
    return [Action(ActionType.DINGQUE, suit=s) for s in Suit]


def encode_obs_vector(obs: dict[str, Any]) -> list[float] | Any:
    """
    Lightweight flat vector: hand 27 counts + wall_remaining + phase one-hot.
    Returns list[float]; if numpy is installed, returns np.ndarray.
    """
    view = obs.get("view") or {}
    seat = int(obs.get("seat", 0))
    hand_ids: list[str] = []
    for p in view.get("players") or []:
        if int(p.get("seat", -1)) == seat:
            hand_ids = list(p.get("hand") or [])
            break
    counts = {tid: 0.0 for tid in TILE_FACE_ORDER}
    for hid in hand_ids:
        if isinstance(hid, str) and hid in counts:
            counts[hid] += 1.0
        else:
            try:
                tid = parse_tile(str(hid)).id
                if tid in counts:
                    counts[tid] += 1.0
            except Exception:
                pass
    vec: list[float] = [counts[tid] for tid in TILE_FACE_ORDER]
    wall_rem = float(view.get("wall_remaining") or 0)
    vec.append(wall_rem)
    phase = str(obs.get("phase") or "")
    for name in PHASE_ONE_HOT:
        vec.append(1.0 if phase == name else 0.0)

    try:
        import numpy as np  # type: ignore

        return np.asarray(vec, dtype=np.float32)
    except ImportError:
        return vec
