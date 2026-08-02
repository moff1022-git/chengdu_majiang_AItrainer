"""Public-information-only belief features for F0028-3."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math
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
    opponent_hypotheses: tuple[dict[str, Any], ...] = ()

    def summary(self) -> dict[str, Any]:
        return {"visible_total": sum(self.visible_counts), "unseen_total": sum(self.unseen_counts), "opponent_hypotheses": self.opponent_hypotheses}


def model_001_rule_baseline(opponents: tuple[Mapping[str, Any], ...]) -> tuple[dict[str, Any], ...]:
    """MODEL-001 public-event-only deterministic fallback distribution."""
    forbidden = {"hand", "physical_hand", "oracle_hands", "wall_order", "label_zone", "truth"}
    out = []
    def contains_forbidden(value: Any) -> bool:
        if isinstance(value, Mapping):
            return bool(forbidden.intersection(value)) or any(contains_forbidden(v) for v in value.values())
        if isinstance(value, (list, tuple)): return any(contains_forbidden(v) for v in value)
        return False
    for opponent in opponents:
        if contains_forbidden(opponent):
            raise PolicyInputError("FORBIDDEN_FEATURE")
        seat = opponent.get("seat")
        if not isinstance(seat, int) or isinstance(seat, bool):
            raise PolicyInputError("FEATURE_SCHEMA")
        meld_counts = [1.0, 1.0, 1.0, 1.0]
        evidence = 0
        for meld in opponent.get("melds", ()):
            face = parse_tile(str(meld["tile_id"]))
            meld_counts[face.suit.sort_key] += int(meld.get("tile_count", 3))
            evidence += 1
        total = sum(meld_counts)
        suit_probs = tuple(v / total for v in meld_counts)
        shape_raw = [1.0, 1.0, 1.0 + evidence, 1.0 + max(meld_counts[:3]) - 1.0, 1.0]
        shape_total = sum(shape_raw)
        discards = tuple(str(v) for v in opponent.get("discard_pile", ()))
        dingque = opponent.get("dingque")
        dq_discards = sum(face.startswith(f"{dingque}_") for face in discards) if dingque else 0
        p_cleared = min(0.95, 0.2 + 0.12 * dq_discards) if dingque else 0.25
        shape_probs=tuple(v / shape_total for v in shape_raw); all_probs=(*suit_probs,*shape_probs)
        out.append({"seat": seat, "p_cleared": p_cleared, "dominant_suit_probs": suit_probs, "shape_probs": shape_probs, "evidence_count": evidence + len(discards), "low_evidence": evidence + len(discards) == 0, "uncertainty": -sum(p*math.log(p) for p in all_probs if p>0), "max_probability": max(all_probs), "prior": {"alpha":1.0}, "posterior": {"dingque_discards":dq_discards,"meld_evidence":evidence}, "contributions": {"public_discards":len(discards),"public_melds":evidence}, "forbidden_scan":"passed", "model_version": "MODEL-001-rule-baseline-v1", "fallback_reason": "RULE_BASELINE"})
    return tuple(sorted(out, key=lambda row: row["seat"]))


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
    hypotheses = model_001_rule_baseline(tuple(others))
    return PublicBelief(tuple(counts), unseen, tuple(pressures[1:]), tuple(danger), hypotheses)
