from copy import deepcopy
from players.humanlike.public_derivation import derive_public_rps


def test_other_seat_private_data_cannot_affect_public_derivation():
    base={"self_player":{"hand":["wan_1"]*13},"other_players":[{"seat":1,"melds":[],"discard_pile":[]}],"wall_remaining":30}
    first=derive_public_rps(base)
    changed=deepcopy(base)
    changed["unrelated_private_store"]={"seat_1_secret":"not projected"}
    # Unknown non-hidden metadata is ignored; only whitelisted public fields drive output.
    assert derive_public_rps(changed)==first


def test_each_seat_uses_its_own_self_projection():
    seat0={"self_player":{"hand":["wan_1"]*13},"other_players":[],"wall_remaining":30,"self_hand_indices":[0]*13}
    seat1={"self_player":{"hand":["tong_1"]*13},"other_players":[],"wall_remaining":30,"self_hand_indices":[9]*13}
    assert derive_public_rps(seat0)["RP-010"] != derive_public_rps(seat1)["RP-010"]
