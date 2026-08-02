from __future__ import annotations

import pytest

from engine.deck import build_full_wall, shuffle_wall
from engine.physical_tile import face_from_physical_id, physical_id_for, physical_tile


def test_physical_id_face_roundtrip_and_boundaries() -> None:
    for tile_id in range(108):
        tile = physical_tile(tile_id)
        assert physical_id_for(tile.face, tile.copy_index) == tile_id
        assert face_from_physical_id(tile_id) == tile.face
    for bad in (-1, 108, True, "1"):
        with pytest.raises(ValueError):
            physical_tile(bad)  # type: ignore[arg-type]


def test_full_wall_has_108_unique_ids_and_four_per_face() -> None:
    wall = build_full_wall()
    assert len(wall) == 108
    assert {tile.tile_id for tile in wall} == set(range(108))
    counts: dict[str, int] = {}
    for tile in wall:
        counts[tile.face_id] = counts.get(tile.face_id, 0) + 1
    assert len(counts) == 27
    assert set(counts.values()) == {4}


def test_shuffle_is_reproducible_without_changing_face_baseline() -> None:
    first = shuffle_wall(build_full_wall(), 42)
    second = shuffle_wall(build_full_wall(), 42)
    assert [tile.tile_id for tile in first] == [tile.tile_id for tile in second]
    assert [tile.id for tile in first] == [tile.id for tile in second]
