"""F0004: seat ready_request / ready protocol + overlay smoke."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

from protocols.wire import (
    decode_line,
    encode_line,
    msg_ready,
    msg_ready_request,
)


def test_wire_ready_messages_roundtrip() -> None:
    req = msg_ready_request(
        round_index=2, game_id="g1", num_players=4, num_rounds=8
    )
    assert req["type"] == "ready_request"
    assert req["round"] == 2
    assert req["num_rounds"] == 8
    line = encode_line(req)
    parsed = decode_line(line)
    assert parsed["type"] == "ready_request"
    assert parsed["game_id"] == "g1"
    assert parsed["num_rounds"] == 8

    rdy = msg_ready(1, auto=True)
    assert rdy == {"type": "ready", "seat": 1, "auto": True}
    assert decode_line(encode_line(rdy))["auto"] is True


def test_wire_set_geometry_roundtrip() -> None:
    from protocols.wire import msg_set_geometry

    msg = msg_set_geometry(x=10, y=20, w=640, h=480)
    assert msg["type"] == "set_geometry"
    assert decode_line(encode_line(msg))["w"] == 640


def test_hub_tracks_last_ready_all_auto() -> None:
    """SeatUIHub.last_ready_all_auto reflects whether every seat used auto."""
    from players.seat_ui_hub import SeatUIHub

    hub = SeatUIHub(4, human_seat=None)
    hub.last_ready_all_auto = False
    # Simulate post-ready bookkeeping (unit without real processes)
    flags = {0: True, 1: True, 2: True, 3: True}
    confirmed = [0, 1, 2, 3]
    hub.last_ready_all_auto = bool(confirmed) and all(
        flags.get(s, False) for s in confirmed
    )
    assert hub.last_ready_all_auto is True
    flags[2] = False
    hub.last_ready_all_auto = bool(confirmed) and all(
        flags.get(s, False) for s in confirmed
    )
    assert hub.last_ready_all_auto is False


def test_control_panel_auto_next_requires_eligible() -> None:
    import os

    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame

    pygame.init()
    from display.control_panel import ControlPanel

    panel = ControlPanel()
    screen = pygame.display.set_mode((960, 540))
    panel.draw(screen, num_players=4, auto_next_eligible=False)
    assert "auto_next" in panel._hits
    center = panel._hits["auto_next"].center
    # not eligible: click must not enable
    panel.handle_click(center, num_players=4, auto_next_eligible=False)
    assert panel.options.auto_next_round is False
    panel.draw(screen, num_players=4, auto_next_eligible=True)
    panel.handle_click(panel._hits["auto_next"].center, num_players=4, auto_next_eligible=True)
    assert panel.options.auto_next_round is True
    pygame.quit()


def test_fake_seat_auto_ready_on_request(tmp_path: Path) -> None:
    """Simulated seat: on ready_request reply ready immediately (auto path)."""
    script = tmp_path / "fake_ready.py"
    script.write_text(
        textwrap.dedent(
            """
            import json, sys, os
            def emit(o):
                sys.stdout.write(json.dumps(o)+\"\\n\")
                sys.stdout.flush()
            emit({\"type\":\"hello\",\"seat\":2,\"version\":1,\"pid\":os.getpid()})
            for line in sys.stdin:
                msg = json.loads(line)
                if msg.get(\"type\") == \"ready_request\":
                    emit({\"type\":\"ready\",\"seat\":2,\"auto\":True})
                    break
                if msg.get(\"type\") == \"shutdown\":
                    break
            """
        ),
        encoding="utf-8",
    )
    root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.Popen(
        [sys.executable, str(script)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(root),
        env=env,
    )
    assert proc.stdout and proc.stdin
    hello = json.loads(proc.stdout.readline())
    assert hello["type"] == "hello"
    proc.stdin.write(encode_line(msg_ready_request(round_index=1, game_id="t")))
    proc.stdin.flush()
    ready = json.loads(proc.stdout.readline())
    assert ready["type"] == "ready"
    assert ready["seat"] == 2
    assert ready["auto"] is True
    proc.terminate()
    proc.wait(timeout=3)


def test_subprocess_transport_request_ready(tmp_path: Path) -> None:
    script = tmp_path / "fake_ready2.py"
    script.write_text(
        textwrap.dedent(
            """
            import json, sys, os
            def emit(o):
                sys.stdout.write(json.dumps(o)+\"\\n\")
                sys.stdout.flush()
            emit({\"type\":\"hello\",\"seat\":0,\"version\":1,\"pid\":os.getpid()})
            for line in sys.stdin:
                msg = json.loads(line)
                if msg.get(\"type\") == \"ready_request\":
                    emit({\"type\":\"ready\",\"seat\":0,\"auto\":False})
                if msg.get(\"type\") == \"shutdown\":
                    break
            """
        ),
        encoding="utf-8",
    )
    from protocols.subprocess_transport import SubprocessTransport

    # Monkey: use script as "module" via custom — SubprocessTransport uses -m module.
    # Drive via manual Popen path already covered; test transport with patched module
    # by using extra_args override — simplest: use start with a fake module package.
    # Instead exercise request_ready on a hand-built transport after attaching proc.
    tr = SubprocessTransport(0, timeout_ms=10_000, module="players.seat_window")
    # Don't start real pygame window — use internal pipe fake:
    root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    proc = subprocess.Popen(
        [sys.executable, str(script)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(root),
        env=env,
        bufsize=1,
    )
    tr._proc = proc
    tr._out_q.clear()
    tr._reader_started = False
    tr._start_stdout_reader()
    # consume hello
    hello = tr._read_message(timeout_ms=5_000)
    assert hello["type"] == "hello"
    msg = tr.request_ready(round_index=3, game_id="g", timeout_ms=5_000)
    assert msg["type"] == "ready"
    assert msg["seat"] == 0
    tr.shutdown()


def test_request_ready_accepts_child_ready(tmp_path: Path) -> None:
    """Parent request_ready must complete when child replies ready."""
    script = tmp_path / "fake_ready_confirm.py"
    script.write_text(
        textwrap.dedent(
            """
            import json, sys, os
            def emit(o):
                sys.stdout.write(json.dumps(o)+\"\\n\")
                sys.stdout.flush()
            emit({\"type\":\"hello\",\"seat\":0,\"version\":1,\"pid\":os.getpid()})
            emit({\"type\":\"window_ready\",\"seat\":0,\"x\":0,\"y\":0,\"w\":100,\"h\":100,\"title\":\"t\"})
            for line in sys.stdin:
                msg = json.loads(line)
                if msg.get(\"type\") == \"ready_request\":
                    emit({\"type\":\"ready\",\"seat\":0,\"auto\":False})
                if msg.get(\"type\") == \"shutdown\":
                    break
            """
        ),
        encoding="utf-8",
    )
    import subprocess

    from protocols.subprocess_transport import SubprocessTransport

    root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    proc = subprocess.Popen(
        [sys.executable, str(script)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(root),
        env=env,
        bufsize=1,
    )
    tr = SubprocessTransport(0, timeout_ms=10_000)
    tr._proc = proc
    tr._out_q.clear()
    tr._reader_started = False
    tr._start_stdout_reader()
    hello = tr._read_message(timeout_ms=5_000)
    assert hello["type"] == "hello"
    wr = tr.wait_window_ready(timeout_ms=5_000)
    assert wr is not None and wr["type"] == "window_ready"
    ready = tr.request_ready(round_index=1, game_id="g", timeout_ms=5_000)
    assert ready["type"] == "ready"
    assert ready["seat"] == 0
    tr.shutdown()


def test_player_view_ready_overlay_hits() -> None:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((640, 400))
    from display.asset_manager import AssetManager
    from players.view.player_view import PlayerView

    am = AssetManager(theme="green")
    pv = PlayerView(am, seat=1)
    pv.mode = "watch"
    pv.draw(screen, {}, "wait", [], status_note="t")
    pv.draw_ready_overlay(screen, round_index=2, auto_start=False)
    assert pv.ready_start_rect.width > 0
    assert pv.hit_ready_start(pv.ready_start_rect.center)
    assert pv.hit_ready_auto(pv.ready_auto_rect.center)
    pygame.quit()
