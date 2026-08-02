"""Discard recommendation display rules for seat window (F0012).

Uses the same ranking list as ``rank_discards`` / F0011 (already sorted best-first).
"""

from __future__ import annotations

from typing import Any, Sequence


_SUIT_ORDER = {"wan": 0, "tong": 1, "tiao": 2}


def sort_ukeire_tile_ids(tile_ids: Sequence[str]) -> list[str]:
    """Order: 万→筒→条, then rank ascending."""

    def key(tid: str) -> tuple[int, int, str]:
        parts = str(tid).split("_", 1)
        suit = parts[0] if parts else ""
        try:
            rank = int(parts[1]) if len(parts) > 1 else 0
        except Exception:
            rank = 0
        return (_SUIT_ORDER.get(suit, 9), rank, str(tid))

    # unique preserve after sort
    seen: set[str] = set()
    out: list[str] = []
    for tid in sorted((str(t) for t in tile_ids), key=key):
        if tid not in seen:
            seen.add(tid)
            out.append(tid)
    return out


def _as_row(item: Any) -> dict[str, Any]:
    if isinstance(item, dict):
        return item
    return {
        "tile_id": getattr(item, "tile_id", None),
        "rank": getattr(item, "rank", None),
        "shanten_after": getattr(item, "shanten_after", None),
        "ukeire_after": getattr(item, "ukeire_after", None),
        "ukeire_tiles": list(getattr(item, "ukeire_tiles", None) or []),
        "score": getattr(item, "score", None),
        "danger": getattr(item, "danger", None),
        "mark": getattr(item, "mark", None),
    }


def build_discard_recommendations(
    discard_ranks: Sequence[Any] | None,
    *,
    max_non_tenpai: int = 3,
) -> list[dict[str, Any]]:
    """Select tiles to mark + renumber order 1..n.

    - If any candidate has ``shanten_after == 0``: recommend **all** such tiles
      (stable order = input rank order).
    - Else: top ``max_non_tenpai`` by existing rank/score order.
    """
    if not discard_ranks:
        return []
    rows = [_as_row(x) for x in discard_ranks]
    rows = [r for r in rows if r.get("tile_id")]
    if not rows:
        return []

    def _sh_after(r: dict[str, Any]) -> int:
        sa = r.get("shanten_after")
        if sa is None:
            return 99
        try:
            return int(sa)
        except Exception:
            return 99

    tenpai = [r for r in rows if _sh_after(r) == 0]
    chosen = tenpai if tenpai else rows[: max(0, int(max_non_tenpai))]

    out: list[dict[str, Any]] = []
    for i, r in enumerate(chosen):
        uke = r.get("ukeire_tiles") or []
        if not isinstance(uke, list):
            uke = []
        sh_a = _sh_after(r)
        out.append(
            {
                "tile_id": str(r["tile_id"]),
                "order": i + 1,
                "shanten_after": sh_a,
                "is_tenpai": sh_a == 0,
                "ukeire_tiles": sort_ukeire_tile_ids([str(x) for x in uke]),
                "score": r.get("score"),
                "danger": r.get("danger"),
                "mark": r.get("mark"),
            }
        )
    return out


def recommendation_order_map(
    recs: Sequence[dict[str, Any]],
) -> dict[str, int]:
    """tile_id → display order number (1-based)."""
    m: dict[str, int] = {}
    for r in recs:
        tid = str(r.get("tile_id") or "")
        if tid and tid not in m:
            m[tid] = int(r.get("order") or 0)
    return m


def ukeire_for_focus(
    recs: Sequence[dict[str, Any]],
    focus_tile_id: str | None,
) -> list[str]:
    """Winning tiles to show above focused hand tile (empty if not tenpai rec)."""
    if not focus_tile_id:
        return []
    for r in recs:
        if str(r.get("tile_id")) == str(focus_tile_id) and r.get("is_tenpai"):
            return list(r.get("ukeire_tiles") or [])
    return []
