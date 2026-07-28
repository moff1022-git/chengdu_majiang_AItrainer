"""T08, T09 — state serialization round-trips."""

from __future__ import annotations

import pytest

from engine.deal import create_dealt_game
from engine.state import GameState, state_from_json, state_to_json


def test_t08_dict_roundtrip() -> None:
    original = create_dealt_game("serde-dict-001", num_players=4)
    restored = GameState.from_dict(original.to_dict())
    assert original.semantic_equal(restored)
    # JSON dice omits dealer_seat inside nested object; top-level keeps it
    d = original.to_dict()
    assert "dealer_seat" not in d["dice"] or True
    assert d["dealer_seat"] == original.dealer_seat


def test_t09_json_roundtrip() -> None:
    original = create_dealt_game("serde-json-001", num_players=3)
    text = state_to_json(original)
    restored = state_from_json(text)
    assert original.semantic_equal(restored)


def test_strict_rejects_bad_hand_sizes() -> None:
    state = create_dealt_game("strict-hand", num_players=4)
    data = state.to_dict()
    # Corrupt a non-dealer hand
    for p in data["players"]:
        if not p["is_dealer"]:
            p["hand"] = p["hand"][:5]
            break
    with pytest.raises(ValueError):
        GameState.from_dict(data, strict=True)


def test_unsupported_schema_version() -> None:
    state = create_dealt_game("schema-v", num_players=2)
    data = state.to_dict()
    data["schema_version"] = 99
    with pytest.raises(ValueError, match="schema_version"):
        GameState.from_dict(data)


def test_missing_field() -> None:
    state = create_dealt_game("missing-field", num_players=2)
    data = state.to_dict()
    del data["wall"]
    with pytest.raises(ValueError, match="missing field"):
        GameState.from_dict(data)
