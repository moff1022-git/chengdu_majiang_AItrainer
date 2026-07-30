import pytest
from players.humanlike.belief import model_001_rule_baseline
from players.humanlike.view import PolicyInputError

def test_model_001_baseline_normalized_deterministic_and_leak_rejected():
    inp=({"seat":1,"dingque":"wan","discard_pile":["wan_1","wan_2"],"melds":[{"tile_id":"tong_3","tile_count":3}]},)
    out=model_001_rule_baseline(inp)[0]
    assert abs(sum(out["dominant_suit_probs"])-1)<1e-12 and abs(sum(out["shape_probs"])-1)<1e-12
    assert out == model_001_rule_baseline(inp)[0] and 0 <= out["p_cleared"] <= 1
    prior=model_001_rule_baseline(({"seat":2},))[0]; assert prior["low_evidence"]
    with pytest.raises(PolicyInputError, match="FORBIDDEN_FEATURE"): model_001_rule_baseline(({"seat":1,"hand":[]},))
    with pytest.raises(PolicyInputError, match="FORBIDDEN_FEATURE"): model_001_rule_baseline(({"seat":1,"nested":{"truth":[]}},))
    assert {"uncertainty","max_probability","prior","posterior","contributions","forbidden_scan"} <= set(out)
    assert model_001_rule_baseline(({"seat":1,"dingque":"wan","discard_pile":["wan_1"]},))[0]["p_cleared"] < model_001_rule_baseline(({"seat":1,"dingque":"wan","discard_pile":["wan_1","wan_2"]},))[0]["p_cleared"]
