"""Result / settlement scene with full per-seat score breakdown (F0008)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame

from display.hud_common import blit_score, draw_text
from engine.blood_battle import GameResult
from engine.score import build_score_ledger

if TYPE_CHECKING:
    from display.asset_manager import AssetManager

_REASON_ZH = {
    "last_one": "血战末家",
    "wall_empty": "流局·墙尽",
    "max_steps": "步数上限",
    "error": "异常结束",
    "unknown": "未知",
}


def _seats_csv(raw: Any) -> str:
    if not raw:
        return "—"
    if isinstance(raw, (list, tuple)):
        return ",".join(f"S{int(x)}" for x in raw)
    return str(raw)


def _hu_line(hu: dict) -> str:
    seat = hu.get("seat")
    fan = hu.get("fan")
    if hu.get("zimo"):
        kind = "自摸"
        extra = ""
    else:
        kind = "点炮胡"
        loser = hu.get("loser")
        extra = f" ←S{loser}" if loser is not None else ""
    fan_s = f" {fan}番" if fan is not None else ""
    return f"S{seat} {kind}{fan_s}{extra}"


def format_cumulative_board(
    totals: dict[int, int] | None,
    *,
    rankings: list[int] | None = None,
) -> str:
    """One-line session totals, e.g. '累计得分  #1 S0:+12  #2 S2:+3 …'."""
    if not totals:
        return "累计得分: —"
    seats = list(rankings) if rankings else sorted(totals.keys(), key=lambda s: (-totals.get(s, 0), s))
    parts: list[str] = []
    for i, seat in enumerate(seats, start=1):
        sc = int(totals.get(int(seat), 0))
        sign = f"{sc:+d}" if sc != 0 else "0"
        parts.append(f"#{i} S{seat}:{sign}")
    return "累计得分  " + "   ".join(parts)


class ResultView:
    def __init__(self, assets: AssetManager) -> None:
        self.assets = assets
        self._bg: pygame.Surface | None = None
        self.lobby_rect = pygame.Rect(0, 0, 200, 56)
        self.again_rect = pygame.Rect(0, 0, 200, 56)

    def draw(
        self,
        screen: pygame.Surface,
        result: GameResult,
        *,
        round_index: int = 0,
        num_rounds: int = 1,
        auto_next_countdown: float | None = None,
        session_scores: dict[int, int] | None = None,
        hand_start_scores: dict[int, int] | None = None,
    ) -> None:
        w, h = screen.get_size()
        cx = w // 2
        if self._bg is None or self._bg.get_size() != (w, h):
            raw = self.assets.bg("result")
            self._bg = pygame.transform.smoothscale(raw, (w, h))
        screen.blit(self._bg, (0, 0))

        # totals: prefer explicit session map, else result.scores (already cumulative if multi-round)
        totals: dict[int, int] = {}
        src = session_scores if session_scores is not None else result.scores
        for k, v in (src or {}).items():
            try:
                totals[int(k)] = int(v)
            except (TypeError, ValueError):
                continue
        starts: dict[int, int] = {}
        for k, v in (hand_start_scores or {}).items():
            try:
                starts[int(k)] = int(v)
            except (TypeError, ValueError):
                continue

        # ---- header ----
        draw_text(screen, "本局结算 · 积分明细", (max(24, w // 2 - 120), max(16, h // 40)), size=28)
        y = max(52, h // 18)
        if num_rounds > 1 or round_index > 0:
            draw_text(
                screen,
                f"第 {round_index}/{num_rounds} 局",
                (max(24, cx - 50), y),
                size=18,
                color=(255, 230, 140),
            )
            y += 26
        if auto_next_countdown is not None and round_index < num_rounds:
            draw_text(
                screen,
                f"⏱ 自动下一局 {auto_next_countdown:.1f}s（R 立即开始）",
                (max(24, cx - 160), y),
                size=20,
                color=(120, 255, 180),
            )
            y += 28

        # ---- cumulative scoreboard (all seats) ----
        rankings = list(result.rankings or sorted(totals.keys(), key=lambda s: (-totals.get(s, 0), s)))
        board = format_cumulative_board(totals, rankings=rankings)
        # banner strip
        bar = pygame.Surface((max(40, w - 40), 36), pygame.SRCALPHA)
        bar.fill((20, 40, 28, 210))
        screen.blit(bar, (20, y - 4))
        pygame.draw.rect(screen, (100, 180, 120), pygame.Rect(20, y - 4, max(40, w - 40), 36), 2, border_radius=4)
        draw_text(screen, board, (28, y + 4), size=18, color=(255, 245, 180))
        y += 42

        reason = result.finished_reason or "unknown"
        reason_zh = _REASON_ZH.get(reason, reason)
        draw_text(
            screen,
            f"结束原因: {reason_zh} ({reason})   牌墙剩余: {result.wall_remaining}",
            (max(20, w // 20), y),
            size=16,
        )
        y += 24

        tags = result.settle_tags or {}
        tag_txt = (
            f"花猪: {_seats_csv(tags.get('hua_zhu'))}   "
            f"有叫: {_seats_csv(tags.get('ting'))}   "
            f"未叫: {_seats_csv(tags.get('not_ting'))}"
        )
        draw_text(screen, tag_txt, (max(20, w // 20), y), size=15, color=(200, 220, 200))
        y += 24

        if result.hu_sequence:
            hu_parts = [_hu_line(hu) for hu in result.hu_sequence[:8]]
            draw_text(
                screen,
                "胡序: " + "  |  ".join(hu_parts),
                (max(20, w // 20), y),
                size=15,
                color=(255, 220, 150),
            )
            y += 26

        # ---- ledger cards ----
        ledger = build_score_ledger(getattr(result, "score_events", None) or [])
        n = max(1, len(rankings))
        # 2 columns when wide enough and ≥3 seats
        cols = 2 if w >= 900 and n >= 3 else 1
        margin = max(16, w // 40)
        gap = 12
        usable_w = w - 2 * margin
        card_w = (usable_w - gap * (cols - 1)) // cols
        # leave room for footer buttons
        footer_h = max(120, h // 7)
        area_top = y + 8
        area_bottom = h - footer_h
        area_h = max(80, area_bottom - area_top)
        rows = (n + cols - 1) // cols
        card_h = max(72, (area_h - gap * (rows - 1)) // rows) if rows else area_h

        for idx, seat in enumerate(rankings):
            col = idx % cols
            row = idx // cols
            x0 = margin + col * (card_w + gap)
            y0 = area_top + row * (card_h + gap)
            seat_i = int(seat)
            total = int(totals.get(seat_i, result.scores.get(seat_i, 0)))
            start = int(starts.get(seat_i, 0))
            hand_delta = total - start
            self._draw_seat_card(
                screen,
                rank=idx + 1,
                seat=seat_i,
                score=total,
                hand_delta=hand_delta,
                show_hand_delta=bool(starts) or num_rounds > 1 or round_index > 1,
                lines=ledger.get(seat_i, []),
                rect=pygame.Rect(x0, y0, card_w, card_h),
            )

        # ---- footer ----
        again_hint = (
            "R / Enter = 再来一局"
            if round_index < num_rounds
            else "已达设定轮数 · L 回大厅"
        )
        draw_text(
            screen,
            f"L = 回大厅（座位窗保留）   {again_hint}",
            (max(20, cx - 220), h - max(120, h // 7)),
            size=15,
            color=(255, 240, 180),
        )
        try:
            btn = self.assets.button("cancel")
            btn = self.assets.scale_to_width(btn, 180)
            self.lobby_rect = btn.get_rect(center=(cx - 120, h - max(56, h // 14)))
            screen.blit(btn, self.lobby_rect)
            btn2 = self.assets.button("confirm")
            btn2 = self.assets.scale_to_width(btn2, 180)
            self.again_rect = btn2.get_rect(center=(cx + 120, h - max(56, h // 14)))
            screen.blit(btn2, self.again_rect)
        except FileNotFoundError:
            pass

    def _draw_seat_card(
        self,
        screen: pygame.Surface,
        *,
        rank: int,
        seat: int,
        score: int,
        lines: list[dict[str, Any]],
        rect: pygame.Rect,
        hand_delta: int = 0,
        show_hand_delta: bool = False,
    ) -> None:
        # translucent panel
        panel = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        panel.fill((12, 28, 22, 200))
        pygame.draw.rect(panel, (80, 140, 100, 220), panel.get_rect(), width=2, border_radius=6)
        screen.blit(panel, rect.topleft)

        pad = 10
        x = rect.x + pad
        y = rect.y + 6
        draw_text(
            screen,
            f"#{rank}  座位 S{seat}",
            (x, y),
            size=20,
            color=(255, 250, 220),
        )
        # cumulative score digits to the right of title when room
        blit_score(
            screen,
            self.assets,
            score,
            (x + min(200, rect.w // 2), y),
            size="md" if rect.w > 280 else "sm",
        )
        y += 28
        draw_text(
            screen,
            f"累计 {score:+d}" if score != 0 else "累计 0",
            (x, y),
            size=16,
            color=(255, 220, 120) if score >= 0 else (255, 140, 140),
        )
        y += 20
        if show_hand_delta:
            draw_text(
                screen,
                f"本局 {hand_delta:+d}" if hand_delta != 0 else "本局 0",
                (x, y),
                size=14,
                color=(180, 230, 180) if hand_delta >= 0 else (255, 170, 160),
            )
            y += 20

        if not lines:
            draw_text(
                screen,
                "（本局无分变）",
                (x, y),
                size=14,
                color=(160, 170, 160),
            )
            return

        # Fit as many detail lines as possible
        line_h = 18
        max_slots = max(1, (rect.bottom - y - 8) // line_h)
        if len(lines) > max_slots:
            show = lines[: max(0, max_slots - 1)]
            rest = len(lines) - len(show)
        else:
            show = lines
            rest = 0
        budget = max(18, (rect.w - 2 * pad) // 9)
        for line in show:
            delta = int(line.get("delta") or 0)
            color = (160, 230, 160) if delta >= 0 else (255, 160, 150)
            text = str(line.get("text") or "")
            if len(text) > budget:
                text = text[: budget - 1] + "…"
            draw_text(screen, text, (x, y), size=14, color=color)
            y += line_h
        if rest > 0:
            draw_text(
                screen,
                f"… 另有 {rest} 笔明细",
                (x, y),
                size=13,
                color=(180, 190, 180),
            )

    def hit_lobby(self, pos: tuple[int, int]) -> bool:
        return self.lobby_rect.collidepoint(pos)

    def hit_again(self, pos: tuple[int, int]) -> bool:
        return self.again_rect.collidepoint(pos)
