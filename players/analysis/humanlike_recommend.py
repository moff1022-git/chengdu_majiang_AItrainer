from engine.action import ActionType
from engine.shanten import shanten
from players.analysis.remain import remain_map, ukeire_count
from players.analysis.danger import danger_map_for_tiles, DANGER_PENALTY
from players.analysis.types import DiscardAdvice
def _remove_one(hand, tile_id):
    out=[]; removed=False
    for t in hand:
        if not removed and t.id == tile_id: removed=True; continue
        out.append(t)
    return out

def rank_humanlike_discards(state, seat, hand, melds, dingque, opponents, *, legal_discards=None, algorithm="humanlike_v2", preset_id=None):
    ids=[]
    for a in legal_discards or []:
        if a.type == ActionType.DISCARD and a.tiles and a.tiles[0].id not in ids: ids.append(a.tiles[0].id)
    remain=remain_map(state,seat); danger=danger_map_for_tiles(ids,state,opponents); out=[]
    for tid in ids:
        s=shanten(_remove_one(hand,tid),melds,dingque); uke=[t.id for t in (s.ukeire or ())]; u=ukeire_count(uke,remain); d=danger.get(tid,"unknown")
        score=-4*s.shanten+0.15*u-DANGER_PENALTY.get(d,.5)
        if algorithm == "rule_ai": score += 0.08*u
        elif algorithm == "rule_ai_plus": score += 0.12*u - (0.35 if d in ("high","critical") else 0)
        out.append(DiscardAdvice(tid,0,s.shanten,u,d,score,"none",uke))
    out.sort(key=lambda a:(-a.score,a.tile_id))
    return [DiscardAdvice(a.tile_id,i+1,a.shanten_after,a.ukeire_after,a.danger,a.score,"best" if i==0 else "second" if i==1 else "none",a.ukeire_tiles) for i,a in enumerate(out)]
