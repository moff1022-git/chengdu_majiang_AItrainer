"""T03–T06, T10, T11 — seeds, dice, deal reproducibility."""

from __future__ import annotations

from engine.deal import create_dealt_game
from engine.dice import roll_dice
from engine.game_id import derive_seeds, generate_game_id, normalize_game_id
from engine.tile import tiles_to_ids
import pytest


def test_t03_same_game_id_same_seeds() -> None:
    a = derive_seeds("demo")
    b = derive_seeds("demo")
    assert a == b
    assert a.master_seed == a.shuffle_seed
    assert a.dice_seed != a.shuffle_seed
    assert a.exchange_seed != a.shuffle_seed
    assert a.exchange_seed != a.dice_seed


def test_t04_different_game_id_different_master() -> None:
    a = derive_seeds("demo-a")
    b = derive_seeds("demo-b")
    assert a.master_seed != b.master_seed


def test_empty_game_id_raises() -> None:
    with pytest.raises(ValueError):
        normalize_game_id("")
    with pytest.raises(ValueError):
        normalize_game_id("   ")
    with pytest.raises(ValueError):
        derive_seeds("")


def test_t05_dice_ranges() -> None:
    seeds = derive_seeds("dice-range-demo")
    for n in (2, 3, 4):
        dice = roll_dice(seeds.dice_seed, n)
        assert 1 <= dice.d1 <= 6
        assert 1 <= dice.d2 <= 6
        assert dice.total == dice.d1 + dice.d2
        assert 0 <= dice.dealer_seat < n
        assert dice.dealer_seat == (dice.total - 1) % n


def test_t06_deal_reproducible() -> None:
    a = create_dealt_game("repro-001", num_players=4)
    b = create_dealt_game("repro-001", num_players=4)
    assert a.dice == b.dice
    assert a.dealer_seat == b.dealer_seat
    assert tiles_to_ids(a.wall) == tiles_to_ids(b.wall)
    for pa, pb in zip(a.players, b.players):
        assert tiles_to_ids(pa.hand) == tiles_to_ids(pb.hand)
        assert pa.is_dealer == pb.is_dealer


def test_t10_auto_game_id_and_reopen() -> None:
    first = create_dealt_game(None, num_players=4)
    assert first.game_id
    assert first.game_id.startswith("cmj-")
    second = create_dealt_game(first.game_id, num_players=4)
    assert first.semantic_equal(second)


def test_t11_exchange_seed_derived_and_distinct() -> None:
    s = derive_seeds("fixed-for-exchange")
    assert s.exchange_seed != s.shuffle_seed
    assert s.exchange_seed != s.dice_seed
    # Stable fixed value for documentation / regression
    assert s.exchange_seed == (
        s.master_seed ^ 0x5A5A5A5A5A5A5A5A
    ) & 0xFFFFFFFFFFFFFFFF


def test_generate_game_id_format() -> None:
    gid = generate_game_id()
    assert gid.startswith("cmj-")
    parts = gid.split("-")
    assert len(parts) == 3
