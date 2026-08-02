#!/usr/bin/env python3
"""Chengdu Mahjong AI Trainer — CLI entry."""

from __future__ import annotations

import argparse
import os
import sys
import traceback
from pathlib import Path

# Reduce macOS multi-process audio races (pygame mixer + seat children)
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")


def cmd_gui(args: argparse.Namespace) -> None:
    from display.app import run_gui

    run_gui(
        theme=args.theme,
        players=args.players,
        spectator=args.spectator,
        step_ms=args.step_ms,
        auto_start=False,
        game_id=args.game_id,
        enable_exchange=not getattr(args, "no_exchange", False),
        num_rounds=int(getattr(args, "rounds", 1) or 1),
    )


def cmd_play(args: argparse.Namespace) -> None:
    parts = [p.strip() for p in args.players.split(",") if p.strip()]
    has_human = any(p.split(":")[0].strip().lower() == "human" for p in parts)

    crash_cfg = None
    if getattr(args, "crash_policy", None):
        from engine.crash import CrashConfig, CrashPolicy

        crash_cfg = CrashConfig.load()
        crash_cfg.policy = CrashPolicy(args.crash_policy)

    save_dir = getattr(args, "save_dir", None)
    save_every = bool(getattr(args, "save_every_decision", False))

    # Explicit headless (or headless+human without GUI)
    if getattr(args, "headless", False):
        from engine.config import EngineConfig
        from engine.orchestrator import run_players_game

        print("Starting headless engine game...")
        result = run_players_game(
            args.players,
            game_id=args.game_id,
            config=EngineConfig(num_players=len(parts)),
            base_seed=0,
            max_steps=50_000,
            theme=getattr(args, "theme", "green"),
            crash_config=crash_cfg,
            save_dir=save_dir,
            save_every_decision=save_every,
            save_on_end=True if save_dir else True,
        )
        print("Game finished:", result.finished_reason, result.scores)
        if save_dir:
            print("Saved under", save_dir)
        return

    # GUI: AI-only spectate, or main window + human subprocess (3AI+1H)
    from display.app import run_gui

    if has_human:
        print(
            "Starting full UI cover: 设置后点「开始」→ 主程序观战 + 座位窗 "
            f"({args.players})"
        )
    # F0003: always land on lobby cover; click 开始 to start
    run_gui(
        theme=args.theme,
        players=args.players,
        spectator=args.spectator,
        step_ms=args.step_ms,
        auto_start=False,
        game_id=args.game_id,
        enable_exchange=not getattr(args, "no_exchange", False),
        num_rounds=int(getattr(args, "rounds", 1) or 1),
    )


def cmd_train(args: argparse.Namespace) -> None:
    from training.runner import run_random_batch

    summary = run_random_batch(
        args.games,
        log_dir=args.log_dir or "logs/train",
        reward_path=args.reward,
        num_players=args.num_players,
        seed=args.seed,
        player_specs=args.players,
    )
    print(summary)


def cmd_resume(args: argparse.Namespace) -> None:
    from engine.config import EngineConfig
    from engine.orchestrator import PlayerGameRunner
    from engine.persistence import load_game
    from players.registry import create_players

    state, meta = load_game(args.save)
    print(f"Loaded {meta.get('game_id')} phase={state.phase}")
    parts = [p.strip() for p in args.players.split(",") if p.strip()]
    if len(parts) != state.num_players:
        parts = ["rule_ai"] * state.num_players
        print("player count mismatch; using", parts)
    players = create_players(parts, base_seed=1, theme=args.theme)
    cfg = EngineConfig.from_dict(meta.get("engine_config") or state.config or {})
    # Rebuild config with correct player count
    cfg = EngineConfig(
        num_players=state.num_players,
        initial_score=cfg.initial_score,
        exchange_dir=cfg.exchange_dir,
        fan_cap=cfg.fan_cap,
        multi_ron=cfg.multi_ron,
        base_score=cfg.base_score,
        force_discard_dingque=cfg.force_discard_dingque,
    )
    runner = PlayerGameRunner(
        players,
        cfg,
        game_id=state.game_id,
        save_dir=args.save_dir,
        save_on_end=True,
    )
    # Inject loaded state and continue from current phase
    runner.state = state
    join_cfg = cfg.to_dict()
    for i, p in enumerate(players):
        p.on_join(i, join_cfg)
    from engine.session import GameSession
    from engine.blood_battle import do_draw, finalize_game, build_game_result
    from engine.crash import AbortGame

    session = GameSession(state, cfg)
    try:
        steps = 0
        while state.phase != "finished" and steps < args.max_steps:
            steps += 1
            if state.phase in ("dealt", "exchange", "dingque", "ready"):
                # cannot easily resume mid-opening without more work
                if state.phase == "ready":
                    from engine.blood_battle import start_play

                    start_play(state, cfg)
                else:
                    print(f"Cannot resume mid-opening phase={state.phase}; abort")
                    break
            elif state.phase == "draw":
                do_draw(state)
            elif state.phase == "discard":
                seat = state.current_seat
                assert seat is not None
                runner._play_seat_action(state, seat, session)
            elif state.phase == "response":
                for seat in list(state.response_seats or []):
                    if state.phase != "response":
                        break
                    if seat in (state.pending_claims or {}):
                        continue
                    runner._play_seat_action(state, seat, session)
            else:
                break
    except AbortGame as e:
        state.phase = "finished"
        state.finished_reason = e.reason
        finalize_game(state, cfg)

    if state.phase != "finished":
        state.phase = "finished"
        state.finished_reason = state.finished_reason or "resume_end"
        finalize_game(state, cfg)
    result = build_game_result(state)
    print("Resume finished:", result.finished_reason, result.scores)
    for p in players:
        p.shutdown()


def cmd_spectate(args: argparse.Namespace) -> None:
    from engine.replay import ReplaySession

    path = Path(args.save)
    replay = ReplaySession(path)
    print(f"Replay frames: {len(replay)} from {path}")
    if args.frame is not None:
        st = replay.frame(args.frame)
        print(
            f"frame {args.frame}: phase={st.phase} wall={len(st.wall)} "
            f"scores={[p.score for p in st.players]}"
        )
        return
    # print summary of all frames (compact)
    for i in range(len(replay)):
        st = replay.frame(i)
        print(
            f"[{i}] phase={st.phase} turn={st.turn_index} "
            f"wall={len(st.wall)} scores={[p.score for p in st.players]}"
        )
        if args.limit and i + 1 >= args.limit:
            break


def cmd_save_info(args: argparse.Namespace) -> None:
    from engine.persistence import load_game

    state, meta = load_game(args.save)
    print("game_id:", meta.get("game_id"))
    print("saved_at:", meta.get("saved_at"))
    print("phase:", state.phase)
    print("players:", state.num_players)
    print("crash_log entries:", len(meta.get("crash_log") or []))


def build_parser() -> argparse.ArgumentParser:
    try:
        from version import APP_DISPLAY, APP_VERSION
    except Exception:
        APP_VERSION = "0.0.0-dev"
        APP_DISPLAY = "Chengdu Mahjong AI Trainer"

    p = argparse.ArgumentParser(
        description=f"Chengdu Mahjong AI Trainer ({APP_DISPLAY})",
    )
    p.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {APP_VERSION}",
    )
    sub = p.add_subparsers(dest="command")

    g = sub.add_parser("gui", help="Open graphical lobby")
    g.add_argument("--theme", default="green", choices=["green", "blue"])
    g.add_argument(
        "--players",
        default="rule_ai,rule_ai,rule_ai,rule_ai",
        help="Comma-separated player types",
    )
    g.add_argument("--spectator", default="full", choices=["full", "public"])
    g.add_argument("--step-ms", type=int, default=200)
    g.add_argument("--game-id", default=None)
    g.add_argument("--rounds", type=int, default=1, help="Session round count")
    g.add_argument(
        "--no-exchange",
        action="store_true",
        help="Disable 换三张 (go straight to dingque)",
    )
    g.set_defaults(func=cmd_gui)

    pl = sub.add_parser(
        "play",
        help="AI spectate GUI, or human/headless if players includes human",
    )
    pl.add_argument("--theme", default="green", choices=["green", "blue"])
    pl.add_argument(
        "--players",
        default="rule_ai,rule_ai,rule_ai,rule_ai",
        help="e.g. human,rule_ai,rule_ai,rule_ai",
    )
    pl.add_argument("--spectator", default="full", choices=["full", "public"])
    pl.add_argument("--step-ms", type=int, default=200)
    pl.add_argument("--game-id", default=None)
    pl.add_argument("--rounds", type=int, default=1, help="Session round count")
    pl.add_argument(
        "--no-exchange",
        action="store_true",
        help="Disable 换三张",
    )
    pl.add_argument("--headless", action="store_true", help="Force headless engine run")
    pl.add_argument("--save-dir", default=None, help="Directory for end-of-game saves")
    pl.add_argument(
        "--save-every-decision",
        action="store_true",
        help="Write steps JSONL snapshots each decision",
    )
    pl.add_argument(
        "--crash-policy",
        default=None,
        choices=["abort_restart", "replace_player", "force_pass"],
    )
    pl.set_defaults(func=cmd_play)

    hu = sub.add_parser("human", help="Alias: human vs AI (opens cover, click Start)")
    hu.add_argument("--theme", default="green", choices=["green", "blue"])
    hu.add_argument("--players", default="human,rule_ai,rule_ai,rule_ai")
    hu.add_argument("--game-id", default=None)
    hu.add_argument("--spectator", default="full", choices=["full", "public"])
    hu.add_argument("--step-ms", type=int, default=200)
    hu.add_argument("--rounds", type=int, default=1)
    hu.add_argument("--no-exchange", action="store_true")
    hu.add_argument("--save-dir", default=None)
    hu.add_argument("--save-every-decision", action="store_true")
    hu.add_argument(
        "--crash-policy",
        default=None,
        choices=["abort_restart", "replace_player", "force_pass"],
    )
    hu.set_defaults(func=cmd_play)

    t = sub.add_parser("train", help="Headless batch simulation")
    t.add_argument("--games", type=int, default=10)
    t.add_argument("--log-dir", default=None)
    t.add_argument("--seed", type=int, default=0)
    t.add_argument("--num-players", type=int, default=4)
    t.add_argument("--players", default=None)
    t.add_argument("--reward", default=None)
    t.set_defaults(func=cmd_train)

    r = sub.add_parser("resume", help="Load a save and continue with AI players")
    r.add_argument("--save", required=True, help="Path to .json save")
    r.add_argument(
        "--players",
        default="rule_ai,rule_ai,rule_ai,rule_ai",
    )
    r.add_argument("--theme", default="green")
    r.add_argument("--save-dir", default="saves")
    r.add_argument("--max-steps", type=int, default=20_000)
    r.set_defaults(func=cmd_resume)

    s = sub.add_parser("spectate", help="Replay a save or steps JSONL (text)")
    s.add_argument("--save", required=True, help="Path to save .json or .steps.jsonl")
    s.add_argument("--frame", type=int, default=None)
    s.add_argument("--limit", type=int, default=None)
    s.set_defaults(func=cmd_spectate)

    si = sub.add_parser("save-info", help="Print save file metadata")
    si.add_argument("--save", required=True)
    si.set_defaults(func=cmd_save_info)

    return p


def _run_seat_window(argv: list[str]) -> int:
    """Frozen / packaging entry: same binary as seat Tk window."""
    from players.seat_window import main as seat_main

    # Drop leading --seat-window flag; remainder matches seat_window CLI
    rest = list(argv)
    if rest and rest[0] == "--seat-window":
        rest = rest[1:]
    return int(seat_main(rest) or 0)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # Packaged multi-process: re-exec of this binary with --seat-window
    if argv and argv[0] == "--seat-window":
        return _run_seat_window(argv)
    parser = build_parser()
    if not argv:
        argv = ["gui"]
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    try:
        args.func(args)
    except SystemExit:
        raise
    except BaseException as e:  # noqa: BLE001 — log unexpected GUI/engine crashes
        try:
            from app_paths import logs_dir

            log_dir = logs_dir()
        except Exception:
            log_dir = Path(__file__).resolve().parent / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
        crash_path = log_dir / "main_crash.log"
        tb = traceback.format_exc()
        try:
            crash_path.write_text(tb, encoding="utf-8")
        except Exception:
            pass
        print(f"[main] unexpected error: {e}\n{tb}", file=sys.stderr)
        print(f"[main] crash log: {crash_path}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    try:
        import faulthandler

        faulthandler.enable()
    except Exception:
        pass
    raise SystemExit(main())
