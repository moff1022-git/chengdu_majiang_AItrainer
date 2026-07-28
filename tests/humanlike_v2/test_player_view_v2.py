from __future__ import annotations

import ast
from pathlib import Path

from engine.session import build_ready_game
from engine.state import Meld
from protocols.player_view_builder import PlayerViewBuilder
from protocols.view_filter import filter_state_for_seat
from training.oracle import build_training_truth

ROOT = Path(__file__).resolve().parents[2]


def test_v2_whitelist_hides_opponents_wall_and_sentinel() -> None:
    state = build_ready_game("view-v2", num_players=4)
    state.future_private_secret = {"sentinel": "must-not-leak"}
    view = PlayerViewBuilder().build(state, 0)
    payload = view.payload
    assert view.view_version == 2
    assert "future_private_secret" not in payload
    assert "wall_tile_ids" not in payload
    assert payload["self_player"]["physical_hand"]
    for player in payload["other_players"]:
        assert "hand" not in player
        assert "physical_hand" not in player
    legacy = filter_state_for_seat(state, 0)
    assert "wall" not in legacy
    assert "physical_hand" not in legacy["players"][0]
    assert "oracle_hands" not in legacy


def test_gp021_wall_and_concealed_gang_visibility_modes() -> None:
    state = build_ready_game("view-modes", num_players=4)
    hidden = PlayerViewBuilder({"wall_remaining": "hidden"}).build(state, 0).payload
    partial = PlayerViewBuilder({"wall_remaining": "public_partial"}).build(state, 0).payload
    exact = PlayerViewBuilder({"wall_remaining": "public_exact"}).build(state, 0).payload
    assert hidden["wall"] is None
    assert "remaining_min" in partial["wall"]
    assert exact["wall"]["remaining_exact"] == len(state.wall)


def test_gp021_all_visibility_fields_have_hidden_partial_exact_contracts() -> None:
    state = build_ready_game("view-all-modes", num_players=4)
    state.players[1].melds.append(Meld("an_gang", (0, 1, 2, 3)))
    state.players[1].status = "finished"
    state.exchange_dir_resolved = "clockwise"
    for level in ("hidden", "public_partial", "public_exact"):
        policy = {
            "wall_remaining": level,
            "draw_source": level,
            "exchange_source": level,
            "concealed_gang_tiles": level,
            "hu_hand": level,
            "draw_round_hand": level,
            "thinking_time": level,
            "cancel_action": level,
        }
        payload = PlayerViewBuilder(policy).build(state, 0).payload
        opponent = payload["other_players"][0]
        concealed = opponent["melds"][-1]
        if level == "hidden":
            assert payload["wall"] is None
            assert payload["exchange_direction_public"] is None
            assert "tile_id" not in concealed and "suit" not in concealed
            assert "revealed_hand" not in opponent
            assert payload["last_public_event"]["draw_source"] is None
        elif level == "public_partial":
            assert "remaining_min" in payload["wall"]
            assert payload["exchange_direction_public"] == "clockwise"
            assert concealed["suit"] == "wan" and "tile_id" not in concealed
            assert opponent["revealed_hand_count"] == len(state.players[1].hand)
            assert payload["last_public_event"]["draw_source"] == "unknown"
        else:
            assert payload["wall"]["remaining_exact"] == len(state.wall)
            assert payload["exchange_direction_public"] == "clockwise"
            assert concealed["tile_id"] == "wan_1"
            assert len(opponent["revealed_hand"]) == len(state.players[1].hand)
            assert payload["last_public_event"]["draw_source"] is None  # no reliable source evidence
        assert payload["last_public_event"]["thinking_time"] is None
        assert payload["last_public_event"]["cancel_action"] is None


def test_oracle_is_separate_and_production_modules_do_not_import_it() -> None:
    state = build_ready_game("truth-only", num_players=4)
    truth = build_training_truth(state)
    assert set(truth.hands) == {0, 1, 2, 3}
    for relative in ("protocols", "players/humanlike", "players/rule_ai_player.py"):
        paths = [ROOT / relative] if (ROOT / relative).is_file() else list((ROOT / relative).rglob("*.py"))
        for path in paths:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            imports = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
            assert "training.oracle" not in imports
