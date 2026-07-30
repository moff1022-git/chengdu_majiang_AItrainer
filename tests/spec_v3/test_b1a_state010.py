import pytest
import subprocess, sys
from engine.orchestrator import InteractiveRunner
from players.random_player import RandomPlayer
from players.humanlike.state010 import FrozenGlobalParameters, GP_IDS, PARAMETER_IDS, PARAMETER_REGISTRY, RP_IDS, ParameterStateError, SeatRuntimeStore, build_registry, resolve_parameters


def test_registry_has_exact_60_ids_and_gp_commit_is_atomic():
    assert tuple(PARAMETER_REGISTRY) == GP_IDS + RP_IDS
    store = FrozenGlobalParameters()
    bad = store.commit({pid: {} for pid in GP_IDS[:-1]})
    assert not bad.accepted and bad.error_code == "MISSING_REQUIRED" and store.snapshot is None
    ok = store.commit({pid: {} for pid in GP_IDS})
    assert ok.accepted and ok.version == 1
    assert store.commit({pid: {} for pid in GP_IDS}).error_code == "LIFECYCLE_VIOLATION"
    assert all(PARAMETER_REGISTRY[pid].type_and_range and PARAMETER_REGISTRY[pid].lifecycle and PARAMETER_REGISTRY[pid].source_reference for pid in PARAMETER_REGISTRY)


def test_four_seats_are_isolated_and_cas_failure_is_zero_write():
    store = SeatRuntimeStore("round-1")
    assert store.update(actor_seat=0, owner_seat=0, changes={"RP-004": {"x": 1}}, expected_version=0).accepted
    before = dict(store.snapshot(0))
    failed = store.update(actor_seat=1, owner_seat=0, changes={"RP-004": {"x": 2}}, expected_version=1)
    assert failed.error_code == "LIFECYCLE_VIOLATION" and dict(store.snapshot(0)) == before
    assert store.snapshot(1)["RP-004"] is None
    archive = store.finalize(0)
    assert archive.owner_seat == 0 and archive.values["RP-004"] == {"x": 1}
    assert store.update(actor_seat=0, owner_seat=0, changes={"RP-005": 1}, expected_version=1).error_code == "LIFECYCLE_VIOLATION"


def test_registry_closure_resolve_metadata_and_duplicate_errors():
    rows = [{"parameter_id": pid} for pid in PARAMETER_IDS]
    assert len(build_registry(rows)) == 60
    with pytest.raises(ParameterStateError) as duplicate:
        build_registry(rows[:-1] + [{"parameter_id": rows[0]["parameter_id"]}])
    assert duplicate.value.code.value == "DUPLICATE_PARAMETER"
    result = resolve_parameters({"GP-001": {}}, phase="match_create", owner_seat=2, ruleset_hash="r", config_hash="c")
    assert result.accepted and result.result["owner_seat"] == 2 and result.result["config_hash"] == "c"
    unknown = resolve_parameters({"GP-999": {}}, phase="event")
    assert not unknown.accepted and unknown.result is None and unknown.error_code == "UNKNOWN_PARAMETER"


def test_orchestrator_builds_four_isolated_state010_owners():
    runner = InteractiveRunner([RandomPlayer(seed=i) for i in range(4)], game_id="state010-orchestrator")
    runner.setup()
    stores = runner._base.state010_stores
    assert len(stores) == 4 and len(runner._base.state010_trace["owner_hashes"]) == 4
    before = [dict(store.snapshot(i)) for i, store in enumerate(stores)]
    assert stores[2].update(actor_seat=2, owner_seat=2, changes={"RP-004": 1}, expected_version=0).accepted
    assert all(dict(stores[i].snapshot(i)) == before[i] for i in (0, 1, 3))


def test_state010_cross_process_fingerprint_is_stable():
    code = "from engine.audit import canonical_hash; from players.humanlike.state010 import resolve_parameters; print(canonical_hash(dict(resolve_parameters({'GP-001':{}},phase='match_create',owner_seat=0).result)))"
    assert len({subprocess.check_output([sys.executable, "-c", code], text=True).strip() for _ in range(3)}) == 1
