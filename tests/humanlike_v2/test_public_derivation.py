import pytest

from players.humanlike.public_derivation import PublicDerivationError, derive_public_rps


def test_public_derivations_are_bounded_and_deterministic():
    view = {"self_hand_indices": [0, 0, 1], "public_tile_indices": [0, 2], "wall_remaining": 40, "active_seats": [0,1,2,3], "other_players": [{"seat": 1, "melds": [1], "discards": [1,2]}]}
    first = derive_public_rps(view)
    assert first == derive_public_rps(view)
    assert first["RP-010"]["visible_counts"][0] == 3
    assert all(0 <= value <= 4 for value in first["RP-010"]["visible_counts"])
    assert 0 <= first["RP-020"]["aggregate_risk"] <= 1
    assert first["RP-022"]["phase"] == "early"


@pytest.mark.parametrize("field", ["hidden_hand", "server_hand", "private_hand", "concealed_tiles", "wall_order", "rng_state"])
def test_hidden_truth_is_rejected(field):
    with pytest.raises(PublicDerivationError):
        derive_public_rps({field: [1,2,3]})
