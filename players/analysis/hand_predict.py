"""Opponent hand-shape Top-K prediction v2.2: beam joint search + refine (raise F1)."""

from __future__ import annotations

import math
import random
from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Any

from engine.hand_utils import MeldView, melds_from_raw
from engine.shanten import shanten as compute_shanten
from engine.state import GameState
from engine.tile import Suit, Tile, parse_tile
from players.analysis.remain import remain_map

DEFAULT_TOP_K = 5
# Softmax temperature for confidence display (lower = sharper top-1)
# L3.1 I2: phase-split temperatures (default mid-ish for legacy callers)
_CONF_TEMPERATURE = 0.45
MID_CONF_TEMPERATURE = 0.50  # L3.1: flatter mid conf
LATE_CONF_TEMPERATURE = 0.35  # L3.1: sharper late conf
# Continuity joint weight multiplier vs fresh samples (keep modest: early errors stick)
_CONTINUITY_WEIGHT_MULT = 1.35
# L1: late continuity stronger
LATE_CONTINUITY_WEIGHT_MULT = 1.6  # L1.3 F4
LATE_CONT_DISCARD_BONUS = 1.7  # L1.3 F5/F6 (was 1.55)
MID_CONT_DISCARD_BONUS = 1.55
LATE_CONT_MUTATIONS = 10  # L1.4 F8
LATE_CONT_PREV_EXTRA = 6  # prev scenes = top_k + this
J6_OTHER_DISCARD_HOLD_PENALTY = 0.12  # L1.5 soft per held copy of just-discarded id
# Early-game coarse UI threshold (max discards among opponents)
EARLY_DISCARD_THRESHOLD = 2
# v2.2: ensemble + MC for tile-F1; beam auxiliary
_BEAM_WIDTH = 4
_BEAM_SAMPLES = 8
_REFINE_SWAPS = 4
_DIVERSE_MMR = 0.28  # legacy default; L3 uses EARLY/MID/LATE_MMR
# L3.2 I3: phase MMR (higher → more diversity / less trust score)
EARLY_MMR = 0.55
MID_MMR = 0.40
LATE_MMR = 0.15
# L3.3 I4: late final blend (fast suit/timeline vs slow shanten)
# Tune 2026-07-12: 0.70/0.30 slightly hurt late best on set20 → pull back toward L2
LATE_BLEND_FAST = 0.76
LATE_BLEND_SHANTEN = 0.24
_MC_JOINTS = 90
_PRESELECT = 64

# --- F0010-ML M1: mid-phase bleed stop (Approved plan) ---
# Phase by *that opponent's* discard count (matches eval buckets)
MID_DISC_LO = 3
MID_DISC_HI = 6
LATE_DISC_LO = 7
MID_USE_QUOTA = False  # M1.1 D6
MID_UNIFORM_RATIO = 0.5  # M1.4 H3
MID_SHARE_INFO_DIV = 12.0  # M1.2 C4c (was effectively /8)
MID_EXTRA_PRESSURE_PENALTY = False  # M1.3 C4d off in mid
MID_ATTACK_WEIGHT_SCALE = 0.5  # M1.5 D3 half attack boost
MID_FORCE_DUAL_PREFER = True  # M1.5 B5

# --- F0010-ML M2: verifiable dump-suit (斩色) constraints ---
DUMP_SUIT_COUNT_MID = 3  # M2.1 K mid
# M2 tune: late K=2 too aggressive on random discards → false 斩色 hurt late F1
DUMP_SUIT_COUNT_LATE = 3  # was 2; align with mid (need clearer dump evidence)
DUMP_SUIT_RECENT_WINDOW = 6
DUMP_SUIT_HAND_CAP = 1  # prefer ≤1 tile of dumped suit in hand
DUMP_SUIT_SHARE_CAP = 1.0 / 13.0  # expected share hard top
DUMP_SUIT_HOLD_PENALTY = 0.12  # per excess tile over HAND_CAP
DUMP_SUIT_PICK_FLOOR_MID = 0.05  # M2.2
DUMP_SUIT_PICK_FLOOR_LATE = 0.02  # M2.2
DUMP_SUIT_PICK_MULT = 0.12  # extra mult when sampling dumped suit
MULTI_DISCARD_ID_SOFT = 0.1  # M2.3 Q2: disc_cnt≥2 soft (not hard ban)
STREAK_DUMP_LEN = 3  # M2.4 trailing consecutive same-suit discards
STREAK_HOLD_CAP = 2
STREAK_HOLD_PENALTY = 0.15
# need ≥ this many of the suit in recent window (was 2; raise → fewer false dumps)
DUMP_SUIT_RECENT_MIN = 3

# --- F0010-DH: discard ↔ hand association (exclude dingque) ---
# early: high combo_assoc → penalty; mid/late: high tenpai_assoc → penalty
DH_EARLY_COMBO_PENALTY = 0.60
DH_MID_TENPAI_PENALTY = 0.55
DH_LATE_TENPAI_PENALTY = 0.70
DH_MIN_MULT = 0.12  # floor for weight multiplier

# --- F0010-ML L2: late/deep shanten target + structure ---
# Empirical mean true_shanten by n_disc (set20+set50 fixed-set logs); index = n_disc
# n_disc≥13 reuse last entry. Meld relief is design prior (few open-meld samples).
TARGET_SHANTEN_BY_DISC: tuple[float, ...] = (
    7.7,
    7.0,
    6.1,
    5.0,
    4.1,
    3.4,
    3.0,  # 0–6 early/mid
    2.5,
    2.2,
    2.1,
    1.9,
    1.8,
    1.6,
    1.6,  # 7–13 late/deep
)
TARGET_SHANTEN_MELD_RELIEF = 0.85  # per open meld
LATE_STRUCTURE_MULT = 1.2  # L2.4 G1: amplify structure bonus only late/deep
LATE_SHANTEN_PENALTY_GE3 = 0.78  # L2.3 G5
LATE_SHANTEN_PENALTY_GE4 = 0.65
LATE_TENPAI_BONUS_BASE = 1.22
LATE_TENPAI_BONUS_LATE_K = 0.35

# --- F0010-ML L3.4 I6: dump-suit compliance (independent of prefer/conc) ---
DUMP_COMPLY_EMPTY = 1.12  # hold 0 of dumped suit
DUMP_COMPLY_AT_CAP = 1.0  # hold ≤ HAND_CAP
DUMP_COMPLY_EXCESS = 0.72  # per tile over HAND_CAP
DUMP_COMPLY_LATE_BOOST = 1.05  # extra ranking tilt late/deep when any dump signal

# --- F0010-S S1: late candidate quality / fake-near-tenpai gates ---
SHANTEN_FAKE_NEAR_DELTA = 2.0  # sh < target - DELTA → suspicious
LATE_STRUCT_FLOOR = 1.08  # structure_score below this is "too weak"
LATE_STRUCT_FLOOR_MULT = 0.30  # S1.4
S1_FAKE_NEAR_SCORE_MULT = 0.22  # heavy soft reject in scoring
S1_RESAMPLE_MAX = 2  # regen / sample retries
S1_LOW_CONC = 0.32  # main-suit concentration threshold for fake-near gate

# --- F0010-S S2: trusted shanten scoring + J4 continuity ---
J4_SHANTEN_WORSEN_TOL = 1  # allow sh to worsen by at most this after discard evolve
J4_WORSEN_SOFT = 0.40  # S2.1 soft mult when sh worsens too much
S_TRUST_TAU = 1.5  # |sh-target| within → full sh term
S_TRUST_OUTSIDE_SCALE = 0.35  # dampen sh term toward 1.0 when outside τ
S2_FAKE_NEAR_EXTRA = 0.55  # S2.3 when sh <= target - DELTA (late)
# LATE_BLEND_SHANTEN stays 0.24 (S2.4)


@dataclass
class OpponentHandHypothesis:
    rank: int
    tiles: list[str]
    confidence: float
    label: str = ""
    scene_id: int = 0
    shanten_est: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class OpponentHandForecast:
    seat: int
    hypotheses: list[OpponentHandHypothesis] = field(default_factory=list)
    accuracy: float | None = None
    accuracy_detail: dict = field(default_factory=dict)
    strategy_hint: str = ""

    def to_dict(self) -> dict:
        return {
            "seat": self.seat,
            "hypotheses": [h.to_dict() for h in self.hypotheses],
            "accuracy": self.accuracy,
            "accuracy_detail": dict(self.accuracy_detail or {}),
            "strategy_hint": self.strategy_hint,
        }


@dataclass
class JointHandScene:
    """One mutually exclusive assignment of hands to all opponents."""

    scene_id: int
    confidence: float
    hands: dict[int, list[str]]  # seat -> sorted tiles
    labels: dict[int, str] = field(default_factory=dict)
    shanten_est: dict[int, int | None] = field(default_factory=dict)
    weight: float = 0.0


@dataclass
class StrategyBelief:
    """Soft weights over simple play styles (sum not required to be 1)."""

    attack_clear: float = 1.0  # 攻一门
    dump_dingque: float = 1.0  # 先打定缺
    safe_fold: float = 1.0  # 防守向
    fast_meld: float = 1.0  # 快副露

    def dominant_label(self) -> str:
        items = [
            ("攻一门", self.attack_clear),
            ("打定缺", self.dump_dingque),
            ("防守", self.safe_fold),
            ("快副露", self.fast_meld),
        ]
        items.sort(key=lambda x: -x[1])
        return items[0][0] if items[0][1] > 0.01 else ""


def expected_hand_count(state: GameState, seat: int) -> int:
    p = state.players[seat]
    if p.status != "active":
        return 0
    n_melds = len(melds_from_raw(p.melds))
    base = 13 - 3 * n_melds
    if (
        state.phase == "discard"
        and state.current_seat == seat
        and getattr(state, "last_draw_tile", None) is not None
    ):
        base += 1
    return max(0, base)


def _hand_count_from_view(view: dict, seat: int) -> int:
    for p in view.get("players") or []:
        if int(p.get("seat", -1)) == seat:
            try:
                return max(0, int(p.get("hand_count", 13)))
            except (TypeError, ValueError):
                return 13
    return 13


def _player_status(view_or_state, seat: int) -> str:
    if isinstance(view_or_state, GameState):
        return str(view_or_state.players[seat].status)
    for p in view_or_state.get("players") or []:
        if int(p.get("seat", -1)) == seat:
            return str(p.get("status") or "active")
    return "active"


def _dingque_suit(view_or_state, seat: int) -> str | None:
    if isinstance(view_or_state, GameState):
        dq = view_or_state.players[seat].dingque
        return dq.value if dq is not None else None
    for p in view_or_state.get("players") or []:
        if int(p.get("seat", -1)) == seat:
            dq = p.get("dingque")
            return str(dq) if dq else None
    return None


def _meld_count(view_or_state, seat: int) -> int:
    if isinstance(view_or_state, GameState):
        return len(melds_from_raw(view_or_state.players[seat].melds))
    for p in view_or_state.get("players") or []:
        if int(p.get("seat", -1)) == seat:
            return len(p.get("melds") or [])
    return 0


def _discard_ids(view_or_state, seat: int) -> list[str]:
    if isinstance(view_or_state, GameState):
        return [t.id for t in view_or_state.players[seat].discard_pile]
    for p in view_or_state.get("players") or []:
        if int(p.get("seat", -1)) == seat:
            out = []
            for t in p.get("discard_pile") or []:
                if isinstance(t, str):
                    out.append(t)
                elif isinstance(t, dict) and t.get("id"):
                    out.append(str(t["id"]))
                elif isinstance(t, dict) and t.get("suit") is not None:
                    out.append(f"{t.get('suit')}_{t.get('rank')}")
            return out
    return []


def _remain_from_view(view: dict, self_seat: int) -> dict[str, int]:
    remain = {f"{su}_{r}": 4 for su in ("wan", "tong", "tiao") for r in range(1, 10)}
    for p in view.get("players") or []:
        for t in p.get("discard_pile") or []:
            tid = t if isinstance(t, str) else (
                t.get("id") if isinstance(t, dict) else None
            )
            if tid and tid in remain:
                remain[tid] = max(0, remain[tid] - 1)
        for m in p.get("melds") or []:
            if not isinstance(m, dict):
                continue
            tid = m.get("tile_id") or m.get("id")
            if not tid:
                continue
            n = 4 if "gang" in str(m.get("kind", "")).lower() else 3
            remain[tid] = max(0, remain.get(tid, 4) - n)
        if int(p.get("seat", -1)) == self_seat:
            for tid in p.get("hand") or []:
                if isinstance(tid, str) and tid in remain:
                    remain[tid] = max(0, remain[tid] - 1)
    return remain


def estimate_strategy(
    discards: list[str],
    *,
    dingque: str | None,
    n_melds: int,
) -> StrategyBelief:
    """Online soft beliefs from discard timeline + melds."""
    bel = StrategyBelief()
    if not discards and n_melds == 0:
        return bel
    suit_cnt: Counter[str] = Counter()
    for tid in discards:
        try:
            suit_cnt[parse_tile(tid).suit.value] += 1
        except Exception:
            pass
    n = max(1, len(discards))
    if dingque:
        early = discards[: max(3, n // 2)]
        dq_n = sum(1 for t in early if t.startswith(dingque + "_"))
        bel.dump_dingque = 1.0 + 3.0 * (dq_n / max(1, len(early)))
    if suit_cnt:
        held_bias = []
        for su in ("wan", "tong", "tiao"):
            if dingque and su == dingque:
                continue
            held_bias.append(1.0 - suit_cnt.get(su, 0) / n)
        if held_bias:
            bel.attack_clear = 1.0 + 3.0 * max(held_bias)
    if n >= 8 and n_melds <= 1:
        bel.safe_fold = 1.0 + 0.18 * n
    bel.fast_meld = 1.0 + 1.4 * n_melds
    return bel


def _suit_of(tid: str) -> str:
    try:
        return parse_tile(tid).suit.value
    except Exception:
        parts = str(tid).split("_", 1)
        return parts[0] if parts else ""


def _suit_label_short(su: str) -> str:
    return {"wan": "万", "tong": "筒", "tiao": "条"}.get(su, su)


def _disc_phase(n_disc: int) -> str:
    """early / mid / late by opponent discard count (deep folds into late for M1)."""
    if n_disc < MID_DISC_LO:
        return "early"
    if n_disc <= MID_DISC_HI:
        return "mid"
    return "late"


def _prefer_suits_for_strategy(
    discards: list[str],
    dingque: str | None,
    bel: StrategyBelief,
    *,
    force_dual: bool | None = None,
) -> list[str]:
    suit_cnt: Counter[str] = Counter()
    for tid in discards:
        su = _suit_of(tid)
        if su:
            suit_cnt[su] += 1
    candidates = [s for s in ("wan", "tong", "tiao") if s != dingque]
    # least discarded first = held / attack suit
    candidates.sort(key=lambda s: (suit_cnt.get(s, 0), s))
    if not candidates:
        return []
    n_disc = len(discards)
    phase = _disc_phase(n_disc)
    # M2: never prefer a 斩色 suit if alternatives exist
    dumped = _dumped_suits(discards, phase)
    non_dump = [s for s in candidates if s not in dumped]
    if non_dump:
        candidates = non_dump
    if force_dual is None:
        force_dual = MID_FORCE_DUAL_PREFER and phase == "mid"
    # M1.5: mid always keep up to 2 colors (don't collapse to single attack suit)
    if force_dual:
        return candidates[:2] if len(candidates) >= 2 else candidates
    if bel.attack_clear >= bel.safe_fold * 0.9:
        return candidates[:1]
    return candidates[:2]


def _discard_suit_pressure(discards: list[str]) -> dict[str, float]:
    """Higher = more evidence the player is dumping that suit (should not hold)."""
    pressure = {s: 0.0 for s in ("wan", "tong", "tiao")}
    if not discards:
        return pressure
    early_n = max(3, len(discards) // 2)
    for i, tid in enumerate(discards):
        su = _suit_of(tid)
        if su not in pressure:
            continue
        # early discards weigh more
        w = 1.6 if i < early_n else 1.0
        pressure[su] += w
    # normalize by discards
    scale = max(1.0, float(len(discards)))
    return {s: p / scale for s, p in pressure.items()}


def _dumped_suits(discards: list[str], phase: str | None = None) -> set[str]:
    """M2.1 斩色: suit count ≥ K and still appears in recent discard window.

    K = DUMP_SUIT_COUNT_MID (3) in mid, DUMP_SUIT_COUNT_LATE (2) in late.
    Early: empty (too little evidence).
    """
    if not discards:
        return set()
    n = len(discards)
    phase = phase or _disc_phase(n)
    if phase == "early":
        return set()
    k = DUMP_SUIT_COUNT_MID if phase == "mid" else DUMP_SUIT_COUNT_LATE
    cnt: Counter[str] = Counter()
    for tid in discards:
        su = _suit_of(tid)
        if su in ("wan", "tong", "tiao"):
            cnt[su] += 1
    recent = discards[-DUMP_SUIT_RECENT_WINDOW:]
    recent_cnt: Counter[str] = Counter()
    for t in recent:
        su = _suit_of(t)
        if su in ("wan", "tong", "tiao"):
            recent_cnt[su] += 1
    out: set[str] = set()
    for su, c in cnt.items():
        # total ≥ K and actively discarding that suit recently (≥2 in window)
        if c >= k and recent_cnt.get(su, 0) >= DUMP_SUIT_RECENT_MIN:
            out.add(su)
    return out


def _streak_dumped_suits(discards: list[str]) -> set[str]:
    """M2.4: trailing consecutive run of same suit length ≥ STREAK_DUMP_LEN."""
    if len(discards) < STREAK_DUMP_LEN:
        return set()
    su = _suit_of(discards[-1])
    if su not in ("wan", "tong", "tiao"):
        return set()
    run = 0
    for tid in reversed(discards):
        if _suit_of(tid) == su:
            run += 1
        else:
            break
    if run >= STREAK_DUMP_LEN:
        return {su}
    return set()


def _expected_suit_share(
    discards: list[str],
    dingque: str | None,
    prefer: list[str],
    strategy: StrategyBelief,
) -> dict[str, float]:
    """Target fraction of hand per suit from public timeline."""
    suits = [s for s in ("wan", "tong", "tiao") if s != dingque]
    if not suits:
        return {"wan": 0.34, "tong": 0.33, "tiao": 0.33}
    pressure = _discard_suit_pressure(discards)
    phase = _disc_phase(len(discards))
    atk_scale = MID_ATTACK_WEIGHT_SCALE if phase == "mid" else 1.0
    dumped = _dumped_suits(discards, phase)
    raw: dict[str, float] = {}
    for s in suits:
        # inverse dump pressure
        raw[s] = max(0.05, 1.2 - 1.4 * pressure.get(s, 0.0))
        if prefer and s == prefer[0]:
            # M1.5: mid halves attack-driven share prior
            raw[s] *= 1.0 + 0.55 * strategy.attack_clear * atk_scale
        elif prefer and s in prefer:
            raw[s] *= 1.15 if phase != "mid" else 1.08
        # M2.1: 斩色 near-zero prior before normalize
        if s in dumped:
            raw[s] = min(raw[s], 0.02)
    total = sum(raw.values()) or 1.0
    shares = {s: raw[s] / total for s in suits}
    # M2.1 hard cap dumped share; renorm only non-dumped mass to fill rest
    for s in dumped:
        if s in shares:
            shares[s] = min(shares[s], DUMP_SUIT_SHARE_CAP)
    rest = [s for s in suits if s not in dumped]
    dumped_mass = sum(shares.get(s, 0.0) for s in dumped if s in shares)
    remain_mass = max(0.0, 1.0 - dumped_mass)
    rst = sum(shares.get(s, 0.0) for s in rest) or 1.0
    for s in rest:
        shares[s] = shares.get(s, 0.0) / rst * remain_mass
    if dingque:
        shares[dingque] = 0.0
    return shares


def _structure_score(tiles: list[str]) -> float:
    """Favor pair / sequence-like density (cheap proxy for mahjong structure)."""
    if not tiles:
        return 1.0
    c = Counter(tiles)
    pairs = sum(1 for v in c.values() if v >= 2)
    trips = sum(1 for v in c.values() if v >= 3)
    # adjacency in same suit
    by_suit: dict[str, list[int]] = {"wan": [], "tong": [], "tiao": []}
    for tid in tiles:
        su = _suit_of(tid)
        try:
            r = int(str(tid).split("_", 1)[1])
        except Exception:
            continue
        if su in by_suit:
            by_suit[su].append(r)
    adj = 0
    for ranks in by_suit.values():
        sset = set(ranks)
        for r in sset:
            if (r + 1) in sset:
                adj += 1
            if (r + 2) in sset and (r + 1) not in sset:
                adj += 0.35  # weak gap chow potential
    n = max(1, len(tiles))
    return 1.0 + 0.12 * pairs + 0.18 * trips + 0.06 * adj / n * 13.0


def _target_shanten(n_disc: int, n_melds: int) -> float:
    """L2.1 C5b: empirical target shanten by discard count (+ meld relief)."""
    if n_disc < 0:
        n_disc = 0
    idx = min(int(n_disc), len(TARGET_SHANTEN_BY_DISC) - 1)
    base = TARGET_SHANTEN_BY_DISC[idx]
    return max(0.0, float(base) - TARGET_SHANTEN_MELD_RELIEF * max(0, int(n_melds)))


def _main_suit_concentration(tiles: list[str], prefer: list[str], dumped: set[str]) -> float:
    if not tiles:
        return 0.0
    prefer_eff = [s for s in prefer if s not in dumped] or prefer
    if not prefer_eff:
        return 0.0
    main = prefer_eff[0]
    hist = Counter(_suit_of(t) for t in tiles if _suit_of(t))
    return hist.get(main, 0) / max(1, len(tiles))


def _is_suspicious_fake_near(
    tiles: list[str],
    *,
    sh: int | None,
    n_disc: int,
    n_melds: int,
    discards: list[str],
    ban_suit: str | None,
    strategy: StrategyBelief,
    phase: str,
) -> bool:
    """S1.1: late/deep sh much better than target + weak timeline/structure signal."""
    if phase not in ("late", "deep") or sh is None:
        return False
    target = _target_shanten(n_disc, n_melds)
    if float(sh) >= target - SHANTEN_FAKE_NEAR_DELTA:
        return False
    dumped = _dumped_suits(discards, phase)
    prefer = _prefer_suits_for_strategy(discards, ban_suit, strategy)
    conc = _main_suit_concentration(tiles, prefer, dumped)
    hist = Counter(_suit_of(t) for t in tiles if _suit_of(t))
    dump_hold = any(hist.get(su, 0) > DUMP_SUIT_HAND_CAP for su in dumped)
    struct = _structure_score(tiles)
    weak_struct = struct < LATE_STRUCT_FLOOR
    low_conc = conc < S1_LOW_CONC
    return bool(dump_hold or weak_struct or low_conc)


def _hand_fails_late_quality_gate(
    tiles: list[str],
    *,
    discards: list[str],
    ban_suit: str | None,
    strategy: StrategyBelief,
    n_melds: int,
    phase: str | None = None,
) -> bool:
    """True if late hand should be resampled (structure floor or fake-near)."""
    n_disc = len(discards)
    ph = phase or _disc_phase(n_disc)
    if ph not in ("late", "deep"):
        return False
    struct = _structure_score(tiles)
    if struct < LATE_STRUCT_FLOOR:
        # only gate when timeline evidence exists (avoid killing pure early late-noise)
        dumped = _dumped_suits(discards, ph)
        if dumped or n_disc >= LATE_DISC_LO:
            # weak structure alone is enough for soft resample at late
            if struct < LATE_STRUCT_FLOOR:
                sh = _shanten_of_ids(tiles, n_melds, ban_suit)
                if sh is not None and float(sh) < _target_shanten(n_disc, n_melds) - 0.5:
                    return True
    sh = _shanten_of_ids(tiles, n_melds, ban_suit)
    return _is_suspicious_fake_near(
        tiles,
        sh=sh,
        n_disc=n_disc,
        n_melds=n_melds,
        discards=discards,
        ban_suit=ban_suit,
        strategy=strategy,
        phase=ph,
    )


def _dump_compliance_mult(
    tiles: list[str],
    discards: list[str],
    phase: str,
) -> float:
    """L3.4 I6: independent dump-suit compliance multiplier (not prefer/conc)."""
    dumped = _dumped_suits(discards, phase)
    if not dumped:
        return 1.0
    hist = Counter(_suit_of(t) for t in tiles if _suit_of(t))
    mult = 1.0
    for su in dumped:
        hold = hist.get(su, 0)
        if hold == 0:
            mult *= DUMP_COMPLY_EMPTY
        elif hold <= DUMP_SUIT_HAND_CAP:
            mult *= DUMP_COMPLY_AT_CAP
        else:
            mult *= DUMP_COMPLY_EXCESS ** (hold - DUMP_SUIT_HAND_CAP)
    if phase in ("late", "deep"):
        mult *= DUMP_COMPLY_LATE_BOOST
    return mult


def _tile_pick_weight(
    tid: str,
    *,
    cnt: int,
    dingque: str | None,
    prefer: list[str],
    strategy: StrategyBelief,
    pressure: dict[str, float],
    disc_set: set[str],
    partial: Counter,
    attack_scale: float = 1.0,
    dumped_suits: set[str] | None = None,
    phase: str = "late",
    disc_cnt: Counter | None = None,
) -> float:
    w = float(cnt)
    su = _suit_of(tid)
    if dingque and su == dingque:
        return 1e-9
    dumped_suits = dumped_suits or set()
    # M2.2: lower floor for 斩色 suits
    if su in dumped_suits:
        floor = (
            DUMP_SUIT_PICK_FLOOR_MID
            if phase == "mid"
            else DUMP_SUIT_PICK_FLOOR_LATE
        )
        w *= max(floor, 1.0 - 0.95 * pressure.get(su, 0.0))
        w *= DUMP_SUIT_PICK_MULT
    else:
        w *= max(0.08, 1.0 - 0.85 * pressure.get(su, 0.0))
    # M1.5: mid halves attack_clear boost on primary prefer suit
    atk = strategy.attack_clear * max(0.0, attack_scale)
    if prefer and su == prefer[0] and su not in dumped_suits:
        w *= 1.0 + 0.9 * atk
    elif prefer and su in prefer and su not in dumped_suits:
        w *= 1.25
    elif prefer and su and su not in prefer:
        w *= 0.45 + 0.08 * strategy.safe_fold
    # recently discarded exact id unlikely still held
    if tid in disc_set:
        w *= 0.12
    # M2.3 soft: id discarded ≥2 times
    if disc_cnt is not None and disc_cnt.get(tid, 0) >= 2:
        w *= MULTI_DISCARD_ID_SOFT
    # structure: boost pair / neighbor with partial hand
    if partial.get(tid, 0) >= 1:
        w *= 1.55
    try:
        r = int(str(tid).split("_", 1)[1])
    except Exception:
        r = -1
    if r > 0 and su:
        for d in (-2, -1, 1, 2):
            nb = f"{su}_{r + d}"
            if partial.get(nb, 0) > 0:
                w *= 1.35 if abs(d) == 1 else 1.12
    return max(1e-9, w)


def _weighted_sample_hand(
    pool: Counter,
    n: int,
    rng: random.Random,
    *,
    strategy: StrategyBelief,
    dingque: str | None,
    prefer_suits: list[str] | None = None,
    discards: list[str] | None = None,
    use_quota: bool = True,
) -> list[str] | None:
    if n <= 0:
        return []
    pool = Counter({k: v for k, v in pool.items() if v > 0})
    if dingque:
        for tid in list(pool.keys()):
            if tid.startswith(dingque + "_"):
                del pool[tid]
    if sum(pool.values()) < n:
        keys = list(pool.keys()) or ["wan_1", "tong_1", "tiao_1"]
        return sorted(rng.choices(keys, k=n))

    prefer_suits = prefer_suits or []
    discards = discards or []
    phase = _disc_phase(len(discards))
    # M1.1 D6: quota only in late (early/mid never)
    if phase != "late":
        use_quota = False
    attack_scale = MID_ATTACK_WEIGHT_SCALE if phase == "mid" else 1.0
    pressure = _discard_suit_pressure(discards)
    disc_set = set(discards[-8:])
    dumped = _dumped_suits(discards, phase)
    # do not fill quota into dumped suits
    if use_quota and dumped:
        prefer_suits = [s for s in prefer_suits if s not in dumped] or prefer_suits
    disc_cnt_map: Counter = Counter(discards)
    work = Counter(pool)
    out: list[str] = []
    partial: Counter = Counter()

    def _pick_one(suit_filter: str | None = None) -> str | None:
        keys: list[str] = []
        weights: list[float] = []
        for tid, cnt in work.items():
            if cnt <= 0:
                continue
            if suit_filter and not tid.startswith(suit_filter + "_"):
                continue
            ww = _tile_pick_weight(
                tid,
                cnt=cnt,
                dingque=dingque,
                prefer=prefer_suits,
                strategy=strategy,
                pressure=pressure,
                disc_set=disc_set,
                partial=partial,
                attack_scale=attack_scale,
                dumped_suits=dumped,
                phase=phase,
                disc_cnt=disc_cnt_map,
            )
            keys.append(tid)
            weights.append(ww)
        if not keys:
            return None
        pick = rng.choices(keys, weights=weights, k=1)[0]
        work[pick] -= 1
        if work[pick] <= 0:
            del work[pick]
        partial[pick] += 1
        return pick

    # Phase 1: meet expected suit quotas (strongly improves suit-level accuracy)
    if use_quota and n >= 4:
        shares = _expected_suit_share(discards, dingque, prefer_suits, strategy)
        suits = [s for s in ("wan", "tong", "tiao") if s != dingque]
        rng.shuffle(suits)
        allocated = 0
        for i_su, su in enumerate(suits):
            remain_suits = len(suits) - i_su - 1
            target = int(round(shares.get(su, 0.0) * n))
            target = min(target, max(0, n - allocated - remain_suits))
            for _ in range(target):
                if allocated >= n:
                    break
                p = _pick_one(su)
                if p is None:
                    break
                out.append(p)
                allocated += 1

    # Phase 2: fill remainder freely
    while len(out) < n:
        p = _pick_one(None)
        if p is None:
            break
        out.append(p)
    if len(out) < n:
        return None
    return sorted(out)


def _shanten_of_ids(tiles: list[str], n_melds: int, dingque: str | None) -> int | None:
    try:
        hand = [parse_tile(t) for t in tiles]
        dq = Suit(dingque) if dingque in ("wan", "tong", "tiao") else None
        if n_melds <= 0:
            return int(compute_shanten(hand, None, dq).shanten)
        # Dummy open melds only to set open-meld count for shanten formula
        melds = [
            MeldView(kind="pong", tile=Tile(Suit.WAN, 9 - (i % 8)))
            for i in range(n_melds)
        ]
        return int(compute_shanten(hand, melds, dq).shanten)
    except Exception:
        return None


def _shanten_result_ids(
    tiles: list[str], n_melds: int, dingque: str | None
):
    """Full ShantenResult for ukeire etc.; None on failure."""
    try:
        hand = [parse_tile(t) for t in tiles]
        dq = Suit(dingque) if dingque in ("wan", "tong", "tiao") else None
        melds = None
        if n_melds > 0:
            melds = [
                MeldView(kind="pong", tile=Tile(Suit.WAN, 9 - (i % 8)))
                for i in range(n_melds)
            ]
        return compute_shanten(hand, melds, dq)
    except Exception:
        return None


def _is_dingque_tile(tid: str, dingque: str | None) -> bool:
    return bool(dingque and str(tid).startswith(dingque + "_"))


def _hand_without_dingque(tiles: list[str], dingque: str | None) -> list[str]:
    if not dingque:
        return list(tiles)
    return [t for t in tiles if not str(t).startswith(dingque + "_")]


def _combo_association(
    d: str, hand: list[str], dingque: str | None
) -> float:
    """How strongly discard d connects to hand combos (0..1). Dingque → 0."""
    if _is_dingque_tile(d, dingque):
        return 0.0
    hand = _hand_without_dingque(hand, dingque)
    if not hand:
        return 0.0
    try:
        dt = parse_tile(d)
        dsu, dr = dt.suit.value, int(dt.rank)
    except Exception:
        return 0.0
    score = 0.0
    same_id = sum(1 for t in hand if t == d)
    score += min(0.9, 0.45 * same_id)
    for t in hand:
        try:
            tt = parse_tile(t)
            if tt.suit.value != dsu:
                continue
            gap = abs(int(tt.rank) - dr)
            if gap == 1:
                score += 0.28
            elif gap == 2:
                score += 0.12
        except Exception:
            continue
    return float(min(1.0, score))


def _tenpai_association(
    d: str,
    hand: list[str],
    n_melds: int,
    dingque: str | None,
    *,
    mid: bool = False,
    full: bool = True,
) -> float:
    """Discard d vs predicted hand tenpai/advance relevance (0..1). Dingque d → 0."""
    if _is_dingque_tile(d, dingque):
        return 0.0
    hand_nd = _hand_without_dingque(hand, dingque)
    combo = _combo_association(d, hand_nd, None)
    if not full:
        # fast path: combo proxy only
        return float(min(1.0, (0.65 if mid else 0.50) * combo))
    # 1) if H is tenpai and d completes H (d in ukeire) → very high
    res_h = _shanten_result_ids(hand, n_melds, dingque)
    if res_h is not None and res_h.shanten == 0 and res_h.ukeire:
        try:
            dt = parse_tile(d)
            for u in res_h.ukeire:
                if u.suit == dt.suit and u.rank == dt.rank:
                    return 1.0
        except Exception:
            pass
    # 2) compare shanten after discarding d vs a few alternative discards
    pre = list(hand) + [d]
    sh_after = res_h.shanten if res_h is not None else _shanten_of_ids(
        hand, n_melds, dingque
    )
    best = 99 if sh_after is None else sh_after
    # cost cap: at most 5 alternative unique discards (prefer non-d first)
    alts = [t for t in set(pre) if t != d]
    alts.sort()
    alts = alts[:5]
    for t in alts:
        h2 = list(pre)
        try:
            h2.remove(t)
        except ValueError:
            continue
        sh = _shanten_of_ids(h2, n_melds, dingque)
        if sh is not None:
            best = min(best, sh)
    damage = 0.0
    if sh_after is not None and best < 99 and sh_after > best:
        damage = min(1.0, 0.45 + 0.28 * float(sh_after - best))
    mix = 0.50 if mid else 0.35
    return float(min(1.0, max(damage, mix * combo + (1.0 - mix) * damage)))


def _discard_hand_assoc_penalty(
    tiles: list[str],
    discards: list[str],
    *,
    ban_suit: str | None,
    n_melds: int,
    phase: str,
    full_tenpai: bool = True,
) -> float:
    """Weight multiplier ≤1: penalize high discard↔hand association (excl. dingque)."""
    if not discards or not tiles:
        return 1.0
    d = discards[-1]
    if _is_dingque_tile(d, ban_suit):
        return 1.0
    if phase == "early":
        assoc = _combo_association(d, tiles, ban_suit)
        return max(DH_MIN_MULT, 1.0 - DH_EARLY_COMBO_PENALTY * assoc)
    assoc = _tenpai_association(
        d,
        tiles,
        n_melds,
        ban_suit,
        mid=(phase == "mid"),
        full=full_tenpai,
    )
    pen = DH_MID_TENPAI_PENALTY if phase == "mid" else DH_LATE_TENPAI_PENALTY
    return max(DH_MIN_MULT, 1.0 - pen * assoc)


def _score_hand(
    tiles: list[str],
    *,
    ban_suit: str | None,
    discards: list[str],
    strategy: StrategyBelief,
    n_melds: int,
    prev_hand: list[str] | None,
    with_shanten: bool = True,
) -> tuple[float, int | None, str]:
    """Return (weight, shanten, label). Higher weight = better hypothesis.

    ``with_shanten=False`` is a fast path for beam expansion (no engine call).
    """
    if not tiles:
        return 1e-6, None, ""
    w = 1.0
    label_parts: list[str] = []
    n = len(tiles)
    n_disc = len(discards)
    phase = _disc_phase(n_disc)
    prefer = _prefer_suits_for_strategy(discards, ban_suit, strategy)
    pressure = _discard_suit_pressure(discards)
    shares = _expected_suit_share(discards, ban_suit, prefer, strategy)
    dumped = _dumped_suits(discards, phase)
    streak_dump = _streak_dumped_suits(discards)

    # --- C2 dingque hard ---
    if ban_suit:
        bad = sum(1 for t in tiles if t.startswith(ban_suit + "_"))
        if bad > 0:
            w *= 0.08 ** min(bad, 3)
        else:
            w *= 1.2

    # --- C4 suit timeline: match expected suit shares ---
    # M1.2: mid uses softer info ramp (/12); early/late keep /8
    info_div = MID_SHARE_INFO_DIV if phase == "mid" else 8.0
    info = min(1.0, n_disc / info_div)
    # M1.2: mid caps share-penalty strength
    share_k = 0.6 + (1.0 * info if phase == "mid" else 2.0 * info)
    hist = Counter(_suit_of(t) for t in tiles)
    for su in ("wan", "tong", "tiao"):
        actual = hist.get(su, 0) / n
        expected = shares.get(su, 0.0)
        err = abs(actual - expected)
        w *= math.exp(-share_k * err)
        # M1.3: extra pressure-hold penalty only outside mid (late/deep)
        if (
            phase != "mid" or MID_EXTRA_PRESSURE_PENALTY
        ) and phase != "early":
            if info > 0.35 and pressure.get(su, 0) >= 0.4 and actual > 0.25:
                w *= 0.7 ** (1.0 + actual * info)

    # M2.1: 斩色 — hold more than HAND_CAP heavily penalized
    for su in dumped:
        hold = hist.get(su, 0)
        if hold > DUMP_SUIT_HAND_CAP:
            w *= DUMP_SUIT_HOLD_PENALTY ** (hold - DUMP_SUIT_HAND_CAP)
        elif hold == 0:
            w *= 1.08
            label_parts.append(f"斩{_suit_label_short(su)}")
        else:
            w *= 0.85  # at most one leftover discouraged lightly

    # M2.4: consecutive same-suit dump streak
    for su in streak_dump:
        hold = hist.get(su, 0)
        if hold > STREAK_HOLD_CAP:
            w *= STREAK_HOLD_PENALTY ** (hold - STREAK_HOLD_CAP)

    # L3.4 I6: dump compliance independent of prefer / concentration
    w *= _dump_compliance_mult(tiles, discards, phase)

    # exact discarded ids should rarely remain
    # M2.3: disc_cnt≥2 → soft MULTI_DISCARD_ID_SOFT (Q2 locked, not hard ban)
    disc_cnt = Counter(discards)
    for tid, hc in Counter(tiles).items():
        dc = disc_cnt.get(tid, 0)
        if dc >= 2:
            w *= MULTI_DISCARD_ID_SOFT ** min(hc, 2)
        elif dc > 0:
            w *= 0.45 ** min(hc, 2)

    recent = set(discards[-6:])
    overlap = sum(1 for t in tiles if t in recent)
    w *= max(0.08, 1.0 - 0.14 * overlap)

    # DH: discard ↔ hand association (exclude dingque); phase-split
    # full tenpai search only when with_shanten (slow path)
    w *= _discard_hand_assoc_penalty(
        tiles,
        discards,
        ban_suit=ban_suit,
        n_melds=n_melds,
        phase=phase,
        full_tenpai=with_shanten,
    )

    # main suit concentration + mid-rank bias in attack suit
    # skip dumped suits as "main"
    prefer_eff = [s for s in prefer if s not in dumped] or prefer
    if prefer_eff:
        main = prefer_eff[0]
        main_n = hist.get(main, 0)
        conc = main_n / n
        # M1.5: mid softer single-suit concentration demand
        if phase == "mid":
            w *= 0.55 + 1.0 * conc
        else:
            w *= 0.48 + 1.35 * conc
        if conc >= 0.5:
            label_parts.append(f"偏{main}")
        elif conc < 0.28 and strategy.attack_clear >= 2.0 and phase != "mid":
            w *= 0.6
        mid_n = 0
        for t in tiles:
            if not t.startswith(main + "_"):
                continue
            try:
                r = int(t.split("_", 1)[1])
                if 3 <= r <= 7:
                    mid_n += 1
            except Exception:
                pass
        if main_n > 0:
            w *= 1.0 + 0.12 * (mid_n / main_n)

    # structure always; L2.4 G1: +20% structure *bonus* only late/deep
    struct_raw = _structure_score(tiles)
    struct = struct_raw
    if phase in ("late", "deep"):
        struct = 1.0 + LATE_STRUCTURE_MULT * (struct_raw - 1.0)
        # S1.4: weak structure floor (only late/deep)
        if struct_raw < LATE_STRUCT_FLOOR:
            w *= LATE_STRUCT_FLOOR_MULT
    w *= struct
    sh: int | None = None
    if with_shanten:
        sh = _shanten_of_ids(tiles, n_melds, ban_suit)
        if sh is not None:
            late_ratio = min(1.0, n_disc / 10.0)
            # L2.1 C5b: table target instead of 4.2-0.25*n_disc-0.7*n_melds
            target = _target_shanten(n_disc, n_melds)
            sh_pen = abs(float(sh) - target)
            # base proximity term
            sh_factor = math.exp(-0.48 * sh_pen)
            # S2.2 S-TRUST: outside |sh-target|≤τ, dampen sh influence toward neutral 1.0
            if phase in ("late", "deep") and sh_pen > S_TRUST_TAU:
                sh_factor = 1.0 + (sh_factor - 1.0) * S_TRUST_OUTSIDE_SCALE
            w *= sh_factor
            # S1.1: soft-kill suspicious fake-near (timeline/structure mismatch)
            fake_near = _is_suspicious_fake_near(
                tiles,
                sh=sh,
                n_disc=n_disc,
                n_melds=n_melds,
                discards=discards,
                ban_suit=ban_suit,
                strategy=strategy,
                phase=phase,
            )
            if fake_near:
                w *= S1_FAKE_NEAR_SCORE_MULT
            # S2.3: pure distance fake-near (even if structure ok)
            if phase in ("late", "deep") and float(sh) <= target - SHANTEN_FAKE_NEAR_DELTA:
                w *= S2_FAKE_NEAR_EXTRA
            # L2.3 G5: late/deep stricter high-shanten penalty; mid keeps old threshold
            if phase in ("late", "deep"):
                if sh >= 4:
                    w *= LATE_SHANTEN_PENALTY_GE4
                elif sh >= 3:
                    w *= LATE_SHANTEN_PENALTY_GE3
                # tenpai bonus only if trusted & not fake-near
                trusted = sh_pen <= S_TRUST_TAU
                if sh <= 0 and not fake_near and trusted:
                    w *= LATE_TENPAI_BONUS_BASE + LATE_TENPAI_BONUS_LATE_K * late_ratio
                    label_parts.append("听/近听")
                elif sh == 1 and trusted:
                    label_parts.append("一向听")
            else:
                if late_ratio > 0.45 and sh >= 4:
                    w *= 0.7
                if sh <= 0:
                    w *= 1.15 + 0.3 * late_ratio
                    label_parts.append("听/近听")
                elif sh == 1:
                    label_parts.append("一向听")
    else:
        # cheap structure proxy for "progress toward tenpai"
        w *= 1.0 + 0.04 * min(6, sum(1 for v in Counter(tiles).values() if v >= 2))
        # S1: late fast-path also soft-penalize very weak structure
        if phase in ("late", "deep") and struct_raw < LATE_STRUCT_FLOOR:
            w *= LATE_STRUCT_FLOOR_MULT

    # continuity soft
    if prev_hand:
        f1 = multiset_f1(tiles, prev_hand)
        w *= 0.35 + 1.25 * f1
        if f1 >= 0.7:
            label_parts.append("连续")

    w *= 0.88 + 0.04 * (
        strategy.dump_dingque
        + strategy.attack_clear
        + strategy.safe_fold
        + strategy.fast_meld
    )
    return max(1e-12, w), sh, "+".join(label_parts[:2])


def _refine_hand(
    hand: list[str],
    residual: Counter,
    *,
    ban_suit: str | None,
    discards: list[str],
    strategy: StrategyBelief,
    n_melds: int,
    prev_hand: list[str] | None,
    rng: random.Random,
    swaps: int = _REFINE_SWAPS,
) -> list[str]:
    """Hill-climb: swap hand tiles with residual tiles not currently in hand.

    ``residual`` = remain − other seats' hands (still includes capacity for this hand).
    """
    if not hand or swaps <= 0:
        return sorted(hand)
    best = sorted(hand)
    best_sc, _, _ = _score_hand(
        best,
        ban_suit=ban_suit,
        discards=discards,
        strategy=strategy,
        n_melds=n_melds,
        prev_hand=prev_hand,
        with_shanten=True,
    )
    # free = residual − current hand usage
    pool = Counter({k: int(v) for k, v in residual.items() if int(v) > 0})
    hc = Counter(best)
    for t, c in hc.items():
        pool[t] = pool.get(t, 0) - c
        if pool[t] <= 0:
            del pool[t]
    for _ in range(swaps):
        if not best or not pool:
            break
        out_i = rng.randrange(len(best))
        out_t = best[out_i]
        keys = [t for t, c in pool.items() if c > 0]
        if not keys:
            break
        prefer = _prefer_suits_for_strategy(discards, ban_suit, strategy)
        weights = []
        for tid in keys:
            ww = float(pool[tid])
            su = _suit_of(tid)
            if ban_suit and su == ban_suit:
                ww *= 0.01
            if prefer and su == prefer[0]:
                ww *= 2.0
            if tid in discards[-6:]:
                ww *= 0.2
            weights.append(max(1e-9, ww))
        in_t = rng.choices(keys, weights=weights, k=1)[0]
        trial = list(best)
        trial[out_i] = in_t
        trial_s = sorted(trial)
        sc, sh_trial, _ = _score_hand(
            trial_s,
            ban_suit=ban_suit,
            discards=discards,
            strategy=strategy,
            n_melds=n_melds,
            prev_hand=prev_hand,
            with_shanten=True,
        )
        # S1.2: reject swaps that create suspicious fake-near even if score spikes
        phase = _disc_phase(len(discards))
        if phase in ("late", "deep") and _is_suspicious_fake_near(
            trial_s,
            sh=sh_trial,
            n_disc=len(discards),
            n_melds=n_melds,
            discards=discards,
            ban_suit=ban_suit,
            strategy=strategy,
            phase=phase,
        ):
            continue
        if sc > best_sc:
            pool[in_t] -= 1
            if pool[in_t] <= 0:
                del pool[in_t]
            pool[out_t] = pool.get(out_t, 0) + 1
            best = trial_s
            best_sc = sc
    return sorted(best)


def _sample_hand_variants(
    pool: Counter,
    need: int,
    rng: random.Random,
    meta_s: dict,
    *,
    n_samples: int,
    prev_hand: list[str] | None = None,
) -> list[tuple[float, list[str]]]:
    """Sample diverse hands; score with fast path; return unique (score, hand)."""
    seen: dict[tuple[str, ...], float] = {}

    def _consider(h: list[str]) -> None:
        if not h or len(h) != need:
            return
        hc = Counter(h)
        if not all(pool.get(t, 0) >= c for t, c in hc.items()):
            return
        sc, _, _ = _score_hand(
            h,
            ban_suit=meta_s["dingque"],
            discards=meta_s["disc"],
            strategy=meta_s["strategy"],
            n_melds=meta_s["n_melds"],
            prev_hand=prev_hand,
            with_shanten=False,
        )
        key = tuple(h)
        if key not in seen or sc > seen[key]:
            seen[key] = sc

    disc_list = list(meta_s.get("disc") or [])
    phase = _disc_phase(len(disc_list))
    for i in range(n_samples):
        pref = list(meta_s["prefer"])
        if pref and (i % 5 == 4) and len(pref) > 1:
            pref = [pref[1]] + pref[:1]
        use_q = (i % 4) != 3
        h = None
        for _try in range(1 + (S1_RESAMPLE_MAX if phase in ("late", "deep") else 0)):
            cand = _weighted_sample_hand(
                Counter(pool),
                need,
                rng,
                strategy=meta_s["strategy"],
                dingque=meta_s["dingque"],
                prefer_suits=pref,
                discards=meta_s["disc"],
                use_quota=use_q,
            )
            if not cand:
                break
            if phase in ("late", "deep") and _hand_fails_late_quality_gate(
                cand,
                discards=disc_list,
                ban_suit=meta_s.get("dingque"),
                strategy=meta_s["strategy"],
                n_melds=int(meta_s.get("n_melds") or 0),
                phase=phase,
            ):
                continue
            h = cand
            break
        if h:
            _consider(h)
        # continuity mutations from prev_hand when legal
        if prev_hand and len(prev_hand) == need and (i % 2 == 0):
            pc = Counter(prev_hand)
            if all(pool.get(t, 0) >= c for t, c in pc.items()):
                mut = list(prev_hand)
                n_mut = 1 + (i % 3)
                for _ in range(n_mut):
                    j = rng.randrange(len(mut))
                    # temporary pool after removing current mut multiset
                    trial_pool = Counter(pool)
                    for t in mut:
                        trial_pool[t] = trial_pool.get(t, 0) - 1
                    trial_pool = Counter({k: v for k, v in trial_pool.items() if v > 0})
                    # release the slot we're replacing
                    trial_pool[mut[j]] = trial_pool.get(mut[j], 0) + 1
                    if trial_pool[mut[j]] <= 0:
                        trial_pool.pop(mut[j], None)
                    pick = _weighted_sample_hand(
                        trial_pool,
                        1,
                        rng,
                        strategy=meta_s["strategy"],
                        dingque=meta_s["dingque"],
                        prefer_suits=pref,
                        discards=meta_s["disc"],
                        use_quota=False,
                    )
                    if pick:
                        mut[j] = pick[0]
                _consider(sorted(mut))
    return sorted(
        ((sc, list(key)) for key, sc in seen.items()),
        key=lambda x: -x[0],
    )


def _beam_search_joints(
    remain: dict[str, int],
    order: list[int],
    meta: dict[int, dict],
    rng: random.Random,
    *,
    prev_by_scene: list[dict[int, list[str]]],
    beam_width: int = _BEAM_WIDTH,
    samples: int = _BEAM_SAMPLES,
) -> list[tuple[float, dict[int, list[str]]]]:
    """Beam joint assignment; scores are fast (no shanten). Returns (partial_score, hands)."""
    # beam item: (score, hands_dict)
    beam: list[tuple[float, dict[int, list[str]]]] = [(0.0, {})]
    for s in order:
        need = meta[s]["need"]
        new_beam: list[tuple[float, dict[int, list[str]]]] = []
        prev_opts = []
        if prev_by_scene:
            for ph in prev_by_scene[:4]:
                if s in ph and len(ph[s]) == need:
                    prev_opts.append(ph[s])
        for sc0, hands0 in beam:
            # reconstruct pool from remain minus assigned hands
            pool = Counter({k: int(v) for k, v in remain.items() if int(v) > 0})
            ok_pool = True
            for hs in hands0.values():
                if not _subtract_hand(pool, hs):
                    ok_pool = False
                    break
            if not ok_pool:
                continue
            if need <= 0:
                h2 = dict(hands0)
                h2[s] = []
                new_beam.append((sc0, h2))
                continue
            variants = _sample_hand_variants(
                pool,
                need,
                rng,
                meta[s],
                n_samples=samples,
                prev_hand=prev_opts[0] if prev_opts else None,
            )
            # force-include continuity hands if they fit pool
            for ph in prev_opts[:3]:
                pc = Counter(ph)
                if all(pool.get(t, 0) >= c for t, c in pc.items()):
                    sc_p, _, _ = _score_hand(
                        ph,
                        ban_suit=meta[s]["dingque"],
                        discards=meta[s]["disc"],
                        strategy=meta[s]["strategy"],
                        n_melds=meta[s]["n_melds"],
                        prev_hand=ph,
                        with_shanten=False,
                    )
                    variants.append((sc_p * 1.15, list(ph)))
            # keep top variants for expansion
            variants.sort(key=lambda x: -x[0])
            used_local: set[tuple[str, ...]] = set()
            for sc_h, h in variants[: max(beam_width + 2, 6)]:
                key = tuple(h)
                if key in used_local:
                    continue
                pc = Counter(h)
                if not all(pool.get(t, 0) >= c for t, c in pc.items()):
                    continue
                used_local.add(key)
                h2 = dict(hands0)
                h2[s] = list(h)
                new_beam.append((sc0 + sc_h, h2))
        if not new_beam:
            # failed expand — keep previous (incomplete) won't work; break
            break
        new_beam.sort(key=lambda x: -x[0])
        # dedupe by hands signature
        uniq: dict[tuple, tuple[float, dict[int, list[str]]]] = {}
        for sc, hands in new_beam:
            sig = tuple(sorted((seat, tuple(hh)) for seat, hh in hands.items()))
            if sig not in uniq or sc > uniq[sig][0]:
                uniq[sig] = (sc, hands)
        beam = sorted(uniq.values(), key=lambda x: -x[0])[:beam_width]
    # only complete joints
    complete = [
        (sc, hands)
        for sc, hands in beam
        if all(seat in hands for seat in order)
    ]
    return complete


def _subtract_hand(pool: Counter, hand: list[str]) -> bool:
    c = Counter(hand)
    for tid, n in c.items():
        if pool.get(tid, 0) < n:
            return False
    for tid, n in c.items():
        pool[tid] -= n
        if pool[tid] <= 0:
            del pool[tid]
    return True


def _info_richness(discards: list[str], n_melds: int, hand_count: int) -> tuple:
    # higher = process first (more constrained)
    return (n_melds, len(discards), -hand_count)


def _prefer_for_refill(
    kept: list[str],
    base_prefer: list[str],
    dingque: str | None,
) -> list[str]:
    """L1.2: prefer suits still in kept hand, then base prefer (for draw refill)."""
    kept_suits = []
    seen: set[str] = set()
    for tid in kept:
        su = _suit_of(tid)
        if su and su != dingque and su not in seen:
            seen.add(su)
            kept_suits.append(su)
    out: list[str] = []
    for su in kept_suits + list(base_prefer or []):
        if su and su != dingque and su not in out:
            out.append(su)
    return out


def _evolve_hand_after_discard(
    hand: list[str],
    disc_tile: str,
    pool: Counter,
    need: int,
    rng: random.Random,
    *,
    strategy: StrategyBelief,
    dingque: str | None,
    prefer: list[str],
    discards: list[str] | None = None,
) -> list[str] | None:
    """Hard C1: disc_tile must be in hand; remove it; reserve kept tiles; refill from pool.

    Mutates ``pool``: subtracts kept tiles + newly drawn fills. Caller must not
    subtract the full hand again. Returns None if C1 fails (caller may regen).
    """
    c = Counter(hand)
    if c.get(disc_tile, 0) < 1:
        return None
    c[disc_tile] -= 1
    if c[disc_tile] <= 0:
        del c[disc_tile]
    kept = list(c.elements())
    if not _subtract_hand(pool, kept):
        return None
    cur = len(kept)
    hand_list = list(kept)
    # L1.2: refill with prefer biased to kept suits + strategy prefer
    refill_prefer = _prefer_for_refill(kept, prefer, dingque)
    while cur < need:
        picked = _weighted_sample_hand(
            pool,
            1,
            rng,
            strategy=strategy,
            dingque=dingque,
            prefer_suits=refill_prefer,
            discards=discards,
        )
        if not picked:
            return None
        t = picked[0]
        if pool.get(t, 0) <= 0:
            return None
        pool[t] -= 1
        if pool[t] <= 0:
            del pool[t]
        hand_list.append(t)
        cur += 1
    if cur > need:
        hand_list = hand_list[:need]
    return sorted(hand_list)


def _restricted_regen_hand(
    pool: Counter,
    need: int,
    rng: random.Random,
    *,
    strategy: StrategyBelief,
    dingque: str | None,
    prefer: list[str],
    discards: list[str] | None,
    n_melds: int = 0,
) -> list[str] | None:
    """L1.1: C1 failed — sample a full new hand from remaining pool (restricted regen).

    S1.3: late may retry if sample trips fake-near / weak-structure gate.
    """
    if need <= 0:
        return []
    disc_list = list(discards or [])
    phase = _disc_phase(len(disc_list))
    tries = 1 + (S1_RESAMPLE_MAX if phase in ("late", "deep") else 0)
    h: list[str] | None = None
    for _ in range(tries):
        cand = _weighted_sample_hand(
            Counter(pool),
            need,
            rng,
            strategy=strategy,
            dingque=dingque,
            prefer_suits=prefer,
            discards=discards,
            use_quota=False,
        )
        if not cand:
            break
        if phase in ("late", "deep") and _hand_fails_late_quality_gate(
            cand,
            discards=disc_list,
            ban_suit=dingque,
            strategy=strategy,
            n_melds=n_melds,
            phase=phase,
        ):
            continue
        h = cand
        break
    # last resort: accept any sample
    if h is None:
        h = _weighted_sample_hand(
            Counter(pool),
            need,
            rng,
            strategy=strategy,
            dingque=dingque,
            prefer_suits=prefer,
            discards=discards,
            use_quota=False,
        )
    if not h or not _subtract_hand(pool, h):
        return None
    return sorted(h)


def _score_joint(
    hands: dict[int, list[str]],
    meta: dict[int, dict],
    *,
    prev_hands: dict[int, list[str]] | None = None,
    last_discarder: int | None = None,
    last_discard_tile: str | None = None,
    continuity: bool = False,
    with_shanten: bool = True,
    remain: dict[str, int] | None = None,
    cont_phase: str = "mid",
) -> tuple[float, dict[int, str], dict[int, int | None]]:
    w_sum = 0.0
    labels: dict[int, str] = {}
    sh_map: dict[int, int | None] = {}
    prev_hands = prev_hands or {}
    disc_bonus = (
        LATE_CONT_DISCARD_BONUS if cont_phase == "late" else MID_CONT_DISCARD_BONUS
    )
    cont_mult = (
        LATE_CONTINUITY_WEIGHT_MULT
        if cont_phase == "late"
        else _CONTINUITY_WEIGHT_MULT
    )
    for s, h in hands.items():
        prev_h = prev_hands.get(s)
        sc, sh, lab = _score_hand(
            h,
            ban_suit=meta[s]["dingque"],
            discards=meta[s]["disc"],
            strategy=meta[s]["strategy"],
            n_melds=meta[s]["n_melds"],
            prev_hand=prev_h,
            with_shanten=with_shanten,
        )
        if continuity and last_discarder == s and last_discard_tile and prev_h:
            # C1-success path gets full bonus; regen still gets mild continuity
            c1_ok = last_discard_tile in (prev_h or [])
            if c1_ok:
                sc *= disc_bonus
            else:
                sc *= 1.15
            # S2.1 J4: after discard evolve, sh should not worsen much vs prev hand
            if c1_ok and with_shanten:
                sh_before = _shanten_of_ids(
                    prev_h, meta[s]["n_melds"], meta[s]["dingque"]
                )
                sh_after = sh
                if sh_after is None:
                    sh_after = _shanten_of_ids(
                        h, meta[s]["n_melds"], meta[s]["dingque"]
                    )
                if (
                    sh_before is not None
                    and sh_after is not None
                    and int(sh_after) > int(sh_before) + J4_SHANTEN_WORSEN_TOL
                ):
                    sc *= J4_WORSEN_SOFT
        # L1.5 J6: others just discarded t — holding many copies of rare t is unlikely
        if (
            last_discard_tile
            and last_discarder is not None
            and s != last_discarder
            and remain is not None
        ):
            hold = Counter(h).get(last_discard_tile, 0)
            rem_n = int(remain.get(last_discard_tile, 0))
            if hold > 0 and rem_n <= 2:
                sc *= max(0.45, 1.0 - J6_OTHER_DISCARD_HOLD_PENALTY * hold * (3 - rem_n))
        w_sum += sc
        labels[s] = lab or meta[s]["strategy"].dominant_label()
        sh_map[s] = sh
    if continuity:
        w_sum *= cont_mult
    return w_sum, labels, sh_map


def _refine_joint(
    hands: dict[int, list[str]],
    remain: dict[str, int],
    meta: dict[int, dict],
    order: list[int],
    rng: random.Random,
    *,
    prev_hands: dict[int, list[str]] | None = None,
) -> dict[int, list[str]]:
    """Refine each seat hand against residual pool after other seats fixed."""
    out = {s: list(h) for s, h in hands.items()}
    prev_hands = prev_hands or {}
    for s in order:
        # residual = remain - other hands
        pool = Counter({k: int(v) for k, v in remain.items() if int(v) > 0})
        ok = True
        for os, oh in out.items():
            if os == s:
                continue
            if not _subtract_hand(pool, oh):
                ok = False
                break
        if not ok:
            continue
        # free pool for swaps = residual (tiles not in other hands); hand tiles
        # may be added back when swapping out
        refined = _refine_hand(
            out[s],
            pool,  # residual = remain − others (includes room for this hand)
            ban_suit=meta[s]["dingque"],
            discards=meta[s]["disc"],
            strategy=meta[s]["strategy"],
            n_melds=meta[s]["n_melds"],
            prev_hand=prev_hands.get(s),
            rng=rng,
            swaps=_REFINE_SWAPS,
        )
        rc = Counter(refined)
        if all(pool.get(t, 0) >= c for t, c in rc.items()):
            out[s] = sorted(refined)
    return out


def _greedy_map_hand(
    pool: Counter,
    need: int,
    meta_s: dict,
) -> list[str] | None:
    """Deterministic high-weight hand (MAP-like) for strong tile-overlap baseline."""
    if need <= 0:
        return []
    work = Counter({k: v for k, v in pool.items() if v > 0})
    ban = meta_s.get("dingque")
    if ban:
        for tid in list(work.keys()):
            if tid.startswith(ban + "_"):
                del work[tid]
    if sum(work.values()) < need:
        work = Counter({k: v for k, v in pool.items() if v > 0})
    disc = list(meta_s.get("disc") or [])
    prefer = list(meta_s.get("prefer") or [])
    pressure = _discard_suit_pressure(disc)
    disc_set = set(disc[-8:])
    phase = _disc_phase(len(disc))
    attack_scale = MID_ATTACK_WEIGHT_SCALE if phase == "mid" else 1.0
    dumped = _dumped_suits(disc, phase)
    disc_cnt_map: Counter = Counter(disc)
    partial: Counter = Counter()
    out: list[str] = []
    for _ in range(need):
        best_t = None
        best_w = -1.0
        for tid, cnt in work.items():
            if cnt <= 0:
                continue
            ww = _tile_pick_weight(
                tid,
                cnt=cnt,
                dingque=ban,
                prefer=prefer,
                strategy=meta_s["strategy"],
                pressure=pressure,
                disc_set=disc_set,
                partial=partial,
                attack_scale=attack_scale,
                dumped_suits=dumped,
                phase=phase,
                disc_cnt=disc_cnt_map,
            )
            # tiny tie-break by tid for stability
            if ww > best_w or (ww == best_w and (best_t is None or tid < best_t)):
                best_w = ww
                best_t = tid
        if best_t is None:
            return None
        out.append(best_t)
        partial[best_t] += 1
        work[best_t] -= 1
        if work[best_t] <= 0:
            del work[best_t]
    return sorted(out)


def _joint_similarity(a: dict[int, list[str]], b: dict[int, list[str]]) -> float:
    seats = set(a) | set(b)
    if not seats:
        return 0.0
    return sum(multiset_f1(a.get(s, []), b.get(s, [])) for s in seats) / len(seats)


def _select_diverse_topk(
    scored: list[tuple],
    top_k: int,
    *,
    mmr: float = _DIVERSE_MMR,
) -> list[tuple]:
    """MMR selection: high score, low multiset similarity to already picked joints."""
    if not scored:
        return []
    remaining = list(scored)
    remaining.sort(key=lambda x: -x[0])
    picked: list[tuple] = []
    while remaining and len(picked) < top_k:
        def mmr_score(item: tuple) -> float:
            w, hands = item[0], item[1]
            if not picked:
                return w
            sim = max(_joint_similarity(hands, p[1]) for p in picked)
            return w * (1.0 - mmr * sim)

        best = max(remaining, key=mmr_score)
        picked.append(best)
        remaining.remove(best)
    return picked


def _calibrate_confidences(weights: list[float], temperature: float = _CONF_TEMPERATURE) -> list[float]:
    """Temperature softmax over log-weights for sharper, calibrated top-1.

    Returns confidences in the **same order** as ``weights``, non-increasing
    when weights are sorted descending (uses integer basis points to avoid
    reverse-order glitches after rounding).
    """
    if not weights:
        return []
    logs = [math.log(max(1e-12, w)) / max(0.15, temperature) for w in weights]
    m = max(logs)
    exps = [math.exp(x - m) for x in logs]
    s = sum(exps) or 1.0
    raw = [e / s for e in exps]
    # basis points: sum to 10000 exactly, preserve arg-sort order of raw
    bps = [int(math.floor(c * 10000 + 1e-9)) for c in raw]
    rem = 10000 - sum(bps)
    # give remainder to highest raw mass (index 0 if weights pre-sorted desc)
    order_idx = sorted(range(len(raw)), key=lambda i: (-raw[i], i))
    i = 0
    while rem > 0 and order_idx:
        bps[order_idx[i % len(order_idx)]] += 1
        rem -= 1
        i += 1
    confs = [bp / 10000.0 for bp in bps]
    return confs


def predict_joint_scenes(
    state: GameState | dict,
    self_seat: int,
    *,
    top_k: int = DEFAULT_TOP_K,
    prev_joints: list[JointHandScene] | None = None,
    prev_forecasts: list[OpponentHandForecast] | None = None,
    last_discarder: int | None = None,
    last_discard_tile: str | None = None,
    seed: int | None = None,
) -> list[JointHandScene]:
    """Generate Top-K joint scenes (v2.2 beam + refine + continuity)."""
    top_k = max(1, min(DEFAULT_TOP_K, int(top_k)))
    rng = random.Random(seed if seed is not None else 0)

    if isinstance(state, GameState):
        remain = remain_map(state, self_seat)
        seats = [
            p.seat
            for p in state.players
            if p.seat != self_seat and p.status == "active"
        ]
        view_like: Any = state
        get_hc = lambda s: expected_hand_count(state, s)
    else:
        view = state if isinstance(state, dict) else {}
        remain = view.get("remain") if isinstance(view.get("remain"), dict) else None
        if remain is None:
            remain = _remain_from_view(view, self_seat)
        seats = [
            int(p.get("seat"))
            for p in (view.get("players") or [])
            if int(p.get("seat", -1)) != self_seat
            and str(p.get("status", "active")) == "active"
        ]
        view_like = view
        get_hc = lambda s: _hand_count_from_view(view, s)

    if not seats:
        return []

    meta: dict[int, dict] = {}
    for s in seats:
        disc = _discard_ids(view_like, s)
        nm = _meld_count(view_like, s)
        dq = _dingque_suit(view_like, s)
        hc = get_hc(s)
        bel = estimate_strategy(disc, dingque=dq, n_melds=nm)
        meta[s] = {
            "disc": disc,
            "n_melds": nm,
            "dingque": dq,
            "need": hc,
            "strategy": bel,
            "prefer": _prefer_suits_for_strategy(disc, dq, bel),
            "rich": _info_richness(disc, nm, hc),
        }

    order = sorted(seats, key=lambda s: meta[s]["rich"], reverse=True)

    prev_by_scene: list[dict[int, list[str]]] = []
    if prev_joints:
        for j in prev_joints:
            prev_by_scene.append({s: list(h) for s, h in j.hands.items()})
    elif prev_forecasts:
        by_seat = {fc.seat: fc for fc in prev_forecasts}
        max_h = max((len(fc.hypotheses) for fc in prev_forecasts), default=0)
        for r in range(max_h):
            hands = {}
            ok = True
            for s in seats:
                fc = by_seat.get(s)
                if not fc or r >= len(fc.hypotheses):
                    ok = False
                    break
                hands[s] = list(fc.hypotheses[r].tiles)
            if ok:
                prev_by_scene.append(hands)

    # raw hands candidates before full rescoring
    raw_hands: list[tuple[dict[int, list[str]], bool, dict[int, list[str]] | None]] = []
    # (hands, is_continuity, prev_hands)

    mean_disc = (
        sum(len(meta[s]["disc"]) for s in meta) / max(1, len(meta)) if meta else 0.0
    )
    early_phase = mean_disc <= 2.5
    late_phase = mean_disc >= 7.0
    mid_phase = (not early_phase) and (not late_phase)

    def _try_continuity(hands0: dict[int, list[str]]) -> None:
        pool = Counter({k: int(v) for k, v in remain.items() if int(v) > 0})
        hands: dict[int, list[str]] = {}
        for s in order:
            if last_discarder is not None and s == last_discarder:
                continue
            h = hands0.get(s)
            if not h or len(h) != meta[s]["need"]:
                h = _weighted_sample_hand(
                    pool,
                    meta[s]["need"],
                    rng,
                    strategy=meta[s]["strategy"],
                    dingque=meta[s]["dingque"],
                    prefer_suits=meta[s]["prefer"],
                    discards=meta[s]["disc"],
                )
            if not h or not _subtract_hand(pool, h):
                return
            hands[s] = sorted(h)
        if last_discarder is not None and last_discarder in meta:
            s = last_discarder
            prev_h = hands0.get(s, [])
            disc_t = last_discard_tile or ""
            evolved: list[str] | None = None
            if disc_t:
                evolved = _evolve_hand_after_discard(
                    prev_h,
                    disc_t,
                    pool,
                    meta[s]["need"],
                    rng,
                    strategy=meta[s]["strategy"],
                    dingque=meta[s]["dingque"],
                    prefer=meta[s]["prefer"],
                    discards=meta[s]["disc"],
                )
            if evolved is None:
                # L1.1: C1 fail → restricted full-hand regen from remaining pool
                evolved = _restricted_regen_hand(
                    pool,
                    meta[s]["need"],
                    rng,
                    strategy=meta[s]["strategy"],
                    dingque=meta[s]["dingque"],
                    prefer=meta[s]["prefer"],
                    discards=meta[s]["disc"],
                    n_melds=int(meta[s].get("n_melds") or 0),
                )
            if not evolved:
                return
            hands[s] = evolved
        for s in seats:
            if s not in hands:
                h = hands0.get(s)
                if not h or len(h) != meta[s]["need"]:
                    return
                if not _subtract_hand(pool, h):
                    return
                hands[s] = sorted(h)
        if not _joint_respects_remain(hands, remain):
            return
        raw_hands.append((hands, True, hands0))

    if early_phase:
        # early: only light continuity — sticky bad hyps hurt F1 hard
        for hands0 in prev_by_scene[:3]:
            _try_continuity(hands0)
    elif late_phase:
        # L1.4: more prev scenes + mutations
        n_prev = top_k + LATE_CONT_PREV_EXTRA
        for hands0 in prev_by_scene[:n_prev]:
            for _mut in range(LATE_CONT_MUTATIONS):
                _try_continuity(hands0)
    else:
        for hands0 in prev_by_scene[: top_k + 3]:
            for _mut in range(5):
                _try_continuity(hands0)

    prev0 = prev_by_scene[0] if prev_by_scene else None

    # Beam only mid/late (expensive + overfits early)
    if not early_phase:
        beam_hits = _beam_search_joints(
            remain,
            order,
            meta,
            rng,
            prev_by_scene=prev_by_scene,
            beam_width=_BEAM_WIDTH,
            samples=_BEAM_SAMPLES,
        )
        for _sc, hands in beam_hits:
            if _joint_respects_remain(hands, remain):
                raw_hands.append((hands, False, prev0))

    def _sample_one_joint(
        *,
        prefer_override: dict[int, list[str]] | None = None,
        uniform: bool = False,
        use_quota: bool = True,
    ) -> dict[int, list[str]] | None:
        pool = Counter({k: int(v) for k, v in remain.items() if int(v) > 0})
        hands: dict[int, list[str]] = {}
        for s in order:
            need = meta[s]["need"]
            if need <= 0:
                hands[s] = []
                continue
            if uniform:
                flat: list[str] = []
                for tid, nn in pool.items():
                    if meta[s]["dingque"] and tid.startswith(meta[s]["dingque"] + "_"):
                        continue
                    flat.extend([tid] * max(0, int(nn)))
                if not flat:
                    for tid, nn in pool.items():
                        flat.extend([tid] * max(0, int(nn)))
                if len(flat) < need:
                    return None
                rng.shuffle(flat)
                h = sorted(flat[:need])
            else:
                pref = (prefer_override or {}).get(s) or list(meta[s]["prefer"])
                h = _weighted_sample_hand(
                    pool,
                    need,
                    rng,
                    strategy=meta[s]["strategy"],
                    dingque=meta[s]["dingque"],
                    prefer_suits=pref,
                    discards=meta[s]["disc"],
                    use_quota=use_quota,
                )
            if not h or not _subtract_hand(pool, h):
                return None
            hands[s] = h
        if hands and _joint_respects_remain(hands, remain):
            return hands
        return None

    if not early_phase:
        # Greedy MAP joint
        pool_g = Counter({k: int(v) for k, v in remain.items() if int(v) > 0})
        greedy_hands: dict[int, list[str]] = {}
        ok_g = True
        for s in order:
            h = _greedy_map_hand(pool_g, meta[s]["need"], meta[s])
            if h is None or not _subtract_hand(pool_g, h):
                ok_g = False
                break
            greedy_hands[s] = h
        if ok_g and greedy_hands and _joint_respects_remain(greedy_hands, remain):
            raw_hands.append((greedy_hands, False, prev0))

        # Suit-mode ensemble
        suit_modes = ["wan", "tong", "tiao"]
        for mode_i, su in enumerate(suit_modes):
            for _ in range(8):
                pref_over = {}
                for s in seats:
                    dq = meta[s]["dingque"]
                    if dq and su == dq:
                        alts = [x for x in suit_modes if x != dq]
                        pref_over[s] = [alts[mode_i % len(alts)]]
                    else:
                        pref_over[s] = [su]
                # suit ensemble: quota only in late game (M1.1)
                j = _sample_one_joint(
                    prefer_override=pref_over,
                    use_quota=(not mid_phase),
                )
                if j:
                    raw_hands.append((j, False, prev0))

    # Monte Carlo: early≈uniform; mid ≥50% uniform + no quota (M1.1/M1.4); late weighted
    n_mc = _MC_JOINTS + (40 if early_phase else (16 if mid_phase else 24))
    # mid: every other sample uniform → 50% when MID_UNIFORM_RATIO≈0.5
    mid_uniform_every = max(1, int(round(1.0 / max(0.1, MID_UNIFORM_RATIO))))
    for i in range(n_mc):
        if early_phase:
            j = _sample_one_joint(uniform=True, use_quota=False)
        elif mid_phase:
            j = _sample_one_joint(
                uniform=(i % mid_uniform_every == 0),
                use_quota=False,  # M1.1 D6
            )
        else:
            j = _sample_one_joint(
                uniform=(i % 7 == 6),
                use_quota=True,
            )
        if j:
            raw_hands.append((j, False, prev0))

    if not raw_hands:
        pool = Counter({k: int(v) for k, v in remain.items() if int(v) > 0})
        hands = {}
        for s in order:
            need = meta[s]["need"]
            flat = []
            for tid, nn in pool.most_common():
                if meta[s]["dingque"] and tid.startswith(meta[s]["dingque"] + "_"):
                    continue
                flat.extend([tid] * nn)
            if not flat:
                for tid, nn in pool.most_common():
                    flat.extend([tid] * nn)
            if not flat:
                flat = [f"wan_{i}" for i in range(1, 10)]
            h = sorted((flat * ((need // len(flat)) + 1))[:need])
            hands[s] = h
            _subtract_hand(pool, h)
        raw_hands.append((hands, False, None))

    # Fast pre-rank; keep top + random tail (avoid score-filter killing true F1 winners)
    scored: list[
        tuple[float, dict[int, list[str]], dict[int, str], dict[int, int | None]]
    ] = []
    pre: list[tuple[float, dict, bool, dict | None]] = []
    for hands, cont, prev_h in raw_hands:
        cont_ph = "late" if late_phase else ("early" if early_phase else "mid")
        w_fast, _, _ = _score_joint(
            hands,
            meta,
            prev_hands=prev_h,
            last_discarder=last_discarder,
            last_discard_tile=last_discard_tile,
            continuity=cont,
            with_shanten=False,
            remain=remain,
            cont_phase=cont_ph,
        )
        pre.append((w_fast, hands, cont, prev_h))
    pre.sort(key=lambda x: -x[0])
    head_n = min(len(pre), max(32, _PRESELECT * 2 // 3))
    head = pre[:head_n]
    tail = pre[head_n:]
    if tail:
        k_tail = min(len(tail), max(12, _PRESELECT - head_n))
        head = head + rng.sample(tail, k_tail)
    pre = head[:_PRESELECT]

    # Rank with FAST score only (suit/timeline/structure/continuity).
    for idx, (w_fast, hands, cont, prev_h) in enumerate(pre):
        refined = hands
        if late_phase and idx < 12:
            refined = _refine_joint(
                hands,
                remain,
                meta,
                order,
                rng,
                prev_hands=prev_h,
            )
            if not _joint_respects_remain(refined, remain):
                refined = hands
        elif mid_phase and idx < 6:
            refined = _refine_joint(
                hands,
                remain,
                meta,
                order,
                rng,
                prev_hands=prev_h,
            )
            if not _joint_respects_remain(refined, remain):
                refined = hands
        if early_phase:
            # Early: nearly flat weights so diversity selection dominates
            w_sum = 1.0 + 0.01 * rng.random()
            labels = {s: meta[s]["strategy"].dominant_label() for s in refined}
            sh_map = {s: None for s in refined}
        else:
            # L2.2 G4: only late/deep use shanten in selection; mid stays fast
            cont_ph = "late" if late_phase else ("early" if early_phase else "mid")
            w_sum, labels, sh_map = _score_joint(
                refined,
                meta,
                prev_hands=prev_h,
                last_discarder=last_discarder,
                last_discard_tile=last_discard_tile,
                continuity=cont,
                with_shanten=bool(late_phase),
                remain=remain,
                cont_phase=cont_ph,
            )
        scored.append((w_sum, refined, labels, sh_map))

    uniq: dict[tuple, tuple] = {}
    for w, hands, labels, sh_map in scored:
        key = tuple(sorted((s, tuple(h)) for s, h in hands.items()))
        if key not in uniq or w > uniq[key][0]:
            uniq[key] = (w, hands, labels, sh_map)

    all_scored = sorted(uniq.values(), key=lambda x: -x[0])
    if not all_scored:
        return []
    # L3.2 I3: phase MMR
    if early_phase:
        ranked = _select_diverse_topk(all_scored, top_k, mmr=EARLY_MMR)
    elif mid_phase:
        ranked = [all_scored[0]]
        rest = _select_diverse_topk(all_scored[1:], max(0, top_k - 1), mmr=MID_MMR)
        ranked.extend(rest)
    else:
        # late: trust score more (lower MMR)
        ranked = [all_scored[0]]
        rest = _select_diverse_topk(all_scored[1:], max(0, top_k - 1), mmr=LATE_MMR)
        ranked.extend(rest)
    ranked = sorted(ranked, key=lambda x: -x[0])[:top_k]

    # Attach real shanten on final Top-K for UI; L2.2: mid blend without shanten weight
    final_rows: list[tuple] = []
    for w, hands, labels, sh_map in ranked:
        if early_phase:
            sh2 = {}
            labels2 = dict(labels)
            for s, h in hands.items():
                sh = _shanten_of_ids(h, meta[s]["n_melds"], meta[s]["dingque"])
                sh2[s] = sh
            final_rows.append((1.0, hands, labels2, sh2))
        elif late_phase:
            # L3.3 I4: more weight on shanten slow path
            cont_ph = "late"
            w2, labels2, sh2 = _score_joint(
                hands,
                meta,
                continuity=False,
                with_shanten=True,
                remain=remain,
                cont_phase=cont_ph,
                last_discarder=last_discarder,
                last_discard_tile=last_discard_tile,
            )
            w_blend = LATE_BLEND_FAST * w + LATE_BLEND_SHANTEN * w2
            final_rows.append((w_blend, hands, labels2 or labels, sh2))
        else:
            # mid: keep selection weight; attach shanten for UI only (G4)
            sh2 = {}
            labels2 = dict(labels)
            for s, h in hands.items():
                sh2[s] = _shanten_of_ids(h, meta[s]["n_melds"], meta[s]["dingque"])
            final_rows.append((w, hands, labels2, sh2))
    final_rows.sort(key=lambda x: -x[0])
    if early_phase:
        confs = [round(1.0 / len(final_rows), 4)] * len(final_rows) if final_rows else []
        if confs:
            confs[0] = round(1.0 - sum(confs[1:]), 4)
    else:
        # L3.1 I2: phase temperature
        t_conf = LATE_CONF_TEMPERATURE if late_phase else MID_CONF_TEMPERATURE
        confs = _calibrate_confidences(
            [max(0.0, r[0]) for r in final_rows],
            temperature=t_conf,
        )
    scenes: list[JointHandScene] = []
    for i, ((w, hands, labels, sh_map), conf) in enumerate(zip(final_rows, confs)):
        scenes.append(
            JointHandScene(
                scene_id=i + 1,
                confidence=conf,
                hands={s: list(h) for s, h in hands.items()},
                labels=dict(labels),
                shanten_est=dict(sh_map),
                weight=w,
            )
        )
    return scenes


def _joint_respects_remain(
    hands: dict[int, list[str]], remain: dict[str, int]
) -> bool:
    used: Counter = Counter()
    for h in hands.values():
        used.update(h)
    for tid, n in used.items():
        if n > int(remain.get(tid, 0)):
            return False
    return True


def joints_to_forecasts(
    scenes: list[JointHandScene],
    *,
    strategy_hints: dict[int, str] | None = None,
) -> list[OpponentHandForecast]:
    """Project joint scenes into per-seat Top-K rows (same scene_id / conf)."""
    seats: set[int] = set()
    for sc in scenes:
        seats.update(sc.hands.keys())
    strategy_hints = strategy_hints or {}
    out: list[OpponentHandForecast] = []
    for seat in sorted(seats):
        hyps: list[OpponentHandHypothesis] = []
        for sc in scenes:
            tiles = sc.hands.get(seat)
            if tiles is None:
                continue
            lab = sc.labels.get(seat, "") or strategy_hints.get(seat, "")
            hyps.append(
                OpponentHandHypothesis(
                    rank=sc.scene_id,
                    tiles=list(tiles),
                    confidence=sc.confidence,
                    label=lab,
                    scene_id=sc.scene_id,
                    shanten_est=sc.shanten_est.get(seat),
                )
            )
        # re-number rank 1..n by scene order already
        for i, h in enumerate(hyps):
            h.rank = i + 1
        out.append(
            OpponentHandForecast(
                seat=seat,
                hypotheses=hyps,
                strategy_hint=strategy_hints.get(seat, ""),
            )
        )
    return out


def predict_opponent_hands(
    state: GameState | dict,
    self_seat: int,
    *,
    top_k: int = DEFAULT_TOP_K,
    prev_forecasts: list[OpponentHandForecast] | None = None,
    prev_joints: list[JointHandScene] | None = None,
    last_discarder: int | None = None,
    last_discard_tile: str | None = None,
    seed: int | None = None,
) -> list[OpponentHandForecast]:
    """
    v2 entry: joint mutual-exclusion + continuity + strategy + shanten.
    Still must NOT use oracle hands.
    """
    # Infer last discard from view if not provided
    if last_discard_tile is None and isinstance(state, dict):
        ld = state.get("last_discard")
        if isinstance(ld, dict):
            last_discard_tile = ld.get("id") or f"{ld.get('suit')}_{ld.get('rank')}"
        elif ld is not None:
            last_discard_tile = str(ld)
        ls = state.get("last_discard_seat")
        if ls is not None and last_discarder is None:
            try:
                last_discarder = int(ls)
            except (TypeError, ValueError):
                pass
    if last_discard_tile is None and isinstance(state, GameState):
        if state.last_discard is not None:
            last_discard_tile = state.last_discard.id
            last_discarder = state.last_discard_seat

    scenes = predict_joint_scenes(
        state,
        self_seat,
        top_k=top_k,
        prev_joints=prev_joints,
        prev_forecasts=prev_forecasts,
        last_discarder=last_discarder,
        last_discard_tile=last_discard_tile,
        seed=seed,
    )

    # strategy hints for UI
    hints: dict[int, str] = {}
    if isinstance(state, GameState):
        for p in state.players:
            if p.seat == self_seat:
                continue
            bel = estimate_strategy(
                [t.id for t in p.discard_pile],
                dingque=p.dingque.value if p.dingque else None,
                n_melds=len(melds_from_raw(p.melds)),
            )
            hints[p.seat] = bel.dominant_label()
    elif isinstance(state, dict):
        for p in state.get("players") or []:
            s = int(p.get("seat", -1))
            if s == self_seat:
                continue
            disc = _discard_ids(state, s)
            bel = estimate_strategy(
                disc,
                dingque=_dingque_suit(state, s),
                n_melds=_meld_count(state, s),
            )
            hints[s] = bel.dominant_label()

    forecasts = joints_to_forecasts(scenes, strategy_hints=hints)
    # Attach joint scenes for continuity cache (UI / next-tick prev_joints)
    for fc in forecasts:
        setattr(fc, "_joint_scenes", scenes)
    return forecasts


def multiset_f1(pred: list[str], truth: list[str]) -> float:
    cp, ct = Counter(pred), Counter(truth)
    if not cp and not ct:
        return 1.0
    if not cp or not ct:
        return 0.0
    inter = sum((cp & ct).values())
    return float(2 * inter) / float(sum(cp.values()) + sum(ct.values()))


def score_accuracy(
    forecast: OpponentHandForecast,
    true_tiles: list[str],
) -> OpponentHandForecast:
    true_sorted = sorted(true_tiles)
    best_f1 = -1.0
    best_rank: int | None = None
    top1_f1: float | None = None
    for i, h in enumerate(forecast.hypotheses):
        f1 = multiset_f1(h.tiles, true_sorted)
        if i == 0:
            top1_f1 = f1
        if f1 > best_f1:
            best_f1 = f1
            best_rank = h.rank
    if best_f1 < 0:
        best_f1 = 0.0
        best_rank = None
    exact = any(sorted(h.tiles) == true_sorted for h in forecast.hypotheses)
    forecast.accuracy = round(float(best_f1), 4)
    forecast.accuracy_detail = {
        "best_rank": best_rank,
        "tile_f1": forecast.accuracy,
        "top1_f1": None if top1_f1 is None else round(float(top1_f1), 4),
        "exact_set": bool(exact),
        "metric": "tile_multiset_f1",  # not whole-hand exact
    }
    return forecast


def apply_oracle_accuracy(
    forecasts: list[OpponentHandForecast],
    oracle_hands: dict[str, list[str]] | dict[int, list[str]] | None,
) -> list[OpponentHandForecast]:
    if not oracle_hands:
        return forecasts
    out = []
    for fc in forecasts:
        key = str(fc.seat)
        tiles = oracle_hands.get(key)
        if tiles is None:
            tiles = oracle_hands.get(fc.seat)  # type: ignore[arg-type]
        if tiles is None:
            out.append(fc)
            continue
        true_ids = [str(t) for t in tiles]
        out.append(score_accuracy(fc, true_ids))
    return out


def discard_fingerprint(view: dict) -> str:
    ld = view.get("last_discard")
    ls = view.get("last_discard_seat")
    seq = view.get("discard_seq")
    if seq is not None:
        return f"seq:{seq}"
    if isinstance(ld, dict):
        tid = ld.get("id") or f"{ld.get('suit')}_{ld.get('rank')}"
    else:
        tid = str(ld) if ld is not None else ""
    return f"{ls}:{tid}"


def assert_mutual_exclusion(
    forecasts: list[OpponentHandForecast],
    remain: dict[str, int],
    *,
    rank: int = 1,
) -> bool:
    """Test helper: scene rank's hands across seats respect remain."""
    used: Counter = Counter()
    for fc in forecasts:
        for h in fc.hypotheses:
            if h.rank == rank or h.scene_id == rank:
                used.update(h.tiles)
                break
    for tid, n in used.items():
        if n > int(remain.get(tid, 0)):
            return False
    return True
