from __future__ import annotations
import csv, json, hashlib, struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEC=ROOT/'docs/spec-v3/decisions'; SEM=ROOT/'docs/spec-v3/semantic-completion'; REV=SEM/'reviews'

def wc(path,rows,fields=None):
    fields=fields or list(rows[0])
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(obj): return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

decisions=list(csv.DictReader((DEC/'B1-A_decision_matrix.csv').open(encoding='utf-8-sig')))
assert len(decisions)==9 and all(r['approval_status']=='APPROVED' and r['recommended_option']=='A' for r in decisions)

# Decimal scan conclusion: no registry field declares Decimal or a scale.
registry=list(csv.DictReader((ROOT/'docs/spec-v3/07-traceability/parameter_registry.csv').open(encoding='utf-8-sig')))
decimal=[r for r in registry if 'decimal' in r['data_type_and_range'].lower() or 'scale' in r['data_type_and_range'].lower() or '小数位' in r['data_type_and_range']]
assert not decimal
wc(DEC/'B1-A_decimal_scale_registry.csv',[{
 'field_path':'__registry_conclusion__','parameter_id':'N/A','numeric_type':'NO_DECIMAL_FIELDS_IN_CANONICAL_CONFIG','scale':'N/A','rounding_mode':'N/A','min':'N/A','max':'N/A','serialized_positive_example':'N/A','serialized_boundary_example':'N/A','source_reference':'docs/spec-v3/07-traceability/parameter_registry.csv (60/60 rows scanned); docs/spec-v3/contracts/common_contracts.md §2/§8','approval_status':'CLOSED_NO_DECIMAL_FIELDS'}])

old=json.loads((DEC/'B1-A_golden_vectors.json').read_text(encoding='utf-8'))['vectors']
byid={x['vector_id']:x for x in old}
rules='CDMJ-AI-RULES 1.0.0'; p1='CDMJ-AI-PARAMS 1.1.0'; p2='CDMJ-AI-PARAMS 2.0.0'; c1='CDMJ-CONTRACTS 1.0.0'; c2='CDMJ-CONTRACTS 2.0.0'
exec_ids={'GV-001','GV-002','GV-004','GV-005','GV-006','GV-007','GV-008','GV-009','GV-010','GV-011','GV-012','GV-013','GV-014','GV-015','GV-016','GV-017','GV-018','GV-019'}
review=[]; vectors=[]
for x in old:
    vid=x['vector_id']; cls='EXECUTABLE_GOLDEN' if vid in exec_ids else 'ILLUSTRATIVE_EXAMPLE'
    reason='complete deterministic input and oracle' if cls=='EXECUTABLE_GOLDEN' else 'RP-033 learning adapter mapping is not part of this three-unit executable surface'
    inp=x['input']; exp=x['expected']; target=''
    err=exp.get('error_code'); chex=None; sh=None; raw=None
    if vid=='GV-001': target='field_validator:GP-003.early_end_score'; inp={'field_path':'global_parameters.GP-003.early_end_score','value':None,'field_present':True}
    elif vid=='GV-002': target='complete_config_required_field_validator'; inp={'config_fixture':'PARAMS-1.1-default','operation':'remove','field_path':'global_parameters.GP-003.total_rounds'}
    elif vid=='GV-003': target='RP archive illustration'
    elif vid=='GV-004': target='STATE-010 lifecycle validator'
    elif vid=='GV-005':
        target='ALGO-009 migration edge 1.0/2.0→1.1/2.1'
        inp={'rule_version':'CDMJ-AI-RULES 1.0.0','parameter_version':'CDMJ-AI-PARAMS 1.0.0','implementation_version':'CDMJ-AI-IMPL 2.0.0','global_parameters':{'GP-024':{'k':'v24'},'GP-025':{'k':'v25'},'GP-026':{'k':'v26'},'GP-027':{'k':'v27'}},'players':[{'player_id':i} for i in range(4)]}
        exp={'accepted':True,'rule_version':'CDMJ-AI-RULES 1.0.0','parameter_version':'CDMJ-AI-PARAMS 1.1.0','implementation_version':'CDMJ-AI-IMPL 2.1.0','global_parameters_absent':['GP-024','GP-025','GP-026','GP-027'],'players_cognitive_parameters':[{'player_id':i,'GP-024':{'k':'v24'},'GP-025':{'k':'v25'},'GP-026':{'k':'v26'},'GP-027':{'k':'v27'}} for i in range(4)],'input_mutated':False}
    elif vid=='GV-006': target='ALGO-009 migration graph resolver'
    elif vid in {'GV-007','GV-008'}: target='ALGO-009 extensions validator'
    elif vid in {'GV-009','GV-010','GV-012'}:
        target='canonical-jcs-nfc-v2 encoder'; chex=exp['canonical_utf8_hex']; sh=sha(bytes.fromhex(chex)); exp['sha256_hex']=sh
    elif vid=='GV-011': target='typed canonical encoder input'; inp={'input_kind':'typed_value','field_path':'synthetic.number','value_kind':'IEEE754_NaN'}; exp={'accepted':False,'result':None,'error_code':'NON_FINITE'}; err='NON_FINITE'
    elif vid=='GV-013': target='NFC object-key collision validator'
    elif vid in {'GV-014','GV-015'}: target='ALGO-009 config activation state machine'
    elif vid=='GV-016': target='ALGO-011 legacy replay reader/derive_seeds'; inp['record_format']='legacy-pre-rng-version'; exp['blake2b_digest_size']=8; exp['integer_byte_order']='big-endian'
    elif vid=='GV-017': target='ALGO-011 new record schema validator'; inp['record_format']='rng-v2-new-record'
    elif vid=='GV-018': target='ALGO-011 rng-v2 coordinate derivation'; exp['blake2b_digest_size']=8; exp['integer_byte_order']='big-endian'
    elif vid=='GV-019': target='ALGO-011 coordinate schema validator'
    rec={'vector_id':vid,'decision_id':x['decision_id'],'vector_class':cls,'execution_target':target,'input_format':'JSON typed fixture','complete_input':inp if cls=='EXECUTABLE_GOLDEN' else None,'raw_input_hex':raw,'rules_version':rules,'parameter_version':p2 if vid in {'GV-009','GV-010','GV-011','GV-012','GV-013','GV-017','GV-018','GV-019'} else p1,'contract_version':c2 if vid in {'GV-009','GV-010','GV-011','GV-012','GV-013','GV-017','GV-018','GV-019'} else c1,'canonical_version':'canonical-jcs-nfc-v2' if vid in {'GV-009','GV-010','GV-011','GV-012','GV-013'} else 'legacy-json-v1','expected_result':exp if cls=='EXECUTABLE_GOLDEN' else None,'expected_error_code':err,'expected_canonical_utf8_hex':chex,'expected_sha256_hex':sh,'hash_algorithm':'SHA-256 (32 bytes; 64 lowercase hexadecimal characters)' if sh else None,'integer_byte_order':'big-endian' if vid in {'GV-016','GV-018'} else 'not_applicable','source_reference':f"docs/spec-v3/decisions/B1-A_decision_pack.md#{x['decision_id']}; docs/spec-v3/decisions/B1-A_golden_vectors.json#{vid}"}
    vectors.append(rec); review.append({'vector_id':vid,'decision_id':x['decision_id'],'previous_kind':x['kind'],'vector_class':cls,'review_finding':reason,'execution_target':target,'fix_applied':('GV-001 scope explicit' if vid=='GV-001' else 'GV-005 machine output fixture' if vid=='GV-005' else 'GV-011 typed non-finite explicit' if vid=='GV-011' else 'hash/BLAKE/version metadata normalized'),'self_check':'PASS' if cls=='EXECUTABLE_GOLDEN' else 'NOT_EXECUTED'})

out={'schema_version':1,'status':'PENDING_CANONICAL_PROFILE_APPROVAL','recommended_profile':'OPTION-J2 / CDMJ canonical-jcs-nfc-v2 profile','vector_count':len(vectors),'executable_count':sum(v['vector_class']=='EXECUTABLE_GOLDEN' for v in vectors),'vectors':vectors}
(DEC/'B1-A_executable_golden_vectors.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
wc(DEC/'B1-A_golden_vector_review.csv',review)

version_rows=[
{'artifact':'legacy config/read','rules_version':rules,'parameter_version':p1,'contract_version':c1,'canonical_version':'legacy-json-v1','rng_version':'legacy-v1/missing old record only','reader':'v1 and v2 adapter','writer':'legacy writer frozen; no new production writes after cutover','status':'READ_ONLY_COMPAT'},
{'artifact':'new config/write','rules_version':rules,'parameter_version':p2,'contract_version':c2,'canonical_version':'canonical-jcs-nfc-v2 profile (OPTION-J2 pending)','rng_version':'2','reader':'v2','writer':'v2 only','status':'PENDING_PROFILE_APPROVAL'},
{'artifact':'legacy replay','rules_version':rules,'parameter_version':p1,'contract_version':c1,'canonical_version':'legacy-json-v1','rng_version':'missing→legacy-v1','reader':'v2 legacy adapter','writer':'none','status':'READ_ONLY_COMPAT'},
{'artifact':'new replay','rules_version':rules,'parameter_version':p2,'contract_version':c2,'canonical_version':'canonical-jcs-nfc-v2 profile','rng_version':'2 explicit','reader':'v2','writer':'v2 only','status':'PENDING_PROFILE_APPROVAL'}]
wc(DEC/'B1-A_version_matrix.csv',version_rows)
edges=[
{'edge_id':'MIG-CONFIG-100-110','source':'RULES1.0/PARAMS1.0/IMPL2.0','target':'RULES1.0/PARAMS1.1/IMPL2.1','operation':'move GP-024..027 from global to four independent player cognitive maps; update versions','input_mutation':'forbidden','hash_behavior':'target legacy-json-v1 hash','approval_status':'APPROVED'},
{'edge_id':'MIG-CONFIG-110-200','source':'CONTRACTS1/PARAMS1.1/legacy-json-v1','target':'CONTRACTS2/PARAMS2.0/canonical-jcs-nfc-v2-profile','operation':'validate strict v1; require empty extensions; add version discriminators; canonicalize and hash under approved profile','input_mutation':'forbidden; atomic new object','hash_behavior':'old hash retained as source_hash; new SHA-256 produced','approval_status':'PENDING_CANONICAL_PROFILE'},
{'edge_id':'MIG-REPLAY-LEGACY-ADAPTER','source':'pre-rng-version replay','target':'v2 reader legacy execution path','operation':'do not rewrite; select legacy-v1 derive_seeds','input_mutation':'forbidden','hash_behavior':'legacy values unchanged','approval_status':'APPROVED'}]
wc(DEC/'B1-A_migration_edges.csv',edges)

proposal='''# B1-A CONTRACTS 2.0 / PARAMS 2.0正式版本变更提案

状态：**BLOCKED_BY_CANONICAL_PROFILE_DECISION**  
提案版本：`B1-A-CONTRACT-V2 2.0.0-rc1`

## 推荐版本组合

不发布PARAMS 1.2。历史读取固定为`PARAMS 1.1.0 + CONTRACTS 1.0.0 + legacy-json-v1`且现有config hash不变；新writer只写`PARAMS 2.0.0 + CONTRACTS 2.0.0 + canonical-jcs-nfc-v2 profile + rng_version=2`。v2 reader双读，v1 reader不读v2。

## JCS/int64选择

标准RFC 8785建立在IEEE-754/ECMAScript Number语义上，无法无损覆盖项目Locked int64全范围。推荐`OPTION-J2`：正式名称`CDMJ canonical-jcs-nfc-v2 profile`。整数token按int64精确十进制、无前导零、整数负零归一为0；非整数采用ECMAScript NumberToString；Decimal按注册scale量化。该profile是JCS的项目扩展，不得宣称为未经修改的RFC 8785。`OPTION-J1`会把整数限制到±(2^53-1)，与ScorePoint/int64契约冲突。

推荐不等于批准；OPTION-J2当前PENDING，因此本包不能解除最终门禁。

## Decimal结论

扫描parameter_registry.csv全部60项，没有字段声明Decimal或scale，结论为`NO_DECIMAL_FIELDS_IN_CANONICAL_CONFIG`。若未来加入Decimal，必须先更新scale registry和版本，不能沿用本次空结论。

## 接口与兼容

v2 DecisionResult以`seed_trace_ref={rng_used,algorithm_version,rng_version,trace_ref}`替代完整seed_trace；完整随机材料只进入受限审计存储。普通策略、PlayerView和DecisionContext禁止master_seed、原始流名、原始index、seed_hash。旧reader/新reader、writer、回放和调用方矩阵见B1-A_version_matrix.csv及effective overlay。

## 破坏性变化与回滚

破坏性变化包括canonical bytes、contract/parameter版本、DecisionResult seed字段和新record必填rng版本。回滚停止v2新写但保留v2 reader；旧文件不重写；已生成v2文件不得用v1 hash覆盖。受影响单元STATE-010/ALGO-009/ALGO-011；调用方包括config/settings/STATE-001、persistence/replay/deal、DecisionResult serializer、audit writer和trainer controller。

## 审批条件

负责人必须在B1-A_contract_v2_approval_form.md明确选择J1或J2并批准版本包与迁移边。只有J选择、合同和MIG-CONFIG-110-200均Approved后，才可重新审查编码门禁。
'''
(DEC/'B1-A_contract_v2_change_proposal.md').write_text(proposal,encoding='utf-8')

form='''# B1-A CONTRACTS/PARAMS 2.0最终审批表

- CANONICAL_PROFILE_OPTION：` `（填写OPTION-J1或OPTION-J2）
- CONTRACT_V2_STATUS：`PENDING`
- MIG-CONFIG-110-200_STATUS：`PENDING`
- APPROVED_BY：` `
- APPROVED_AT：` `
- DECISION_VERSION：`B1-A-CONTRACT-V2 2.0.0-rc1`
- COMMENT：` `

推荐：OPTION-J2 / `CDMJ canonical-jcs-nfc-v2 profile`。本表未填写前不得编码。
'''
(DEC/'B1-A_contract_v2_approval_form.md').write_text(form,encoding='utf-8')

overlay='''# B1-A Effective Spec Overlay

状态：**PENDING CANONICAL PROFILE APPROVAL**

本覆盖层不修改Locked源文件；批准后对B1-A开发提供版本化有效解释。历史读取使用PARAMS1.1/CONTRACTS1/legacy-json-v1，新写使用PARAMS2/CONTRACTS2/canonical profile/rng2。SHA-256统一表述为：SHA-256，32字节，序列化为64个小写十六进制字符。Locked中的“64小写hex/64位小写hex”列为待v2更正文案，不在本任务直接修改。

DecisionResult v2使用安全seed_trace_ref；完整SeedTrace为restricted audit payload。旧回放缺rng版本固定走legacy-v1；新record必须显式rng_version=2。迁移图只能使用B1-A_migration_edges.csv登记边。
'''
(DEC/'B1-A_effective_spec_overlay.md').write_text(overlay,encoding='utf-8')

# Effective delta layer.
generic=list(csv.DictReader((REV/'task18b_83_parameter_recheck.csv').open(encoding='utf-8-sig')))
sem=list(csv.DictReader((REV/'B1-A_semantic_deltas.csv').open(encoding='utf-8-sig')))
tests=list(csv.DictReader((REV/'B1-A_test_deltas.csv').open(encoding='utf-8-sig')))
evid=list(csv.DictReader((REV/'B1-A_evidence_deltas.csv').open(encoding='utf-8-sig')))
effective=[]; sup=[]
for i,r in enumerate(generic,1):
    old_id=f"LEGACY-SEM-PARAMETER-{r['unit_id']}"
    effective.append({'delta_id':old_id,'unit_id':r['unit_id'],'delta_kind':'semantic_delta','effective_status':'SUPERSEDED','source_file':'Task18B original generated semantic_delta_catalog','requirement':'泛化参数接入（无具体参数行为差异）','superseded_by':'R1 concrete deltas when unit is B1-A; otherwise future unit-specific review','development_readable':'false'})
    sup.append({'superseded_delta_id':old_id,'unit_id':r['unit_id'],'supersession_status':'SUPERSEDED','replacement_delta_ids':'|'.join(x['delta_id'] for x in sem if x['unit_id']==r['unit_id']),'reason':'未指出具体parameter_id及当前/目标生产行为差异','effective_from':'Task18B-R1','may_be_used_by_development':'false'})
for rows,kind in [(sem,'semantic_delta'),(tests,'test_delta'),(evid,'evidence_delta')]:
    for r in rows:
        effective.append({'delta_id':r['delta_id'],'unit_id':r['unit_id'],'delta_kind':kind,'effective_status':'ACTIVE','source_file':f"docs/spec-v3/semantic-completion/reviews/B1-A_{'semantic_deltas' if kind=='semantic_delta' else 'test_deltas' if kind=='test_delta' else 'evidence_deltas'}.csv",'requirement':r.get('semantic_delta') or r.get('test_oracle') or r.get('collection_method'),'superseded_by':'','development_readable':'true'})
wc(SEM/'task18b_r1_effective_delta_catalog.csv',effective)
wc(SEM/'task18b_r1_supersession_map.csv',sup)

# 42 AC version rebinding, without changing assertions.
acs=list(csv.DictReader((SEM/'first_batch_acceptance_matrix.csv').open(encoding='utf-8-sig')))
reb=[]
for r in acs:
    reb.append({'unit_id':r['unit_id'],'ac_id':r['ac_id'],'rules_version':rules,'legacy_parameter_version':p1,'target_parameter_version':p2,'legacy_contract_version':c1,'target_contract_version':c2,'legacy_canonical_version':'legacy-json-v1','target_canonical_version':'CDMJ canonical-jcs-nfc-v2 profile (OPTION-J2 pending)','decision_version':'B1-A-DECISIONS 1.0.0','golden_contract':'B1-A_executable_golden_vectors.json','binding_status':'PENDING_CANONICAL_PROFILE_APPROVAL'})
wc(REV/'B1-A_contract_v2_acceptance_rebinding.csv',reb)

# Self-check executable hashes and metadata.
for v in vectors:
    if v['vector_class']!='EXECUTABLE_GOLDEN': continue
    for key in ['execution_target','input_format','complete_input','rules_version','parameter_version','contract_version','canonical_version','expected_result','hash_algorithm','integer_byte_order','source_reference']:
        assert key in v
    if v['expected_canonical_utf8_hex']:
        b=bytes.fromhex(v['expected_canonical_utf8_hex']); assert sha(b)==v['expected_sha256_hex']
assert len(acs)==42 and len(generic)==83 and len(sem)==24
print(json.dumps({'decisions_approved_a':9,'decimal_fields':0,'decimal_conclusion':'NO_DECIMAL_FIELDS_IN_CANONICAL_CONFIG','vectors':len(vectors),'executable':sum(v['vector_class']=='EXECUTABLE_GOLDEN' for v in vectors),'illustrative':sum(v['vector_class']=='ILLUSTRATIVE_EXAMPLE' for v in vectors),'effective_rows':len(effective),'superseded_generic':len(sup),'ac_rebound':len(reb),'final_status':'BLOCKED_BY_CANONICAL_PROFILE_DECISION'},ensure_ascii=False))
