import json
import pytest
from engine.audit import AuditError, DecisionAuditWriter, canonical_hash, verify_audit

def test_audit_003_chain_golden_tamper_and_truncate(tmp_path):
    path=tmp_path/"audit.jsonl"; writer=DecisionAuditWriter(path,game_id="g",engine_config={},initial_state={"x":0})
    writer.finish(final_state={"x":0},finished_reason="done")
    result=verify_audit(path); assert result.complete and result.decision_count==0
    assert canonical_hash({"b":2,"a":1}) == canonical_hash({"a":1,"b":2})
    rows=path.read_text().splitlines(); tampered=json.loads(rows[0]); tampered["game_id"]="x"
    bad=tmp_path/"bad.jsonl"; bad.write_text(json.dumps(tampered)+"\n"+rows[1]+"\n")
    with pytest.raises(AuditError): verify_audit(bad)
    short=tmp_path/"short.jsonl"; short.write_text(rows[0]+"\n")
    assert verify_audit(short, strict=False).complete is False
    reordered=tmp_path/"reordered.jsonl"; reordered.write_text("\n".join(reversed(rows))+"\n")
    with pytest.raises(AuditError): verify_audit(reordered)
