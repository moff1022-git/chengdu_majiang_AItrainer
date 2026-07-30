from engine.session import build_ready_game
from protocols.player_view_builder import PlayerViewBuilder

def test_rule_016_four_seat_hidden_information_isolation():
    state=build_ready_game("rule016",num_players=4); state.future_private_secret={"sentinel":"no"}
    for seat in range(4):
        view=PlayerViewBuilder().build(state,seat)
        assert "future_private_secret" not in view.payload and "wall_tile_ids" not in view.payload
        assert all("hand" not in p and "physical_hand" not in p for p in view.payload["other_players"])
