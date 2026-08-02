"""Deterministic migration of face-only state schemas to physical schema 5."""

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from typing import Any

from engine.physical_tile import physical_id_for
from engine.tile import parse_tile


class StateMigrationError(ValueError):
    """A legacy snapshot cannot be mapped to one conserved physical wall."""


def _meld_size(kind: str) -> int:
    if kind == "pong":
        return 3
    if kind in {"ming_gang", "an_gang", "jia_gang"}:
        return 4
    raise StateMigrationError(f"unsupported legacy meld kind: {kind!r}")


def migrate_state_to_v5(raw_state: dict[str, Any]) -> dict[str, Any]:
    """Return a new schema-5 dict; never mutate the caller's legacy state."""
    if not isinstance(raw_state, dict):
        raise StateMigrationError("state must be an object")
    version = int(raw_state.get("schema_version", 0))
    if version == 5:
        return deepcopy(raw_state)
    if version not in {1, 2, 3, 4}:
        raise StateMigrationError(f"cannot migrate schema_version {version}")

    data = deepcopy(raw_state)
    players = data.get("players")
    if not isinstance(players, list):
        raise StateMigrationError("legacy players must be an array")
    players.sort(key=lambda item: int(item.get("seat", -1)))

    pools: dict[str, list[int]] = {}
    for suit in ("wan", "tong", "tiao"):
        for rank in range(1, 10):
            face_id = f"{suit}_{rank}"
            face = parse_tile(face_id)
            pools[face_id] = [physical_id_for(face, copy) for copy in range(4)]

    def take(face_id: str, context: str) -> int:
        if face_id not in pools:
            raise StateMigrationError(f"invalid face {face_id!r} at {context}")
        if not pools[face_id]:
            raise StateMigrationError(f"more than four ownership tiles for {face_id} at {context}")
        return pools[face_id].pop(0)

    wall_ids = [take(str(face), f"wall[{index}]") for index, face in enumerate(data.get("wall") or [])]
    player_hand_ids: dict[int, list[int]] = {}
    discard_slots: list[tuple[int, int, str]] = []
    for player in players:
        seat = int(player["seat"])
        player_hand_ids[seat] = [take(str(face), f"players[{seat}].hand") for face in player.get("hand") or []]
        for index, face in enumerate(player.get("discard_pile") or []):
            discard_slots.append((seat, index, str(face)))

    claimed_slots: set[tuple[int, int]] = set()
    discard_assignment: dict[tuple[int, int], dict[str, Any]] = {}
    melds_by_seat: dict[int, list[dict[str, Any]]] = defaultdict(list)

    def latest_unclaimed_discard(face_id: str) -> tuple[int, int] | None:
        candidates = [
            (seat, index)
            for seat, index, face in discard_slots
            if face == face_id and (seat, index) not in claimed_slots
        ]
        return max(candidates) if candidates else None

    for player in players:
        seat = int(player["seat"])
        for meld_index, raw_meld in enumerate(player.get("melds") or []):
            if not isinstance(raw_meld, dict):
                raise StateMigrationError(f"invalid meld at seat {seat}")
            kind = str(raw_meld.get("kind"))
            face_id = str(raw_meld.get("tile_id") or raw_meld.get("tile") or "")
            size = _meld_size(kind)
            tile_ids: list[int] = []
            source_seat = None
            claimed_event = None
            if kind in {"pong", "ming_gang", "jia_gang"}:
                slot = latest_unclaimed_discard(face_id)
                if slot is not None:
                    source_seat, claimed_event = slot
                    claimed_slots.add(slot)
                    claimed_id = take(face_id, f"claimed discard for seat {seat} meld {meld_index}")
                    discard_assignment[slot] = {
                        "event_index": claimed_event,
                        "seat": source_seat,
                        "tile_id": claimed_id,
                        "claimed_by": seat,
                        "claim_kind": kind,
                    }
                    tile_ids.append(claimed_id)
            while len(tile_ids) < size:
                tile_ids.append(take(face_id, f"seat {seat} meld {meld_index}"))
            melds_by_seat[seat].append(
                {
                    "kind": kind,
                    "tile_ids": sorted(tile_ids),
                    "source_seat": source_seat,
                    "claimed_discard_event": claimed_event,
                }
            )

    # Remaining discard history owns a tile unless it is a plausible historical
    # hu reference already represented in a finished winner's concealed hand.
    for seat, index, face_id in discard_slots:
        slot = (seat, index)
        if slot in discard_assignment:
            continue
        if pools[face_id]:
            tile_id = take(face_id, f"players[{seat}].discard_pile[{index}]")
            discard_assignment[slot] = {
                "event_index": index,
                "seat": seat,
                "tile_id": tile_id,
                "claimed_by": None,
                "claim_kind": None,
            }
            continue
        winner = next(
            (
                player
                for player in players
                if isinstance(player.get("last_win"), dict)
                and player["last_win"].get("loser") == seat
                and any(
                    # IDs assigned from the same four-id face block.
                    tile_id // 4 == physical_id_for(parse_tile(face_id), 0) // 4
                    for tile_id in player_hand_ids[int(player["seat"])]
                )
            ),
            None,
        )
        if winner is None:
            raise StateMigrationError(f"cannot place legacy discard {face_id} for seat {seat}")
        winner_ids = player_hand_ids[int(winner["seat"])]
        tile_type = physical_id_for(parse_tile(face_id), 0) // 4
        tile_id = min(value for value in winner_ids if value // 4 == tile_type)
        discard_assignment[slot] = {
            "event_index": index,
            "seat": seat,
            "tile_id": tile_id,
            "claimed_by": int(winner["seat"]),
            "claim_kind": "hu",
        }

    if any(pool for pool in pools.values()):
        remaining = {face: ids for face, ids in pools.items() if ids}
        raise StateMigrationError(f"legacy state does not account for all 108 tiles: {remaining}")

    out_players: list[dict[str, Any]] = []
    for player in players:
        seat = int(player["seat"])
        converted = {key: value for key, value in player.items() if key not in {"hand", "melds", "discard_pile"}}
        converted["concealed_tile_ids"] = player_hand_ids[seat]
        converted["melds"] = melds_by_seat[seat]
        converted["discards"] = [
            discard_assignment[(seat, index)]
            for index, _face in enumerate(player.get("discard_pile") or [])
        ]
        out_players.append(converted)

    converted_state = {key: value for key, value in data.items() if key not in {"wall", "players", "pending_exchange", "last_discard", "last_draw_tile"}}
    converted_state["schema_version"] = 5
    converted_state["wall_tile_ids"] = wall_ids
    converted_state["players"] = out_players

    # Legacy selections are face-only references to the hand. Resolve each
    # occurrence deterministically to the lowest still-unselected matching ID.
    pending: dict[str, list[int]] = {}
    for seat_key, faces in (data.get("pending_exchange") or {}).items():
        seat = int(seat_key)
        available = list(player_hand_ids[seat])
        chosen: list[int] = []
        for face_id in faces or []:
            tile_type = physical_id_for(parse_tile(str(face_id)), 0) // 4
            matches = [tile_id for tile_id in available if tile_id // 4 == tile_type]
            if not matches:
                raise StateMigrationError(f"pending exchange tile missing from seat {seat} hand")
            tile_id = min(matches)
            chosen.append(tile_id)
            available.remove(tile_id)
        pending[str(seat)] = chosen
    converted_state["pending_exchange_tile_ids"] = pending
    converted_state["transit_tile_ids"] = []
    converted_state["winning_tile_ids"] = []

    def face_reference_id(face_value: Any) -> int | None:
        if not face_value:
            return None
        face_id = str(face_value)
        references = [
            record["tile_id"]
            for record in discard_assignment.values()
            if record["tile_id"] // 4 == physical_id_for(parse_tile(face_id), 0) // 4
        ]
        if references:
            return max(references)
        all_owned = wall_ids + [tile for values in player_hand_ids.values() for tile in values]
        return min(tile for tile in all_owned if tile // 4 == physical_id_for(parse_tile(face_id), 0) // 4)

    converted_state["last_discard_tile_id"] = face_reference_id(data.get("last_discard"))
    converted_state["last_draw_tile_id"] = face_reference_id(data.get("last_draw_tile"))
    return converted_state
