import hashlib
import subprocess, sys

import pytest

from players.humanlike.config_v2 import ConfigActivator, ConfigV2Error, canonical_v2_bytes, freeze_v2, load_v2_bytes, migrate_1_0_to_1_1, migrate_1_1_to_2_0, validate_and_freeze
from players.humanlike.settings_service import read_raw, save_v2_raw


def test_canonical_v2_golden_number_unicode_and_hash():
    assert canonical_v2_bytes({"n": -0.0}).hex() == "7b226e223a307d"
    data = canonical_v2_bytes({"key".replace("key", "e\u0301"): "e\u0301"})
    assert data.hex() == "7b22c3a9223a22c3a9227d"
    assert hashlib.sha256(data).hexdigest() == "e8b55b29bf172acb65a8ec20d1762cd9d6112c7abd6799895503d9151b8f42ab"


@pytest.mark.parametrize("value,code", [(float("nan"), "NON_FINITE"), (2**63, "PARAM_RANGE")])
def test_canonical_rejects_invalid_numbers(value, code):
    with pytest.raises(ConfigV2Error) as error:
        canonical_v2_bytes({"n": value})
    assert error.value.code == code


def test_nfc_collision_rejected():
    with pytest.raises(ConfigV2Error) as error:
        canonical_v2_bytes({"é": 1, "e\u0301": 2})
    assert error.value.code == "SCHEMA_INVALID"


def test_explicit_migration_and_empty_extensions():
    source = {"parameter_version": "CDMJ-AI-PARAMS 1.1.0", "global_parameters": {"GP-002": {"extensions": []}, "GP-004": {"extensions": []}}, "players": []}
    migrated = migrate_1_1_to_2_0(source, source_hash="a" * 64)
    assert migrated["parameter_version"] == "CDMJ-AI-PARAMS 2.0.0"
    frozen = freeze_v2(migrated, source_hash="a" * 64)
    assert frozen.parameter_version.endswith("2.0.0") and len(frozen.config_hash) == 64
    bad = dict(migrated); bad["unknown"] = 1
    with pytest.raises(ConfigV2Error) as error:
        freeze_v2(bad)
    assert error.value.code == "PARAM_UNKNOWN"


def test_legacy_edge_is_pure_and_v2_writer_never_emits_v1(tmp_path):
    raw = {"parameter_version": "CDMJ-AI-PARAMS 1.0.0", "implementation_version": "CDMJ-AI-IMPL 2.0.0", "global_parameters": {f"GP-{i:03d}": {"k": i} for i in range(24, 28)}, "players": [{"player_id": i} for i in range(4)]}
    before = repr(raw)
    migrated = migrate_1_0_to_1_1(raw)
    assert repr(raw) == before and all("cognitive_parameters" in p for p in migrated["players"])
    target = tmp_path / "v2.json"
    frozen = save_v2_raw(read_raw(), target)
    assert target.read_bytes().rstrip() == frozen.canonical_bytes
    assert b"CDMJ-AI-PARAMS 2.0.0" in target.read_bytes() and b"CDMJ-AI-PARAMS 1.1.0" not in target.read_bytes()
    loaded = load_v2_bytes(target.read_bytes())
    assert loaded.config_hash == frozen.config_hash and loaded.migration_steps == ("MIG-CONFIG-110-200",)


@pytest.mark.parametrize("value", [False, 0, "", [], 2**53 - 1, 2**53 + 1, 1e20, "😀"])
def test_canonical_boundary_values_are_deterministic(value):
    assert canonical_v2_bytes({"v": value}) == canonical_v2_bytes({"v": value})


def test_activator_failure_preserves_active_hash():
    raw = read_raw(); good = migrate_1_1_to_2_0(raw)
    activator = ConfigActivator(); active = activator.activate(good)
    with pytest.raises(ConfigV2Error):
        activator.activate({})
    assert activator.active.config_hash == active.config_hash


def test_pipeline_order_idempotence_and_infinity_error():
    raw = read_raw(); first, stages = validate_and_freeze(raw)
    assert stages == ("parse", "version", "migration", "defaults", "type_range", "cross_constraint", "unknown", "canonical_hash")
    second = migrate_1_1_to_2_0(first.value)
    assert canonical_v2_bytes(second) == first.canonical_bytes
    with pytest.raises(ConfigV2Error) as error:
        canonical_v2_bytes({"n": float("inf")})
    assert error.value.code == "NON_FINITE"


def test_canonical_cross_process_and_key_order_100_times():
    expected = canonical_v2_bytes({"é": 2**53 + 1, "a": -0.0})
    assert all(canonical_v2_bytes({"a": -0.0, "e\u0301": 2**53 + 1}) == expected for _ in range(100))
    code = "from players.humanlike.config_v2 import canonical_v2_bytes as c; print(c({'a':-0.0,'e\\u0301':9007199254740993}).hex())"
    assert bytes.fromhex(subprocess.check_output([sys.executable, "-c", code], text=True).strip()) == expected
