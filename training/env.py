"""Gymnasium-style single-agent env for Chengdu blood-battle mahjong (M11)."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any
from uuid import uuid4

from engine.action import Action, ActionType
from engine.blood_battle import (
    GameResult,
    PlayError,
    build_game_result,
    do_draw,
    finalize_game,
    start_play,
)
from engine.config import EngineConfig
from engine.deal import create_dealt_game
from engine.exchange import pick_same_suit_triple, validate_exchange_tiles
from engine.legal import action_in_legal, legal_actions
from engine.opening import begin_opening, submit_dingque, submit_exchange
from engine.reward import RewardCalculator, RewardConfig
from engine.session import GameSession
from engine.state import GameState
from engine.tile import Suit
from players.base_player import BasePlayer
from players.registry import create_player
from protocols.messages import ActionRequest
from protocols.view_filter import build_observation, filter_state_for_seat
from training.episode_log import EpisodeLogger
from training.spaces import (
    encode_obs_vector,
    enumerate_exchange_actions,
    opening_dingque_actions,
)

__all__ = [
    "ChengduMahjongEnv",
    "encode_obs_vector",
    "smoke_random_episode",
]


class EnvError(RuntimeError):
    """Invalid env usage or illegal action."""


class ChengduMahjongEnv:
    """
    Single-seat learner API; other seats use fixed BasePlayer opponents.

    step returns Gymnasium 5-tuple:
      obs, reward, terminated, truncated, info
    """

    def __init__(
        self,
        *,
        learner_seat: int = 0,
        num_players: int = 4,
        opponent_spec: str = "rule_ai",
        opponents: str | None = None,
        reward_config: RewardConfig | None = None,
        engine_config: EngineConfig | None = None,
        log_dir: Path | str | None = None,
        seed: int | None = None,
        max_episode_steps: int = 10_000,
    ) -> None:
        if num_players not in (2, 3, 4):
            raise ValueError(f"num_players must be 2-4, got {num_players}")
        if not 0 <= learner_seat < num_players:
            raise ValueError(
                f"learner_seat {learner_seat} out of range for {num_players}p"
            )
        self.learner_seat = learner_seat
        self.num_players = num_players
        self.opponent_spec = opponent_spec
        self.opponents_csv = opponents
        self.reward_config = reward_config
        self.engine_config = engine_config
        self.log_dir = Path(log_dir) if log_dir else None
        self.seed = seed
        self.max_episode_steps = max_episode_steps

        self._state: GameState | None = None
        self.config: EngineConfig | None = None
        self.players: dict[int, BasePlayer] = {}
        self.reward_calc: RewardCalculator | None = None
        self.session: GameSession | None = None
        self.logger: EpisodeLogger | None = None
        self._episode_result: GameResult | None = None
        self._internal_steps = 0
        self._learner_steps = 0
        self._pending_legals: list[Action] = []
        self._request_id: str = ""
        self._reward_baseline = 0.0
        self._closed = False
        self._rng = random.Random(seed if seed is not None else 0)

    # --- public API -------------------------------------------------------

    @property
    def state(self) -> GameState:
        if self._state is None:
            raise EnvError("call reset() first")
        return self._state

    @property
    def episode_result(self) -> GameResult | None:
        return self._episode_result

    def reset(
        self, game_id: str | None = None, *, seed: int | None = None
    ) -> dict[str, Any]:
        if self._closed:
            raise EnvError("env is closed")
        self.close_episode()
        if seed is not None:
            self.seed = seed
            self._rng = random.Random(seed)

        cfg = self.engine_config or EngineConfig(num_players=self.num_players)
        if cfg.num_players != self.num_players:
            cfg = EngineConfig(
                num_players=self.num_players,
                initial_score=cfg.initial_score,
                exchange_dir=cfg.exchange_dir,
                fan_cap=cfg.fan_cap,
                multi_ron=cfg.multi_ron,
                base_score=cfg.base_score,
                force_discard_dingque=cfg.force_discard_dingque,
            )
        self.config = cfg

        base_seed = self.seed if self.seed is not None else self._rng.randint(0, 1 << 30)
        self.players = self._build_opponents(base_seed)
        self.reward_calc = RewardCalculator(self.reward_config)
        self.reward_calc.reset()

        state = create_dealt_game(game_id, config=cfg)
        self._state = state
        self.session = None
        self._episode_result = None
        self._internal_steps = 0
        self._learner_steps = 0
        self._pending_legals = []
        self._request_id = ""
        self._reward_baseline = 0.0

        if self.log_dir is not None:
            self.logger = EpisodeLogger(self.log_dir, state.game_id, log_private=True)
            self.logger.emit(
                "game_start",
                game_id=state.game_id,
                seed=state.master_seed,
                config=cfg.to_dict(),
                learner_seat=self.learner_seat,
            )
        else:
            self.logger = None

        join_cfg = cfg.to_dict()
        for seat, pl in self.players.items():
            pl.on_join(seat, join_cfg)

        begin_opening(state, cfg)
        self._advance_until_learner_or_done()
        if self._is_done():
            self._finalize_episode()
            return self._terminal_obs()
        return self._build_obs()

    def step(
        self, action: Action | dict | int
    ) -> tuple[dict[str, Any], float, bool, bool, dict[str, Any]]:
        if self._closed:
            raise EnvError("env is closed")
        if self._state is None:
            raise EnvError("call reset() first")
        if self._is_done():
            raise EnvError("episode finished; call reset()")
        if not self._pending_legals:
            raise EnvError("no pending learner decision")

        resolved = self._resolve_action(action)
        if not action_in_legal(resolved, self._pending_legals):
            raise EnvError(
                f"illegal action {resolved}; not in legal_actions "
                f"({len(self._pending_legals)} options)"
            )

        score_before = self._learner_score()
        reward_before = self._reward_baseline

        self._apply_learner_action(resolved)
        self._learner_steps += 1
        self._advance_until_learner_or_done()

        terminated = False
        truncated = False
        if self._is_done():
            self._finalize_episode()
            terminated = True
        elif self._internal_steps >= self.max_episode_steps:
            self._state.phase = "finished"
            self._state.finished_reason = "max_steps"
            self._finalize_episode()
            truncated = True

        reward_after = (
            self.reward_calc.episode_rewards.get(self.learner_seat, 0.0)
            if self.reward_calc
            else 0.0
        )
        reward = float(reward_after - reward_before)
        self._reward_baseline = reward_after

        score_after = self._learner_score()
        info = self._build_info(score_before, score_after)
        if terminated or truncated:
            obs = self._terminal_obs()
            if self._episode_result is not None:
                info["result"] = self._episode_result.to_dict()
        else:
            obs = self._build_obs()
        return obs, reward, terminated, truncated, info

    def legal_actions(self) -> list[Action]:
        return list(self._pending_legals)

    def legal_action_dicts(self) -> list[dict]:
        return [a.to_dict() for a in self._pending_legals]

    def close(self) -> None:
        self.close_episode()
        self._closed = True

    def close_episode(self) -> None:
        for pl in self.players.values():
            try:
                pl.shutdown()
            except Exception:
                pass
        self.players = {}
        if self.logger is not None:
            try:
                self.logger.close()
            except Exception:
                pass
            self.logger = None

    # --- opponents --------------------------------------------------------

    def _build_opponents(self, base_seed: int) -> dict[int, BasePlayer]:
        if self.opponents_csv:
            parts = [p.strip() for p in self.opponents_csv.split(",") if p.strip()]
            if len(parts) != self.num_players - 1:
                raise ValueError(
                    f"opponents must list {self.num_players - 1} specs "
                    f"(excluding learner), got {len(parts)}"
                )
        else:
            parts = [self.opponent_spec] * (self.num_players - 1)

        out: dict[int, BasePlayer] = {}
        oi = 0
        for seat in range(self.num_players):
            if seat == self.learner_seat:
                continue
            spec = parts[oi]
            oi += 1
            key = spec.split(":")[0].strip().lower()
            if key == "human":
                raise ValueError("human is not allowed as env opponent")
            out[seat] = create_player(
                spec,
                seat=seat,
                seed=base_seed + seat * 9973,
                training_mode=True,
            )
        return out

    # --- advance / apply --------------------------------------------------

    def _is_done(self) -> bool:
        return self._state is not None and self._state.phase == "finished"

    def _player_state(self, seat: int):
        assert self._state is not None
        for p in self._state.players:
            if p.seat == seat:
                return p
        raise PlayError(f"missing seat {seat}")

    def _advance_until_learner_or_done(self) -> None:
        assert self._state is not None and self.config is not None
        state = self._state
        cfg = self.config

        while state.phase != "finished":
            self._internal_steps += 1
            if self._internal_steps > self.max_episode_steps:
                state.phase = "finished"
                state.finished_reason = "max_steps"
                return

            if state.phase == "exchange":
                waiting = self._exchange_waiting()
                if not waiting:
                    # resolve should have moved phase; safety
                    return
                seat = waiting[0]
                if seat == self.learner_seat:
                    hand = self._player_state(seat).hand
                    self._pending_legals = enumerate_exchange_actions(hand)
                    if not self._pending_legals:
                        triple = pick_same_suit_triple(hand)
                        self._pending_legals = [
                            Action(ActionType.EXCHANGE, tiles=tuple(triple))
                        ]
                    self._request_id = uuid4().hex[:12]
                    return
                self._opp_opening_exchange(seat)
                continue

            if state.phase == "dingque":
                waiting = self._dingque_waiting()
                if not waiting:
                    return
                seat = waiting[0]
                if seat == self.learner_seat:
                    self._pending_legals = opening_dingque_actions()
                    self._request_id = uuid4().hex[:12]
                    return
                self._opp_opening_dingque(seat)
                continue

            if state.phase == "ready":
                self.session = GameSession(
                    state,
                    cfg,
                    logger=self.logger,
                    reward_calc=self.reward_calc,
                )
                start_play(state, cfg)
                if self.logger:
                    self.logger.emit("phase", phase="discard", dealer=state.dealer_seat)
                continue

            if state.phase == "draw":
                do_draw(state)
                if self.session:
                    self.session._flush_score_rewards()
                continue

            if state.phase == "discard":
                seat = state.current_seat
                if seat is None:
                    raise PlayError("current_seat is None")
                # Blood-battle: if current seat already hu'd, skip to next active
                if self._player_state(seat).status != "active":
                    from engine.blood_battle import next_active

                    nxt = next_active(state, seat)
                    if nxt is None:
                        state.phase = "finished"
                        state.finished_reason = state.finished_reason or "last_one"
                        return
                    state.current_seat = nxt
                    state.phase = "draw"
                    continue
                if seat == self.learner_seat and self._player_state(seat).status == "active":
                    self._pending_legals = legal_actions(state, seat)
                    self._request_id = uuid4().hex[:12]
                    return
                self._opp_play(seat)
                continue

            if state.phase == "response":
                acted = False
                for seat in list(state.response_seats or []):
                    if state.phase != "response":
                        break
                    if seat in (state.pending_claims or {}):
                        continue
                    if self._player_state(seat).status != "active":
                        continue
                    if seat == self.learner_seat and self._player_state(seat).status == "active":
                        self._pending_legals = legal_actions(state, seat)
                        self._request_id = uuid4().hex[:12]
                        return
                    self._opp_play(seat)
                    acted = True
                    break
                if not acted and state.phase == "response":
                    # all claimed or empty — avoid spin
                    if not state.response_seats:
                        raise PlayError("stuck in response with no seats")
                    # pending all filled should have resolved; force step
                    continue
                continue

            raise PlayError(f"unexpected phase {state.phase!r}")

        self._pending_legals = []

    def _exchange_waiting(self) -> list[int]:
        assert self._state is not None
        pe = self._state.pending_exchange or {}
        return [s for s in range(self._state.num_players) if s not in pe]

    def _dingque_waiting(self) -> list[int]:
        assert self._state is not None
        return [p.seat for p in self._state.players if p.dingque is None]

    def _apply_learner_action(self, action: Action) -> None:
        assert self._state is not None and self.config is not None
        seat = self.learner_seat
        state = self._state
        phase = state.phase

        if self.logger:
            self.logger.emit(
                "decision",
                seat=seat,
                request_id=self._request_id,
                action=action.to_dict(),
                reason="learner",
                phase=phase,
            )

        if phase == "exchange":
            tiles = list(action.tiles)
            validate_exchange_tiles(self._player_state(seat).hand, tiles)
            submit_exchange(state, seat, tiles)
            self._pending_legals = []
            return

        if phase == "dingque":
            if action.suit is None:
                raise EnvError("dingque requires suit")
            submit_dingque(state, seat, action.suit)
            self._pending_legals = []
            return

        if phase in ("discard", "response"):
            if self.session is None:
                raise PlayError("session missing in play phase")
            self.session.apply(seat, action)
            self._pending_legals = []
            return

        raise EnvError(f"cannot apply learner action in phase {phase!r}")

    def _opp_opening_exchange(self, seat: int) -> None:
        assert self._state is not None
        player = self.players[seat]
        hand = self._player_state(seat).hand
        legals = enumerate_exchange_actions(hand)
        if not legals:
            triple = pick_same_suit_triple(hand)
            legals = [Action(ActionType.EXCHANGE, tiles=tuple(triple))]
        obs = build_observation(self._state, seat)
        player.observe(obs)
        req = ActionRequest.create(seat, "exchange", legals)
        try:
            dec = player.decide(req)
            tiles = list(dec.action.tiles)
            validate_exchange_tiles(hand, tiles)
        except Exception:
            tiles = pick_same_suit_triple(hand)
        if self.logger:
            self.logger.emit(
                "decision",
                seat=seat,
                phase="exchange",
                action={"type": "exchange", "tiles": [t.id for t in tiles]},
                reason="opponent",
            )
        submit_exchange(self._state, seat, tiles)

    def _opp_opening_dingque(self, seat: int) -> None:
        assert self._state is not None
        player = self.players[seat]
        legals = opening_dingque_actions()
        obs = build_observation(self._state, seat)
        player.observe(obs)
        req = ActionRequest.create(seat, "dingque", legals)
        try:
            dec = player.decide(req)
            if dec.action.type == ActionType.DINGQUE and dec.action.suit is not None:
                suit: Suit = dec.action.suit
            else:
                suit = Suit.WAN
        except Exception:
            suit = Suit.WAN
        if self.logger:
            self.logger.emit(
                "decision",
                seat=seat,
                phase="dingque",
                action={"type": "dingque", "suit": suit.value},
                reason="opponent",
            )
        submit_dingque(self._state, seat, suit)

    def _opp_play(self, seat: int) -> None:
        assert self._state is not None and self.config is not None
        player = self.players.get(seat)
        if player is None:
            # learner seat but inactive — skip (should not call)
            return
        if self._player_state(seat).status != "active":
            return
        if self.session is None:
            self.session = GameSession(
                self._state,
                self.config,
                logger=self.logger,
                reward_calc=self.reward_calc,
            )
        setattr(player, "_engine_state", self._state)
        obs = build_observation(self._state, seat)
        player.observe(obs)
        legal = legal_actions(self._state, seat)
        if not legal:
            return
        req = ActionRequest.create(seat, self._state.phase, legal)
        try:
            dec = player.decide(req)
            action = dec.action
            if not action_in_legal(action, legal):
                action = legal[0]
        except Exception:
            action = legal[0]
        if self.logger:
            self.logger.emit(
                "decision",
                seat=seat,
                request_id=req.request_id,
                action=action.to_dict(),
                reason="opponent",
            )
        self.session.apply(seat, action)

    def _finalize_episode(self) -> None:
        assert self._state is not None and self.config is not None
        state = self._state
        if state.phase != "finished":
            state.phase = "finished"
            state.finished_reason = state.finished_reason or "unknown"
        finalize_game(state, self.config)
        if self.session is not None:
            self.session._flush_score_rewards()
        else:
            # flush any score events without session
            self._flush_scores_standalone()
        result = build_game_result(state)
        if self.reward_calc is not None:
            end_r = self.reward_calc.on_game_end(result, state)
            if self.logger:
                self.logger.emit(
                    "reward",
                    seat_rewards=end_r,
                    final=True,
                    episode_totals=self.reward_calc.episode_rewards,
                )
        self._episode_result = result
        if self.logger:
            self.logger.emit("game_end", result=result.to_dict())
            self.logger.close()
            self.logger = None
        for pl in self.players.values():
            try:
                pl.on_game_end(result.to_dict())
            except Exception:
                pass
        self._pending_legals = []

    def _flush_scores_standalone(self) -> None:
        """Rare path: play never started but finished (should not happen)."""
        if self.reward_calc is None or self._state is None:
            return
        from engine.score import ScoreTransfer

        for ev in self._state.score_events or []:
            if ev.get("type") != "score":
                continue
            transfers = []
            for t in ev.get("transfers") or []:
                transfers.append(
                    ScoreTransfer(
                        reason=t["reason"],
                        from_seat=int(t["from_seat"]),
                        to_seat=int(t["to_seat"]),
                        amount=int(t["amount"]),
                        fan=t.get("fan"),
                        meta=t.get("meta") or {},
                    )
                )
            self.reward_calc.on_transfers(transfers)

    # --- obs / action / info ----------------------------------------------

    def _resolve_action(self, action: Action | dict | int) -> Action:
        if isinstance(action, int):
            if action < 0 or action >= len(self._pending_legals):
                raise EnvError(
                    f"action index {action} out of range "
                    f"[0, {len(self._pending_legals)})"
                )
            return self._pending_legals[action]
        if isinstance(action, dict):
            return Action.from_dict(action)
        if isinstance(action, Action):
            return action
        raise EnvError(f"unsupported action type: {type(action)!r}")

    def _build_obs(self) -> dict[str, Any]:
        assert self._state is not None
        seat = self.learner_seat
        return {
            "game_id": self._state.game_id,
            "seat": seat,
            "phase": self._state.phase,
            "view": filter_state_for_seat(self._state, seat),
            "legal_actions": [a.to_dict() for a in self._pending_legals],
            "request_id": self._request_id,
        }

    def _terminal_obs(self) -> dict[str, Any]:
        assert self._state is not None
        seat = self.learner_seat
        return {
            "game_id": self._state.game_id,
            "seat": seat,
            "phase": self._state.phase,
            "view": filter_state_for_seat(self._state, seat),
            "legal_actions": [],
            "request_id": self._request_id or "",
        }

    def _learner_score(self) -> int:
        if self._state is None:
            return 0
        return int(self._player_state(self.learner_seat).score)

    def _build_info(self, score_before: int, score_after: int) -> dict[str, Any]:
        info: dict[str, Any] = {
            "score": score_after,
            "score_delta": score_after - score_before,
            "phase": self._state.phase if self._state else "unknown",
            "learner_steps": self._learner_steps,
        }
        if self._episode_result is not None:
            info["fan"] = None
            if self._episode_result.hu_sequence:
                # last hu fan if present
                last = self._episode_result.hu_sequence[-1]
                info["fan"] = last.get("fan")
        return info


def smoke_random_episode(
    *,
    game_id: str | None = "smoke-env-1",
    opponent_spec: str = "random",
    num_players: int = 4,
    seed: int = 0,
    max_steps: int = 10_000,
) -> dict[str, Any]:
    """Run one random-policy episode; return summary dict."""
    env = ChengduMahjongEnv(
        opponent_spec=opponent_spec,
        num_players=num_players,
        seed=seed,
        max_episode_steps=max_steps,
    )
    obs = env.reset(game_id=game_id)
    total_r = 0.0
    steps = 0
    terminated = False
    truncated = False
    info: dict[str, Any] = {}
    while True:
        legal = env.legal_actions()
        if not legal:
            break
        action = legal[env._rng.randrange(len(legal))]
        obs, reward, terminated, truncated, info = env.step(action)
        total_r += reward
        steps += 1
        if terminated or truncated:
            break
    result = env.episode_result
    summary = {
        "game_id": obs.get("game_id"),
        "steps": steps,
        "total_reward": total_r,
        "terminated": terminated,
        "truncated": truncated,
        "scores": result.scores if result else None,
        "finished_reason": result.finished_reason if result else None,
    }
    env.close()
    return summary
