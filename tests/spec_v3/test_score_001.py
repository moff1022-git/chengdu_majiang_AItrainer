import pytest
from engine.score import ConservedScoreLedger, LedgerInvariantError, LedgerTransfer, apply_conserved_transfers

def test_score_001_golden_boundary_illegal_and_conservation():
    after, delta = apply_conserved_transfers((0, 0, 0, 0), (LedgerTransfer(1, 0, 4),))
    assert after == (4, -4, 0, 0) and delta == after and sum(delta) == 0
    assert apply_conserved_transfers((-5, 5), ())[0] == (-5, 5)
    for transfer, code in [(LedgerTransfer(0, 0, 1), "SELF_TRANSFER"), (LedgerTransfer(0, 1, 0), "AMOUNT_RANGE")]:
        with pytest.raises(LedgerInvariantError) as exc: apply_conserved_transfers((0, 0), (transfer,))
        assert exc.value.code == code

def test_score_001_event_idempotency_layers_and_conflict():
    ledger=ConservedScoreLedger((0,0,0,0)); transfers=(LedgerTransfer(1,0,4),)
    first=ledger.apply_event(event_id="e1",layer="atomic",reason="hu",transfers=transfers)
    second=ledger.apply_event(event_id="e1",layer="atomic",reason="hu",transfers=transfers)
    assert first["sum_delta"]==0 and not first["idempotent"] and second["idempotent"] and ledger.balances==(4,-4,0,0)
    with pytest.raises(LedgerInvariantError,match="DUPLICATE_SCORE_EVENT"): ledger.apply_event(event_id="e1",layer="atomic",reason="other",transfers=transfers)
    with pytest.raises(LedgerInvariantError,match="TRANSFER_SCHEMA"): ledger.apply_event(event_id="e2",layer="bad",reason="x",transfers=())
    assert len(first["event_hash"])==64
