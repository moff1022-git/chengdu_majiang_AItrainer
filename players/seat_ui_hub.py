"""Spawn and manage ALL seat windows (human play + AI watch) — F0002/F0004."""

from __future__ import annotations

import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable

from engine.state import GameState
from protocols.subprocess_transport import SubprocessTransport
from protocols.view_filter import build_observation

# Sequential spawn off the main pygame thread.
# Tk seat windows are multi-process safe; short gap is enough.
_SPAWN_GAP_S = 0.35
_POST_HELLO_STABLE_S = 0.15
_SPAWN_RETRIES = 2


class SeatUIHub:
    """
    Starts one seat_window process per seat using a shared WindowPlan.
    Human seats use mode=play; AI seats use mode=watch (F0020 multi-human).
    """

    def __init__(
        self,
        num_players: int,
        *,
        human_seat: int | None = None,
        human_seats: list[int] | None = None,
        theme: str = "green",
        python_exe: str | None = None,
        plan=None,
        human_timeout_ms: int = 300_000,
    ) -> None:
        self.num_players = num_players
        # F0020: prefer human_seats list; human_seat kept as first-human alias
        if human_seats is not None:
            self.human_seats = [int(s) for s in human_seats]
        elif human_seat is not None:
            self.human_seats = [int(human_seat)]
        else:
            self.human_seats = []
        self.human_seat = self.human_seats[0] if self.human_seats else None
        self.theme = theme
        self.python_exe = python_exe or sys.executable
        self.plan = plan
        self.human_timeout_ms = human_timeout_ms
        self._root = str(Path(__file__).resolve().parent.parent)
        self.errors: list[str] = []
        self.started_seats: list[int] = []
        self.transports: dict[int, SubprocessTransport] = {}
        self._lock = threading.Lock()
        # Last wait_all_ready: every seat confirmed with auto=True
        self.last_ready_all_auto: bool = False
        # While True, main-thread poll_async must not steal ready/decision lines
        self._ready_wait_active: bool = False
        # Per-seat AI type overrides from seat window settings (next hand)
        # seat -> strategy preset id or player key (human seats ignored)
        # e.g. "random" | "rule_ai" | "rule_ai_plus"
        self.seat_ai_types: dict[int, str] = {}
        self.seat_auto_start: dict[int, bool] = {}
        # F0010: seats that enabled opponent-hand prediction (public view only).
        self.seat_predict_opponents: dict[int, bool] = {}
        self._discard_seq: int = 0
        self._last_discard_fp: str | None = None
        # F0013 broadcast throttle / content signature
        self._last_broadcast_sig: Any = None
        self._last_broadcast_t: float = 0.0
        self._broadcast_min_interval_s: float = 0.06
        # Actual human Tk client size from window_ready (for MAIN height match)
        self.human_client_size: tuple[int, int] | None = None
        # seat -> transport for every play (human) seat
        self.human_transports: dict[int, SubprocessTransport] = {}

    def _mode_for(self, seat: int) -> str:
        if int(seat) in set(self.human_seats):
            return "play"
        return "watch"

    def _spawn_one(self, seat: int, mode: str) -> SubprocessTransport:
        from display.window_geometry import (
            force_placement_by_pid,
            plan_cli_args,
            plan_for_screen,
        )

        if self.plan is None:
            plan = plan_for_screen(
                self.num_players, human_seats=list(self.human_seats)
            )
        else:
            plan = self.plan
        # Windows only: keep seats on real monitor work areas
        if sys.platform == "win32":
            from display.window_geometry import clamp_rect_to_visible, sanitize_window_plan

            plan = sanitize_window_plan(plan)
        self.plan = plan
        rect = plan.players.get(seat)
        if rect is not None and sys.platform == "win32":
            from display.window_geometry import clamp_rect_to_visible

            rect = clamp_rect_to_visible(rect)
        extra = plan_cli_args(rect) if rect else []
        extra = [
            "--mode",
            mode,
            "--num-players",
            str(self.num_players),
            *extra,
        ]
        tr = SubprocessTransport(
            seat,
            theme=self.theme,
            # Watch windows also need long ready-confirm timeout
            timeout_ms=self.human_timeout_ms if mode == "play" else max(
                120_000, self.human_timeout_ms
            ),
            extra_args=extra,
            module="players.seat_window",
            python_exe=self.python_exe,
        )
        hello = tr.start()
        time.sleep(_POST_HELLO_STABLE_S)
        if tr._proc is None or tr._proc.poll() is not None:
            code = tr._proc.returncode if tr._proc else None
            try:
                tr.shutdown()
            except Exception:
                pass
            raise RuntimeError(
                f"S{seat} exited right after hello code={code} "
                f"(see logs/human_seat{seat}_stderr.log / seat_*_crash.log)"
            )

        pid = int(hello.get("pid") or (tr._proc.pid if tr._proc else 0) or 0)
        # Best-effort: wait for window_ready, then pin by PID.
        # Do NOT kill just because HWND lookup failed — that made every seat flaky.
        wr = None
        try:
            wr = tr.wait_window_ready(timeout_ms=5_000)
        except Exception as e:
            print(f"[seat-hub] S{seat} window_ready wait err: {e}")
        # Human seat: remember actual client size so MAIN can match height
        if wr and mode == "play":
            try:
                self.human_client_size = (
                    int(wr.get("w") or 0),
                    int(wr.get("h") or 0),
                )
                print(
                    f"[seat-hub] human client size from window_ready: "
                    f"{self.human_client_size[0]}x{self.human_client_size[1]}"
                )
            except Exception:
                pass

        if tr._proc is not None and tr._proc.poll() is not None:
            code = tr._proc.returncode
            try:
                tr.shutdown()
            except Exception:
                pass
            raise RuntimeError(
                f"S{seat} died after hello code={code} (see logs/human_seat{seat}_stderr.log)"
            )

        # Windows: re-pin via HWND. macOS/Linux: Tk already used CLI geometry (F0005).
        placed = False
        if sys.platform == "win32" and rect is not None and pid:
            for attempt in range(1, 5):
                placed = force_placement_by_pid(
                    pid, rect.x, rect.y, rect.w, rect.h, timeout_s=0.8
                )
                if placed:
                    break
                time.sleep(0.3 * attempt)
        elif rect is not None:
            # Geometry applied at seat_window open via Tk --geometry (authoritative).
            placed = True

        print(
            f"[seat-hub] {mode} S{seat} ok pid={pid} placed={placed} "
            f"ready={bool(wr)} @ {rect}"
        )
        if not placed and sys.platform == "win32":
            print(
                f"[seat-hub] WARNING S{seat}: no HWND yet — will reassert later; "
                f"check logs/human_seat{seat}_stderr.log"
            )
        time.sleep(_SPAWN_GAP_S)
        return tr

    def _spawn_with_retries(self, seat: int) -> SubprocessTransport:
        mode = self._mode_for(seat)
        last_err: Exception | None = None
        for attempt in range(1, _SPAWN_RETRIES + 1):
            try:
                # Clear any half-dead transport
                old = self.transports.pop(seat, None)
                if old is not None:
                    try:
                        old.shutdown()
                    except Exception:
                        pass
                return self._spawn_one(seat, mode)
            except Exception as e:
                last_err = e
                print(
                    f"[seat-hub] {mode} S{seat} attempt {attempt}/{_SPAWN_RETRIES} "
                    f"failed: {e}"
                )
                time.sleep(0.5 * attempt)
        raise RuntimeError(f"S{seat} failed after {_SPAWN_RETRIES} tries: {last_err}")

    def _register(self, seat: int, tr: SubprocessTransport) -> None:
        with self._lock:
            self.transports[seat] = tr
            if seat not in self.started_seats:
                self.started_seats.append(seat)
            self.started_seats = sorted(set(self.started_seats))

    def seat_pids(self) -> dict[int, int]:
        out: dict[int, int] = {}
        with self._lock:
            items = list(self.transports.items())
        for seat, tr in items:
            if tr._proc is not None and tr._proc.poll() is None:
                out[seat] = int(tr._proc.pid)
        return out

    def reassert_placements(self) -> None:
        """
        Re-place seat windows only (never the main pygame window).

        Must be safe to call from the engine **background** thread: do not
        call pygame.display.set_mode / force_window_placement on main.
        """
        if self.plan is None:
            return
        try:
            from display.window_geometry import reassert_plan_windows

            # include_main=False: main pin is main-thread only (macOS SEGV otherwise)
            results = reassert_plan_windows(
                self.plan, seat_pids=self.seat_pids(), include_main=False
            )
            print(f"[seat-hub] reassert placements: {results}")
        except Exception as e:
            print(f"[seat-hub] reassert placements skipped: {e}")
        # macOS/Linux: push Tk geometry over NDJSON (authoritative there).
        # Windows: HWND place above is enough — do NOT also flood set_geometry
        # (fights user drag/resize and can steal focus).
        if sys.platform != "win32":
            try:
                self.apply_window_plan(self.plan)
            except Exception as e:
                print(f"[seat-hub] apply_window_plan skip: {e}")

    def apply_window_plan(self, plan) -> None:
        """Update shared plan and tell each seat Tk window to move/resize."""
        if plan is None:
            return
        if sys.platform == "win32":
            from display.window_geometry import clamp_rect_to_visible, sanitize_window_plan

            plan = sanitize_window_plan(plan)
        self.plan = plan
        with self._lock:
            items = list(self.transports.items())
        for seat, tr in items:
            if tr._proc is None or tr._proc.poll() is not None:
                continue
            rect = None
            try:
                rect = plan.players.get(seat)
            except Exception:
                rect = None
            if rect is None:
                continue
            if sys.platform == "win32":
                from display.window_geometry import clamp_rect_to_visible

                rect = clamp_rect_to_visible(rect)
            try:
                tr.send_set_geometry(rect.x, rect.y, rect.w, rect.h)
            except Exception as e:
                print(f"[seat-hub] set_geometry S{seat} failed: {e}")

    def start_all(self) -> dict[int, SubprocessTransport]:
        """
        Spawn every seat window **sequentially** (humans first).
        Returns map seat -> transport for all play (human) seats.
        """
        from display.window_geometry import log_plan, plan_for_screen

        if self.plan is None:
            plan = plan_for_screen(
                self.num_players, human_seats=list(self.human_seats)
            )
        else:
            plan = self.plan
        self.plan = plan
        log_plan(plan, prefix="[seat-hub]")
        self.errors = []
        self.started_seats = []
        self.transports = {}
        self.human_transports = {}

        order: list[int] = list(self.human_seats)
        for s in range(self.num_players):
            if s not in order:
                order.append(s)

        print(
            f"[seat-hub] sequential spawn order={order} "
            f"human_seats={self.human_seats}"
        )
        for seat in order:
            try:
                tr = self._spawn_with_retries(seat)
                self._register(seat, tr)
                if seat in self.human_seats:
                    self.human_transports[seat] = tr
            except Exception as e:
                msg = f"{self._mode_for(seat)} S{seat} failed: {e}"
                self.errors.append(msg)
                print(f"[seat-hub] {msg}")

        # Second pass: fill any missing/dead seats
        missing = [
            s
            for s in range(self.num_players)
            if not self._alive(s)
        ]
        if missing:
            print(f"[seat-hub] second pass for missing: {missing}")
            for seat in missing:
                try:
                    tr = self._spawn_with_retries(seat)
                    self._register(seat, tr)
                    if seat in self.human_seats:
                        self.human_transports[seat] = tr
                    # remove prior error for this seat if recovered
                    self.errors = [
                        e for e in self.errors if f"S{seat}" not in e
                    ]
                except Exception as e:
                    msg = f"second-pass S{seat} failed: {e}"
                    self.errors.append(msg)
                    print(f"[seat-hub] {msg}")

        self.started_seats = self.alive_seats()
        print(
            f"[seat-hub] started={self.started_seats} errors={self.errors or 0}"
        )
        if set(range(self.num_players)) - set(self.started_seats):
            still = sorted(set(range(self.num_players)) - set(self.started_seats))
            print(f"[seat-hub] WARNING still missing seats: {still}")

        # Parent forces all titles to plan positions (fixes off-screen / buried)
        time.sleep(0.2)
        self.reassert_placements()
        return dict(self.human_transports)

    def start(self) -> None:
        """Back-compat alias."""
        self.start_all()

    def _alive(self, seat: int) -> bool:
        tr = self.transports.get(seat)
        if tr is None or tr._proc is None:
            return False
        return tr._proc.poll() is None

    def alive_seats(self) -> list[int]:
        with self._lock:
            seats = list(self.transports.keys())
        return sorted(s for s in seats if self._alive(s))

    def ensure_all(self) -> dict[int, SubprocessTransport]:
        """
        Keep live windows; respawn only missing/dead seats (sequential).
        Returns map of human seat -> transport.
        """
        if not self.transports:
            return self.start_all()

        self.human_transports = {
            s: self.transports[s]
            for s in self.human_seats
            if s in self.transports and self._alive(s)
        }

        for seat in range(self.num_players):
            if self._alive(seat):
                continue
            mode = self._mode_for(seat)
            try:
                tr = self._spawn_with_retries(seat)
                self._register(seat, tr)
                if seat in self.human_seats:
                    self.human_transports[seat] = tr
                print(f"[seat-hub] respawned {mode} S{seat}")
            except Exception as e:
                self.errors.append(f"respawn {mode} S{seat}: {e}")
                print(f"[seat-hub] respawn {mode} S{seat} failed: {e}")

        self.started_seats = self.alive_seats()
        self.reassert_placements()
        return dict(self.human_transports)

    def _broadcast_signature(self, state: GameState) -> tuple:
        """Content signature for F0013 skip-identical broadcasts."""
        try:
            ld = state.last_discard.id if state.last_discard is not None else None
        except Exception:
            ld = None
        try:
            scores = tuple(
                int(getattr(p, "score", 0) or 0) for p in (state.players or [])
            )
            # Hand tile multiset — exchange can change tiles without length change
            hands_key = []
            meld_key = []
            statuses = []
            for p in state.players or []:
                hand = getattr(p, "hand", None) or []
                try:
                    hands_key.append(
                        tuple(sorted(getattr(t, "id", str(t)) for t in hand))
                    )
                except Exception:
                    hands_key.append((len(hand),))
                melds = getattr(p, "melds", None) or []
                try:
                    meld_key.append(
                        tuple(
                            (
                                str(m.get("kind") if isinstance(m, dict) else ""),
                                str(
                                    m.get("tile_id")
                                    if isinstance(m, dict)
                                    else getattr(m, "tile_id", "")
                                ),
                            )
                            for m in melds
                        )
                    )
                except Exception:
                    meld_key.append((len(melds),))
                statuses.append(str(getattr(p, "status", "") or ""))
            hands_key_t = tuple(hands_key)
            meld_key_t = tuple(meld_key)
            statuses_t = tuple(statuses)
        except Exception:
            scores = ()
            hands_key_t = ()
            meld_key_t = ()
            statuses_t = ()
        return (
            str(getattr(state, "phase", "") or ""),
            int(getattr(state, "turn_index", 0) or 0),
            int(len(getattr(state, "wall", None) or [])),
            ld,
            getattr(state, "last_discard_seat", None),
            getattr(state, "current_seat", None),
            scores,
            hands_key_t,
            meld_key_t,
            statuses_t,
            int(self._discard_seq),
        )

    def broadcast(self, state: GameState) -> None:
        dead: list[int] = []
        with self._lock:
            items = list(self.transports.items())
        # Track global discard generation for F0010 refresh cadence
        try:
            ld = state.last_discard.id if state.last_discard is not None else None
            ls = state.last_discard_seat
            fp = f"{ls}:{ld}"
            if ld is not None and fp != self._last_discard_fp:
                self._last_discard_fp = fp
                self._discard_seq += 1
        except Exception:
            pass

        # F0013: skip identical state bursts; allow immediate send when sig changes
        now = time.time()
        try:
            sig = self._broadcast_signature(state)
        except Exception:
            sig = None
        if (
            sig is not None
            and sig == self._last_broadcast_sig
            and (now - float(self._last_broadcast_t or 0.0))
            < float(self._broadcast_min_interval_s or 0.06)
        ):
            return
        if sig is not None:
            self._last_broadcast_sig = sig
            self._last_broadcast_t = now

        # Throttle: after a seat has hu'd, still update UI but never block engine
        for seat, tr in items:
            try:
                if tr._proc is None or tr._proc.poll() is not None:
                    dead.append(seat)
                    continue
                obs = build_observation(
                    state,
                    seat,
                    discard_seq=self._discard_seq,
                )
                tr.send_observation(obs)
            except Exception as e:
                # Do not kill the whole hand if one seat window lags
                print(f"[seat-hub] broadcast S{seat} failed: {e}")
        if dead:
            with self._lock:
                for s in dead:
                    self.transports.pop(s, None)
                    if s in self.started_seats:
                        self.started_seats.remove(s)

    def send_game_end(self, result: dict) -> None:
        with self._lock:
            items = list(self.transports.items())
        for seat, tr in items:
            try:
                tr.send_game_end(result)
            except Exception:
                pass

    def apply_seat_settings_msg(self, msg: dict) -> None:
        """Apply seat_settings from a seat window (AI type / auto preference)."""
        try:
            seat = int(msg.get("seat", -1))
        except (TypeError, ValueError):
            return
        if seat < 0 or seat >= self.num_players:
            return
        if "auto_start" in msg:
            self.seat_auto_start[seat] = bool(msg.get("auto_start"))
        if "predict_opponents" in msg:
            self.seat_predict_opponents[seat] = bool(msg.get("predict_opponents"))
            print(
                f"[seat-hub] S{seat} predict_opponents -> "
                f"{self.seat_predict_opponents[seat]}"
            )
        ai = msg.get("ai_type")
        if ai is not None:
            key = str(ai).strip().lower().split(":")[0]
            try:
                from players.strategy_presets import get_preset, list_strategy_ids

                known = set(list_strategy_ids()) | {"random", "rule_ai"}
                ok = key in known or get_preset(key) is not None
            except Exception:
                ok = key in ("random", "rule_ai", "rule_ai_plus")
            if ok:
                # Never override human seat type (F0020: multi-human)
                if int(seat) in set(self.human_seats):
                    return
                self.seat_ai_types[seat] = key
                print(f"[seat-hub] S{seat} ai_type -> {key} (next hand)")

    def poll_async_messages(self) -> int:
        """
        Non-blocking drain of seat stdout for seat_settings (and ignore noise).
        Re-queues decision/ready so decision/ready waits still work.
        Returns number of seat_settings applied.

        While ``_ready_wait_active``, skip entirely — concurrent pop races with
        ``request_ready`` and can drop or reorder ready replies (4AI hang / no UI).
        """
        if self._ready_wait_active:
            return 0
        n = 0
        with self._lock:
            items = list(self.transports.items())
        for seat, tr in items:
            if tr._proc is None or tr._proc.poll() is not None:
                continue
            while True:
                msg = tr.try_pop_message()
                if msg is None:
                    break
                mtype = msg.get("type")
                if mtype == "seat_settings":
                    self.apply_seat_settings_msg(msg)
                    n += 1
                elif mtype in ("ready", "decision", "hello", "window_ready"):
                    # Must not drop — put back for the waiting reader
                    try:
                        tr.requeue_message(msg)
                    except Exception:
                        pass
                    break  # stop draining this seat to avoid busy loop
                # else: drop unknown/noise
        return n

    def compose_players_spec(self, base_spec: str) -> str:
        """
        Merge lobby base players_spec with per-seat AI overrides.
        Human seats stay human; AI seats may become random/rule_ai.
        """
        parts = [p.strip() for p in str(base_spec).split(",") if p.strip()]
        # pad / trim to num_players
        while len(parts) < self.num_players:
            parts.append("rule_ai")
        parts = parts[: self.num_players]
        out: list[str] = []
        for i, spec in enumerate(parts):
            key = spec.split(":")[0].strip().lower()
            if key == "human":
                out.append(spec)
                continue
            if i in self.seat_ai_types:
                out.append(self.seat_ai_types[i])
            else:
                out.append(spec)
        return ",".join(out)

    def wait_all_ready(
        self,
        *,
        round_index: int = 1,
        game_id: str = "",
        num_rounds: int = 1,
        timeout_ms: int = 600_000,
        on_progress: Callable[[str], None] | None = None,
    ) -> list[int]:
        """
        Ask every alive seat window to confirm start (parallel).
        Returns sorted list of seats that confirmed.
        Raises RuntimeError if any seat fails/times out.
        """
        # Best-effort: bring missing seats back before ready
        try:
            self.ensure_all()
        except Exception as e:
            print(f"[seat-hub] ensure_all before ready: {e}")

        with self._lock:
            items = [
                (s, tr)
                for s, tr in self.transports.items()
                if tr._proc is not None and tr._proc.poll() is None
            ]
        if not items:
            raise RuntimeError("no alive seat windows for ready confirm")

        seats = sorted(s for s, _ in items)
        expected = list(range(self.num_players))
        if set(seats) != set(expected):
            print(
                f"[seat-hub] WARNING ready with partial seats "
                f"{seats} expected {expected}"
            )

        print(
            f"[seat-hub] ready_request round={round_index}/{num_rounds} "
            f"seats={seats} game_id={game_id!r}"
        )
        if on_progress:
            try:
                on_progress(f"等待座位确认: {seats} · 第{round_index}/{num_rounds}局")
            except Exception:
                pass

        confirmed: list[int] = []
        auto_flags: dict[int, bool] = {}
        errors: list[str] = []
        self.last_ready_all_auto = False
        # Set BEFORE any I/O so main-thread poll cannot race on ready lines
        self._ready_wait_active = True
        try:
            def _one(seat: int, tr: SubprocessTransport) -> tuple[int, str | None, bool]:
                try:
                    msg = tr.request_ready(
                        round_index=round_index,
                        game_id=game_id,
                        num_players=self.num_players,
                        num_rounds=num_rounds,
                        timeout_ms=timeout_ms,
                    )
                    auto = bool(msg.get("auto"))
                    print(
                        f"[seat-hub] ready S{seat}"
                        + (" (auto)" if auto else "")
                    )
                    return seat, None, auto
                except Exception as e:
                    return seat, str(e), False

            with ThreadPoolExecutor(max_workers=max(1, len(items))) as pool:
                futs = [pool.submit(_one, s, tr) for s, tr in items]
                for fut in as_completed(futs):
                    seat, err, auto = fut.result()
                    if err is None:
                        confirmed.append(seat)
                        auto_flags[seat] = auto
                        if on_progress:
                            try:
                                left = sorted(set(seats) - set(confirmed))
                                on_progress(
                                    f"已确认 {sorted(confirmed)}；等待 {left or '—'}"
                                )
                            except Exception:
                                pass
                    else:
                        errors.append(f"S{seat}: {err}")
        finally:
            self._ready_wait_active = False

        confirmed = sorted(confirmed)
        if errors or set(confirmed) != set(seats):
            self.last_ready_all_auto = False
            raise RuntimeError(
                "ready confirm incomplete: "
                f"ok={confirmed} errors={errors}"
            )
        # All seats confirmed AND every reply was auto-start
        self.last_ready_all_auto = bool(confirmed) and all(
            auto_flags.get(s, False) for s in confirmed
        )
        print(
            f"[seat-hub] ready complete all_auto={self.last_ready_all_auto} "
            f"flags={auto_flags}"
        )
        if on_progress:
            try:
                on_progress(f"全部确认 {confirmed}，开局中…")
            except Exception:
                pass
        return confirmed

    def shutdown(self) -> None:
        with self._lock:
            items = list(self.transports.items())
            self.transports.clear()
        for seat, tr in items:
            try:
                tr.shutdown()
            except Exception:
                pass
            print(f"[seat-hub] shutdown S{seat}")
