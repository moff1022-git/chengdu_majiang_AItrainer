"""Multi-player game runner: opening + blood-battle with BasePlayer decide."""

from __future__ import annotations

import random
import time
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Sequence

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
from engine.crash import AbortGame, CrashConfig, CrashHandler
from engine.deal import create_dealt_game
from engine.exchange import pick_same_suit_triple, validate_exchange_tiles
from engine.legal import action_in_legal, legal_actions
from engine.opening import begin_opening, submit_dingque, submit_exchange
from engine.persistence import default_save_path, save_game
from engine.replay import StepRecorder
from engine.reward import RewardCalculator, RewardConfig
from engine.rules import config_from_state
from engine.session import GameSession
from engine.state import GameState
from engine.tile import Suit, Tile
from players.base_player import BasePlayer
from protocols.messages import ActionRequest, Decision
from protocols.transport import InProcessTransport
from protocols.view_filter import build_observation

if TYPE_CHECKING:
    from training.episode_log import EpisodeLogger


def _opening_exchange_legals(hand: list[Tile]) -> list[Action]:
    """Provide at least one legal EXCHANGE (same-suit triple)."""
    try:
        triple = pick_same_suit_triple(hand)
        return [Action(ActionType.EXCHANGE, tiles=tuple(triple))]
    except Exception:
        return []


def _opening_dingque_legals() -> list[Action]:
    return [Action(ActionType.DINGQUE, suit=s) for s in Suit]


class PlayerGameRunner:
    """Run a full game with pluggable BasePlayer instances (InProcess)."""

    def __init__(
        self,
        players: Sequence[BasePlayer],
        config: EngineConfig | None = None,
        *,
        game_id: str | None = None,
        logger: EpisodeLogger | None = None,
        reward_calc: RewardCalculator | None = None,
        max_steps: int = 10_000,
        crash_config: CrashConfig | None = None,
        save_dir: Path | str | None = None,
        save_every_decision: bool = False,
        save_on_end: bool = True,
        on_state_change: Callable[[GameState], None] | None = None,
        join_extras: dict | None = None,
        shutdown_players_on_end: bool = True,
        step_delay_ms: int = 0,
        starting_scores: dict[int, int] | None = None,
    ) -> None:
        self.players = list(players)
        n = len(self.players)
        if n not in (2, 3, 4):
            raise ValueError(f"need 2-4 players, got {n}")
        self.config = config or EngineConfig(num_players=n)
        if self.config.num_players != n:
            self.config = replace(self.config, num_players=n)
        self.game_id = game_id
        self.logger = logger
        self.reward_calc = reward_calc or RewardCalculator()
        self.max_steps = max_steps
        self.transport = InProcessTransport()
        self.state: GameState | None = None
        self.crash = CrashHandler(crash_config or CrashConfig.load())
        self.save_dir = Path(save_dir) if save_dir else None
        self.save_every_decision = save_every_decision
        self.save_on_end = save_on_end
        self.on_state_change = on_state_change
        self.join_extras = dict(join_extras or {})
        self.shutdown_players_on_end = shutdown_players_on_end
        # Live GUI: delay AI steps so 血战 after human hu is visible (ms)
        self.step_delay_ms = max(0, int(step_delay_ms))
        # Multi-round session: carry cumulative scores into next hand
        self.starting_scores = {
            int(k): int(v) for k, v in (starting_scores or {}).items()
        }
        self._step_recorder: StepRecorder | None = None
        self.players_meta: list[dict] = [
            {"seat": i, "type": type(p).__name__, "name": p.name}
            for i, p in enumerate(self.players)
        ]

    def _notify_state(self) -> None:
        if self.on_state_change is None or self.state is None:
            return
        try:
            self.on_state_change(self.state)
        except Exception:
            pass
        # Pace AI-only stretches (esp. after a human has already hu'd)
        if self.step_delay_ms > 0 and self.state.phase != "finished":
            time.sleep(self.step_delay_ms / 1000.0)

    def run(self) -> GameResult:
        gid = self.game_id
        state = create_dealt_game(gid, config=self.config)
        # Apply session carry-over scores (multi-round GUI / training sessions)
        if self.starting_scores:
            for p in state.players:
                if p.seat in self.starting_scores:
                    p.score = int(self.starting_scores[p.seat])
        self.state = state
        cfg = self.config

        if self.save_dir and self.save_every_decision:
            self._step_recorder = StepRecorder(
                Path(self.save_dir) / f"{state.game_id}.steps.jsonl",
                snapshot_every=1,
            )
            self._step_recorder.record_snapshot(state)

        join_cfg = cfg.to_dict()
        join_cfg.setdefault("theme", "green")
        join_cfg.setdefault(
            "human_timeout_ms", self.crash.config.timeout_ms
        )
        for p in self.players:
            th = getattr(p, "theme", None)
            if th:
                join_cfg["theme"] = th
                break
        if self.join_extras:
            join_cfg.update(self.join_extras)
        for i, p in enumerate(self.players):
            p.on_join(i, join_cfg)

        # First snapshot so seat windows (esp. human) have hand UI before acts
        for i, p in enumerate(self.players):
            try:
                obs0 = build_observation(state, i)
                self.transport.send_observation(p, obs0)
            except Exception:
                pass
        self._notify_state()

        if self.logger:
            self.logger.emit(
                "game_start",
                game_id=state.game_id,
                seed=state.master_seed,
                config=cfg.to_dict(),
                players=[
                    {"seat": i, "name": pl.name, "id": pl.player_id}
                    for i, pl in enumerate(self.players)
                ],
            )

        try:
            # --- Opening: optional exchange → dingque ---
            begin_opening(state, cfg)
            self._notify_state()
            if state.phase == "exchange":
                for seat in range(state.num_players):
                    self._decide_and_opening_exchange(state, seat)
                    self._notify_state()
                if state.phase != "dingque":
                    raise PlayError(
                        f"expected dingque after exchange, got {state.phase}"
                    )

            if state.phase != "dingque":
                raise PlayError(f"expected dingque after opening, got {state.phase}")

            # --- Opening: dingque ---
            for seat in range(state.num_players):
                self._decide_and_opening_dingque(state, seat)
                self._notify_state()

            if state.phase != "ready":
                raise PlayError(f"expected ready after dingque, got {state.phase}")

            # --- Play ---
            session = GameSession(
                state,
                cfg,
                logger=self.logger,
                reward_calc=self.reward_calc,
            )
            start_play(state, cfg)
            self._notify_state()
            if self.logger:
                self.logger.emit("phase", phase="discard", dealer=state.dealer_seat)

            steps = 0
            while state.phase != "finished" and steps < self.max_steps:
                steps += 1
                if state.phase == "draw":
                    do_draw(state)
                    self._notify_state()
                    continue
                if state.phase == "discard":
                    seat = state.current_seat
                    if seat is None:
                        raise PlayError("current_seat is None")
                    from engine.blood_battle import next_active, player_at

                    # 血战: never ask a seat that already hu'd
                    if player_at(state, seat).status != "active":
                        nxt = next_active(state, seat)
                        if nxt is None:
                            state.phase = "finished"
                            state.finished_reason = state.finished_reason or "last_one"
                            finalize_game(state, cfg)
                        else:
                            state.current_seat = nxt
                            state.phase = "draw"
                        self._notify_state()
                        continue
                    self._play_seat_action(state, seat, session)
                    self._notify_state()
                    continue
                if state.phase == "response":
                    from engine.action import Action, ActionType
                    from engine.blood_battle import force_complete_response, player_at

                    pending_before = len(state.pending_claims or {})
                    acted = False
                    for seat in list(state.response_seats or []):
                        if state.phase != "response":
                            break
                        if seat in (state.pending_claims or {}):
                            continue
                        # Finished seats must not block multi-claim resolve
                        if player_at(state, seat).status != "active":
                            pc = dict(state.pending_claims or {})
                            pc[seat] = Action(ActionType.PASS)
                            state.pending_claims = pc
                            if set(state.response_seats or []).issubset(pc.keys()):
                                force_complete_response(state, cfg)
                            acted = True
                            continue
                        self._play_seat_action(state, seat, session)
                        acted = True
                        self._notify_state()
                        if state.phase != "response":
                            break
                    # Stuck safety: no progress → force PASS fill + resolve
                    if (
                        state.phase == "response"
                        and len(state.pending_claims or {}) == pending_before
                        and not acted
                    ):
                        force_complete_response(state, cfg)
                        self._notify_state()
                    elif state.phase == "response":
                        # After a full pass of seats, if all claimed, resolve
                        needed = set(state.response_seats or [])
                        got = set((state.pending_claims or {}).keys())
                        if needed and needed.issubset(got):
                            force_complete_response(state, cfg)
                            self._notify_state()
                    continue
                if state.phase == "finished":
                    break
                raise PlayError(f"stuck in phase {state.phase}")

            if state.phase != "finished":
                state.phase = "finished"
                state.finished_reason = state.finished_reason or "max_steps"
                finalize_game(state, cfg)
        except AbortGame as e:
            state.phase = "finished"
            state.finished_reason = e.reason
            finalize_game(state, cfg)

        result = build_game_result(state)
        if self.reward_calc:
            end_r = self.reward_calc.on_game_end(result, state)
            if self.logger:
                self.logger.emit(
                    "reward",
                    seat_rewards=end_r,
                    final=True,
                    episode_totals=self.reward_calc.episode_rewards,
                )
        if self.logger:
            self.logger.emit("game_end", result=result.to_dict())

        if self.save_dir and self.save_on_end:
            path = default_save_path(self.save_dir, state.game_id)
            save_game(
                path,
                state,
                config=cfg,
                players_meta=self.players_meta,
                crash_log=self.crash.crash_log,
            )

        for pl in self.players:
            try:
                pl.on_game_end(result.to_dict())
            except Exception:
                pass
            if self.shutdown_players_on_end:
                try:
                    pl.shutdown()
                except Exception:
                    pass
        return result

    def _play_seat_action(
        self, state: GameState, seat: int, session: GameSession
    ) -> None:
        from engine.blood_battle import next_active, player_at
        from engine.action import Action, ActionType

        # Blood-battle: finished (hu'd) seats never decide again
        try:
            if player_at(state, seat).status != "active":
                return
        except Exception:
            return

        player = self.players[seat]
        setattr(player, "_engine_state", state)
        obs = build_observation(state, seat)
        self.transport.send_observation(player, obs)
        legal = legal_actions(state, seat)
        if not legal:
            # Safety: inactive / desynced seat — do not block the engine
            if state.phase == "response":
                try:
                    session.apply(seat, Action(ActionType.PASS))
                except Exception:
                    pass
            elif state.phase == "discard" and state.current_seat == seat:
                nxt = next_active(state, seat)
                if nxt is None:
                    state.phase = "finished"
                    state.finished_reason = state.finished_reason or "last_one"
                else:
                    state.current_seat = nxt
                    state.phase = "draw"
            return
        req = ActionRequest.create(seat, state.phase, legal)
        try:
            dec = self.transport.request_decision(player, req)
            if not dec.reason:
                raise PlayError(f"empty decision reason from seat {seat}")
            if not action_in_legal(dec.action, legal):
                dec = self.crash.handle_illegal(state, seat, req, legal, dec)
        except AbortGame:
            raise
        except Exception as e:
            dec = self.crash.handle(
                state, seat, e, req, legal, self.players
            )

        if self.logger:
            self.logger.emit(
                "decision",
                seat=seat,
                request_id=req.request_id,
                action=dec.action.to_dict(),
                reason=dec.reason,
                analysis=dec.analysis,
            )
        if self._step_recorder:
            self._step_recorder.record_decision(
                seat,
                dec.action.to_dict(),
                dec.reason,
                state=state if self.save_every_decision else None,
            )
        try:
            session.apply(seat, dec.action)
        except Exception as e:
            # Never let a single apply kill the whole blood-battle hand
            print(f"[orchestrator] apply failed seat={seat} phase={state.phase}: {e}")
            if state.phase == "response":
                try:
                    from engine.action import Action, ActionType
                    from engine.blood_battle import force_complete_response

                    pc = dict(state.pending_claims or {})
                    pc[seat] = Action(ActionType.PASS)
                    state.pending_claims = pc
                    force_complete_response(state, self.config)
                except Exception as e2:
                    print(f"[orchestrator] response recovery failed: {e2}")
                    raise PlayError(str(e)) from e
            else:
                raise

    def _decide_and_opening_exchange(self, state: GameState, seat: int) -> None:
        player = self.players[seat]
        p = next(x for x in state.players if x.seat == seat)
        obs = build_observation(state, seat)
        self.transport.send_observation(player, obs)
        legals = _opening_exchange_legals(p.hand)
        # Also allow player-chosen triple via validate if they invent — only offer one
        req = ActionRequest.create(seat, "exchange", legals)
        dec = self.transport.request_decision(player, req)
        if dec.action.type != ActionType.EXCHANGE or len(dec.action.tiles) != 3:
            # fallback: engine pick
            tiles = pick_same_suit_triple(p.hand)
        else:
            tiles = list(dec.action.tiles)
            try:
                validate_exchange_tiles(p.hand, tiles)
            except Exception:
                tiles = pick_same_suit_triple(p.hand)
        if self.logger:
            self.logger.emit(
                "decision",
                seat=seat,
                phase="exchange",
                reason=dec.reason,
                action={"type": "exchange", "tiles": [t.id for t in tiles]},
            )
        submit_exchange(state, seat, tiles)

    def _decide_and_opening_dingque(self, state: GameState, seat: int) -> None:
        player = self.players[seat]
        obs = build_observation(state, seat)
        self.transport.send_observation(player, obs)
        legals = _opening_dingque_legals()
        req = ActionRequest.create(seat, "dingque", legals)
        dec = self.transport.request_decision(player, req)
        if dec.action.type == ActionType.DINGQUE and dec.action.suit is not None:
            suit = dec.action.suit
        else:
            suit = Suit.WAN
        if self.logger:
            self.logger.emit(
                "decision",
                seat=seat,
                phase="dingque",
                reason=dec.reason,
                action={"type": "dingque", "suit": suit.value},
            )
        submit_dingque(state, seat, suit)


def run_players_game(
    player_specs: str | list[str],
    *,
    game_id: str | None = None,
    config: EngineConfig | None = None,
    base_seed: int = 0,
    log_dir: Path | str | None = None,
    reward_config: RewardConfig | None = None,
    max_steps: int = 10_000,
    theme: str = "green",
    human_timeout_ms: int = 120_000,
    crash_config: CrashConfig | None = None,
    save_dir: Path | str | None = None,
    save_every_decision: bool = False,
    save_on_end: bool = True,
) -> GameResult:
    from players.registry import create_players
    from training.episode_log import EpisodeLogger

    players = create_players(
        player_specs,
        base_seed=base_seed,
        theme=theme,
        human_timeout_ms=human_timeout_ms,
    )
    n = len(players)
    cfg = config or EngineConfig(num_players=n)
    logger = None
    gid = game_id or f"pg-{base_seed}"
    if log_dir is not None:
        logger = EpisodeLogger(log_dir, gid, log_private=True)
    reward_calc = RewardCalculator(reward_config)
    try:
        runner = PlayerGameRunner(
            players,
            cfg,
            game_id=gid,
            logger=logger,
            reward_calc=reward_calc,
            max_steps=max_steps,
            crash_config=crash_config,
            save_dir=save_dir,
            save_every_decision=save_every_decision,
            save_on_end=save_on_end,
        )
        return runner.run()
    finally:
        for pl in players:
            try:
                pl.shutdown()
            except Exception:
                pass
        if logger:
            logger.close()


class InteractiveRunner:
    """
    Stepwise runner for GUI: setup() then step_once() until finished.
    Opening steps (exchange/dingque per seat) are done in setup for speed.
    """

    def __init__(
        self,
        players: Sequence[BasePlayer],
        config: EngineConfig | None = None,
        *,
        game_id: str | None = None,
        max_steps: int = 10_000,
    ) -> None:
        self._base = PlayerGameRunner(
            players, config, game_id=game_id, max_steps=max_steps
        )
        self._session: GameSession | None = None
        self._steps = 0
        self._finished = False
        self._result: GameResult | None = None
        self.last_event: str | None = None

    @property
    def state(self) -> GameState:
        if self._base.state is None:
            raise PlayError("call setup() first")
        return self._base.state

    @property
    def result(self) -> GameResult | None:
        return self._result

    def setup(self) -> GameState:
        """Deal, full opening (all seats), start_play → discard phase."""
        runner = self._base
        gid = runner.game_id
        state = create_dealt_game(gid, config=runner.config)
        runner.state = state
        cfg = runner.config
        join_cfg = cfg.to_dict()
        join_cfg.setdefault("theme", "green")
        for p in runner.players:
            th = getattr(p, "theme", None)
            if th:
                join_cfg["theme"] = th
                break
        for i, p in enumerate(runner.players):
            p.on_join(i, join_cfg)
        begin_opening(state, cfg)
        if state.phase == "exchange":
            for seat in range(state.num_players):
                runner._decide_and_opening_exchange(state, seat)
        for seat in range(state.num_players):
            runner._decide_and_opening_dingque(state, seat)
        self._session = GameSession(state, cfg, reward_calc=runner.reward_calc)
        start_play(state, cfg)
        self._steps = 0
        self._finished = False
        self._result = None
        self.last_event = "start"
        return state

    def step_once(self) -> bool:
        """Advance one action or auto-draw. Return True if game finished."""
        if self._finished:
            return True
        state = self.state
        session = self._session
        if session is None:
            raise PlayError("call setup() first")
        runner = self._base
        self._steps += 1
        if self._steps > runner.max_steps:
            state.phase = "finished"
            state.finished_reason = "max_steps"
            finalize_game(state, runner.config)
            self._finish()
            return True

        if state.phase == "draw":
            do_draw(state)
            self.last_event = "draw"
            if state.phase == "finished":
                self._finish()
                return True
            return False

        if state.phase == "discard":
            from engine.blood_battle import next_active, player_at

            seat = state.current_seat
            if seat is None:
                raise PlayError("current_seat is None")
            if player_at(state, seat).status != "active":
                nxt = next_active(state, seat)
                if nxt is None:
                    state.phase = "finished"
                    state.finished_reason = state.finished_reason or "last_one"
                    self._finish()
                    return True
                state.current_seat = nxt
                state.phase = "draw"
                self.last_event = "skip_finished"
                return False
            runner._play_seat_action(state, seat, session)
            self.last_event = "discard_or_self"
            if state.phase == "finished":
                self._finish()
                return True
            return False

        if state.phase == "response":
            from engine.action import Action, ActionType
            from engine.blood_battle import force_complete_response, player_at

            # one pending seat per step for visual pacing
            for seat in list(state.response_seats or []):
                if seat in (state.pending_claims or {}):
                    continue
                if player_at(state, seat).status != "active":
                    pc = dict(state.pending_claims or {})
                    pc[seat] = Action(ActionType.PASS)
                    state.pending_claims = pc
                    if set(state.response_seats or []).issubset(pc.keys()):
                        force_complete_response(state, runner.config)
                    self.last_event = "response_autofill"
                    if state.phase == "finished":
                        self._finish()
                        return True
                    return False
                runner._play_seat_action(state, seat, session)
                self.last_event = "response"
                if state.phase == "finished":
                    self._finish()
                    return True
                return False
            # all claimed / none left — force resolve if still in response
            if state.phase == "response":
                force_complete_response(state, runner.config)
                if state.phase == "finished":
                    self._finish()
                    return True
            return False

        if state.phase == "finished":
            self._finish()
            return True

        raise PlayError(f"unexpected phase {state.phase}")

    def _finish(self) -> None:
        if self._finished:
            return
        self._finished = True
        state = self.state
        finalize_game(state, self._base.config)
        self._result = build_game_result(state)
        for pl in self._base.players:
            pl.on_game_end(self._result.to_dict())
            pl.shutdown()

