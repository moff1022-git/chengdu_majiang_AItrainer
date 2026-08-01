from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def test_versioning_policy_freezes_all_current_subcontracts():
    text=(ROOT/"docs/spec-v3/contracts/versioning_policy.md").read_text(encoding="utf-8")
    for token in ("CDMJ-CONTRACTS 1.0.0","GameState schema","PlayerView","Action codec","Audit format","Fixture","MAJOR.MINOR.PATCH","VERSION_CONFLICT"):
        assert token in text

def test_common_contract_forbids_duplicate_strategy_dtos_and_truth_access():
    common=(ROOT/"docs/spec-v3/contracts/common_contracts.md").read_text(encoding="utf-8")
    visibility=(ROOT/"docs/spec-v3/contracts/data_visibility_contract.md").read_text(encoding="utf-8")
    assert "禁止另建同义DTO" in common
    assert "策略禁止" in visibility and "SIMULATOR_TRUTH" in visibility
