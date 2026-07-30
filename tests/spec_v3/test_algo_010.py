import pytest
from engine.session import build_ready_game
from protocols.player_view_builder import PlayerViewBuilder

def test_algo_010_golden_finished_wall_hidden_and_invalid_viewer():
    state=build_ready_game("algo010",num_players=4)
    view=PlayerViewBuilder({"wall_remaining":"hidden"}).build(state,0)
    assert view.payload["wall"] is None and "hand" in view.payload["self_player"]
    assert all("hand" not in p for p in view.payload["other_players"])
    with pytest.raises(ValueError,match="INVALID_VIEWER"): PlayerViewBuilder().build(state,4)
    state.phase="oracle"
    with pytest.raises(ValueError,match="INVALID_PHASE"): PlayerViewBuilder().build(state,0)
