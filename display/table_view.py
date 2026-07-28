"""Table spectator rendering — F0015 interior + F0007 tiles (F0018)."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Literal

import pygame

from display.control_panel import ControlPanel, TableUIOptions
from display.hud_common import blit_score, draw_text
from display.inference_hud import draw_inference_hud
from display.layout import MIN_TABLE_TW, Layout, seat_to_slot
from display.play_log_panel import draw_play_log_panel
from display.side_scoreboard import draw_side_scoreboard
from display.strategy_hud import draw_strategy_hud
from engine.state import GameState
from engine.tile import parse_tile

if TYPE_CHECKING:
    from display.asset_manager import AssetManager
    from display.hud_common import FxOverlay
    from display.play_event_log import PlayEventLog
    from players.analysis.types import AnalysisSnapshot

SpectatorMode = Literal["full", "public"]


def _pack_fixed(
    n: int,
    area_w: int,
    area_h: int,
    cell_w: int,
    cell_h: int,
    *,
    gap: int = 3,
    horizontal: bool = True,
) -> tuple[int, int, int, int]:
    """
    Return (per_line, lines, cell_w, cell_h).

    Shrinks cell (keeping aspect) until the grid fits inside area_w×area_h,
    so tiles stay within the designed strip rectangle.
    """
    n = max(0, int(n))
    gap = max(0, int(gap))
    area_w = max(8, int(area_w))
    area_h = max(8, int(area_h))
    cell_w = max(8, int(cell_w))
    cell_h = max(8, int(cell_h))
    if n == 0:
        return 1, 0, cell_w, cell_h

    aspect = cell_h / max(1, cell_w)
    floor_w = 10

    def _try(cw: int, ch: int) -> tuple[int, int]:
        if horizontal:
            per = max(1, (area_w + gap) // (cw + gap))
            lines = max(1, math.ceil(n / per))
            need_h = lines * ch + max(0, lines - 1) * gap
            need_w = min(n, per) * cw + max(0, min(n, per) - 1) * gap
            ok = need_h <= area_h and need_w <= area_w
            return per, lines if ok or cw <= floor_w else (per, lines)
        per = max(1, (area_h + gap) // (ch + gap))
        lines = max(1, math.ceil(n / per))
        need_w = lines * cw + max(0, lines - 1) * gap
        need_h = min(n, per) * ch + max(0, min(n, per) - 1) * gap
        return per, lines

    cw, ch = cell_w, cell_h
    for _ in range(48):
        if horizontal:
            per = max(1, (area_w + gap) // (cw + gap))
            lines = max(1, math.ceil(n / per))
            need_h = lines * ch + max(0, lines - 1) * gap
            need_w = min(n, per) * cw + max(0, min(n, per) - 1) * gap
            if need_h <= area_h and need_w <= area_w:
                return per, lines, cw, ch
        else:
            per = max(1, (area_h + gap) // (ch + gap))
            lines = max(1, math.ceil(n / per))
            need_w = lines * cw + max(0, lines - 1) * gap
            need_h = min(n, per) * ch + max(0, min(n, per) - 1) * gap
            if need_w <= area_w and need_h <= area_h:
                return per, lines, cw, ch
        if cw <= floor_w:
            break
        cw = max(floor_w, cw - 1)
        ch = max(floor_w, int(round(cw * aspect)))
    # last resort: use shrunk cell even if slightly tight
    if horizontal:
        per = max(1, (area_w + gap) // (cw + gap))
        lines = max(1, math.ceil(n / per))
    else:
        per = max(1, (area_h + gap) // (ch + gap))
        lines = max(1, math.ceil(n / per))
    return per, lines, cw, ch


def _center_origin(
    area_x: int,
    area_y: int,
    area_w: int,
    area_h: int,
    *,
    n: int,
    per: int,
    lines: int,
    cell_w: int,
    cell_h: int,
    gap: int,
    horizontal: bool,
) -> tuple[int, int]:
    """Top-left of a centered tile grid inside the area rect.

    For a single horizontal row (top/bottom hands), center on **actual tile count**
    ``n``, not full capacity ``per`` — otherwise short hands look left-shifted.
    """
    if n <= 0 or per <= 0 or lines <= 0:
        return area_x, area_y
    if horizontal:
        # Single row: use real n; multi-row block: use max row width (per)
        if lines <= 1:
            cols = max(1, min(int(n), int(per)))
        else:
            cols = max(1, int(per))
        content_w = cols * cell_w + max(0, cols - 1) * gap
        content_h = lines * cell_h + max(0, lines - 1) * gap
    else:
        if lines <= 1:
            # one column of n tiles (per is stack capacity along height)
            rows_used = max(1, min(int(n), int(per)))
            content_h = rows_used * cell_h + max(0, rows_used - 1) * gap
            content_w = cell_w
        else:
            content_w = lines * cell_w + max(0, lines - 1) * gap
            content_h = per * cell_h + max(0, per - 1) * gap
    ox = area_x + max(0, (area_w - content_w) // 2)
    oy = area_y + max(0, (area_h - content_h) // 2)
    return ox, oy


class TableView:
    def __init__(
        self,
        assets: AssetManager,
        layout: Layout | None = None,
        *,
        spectator: SpectatorMode = "full",
        focus_seat: int = 0,
        show_hud: bool = True,
        control_panel: ControlPanel | None = None,
    ) -> None:
        self.assets = assets
        self.layout = layout or Layout()
        self.spectator = spectator
        self.focus_seat = focus_seat
        self.show_hud = show_hud
        self.panel = control_panel or ControlPanel()
        self._bg_scaled: pygame.Surface | None = None
        self.last_focus_hand_pos: list[tuple[str, int, int, int]] = []
        # From app: all seats used auto-start last ready (enables settlement auto-next switch)
        self.auto_next_eligible: bool = False
        self.play_log: PlayEventLog | None = None

    @property
    def options(self) -> TableUIOptions:
        return self.panel.options

    def set_spectator(self, mode: SpectatorMode, focus_seat: int = 0) -> None:
        self.spectator = mode
        self.focus_seat = focus_seat
        self.options.focus_seat = focus_seat

    def resize(self, width: int, height: int) -> None:
        collapsed = not self.panel.options.panel_expanded
        self.layout = Layout.from_window(
            width, height, side_collapsed=collapsed
        )
        # SIDE mid region for control panel
        regions = self.layout.side_regions()
        self.panel.set_region(regions["mid"] if not collapsed else None)
        self._bg_scaled = None

    def _bg(self, screen: pygame.Surface) -> None:
        sw, sh = screen.get_size()
        collapsed = not self.panel.options.panel_expanded
        need = (
            self.layout.width != sw
            or self.layout.height != sh
            or bool(self.layout.panel_w <= 40) != collapsed
        )
        if need:
            self.resize(sw, sh)
        if self._bg_scaled is None or self._bg_scaled.get_size() != (sw, sh):
            raw = self.assets.bg("table")
            # Scale bg to TABLE area only, fill side solid
            mi = self.layout.ensure_interior()
            table_bg = pygame.transform.smoothscale(raw, (mi.table.w, mi.table.h))
            full = pygame.Surface((sw, sh))
            full.fill((12, 28, 22))
            full.blit(table_bg, (mi.table.x, mi.table.y))
            self._bg_scaled = full
        screen.blit(self._bg_scaled, (0, 0))

    def _show_face(self, seat: int) -> bool:
        if not self.options.face_visible(seat):
            return False
        if self.spectator == "full":
            return True
        return seat == self.focus_seat

    def _draw_dice_center(
        self,
        screen: pygame.Surface,
        state: GameState,
        *,
        dice_fx=None,
    ) -> None:
        """Center plate: animated or final dice + dealer + wall remaining."""
        ly = self.layout
        mi = ly.ensure_interior()
        cx, cy = mi.dice.center()
        dice_rect = pygame.Rect(*mi.dice.as_tuple())
        rolling = bool(dice_fx is not None and getattr(dice_fx, "is_rolling", lambda: False)())
        # Stronger highlight while rolling
        plate = pygame.Surface((dice_rect.w, dice_rect.h), pygame.SRCALPHA)
        plate.fill((30, 70, 40, 200) if rolling else (20, 50, 36, 170))
        screen.blit(plate, dice_rect.topleft)
        border = (255, 193, 7) if rolling else (80, 140, 100)
        pygame.draw.rect(screen, border, dice_rect, 3 if rolling else 2, border_radius=8)

        # Resolve faces: active fx > state.dice > placeholder
        f1, f2 = 1, 1
        dealer = getattr(state, "dealer_seat", None)
        total = None
        if dice_fx is not None:
            try:
                f1, f2 = dice_fx.faces()
                dealer = int(dice_fx.dealer_seat)
                total = int(dice_fx.total)
            except Exception:
                pass
        elif getattr(state, "dice", None) is not None:
            try:
                f1, f2 = int(state.dice.d1), int(state.dice.d2)
                total = int(state.dice.total)
                dealer = int(state.dealer_seat)
            except Exception:
                pass

        face_w = max(28, min(72, dice_rect.w // 3))
        try:
            img1 = self.assets.scale_to_width(self.assets.dice(f1), face_w)
            img2 = self.assets.scale_to_width(self.assets.dice(f2), face_w)
            gap = max(8, face_w // 6)
            y0 = cy - img1.get_height() // 2 - (10 if rolling else 18)
            screen.blit(img1, (cx - img1.get_width() - gap // 2, y0))
            screen.blit(img2, (cx + gap // 2, y0))
        except Exception:
            draw_text(
                screen,
                f"{f1}  {f2}",
                (cx - 24, cy - 30),
                size=28,
                color=(255, 240, 180),
            )

        # Caption
        if dice_fx is not None:
            cap = dice_fx.caption()
            col = (255, 230, 120) if rolling else (180, 255, 180)
        else:
            if total is not None and dealer is not None:
                cap = f"骰点 {f1}+{f2}={total} · 庄 S{dealer}"
            else:
                cap = "掷骰定庄"
            col = (220, 230, 200)
        draw_text(
            screen,
            cap,
            (max(dice_rect.x + 4, cx - len(cap) * 4), dice_rect.y + 6),
            size=14,
            color=col,
        )

        # Wall remaining (below dice faces)
        wall_n = len(state.wall) if state.wall is not None else 0
        blit_score(
            screen, self.assets, wall_n, (cx - 8, cy + face_w // 3), size="md"
        )
        draw_text(
            screen,
            f"牌墙 {wall_n}",
            (cx - 36, cy + face_w // 3 + 28),
            size=14,
            color=(220, 230, 200),
        )
        if dealer is not None and not rolling:
            draw_text(
                screen,
                f"★ 庄家 S{dealer}",
                (cx - 48, dice_rect.bottom - 22),
                size=15,
                color=(255, 220, 120),
            )

    def draw(
        self,
        screen: pygame.Surface,
        state: GameState,
        fx: FxOverlay | None = None,
        analysis: AnalysisSnapshot | None = None,
        dice_fx=None,
    ) -> None:
        self._bg(screen)
        n = state.num_players
        self.options.ensure_seats(n)
        self.options.focus_seat = self.focus_seat
        self.last_focus_hand_pos = []
        ly = self.layout

        # Status (top-left, clear of hands)
        draw_text(screen, f"phase: {state.phase}", (12, 8), size=16)
        draw_text(
            screen,
            f"game: {str(state.game_id)[:20]}",
            (12, 28),
            size=13,
            color=(180, 200, 180),
        )
        if self._status_line():
            draw_text(
                screen,
                self._status_line(),
                (12, 46),
                size=12,
                color=(160, 200, 255),
            )

        # DICE center: real roll process / result (F0023)
        self._draw_dice_center(screen, state, dice_fx=dice_fx)

        # HUD first (center / side), then seats so hand tiles paint on top
        bot = ly.bottom_band()
        if self.show_hud and analysis is not None:
            if self.options.show_inference:
                draw_inference_hud(
                    screen,
                    self.assets,
                    self.layout,
                    state,
                    analysis,
                    self.focus_seat,
                    hand_positions=None,  # markers after hands drawn
                    panel_w=self.panel.width,
                )
            if self.options.show_strategy:
                draw_strategy_hud(
                    screen,
                    self.assets,
                    analysis,
                    hand_positions=None,
                    panel_w=self.panel.width,
                    bottom_hand_y=bot[1],
                )

        for p in state.players:
            slot = seat_to_slot(p.seat, self.focus_seat, n)
            self._draw_player(screen, state, p.seat, slot)

        # Danger / strategy marks on focus hand (after tiles, above panel)
        if self.show_hud and analysis is not None and self.last_focus_hand_pos:
            if self.options.show_inference:
                draw_inference_hud(
                    screen,
                    self.assets,
                    self.layout,
                    state,
                    analysis,
                    self.focus_seat,
                    hand_positions=self.last_focus_hand_pos,
                    panel_w=self.panel.width,
                    marks_only=True,
                )
            if self.options.show_strategy:
                draw_strategy_hud(
                    screen,
                    self.assets,
                    analysis,
                    hand_positions=self.last_focus_hand_pos,
                    panel_w=self.panel.width,
                    bottom_hand_y=bot[1],
                    marks_only=True,
                )

        # SIDE: scoreboard (top) + control mid + play log bot
        regions = ly.side_regions()
        draw_side_scoreboard(
            screen,
            regions["top"],
            state,
            focus_seat=self.focus_seat,
        )
        self.panel.set_region(regions["mid"])
        self.panel.draw(
            screen,
            num_players=n,
            auto_next_eligible=bool(self.auto_next_eligible),
        )
        draw_play_log_panel(screen, regions["bot"], self.play_log)

        if fx:
            fx.draw(screen, self.assets)

    def _status_line(self) -> str:
        parts = []
        if self.show_hud:
            parts.append("HUD")
        if self.options.show_inference:
            parts.append("推理")
        if self.options.show_strategy:
            parts.append("策略")
        return " · ".join(parts)

    def _draw_player(
        self, screen: pygame.Surface, state: GameState, seat: int, slot: str
    ) -> None:
        p = next(x for x in state.players if x.seat == seat)
        ly = self.layout
        tw = ly.tile_w
        assert tw >= MIN_TABLE_TW
        rot = self._slot_tile_rotation(slot)
        cell_w, cell_h = ly.cell_size(rotate=rot)
        gap = 3

        # Avatar + score (offset so they don't cover tile band)
        ax, ay = ly.avatar_pos(slot)
        try:
            av = self.assets.avatar((seat % 4) + 1)
            av = self.assets.scale_to_width(av, 48)
            screen.blit(av, (ax, ay))
            if p.is_dealer:
                badge = self.assets.dealer_badge()
                badge = self.assets.scale_to_width(badge, 18)
                screen.blit(badge, (ax + 34, ay - 2))
        except FileNotFoundError:
            pass
        sx, sy = ly.score_pos(slot)
        blit_score(screen, self.assets, p.score, (sx, sy), size="sm")
        st_label = str(p.status)
        if st_label == "finished":
            st_label = "已胡"
        draw_text(
            screen,
            f"S{seat} {st_label}",
            (sx, sy + 22),
            size=13,
            color=(255, 230, 160) if p.status == "finished" else (220, 220, 200),
        )

        face = self._show_face(seat) and p.status == "active"
        hand = p.sorted_hand() if p.status == "active" else []
        # show finished hand face-up if they already won (optional readability)
        if p.status == "finished" and self._show_face(seat):
            hand = p.sorted_hand()
            face = True

        hx, hy, hw, hh = {
            "bottom": ly.bottom_band(),
            "top": ly.top_band(),
            "left": ly.left_band(),
            "right": ly.right_band(),
        }[slot]

        collect = seat == self.focus_seat
        horizontal = slot in ("bottom", "top")
        hand_lines = 0
        prev_clip = screen.get_clip()

        # --- Hand (strict ZONE_HAND rect; same face size & center logic all seats) ---
        if hand:
            # cell_w/h already account for ±90° (L/R → th×tw on screen)
            per, hand_lines, cw, ch = _pack_fixed(
                len(hand),
                hw,
                hh,
                cell_w,
                cell_h,
                gap=gap,
                horizontal=horizontal,
            )
            # Face width for scale_to_width (pre-rotation). After ±90°, on-screen
            # size is (≈1.4·draw_tw)×draw_tw which matches packed (cw)×(ch).
            if horizontal:
                draw_tw = min(tw, cw)
                draw_th = max(1, int(round(draw_tw * 1.4)))
                step_w, step_h = draw_tw, max(ch, draw_th)
            else:
                # ch is post-rotation face width (= pre-rotation draw_tw)
                # cw is post-rotation face height (≈1.4·draw_tw)
                draw_tw = min(tw, ch)
                step_w, step_h = cw, ch
            ox, oy = _center_origin(
                hx,
                hy,
                hw,
                hh,
                n=len(hand),
                per=per,
                lines=hand_lines,
                cell_w=step_w,
                cell_h=step_h,
                gap=gap,
                horizontal=horizontal,
            )
            screen.set_clip(pygame.Rect(hx, hy, hw, hh))
            for i, t in enumerate(hand):
                if horizontal:
                    row, col = divmod(i, per)
                    x = ox + col * (step_w + gap)
                    y = oy + row * (step_h + gap)
                    x += max(0, (step_w - draw_tw) // 2)
                else:
                    # same divmod model as horizontal, axes swapped via per-along-height
                    col, row = divmod(i, per)
                    x = ox + col * (step_w + gap)
                    y = oy + row * (step_h + gap)
                    # center face in cell if packed step exceeds drawn tile
                    x += max(0, (step_w - max(1, int(round(draw_tw * 1.4)))) // 2)
                    y += max(0, (step_h - draw_tw) // 2)
                tid = t.id if face else None
                self._blit_tile(screen, tid, x, y, draw_tw, rotate=rot)
                if collect and face:
                    self.last_focus_hand_pos.append((t.id, x, y, draw_tw))
            screen.set_clip(prev_clip)

        # --- Melds (ZONE_MELD, centered) ---
        if self.options.show_melds and (p.melds or []):
            flat: list[str] = []
            for m in p.melds or []:
                if not isinstance(m, dict):
                    continue
                tid = m.get("tile_id")
                kind = str(m.get("kind") or "")
                if not tid:
                    continue
                n = 4 if "gang" in kind else 3
                flat.extend([str(tid)] * n)
            if flat:
                mx, my, mw, mh = ly.meld_area(slot)
                horiz = slot in ("bottom", "top")
                mrot = rot if not horiz else 0
                mcw0, mch0 = ly.cell_size(rotate=mrot)
                per_m, lines_m, mcw, mch = _pack_fixed(
                    len(flat), mw, mh, mcw0, mch0, gap=2, horizontal=horiz
                )
                ox, oy = _center_origin(
                    mx,
                    my,
                    mw,
                    mh,
                    n=len(flat),
                    per=per_m,
                    lines=lines_m,
                    cell_w=mcw,
                    cell_h=mch,
                    gap=2,
                    horizontal=horiz,
                )
                draw_tw = min(tw, mcw if horiz else mch)
                screen.set_clip(pygame.Rect(mx, my, mw, mh))
                for i, tid in enumerate(flat):
                    if horiz:
                        row, col = divmod(i, per_m)
                        x = ox + col * (mcw + 2)
                        y = oy + row * (mch + 2)
                    else:
                        col, row = divmod(i, per_m)
                        x = ox + col * (mcw + 2)
                        y = oy + row * (mch + 2)
                    self._blit_tile(screen, tid, x, y, draw_tw, rotate=mrot)
                screen.set_clip(prev_clip)

        # --- Discards (ZONE_DISC, centered + clip) ---
        if self.options.show_discards:
            disc = list(p.discard_pile or [])[-24:]
            if disc:
                self._draw_discards(screen, disc, slot, tw)

    def _draw_discards(
        self,
        screen: pygame.Surface,
        disc: list,
        slot: str,
        tw: int,
    ) -> None:
        """Draw river inside ZONE_DISC, centered and hard-clipped to the rect."""
        ly = self.layout
        gap = 2
        rot = 0 if slot in ("bottom", "top") else self._slot_tile_rotation(slot)
        cell_w, cell_h = ly.cell_size(rotate=rot)
        ax, ay, aw, ah = ly.river_area(slot)
        horiz = slot in ("bottom", "top")
        per, lines, cw, ch = _pack_fixed(
            len(disc), aw, ah, cell_w, cell_h, gap=gap, horizontal=horiz
        )
        max_tiles = per * max(1, lines)
        if len(disc) > max_tiles:
            disc = disc[-max_tiles:]
            # recompute lines for truncated count
            lines = max(1, math.ceil(len(disc) / per))

        ox, oy = _center_origin(
            ax,
            ay,
            aw,
            ah,
            n=len(disc),
            per=per,
            lines=lines,
            cell_w=cw,
            cell_h=ch,
            gap=gap,
            horizontal=horiz,
        )
        draw_tw = min(tw, cw if horiz else ch)
        prev = screen.get_clip()
        screen.set_clip(pygame.Rect(ax, ay, aw, ah))
        for i, t in enumerate(disc):
            tid = t.id if hasattr(t, "id") else str(t)
            if horiz:
                row, col = divmod(i, per)
                x = ox + col * (cw + gap)
                y = oy + row * (ch + gap)
            else:
                col, row = divmod(i, per)
                x = ox + col * (cw + gap)
                y = oy + row * (ch + gap)
            self._blit_tile(screen, tid, x, y, draw_tw, rotate=rot)
        screen.set_clip(prev)

    @staticmethod
    def _slot_tile_rotation(slot: str) -> int:
        if slot == "left":
            return -90
        if slot == "right":
            return 90
        return 0

    def _blit_tile(
        self,
        screen: pygame.Surface,
        tile_id: str | None,
        x: int,
        y: int,
        w: int,
        *,
        rotate: int = 0,
    ) -> tuple[int, int]:
        try:
            if tile_id is None:
                surf = self.assets.tile_back()
            else:
                t = parse_tile(tile_id)
                surf = self.assets.tile(t.suit.value, t.rank)
            surf = self.assets.scale_to_width(surf, w)
            if rotate:
                surf = pygame.transform.rotate(surf, int(rotate))
            screen.blit(surf, (x, y))
            return surf.get_width(), surf.get_height()
        except (FileNotFoundError, ValueError):
            h = int(w * 1.4)
            if abs(int(rotate)) % 180 == 90:
                rw, rh = h, w
            else:
                rw, rh = w, h
            pygame.draw.rect(screen, (80, 80, 80), (x, y, rw, rh), 1)
            return rw, rh
