from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace

import pytest

from engine.deal import DealRequest, DealTransaction
from engine.match import MatchController, MatchCreateRequest, MatchError, SeatBinding
from engine.physical_tile import physical_tile
from engine.round_state_machine import RoundPhase, RoundSnapshot, RoundStateMachine, TransitionRequest
from players.random_player import RandomPlayer
from engine.orchestrator import PlayerGameRunner
from players.humanlike.config_v2 import CANONICAL_V2, CONTRACTS_V2, PARAMS_V2, FrozenConfigV2, canonical_v2_bytes
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from dataclasses import asdict
from engine.game_id import derive_seeds
from engine.rng_v2 import select_rng_version
from protocols.player_view_builder import PlayerViewBuilder


def match_request(n=4, **changes):
    base = MatchCreateRequest(
        event_id="create", match_id="m", expected_state_version=0,
        ruleset_hash="a" * 64, config_hash="b" * 64, seed_trace_ref="safe",
        bindings=tuple(SeatBinding(i, f"p{i}", f"profile{i}") for i in range(n)),
        total_rounds=1, starting_scores={i: 0 for i in range(n)},
    )
    return replace(base, **changes)


def test_state001_all_seat_counts_boundaries_schema_and_concurrent_idempotency():
    for n in (2, 3, 4):
        result = MatchController().create(match_request(n))
        assert result.accepted and tuple(x.seat for x in result.context.bindings) == tuple(range(n))
    for rounds, accepted in ((1, True), (10_000, True), (0, False), (10_001, False)):
        assert MatchController().create(match_request(total_rounds=rounds)).accepted is accepted
    raw = {name: getattr(match_request(), name) for name in MatchCreateRequest.__dataclass_fields__ if name != "frozen_config"}
    assert MatchCreateRequest.from_mapping(raw).match_id == "m"
    with pytest.raises(MatchError) as caught:
        MatchCreateRequest.from_mapping({**raw, "unknown": 1})
    assert caught.value.code == "SCHEMA_INVALID"
    controller = MatchController()
    with ThreadPoolExecutor(max_workers=16) as pool:
        results = list(pool.map(lambda _: controller.create(match_request()), range(100)))
    assert all(item.accepted for item in results)
    assert len({item.context.fingerprint for item in results}) == 1
    assert controller.context.state_version == 1


def test_state001_real_runner_chain_exposes_safe_context_only():
    runner = PlayerGameRunner([RandomPlayer() for _ in range(4)], game_id="b1b-match-chain", max_steps=3000)
    runner.run()
    assert runner.match_context is not None
    assert runner.match_controller.prepared_players == tuple(runner.players)
    public = dict(runner.match_context.public_projection())
    assert "master_seed" not in repr(public) and "profile" not in repr(public).lower()


def test_state001_runner_freezes_approved_config_bytes():
    value = {"parameter_version": PARAMS_V2, "contract_version": CONTRACTS_V2, "canonical_version": CANONICAL_V2}
    encoded = canonical_v2_bytes(value)
    frozen = FrozenConfigV2(value, encoded, hashlib.sha256(encoded).hexdigest(), None)
    runner = PlayerGameRunner([RandomPlayer() for _ in range(2)], game_id="b1b-frozen", max_steps=3000, frozen_config=frozen)
    runner.run()
    assert runner.match_context.config_canonical_bytes == encoded
    value["parameter_version"] = "mutated"
    assert runner.match_context.config_canonical_bytes == encoded


def test_state001_one_hundred_cross_process_full_match_bytes():
    code = r'''import json
from engine.match import MatchController,MatchCreateRequest,SeatBinding
c=MatchController(); r=c.create(MatchCreateRequest("e","m",0,"a"*64,"b"*64,"safe",tuple(SeatBinding(i,f"p{i}",f"profile{i}") for i in range(4)),1,{i:0 for i in range(4)})); d=c.complete_round(event_id="done",expected_state_version=1,scores={i:i for i in range(4)}); print(json.dumps({"context":r.context.fingerprint,"result":d.match_result.fingerprint,"rankings":d.match_result.rankings,"version":d.next_state_version},sort_keys=True,separators=(",",":")))'''
    values = [subprocess.check_output([sys.executable, "-c", code], text=True).strip() for _ in range(100)]
    assert len(set(values)) == 1


def test_state011_domains_faults_and_shared_concurrency():
    ok = DealTransaction().execute(DealRequest("ok", 0, "domain-game"))
    assert ok.accepted and set(ok.domain_trace_refs) == {"shuffle", "dice", "exchange"}
    assert len(set(ok.domain_trace_refs.values())) == 3

    duplicate = [physical_tile(i) for i in range(107)] + [physical_tile(0)]
    failed = DealTransaction(wall_builder=lambda: duplicate).execute(DealRequest("bad", 0, "fault-game"))
    assert failed.error_code == "DECK_DUPLICATE" and failed.game_state is None and failed.next_state_version == 0

    tx = DealTransaction()
    request = DealRequest("shared", 0, "shared-game")
    with ThreadPoolExecutor(max_workers=16) as pool:
        results = list(pool.map(lambda _: tx.execute(request), range(100)))
    assert all(item.accepted for item in results)
    assert tx.state_version == 1 and len({item.state_fingerprint for item in results}) == 1
    for stage, code in (("shuffle", "RNG_STREAM_MISSING"), ("deal", "DEAL_COUNT"), ("conservation", "CONSERVATION_FAILED")):
        faulty = DealTransaction(); faulty.inject_fault(stage)
        rejected = faulty.execute(DealRequest(stage, 0, f"fault-{stage}"))
        assert rejected.error_code == code and rejected.game_state is None and faulty.state_version == 0


def test_state011_approved_legacy_full_deal_golden():
    path = Path(__file__).with_name("fixtures") / "state011_legacy_deal_golden_v1.json"
    raw = path.read_bytes().strip()
    assert hashlib.sha256(raw).hexdigest() == "e806f33e58780a1ccdbaf306a417cd8d181dedd1173053ec4a98d5eada0547c5"
    expected = json.loads(raw)
    assert select_rng_version({"record_format": expected["record_format"]}) == "legacy-v1"
    state = DealTransaction().execute(DealRequest(
        "golden", 0, expected["game_id"], rng_version=1, algorithm_version=1,
        record_format=expected["record_format"],
    )).game_state
    actual = {
        "algorithm_version": 1, "dealer_seat": state.dealer_seat,
        "dice": state.dice.to_dict(), "fixture_version": expected["fixture_version"],
        "game_id": state.game_id,
        "hands": {str(player.seat): [tile.tile_id for tile in player.hand] for player in state.players},
        "record_format": expected["record_format"], "rng_version": 1,
        "seeds": asdict(derive_seeds(state.game_id)),
        "wall": [tile.tile_id for tile in state.wall],
    }
    assert actual == expected


def test_state011_committed_deal_hidden_perturbation_all_seats():
    committed = DealTransaction().execute(DealRequest("visible", 0, "hidden-pair")).game_state
    builder = PlayerViewBuilder()
    for seat in range(4):
        changed = deepcopy(committed)
        changed.wall.reverse()
        candidates = [player for player in changed.players if player.seat != seat and len(player.hand) == 13]
        if len(candidates) >= 2:
            candidates[0].hand, candidates[1].hand = candidates[1].hand, candidates[0].hand
        assert builder.build(committed, seat).stable_hash == builder.build(changed, seat).stable_hash


def test_state004_full_table_outbox_failure_and_runner_authority_chain():
    delivered = []
    machine = RoundStateMachine(RoundSnapshot(RoundPhase.CONFIGURED, 0, (0, 1, 2, 3), 55), outbox=lambda result: delivered.append(result.audit_ref))
    sequence = [
        ("DEAL_COMMITTED", {}), ("EXCHANGE_STARTED", {}), ("EXCHANGE_RESOLVED", {}),
        ("DINGQUE_RESOLVED", {}), ("PLAY_STARTED", {}), ("DISCARD_COMMITTED", {}),
        ("CLAIMS_PASSED", {}), ("WALL_EXHAUSTED", {}),
        ("SETTLEMENT_COMMITTED", {"settlement_hash": "a" * 64}),
    ]
    for index, (event, payload) in enumerate(sequence):
        result = machine.transition(TransitionRequest(str(index), index, event, "engine", payload))
        assert result.accepted
    assert machine.snapshot.phase is RoundPhase.SETTLED and len(delivered) == len(sequence)

    failing = RoundStateMachine(RoundSnapshot(RoundPhase.FINISHED, 0, (0,), 0), outbox=lambda _: (_ for _ in ()).throw(RuntimeError("notify")))
    committed = failing.transition(TransitionRequest("settle", 0, "SETTLEMENT_COMMITTED", "engine", {"settlement_hash": "b" * 64}))
    assert committed.accepted and failing.snapshot.phase is RoundPhase.SETTLED

    runner = PlayerGameRunner([RandomPlayer() for _ in range(4)], game_id="b1b-state004-chain", max_steps=3000)
    runner.run()
    assert runner.state004_machine.audit_records
    assert runner.state004_machine.snapshot.authority_hash
    assert runner.state004_machine.snapshot.phase in {RoundPhase.FINISHED, RoundPhase.SETTLED}


def test_state004_transaction_rolls_back_exact_state_on_failure():
    from engine.deal import create_dealt_game
    state = create_dealt_game("state004-rollback")
    before = state.to_dict()
    machine = RoundStateMachine(RoundSnapshot(RoundPhase.DEALT, 7, (0, 1, 2, 3), 55))
    def corrupt():
        state.wall.pop()
        state.players[0].hand.append(state.players[1].hand[0])
    result = machine.apply_legacy_transaction(state, event_id="bad", mutation=corrupt)
    assert not result.accepted and result.error_code == "INVARIANT_FAILED"
    assert state.to_dict() == before and machine.snapshot.state_version == 7


def test_state004_complete_phase_event_cartesian():
    events = {
        "DEAL_COMMITTED", "EXCHANGE_STARTED", "EXCHANGE_SKIPPED", "EXCHANGE_RESOLVED",
        "DINGQUE_RESOLVED", "PLAY_STARTED", "DRAW_COMPLETED", "DISCARD_COMMITTED",
        "CLAIMS_PASSED", "PONG_COMMITTED", "GANG_COMMITTED", "HU_RESOLVED",
        "WALL_EXHAUSTED", "GAME_FINISHED", "SETTLEMENT_COMMITTED",
    }
    expected = {
        (RoundPhase.CONFIGURED, "DEAL_COMMITTED"), (RoundPhase.DEALT, "EXCHANGE_STARTED"),
        (RoundPhase.DEALT, "EXCHANGE_SKIPPED"), (RoundPhase.EXCHANGE, "EXCHANGE_RESOLVED"),
        (RoundPhase.DINGQUE, "DINGQUE_RESOLVED"), (RoundPhase.READY, "PLAY_STARTED"),
        (RoundPhase.DRAW, "DRAW_COMPLETED"), (RoundPhase.DISCARD, "DISCARD_COMMITTED"),
        (RoundPhase.RESPONSE, "CLAIMS_PASSED"), (RoundPhase.RESPONSE, "PONG_COMMITTED"),
        (RoundPhase.RESPONSE, "GANG_COMMITTED"), (RoundPhase.DISCARD, "GANG_COMMITTED"),
        (RoundPhase.DISCARD, "HU_RESOLVED"), (RoundPhase.RESPONSE, "HU_RESOLVED"),
        (RoundPhase.DRAW, "WALL_EXHAUSTED"), (RoundPhase.DISCARD, "WALL_EXHAUSTED"),
        (RoundPhase.RESPONSE, "WALL_EXHAUSTED"), (RoundPhase.DRAW, "GAME_FINISHED"),
        (RoundPhase.DISCARD, "GAME_FINISHED"), (RoundPhase.RESPONSE, "GAME_FINISHED"),
        (RoundPhase.FINISHED, "SETTLEMENT_COMMITTED"),
    }
    accepted = set()
    for phase in RoundPhase:
        for index, event in enumerate(sorted(events)):
            payload = {"hu_seats": [1]} if event == "HU_RESOLVED" else {"settlement_hash": "a" * 64} if event == "SETTLEMENT_COMMITTED" else {}
            machine = RoundStateMachine(RoundSnapshot(phase, 0, (0, 1, 2, 3), 55))
            result = machine.transition(TransitionRequest(f"{phase.value}-{index}", 0, event, "engine", payload))
            if result.accepted:
                accepted.add((phase, event))
            else:
                assert result.snapshot.phase is phase and result.snapshot.state_version == 0
                assert result.error_code in {"ILLEGAL_TRANSITION", "TERMINAL_STATE"}
    assert accepted == expected


def test_state004_ordered_hu_and_transactional_claim_effects():
    machine = RoundStateMachine(RoundSnapshot(RoundPhase.RESPONSE, 0, (0, 1, 2, 3), 20))
    first = machine.transition(TransitionRequest("hu-1", 0, "HU_RESOLVED", "engine", {"hu_seats": [2]}))
    assert first.snapshot.phase is RoundPhase.DRAW and first.snapshot.active_seats == (0, 1, 3)
    machine.transition(TransitionRequest("draw", 1, "DRAW_COMPLETED", "engine", {}))
    machine.transition(TransitionRequest("discard", 2, "DISCARD_COMMITTED", "engine", {}))
    second = machine.transition(TransitionRequest("hu-2", 3, "HU_RESOLVED", "engine", {"hu_seats": [3, 1]}))
    assert second.snapshot.phase is RoundPhase.FINISHED and second.snapshot.active_seats == (0,)

    from engine.deal import create_dealt_game
    state = create_dealt_game("state004-claim-effects")
    state.phase = "response"
    state.response_seats = [1, 2]
    from engine.action import Action, ActionType
    state.pending_claims = {1: Action(ActionType.PASS)}
    state.validate()
    authority = RoundStateMachine(RoundSnapshot(RoundPhase.RESPONSE, 5, (0, 1, 2, 3), len(state.wall), pending_claim_seats=(1,)))
    wall_before = len(state.wall)
    owner_before = len(state.players[2].hand)
    def committed_gang_effect():
        state.pending_claims = {}
        state.response_seats = []
        state.current_seat = 2
        state.players[2].hand.append(state.wall.pop(0))
        state.phase = "discard"
    result = authority.apply_legacy_transaction(state, event_id="gang-effect", mutation=committed_gang_effect)
    assert result.accepted and result.snapshot.pending_claim_seats == ()
    assert len(state.wall) == wall_before - 1 and len(state.players[2].hand) == owner_before + 1
    assert result.snapshot.current_seat == 2


@pytest.mark.parametrize("effect,draws", [("pong", 0), ("gang_ming", 1), ("gang_an", 1), ("gang_jia", 1)])
def test_state004_pong_and_three_gang_transaction_effects(effect, draws):
    from engine.deal import create_dealt_game
    from engine.action import Action, ActionType
    state = create_dealt_game(f"state004-{effect}")
    state.phase = "response" if effect in {"pong", "gang_ming"} else "discard"
    state.current_seat = 1
    state.response_seats = [1, 2] if state.phase == "response" else []
    state.pending_claims = {2: Action(ActionType.PASS)} if state.phase == "response" else {}
    state.validate()
    machine = RoundStateMachine(RoundSnapshot(
        RoundPhase.RESPONSE if state.phase == "response" else RoundPhase.DISCARD,
        0, (0, 1, 2, 3), len(state.wall), pending_claim_seats=tuple(state.pending_claims), current_seat=1,
    ))
    wall_before = len(state.wall)
    hand_before = len(state.players[1].hand)
    def effect_commit():
        state.pending_claims = {}
        state.response_seats = []
        if draws:
            state.players[1].hand.append(state.wall.pop(0))
            state.after_gang_draw = True
        state.phase = "discard"
    committed = machine.apply_legacy_transaction(state, event_id=effect, mutation=effect_commit)
    assert committed.accepted and committed.snapshot.pending_claim_seats == ()
    assert len(state.wall) == wall_before - draws
    assert len(state.players[1].hand) == hand_before + draws
    assert state.after_gang_draw is bool(draws)
