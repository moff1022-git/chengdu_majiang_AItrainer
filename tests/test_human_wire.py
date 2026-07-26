"""M09 — human wire protocol and mock subprocess tests."""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from engine.action import Action, ActionType
from engine.tile import Suit, Tile
from players.registry import PLAYER_REGISTRY, create_player, create_players
from protocols.messages import ActionRequest, Decision, Observation
from protocols.wire import (
    decode_line,
    encode_line,
    msg_decision,
    msg_hello,
    msg_observation,
    parse_decision,
    parse_observation,
)


def test_h01_wire_decision_roundtrip() -> None:
    dec = Decision(
        request_id="abc123",
        action=Action(ActionType.PASS),
        reason="human:click",
    )
    line = encode_line(msg_decision(dec))
    data = decode_line(line)
    back = parse_decision(data)
    assert back.request_id == "abc123"
    assert back.action.type == ActionType.PASS
    assert back.reason == "human:click"


def test_h01b_observation_roundtrip() -> None:
    obs = Observation(
        game_id="g1",
        self_seat=0,
        phase="discard",
        view={"wall_remaining": 55, "players": []},
    )
    data = decode_line(encode_line(msg_observation(obs)))
    back = parse_observation(data)
    assert back.game_id == "g1"
    assert back.self_seat == 0
    assert back.view["wall_remaining"] == 55


def test_h05_registry_human() -> None:
    assert "human" in PLAYER_REGISTRY
    with pytest.raises(ValueError, match="at most one human"):
        create_players("human,human,rule_ai,rule_ai")


def test_h04_fake_human_script(tmp_path: Path) -> None:
    """Spawn a fake human that hellos and always PASS on request."""
    script = tmp_path / "fake_human.py"
    script.write_text(
        textwrap.dedent(
            """
            import json, sys, os
            def emit(o):
                sys.stdout.write(json.dumps(o) + "\\n")
                sys.stdout.flush()
            emit({"type": "hello", "seat": 0, "version": 1, "pid": os.getpid()})
            for line in sys.stdin:
                msg = json.loads(line)
                if msg.get("type") == "shutdown":
                    break
                if msg.get("type") == "action_request":
                    rid = msg["request_id"]
                    # prefer PASS if present else first legal
                    legal = msg.get("legal_actions") or []
                    action = {"type": "pass"}
                    for a in legal:
                        if a.get("type") == "pass":
                            action = a
                            break
                        action = a
                    emit({
                        "type": "decision",
                        "request_id": rid,
                        "action": action,
                        "reason": "fake:pass",
                    })
            """
        ),
        encoding="utf-8",
    )

    from protocols.subprocess_transport import SubprocessTransport
    from protocols.wire import msg_action_request
    from protocols.messages import ActionRequest

    # Monkeypatch start command by using custom python -c via extra
    transport = SubprocessTransport(0, timeout_ms=10_000)
    # manually start with fake script
    import os
    import subprocess as sp

    root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    transport._proc = sp.Popen(
        [sys.executable, str(script)],
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        text=True,
        bufsize=1,
        cwd=str(root),
        env=env,
    )
    transport._out_q.clear()
    transport._reader_started = False
    transport._start_stdout_reader()
    hello = transport._read_message(timeout_ms=10_000)
    assert hello["type"] == "hello"
    req = ActionRequest.create(
        0,
        "response",
        [Action(ActionType.PASS), Action(ActionType.PONG, tiles=(Tile(Suit.WAN, 1),))],
    )
    dec = transport.request_decision(req)
    assert dec.request_id == req.request_id
    assert dec.action.type == ActionType.PASS
    transport.shutdown()


def test_h06_read_skips_non_json_noise(tmp_path: Path) -> None:
    """stdout noise (e.g. pygame banner) must not break hello handshake."""
    script = tmp_path / "noisy_human.py"
    script.write_text(
        textwrap.dedent(
            """
            import json, sys, os
            print("pygame 2.x Hello from the pygame community.", flush=True)
            print("", flush=True)
            sys.stdout.write(json.dumps({
                "type": "hello", "seat": 0, "version": 1, "pid": os.getpid()
            }) + "\\n")
            sys.stdout.flush()
            for line in sys.stdin:
                if json.loads(line).get("type") == "shutdown":
                    break
            """
        ),
        encoding="utf-8",
    )
    import os
    import subprocess as sp

    from protocols.subprocess_transport import SubprocessTransport

    root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    transport = SubprocessTransport(0, timeout_ms=10_000)
    transport._proc = sp.Popen(
        [sys.executable, str(script)],
        stdin=sp.PIPE,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        text=True,
        bufsize=1,
        cwd=str(root),
        env=env,
    )
    transport._out_q.clear()
    transport._reader_started = False
    transport._start_stdout_reader()
    hello = transport._read_message(timeout_ms=10_000)
    assert hello["type"] == "hello"
    assert hello["seat"] == 0
    transport.shutdown()


def test_h02_parse_match_request_id() -> None:
    raw = {
        "type": "decision",
        "request_id": "req9",
        "action": {"type": "discard", "tiles": ["wan_3"]},
        "reason": "human:click",
    }
    dec = parse_decision(raw)
    assert dec.action.tiles[0].id == "wan_3"
