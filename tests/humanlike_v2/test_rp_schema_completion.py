import pytest

from players.humanlike.rp_schema import RPSchemaError, make_envelope, validate_envelope
from players.humanlike.runtime import RoundRuntime


def test_event_mirrors_remaining_public_slots():
    runtime = RoundRuntime.create_round(round_id="g", round_index=1, dealer_id=0, self_seat=0, scores=(0, 0, 0, 0))
    runtime.apply_event({"type": "discard", "actor": 0, "tile": "wan1"})
    snapshot = runtime.envelope_snapshot().values
    for parameter_id in ("RP-009", "RP-022", "RP-031"):
        assert snapshot[parameter_id]["schema_version"] == "F0037-RP-1.0"


def test_public_envelope_rejects_hidden_payload():
    value = make_envelope("RP-031", {"server_hand": [1]}, event_index=1, visibility="public_partial")
    with pytest.raises(RPSchemaError):
        validate_envelope(value)


def test_envelope_write_is_idempotent_for_same_payload():
    first = make_envelope("RP-022", {"phase": "early"}, event_index=2, visibility="public_partial")
    second = make_envelope("RP-022", {"phase": "early"}, event_index=2, visibility="public_partial")
    assert first == second
