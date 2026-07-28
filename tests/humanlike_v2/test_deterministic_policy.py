from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path

import pytest

from engine.action import Action, ActionType
from engine.deal import create_dealt_game
from engine.tile import Suit, parse_tile
from players.humanlike.belief import build_public_belief
from players.humanlike.candidates import build_candidates, stable_action_key
from players.humanlike.config import load_config
from players.humanlike.evaluator import evaluate_candidates
from players.humanlike.player import HumanlikeV2Player, default_humanlike_config_path
from players.humanlike.view import PolicyInputError, build_decision_context
from protocols.messages import ActionRequest, Observation
from protocols.view_filter import build_observation


def _context(*, phase: str = "discard", actions: list[Action] | None = None):
    state = create_dealt_game("f28-context")
    obs = build_observation(state, 0)
    obs.phase = phase
    obs.view["phase"] = phase
    cfg = load_config(default_humanlike_config_path())
    legal = actions or [Action(ActionType.DISCARD, (parse_tile(obs.view["players"][0]["hand"][0]),))]
    req = ActionRequest("req", 0, phase, legal)
    return build_decision_context(obs, req, bound_seat=0, profile=cfg.players[0], config_hash=cfg.config_hash), cfg


def test_context_rejects_wrong_view_version_and_seat() -> None:
    context, cfg = _context()
    assert context.view.view_version == 2
    obs = Observation(context.view.game_id, 0, "discard", context.view.to_legacy_dict())
    obs.view["view_version"] = 1
    req = ActionRequest("bad", 0, "discard", list(context.legal_actions))
    with pytest.raises(PolicyInputError, match="version 2"):
        build_decision_context(obs, req, bound_seat=0, profile=cfg.players[0], config_hash=cfg.config_hash)
    seat_obs = build_observation(create_dealt_game("seat"), 0)
    seat_obs.phase = "discard"
    with pytest.raises(PolicyInputError, match="seats must match"):
        build_decision_context(seat_obs, ActionRequest("bad", 1, "discard", list(context.legal_actions)), bound_seat=0, profile=cfg.players[0], config_hash=cfg.config_hash)


def test_public_belief_uses_only_visible_counts() -> None:
    context, _ = _context()
    belief = build_public_belief(context)
    assert len(belief.visible_counts) == 27
    assert len(belief.unseen_counts) == 27
    assert all(v + u == 4 for v, u in zip(belief.visible_counts, belief.unseen_counts))
    assert sum(belief.visible_counts) in (13, 14)


def test_mandatory_hu_survives_candidate_cap() -> None:
    actions = [
        Action(ActionType.DISCARD, (parse_tile("wan_1"),)),
        Action(ActionType.DISCARD, (parse_tile("wan_2"),)),
        Action(ActionType.HU),
    ]
    context, _ = _context(actions=actions)
    candidates = build_candidates(context, max_candidates=1)
    assert any(item.action.type == ActionType.HU and item.mandatory for item in candidates.candidates)
    assert len(candidates.candidates) == 2


def test_stable_action_key_is_explicit() -> None:
    actions = [Action(ActionType.PASS), Action(ActionType.DISCARD, (parse_tile("tong_2"),)), Action(ActionType.HU)]
    assert [action.type for action in sorted(actions, key=stable_action_key)] == [ActionType.HU, ActionType.DISCARD, ActionType.PASS]


def test_evaluation_is_repeatable_and_rng_free() -> None:
    context, cfg = _context(actions=[Action(ActionType.DISCARD, (parse_tile("wan_1"),)), Action(ActionType.DISCARD, (parse_tile("wan_2"),))])
    belief = build_public_belief(context)
    candidates = build_candidates(context, max_candidates=8)
    first = evaluate_candidates(context, candidates, belief, cfg.global_parameters["GP-026"]["decision_weights"])
    second = evaluate_candidates(context, candidates, belief, cfg.global_parameters["GP-026"]["decision_weights"])
    assert first.selected == second.selected
    assert first.trace == second.trace
    assert first.trace["rng_used"] is False
    assert all(round(item.score, 8) == item.score for item in first.scored)


def test_player_dingque_and_trace_are_deterministic() -> None:
    state = create_dealt_game("f28-player")
    obs = build_observation(state, 0)
    obs.phase = "dingque"
    obs.view["phase"] = "dingque"
    actions = [Action(ActionType.DINGQUE, suit=suit) for suit in Suit]
    outputs = []
    for _ in range(3):
        player = HumanlikeV2Player(seed=999)
        player.on_join(0, {})
        player.observe(deepcopy(obs))
        outputs.append(player.decide(ActionRequest("same", 0, "dingque", actions)).to_dict())
    assert outputs[0] == outputs[1] == outputs[2]
    assert outputs[0]["analysis"]["rng_used"] is False


def test_hidden_opponent_hands_cannot_change_decision() -> None:
    first_state = create_dealt_game("f28-hidden")
    second_state = deepcopy(first_state)
    second_state.players[1].hand, second_state.players[2].hand = second_state.players[2].hand, second_state.players[1].hand
    first_obs = build_observation(first_state, 0)
    second_obs = build_observation(second_state, 0)
    first_obs.phase = second_obs.phase = "dingque"
    assert first_obs.view == second_obs.view
    actions = [Action(ActionType.DINGQUE, suit=suit) for suit in Suit]
    decisions = []
    for obs in (first_obs, second_obs):
        player = HumanlikeV2Player(seed=1)
        player.on_join(0, {})
        player.observe(obs)
        decisions.append(player.decide(ActionRequest("hidden", 0, "dingque", actions)).to_dict())
    assert decisions[0] == decisions[1]


def test_policy_sources_do_not_import_oracle_or_access_engine_state() -> None:
    root = Path(__file__).resolve().parents[2] / "players" / "humanlike"
    production = [path for path in root.glob("*.py") if path.name not in {"engine_adapter.py"}]
    for path in production:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        assert "training.oracle" not in source
        assert "_engine_state" not in source
        assert not any(isinstance(node, ast.Name) and node.id == "GameState" for node in ast.walk(tree))
