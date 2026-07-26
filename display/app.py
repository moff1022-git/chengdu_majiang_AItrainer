"""Pygame application: Lobby / Table / Result scenes.

Supports:
- AI-only spectate via InteractiveRunner (main-thread step)
- Human + AI: main GUI spectates while PlayerGameRunner runs in a
  background thread; human plays in a separate subprocess window.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Literal

import pygame

from display.asset_manager import AssetManager
from display.control_panel import ControlPanel
from display.hud_common import FxOverlay, draw_text
from display.layout import Layout
from display.lobby_view import LobbyView
from display.play_event_log import PlayEventLog
from display.result_view import ResultView
from display.table_view import TableView
from display.interior_scale import MAIN_REF_H, MAIN_REF_W
from display.window_geometry import (
    FULL_MAIN_H,
    FULL_MAIN_W,
    MIN_MAIN_H,
    MIN_MAIN_W,
    WindowPlan,
    clamp_outer_size,
    detect_layout_screen,
    force_window_placement,
    log_plan,
    log_screen,
    open_resizable_window,
    plan_for_screen,
    plan_to_dict,
    raise_main_window,
)
from engine.action import ActionType
from engine.blood_battle import GameResult
from engine.config import EngineConfig
from engine.legal import legal_actions
from engine.orchestrator import InteractiveRunner, PlayerGameRunner
from engine.state import GameState
from players.analysis.pipeline import AnalysisSnapshot, analyze_for_seat
from players.registry import create_players

Scene = Literal["lobby", "table", "result"]


def _parse_parts(spec: str) -> list[str]:
    return [p.strip() for p in spec.split(",") if p.strip()]


def _human_seat_index(parts: list[str]) -> int | None:
    for i, p in enumerate(parts):
        if p.split(":")[0].strip().lower() == "human":
            return i
    return None


def _human_seats(parts: list[str]) -> list[int]:
    out: list[int] = []
    for i, p in enumerate(parts):
        if p.split(":")[0].strip().lower() == "human":
            out.append(i)
    return out


@dataclass
class AppConfig:
    theme: str = "green"
    num_players: int = 4
    players_spec: str = "rule_ai,rule_ai,rule_ai,rule_ai"
    spectator: str = "full"  # full | public
    focus_seat: int = 0
    step_ms: int = 200
    game_id: str | None = None
    show_hud: bool = True
    game_mode: str = "blood_battle"  # display / rules family
    enable_exchange: bool = True
    num_rounds: int = 1


class MahjongApp:
    def __init__(self, config: AppConfig | None = None) -> None:
        self.cfg = config or AppConfig()
        # 1) Current cursor/console screen  2) Plan  3) Open main on that screen
        self.screen_info = detect_layout_screen(prefer_main=False)
        log_screen(self.screen_info, prefix="[display]")
        # Default lobby plan: layout A (1 human seat 0) until Start sets real seats
        self._plan_human_seats: list[int] = [0]
        self.window_plan: WindowPlan = plan_for_screen(
            self.cfg.num_players,
            screen=self.screen_info,
            human_seats=self._plan_human_seats,
        )
        log_plan(self.window_plan, prefix="[display]")
        pygame.init()
        main = self.window_plan.main
        # Complete-mode size: same client size as human seat (plan → matched client)
        from display.window_geometry import plan_to_matched_client_size

        mw, mh = clamp_outer_size(main.w, main.h, kind="main")
        mw, mh = plan_to_matched_client_size(mw, mh)
        # Match seat client height exactly (human full uses same plan h)
        human0 = self.window_plan.players.get(0)
        if human0 is not None:
            hw, hh = clamp_outer_size(human0.w, human0.h, kind="human")
            hw, hh = plan_to_matched_client_size(hw, hh)
            # Force identical client height for MAIN and human seat
            mh = hh
            mw = max(mw, hw) if mw != hw else mw
            # Prefer exact human width when layout A bottom row (same size class)
            if abs(mw - hw) <= 2:
                mw = hw
        self._main_locked_size = (mw, mh)
        self.screen = open_resizable_window(
            (mw, mh),
            pos=(main.x, main.y),
            caption="Chengdu Mahjong AI Trainer — 主程序",
            min_size=(mw, mh),
        )
        # Do not probe pygame._sdl2 for actual window screen (macOS SEGV).
        self.clock = pygame.time.Clock()
        self.assets = AssetManager(theme=self.cfg.theme)
        self.control_panel = ControlPanel()
        self.play_log = PlayEventLog(capacity=200)
        self.layout = Layout.from_window(mw, mh)
        self.lobby = LobbyView(self.assets)
        self.table = TableView(
            self.assets,
            layout=self.layout,
            spectator="full" if self.cfg.spectator == "full" else "public",
            focus_seat=self.cfg.focus_seat,
            show_hud=self.cfg.show_hud,
            control_panel=self.control_panel,
        )
        self.table.play_log = self.play_log
        # Sync initial HUD toggles
        self.control_panel.options.show_inference = self.cfg.show_hud
        self.control_panel.options.show_strategy = self.cfg.show_hud
        self.result_view = ResultView(self.assets)
        self.fx = FxOverlay()
        self.scene: Scene = "lobby"
        # AI-only path
        self.runner: InteractiveRunner | None = None
        # Human+AI live path
        self._live_runner: PlayerGameRunner | None = None
        self._live_thread: threading.Thread | None = None
        self._live_done = False
        self._live_error: BaseException | None = None
        self._live_mode = False
        self._seat_hub = None
        self._status_msg = ""
        self.game_result: GameResult | None = None
        self.analysis: AnalysisSnapshot | None = None
        self._last_step = 0.0
        self._last_analysis = 0.0
        self._running = True
        self._auto_start = False
        # Multi-round session (F0003)
        self._round_index = 0  # completed rounds in session
        self._session_active = False
        # Cumulative scores across hands in this session (seat -> total)
        self._session_scores: dict[int, int] = {}
        # Scores at the start of the current hand (for 本局 delta on result)
        self._hand_start_scores: dict[int, int] = {}
        # Last hand: all seat windows confirmed via auto-start
        self._last_ready_all_auto: bool = False
        # Result scene auto next-round countdown (monotonic deadline)
        self._auto_next_deadline: float | None = None
        self._auto_next_seconds: float = 3.0
        # Main-thread only: plan to apply via pygame (worker must not call set_mode)
        self._pending_main_pin: WindowPlan | None = None
        # Lock layout to the screen chosen at app/session start (avoid cursor jumps)
        self._session_layout_screen = self.screen_info

    def run(self, *, auto_start: bool = False) -> None:
        self._auto_start = auto_start
        if auto_start:
            self._start_game()
        while self._running:
            self.clock.tick(60)
            self._flush_pending_main_pin()
            self._handle_events()
            if self.scene == "table":
                self._maybe_step()
            elif self.scene == "result":
                self._tick_auto_next_round()
            self._draw()
            pygame.display.flip()
        # App exit — close seat windows
        self._stop_live_game(close_seats=True)
        pygame.quit()

    def _current_state(self) -> GameState | None:
        if self._live_mode and self._live_runner is not None:
            return self._live_runner.state
        if self.runner is not None:
            try:
                return self.runner.state
            except Exception:
                return None
        return None

    def _engine_config(self, n: int) -> EngineConfig:
        return EngineConfig(
            num_players=n,
            enable_exchange=bool(self.cfg.enable_exchange),
        )

    def _start_game(self, *, new_session: bool = False) -> None:
        """Start a hand. new_session=True resets round counter (from lobby Start)."""
        # Stop engine/thread only; keep seat windows unless settings force rebuild
        self._stop_live_game(close_seats=False)

        parts = _parse_parts(self.cfg.players_spec)
        n = len(parts) if parts else self.cfg.num_players
        if len(parts) != n:
            parts = ["rule_ai"] * self.cfg.num_players
            self.cfg.players_spec = ",".join(parts)
            n = self.cfg.num_players
        self.cfg.num_players = n

        if new_session or not self._session_active:
            self._round_index = 0
            self._session_active = True
            self._session_scores = {i: 0 for i in range(n)}
        else:
            # Ensure keys exist for current player count
            for i in range(n):
                self._session_scores.setdefault(i, 0)

        # GUI always uses seat windows + per-seat ready confirm (F0004),
        # including pure 4AI (all watch seats). No silent auto-start.
        human_seat = _human_seat_index(parts)
        self._plan_human_seats = _human_seats(parts)
        if human_seat is not None:
            self.cfg.focus_seat = human_seat
        try:
            self.play_log.clear()
            self.play_log.append("info", f"开局 · 第{self._round_index + 1}局")
        except Exception:
            pass
        self._start_live_game(parts, n, human_seat=human_seat)

        self.table.set_spectator(
            "full" if self.cfg.spectator == "full" else "public",
            self.cfg.focus_seat,
        )
        self.table.show_hud = self.cfg.show_hud
        self.table.focus_seat = self.cfg.focus_seat
        self.scene = "table"
        self.game_result = None
        self.analysis = None
        self._last_step = time.time()
        self._last_analysis = 0.0
        self.fx.key = None
        r_disp = self._round_index + 1
        self._status_msg = (
            f"第 {r_disp}/{self.cfg.num_rounds} 局 | "
            f"换三张={'开' if self.cfg.enable_exchange else '关'} | "
            f"{self.cfg.game_mode}"
        )

    def _start_ai_spectate_game(self, parts: list[str], n: int) -> None:
        """Legacy main-thread AI step (no seats). Prefer `_start_live_game`."""
        self._live_mode = False
        self._status_msg = "AI 观战（无座位窗）"
        players = create_players(
            self.cfg.players_spec,
            base_seed=int(time.time()) % 100000,
            theme=self.cfg.theme,
            training_mode=True,
        )
        eng = self._engine_config(n)
        self.runner = InteractiveRunner(
            players,
            eng,
            game_id=self.cfg.game_id or f"gui-{int(time.time())}",
        )
        self.runner.setup()
        self._refresh_analysis()

    def _refresh_window_plan(
        self,
        num_players: int,
        *,
        relock: bool = False,
        prefer_main: bool = False,
        screen=None,
    ) -> WindowPlan:
        """
        Rebuild the shared window plan.

        By default reuses the session layout screen so clicking seat windows
        on another monitor cannot steal the grid mid-hand. Pass relock=True
        when starting a hand to follow the **current** screen (cursor).
        """
        if screen is not None:
            self.screen_info = screen
            self._session_layout_screen = screen
        elif relock or self._session_layout_screen is None:
            self.screen_info = detect_layout_screen(prefer_main=prefer_main)
            self._session_layout_screen = self.screen_info
        else:
            self.screen_info = self._session_layout_screen
        log_screen(self.screen_info, prefix="[display]")
        self.window_plan = plan_for_screen(
            num_players,
            screen=self.screen_info,
            human_seats=list(self._plan_human_seats),
        )
        log_plan(self.window_plan, prefix="[display]")
        return self.window_plan

    def _pin_main_window(self, plan: WindowPlan | None = None) -> None:
        """Place main pygame window (main thread only). Stable path for macOS."""
        from display.window_geometry import set_sdl_window_pos

        p = plan or self.window_plan
        if p is None:
            return
        m = p.main
        from display.window_geometry import plan_to_matched_client_size

        mw, mh = clamp_outer_size(m.w, m.h, kind="main")
        mw, mh = plan_to_matched_client_size(mw, mh)
        # Prefer actual human Tk client size (window_ready) so outer frames match
        hub = getattr(self, "_seat_hub", None)
        hcs = getattr(hub, "human_client_size", None) if hub is not None else None
        if hcs and int(hcs[1]) >= 160:
            hw, hh = int(hcs[0]), int(hcs[1])
            # Same height class as human seat; keep width from plan (layout A equal)
            mh = hh
            if abs(mw - hw) <= 4:
                mw = hw
            print(f"[display] pin main match human client {mw}x{mh}")
        else:
            p = plan or self.window_plan
            if p is not None:
                for _s, r in (p.players or {}).items():
                    if abs(int(r.y) - int(m.y)) <= 2 and int(r.h) >= 100:
                        _hw, hh = clamp_outer_size(r.w, r.h, kind="human")
                        _hw, hh = plan_to_matched_client_size(_hw, hh)
                        mh = hh
                        if abs(mw - _hw) <= 2:
                            mw = _hw
                        break
        self._main_locked_size = (mw, mh)
        try:
            # Env + single set_mode only (no display.quit, no _sdl2)
            set_sdl_window_pos(m.x, m.y)
            self.screen = pygame.display.set_mode((mw, mh), pygame.RESIZABLE)
            if self.screen is None:
                self.screen = pygame.display.get_surface()
            if self.screen is None:
                raise RuntimeError("display surface missing after pin")
            pygame.display.set_caption("Chengdu Mahjong AI Trainer — 主程序")
            self.layout = Layout.from_window(mw, mh)
            self.table.resize(mw, mh)
            raise_main_window()
            print(
                f"[display] pin main {mw}x{mh}@({m.x},{m.y}) "
                f"via {getattr(p, 'screen_source', '?')} (capped≤1080p full)"
            )
        except Exception as e:
            print(f"[display] pin main skip: {e}")

    def _align_plan_after_pin(self, num_players: int, target_screen) -> WindowPlan:
        """Lock plan to the intended target screen (no unsafe main-window probe)."""
        return self._refresh_window_plan(num_players, screen=target_screen)

    def _request_main_pin(self, plan: WindowPlan | None = None) -> None:
        """Queue a main-window pin for the next main-loop tick (thread-safe)."""
        p = plan or self.window_plan
        if p is not None:
            self.window_plan = p
            self._pending_main_pin = p

    def _flush_pending_main_pin(self) -> None:
        p = self._pending_main_pin
        if p is None:
            return
        self._pending_main_pin = None
        self._pin_main_window(p)

    def _hub_compatible(self, n: int, human_seat: int | None) -> bool:
        hub = self._seat_hub
        if hub is None:
            return False
        return (
            hub.num_players == n
            and hub.human_seat == human_seat
            and hub.theme == self.cfg.theme
        )

    def _start_live_human_game(
        self,
        parts: list[str],
        n: int,
        *,
        human_seat: int | None = None,
    ) -> None:
        """Backward-compatible alias for `_start_live_game`."""
        self._start_live_game(parts, n, human_seat=human_seat)

    def _start_live_game(
        self,
        parts: list[str],
        n: int,
        *,
        human_seat: int | None = None,
    ) -> None:
        """
        Main GUI stays responsive; seat spawn + ready confirm + engine all run
        on a background thread (never block the pygame event loop).

        Works for human+AI and pure AI (all seats = watch windows).
        """
        from players.human_proxy import HumanPlayerProxy
        from players.seat_ui_hub import SeatUIHub

        self._live_mode = True
        self.runner = None
        self._live_done = False
        self._live_error = None
        self._live_runner = None
        # None ⇒ all seats are AI watch windows (must still confirm start)
        if human_seat is None:
            human_seat = _human_seat_index(parts)
        round_disp = self._round_index + 1
        gid = self.cfg.game_id or (
            f"human-{int(time.time())}"
            if human_seat is not None
            else f"ai-{int(time.time())}"
        )
        # Per-seat AI overrides from seat window settings (may update during wait)
        players_spec = self.cfg.players_spec
        theme = self.cfg.theme
        enable_exchange = bool(self.cfg.enable_exchange)
        num_rounds = max(1, int(self.cfg.num_rounds or 1))

        # 1) Layout on **current** cursor/console screen; pin main on THIS
        #    thread only; seats spawn on background with the same plan.
        from display.window_geometry import detect_screen as _detect_now

        target_screen = _detect_now()
        print(
            f"[live] target (current) screen {target_screen.width}x{target_screen.height} "
            f"@({target_screen.origin_x},{target_screen.origin_y}) "
            f"via {target_screen.source}"
        )
        plan = self._refresh_window_plan(n, screen=target_screen)
        try:
            # Main thread only — never call set_mode from seat-spawn worker
            self._pin_main_window(plan)
        except Exception as e:
            print(f"[display] main resize skip: {e}")

        self._status_msg = (
            f"第 {round_disp} 局 | 正在后台启动座位窗 S0–S{n - 1}…"
            f" @ {plan.screen_source}"
        )

        def work() -> None:
            human_tr = None
            nonlocal plan
            try:
                # 2) Spawn / reuse seats OFF main thread (same plan as main)
                if self._hub_compatible(n, human_seat) and self._seat_hub is not None:
                    try:
                        self._seat_hub.plan = plan
                        self._status_msg = "复用座位窗 / 补启缺失…"
                        human_tr = self._seat_hub.ensure_all()
                        # Pull reused seats onto the preferred layout screen
                        try:
                            self._seat_hub.apply_window_plan(plan)
                        except Exception:
                            pass
                        print(
                            f"[live] reusing seat hub alive="
                            f"{self._seat_hub.alive_seats()}"
                        )
                    except Exception as e:
                        print(f"[live] ensure_all failed, respawn: {e}")
                        try:
                            self._seat_hub.shutdown()
                        except Exception:
                            pass
                        self._seat_hub = None

                if self._seat_hub is None:
                    self._status_msg = "正在启动座位窗口（串行，约数秒）…"
                    self._seat_hub = SeatUIHub(
                        n,
                        human_seat=human_seat,
                        theme=theme,
                        plan=plan,
                    )
                    try:
                        human_tr = self._seat_hub.start_all()
                    except Exception as e:
                        print(f"[live] seat hub start_all failed: {e}")
                        self._status_msg = f"座位窗启动失败: {e}"
                        raise

                # Always ensure missing seats after first pass
                try:
                    human_tr = self._seat_hub.ensure_all() or human_tr
                except Exception as e:
                    print(f"[live] ensure_all after start: {e}")

                # Re-pin seats (Win HWND + macOS set_geometry wire)
                try:
                    if self._seat_hub is not None:
                        self._seat_hub.reassert_placements()
                except Exception as e:
                    print(f"[live] reassert skip: {e}")
                # Main pin must run on pygame thread
                self._request_main_pin(plan)

                started = list(getattr(self._seat_hub, "started_seats", []) or [])
                errs = list(getattr(self._seat_hub, "errors", []) or [])
                self._status_msg = (
                    f"第 {round_disp} 局 | 座位已启 {started}"
                    + (f" | 失败:{errs}" if errs else " | 请各窗确认开始")
                )

                # 1) Ready confirm FIRST so seat windows show 确认开始 immediately
                hub = self._seat_hub
                if hub is None or not hub.alive_seats():
                    raise RuntimeError(
                        f"无可用座位窗: started={started} errors={errs}"
                    )

                def _prog(msg: str) -> None:
                    self._status_msg = msg

                hub.wait_all_ready(
                    round_index=round_disp,
                    game_id=gid,
                    num_rounds=num_rounds,
                    timeout_ms=600_000,
                    on_progress=_prog,
                )
                self._last_ready_all_auto = bool(
                    getattr(hub, "last_ready_all_auto", False)
                )
                print(f"[live] ready all_auto={self._last_ready_all_auto}")
                self._status_msg = f"第 {round_disp} 局已确认，开局中…"

                # After all ready: reassert the *same* plan (do NOT re-detect
                # under cursor — user just clicked seats which may sit on another
                # monitor and would steal the layout away from the start screen).
                try:
                    if self._seat_hub is not None:
                        self._seat_hub.apply_window_plan(plan)
                    self._request_main_pin(plan)
                    print(f"[live] post-ready pin source={plan.screen_source}")
                except Exception as e:
                    print(f"[live] post-ready pin: {e}")

                # 2) Build players after ready (apply seat AI settings)
                # NOTE: do not assign to `players_spec` here — that would make it a
                # local name and raise UnboundLocalError on the RHS / create_players.
                effective_spec = players_spec
                if self._seat_hub is not None:
                    try:
                        self._seat_hub.poll_async_messages()
                        effective_spec = self._seat_hub.compose_players_spec(
                            players_spec
                        )
                        print(f"[live] players_spec effective={effective_spec}")
                    except Exception as e:
                        print(f"[live] compose players_spec: {e}")

                players = create_players(
                    effective_spec,
                    base_seed=int(time.time()) % 100000,
                    theme=theme,
                    training_mode=False,
                )
                if human_seat is not None and 0 <= human_seat < len(players):
                    pl = players[human_seat]
                    if isinstance(pl, HumanPlayerProxy) and human_tr is not None:
                        pl.attach_transport(human_tr, human_seat)
                        print(f"[live] human S{human_seat} attached")
                    elif isinstance(pl, HumanPlayerProxy):
                        print(
                            f"[live] WARNING: human transport missing; "
                            f"errors={getattr(self._seat_hub, 'errors', None)}"
                        )

                eng = EngineConfig(
                    num_players=n,
                    enable_exchange=enable_exchange,
                )

                def on_state(state: GameState) -> None:
                    hub2 = self._seat_hub
                    if hub2 is not None:
                        try:
                            hub2.poll_async_messages()
                        except Exception:
                            pass
                        hub2.broadcast(state)
                    # Main-window play log (display-only from existing events)
                    try:
                        self._ingest_play_log(state)
                    except Exception:
                        pass
                    # Main-window status: show mid-hand hu, never imply "round over"
                    try:
                        finished = [
                            p.seat
                            for p in state.players
                            if p.status == "finished"
                        ]
                        active = [
                            p.seat
                            for p in state.players
                            if p.status == "active"
                        ]
                        if state.phase == "finished":
                            self._status_msg = (
                                f"本局结束 ({state.finished_reason}) "
                                f"胡序={len(state.hu_sequence or [])}"
                            )
                        elif finished:
                            self._status_msg = (
                                f"血战继续 · 已胡 S{finished} · "
                                f"仍在打 S{active} · phase={state.phase} "
                                f"current=S{state.current_seat} 牌墙={len(state.wall)}"
                            )
                        else:
                            self._status_msg = (
                                f"行牌 phase={state.phase} "
                                f"current=S{state.current_seat} 牌墙={len(state.wall)}"
                            )
                    except Exception:
                        pass

                # Carry cumulative scores into this hand (multi-round session)
                start_scores = {
                    i: int(self._session_scores.get(i, 0)) for i in range(n)
                }
                self._hand_start_scores = dict(start_scores)
                step_ms = int(getattr(self.cfg, "step_ms", 200) or 200)
                self._live_runner = PlayerGameRunner(
                    players,
                    eng,
                    game_id=gid,
                    max_steps=50_000,
                    on_state_change=on_state,
                    join_extras={
                        "theme": theme,
                        "window_plan": plan_to_dict(plan),
                    },
                    shutdown_players_on_end=False,
                    # After human hus, only AI act — without delay the rest of
                    # the hand finishes in ms and looks like "hu then settle".
                    step_delay_ms=max(120, step_ms),
                    starting_scores=start_scores,
                )

                assert self._live_runner is not None
                result = self._live_runner.run()
                self.game_result = result
                # Persist cumulative totals for next hand / UI
                if result is not None and result.scores:
                    for sk, sv in result.scores.items():
                        try:
                            self._session_scores[int(sk)] = int(sv)
                        except (TypeError, ValueError):
                            pass
                if self._seat_hub is not None and result is not None:
                    try:
                        self._seat_hub.send_game_end(result.to_dict())
                    except Exception:
                        pass
            except BaseException as e:  # noqa: BLE001
                self._live_error = e
                print(f"[live] game error: {e}")
                self._status_msg = f"对局错误: {e}"
                try:
                    from pathlib import Path

                    for pth in sorted(Path("logs").glob("*.log")):
                        print(f"[live] log: {pth}")
                except Exception:
                    pass
            finally:
                self._live_done = True

        self._live_thread = threading.Thread(
            target=work, name="engine-live", daemon=True
        )
        self._live_thread.start()

    def _stop_live_game(self, *, close_seats: bool = True) -> None:
        """Stop engine thread. close_seats=False keeps player windows (F0003)."""
        if self._live_runner is not None:
            for pl in self._live_runner.players:
                try:
                    # Soft: HumanPlayerProxy without owns does not kill hub child
                    pl.shutdown()
                except Exception:
                    pass
        if self._live_thread is not None and self._live_thread.is_alive():
            self._live_thread.join(timeout=1.5)
        self._live_runner = None
        self._live_thread = None
        self._live_done = False
        self._live_error = None
        self._live_mode = False
        if self.runner is not None:
            try:
                for pl in self.runner._base.players:
                    pl.shutdown()
            except Exception:
                pass
        self.runner = None

        if close_seats:
            hub = getattr(self, "_seat_hub", None)
            if hub is not None:
                try:
                    hub.shutdown()
                except Exception:
                    pass
                self._seat_hub = None

    def _refresh_analysis(self) -> None:
        need = (
            self.cfg.show_hud
            or self.control_panel.options.show_inference
            or self.control_panel.options.show_strategy
        )
        if not need:
            self.analysis = None
            return
        st = self._current_state()
        if st is None:
            self.analysis = None
            return
        seat = self.cfg.focus_seat
        if seat >= st.num_players:
            seat = 0
            self.cfg.focus_seat = 0
            self.table.focus_seat = 0
            self.control_panel.options.focus_seat = 0
        legal = None
        if st.phase == "discard" and st.current_seat == seat:
            acts = legal_actions(st, seat)
            legal = [a for a in acts if a.type == ActionType.DISCARD]
        try:
            self.analysis = analyze_for_seat(st, seat, legal_discards=legal)
        except Exception as e:
            print(f"[hud] analysis error: {e}")
            self.analysis = None

    def _maybe_step(self) -> None:
        if self._live_mode:
            self._poll_live_game()
            return
        if not self.runner or self.runner.result is not None:
            return
        now = time.time()
        if (now - self._last_step) * 1000 < self.cfg.step_ms:
            return
        self._last_step = now
        try:
            done = self.runner.step_once()
        except Exception as e:
            print(f"[gui] step error: {e}")
            done = True
            if self.runner.state.phase != "finished":
                self.runner.state.phase = "finished"
                self.runner.state.finished_reason = "error"
            self.runner._finish()
        st = self.runner.state
        self._note_score_fx(st)
        self._refresh_analysis()
        if done or (self.runner.result is not None):
            self.game_result = self.runner.result
            if self.game_result and self.game_result.finished_reason == "wall_empty":
                self.fx.trigger("liuju", 1.2)
            self._round_index += 1
            self.scene = "result"
            self._arm_auto_next_round()

    def _poll_live_game(self) -> None:
        # Drain seat settings even while waiting / mid-hand
        if self._seat_hub is not None:
            try:
                self._seat_hub.poll_async_messages()
            except Exception:
                pass
        st = self._current_state()
        if st is not None:
            self._note_score_fx(st)
            now = time.time()
            if now - self._last_analysis > 0.35:
                self._last_analysis = now
                self._refresh_analysis()
            # status line by phase
            if st.phase in ("exchange", "dingque"):
                self._status_msg = (
                    f"开局 {st.phase} — 请在玩家窗口完成操作 (座位 S{self.cfg.focus_seat})"
                )
            elif st.phase in ("discard", "draw", "response"):
                self._status_msg = (
                    f"行牌 phase={st.phase} current=S{st.current_seat} "
                    f"— 主窗观战 / 玩家窗操作"
                )
            elif st.phase == "finished":
                self._status_msg = "本局结束"

        if self._live_done:
            if self._live_error is not None:
                self._status_msg = f"对局错误: {self._live_error}"
                print(f"[live] {self._live_error}")
            # Only settle when the engine hand is truly finished (血战)
            st_end = None
            if self._live_runner is not None:
                st_end = self._live_runner.state
            phase_done = st_end is not None and st_end.phase == "finished"
            if self.game_result is None and phase_done and st_end is not None:
                try:
                    from engine.blood_battle import build_game_result

                    self.game_result = build_game_result(st_end)
                except Exception:
                    pass
            if self.game_result is not None and phase_done:
                if self.game_result.finished_reason == "wall_empty":
                    self.fx.trigger("liuju", 1.2)
                self._round_index += 1
                self.scene = "result"
                self._arm_auto_next_round()
                alive = []
                if self._seat_hub is not None:
                    try:
                        alive = self._seat_hub.alive_seats()
                    except Exception:
                        pass
                self._status_msg = (
                    f"本局结束 第{self._round_index}/{self.cfg.num_rounds} | "
                    f"座位窗仍在 {alive or '—'} | "
                    f"原因={self.game_result.finished_reason} "
                    f"胡={len(self.game_result.hu_sequence or [])}家"
                )
            elif self._live_error is not None:
                # Keep table scene so user can read error / retry Start from lobby
                # without "vanishing" seat windows into a silent cover bounce.
                self.scene = "table"
                self._status_msg = (
                    f"对局中断: {self._live_error}  — 按 Esc 回大厅后可重开"
                )
                print(f"[live] stay on table after error: {self._live_error}")
            else:
                # Incomplete hand without result — do not silently return to lobby
                self.scene = "table"
                self._status_msg = "对局未正常结束 — 按 Esc 回大厅或检查座位窗"
            self._live_mode = False

    def _note_score_fx(self, st: GameState) -> None:
        if not st.score_events:
            return
        last = st.score_events[-1]
        if last.get("type") != "score":
            return
        for t in last.get("transfers") or []:
            if str(t.get("reason", "")).startswith("hu"):
                self.fx.trigger("hu")
                break
            if "gang" in str(t.get("reason", "")):
                self.fx.trigger("gang")
                break

    def _ingest_play_log(self, state: GameState) -> None:
        """Append display lines from public state deltas (no rule changes)."""
        log = self.play_log
        # Track last discard
        ld = getattr(state, "last_discard", None)
        if ld is not None:
            seat = getattr(ld, "seat", None)
            tid = getattr(ld, "tile_id", None) or getattr(ld, "tile", None)
            if hasattr(tid, "id"):
                tid = tid.id
            fp = ("discard", seat, str(tid) if tid else None, getattr(state, "action_index", None))
            if getattr(self, "_play_log_fp", None) != fp:
                self._play_log_fp = fp
                seat_s = f"S{seat}" if seat is not None else "?"
                log.append("discard", f"{seat_s} 出 {tid or '?'}", seat=seat, tile_id=str(tid) if tid else None)
        # Score / hu events tail
        events = list(getattr(state, "score_events", None) or [])
        n_seen = int(getattr(self, "_play_log_score_n", 0) or 0)
        if len(events) < n_seen:
            n_seen = 0
        for ev in events[n_seen:]:
            if not isinstance(ev, dict):
                continue
            et = str(ev.get("type") or "")
            if et == "score":
                for t in ev.get("transfers") or []:
                    reason = str(t.get("reason") or "")
                    fr = t.get("from")
                    to = t.get("to")
                    if reason.startswith("hu"):
                        log.append("hu", f"S{to if to is not None else '?'} 胡 ({reason})")
                    elif "gang" in reason:
                        log.append("gang", f"杠分 {reason} S{fr}→S{to}")
            elif et:
                log.append("info", et)
        self._play_log_score_n = len(events)
        if state.phase == "finished":
            fin_fp = ("finished", str(state.finished_reason), len(state.hu_sequence or []))
            if getattr(self, "_play_log_fin_fp", None) != fin_fp:
                self._play_log_fin_fp = fin_fp
                log.append(
                    "info",
                    f"本局结束 · {state.finished_reason or '?'}",
                )

    def _on_resize(self, w: int, h: int) -> None:
        # Full mode: lock to plan complete size (≤1080p); do not enlarge
        locked = getattr(self, "_main_locked_size", None)
        if locked is not None:
            tw, th = int(locked[0]), int(locked[1])
        else:
            tw, th = clamp_outer_size(int(w), int(h), kind="main")
        # If user dragged larger, snap back to locked complete size
        if int(w) != tw or int(h) != th:
            w, h = tw, th
        else:
            w, h = tw, th
        self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
        if self.screen is None:
            self.screen = pygame.display.get_surface()
        self.layout = Layout.from_window(w, h)
        self.table.resize(w, h)

    def _handle_events(self) -> None:
        try:
            events = list(pygame.event.get())
        except Exception as e:
            print(f"[display] event.get failed: {e}")
            return
        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.VIDEORESIZE:
                self._on_resize(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.scene == "lobby":
                        self._running = False
                    else:
                        # Back to cover; keep seat windows for next Start
                        self._stop_live_game(close_seats=False)
                        self._session_active = False
                        self.scene = "lobby"
                elif self.scene == "lobby":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self._start_game(new_session=True)
                    elif event.key == pygame.K_t:
                        self._toggle_theme()
                    elif event.key == pygame.K_e:
                        self.cfg.enable_exchange = not self.cfg.enable_exchange
                    elif event.key == pygame.K_f:
                        self.cfg.spectator = "full"
                    elif event.key == pygame.K_p:
                        self.cfg.spectator = "public"
                elif self.scene == "result":
                    if event.key in (pygame.K_RETURN, pygame.K_r):
                        self._on_play_again()
                    elif event.key == pygame.K_l:
                        self._return_to_lobby(close_seats=False)
                elif self.scene == "table":
                    if event.key == pygame.K_RIGHT:
                        self._last_step = 0
                    elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                        self.cfg.step_ms = max(50, self.cfg.step_ms - 50)
                    elif event.key == pygame.K_MINUS:
                        self.cfg.step_ms = min(2000, self.cfg.step_ms + 50)
                    elif event.key == pygame.K_h:
                        self.cfg.show_hud = not self.cfg.show_hud
                        self.table.show_hud = self.cfg.show_hud
                        self.control_panel.options.show_inference = self.cfg.show_hud
                        self.control_panel.options.show_strategy = self.cfg.show_hud
                        self._refresh_analysis()
                    elif event.key == pygame.K_a:
                        self._refresh_analysis()
                    elif event.key in (
                        pygame.K_1,
                        pygame.K_2,
                        pygame.K_3,
                        pygame.K_4,
                    ):
                        seat = event.key - pygame.K_1
                        st = self._current_state()
                        if st is not None and seat < st.num_players:
                            self.cfg.focus_seat = seat
                            self.table.focus_seat = seat
                            self.control_panel.options.focus_seat = seat
                            self._refresh_analysis()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if self.scene == "lobby":
                    self._handle_lobby_click(pos)
                elif self.scene == "result":
                    if self.result_view.hit_lobby(pos):
                        self._return_to_lobby(close_seats=False)
                    elif self.result_view.hit_again(pos):
                        self._on_play_again()
                elif self.scene == "table":
                    st = self._current_state()
                    n = st.num_players if st is not None else self.cfg.num_players
                    if self.control_panel.handle_click(
                        pos,
                        num_players=n,
                        auto_next_eligible=self._auto_next_eligible(),
                    ):
                        # keep legacy show_hud in sync with both HUD switches
                        self.cfg.show_hud = (
                            self.control_panel.options.show_inference
                            or self.control_panel.options.show_strategy
                        )
                        self.table.show_hud = self.cfg.show_hud
                        # panel width may change when collapse/expand
                        sw, sh = self.screen.get_size()
                        self.table.resize(sw, sh)
                        self._refresh_analysis()

    def _handle_lobby_click(self, pos: tuple[int, int]) -> None:
        from display.lobby_view import (
            CTL_EXCHANGE,
            CTL_MODE,
            CTL_PLAYERS,
            CTL_ROUNDS,
            CTL_START,
            CTL_THEME,
        )

        ctl = self.lobby.hit_control(pos)
        if ctl == CTL_START or self.lobby.hit_start(pos):
            self._start_game(new_session=True)
            return
        if ctl == CTL_THEME or self.lobby.hit_theme(pos):
            self._toggle_theme()
            return
        if ctl == CTL_MODE:
            self.cfg.game_mode = self.lobby.cycle_mode(self.cfg.game_mode)
            return
        if ctl == CTL_PLAYERS:
            old = self.cfg.players_spec
            self.cfg.players_spec = self.lobby.cycle_players(old)
            parts = _parse_parts(self.cfg.players_spec)
            self.cfg.num_players = len(parts) or 4
            hi = _human_seat_index(parts)
            self.cfg.focus_seat = hi if hi is not None else 0
            # Player layout changed — must rebuild seat windows next start
            if old != self.cfg.players_spec:
                self._stop_live_game(close_seats=True)
            return
        if ctl == CTL_EXCHANGE:
            self.cfg.enable_exchange = not self.cfg.enable_exchange
            return
        if ctl == CTL_ROUNDS:
            self.cfg.num_rounds = self.lobby.cycle_rounds(self.cfg.num_rounds)
            return

    def _auto_next_eligible(self) -> bool:
        """Settlement auto-next only when all seats auto-confirmed last hand."""
        return bool(self._last_ready_all_auto) and self.cfg.num_rounds > 1

    def _arm_auto_next_round(self) -> None:
        """Start 3s countdown on result if switch on and all seats auto."""
        self._auto_next_deadline = None
        if not self.control_panel.options.auto_next_round:
            return
        if not self._auto_next_eligible():
            return
        if self._round_index >= self.cfg.num_rounds:
            return
        self._auto_next_deadline = time.time() + float(self._auto_next_seconds)
        self._status_msg = (
            f"四方已自动开始 · {int(self._auto_next_seconds)} 秒后进入下一局…"
        )

    def _tick_auto_next_round(self) -> None:
        """Countdown on result scene; fire play-again when due."""
        if self.scene != "result":
            return
        if self._auto_next_deadline is None:
            # Allow enabling the switch while already on result
            if (
                self.control_panel.options.auto_next_round
                and self._auto_next_eligible()
                and self._round_index < self.cfg.num_rounds
            ):
                self._arm_auto_next_round()
            return
        if not self.control_panel.options.auto_next_round or not self._auto_next_eligible():
            self._auto_next_deadline = None
            return
        remain = self._auto_next_deadline - time.time()
        if remain <= 0:
            self._auto_next_deadline = None
            self._status_msg = "自动进入下一局…"
            self._on_play_again()
            return
        self._status_msg = f"自动下一局倒计时 {remain:.1f}s（R 立即开始）"

    def _on_play_again(self) -> None:
        """Continue session if rounds remain; else stay on result / lobby."""
        self._auto_next_deadline = None
        if self._round_index >= self.cfg.num_rounds:
            self._status_msg = (
                f"已完成全部 {self.cfg.num_rounds} 局，回大厅可改设置后重新开始"
            )
            self._return_to_lobby(close_seats=False)
            return
        self._start_game(new_session=False)

    def _return_to_lobby(self, *, close_seats: bool = False) -> None:
        self._stop_live_game(close_seats=close_seats)
        self._session_active = False
        self._auto_next_deadline = None
        # Keep last session scores visible only until next lobby Start (reset then)
        self.scene = "lobby"

    def _toggle_theme(self) -> None:
        new = "blue" if self.cfg.theme == "green" else "green"
        self.cfg.theme = new
        self.assets.set_theme(new)
        self.lobby = LobbyView(self.assets)
        sw, sh = self.screen.get_size()
        self.layout = Layout.from_window(sw, sh)
        self.table = TableView(
            self.assets,
            layout=self.layout,
            spectator="full" if self.cfg.spectator == "full" else "public",
            focus_seat=self.cfg.focus_seat,
            show_hud=self.cfg.show_hud,
            control_panel=self.control_panel,
        )
        self.table.play_log = self.play_log
        self.result_view = ResultView(self.assets)
        # Theme change requires new seat assets/theme → close seats
        self._stop_live_game(close_seats=True)

    def _draw(self) -> None:
        # Guard against stale Surface after set_mode / window pin
        if self.screen is None or not getattr(self.screen, "get_width", None):
            surf = pygame.display.get_surface()
            if surf is not None:
                self.screen = surf
        if self.screen is None:
            return
        try:
            _ = self.screen.get_size()
        except Exception:
            surf = pygame.display.get_surface()
            if surf is None:
                return
            self.screen = surf
        if self.scene == "lobby":
            self.lobby.draw(
                self.screen,
                theme=self.cfg.theme,
                num_players=self.cfg.num_players,
                players_spec=self.cfg.players_spec,
                spectator=self.cfg.spectator,
                game_mode=self.cfg.game_mode,
                enable_exchange=self.cfg.enable_exchange,
                num_rounds=self.cfg.num_rounds,
            )
        elif self.scene == "table":
            st = self._current_state()
            if st is not None:
                self.table.auto_next_eligible = self._auto_next_eligible()
                self.table.draw(
                    self.screen,
                    st,
                    self.fx,
                    analysis=self.analysis if self.cfg.show_hud else None,
                )
            else:
                self.screen.fill((20, 40, 30))
                draw_text(
                    self.screen,
                    "正在启动对局 / 等待引擎发牌…",
                    (40, 40),
                    size=22,
                    color=(200, 220, 200),
                )
            if self._status_msg:
                draw_text(
                    self.screen,
                    self._status_msg,
                    (20, self.screen.get_height() - 28),
                    size=14,
                    color=(255, 240, 160),
                )
        elif self.scene == "result" and self.game_result is not None:
            countdown = None
            if self._auto_next_deadline is not None:
                countdown = max(0.0, self._auto_next_deadline - time.time())
            self.result_view.draw(
                self.screen,
                self.game_result,
                round_index=self._round_index,
                num_rounds=self.cfg.num_rounds,
                auto_next_countdown=countdown,
                session_scores=dict(self._session_scores)
                if self._session_scores
                else dict(self.game_result.scores or {}),
                hand_start_scores=dict(self._hand_start_scores or {}),
            )
            if self._status_msg:
                draw_text(
                    self.screen,
                    self._status_msg,
                    (20, self.screen.get_height() - 28),
                    size=14,
                    color=(255, 240, 160),
                )
        else:
            self.screen.fill((20, 40, 30))


def run_gui(
    *,
    theme: str = "green",
    players: str = "rule_ai,rule_ai,rule_ai,rule_ai",
    spectator: str = "full",
    step_ms: int = 200,
    auto_start: bool = False,
    game_id: str | None = None,
    enable_exchange: bool = True,
    num_rounds: int = 1,
    game_mode: str = "blood_battle",
) -> None:
    parts = _parse_parts(players)
    human_i = _human_seat_index(parts)
    app = MahjongApp(
        AppConfig(
            theme=theme,
            num_players=len(parts) or 4,
            players_spec=players,
            spectator=spectator,
            step_ms=step_ms,
            game_id=game_id,
            focus_seat=human_i if human_i is not None else 0,
            enable_exchange=enable_exchange,
            num_rounds=max(1, int(num_rounds)),
            game_mode=game_mode,
        )
    )
    app.run(auto_start=auto_start)
