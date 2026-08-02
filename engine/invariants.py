"""Lightweight event-boundary invariants for physical schema 5."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engine.physical_tile import PHYSICAL_TILE_COUNT


@dataclass(frozen=True, slots=True)
class InvariantViolation(ValueError):
    code: str
    event_type: str
    event_index: int
    details: dict[str, Any]

    def __str__(self) -> str:
        return f"{self.code} after {self.event_type}@{self.event_index}: {self.details}"


def _fail(state, code: str, event_type: str, **details: Any) -> None:
    raise InvariantViolation(code, event_type, int(getattr(state, "turn_index", 0)), details)


def ownership_regions(state) -> dict[str, list[int]]:
    regions: dict[str, list[int]] = {
        "wall": [tile.tile_id for tile in state.wall],
        "transit": list(getattr(state, "transit_tile_ids", None) or []),
        "winning": list(getattr(state, "winning_tile_ids", None) or []),
    }
    for player in state.players:
        regions[f"seat{player.seat}.hand"] = [tile.tile_id for tile in player.hand]
        regions[f"seat{player.seat}.melds"] = [
            tile_id for meld in player.melds for tile_id in meld.tile_ids
        ]
        regions[f"seat{player.seat}.unclaimed_discards"] = [
            record.tile_id
            for record in player.discard_records
            if record.claimed_by is None
        ]
    return regions


def assert_event_boundary(state, *, event_type: str = "validate", legal_actions_by_seat=None) -> None:
    # Hot path: a fixed-size counter is substantially cheaper than materializing
    # region sets/dicts after every atomic action. Detailed regions are built only
    # on failure.
    counts = [0] * PHYSICAL_TILE_COUNT

    def add(tile_id: int, region: str) -> None:
        if not isinstance(tile_id, int) or isinstance(tile_id, bool) or not 0 <= tile_id < PHYSICAL_TILE_COUNT:
            _fail(state, "PHYSICAL_ID_RANGE", event_type, region=region, tile_id=tile_id)
        counts[tile_id] += 1

    for tile in state.wall:
        add(tile.tile_id, "wall")
    for tile_id in getattr(state, "transit_tile_ids", None) or ():
        add(tile_id, "transit")
    for tile_id in getattr(state, "winning_tile_ids", None) or ():
        add(tile_id, "winning")
    for player in state.players:
        for tile in player.hand:
            add(tile.tile_id, "hand")
        for meld in player.melds:
            for tile_id in meld.tile_ids:
                add(tile_id, "meld")
        for record in player.discard_records:
            if record.claimed_by is None:
                add(record.tile_id, "discard")
    bad = [tile_id for tile_id, count in enumerate(counts) if count != 1]
    if bad:
        regions = ownership_regions(state)
        owners = {
            tile_id: [name for name, values in regions.items() if tile_id in values]
            for tile_id in bad
        }
        duplicates = {tile_id: names for tile_id, names in owners.items() if len(names) > 1}
        if duplicates:
            _fail(state, "OWNERSHIP_DUPLICATE", event_type, duplicates=duplicates)
        _fail(state, "OWNERSHIP_COVERAGE", event_type, missing=[tile_id for tile_id in bad if not owners[tile_id]], extra=[])

    for player in state.players:
        if len(player.discard_pile) != len(player.discard_records):
            _fail(state, "DISCARD_HISTORY_LENGTH", event_type, seat=player.seat)
        for tile, record in zip(player.discard_pile, player.discard_records):
            if tile.tile_id != record.tile_id or record.seat != player.seat:
                _fail(state, "DISCARD_REFERENCE", event_type, seat=player.seat)
        for meld in player.melds:
            if len(meld.tile_ids) not in {3, 4}:
                _fail(state, "MELD_INVALID", event_type, seat=player.seat, kind=meld.kind)

    for name in ("last_discard", "last_draw_tile"):
        tile = getattr(state, name, None)
        if tile is not None and counts[tile.tile_id] != 1:
            _fail(state, "REFERENCE_DANGLING", event_type, field=name, tile_id=tile.tile_id)
    for seat, selections in (state.pending_exchange or {}).items():
        hand_ids = {tile.tile_id for tile in state.players[seat].hand}
        selected = [tile.tile_id for tile in selections]
        if len(selected) != len(set(selected)) or not set(selected).issubset(hand_ids):
            _fail(state, "PENDING_EXCHANGE_REFERENCE", event_type, seat=seat, selected=selected)

    for event in state.score_events or []:
        transfers = event.get("transfers") if isinstance(event, dict) else None
        if not transfers:
            continue
        delta = 0
        for transfer in transfers:
            amount = int(transfer.get("amount", 0))
            delta += amount
            delta -= amount
        if delta != 0 and not event.get("non_zero_sum"):
            _fail(state, "SCORE_NOT_ZERO_SUM", event_type, delta=delta)

    if legal_actions_by_seat is not None:
        for seat, actions in legal_actions_by_seat.items():
            hand_faces = {tile.id for tile in state.players[seat].hand}
            for action in actions:
                if action.tiles and action.type.value in {"discard", "gang_an", "gang_jia"}:
                    if any(tile.id not in hand_faces for tile in action.tiles):
                        _fail(state, "LEGAL_ACTION_OWNERSHIP", event_type, seat=seat, action=str(action))
