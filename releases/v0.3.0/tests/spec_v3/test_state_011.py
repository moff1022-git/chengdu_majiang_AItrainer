from concurrent.futures import ThreadPoolExecutor

from engine.deal import DealRequest, DealTransaction, create_dealt_game


def test_state011_closed_set_counts_and_safe_trace():
    result = DealTransaction().execute(DealRequest("deal-1", 0, "state011-golden"))
    assert result.accepted and result.conservation == {"tiles":108,"players":4,"wall":55}
    all_ids = [t.tile_id for t in result.game_state.wall]
    for player in result.game_state.players:
        all_ids += [t.tile_id for t in player.hand]
    assert set(all_ids) == set(range(108)) and len(all_ids) == 108
    assert len(result.seed_trace_ref) == 64


def test_state011_legacy_result_is_unchanged_and_v2_is_deterministic():
    legacy_direct = create_dealt_game("legacy-state011", rng_version=1).to_dict()
    legacy_tx = DealTransaction().execute(DealRequest("legacy",0,"legacy-state011",rng_version=1,algorithm_version=1,record_format="legacy-pre-rng-version"))
    assert legacy_tx.accepted and legacy_tx.game_state.to_dict() == legacy_direct
    def run(_):
        return DealTransaction().execute(DealRequest("v2",0,"v2-state011")).state_fingerprint
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert len(set(pool.map(run, range(100)))) == 1


def test_state011_versions_cas_and_event_idempotency():
    tx = DealTransaction()
    unknown = tx.execute(DealRequest("bad",0,"x",rng_version=3,algorithm_version=3))
    assert unknown.error_code == "RNG_VERSION_UNKNOWN" and tx.state_version == 0
    stale = tx.execute(DealRequest("stale",1,"x"))
    assert stale.error_code == "VERSION_CONFLICT" and tx.state_version == 0
    first = tx.execute(DealRequest("ok",0,"x"))
    again = tx.execute(DealRequest("ok",0,"x"))
    assert first is again and tx.state_version == 1
    conflict = tx.execute(DealRequest("ok",0,"different"))
    assert conflict.error_code == "SCHEMA_INVALID" and tx.state_version == 1


def test_state011_player_counts_dealer_hands_and_domain_difference():
    fingerprints = []
    for n in (2,3,4):
        result = DealTransaction().execute(DealRequest(f"e{n}",0,f"game{n}",num_players=n))
        assert result.accepted
        lengths = [len(p.hand) for p in result.game_state.players]
        assert lengths.count(14) == 1 and lengths.count(13) == n-1
        assert len(result.game_state.wall) == 108-(13*n+1)
        fingerprints.append(result.state_fingerprint)
    assert len(set(fingerprints)) == 3

