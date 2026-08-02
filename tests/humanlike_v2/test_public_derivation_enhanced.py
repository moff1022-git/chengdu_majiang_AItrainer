from players.humanlike.public_derivation import derive_public_rps


def test_own_hand_waits_use_public_self_projection_only():
    view = {"self_player": {"hand": ["wan_1"] * 13, "melds": [], "dingque": None}, "other_players": [], "wall_remaining": 40, "active_seats": [0,1,2,3], "self_hand_indices": [0] * 13}
    result = derive_public_rps(view)
    assert 0 <= result["RP-018"]["live_total"] <= 108
    assert 0 <= result["RP-018"]["probability"] <= 1


def test_opponent_posterior_is_public_only_and_normalized_fields_present():
    view = {"self_player": {"hand": ["wan_1"] * 13}, "other_players": [{"seat": 1, "melds": [{"tile_id": "tong_1", "tile_count": 3}], "discard_pile": ["wan_9"]}], "wall_remaining": 20}
    hypotheses = derive_public_rps(view)["RP-019"]["hypotheses"]
    assert hypotheses and hypotheses[0]["model_version"] == "MODEL-001-rule-baseline-v1"
    assert 0 <= hypotheses[0]["ready_probability"] <= 1
