"""app_paths: resource roots and seat-window command (dev mode)."""

from __future__ import annotations

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
