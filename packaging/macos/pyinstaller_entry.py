#!/usr/bin/env python3
"""
Unified entry for macOS frozen builds (PyInstaller / Nuitka).

- Default / GUI: delegates to main.main
- Multi-process seats: argv starts with --seat-window → players.seat_window

Usage (dev):
  python packaging/macos/pyinstaller_entry.py gui
  python packaging/macos/pyinstaller_entry.py --seat-window --seat 0 --mode play
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure project root is importable when running from packaging/macos/
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
os.environ.setdefault("PYTHONUNBUFFERED", "1")


def main() -> int:
    try:
        import faulthandler

        faulthandler.enable()
    except Exception:
        pass

    # multiprocessing / spawn safety on some platforms
    try:
        import multiprocessing

        multiprocessing.freeze_support()
    except Exception:
        pass

    from main import main as app_main

    return int(app_main() or 0)


if __name__ == "__main__":
    raise SystemExit(main())
