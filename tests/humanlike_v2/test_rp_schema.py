from __future__ import annotations

import pytest

from players.humanlike.rp_schema import RPSchemaError, make_envelope, migrate_legacy, validate_envelope


def test_envelope_round_trip_and_hash():
    value = make_envelope("RP-023", {"count": 2}, event_index=4, owner_seat=1, source="humanlike_policy")
    assert validate_envelope(value, "RP-023")["payload"] == {"count": 2}


def test_legacy_payload_migrates_without_semantic_change():
    value = migrate_legacy("RP-010", {"visible_counts": [0] * 27})
    assert value["payload"]["visible_counts"] == [0] * 27
    assert value["source"] == "legacy"


def test_envelope_tamper_and_parameter_mismatch_fail():
    value = make_envelope("RP-001", {}, event_index=0)
    value["payload"] = {"tampered": True}
    with pytest.raises(RPSchemaError):
        validate_envelope(value)
    value = make_envelope("RP-001", {}, event_index=0)
    with pytest.raises(RPSchemaError):
        validate_envelope(value, "RP-002")
