"""First-person seat table rendering (human play + AI watch)."""

from __future__ import annotations

from typing import Any

import pygame

from display.asset_manager import AssetManager
from display.hud_common import blit_score, draw_text
from engine.action import Action, ActionType
from engine.tile import parse_tile, sorted_tiles
from players.view.responsive import compute_button_rows, compute_tile_grid


def _sort_hand_ids(hand_ids: list[str]) -> list[str]:
    """万 → 筒 → 条，同花色 1→9（展示与点选顺序）。"""
    tiles = []
    raw_keep: list[str] = []
    for tid in hand_ids:
        try:
            tiles.append(parse_tile(str(tid)))
        except Exception:
            raw_keep.append(str(tid))
    return [t.id for t in sorted_tiles(tiles)] + raw_keep


class PlayerView:
    def __init__(self, assets: AssetManager, seat: int) -> None:
        self.assets = assets
        self.seat = seat
        self.selected: list[str] = []  # tile ids for multi-select (exchange)
        self.hand_rects: list[tuple[str, pygame.Rect]] = []
        self.button_rects: dict[str, pygame.Rect] = {}
        self.mode: str = "play"  # play | watch
        # F0004 ready-confirm hit targets
        self.ready_start_rect = pygame.Rect(0, 0, 0, 0)
        self.ready_auto_rect = pygame.Rect(0, 0, 0, 0)

    def draw(
        self,
        screen: pygame.Surface,
        view: dict[str, Any],
        phase: str,
        legal: list[Action],
        hints: dict | None = None,
        *,
        status_note: str = "",
    ) -> None:
        w, h = screen.get_size()
        try:
            bg = self.assets.bg("table")
            bg = pygame.transform.smoothscale(bg, (w, h))
            screen.blit(bg, (0, 0))
        except Exception:
            screen.fill((20, 50, 35))

        # Always-visible chrome (never "background only")
        header = pygame.Rect(8, 8, max(120, w - 16), 72)
        pygame.draw.rect(screen, (10, 25, 20), header)
        pygame.draw.rect(screen, (80, 160, 120), header, 2)

        role = "人类操作" if self.mode == "play" else "AI 观战(只读)"
        draw_text(
            screen,
            f"座位 S{self.seat}  [{role}]  phase={phase}",
            (16, 14),
            size=18,
            color=(255, 255, 240),
        )
        draw_text(
            screen,
            f"剩余牌墙: {view.get('wall_remaining', '—')}",
            (16, 40),
            size=16,
            color=(200, 230, 200),
        )
        if status_note:
            draw_text(
                screen,
                status_note,
                (16, 88),
                size=16,
                color=(255, 220, 120),
            )

        me = None
        for p in view.get("players") or []:
            try:
                if int(p.get("seat", -1)) == self.seat:
                    me = p
                    break
            except (TypeError, ValueError):
                continue

        if not view or me is None:
            # Empty / connecting skeleton
            box = pygame.Rect(24, 120, max(100, w - 48), max(80, h - 200))
            pygame.draw.rect(screen, (15, 35, 28), box)
            pygame.draw.rect(screen, (120, 180, 140), box, 2)
            draw_text(
                screen,
                "等待主程序推送牌局数据…",
                (box.x + 16, box.y + 24),
                size=20,
                color=(255, 240, 180),
            )
            draw_text(
                screen,
                "若长时间无变化：确认已从仓库根目录启动 main.py human",
                (box.x + 16, box.y + 56),
                size=14,
                color=(200, 200, 180),
            )
            self.hand_rects = []
            self.button_rects = {}
            return

        try:
            blit_score(
                screen, self.assets, int(me.get("score", 0)), (20, 100), size="md"
            )
        except Exception:
            draw_text(
                screen,
                f"分: {me.get('score', 0)}",
                (20, 100),
                size=18,
                color=(255, 220, 100),
            )

        # Button bar height first (may wrap) so hand/disc sit above it
        btn_zone = self._estimate_btn_zone(legal, phase, w, h)
        hand = _sort_hand_ids(list(me.get("hand") or []))
        hand_grid = self._draw_hand(screen, hand, h, btn_zone=btn_zone)

        # 本家副露（碰/杠）— 手牌上方
        melds = list(me.get("melds") or [])
        hand_top = h - btn_zone - 12
        if hand_grid is not None and hand_grid.n > 0:
            hand_top = hand_grid.cell_bottom_up(0, origin_x=16, bottom_y=h - btn_zone - 8)[1]
        if melds:
            self._draw_melds(screen, melds, w, h, hand_top=hand_top)

        # 弃牌：手牌上方区域，可多行
        disc_bottom = hand_top - 8
        self._draw_discards(
            screen, list(me.get("discard_pile") or [])[-24:], w, disc_bottom
        )

        # 对手信息靠右上，宽度随窗
        opp_x = max(8, w - min(360, max(180, w // 3)))
        y = 100
        for p in view.get("players") or []:
            try:
                ps = int(p.get("seat", -1))
            except (TypeError, ValueError):
                continue
            if ps == self.seat:
                continue
            meld_n = len(p.get("melds") or [])
            draw_text(
                screen,
                f"S{ps} 手={p.get('hand_count')} "
                f"副露={meld_n} 分={p.get('score')} {p.get('status')}",
                (opp_x, y),
                size=max(11, min(14, w // 50)),
                color=(220, 220, 200),
            )
            mx = opp_x
            my = y + 18
            opp_melds = list(p.get("melds") or [])[:4]
            flat: list[str] = []
            for m in opp_melds:
                tid = m.get("tile_id") if isinstance(m, dict) else None
                kind = (m.get("kind") if isinstance(m, dict) else "") or ""
                if tid:
                    n = 4 if "gang" in str(kind) else 3
                    flat.extend([str(tid)] * min(n, 4))
            if flat:
                og = compute_tile_grid(
                    len(flat),
                    w - opp_x - 8,
                    min_tw=14,
                    max_tw=20,
                    gap=2,
                    margin=0,
                    label_w=0,
                )
                for i, tid in enumerate(flat):
                    ox, oy = og.cell(i, origin_x=mx, origin_y=my)
                    self._blit_tile(screen, tid, ox, oy, og.tw)
                y += 18 + og.total_height + 6
            else:
                y += 22

        if self.mode == "play":
            self._draw_buttons(screen, legal, phase, w, h)
        else:
            self.button_rects = {}
            draw_text(
                screen,
                "只读观战 — 由引擎 AI 自动出牌",
                (40, h - 36),
                size=14,
                color=(180, 200, 220),
            )

        if hints and phase == "discard" and self.mode == "play":
            draw_text(
                screen,
                f"提示 shanten={hints.get('shanten')} best={hints.get('best')}",
                (40, max(90, h - btn_zone - 40)),
                size=16,
                color=(255, 220, 120),
            )

    def _estimate_btn_zone(
        self, legal: list[Action], phase: str, w: int, h: int
    ) -> int:
        if self.mode != "play":
            return 48
        keys = self._button_keys(legal, phase)
        per, rows = compute_button_rows(len(keys), w, btn_w=108, gap=10, margin=24)
        rows = max(1, rows)
        # hint line + button rows
        return min(h // 2, 28 + rows * 40 + 12)

    def _button_keys(
        self, legal: list[Action], phase: str
    ) -> list[tuple[str, ActionType | str]]:
        keys: list[tuple[str, ActionType | str]] = []
        if phase == "dingque":
            return [
                ("万 wan", "wan"),
                ("筒 tong", "tong"),
                ("条 tiao", "tiao"),
            ]
        if phase == "exchange":
            return [
                ("确认换牌", "confirm_exchange"),
                ("自动三张", "auto_exchange"),
            ]
        type_set = {a.type for a in legal}
        mapping = [
            ("胡", ActionType.HU),
            ("碰", ActionType.PONG),
            ("明杠", ActionType.GANG_MING),
            ("暗杠", ActionType.GANG_AN),
            ("加杠", ActionType.GANG_JIA),
        ]
        for label, typ in mapping:
            if typ in type_set:
                keys.append((label, typ))
        if ActionType.PASS in type_set and any(
            a.type != ActionType.PASS for a in legal
        ):
            keys.append(("过", ActionType.PASS))
        return keys

    def _draw_melds(
        self,
        screen: pygame.Surface,
        melds: list,
        w: int,
        h: int,
        *,
        hand_top: int,
    ) -> None:
        """Draw own exposed melds (碰=3, 杠=4) above the hand strip; may wrap."""
        labels = {
            "pong": "碰",
            "ming_gang": "明杠",
            "an_gang": "暗杠",
            "jia_gang": "加杠",
        }
        # Flatten groups for sizing; draw group-by-group with wrap
        tw = max(18, min(32, w // 28))
        th = int(tw * 1.4)
        gap = 2
        group_gap = 10
        x = 16
        y = max(100, hand_top - th - 28)
        draw_text(screen, "副露", (x, y - 18), size=14, color=(255, 230, 160))
        line_y = y
        line_x = x
        for m in melds:
            if not isinstance(m, dict):
                continue
            tid = m.get("tile_id")
            kind = str(m.get("kind") or "")
            if not tid:
                continue
            n = 4 if "gang" in kind else 3
            need_w = n * (tw + gap) + group_gap
            if line_x > 16 and line_x + need_w > w - 8:
                line_x = 16
                line_y += th + 18
            label = labels.get(kind, kind or "副露")
            draw_text(
                screen, label, (line_x, line_y - 2), size=11, color=(200, 220, 200)
            )
            for _ in range(n):
                self._blit_tile(screen, str(tid), line_x, line_y + 12, tw)
                line_x += tw + gap
            line_x += group_gap

    def _draw_discards(
        self,
        screen: pygame.Surface,
        discs: list,
        w: int,
        bottom_y: int,
    ) -> None:
        if not discs:
            return
        grid = compute_tile_grid(
            len(discs),
            w,
            min_tw=20,
            max_tw=28,
            gap=2,
            margin=16,
            label_w=36,
            max_rows=8,
        )
        top = bottom_y - grid.total_height
        top = max(90, top)
        draw_text(screen, "弃牌", (16, top - 16), size=12, color=(160, 180, 160))
        for i, tid in enumerate(discs):
            x, y = grid.cell(i, origin_x=52, origin_y=top)
            self._blit_tile(screen, str(tid), x, y, grid.tw)

    def _draw_hand(
        self,
        screen: pygame.Surface,
        hand: list[str],
        h: int,
        *,
        btn_zone: int = 72,
    ):
        """Hand above the button bar; wraps to extra rows when width is tight (F0006)."""
        from players.view.responsive import TileGrid

        self.hand_rects = []
        w = screen.get_width()
        if not hand:
            y = max(110, h - btn_zone - 40)
            draw_text(
                screen,
                "（本家手牌为空或未下发）",
                (16, y),
                size=16,
                color=(255, 180, 120),
            )
            return TileGrid(tw=32, th=44, per_row=1, rows=0, gap=3, n=0)

        max_h = max(60, h - btn_zone - 100)
        from players.view.responsive import DEFAULT_MAX_HAND_TW, DEFAULT_MIN_HAND_TW

        grid = compute_tile_grid(
            len(hand),
            w,
            min_tw=DEFAULT_MIN_HAND_TW,
            max_tw=DEFAULT_MAX_HAND_TW,
            gap=3,
            margin=16,
            label_w=0,
            max_rows=12,
            max_height=max_h,
        )
        bottom_y = h - btn_zone - 8
        for i, tid in enumerate(hand):
            tid_s = str(tid)
            x, y = grid.cell_bottom_up(i, origin_x=16, bottom_y=bottom_y)
            rect = pygame.Rect(x, y, grid.tw, grid.th)
            self._blit_tile(screen, tid_s, x, y, grid.tw)
            if tid_s in self.selected:
                pygame.draw.rect(screen, (255, 220, 80), rect, 3)
            self.hand_rects.append((tid_s, rect))
        return grid

    def _blit_tile(
        self, screen: pygame.Surface, tid: str, x: int, y: int, tw: int
    ) -> None:
        try:
            t = parse_tile(tid)
            surf = self.assets.tile(t.suit.value, t.rank)
            surf = self.assets.scale_to_width(surf, tw)
            screen.blit(surf, (x, y))
        except Exception:
            pygame.draw.rect(screen, (90, 100, 90), (x, y, tw, int(tw * 1.4)))
            pygame.draw.rect(screen, (200, 200, 180), (x, y, tw, int(tw * 1.4)), 1)
            draw_text(screen, tid[-3:], (x + 2, y + 4), size=12, color=(240, 240, 200))

    def _draw_buttons(
        self,
        screen: pygame.Surface,
        legal: list[Action],
        phase: str,
        w: int,
        h: int,
    ) -> None:
        self.button_rects = {}
        keys = self._button_keys(legal, phase)
        per_row, rows = compute_button_rows(len(keys), w, btn_w=108, gap=10, margin=24)
        rows = max(1, rows) if keys else 1
        bar_h = min(h // 2, 28 + rows * 40 + 8)

        # Dedicated button bar at bottom (never under tiles)
        bar = pygame.Rect(0, h - bar_h, w, bar_h)
        pygame.draw.rect(screen, (12, 28, 22), bar)
        pygame.draw.line(screen, (80, 140, 100), (0, h - bar_h), (w, h - bar_h), 2)

        if phase == "exchange":
            draw_text(
                screen,
                f"换三张: 已选 {len(self.selected)}/3 同花色 → 点「确认换牌」或「自动三张」",
                (12, h - bar_h + 4),
                size=14,
                color=(255, 240, 160),
            )
        elif phase == "discard" and any(a.type == ActionType.DISCARD for a in legal):
            draw_text(
                screen,
                "出牌: 双击手牌直接打出（无需确认按钮）",
                (12, h - bar_h + 4),
                size=14,
                color=(255, 240, 160),
            )
        elif phase == "response":
            draw_text(
                screen,
                "可碰/杠/胡时点按钮；仅能过时将自动过",
                (12, h - bar_h + 4),
                size=14,
                color=(255, 240, 160),
            )

        btn_w, btn_h, gap = 108, 32, 10
        for i, (label, key) in enumerate(keys):
            row = i // per_row
            col = i % per_row
            x = 12 + col * (btn_w + gap)
            y = h - bar_h + 26 + row * (btn_h + 8)
            rect = pygame.Rect(x, y, btn_w, btn_h)
            ready = (
                (key == "confirm_exchange" and len(self.selected) == 3)
                or key == "auto_exchange"
                or key in ("wan", "tong", "tiao")
                or isinstance(key, ActionType)
                or key in (
                    ActionType.HU.value,
                    ActionType.PONG.value,
                    ActionType.PASS.value,
                    ActionType.GANG_MING.value,
                    ActionType.GANG_AN.value,
                    ActionType.GANG_JIA.value,
                )
            )
            color = (40, 120, 70) if ready else (50, 70, 60)
            border = (180, 255, 180) if ready else (120, 140, 120)
            pygame.draw.rect(screen, color, rect, border_radius=4)
            pygame.draw.rect(screen, border, rect, 2, border_radius=4)
            draw_text(screen, str(label), (x + 8, y + 6), size=15, color=(255, 255, 240))
            self.button_rects[str(key if not isinstance(key, ActionType) else key.value)] = (
                rect
            )
            if isinstance(key, ActionType):
                self.button_rects[str(key)] = rect

    def build_exchange_action(self, legal: list[Action]) -> Action | None:
        """Build EXCHANGE from selection, or fall back to first legal triple."""
        if len(self.selected) == 3:
            try:
                tiles = tuple(parse_tile(t) for t in self.selected)
                # same suit check
                if len({t.suit for t in tiles}) == 1:
                    return Action(ActionType.EXCHANGE, tiles=tiles)
            except Exception:
                pass
        for a in legal:
            if a.type == ActionType.EXCHANGE and len(a.tiles) == 3:
                return a
        return None

    def handle_click(
        self, pos: tuple[int, int], legal: list[Action], phase: str
    ) -> Action | None | str:
        """
        Returns Action, None (selection changed / no-op), or str status message.
        """
        if self.mode != "play":
            return None

        # Buttons first (bottom bar is dedicated)
        for key, rect in self.button_rects.items():
            if not rect.collidepoint(pos):
                continue
            if phase == "dingque" and key in ("wan", "tong", "tiao"):
                from engine.tile import Suit

                return Action(ActionType.DINGQUE, suit=Suit(key))
            if key in ("confirm_exchange", "auto_exchange"):
                act = self.build_exchange_action(legal)
                if act is not None:
                    return act
                if key == "auto_exchange":
                    return "自动换牌失败：引擎未提供合法三张"
                return f"请先点选 3 张【同一花色】的牌（已选 {len(self.selected)}/3）"
            for a in legal:
                if str(a.type) == key or a.type.value == key:
                    return a
                try:
                    if a.type == ActionType(key):
                        return a
                except Exception:
                    continue

        # Hand tiles: single-click select only (discard via double-click in seat_window)
        for tid, rect in self.hand_rects:
            if rect.collidepoint(pos):
                if phase == "exchange":
                    if tid in self.selected:
                        self.selected.remove(tid)
                    elif len(self.selected) < 3:
                        if self.selected:
                            try:
                                s0 = parse_tile(self.selected[0]).suit
                                if parse_tile(tid).suit != s0:
                                    return "换三张必须同一花色（万/筒/条）"
                            except Exception:
                                pass
                        self.selected.append(tid)
                    else:
                        return "已选满 3 张，可点「确认换牌」或取消重选"
                    return None
                # discard / other: select highlight
                self.selected = [tid]
                return None
        return None

    def discard_action_for_tile(
        self, tid: str, legal: list[Action]
    ) -> Action | None:
        """Build a DISCARD action for tile id if legal (or construct if list has discards)."""
        for a in legal:
            if a.type == ActionType.DISCARD and a.tiles and a.tiles[0].id == tid:
                return a
        if any(a.type == ActionType.DISCARD for a in legal):
            try:
                return Action(ActionType.DISCARD, tiles=(parse_tile(tid),))
            except Exception:
                return None
        return None

    def tile_at(self, pos: tuple[int, int]) -> str | None:
        for tid, rect in self.hand_rects:
            if rect.collidepoint(pos):
                return tid
        return None

    def draw_ready_overlay(
        self,
        screen: pygame.Surface,
        *,
        round_index: int = 1,
        auto_start: bool = False,
        role_label: str = "",
    ) -> None:
        """Modal confirm layer: 确认开始 + 自动开始 checkbox (play & watch)."""
        w, h = screen.get_size()
        # Dim entire window
        dim = pygame.Surface((w, h), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 150))
        screen.blit(dim, (0, 0))

        box_w = min(420, w - 40)
        box_h = 200
        box = pygame.Rect(0, 0, box_w, box_h)
        box.center = (w // 2, h // 2)
        pygame.draw.rect(screen, (18, 42, 32), box, border_radius=12)
        pygame.draw.rect(screen, (120, 200, 150), box, 2, border_radius=12)

        title = f"第 {round_index} 局 — 确认开始"
        draw_text(
            screen,
            title,
            (box.x + 24, box.y + 20),
            size=22,
            color=(255, 250, 220),
        )
        sub = role_label or (
            "人类座位" if self.mode == "play" else "AI 观战座位"
        )
        draw_text(
            screen,
            f"S{self.seat}  {sub}",
            (box.x + 24, box.y + 52),
            size=16,
            color=(200, 230, 200),
        )
        draw_text(
            screen,
            "所有座位确认后才会发牌开局",
            (box.x + 24, box.y + 76),
            size=14,
            color=(180, 200, 180),
        )

        # Auto-start checkbox
        cb = pygame.Rect(box.x + 28, box.y + 110, 22, 22)
        self.ready_auto_rect = cb
        pygame.draw.rect(screen, (40, 70, 55), cb, border_radius=3)
        pygame.draw.rect(screen, (180, 220, 180), cb, 2, border_radius=3)
        if auto_start:
            pygame.draw.rect(
                screen,
                (80, 200, 120),
                cb.inflate(-6, -6),
                border_radius=2,
            )
        draw_text(
            screen,
            "自动开始（本窗下次自动确认）",
            (cb.right + 10, cb.y + 2),
            size=15,
            color=(240, 245, 230),
        )

        # Confirm button
        btn = pygame.Rect(0, 0, 180, 40)
        btn.centerx = box.centerx
        btn.bottom = box.bottom - 18
        self.ready_start_rect = btn
        pygame.draw.rect(screen, (40, 130, 80), btn, border_radius=6)
        pygame.draw.rect(screen, (180, 255, 180), btn, 2, border_radius=6)
        draw_text(
            screen,
            "确认开始",
            (btn.centerx - 40, btn.centery - 10),
            size=18,
            color=(255, 255, 240),
        )

    def hit_ready_start(self, pos: tuple[int, int]) -> bool:
        return self.ready_start_rect.collidepoint(pos)

    def hit_ready_auto(self, pos: tuple[int, int]) -> bool:
        return self.ready_auto_rect.collidepoint(pos)
