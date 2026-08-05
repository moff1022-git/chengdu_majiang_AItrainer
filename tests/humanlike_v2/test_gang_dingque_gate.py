from engine.action import Action, ActionType
from engine.deal import create_dealt_game
from engine.tile import parse_tile
from players.humanlike.candidates import build_candidates
from players.humanlike.config import load_config
from players.humanlike.player import default_humanlike_config_path
from players.humanlike.view import build_decision_context
from protocols.messages import ActionRequest
from protocols.view_filter import build_observation

def test_last_dingque_tile_cannot_be_used_for_gang() -> None:
    state=create_dealt_game("f44-gang-gate"); obs=build_observation(state,0); obs.phase="discard"; obs.view["phase"]="discard"
    own=obs.view["players"][0]; own["dingque"]="tiao"; own["hand"]=["tiao_8","wan_1"]
    cfg=load_config(default_humanlike_config_path()); actions=[Action(ActionType.GANG_JIA,(parse_tile("tiao_8"),)),Action(ActionType.DISCARD,(parse_tile("tiao_8"),))]
    ctx=build_decision_context(obs,ActionRequest("f44",0,"discard",actions),bound_seat=0,profile=cfg.players[0],config_hash=cfg.config_hash)
    c=build_candidates(ctx,max_candidates=8)
    assert all(x.action.type is not ActionType.GANG_JIA for x in c.candidates)
