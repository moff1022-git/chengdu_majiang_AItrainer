"""Ring buffer for main-window play event log (F0018 P4 — display only)."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class PlayEvent:
    seq: int
    kind: str  # discard | pong | gang | hu | pass | info
    seat: int | None
    text: str
    tile_id: str | None = None


class PlayEventLog:
    """Bounded FIFO of display-only action lines."""

    def __init__(self, capacity: int = 200) -> None:
        self.capacity = max(1, int(capacity))
        self._buf: deque[PlayEvent] = deque(maxlen=self.capacity)
        self._seq = 0

    def clear(self) -> None:
        self._buf.clear()

    def append(
        self,
        kind: str,
        text: str,
        *,
        seat: int | None = None,
        tile_id: str | None = None,
    ) -> PlayEvent:
        self._seq += 1
        ev = PlayEvent(
            seq=self._seq,
            kind=str(kind),
            seat=seat,
            text=str(text),
            tile_id=tile_id,
        )
        self._buf.append(ev)
        return ev

    def extend(self, events: Iterable[PlayEvent]) -> None:
        for e in events:
            self._buf.append(e)

    def lines(self, limit: int | None = None) -> list[PlayEvent]:
        items = list(self._buf)
        if limit is not None and limit >= 0:
            return items[-int(limit) :]
        return items

    def texts(self, limit: int | None = 40) -> list[str]:
        return [e.text for e in self.lines(limit)]

    def __len__(self) -> int:
        return len(self._buf)

    def note_from_action(self, action: Any) -> PlayEvent | None:
        """Best-effort format from engine Action-like objects."""
        if action is None:
            return None
        try:
            kind = str(getattr(action, "type", None) or getattr(action, "kind", "info"))
            seat = getattr(action, "seat", None)
            if seat is not None:
                seat = int(seat)
            tid = getattr(action, "tile_id", None) or getattr(action, "tile", None)
            if tid is not None:
                tid = str(tid)
            seat_s = f"S{seat}" if seat is not None else "?"
            try:
                from display.play_log_format import tile_zh

                tid_zh = tile_zh(tid) if tid else "?"
            except Exception:
                tid_zh = tid or "?"
            if kind in ("discard", "DISCARD"):
                text = f"{seat_s} 打出 {tid_zh}"
                return self.append("discard", text, seat=seat, tile_id=tid)
            if kind in ("pong", "PONG", "peng"):
                text = f"{seat_s} 碰 {tid_zh}".strip()
                return self.append("pong", text, seat=seat, tile_id=tid)
            if kind in ("gang", "GANG", "an_gang", "jia_gang", "ming_gang"):
                text = f"{seat_s} 杠 {tid_zh}".strip()
                return self.append("gang", text, seat=seat, tile_id=tid)
            if kind in ("hu", "HU", "zimo", "ron"):
                text = f"{seat_s} 胡"
                return self.append("hu", text, seat=seat, tile_id=tid)
            if kind in ("pass", "PASS", "skip"):
                text = f"{seat_s} 过"
                return self.append("pass", text, seat=seat)
            text = f"{seat_s} {kind}"
            return self.append("info", text, seat=seat, tile_id=tid)
        except Exception:
            return None
