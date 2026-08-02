from __future__ import annotations
import json, sys
from pathlib import Path

root=Path(sys.argv[1]); games= root/'games.jsonl'; trace=root/'traces'
rows=[json.loads(x) for x in games.read_text().splitlines() if x.strip()]
ok=[]; bad=[]
for r in rows:
 gid=r.get('game_id'); steps=trace/f'{gid}.steps.jsonl'; audit=trace/f'{gid}.audit.jsonl'
 if r.get('status')=='FAILED': continue
 if steps.exists() and audit.exists() and steps.stat().st_size and audit.stat().st_size: ok.append(gid)
 else: bad.append({'game_id':gid,'steps':steps.exists(),'audit':audit.exists()})
out={'games':len(rows),'successful_games':sum(r.get('status')!='FAILED' for r in rows),'complete_trace_games':len(ok),'incomplete_successful_games':bad,'status':'PASS' if not bad else 'FAIL'}
(root/'trace_completeness.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'games':out['games'],'successful':out['successful_games'],'complete':len(ok),'incomplete':len(bad),'status':out['status']}))
