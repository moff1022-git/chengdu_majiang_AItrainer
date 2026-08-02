from __future__ import annotations

from engine.config import EngineConfig
from engine.deal import create_dealt_game
from players.analysis.pipeline import analyze_for_seat


def test_current_recommendation_algorithms_do_not_enable_f0011() -> None:
    state = create_dealt_game("recommend-contract-001", config=EngineConfig(num_players=4))
    for algorithm in ("rule_ai", "rule_ai_plus", "humanlike_v2"):
        snap = analyze_for_seat(state, 0, recommendation_algorithm=algorithm)
        assert snap.use_f0011 is False


def test_recommendation_ranking_stays_within_legal_discards() -> None:
    state = create_dealt_game("recommend-contract-002", config=EngineConfig(num_players=4))
    snap = analyze_for_seat(state, 0, recommendation_algorithm="humanlike_v2", humanlike_preset="novice_balanced")
    hand_ids = {tile.id for tile in state.players[0].hand}
    assert {item.tile_id for item in snap.discard_ranks} <= hand_ids
