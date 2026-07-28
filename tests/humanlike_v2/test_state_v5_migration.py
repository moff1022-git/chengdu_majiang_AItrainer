from __future__ import annotations

import copy

import pytest

from engine.deal import create_dealt_game
from engine.state import GameState
from engine.state_migrations import migrate_state_to_v5


def _legacy_dealt(version: int = 4) -> dict:
    state = create_dealt_game("legacy-v4", num_players=4)
    current = state.to_dict()
    return {
        **{key: value for key, value in current.items() if key not in {"wall_tile_ids", "players", "pending_exchange_tile_ids", "last_discard_tile_id", "last_draw_tile_id", "transit_tile_ids", "winning_tile_ids"}},
        "schema_version": version,
        "wall": [tile.id for tile in state.wall],
        "players": [
            {
                **{key: value for key, value in player.to_dict().items() if key not in {"concealed_tile_ids", "melds", "discards"}},
                "hand": [tile.id for tile in player.hand],
                "melds": [],
                "discard_pile": [],
            }
            for player in state.players
        ],
        "pending_exchange": {},
        "last_discard": None,
        "last_draw_tile": None,
    }


@pytest.mark.parametrize("version", [1, 2, 3, 4])
def test_legacy_migration_is_deterministic_and_non_mutating(version: int) -> None:
    legacy = _legacy_dealt(version)
    before = copy.deepcopy(legacy)
    first = migrate_state_to_v5(legacy)
    second = migrate_state_to_v5(legacy)
    assert legacy == before
    assert first == second
    assert first["schema_version"] == 5
    assert set(first["wall_tile_ids"]) | {
        tile_id
        for player in first["players"]
        for tile_id in player["concealed_tile_ids"]
    } == set(range(108))
    restored = GameState.from_dict(legacy)
    assert restored.schema_version == 5


def test_bad_legacy_state_fails_instead_of_guessing() -> None:
    legacy = _legacy_dealt()
    legacy["players"][0]["hand"].append(legacy["players"][0]["hand"][0])
    with pytest.raises(ValueError, match="migration failed"):
        GameState.from_dict(legacy)
