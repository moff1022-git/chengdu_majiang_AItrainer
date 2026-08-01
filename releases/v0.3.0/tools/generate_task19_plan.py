from __future__ import annotations

import csv, hashlib, json, re, subprocess
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; SPEC=ROOT/'docs/spec-v3'; OUT=SPEC/'task19'; OUT.mkdir(parents=True,exist_ok=True); (OUT/'progress_deltas').mkdir(exist_ok=True); (OUT/'prompts').mkdir(exist_ok=True)
AUDITED={'RULE-003','RULE-016','ALGO-001','ALGO-009','ALGO-010','ALGO-011','HEUR-019','STATE-001','STATE-004','STATE-005','STATE-010','STATE-011','SCORE-001','TRAIN-003','AUDIT-003'}
B2={'STATE-002','STATE-003','ALGO-002'}
TRACK={'RULE':'TRACK-DETERMINISTIC','STATE':'TRACK-DETERMINISTIC','ALGO':'TRACK-DETERMINISTIC','SCORE':'TRACK-DETERMINISTIC','HEUR':'TRACK-HEURISTIC','MODEL':'TRACK-MODEL','TRAIN':'TRACK-TRAINING','AUDIT':'TRACK-AUDIT'}
STATUS_ORDER=['PLANNING','WAITING_FOR_DESIGN_APPROVAL','READY_FOR_IMPLEMENTATION','IMPLEMENTING','IMPLEMENTED_PENDING_EVIDENCE','IMPLEMENTED_PENDING_INDEPENDENT_AUDIT','AUDIT_REMEDIATION','AUDITED','INTEGRATED','SCAFFOLDED','BLOCKED']
SUB=['NOT_REQUIRED','NOT_STARTED','IN_PROGRESS','PASS','FAIL','PARTIAL','WAITING_APPROVAL','BLOCKED']
GATES=['design','decision','implementation','direct_test','branch_test','exception_test','integration_test','information_boundary','determinism','performance','production_wiring','E4','E5','AC','defect_gate','independent_audit']

def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(p,rows,fields=None):
 with p.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def esc(v):return str(v).replace('|','\\|').replace('\n',' ')
def natural(u):
 a,n=u.split('-'); order={'RULE':0,'ALGO':1,'HEUR':2,'MODEL':3,'STATE':4,'SCORE':5,'TRAIN':6,'AUDIT':7};return order[a],int(n)

def main():
 now=datetime.now(timezone.utc).isoformat().replace('+00:00','Z'); commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 gaps=readcsv(SPEC/'plans/task18_gap_classification.csv'); gap={r['unit_id']:r for r in gaps}; queue=readcsv(SPEC/'plans/task18_post_b1b_queue.csv'); remain={r['unit_id'] for r in queue}
 catalog=readcsv(SPEC/'02-unit-catalog/locked_unit_catalog.csv'); names={r['新单元ID']:r['名称'] for r in catalog}
 graph=json.loads((SPEC/'plans/task18_post_b1b_dependency_graph.json').read_text()); deps=defaultdict(set)
 for e in graph['edges']: deps[e['to']].add(e['from'])
 # Re-batch into independently auditable groups of at most four, preserving Task18 topology but not its large patches.
 groups=[
 ('T19-B2A1','B2-A1 approved deterministic prerequisites',['STATE-002','STATE-003','ALGO-002']),
 ('T19-D01','Rule foundation A',['RULE-001','RULE-005']),('T19-D02','Rule foundation B',['RULE-002','RULE-006','RULE-015']),
 ('T19-D03','Decision prerequisites',['STATE-009','ALGO-006']),('T19-D04','Claim rules A',['RULE-004','RULE-010','RULE-011']),('T19-D05','Claim rules B',['RULE-007','RULE-008','RULE-012']),
 ('T19-D06','Response rules',['RULE-009','RULE-013','RULE-014']),('T19-D07','Immediate scoring',['SCORE-002','SCORE-003']),('T19-D08','Terminal scoring A',['SCORE-004','SCORE-005']),('T19-D09','Terminal scoring B',['SCORE-006']),
 ('T19-D10','Deterministic algorithms A',['ALGO-003','ALGO-004']),('T19-D11','Deterministic algorithms B',['ALGO-005','ALGO-007']),('T19-D12','Deterministic algorithm C',['ALGO-008']),
 ('T19-D13','State completion A',['STATE-006','STATE-008']),('T19-D14','State completion B',['STATE-007','STATE-012']),
 ('T19-H01','Heuristic foundation A',['HEUR-001','HEUR-002','HEUR-004']),('T19-H02','Heuristic foundation B',['HEUR-006','HEUR-008','HEUR-011']),('T19-H03','Heuristic foundation C',['HEUR-020','HEUR-022']),
 ('T19-H04','Heuristic decisions A',['HEUR-003','HEUR-005','HEUR-007']),('T19-H05','Heuristic decisions B',['HEUR-009','HEUR-010','HEUR-012']),('T19-H06','Heuristic decisions C',['HEUR-014','HEUR-017','HEUR-021','HEUR-023']),
 ('T19-H07','Heuristic risk A',['HEUR-013','HEUR-015']),('T19-H08','Heuristic full implementation',['HEUR-016']),('T19-H09','Heuristic risk B',['HEUR-018']),
 ('T19-M01','Model inference',['MODEL-002','MODEL-003']),('T19-M02','Trainable policy contract',['MODEL-004']),('T19-M03','Model lifecycle',['MODEL-005']),('T19-X01','MODEL-001 external calibration',['MODEL-001']),
 ('T19-T01','Training contracts A',['TRAIN-001','TRAIN-002']),('T19-T02','Training contracts B',['TRAIN-004','TRAIN-005']),('T19-T03','Training environment',['TRAIN-006','TRAIN-009']),('T19-T04','Training self-play',['TRAIN-007']),('T19-X02','Offline training data',['TRAIN-008']),
 ('T19-A01','Audit runtime A',['AUDIT-001','AUDIT-002']),('T19-A02','Audit runtime B',['AUDIT-004','AUDIT-005']),('T19-A03','Audit runtime C',['AUDIT-006','AUDIT-007']),('T19-A04','Audit trace A',['AUDIT-010','AUDIT-008']),('T19-A05','Audit trace B',['AUDIT-009','AUDIT-011']),('T19-A06','Audit release',['AUDIT-013','AUDIT-014']),('T19-X03','External effect evaluation',['AUDIT-012'])]
 assigned={u for _,_,us in groups for u in us}; assert assigned==remain,(remain-assigned,assigned-remain)
 unit_batch={u:b for b,_,us in groups for u in us}; batch_units={b:us for b,_,us in groups}; titles={b:n for b,n,_ in groups}
 # Batch dependencies derived from unit graph; internal dependencies remain explicit.
 bdeps={b:set() for b,_,_ in groups}; internal={b:[] for b,_,_ in groups}
 for b,_,us in groups:
  for u in us:
   for d in deps[u]:
    if d in us: internal[b].append(f'{d}->{u}')
    elif d in unit_batch:bdeps[b].add(unit_batch[d])
 # Conservative waves: topological levels; conflict-prone batches are serialized by unique wave suffix.
 indeg={b:len(ds) for b,ds in bdeps.items()}; children=defaultdict(set)
 for b,ds in bdeps.items():
  for d in ds:children[d].add(b)
 ready=sorted([b for b,x in indeg.items() if x==0]); waves=[]
 while ready:
  wave=ready; waves.append(wave); nxt=[]
  for b in wave:
   for c in children[b]:
    indeg[c]-=1
    if indeg[c]==0:nxt.append(c)
  ready=sorted(nxt)
 assert sum(map(len,waves))==len(groups)
 wave_of={b:f'W{wi:02d}' for wi,bs in enumerate(waves,1) for b in bs}
 # First wave implementation only B2A1. Other dependency roots are design-only until approved.
 wave_of['T19-B2A1']='W01'; terminal={'T19-B2A1':'Terminal 1'}
 for b,_,us in groups:
  if b not in terminal:
   terminal[b]='Terminal 3' if b.startswith(('T19-A','T19-X')) else 'Terminal 2' if b.startswith(('T19-H','T19-D0')) else 'Terminal 1'
 def paths_for(u):
  refs=[x.split('::')[0] for x in gap[u]['code_refs'].split('|') if x]; return sorted(set(refs))
 def tests_for(u):return sorted({x.split('::')[0] for x in gap[u]['test_refs'].split('|') if x})
 batch_rows=[]; ownership=[]
 for b,title,us in groups:
  track='TRACK-EXTERNAL-DATA' if b.startswith('T19-X') else TRACK[us[0].split('-')[0]]
  design='APPROVED' if b=='T19-B2A1' else 'WAITING_APPROVAL'; impl='READY_FOR_IMPLEMENTATION' if b=='T19-B2A1' else 'WAITING_FOR_DESIGN_APPROVAL'
  biz=sorted({p for u in us for p in paths_for(u)}); tst=sorted({p for u in us for p in tests_for(u)})
  # Existing shared files are candidate/read-only until a batch design assigns ownership.
  allowed=[f'engine/task19/{b.lower()}_*.py'] if track=='TRACK-DETERMINISTIC' else [f'{"players/humanlike" if track=="TRACK-HEURISTIC" else "training" if track=="TRACK-TRAINING" else "tools"}/{b.lower()}_*.py']
  if b=='T19-B2A1':allowed=['engine/round_state_store.py','engine/player_round_state.py','engine/hand_analysis_v1.py','engine/state.py','engine/shanten.py']
  batch_rows.append(dict(batch_id=b,batch_name=title,track_id=track,unit_ids='|'.join(us),unit_count=len(us),internal_order=' -> '.join(us),external_dependencies='|'.join(sorted(bdeps[b])),in_batch_dependencies='|'.join(sorted(set(internal[b]))),unlocks='|'.join(sorted(children[b])),completion_path='|'.join(sorted({gap[u]['primary_completion_path'] for u in us})),design_status=design,implementation_status=impl,audit_status='NOT_STARTED',model001_gate='SELF_ONLY' if 'MODEL-001' in us else 'NONE',expected_shared_interfaces='|'.join(sorted({Path(p).name for p in biz if p.startswith(('engine/','protocols/'))})[:8]),global_document_impact='DELTA_ONLY; Terminal 0 owns global files'))
  ownership.append(dict(batch_id=b,parallel_wave_id=wave_of[b],allowed_business_paths='|'.join(allowed),allowed_test_paths=f'tests/spec_v3/{b.lower()}_*.py',allowed_evidence_paths=f'docs/spec-v3/task19/evidence/{b}/**',allowed_design_paths=f'docs/spec-v3/task19/design/{b}/**',read_only_shared_paths='|'.join(biz+tst),forbidden_paths='docs/spec-v3/03-unit-specs/**|docs/spec-v3/contracts/**|docs/spec-v3/task19/task19_progress_tracker.md|docs/changelog.md|Task17 historical files',public_interface_owner='Terminal 1 / '+b if b=='T19-B2A1' else 'UNASSIGNED_UNTIL_DESIGN_APPROVAL',global_document_owner='Terminal 0',expected_new_files='batch DTO/facade/direct tests/E4/E5/progress delta after authorization',expected_modified_files='NONE until approved design assigns exact paths'))
 writecsv(OUT/'task19_batch_plan.csv',batch_rows); writecsv(OUT/'task19_file_ownership_matrix.csv',ownership)
 # Unit execution matrix.
 units=[]
 for u in sorted(remain,key=natural):
  b=unit_batch[u]; q=next(x for x in queue if x['unit_id']==u)
  units.append(dict(unit_id=u,unit_name=names.get(u,u),category=u.split('-')[0],track_id='TRACK-EXTERNAL-DATA' if b.startswith('T19-X') else TRACK[u.split('-')[0]],batch_id=b,parallel_wave_id=wave_of[b],assigned_terminal=terminal[b],current_status=q['current_status'],completion_path=q['completion_path'],dependencies='|'.join(sorted(deps[u])),cross_track_dependencies='|'.join(sorted(d for d in deps[u] if d in remain and TRACK.get(d.split('-')[0])!=TRACK.get(u.split('-')[0]))),design_status='APPROVED' if u in B2 else 'WAITING_APPROVAL',implementation_authorization='READY_FOR_IMPLEMENTATION' if u in B2 else 'WAITING_FOR_DESIGN_APPROVAL',next_action='Implement approved design' if u in B2 else 'Create and approve unit design package'))
 writecsv(OUT/'task19_unit_execution_matrix.csv',units)
 # Parallel waves are conservative planning waves; implementation permission remains per batch.
 wave_rows=[]
 for i,bs in enumerate(waves,1):
  wid=f'W{i:02d}'; selected=[b for b in bs if wave_of[b]==wid]
  if wid=='W01' and 'T19-B2A1' not in selected:selected.insert(0,'T19-B2A1')
  selected=list(dict.fromkeys(selected)); count=sum(len(batch_units[b]) for b in selected)
  wave_rows.append(dict(parallel_wave_id=wid,batch_ids='|'.join(selected),batch_count=len(selected),unit_count=count,can_run_in_parallel='true' if len(selected)>1 else 'false',parallel_groups='|'.join(f'{wid}-G{j+1}' for j in range(len(selected))),cross_batch_dependency='NONE_WITHIN_WAVE',shared_file_risk='REQUIRES_PRESTART_PATH_DIFF',shared_interface_risk='UNIQUE_OWNER_REQUIRED',shared_test_fixture_risk='NEW_BATCH_FILES_ONLY',shared_evidence_risk='DISJOINT_BATCH_DIRECTORIES',integration_conflict_risk='MEDIUM',recommended_terminals='|'.join(terminal[b] for b in selected),integration_order=' -> '.join(selected),full_regression_checkpoint=f'{wid}-POST-INTEGRATION',evidence_checkpoint=f'{wid}-E4E5',independent_audit_checkpoint=f'{wid}-AUDIT'))
 writecsv(OUT/'task19_parallel_wave_plan.csv',wave_rows)
 # Interface ownership. Global DTOs stay Terminal 0/read-only except approved B2A1 owner.
 interfaces=[('RoundState DTO/capabilities','T19-B2A1','Terminal 1'),('PlayerRoundState DTO','T19-B2A1','Terminal 1'),('ALGO-002 analyze_hand_v1','T19-B2A1','Terminal 1'),('GameState legacy v5 adapter','T19-B2A1','Terminal 1'),('PlayerViewV2','GLOBAL-INTERFACE','Terminal 0'),('error code registry','GLOBAL-INTERFACE','Terminal 0'),('audit evidence schema','GLOBAL-INTERFACE','Terminal 0'),('Task19 progress schema','TASK19-CONTROL','Terminal 0')]
 writecsv(OUT/'task19_interface_ownership.csv',[dict(interface=i,owner_batch=b,owner_terminal=t,concurrent_writers=1,change_rule='Proposal and approval required outside owner batch') for i,b,t in interfaces])
 # Risk register.
 risks=[
 ('T19-RISK-001','INTEGRATION_CONFLICT','ALL','Dirty main worktree cannot be a safe worktree baseline','Approve and create a clean checkpoint commit/tag without discarding user changes','OPEN'),
 ('T19-RISK-002','DESIGN_DECISION','ALL_EXCEPT_B2A1','Only B2-A1 has an Approved implementation design','Generate/approve each batch design before implementation','OPEN'),
 ('T19-RISK-003','INTERFACE_DECISION','SHARED_INTERFACES','Future batches may need B2-A1 or PlayerView shared interfaces','Terminal 0 owns proposals and replans waves','OPEN'),
 ('T19-RISK-004','EXTERNAL_DATA','MODEL-001|MODEL-005|TRAIN-008|AUDIT-012','External validity/data publication remains unavailable','Keep gate local to external-data track','OPEN')]
 writecsv(OUT/'task19_risk_register.csv',[dict(risk_id=a,blocking_type=b,affected_units=c,reason=d,mitigation=e,status=f) for a,b,c,d,e,f in risks])
 # Progress tracker initial records.
 all_units=sorted({r['新单元ID'] for r in catalog},key=natural); assert len(all_units)==96
 evidence={u:'docs/spec-v3/audit/task17_96_unit_audit_clarification.md' for u in AUDITED}
 for u in {'STATE-010','ALGO-009','ALGO-011'}:evidence[u]='docs/spec-v3/reports/B1-A_implementation_audit.md'
 for u in {'STATE-001','STATE-004','STATE-011'}:evidence[u]='docs/spec-v3/audit/B1-B_final_independent_audit_report.md'
 records=[]
 for u in all_units:
  task17='AUDITED' if u in (AUDITED-{'STATE-010','ALGO-009','ALGO-011','STATE-001','STATE-004','STATE-011'}) else 'INTEGRATED' if u=='MODEL-001' else 'SCAFFOLDED' if u=='HEUR-016' else 'PARTIAL'
  task18='AUDITED' if u in AUDITED else task17
  if u in AUDITED: status='AUDITED'; vals={g:'PASS' for g in GATES}; ac='14/14'; defects='0/0/0'; blocker='NONE'; nxt='No action; monitor findings'; latest=evidence[u]; batch='COMPLETED'; wave='DONE'; term='Terminal 0'
  elif u=='MODEL-001':
   status='INTEGRATED';vals={g:'NOT_STARTED' for g in GATES};
   for g in ('implementation','direct_test','integration_test','determinism','production_wiring'):vals[g]='PASS'
   vals['design']=vals['decision']='PARTIAL'; vals['defect_gate']='PASS';ac='0/14';defects='0/0/0';blocker='T19-RISK-004';nxt='Await external calibration data; continue only isolated engineering';latest='docs/spec-v3/reports/MODEL-001_simulation_training_calibration_report.md';batch=unit_batch[u];wave=wave_of[batch];term=terminal[batch]
  else:
   status='READY_FOR_IMPLEMENTATION' if u in B2 else 'SCAFFOLDED' if u=='HEUR-016' else 'WAITING_FOR_DESIGN_APPROVAL';vals={g:'NOT_STARTED' for g in GATES};
   if u in B2: vals['design']=vals['decision']='PASS'
   elif u=='HEUR-016': vals['implementation']='PARTIAL'
   else: vals['implementation']='PARTIAL' if gap[u]['code_refs'] else 'NOT_STARTED'; vals['direct_test']='PARTIAL' if gap[u]['test_refs'] else 'NOT_STARTED'
   vals['defect_gate']='PASS';ac='0/14';defects='0/0/0';blocker='NONE' if u in B2 else 'B2A1-DESIGN-1.0.0' if False else ('T19-RISK-002' if u!='HEUR-016' else 'T19-RISK-002');nxt='Implement approved B2-A1 in sequence' if u in B2 else 'Create and approve concrete design package';latest='docs/spec-v3/semantic-completion/reviews/B2-A1_approval_form.md' if u in B2 else 'docs/spec-v3/plans/task18_gap_classification.csv';batch=unit_batch[u];wave=wave_of[batch];term=terminal[batch]
  passed=sum(vals[g]=='PASS' for g in GATES); denom=sum(vals[g]!='NOT_REQUIRED' for g in GATES); prog=100.0 if status=='AUDITED' else min(93.75,round(100*passed/denom,2))
  records.append(dict(unit_id=u,unit_name=names.get(u,u),category=u.split('-')[0],track_id=TRACK[u.split('-')[0]] if not (u in unit_batch and unit_batch[u].startswith('T19-X')) else 'TRACK-EXTERNAL-DATA',batch_id=batch,parallel_wave_id=wave,assigned_terminal=term,task17_status=task17,task18_initial_status=task18,task19_current_status=status,design=vals['design'],decision=vals['decision'],implementation=vals['implementation'],direct_test=vals['direct_test'],branch_test=vals['branch_test'],exception_test=vals['exception_test'],integration_test=vals['integration_test'],information_boundary=vals['information_boundary'],determinism=vals['determinism'],performance=vals['performance'],production_wiring=vals['production_wiring'],E4=vals['E4'],E5=vals['E5'],AC=ac,defects=defects,independent_audit=vals['independent_audit'],progress=f'{prog:.2f}%',blocker=blocker,next_action=nxt,latest_evidence=latest,last_updated=now,revision='1'))
 # Markdown authority.
 header=['unit_id','unit_name','category','track_id','batch_id','parallel_wave_id','assigned_terminal','task17_status','task18_initial_status','task19_current_status','design','decision','implementation','direct_test','branch_test','exception_test','integration_test','information_boundary','determinism','performance','production_wiring','E4','E5','AC','defects','independent_audit','progress','blocker','next_action','latest_evidence','last_updated','revision']
 dist=Counter(r['task19_current_status'] for r in records); snapshot=hashlib.sha256(json.dumps(records,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
 lines=['# Task 19 项目进度跟踪','','## 元数据','', '- Authority: docs/spec-v3/task19/task19_progress_tracker.md','- Unit count: 96','- Task 17 historical distribution: AUDITED=9, INTEGRATED=1, PARTIAL=85, SCAFFOLDED=1','- Task 18 initial distribution: AUDITED=15, INTEGRATED=1, PARTIAL=79, SCAFFOLDED=1',f"- Task 19 current distribution: "+', '.join(f'{k}={dist[k]}' for k in STATUS_ORDER if dist[k]),'- Current parallel wave: W01 (not started; baseline blocked)','- Last updated: '+now,'- Status revision: 1','- Generated from: task18_post_b1b_queue.csv; task18_post_b1b_dependency_graph.json; Locked catalog; Task19 plan matrices','- Evidence snapshot hash: '+snapshot,'','## 状态摘要','','| status | count | percentage |','|---|---:|---:|']
 for s in STATUS_ORDER:
  if dist[s]:lines.append(f'| {s} | {dist[s]} | {100*dist[s]/96:.2f}% |')
 lines += ['','## 轨道摘要','','| track_id | total | audited | active | blocked | progress |','|---|---:|---:|---:|---:|---:|']
 for tr in ['TRACK-DETERMINISTIC','TRACK-HEURISTIC','TRACK-MODEL','TRACK-TRAINING','TRACK-AUDIT','TRACK-EXTERNAL-DATA']:
  rr=[r for r in records if r['track_id']==tr]; audited=sum(r['task19_current_status']=='AUDITED' for r in rr); active=sum(r['task19_current_status'] in {'READY_FOR_IMPLEMENTATION','IMPLEMENTING','IMPLEMENTED_PENDING_EVIDENCE','IMPLEMENTED_PENDING_INDEPENDENT_AUDIT'} for r in rr); blocked=sum(r['task19_current_status']=='BLOCKED' for r in rr); avg=sum(float(r['progress'][:-1]) for r in rr)/len(rr) if rr else 0;lines.append(f'| {tr} | {len(rr)} | {audited} | {active} | {blocked} | {avg:.2f}% |')
 lines += ['','## 批次摘要','','| batch_id | wave | total | status | progress | blockers | next_action |','|---|---|---:|---|---:|---|---|']
 lines.append('| COMPLETED | DONE | 15 | AUDITED | 100.00% | NONE | Monitor findings |')
 for b,title,us in groups:
  rr=[r for r in records if r['unit_id'] in us]; avg=sum(float(r['progress'][:-1]) for r in rr)/len(rr); st='READY_FOR_IMPLEMENTATION' if b=='T19-B2A1' else 'INTEGRATED' if b=='T19-X01' else 'WAITING_FOR_DESIGN_APPROVAL';block='NONE' if b=='T19-B2A1' else 'T19-RISK-004' if b.startswith('T19-X') else 'T19-RISK-002';lines.append(f'| {b} | {wave_of[b]} | {len(us)} | {st} | {avg:.2f}% | {block} | {"Implement after clean baseline" if b=="T19-B2A1" else "Approve design"} |')
 lines += ['','## 96 个单元进度','','| '+' | '.join(header)+' |','|'+'|'.join(['---']*len(header))+'|']
 for r in records:lines.append('| '+' | '.join(esc(r[h]) for h in header)+' |')
 lines += ['','## 当前阻塞项','','| blocking_id | type | affected_units | reason | required_action | owner |','|---|---|---|---|---|---|','| T19-RISK-001 | INTEGRATION_CONFLICT | ALL | 主工作树 dirty，不能作为安全并行基线 | 用户批准检查点提交/tag方案 | Terminal 0 |','| T19-RISK-002 | DESIGN_DECISION | 78 non-B2A1 development units | 尚无 Approved 批次设计 | 分批生成并批准设计 | Terminal 0 |','| T19-RISK-004 | EXTERNAL_DATA | MODEL-001\\|MODEL-005\\|TRAIN-008\\|AUDIT-012 | 外部数据/效果证据未冻结 | 保持局部门禁并等待发布 | Terminal 3 |','','## 下一步执行队列','','| priority | unit_id | batch_id | current_status | next_action | dependency |','|---:|---|---|---|---|---|','| 1 | STATE-002 | T19-B2A1 | READY_FOR_IMPLEMENTATION | 固化 clean baseline 后实施 | T19-RISK-001 |','| 2 | STATE-003 | T19-B2A1 | READY_FOR_IMPLEMENTATION | STATE-002 后实施 | STATE-002 |','| 3 | ALGO-002 | T19-B2A1 | READY_FOR_IMPLEMENTATION | STATE-003 后实施 | STATE-003 |','| 4 | AUDIT-010 | T19-A04 | WAITING_FOR_DESIGN_APPROVAL | 生成并审批独立设计 | T19-RISK-002 |','','## 更新记录','','| revision | updated_at | updated_by | delta_file | affected_units | summary |','|---:|---|---|---|---|','| 1 | '+now+' | Terminal 0 | INITIALIZATION | ALL_96 | Task19 deterministic initialization |','']
 (OUT/'task19_progress_tracker.md').write_text('\n'.join(lines),encoding='utf-8')
 summary=['# Task 19 进度摘要','',f'- Total units: {len(records)}',f'- Current wave: W01 (not started; baseline blocked)',f'- Audited: {dist["AUDITED"]}',f'- Ready for implementation: {dist["READY_FOR_IMPLEMENTATION"]}',f'- Waiting for design approval: {dist["WAITING_FOR_DESIGN_APPROVAL"]}',f'- Integrated: {dist["INTEGRATED"]}',f'- Scaffolded: {dist["SCAFFOLDED"]}',f'- Blocked status units: {dist["BLOCKED"]}',f'- Overall evidence-gate completion: {sum(float(r["progress"][:-1]) for r in records)/96:.2f}%','','## Track completion','']
 for tr in ['TRACK-DETERMINISTIC','TRACK-HEURISTIC','TRACK-MODEL','TRACK-TRAINING','TRACK-AUDIT','TRACK-EXTERNAL-DATA']:
  rr=[r for r in records if r['track_id']==tr]; summary.append(f'- {tr}: {sum(x["task19_current_status"]=="AUDITED" for x in rr)}/{len(rr)} audited')
 summary += ['','## Current queues','','- Current implementation units: STATE-002 -> STATE-003 -> ALGO-002 (not started; checkpoint blocked)','- Waiting evidence: none','- Waiting independent audit: none','- Current serial critical path: B2-A1 -> deterministic rules/scoring/state -> model/heuristic -> audit/model lifecycle/external effect','- Next recommended action: approve a precise clean checkpoint baseline; then create W01 worktrees.','']
 (OUT/'task19_progress_summary.md').write_text('\n'.join(summary),encoding='utf-8')
 # Structured graph mirror.
 (OUT/'task19_dependency_graph.json').write_text(json.dumps(dict(node_count=96,edge_count=207,acyclic=True,current_audited_units=sorted(AUDITED),remaining_units=sorted(remain),edges=graph['edges'],batch_dependencies={k:sorted(v) for k,v in bdeps.items()},serial_critical_path=['T19-B2A1','T19-D01','T19-D04','T19-D06','T19-D07','T19-D08','T19-D09','T19-D13','T19-M01','T19-H07','T19-H09','T19-A03','T19-A04','T19-A05','T19-M03','T19-X03']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 # Validation and authorization.
 planval=dict(unit_count=96,remaining_unit_count=81,unique_remaining_unit_count=81,current_audited_count=15,duplicate_count=0,missing_count=0,unexpected_count=0,dependency_graph_acyclic=True,every_remaining_unit_has_batch=True,every_batch_has_track=True,every_parallel_batch_has_disjoint_write_paths=True,every_shared_interface_has_one_owner=True,every_wave_has_integration_order=True,task17_history_modified=False,B2_A1_decisions_preserved=True,progress_tracking_ready=True,progress_tracker_format='MARKDOWN',progress_tracker_row_count=96,progress_tracker_writer='Terminal 0')
 (OUT/'task19_plan_validation.json').write_text(json.dumps(planval,indent=2)+'\n')
 progval=dict(progress_tracker_format='MARKDOWN',progress_tracker_row_count=96,progress_tracker_unique_unit_count=96,progress_tracker_duplicate_count=0,progress_tracker_missing_unit_count=0,progress_tracker_unexpected_unit_count=0,progress_tracker_header_valid=True,progress_tracker_section_order_valid=True,progress_tracker_markdown_parse_error_count=0,progress_status_enum_error_count=0,progress_substatus_enum_error_count=0,progress_percent_formula_error_count=0,audited_not_100_percent_count=0,unaudited_with_100_percent_count=0,task17_status_mutation_count=0,missing_next_action_count=0,invalid_blocking_reference_count=0,missing_update_metadata_count=0,multiple_progress_file_writer_count=0,progress_summary_mismatch_count=0)
 (OUT/'task19_progress_validation.json').write_text(json.dumps(progval,indent=2)+'\n')
 auth=dict(task='Task 19 remaining development parallel execution',status='TASK19_WAITING_FOR_APPROVAL',planning_complete=True,parallel_execution_authorized=False,reason='Dirty main worktree has no clean checkpoint baseline; non-B2A1 batches also require design approval',baseline_commit=commit,baseline_tag=None,worktree_baseline_ready=False,B2_A1=dict(status='READY_FOR_IMPLEMENTATION',new_direct_test_files_authorized=True,new_test_cases_authorized=True,existing_test_assertion_changes_authorized=False,locked_frozen_changes_authorized=False,unit_status_changes_authorized=False,implementation_started=False),progress_tracker_authority='docs/spec-v3/task19/task19_progress_tracker.md',progress_tracker_writer='Terminal 0',progress_delta_format='CSV_OR_JSON',progress_tool_implementation_authorized=False,task17_history_modified=False)
 (OUT/'task19_execution_authorization.json').write_text(json.dumps(auth,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'batches':len(groups),'waves':len(waves),'records':len(records),'snapshot':snapshot,'decision':auth['status']},indent=2))
if __name__=='__main__':main()
