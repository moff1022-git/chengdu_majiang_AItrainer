"""SIDE_BOT play log panel for main window (F0018 P4 / F0024 detail)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from display.hud_common import draw_text
from display.interior_scale import main_scale

if TYPE_CHECKING:
    from display.play_event_log import PlayEventLog

# Colors aligned with event kinds (human-readable log)
_KIND_COLOR: dict[str, tuple[int, int, int]] = {
    "discard": (210, 225, 200),
    "draw": (150, 175, 200),
    "pong": (255, 220, 140),
    "gang": (255, 190, 110),
    "hu": (255, 230, 100),
    "score": (160, 230, 170),
    "pass": (150, 160, 150),
    "info": (190, 210, 190),
    "dice": (255, 230, 140),
}


def draw_play_log_panel(
    screen: pygame.Surface,
    rect: pygame.Rect | tuple[int, int, int, int],
    log: PlayEventLog | None,
    *,
    title: str = "出牌日志",
) -> None:
    if isinstance(rect, tuple):
        r = pygame.Rect(*rect)
    else:
        r = rect
    if r.w < 8 or r.h < 8:
        return
    sw, sh = screen.get_size()
    ms = main_scale(sw, sh)
    overlay = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
    overlay.fill((8, 20, 16, 230))
    screen.blit(overlay, r.topleft)
    pygame.draw.rect(screen, (50, 100, 80), r, 1)
    # gold top accent like human chrome
    pygame.draw.line(
        screen,
        (255, 193, 7),
        (r.x + 2, r.y + 1),
        (r.right - 2, r.y + 1),
        2,
    )

    x0 = r.x + ms.pad
    y = r.y + max(2, ms.pad // 2)
    n = len(log) if log is not None else 0
    draw_text(
        screen,
        f"{title} · {n}",
        (x0, y),
        size=ms.font_title,
        color=(200, 230, 200),
    )
    y += ms.row_h
    if log is None or n == 0:
        draw_text(
            screen, "（暂无记录）", (x0, y), size=ms.font_body, color=(120, 140, 120)
        )
        return

    line_h = max(12, ms.font_body + 3)
    max_lines = max(1, (r.bottom - y - 4) // line_h)
    # Prefer more chars for detailed lines
    max_chars = max(16, (r.w - 2 * ms.pad) // max(5, ms.font_body // 2))
    events = log.lines(limit=max_lines)
    for ev in events:
        if y + line_h > r.bottom - 2:
            break
        t = ev.text
        s = t if len(t) <= max_chars else t[: max_chars - 1] + "…"
        color = _KIND_COLOR.get(str(ev.kind), (190, 210, 190))
        draw_text(screen, s, (x0, y), size=ms.font_body, color=color)
        y += line_h
