"""Standalone, headless and reproducible AI capability benchmark."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import multiprocessing
import os
import signal
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
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
EXECUTORS = ("serial", "thread", "process")
DEFAULT_WORKER_MIB = 96


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


def available_test_ids() -> list[str]:
    """Return dataset groups available locally, including the shipped registry.

    Large fairness artifacts are intentionally excluded from Git, so a clean
    checkout may have no ``data/fairness`` manifests.  Keep the canonical
    generated group discoverable in that case; selecting it still fails with
    the normal missing-dataset error until artifacts are provisioned.
    """
    discovered = {
        path.parent.name for path in (ROOT / "data/fairness").glob("*/manifest.json")
    }
    discovered.add("fairness-20260805-blind-001")
    return sorted(discovered)


def load_fixed_dataset(test_id: str, games: int, *, fairness_root: Path | None = None) -> tuple[list[dict], dict]:
    root = (fairness_root or (ROOT / "data/fairness")) / test_id
    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("test_id") != test_id:
        raise ValueError("dataset manifest test_id mismatch")
    dataset = (manifest.get("datasets") or {}).get(str(games))
    flat_games = int(manifest.get("games", -1))
    flat_prefix = False
    if not dataset and 0 < games <= flat_games and manifest.get("artifact") and manifest.get("sha256"):
        dataset = {"artifact": manifest["artifact"], "sha256": manifest["sha256"]}
        flat_prefix = games < flat_games
    if not dataset:
        raise ValueError(f"dataset {test_id} does not provide {games} games")
    artifact = root / dataset["artifact"]
    payload = artifact.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != dataset["sha256"]:
        raise ValueError("dataset SHA-256 mismatch")
    deals = [json.loads(line) for line in payload.decode("utf-8").splitlines() if line]
    if flat_prefix:
        deals = deals[:games]
        prefix_payload = "".join(json.dumps(deal, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for deal in deals).encode("utf-8")
        digest = hashlib.sha256(prefix_payload).hexdigest()
    if len(deals) != games or len({deal["game_id"] for deal in deals}) != games:
        raise ValueError("dataset game count or game_id uniqueness mismatch")
    return deals, {"test_id": test_id, "dataset_games": games, "dataset_sha256": digest, "dataset_artifact": str(artifact)}


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


def run_game(specs: list[str], game_id: str, presets: list[str | None] | None = None, *, trace_dir: Path | None = None) -> dict:
    players, timing = _timed_players(specs, presets)
    started = time.perf_counter()
    result = PlayerGameRunner(players, EngineConfig(num_players=4), game_id=game_id, save_dir=trace_dir, save_every_decision=trace_dir is not None).run()
    row = result.to_dict()
    row["elapsed_seconds"] = time.perf_counter() - started
    row["decision_timing"] = timing
    return row


def failed_game(game_id: str, exc: Exception) -> dict:
    return {"game_id": game_id, "status": "FAILED", "finished_reason": "runner_exception", "error_type": type(exc).__name__, "error": str(exc), "scores": {}, "rankings": [], "hu_sequence": [], "decision_timing": [{"seconds": [], "phases": {}} for _ in range(4)]}


def run_game_task(task: tuple[int, list[str], str, list[str | None] | None, dict | None, str | None]) -> tuple[int, dict]:
    """Spawn-safe game worker; it never writes shared reports/checkpoints."""
    index, specs, game_id, presets, fixed_deal, trace_path = task
    try:
        if trace_path:
            Path(trace_path).mkdir(parents=True, exist_ok=True)
        players, timing = _timed_players(specs, presets)
        started = time.perf_counter()
        result = PlayerGameRunner(
            players, EngineConfig(num_players=4), game_id=game_id,
            fixed_deal=fixed_deal, save_dir=Path(trace_path) if trace_path else None,
            save_every_decision=bool(trace_path),
        ).run()
        row = result.to_dict()
        row["elapsed_seconds"] = time.perf_counter() - started
        row["decision_timing"] = timing
        return index, row
    except Exception as exc:
        return index, failed_game(game_id, exc)


def effective_workers(requested: int, pending: int, memory_budget_mib: int, *, worker_mib: int = DEFAULT_WORKER_MIB) -> tuple[int, str | None]:
    cpu_limit = max(1, os.cpu_count() or 1)
    memory_limit = max(1, int(memory_budget_mib) // max(1, worker_mib))
    actual = max(1, min(int(requested), max(1, pending), cpu_limit, memory_limit))
    reason = None if actual == requested else f"workers由{requested}限制为{actual}（CPU/待运行局数/内存预算）"
    return actual, reason


def execute_tasks(tasks, *, executor: str, workers: int, should_stop=lambda: False):
    """Yield completed `(index, row)` pairs using the selected backend."""
    if executor == "serial" or workers == 1:
        for task in tasks:
            if should_stop(): break
            yield run_game_task(task)
        return
    pool_type = ProcessPoolExecutor if executor == "process" else ThreadPoolExecutor
    kwargs = {"max_workers": workers}
    if executor == "process":
        kwargs["mp_context"] = multiprocessing.get_context("spawn")
    with pool_type(**kwargs) as pool:
        task_iter = iter(tasks)
        futures = set()
        for _ in range(workers):
            if should_stop(): break
            try: futures.add(pool.submit(run_game_task, next(task_iter)))
            except StopIteration: break
        while futures:
            future = next(as_completed(futures))
            futures.remove(future)
            yield future.result()
            if not should_stop():
                try: futures.add(pool.submit(run_game_task, next(task_iter)))
                except StopIteration: pass


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


def trace_integrity(out: Path, rows: list[dict]) -> dict:
    successful = [row["game_id"] for row in rows if row.get("status") != "FAILED"]
    missing = []
    for game_id in successful:
        root = out / "traces" / game_id
        required = (root / f"{game_id}.steps.jsonl", root / f"{game_id}.audit.jsonl", root / f"{game_id}.json")
        if not all(path.is_file() and path.stat().st_size > 0 for path in required):
            missing.append(game_id)
    return {"successful_games": len(successful), "complete_games": len(successful) - len(missing), "missing_games": missing, "complete": not missing}


def write_outputs(out: Path, rows: list[dict], specs: list[str], requested: int, interrupted: bool, code: str | None = None, presets=None, report_stamp: str | None = None) -> None:
    report_stamp = report_stamp or datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    summary = summarize(rows, specs, requested, interrupted, presets)
    if code:
        summary["verification_code"] = code
    config_path = out / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    for key in ("test_id", "dataset_games", "dataset_sha256", "dataset_artifact", "replay_mode", "replay_trace"):
        if key in config:
            summary[key] = config[key]
    if config.get("replay_trace"):
        summary["trace_integrity"] = trace_integrity(out, rows)
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
    if config:
        if config.get("test_id"):
            lines.extend((f"- 测试编号：`{config['test_id']}`", f"- 数据集规模：`{config['dataset_games']}`", f"- 数据集 SHA-256：`{config['dataset_sha256']}`", f"- 复现方式：`{config.get('replay_mode', 'game_id')}`", f"- 完整复盘：`{bool(config.get('replay_trace'))}`"))
    if summary.get("trace_integrity"):
        ti = summary["trace_integrity"]
        lines.append(f"- 复盘完整性：`{ti['complete_games']}/{ti['successful_games']}`；门禁：`{'PASS' if ti['complete'] else 'FAIL'}`")
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


def confirm_run(games: int, mode: str, target: str | None = None, threads: int = 1, *, executor: str = "thread", memory_budget_mib: int | None = None, input_fn=input) -> bool:
    experiments = 12 if mode == "capability" else 1
    minutes = estimate_seconds(games, mode, threads=threads) / 60
    label = f"目标 {target}，" if target else ""
    memory = f"；内存预算 {memory_budget_mib} MiB" if memory_budget_mib is not None else ""
    answer = input_fn(f"\n即将开始：{label}{experiments} 个实验，共 {games * experiments} 局；执行器 {executor}；workers {threads}{memory}；预计耗时约 {minutes:.1f} 分钟。确认开始？[y/N] ")
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


def run_capability_mode(target: str, games: int, output: Path, presets=None, threads: int = 1, *, executor: str = "thread", memory_budget_mib: int = 1024) -> int:
    output.mkdir(parents=True, exist_ok=True)
    experiments = capability_experiments(target)
    started_at = datetime.now().astimezone()
    run_stamp = started_at.strftime("%Y%m%d_%H%M%S")
    ids_for_code = game_ids(games)
    code = verification_code(games=games, game_id_list=ids_for_code, players=[target] * 4, mode="capability", target=target)
    preset_id = presets[0] if isinstance(presets, (list, tuple)) else presets
    workers, worker_reason = effective_workers(threads, games, memory_budget_mib)
    if executor == "serial": workers = 1
    manifest = {"mode": "capability", "target": target, "humanlike_preset": preset_id, "executor": executor, "workers": workers, "memory_budget_mib": memory_budget_mib, "worker_limit_reason": worker_reason, "games_per_experiment": games,
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
        tasks = [(index, experiment["players"], ids[index], exp_presets, None, None) for index in pending]
        for index, row in execute_tasks(tasks, executor=executor, workers=workers, should_stop=lambda: STOP):
            rows.append(row)
            write_outputs(run_dir, rows, experiment["players"], games, True, presets=exp_presets, report_stamp=run_stamp)
            (run_dir / "checkpoint.json").write_text(json.dumps({"next_index": len(rows), "last_game_id": ids[index]}, ensure_ascii=False, indent=2), encoding="utf-8")
            completed_total = (number - 1) * games + len(rows)
            total = len(experiments) * games
            elapsed = time.perf_counter() - wall_start
            rate = elapsed / completed_total if completed_total else 0.0
            eta = rate * (total - completed_total)
            print(f"\r能力评估 {progress_bar(completed_total, total)} 总局数 {completed_total}/{total} 校验码 {code} 实验 {number}/{len(experiments)} {name} 局 {len(rows)}/{games} 已运行 {elapsed:.1f}s 剩余约 {eta:.1f}s", end="", flush=True)
            if STOP: break
        write_outputs(run_dir, rows, experiment["players"], games, len(rows) < games, presets=presets, report_stamp=run_stamp)
        target_stat = summarize(rows, experiment["players"], games, len(rows) < games)["seats"][experiment["seat"]]
        aggregate.append({"baseline": experiment["baseline"], "target_seat": f"s{experiment['seat']}", **target_stat})
        if STOP: break
    (output / "capability_summary.json").write_text(json.dumps({"target": target, "games_per_experiment": games, "verification_code": code, "completed_experiments": len(aggregate), "results": aggregate}, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# {target} AI 能力评估", "", f"每个基线每个座位：{games} 局", f"唯一校验码：`{code}`", f"人格预设：`{preset_id or '无'}`", f"执行器/workers：`{executor}/{workers}`", "", "|基线|目标座位|人格预设|胜率|Top1率|平均得分|平均响应(ms)|P95响应(ms)|", "|---|---|---|---:|---:|---:|---:|---:|"]
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
    parser.add_argument("--executor", choices=EXECUTORS)
    parser.add_argument("--workers", type=int)
    parser.add_argument("--memory-budget-mib", type=int, default=1024)
    parser.add_argument("--test-id")
    parser.add_argument("--dataset-games", type=int)
    parser.add_argument("--replay-fixed-deal", action="store_true")
    parser.add_argument("--replay-trace", action="store_true")
    parser.add_argument("--humanlike-preset", choices=PRESET_IDS)
    parser.add_argument("--humanlike-presets", help="batch四座preset，逗号分隔；非humanlike座位可留空")
    parser.add_argument("--yes", action="store_true", help="跳过启动确认")
    parser.add_argument("--list-test-groups", action="store_true", help="列出可用固定牌局组")
    args = parser.parse_args(argv)
    if args.list_test_groups:
        for test_id in available_test_ids():
            try:
                manifest = json.loads((ROOT / "data/fairness" / test_id / "manifest.json").read_text(encoding="utf-8"))
                counts = manifest.get("supported_counts") or ([manifest.get("games")] if manifest.get("games") else [])
                print(json.dumps({"test_id": test_id, "mode": manifest.get("mode"), "games": counts, "sha256": manifest.get("sha256"), "seed": manifest.get("seed")}, ensure_ascii=False))
            except (OSError, json.JSONDecodeError):
                continue
        return 0
    resume_config = None
    if args.resume:
        resume_path = Path(args.resume) / "config.json"
        if not resume_path.is_file():
            parser.error(f"--resume 缺少配置文件：{resume_path}")
        resume_config = json.loads(resume_path.read_text(encoding="utf-8"))
        args.mode = "batch"
        args.games = int(resume_config["games"])
        args.players = ",".join(resume_config["players"])
        args.executor = resume_config.get("executor", args.executor or "serial")
        args.threads = int(resume_config.get("workers", resume_config.get("threads", args.threads or 1)))
        args.test_id = resume_config.get("test_id")
        args.dataset_games = resume_config.get("dataset_games")
        batch_presets = resume_config.get("presets")
    else:
        batch_presets = None
    if args.workers is not None:
        if args.workers < 1: parser.error("--workers 必须大于0")
        args.threads = args.workers
    if args.humanlike_presets is not None:
        values = [value.strip() or None for value in args.humanlike_presets.split(",")]
        if len(values) != 4 or any(value is not None and value not in PRESET_IDS for value in values):
            parser.error("--humanlike-presets 必须是四个合法preset/空值")
        batch_presets = values
    while not args.resume:
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
        if args.mode == "batch" and args.test_id is None and available_test_ids():
            selected = choose_option("固定测试编号", ["不使用"] + available_test_ids())
            args.test_id = None if selected == "不使用" else selected
        selected_specs = ([args.target] if args.mode == "capability" else ([item.strip() for item in args.players.split(",")] if args.players else []))
        if args.executor is None:
            args.executor = "serial" if "humanlike_v2" in selected_specs else "thread"
        if args.threads is None:
            args.threads = 1 if args.executor == "serial" else int(choose_option("workers", [str(x) for x in THREAD_OPTIONS]))
        if args.yes or confirm_run(args.games, args.mode, args.target, args.threads, executor=args.executor, memory_budget_mib=args.memory_budget_mib): break
        print("已取消，返回参数选择。")
        args.games = None; args.target = None; args.players = None; args.mode = None; args.threads = None; args.executor = None; args.humanlike_preset = None; batch_presets = None
    if args.mode == "capability":
        return run_capability_mode(args.target, args.games, Path(args.output) / f"capability_{args.target}_{args.games}", [args.humanlike_preset] * 4 if args.humanlike_preset else None, args.threads, executor=args.executor, memory_budget_mib=args.memory_budget_mib)
    specs = [item.strip() for item in args.players.split(",")]
    if len(specs) != 4 or any(item not in TYPES for item in specs):
        parser.error("--players 必须包含四个合法 AI：" + ",".join(TYPES))
    out = Path(args.resume) if args.resume else Path(args.output) / f"{args.games}_{'_'.join(specs)}"
    out.mkdir(parents=True, exist_ok=True)
    config_path = out / "config.json"
    rows = []
    if args.resume:
        config = resume_config or json.loads(config_path.read_text(encoding="utf-8"))
        args.games, specs = int(config["games"]), list(config["players"])
        games_file = out / "games.jsonl"
        if games_file.exists(): rows = [json.loads(line) for line in games_file.read_text(encoding="utf-8").splitlines() if line]
    else:
        if args.dataset_games is not None and args.dataset_games != args.games:
            parser.error("--dataset-games 必须与 --games 一致")
        deals, dataset_meta = load_fixed_dataset(args.test_id, args.games) if args.test_id else (None, {})
        ids = [deal["game_id"] for deal in deals] if deals else game_ids(args.games)
        code = verification_code(games=args.games, game_id_list=ids, players=specs, mode="batch")
        actual_workers, worker_reason = effective_workers(args.threads, args.games, args.memory_budget_mib)
        if args.executor == "serial": actual_workers = 1
        args.threads = actual_workers
        config_path.write_text(json.dumps({"games": args.games, "players": specs, "presets": batch_presets, "executor": args.executor, "workers": actual_workers, "memory_budget_mib": args.memory_budget_mib, "worker_limit_reason": worker_reason, "game_ids": ids, "verification_code": code, **dataset_meta, "replay_mode": "fixed_deal" if (args.replay_fixed_deal or args.replay_trace) else "game_id", "replay_trace": bool(args.replay_trace)}, ensure_ascii=False, indent=2), encoding="utf-8")
    config_data = json.loads(config_path.read_text(encoding="utf-8"))
    ids = config_data["game_ids"]
    batch_presets = config_data.get("presets", batch_presets or [None] * 4)
    deals_by_id = {}
    if config_data.get("test_id"):
        loaded_deals, checked_meta = load_fixed_dataset(config_data["test_id"], int(config_data["dataset_games"]))
        if checked_meta["dataset_sha256"] != config_data["dataset_sha256"]:
            raise ValueError("resume dataset SHA-256 differs from config")
        deals_by_id = {deal["game_id"]: deal for deal in loaded_deals}
    if args.resume:
        args.executor = config_data.get("executor", args.executor or "serial")
        args.threads = int(config_data.get("workers", config_data.get("threads", args.threads or 1)))
    code = verification_code(games=args.games, game_id_list=ids, players=specs, mode="batch")
    global STOP
    signal.signal(signal.SIGINT, lambda *_: globals().__setitem__("STOP", True))
    wall_start = time.perf_counter()
    report_stamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    completed_ids = {row.get("game_id") for row in rows}
    pending = [index for index, game_id in enumerate(ids) if game_id not in completed_ids]
    fixed = config_data.get("replay_mode") == "fixed_deal"
    replay_trace = bool(config_data.get("replay_trace"))
    tasks = [(index, specs, ids[index], batch_presets, deals_by_id.get(ids[index]) if fixed else None, str(out / "traces" / ids[index]) if replay_trace else None) for index in pending]
    try:
        for index, row in execute_tasks(tasks, executor=args.executor, workers=args.threads, should_stop=lambda: STOP):
            rows.append(row)
            rows.sort(key=lambda item: ids.index(item.get("game_id", "")))
            elapsed = time.perf_counter() - wall_start
            rate = elapsed / max(1, len(rows) - (index - (len(rows) - 1)))
            eta = rate * (args.games - len(rows))
            write_outputs(out, rows, specs, args.games, True, code, presets=batch_presets, report_stamp=report_stamp)
            (out / "checkpoint.json").write_text(json.dumps({"next_index": len(rows), "last_game_id": ids[index]}, ensure_ascii=False, indent=2), encoding="utf-8")
            score_text = " ".join(f"s{s}:{row.get('scores', {}).get(str(s), 0)}" for s in range(4))
            print(f"\r{progress_bar(len(rows), args.games)} 总局数 {len(rows)}/{args.games} 校验码 {code} {score_text} executor={args.executor} workers={args.threads} elapsed={elapsed:.1f}s ETA={eta:.1f}s", end="", flush=True)
            if STOP: break
    except KeyboardInterrupt:
        # SIGINT can also reach a process worker.  Its future then re-raises
        # KeyboardInterrupt in the parent even though our signal handler has
        # already requested a graceful stop.  Treat both paths identically so
        # completed rows are checkpointed and the CLI exits with 130.
        STOP = True
    print()
    write_outputs(out, rows, specs, args.games, len(rows) < args.games, code, presets=batch_presets, report_stamp=report_stamp)
    integrity = trace_integrity(out, rows) if replay_trace else {"complete": True}
    return 130 if STOP else (1 if len(rows) == args.games and not integrity["complete"] else 0)


if __name__ == "__main__":
    raise SystemExit(main())
