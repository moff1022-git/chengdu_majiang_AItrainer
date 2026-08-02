import pytest
from engine.action import Action, ActionType
from engine.tile import Suit, Tile
from training.action_codec_v2 import ACTION_SPACE_SIZE, ActionCodecError, decode_action, encode_action, legal_action_mask

def test_train_003_codec_mask_bijection_boundary_and_illegal():
    actions=[Action(ActionType.PASS),Action(ActionType.DISCARD,tiles=(Tile(Suit.WAN,1),)),Action(ActionType.DINGQUE,suit=Suit.TIAO)]
    for action in actions: assert decode_action(encode_action(action)) == action
    mask=legal_action_mask(actions); assert len(mask)==ACTION_SPACE_SIZE and sum(mask)==3
    assert decode_action(110) == Action(ActionType.DISCARD,tiles=(Tile(Suit.WAN,1),))
    assert decode_action(632) == Action(ActionType.DINGQUE,suit=Suit.WAN)
    assert decode_action(634) == Action(ActionType.DINGQUE,suit=Suit.TIAO)
    for value in (-1, ACTION_SPACE_SIZE):
        with pytest.raises(ActionCodecError) as exc: decode_action(value)
        assert exc.value.code == "ACTION_CODEC_INVALID"

def test_train_003_all_635_slots_are_bijective():
    for index in range(ACTION_SPACE_SIZE): assert encode_action(decode_action(index)) == index
    mixed=Action(ActionType.EXCHANGE,tiles=(Tile(Suit.WAN,1),Tile(Suit.TONG,1),Tile(Suit.WAN,2)))
    with pytest.raises(ActionCodecError) as exc: encode_action(mixed)
    assert exc.value.code == "ACTION_CODEC_INVALID"
