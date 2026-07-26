#!/usr/bin/env python3
"""
Capture / refresh README feature screenshots into docs/media/readme/.

Primary windows (lobby / main play / result): real pygame offscreen render.
Seat windows (human / AI): prefer OS window grab when Screen Recording is allowed;
otherwise fall back to asset-composed mockups (same tiles/chrome assets as the app).

Usage (repo root):
  .venv/bin/python tools/capture_readme_screenshots.py
  .venv/bin/python tools/capture_readme_screenshots.py --scale 2

Must re-run after UI-affecting releases (see docs/features/F0026_readme_screenshots.md).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "media" / "readme"
MOCK_DIR = ROOT / "docs" / "design" / "window_interiors"

# Fixed filenames consumed by README.md
FILES = {
    "lobby": "01_lobby.png",
    "main": "02_main_play.png",
    "human": "03_human_play.png",
    "ai": "04_ai_watch.png",
    "result": "05_result.png",
}

GAME_ID = "readme-screenshot-fixed"


def _ensure_env() -> None:
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
    # Offscreen-friendly; seat grab needs a real display (separate path).
    if os.environ.get("CHENGDU_SHOT_REAL_DISPLAY", "").strip() not in ("1", "true", "yes"):
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def _app_version() -> str:
    sys.path.insert(0, str(ROOT))
    from version import APP_VERSION

    return APP_VERSION


def _save_surface(screen, path: Path) -> None:
    import pygame

    path.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(screen, str(path))


def capture_main_scenes(*, scale: int = 2, theme: str = "green") -> dict[str, str]:
    """Render lobby / table / result via pygame; return method map."""
    import pygame

    pygame.init()
    from display.asset_manager import AssetManager
    from display.hud_common import FxOverlay
    from display.lobby_view import LobbyView
    from display.result_view import ResultView
    from display.table_view import TableView
    from display.window_geometry import FULL_MAIN_H, FULL_MAIN_W
    from engine.blood_battle import GameResult
    from engine.config import EngineConfig
    from engine.orchestrator import InteractiveRunner
    from players.registry import create_players

    w, h = FULL_MAIN_W * scale, FULL_MAIN_H * scale
    assets = AssetManager(theme=theme)
    methods: dict[str, str] = {}

    # --- Lobby ---
    screen = pygame.Surface((w, h))
    LobbyView(assets).draw(
        screen,
        theme=theme,
        num_players=4,
        players_spec="human,rule_ai,rule_ai,rule_ai",
        spectator="full",
        game_mode="blood_battle",
        enable_exchange=True,
        num_rounds=1,
    )
    _save_surface(screen, OUT_DIR / FILES["lobby"])
    methods["lobby"] = "pygame_offscreen"

    # --- In-game main table ---
    players = create_players("rule_ai,rule_ai,rule_ai,rule_ai")
    runner = InteractiveRunner(
        players, EngineConfig(num_players=4), game_id=GAME_ID
    )
    runner.setup()
    for _ in range(35):
        if runner.result is not None:
            break
        runner.step_once()

    screen = pygame.Surface((w, h))
    tv = TableView(assets, spectator="full", focus_seat=0, show_hud=True)
    tv.resize(w, h)
    tv.draw(screen, runner.state, FxOverlay())
    _save_surface(screen, OUT_DIR / FILES["main"])
    methods["main"] = f"pygame_offscreen(phase={runner.state.phase})"

    # --- Finish hand for result screen ---
    guard = 0
    while runner.result is None and guard < 50_000:
        if runner.step_once():
            break
        guard += 1
    result = runner.result
    if result is None:
        result = GameResult(
            game_id=GAME_ID,
            rankings=[0, 1, 2, 3],
            scores={0: 8, 1: -2, 2: 0, 3: -6},
            hu_sequence=[{"seat": 0, "fan": 2, "zimo": True}],
            finished_reason="last_one",
            wall_remaining=12,
            settle_tags={},
            score_events=[],
        )
        methods["result"] = "pygame_offscreen(synthetic_result)"
    else:
        methods["result"] = f"pygame_offscreen(reason={result.finished_reason})"

    screen = pygame.Surface((w, h))
    ResultView(assets).draw(
        screen,
        result,
        round_index=1,
        num_rounds=1,
        session_scores=result.scores,
    )
    _save_surface(screen, OUT_DIR / FILES["result"])
    return methods


def _try_os_grab_bbox(bbox: tuple[int, int, int, int], path: Path) -> bool:
    """Grab screen region; requires macOS Screen Recording permission."""
    try:
        from PIL import ImageGrab

        img = ImageGrab.grab(bbox=bbox)
        if img is None or min(img.size) < 32:
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path, format="PNG")
        return path.is_file() and path.stat().st_size > 1000
    except Exception:
        return False


def try_capture_seat_windows(*, theme: str = "green") -> dict[str, str]:
    """
    Attempt live Tk seat window captures (needs display + OS permission).
    Returns methods for human/ai keys only when successful.
    """
    if os.environ.get("CHENGDU_SHOT_SKIP_SEAT_GRAB", "").strip() in ("1", "true", "yes"):
        return {}

    methods: dict[str, str] = {}
    try:
        from engine.config import EngineConfig
        from engine.orchestrator import InteractiveRunner
        from players.registry import create_players
        from players.seat_window import TkSeatApp
        from protocols.view_filter import build_observation
        from protocols.wire import msg_observation
        from display.window_geometry import (
            clamp_outer_size,
            plan_for_screen,
            plan_to_matched_client_size,
        )
    except Exception as e:
        print(f"[capture] seat grab imports failed: {e}", file=sys.stderr)
        return {}

    players = create_players("rule_ai,rule_ai,rule_ai,rule_ai")
    runner = InteractiveRunner(
        players, EngineConfig(num_players=4), game_id=GAME_ID + "-seat"
    )
    runner.setup()
    for _ in range(25):
        if runner.result is not None:
            break
        runner.step_once()
    state = runner.state
    plan = plan_for_screen(4)

    def one(mode: str, seat: int, key: str) -> None:
        rect = plan.players.get(seat, plan.main)
        kind = "human" if mode == "play" else "ai"
        ww, hh = clamp_outer_size(rect.w, rect.h, kind=kind)
        ww, hh = plan_to_matched_client_size(ww, hh)
        x, y = 60, 60
        app = TkSeatApp(
            seat=seat,
            mode=mode,
            theme=theme,
            title=f"README {mode} S{seat}",
            x=x,
            y=y,
            w=ww,
            h=hh,
        )
        try:
            app.handle_msg(msg_observation(build_observation(state, seat)))
            for _ in range(40):
                app.root.update()
                time.sleep(0.02)
            app.root.update_idletasks()
            app.root.lift()
            try:
                app.root.attributes("-topmost", True)
            except Exception:
                pass
            app.root.update()
            time.sleep(0.25)
            rx = int(app.root.winfo_rootx())
            ry = int(app.root.winfo_rooty())
            rw = int(app.root.winfo_width())
            rh = int(app.root.winfo_height())
            out = OUT_DIR / FILES[key]
            if _try_os_grab_bbox((rx, ry, rx + rw, ry + rh), out):
                methods[key] = f"os_window_grab({mode})"
        finally:
            try:
                app.root.destroy()
            except Exception:
                pass

    try:
        one("play", 0, "human")
        one("watch", 1, "ai")
    except Exception as e:
        print(f"[capture] seat grab error: {e}", file=sys.stderr)
    return methods


def fallback_seat_mockups() -> dict[str, str]:
    """Use asset-composed mockups when OS grab is unavailable."""
    from PIL import Image

    methods: dict[str, str] = {}
    # Regenerate mockups if generator present
    gen = ROOT / "tools" / "gen_window_mockups_from_assets.py"
    if gen.is_file():
        import runpy

        try:
            runpy.run_path(str(gen), run_name="__mock_gen__")
        except Exception as e:
            print(f"[capture] mockup regen warning: {e}", file=sys.stderr)

    mapping = {
        "human": MOCK_DIR / "HUMAN_mockup_assets_green.jpg",
        "ai": MOCK_DIR / "AI_mockup_assets_green.jpg",
    }
    for key, src in mapping.items():
        if not src.is_file():
            print(f"[capture] missing mockup {src}", file=sys.stderr)
            continue
        img = Image.open(src).convert("RGB")
        # README: keep large but reasonable width
        max_w = 1400
        if img.width > max_w:
            nh = int(round(img.height * (max_w / img.width)))
            img = img.resize((max_w, nh), Image.Resampling.LANCZOS)
        dest = OUT_DIR / FILES[key]
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(dest, format="PNG", optimize=True)
        methods[key] = f"asset_mockup:{src.name}"
    return methods


def write_manifest(methods: dict[str, str], *, scale: int) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    man = {
        "app_version": _app_version(),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "game_id": GAME_ID,
        "scale": scale,
        "files": FILES,
        "methods": methods,
        "note": (
            "Lobby/main/result are live pygame renders. "
            "Human/AI seats use OS grab when permitted; else asset mockups."
        ),
    }
    path = OUT_DIR / "MANIFEST.json"
    path.write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Refresh README screenshots")
    parser.add_argument(
        "--scale",
        type=int,
        default=2,
        choices=[1, 2, 3],
        help="Render scale for main window surfaces (default 2)",
    )
    parser.add_argument("--theme", default="green", choices=["green", "blue"])
    parser.add_argument(
        "--prefer-seat-grab",
        action="store_true",
        help="Try live Tk window grab for human/AI (needs Screen Recording on macOS)",
    )
    args = parser.parse_args(argv)

    os.chdir(ROOT)
    _ensure_env()
    # Seat grab needs non-dummy display interaction; main scenes use dummy.
    if args.prefer_seat_grab:
        os.environ["CHENGDU_SHOT_REAL_DISPLAY"] = "1"
        os.environ.pop("SDL_VIDEODRIVER", None)

    print(f"==> README screenshots → {OUT_DIR} (v{_app_version()})")
    methods: dict[str, str] = {}
    methods.update(capture_main_scenes(scale=args.scale, theme=args.theme))

    seat_m: dict[str, str] = {}
    if args.prefer_seat_grab:
        seat_m = try_capture_seat_windows(theme=args.theme)
    if "human" not in seat_m or "ai" not in seat_m:
        seat_m = {**seat_m, **fallback_seat_mockups()}
    methods.update(seat_m)

    man = write_manifest(methods, scale=args.scale)
    print(f"manifest: {man}")
    for key, name in FILES.items():
        p = OUT_DIR / name
        ok = p.is_file() and p.stat().st_size > 500
        print(f"  [{'OK' if ok else 'MISSING'}] {name}  method={methods.get(key, '?')}")
        if not ok:
            return 1
    print("Done. Commit docs/media/readme/* with README changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
