"""Result / settlement — chrome aligned with human seat window UI (F0008)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame

from display.hud_common import blit_score, draw_text
from display.ui_chrome import (
    BG_DEEP,
    BORDER_GOLD,
    BORDER_GREEN,
    TEXT_DIM,
    TEXT_GOLD,
    TEXT_MUTED,
    TEXT_NEG,
    TEXT_POS,
    TEXT_TITLE,
    TEXT_VALUE,
    draw_footer_zone,
    draw_header_bar,
    draw_panel,
    draw_primary_button,
    draw_secondary_button,
    metrics,
)
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
    seats = (
        list(rankings)
        if rankings
        else sorted(totals.keys(), key=lambda s: (-totals.get(s, 0), s))
    )
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
        m = metrics(w, h)
        cx = w // 2

        screen.fill(BG_DEEP)
        try:
            if self._bg is None or self._bg.get_size() != (w, h):
                raw = self.assets.bg("result")
                self._bg = pygame.transform.smoothscale(raw, (w, h))
            dim = pygame.Surface((w, h), pygame.SRCALPHA)
            dim.fill((8, 22, 16, 170))
            screen.blit(self._bg, (0, 0))
            screen.blit(dim, (0, 0))
        except Exception:
            pass

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

        # ---- HEADER ----
        sub_bits = []
        if num_rounds > 1 or round_index > 0:
            sub_bits.append(f"第 {round_index}/{num_rounds} 局")
        if auto_next_countdown is not None and round_index < num_rounds:
            sub_bits.append(f"⏱ 自动下一局 {auto_next_countdown:.1f}s（R 立即）")
        body_top = draw_header_bar(
            screen,
            m,
            title="本局结算 · 积分明细",
            subtitle="  ·  ".join(sub_bits) if sub_bits else "血战到底",
        )

        # ---- FOOTER (fixed; cards stay above) ----
        footer = draw_footer_zone(screen, m)
        again_hint = (
            "R / Enter = 再来一局"
            if round_index < num_rounds
            else "已达设定轮数 · L 回大厅"
        )
        draw_text(
            screen,
            f"L = 回大厅（座位窗保留）   {again_hint}",
            (m.margin, footer.y + 6),
            size=m.font_small,
            color=TEXT_GOLD,
        )
        btn_w = min(200, max(120, (w - 3 * m.gap - 2 * m.margin) // 2))
        btn_h = min(m.btn_h, footer.h - m.font_small - 20)
        self.lobby_rect = pygame.Rect(0, 0, btn_w, btn_h)
        self.again_rect = pygame.Rect(0, 0, btn_w, btn_h)
        self.lobby_rect.center = (cx - btn_w // 2 - m.gap, footer.centery + 8)
        self.again_rect.center = (cx + btn_w // 2 + m.gap, footer.centery + 8)
        # clamp inside footer
        for r in (self.lobby_rect, self.again_rect):
            if r.bottom > footer.bottom - 4:
                r.bottom = footer.bottom - 4
            if r.top < footer.top + m.font_small + 10:
                r.top = footer.top + m.font_small + 10
        draw_secondary_button(
            screen, self.lobby_rect, "回大厅", font_size=m.font_body, radius=m.radius
        )
        draw_primary_button(
            screen, self.again_rect, "再来一局", font_size=m.font_body, radius=m.radius
        )

        # ---- SUMMARY strip (seat play_panel style) ----
        rankings = list(
            result.rankings
            or sorted(totals.keys(), key=lambda s: (-totals.get(s, 0), s))
        )
        board = format_cumulative_board(totals, rankings=rankings)
        reason = result.finished_reason or "unknown"
        reason_zh = _REASON_ZH.get(reason, reason)
        tags = result.settle_tags or {}
        tag_txt = (
            f"花猪:{_seats_csv(tags.get('hua_zhu'))}  "
            f"有叫:{_seats_csv(tags.get('ting'))}  "
            f"未叫:{_seats_csv(tags.get('not_ting'))}"
        )
        sum_lines = [
            board,
            f"结束: {reason_zh}  ·  牌墙剩余 {result.wall_remaining}",
            tag_txt,
        ]
        if result.hu_sequence:
            hu_parts = [_hu_line(hu) for hu in result.hu_sequence[:6]]
            sum_lines.append("胡序: " + " | ".join(hu_parts))

        line_h = m.font_body + 4
        sum_h = len(sum_lines) * line_h + m.gap * 2
        sum_rect = pygame.Rect(
            m.margin,
            body_top,
            w - 2 * m.margin,
            min(sum_h, max(48, (footer.top - body_top) // 4)),
        )
        draw_panel(
            screen,
            sum_rect,
            border=BORDER_GOLD,
            radius=m.radius,
            alpha=230,
        )
        sy = sum_rect.y + m.gap
        for i, line in enumerate(sum_lines):
            if sy + line_h > sum_rect.bottom - 4:
                break
            # truncate by width budget
            budget = max(12, (sum_rect.w - 20) // max(6, m.font_small // 2))
            text = line if len(line) <= budget else line[: budget - 1] + "…"
            draw_text(
                screen,
                text,
                (sum_rect.x + 10, sy),
                size=m.font_body if i == 0 else m.font_small,
                color=TEXT_GOLD if i == 0 else TEXT_MUTED,
            )
            sy += line_h

        # ---- SEAT CARDS (2×2 / 1 col) — fully inside remaining band ----
        area_top = sum_rect.bottom + m.gap
        area_bottom = footer.top - m.gap
        area_h = max(60, area_bottom - area_top)
        n = max(1, len(rankings))
        cols = 2 if w >= 720 and n >= 3 else 1
        rows = (n + cols - 1) // cols
        gap = m.gap
        usable_w = w - 2 * m.margin
        card_w = max(120, (usable_w - gap * (cols - 1)) // cols)
        card_h = max(64, (area_h - gap * (rows - 1)) // rows) if rows else area_h

        ledger = build_score_ledger(getattr(result, "score_events", None) or [])
        for idx, seat in enumerate(rankings):
            col = idx % cols
            row = idx // cols
            x0 = m.margin + col * (card_w + gap)
            y0 = area_top + row * (card_h + gap)
            # hard clip to area
            if y0 >= area_bottom:
                break
            ch = min(card_h, area_bottom - y0)
            if ch < 40:
                break
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
                rect=pygame.Rect(x0, y0, card_w, ch),
                font_body=m.font_body,
                font_small=m.font_small,
                radius=m.radius,
            )

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
        font_body: int = 16,
        font_small: int = 13,
        radius: int = 8,
    ) -> None:
        draw_panel(
            screen,
            rect,
            border=BORDER_GREEN if rank > 1 else BORDER_GOLD,
            radius=radius,
            alpha=220,
        )
        pad = max(6, rect.h // 20)
        x = rect.x + pad
        y = rect.y + pad
        draw_text(
            screen,
            f"#{rank}  座位 S{seat}",
            (x, y),
            size=font_body,
            color=TEXT_TITLE,
        )
        try:
            blit_score(
                screen,
                self.assets,
                score,
                (x + min(180, rect.w // 2), y),
                size="md" if rect.w > 280 else "sm",
            )
        except Exception:
            pass
        y += font_body + 6
        draw_text(
            screen,
            f"累计 {score:+d}" if score != 0 else "累计 0",
            (x, y),
            size=font_small + 1,
            color=TEXT_GOLD if score >= 0 else TEXT_NEG,
        )
        y += font_small + 6
        if show_hand_delta:
            draw_text(
                screen,
                f"本局 {hand_delta:+d}" if hand_delta != 0 else "本局 0",
                (x, y),
                size=font_small,
                color=TEXT_POS if hand_delta >= 0 else TEXT_NEG,
            )
            y += font_small + 4

        if y >= rect.bottom - font_small:
            return
        if not lines:
            draw_text(
                screen,
                "（本局无分变）",
                (x, y),
                size=font_small,
                color=TEXT_DIM,
            )
            return

        line_h = font_small + 4
        max_slots = max(1, (rect.bottom - y - pad) // line_h)
        if len(lines) > max_slots:
            show = lines[: max(0, max_slots - 1)]
            rest = len(lines) - len(show)
        else:
            show = lines
            rest = 0
        budget = max(12, (rect.w - 2 * pad) // max(6, font_small // 2))
        for line in show:
            if y + line_h > rect.bottom - 2:
                break
            delta = int(line.get("delta") or 0)
            color = TEXT_POS if delta >= 0 else TEXT_NEG
            text = str(line.get("text") or "")
            if len(text) > budget:
                text = text[: budget - 1] + "…"
            draw_text(screen, text, (x, y), size=font_small, color=color)
            y += line_h
        if rest > 0 and y + line_h <= rect.bottom:
            draw_text(
                screen,
                f"… 另有 {rest} 笔明细",
                (x, y),
                size=max(11, font_small - 1),
                color=TEXT_DIM,
            )

    def hit_lobby(self, pos: tuple[int, int]) -> bool:
        return self.lobby_rect.collidepoint(pos)

    def hit_again(self, pos: tuple[int, int]) -> bool:
        return self.again_rect.collidepoint(pos)
