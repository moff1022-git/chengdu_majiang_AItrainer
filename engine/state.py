"""Serializable game state snapshot."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Optional

from engine.action import Action
from engine.config import EngineConfig
from engine.dice import DiceResult
from engine.tile import Suit, Tile, ids_to_tiles, parse_tile, sorted_tiles, tiles_to_ids

SCHEMA_VERSION = 4
SUPPORTED_SCHEMA_VERSIONS = frozenset({1, 2, 3, 4})

_OPENING_HAND_PHASES = frozenset({"dealt", "exchange", "dingque", "ready"})
_PLAY_PHASES = frozenset({"draw", "discard", "response", "finished"})


@dataclass
class PlayerState:
    seat: int
    hand: list[Tile]
    score: int = 0
    is_dealer: bool = False
    dingque: Optional[Suit] = None
    melds: list[Any] = field(default_factory=list)
    discard_pile: list[Tile] = field(default_factory=list)
    status: str = "active"
    hu_order: int | None = None
    last_win: dict | None = None

    def sorted_hand(self) -> list[Tile]:
        """万 → 筒 → 条，同花色点数 1→9。"""
        return sorted_tiles(self.hand)

    def sort_hand_inplace(self) -> None:
        """Keep engine hand in display order (wan/tong/tiao, rank asc)."""
        self.hand = sorted_tiles(self.hand)

    def to_dict(self) -> dict:
        return {
            "seat": self.seat,
            # Always export sorted — UI / wire / logs consistent
            "hand": tiles_to_ids(sorted_tiles(self.hand)),
            "score": self.score,
            "is_dealer": self.is_dealer,
            "dingque": self.dingque.value if self.dingque else None,
            "melds": list(self.melds),
            "discard_pile": tiles_to_ids(self.discard_pile),
            "status": self.status,
            "hu_order": self.hu_order,
            "last_win": self.last_win,
        }

    @classmethod
    def from_dict(cls, data: dict) -> PlayerState:
        try:
            seat = int(data["seat"])
            hand = ids_to_tiles(data["hand"])
            score = int(data.get("score", 0))
            is_dealer = bool(data.get("is_dealer", False))
            dingque_raw = data.get("dingque")
            dingque = Suit(dingque_raw) if dingque_raw else None
            melds = list(data.get("melds") or [])
            discard_pile = ids_to_tiles(data.get("discard_pile") or [])
            status = str(data.get("status", "active"))
            hu_order = data.get("hu_order")
            hu_order = int(hu_order) if hu_order is not None else None
            last_win = data.get("last_win")
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"invalid player state: {data!r}") from e
        return cls(
            seat=seat,
            hand=hand,
            score=score,
            is_dealer=is_dealer,
            dingque=dingque,
            melds=melds,
            discard_pile=discard_pile,
            status=status,
            hu_order=hu_order,
            last_win=last_win,
        )


def _pending_to_json(
    pending: dict[int, list[Tile]] | None,
) -> dict[str, list[str]] | None:
    if pending is None:
        return None
    out: dict[str, list[str]] = {}
    for seat, tiles in pending.items():
        if tiles is None:
            continue
        out[str(seat)] = tiles_to_ids(tiles)
    return out


def _pending_from_json(raw: dict | None) -> dict[int, list[Tile]]:
    if not raw:
        return {}
    out: dict[int, list[Tile]] = {}
    for k, v in raw.items():
        seat = int(k)
        out[seat] = ids_to_tiles(v)
    return out


def _claims_to_json(
    claims: dict[int, Action] | None,
) -> dict[str, dict] | None:
    if not claims:
        return None
    return {str(k): v.to_dict() for k, v in claims.items()}


def _claims_from_json(raw: dict | None) -> dict[int, Action]:
    if not raw:
        return {}
    return {int(k): Action.from_dict(v) for k, v in raw.items()}


@dataclass
class GameState:
    game_id: str
    master_seed: int
    phase: str
    num_players: int
    dice: DiceResult
    dealer_seat: int
    wall: list[Tile]
    players: list[PlayerState]
    turn_index: int = 0
    config: dict = field(default_factory=dict)
    schema_version: int = SCHEMA_VERSION
    current_seat: int | None = None
    exchange_dir_resolved: str | None = None
    pending_exchange: dict[int, list[Tile]] | None = field(default_factory=dict)
    exchange_log: list[dict[str, Any]] = field(default_factory=list)
    # M04 play fields
    last_discard: Tile | None = None
    last_discard_seat: int | None = None
    response_seats: list[int] = field(default_factory=list)
    pending_claims: dict[int, Action] = field(default_factory=dict)
    last_draw_tile: Tile | None = None
    after_gang_draw: bool = False
    qiang_gang_context: dict | None = None
    finished_reason: str | None = None
    score_events: list[dict] = field(default_factory=list)
    hu_sequence: list[dict] = field(default_factory=list)
    hu_count: int = 0
    end_settled: bool = False
    settle_tags: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "schema_version": SCHEMA_VERSION,
            "game_id": self.game_id,
            "master_seed": self.master_seed,
            "phase": self.phase,
            "num_players": self.num_players,
            "dice": {
                "d1": self.dice.d1,
                "d2": self.dice.d2,
                "total": self.dice.total,
            },
            "dealer_seat": self.dealer_seat,
            "wall": tiles_to_ids(self.wall),
            "players": [p.to_dict() for p in self.players],
            "turn_index": self.turn_index,
            "config": dict(self.config),
            "current_seat": self.current_seat,
            "exchange_dir_resolved": self.exchange_dir_resolved,
            "pending_exchange": _pending_to_json(self.pending_exchange),
            "exchange_log": list(self.exchange_log),
            "last_discard": self.last_discard.id if self.last_discard else None,
            "last_discard_seat": self.last_discard_seat,
            "response_seats": list(self.response_seats or []),
            "pending_claims": _claims_to_json(self.pending_claims),
            "last_draw_tile": self.last_draw_tile.id if self.last_draw_tile else None,
            "after_gang_draw": self.after_gang_draw,
            "qiang_gang_context": self.qiang_gang_context,
            "finished_reason": self.finished_reason,
            "score_events": list(self.score_events or []),
            "hu_sequence": list(self.hu_sequence or []),
            "hu_count": self.hu_count,
            "end_settled": self.end_settled,
            "settle_tags": dict(self.settle_tags or {}),
        }

    @classmethod
    def from_dict(cls, data: dict, *, strict: bool = True) -> GameState:
        if not isinstance(data, dict):
            raise ValueError("state must be a dict")
        try:
            schema_version = int(data["schema_version"])
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError("missing or invalid schema_version") from e
        if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
            raise ValueError(
                f"unsupported schema_version: {schema_version} "
                f"(supported {sorted(SUPPORTED_SCHEMA_VERSIONS)})"
            )

        required = (
            "game_id",
            "master_seed",
            "phase",
            "num_players",
            "dice",
            "dealer_seat",
            "wall",
            "players",
        )
        for key in required:
            if key not in data:
                raise ValueError(f"missing field: {key}")

        try:
            game_id = str(data["game_id"])
            master_seed = int(data["master_seed"])
            phase = str(data["phase"])
            num_players = int(data["num_players"])
            dealer_seat = int(data["dealer_seat"])
            wall = ids_to_tiles(data["wall"])
            players_raw = data["players"]
            turn_index = int(data.get("turn_index", 0))
            config = dict(data.get("config") or {})
            dice_raw = dict(data["dice"])
            current_seat_raw = data.get("current_seat", None)
            current_seat = (
                int(current_seat_raw) if current_seat_raw is not None else None
            )
            exchange_dir_resolved = data.get("exchange_dir_resolved")
            if exchange_dir_resolved is not None:
                exchange_dir_resolved = str(exchange_dir_resolved)
            pending_exchange = _pending_from_json(data.get("pending_exchange"))
            exchange_log = list(data.get("exchange_log") or [])
            ld = data.get("last_discard")
            last_discard = parse_tile(ld) if ld else None
            last_discard_seat = data.get("last_discard_seat")
            last_discard_seat = (
                int(last_discard_seat) if last_discard_seat is not None else None
            )
            response_seats = [int(x) for x in (data.get("response_seats") or [])]
            pending_claims = _claims_from_json(data.get("pending_claims"))
            ldt = data.get("last_draw_tile")
            last_draw_tile = parse_tile(ldt) if ldt else None
            after_gang_draw = bool(data.get("after_gang_draw", False))
            qiang_gang_context = data.get("qiang_gang_context")
            finished_reason = data.get("finished_reason")
            score_events = list(data.get("score_events") or [])
            hu_sequence = list(data.get("hu_sequence") or [])
            hu_count = int(data.get("hu_count", 0))
            end_settled = bool(data.get("end_settled", False))
            settle_tags = dict(data.get("settle_tags") or {})
        except (TypeError, ValueError) as e:
            raise ValueError(f"invalid state fields: {e}") from e

        if "dealer_seat" not in dice_raw:
            dice_raw["dealer_seat"] = dealer_seat
        dice = DiceResult.from_dict(dice_raw)

        if not isinstance(players_raw, list) or len(players_raw) != num_players:
            raise ValueError(
                f"players length "
                f"{len(players_raw) if isinstance(players_raw, list) else '?'} "
                f"!= num_players {num_players}"
            )
        players = [PlayerState.from_dict(p) for p in players_raw]
        players.sort(key=lambda p: p.seat)

        state = cls(
            game_id=game_id,
            master_seed=master_seed,
            phase=phase,
            num_players=num_players,
            dice=dice,
            dealer_seat=dealer_seat,
            wall=wall,
            players=players,
            turn_index=turn_index,
            config=config,
            schema_version=SCHEMA_VERSION,
            current_seat=current_seat,
            exchange_dir_resolved=exchange_dir_resolved,
            pending_exchange=pending_exchange,
            exchange_log=exchange_log,
            last_discard=last_discard,
            last_discard_seat=last_discard_seat,
            response_seats=response_seats,
            pending_claims=pending_claims,
            last_draw_tile=last_draw_tile,
            after_gang_draw=after_gang_draw,
            qiang_gang_context=qiang_gang_context,
            finished_reason=finished_reason,
            score_events=score_events,
            hu_sequence=hu_sequence,
            hu_count=hu_count,
            end_settled=end_settled,
            settle_tags=settle_tags,
        )
        if strict:
            state.validate()
        return state

    def validate(self) -> None:
        if self.num_players not in (2, 3, 4):
            raise ValueError(f"invalid num_players: {self.num_players}")
        if len(self.players) != self.num_players:
            raise ValueError("players count mismatch")
        if self.dealer_seat != self.dice.dealer_seat:
            raise ValueError("dealer_seat does not match dice.dealer_seat")
        if not 0 <= self.dealer_seat < self.num_players:
            raise ValueError("dealer_seat out of range")

        expected_wall = 108 - (13 * self.num_players + 1)
        if self.phase in _OPENING_HAND_PHASES and len(self.wall) != expected_wall:
            raise ValueError(
                f"wall length {len(self.wall)} != expected {expected_wall} "
                f"for phase={self.phase}"
            )

        dealer_count = 0
        for p in self.players:
            if p.seat < 0 or p.seat >= self.num_players:
                raise ValueError(f"invalid seat: {p.seat}")
            if p.is_dealer:
                dealer_count += 1
                if p.seat != self.dealer_seat:
                    raise ValueError("is_dealer seat mismatch")
                if self.phase in _OPENING_HAND_PHASES and len(p.hand) != 14:
                    raise ValueError(f"dealer hand size {len(p.hand)} != 14")
            elif self.phase in _OPENING_HAND_PHASES and len(p.hand) != 13:
                raise ValueError(
                    f"non-dealer seat {p.seat} hand size {len(p.hand)} != 13"
                )

            if self.phase == "ready" and p.dingque is None:
                raise ValueError(f"ready requires dingque for seat {p.seat}")

        if dealer_count != 1:
            raise ValueError(f"expected exactly one dealer, got {dealer_count}")

        if self.phase == "ready":
            if self.current_seat != self.dealer_seat:
                raise ValueError(
                    f"ready current_seat {self.current_seat} != dealer {self.dealer_seat}"
                )

        if self.phase == "exchange" and self.exchange_dir_resolved is None:
            raise ValueError("exchange phase requires exchange_dir_resolved")

        # play phases: basic seat checks only
        if self.phase in _PLAY_PHASES and self.phase != "finished":
            if self.current_seat is not None and not (
                0 <= self.current_seat < self.num_players
            ):
                raise ValueError("current_seat out of range")

    def semantic_equal(self, other: GameState) -> bool:
        if self.game_id != other.game_id:
            return False
        if self.master_seed != other.master_seed:
            return False
        if self.phase != other.phase:
            return False
        if self.num_players != other.num_players:
            return False
        if self.dealer_seat != other.dealer_seat:
            return False
        if self.dice != other.dice:
            return False
        if self.turn_index != other.turn_index:
            return False
        if self.config != other.config:
            return False
        if self.current_seat != other.current_seat:
            return False
        if self.exchange_dir_resolved != other.exchange_dir_resolved:
            return False
        if tiles_to_ids(self.wall) != tiles_to_ids(other.wall):
            return False
        if (self.exchange_log or []) != (other.exchange_log or []):
            return False
        pe_a = self.pending_exchange or {}
        pe_b = other.pending_exchange or {}
        if set(pe_a.keys()) != set(pe_b.keys()):
            return False
        for k in pe_a:
            if tiles_to_ids(pe_a[k]) != tiles_to_ids(pe_b[k]):
                return False
        if len(self.players) != len(other.players):
            return False
        for a, b in zip(self.players, other.players):
            if a.seat != b.seat or a.score != b.score or a.is_dealer != b.is_dealer:
                return False
            if a.status != b.status:
                return False
            if tiles_to_ids(a.hand) != tiles_to_ids(b.hand):
                return False
            if tiles_to_ids(a.discard_pile) != tiles_to_ids(b.discard_pile):
                return False
            if a.dingque != b.dingque or a.melds != b.melds:
                return False
        return True


def state_to_json(state: GameState) -> str:
    return json.dumps(state.to_dict(), ensure_ascii=False, separators=(",", ":"))


def state_from_json(text: str, *, strict: bool = True) -> GameState:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid json: {e}") from e
    return GameState.from_dict(data, strict=strict)


def config_snapshot(config: EngineConfig) -> dict:
    return config.to_dict()
