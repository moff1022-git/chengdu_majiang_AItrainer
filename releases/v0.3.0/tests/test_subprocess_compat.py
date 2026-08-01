"""F0005: subprocess transport cross-platform kwargs."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

from protocols.subprocess_transport import SubprocessTransport


def test_popen_uses_utf8_and_platform_creationflags():
    captured: dict = {}

    class FakeProc:
        def __init__(self, **kwargs):
            captured.update(kwargs)
            self.stdout = MagicMock()
            self.stdin = MagicMock()
            self.pid = 4242
            self.returncode = None

        def poll(self):
            return None

    tr = SubprocessTransport(0, theme="green", timeout_ms=1000)

    def fake_read(*_a, **_k):
        return {"type": "hello", "seat": 0, "pid": 4242, "version": 1}

    with patch("protocols.subprocess_transport.subprocess.Popen", FakeProc):
        with patch.object(tr, "_read_message", fake_read):
            with patch.object(tr, "_start_stdout_reader", lambda: None):
                hello = tr.start()
    assert hello["type"] == "hello"
    assert captured.get("encoding") == "utf-8"
    assert captured.get("errors") == "replace"
    assert captured.get("text") is True
    if sys.platform == "win32":
        assert "creationflags" in captured
    else:
        assert "creationflags" not in captured


def test_popen_omits_windows_creationflags_on_macos():
    captured: dict = {}

    class FakeProc:
        def __init__(self, **kwargs):
            captured.update(kwargs)
            self.stdout = MagicMock()
            self.stdin = MagicMock()
            self.pid = 4242
            self.returncode = None

        def poll(self):
            return None

    tr = SubprocessTransport(0, theme="green", timeout_ms=1000)

    with patch("protocols.subprocess_transport.sys.platform", "darwin"):
        with patch("protocols.subprocess_transport.subprocess.Popen", FakeProc):
            with patch.object(
                tr,
                "_read_message",
                lambda *_a, **_k: {
                    "type": "hello",
                    "seat": 0,
                    "pid": 4242,
                    "version": 1,
                },
            ):
                with patch.object(tr, "_start_stdout_reader", lambda: None):
                    tr.start()

    assert "creationflags" not in captured
    assert captured.get("encoding") == "utf-8"
