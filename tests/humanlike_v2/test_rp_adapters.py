import pytest

from players.humanlike.rp_adapters import write_rp
from players.humanlike.runtime import RoundRuntime, RuntimeStateError


def test_role_scoped_write_stores_valid_envelope():
    runtime = RoundRuntime.create_round(round_id="g", round_index=1, dealer_id=0, self_seat=1, scores=(0, 0, 0, 0))
    write_rp(runtime, "RP-023", {"count": 1}, role="player_policy", owner_seat=1)
    assert runtime.envelope_snapshot().values["RP-023"]["schema_version"] == "F0037-RP-1.0"


def test_role_scope_rejects_unauthorized_write():
    runtime = RoundRuntime.create_round(round_id="g", round_index=1, dealer_id=0, self_seat=1, scores=(0, 0, 0, 0))
    with pytest.raises(RuntimeStateError):
        write_rp(runtime, "RP-001", {}, role="player_policy")
