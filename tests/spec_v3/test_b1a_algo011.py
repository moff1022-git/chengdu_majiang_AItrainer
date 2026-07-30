import concurrent.futures
import json
import subprocess
import sys
import random

import pytest

from engine.game_id import derive_seeds
from engine.deal import create_dealt_game
from engine.rng_v2 import RestrictedSeedTraceStore, RngV2Error, derive_coordinate_seed, master_input, select_rng_version, stream_input


def test_legacy_golden_is_unchanged_and_version_selection_is_explicit():
    seeds = derive_seeds("fixed-for-exchange")
    assert (seeds.master_seed, seeds.shuffle_seed, seeds.dice_seed, seeds.exchange_seed) == (2403837098037711652, 2403837098037711652, 9581831241709401729, 8864912832000149886)
    assert select_rng_version({"record_format": "legacy-pre-rng-version"}) == "legacy-v1"
    assert select_rng_version({"record_format": "rng-v2-new-record", "rng_version": 2}) == "rng-v2"


def test_rng_v2_golden_and_strategy_visibility():
    trace = derive_coordinate_seed(game_id="demo", stream_name="policy_noise", consumer_kind="policy", consumer_id="seat-0", event_id="event-42", sample_index=0)
    assert master_input("demo").hex() == "43444d4a2d524e47006d617374657200000464656d6f00020002"
    assert trace.master_seed == 1435199040579534962 and trace.sample_seed == 1912371584853373347
    assert stream_input(trace.master_seed, "policy_noise").hex() == "43444d4a2d524e470073747265616d0013ead9ec63b98072000c706f6c6963795f6e6f6973650002"
    assert set(trace.strategy_ref()) == {"rng_used", "algorithm_version", "rng_version", "trace_ref"}


def test_stateless_coordinates_ignore_worker_schedule():
    indices = list(range(100))
    expected = {i: derive_coordinate_seed(game_id="g", stream_name="training_noise", consumer_kind="trainer", consumer_id="batch", event_id="e", sample_index=i).sample_seed for i in indices}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        actual = dict(pool.map(lambda i: (i, derive_coordinate_seed(game_id="g", stream_name="training_noise", consumer_kind="trainer", consumer_id="batch", event_id="e", sample_index=i).sample_seed), reversed(indices)))
    assert actual == expected


def test_unknown_stream_and_missing_new_version_rejected():
    with pytest.raises(RngV2Error) as stream_error:
        derive_coordinate_seed(game_id="g", stream_name="unknown", consumer_kind="x", consumer_id="x", event_id="x", sample_index=0)
    assert stream_error.value.code == "STREAM_UNKNOWN"
    with pytest.raises(RngV2Error) as version_error:
        select_rng_version({"record_format": "rng-v2-new-record", "rng_version": None})
    assert version_error.value.code == "SCHEMA_INVALID"


def test_production_deal_v2_is_reproducible_and_legacy_default_unchanged():
    first = create_dealt_game("b1a-deal", rng_version=2).to_dict()
    second = create_dealt_game("b1a-deal", rng_version=2).to_dict()
    assert first == second
    assert create_dealt_game("b1a-deal").to_dict() == create_dealt_game("b1a-deal", rng_version=1).to_dict()


def test_restricted_trace_store_keeps_sensitive_fields_out_of_strategy_ref(tmp_path):
    trace = derive_coordinate_seed(game_id="g", stream_name="policy_noise", consumer_kind="policy", consumer_id="seat-0", event_id="e", sample_index=1)
    ref = RestrictedSeedTraceStore(tmp_path / "trace.jsonl").append(trace)
    assert ref == trace.strategy_ref()["trace_ref"]
    assert all(name not in trace.strategy_ref() for name in ("master_seed", "stream_name", "logical_index", "sample_seed"))


@pytest.mark.parametrize("game_id,accepted", [("x", True), ("x" * 256, True), ("", False), ("x" * 257, False), ("牌局", True)])
def test_rng_identifier_utf8_boundaries(game_id, accepted):
    if accepted:
        assert derive_coordinate_seed(game_id=game_id, stream_name="deal", consumer_kind="engine", consumer_id="c", event_id="e", sample_index=0).sample_seed >= 0
    else:
        with pytest.raises(RngV2Error):
            derive_coordinate_seed(game_id=game_id, stream_name="deal", consumer_kind="engine", consumer_id="c", event_id="e", sample_index=0)


def test_rng_cross_process_is_identical():
    code = "from engine.rng_v2 import derive_coordinate_seed as d; print(d(game_id='g',stream_name='deal',consumer_kind='engine',consumer_id='c',event_id='e',sample_index=0).sample_seed)"
    values = [subprocess.check_output([sys.executable, "-c", code], text=True).strip() for _ in range(3)]
    assert len(set(values)) == 1


def test_seed_trace_audit_envelope_has_exact_seven_typed_fields():
    trace = derive_coordinate_seed(game_id="g", stream_name="deal", consumer_kind="engine", consumer_id="c", event_id="e", sample_index=0)
    envelope = trace.audit_envelope()
    assert set(envelope) == {"algorithm_version", "rng_version", "master_hash", "stream_names", "seed_hashes", "coordinate_hash", "trace_ref"}
    assert isinstance(envelope["algorithm_version"], int) and all(len(envelope[key]) == 64 for key in ("master_hash", "coordinate_hash", "trace_ref"))
    with pytest.raises(RngV2Error) as error:
        select_rng_version({"record_format": "rng-v2-new-record", "rng_version": 99})
    assert error.value.code == "RNG_VERSION_UNKNOWN"


def test_one_hundred_worker_schedules_retries_and_cancellation_do_not_change_coordinates():
    expected = {i: derive_coordinate_seed(game_id="sched", stream_name="training_noise", consumer_kind="trainer", consumer_id="pool", event_id="e", sample_index=i).sample_seed for i in range(32)}
    for schedule in range(100):
        order = list(expected); random.Random(schedule).shuffle(order)
        actual = {i: derive_coordinate_seed(game_id="sched", stream_name="training_noise", consumer_kind="trainer", consumer_id="pool", event_id="e", sample_index=i).sample_seed for i in order if i % 7 != 0}
        # Cancelled coordinates are simply absent; retries recompute, never advance shared state.
        assert all(actual[i] == expected[i] for i in actual)
        assert derive_coordinate_seed(game_id="sched", stream_name="training_noise", consumer_kind="trainer", consumer_id="pool", event_id="e", sample_index=1).sample_seed == expected[1]
