"""M08 — analysis pipeline tests."""

from __future__ import annotations

import os

import pytest

from engine.action import Action, ActionType
from engine.session import build_ready_game
from engine.blood_battle import start_play
from engine.legal import legal_actions
from players.analysis.pipeline import analyze_for_seat
from players.analysis.remain import remain_map
from players.rule_ai_player import RuleAIPlayer
from protocols.messages import ActionRequest
from engine.tile import Suit, Tile


def test_an01_remain_bounds() -> None:
    state = build_ready_game("m08-rem", num_players=4)
    rem = remain_map(state, 0)
    assert len(rem) == 27
    assert all(0 <= v <= 4 for v in rem.values())
    # self hand counted: some tiles have remain < 4
    assert sum(1 for v in rem.values() if v < 4) > 0


def test_an02_discards_safer() -> None:
    state = build_ready_game("m08-dang", num_players=2)
    start_play(state)
    # put a tile in discard piles
    t = Tile(Suit.WAN, 5)
    state.players[0].discard_pile.append(t)
    state.players[1].discard_pile.append(t)
    snap = analyze_for_seat(state, 0)
    if "wan_5" in snap.danger:
        assert snap.danger["wan_5"] in ("safe", "low", "unknown", "medium")


def test_an03_strategy_best_min_shanten() -> None:
    state = build_ready_game("m08-str", num_players=2)
    start_play(state)
    seat = state.current_seat
    assert seat is not None
    legal = [a for a in legal_actions(state, seat) if a.type == ActionType.DISCARD]
    snap = analyze_for_seat(state, seat, legal_discards=legal)
    if len(snap.discard_ranks) >= 2:
        best = snap.discard_ranks[0]
        assert best.mark == "best"
        # best shanten should be minimal among ranks
        min_sh = min(a.shanten_after for a in snap.discard_ranks)
        assert best.shanten_after == min_sh


def test_an04_no_state_mutation() -> None:
    state = build_ready_game("m08-immut", num_players=2)
    before = state.to_dict()
    analyze_for_seat(state, 0)
    after = state.to_dict()
    assert before["players"][0]["concealed_tile_ids"] == after["players"][0]["concealed_tile_ids"]
    assert before["wall_tile_ids"] == after["wall_tile_ids"]


def test_an05_rule_ai_pipeline_analysis() -> None:
    state = build_ready_game("m08-ai", num_players=2)
    start_play(state)
    seat = state.current_seat
    p = RuleAIPlayer(seed=1)
    p.on_join(seat, {})
    p._engine_state = state
    legal = legal_actions(state, seat)
    discards = [a for a in legal if a.type == ActionType.DISCARD]
    if not discards:
        pytest.skip("no discards")
    # need observation for dingque path etc.
    from protocols.view_filter import build_observation

    p.observe(build_observation(state, seat))
    req = ActionRequest.create(seat, "discard", legal)
    dec = p.decide(req)
    assert dec.reason
    if dec.action.type == ActionType.DISCARD:
        assert dec.analysis is not None
        assert "shanten" in dec.analysis or "best" in dec.analysis


def test_an06_assets_danger_strategy() -> None:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame

    pygame.init()
    from display.asset_manager import AssetManager

    am = AssetManager(theme="green")
    assert am.danger("safe").get_width() > 0
    assert am.strategy_asset("mark_best").get_width() > 0
    assert am.inference("tenpai_active").get_width() > 0
