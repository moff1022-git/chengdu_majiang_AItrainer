"""Discard ranking / strategy advice."""

from __future__ import annotations

from engine.action import Action, ActionType
from engine.shanten import shanten
from engine.state import GameState
from engine.tile import Tile, parse_tile
from players.analysis.danger import DANGER_PENALTY, danger_map_for_tiles
from players.analysis.remain import remain_map, ukeire_count
from players.analysis.types import DiscardAdvice, OpponentHint


def _remove_one(hand: list[Tile], tile_id: str) -> list[Tile]:
    out: list[Tile] = []
    removed = False
    for t in hand:
        if not removed and t.id == tile_id:
            removed = True
            continue
        out.append(t)
    return out


def rank_discards(
    state: GameState,
    seat: int,
    hand: list[Tile],
    melds: list,
    dingque,
    opponents: list[OpponentHint],
    *,
    legal_discards: list[Action] | None = None,
    use_f0011: bool = False,
    f0011_top_k: int = 3,
) -> list[DiscardAdvice]:
    if use_f0011:
        from players.analysis.integrated_discard import rank_discards_f0011

        return rank_discards_f0011(
            state,
            seat,
            hand,
            melds,
            dingque,
            opponents,
            legal_discards=legal_discards,
            f0010_top_k=f0011_top_k,
            seed=abs(hash(getattr(state, "game_id", "") or "0")) % (2**31),
        )
    remain = remain_map(state, seat)
    if legal_discards is not None:
        cands = []
        for a in legal_discards:
            if a.type == ActionType.DISCARD and a.tiles:
                cands.append(a.tiles[0].id)
        # unique preserve order
        seen = set()
        tile_ids = []
        for tid in cands:
            if tid not in seen:
                seen.add(tid)
                tile_ids.append(tid)
    else:
        seen = set()
        tile_ids = []
        for t in hand:
            if t.id not in seen:
                seen.add(t.id)
                tile_ids.append(t.id)

    dangers = danger_map_for_tiles(tile_ids, state, opponents)
    scored: list[tuple[float, DiscardAdvice]] = []

    for tid in tile_ids:
        trial = _remove_one(hand, tid)
        try:
            s = shanten(trial, melds, dingque)
            sh_after = s.shanten
            uke = [t.id for t in (s.ukeire or [])]
            uke_n = ukeire_count(uke, remain)
        except Exception:
            sh_after = 8
            uke = []
            uke_n = 0
        dang = dangers.get(tid, "unknown")
        score = -4.0 * sh_after + 0.15 * uke_n - DANGER_PENALTY.get(dang, 0.5)
        scored.append(
            (
                score,
                DiscardAdvice(
                    tile_id=tid,
                    rank=0,
                    shanten_after=sh_after,
                    ukeire_after=uke_n,
                    danger=dang,
                    score=score,
                    mark="none",
                    ukeire_tiles=list(uke),
                ),
            )
        )

    scored.sort(key=lambda x: (-x[0], x[1].tile_id))
    out: list[DiscardAdvice] = []
    for i, (_, adv) in enumerate(scored):
        mark = "none"
        if i == 0:
            mark = "best"
        elif i == 1:
            mark = "second"
        if adv.danger in ("critical", "high") and mark != "best":
            mark = "avoid"
        out.append(
            DiscardAdvice(
                tile_id=adv.tile_id,
                rank=i + 1,
                shanten_after=adv.shanten_after,
                ukeire_after=adv.ukeire_after,
                danger=adv.danger,
                score=adv.score,
                mark=mark,
                ukeire_tiles=list(adv.ukeire_tiles or []),
            )
        )
    return out
