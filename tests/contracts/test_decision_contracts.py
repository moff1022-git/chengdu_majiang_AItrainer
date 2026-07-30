from __future__ import annotations
import json
from pathlib import Path
from engine.action import Action, ActionType
from players.humanlike.candidates import Candidate, CandidateSet, stable_action_key
from players.humanlike.attention import rank_attention_cues

ROOT=Path(__file__).resolve().parents[2]

def test_candidate_uses_canonical_action_and_stable_key():
    action=Action(ActionType.PASS); candidate=Candidate(action,False); group=CandidateSet((candidate,))
    assert group.candidates[0].action is action and stable_action_key(action)==(8,"",())

def test_score_breakdown_explanation_fields_are_complete():
    out=rank_attention_cues(({"candidate_key":"pass","mandatory":False,"salience":.5,"freshness":1,"memory_strength":.25},),capacity=1)[0]
    assert {"raw_features","score_components","corrections","final_score","rank","selected","filtered_reason","abandon_reason","stop_reason"} <= set(out)
    assert -4 <= out["final_score"] <= 4

def test_decision_schema_requires_versions_hashes_seed_and_explanation():
    schema=json.loads((ROOT/"docs/spec-v3/contracts/schemas/decision.schema.json").read_text())
    required=set(schema["required"])
    assert {"selected_action","explanation","config_hash","ruleset_hash","seed_trace","state_version_before","state_version_after","error_code"} <= required

def test_explanation_schema_covers_generation_scoring_filter_selection_abandon():
    defs=json.loads((ROOT/"docs/spec-v3/contracts/schemas/common_contracts.schema.json").read_text())["$defs"]
    required=set(defs["decision_explanation"]["required"])
    assert {"generated_candidates","scored_candidates","filtered_candidates","selected_candidate_key","selection_reason","abandoned_reasons","stop_reason"} <= required
