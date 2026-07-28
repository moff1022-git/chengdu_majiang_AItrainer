"""Public-information-only belief features for F0028-3."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Mapping

from engine.hand_utils import NUM_FACES, tile_index
from engine.tile import Suit, parse_tile
from players.humanlike.view import DecisionContext, PolicyInputError


@dataclass(frozen=True, slots=True)
class PublicBelief:
    visible_counts: tuple[int, ...]
    unseen_counts: tuple[int, ...]
    opponent_suit_pressure: tuple[tuple[float, float, float], ...]
    danger_by_face: tuple[float, ...]

    def summary(self) -> dict[str, Any]:
        return {"visible_total": sum(self.visible_counts), "unseen_total": sum(self.unseen_counts)}


def _add_face(counts: list[int], face_id: str, amount: int = 1) -> None:
    try:
        idx = tile_index(parse_tile(face_id))
    except ValueError as exc:
        raise PolicyInputError(f"invalid visible face id: {face_id!r}") from exc
    counts[idx] += amount
    if counts[idx] > 4:
        raise PolicyInputError(f"visible tile count exceeds four for {face_id}")


def build_public_belief(context: DecisionContext) -> PublicBelief:
    payload = context.view.payload
    own = payload["self_player"]
    others = payload["other_players"]
    counts = [0] * NUM_FACES
    seen_physical: set[int] = set()

    physical = own.get("physical_hand") if isinstance(own, Mapping) else None
    if physical:
        for item in physical:
            tile_id = int(item["tile_id"])
            if tile_id in seen_physical:
                raise PolicyInputError(f"duplicate visible physical tile id: {tile_id}")
            seen_physical.add(tile_id)
            _add_face(counts, str(item["face_id"]))
    else:
        for face_id in own.get("hand", ()):
            _add_face(counts, str(face_id))

    players = (own, *tuple(others))
    pressures: list[tuple[float, float, float]] = []
    public_discards: set[str] = set()
    claimed = Counter(
        str(record.get("face_id"))
        for record in payload.get("discard_history", ())
        if isinstance(record, Mapping) and record.get("claimed_by") is not None
    )
    for player in players:
        suit_melds = [0, 0, 0]
        for face_id in player.get("discard_pile", ()):
            face = str(face_id)
            if claimed[face] > 0:
                claimed[face] -= 1
                public_discards.add(face)
                continue
            _add_face(counts, face)
            public_discards.add(face)
        for meld in player.get("melds", ()):
            if not isinstance(meld, Mapping) or "tile_id" not in meld:
                continue
            face = parse_tile(str(meld["tile_id"]))
            amount = int(meld.get("tile_count", 3))
            _add_face(counts, face.id, amount)
            suit_melds[face.suit.sort_key] += amount
        total = sum(suit_melds)
        pressures.append(tuple(round(value / total, 8) if total else 0.0 for value in suit_melds))

    unseen = tuple(4 - value for value in counts)
    danger: list[float] = []
    for idx in range(NUM_FACES):
        suit = idx // 9
        rank = idx % 9 + 1
        face_id = f"{(Suit.WAN, Suit.TONG, Suit.TIAO)[suit].value}_{rank}"
        if face_id in public_discards:
            value = 0.1
        else:
            scarcity = counts[idx] / 4.0
            center = 1.0 - abs(rank - 5) / 5.0
            pressure = max((p[suit] for p in pressures[1:]), default=0.0)
            value = 0.15 + 0.35 * center + 0.35 * pressure - 0.2 * scarcity
        danger.append(round(max(0.0, min(1.0, value)), 8))
    return PublicBelief(tuple(counts), unseen, tuple(pressures[1:]), tuple(danger))
