"""
Human player subprocess entry (compat).

Delegates to ``players.seat_window`` in ``play`` mode (F0002).

  python -m players.human_player --seat 0 --theme green
"""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # Ensure play mode unless caller already set --mode
    if "--mode" not in argv:
        argv = ["--mode", "play", *argv]
    from players.seat_window import main as seat_main

    return seat_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
