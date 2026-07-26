"""Strategy HUD: panel + discard marks."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from display.hud_common import blit_score, draw_text

if TYPE_CHECKING:
    from display.asset_manager import AssetManager
    from players.analysis.types import AnalysisSnapshot


def draw_strategy_hud(
    screen: pygame.Surface,
    assets: AssetManager,
    analysis: AnalysisSnapshot,
    *,
    hand_positions: list[tuple[str, int, int, int]] | None = None,
    panel_pos: tuple[int, int] | None = None,
    panel_w: int = 0,
    bottom_hand_y: int | None = None,
    marks_only: bool = False,
) -> None:
    """
    Strategy / 向听 panel.

    Place **above** the bottom hand band (never cover bottom-seat tiles).
    ``bottom_hand_y`` = top Y of bottom hand band when known.
    ``marks_only``: only draw hand marks (panel already drawn).
    """
    if not marks_only:
        panel_h = 92
        panel_w_draw = 340
        if panel_pos is None:
            pw = max(0, int(panel_w))
            content_w = max(200, screen.get_width() - pw)
            px = max(12, content_w // 2 - panel_w_draw // 2)
            # Sit in the center zone, just above bottom hand
            if bottom_hand_y is not None:
                py = int(bottom_hand_y) - panel_h - 10
            else:
                py = max(80, screen.get_height() // 2 + 40)
            py = max(70, min(py, screen.get_height() - panel_h - 40))
            # Keep clear of bottom ~20% (hand band reserve)
            max_py = int(screen.get_height() * 0.72) - panel_h
            py = min(py, max(70, max_py))
        else:
            px, py = panel_pos
        try:
            panel = assets.strategy_asset("strategy_panel")
            panel = assets.scale_to_width(panel, panel_w_draw)
            screen.blit(panel, (px, py))
        except FileNotFoundError:
            pygame.draw.rect(screen, (20, 40, 50), (px, py, panel_w_draw, panel_h))

        draw_text(
            screen, f"向听/Shanten: {analysis.shanten}", (px + 16, py + 12), size=16
        )
        draw_text(
            screen,
            f"Ukeire tiles: {analysis.ukeire_count}",
            (px + 16, py + 36),
            size=14,
            color=(200, 220, 200),
        )
        if analysis.discard_ranks:
            best = analysis.discard_ranks[0]
            draw_text(
                screen,
                f"Best: {best.tile_id}  dmg={best.danger}",
                (px + 16, py + 58),
                size=14,
                color=(255, 220, 120),
            )
            deal_map = {
                "safe": 5,
                "low": 15,
                "unknown": 25,
                "medium": 40,
                "high": 65,
                "critical": 90,
            }
            pct = deal_map.get(best.danger, 30)
            try:
                bar = assets.strategy_asset("deal_in_bar")
                bar = assets.scale_to_width(bar, 200)
                screen.blit(bar, (px + 150, py + 12))
                draw_text(screen, f"{pct}%", (px + 300, py + 14), size=14)
            except FileNotFoundError:
                draw_text(screen, f"risk {pct}%", (px + 200, py + 12), size=14)

    # marks on hand
    if not hand_positions or not analysis.discard_ranks:
        return
    mark_by_tile = {a.tile_id: a.mark for a in analysis.discard_ranks}
    for tid, x, y, tw in hand_positions:
        mark = mark_by_tile.get(tid, "none")
        if mark == "none":
            continue
        key = {
            "best": "mark_best",
            "second": "mark_second",
            "avoid": "mark_avoid",
        }.get(mark)
        if not key:
            continue
        try:
            m = assets.strategy_asset(key)
            m = assets.scale_to_width(m, 16)
            screen.blit(m, (x - 2, y - 4))
        except FileNotFoundError:
            pass
