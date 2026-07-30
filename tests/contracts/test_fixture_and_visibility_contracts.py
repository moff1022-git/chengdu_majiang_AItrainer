from __future__ import annotations
import ast,json
from pathlib import Path
from engine.audit import canonical_hash
from engine.config import EngineConfig
from engine.session import build_ready_game
from protocols.player_view_builder import PlayerViewBuilder

ROOT=Path(__file__).resolve().parents[2]

def test_fixture_format_has_state_views_truth_steps_and_expected():
    schema=json.loads((ROOT/"docs/spec-v3/contracts/schemas/fixture.schema.json").read_text())
    assert {"initial_state","player_views","restricted_truth","steps","expected","ruleset_hash","seed"} <= set(schema["required"])
    step_required=set(schema["properties"]["steps"]["items"]["required"])
    assert {"event_id","actor","phase","seed_stream","input","expected_output","expected_state_hash","expected_error"} <= step_required

def test_four_seat_visibility_and_recursive_sentinel_isolation():
    state=build_ready_game("contract-four-views",num_players=4); state.oracle_hands={"sentinel":"secret"}; hashes=[]
    for seat in range(4):
        view=PlayerViewBuilder().build(state,seat); text=json.dumps(view.to_legacy_dict(),sort_keys=True)
        assert "sentinel" not in text and "oracle_hands" not in text and "wall_tile_ids" not in text
        assert all("hand" not in p and "physical_hand" not in p for p in view.payload["other_players"])
        hashes.append(view.stable_hash)
    assert len(set(hashes))==4

def test_policy_modules_do_not_import_training_oracle():
    for base in (ROOT/"players/humanlike",ROOT/"protocols"):
        for path in base.rglob("*.py"):
            tree=ast.parse(path.read_text(encoding="utf-8")); modules=[]
            for node in ast.walk(tree):
                if isinstance(node,ast.ImportFrom): modules.append(node.module or "")
                elif isinstance(node,ast.Import): modules.extend(alias.name for alias in node.names)
            assert "training.oracle" not in modules, path

def test_parameter_and_hash_units_are_canonical():
    config=EngineConfig().to_dict(); assert len(canonical_hash(config))==64
    assert isinstance(config["base_score"],int) and isinstance(config["multi_ron"],bool)
