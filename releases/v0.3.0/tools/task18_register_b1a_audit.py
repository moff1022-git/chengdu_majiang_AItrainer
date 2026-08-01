"""Register the approved B1-A audit delta without modifying Task 17 history."""
from __future__ import annotations
import csv, hashlib, json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'docs/spec-v3/audit'
SOURCE=AUDIT/'unit_gap_matrix_v3.csv'
PROMOTED=('STATE-010','ALGO-009','ALGO-011')
EVIDENCE={
 'STATE-010':'docs/spec-v3/reports/B1-A_acceptance_audit_matrix.csv; tests/spec_v3/test_b1a_state010.py; docs/spec-v3/evidence/task18b_b1a/B1-A_runtime_evidence.json',
 'ALGO-009':'docs/spec-v3/reports/B1-A_acceptance_audit_matrix.csv; tests/spec_v3/test_b1a_algo009.py; docs/spec-v3/evidence/task18b_b1a/B1-A_golden_execution.json',
 'ALGO-011':'docs/spec-v3/reports/B1-A_acceptance_audit_matrix.csv; tests/spec_v3/test_b1a_algo011.py; docs/spec-v3/evidence/task18b_b1a/B1-A_E5_manifest.json',
}
def write_csv(path, rows, fields):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def main():
    source=list(csv.DictReader(SOURCE.open(encoding='utf-8-sig')))
    assert len(source)==96 and len({r['unit_id'] for r in source})==96
    by_id={r['unit_id']:r for r in source}
    assert all(by_id[u]['current_status']=='PARTIAL' for u in PROMOTED)
    ac=list(csv.DictReader((ROOT/'docs/spec-v3/reports/B1-A_acceptance_audit_matrix.csv').open(encoding='utf-8-sig')))
    assert len(ac)==42 and all(r['result']=='PASS' for r in ac)
    manifest=json.loads((ROOT/'docs/spec-v3/evidence/task18b_b1a/B1-A_E5_manifest.json').read_text(encoding='utf-8'))
    assert manifest['audit_result']=='AUDITED_CANDIDATE' and manifest['ac_pass']==42
    delta=[]; current=[]
    for r in source:
        uid=r['unit_id']; old=r['current_status']; new='AUDITED' if uid in PROMOTED else old
        current.append({'unit_id':uid,'unit_name':r['unit_name'],'category':r['category'],'task17_status':old,'current_status':new,'status_source':'TASK18-B1A-AUDIT-DELTA-1' if uid in PROMOTED else 'TASK17-REBASELINE','evidence_refs':EVIDENCE.get(uid,r.get('runtime_refs','')),'effective_date':'2026-07-30'})
        if uid in PROMOTED:
            delta.append({'unit_id':uid,'previous_status':old,'new_status':new,'decision':'APPROVED','authority':'project_owner_user: execute tasks 1-2','ac_result':'14/14 PASS','four_evidence_classes':'PASS','evidence_refs':EVIDENCE[uid],'effective_date':'2026-07-30','historical_files_modified':'false'})
    dist=Counter(r['current_status'] for r in current)
    assert dist==Counter({'PARTIAL':82,'AUDITED':12,'INTEGRATED':1,'SCAFFOLDED':1})
    assert sum(dist.values())==96
    write_csv(AUDIT/'task18_b1a_audit_status_delta.csv',delta,list(delta[0]))
    write_csv(AUDIT/'task18_current_96_unit_status.csv',current,list(current[0]))
    categories=defaultdict(Counter)
    for r in current: categories[r['category']][r['current_status']]+=1
    payload={'authority':'Task 18 current status = immutable Task 17 baseline + approved B1-A delta','effective_date':'2026-07-30','unit_count':96,'status_distribution':dict(sorted(dist.items())),'audited_units':[r['unit_id'] for r in current if r['current_status']=='AUDITED'],'promoted_units':list(PROMOTED),'task17_history_modified':False,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'category_distribution':{k:dict(sorted(v.items())) for k,v in sorted(categories.items())},'matrix':'docs/spec-v3/audit/task18_current_96_unit_status.csv','delta':'docs/spec-v3/audit/task18_b1a_audit_status_delta.csv'}
    (AUDIT/'task18_current_96_unit_status.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Task 18当前96单元权威审计状态','',f'状态：**CURRENT / APPROVED**  ','生效日期：2026-07-30  ','组成：Task 17不可变历史基线 + `TASK18-B1A-AUDIT-DELTA-1`。','','## 当前分布','', '| 状态 | 数量 |','|---|---:|']+[f'| {s} | {dist[s]} |' for s in ('AUDITED','INTEGRATED','PARTIAL','SCAFFOLDED')]+['| 合计 | 96 |','','## 本次增量','','`STATE-010`、`ALGO-009`、`ALGO-011`由PARTIAL登记为AUDITED。三单元分别通过AC-01～AC-14，共42/42 PASS；代码、直接/边界/集成测试、生产运行和E5追溯证据闭环。','','## 当前12个AUDITED','','`'+'`、`'.join(payload['audited_units'])+'`。','','## 历史边界','','未修改`task17_96_unit_audit_clarification.md`、`unit_gap_matrix_v3.csv`或`unit_rebaseline_summary.json`。引用“Task 17状态”时仍为9/1/85/1；引用“当前状态”时必须使用本文件及Task 18 current矩阵。']
    (AUDIT/'task18_current_96_unit_status_summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'delta':len(delta),'distribution':dict(dist),'audited':payload['audited_units']},ensure_ascii=False))
if __name__=='__main__': main()
