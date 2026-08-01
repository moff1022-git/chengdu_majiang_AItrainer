"""T01, T02, T07 — tiles and wall dealing."""

from __future__ import annotations

from collections import Counter

import pytest

from engine.deal import create_dealt_game
from engine.deck import build_full_wall, shuffle_wall
from engine.tile import Suit, Tile, parse_tile


def test_t01_full_wall_108_and_four_of_each() -> None:
    wall = build_full_wall()
    assert len(wall) == 108
    counts = Counter(t.id for t in wall)
    assert len(counts) == 27
    assert all(v == 4 for v in counts.values())
    # Fixed build order: wan_1 x4 first
    assert wall[0] == Tile(Suit.WAN, 1)
    assert wall[3] == Tile(Suit.WAN, 1)
    assert wall[4] == Tile(Suit.WAN, 2)


def test_t02_tile_id_roundtrip_and_invalid() -> None:
    for suit in Suit:
        for rank in range(1, 10):
            t = Tile(suit, rank)
            assert parse_tile(t.id) == t
    with pytest.raises(ValueError):
        parse_tile("")
    with pytest.raises(ValueError):
        parse_tile("wind_1")
    with pytest.raises(ValueError):
        parse_tile("wan_0")
    with pytest.raises(ValueError):
        parse_tile("wan_10")
    with pytest.raises(ValueError):
        parse_tile("notile")


def test_shuffle_is_deterministic() -> None:
    a = shuffle_wall(build_full_wall(), 42)
    b = shuffle_wall(build_full_wall(), 42)
    c = shuffle_wall(build_full_wall(), 43)
    assert [t.id for t in a] == [t.id for t in b]
    assert [t.id for t in a] != [t.id for t in c]


@pytest.mark.parametrize("num_players,expected_wall", [(4, 55), (3, 68), (2, 81)])
def test_t07_hand_sizes_and_wall_remaining(
    num_players: int, expected_wall: int
) -> None:
    state = create_dealt_game("hand-size-demo", num_players=num_players)
    assert len(state.wall) == expected_wall
    dealers = [p for p in state.players if p.is_dealer]
    assert len(dealers) == 1
    assert len(dealers[0].hand) == 14
    for p in state.players:
        if not p.is_dealer:
            assert len(p.hand) == 13
    # Total tiles conserved
    total = len(state.wall) + sum(len(p.hand) for p in state.players)
    assert total == 108
