"""Opening phase state machine: exchange-three then dingque."""

from __future__ import annotations

from typing import Any

from engine.action import Action, ActionType
from engine.config import EngineConfig
from engine.exchange import (
    ExchangeError,
    destination_seat,
    remove_tiles_from_hand,
    resolve_exchange_direction,
    validate_exchange_tiles,
)
from engine.state import GameState
from engine.tile import Suit, Tile, tiles_to_ids


class OpeningError(ValueError):
    """Illegal opening-phase transition or submission."""


def _config_from_state(state: GameState, config: EngineConfig | None) -> EngineConfig:
    if config is not None:
        return config
    if state.config:
        try:
            return EngineConfig.from_dict(state.config)
        except ValueError:
            pass
    return EngineConfig(num_players=state.num_players)


def _player(state: GameState, seat: int):
    if not 0 <= seat < state.num_players:
        raise OpeningError(f"seat out of range: {seat}")
    for p in state.players:
        if p.seat == seat:
            return p
    raise OpeningError(f"missing player seat {seat}")


def begin_exchange(
    state: GameState, config: EngineConfig | None = None
) -> GameState:
    """dealt → exchange; resolve and store exchange direction (in-place)."""
    if state.phase != "dealt":
        raise OpeningError(f"begin_exchange requires phase=dealt, got {state.phase!r}")
    cfg = _config_from_state(state, config)
    if cfg.num_players != state.num_players:
        raise OpeningError("config.num_players does not match state")
    direction = resolve_exchange_direction(state, cfg)
    state.phase = "exchange"
    state.exchange_dir_resolved = direction
    state.pending_exchange = {}
    state.exchange_log = []
    state.current_seat = None
    state.schema_version = 2
    # keep config snapshot in sync with exchange_dir used
    snap = cfg.to_dict()
    state.config = snap
    state.validate()
    return state


def begin_dingque_skip_exchange(
    state: GameState, config: EngineConfig | None = None
) -> GameState:
    """dealt → dingque without 换三张 (enable_exchange=False)."""
    if state.phase != "dealt":
        raise OpeningError(
            f"begin_dingque_skip_exchange requires phase=dealt, got {state.phase!r}"
        )
    cfg = _config_from_state(state, config)
    if cfg.num_players != state.num_players:
        raise OpeningError("config.num_players does not match state")
    state.phase = "dingque"
    state.exchange_dir_resolved = None
    state.pending_exchange = {}
    state.exchange_log = []
    state.current_seat = None
    state.schema_version = 2
    state.config = cfg.to_dict()
    state.validate()
    return state


def begin_opening(
    state: GameState, config: EngineConfig | None = None
) -> GameState:
    """dealt → exchange or dingque depending on EngineConfig.enable_exchange."""
    cfg = _config_from_state(state, config)
    if cfg.enable_exchange:
        return begin_exchange(state, cfg)
    return begin_dingque_skip_exchange(state, cfg)


def _all_exchanges_submitted(state: GameState) -> bool:
    pe = state.pending_exchange or {}
    return all(seat in pe and pe[seat] is not None for seat in range(state.num_players))


def _resolve_exchange(state: GameState) -> None:
    """Apply pending exchanges atomically; phase → dingque."""
    if state.phase != "exchange":
        raise OpeningError("resolve only in exchange phase")
    if not _all_exchanges_submitted(state):
        raise OpeningError("not all seats have submitted exchange")
    direction = state.exchange_dir_resolved
    if direction is None:
        raise OpeningError("exchange_dir_resolved is missing")

    n = state.num_players
    pending = state.pending_exchange or {}
    offers: dict[int, list[Tile]] = {}
    for seat in range(n):
        tiles = pending[seat]
        assert tiles is not None
        player = _player(state, seat)
        validated = validate_exchange_tiles(player.hand, tiles)
        # re-check against current hand (pending was validated at submit)
        offers[seat] = validated

    # Remove all offers first
    new_hands: dict[int, list[Tile]] = {}
    for seat in range(n):
        player = _player(state, seat)
        new_hands[seat] = remove_tiles_from_hand(player.hand, offers[seat])

    log: list[dict[str, Any]] = []
    # Add offers to destinations
    for seat in range(n):
        dest = destination_seat(seat, direction, n)  # type: ignore[arg-type]
        new_hands[dest] = list(new_hands[dest]) + list(offers[seat])
        log.append(
            {
                "from_seat": seat,
                "to_seat": dest,
                "tiles": tiles_to_ids(offers[seat]),
            }
        )

    for seat in range(n):
        pl = _player(state, seat)
        pl.hand = new_hands[seat]
        pl.sort_hand_inplace()

    state.exchange_log = log
    state.pending_exchange = {}
    state.phase = "dingque"
    state.validate()


def submit_exchange(
    state: GameState, seat: int, tiles: list[Tile]
) -> GameState:
    """Record/overwrite pending exchange; auto-resolve when all submitted."""
    if state.phase != "exchange":
        raise OpeningError(
            f"submit_exchange requires phase=exchange, got {state.phase!r}"
        )
    player = _player(state, seat)
    validated = validate_exchange_tiles(player.hand, tiles)
    if state.pending_exchange is None:
        state.pending_exchange = {}
    state.pending_exchange[seat] = list(validated)

    if _all_exchanges_submitted(state):
        _resolve_exchange(state)
    return state


def submit_dingque(state: GameState, seat: int, suit: Suit) -> GameState:
    """Set/overwrite dingque; when all set → ready."""
    if state.phase != "dingque":
        raise OpeningError(
            f"submit_dingque requires phase=dingque, got {state.phase!r}"
        )
    if not isinstance(suit, Suit):
        try:
            suit = Suit(suit)  # type: ignore[arg-type]
        except (TypeError, ValueError) as e:
            raise OpeningError(f"invalid dingque suit: {suit!r}") from e
    player = _player(state, seat)
    player.dingque = suit

    if all(p.dingque is not None for p in state.players):
        state.phase = "ready"
        state.current_seat = state.dealer_seat
        state.validate()
    return state


def get_opening_status(state: GameState) -> dict[str, Any]:
    waiting: list[int] = []
    if state.phase == "exchange":
        pe = state.pending_exchange or {}
        waiting = [s for s in range(state.num_players) if s not in pe]
    elif state.phase == "dingque":
        waiting = [p.seat for p in state.players if p.dingque is None]
    return {
        "phase": state.phase,
        "waiting_seats": waiting,
        "exchange_dir": state.exchange_dir_resolved,
        "current_seat": state.current_seat,
        "dealer_seat": state.dealer_seat,
    }


def validate_exchange_action(state: GameState, seat: int, action: Action) -> None:
    if action.type != ActionType.EXCHANGE:
        raise OpeningError(f"expected EXCHANGE, got {action.type}")
    if state.phase != "exchange":
        raise OpeningError("not in exchange phase")
    validate_exchange_tiles(_player(state, seat).hand, list(action.tiles))


def validate_dingque_action(state: GameState, seat: int, action: Action) -> None:
    if action.type != ActionType.DINGQUE:
        raise OpeningError(f"expected DINGQUE, got {action.type}")
    if state.phase != "dingque":
        raise OpeningError("not in dingque phase")
    if action.suit is None:
        raise OpeningError("dingque action requires suit")
    Suit(action.suit)  # validate
    _player(state, seat)  # seat exists


def run_opening_with_choices(
    state: GameState,
    exchanges: dict[int, list[Tile]],
    dingque: dict[int, Suit],
    config: EngineConfig | None = None,
) -> GameState:
    """dealt → (optional exchange) → dingque → ready using provided choices."""
    if state.phase != "dealt":
        raise OpeningError(f"run_opening requires phase=dealt, got {state.phase!r}")
    cfg = _config_from_state(state, config)
    begin_opening(state, cfg)
    if state.phase == "exchange":
        for seat in range(state.num_players):
            if seat not in exchanges:
                raise OpeningError(f"missing exchange for seat {seat}")
            submit_exchange(state, seat, exchanges[seat])
        if state.phase != "dingque":
            raise OpeningError(f"expected dingque after exchanges, got {state.phase!r}")
    elif state.phase != "dingque":
        raise OpeningError(f"expected dingque after begin_opening, got {state.phase!r}")
    for seat in range(state.num_players):
        if seat not in dingque:
            raise OpeningError(f"missing dingque for seat {seat}")
        submit_dingque(state, seat, dingque[seat])
    if state.phase != "ready":
        raise OpeningError(f"expected ready after dingque, got {state.phase!r}")
    return state


# Re-export exchange errors used by callers
__all__ = [
    "OpeningError",
    "ExchangeError",
    "begin_exchange",
    "begin_dingque_skip_exchange",
    "begin_opening",
    "submit_exchange",
    "submit_dingque",
    "get_opening_status",
    "validate_exchange_action",
    "validate_dingque_action",
    "run_opening_with_choices",
]
