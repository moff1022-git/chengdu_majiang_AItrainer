"""F0011: integrated discard advisor — offense + defense + junk safety.

Combines F0010 joint scenes, remain_eff, shanten/ukeire, fan proxy, deal-in risk.
Default off at pipeline; enable via use_f0011=True.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Sequence

from engine.action import Action, ActionType
from engine.hand_utils import melds_from_raw
from engine.shanten import shanten as compute_shanten
from engine.state import GameState
from engine.tile import Tile, parse_tile
from players.analysis.danger import DANGER_PENALTY
from players.analysis.hand_predict import (
    _combo_association,
    _dumped_suits,
    _disc_phase,
    predict_joint_scenes,
    JointHandScene,
)
from players.analysis.remain import remain_map, ukeire_count
from players.analysis.types import DiscardAdvice, OpponentHint

# --- phase by wall remaining (self-centric) ---
def self_phase(wall_n: int) -> str:
    if wall_n >= 70:
        return "early"
    if wall_n >= 40:
        return "mid"
    return "late"


# attack / defense / junk weights by phase
_WEIGHTS = {
    "early": {"sh": 4.0, "uke": 0.18, "fan": 0.15, "break": 0.55, "fang": 0.7, "fei": 0.35},
    "mid": {"sh": 4.2, "uke": 0.20, "fan": 0.35, "break": 0.40, "fang": 1.2, "fei": 0.55},
    "late": {"sh": 5.0, "uke": 0.22, "fan": 0.55, "break": 0.25, "fang": 2.0, "fei": 0.65},
}


@dataclass
class F0010Context:
    scenes: list[JointHandScene] = field(default_factory=list)
    dumps: dict[int, set[str]] = field(default_factory=dict)  # seat -> dumped suits
    waits: dict[int, dict[str, float]] = field(default_factory=dict)
    # seat -> tile_id -> probability mass (weighted over scenes)
    remain_eff: dict[str, int] = field(default_factory=dict)
    public_discards: set[str] = field(default_factory=set)


def build_f0010_context(
    state: GameState,
    self_seat: int,
    *,
    top_k: int = 3,
    seed: int | None = 0,
) -> F0010Context:
    """A1 raw material: joint scenes → dumps, waits, remain_eff."""
    remain = remain_map(state, self_seat)
    scenes = predict_joint_scenes(
        state, self_seat, top_k=max(1, min(5, top_k)), seed=seed
    )
    ctx = F0010Context(scenes=list(scenes), remain_eff=dict(remain))
    # public discards (all rivers)
    for p in state.players:
        for t in p.discard_pile:
            ctx.public_discards.add(t.id)
        for m in melds_from_raw(p.melds):
            ctx.public_discards.add(m.tile.id)

    # dumps from visible discard timeline (not only from scenes)
    for p in state.players:
        if p.seat == self_seat or p.status != "active":
            continue
        disc = [t.id for t in p.discard_pile]
        ph = _disc_phase(len(disc))
        ctx.dumps[p.seat] = _dumped_suits(disc, ph)

    # weighted waits + occupancy for remain_eff
    waits_acc: dict[int, Counter] = {}
    occ: Counter = Counter()  # tid -> expected count in all opp hands
    w_sum = sum(max(0.0, sc.confidence) for sc in scenes) or 1.0
    for sc in scenes:
        wk = max(0.0, sc.confidence) / w_sum
        for seat, tiles in sc.hands.items():
            for tid in tiles:
                occ[tid] += wk
            # tenpai waits if shanten==0
            sh_est = (sc.shanten_est or {}).get(seat)
            if sh_est is not None and int(sh_est) == 0 and tiles:
                try:
                    hand = [parse_tile(x) for x in tiles]
                    p = state.players[seat]
                    melds = melds_from_raw(p.melds)
                    dq = p.dingque
                    res = compute_shanten(hand, melds, dq)
                    if res.shanten == 0 and res.ukeire:
                        waits_acc.setdefault(seat, Counter())
                        for u in res.ukeire:
                            waits_acc[seat][u.id] += wk
                except Exception:
                    pass
            elif tiles:
                # weak: neighbor of held tiles as soft danger (一向听热区 proxy)
                for tid in set(tiles):
                    try:
                        t = parse_tile(tid)
                        for dr in (-1, 1):
                            r = t.rank + dr
                            if 1 <= r <= 9:
                                nid = f"{t.suit.value}_{r}"
                                waits_acc.setdefault(seat, Counter())
                                waits_acc[seat][nid] += 0.15 * wk
                    except Exception:
                        pass

    for seat, ctr in waits_acc.items():
        total = sum(ctr.values()) or 1.0
        ctx.waits[seat] = {tid: v / total for tid, v in ctr.items()}

    # remain_eff: hidden pool minus expected opponent occupancy
    for tid, n in remain.items():
        ctx.remain_eff[tid] = max(0, int(round(n - float(occ.get(tid, 0.0)))))
    return ctx


def ron_probability(tile_id: str, ctx: F0010Context) -> float:
    """Approximate P(deal-in) if discarding tile_id."""
    p = 0.0
    for seat, wmap in ctx.waits.items():
        p += float(wmap.get(tile_id, 0.0))
    return min(1.0, p)


def rate_danger_f0011(tile_id: str, ctx: F0010Context, opponents: list[OpponentHint]) -> str:
    """A1: danger levels using F0010-weighted waits +现物."""
    pr = ron_probability(tile_id, ctx)
    in_disc = tile_id in ctx.public_discards
    max_op = max((o.tenpai_prob for o in opponents), default=0.0)
    if pr >= 0.35 or (pr >= 0.2 and max_op >= 0.55):
        return "critical"
    if pr >= 0.18 or (pr >= 0.1 and not in_disc and max_op >= 0.4):
        return "high"
    if pr >= 0.08 or (max_op >= 0.55 and not in_disc):
        return "medium"
    if in_disc:
        return "safe" if pr < 0.05 else "low"
    if pr < 0.03:
        return "low"
    return "unknown"


def s_fei(tile_id: str, ctx: F0010Context) -> float:
    """A2: junk / opponent-unwanted score (higher = safer to discard)."""
    score = 0.0
    if tile_id in ctx.public_discards:
        score += 1.2  # 现物
    # dumped suits across opponents
    try:
        su = parse_tile(tile_id).suit.value
    except Exception:
        su = ""
    for seat, dumps in ctx.dumps.items():
        if su and su in dumps:
            score += 0.9
    # not in high-weight scene hands
    if ctx.scenes:
        w_sum = sum(max(0.0, sc.confidence) for sc in ctx.scenes) or 1.0
        not_in = 0.0
        for sc in ctx.scenes:
            wk = max(0.0, sc.confidence) / w_sum
            held = any(tile_id in (sc.hands.get(s) or []) for s in sc.hands)
            if not held:
                not_in += wk
        score += 0.7 * not_in
    # not a weighted wait
    pr = ron_probability(tile_id, ctx)
    score += 0.8 * (1.0 - min(1.0, pr * 3.0))
    return score


def fan_proxy_after(
    hand: list[Tile],
    melds: list,
    dingque,
) -> float:
    """A4: cheap expected-fan proxy (0..~6), not full fan table."""
    try:
        ids = [t.id for t in hand]
        if dingque is not None:
            dq = dingque.value if hasattr(dingque, "value") else str(dingque)
            ids = [i for i in ids if not i.startswith(dq + "_")]
        if not ids:
            return 0.0
        suit_cnt: Counter = Counter(i.split("_", 1)[0] for i in ids)
        main_n = max(suit_cnt.values()) if suit_cnt else 0
        conc = main_n / max(1, len(ids))
        # 清一色进度
        qing = 2.5 * max(0.0, conc - 0.45) / 0.55
        # 对子/刻子密度
        c = Counter(ids)
        pairs = sum(1 for v in c.values() if v >= 2)
        trips = sum(1 for v in c.values() if v >= 3)
        pongish = 0.35 * pairs + 0.55 * trips
        # 中张
        mid = 0
        for i in ids:
            try:
                r = int(i.split("_", 1)[1])
                if 3 <= r <= 7:
                    mid += 1
            except Exception:
                pass
        mid_s = 0.4 * (mid / max(1, len(ids)))
        open_n = len(melds or [])
        open_b = 0.25 * open_n  # 副露碰碰倾向
        return float(min(6.0, qing + pongish + mid_s + open_b))
    except Exception:
        return 0.0


def break_cost(hand: list[Tile], tile_id: str, dingque) -> float:
    """Cost of discarding a combo-linked tile (higher = worse to break)."""
    dq = None
    if dingque is not None:
        dq = dingque.value if hasattr(dingque, "value") else str(dingque)
    ids = [t.id for t in hand if t.id != tile_id or True]
    # hand without one copy of tile_id
    rest: list[str] = []
    removed = False
    for t in hand:
        if not removed and t.id == tile_id:
            removed = True
            continue
        rest.append(t.id)
    return _combo_association(tile_id, rest, dq)


def _remove_one(hand: list[Tile], tile_id: str) -> list[Tile]:
    out: list[Tile] = []
    removed = False
    for t in hand:
        if not removed and t.id == tile_id:
            removed = True
            continue
        out.append(t)
    return out


def _candidate_ids(
    hand: list[Tile],
    legal_discards: Sequence[Action] | None,
) -> list[str]:
    if legal_discards is not None:
        cands: list[str] = []
        for a in legal_discards:
            if a.type == ActionType.DISCARD and a.tiles:
                cands.append(a.tiles[0].id)
        seen: set[str] = set()
        out: list[str] = []
        for tid in cands:
            if tid not in seen:
                seen.add(tid)
                out.append(tid)
        return out
    seen = set()
    out = []
    for t in hand:
        if t.id not in seen:
            seen.add(t.id)
            out.append(t.id)
    return out


def rank_discards_f0011(
    state: GameState,
    seat: int,
    hand: list[Tile],
    melds: list,
    dingque,
    opponents: list[OpponentHint],
    *,
    legal_discards: Sequence[Action] | None = None,
    f0010_top_k: int = 3,
    seed: int | None = 0,
) -> list[DiscardAdvice]:
    """Full A1–A4 integrated ranking."""
    tile_ids = _candidate_ids(hand, legal_discards)
    if not tile_ids:
        return []
    wall_n = len(state.wall or [])
    phase = self_phase(wall_n)
    W = _WEIGHTS[phase]
    # late wall boost defense
    fang_scale = 1.0
    if wall_n < 30:
        fang_scale = 1.75
    elif wall_n < 50:
        fang_scale = 1.35

    ctx = build_f0010_context(state, seat, top_k=f0010_top_k, seed=seed)
    remain_eff = ctx.remain_eff or remain_map(state, seat)

    scored: list[tuple[float, DiscardAdvice, dict[str, float]]] = []
    for tid in tile_ids:
        trial = _remove_one(hand, tid)
        try:
            sres = compute_shanten(trial, melds, dingque)
            sh_after = int(sres.shanten)
            uke_ids = [t.id for t in (sres.ukeire or [])]
            uke_n = ukeire_count(uke_ids, remain_eff)
        except Exception:
            sh_after = 8
            uke_n = 0
            uke_ids = []
        fang_lvl = rate_danger_f0011(tid, ctx, opponents)
        s_fang = DANGER_PENALTY.get(fang_lvl, 0.5) * fang_scale
        s_fei_v = s_fei(tid, ctx)
        s_break = break_cost(hand, tid, dingque)
        s_fan = fan_proxy_after(trial, melds, dingque)
        s_gong = (
            -W["sh"] * sh_after
            + W["uke"] * uke_n
            + W["fan"] * s_fan
            - W["break"] * s_break
        )
        total = s_gong - W["fang"] * s_fang + W["fei"] * s_fei_v
        detail = {
            "s_gong": round(s_gong, 4),
            "s_fang": round(s_fang, 4),
            "s_fei": round(s_fei_v, 4),
            "fan_proxy": round(s_fan, 4),
            "break_cost": round(s_break, 4),
            "ukeire_eff": float(uke_n),
            "ron_p": round(ron_probability(tid, ctx), 4),
            "phase": phase,
        }
        scored.append(
            (
                total,
                DiscardAdvice(
                    tile_id=tid,
                    rank=0,
                    shanten_after=sh_after,
                    ukeire_after=uke_n,
                    danger=fang_lvl,
                    score=total,
                    mark="none",
                    ukeire_tiles=list(uke_ids),
                ),
                detail,
            )
        )

    scored.sort(key=lambda x: (-x[0], x[1].tile_id))
    out: list[DiscardAdvice] = []
    for i, (total, adv, detail) in enumerate(scored):
        mark = "none"
        if i == 0:
            mark = "best"
        elif i == 1:
            mark = "second"
        if adv.danger in ("critical", "high") and mark != "best":
            mark = "avoid"
        # attach detail on object if possible
        a = DiscardAdvice(
            tile_id=adv.tile_id,
            rank=i + 1,
            shanten_after=adv.shanten_after,
            ukeire_after=adv.ukeire_after,
            danger=adv.danger,
            score=round(total, 4),
            mark=mark,
            ukeire_tiles=list(adv.ukeire_tiles or []),
        )
        setattr(a, "f0011_detail", detail)
        out.append(a)
    return out
