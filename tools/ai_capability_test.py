"""Standalone, headless and reproducible AI capability benchmark."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import signal
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from statistics import mean, median
from types import MethodType

from engine.config import EngineConfig
from engine.orchestrator import PlayerGameRunner
from players.registry import create_players
from players.humanlike.personality_presets import PRESET_IDS, apply_personality_preset
from players.humanlike.config import load_config
from players.humanlike.player import default_humanlike_config_path

ROOT = Path(__file__).resolve().parents[1]
COUNTS = (100, 200, 500, 1000, 2000, 5000, 10000)
TYPES = ("random", "rule_ai", "rule_ai_plus", "humanlike_v2")
STOP = False
SECONDS_PER_GAME = 4.0
THREAD_OPTIONS = (1, 5, 10, 20, 50, 100)


def progress_bar(completed: int, total: int, *, width: int = 28) -> str:
    """Render a compact ASCII progress bar suitable for terminal refresh."""
    total = max(1, total)
    ratio = min(1.0, max(0.0, completed / total))
    filled = int(width * ratio)
    return f"[{'#' * filled}{'-' * (width - filled)}] {ratio:6.2%}"


def _index(path: Path) -> int:
    try:
        return int(path.stem.rsplit("-", 1)[1])
    except (IndexError, ValueError):
        return 10**12


def game_ids(count: int) -> list[str]:
    """Load the generated fixed IDs, extending the same series if needed."""
    log_dir = ROOT / "data/ai_capability/fixed_game_sets" / f"{count}_games/logs"
    found = [p.stem for p in sorted(log_dir.glob("*.jsonl"), key=_index)]
    used = set(found)
    generated = (f"batch-20260301-{i}" for i in range(count))
    return (found + [gid for gid in generated if gid not in used])[:count]


def verification_code(*, games: int, game_id_list: list[str], players: list[str], mode: str, target: str | None = None) -> str:
    payload = {"games": games, "game_ids": game_id_list, "players": players, "mode": mode, "target": target}
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()[:16].upper()


def _timed_players(specs: list[str], presets: list[str | None] | None = None):
    players = create_players(specs, base_seed=0, humanlike_presets=presets)
    timing = [{"seconds": [], "phases": {}} for _ in specs]
    for seat, player in enumerate(players):
        original = player.decide

        def timed(self, request, *, _original=original, _seat=seat):
            started = time.perf_counter()
            try:
                return _original(request)
            finally:
                elapsed = time.perf_counter() - started
                timing[_seat]["seconds"].append(elapsed)
                timing[_seat]["phases"].setdefault(request.phase, []).append(elapsed)

        player.decide = MethodType(timed, player)
    return players, timing


def run_game(specs: list[str], game_id: str, presets: list[str | None] | None = None) -> dict:
    players, timing = _timed_players(specs, presets)
    started = time.perf_counter()
    result = PlayerGameRunner(players, EngineConfig(num_players=4), game_id=game_id).run()
    row = result.to_dict()
    row["elapsed_seconds"] = time.perf_counter() - started
    row["decision_timing"] = timing
    return row


def _percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int((len(ordered) - 1) * fraction))]


def summarize(rows: list[dict], specs: list[str], requested: int, interrupted: bool, presets=None) -> dict:
    preset_list = list(presets or [None] * len(specs))
    template = load_config(default_humanlike_config_path()).normalized_dict()["players"][0]
    snapshots = []
    for player_type, preset_id in zip(specs, preset_list):
        if player_type != "humanlike_v2" or not preset_id:
            snapshots.append(None); continue
        player = apply_personality_preset(template, preset_id)
        profile = player["profile"]; gp025 = player["cognitive_parameters"]["GP-025"]; gp026 = player["cognitive_parameters"]["GP-026"]
        snapshots.append({"preset_id": preset_id, "profile": {k: profile[k] for k in ("peng_preference", "gang_preference", "big_hand_preference", "defense_awareness", "plan_persistence", "thinking_speed")}, "GP-025": {k: gp025[k] for k in ("emotional_stability", "habit_strength", "max_error_probability", "near_equal_randomness")}, "GP-026": {k: gp026[k] for k in ("min_candidates", "max_candidates", "search_depth", "attention_capacity", "satisfaction_threshold") } | {"decision_weights": dict(gp026["decision_weights"])}})
    seats = []
    for seat, player_type in enumerate(specs):
        scores = [int(row.get("scores", {}).get(str(seat), 0)) for row in rows if row.get("status") != "FAILED"]
        top1 = [row for row in rows if row.get("status") != "FAILED" and seat in row.get("rankings", [])[:1]]
        wins = [row for row in rows if row.get("status") != "FAILED" and any(int(h.get("seat", -1)) == seat for h in row.get("hu_sequence", []))]
        latencies = [x for row in rows for x in row.get("decision_timing", [{"seconds": []}] * 4)[seat]["seconds"]]
        seats.append({
            "seat": f"s{seat}", "player": player_type, "games": len(rows),
            "wins": len(wins), "win_rate": len(wins) / len(rows) if rows else 0.0,
            "top1": len(top1), "top1_rate": len(top1) / len(rows) if rows else 0.0,
            "total_score": sum(scores), "average_score": mean(scores) if scores else 0.0,
            "decisions": len(latencies), "avg_response_ms": mean(latencies) * 1000 if latencies else 0.0,
            "median_response_ms": median(latencies) * 1000 if latencies else 0.0,
            "p95_response_ms": _percentile(latencies, .95) * 1000,
            "p99_response_ms": _percentile(latencies, .99) * 1000,
            "max_response_ms": max(latencies, default=0.0) * 1000,
        })
    return {"requested": requested, "completed": len(rows), "interrupted": interrupted, "players": specs, "presets": preset_list, "preset_parameters": snapshots, "seats": seats}


def write_outputs(out: Path, rows: list[dict], specs: list[str], requested: int, interrupted: bool, code: str | None = None, presets=None, report_stamp: str | None = None) -> None:
    report_stamp = report_stamp or datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    summary = summarize(rows, specs, requested, interrupted, presets)
    if code:
        summary["verification_code"] = code
    summary_text = json.dumps(summary, ensure_ascii=False, indent=2)
    (out / f"summary_{report_stamp}.json").write_text(summary_text, encoding="utf-8")
    (out / "summary.json").write_text(summary_text, encoding="utf-8")
    with (out / "games.jsonl").open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    report_csv = out / f"report_{report_stamp}.csv"
    with report_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary["seats"][0].keys())
        writer.writeheader(); writer.writerows(summary["seats"])
    report_csv_latest = out / "report.csv"
    report_csv_latest.write_text(report_csv.read_text(encoding="utf-8"), encoding="utf-8")
    lines = ["# AI 能力测试报告", "", f"- 请求/完成：{requested}/{len(rows)}", f"- 状态：{'已中断（可续跑）' if interrupted else '已完成'}"]
    if code: lines.append(f"- 唯一校验码：`{code}`")
    lines.append(f"- humanlike_v2 人格预设：`{json.dumps(dict(enumerate(summary['presets'])), ensure_ascii=False)}`")
    lines.append(f"- 人格参数快照：`{json.dumps(dict(enumerate(summary['preset_parameters'])), ensure_ascii=False, sort_keys=True)}`")
    lines += ["", "|座位|AI|胜局/胜率|Top1率|总分/均分|平均/P95响应(ms)|", "|---|---|---:|---:|---:|---:|"]
    for s in summary["seats"]:
        lines.append(f"|{s['seat']}|{s['player']}|{s['wins']} / {s['win_rate']:.2%}|{s['top1_rate']:.2%}|{s['total_score']} / {s['average_score']:.2f}|{s['avg_response_ms']:.3f} / {s['p95_response_ms']:.3f}|")
    report_text = "\n".join(lines) + "\n"
    (out / f"report_{report_stamp}.md").write_text(report_text, encoding="utf-8")
    (out / "report.md").write_text(report_text, encoding="utf-8")


def capability_experiments(target: str) -> list[dict]:
    """Return one experiment per baseline and target seat rotation."""
    baselines = [item for item in TYPES if item != target]
    return [{"baseline": baseline, "seat": seat,
             "players": [target if index == seat else baseline for index in range(4)]}
            for baseline in baselines for seat in range(4)]


def estimate_seconds(games: int, mode: str = "batch", remaining_experiments: int | None = None, threads: int = 1) -> float:
    """Estimate wall time with bounded parallel workers (including scheduler overhead)."""
    experiments = remaining_experiments if remaining_experiments is not None else (12 if mode == "capability" else 1)
    total = games * experiments
    workers = max(1, min(int(threads), total))
    return ((total + workers - 1) // workers) * SECONDS_PER_GAME


def confirm_run(games: int, mode: str, target: str | None = None, threads: int = 1, *, input_fn=input) -> bool:
    experiments = 12 if mode == "capability" else 1
    minutes = estimate_seconds(games, mode, threads=threads) / 60
    label = f"目标 {target}，" if target else ""
    answer = input_fn(f"\n即将开始：{label}{experiments} 个实验，共 {games * experiments} 局；并发线程 {threads}；预计耗时约 {minutes:.1f} 分钟。确认开始？[y/N] ")
    return answer.strip().lower() in {"y", "yes"}


def choose_option(label: str, options: list[str], *, input_fn=input) -> str:
    """Select one value from a numbered menu; never require typing the value."""
    while True:
        print(f"\n{label}")
        for index, option in enumerate(options, 1):
            print(f"  {index}. {option}")
        raw = input_fn("请选择编号: ").strip()
        try:
            selected = int(raw)
            if 1 <= selected <= len(options):
                return options[selected - 1]
        except ValueError:
            pass
        print("输入无效，请输入菜单编号。")


def choose_players(*, input_fn=input) -> str:
    """Choose four seats independently from the AI type menu."""
    return ",".join(choose_option(f"选择 s{seat} AI 类型", list(TYPES), input_fn=input_fn) for seat in range(4))


def choose_batch_configuration(*, input_fn=input) -> tuple[str, list[str | None]]:
    """Choose each seat and its preset together before moving to next seat."""
    specs, presets = [], []
    for seat in range(4):
        player = choose_option(f"选择 s{seat} AI 类型", list(TYPES), input_fn=input_fn)
        specs.append(player)
        presets.append(choose_option(f"选择 s{seat} humanlike_v2 人格预设", list(PRESET_IDS), input_fn=input_fn)
                       if player == "humanlike_v2" else None)
    return ",".join(specs), presets


def choose_batch_presets(specs: list[str], *, input_fn=input) -> list[str | None]:
    """Prompt only for seats using humanlike_v2."""
    return [choose_option(f"选择 s{seat} humanlike_v2 人格预设", list(PRESET_IDS), input_fn=input_fn)
            if player == "humanlike_v2" else None for seat, player in enumerate(specs)]


def run_capability_mode(target: str, games: int, output: Path, presets=None, threads: int = 1) -> int:
    output.mkdir(parents=True, exist_ok=True)
    experiments = capability_experiments(target)
    started_at = datetime.now().astimezone()
    run_stamp = started_at.strftime("%Y%m%d_%H%M%S")
    ids_for_code = game_ids(games)
    code = verification_code(games=games, game_id_list=ids_for_code, players=[target] * 4, mode="capability", target=target)
    preset_id = presets[0] if isinstance(presets, (list, tuple)) else presets
    manifest = {"mode": "capability", "target": target, "humanlike_preset": preset_id, "threads": threads, "games_per_experiment": games,
                "started_at": started_at.isoformat(), "verification_code": code, "report_file": f"capability_report_{run_stamp}.md",
                "experiments": experiments}
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    aggregate = []
    wall_start = time.perf_counter()
    for number, experiment in enumerate(experiments, 1):
        name = f"vs_{experiment['baseline']}_target_s{experiment['seat']}"
        run_dir = output / name
        run_dir.mkdir(parents=True, exist_ok=True)
        config = run_dir / "config.json"
        if not config.exists():
            config.write_text(json.dumps({"games": games, "players": experiment["players"], "game_ids": game_ids(games)}, ensure_ascii=False, indent=2), encoding="utf-8")
        ids = json.loads(config.read_text(encoding="utf-8"))["game_ids"]
        games_file = run_dir / "games.jsonl"
        rows = [json.loads(line) for line in games_file.read_text(encoding="utf-8").splitlines() if line] if games_file.exists() else []
        pending = list(range(len(rows), games))
        exp_presets = [preset_id if (target == "humanlike_v2" and seat == experiment["seat"]) else None for seat in range(4)] if preset_id else None
        def execute(index):
            try:
                return index, run_game(experiment["players"], ids[index], exp_presets)
            except Exception as exc:
                return index, {"game_id": ids[index], "status": "FAILED", "finished_reason": "runner_exception", "error_type": type(exc).__name__, "error": str(exc), "scores": {}, "rankings": [], "hu_sequence": [], "decision_timing": [{"seconds": [], "phases": {}} for _ in range(4)]}
        with ThreadPoolExecutor(max_workers=threads) as pool:
          for index, row in ((execute(i) for i in pending) if threads == 1 else (f.result() for f in as_completed([pool.submit(execute, i) for i in pending]))):
            if STOP: break
            rows.append(row)
            write_outputs(run_dir, rows, experiment["players"], games, True, presets=exp_presets, report_stamp=run_stamp)
            (run_dir / "checkpoint.json").write_text(json.dumps({"next_index": len(rows), "last_game_id": ids[index]}, ensure_ascii=False, indent=2), encoding="utf-8")
            completed_total = (number - 1) * games + len(rows)
            total = len(experiments) * games
            elapsed = time.perf_counter() - wall_start
            rate = elapsed / completed_total if completed_total else 0.0
            eta = rate * (total - completed_total)
            print(f"\r能力评估 {progress_bar(completed_total, total)} 总局数 {completed_total}/{total} 校验码 {code} 实验 {number}/{len(experiments)} {name} 局 {len(rows)}/{games} 已运行 {elapsed:.1f}s 剩余约 {eta:.1f}s", end="", flush=True)
        write_outputs(run_dir, rows, experiment["players"], games, len(rows) < games, presets=presets, report_stamp=run_stamp)
        target_stat = summarize(rows, experiment["players"], games, len(rows) < games)["seats"][experiment["seat"]]
        aggregate.append({"baseline": experiment["baseline"], "target_seat": f"s{experiment['seat']}", **target_stat})
        if STOP: break
    (output / "capability_summary.json").write_text(json.dumps({"target": target, "games_per_experiment": games, "verification_code": code, "completed_experiments": len(aggregate), "results": aggregate}, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# {target} AI 能力评估", "", f"每个基线每个座位：{games} 局", f"唯一校验码：`{code}`", f"人格预设：`{preset_id or '无'}`", f"并发线程数：`{threads}`", "", "|基线|目标座位|人格预设|胜率|Top1率|平均得分|平均响应(ms)|P95响应(ms)|", "|---|---|---|---:|---:|---:|---:|---:|"]
    lines += [f"|{r['baseline']}|{r['target_seat']}|{preset_id or '无'}|{r['win_rate']:.2%}|{r['top1_rate']:.2%}|{r['average_score']:.2f}|{r['avg_response_ms']:.3f}|{r['p95_response_ms']:.3f}|" for r in aggregate]
    report_name = f"capability_report_{run_stamp}.md"
    report_text = "\n".join(lines) + "\n"
    (output / report_name).write_text(report_text, encoding="utf-8")
    # Keep a stable pointer for scripts while the timestamped file is canonical.
    (output / "capability_report.md").write_text(report_text, encoding="utf-8")
    return 130 if STOP else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="成都麻将 AI 无 UI 能力测试")
    parser.add_argument("--games", type=int, choices=COUNTS)
    parser.add_argument("--players", help="s0,s1,s2,s3，例如 random,rule_ai,rule_ai_plus,humanlike_v2")
    parser.add_argument("--output", default="data/ai_capability/results")
    parser.add_argument("--resume", metavar="RUN_DIR")
    parser.add_argument("--mode", choices=("batch", "capability"), default=None)
    parser.add_argument("--target", choices=TYPES, help="capability 模式中的目标 AI")
    parser.add_argument("--threads", type=int, choices=THREAD_OPTIONS, default=None)
    parser.add_argument("--humanlike-preset", choices=PRESET_IDS)
    args = parser.parse_args(argv)
    batch_presets = None
    while True:
        if args.mode is None:
            args.mode = choose_option("测试模式", ["batch", "capability"])
        if args.games is None:
            args.games = int(choose_option("测试局数", [str(item) for item in COUNTS]))
        if args.mode == "capability":
            if args.target is None: args.target = choose_option("目标 AI 类型", list(TYPES))
            if args.target == "humanlike_v2" and args.humanlike_preset is None:
                args.humanlike_preset = choose_option("humanlike_v2 人格预设", list(PRESET_IDS))
        elif args.players is None:
            args.players, batch_presets = choose_batch_configuration()
        if args.threads is None:
            args.threads = int(choose_option("并发线程数", [str(x) for x in THREAD_OPTIONS]))
        if confirm_run(args.games, args.mode, args.target, args.threads): break
        print("已取消，返回参数选择。")
        args.games = None; args.target = None; args.players = None; args.mode = None; args.threads = None; args.humanlike_preset = None; batch_presets = None
    if args.mode == "capability":
        return run_capability_mode(args.target, args.games, Path(args.output) / f"capability_{args.target}_{args.games}", [args.humanlike_preset] * 4 if args.humanlike_preset else None, args.threads)
    specs = [item.strip() for item in args.players.split(",")]
    if len(specs) != 4 or any(item not in TYPES for item in specs):
        parser.error("--players 必须包含四个合法 AI：" + ",".join(TYPES))
    out = Path(args.resume) if args.resume else Path(args.output) / f"{args.games}_{'_'.join(specs)}"
    out.mkdir(parents=True, exist_ok=True)
    config_path = out / "config.json"
    rows = []
    if args.resume:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        args.games, specs = int(config["games"]), list(config["players"])
        games_file = out / "games.jsonl"
        if games_file.exists(): rows = [json.loads(line) for line in games_file.read_text(encoding="utf-8").splitlines() if line]
    else:
        ids = game_ids(args.games)
        code = verification_code(games=args.games, game_id_list=ids, players=specs, mode="batch")
        config_path.write_text(json.dumps({"games": args.games, "players": specs, "presets": batch_presets, "threads": args.threads, "game_ids": ids, "verification_code": code}, ensure_ascii=False, indent=2), encoding="utf-8")
    config_data = json.loads(config_path.read_text(encoding="utf-8"))
    ids = config_data["game_ids"]
    batch_presets = config_data.get("presets", batch_presets or [None] * 4)
    if args.resume:
        args.threads = int(config_data.get("threads", args.threads or 1))
    code = verification_code(games=args.games, game_id_list=ids, players=specs, mode="batch")
    global STOP
    signal.signal(signal.SIGINT, lambda *_: globals().__setitem__("STOP", True))
    wall_start = time.perf_counter()
    report_stamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    pending = list(range(len(rows), args.games))
    def execute_batch(index):
        try:
            return index, run_game(specs, ids[index], batch_presets)
        except Exception as exc:
            return index, {"game_id": ids[index], "status": "FAILED", "finished_reason": "runner_exception", "error_type": type(exc).__name__, "error": str(exc), "scores": {}, "rankings": [], "hu_sequence": [], "decision_timing": [{"seconds": [], "phases": {}} for _ in range(4)]}
    with ThreadPoolExecutor(max_workers=args.threads) as pool:
      futures = [pool.submit(execute_batch, index) for index in pending]
      iterator = (execute_batch(index) for index in pending) if args.threads == 1 else (future.result() for future in as_completed(futures))
      for index, row in iterator:
        if STOP: break
        rows.append(row)
        rows.sort(key=lambda item: ids.index(item.get("game_id", "")))
        elapsed = time.perf_counter() - wall_start
        rate = elapsed / max(1, len(rows) - (index - (len(rows) - 1)))
        eta = rate * (args.games - len(rows))
        write_outputs(out, rows, specs, args.games, True, code, presets=batch_presets, report_stamp=report_stamp)
        (out / "checkpoint.json").write_text(json.dumps({"next_index": len(rows), "last_game_id": ids[index]}, ensure_ascii=False, indent=2), encoding="utf-8")
        score_text = " ".join(f"s{s}:{row.get('scores', {}).get(str(s), 0)}" for s in range(4))
        print(f"\r{progress_bar(len(rows), args.games)} 总局数 {len(rows)}/{args.games} 校验码 {code} {score_text} elapsed={elapsed:.1f}s ETA={eta:.1f}s", end="", flush=True)
    print()
    write_outputs(out, rows, specs, args.games, len(rows) < args.games, code, presets=batch_presets, report_stamp=report_stamp)
    return 130 if STOP else 0


if __name__ == "__main__":
    raise SystemExit(main())
