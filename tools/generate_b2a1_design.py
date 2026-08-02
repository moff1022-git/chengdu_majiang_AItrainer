from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/spec-v3/semantic-completion/reviews"
PARAMS = ROOT / "docs/spec-v3/07-traceability/parameter_registry.csv"
UNITS = ("STATE-002", "STATE-003", "ALGO-002")

SEM = {
"STATE-002": [
("01","Single authoritative owner and capability-checked read/write API"),("02","Versioned RoundState DTO, schema/migration metadata and canonical validation"),("03","Deep immutable committed snapshots and no mutable authority references"),("04","state_version CAS with success +1 and reject unchanged"),("05","event_id ledger: exact duplicate idempotency, payload conflict and late-event rejection"),("06","prepare-validate-commit-audit-outbox transaction with byte-exact rollback"),("07","phase/terminal authorization, legacy v5 compatible adapter and commit-only consumers"),("08","PlayerView-only policy projection, restricted audit hashes and deterministic fingerprint")],
"STATE-003": [
("01","Versioned PlayerRoundState DTO and actor/phase/event validation"),("02","draw/discard/dingque mutation contracts with exact physical ownership transfer"),("03","pong/ming-gang/an-gang/jia-gang atomic hand/meld/discard mutation"),("04","qiang-gang provisional upgrade, cancellation or commit contract"),("05","pass-hu state creation and approved reset trigger contract"),("06","first/multi-hu order, active-set exit and terminal player state"),("07","108-tile conservation, uniqueness, canonical ordering and exact rollback through STATE-002"),("08","owner/opponent PlayerView projections, audit hashes and deterministic event ordering")],
"ALGO-002": [
("01","Versioned pure request/result DTO and canonical 27-count normalization"),("02","Canonical standard decomposition and standard shanten formula"),("03","Seven-pairs decomposition/shanten with open-meld N/A rule"),("04","Global minimum shanten, win=-1 and approved tie semantics"),("05","Fourteen-tile discard-to-shanten map for every distinct discard face"),("06","All 27 improving faces, ukeire face set/count and zero-error invariants"),("07","Wait-shape classification and duplicate-decomposition elimination"),("08","Canonical ordering, full error taxonomy, P95<=5ms and no authority/RNG/oracle access")],
}

TESTS = {
"STATE-002":[("01","Direct DTO/capability/snapshot/phase/terminal/legacy-v5 matrix"),("02","Duplicate/late/conflicting event and 100-way CAS concurrency matrix"),("03","Fault at every prepare/validate/commit/audit/outbox boundary with exact rollback"),("04","100 repeat, fresh-process, container-order and hidden-poison determinism")],
"STATE-003":[("01","Every event-to-field mutation row with phase/actor/count/ownership assertions"),("02","Duplicate tile, invalid meld/status/hu-order, illegal actor/phase and terminal rejection"),("03","STATE-002 transactional fault injection and full 108-tile conservation rollback"),("04","Multi-hu/order permutations, 100 repeats and four-seat visibility perturbations")],
"ALGO-002":[("01","Locked standard/seven-pairs/combined formula goldens including tie and N/A"),("02","13/14/open-meld/dingque/count/null/type/error boundary matrix"),("03","Discard map, 27-face improving set, ukeire and every wait-shape golden"),("04","100 repeat/fresh-process/order tests plus P95<=5ms benchmark and forbidden-access scan")],
}

EVID = {u:[("01","Four production-path E4 records: NORMAL, BOUNDARY, HARD_FAILURE, DETERMINISM"),("02","Per-delta E5 trace with resolvable E4 IDs, AC references, symbols and SHA-256 artifacts")] for u in UNITS}

DECISIONS = [
("B2A1-DEC-001","STATE-002 canonical authority DTO/schema/migration version","A: new additive immutable DTO v1 + v5 adapter","B: freeze legacy GameState directly","C: replace GameState schema","A","STATE-002|STATE-003"),
("B2A1-DEC-002","Capability representation and owner placement","A: store-owned opaque read/write capability tokens","B: caller-name allowlist","C: unrestricted internal access","A","STATE-002"),
("B2A1-DEC-003","Duplicate versus late/conflicting event error mapping","A: same payload returns original; changed payload INVALID_EVENT; stale version VERSION_CONFLICT","B: every duplicate rejects","C: every duplicate succeeds","A","STATE-002|STATE-003"),
("B2A1-DEC-004","Audit/outbox failure boundary after authority commit","A: audit atomic with commit; outbox retry after commit","B: both atomic","C: both best effort","A","STATE-002"),
("B2A1-DEC-005","Qiang-gang representation","A: provisional jia-gang transaction committed only after response resolution","B: commit then compensating rollback","C: mutate legacy object in place","A","STATE-003"),
("B2A1-DEC-006","Pass-hu reset trigger and value threshold payload","A: bind exactly to approved GP-009 mode and explicit candidate value","B: always reset on own draw","C: reset each turn","A","STATE-003"),
("B2A1-DEC-007","Multi-hu hu_order semantics","A: deterministic seat/event sequence with unique ordinal","B: equal ordinal for same event","C: response arrival order","A","STATE-003"),
("B2A1-DEC-008","ALGO-002 facade/formula version identifiers","A: additive analyze_hand_v1 facade preserving shanten wrapper","B: change shanten return type","C: replace win_check","A","ALGO-002"),
("B2A1-DEC-009","Canonical decomposition and tie ordering","A: lexicographic normalized group tuples; standard before seven-pairs only in display list","B: DFS discovery order","C: shortest serialized form","A","ALGO-002"),
("B2A1-DEC-010","Dingque handling in shanten and improving faces","A: reject winning/tenpai interpretation while missing-suit count >0 and compute discard burden explicitly","B: remove missing suit before formula","C: ignore dingque","A","ALGO-002"),
("B2A1-DEC-011","Ukeire quantity meaning without visibility input","A: return improving face set only; count is number of faces 0..27","B: assume four copies per face","C: accept visible counts","A","ALGO-002"),
("B2A1-DEC-012","STATE-003 PlayerView reveal for an-gang/terminal","A: defer entirely to GP-021/RULE-016 projector","B: expose physical IDs","C: expose all at terminal","A","STATE-003")]

INTERFACES = [
("GameState","STATE-002|STATE-003","COMPATIBLE_ADAPTER","Legacy mutable v5 remains; adapter imports/exports validated snapshots; never policy-visible"),
("PlayerState","STATE-003","COMPATIBLE_ADAPTER","Legacy mutable fields map to additive immutable PlayerRoundState DTO"),
("RoundRuntime","STATE-002","REUSE_AS_IS","Policy RP lifecycle remains separate and consumes PlayerView events only; never authority owner"),
("PlayerViewV2","STATE-002|STATE-003","REUSE_AS_IS","Only existing whitelist projector may cross policy boundary"),
("apply_event","STATE-002|STATE-003","ADDITIVE_INTERFACE","Add authority transaction entrypoint; do not repurpose RoundRuntime.apply_event"),
("shanten","ALGO-002","COMPATIBLE_ADAPTER","Keep scalar legacy wrapper over approved versioned pure facade"),
("win_check","ALGO-002","REUSE_AS_IS","Consumer/cross-check only; no return-type change"),
("hand_analyzer","ALGO-002","COMPATIBLE_ADAPTER","Consume ALGO-002 result from own visible hand only"),
("legal_actions","STATE-003|ALGO-002","REUSE_AS_IS","Consumer of committed state/results; does not own mutation or algorithm")]

def write_csv(name, rows, fields):
    with (BASE/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def main():
    BASE.mkdir(parents=True,exist_ok=True)
    sem=[]
    for u in UNITS:
        for n,text in SEM[u]: sem.append(dict(unit_id=u,delta_id=f"SEM-{u}-{n}",semantic_target=text,locked_source="unit card §§3-20",current_gap="Candidate implementation is not an isolated approved v3 contract",interface_class="ADDITIVE_INTERFACE" if n in {'01','02'} else "COMPATIBLE_ADAPTER",decision_ids="|".join(d[0] for d in DECISIONS if u in d[6]),acceptance_ids=f"AC-{u}-{int(n):02d}",result="APPROVED"))
    write_csv('B2-A1_semantic_deltas.csv',sem,list(sem[0]))
    tests=[]
    for u in UNITS:
        for n,text in TESTS[u]: tests.append(dict(unit_id=u,delta_id=f"TEST-{u}-{n}",test_requirement=text,exact_oracle="All listed fields/errors/hashes equal; rejection leaves version and canonical snapshot byte-identical",references=f"SEM-{u}-01..08",result="APPROVED"))
    write_csv('B2-A1_test_deltas.csv',tests,list(tests[0]))
    ev=[]
    for u in UNITS:
        for n,text in EVID[u]: ev.append(dict(unit_id=u,delta_id=f"EVID-{u}-{n}",evidence_requirement=text,required_fields="unit_id|scenario_id|production_call_site|input_hash|state_before|intermediate|state_after|accepted|error_code|version_before|version_after|output_hash|latency_us|artifact_sha256",result="APPROVED"))
    write_csv('B2-A1_evidence_deltas.csv',ev,list(ev[0]))
    dec=[]
    for did,q,a,b,c,rec,blocks in DECISIONS: dec.append(dict(decision_id=did,question=q,option_a=a,option_b=b,option_c=c,compatibility_impact="A is additive/compatible; B/C may bind legacy behavior or break shared contracts",test_impact="Selected option must have exact golden, boundary, failure and compatibility tests",recommended_option=rec,selected_option="A",approval_status="APPROVED",approved_by="project owner (user)",approval_basis="User instruction: execute tasks 1 and 2",blocked_units=blocks))
    write_csv('B2-A1_decision_matrix.csv',dec,list(dec[0]))
    iface=[dict(symbol=s,units=u,classification=c,rationale=r,breaking_change="true" if c=="BREAKING_CHANGE" else "false",approval_status="APPROVED") for s,u,c,r in INTERFACES]
    write_csv('B2-A1_interface_impact.csv',iface,list(iface[0]))
    # Exact registry text is preserved; structured scalar columns remain N/A when the Locked value is composite.
    with PARAMS.open(encoding='utf-8-sig',newline='') as f: registry=list(csv.DictReader(f))
    wanted={f'GP-{i:03d}' for i in range(11,21)}|{f'RP-{i:03d}' for i in range(1,34)}
    params=[]
    for r in registry:
        if r['parameter_id'] not in wanted: continue
        users=[u for u in UNITS if u in r['consumer_unit_ids'].split('|')]
        if not users: continue
        params.append(dict(parameter_id=r['parameter_id'],parameter_name=r['parameter_name'],data_type=r['data_type_and_range'].split('；',1)[0],minimum="SEE_LOCKED_RANGE",maximum="SEE_LOCKED_RANGE",options="SEE_LOCKED_RANGE",default_value="NO_UNIQUE_DEFAULT" if '默认' not in r['data_type_and_range'] else "SEE_LOCKED_RANGE",null_semantics="NOT_NULL_UNLESS_EXPLICIT_IN_LOCKED_RANGE",scope="global" if r['parameter_id'].startswith('GP-') else "round",locked_range_and_formula=r['data_type_and_range'],lifecycle=r['lifecycle_or_update'],source_chapter=r['source_section'],using_units='|'.join(users),decision_required="true" if ('custom' in r['data_type_and_range'] or '平台' in r['data_type_and_range']) else "false"))
    write_csv('B2-A1_parameter_matrix.csv',params,list(params[0]))
    vis=[]
    entries=[
    ("STATE-002","authority_snapshot","AUTHORITY_ONLY","Full state and mutable references never cross policy boundary","Mutate opponent hand/wall/raw seed; PlayerView unchanged"),
    ("STATE-002","TrainingTruth/oracle","FORBIDDEN_POLICY_INPUT","Training-only object must not be imported or reachable","Recursive object/import scan zero paths"),
    ("STATE-003","own concealed hand","OWNER_ONLY","Owner sees approved projection; others see count/public effects","Four-seat sentinel perturbation"),
    ("STATE-003","opponent concealed/an-gang","AUTHORITY_ONLY_OR_GP021","Reveal only through GP-021/RULE-016","Swap hidden physical IDs; unrelated views unchanged"),
    ("ALGO-002","explicit counts/melds/dingque","CALLER_INPUT","Pure explicit input only","Monkeypatch GameState/wall/RNG/oracle access to fail"),
    ("ALGO-002","wall/opponents/seed/cache/training label","FORBIDDEN","No reads, imports, globals or hidden memo state","Static import scan and paired hidden perturbation")]
    for u,f,v,r,t in entries:vis.append(dict(unit_id=u,field_or_channel=f,visibility=v,rule=r,required_test=t,result="APPROVED"))
    write_csv('B2-A1_visibility_matrix.csv',vis,list(vis[0]))
    ac=[]
    common=[
    (1,"Valid normal request","Invoke production entry","accepted=true and complete typed result","null","100% exact fields"),
    (2,"Minimum/maximum/null/type boundary matrix","Invoke validator","Only Locked-valid boundaries accepted","SCHEMA_INVALID or unit-specific","All matrix rows exact"),
    (3,"Invalid domain invariant","Invoke production entry","result=null; state unchanged","unit-specific invariant code","before_hash==after_hash"),
    (4,"Duplicate same event/pure same input","Run twice","Idempotent original result / byte-identical pure result","null","version adds at most once"),
    (5,"Late event or stale version","Submit stale request","Rejected; no mutation","VERSION_CONFLICT","version/hash unchanged"),
    (6,"Conflicting or unauthorized request","Change payload/actor/capability","Rejected","INVALID_EVENT or UNAUTHORIZED","zero publication"),
    (7,"Injected prepare/compute failure","Fail first internal stage","Rejected with no partial result","INVARIANT_FAILED or DECOMPOSITION_FAILED","all authoritative bytes unchanged"),
    (8,"Injected validate/commit failure","Fail validation/commit","Rejected and exact rollback","INVARIANT_FAILED","outbox count=0"),
    (9,"Production caller integration","Run real upstream->unit->consumer chain","No test-only facade; one committed/returned result","null","call site and artifact hash present"),
    (10,"Hidden-information perturbation","Pair equal-visible inputs","Same policy view/result","null","100% output hashes equal"),
    (11,"Legacy/Frozen compatibility","Replay legacy v5/current wrappers","Approved legacy output unchanged","documented legacy error","all goldens exact"),
    (12,"100 repeats and fresh processes","Run canonical input","One unique serialization/hash","null","unique_count=1"),
    (13,"Input/container/concurrency permutation","Permute order/schedule","Canonical result unchanged","null","100% permutations equal"),
    (14,"Performance and evidence trace","Measure Locked workload and build E4/E5","P95 within Locked threshold; references resolve","null","ALGO-002 P95<=5ms; STATE units use quoted Locked threshold or decision required")]
    unit_errors={"STATE-002":"VERSION_CONFLICT|UNAUTHORIZED_READ|INVALID_EVENT|INVARIANT_FAILED|SCHEMA_INVALID|UNAUTHORIZED|DETERMINISM_VIOLATION","STATE-003":"PLAYER_NOT_FOUND|DUPLICATE_TILE|INVALID_MELD|INVALID_STATUS|INVALID_HU_ORDER|SCHEMA_INVALID|VERSION_CONFLICT|UNAUTHORIZED|INVARIANT_FAILED","ALGO-002":"HAND_SIZE_INVALID|FACE_COUNT_EXCEEDED|MELD_INVALID|DINGQUE_CONFLICT|DECOMPOSITION_FAILED|SCHEMA_INVALID|VERSION_CONFLICT|NUMERIC_INVARIANT|DETERMINISM_VIOLATION"}
    for u in UNITS:
        for n,inp,op,out,err,quant in common:
            ac.append(dict(unit_id=u,ac_id=f"AC-{u}-{n:02d}",input=inp,operation=op,expected_output=out,error_code=err,quantitative_judgment=quant,semantic_delta_refs=f"SEM-{u}-{max(1,min(8,n)):02d}",test_delta_refs=f"TEST-{u}-{((n-1)%4)+1:02d}",evidence_delta_refs=f"EVID-{u}-01|EVID-{u}-02",allowed_error_codes=unit_errors[u],approval_status="APPROVED"))
    write_csv('B2-A1_acceptance_matrix.csv',ac,list(ac[0]))

if __name__=='__main__': main()
