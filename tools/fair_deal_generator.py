"""Deterministic fair fixed-deal dataset generator (F0049)."""
from __future__ import annotations

import argparse, hashlib, json, random
from collections import Counter
from pathlib import Path

from engine.tile import all_tile_faces

ALGORITHM = "fair-window-candidate-v1"
CANDIDATES = 16

def _seed(*parts: object) -> int:
    return int.from_bytes(hashlib.sha256("|".join(map(str, parts)).encode()).digest()[:8], "big")

def _hands(wall: list[str], dealer: int) -> dict[str, list[str]]:
    sizes=[14 if s==dealer else 13 for s in range(4)]; out={f"s{s}":[] for s in range(4)}; pos=0
    # Fixed-deal contract consumes the first 53 tiles; group assignment is explicit.
    for s,n in enumerate(sizes): out[f"s{s}"]=sorted(wall[pos:pos+n]); pos+=n
    return out

def _features(hand: list[str]) -> tuple[list[int],int,int]:
    suits=[sum(t.startswith(x) for t in hand) for x in ("wan_","tong_","tiao_")]
    c=Counter(hand); pairs=sum(v>=2 for v in c.values()); middle=sum(2<=int(t.rsplit('_',1)[1])<=8 for t in hand)
    return suits,pairs,middle

def _score(hands: dict[str,list[str]], cumulative: list[list[int]], window: int) -> int:
    fs=[_features(hands[f"s{s}"]) for s in range(4)]
    score=sum(max(x[i] for x,_,_ in fs)-min(x[i] for x,_,_ in fs) for i in range(3))*20
    score+=(max(x[1] for x in fs)-min(x[1] for x in fs))*8+(max(x[2] for x in fs)-min(x[2] for x in fs))*2
    if cumulative:
        recent=cumulative[-window:]
        totals=[[sum(row[s*3+i] for row in recent)+fs[s][0][i] for i in range(3)] for s in range(4)]
        score+=sum(max(t[i] for t in totals)-min(t[i] for t in totals) for i in range(3))*5
    return score

def generate(test_id: str, seed: str, games: int, output: Path, window: int=50) -> dict:
    output.mkdir(parents=True,exist_ok=True); artifact=output/'deals.jsonl'; rows=[]; history=[]
    base=[t.id for t in all_tile_faces() for _ in range(4)]
    for i in range(games):
        dealer=i%4; choices=[]
        for c in range(CANDIDATES):
            wall=base.copy(); random.Random(_seed(seed,test_id,i,c)).shuffle(wall); hands=_hands(wall,dealer)
            choices.append((_score(hands,history,window),c,wall,hands))
        score,c,wall,hands=min(choices,key=lambda x:(x[0],x[1]))
        history.append([v for s in range(4) for v in _features(hands[f's{s}'])[0]])
        rows.append({'game_id':f'{test_id}-{i:06d}','dealer':dealer,'wall_order':wall,'initial_hands':hands,'generation':{'algorithm':ALGORITHM,'seed':seed,'candidate_index':c,'candidate_score':score}})
    data=''.join(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n' for r in rows).encode();artifact.write_bytes(data)
    manifest={'test_id':test_id,'mode':'fair','schema_version':'deal-fairness-v1','algorithm':ALGORITHM,'seed':seed,'games':games,'candidate_count':CANDIDATES,'window':window,'artifact':'deals.jsonl','sha256':hashlib.sha256(data).hexdigest()}
    (output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');return manifest

def validate(output: Path) -> None:
    m=json.load(open(output/'manifest.json')); raw=(output/m['artifact']).read_bytes(); assert hashlib.sha256(raw).hexdigest()==m['sha256']
    expected=sorted(t.id for t in all_tile_faces() for _ in range(4)); rows=[json.loads(x) for x in raw.splitlines()]; assert len(rows)==m['games']
    for i,r in enumerate(rows):
        assert r['dealer']==i%4 and len(r['wall_order'])==108 and sorted(r['wall_order'])==expected
        assert [len(r['initial_hands'][f's{s}']) for s in range(4)]==[14 if s==r['dealer'] else 13 for s in range(4)]
        assert sorted(sum((r['initial_hands'][f's{s}'] for s in range(4)),[]))==sorted(r['wall_order'][:53])

def main() -> int:
    p=argparse.ArgumentParser();p.add_argument('--test-id',required=True);p.add_argument('--seed',required=True);p.add_argument('--games',type=int,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--validate-only',action='store_true');a=p.parse_args()
    if not a.validate_only: print(json.dumps(generate(a.test_id,a.seed,a.games,a.output),ensure_ascii=False))
    validate(a.output);return 0
if __name__=='__main__':raise SystemExit(main())
