"""F0010-L: per-game opponent-hand prediction JSONL log + offline analysis."""

from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from players.analysis.hand_predict import (
    OpponentHandForecast,
    multiset_f1,
    _shanten_of_ids,
)

DEFAULT_PREDICT_LOG_DIR = Path("logs/predict")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _suit_hist(tiles: list[str]) -> dict[str, int]:
    c: Counter[str] = Counter()
    for tid in tiles:
        try:
            c[str(tid).split("_", 1)[0]] += 1
        except Exception:
            c["?"] += 1
    return {k: int(v) for k, v in sorted(c.items())}


def _dominant_suit(hist: dict[str, int], ban: str | None = None) -> str | None:
    items = [(s, n) for s, n in hist.items() if ban is None or s != ban]
    if not items:
        return None
    items.sort(key=lambda x: (-x[1], x[0]))
    return items[0][0]


def random_baseline_f1(
    true_tiles: list[str],
    remain: dict[str, int],
    *,
    n_samples: int = 8,
    seed: int = 0,
) -> float:
    """Mean multiset F1 of random hands sampled from remain (same length)."""
    need = len(true_tiles)
    if need <= 0:
        return 1.0
    pool: list[str] = []
    for tid, n in remain.items():
        pool.extend([tid] * max(0, int(n)))
    if not pool:
        return 0.0
    rng = random.Random(seed)
    scores: list[float] = []
    for i in range(max(1, n_samples)):
        if len(pool) >= need:
            # sample without replacement when possible
            work = list(pool)
            rng.shuffle(work)
            pred = sorted(work[:need])
        else:
            pred = sorted(rng.choices(pool, k=need))
        scores.append(multiset_f1(pred, true_tiles))
    return float(sum(scores) / len(scores))


def build_opponent_diag(
    fc: OpponentHandForecast,
    true_tiles: list[str] | None,
    *,
    n_discards: int = 0,
    n_melds: int = 0,
    dingque: str | None = None,
    remain: dict[str, int] | None = None,
    baseline_seed: int = 0,
) -> dict[str, Any]:
    true_ids = [str(t) for t in (true_tiles or [])]
    top1 = fc.hypotheses[0] if fc.hypotheses else None
    top1_tiles = list(top1.tiles) if top1 else []
    top1_f1 = multiset_f1(top1_tiles, true_ids) if true_ids and top1 else None
    best_f1 = fc.accuracy
    best_rank = (fc.accuracy_detail or {}).get("best_rank")
    if best_f1 is None and true_ids:
        best_f1 = -1.0
        best_rank = None
        for h in fc.hypotheses:
            f1 = multiset_f1(h.tiles, true_ids)
            if f1 > best_f1:
                best_f1 = f1
                best_rank = h.rank
        if best_f1 < 0:
            best_f1 = 0.0
    true_hist = _suit_hist(true_ids) if true_ids else {}
    pred_hist = _suit_hist(top1_tiles) if top1_tiles else {}
    true_main = _dominant_suit(true_hist, dingque)
    pred_main = _dominant_suit(pred_hist, dingque)
    true_sh = (
        _shanten_of_ids(true_ids, n_melds, dingque) if true_ids else None
    )
    pred_sh = (
        getattr(top1, "shanten_est", None)
        if top1 is not None
        else None
    )
    if pred_sh is None and top1_tiles:
        pred_sh = _shanten_of_ids(top1_tiles, n_melds, dingque)
    baseline = None
    if true_ids and remain is not None:
        baseline = round(
            random_baseline_f1(true_ids, remain, seed=baseline_seed), 4
        )
    hyp_rows = []
    for h in fc.hypotheses:
        row = {
            "rank": h.rank,
            "scene_id": h.scene_id,
            "confidence": h.confidence,
            "label": h.label,
            "shanten_est": h.shanten_est,
            "n_tiles": len(h.tiles),
        }
        if true_ids:
            row["f1"] = round(multiset_f1(h.tiles, true_ids), 4)
        hyp_rows.append(row)
    return {
        "seat": fc.seat,
        "accuracy": None if best_f1 is None else round(float(best_f1), 4),
        "top1_f1": None if top1_f1 is None else round(float(top1_f1), 4),
        "best_rank": best_rank,
        "exact_set": bool((fc.accuracy_detail or {}).get("exact_set"))
        if fc.accuracy_detail
        else (
            bool(true_ids)
            and any(sorted(h.tiles) == sorted(true_ids) for h in fc.hypotheses)
        ),
        "strategy_hint": fc.strategy_hint or "",
        "n_discards": int(n_discards),
        "n_melds": int(n_melds),
        "dingque": dingque,
        "hand_count": len(true_ids) if true_ids else (len(top1_tiles) or None),
        "true_suit_hist": true_hist,
        "pred_top1_suit_hist": pred_hist,
        "suit_match": (
            true_main is not None and true_main == pred_main
            if true_ids and top1_tiles
            else None
        ),
        "true_shanten": true_sh,
        "pred_top1_shanten": pred_sh,
        "random_baseline_f1": baseline,
        "lift_vs_random": (
            None
            if best_f1 is None or baseline is None
            else round(float(best_f1) - float(baseline), 4)
        ),
        "hypotheses": hyp_rows,
    }


def build_predict_tick(
    *,
    game_id: str,
    self_seat: int,
    forecasts: list[OpponentHandForecast],
    oracle_hands: dict[str, list[str]] | dict[int, list[str]] | None = None,
    discard_fp: str = "",
    discard_seq: int | None = None,
    last_discarder: int | None = None,
    last_discard_tile: str | None = None,
    phase: str = "",
    wall_remaining: int | None = None,
    used_continuity: bool = False,
    remain: dict[str, int] | None = None,
    meta_by_seat: dict[int, dict[str, Any]] | None = None,
    source: str = "seat_window",
) -> dict[str, Any]:
    meta_by_seat = meta_by_seat or {}
    opponents: list[dict[str, Any]] = []
    for fc in forecasts:
        m = meta_by_seat.get(fc.seat, {})
        true = None
        if oracle_hands:
            true = oracle_hands.get(str(fc.seat))
            if true is None:
                true = oracle_hands.get(fc.seat)  # type: ignore[arg-type]
        opponents.append(
            build_opponent_diag(
                fc,
                list(true) if true is not None else None,
                n_discards=int(m.get("n_discards", 0)),
                n_melds=int(m.get("n_melds", 0)),
                dingque=m.get("dingque"),
                remain=remain,
                baseline_seed=hash((game_id, self_seat, fc.seat, discard_fp))
                % (2**31),
            )
        )
    accs = [o["accuracy"] for o in opponents if o.get("accuracy") is not None]
    return {
        "type": "predict_tick",
        "ts": _utc_now(),
        "source": source,
        "game_id": game_id,
        "self_seat": int(self_seat),
        "discard_fp": discard_fp,
        "discard_seq": discard_seq,
        "last_discarder": last_discarder,
        "last_discard_tile": last_discard_tile,
        "phase": phase,
        "wall_remaining": wall_remaining,
        "used_continuity": bool(used_continuity),
        "n_opponents": len(opponents),
        "mean_accuracy": (
            round(sum(accs) / len(accs), 4) if accs else None
        ),
        "opponents": opponents,
    }


class PredictLogWriter:
    """Append-only JSONL writer, one file per game_id."""

    def __init__(
        self,
        game_id: str,
        *,
        log_dir: Path | str = DEFAULT_PREDICT_LOG_DIR,
    ) -> None:
        self.game_id = str(game_id or "unknown")
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        safe = "".join(
            c if c.isalnum() or c in "-_." else "_" for c in self.game_id
        )[:120] or "unknown"
        self.path = self.log_dir / f"{safe}.jsonl"
        self._fp = self.path.open("a", encoding="utf-8")

    def emit(self, row: dict[str, Any]) -> None:
        self._fp.write(json.dumps(row, ensure_ascii=False) + "\n")
        self._fp.flush()

    def emit_tick(self, **kwargs: Any) -> dict[str, Any]:
        row = build_predict_tick(**kwargs)
        self.emit(row)
        return row

    def close(self) -> None:
        if self._fp and not self._fp.closed:
            self._fp.close()

    def __enter__(self) -> PredictLogWriter:
        return self
    def __exit__(self, *args: object) -> None:
        self.close()


# Module-level cache for seat_window: game_id -> writer
_writers: dict[str, PredictLogWriter] = {}


def get_predict_logger(
    game_id: str,
    *,
    log_dir: Path | str = DEFAULT_PREDICT_LOG_DIR,
) -> PredictLogWriter:
    gid = str(game_id or "unknown")
    w = _writers.get(gid)
    if w is None or w._fp.closed:
        w = PredictLogWriter(gid, log_dir=log_dir)
        _writers[gid] = w
    return w


def close_all_predict_loggers() -> None:
    for w in list(_writers.values()):
        try:
            w.close()
        except Exception:
            pass
    _writers.clear()


def iter_predict_ticks(paths: Iterable[Path | str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            files = sorted(path.glob("*.jsonl"))
        else:
            files = [path]
        for f in files:
            if not f.is_file():
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except OSError:
                continue
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if obj.get("type") == "predict_tick":
                    rows.append(obj)
    return rows


def _info_bucket(n_discards: int) -> str:
    if n_discards <= 2:
        return "early(≤2 disc)"
    if n_discards <= 6:
        return "mid(3-6 disc)"
    if n_discards <= 12:
        return "late(7-12 disc)"
    return "deep(>12 disc)"


@dataclass
class PredictAnalysis:
    n_ticks: int = 0
    n_opponent_samples: int = 0
    n_games: int = 0
    mean_best_f1: float | None = None
    mean_top1_f1: float | None = None
    mean_baseline_f1: float | None = None
    mean_lift: float | None = None
    exact_rate: float | None = None
    suit_match_rate: float | None = None
    best_rank_hist: dict[str, int] = field(default_factory=dict)
    by_info_bucket: dict[str, dict[str, float]] = field(default_factory=dict)
    by_continuity: dict[str, dict[str, float]] = field(default_factory=dict)
    causes: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    raw_stats: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "n_ticks": self.n_ticks,
            "n_opponent_samples": self.n_opponent_samples,
            "n_games": self.n_games,
            "mean_best_f1": self.mean_best_f1,
            "mean_top1_f1": self.mean_top1_f1,
            "mean_baseline_f1": self.mean_baseline_f1,
            "mean_lift": self.mean_lift,
            "exact_rate": self.exact_rate,
            "suit_match_rate": self.suit_match_rate,
            "best_rank_hist": dict(self.best_rank_hist),
            "by_info_bucket": dict(self.by_info_bucket),
            "by_continuity": dict(self.by_continuity),
            "causes": list(self.causes),
            "recommendations": list(self.recommendations),
            "raw_stats": dict(self.raw_stats),
        }

    def to_markdown(self) -> str:
        d = self.to_dict()
        lines = [
            "# F0010 对手牌预测准确率分析",
            "",
            f"- ticks: **{d['n_ticks']}**  |  opponent-samples: **{d['n_opponent_samples']}**  |  games: **{d['n_games']}**",
            f"- mean best-of-TopK F1: **{d['mean_best_f1']}**",
            f"- mean Top-1 F1: **{d['mean_top1_f1']}**",
            f"- mean random-baseline F1: **{d['mean_baseline_f1']}**",
            f"- mean lift (best − baseline): **{d['mean_lift']}**",
            f"- exact_set rate: **{d['exact_rate']}**",
            f"- main-suit match rate: **{d['suit_match_rate']}**",
            "",
            "## best_rank 分布（最佳匹配落在第几名）",
            "",
        ]
        for k, v in sorted(d["best_rank_hist"].items(), key=lambda x: str(x[0])):
            lines.append(f"- rank {k}: {v}")
        lines += ["", "## 按弃牌信息量分桶（mean best F1）", ""]
        for k, st in sorted(d["by_info_bucket"].items()):
            lines.append(
                f"- {k}: n={int(st.get('n', 0))}  best_f1={st.get('mean_best_f1')}  "
                f"top1={st.get('mean_top1_f1')}  lift={st.get('mean_lift')}"
            )
        lines += ["", "## 连续性 on/off", ""]
        for k, st in sorted(d["by_continuity"].items()):
            lines.append(
                f"- {k}: n={int(st.get('n', 0))}  best_f1={st.get('mean_best_f1')}  "
                f"lift={st.get('mean_lift')}"
            )
        # S0 shanten diagnostics
        rs = d.get("raw_stats") or {}
        lines += ["", "## 向听诊断（S0）", ""]
        lines.append(f"- Top1 向听 MAE: **{rs.get('mean_abs_shanten_err')}**")
        lines.append(
            f"- 有符号误差 mean(pred−true): **{rs.get('mean_signed_shanten_err')}** "
            f"（负=预测偏近听）"
        )
        lines.append(
            f"- 假近听率 (pred ≤ true−2): **{rs.get('fake_near_rate')}**"
        )
        lines.append(
            f"- best-F1 假设的向听 MAE: **{rs.get('mean_abs_shanten_err_best_f1_hyp')}**"
        )
        for ph, st in (rs.get("shanten_mae_by_phase") or {}).items():
            lines.append(
                f"- {ph}: n={int(st.get('n', 0))}  MAE={st.get('mean_abs_shanten_err')}"
            )
        lines += ["", "## 准确率偏低的主要原因", ""]
        for i, c in enumerate(d["causes"], 1):
            lines.append(f"{i}. {c}")
        lines += ["", "## 改进建议", ""]
        for i, c in enumerate(d["recommendations"], 1):
            lines.append(f"{i}. {c}")
        lines.append("")
        return "\n".join(lines)


def _mean(xs: list[float]) -> float | None:
    return round(sum(xs) / len(xs), 4) if xs else None


def analyze_predict_logs(
    paths: Iterable[Path | str] | Path | str,
) -> PredictAnalysis:
    if isinstance(paths, (str, Path)):
        path_list: list[Path | str] = [paths]
    else:
        path_list = list(paths)
    ticks = iter_predict_ticks(path_list)
    return analyze_ticks(ticks)


def analyze_ticks(ticks: list[dict[str, Any]]) -> PredictAnalysis:
    a = PredictAnalysis()
    a.n_ticks = len(ticks)
    games = {t.get("game_id") for t in ticks if t.get("game_id")}
    a.n_games = len(games)

    bests: list[float] = []
    top1s: list[float] = []
    bases: list[float] = []
    lifts: list[float] = []
    exacts: list[float] = []
    suits: list[float] = []
    rank_hist: Counter[str] = Counter()
    bucket_vals: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    cont_vals: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    shanten_abs_err: list[float] = []
    shanten_signed_err: list[float] = []  # pred - true (neg = pred too near)
    fake_near_flags: list[float] = []  # pred <= true - 2
    mae_by_phase: dict[str, list[float]] = defaultdict(list)
    best_hyp_sh_err: list[float] = []  # |sh of best-F1 hyp - true|
    rank1_is_best = 0
    rank1_total = 0

    for t in ticks:
        cont_key = "with_continuity" if t.get("used_continuity") else "cold_start"
        for o in t.get("opponents") or []:
            if o.get("accuracy") is None:
                continue
            a.n_opponent_samples += 1
            bf = float(o["accuracy"])
            bests.append(bf)
            if o.get("top1_f1") is not None:
                top1s.append(float(o["top1_f1"]))
            if o.get("random_baseline_f1") is not None:
                bases.append(float(o["random_baseline_f1"]))
            if o.get("lift_vs_random") is not None:
                lifts.append(float(o["lift_vs_random"]))
            exacts.append(1.0 if o.get("exact_set") else 0.0)
            if o.get("suit_match") is not None:
                suits.append(1.0 if o.get("suit_match") else 0.0)
            br = o.get("best_rank")
            rank_hist[str(br if br is not None else "?")] += 1
            if br is not None:
                rank1_total += 1
                if int(br) == 1:
                    rank1_is_best += 1
            bname = _info_bucket(int(o.get("n_discards") or 0))
            bucket_vals[bname]["best"].append(bf)
            if o.get("top1_f1") is not None:
                bucket_vals[bname]["top1"].append(float(o["top1_f1"]))
            if o.get("lift_vs_random") is not None:
                bucket_vals[bname]["lift"].append(float(o["lift_vs_random"]))
            cont_vals[cont_key]["best"].append(bf)
            if o.get("lift_vs_random") is not None:
                cont_vals[cont_key]["lift"].append(float(o["lift_vs_random"]))
            ts = o.get("true_shanten")
            ps = o.get("pred_top1_shanten")
            if ts is not None and ps is not None:
                err = abs(float(ts) - float(ps))
                shanten_abs_err.append(err)
                shanten_signed_err.append(float(ps) - float(ts))
                fake_near_flags.append(1.0 if float(ps) <= float(ts) - 2.0 else 0.0)
                mae_by_phase[bname].append(err)
                bucket_vals[bname]["sh_mae"].append(err)
            # S0: best-F1 hypothesis shanten vs true
            if ts is not None and o.get("hypotheses"):
                best_h = None
                best_f = -1.0
                for h in o["hypotheses"]:
                    f1 = h.get("f1")
                    if f1 is None:
                        continue
                    if float(f1) > best_f:
                        best_f = float(f1)
                        best_h = h
                if best_h is not None and best_h.get("shanten_est") is not None:
                    best_hyp_sh_err.append(
                        abs(float(best_h["shanten_est"]) - float(ts))
                    )

    a.mean_best_f1 = _mean(bests)
    a.mean_top1_f1 = _mean(top1s)
    a.mean_baseline_f1 = _mean(bases)
    a.mean_lift = _mean(lifts)
    a.exact_rate = _mean(exacts)
    a.suit_match_rate = _mean(suits)
    a.best_rank_hist = dict(rank_hist)
    for k, m in bucket_vals.items():
        a.by_info_bucket[k] = {
            "n": float(len(m["best"])),
            "mean_best_f1": _mean(m["best"]),
            "mean_top1_f1": _mean(m.get("top1", [])),
            "mean_lift": _mean(m.get("lift", [])),
            "mean_abs_shanten_err": _mean(m.get("sh_mae", [])),
        }
    for k, m in cont_vals.items():
        a.by_continuity[k] = {
            "n": float(len(m["best"])),
            "mean_best_f1": _mean(m["best"]),
            "mean_lift": _mean(m.get("lift", [])),
        }
    sh_phase = {
        k: {"n": float(len(v)), "mean_abs_shanten_err": _mean(v)}
        for k, v in sorted(mae_by_phase.items())
    }
    a.raw_stats = {
        "rank1_is_best_rate": (
            round(rank1_is_best / rank1_total, 4) if rank1_total else None
        ),
        "mean_abs_shanten_err": _mean(shanten_abs_err),
        "mean_signed_shanten_err": _mean(shanten_signed_err),
        "fake_near_rate": _mean(fake_near_flags),
        "mean_abs_shanten_err_best_f1_hyp": _mean(best_hyp_sh_err),
        "shanten_mae_by_phase": sh_phase,
        "top1_vs_best_gap": (
            round(a.mean_best_f1 - a.mean_top1_f1, 4)
            if a.mean_best_f1 is not None and a.mean_top1_f1 is not None
            else None
        ),
    }
    a.causes, a.recommendations = _infer_causes(a)
    return a


def _infer_causes(a: PredictAnalysis) -> tuple[list[str], list[str]]:
    causes: list[str] = []
    recs: list[str] = []
    if a.n_opponent_samples == 0:
        return (
            ["无有效带 oracle 的预测样本（未开启预测或未跑评估）。"],
            ["运行 `python tools/eval_hand_predict.py --games 20` 或开座位窗预测打几局。"],
        )

    mb = a.mean_best_f1 or 0.0
    mt = a.mean_top1_f1 or 0.0
    base = a.mean_baseline_f1 or 0.0
    lift = a.mean_lift if a.mean_lift is not None else mb - base

    # Absolute level
    if mb < 0.35:
        causes.append(
            f"整体 best-of-K tile F1 仅约 {mb:.2%}，完整 13 张多重集合匹配本身极难"
            "（搜索空间巨大，等价于在 remain 中猜隐藏多重集合）。"
        )
        recs.append(
            "降低 UI 期望：主指标改为「主攻花色 / 向听区间 / 危险张」分层展示，"
            "完整手牌假设标为「示意」而非「精猜」。"
        )
    elif mb < 0.5:
        causes.append(
            f"best-of-K F1≈{mb:.2%} 仍偏低；完整手牌级预测信息不足是主因之一。"
        )

    # vs random
    if lift < 0.03:
        causes.append(
            f"相对随机基线 lift≈{lift:.3f} 接近 0：当前打分/采样几乎未优于「从 remain 乱抽」。"
            "说明策略/连续性/向听权重对真牌区分度弱。"
        )
        recs.append(
            "加强弃牌时序特征（斩色、现物、中张保留）与定缺后硬约束；"
            "减少与牌理无关的噪声加权。"
        )
    elif lift < 0.08:
        causes.append(
            f"相对随机有微弱增益（lift≈{lift:.3f}），但信号仍弱。"
        )
        recs.append("提高采样 attempts 或改用约束传播/枚举小手牌空间。")

    # ranking
    r1 = (a.raw_stats or {}).get("rank1_is_best_rate")
    gap = (a.raw_stats or {}).get("top1_vs_best_gap")
    if r1 is not None and r1 < 0.35:
        causes.append(
            f"最佳匹配落在 #1 的比例仅 {r1:.1%}：排序/可信度校准差，"
            f"Top-1 F1({mt:.2%}) 明显低于 best-of-K({mb:.2%})，gap={gap}。"
        )
        recs.append(
            "校准场景权重：用 oracle 离线拟合 logistic 或温度缩放；"
            "UI 默认展开 Top-3 而非只强调 #1。"
        )

    # info buckets
    buckets = a.by_info_bucket or {}
    early = buckets.get("early(≤2 disc)", {})
    late = buckets.get("late(7-12 disc)", {}) or buckets.get("deep(>12 disc)", {})
    if early and late:
        e = early.get("mean_best_f1") or 0
        l = late.get("mean_best_f1") or 0
        if l - e < 0.05:
            causes.append(
                f"弃牌增多后准确率提升有限（early {e} → late-ish {l}）："
                "弃牌序列未被有效用于收紧假设。"
            )
            recs.append(
                "实现更强 C1–C4：打出牌必须从假设中扣除并补摸；"
                "早期大量打出的花色在假设中降权到近 0。"
            )
        else:
            causes.append(
                f"信息量分桶显示后期好于早期（{e} → {l}），早期冷启动贡献了平均偏低。"
            )
            recs.append("开局几巡可只显示花色/向听粗粒度，完整 Top-K 延后。")

    # continuity
    cont = a.by_continuity or {}
    if "with_continuity" in cont and "cold_start" in cont:
        cw = cont["with_continuity"].get("mean_best_f1") or 0
        cc = cont["cold_start"].get("mean_best_f1") or 0
        if cw <= cc + 0.01:
            causes.append(
                f"启用 prev_joints 连续性后 F1（{cw}）未显著高于冷启动（{cc}）："
                "连续演化路径过窄或常被 residual 采样淹没。"
            )
            recs.append(
                "提高连续性分支权重与候选保留数；"
                "丢弃无法 C1 的旧场景而非混入大量新鲜随机场景。"
            )

    # suit
    if a.suit_match_rate is not None and a.suit_match_rate < 0.45:
        causes.append(
            f"主攻花色一致率仅 {a.suit_match_rate:.1%}：策略信念/花色先验偏差大。"
        )
        recs.append("先优化「一门颜色」分类准确率，再细化具体张。")

    # shanten
    se = (a.raw_stats or {}).get("mean_abs_shanten_err")
    if se is not None and se > 1.5:
        causes.append(
            f"预测向听与真实向听平均绝对误差≈{se}：听牌方向约束未对齐真牌结构。"
        )
        recs.append("用真实向听分布做软标签；副露后手牌张数/搭子结构约束加严。")

    # exact
    if a.exact_rate is not None and a.exact_rate < 0.01:
        causes.append(
            f"exact_set 命中率≈{a.exact_rate:.2%}（预期极低）："
            "不宜用「整手全中」衡量算法；tile F1 / 花色 / 向听更合适。"
        )
        recs.append("文档与 UI 准确度说明改为「牌张重合度」，避免误解为猜中整副牌。")

    if not causes:
        causes.append("样本显示准确率处于可解释区间，未见单一压倒性故障。")
    if not recs:
        recs.append("继续积累更多局日志后复跑分析。")
    return causes, recs


def write_analysis_report(
    analysis: PredictAnalysis,
    out_path: Path | str,
) -> Path:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(analysis.to_markdown(), encoding="utf-8")
    side = path.with_suffix(".json")
    side.write_text(
        json.dumps(analysis.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path
