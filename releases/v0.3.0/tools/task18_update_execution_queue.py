"""Advance Task 18 queue after the approved B1-A audit delta."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PLANS=ROOT/'docs/spec-v3/plans'
SOURCE=PLANS/'task18_execution_queue.json'
def main():
    data=json.loads(SOURCE.read_text(encoding='utf-8'))
    original=list(data['recommended_order'])
    data['task']='Task 18 current executable queue'
    data['updated_on']='2026-07-30'
    data['queue_version']='TASK18-QUEUE-2'
    data['status_authority']='docs/spec-v3/audit/task18_current_96_unit_status.json'
    data['historical_task18a_baseline']=data.pop('authoritative_status_unchanged')
    data['current_status_distribution']={'AUDITED':12,'INTEGRATED':1,'PARTIAL':82,'SCAFFOLDED':1,'BLOCKED':0}
    data['current_test_baseline']={'python':'3.12.10','tests':423,'passed':423,'failed':0,'skipped':0,'time_seconds':181.87}
    data['completed_batches']=['B1-A']
    data['completed_batch_evidence']={'B1-A':{'unit_ids':data['batch_unit_ids']['B1-A'],'audit_result':'42/42 PASS','status_delta':'docs/spec-v3/audit/task18_b1a_audit_status_delta.csv','e5_manifest':'docs/spec-v3/evidence/task18b_b1a/B1-A_E5_manifest.json','full_regression':'423 passed'}}
    data['immediately_executable_batches']=['B1-B']
    data['dependency_blocked_batches']=[b for b in data['dependency_blocked_batches'] if b!='B1-B']
    data['batch_status']={b:('COMPLETED' if b=='B1-A' else 'IMMEDIATELY_EXECUTABLE' if b=='B1-B' else 'EXTERNAL_DATA_GATED' if b in data['external_data_gated_batches'] else 'DEPENDENCY_BLOCKED') for b in original}
    data['entry_criteria']['B1-B']='B1-A三个单元已按Task18当前状态独立AUDITED；STATE-001/STATE-011/STATE-004规格Locked；工作树已保护；开始前建立本批语义差距和接口影响基线'
    data['recommended_order']=['B1-B','B4-DATA-MODEL001']+[b for b in original if b not in {'B1-A','B1-B','B4-DATA-MODEL001'}]
    data['parallel_groups']['P1']=[b for b in data['parallel_groups']['P1'] if b!='B1-A']
    data['next_batch']={'batch_id':'B1-B','unit_ids':['STATE-001','STATE-011','STATE-004'],'dependency_batches':['B1-A'],'dependency_status':'SATISFIED','implementation_authorized':False,'required_next_action':'先执行B1-B语义/接口复核并形成Approved实现设计'}
    target=PLANS/'task18_execution_queue_current.json'
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    summary='''# Task 18当前执行队列\n\n状态：**B1-A COMPLETED；B1-B IMMEDIATELY_EXECUTABLE FOR DESIGN REVIEW**  \n版本：`TASK18-QUEUE-2`\n\n## 队列变化\n\n- `B1-A`已完成：STATE-010、ALGO-009、ALGO-011均为当前AUDITED，42/42 AC，全量423 passed。\n- `B1-B`的唯一批次依赖B1-A已满足，从dependency-blocked移动为immediately-executable。\n- B1-B单元：`STATE-001`、`STATE-011`、`STATE-004`。\n- B1-B尚未取得本批Approved语义实现设计，因此“立即可执行”仅授权启动设计复核，不自动授权编码。\n- MODEL-001外部数据轨继续与确定性主链并行，不阻断B1-B。\n\n## 当前队列\n\n| 集合 | 批次 |\n|---|---|\n| completed | B1-A |\n| immediately executable | B1-B |\n| external data gated | B4-DATA-MODEL001、B4-B、B6-C |\n| dependency blocked | 其余18个批次 |\n\n## B1-B入口\n\n先对STATE-001、STATE-011、STATE-004逐单元比较Locked语义、当前实现、具体semantic/test/evidence delta和Frozen接口影响；只有设计Approved且无接口阻断后才编码。\n\nTask18A原始队列文件保持为历史规划输入；当前执行以`task18_execution_queue_current.json`为准。\n'''
    (PLANS/'task18_execution_queue_current.md').write_text(summary,encoding='utf-8')
    print(json.dumps({'completed':data['completed_batches'],'immediate':data['immediately_executable_batches'],'next':data['next_batch']},ensure_ascii=False))
if __name__=='__main__': main()
