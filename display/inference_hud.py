"""Inference HUD overlays (danger markers, tenpai lights)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from display.hud_common import draw_text
from display.layout import seat_to_slot

if TYPE_CHECKING:
    from display.asset_manager import AssetManager
    from display.layout import Layout
    from engine.state import GameState
    from players.analysis.types import AnalysisSnapshot


def draw_inference_hud(
    screen: pygame.Surface,
    assets: AssetManager,
    layout: Layout,
    state: GameState,
    analysis: AnalysisSnapshot,
    focus_seat: int,
    *,
    hand_positions: list[tuple[str, int, int, int]] | None = None,
    panel_w: int = 0,
    marks_only: bool = False,
) -> None:
    """
    hand_positions: optional list of (tile_id, x, y, tile_w) for focus hand.
    panel_w: main control panel width (F0007) — keep text left of it.
    marks_only: only danger markers on hand (skip panels).
    """
    n = state.num_players
    if marks_only:
        if hand_positions:
            for tid, x, y, tw in hand_positions:
                level = analysis.danger.get(tid, "unknown")
                try:
                    mark = assets.danger(level)
                    mark = assets.scale_to_width(mark, 14)
                    screen.blit(mark, (x + tw - 16, y - 2))
                except FileNotFoundError:
                    pass
        return

    # opponent tenpai lights near avatars
    for op in analysis.opponents:
        slot = seat_to_slot(op.seat, focus_seat, n)
        ax, ay = layout.avatar_pos(slot)
        try:
            key = "tenpai_active" if op.tenpai_level == "active" else "tenpai_unknown"
            lamp = assets.inference(key)
            lamp = assets.scale_to_width(lamp, 22)
            screen.blit(lamp, (ax + 50, ay + 30))
        except FileNotFoundError:
            color = (255, 200, 50) if op.tenpai_level == "active" else (120, 120, 120)
            pygame.draw.circle(screen, color, (ax + 60, ay + 40), 6)
        draw_text(
            screen,
            f"{int(op.tenpai_prob * 100)}%",
            (ax, ay + 58),
            size=12,
            color=(220, 220, 180),
        )

    # Compact info strip just left of control panel (not over hands)
    right = screen.get_width() - max(0, int(panel_w)) - 12
    left = max(12, right - 190)
    top = max(70, layout.top_band()[1] + layout.top_band()[3] + 4)
    try:
        panel = assets.inference("infer_panel")
        panel = assets.scale_to_width(panel, 180)
        screen.blit(panel, (left, top))
        draw_text(screen, f"Focus S{focus_seat}", (left + 12, top + 10), size=13)
        draw_text(
            screen,
            f"shanten {analysis.shanten}",
            (left + 12, top + 32),
            size=13,
        )
        y = top + 54
        for op in analysis.opponents[:3]:
            draw_text(
                screen,
                f"S{op.seat} tenpai~{op.tenpai_prob:.2f}",
                (left + 12, y),
                size=11,
            )
            y += 16
    except FileNotFoundError:
        draw_text(
            screen,
            f"推理 S{focus_seat}  shanten={analysis.shanten}",
            (left, top),
            size=13,
            color=(200, 220, 255),
        )

    # danger markers on hand tiles
    if hand_positions:
        for tid, x, y, tw in hand_positions:
            level = analysis.danger.get(tid, "unknown")
            try:
                mark = assets.danger(level)
                mark = assets.scale_to_width(mark, 14)
                screen.blit(mark, (x + tw - 16, y - 2))
            except FileNotFoundError:
                pass
