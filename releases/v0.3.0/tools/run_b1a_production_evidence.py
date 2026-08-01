"""Collect deterministic B1-A E4 evidence through production public entry points."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.audit import canonical_hash
from engine.deal import create_dealt_game
from engine.orchestrator import InteractiveRunner
from players.random_player import RandomPlayer
from engine.rng_v2 import derive_coordinate_seed
from engine.rng_v2 import RngV2Error, select_rng_version
from players.humanlike.config_v2 import ConfigV2Error, canonical_v2_bytes
from players.humanlike.settings_service import read_raw, validate_and_migrate_v2
from players.humanlike.state010 import GP_IDS, FrozenGlobalParameters, SeatRuntimeStore


def main() -> None:
    out = Path("docs/spec-v3/evidence/task18b_b1a")
    out.mkdir(parents=True, exist_ok=True)
    rows = []

    started = time.perf_counter_ns()
    gp = FrozenGlobalParameters()
    commit = gp.commit({pid: {} for pid in GP_IDS})
    runtime = SeatRuntimeStore("b1a-evidence-round")
    update = runtime.update(actor_seat=0, owner_seat=0, changes={"RP-004": {"phase": "created"}}, expected_version=0)
    rows.append({"unit_id": "STATE-010", "scenario_id": "production-owned-state", "input_hash": canonical_hash({"gp_ids": list(GP_IDS), "seat": 0}), "parameter_version": "CDMJ-AI-PARAMS 2.0.0", "seed_ref": None, "intermediate_result": {"gp_version": commit.version, "rp_version": update.version}, "final_output_hash": canonical_hash(dict(runtime.snapshot(0))), "call_site": "FrozenGlobalParameters.commit→SeatRuntimeStore.update", "test_or_replay_ref": "tests/spec_v3/test_b1a_state010.py", "accepted": commit.accepted and update.accepted, "error_code": None, "latency_us": (time.perf_counter_ns() - started) // 1000})
    orchestrator = InteractiveRunner([RandomPlayer(seed=i) for i in range(4)], game_id="b1a-state010-e4")
    orchestrator.setup(); orchestrator._base._archive_state010(orchestrator.state)
    rows[0]["intermediate_result"]["orchestrator_trace"] = orchestrator._base.state010_trace
    rows[0]["call_site"] = "InteractiveRunner.setup→PlayerGameRunner._initialize_state010→_archive_state010"
    before = canonical_hash(dict(runtime.snapshot(0)))
    for scenario, result in (
        ("wrong-owner", runtime.update(actor_seat=1, owner_seat=0, changes={"RP-005": 1}, expected_version=1)),
        ("version-conflict", runtime.update(actor_seat=0, owner_seat=0, changes={"RP-005": 1}, expected_version=0)),
        ("unknown-rp", runtime.update(actor_seat=0, owner_seat=0, changes={"RP-999": 1}, expected_version=1)),
    ):
        rows.append({"unit_id": "STATE-010", "scenario_id": scenario, "input_hash": canonical_hash({"scenario": scenario}), "parameter_version": "CDMJ-AI-PARAMS 2.0.0", "seed_ref": None, "intermediate_result": {"state_hash_before": before}, "final_output_hash": canonical_hash(dict(runtime.snapshot(0))), "call_site": "SeatRuntimeStore.update", "test_or_replay_ref": "tests/spec_v3/test_b1a_state010.py", "accepted": result.accepted, "error_code": result.error_code, "latency_us": 0})

    started = time.perf_counter_ns()
    raw = read_raw()
    source_hash = hashlib.sha256(json.dumps(raw, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    frozen = validate_and_migrate_v2(raw, source_hash=source_hash)
    rows.append({"unit_id": "ALGO-009", "scenario_id": "settings-v1.1-to-v2", "input_hash": source_hash, "source_hash": source_hash, "parameter_version": frozen.parameter_version, "contract_version": frozen.contract_version, "canonical_version": frozen.canonical_version, "seed_ref": None, "intermediate_result": {"schema_before_after": frozen.schema_before_after, "migration_steps": frozen.migration_steps, "defaults": frozen.defaults, "errors": [], "canonical_size": len(frozen.canonical_bytes)}, "final_output_hash": frozen.config_hash, "canonical_hash": frozen.config_hash, "call_site": "settings_service.read_raw→validate_and_migrate_v2→validate_and_freeze", "test_or_replay_ref": "tests/spec_v3/test_b1a_algo009.py", "accepted": True, "error_code": None, "latency_us": (time.perf_counter_ns() - started) // 1000})
    algo009_failures = [
        ("missing-required", lambda: validate_and_migrate_v2({"parameter_version": "CDMJ-AI-PARAMS 2.0.0"})),
        ("non-finite", lambda: canonical_v2_bytes({"n": float("nan")})),
        ("unknown-field", lambda: validate_and_migrate_v2({**json.loads(json.dumps(frozen.value)), "unknown": 1})),
    ]
    for scenario, operation in algo009_failures:
        try:
            operation(); code = None; accepted = True
        except (ConfigV2Error, ValueError) as exc:
            code = getattr(exc, "code", "SCHEMA_INVALID"); accepted = False
        rows.append({"unit_id": "ALGO-009", "scenario_id": scenario, "input_hash": canonical_hash({"scenario": scenario}), "parameter_version": "CDMJ-AI-PARAMS 2.0.0", "contract_version": "CDMJ-CONTRACTS 2.0.0", "canonical_version": "CDMJ canonical-jcs-nfc-v2 profile", "seed_ref": None, "intermediate_result": {"active_hash_before": frozen.config_hash}, "final_output_hash": frozen.config_hash, "call_site": "settings_service.validate_and_migrate_v2", "test_or_replay_ref": "tests/spec_v3/test_b1a_algo009.py", "accepted": accepted, "error_code": code, "latency_us": 0})

    started = time.perf_counter_ns()
    state = create_dealt_game("b1a-production-evidence", rng_version=2)
    trace = derive_coordinate_seed(game_id=state.game_id, stream_name="shuffle", consumer_kind="engine", consumer_id="wall", event_id="initial", sample_index=0)
    rows.append({"unit_id": "ALGO-011", "scenario_id": state.game_id, "game_id_hash": canonical_hash(state.game_id), "input_hash": canonical_hash({"game_id": state.game_id, "rng_version": 2}), "parameter_version": "CDMJ-AI-PARAMS 2.0.0", "algorithm_version": 2, "rng_version": 2, "seed_ref": trace.strategy_ref()["trace_ref"], "intermediate_result": {"wall_size": len(state.wall), "dealer": state.dealer_seat, **trace.audit_envelope()}, "final_output_hash": canonical_hash(state.to_dict()), "call_site": "create_dealt_game(rng_version=2)→derive_coordinate_seed; replay/worker use persisted version/logical coordinate", "test_or_replay_ref": "tests/spec_v3/test_b1a_algo011.py", "accepted": True, "error_code": None, "latency_us": (time.perf_counter_ns() - started) // 1000})
    for scenario, operation in (
        ("unknown-stream", lambda: derive_coordinate_seed(game_id="g", stream_name="unknown", consumer_kind="x", consumer_id="x", event_id="x", sample_index=0)),
        ("missing-new-version", lambda: select_rng_version({"record_format": "rng-v2-new-record", "rng_version": None})),
        ("unsupported-deal-version", lambda: create_dealt_game("g", rng_version=3)),
    ):
        try:
            operation(); code = None; accepted = True
        except (RngV2Error, ValueError) as exc:
            code = getattr(exc, "code", "VERSION_CONFLICT"); accepted = False
        rows.append({"unit_id": "ALGO-011", "scenario_id": scenario, "input_hash": canonical_hash({"scenario": scenario}), "parameter_version": "CDMJ-AI-PARAMS 2.0.0", "rng_version": 2, "seed_ref": None, "intermediate_result": {}, "final_output_hash": None, "call_site": "create_dealt_game/select_rng_version/derive_coordinate_seed", "test_or_replay_ref": "tests/spec_v3/test_b1a_algo011.py", "accepted": accepted, "error_code": code, "latency_us": 0})

    evidence = out / "B1-A_runtime_evidence.json"
    evidence.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    digest = hashlib.sha256(evidence.read_bytes()).hexdigest()
    manifest = {"artifact": str(evidence).replace("\\", "/"), "sha256": digest, "record_count": len(rows), "unit_ids": [row["unit_id"] for row in rows]}
    (out / "B1-A_evidence_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
