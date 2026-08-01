from engine.round_state_machine import (
    RoundPhase, RoundSnapshot, RoundStateMachine, TransitionRequest,
    phase_from_legacy, phase_to_legacy,
)


def req(event, version, kind, payload=None):
    return TransitionRequest(event, version, kind, "engine", payload or {})


def test_state004_exact_enum_and_legacy_adapter():
    assert {p.value for p in RoundPhase} == {"CONFIGURED","DEALT","EXCHANGE","DINGQUE","READY","DRAW","DISCARD","RESPONSE","FINISHED","SETTLED"}
    assert phase_from_legacy("finished", end_settled=True) is RoundPhase.SETTLED
    assert phase_to_legacy(RoundPhase.SETTLED) == ("finished", True)
    for forbidden in ("WALL_READY","PLAYING","SETTLEMENT"):
        assert forbidden not in RoundPhase.__members__


def test_state004_opening_edges_skip_and_illegal_zero_write():
    sm = RoundStateMachine(RoundSnapshot(RoundPhase.CONFIGURED,0,(0,1,2,3),55))
    assert sm.transition(req("d",0,"DEAL_COMMITTED")).snapshot.phase is RoundPhase.DEALT
    assert sm.transition(req("skip",1,"EXCHANGE_SKIPPED")).snapshot.phase is RoundPhase.DINGQUE
    before = sm.snapshot
    bad = sm.transition(req("bad",2,"DISCARD_COMMITTED"))
    assert not bad.accepted and bad.error_code == "ILLEGAL_TRANSITION" and sm.snapshot is before


def test_state004_cas_idempotency_hu_and_wall_terminal():
    sm = RoundStateMachine(RoundSnapshot(RoundPhase.RESPONSE,5,(0,1,2,3),10))
    stale = sm.transition(req("stale",4,"CLAIMS_PASSED"))
    assert stale.error_code == "VERSION_CONFLICT" and sm.snapshot.state_version == 5
    hu = sm.transition(req("hu",5,"HU_RESOLVED",{"hu_seats":[1,2]}))
    assert hu.snapshot.phase is RoundPhase.DRAW and hu.snapshot.active_seats == (0,3)
    assert sm.transition(req("hu",5,"HU_RESOLVED",{"hu_seats":[1,2]})) is hu
    terminal = sm.transition(req("empty",6,"WALL_EXHAUSTED"))
    assert terminal.snapshot.phase is RoundPhase.FINISHED and terminal.snapshot.wall_remaining == 0


def test_state004_settlement_absorbs_and_emits_commit_only_notifications():
    sm = RoundStateMachine(RoundSnapshot(RoundPhase.FINISHED,9,(0,),0))
    invalid = sm.transition(req("settle-bad",9,"SETTLEMENT_COMMITTED",{}))
    assert invalid.error_code == "INVARIANT_FAILED" and invalid.notify == ()
    good = sm.transition(req("settle",9,"SETTLEMENT_COMMITTED",{"settlement_hash":"a"*64}))
    assert good.accepted and good.snapshot.phase is RoundPhase.SETTLED and len(good.notify) == 3
    after = sm.transition(req("late",10,"SETTLEMENT_COMMITTED",{"settlement_hash":"a"*64}))
    assert after.error_code == "TERMINAL_STATE" and after.snapshot is good.snapshot

