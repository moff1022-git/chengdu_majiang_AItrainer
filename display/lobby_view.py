"""Lobby / game cover: mode, exchange, rounds, theme, start (resize-aware)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame

from display.hud_common import draw_text

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
    ("human,rule_ai,rule_ai,rule_ai", "人类 + 3AI"),
    ("rule_ai,rule_ai,rule_ai,rule_ai", "4AI（座位窗确认）"),
    ("human,random,random,random", "人类 + 3随机"),
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
        cx = w // 2
        self._hit = {}
        self._last_cfg = {
            "theme": theme,
            "players_spec": players_spec,
            "game_mode": game_mode,
            "enable_exchange": enable_exchange,
            "num_rounds": num_rounds,
        }

        if self._bg is None or self._bg.get_size() != (w, h):
            raw = self.assets.bg("lobby")
            self._bg = pygame.transform.smoothscale(raw, (w, h))
        screen.blit(self._bg, (0, 0))

        # Title / logo
        title_y = max(28, h // 18)
        try:
            logo = self.assets.icon("logo")
            logo = self.assets.scale_to_width(logo, min(320, w // 3))
            screen.blit(logo, (cx - logo.get_width() // 2, title_y))
            subtitle_y = title_y + logo.get_height() + 8
        except FileNotFoundError:
            draw_text(
                screen,
                "成都麻将 AI 训练器",
                (cx - 140, title_y),
                size=32,
                color=(255, 250, 220),
            )
            subtitle_y = title_y + 48

        draw_text(
            screen,
            "游戏封面 · 设置后点击「开始」进入对局",
            (cx - 180, subtitle_y),
            size=18,
            color=(255, 230, 140),
        )

        # Settings panel
        panel_w = min(520, max(200, w - 40))
        panel_x = cx - panel_w // 2
        panel_y = min(subtitle_y + 36, max(40, h // 3))
        # Keep row/panel sizes positive even on tiny or just-resized surfaces
        avail = max(120, h - panel_y - 120)
        row_h = max(36, min(56, avail // 6))
        panel_h = max(row_h * 5 + 24, 200)
        if panel_y + panel_h > h - 40:
            panel_h = max(160, h - panel_y - 40)
            row_h = max(28, (panel_h - 24) // 5)
        panel = pygame.Rect(int(panel_x), int(panel_y), int(panel_w), int(panel_h))
        try:
            pygame.draw.rect(screen, (8, 28, 22), panel, border_radius=10)
            pygame.draw.rect(screen, (80, 160, 120), panel, 2, border_radius=10)
        except Exception:
            # Fallback without border_radius (older / unstable SDL surfaces)
            pygame.draw.rect(screen, (8, 28, 22), panel)
            pygame.draw.rect(screen, (80, 160, 120), panel, 2)

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
            (CTL_ROUNDS, "轮数", f"{num_rounds} 局", "点击切换 1/2/4/8"),
            (CTL_THEME, "主题", theme, "点击切换 green/blue"),
        ]

        y = panel_y + 12
        for key, label, value, hint in rows:
            row = pygame.Rect(panel_x + 12, y, panel_w - 24, row_h - 8)
            pygame.draw.rect(screen, (20, 50, 40), row, border_radius=6)
            pygame.draw.rect(screen, (100, 170, 130), row, 1, border_radius=6)
            draw_text(
                screen,
                label,
                (row.x + 12, row.y + 8),
                size=16,
                color=(180, 220, 200),
            )
            draw_text(
                screen,
                value,
                (row.x + 140, row.y + 6),
                size=20,
                color=(255, 255, 230),
            )
            draw_text(
                screen,
                hint,
                (row.right - 160, row.y + 10),
                size=13,
                color=(160, 180, 160),
            )
            self._hit[key] = row
            y += row_h

        self.theme_rect = self._hit.get(CTL_THEME, pygame.Rect(0, 0, 0, 0))

        # Start button — plain solid color (no background image asset)
        btn_w = min(260, max(180, w // 3))
        btn_h = 64
        self.start_rect = pygame.Rect(0, 0, btn_w, btn_h)
        self.start_rect.center = (cx, h - max(70, h // 12))
        pygame.draw.rect(screen, (40, 120, 80), self.start_rect, border_radius=8)
        pygame.draw.rect(screen, (80, 180, 120), self.start_rect, 2, border_radius=8)
        draw_text(
            screen,
            "开  始",
            (self.start_rect.centerx - 28, self.start_rect.centery - 12),
            size=22,
            color=(255, 255, 240),
        )
        self._hit[CTL_START] = self.start_rect

        draw_text(
            screen,
            "ENTER=开始  ESC=退出  |  对局中座位窗会保留至退出程序",
            (max(20, cx - 240), h - max(36, h // 24)),
            size=14,
            color=(200, 210, 190),
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
