from __future__ import annotations

import pytest

from players.humanlike.runtime import RP_IDS, RoundLifecycle, RoundRuntime, RuntimeStateError


def _runtime() -> RoundRuntime:
    return RoundRuntime.create_round(round_id="g1-r1", round_index=1, dealer_id=0, self_seat=2, scores=(0, 0, 0, 0))


def test_runtime_registers_exactly_33_rp_and_initializes_first_three() -> None:
    runtime = _runtime()
    snapshot = runtime.snapshot()
    assert tuple(snapshot.values) == RP_IDS
    assert all(snapshot.values[parameter_id] is not None for parameter_id in RP_IDS[:3])
    assert all(snapshot.values[parameter_id] is None for parameter_id in RP_IDS[3:])
    assert snapshot.lifecycle is RoundLifecycle.ACTIVE


def test_event_decision_and_finalize_lifecycle() -> None:
    runtime = _runtime()
    assert runtime.apply_event({"type": "deal", "actor": 0}) == 1
    runtime.begin_decision(legal_actions=[{"type": "discard", "tile": 0}], deadline_ms=1000)
    assert runtime.lifecycle is RoundLifecycle.DECIDING
    runtime.append_decision({"action": {"type": "discard", "tile": 0}, "reason": "dingque"})
    assert runtime.lifecycle is RoundLifecycle.ACTIVE
    final = runtime.finalize_round(round_result=(3, -1, -1, -1), learning_output={"public_only": True})
    assert final.lifecycle is RoundLifecycle.FINALIZED
    assert final.values["RP-032"]["round_result"] == [3, -1, -1, -1]
    with pytest.raises(RuntimeStateError, match="immutable"):
        runtime.set_parameter("RP-010", {})


def test_unknown_rp_and_invalid_transition_fail() -> None:
    runtime = _runtime()
    with pytest.raises(RuntimeStateError, match="unknown"):
        runtime.set_parameter("RP-034", {})
    with pytest.raises(RuntimeStateError, match="open decision"):
        runtime.append_decision({"action": "pass"})
    runtime.begin_decision(legal_actions=[{"type": "pass"}], deadline_ms=0)
    with pytest.raises(RuntimeStateError, match="decision is open"):
        runtime.apply_event({"type": "discard"})
