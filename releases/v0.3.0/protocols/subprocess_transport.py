"""Subprocess transport for human players (stdin/stdout NDJSON)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from collections import deque
from pathlib import Path
from collections.abc import Callable
from typing import TextIO

from protocols.messages import ActionRequest, Decision, Observation
from protocols.wire import (
    PROTOCOL_VERSION,
    decode_line,
    encode_line,
    msg_action_request,
    msg_game_end,
    msg_observation,
    msg_ready_request,
    msg_set_geometry,
    msg_shutdown,
    parse_decision,
)


class HumanTimeoutError(TimeoutError):
    """Human subprocess did not answer in time."""


class HumanProcessError(RuntimeError):
    """Human subprocess failed or exited unexpectedly."""


class SubprocessTransport:
    def __init__(
        self,
        seat: int,
        *,
        theme: str = "green",
        timeout_ms: int = 120_000,
        python_exe: str | None = None,
        extra_args: list[str] | None = None,
        module: str = "players.seat_window",
    ) -> None:
        self.seat = seat
        self.theme = theme
        self.timeout_ms = timeout_ms
        self.python_exe = python_exe or sys.executable
        self.extra_args = extra_args or []
        self.module = module
        self._proc: subprocess.Popen[str] | None = None
        self._lock = threading.Lock()
        self._out_q: deque[str] = deque()
        self._out_lock = threading.Lock()
        self._reader_started = False
        self._err_chunks: list[str] = []
        self._stderr_path: Path | None = None

    @property
    def proc(self) -> subprocess.Popen[str]:
        if self._proc is None:
            raise HumanProcessError("subprocess not started")
        return self._proc

    def _start_stdout_reader(self) -> None:
        if self._reader_started or self._proc is None or self._proc.stdout is None:
            return
        self._reader_started = True
        stream = self._proc.stdout

        def _bg_out() -> None:
            try:
                for line in stream:
                    with self._out_lock:
                        self._out_q.append(line)
            except Exception:
                pass

        threading.Thread(
            target=_bg_out, daemon=True, name=f"human-stdout-{self.seat}"
        ).start()

    def _dead_detail(self, code: int | None) -> str:
        err = "".join(self._err_chunks)[-1500:]
        if not err and self._stderr_path and self._stderr_path.is_file():
            try:
                err = self._stderr_path.read_text(encoding="utf-8", errors="replace")[
                    -1500:
                ]
            except Exception:
                pass
        # Also peek common crash log from seat_window
        try:
            from app_paths import logs_dir

            log_base = logs_dir()
        except Exception:
            log_base = Path(__file__).resolve().parent.parent / "logs"
        for mode in ("play", "watch"):
            crash = log_base / f"seat_{mode}_{self.seat}_crash.log"
            if crash.is_file():
                try:
                    err = (err + "\n" + crash.read_text(encoding="utf-8", errors="replace"))[
                        -2000:
                    ]
                except Exception:
                    pass
                break
        err = err.strip() or "(no stderr — see logs/seat_*_crash.log)"
        return f"human process died code={code}: {err[:800]}"

    def start(self) -> dict:
        """Spawn seat_window module (or frozen --seat-window); wait for hello."""
        try:
            from app_paths import logs_dir, project_root, seat_window_command

            root = str(project_root())
            log_dir = logs_dir()
            cmd = seat_window_command(
                seat=self.seat,
                theme=self.theme,
                extra_args=list(self.extra_args),
                python_exe=self.python_exe,
                module=self.module,
            )
        except Exception:
            root = str(Path(__file__).resolve().parent.parent)
            log_dir = Path(root) / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            cmd = [
                self.python_exe,
                "-u",  # unbuffered stdio — critical on Windows pipes
                "-m",
                self.module,
                "--seat",
                str(self.seat),
                "--theme",
                self.theme,
                *self.extra_args,
            ]
        env = os.environ.copy()
        env["PYTHONPATH"] = root + os.pathsep + env.get("PYTHONPATH", "")
        env["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUNBUFFERED"] = "1"
        env["CHENGDU_MAHJONG_ROOT"] = root
        # Critical: do NOT inherit parent's SDL_VIDEO_WINDOW_POS (main window pos).
        # Multiple children fighting the same env var / video init causes missing seats.
        env.pop("SDL_VIDEO_WINDOW_POS", None)
        env.pop("SDL_VIDEO_CENTERED", None)
        env["SDL_AUDIODRIVER"] = "dummy"
        # Prefer GDI-ish path when available — fewer multi-process GPU races (Windows)
        if sys.platform == "win32":
            env["SDL_VIDEODRIVER"] = "windows"
            env["SDL_RENDER_DRIVER"] = "software"
        log_dir.mkdir(parents=True, exist_ok=True)
        self._stderr_path = log_dir / f"human_seat{self.seat}_stderr.log"
        err_fp = self._stderr_path.open("w", encoding="utf-8", errors="replace")
        # F0005: utf-8 pipes on Windows code pages; creationflags only on win32
        popen_kwargs: dict = {
            "args": cmd,
            "stdin": subprocess.PIPE,
            "stdout": subprocess.PIPE,
            "stderr": err_fp,
            "text": True,
            "encoding": "utf-8",
            "errors": "replace",
            "bufsize": 1,
            "cwd": root,
            "env": env,
        }
        # Note: do NOT use CREATE_NEW_PROCESS_GROUP on Windows — it has been
        # associated with broken stdout pipes (OSError 22 on child flush).
        # Pass the Windows-only kwarg explicitly with neutral semantics; omitting
        # it on macOS/Linux is required because POSIX Popen rejects creationflags.
        if sys.platform == "win32":
            popen_kwargs["creationflags"] = 0
        self._proc = subprocess.Popen(**popen_kwargs)

        self._out_q.clear()
        self._err_chunks.clear()
        self._reader_started = False
        self._start_stdout_reader()
        # Also tail the stderr file in background for live errors
        def _tail_err() -> None:
            try:
                with self._stderr_path.open("r", encoding="utf-8", errors="replace") as f:
                    while self._proc is not None and self._proc.poll() is None:
                        line = f.readline()
                        if line:
                            self._err_chunks.append(line)
                        else:
                            time.sleep(0.05)
                    # drain rest
                    rest = f.read()
                    if rest:
                        self._err_chunks.append(rest)
            except Exception:
                pass

        threading.Thread(
            target=_tail_err, daemon=True, name=f"human-errfile-{self.seat}"
        ).start()

        try:
            # Early hello (before child pygame) — keep short so parent UI never freezes long
            hello = self._read_message(timeout_ms=min(self.timeout_ms, 15_000))
        except HumanProcessError:
            raise
        except Exception as e:
            self.shutdown()
            raise HumanProcessError(f"hello failed: {e}; {self._dead_detail(None)}") from e
        if hello.get("type") != "hello":
            self.shutdown()
            raise HumanProcessError(f"expected hello, got {hello}")
        if int(hello.get("seat", -1)) != self.seat:
            self.shutdown()
            raise HumanProcessError(
                f"hello seat mismatch: {hello.get('seat')} != {self.seat}"
            )
        return hello

    def wait_window_ready(self, timeout_ms: int = 12_000) -> dict | None:
        """
        After hello, wait for window_ready from the seat process.
        Returns the message dict, or None on timeout (caller may still PID-place).
        """
        end = time.time() + timeout_ms / 1000.0
        while time.time() < end:
            remaining = max(50, int((end - time.time()) * 1000))
            try:
                msg = self._read_message(timeout_ms=min(remaining, 2000))
            except HumanTimeoutError:
                continue
            except HumanProcessError:
                raise
            if msg.get("type") == "window_ready":
                return msg
            if msg.get("type") == "error":
                raise HumanProcessError(msg.get("message", "window_ready error"))
            # ignore other messages
        return None

    def send_observation(self, obs: Observation) -> None:
        # Non-critical: never block engine on a lagging seat window
        try:
            self._write(msg_observation(obs), critical=False)
        except HumanProcessError:
            pass

    def request_decision(
        self, req: ActionRequest, hints: dict | None = None
    ) -> Decision:
        self._write(msg_action_request(req, hints=hints))
        deadline = self.timeout_ms
        if req.deadline_ms is not None:
            deadline = req.deadline_ms
        while True:
            msg = self._read_message(timeout_ms=deadline)
            if msg.get("type") == "error":
                raise HumanProcessError(msg.get("message", "human error"))
            if msg.get("type") != "decision":
                # ignore stray messages
                continue
            dec = parse_decision(msg)
            if dec.request_id != req.request_id:
                continue
            return dec

    def send_game_end(self, result: dict) -> None:
        try:
            self._write(msg_game_end(result))
        except HumanProcessError:
            pass

    def send_set_geometry(self, x: int, y: int, w: int, h: int) -> None:
        """Ask seat Tk window to move/resize to the planned rect (macOS multi-mon)."""
        try:
            self._write(
                msg_set_geometry(x=int(x), y=int(y), w=int(w), h=int(h)),
                critical=False,
            )
        except HumanProcessError:
            pass

    def request_ready(
        self,
        *,
        round_index: int = 1,
        game_id: str = "",
        num_players: int = 4,
        num_rounds: int = 1,
        timeout_ms: int | None = None,
    ) -> dict:
        """
        Send ready_request and wait for a ready reply from this seat window.
        Ignores stray non-ready messages (e.g. leftover acks).
        """
        # Drain any stale stdout (window_ready leftovers already consumed at spawn)
        pending_settings: list[dict] = []
        while True:
            stale = self.try_pop_message()
            if stale is None:
                break
            # If a ready is already sitting in the queue (user clicked early), accept it
            if stale.get("type") == "ready":
                for s in pending_settings:
                    try:
                        self.requeue_message(s)
                    except Exception:
                        pass
                return stale
            # Preserve seat_settings for hub after ready completes
            if stale.get("type") == "seat_settings":
                pending_settings.append(stale)
                continue

        self._write(
            msg_ready_request(
                round_index=round_index,
                game_id=game_id,
                num_players=num_players,
                num_rounds=num_rounds,
            )
        )
        deadline = self.timeout_ms if timeout_ms is None else int(timeout_ms)
        # Allow long wait while human clicks confirm
        deadline = max(deadline, 60_000)
        end = time.time() + deadline / 1000.0
        try:
            while time.time() < end:
                remaining = max(100, int((end - time.time()) * 1000))
                try:
                    msg = self._read_message(timeout_ms=min(remaining, 5_000))
                except HumanTimeoutError:
                    continue
                except HumanProcessError:
                    raise
                mtype = msg.get("type")
                if mtype == "ready":
                    return msg
                if mtype == "seat_settings":
                    pending_settings.append(msg)
                    continue
                if mtype == "error":
                    raise HumanProcessError(msg.get("message", "ready error"))
                # ignore window_ready / hello / stray
                continue
            raise HumanTimeoutError(
                f"timeout waiting ready seat={self.seat} round={round_index}"
            )
        finally:
            # Re-queue settings so hub.poll_async can apply AI / auto prefs
            for s in pending_settings:
                try:
                    self.requeue_message(s)
                except Exception:
                    pass

    def shutdown(self) -> None:
        if self._proc is None:
            return
        try:
            self._write(msg_shutdown())
        except Exception:
            pass
        try:
            self._proc.terminate()
            self._proc.wait(timeout=3)
        except Exception:
            try:
                self._proc.kill()
            except Exception:
                pass
        self._proc = None

    def _write(self, obj: dict, *, critical: bool = True) -> None:
        """
        Write one NDJSON line to the child.

        Observations are best-effort: if the pipe is full (child not reading,
        e.g. after human hu while UI is busy), drop the message instead of
        blocking the whole blood-battle engine thread.
        """
        with self._lock:
            p = self.proc
            if p.poll() is not None:
                raise HumanProcessError(self._dead_detail(p.returncode))
            assert p.stdin is not None
            line = encode_line(obj)
            try:
                # Prefer non-blocking so a stalled seat window cannot freeze
                # the engine after 血战 hu (child may lag on heavy re-render).
                if not critical:
                    self._set_stdin_nonblocking(p, True)
                p.stdin.write(line)
                p.stdin.flush()
            except BlockingIOError:
                if critical:
                    raise HumanProcessError(
                        f"stdin blocked seat={self.seat}; {self._dead_detail(p.poll())}"
                    )
                # drop observation / non-critical
                return
            except Exception as e:
                code = p.poll()
                if not critical and isinstance(e, (BrokenPipeError, OSError)):
                    return
                raise HumanProcessError(
                    f"write failed ({e}); {self._dead_detail(code)}"
                ) from e
            finally:
                if not critical:
                    try:
                        self._set_stdin_nonblocking(p, False)
                    except Exception:
                        pass

    @staticmethod
    def _set_stdin_nonblocking(proc: subprocess.Popen[str], nonblock: bool) -> None:
        if proc.stdin is None:
            return
        try:
            import fcntl

            fd = proc.stdin.fileno()
            flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            if nonblock:
                fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
            else:
                fcntl.fcntl(fd, fcntl.F_SETFL, flags & ~os.O_NONBLOCK)
        except Exception:
            # Windows or unsupported — leave blocking; critical path still works
            pass

    def _pop_line(self) -> str | None:
        with self._out_lock:
            if self._out_q:
                return self._out_q.popleft()
        return None

    def try_pop_message(self) -> dict | None:
        """Non-blocking: decode one queued stdout line, or None."""
        self._start_stdout_reader()
        while True:
            line = self._pop_line()
            if line is None:
                return None
            if not str(line).strip():
                continue
            try:
                return decode_line(line)
            except (ValueError, json.JSONDecodeError):
                continue

    def requeue_message(self, msg: dict) -> None:
        """Put a decoded message back on the front of the queue."""
        line = encode_line(msg)
        if not line.endswith("\n"):
            line = line + "\n"
        with self._out_lock:
            self._out_q.appendleft(line)

    def _read_message(self, timeout_ms: int) -> dict:
        p = self.proc
        if p.stdout is None:
            raise HumanProcessError("no stdout")
        self._start_stdout_reader()
        deadline = time.time() + timeout_ms / 1000.0
        while time.time() < deadline:
            if p.poll() is not None:
                line = self._pop_line()
                if line is None:
                    raise HumanProcessError(self._dead_detail(p.returncode))
            else:
                line = self._pop_line()
            if line is None:
                time.sleep(0.02)
                continue
            if not line.strip():
                continue
            try:
                return decode_line(line)
            except (ValueError, json.JSONDecodeError):
                continue
        raise HumanTimeoutError(f"timeout waiting human seat={self.seat}")
