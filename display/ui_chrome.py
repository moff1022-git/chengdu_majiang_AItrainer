"""
Shared chrome aligned with human seat window (TkSeatApp) visuals.

Palette / panel / button helpers for MAIN lobby & result scenes so they match
OP_INFO / OP_STATUS / settings strips in players/seat_window.py.
"""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from display.hud_common import draw_text

# --- Colors (seat_window play theme) ---
BG_DEEP = (10, 25, 20)  # #0a1914
BG_PANEL = (20, 53, 40)  # #143528
BG_ROW = (13, 40, 24)  # #0d2818
BG_CARD = (15, 36, 28)  # #0f241c
BG_ACCENT = (26, 40, 24)  # #1a2818
BG_BTN = (46, 125, 79)  # #2e7d4f
BG_BTN_HOVER = (56, 142, 90)
BORDER_GREEN = (102, 187, 106)  # #66bb6a
BORDER_TEAL = (77, 182, 172)  # #4db6ac
BORDER_GOLD = (255, 193, 7)  # #ffc107
BORDER_SOFT = (100, 170, 130)
TEXT_TITLE = (255, 250, 220)
TEXT_GOLD = (255, 224, 130)  # #ffe082
TEXT_STATUS = (255, 224, 140)  # #ffe08c
TEXT_MUTED = (200, 220, 200)
TEXT_DIM = (160, 180, 160)
TEXT_VALUE = (255, 255, 230)
TEXT_NEG = (255, 140, 140)
TEXT_POS = (160, 230, 160)


@dataclass(frozen=True)
class LayoutMetrics:
    """Responsive sizes from window; never zero."""

    w: int
    h: int
    margin: int
    gap: int
    font_title: int
    font_sub: int
    font_body: int
    font_small: int
    header_h: int
    footer_h: int
    row_h: int
    btn_h: int
    radius: int


def metrics(w: int, h: int) -> LayoutMetrics:
    w = max(320, int(w))
    h = max(240, int(h))
    # Reference human full ~885×498 (UI design 1080p class)
    s = min(w / 885.0, h / 498.0, 1.35)
    s = max(0.55, s)
    margin = max(12, int(round(16 * s)))
    gap = max(6, int(round(10 * s)))
    return LayoutMetrics(
        w=w,
        h=h,
        margin=margin,
        gap=gap,
        font_title=max(16, int(round(26 * s))),
        font_sub=max(13, int(round(18 * s))),
        font_body=max(12, int(round(16 * s))),
        font_small=max(11, int(round(13 * s))),
        header_h=max(44, int(round(min(h * 0.12, 72 * s)))),
        footer_h=max(72, int(round(min(h * 0.18, 110 * s)))),
        row_h=max(36, int(round(min(52 * s, h * 0.09)))),
        btn_h=max(40, int(round(min(56 * s, h * 0.1)))),
        radius=max(4, int(round(8 * s))),
    )


def fill_base(screen: pygame.Surface, color: tuple[int, int, int] = BG_DEEP) -> None:
    screen.fill(color)


def draw_panel(
    screen: pygame.Surface,
    rect: pygame.Rect,
    *,
    fill: tuple[int, int, int] = BG_PANEL,
    border: tuple[int, int, int] = BORDER_GREEN,
    width: int = 2,
    radius: int = 8,
    alpha: int | None = 230,
) -> None:
    if rect.w < 2 or rect.h < 2:
        return
    if alpha is not None and alpha < 255:
        surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        r, g, b = fill
        surf.fill((r, g, b, max(0, min(255, alpha))))
        try:
            pygame.draw.rect(
                surf, (*border, 240), surf.get_rect(), width, border_radius=radius
            )
        except Exception:
            pygame.draw.rect(surf, (*border, 240), surf.get_rect(), width)
        screen.blit(surf, rect.topleft)
    else:
        try:
            pygame.draw.rect(screen, fill, rect, border_radius=radius)
            pygame.draw.rect(screen, border, rect, width, border_radius=radius)
        except Exception:
            pygame.draw.rect(screen, fill, rect)
            pygame.draw.rect(screen, border, rect, width)


def draw_header_bar(
    screen: pygame.Surface,
    m: LayoutMetrics,
    title: str,
    subtitle: str = "",
) -> int:
    """Top strip like seat OP_INFO. Returns y below header."""
    rect = pygame.Rect(0, 0, m.w, m.header_h)
    draw_panel(
        screen,
        rect,
        fill=BG_DEEP,
        border=BORDER_TEAL,
        width=1,
        radius=0,
        alpha=None,
    )
    # bottom gold accent line
    pygame.draw.line(
        screen,
        BORDER_GOLD,
        (m.margin, m.header_h - 2),
        (m.w - m.margin, m.header_h - 2),
        2,
    )
    draw_text(
        screen,
        title,
        (m.margin + 4, max(6, m.header_h // 2 - m.font_title // 2 - (8 if subtitle else 0))),
        size=m.font_title,
        color=TEXT_TITLE,
    )
    if subtitle:
        draw_text(
            screen,
            subtitle,
            (m.margin + 4, m.header_h - m.font_sub - 10),
            size=m.font_small,
            color=TEXT_GOLD,
        )
    return m.header_h + m.gap


def draw_footer_zone(
    screen: pygame.Surface,
    m: LayoutMetrics,
) -> pygame.Rect:
    """Fixed footer band; content must stay above this.rect.top."""
    top = m.h - m.footer_h
    rect = pygame.Rect(0, top, m.w, m.footer_h)
    draw_panel(
        screen,
        rect,
        fill=BG_ROW,
        border=BORDER_GREEN,
        width=1,
        radius=0,
        alpha=None,
    )
    pygame.draw.line(
        screen,
        BORDER_TEAL,
        (0, top),
        (m.w, top),
        2,
    )
    return rect


def draw_primary_button(
    screen: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    *,
    font_size: int = 20,
    radius: int = 8,
) -> None:
    draw_panel(
        screen,
        rect,
        fill=BG_BTN,
        border=BORDER_GREEN,
        width=2,
        radius=radius,
        alpha=None,
    )
    # center-ish text (approx width)
    tw = max(8, len(label) * font_size // 2)
    draw_text(
        screen,
        label,
        (rect.centerx - tw // 2, rect.centery - font_size // 2 - 2),
        size=font_size,
        color=TEXT_VALUE,
    )


def draw_secondary_button(
    screen: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    *,
    font_size: int = 16,
    radius: int = 6,
) -> None:
    draw_panel(
        screen,
        rect,
        fill=BG_ACCENT,
        border=BORDER_GOLD,
        width=2,
        radius=radius,
        alpha=None,
    )
    tw = max(8, len(label) * font_size // 2)
    draw_text(
        screen,
        label,
        (rect.centerx - tw // 2, rect.centery - font_size // 2 - 1),
        size=font_size,
        color=TEXT_GOLD,
    )


def draw_setting_row(
    screen: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    value: str,
    hint: str,
    *,
    font_body: int,
    font_small: int,
    radius: int = 6,
) -> None:
    draw_panel(
        screen,
        rect,
        fill=BG_ROW,
        border=BORDER_SOFT,
        width=1,
        radius=radius,
        alpha=None,
    )
    pad = max(8, rect.h // 6)
    draw_text(
        screen,
        label,
        (rect.x + pad, rect.y + pad),
        size=font_small,
        color=TEXT_MUTED,
    )
    # value left of center-ish
    vx = rect.x + max(100, rect.w // 4)
    draw_text(
        screen,
        value,
        (vx, rect.y + max(4, pad - 2)),
        size=font_body,
        color=TEXT_VALUE,
    )
    # hint right-aligned approximate
    hx = max(rect.x + pad, rect.right - max(90, len(hint) * font_small // 2) - pad)
    draw_text(
        screen,
        hint,
        (hx, rect.y + pad + 2),
        size=font_small,
        color=TEXT_DIM,
    )
