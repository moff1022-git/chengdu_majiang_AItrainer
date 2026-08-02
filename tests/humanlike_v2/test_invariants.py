from __future__ import annotations

import pytest

from engine.invariants import InvariantViolation, assert_event_boundary, ownership_regions
from engine.session import build_ready_game


@pytest.mark.parametrize("players", [2, 3, 4])
def test_ready_state_owns_every_physical_tile_once(players: int) -> None:
    state = build_ready_game(f"invariant-{players}", num_players=players)
    regions = ownership_regions(state)
    flat = [tile_id for values in regions.values() for tile_id in values]
    assert len(flat) == 108
    assert set(flat) == set(range(108))
    assert_event_boundary(state, event_type="test")


def test_duplicate_ownership_reports_structured_failure() -> None:
    state = build_ready_game("invariant-duplicate", num_players=4)
    state.players[0].hand.append(state.wall[0])
    with pytest.raises(InvariantViolation) as captured:
        assert_event_boundary(state, event_type="corrupt")
    assert captured.value.code == "OWNERSHIP_DUPLICATE"
    assert captured.value.event_type == "corrupt"
