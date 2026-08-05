import json
from tools.f0057_trace_audit import audit


def test_public_candidate_audit(tmp_path):
    games = tmp_path / "games.jsonl"; games.write_text(json.dumps({"game_id":"g","settle_tags":{"hua_zhu":[0]}})+"\n")
    root = tmp_path / "traces"; folder = root / "g"; folder.mkdir(parents=True)
    row = {"game_id":"g","seat":0,"decision_trace":{"candidates":[{"score":2,"features":{"shanten":1,"dingque_tiles":2,"ukeire_public_count":3}},{"score":1,"features":{}}]}}
    (folder / "g.audit.jsonl").write_text(json.dumps(row)+"\n")
    result = audit(root, games)
    assert result["decision_records"] == 1
    assert result["field_coverage"]["shanten"]["rate"] == 1
    assert result["strata"][0]["outcome"] == "hua_zhu"
    assert result["causal_claim"] is False
