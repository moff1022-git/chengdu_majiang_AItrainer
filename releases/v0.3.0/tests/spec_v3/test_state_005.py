import pytest
from engine.session import build_ready_game
from protocols.player_view_builder import PlayerViewBuilder

def test_state_005_deep_freeze_hash_and_serialization_stability():
    state=build_ready_game("state005",num_players=4); view=PlayerViewBuilder().build(state,0)
    assert view.stable_hash == PlayerViewBuilder().build(state,0).stable_hash
    with pytest.raises(TypeError): view.payload["self_player"]["score"] = 99
    with pytest.raises(AttributeError): view.payload["other_players"].append({})
