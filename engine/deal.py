"""One-shot dealt game creation from game_id."""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Any, Mapping

from engine.config import EngineConfig
from engine.deck import Deck, build_full_wall, deal_hands
from engine.dice import roll_dice
from engine.game_id import derive_seeds, generate_game_id, normalize_game_id
from engine.rng_v2 import RngV2Error, derive_coordinate_seed
from engine.audit import canonical_hash
from engine.state import GameState, PlayerState, config_snapshot
from engine.tile import sorted_tiles


def create_dealt_game(
    game_id: str | None = None,
    *,
    num_players: int = 4,
    initial_score: int = 0,
    config: EngineConfig | None = None,
    rng_version: int = 1,
) -> GameState:
    """
    Build a reproducible phase='dealt' GameState.

    If game_id is None, a new id is generated. Same game_id always yields
    the same dice, dealer, hands, and remaining wall.
    """
    if config is None:
        config = EngineConfig(num_players=num_players, initial_score=initial_score)
    else:
        # Explicit kwargs only apply when config is not passed; if both given,
        # prefer config object but allow validation.
        if num_players != 4 or initial_score != 0:
            # Keep simple: config object wins when provided.
            pass

    if game_id is None:
        gid = generate_game_id()
    else:
        gid = normalize_game_id(game_id)

    if rng_version == 1:
        seeds = derive_seeds(gid)
        master_seed, dice_seed, shuffle_seed = seeds.master_seed, seeds.dice_seed, seeds.shuffle_seed
    elif rng_version == 2:
        master_seed = derive_coordinate_seed(game_id=gid, stream_name="deal", consumer_kind="engine", consumer_id="game", event_id="master", sample_index=0).master_seed
        dice_seed = derive_coordinate_seed(game_id=gid, stream_name="dice", consumer_kind="engine", consumer_id="dealer", event_id="initial", sample_index=0).sample_seed
        shuffle_seed = derive_coordinate_seed(game_id=gid, stream_name="shuffle", consumer_kind="engine", consumer_id="wall", event_id="initial", sample_index=0).sample_seed
    else:
        raise ValueError("rng_version must be 1 or 2")
    dice = roll_dice(dice_seed, config.num_players)
    deck = Deck.create_shuffled(shuffle_seed)
    hands = deal_hands(
        deck,
        num_players=config.num_players,
        dealer_seat=dice.dealer_seat,
    )

    players: list[PlayerState] = []
    for seat in range(config.num_players):
        players.append(
            PlayerState(
                seat=seat,
                # 万→筒→条，点数升序（展示与引擎一致）
                hand=sorted_tiles(hands[seat]),
                score=config.initial_score,
                is_dealer=(seat == dice.dealer_seat),
            )
        )

    state = GameState(
        game_id=gid,
        master_seed=master_seed,
        phase="dealt",
        num_players=config.num_players,
        dice=dice,
        dealer_seat=dice.dealer_seat,
        wall=deck.remaining_tiles(),
        players=players,
        turn_index=0,
        config=config_snapshot(config),
        current_seat=None,
        exchange_dir_resolved=None,
        pending_exchange={},
        exchange_log=[],
    )
    state.validate()
    return state


@dataclass(frozen=True, slots=True)
class DealRequest:
    event_id: str
    expected_state_version: int
    game_id: str
    num_players: int = 4
    initial_score: int = 0
    rng_version: int = 2
    algorithm_version: int = 2
    record_format: str = "rng-v2-new-record"
    ruleset_hash: str = ""
    config_hash: str = ""


@dataclass(frozen=True, slots=True)
class FrozenDealResult:
    accepted: bool
    game_state: GameState | None
    error_code: str | None
    next_state_version: int
    audit_ref: str
    state_fingerprint: str | None = None
    conservation: Mapping[str, int] | None = None
    seed_trace_ref: str | None = None
    domain_trace_refs: Mapping[str, str] | None = None


class DealTransaction:
    """STATE-011 prepare/validate/commit facade around the legacy deal API."""

    def __init__(self, state_version: int = 0, *, wall_builder=build_full_wall, dealt_game_builder=create_dealt_game):
        self.state_version = state_version
        self._events: dict[str, tuple[str, FrozenDealResult]] = {}
        self._lock = RLock()
        self._wall_builder = wall_builder
        self._dealt_game_builder = dealt_game_builder
        self._fault_stage: str | None = None

    def inject_fault(self, stage: str) -> None:
        if stage not in {"shuffle", "deal", "conservation"}:
            raise ValueError("unknown deal fault stage")
        self._fault_stage = stage

    def execute(self, request: DealRequest, *, config: EngineConfig | None = None) -> FrozenDealResult:
        with self._lock:
            return self._execute_locked(request, config=config)

    def _execute_locked(self, request: DealRequest, *, config: EngineConfig | None = None) -> FrozenDealResult:
        try:
            payload = {
                "event_id": request.event_id, "expected_state_version": request.expected_state_version,
                "game_id": request.game_id, "num_players": request.num_players,
                "initial_score": request.initial_score, "rng_version": request.rng_version,
                "algorithm_version": request.algorithm_version, "record_format": request.record_format,
                "ruleset_hash": request.ruleset_hash, "config_hash": request.config_hash,
            }
            event_hash = canonical_hash(payload)
        except Exception:
            return self._reject("SCHEMA_INVALID", "invalid-request")
        old = self._events.get(request.event_id)
        if old:
            return old[1] if old[0] == event_hash else self._reject("SCHEMA_INVALID", event_hash)
        if not request.event_id or not request.game_id:
            return self._remember(request.event_id, event_hash, self._reject("SCHEMA_INVALID", event_hash))
        if request.expected_state_version != self.state_version:
            return self._remember(request.event_id, event_hash, self._reject("VERSION_CONFLICT", event_hash))
        if request.num_players not in (2, 3, 4):
            return self._remember(request.event_id, event_hash, self._reject("INVALID_PLAYER_COUNT", event_hash))
        if request.algorithm_version != request.rng_version or request.rng_version not in (1, 2):
            return self._remember(request.event_id, event_hash, self._reject("RNG_VERSION_UNKNOWN", event_hash))
        if request.rng_version == 1 and request.record_format != "legacy-pre-rng-version":
            return self._remember(request.event_id, event_hash, self._reject("SCHEMA_INVALID", event_hash))
        if request.rng_version == 2 and request.record_format != "rng-v2-new-record":
            return self._remember(request.event_id, event_hash, self._reject("SCHEMA_INVALID", event_hash))

        try:
            if self._fault_stage == "shuffle":
                raise RngV2Error("RNG_STREAM_MISSING", "injected shuffle failure")
            wall = self._wall_builder()
            ids = [tile.tile_id for tile in wall]
            if len(ids) != 108 or set(ids) != set(range(108)):
                return self._remember(request.event_id, event_hash, self._reject("DECK_DUPLICATE", event_hash))
            face_counts: dict[str, int] = {}
            for tile in wall:
                face_counts[tile.id] = face_counts.get(tile.id, 0) + 1
            if len(face_counts) != 27 or any(count != 4 for count in face_counts.values()):
                return self._remember(request.event_id, event_hash, self._reject("CONSERVATION_FAILED", event_hash))
            cfg = config or EngineConfig(num_players=request.num_players, initial_score=request.initial_score)
            if cfg.num_players != request.num_players:
                return self._remember(request.event_id, event_hash, self._reject("INVALID_PLAYER_COUNT", event_hash))
            # The legacy function builds only local working objects and returns
            # after GameState.validate, which is the transaction commit point.
            if self._fault_stage == "deal":
                return self._remember(request.event_id, event_hash, self._reject("DEAL_COUNT", event_hash))
            state = self._dealt_game_builder(request.game_id, config=cfg, rng_version=request.rng_version)
            all_ids = [tile.tile_id for tile in state.wall]
            for player in state.players:
                all_ids.extend(tile.tile_id for tile in player.hand)
            if self._fault_stage == "conservation":
                return self._remember(request.event_id, event_hash, self._reject("CONSERVATION_FAILED", event_hash))
            if len(all_ids) != 108 or len(set(all_ids)) != 108:
                return self._remember(request.event_id, event_hash, self._reject("CONSERVATION_FAILED", event_hash))
            expected_wall = 108 - (13 * request.num_players + 1)
            if len(state.wall) != expected_wall:
                return self._remember(request.event_id, event_hash, self._reject("DEAL_COUNT", event_hash))
            trace_ref = None
            domain_refs = None
            if request.rng_version == 2:
                domain_refs = {
                    "shuffle": str(derive_coordinate_seed(game_id=state.game_id, stream_name="shuffle", consumer_kind="engine", consumer_id="wall", event_id="initial", sample_index=0).strategy_ref()["trace_ref"]),
                    "dice": str(derive_coordinate_seed(game_id=state.game_id, stream_name="dice", consumer_kind="engine", consumer_id="dealer", event_id="initial", sample_index=0).strategy_ref()["trace_ref"]),
                    "exchange": str(derive_coordinate_seed(game_id=state.game_id, stream_name="exchange", consumer_kind="engine", consumer_id="opening", event_id="initial", sample_index=0).strategy_ref()["trace_ref"]),
                }
                trace_ref = domain_refs["shuffle"]
            fingerprint = canonical_hash(state.to_dict())
        except RngV2Error as exc:
            return self._remember(request.event_id, event_hash, self._reject(exc.code, event_hash))
        except ValueError:
            return self._remember(request.event_id, event_hash, self._reject("INVARIANT_FAILED", event_hash))

        next_version = self.state_version + 1
        audit = canonical_hash({"unit_id": "STATE-011", "event": event_hash, "version": next_version, "state": fingerprint})
        result = FrozenDealResult(True, state, None, next_version, audit, fingerprint, {"tiles": 108, "players": request.num_players, "wall": len(state.wall)}, trace_ref, domain_refs)
        self.state_version = next_version
        return self._remember(request.event_id, event_hash, result)

    def _reject(self, code: str, event_hash: str) -> FrozenDealResult:
        audit = canonical_hash({"unit_id": "STATE-011", "accepted": False, "error": code, "event": event_hash, "version": self.state_version})
        return FrozenDealResult(False, None, code, self.state_version, audit)

    def _remember(self, event_id: str, event_hash: str, result: FrozenDealResult) -> FrozenDealResult:
        if event_id:
            self._events[event_id] = (event_hash, result)
        return result
