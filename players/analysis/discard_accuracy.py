"""Discard accuracy metric (literature-style: top-1 / top-3 among legal tiles).

Literature reports ~68–88% top-1 on **human** discard labels (full own hand visible).
Here we score our ``rank_discards`` model against the **actual tile discarded**
in the eval trajectory, and also report a pure min-shanten expert consistency.

Note: fixed-set F0010 eval currently plays **uniform random legal discards**,
so top-1 vs actual is expected near the random baseline 1/n_legal (not 68–88%).
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from engine.action import Action, ActionType
from engine.shanten import shanten as compute_shanten
from engine.state import GameState
from engine.tile import Tile


def _remove_one(hand: list[Tile], tile_id: str) -> list[Tile]:
    out: list[Tile] = []
    removed = False
    for t in hand:
        if not removed and t.id == tile_id:
            removed = True
            continue
        out.append(t)
    return out


def _min_shanten_expert_tile(
    hand: list[Tile],
    melds: list,
    dingque,
    legal_tile_ids: list[str],
) -> str | None:
    """Pure min-shanten (then lexicographic tile_id) among legal discards."""
    best_tid: str | None = None
    best_sh = 99
    for tid in legal_tile_ids:
        trial = _remove_one(hand, tid)
        try:
            sh = int(compute_shanten(trial, melds, dingque).shanten)
        except Exception:
            sh = 8
        if best_tid is None or sh < best_sh or (sh == best_sh and tid < best_tid):
            best_sh = sh
            best_tid = tid
    return best_tid


def score_discard_decision(
    state: GameState,
    seat: int,
    legal_discards: list[Action],
    actual_tile_id: str,
) -> dict[str, Any]:
    """Score rank_discards top-1/top-3 vs actual; plus min-shanten expert consistency."""
    from players.analysis.opponent_model import estimate_opponents
    from players.analysis.strategy import rank_discards

    player = state.players[seat]
    hand = list(player.hand)
    melds = list(player.melds or [])
    dingque = player.dingque
    legal_ids: list[str] = []
    seen: set[str] = set()
    for a in legal_discards:
        if a.type == ActionType.DISCARD and a.tiles:
            tid = a.tiles[0].id
            if tid not in seen:
                seen.add(tid)
                legal_ids.append(tid)
    n_legal = len(legal_ids)
    if n_legal == 0:
        return {
            "seat": seat,
            "actual": actual_tile_id,
            "n_legal": 0,
            "top1_hit": False,
            "top3_hit": False,
            "rank": None,
            "mrr": 0.0,
            "random_baseline": 0.0,
            "pred_top1": None,
            "expert_min_shanten": None,
            "expert_hit": False,
            "n_discards_before": len(player.discard_pile or []),
        }

    ops = estimate_opponents(state, seat)
    ranked = rank_discards(
        state,
        seat,
        hand,
        melds,
        dingque,
        ops,
        legal_discards=legal_discards,
    )
    order = [r.tile_id for r in ranked]
    if actual_tile_id in order:
        rank = order.index(actual_tile_id) + 1
    else:
        rank = n_legal
    pred_top1 = order[0] if order else None
    expert = _min_shanten_expert_tile(hand, melds, dingque, legal_ids)
    n_disc = len(player.discard_pile or [])
    return {
        "seat": seat,
        "actual": actual_tile_id,
        "pred_top1": pred_top1,
        "n_legal": n_legal,
        "top1_hit": bool(pred_top1 == actual_tile_id),
        "top3_hit": bool(actual_tile_id in order[:3]),
        "rank": rank,
        "mrr": round(1.0 / rank, 6) if rank else 0.0,
        "random_baseline": round(1.0 / n_legal, 6),
        "expert_min_shanten": expert,
        "expert_hit": bool(pred_top1 is not None and pred_top1 == expert),
        "n_discards_before": n_disc,
        "phase_bucket": _phase_bucket(n_disc),
    }


def _phase_bucket(n_discards: int) -> str:
    if n_discards <= 2:
        return "early(≤2 disc)"
    if n_discards <= 6:
        return "mid(3-6 disc)"
    if n_discards <= 12:
        return "late(7-12 disc)"
    return "deep(>12 disc)"


def append_discard_acc_row(log_dir: Path | str, row: dict[str, Any]) -> None:
    path = Path(log_dir) / "discard_acc.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _mean(xs: list[float]) -> float | None:
    return round(sum(xs) / len(xs), 4) if xs else None


def _percentile(sorted_xs: list[float], p: float) -> float | None:
    if not sorted_xs:
        return None
    if len(sorted_xs) == 1:
        return round(sorted_xs[0], 4)
    k = (len(sorted_xs) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return round(sorted_xs[int(k)], 4)
    return round(sorted_xs[f] * (c - k) + sorted_xs[c] * (k - f), 4)


def analyze_discard_acc_file(path: Path | str) -> dict[str, Any]:
    """Aggregate discard_acc.jsonl → means, phase buckets, distribution."""
    path = Path(path)
    if not path.is_file():
        return {"n": 0, "note": "no discard_acc.jsonl"}
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if not rows:
        return {"n": 0}

    top1 = [1.0 if r.get("top1_hit") else 0.0 for r in rows]
    top3 = [1.0 if r.get("top3_hit") else 0.0 for r in rows]
    mrr = [float(r.get("mrr") or 0.0) for r in rows]
    base = [float(r.get("random_baseline") or 0.0) for r in rows]
    expert = [1.0 if r.get("expert_hit") else 0.0 for r in rows]
    ranks = [float(r["rank"]) for r in rows if r.get("rank") is not None]
    n_legals = [float(r.get("n_legal") or 0) for r in rows]
    ranks_sorted = sorted(ranks)
    by_phase: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    by_game: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        ph = str(r.get("phase_bucket") or "?")
        hit = 1.0 if r.get("top1_hit") else 0.0
        by_phase[ph]["top1"].append(hit)
        by_phase[ph]["top3"].append(1.0 if r.get("top3_hit") else 0.0)
        by_phase[ph]["mrr"].append(float(r.get("mrr") or 0.0))
        by_phase[ph]["baseline"].append(float(r.get("random_baseline") or 0.0))
        by_phase[ph]["expert"].append(1.0 if r.get("expert_hit") else 0.0)
        gid = str(r.get("game_id") or "?")
        by_game[gid].append(hit)

    game_means = sorted(
        (sum(v) / len(v) for v in by_game.values() if v),
    )
    phase_out: dict[str, dict[str, float | None]] = {}
    for ph, m in sorted(by_phase.items()):
        phase_out[ph] = {
            "n": float(len(m["top1"])),
            "top1_acc": _mean(m["top1"]),
            "top3_acc": _mean(m["top3"]),
            "mrr": _mean(m["mrr"]),
            "random_baseline": _mean(m["baseline"]),
            "expert_consistency": _mean(m["expert"]),
        }

    top1_mean = _mean(top1) or 0.0
    base_mean = _mean(base) or 0.0
    return {
        "n": len(rows),
        "n_games_with_discards": len(by_game),
        "top1_accuracy": _mean(top1),
        "top3_accuracy": _mean(top3),
        "mean_mrr": _mean(mrr),
        "random_baseline_mean": _mean(base),
        "lift_vs_random": round(top1_mean - base_mean, 4),
        "expert_min_shanten_consistency": _mean(expert),
        "mean_rank_of_actual": _mean(ranks),
        "mean_n_legal": _mean(n_legals),
        "rank_distribution": {
            "p10": _percentile(ranks_sorted, 0.10),
            "p25": _percentile(ranks_sorted, 0.25),
            "p50": _percentile(ranks_sorted, 0.50),
            "p75": _percentile(ranks_sorted, 0.75),
            "p90": _percentile(ranks_sorted, 0.90),
            "min": round(ranks_sorted[0], 4) if ranks_sorted else None,
            "max": round(ranks_sorted[-1], 4) if ranks_sorted else None,
        },
        "per_game_top1_acc_distribution": {
            "p10": _percentile(game_means, 0.10),
            "p25": _percentile(game_means, 0.25),
            "p50": _percentile(game_means, 0.50),
            "p75": _percentile(game_means, 0.75),
            "p90": _percentile(game_means, 0.90),
            "min": round(game_means[0], 4) if game_means else None,
            "max": round(game_means[-1], 4) if game_means else None,
            "mean": _mean(list(game_means)),
        },
        "by_phase": phase_out,
        "literature_band": "0.68–0.88 top-1 on human labels (not random play)",
        "note": (
            "Eval play is uniform random legal discards; top1_accuracy is expected "
            "near random_baseline_mean. expert_min_shanten_consistency measures how "
            "often rank_discards top1 equals pure min-shanten (own-hand oracle)."
        ),
    }


def discard_acc_markdown(stats: dict[str, Any]) -> str:
    if not stats or not stats.get("n"):
        return "## Discard accuracy\n\n- (no samples)\n"
    rd = stats.get("rank_distribution") or {}
    gd = stats.get("per_game_top1_acc_distribution") or {}
    lines = [
        "## Discard accuracy（文献式 top-1 / top-3）",
        "",
        f"- samples: **{stats.get('n')}**  |  games: **{stats.get('n_games_with_discards')}**",
        f"- **top1 accuracy: {stats.get('top1_accuracy')}**  "
        f"(literature band often **0.68–0.88** on human logs)",
        f"- top3 accuracy: **{stats.get('top3_accuracy')}**",
        f"- mean MRR: **{stats.get('mean_mrr')}**  |  mean rank of actual: **{stats.get('mean_rank_of_actual')}**",
        f"- random baseline (mean 1/n_legal): **{stats.get('random_baseline_mean')}**  "
        f"| lift: **{stats.get('lift_vs_random')}**",
        f"- expert min-shanten consistency (model top1 == min-shanten): "
        f"**{stats.get('expert_min_shanten_consistency')}**",
        f"- mean n_legal unique tiles: **{stats.get('mean_n_legal')}**",
        "",
        "### Rank of actual discard (lower better)",
        "",
        f"- min={rd.get('min')}  p10={rd.get('p10')}  p25={rd.get('p25')}  "
        f"p50={rd.get('p50')}  p75={rd.get('p75')}  p90={rd.get('p90')}  max={rd.get('max')}",
        "",
        "### Per-game top1 accuracy distribution",
        "",
        f"- min={gd.get('min')}  p10={gd.get('p10')}  p25={gd.get('p25')}  "
        f"p50={gd.get('p50')}  p75={gd.get('p75')}  p90={gd.get('p90')}  "
        f"max={gd.get('max')}  mean={gd.get('mean')}",
        "",
        "### By phase (discarder's n_discards before this action)",
        "",
    ]
    for ph, st in (stats.get("by_phase") or {}).items():
        lines.append(
            f"- {ph}: n={int(st.get('n') or 0)}  top1={st.get('top1_acc')}  "
            f"top3={st.get('top3_acc')}  mrr={st.get('mrr')}  "
            f"baseline={st.get('random_baseline')}  expert={st.get('expert_consistency')}"
        )
    lines += [
        "",
        f"> {stats.get('note', '')}",
        f"> Literature: {stats.get('literature_band', '')}",
        "",
    ]
    return "\n".join(lines)
