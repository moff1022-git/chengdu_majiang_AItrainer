"""F0060 fixed-deal serial/process acceptance runner."""
from __future__ import annotations

import argparse
import json
import resource
import time
from pathlib import Path

from tools.ai_capability_test import execute_tasks


def canonical_result(row: dict) -> dict:
    return {key: row.get(key) for key in ("game_id", "scores", "rankings", "hu_sequence", "finished_reason", "wall_remaining", "settle_tags", "score_events")}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--executor", choices=("serial", "process"), required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = Path("data/fairness/fairness-20260802-fair-004/100/deals.jsonl")
    deals = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line]
    specs = ["humanlike_v2"] * 4
    presets = ["nonhuman_optimized", "novice_balanced", "novice_balanced", "novice_balanced"]
    tasks = [(index, specs, deal["game_id"], presets, deal, None) for index, deal in enumerate(deals)]
    started = time.perf_counter()
    rows = [row for _, row in execute_tasks(tasks, executor=args.executor, workers=args.workers)]
    rows.sort(key=lambda row: next(i for i, deal in enumerate(deals) if deal["game_id"] == row["game_id"]))
    usage = resource.getrusage(resource.RUSAGE_SELF)
    child_usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    result = {
        "executor": args.executor, "workers": args.workers, "games": len(rows),
        "failed": sum(row.get("status") == "FAILED" for row in rows),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "self_max_rss_mib": round(usage.ru_maxrss / 1024 / 1024, 3),
        "children_max_rss_mib": round(child_usage.ru_maxrss / 1024 / 1024, 3),
        "results": [canonical_result(row) for row in rows],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "results"}, ensure_ascii=False))
    return 0 if not result["failed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
