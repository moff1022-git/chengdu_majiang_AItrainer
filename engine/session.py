"""Game session orchestration for blood-battle play."""

from __future__ import annotations

import random
from pathlib import Path
from typing import TYPE_CHECKING

from engine.action import Action, ActionType
from engine.blood_battle import (
    GameResult,
    PlayError,
    apply_action,
    build_game_result,
    do_draw,
    finalize_game,
    start_play,
)
from engine.config import EngineConfig
from engine.deal import create_dealt_game
from engine.exchange import pick_same_suit_triple
from engine.legal import legal_actions
from engine.opening import run_opening_with_choices
from engine.reward import RewardCalculator, RewardConfig
from engine.rules import config_from_state
from engine.state import GameState
from engine.tile import Suit, tiles_to_ids

if TYPE_CHECKING:
    from training.episode_log import EpisodeLogger


class GameSession:
    def __init__(
        self,
        state: GameState,
        config: EngineConfig | None = None,
        *,
        logger: EpisodeLogger | None = None,
        reward_calc: RewardCalculator | None = None,
    ) -> None:
        self.state = state
        self.config = config_from_state(state, config)
        self.logger = logger
        self.reward_calc = reward_calc
        self._last_score_event_count = len(state.score_events or [])

    def start_play(self) -> GameState:
        start_play(self.state, self.config)
        if self.logger:
            self.logger.emit(
                "game_start",
                game_id=self.state.game_id,
                seed=self.state.master_seed,
                config=self.config.to_dict(),
                num_players=self.state.num_players,
            )
            if self.logger.log_private:
                hands = {
                    str(p.seat): tiles_to_ids(p.hand) for p in self.state.players
                }
                self.logger.emit("deal", hands=hands)
        return self.state

    def legal_actions(self, seat: int) -> list[Action]:
        return legal_actions(self.state, seat)

    def apply(self, seat: int, action: Action) -> GameState:
        if self.logger:
            self.logger.emit(
                "action",
                seat=seat,
                action=action.to_dict(),
                phase=self.state.phase,
                turn_index=self.state.turn_index,
            )
        apply_action(self.state, seat, action, self.config)
        self._flush_score_rewards()
        return self.state

    def step_auto_draw(self) -> GameState:
        if self.state.phase == "draw":
            do_draw(self.state)
            self._flush_score_rewards()
        return self.state

    def _flush_score_rewards(self) -> None:
        events = self.state.score_events or []
        new_events = events[self._last_score_event_count :]
        self._last_score_event_count = len(events)
        for ev in new_events:
            if ev.get("type") != "score":
                continue
            if self.logger:
                self.logger.emit(
                    "score",
                    turn_index=ev.get("turn_index"),
                    transfers=ev.get("transfers"),
                    balances=ev.get("balances_after"),
                )
            if self.reward_calc:
                from engine.score import ScoreTransfer

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
                rewards = self.reward_calc.on_transfers(transfers)
                if self.logger and rewards:
                    self.logger.emit("reward", seat_rewards=rewards)

    def is_terminal(self) -> bool:
        return self.state.phase == "finished"

    def result(self) -> GameResult:
        if not self.is_terminal():
            raise PlayError("game not finished")
        finalize_game(self.state, self.config)
        self._flush_score_rewards()
        result = build_game_result(self.state)
        if self.reward_calc:
            end_r = self.reward_calc.on_game_end(result, self.state)
            if self.logger:
                self.logger.emit(
                    "reward",
                    seat_rewards=end_r,
                    final=True,
                    episode_totals=self.reward_calc.episode_rewards,
                )
        if self.logger:
            self.logger.emit("game_end", result=result.to_dict())
        return result


def build_ready_game(
    game_id: str,
    *,
    num_players: int = 4,
    config: EngineConfig | None = None,
    dingque_plan: dict[int, Suit] | None = None,
) -> GameState:
    """Deal + exchange + dingque → ready."""
    cfg = config or EngineConfig(num_players=num_players)
    state = create_dealt_game(game_id, num_players=cfg.num_players, config=cfg)
    exchanges = {p.seat: pick_same_suit_triple(p.hand) for p in state.players}
    if dingque_plan is None:
        suits = [Suit.WAN, Suit.TONG, Suit.TIAO]
        dingque_plan = {p.seat: suits[p.seat % 3] for p in state.players}
    run_opening_with_choices(state, exchanges, dingque_plan, cfg)
    return state


def play_random_game(
    game_id: str,
    *,
    num_players: int = 4,
    config: EngineConfig | None = None,
    rng: random.Random | None = None,
    max_steps: int = 10_000,
) -> GameResult:
    """Headless random legal play until terminal."""
    return play_random_game_logged(
        game_id,
        num_players=num_players,
        config=config,
        rng=rng,
        max_steps=max_steps,
        log_dir=None,
        reward_config=None,
    )


def play_random_game_logged(
    game_id: str,
    *,
    num_players: int = 4,
    config: EngineConfig | None = None,
    rng: random.Random | None = None,
    max_steps: int = 10_000,
    log_dir: Path | str | None = None,
    reward_config: RewardConfig | None = None,
) -> GameResult:
    from training.episode_log import EpisodeLogger

    rng = rng or random.Random(0)
    cfg = config or EngineConfig(num_players=num_players)
    state = build_ready_game(game_id, num_players=cfg.num_players, config=cfg)
    logger = None
    if log_dir is not None:
        logger = EpisodeLogger(log_dir, game_id, log_private=True)
    reward_calc = RewardCalculator(reward_config) if reward_config else RewardCalculator()
    session = GameSession(
        state, cfg, logger=logger, reward_calc=reward_calc
    )
    try:
        session.start_play()
        steps = 0
        while not session.is_terminal() and steps < max_steps:
            steps += 1
            st = session.state
            if st.phase == "draw":
                session.step_auto_draw()
                continue
            if st.phase == "discard":
                seat = st.current_seat
                assert seat is not None
                acts = session.legal_actions(seat)
                if not acts:
                    raise PlayError(f"no legal actions for seat {seat}")
                discards = [a for a in acts if a.type == ActionType.DISCARD]
                pool = discards if discards else acts
                action = rng.choice(pool)
                session.apply(seat, action)
                continue
            if st.phase == "response":
                for seat in list(st.response_seats or []):
                    if session.is_terminal():
                        break
                    if st.phase != "response":
                        break
                    if seat not in (st.response_seats or []):
                        continue
                    if seat in (st.pending_claims or {}):
                        continue
                    acts = session.legal_actions(seat)
                    if not acts:
                        continue
                    passes = [a for a in acts if a.type == ActionType.PASS]
                    action = passes[0] if passes else rng.choice(acts)
                    session.apply(seat, action)
                continue
            if st.phase == "ready":
                session.start_play()
                continue
            if st.phase == "finished":
                break
            raise PlayError(f"stuck in phase {st.phase}")

        if not session.is_terminal():
            st = session.state
            st.phase = "finished"
            st.finished_reason = st.finished_reason or "max_steps"
            finalize_game(st, cfg)
        return session.result()
    finally:
        if logger:
            logger.close()
