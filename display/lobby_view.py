"""Lobby / game cover — chrome aligned with human seat window UI."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame

from display.hud_common import draw_text
from display.ui_chrome import (
    BG_DEEP,
    TEXT_DIM,
    TEXT_GOLD,
    TEXT_MUTED,
    TEXT_TITLE,
    draw_footer_zone,
    draw_header_bar,
    draw_panel,
    draw_primary_button,
    draw_setting_row,
    metrics,
)

if TYPE_CHECKING:
    from display.asset_manager import AssetManager

# Clickable control ids
CTL_MODE = "mode"
CTL_PLAYERS = "players"
CTL_EXCHANGE = "exchange"
CTL_ROUNDS = "rounds"
CTL_THEME = "theme"
CTL_START = "start"

_GAME_MODES = [
    ("blood_battle", "血战到底"),
]

_PLAYER_PRESETS = [
    ("human,rule_ai,rule_ai,rule_ai", "1人类 + 3AI"),
    ("human,human,rule_ai,rule_ai", "2人类 + 2AI"),
    ("human,human,human,rule_ai", "3人类 + 1AI"),
    ("rule_ai,rule_ai,rule_ai,rule_ai", "4AI（座位窗确认）"),
    ("human,random,random,random", "1人类 + 3随机"),
]

_ROUND_OPTIONS = [1, 2, 4, 8]


class LobbyView:
    def __init__(self, assets: AssetManager) -> None:
        self.assets = assets
        self._bg: pygame.Surface | None = None
        self.start_rect = pygame.Rect(0, 0, 240, 64)
        self.theme_rect = pygame.Rect(0, 0, 200, 40)
        self._hit: dict[str, pygame.Rect] = {}
        self._last_cfg: dict[str, Any] = {}

    def draw(
        self,
        screen: pygame.Surface,
        *,
        theme: str,
        num_players: int,
        players_spec: str,
        spectator: str,
        game_mode: str = "blood_battle",
        enable_exchange: bool = True,
        num_rounds: int = 1,
    ) -> None:
        w, h = screen.get_size()
        m = metrics(w, h)
        self._hit = {}
        self._last_cfg = {
            "theme": theme,
            "players_spec": players_spec,
            "game_mode": game_mode,
            "enable_exchange": enable_exchange,
            "num_rounds": num_rounds,
        }

        # Soft table-like base (seat mid color family), optional bg image dimmed
        screen.fill(BG_DEEP)
        try:
            if self._bg is None or self._bg.get_size() != (w, h):
                raw = self.assets.bg("lobby")
                self._bg = pygame.transform.smoothscale(raw, (w, h))
            dim = pygame.Surface((w, h), pygame.SRCALPHA)
            dim.fill((8, 22, 16, 160))
            screen.blit(self._bg, (0, 0))
            screen.blit(dim, (0, 0))
        except Exception:
            pass

        try:
            from version import APP_VERSION

            ver_s = f"v{APP_VERSION}"
        except Exception:
            ver_s = ""

        # ---- HEADER (seat OP_INFO style) ----
        body_top = draw_header_bar(
            screen,
            m,
            title="成都麻将 AI 训练器",
            subtitle=f"游戏封面 · 设置后点「开始」  {ver_s}".strip(),
        )

        # Optional small logo in header right
        try:
            logo = self.assets.icon("logo")
            lw = min(120, max(48, m.header_h - 12), w // 6)
            logo = self.assets.scale_to_width(logo, lw)
            screen.blit(
                logo,
                (w - m.margin - logo.get_width(), max(4, (m.header_h - logo.get_height()) // 2)),
            )
        except Exception:
            pass

        # ---- FOOTER first (reserve space so body never overlaps) ----
        footer = draw_footer_zone(screen, m)
        btn_w = min(280, max(160, w // 3))
        btn_h = m.btn_h
        self.start_rect = pygame.Rect(0, 0, btn_w, btn_h)
        self.start_rect.centerx = w // 2
        self.start_rect.centery = footer.y + footer.h // 2 - 8
        # keep inside footer
        if self.start_rect.bottom > footer.bottom - 4:
            self.start_rect.bottom = footer.bottom - 4
        if self.start_rect.top < footer.top + 4:
            self.start_rect.top = footer.top + 4
        draw_primary_button(
            screen,
            self.start_rect,
            "开  始",
            font_size=m.font_sub + 2,
            radius=m.radius,
        )
        self._hit[CTL_START] = self.start_rect
        hint_y = min(self.start_rect.bottom + 4, footer.bottom - m.font_small - 4)
        draw_text(
            screen,
            "ENTER=开始  ESC=退出  ·  对局中座位窗保留至退出",
            (m.margin, hint_y),
            size=m.font_small,
            color=TEXT_DIM,
        )

        # ---- BODY: settings card between header and footer ----
        body_bottom = footer.top - m.gap
        body_h = max(80, body_bottom - body_top)
        panel_w = min(560, max(240, w - 2 * m.margin))
        panel_x = (w - panel_w) // 2

        n_rows = 5
        # Fit all rows + padding inside body without clipping
        pad = m.gap
        inner_h = body_h - 2 * pad
        row_h = max(32, min(m.row_h, (inner_h - pad * (n_rows - 1)) // n_rows))
        panel_h = n_rows * row_h + pad * (n_rows + 1)
        if panel_h > body_h:
            # shrink rows further
            row_h = max(28, (body_h - pad * (n_rows + 1)) // n_rows)
            panel_h = n_rows * row_h + pad * (n_rows + 1)
        panel_y = body_top + max(0, (body_h - panel_h) // 2)
        # clamp so panel stays in body
        if panel_y + panel_h > body_bottom:
            panel_y = max(body_top, body_bottom - panel_h)

        panel = pygame.Rect(panel_x, panel_y, panel_w, min(panel_h, body_bottom - panel_y))
        draw_panel(
            screen,
            panel,
            radius=m.radius,
            alpha=235,
        )
        # section label
        draw_text(
            screen,
            "对局设置",
            (panel.x + pad, panel.y + 4),
            size=m.font_small,
            color=TEXT_GOLD,
        )

        mode_label = next(
            (lab for k, lab in _GAME_MODES if k == game_mode),
            game_mode,
        )
        players_label = next(
            (lab for k, lab in _PLAYER_PRESETS if k == players_spec),
            players_spec,
        )
        rows = [
            (CTL_MODE, "游戏模式", mode_label, "点击切换"),
            (CTL_PLAYERS, "玩家配置", players_label, "点击切换"),
            (
                CTL_EXCHANGE,
                "换三张",
                "开启" if enable_exchange else "关闭",
                "点击开关",
            ),
            (CTL_ROUNDS, "轮数", f"{num_rounds} 局", "1/2/4/8"),
            (CTL_THEME, "主题", theme, "green/blue"),
        ]

        # rows start below section title
        y = panel.y + max(pad + m.font_small + 4, pad * 2)
        avail_bottom = panel.bottom - pad
        for key, label, value, hint in rows:
            if y + row_h - 6 > avail_bottom:
                break
            row = pygame.Rect(panel.x + pad, y, panel.w - 2 * pad, row_h - 6)
            draw_setting_row(
                screen,
                row,
                label,
                value,
                hint,
                font_body=m.font_body,
                font_small=m.font_small,
                radius=max(4, m.radius - 2),
            )
            self._hit[key] = row
            y += row_h

        self.theme_rect = self._hit.get(CTL_THEME, pygame.Rect(0, 0, 0, 0))

        # spectator note (non-clickable) under panel if space
        note_y = panel.bottom + 4
        if note_y + m.font_small < footer.top - 4:
            draw_text(
                screen,
                f"观战视角: {spectator}  ·  座位窗风格一致（绿/金边 · 深桌面）",
                (m.margin, note_y),
                size=m.font_small,
                color=TEXT_MUTED,
            )

    def hit_start(self, pos: tuple[int, int]) -> bool:
        return self.start_rect.collidepoint(pos)

    def hit_theme(self, pos: tuple[int, int]) -> bool:
        return self.theme_rect.collidepoint(pos)

    def hit_control(self, pos: tuple[int, int]) -> str | None:
        """Return control id under click, or None."""
        for key, rect in self._hit.items():
            if rect.collidepoint(pos):
                return key
        return None

    def cycle_mode(self, current: str) -> str:
        keys = [k for k, _ in _GAME_MODES]
        if current not in keys:
            return keys[0]
        return keys[(keys.index(current) + 1) % len(keys)]

    def cycle_players(self, current: str) -> str:
        keys = [k for k, _ in _PLAYER_PRESETS]
        if current not in keys:
            return keys[0]
        return keys[(keys.index(current) + 1) % len(keys)]

    def cycle_rounds(self, current: int) -> int:
        if current not in _ROUND_OPTIONS:
            return _ROUND_OPTIONS[0]
        i = _ROUND_OPTIONS.index(current)
        return _ROUND_OPTIONS[(i + 1) % len(_ROUND_OPTIONS)]
