from __future__ import annotations
import json
from pathlib import Path
import pytest
from engine.action import Action, ActionType
from engine.game_id import derive_seeds
from engine.physical_tile import build_physical_wall, physical_tile
from engine.session import build_ready_game
from engine.state import GameState, Meld
from engine.tile import Suit, Tile
from protocols.player_view_builder import PlayerViewBuilder
from training.action_codec_v2 import ACTION_SPACE_SIZE, decode_action, encode_action

ROOT=Path(__file__).resolve().parents[2]
SCHEMAS=ROOT/"docs/spec-v3/contracts/schemas"

def load(name): return json.loads((SCHEMAS/name).read_text(encoding="utf-8"))

def test_contract_schemas_parse_and_freeze_version():
    common=load("common_contracts.schema.json"); decision=load("decision.schema.json"); fixture=load("fixture.schema.json")
    assert common["$schema"].endswith("2020-12/schema")
    assert common["properties"]["contract_version"]["const"] == "CDMJ-CONTRACTS 1.0.0"
    assert decision["properties"]["contract_version"]["const"] == "CDMJ-CONTRACTS 1.0.0"
    assert fixture["properties"]["fixture_version"]["const"] == 1
    assert {"physical_tile","discard","meld","player","action","candidate","score_breakdown","seed_trace","decision_explanation"} <= set(common["$defs"])

def test_tile_wall_hand_discard_meld_contract():
    wall=build_physical_wall(); assert len(wall)==108 and len({t.tile_id for t in wall})==108
    for tile in wall: assert tile.face_id == f"{tile.suit.value}_{tile.rank}" and tile.copy_index == tile.tile_id % 4
    meld=Meld("pong",(0,1,2)); assert Meld.from_dict(meld.to_dict()) == meld
    with pytest.raises(ValueError): Meld("pong",(0,1,4))

def test_player_and_game_state_v5_roundtrip():
    state=build_ready_game("contract-state",num_players=4); raw=state.to_dict(); restored=GameState.from_dict(raw)
    assert raw["schema_version"]==5 and restored.to_dict()==raw
    assert sorted(p.seat for p in state.players)==[0,1,2,3]
    assert all(p.status in {"active","finished"} for p in state.players)

def test_action_contract_roundtrip_and_codec():
    samples=(Action(ActionType.PASS),Action(ActionType.HU),Action(ActionType.DISCARD,tiles=(Tile(Suit.WAN,1),)),Action(ActionType.DINGQUE,suit=Suit.TIAO))
    for action in samples: assert Action.from_dict(action.to_dict())==action
    for index in range(ACTION_SPACE_SIZE): assert encode_action(decode_action(index))==index

def test_seed_contract_is_deterministic_and_versioned_by_source():
    first=derive_seeds("contract-seed"); second=derive_seeds("contract-seed")
    assert first==second and 0 <= first.master_seed < 2**64
    assert len({first.shuffle_seed,first.dice_seed,first.exchange_seed})==3

def test_player_view_is_deep_frozen_and_hidden():
    state=build_ready_game("contract-view",num_players=4); state.future_truth={"wall_order":[1,2,3]}
    view=PlayerViewBuilder().build(state,0)
    assert view.view_version==2 and "future_truth" not in view.payload
    assert all("hand" not in p and "physical_hand" not in p for p in view.payload["other_players"])
    with pytest.raises(TypeError): view.payload["self_player"]["score"]=99
    assert len(view.stable_hash)==64
