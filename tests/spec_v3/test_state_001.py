from dataclasses import replace

import pytest

from engine.match import MatchController, MatchCreateRequest, SeatBinding


def request(**changes):
    base = MatchCreateRequest(
        event_id="create-1", match_id="match-1", expected_state_version=0,
        ruleset_hash="r" * 64, config_hash="c" * 64, seed_trace_ref="safe-ref",
        bindings=tuple(SeatBinding(i, f"p{i}", f"profile{i}") for i in range(4)),
        total_rounds=2, starting_scores={i: 0 for i in range(4)},
    )
    return replace(base, **changes)


def test_state001_schema_freeze_and_projection():
    controller = MatchController()
    result = controller.create(request())
    assert result.accepted and result.next_state_version == 1
    assert result.context.bindings == tuple(sorted(result.context.bindings, key=lambda b: b.seat))
    assert "profile" not in repr(dict(result.context.public_projection())).lower()
    with pytest.raises(TypeError):
        result.context.starting_scores[0] = 1
    assert controller.create(request()).context is result.context


def test_state001_rejects_schema_seats_versions_and_ranges_atomically():
    cases = [
        (request(event_id=""), "SCHEMA_INVALID"),
        (request(seed_trace_ref=""), "SEED_MISSING"),
        (request(total_rounds=0), "INVALID_MATCH_REQUEST"),
        (request(total_rounds=10001), "INVALID_MATCH_REQUEST"),
        (request(bindings=(SeatBinding(0,"a","a"), SeatBinding(0,"b","b"))), "DUPLICATE_SEAT"),
        (request(rng_version=3), "VERSION_CONFLICT"),
    ]
    for req, code in cases:
        controller = MatchController()
        result = controller.create(req)
        assert not result.accepted and result.error_code == code
        assert controller.context is None


def test_state001_two_phase_factory_failure_has_zero_publication():
    controller = MatchController()
    calls = []
    def ok():
        calls.append("prepared")
        return object()
    def fail():
        raise RuntimeError("factory failed")
    result = controller.create(request(), player_factories={0: ok, 1: ok, 2: fail, 3: ok})
    assert not result.accepted and result.error_code == "INVARIANT_FAILED"
    assert controller.context is None


def test_state001_round_cas_completion_and_terminal_absorption():
    controller = MatchController()
    assert controller.create(request()).accepted
    stale = controller.complete_round(event_id="round-1", expected_state_version=0, scores={i: 1 for i in range(4)})
    assert stale.error_code == "VERSION_CONFLICT"
    first = controller.complete_round(event_id="round-1", expected_state_version=1, scores={0:4,1:3,2:2,3:1})
    assert first.accepted and first.match_result is None and first.next_state_version == 2
    second = controller.complete_round(event_id="round-2", expected_state_version=2, scores={0:4,1:3,2:2,3:1})
    assert second.match_result.status == "COMPLETED" and second.match_result.rankings == (0,1,2,3)
    assert controller.complete_round(event_id="round-3", expected_state_version=3, scores={0:4,1:3,2:2,3:1}).error_code == "TERMINAL_STATE"

