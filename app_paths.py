"""
Project / resource path resolution for dev and frozen builds.

Supports:
  - Development: repo root (directory containing main.py / assets / configs)
  - PyInstaller: sys._MEIPASS (onefile extract) or onedir bundle
  - Nuitka: executable directory / __compiled__ layout
  - Writable runtime data (logs/) always under user-writable base
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def is_frozen() -> bool:
    """True when running as a packaged binary (PyInstaller / Nuitka / etc.)."""
    if getattr(sys, "frozen", False):
        return True
    if hasattr(sys, "_MEIPASS"):
        return True
    # Nuitka marks compiled modules with __compiled__
    main = sys.modules.get("__main__")
    if main is not None and getattr(main, "__compiled__", None) is not None:
        return True
    # This module itself compiled by Nuitka
    if globals().get("__compiled__", None) is not None:
        return True
    return False


def _meipass() -> Path | None:
    mp = getattr(sys, "_MEIPASS", None)
    if mp:
        return Path(mp)
    return None


def resource_root() -> Path:
    """
    Read-only resources root (assets/, configs/ live here).

    Dev: repository root.
    Frozen: PyInstaller _MEIPASS or directory of the executable / Contents/Resources.
    """
    env = os.environ.get("CHENGDU_MAHJONG_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        if p.is_dir():
            return p

    mp = _meipass()
    if mp is not None:
        return mp.resolve()

    if getattr(sys, "frozen", False) or is_frozen():
        exe = Path(sys.executable).resolve()
        # macOS .app: .../Foo.app/Contents/MacOS/Foo
        # Prefer Contents/Resources if present (some packagers put data there)
        if exe.parent.name == "MacOS" and exe.parent.parent.name == "Contents":
            resources = exe.parent.parent / "Resources"
            if (resources / "assets").is_dir() or (resources / "configs").is_dir():
                return resources
            # PyInstaller 6 onedir often uses Contents/Frameworks or _internal next to exe
            internal = exe.parent / "_internal"
            if (internal / "assets").is_dir():
                return internal
        # Nuitka / onedir: data next to binary or in sibling folder
        here = exe.parent
        if (here / "assets").is_dir():
            return here
        internal = here / "_internal"
        if (internal / "assets").is_dir():
            return internal
        return here

    # Development: this file lives at repo root
    return Path(__file__).resolve().parent


def project_root() -> Path:
    """Alias of resource_root for code that historically used 'project root'."""
    return resource_root()


def assets_dir() -> Path:
    return resource_root() / "assets"


def configs_dir() -> Path:
    return resource_root() / "configs"


def runtime_base() -> Path:
    """
    Writable base for logs/, saves/, crash files.

    Frozen apps often cannot write inside the .app bundle — use
    ~/Library/Application Support/ChengduMahjongAITrainer on macOS.
    """
    env = os.environ.get("CHENGDU_MAHJONG_DATA")
    if env:
        p = Path(env).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        return p

    if is_frozen() or getattr(sys, "frozen", False) or _meipass() is not None:
        if sys.platform == "darwin":
            base = (
                Path.home()
                / "Library"
                / "Application Support"
                / "ChengduMahjongAITrainer"
            )
        elif sys.platform == "win32":
            appdata = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
            base = Path(appdata) / "ChengduMahjongAITrainer"
        else:
            base = Path.home() / ".local" / "share" / "ChengduMahjongAITrainer"
        base.mkdir(parents=True, exist_ok=True)
        return base

    # Dev: repo root
    return Path(__file__).resolve().parent


def logs_dir() -> Path:
    d = runtime_base() / "logs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def saves_dir() -> Path:
    d = runtime_base() / "saves"
    d.mkdir(parents=True, exist_ok=True)
    return d


def seat_window_command(
    *,
    seat: int,
    theme: str = "green",
    extra_args: list[str] | None = None,
    python_exe: str | None = None,
    module: str = "players.seat_window",
) -> list[str]:
    """
    Build argv to spawn a seat window process.

    Frozen: re-exec the same binary with --seat-window ...
    Dev: python -m players.seat_window ...
    """
    extra = list(extra_args or [])
    if is_frozen() or getattr(sys, "frozen", False) or _meipass() is not None:
        exe = python_exe or sys.executable
        return [
            exe,
            "--seat-window",
            "--seat",
            str(seat),
            "--theme",
            theme,
            *extra,
        ]
    exe = python_exe or sys.executable
    return [
        exe,
        "-u",
        "-m",
        module,
        "--seat",
        str(seat),
        "--theme",
        theme,
        *extra,
    ]
