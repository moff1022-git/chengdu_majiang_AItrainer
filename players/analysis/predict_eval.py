"""Headless multi-game evaluation of F0010 hand prediction with JSONL logs."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

from engine.action import ActionType
from engine.blood_battle import PlayError, finalize_game
from engine.config import EngineConfig
from engine.session import GameSession, build_ready_game
from players.analysis.hand_predict import (
    apply_oracle_accuracy,
    discard_fingerprint,
    predict_opponent_hands,
)
from players.analysis.predict_log import (
    PredictAnalysis,
    PredictLogWriter,
    analyze_predict_logs,
    write_analysis_report,
)
from players.analysis.remain import remain_map
from protocols.view_filter import filter_state_for_seat

# Fixed bench sets: configs/f0010_eval_sets.json (20 ⊂ 50 ⊂ 100)
DEFAULT_EVAL_SETS_PATH = (
    Path(__file__).resolve().parents[2] / "configs" / "f0010_eval_sets.json"
)


def load_eval_set(
    set_name: str | int = "20",
    *,
    path: Path | str | None = None,
) -> list[dict[str, Any]]:
    """Load fixed {game_id, play_seed, index} list for set 20 / 50 / 100."""
    path = Path(path) if path is not None else DEFAULT_EVAL_SETS_PATH
    key = str(set_name)
    if not path.is_file():
        raise FileNotFoundError(f"F0010 eval set file missing: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    sets = data.get("sets") or {}
    if key not in sets:
        raise KeyError(
            f"unknown eval set {key!r}; available: {sorted(sets.keys())}"
        )
    entries = list(sets[key])
    if not entries:
        raise ValueError(f"eval set {key!r} is empty")
    for e in entries:
        if "game_id" not in e or "play_seed" not in e:
            raise ValueError(f"invalid entry in set {key}: {e!r}")
    return entries


def list_eval_sets(*, path: Path | str | None = None) -> dict[str, int]:
    path = Path(path) if path is not None else DEFAULT_EVAL_SETS_PATH
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: len(v) for k, v in (data.get("sets") or {}).items()}


def _meta_from_state(state, self_seat: int) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for p in state.players:
        if p.seat == self_seat:
            continue
        out[p.seat] = {
            "n_discards": len(p.discard_pile),
            "n_melds": len(p.melds or []),
            "dingque": p.dingque.value if p.dingque else None,
        }
    return out


def _oracle_from_state(state, self_seat: int) -> dict[str, list[str]]:
    return {
        str(p.seat): [t.id for t in p.hand]
        for p in state.players
        if p.seat != self_seat and p.status == "active"
    }


def snapshot_predict(
    state,
    self_seat: int,
    *,
    writer: PredictLogWriter | None,
    prev_joints: list | None,
    prev_forecasts: list | None,
    discard_seq: int,
    source: str = "eval",
) -> tuple[list, list, dict]:
    view = filter_state_for_seat(state, self_seat)
    view["discard_seq"] = discard_seq
    if state.last_discard is not None:
        view["last_discard"] = state.last_discard.id
        view["last_discard_seat"] = state.last_discard_seat
    fp = discard_fingerprint(view)
    seed = abs(hash(fp)) % (2**31)
    last_tile = state.last_discard.id if state.last_discard else None
    last_discarder = state.last_discard_seat
    forecasts = predict_opponent_hands(
        view,
        self_seat,
        top_k=5,
        prev_joints=prev_joints,
        prev_forecasts=prev_forecasts,
        last_discarder=last_discarder,
        last_discard_tile=last_tile,
        seed=seed,
    )
    oracle = _oracle_from_state(state, self_seat)
    forecasts = apply_oracle_accuracy(forecasts, oracle)
    scenes = []
    if forecasts:
        scenes = list(getattr(forecasts[0], "_joint_scenes", None) or [])
    remain = remain_map(state, self_seat)
    row = None
    if writer is not None:
        row = writer.emit_tick(
            game_id=state.game_id,
            self_seat=self_seat,
            forecasts=forecasts,
            oracle_hands=oracle,
            discard_fp=fp,
            discard_seq=discard_seq,
            last_discarder=last_discarder,
            last_discard_tile=last_tile,
            phase=state.phase,
            wall_remaining=len(state.wall or []),
            used_continuity=bool(prev_joints),
            remain=remain,
            meta_by_seat=_meta_from_state(state, self_seat),
            source=source,
        )
    return forecasts, scenes, row or {}


def evaluate_one_game(
    game_id: str,
    *,
    log_dir: Path | str,
    self_seats: list[int] | None = None,
    config: EngineConfig | None = None,
    rng: random.Random | None = None,
    max_steps: int = 10_000,
    sample_every_discard: bool = True,
) -> dict[str, Any]:
    """Play a random legal game; log prediction ticks for each self_seat."""
    rng = rng or random.Random(0)
    cfg = config or EngineConfig(num_players=4)
    state = build_ready_game(game_id, num_players=cfg.num_players, config=cfg)
    session = GameSession(state, cfg)
    seats = self_seats or [0]
    writers = {
        s: PredictLogWriter(f"{game_id}-S{s}", log_dir=log_dir) for s in seats
    }
    # Also write combined under game_id for convenience
    combined = PredictLogWriter(game_id, log_dir=log_dir)
    tracks: dict[int, dict] = {
        s: {"joints": None, "forecasts": None, "seq": 0} for s in seats
    }
    n_ticks = 0
    try:
        session.start_play()
        steps = 0
        while not session.is_terminal() and steps < max_steps:
            steps += 1
            st = session.state
            if st.phase == "draw":
                session.step_auto_draw()
                continue
            if st.phase == "discard":
                seat = st.current_seat
                assert seat is not None
                acts = session.legal_actions(seat)
                if not acts:
                    raise PlayError(f"no legal actions for seat {seat}")
                discards = [a for a in acts if a.type == ActionType.DISCARD]
                pool = discards if discards else acts
                action = rng.choice(pool)
                # Literature-style discard accuracy (rank_discards vs actual)
                if discards and action.type == ActionType.DISCARD and action.tiles:
                    try:
                        from players.analysis.discard_accuracy import (
                            append_discard_acc_row,
                            score_discard_decision,
                        )

                        acc_row = score_discard_decision(
                            st, seat, discards, action.tiles[0].id
                        )
                        acc_row["game_id"] = game_id
                        acc_row["type"] = "discard_acc"
                        append_discard_acc_row(log_dir, acc_row)
                    except Exception:
                        pass
                session.apply(seat, action)
                if sample_every_discard:
                    for s in seats:
                        tr = tracks[s]
                        tr["seq"] += 1
                        fcs, joints, row = snapshot_predict(
                            session.state,
                            s,
                            writer=writers[s],
                            prev_joints=tr["joints"],
                            prev_forecasts=tr["forecasts"],
                            discard_seq=tr["seq"],
                        )
                        if row:
                            combined.emit(row)
                        tr["forecasts"] = fcs
                        tr["joints"] = joints
                        n_ticks += 1
                continue
            if st.phase == "response":
                for rseat in list(st.response_seats or []):
                    if session.is_terminal():
                        break
                    if st.phase != "response":
                        break
                    if rseat not in (st.response_seats or []):
                        continue
                    if rseat in (st.pending_claims or {}):
                        continue
                    acts = session.legal_actions(rseat)
                    if not acts:
                        continue
                    passes = [a for a in acts if a.type == ActionType.PASS]
                    action = passes[0] if passes else rng.choice(acts)
                    session.apply(rseat, action)
                continue
            if st.phase == "ready":
                session.start_play()
                continue
            if st.phase == "finished":
                break
            raise PlayError(f"stuck in phase {st.phase}")
        if not session.is_terminal():
            st = session.state
            st.phase = "finished"
            st.finished_reason = st.finished_reason or "max_steps"
            finalize_game(st, cfg)
        result = session.result()
        return {
            "game_id": game_id,
            "finished_reason": result.finished_reason,
            "n_ticks": n_ticks,
            "log_dir": str(log_dir),
        }
    finally:
        for w in writers.values():
            w.close()
        combined.close()


def run_predict_eval(
    n_games: int = 10,
    *,
    seed: int = 0,
    log_dir: Path | str | None = None,
    self_seats: list[int] | None = None,
    write_report: bool = True,
    eval_set: str | int | None = None,
    eval_set_path: Path | str | None = None,
    game_specs: list[dict[str, Any]] | None = None,
) -> tuple[dict[str, Any], PredictAnalysis]:
    """Run prediction eval.

    Reproducibility (preferred):
      - ``eval_set="20"|"50"|"100"`` loads fixed game_id + play_seed from
        ``configs/f0010_eval_sets.json`` (nested: 20 ⊂ 50 ⊂ 100).
      - or pass ``game_specs=[{"game_id": ..., "play_seed": ...}, ...]``.

    Legacy: if neither is set, uses ``pred-eval-{seed}-{i}`` and RNG derived
    from ``seed`` (non-fixed across set sizes).
    """
    from datetime import datetime, timezone

    specs: list[dict[str, Any]]
    set_label: str | None = None
    if game_specs is not None:
        specs = list(game_specs)
        set_label = "custom"
    elif eval_set is not None:
        set_label = str(eval_set)
        specs = load_eval_set(eval_set, path=eval_set_path)
    else:
        # legacy ephemeral ids
        rng = random.Random(seed)
        specs = [
            {
                "index": i,
                "game_id": f"pred-eval-{seed}-{i}",
                "play_seed": rng.randint(0, 2**30),
            }
            for i in range(n_games)
        ]
        set_label = f"legacy-seed-{seed}"

    n_games = len(specs)
    if log_dir is None:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        tag = f"set{set_label}" if set_label and set_label.isdigit() else "eval"
        log_dir = Path("logs/predict") / f"{tag}-{ts}"
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    # Persist which set was used for this run
    (log_dir / "eval_set_used.json").write_text(
        json.dumps(
            {
                "set": set_label,
                "n_games": n_games,
                "game_ids": [s["game_id"] for s in specs],
                "play_seeds": [int(s["play_seed"]) for s in specs],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    games_meta = []
    for spec in specs:
        gid = str(spec["game_id"])
        play_seed = int(spec["play_seed"])
        meta = evaluate_one_game(
            gid,
            log_dir=log_dir,
            self_seats=self_seats or [0],
            rng=random.Random(play_seed),
        )
        meta["play_seed"] = play_seed
        meta["set_index"] = spec.get("index")
        games_meta.append(meta)
    analysis = analyze_predict_logs(log_dir)
    from players.analysis.discard_accuracy import (
        analyze_discard_acc_file,
        discard_acc_markdown,
    )

    discard_stats = analyze_discard_acc_file(log_dir / "discard_acc.jsonl")
    analysis.raw_stats = dict(analysis.raw_stats or {})
    analysis.raw_stats["discard_accuracy"] = discard_stats
    report_path = None
    if write_report:
        report_path = write_analysis_report(analysis, log_dir / "ANALYSIS.md")
        # Append discard accuracy section
        md_extra = discard_acc_markdown(discard_stats)
        with Path(report_path).open("a", encoding="utf-8") as f:
            f.write("\n" + md_extra)
        (log_dir / "DISCARD_ACCURACY.json").write_text(
            json.dumps(discard_stats, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        latest = Path("logs/predict") / "LATEST_ANALYSIS.md"
        latest.parent.mkdir(parents=True, exist_ok=True)
        latest.write_text(analysis.to_markdown() + "\n" + md_extra, encoding="utf-8")
        docs_path = Path("docs/status/F0010_predict_accuracy_analysis.md")
        docs_path.write_text(analysis.to_markdown() + "\n" + md_extra, encoding="utf-8")
    summary = {
        "games": n_games,
        "eval_set": set_label,
        "log_dir": str(log_dir),
        "report": str(report_path) if report_path else None,
        "mean_best_f1": analysis.mean_best_f1,
        "mean_top1_f1": analysis.mean_top1_f1,
        "mean_lift": analysis.mean_lift,
        "n_ticks": analysis.n_ticks,
        "n_opponent_samples": analysis.n_opponent_samples,
        "discard_accuracy": {
            "top1": discard_stats.get("top1_accuracy"),
            "top3": discard_stats.get("top3_accuracy"),
            "random_baseline": discard_stats.get("random_baseline_mean"),
            "expert_consistency": discard_stats.get("expert_min_shanten_consistency"),
            "n": discard_stats.get("n"),
        },
        "game_ids": [s["game_id"] for s in specs],
        "games_meta": games_meta,
    }
    return summary, analysis
