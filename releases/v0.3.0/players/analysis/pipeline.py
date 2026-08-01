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
from players.analysis.strategy import rank_discards
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

    if use_f0011 is None:
        use_f0011 = _env_f0011()

    disc_list = list(legal_discards) if legal_discards is not None else None
    ranks: list[DiscardAdvice] = []
    if disc_list is not None or len(hand) % 3 == 2:
        if use_f0011:
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
            )

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
