#!/usr/bin/env python3
"""CLI: evaluate F0010 opponent hand prediction and write analysis report.

Usage (fixed bench sets — preferred):
  .venv/bin/python tools/eval_hand_predict.py --set 20
  .venv/bin/python tools/eval_hand_predict.py --set 50
  .venv/bin/python tools/eval_hand_predict.py --set 100

Legacy (ephemeral game ids from --seed):
  .venv/bin/python tools/eval_hand_predict.py --games 20 --seed 42

Analyze only:
  .venv/bin/python tools/eval_hand_predict.py --analyze-dir logs/predict/...
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# repo root on path
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="F0010 hand-predict eval + analysis")
    p.add_argument(
        "--set",
        dest="eval_set",
        type=str,
        default=None,
        choices=["20", "50", "100"],
        help="fixed bench set from configs/f0010_eval_sets.json (20⊂50⊂100)",
    )
    p.add_argument(
        "--set-path",
        type=str,
        default=None,
        help="override path to eval set JSON",
    )
    p.add_argument(
        "--games",
        type=int,
        default=None,
        help="legacy: number of games (ignored if --set is used)",
    )
    p.add_argument(
        "--seed",
        type=int,
        default=0,
        help="legacy: seed for ephemeral game_ids when --set is not used",
    )
    p.add_argument("--log-dir", type=str, default=None)
    p.add_argument(
        "--self-seats",
        type=str,
        default="0",
        help="comma seats to predict from, e.g. 0 or 0,1",
    )
    p.add_argument(
        "--analyze-dir",
        type=str,
        default=None,
        help="only analyze existing JSONL dir (skip simulation)",
    )
    p.add_argument("--no-report", action="store_true")
    p.add_argument(
        "--list-sets",
        action="store_true",
        help="print available fixed sets and exit",
    )
    args = p.parse_args(argv)

    if args.list_sets:
        from players.analysis.predict_eval import list_eval_sets

        print(json.dumps(list_eval_sets(path=args.set_path), indent=2))
        return 0

    if args.analyze_dir:
        from players.analysis.predict_log import (
            analyze_predict_logs,
            write_analysis_report,
        )

        analysis = analyze_predict_logs(args.analyze_dir)
        out = Path(args.analyze_dir) / "ANALYSIS.md"
        if not args.no_report:
            write_analysis_report(analysis, out)
            Path("logs/predict/LATEST_ANALYSIS.md").write_text(
                analysis.to_markdown(), encoding="utf-8"
            )
            Path("docs/status/F0010_predict_accuracy_analysis.md").write_text(
                analysis.to_markdown(), encoding="utf-8"
            )
        print(json.dumps(analysis.to_dict(), ensure_ascii=False, indent=2))
        print(analysis.to_markdown())
        return 0

    from players.analysis.predict_eval import run_predict_eval

    seats = [int(x) for x in args.self_seats.split(",") if x.strip() != ""]
    if args.eval_set is None and args.games is None:
        # default: fixed set 20
        args.eval_set = "20"

    summary, analysis = run_predict_eval(
        args.games if args.games is not None else 0,
        seed=args.seed,
        log_dir=args.log_dir,
        self_seats=seats or [0],
        write_report=not args.no_report,
        eval_set=args.eval_set,
        eval_set_path=args.set_path,
    )
    slim = {k: v for k, v in summary.items() if k not in ("games_meta", "game_ids")}
    slim["game_ids_head"] = (summary.get("game_ids") or [])[:3]
    slim["n_game_ids"] = len(summary.get("game_ids") or [])
    print(json.dumps(slim, indent=2))
    print()
    print(analysis.to_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
