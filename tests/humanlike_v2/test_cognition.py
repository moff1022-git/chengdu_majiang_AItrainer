from __future__ import annotations

from dataclasses import replace

from engine.action import Action, ActionType
from engine.deal import create_dealt_game
from engine.tile import parse_tile
from players.humanlike.attention import select_attention
from players.humanlike.belief import build_public_belief
from players.humanlike.candidates import build_candidates
from players.humanlike.cognition import (
    CognitiveState,
    effective_attention_capacity,
    effective_candidate_capacity,
    effective_satisfaction_threshold,
)
from players.humanlike.config import load_config
from players.humanlike.evaluator import EvaluationResult, evaluate_candidates
from players.humanlike.memory import MemoryStore, VisibleToken
from players.humanlike.player import default_humanlike_config_path
from players.humanlike.player import HumanlikeV2Player
from players.humanlike.policy import select_cognitively
from players.humanlike.view import build_decision_context
from protocols.messages import ActionRequest
from protocols.view_filter import build_observation


def _fixture(actions: list[Action] | None = None):
    state = create_dealt_game("f28-cognition")
    observation = build_observation(state, 0)
    observation.phase = "discard"
    observation.view["phase"] = "discard"
    cfg = load_config(default_humanlike_config_path())
    actions = actions or [
        Action(ActionType.DISCARD, (parse_tile(observation.view["players"][0]["hand"][0]),)),
        Action(ActionType.DISCARD, (parse_tile(observation.view["players"][0]["hand"][1]),)),
    ]
    request = ActionRequest("cognitive", 0, "discard", actions, deadline_ms=3000)
    context = build_decision_context(
        observation,
        request,
        bound_seat=0,
        profile=cfg.players[0],
        config_hash=cfg.config_hash,
    )
    belief = build_public_belief(context)
    candidates = build_candidates(context, max_candidates=8)
    evaluation = evaluate_candidates(
        context,
        candidates,
        belief,
        cfg.players[0].cognitive_parameters["GP-026"]["decision_weights"],
    )
    state = CognitiveState.create(context.view.game_id, cfg.players[0].cognitive_parameters["GP-024"])
    state.update_plan(context, evaluation.plan)
    return context, cfg, candidates, evaluation, state


def test_memory_decay_fuzziness_and_public_reinforcement() -> None:
    memory = MemoryStore(initial_strength=0.3, forget_rate=0.5, salience_boost=0.2, capacity=2)
    token = VisibleToken("discard:S1:wan_1:0", "discard", "S1:wan_1", 0.5)
    first = memory.update(1, [token])
    assert first.exact == 1
    memory.update(10, [])
    item = memory.items[token.key]
    assert item.exact is False
    assert item.summary == "discard"
    strength = item.strength
    memory.update(11, [])
    assert memory.items[token.key].strength < strength
    assert memory.items[token.key].exact is False
    memory.update(12, [token])
    assert memory.items[token.key].exact is True
    assert memory.items[token.key].reinforcements == 2


def test_cumulative_visible_history_is_not_a_new_memory_prompt() -> None:
    memory = MemoryStore(initial_strength=0.3, forget_rate=0.5, salience_boost=0.0, capacity=4)
    token = VisibleToken("discard:S1:wan_1:0", "discard", "S1:wan_1", 0.5)
    memory.update(1, [token])
    memory.update(10, [token])
    assert memory.items[token.key].exact is False
    assert memory.items[token.key].reinforcements == 1


def test_memory_capacity_evicts_stably() -> None:
    memory = MemoryStore(initial_strength=0.4, forget_rate=0.0, salience_boost=0.1, capacity=2)
    tokens = [VisibleToken(f"k{index}", "discard", f"v{index}", 0.5) for index in range(3)]
    summary = memory.update(1, tokens)
    assert tuple(sorted(memory.items)) == ("k1", "k2")
    assert summary.forgotten == 1


def test_attention_is_top_k_then_softmax() -> None:
    context, _, candidates, _, state = _fixture()
    state.memory.update(1, [VisibleToken("high", "recent", "event", 1.0)])
    focus = select_attention(context, candidates, state.memory, capacity=2)
    assert len(focus) == 2
    assert [item.salience for item in focus] == sorted((item.salience for item in focus), reverse=True)
    assert abs(sum(item.weight for item in focus) - 1.0) <= 1e-8
    assert all(item.weight > 0 for item in focus)


def test_level_and_style_parameters_are_monotonic() -> None:
    assert effective_candidate_capacity("novice", 2, 10) < effective_candidate_capacity("expert", 2, 10)
    assert effective_attention_capacity("novice", 10) < effective_attention_capacity("expert", 10)
    novice = effective_satisfaction_threshold("novice", "conservative", 0.72)
    expert = effective_satisfaction_threshold("expert", "aggressive", 0.72)
    assert novice < expert
    assert 0.45 <= novice <= expert <= 0.95


def test_mandatory_action_never_consumes_rng() -> None:
    context, cfg, candidates, evaluation, state = _fixture([Action(ActionType.HU)])
    decision = select_cognitively(
        context,
        evaluation,
        state,
        gp022=cfg.global_parameters["GP-022"],
        gp025={**cfg.players[0].cognitive_parameters["GP-025"], "max_error_probability": 1.0, "near_equal_randomness": 1.0},
        gp026=cfg.players[0].cognitive_parameters["GP-026"],
        config_seed=cfg.seed,
        plan_restarted=False,
        restart_reasons=(),
    )
    assert decision.selected.type is ActionType.HU
    assert decision.trace["stop_reason"] == "mandatory"
    assert decision.trace["rng_used"] is False
    assert decision.trace["rng_index_before"] == decision.trace["rng_index_after"] == 0


def test_bounded_noise_is_reproducible_and_stays_in_near_pool() -> None:
    context, cfg, _, evaluation, _ = _fixture()
    close = tuple(replace(item, score=0.50000000 - index * 0.001) for index, item in enumerate(evaluation.scored))
    synthetic = EvaluationResult(close[0].action, evaluation.plan, close, evaluation.trace)
    outputs = []
    for _ in range(2):
        state = CognitiveState.create(context.view.game_id, cfg.players[0].cognitive_parameters["GP-024"])
        state.update_plan(context, evaluation.plan)
        result = select_cognitively(
            context,
            synthetic,
            state,
            gp022=cfg.global_parameters["GP-022"],
            gp025={**cfg.players[0].cognitive_parameters["GP-025"], "max_error_probability": 1.0, "near_equal_randomness": 1.0},
            gp026={**cfg.players[0].cognitive_parameters["GP-026"], "satisfaction_threshold": 0.95},
            config_seed=99,
            plan_restarted=True,
            restart_reasons=("fixture",),
        )
        outputs.append(result)
    assert outputs[0].selected.to_dict() == outputs[1].selected.to_dict()
    assert outputs[0].trace == outputs[1].trace
    assert outputs[0].trace["rng_used"] is True
    assert outputs[0].trace["noise_pool_size"] == len(close)
    assert outputs[0].selected.to_dict() in [item.action.to_dict() for item in close]


def test_clear_score_gap_disables_noise_and_think_time_is_bounded() -> None:
    context, cfg, _, evaluation, state = _fixture()
    separated = tuple(replace(item, score=0.9 - index * 0.2) for index, item in enumerate(evaluation.scored))
    synthetic = EvaluationResult(separated[0].action, evaluation.plan, separated, evaluation.trace)
    result = select_cognitively(
        context,
        synthetic,
        state,
        gp022=cfg.global_parameters["GP-022"],
        gp025={**cfg.players[0].cognitive_parameters["GP-025"], "max_error_probability": 1.0, "near_equal_randomness": 0.1},
        gp026=cfg.players[0].cognitive_parameters["GP-026"],
        config_seed=7,
        plan_restarted=False,
        restart_reasons=(),
    )
    assert result.selected.to_dict() == separated[0].action.to_dict()
    assert result.trace["rng_used"] is False
    assert 0 <= result.trace["think_time_ms"] <= cfg.global_parameters["GP-022"]["max_performance_delay_ms"]


def test_round_reset_keeps_only_bounded_public_impressions() -> None:
    _, cfg, _, _, state = _fixture()
    state.memory.update(1, [VisibleToken("discard:S1:wan_1:0", "discard", "S1:wan_1", 1.0)])
    state.primary_plan = "fast_win"
    state.begin_new_round("next-round", cfg.players[0].cognitive_parameters["GP-024"], attention_capacity=4)
    assert state.game_id == "next-round"
    assert state.memory.items == {}
    assert state.primary_plan is None
    assert state.opponent_impressions == [{"round": "f28-cognition", "public_categories": {"discard": 1}}]


def test_player_emits_trace_v2_and_cognitive_rp_slots() -> None:
    context, _, _, _, _ = _fixture()
    observation = build_observation(create_dealt_game(context.view.game_id), 0)
    observation.phase = "discard"
    observation.view["phase"] = "discard"
    tile = parse_tile(observation.view["players"][0]["hand"][0])
    player = HumanlikeV2Player(seed=4)
    player.on_join(0, {})
    player.observe(observation)
    decision = player.decide(ActionRequest("trace-v2", 0, "discard", [Action(ActionType.DISCARD, (tile,))]))
    assert decision.analysis["trace_version"] == 2
    assert decision.analysis["policy"] == "humanlike_v2_cognitive"
    assert decision.analysis["stop_reason"] == "mandatory"
    assert decision.analysis["rng_used"] is False
    assert "memory" in decision.analysis and "attention" in decision.analysis
    values = player.runtime.snapshot().values
    for parameter_id in ("RP-024", "RP-025", "RP-026", "RP-027", "RP-028", "RP-029"):
        assert values[parameter_id] is not None
    assert values["RP-029"][-1]["selected_action"] == decision.action.to_dict()
