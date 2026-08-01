import pytest
from players.humanlike.attention import rank_attention_cues

def test_heur_019_allowed_ranking_mandatory_and_boundaries():
    cues=({"candidate_key":"b","mandatory":False,"salience":1,"freshness":0,"memory_strength":0},{"candidate_key":"a","mandatory":True,"salience":0,"freshness":0,"memory_strength":0},{"candidate_key":"c","mandatory":False,"salience":.5,"freshness":1,"memory_strength":1})
    out=rank_attention_cues(cues, capacity=1)
    assert [x["candidate_key"] for x in out] == ["a", "c"]
    assert out == rank_attention_cues(tuple(reversed(cues)), capacity=1)
    assert set(out[0]) >= {"raw_features","score_components","corrections","selected","filtered_reason","abandon_reason","stop_reason"}
    with pytest.raises(ValueError, match="FEATURE_RANGE"): rank_attention_cues(({"candidate_key":"x","salience":2,"freshness":0,"memory_strength":0},),capacity=1)
    with pytest.raises(ValueError,match="CAPACITY_RANGE"): rank_attention_cues(cues,capacity=0)
    with pytest.raises(ValueError,match="FEATURE_SCHEMA"): rank_attention_cues(({"candidate_key":"","salience":0,"freshness":0,"memory_strength":0},),capacity=1)
