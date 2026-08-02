import pytest
from engine.legal import legal_discards, query_legal_discards
from engine.session import build_ready_game
from engine.tile import Suit
from engine.audit import canonical_hash

def test_rule_003_forced_dingque_clear_then_release_and_determinism():
    state=build_ready_game("rule003",num_players=4); state.phase="discard"; state.current_seat=0
    player=state.players[0]; player.dingque=Suit.WAN
    before=canonical_hash(state.to_dict()); version=state.schema_version
    first=legal_discards(state,0)
    if any(tile.suit==Suit.WAN for tile in player.hand): assert first and all(a.tiles[0].suit==Suit.WAN for a in first)
    assert first == legal_discards(state,0)
    assert canonical_hash(state.to_dict()) == before and state.schema_version == version
    player.hand[:] = [tile for tile in player.hand if tile.suit != Suit.WAN]
    assert all(a.tiles[0].suit != Suit.WAN for a in legal_discards(state,0))
    player.status="finished"; assert legal_discards(state,0)==[]

def test_rule_003_query_envelope_and_rejections():
    state=build_ready_game("rule003-envelope",num_players=4); state.phase="discard"; state.current_seat=0; state.players[0].dingque=Suit.WAN
    result=query_legal_discards(state,0); assert result.state_version_before==result.state_version_after and len(result.input_hash)==64
    state.phase="draw"
    with pytest.raises(ValueError,match="WRONG_PHASE"): query_legal_discards(state,0)
    state.phase="discard"; state.current_seat=1
    with pytest.raises(ValueError,match="NOT_ACTOR"): query_legal_discards(state,0)
    state.current_seat=0; state.players[0].dingque=None
    with pytest.raises(ValueError,match="DINGQUE_UNSET"): query_legal_discards(state,0)
