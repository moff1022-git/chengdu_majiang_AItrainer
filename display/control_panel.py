"""Main-window control panel (F0007/F0019): face toggles, HUD switches."""

from __future__ import annotations

from dataclasses import dataclass, field

import pygame

from display.hud_common import draw_text
from display.interior_scale import main_scale

PANEL_W = 216
PANEL_COLLAPSED_W = 28
ROW_H = 28
PAD = 10


@dataclass
class TableUIOptions:
    """Runtime toggles for main table rendering."""

    show_faces: dict[int, bool] = field(
        default_factory=lambda: {0: True, 1: True, 2: True, 3: True}
    )
    show_inference: bool = True
    show_strategy: bool = True
    show_discards: bool = True
    show_melds: bool = True
    # Settlement auto-advance (only effective when all seat windows used auto-start)
    auto_next_round: bool = False
    panel_expanded: bool = True
    focus_seat: int = 0
    humanlike_status: str = "关闭"

    def face_visible(self, seat: int) -> bool:
        return bool(self.show_faces.get(int(seat), True))

    def set_all_faces(self, on: bool) -> None:
        for k in list(self.show_faces.keys()):
            self.show_faces[k] = on

    def ensure_seats(self, n: int) -> None:
        for s in range(n):
            self.show_faces.setdefault(s, True)
        # drop extras
        for s in list(self.show_faces.keys()):
            if s >= n:
                del self.show_faces[s]


class ControlPanel:
    """SIDE_MID control switches (F0015); optional full-height legacy mode."""

    def __init__(self) -> None:
        self.options = TableUIOptions()
        self._hits: dict[str, pygame.Rect] = {}
        self._rect = pygame.Rect(0, 0, PANEL_W, 100)
        # When set, draw only inside this mid strip (F0015 SIDE 中 30%)
        self.region: pygame.Rect | None = None

    @property
    def width(self) -> int:
        if self.region is not None and self.options.panel_expanded:
            return max(PANEL_COLLAPSED_W, int(self.region.w))
        return PANEL_W if self.options.panel_expanded else PANEL_COLLAPSED_W

    def content_width(self, screen_w: int) -> int:
        return max(200, int(screen_w) - self.width)

    def set_region(self, rect: pygame.Rect | tuple[int, int, int, int] | None) -> None:
        if rect is None:
            self.region = None
            return
        if isinstance(rect, tuple):
            self.region = pygame.Rect(*rect)
        else:
            self.region = pygame.Rect(rect)

    def layout_rect(self, screen_w: int, screen_h: int) -> pygame.Rect:
        if self.region is not None and self.options.panel_expanded:
            self._rect = pygame.Rect(self.region)
            return self._rect
        w = self.width
        if self.region is not None and not self.options.panel_expanded:
            # collapsed: thin strip on right of full height
            self._rect = pygame.Rect(screen_w - PANEL_COLLAPSED_W, 0, PANEL_COLLAPSED_W, screen_h)
            return self._rect
        self._rect = pygame.Rect(screen_w - w, 0, w, screen_h)
        return self._rect

    def draw(
        self,
        screen: pygame.Surface,
        *,
        num_players: int = 4,
        auto_next_eligible: bool = False,
    ) -> None:
        self.options.ensure_seats(num_players)
        sw, sh = screen.get_size()
        ms = main_scale(sw, sh)
        pad = ms.pad
        row_h = ms.row_h
        self._draw_pad = pad
        self._draw_row_h = row_h
        self._draw_font = ms.font_body
        self._draw_font_sm = ms.font_small
        self._draw_font_title = ms.font_title
        panel = self.layout_rect(sw, sh)
        self._hits = {}

        # Backdrop
        overlay = pygame.Surface((panel.w, panel.h), pygame.SRCALPHA)
        overlay.fill((8, 22, 16, 230))
        screen.blit(overlay, panel.topleft)
        pygame.draw.line(
            screen, (70, 140, 100), (panel.x, 0), (panel.x + panel.w, 0), 1
        )
        pygame.draw.line(
            screen, (70, 140, 100), (panel.x, 0), (panel.x, panel.bottom), 2
        )

        if not self.options.panel_expanded:
            # Collapsed strip
            tab = pygame.Rect(panel.x + 4, sh // 2 - 40, max(16, pad * 3), 80)
            pygame.draw.rect(screen, (40, 100, 70), tab, border_radius=4)
            draw_text(
                screen,
                "»",
                (tab.x + 4, tab.y + 30),
                size=ms.font_title,
                color=(255, 255, 220),
            )
            self._hits["expand"] = tab
            return

        x0 = panel.x + pad
        y = panel.y + pad
        draw_text(
            screen,
            "控制面板",
            (x0, y),
            size=ms.font_title,
            color=(255, 245, 200),
        )
        y += row_h
        cb = max(18, int(22 * ms.s))
        collapse = pygame.Rect(panel.right - cb - pad, panel.y + pad, cb, cb)
        pygame.draw.rect(screen, (50, 80, 60), collapse, border_radius=3)
        draw_text(
            screen,
            "«",
            (collapse.x + 4, collapse.y + 2),
            size=ms.font_body,
        )
        self._hits["collapse"] = collapse

        y = self._toggle_row(
            screen, x0, y, "infer", "推理 HUD", self.options.show_inference
        )
        y = self._toggle_row(
            screen, x0, y, "strategy", "策略 HUD", self.options.show_strategy
        )
        y = self._toggle_row(
            screen, x0, y, "discards", "显示弃牌", self.options.show_discards
        )
        y = self._toggle_row(
            screen, x0, y, "melds", "显示副露", self.options.show_melds
        )
        y += max(2, pad // 2)
        # Settlement auto next-round (requires all seats auto-start)
        y = self._toggle_row(
            screen,
            x0,
            y,
            "auto_next",
            "结算自动下一局",
            bool(self.options.auto_next_round) and auto_next_eligible,
            enabled=auto_next_eligible,
        )
        hint_sz = getattr(self, "_draw_font_sm", 11)
        if not auto_next_eligible:
            draw_text(
                screen,
                "需四方「自动开始」",
                (x0 + 4, y - 2),
                size=hint_sz,
                color=(160, 150, 120),
            )
            y += max(12, row_h - 8)
        else:
            draw_text(
                screen,
                "结算页显示3秒后下一局",
                (x0 + 4, y - 2),
                size=hint_sz,
                color=(140, 200, 160),
            )
            y += max(12, row_h - 8)
        y += max(2, pad // 2)
        y = self._toggle_row(screen, x0, y, "humanlike", "人类化 AI 下局", self.options.humanlike_status == "开启")
        y = self._button_row(screen, x0, y, "humanlike_settings", "Humanlike 参数…")
        draw_text(
            screen,
            "各座明牌",
            (x0, y),
            size=getattr(self, "_draw_font_title", 15),
            color=(200, 230, 200),
        )
        y += row_h
        for s in range(num_players):
            on = self.options.face_visible(s)
            y = self._toggle_row(
                screen, x0, y, f"face_{s}", f"S{s} 明牌", on
            )
        y += max(2, pad // 2)
        y = self._button_row(screen, x0, y, "faces_all", "全部明牌")
        y = self._button_row(screen, x0, y, "faces_none", "全部暗牌")
        y += pad
        draw_text(
            screen,
            f"焦点 S{self.options.focus_seat}  (键1-4)",
            (x0, y),
            size=hint_sz,
            color=(180, 200, 220),
        )
        y += row_h
        draw_text(
            screen,
            "H=HUD  +/-速度",
            (x0, y),
            size=hint_sz,
            color=(150, 170, 160),
        )

    def _toggle_row(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        key: str,
        label: str,
        on: bool,
        *,
        enabled: bool = True,
    ) -> int:
        pad = int(getattr(self, "_draw_pad", PAD))
        row_h = int(getattr(self, "_draw_row_h", ROW_H))
        font_sz = int(getattr(self, "_draw_font", 14))
        box_s = max(12, min(22, row_h - 4))
        box = pygame.Rect(x, y, box_s, box_s)
        if not enabled:
            fill, border, txt = (35, 35, 35), (80, 80, 80), (140, 140, 130)
        else:
            fill = (30, 70, 50) if on else (40, 40, 40)
            border = (160, 220, 160) if on else (100, 100, 100)
            txt = (240, 245, 230)
        pygame.draw.rect(screen, fill, box, border_radius=3)
        pygame.draw.rect(screen, border, box, 2, border_radius=3)
        if on and enabled:
            pygame.draw.rect(
                screen, (100, 220, 140), box.inflate(-6, -6), border_radius=2
            )
        draw_text(screen, label, (x + box_s + 8, y + 2), size=font_sz, color=txt)
        hit = pygame.Rect(x, y, max(40, self.width - 2 * pad), row_h)
        self._hits[key] = hit
        return y + row_h

    def _button_row(
        self, screen: pygame.Surface, x: int, y: int, key: str, label: str
    ) -> int:
        pad = int(getattr(self, "_draw_pad", PAD))
        row_h = int(getattr(self, "_draw_row_h", ROW_H))
        font_sz = int(getattr(self, "_draw_font", 13))
        bh = max(18, row_h)
        r = pygame.Rect(x, y, max(40, self.width - 2 * pad - 8), bh)
        pygame.draw.rect(screen, (36, 90, 60), r, border_radius=4)
        pygame.draw.rect(screen, (120, 180, 140), r, 1, border_radius=4)
        draw_text(screen, label, (r.x + 10, r.y + 5), size=font_sz, color=(255, 255, 240))
        self._hits[key] = r
        return y + bh + max(2, pad // 2)

    def hit(self, pos: tuple[int, int]) -> str | None:
        for key, rect in self._hits.items():
            if rect.collidepoint(pos):
                return key
        if self._rect.collidepoint(pos):
            return "panel_bg"
        return None

    def handle_click(
        self,
        pos: tuple[int, int],
        *,
        num_players: int = 4,
        auto_next_eligible: bool = False,
    ) -> bool:
        """Apply click; return True if consumed."""
        self.options.ensure_seats(num_players)
        key = self.hit(pos)
        if key is None:
            return False
        if key in ("panel_bg",):
            return True
        if key == "collapse":
            self.options.panel_expanded = False
            return True
        if key == "expand":
            self.options.panel_expanded = True
            return True
        if key == "infer":
            self.options.show_inference = not self.options.show_inference
            return True
        if key == "strategy":
            self.options.show_strategy = not self.options.show_strategy
            return True
        if key == "discards":
            self.options.show_discards = not self.options.show_discards
            return True
        if key == "melds":
            self.options.show_melds = not self.options.show_melds
            return True
        if key == "auto_next":
            # Only effective when all seats used auto-start this session hand
            if not auto_next_eligible:
                return True  # consume click but no change
            self.options.auto_next_round = not self.options.auto_next_round
            return True
        if key == "faces_all":
            self.options.set_all_faces(True)
            return True
        if key == "faces_none":
            self.options.set_all_faces(False)
            return True
        if key.startswith("face_"):
            try:
                s = int(key.split("_", 1)[1])
                self.options.show_faces[s] = not self.options.face_visible(s)
            except Exception:
                pass
            return True
        return True
