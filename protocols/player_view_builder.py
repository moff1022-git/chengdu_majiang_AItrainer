"""Explicit whitelist builder for PlayerView v2."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from engine.state import GameState, Meld, PlayerState
from protocols.player_view_v2 import PlayerViewV2

VISIBILITY_LEVELS = frozenset({"hidden", "public_partial", "public_exact"})
DEFAULT_VISIBILITY = {
    "wall_remaining": "public_exact",
    "draw_source": "public_exact",
    "exchange_source": "public_exact",
    "concealed_gang_tiles": "public_exact",
    "hu_hand": "public_exact",
    "draw_round_hand": "public_exact",
    "thinking_time": "hidden",
    "cancel_action": "hidden",
}


def _visibility(policy: Mapping[str, str] | None) -> dict[str, str]:
    result = dict(DEFAULT_VISIBILITY)
    if policy:
        for key, value in policy.items():
            if key in result:
                if value not in VISIBILITY_LEVELS:
                    raise ValueError(f"invalid visibility {key}={value!r}")
                result[key] = value
    return result


def _public_meld(meld: Meld, level: str) -> dict[str, Any]:
    result: dict[str, Any] = {"kind": meld.kind, "tile_count": len(meld.tile_ids)}
    if meld.kind != "an_gang" or level == "public_exact":
        result["tile_id"] = meld.face.id
    elif level == "public_partial":
        result["suit"] = meld.face.suit.value
    return result


def _player_dict(player: PlayerState, *, own: bool, visibility: Mapping[str, str], phase: str) -> dict[str, Any]:
    meld_level = visibility["concealed_gang_tiles"]
    result: dict[str, Any] = {
        "seat": player.seat,
        "score": player.score,
        "is_dealer": player.is_dealer,
        "dingque": player.dingque.value if player.dingque else None,
        "melds": [_public_meld(meld, meld_level) for meld in player.melds],
        "discard_pile": [tile.id for tile in player.discard_pile],
        "hand_count": len(player.hand),
        "status": player.status,
        "hu_order": player.hu_order,
        "last_win": dict(player.last_win) if player.last_win else None,
    }
    reveal_level = visibility["draw_round_hand"] if phase == "finished" else visibility["hu_hand"]
    if own:
        result["hand"] = [tile.id for tile in player.sorted_hand()]
        result["physical_hand"] = [
            {"tile_id": tile.tile_id, "face_id": tile.face_id}
            for tile in player.sorted_hand()
        ]
    elif player.status == "finished" and reveal_level == "public_exact":
        result["revealed_hand"] = [tile.id for tile in player.sorted_hand()]
    elif player.status == "finished" and reveal_level == "public_partial":
        result["revealed_hand_count"] = len(player.hand)
    return result


class PlayerViewBuilder:
    def __init__(self, visibility: Mapping[str, str] | None = None) -> None:
        self.visibility = _visibility(visibility)

    def build(
        self,
        state: GameState,
        seat: int,
        *,
        legal_actions: list[dict[str, Any]] | None = None,
        deadline_ms: int | None = None,
    ) -> PlayerViewV2:
        if state.phase not in {"dealt","exchange","dingque","ready","draw","discard","response","finished"}:
            raise ValueError("INVALID_PHASE")
        if seat not in {player.seat for player in state.players}:
            raise ValueError(f"INVALID_VIEWER: {seat}")
        wall_level = self.visibility["wall_remaining"]
        if wall_level == "hidden":
            wall_remaining: int | None = None
            wall: dict[str, Any] | None = None
        elif wall_level == "public_partial":
            exact = len(state.wall)
            lower = (exact // 8) * 8
            wall_remaining = None
            wall = {"remaining_min": lower, "remaining_max": min(108, lower + 7), "bucket": lower // 8}
        else:
            wall_remaining = len(state.wall)
            wall = {"remaining_exact": wall_remaining}

        exchange_level = self.visibility["exchange_source"]
        exchange_direction = state.exchange_dir_resolved if exchange_level != "hidden" else None
        players = [
            _player_dict(player, own=player.seat == seat, visibility=self.visibility, phase=state.phase)
            for player in sorted(state.players, key=lambda item: item.seat)
        ]
        payload: dict[str, Any] = {
            "dealer_seat": state.dealer_seat,
            "turn_index": state.turn_index,
            "current_seat": state.current_seat,
            "exchange_direction_public": exchange_direction,
            "wall": wall,
            "self_player": next(player for player in players if player["seat"] == seat),
            "other_players": [player for player in players if player["seat"] != seat],
            "discard_history": [
                {
                    "event_index": record.event_index,
                    "seat": player.seat,
                    "face_id": next(tile.id for tile in player.discard_pile if tile.tile_id == record.tile_id),
                    "claimed_by": record.claimed_by,
                    "claim_kind": record.claim_kind,
                }
                for player in state.players
                for record in player.discard_records
            ],
            "legal_actions": list(legal_actions or []),
            "deadline_ms": deadline_ms,
            "last_public_event": {
                "type": "discard" if state.last_discard else None,
                "face_id": state.last_discard.id if state.last_discard else None,
                "seat": state.last_discard_seat,
                "draw_source": None if self.visibility["draw_source"] != "public_partial" else "unknown",
                "thinking_time": None,
                "cancel_action": None,
            },
        }
        view = PlayerViewV2(
            game_id=state.game_id,
            self_seat=seat,
            phase=state.phase,
            event_index=state.turn_index,
            payload=payload,
        )
        # STATE-005 production boundary: force full canonical traversal now.
        _ = view.stable_hash
        return view

    def build_legacy_dict(self, state: GameState, seat: int) -> dict[str, Any]:
        result = self.build(state, seat).to_legacy_dict()
        result["schema_version"] = state.schema_version
        result["num_players"] = state.num_players
        result["wall_remaining"] = len(state.wall) if self.visibility["wall_remaining"] == "public_exact" else None
        exchange_level = self.visibility["exchange_source"]
        result["exchange_log"] = []
        if exchange_level != "hidden":
            for event in state.exchange_log or []:
                item = {"from_seat": event.get("from_seat"), "to_seat": event.get("to_seat")}
                if exchange_level == "public_exact" and int(event.get("to_seat", -1)) == seat:
                    item["tiles"] = list(event.get("tiles") or [])
                result["exchange_log"].append(item)
        pending: dict[str, list[str]] = {}
        submitted: dict[str, bool] = {}
        for pending_seat, tiles in (state.pending_exchange or {}).items():
            submitted[str(pending_seat)] = bool(tiles)
            if pending_seat == seat:
                pending[str(pending_seat)] = [tile.id for tile in tiles]
        result["pending_exchange"] = pending
        result["exchange_submitted"] = submitted
        result["last_discard"] = state.last_discard.id if state.last_discard else None
        result["last_discard_seat"] = state.last_discard_seat
        result["response_seats"] = list(state.response_seats or [])
        result["after_gang_draw"] = state.after_gang_draw
        result["finished_reason"] = state.finished_reason
        result["hu_sequence"] = list(state.hu_sequence or [])
        result["hu_count"] = state.hu_count
        result["end_settled"] = state.end_settled
        result["settle_tags"] = dict(state.settle_tags or {})
        return result
