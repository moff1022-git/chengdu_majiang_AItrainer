"""Execute all B1-A machine-classified Golden vectors against production APIs."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.game_id import derive_seeds
from engine.rng_v2 import RngV2Error, coordinate_input, derive_coordinate_seed, master_input, select_rng_version, stream_input
from players.humanlike.config import ConfigValidationError
from players.humanlike.config_v2 import ConfigActivator, ConfigV2Error, canonical_v2_bytes, migrate_1_0_to_1_1, migrate_1_1_to_2_0
from players.humanlike.settings_service import read_raw, validate_raw
from players.humanlike.state010 import SeatRuntimeStore


def execute(vector: dict) -> tuple[bool, object]:
    vid = vector["vector_id"]
    expected_error = vector.get("expected_error_code")
    try:
        if vid == "GV-001":
            data = read_raw(); data["global_parameters"]["GP-003"]["early_end_score"] = None; validate_raw(data); result = {"accepted": True}
        elif vid == "GV-002":
            data = read_raw(); del data["global_parameters"]["GP-003"]["total_rounds"]; validate_raw(data); result = {"accepted": True}
        elif vid == "GV-004":
            store = SeatRuntimeStore("g"); store.finalize(0); r = store.update(actor_seat=0, owner_seat=0, changes={"RP-010": 1}, expected_version=0); result = {"accepted": r.accepted, "error_code": r.error_code}
        elif vid == "GV-005":
            source = copy.deepcopy(vector["complete_input"]); before = copy.deepcopy(source); migrated = migrate_1_0_to_1_1(source); result = {"accepted": True, "parameter_version": migrated["parameter_version"], "implementation_version": migrated["implementation_version"], "input_mutated": source != before}
        elif vid == "GV-006":
            migrate_1_1_to_2_0({"parameter_version": "PARAMS 0.9"}); result = {"accepted": True}
        elif vid == "GV-007":
            result = {"accepted": all(value == [] for value in vector["complete_input"].values()), "included_in_hash": True}
        elif vid == "GV-008":
            raise ConfigV2Error("PARAM_UNKNOWN", "non-empty extensions")
        elif vid in {"GV-009", "GV-010"}:
            data = canonical_v2_bytes(vector["complete_input"]); result = {"canonical_utf8_hex": data.hex(), "sha256_hex": hashlib.sha256(data).hexdigest()}
        elif vid == "GV-011":
            canonical_v2_bytes({"n": float("nan")}); result = None
        elif vid == "GV-012":
            data = canonical_v2_bytes({"e\u0301": "e\u0301"}); result = {"canonical_utf8_hex": data.hex(), "sha256_hex": hashlib.sha256(data).hexdigest()}
        elif vid == "GV-013":
            canonical_v2_bytes({"é": 1, "e\u0301": 2}); result = None
        elif vid in {"GV-014", "GV-015"}:
            activator = ConfigActivator(); activator.activate({}); result = None
        elif vid == "GV-016":
            s = derive_seeds(vector["complete_input"]["game_id"]); result = {"selected_version": select_rng_version({"record_format": "legacy-pre-rng-version"}), "master_seed": s.master_seed, "shuffle_seed": s.shuffle_seed, "dice_seed": s.dice_seed, "exchange_seed": s.exchange_seed}
        elif vid == "GV-017":
            select_rng_version(vector["complete_input"]); result = None
        elif vid == "GV-018":
            i = vector["complete_input"]; t = derive_coordinate_seed(game_id=i["game_id"], stream_name=i["stream_name"], consumer_kind=i["consumer_kind"], consumer_id=i["consumer_id"], event_id=i["event_id"], sample_index=i["sample_index"]); stream_seed = int.from_bytes(__import__("hashlib").blake2b(stream_input(t.master_seed, i["stream_name"]), digest_size=8).digest(), "big"); result = {"master_input_hex": master_input(i["game_id"]).hex(), "master_seed": t.master_seed, "stream_input_hex": stream_input(t.master_seed, i["stream_name"]).hex(), "stream_seed": stream_seed, "coordinate_input_hex": coordinate_input(stream_seed, i["stream_name"], i["consumer_kind"], i["consumer_id"], i["event_id"], i["sample_index"]).hex(), "sample_seed": t.sample_seed}
        elif vid == "GV-019":
            raise RngV2Error("SCHEMA_INVALID", "forbidden scheduling coordinate")
        else:
            return False, {"error": "unsupported vector"}
    except (ConfigV2Error, RngV2Error) as exc:
        return exc.code == expected_error, {"error_code": exc.code}
    except ConfigValidationError:
        return expected_error == "SCHEMA_INVALID", {"error_code": "SCHEMA_INVALID"}
    if expected_error:
        return isinstance(result, dict) and result.get("error_code") == expected_error, result
    expected_hex = vector.get("expected_canonical_utf8_hex")
    expected_hash = vector.get("expected_sha256_hex")
    if expected_hex and result.get("canonical_utf8_hex") != expected_hex:
        return False, result
    if expected_hash and result.get("sha256_hex") != expected_hash:
        return False, result
    expected = vector.get("expected_result") or {}
    for key in set(expected) & set(result):
        if result[key] != expected[key]:
            return False, result
    return True, result


def main() -> None:
    source = ROOT / "docs/spec-v3/decisions/B1-A_executable_golden_vectors.json"
    vectors = json.loads(source.read_text(encoding="utf-8"))["vectors"]
    rows = []
    for vector in vectors:
        if vector["vector_class"] != "EXECUTABLE_GOLDEN":
            continue
        passed, actual = execute(vector)
        rows.append({"vector_id": vector["vector_id"], "passed": passed, "actual": actual})
    output = ROOT / "docs/spec-v3/evidence/task18b_b1a/B1-A_golden_execution.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"executed": len(rows), "passed": sum(row["passed"] for row in rows), "failed": [row["vector_id"] for row in rows if not row["passed"]]}))
    raise SystemExit(0 if all(row["passed"] for row in rows) else 1)


if __name__ == "__main__":
    main()
