from __future__ import annotations
import json, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from players.humanlike.player import HumanlikeV2Player
from tools.ai_capability_test import run_game

src = Path(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
rows = [json.loads(x) for x in (src / 'games.jsonl').read_text().splitlines() if x.strip()]
failed = [r['game_id'] for r in rows if r.get('status') == 'FAILED']
presets = ['nonhuman_optimized','novice_balanced','novice_balanced','novice_balanced']
trace_dir = out / 'traces'; trace_dir.mkdir(exist_ok=True)
def one(gid):
    try: return run_game(['humanlike_v2']*4, gid, presets, trace_dir=trace_dir)
    except Exception as exc: return {'game_id':gid,'status':'FAILED','error_type':type(exc).__name__,'error':str(exc)}
results=[]
with ThreadPoolExecutor(max_workers=50) as pool:
    futures=[pool.submit(one,g) for g in failed]
    for f in as_completed(futures): results.append(f.result())
results.sort(key=lambda r: failed.index(r.get('game_id','')))
(out/'games.jsonl').write_text('\n'.join(json.dumps(r,ensure_ascii=False) for r in results)+'\n')
(out/'retry_manifest.json').write_text(json.dumps({'source':str(src),'requested':len(failed),'completed':sum(r.get('status')!='FAILED' for r in results),'failed':sum(r.get('status')=='FAILED' for r in results),'game_ids':failed},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'requested':len(failed),'completed':sum(r.get('status')!='FAILED' for r in results),'failed':sum(r.get('status')=='FAILED' for r in results)}))
