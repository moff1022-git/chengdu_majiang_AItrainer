"""app_paths: resource roots and seat-window command (dev + frozen mock)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import app_paths


def test_resource_root_has_assets_and_configs() -> None:
    root = app_paths.resource_root()
    assert (root / "assets").is_dir()
    assert (root / "configs").is_dir()
    assert (root / "configs" / "fan_table.json").is_file()
    assert app_paths.assets_dir() == root / "assets"
    assert app_paths.configs_dir() == root / "configs"


def test_logs_dir_writable() -> None:
    d = app_paths.logs_dir()
    assert d.is_dir()
    probe = d / ".write_probe"
    probe.write_text("ok", encoding="utf-8")
    probe.unlink(missing_ok=True)


def test_seat_window_command_dev_uses_module() -> None:
    # In tests we are not frozen
    assert app_paths.is_frozen() is False
    cmd = app_paths.seat_window_command(seat=2, theme="blue", extra_args=["--mode", "watch"])
    assert cmd[0] == sys.executable
    assert "-m" in cmd
    assert "players.seat_window" in cmd
    assert "--seat" in cmd and "2" in cmd
    assert "--theme" in cmd and "blue" in cmd
    assert "--mode" in cmd and "watch" in cmd


def test_seat_window_command_frozen_reexec(monkeypatch) -> None:
    """F0025: frozen builds re-exec same binary with --seat-window (no -m)."""
    monkeypatch.setattr(app_paths, "is_frozen", lambda: True)
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    cmd = app_paths.seat_window_command(seat=0, theme="green", extra_args=["--mode", "play"])
    assert cmd[0] == sys.executable
    assert cmd[1] == "--seat-window"
    assert "-m" not in cmd
    assert "players.seat_window" not in cmd
    assert "--seat" in cmd and "0" in cmd


def test_resource_root_meipass(monkeypatch) -> None:
    """PyInstaller onefile/onedir: prefer sys._MEIPASS when assets live there."""
    import tempfile

    # Avoid pytest tmp_path (may hit permission on some Win/OneDrive temps)
    with tempfile.TemporaryDirectory(prefix="f0025_meipass_") as td:
        meipass = Path(td) / "meipass"
        (meipass / "assets").mkdir(parents=True)
        (meipass / "configs").mkdir()
        monkeypatch.setattr(sys, "_MEIPASS", str(meipass), raising=False)
        monkeypatch.delenv("CHENGDU_MAHJONG_ROOT", raising=False)
        assert app_paths.resource_root() == meipass.resolve()


def test_runtime_base_win32_frozen(monkeypatch) -> None:
    """Windows frozen: writable base under CHENGDU_MAHJONG_DATA override."""
    import tempfile

    with tempfile.TemporaryDirectory(prefix="f0025_data_") as td:
        data_root = Path(td) / "ChengduMahjongAITrainer"
        monkeypatch.setenv("CHENGDU_MAHJONG_DATA", str(data_root))
        monkeypatch.setattr(app_paths, "is_frozen", lambda: True)
        monkeypatch.setattr(sys, "frozen", True, raising=False)
        base = app_paths.runtime_base()
        assert base == data_root.resolve()
        assert base.is_dir()


def test_main_seat_window_dispatch(monkeypatch) -> None:
    """main.main routes --seat-window without full GUI."""
    called: list[list[str]] = []

    def fake_seat(argv=None):
        called.append(list(argv or []))
        return 0

    import players.seat_window as sw
    import main as main_mod

    monkeypatch.setattr(sw, "main", fake_seat)
    rc = main_mod.main(["--seat-window", "--seat", "1", "--mode", "watch"])
    assert rc == 0
    assert called
    flat = called[0]
    assert flat[:2] == ["--seat", "1"] or "--seat" in flat
    assert "--seat-window" not in flat
