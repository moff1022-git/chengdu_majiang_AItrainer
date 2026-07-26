"""SIDE_TOP scoreboard strip for main window (F0015/F0018)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame

from display.hud_common import draw_text
from display.interior_scale import main_scale

if TYPE_CHECKING:
    from engine.state import GameState


def draw_side_scoreboard(
    screen: pygame.Surface,
    rect: pygame.Rect | tuple[int, int, int, int],
    state: GameState | None,
    *,
    focus_seat: int = 0,
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
    overlay.fill((10, 28, 20, 220))
    screen.blit(overlay, r.topleft)
    pygame.draw.rect(screen, (60, 120, 90), r, 1)

    x0 = r.x + ms.pad
    y = r.y + max(2, ms.pad // 2)
    draw_text(
        screen, "积分 · 状态", (x0, y), size=ms.font_title, color=(255, 240, 180)
    )
    y += ms.row_h
    if state is None:
        draw_text(
            screen, "（等待开局）", (x0, y), size=ms.font_body, color=(160, 180, 160)
        )
        return

    row_h = max(ms.font_body + 4, min(ms.row_h, (r.h - ms.row_h) // max(1, state.num_players)))
    for p in state.players:
        if y + ms.font_body > r.bottom - 4:
            break
        st = str(getattr(p, "status", "") or "")
        if st == "finished":
            st = "已胡"
        elif st == "active":
            st = "对局中"
        mark = "▶" if int(p.seat) == int(focus_seat) else " "
        color = (255, 230, 140) if int(p.seat) == int(focus_seat) else (210, 220, 200)
        line = f"{mark}S{p.seat}  {int(getattr(p, 'score', 0))}  {st}"
        draw_text(screen, line, (x0, y), size=ms.font_body, color=color)
        y += row_h
