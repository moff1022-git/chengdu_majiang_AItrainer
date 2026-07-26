"""M06 — BasePlayer / AI / orchestrator tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine.action import Action, ActionType
from engine.orchestrator import PlayerGameRunner, run_players_game
from engine.tile import Suit, Tile
from players.random_player import RandomPlayer
from players.registry import create_player, create_players
from players.rule_ai_player import RuleAIPlayer
from protocols.messages import ActionRequest


def test_p02_random_decisions_legal() -> None:
    p = RandomPlayer(seed=1)
    p.on_join(0, {})
    legal = [
        Action(ActionType.DISCARD, tiles=(Tile(Suit.WAN, 1),)),
        Action(ActionType.DISCARD, tiles=(Tile(Suit.WAN, 2),)),
        Action(ActionType.PASS),
    ]
    for _ in range(50):
        req = ActionRequest.create(0, "response", legal)
        dec = p.decide(req)
        assert dec.reason
        assert dec.action in legal or any(
            a.type == dec.action.type
            and tuple(t.id for t in a.tiles) == tuple(t.id for t in dec.action.tiles)
            for a in legal
        )


def test_p03_rule_ai_prefers_hu() -> None:
    p = RuleAIPlayer(seed=0)
    p.on_join(0, {})
    legal = [
        Action(ActionType.PASS),
        Action(ActionType.PONG, tiles=(Tile(Suit.WAN, 3),)),
        Action(ActionType.HU),
    ]
    req = ActionRequest.create(0, "response", legal)
    dec = p.decide(req)
    assert dec.action.type == ActionType.HU
    assert "hu" in dec.reason


def test_p04_four_rule_ai_finishes() -> None:
    result = run_players_game(
        "rule_ai,rule_ai,rule_ai,rule_ai",
        game_id="m06-4ai",
        base_seed=7,
        max_steps=8000,
    )
    assert result.finished_reason in ("last_one", "wall_empty", "max_steps")
    assert len(result.rankings) == 4


def test_p05_mixed_games(tmp_path: Path) -> None:
    for i in range(5):
        result = run_players_game(
            "rule_ai,random,rule_ai,random",
            game_id=f"m06-mix-{i}",
            base_seed=100 + i,
            log_dir=tmp_path if i == 0 else None,
            max_steps=8000,
        )
        assert result.game_id
    # decision lines when logged
    path = tmp_path / "m06-mix-0.jsonl"
    if path.exists():
        types = [json.loads(l)["type"] for l in path.read_text(encoding="utf-8").splitlines() if l]
        assert "decision" in types or "game_end" in types


def test_p06_reason_nonempty() -> None:
    p = RuleAIPlayer(seed=2)
    p.on_join(1, {})
    legal = [Action(ActionType.DINGQUE, suit=s) for s in Suit]
    dec = p.decide(ActionRequest.create(1, "dingque", legal))
    assert dec.reason


def test_registry() -> None:
    players = create_players("random,rule_ai", base_seed=0)
    assert len(players) == 2
    assert isinstance(players[0], RandomPlayer)
    assert isinstance(players[1], RuleAIPlayer)
    with pytest.raises(ValueError):
        create_player("unknown_bot")
