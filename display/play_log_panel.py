"""SIDE_BOT play log panel for main window (F0018 P4)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from display.hud_common import draw_text
from display.interior_scale import main_scale

if TYPE_CHECKING:
    from display.play_event_log import PlayEventLog


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

    x0 = r.x + ms.pad
    y = r.y + max(2, ms.pad // 2)
    draw_text(screen, title, (x0, y), size=ms.font_title, color=(200, 230, 200))
    y += ms.row_h
    if log is None or len(log) == 0:
        draw_text(
            screen, "（暂无记录）", (x0, y), size=ms.font_body, color=(120, 140, 120)
        )
        return

    line_h = max(12, ms.font_body + 4)
    max_lines = max(1, (r.bottom - y - 4) // line_h)
    texts = log.texts(limit=max_lines)
    max_chars = max(12, r.w // max(6, ms.font_body // 2))
    for t in texts:
        if y + line_h > r.bottom - 2:
            break
        s = t if len(t) <= max_chars else t[: max_chars - 1] + "…"
        draw_text(screen, s, (x0, y), size=ms.font_body, color=(190, 210, 190))
        y += line_h
