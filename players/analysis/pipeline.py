"""Unified analysis entrypoint."""

from __future__ import annotations

import os
import time
from typing import Sequence

from engine.action import Action
from engine.hand_utils import melds_from_raw
from engine.shanten import shanten
from engine.state import GameState
from players.analysis.danger import danger_map_for_tiles
from players.analysis.opponent_model import estimate_opponents
from players.analysis.remain import remain_map, ukeire_count
from players.analysis.types import AnalysisSnapshot, DiscardAdvice


def _env_f0011() -> bool:
    v = (os.environ.get("F0011") or os.environ.get("CMJ_F0011") or "").strip().lower()
    return v in ("1", "true", "yes", "on")


def analyze_for_seat(
    state: GameState,
    seat: int,
    *,
    legal_discards: Sequence[Action] | None = None,
    use_f0011: bool | None = None,
    f0011_top_k: int = 3,
    humanlike_preset: str | None = None,
    recommendation_algorithm: str = "humanlike_v2",
) -> AnalysisSnapshot:
    """
    Analysis snapshot for HUD / seat window.

    use_f0011:
      - None → env F0011 / CMJ_F0011 enables integrated advisor (A5)
      - True/False → explicit
    """
    t0 = time.perf_counter()
    p = next(x for x in state.players if x.seat == seat)
    hand = list(p.hand)
    melds = melds_from_raw(p.melds)
    dingque = p.dingque
    remain = remain_map(state, seat)
    opponents = estimate_opponents(state, seat)

    try:
        sres = shanten(hand, melds, dingque)
        sh_val = sres.shanten
        uke_ids = [t.id for t in (sres.ukeire or [])]
    except Exception:
        sh_val = 8
        uke_ids = []

    uke_n = ukeire_count(uke_ids, remain)

    use_f0011 = False

    disc_list = list(legal_discards) if legal_discards is not None else None
    ranks: list[DiscardAdvice] = []
    if disc_list is not None or len(hand) % 3 == 2:
        from players.analysis.humanlike_recommend import rank_humanlike_discards
        ranks = rank_humanlike_discards(state, seat, hand, melds, dingque, opponents, legal_discards=disc_list, algorithm=recommendation_algorithm, preset_id=humanlike_preset)
        """if use_f0011:
            from players.analysis.integrated_discard import rank_discards_f0011

            ranks = rank_discards_f0011(
                state,
                seat,
                hand,
                melds,
                dingque,
                opponents,
                legal_discards=disc_list,
                f0010_top_k=f0011_top_k,
                seed=abs(hash(state.game_id)) % (2**31),
            )
        else:
            ranks = rank_discards(
                state,
                seat,
                hand,
                melds,
                dingque,
                opponents,
                legal_discards=disc_list,
            )"""
    if humanlike_preset and ranks:
        from players.humanlike.personality_presets import apply_personality_preset
        # Stable style adjustment over the existing legal ranking; no new actions.
        weights = {"speed": 0.35, "hand_value": 0.25, "defense": 0.25, "flexibility": 0.15}
        try:
            probe = {"profile": {}, "cognitive_parameters": {"GP-025": {}, "GP-026": {}}}
            cfg = apply_personality_preset(probe, humanlike_preset)
            weights = cfg["cognitive_parameters"]["GP-026"].get("decision_weights", weights)
            defense = float(cfg["profile"].get("defense_awareness", 0.55))
            big = float(cfg["profile"].get("big_hand_preference", 0.45))
        except Exception:
            defense, big = 0.55, 0.45
        for a in ranks:
            a.score += (defense - 0.55) * (1.0 if a.danger in ("high", "critical") else -0.15)
            a.score += (big - 0.45) * 0.01 * float(a.ukeire_after)
        ranks.sort(key=lambda a: (-a.score, a.tile_id))
        ranks = [type(a)(a.tile_id, i + 1, a.shanten_after, a.ukeire_after, a.danger, a.score, a.mark, list(a.ukeire_tiles or [])) for i, a in enumerate(ranks)]

    uniq: list[str] = []
    seen: set[str] = set()
    for t in hand:
        if t.id not in seen:
            seen.add(t.id)
            uniq.append(t.id)
    if use_f0011 and ranks:
        dang = {a.tile_id: a.danger for a in ranks}
        for tid in uniq:
            dang.setdefault(tid, "unknown")
    else:
        dang = danger_map_for_tiles(uniq, state, opponents)
        for a in ranks:
            dang[a.tile_id] = a.danger

    ms = (time.perf_counter() - t0) * 1000
    snap = AnalysisSnapshot(
        seat=seat,
        shanten=sh_val,
        ukeire=uke_ids,
        ukeire_count=uke_n,
        remain=remain,
        danger=dang,
        discard_ranks=ranks,
        opponents=opponents,
        generated_ms=round(ms, 2),
    )
    setattr(snap, "use_f0011", bool(use_f0011))
    return snap
