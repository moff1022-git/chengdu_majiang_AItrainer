"""M02 — exchange-three and dingque opening phases."""

from __future__ import annotations

from collections import Counter

import pytest

from engine.config import EngineConfig
from engine.deal import create_dealt_game
from engine.exchange import (
    ExchangeError,
    destination_seat,
    pick_same_suit_triple,
    resolve_exchange_direction,
)
from engine.opening import (
    OpeningError,
    begin_exchange,
    get_opening_status,
    run_opening_with_choices,
    submit_dingque,
    submit_exchange,
)
from engine.state import GameState, state_from_json, state_to_json
from engine.tile import Suit, Tile, tiles_to_ids


def _exchanges_for_all(state) -> dict[int, list[Tile]]:
    return {p.seat: pick_same_suit_triple(p.hand) for p in state.players}


def _dingque_for_all(state) -> dict[int, Suit]:
    suits = [Suit.WAN, Suit.TONG, Suit.TIAO]
    return {p.seat: suits[p.seat % 3] for p in state.players}


def test_t01_begin_exchange() -> None:
    state = create_dealt_game("m02-begin", num_players=4)
    begin_exchange(state)
    assert state.phase == "exchange"
    assert state.exchange_dir_resolved in (
        "clockwise",
        "counterclockwise",
        "across",
    )
    st = get_opening_status(state)
    assert st["phase"] == "exchange"
    assert set(st["waiting_seats"]) == {0, 1, 2, 3}


def test_t02_auto_dice_mapping() -> None:
    state = create_dealt_game("m02-autodice", num_players=4)
    cfg = EngineConfig(num_players=4, exchange_dir="auto_dice")
    begin_exchange(state, cfg)
    r = state.dice.total % 3
    expected = {0: "clockwise", 1: "across", 2: "counterclockwise"}[r]
    assert state.exchange_dir_resolved == expected
    assert resolve_exchange_direction(state, cfg) == expected
    # Reproducible
    s2 = create_dealt_game("m02-autodice", num_players=4)
    begin_exchange(s2, cfg)
    assert s2.exchange_dir_resolved == state.exchange_dir_resolved


def test_t03_full_exchange_to_dingque() -> None:
    state = create_dealt_game("m02-full-ex", num_players=4)
    begin_exchange(state, EngineConfig(num_players=4, exchange_dir="clockwise"))
    for seat, tiles in _exchanges_for_all(state).items():
        submit_exchange(state, seat, tiles)
    assert state.phase == "dingque"
    for p in state.players:
        if p.is_dealer:
            assert len(p.hand) == 14
        else:
            assert len(p.hand) == 13
    assert len(state.wall) == 55


def test_t04_multiset_transfer() -> None:
    state = create_dealt_game("m02-transfer", num_players=4)
    cfg = EngineConfig(num_players=4, exchange_dir="clockwise")
    begin_exchange(state, cfg)
    offers = _exchanges_for_all(state)
    before = {p.seat: Counter(tiles_to_ids(p.hand)) for p in state.players}
    offer_c = {s: Counter(tiles_to_ids(t)) for s, t in offers.items()}

    for seat, tiles in offers.items():
        submit_exchange(state, seat, tiles)

    after = {p.seat: Counter(tiles_to_ids(p.hand)) for p in state.players}
    n = 4
    for seat in range(n):
        dest = destination_seat(seat, "clockwise", n)
        # seat lost offer, gained offers from (seat-1)
        src = (seat - 1) % n
        expected = before[seat] - offer_c[seat] + offer_c[src]
        assert after[seat] == expected
        assert dest == (seat + 1) % n


def test_t05_illegal_exchange() -> None:
    state = create_dealt_game("m02-illegal", num_players=4)
    begin_exchange(state)
    hand = state.players[0].hand
    # wrong count
    with pytest.raises((OpeningError, ExchangeError)):
        submit_exchange(state, 0, hand[:2])
    # mixed suits if possible
    mixed = []
    seen = set()
    for t in hand:
        if t.suit not in seen:
            mixed.append(t)
            seen.add(t.suit)
        if len(mixed) == 3:
            break
    if len(mixed) == 3 and len({t.suit for t in mixed}) > 1:
        with pytest.raises((OpeningError, ExchangeError)):
            submit_exchange(state, 0, mixed)
    # not in hand
    fake = [Tile(Suit.WAN, 1), Tile(Suit.WAN, 1), Tile(Suit.WAN, 1)]
    # may or may not be in hand; force impossible
    with pytest.raises((OpeningError, ExchangeError)):
        submit_exchange(
            state,
            0,
            [Tile(Suit.WAN, 9), Tile(Suit.WAN, 9), Tile(Suit.WAN, 9)]
            if Counter(tiles_to_ids(hand))["wan_9"] < 3
            else [Tile(Suit.TIAO, 9), Tile(Suit.TIAO, 9), Tile(Suit.TIAO, 9)],
        )
    assert state.phase == "exchange"
    assert 0 not in (state.pending_exchange or {})


def test_t06_overwrite_pending() -> None:
    state = create_dealt_game("m02-overwrite", num_players=2)
    begin_exchange(state, EngineConfig(num_players=2, exchange_dir="across"))
    p0 = next(p for p in state.players if p.seat == 0)
    first = pick_same_suit_triple(p0.hand)
    submit_exchange(state, 0, first)
    # still exchange (seat 1 not done)
    assert state.phase == "exchange"
    # pick again (may be same)
    second = pick_same_suit_triple(p0.hand)
    submit_exchange(state, 0, second)
    assert tiles_to_ids((state.pending_exchange or {})[0]) == tiles_to_ids(second)


def test_t07_fixed_clockwise() -> None:
    state = create_dealt_game("m02-cw", num_players=4)
    begin_exchange(state, EngineConfig(num_players=4, exchange_dir="clockwise"))
    assert state.exchange_dir_resolved == "clockwise"
    offers = _exchanges_for_all(state)
    for s, t in offers.items():
        submit_exchange(state, s, t)
    # log destinations
    for entry in state.exchange_log:
        assert entry["to_seat"] == (entry["from_seat"] + 1) % 4


def test_t08_dingque_to_ready() -> None:
    state = create_dealt_game("m02-dq2", num_players=4)
    ex = _exchanges_for_all(state)
    dq = _dingque_for_all(state)
    run_opening_with_choices(
        state,
        ex,
        dq,
        EngineConfig(num_players=4, exchange_dir="clockwise"),
    )
    assert state.phase == "ready"
    assert state.current_seat == state.dealer_seat
    assert all(p.dingque is not None for p in state.players)


def test_t09_dingque_overwrite() -> None:
    state = create_dealt_game("m02-dq-ow", num_players=2)
    ex = _exchanges_for_all(state)
    begin_exchange(state, EngineConfig(num_players=2, exchange_dir="clockwise"))
    for s, t in ex.items():
        submit_exchange(state, s, t)
    assert state.phase == "dingque"
    submit_dingque(state, 0, Suit.WAN)
    submit_dingque(state, 0, Suit.TONG)
    assert next(p for p in state.players if p.seat == 0).dingque == Suit.TONG
    assert state.phase == "dingque"
    submit_dingque(state, 1, Suit.TIAO)
    assert state.phase == "ready"


def test_t10_e2e_serde() -> None:
    state = create_dealt_game("m02-serde", num_players=3)
    ex = _exchanges_for_all(state)
    dq = _dingque_for_all(state)
    run_opening_with_choices(
        state, ex, dq, EngineConfig(num_players=3, exchange_dir="auto_dice")
    )
    restored = state_from_json(state_to_json(state))
    assert state.semantic_equal(restored)
    assert restored.schema_version >= 2


@pytest.mark.parametrize("n", [2, 3, 4])
def test_t11_player_counts(n: int) -> None:
    state = create_dealt_game(f"m02-n{n}", num_players=n)
    ex = _exchanges_for_all(state)
    dq = _dingque_for_all(state)
    run_opening_with_choices(
        state, ex, dq, EngineConfig(num_players=n, exchange_dir="across")
    )
    assert state.phase == "ready"
    total = len(state.wall) + sum(len(p.hand) for p in state.players)
    assert total == 108


def test_t12_v1_dealt_readable() -> None:
    state = create_dealt_game("m02-v1", num_players=4)
    data = state.to_dict()
    # Simulate legacy v1 snapshot (no opening fields)
    data["schema_version"] = 1
    for k in (
        "current_seat",
        "exchange_dir_resolved",
        "pending_exchange",
        "exchange_log",
    ):
        data.pop(k, None)
    restored = GameState.from_dict(data, strict=True)
    assert restored.phase == "dealt"
    assert restored.schema_version >= 2  # upgraded on load to current


def test_wrong_phase_ops() -> None:
    state = create_dealt_game("m02-phase", num_players=2)
    with pytest.raises(OpeningError):
        submit_exchange(state, 0, pick_same_suit_triple(state.players[0].hand))
    begin_exchange(state)
    with pytest.raises(OpeningError):
        submit_dingque(state, 0, Suit.WAN)
