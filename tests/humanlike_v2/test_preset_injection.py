from players.registry import create_players

def test_humanlike_preset_is_injected_per_seat():
    players=create_players(["humanlike_v2"]*4, humanlike_presets=["novice_conservative","normal_balanced","skilled_aggressive","expert_balanced"])
    assert [p.preset_id for p in players] == ["novice_conservative","normal_balanced","skilled_aggressive","expert_balanced"]
