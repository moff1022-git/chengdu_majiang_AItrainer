"""Pure geometry for human (play) and AI (watch) seat windows — F0016/F0017/F0019.

Vertical OP (design HUMAN/AI_WINDOW_LAYOUT §3.1 v0.2)::

    OP_INFO     1 row fixed
    OP_STATUS   20% of flex (rest after info+settings)
    OP_PLAY     60% of flex  (hand + action bar at bottom of this zone)
    OP_SETTINGS 2 rows fixed

Horizontal::

    OP 67% | EXT 33%  (EXT fold → OP 100%)
    EXT_TOP 30% | EXT_BOT 70%
"""

from __future__ import annotations

from dataclasses import dataclass


OP_WIDTH_RATIO = 0.67
EXT_WIDTH_RATIO = 0.33
# HUMAN/AI_WINDOW_LAYOUT v0.2: status 20% / play 60% of flex (weights sum 80)
STATUS_RATIO = 0.20
PLAY_RATIO = 0.60
EXT_HUD_RATIO = 0.30
EXT_DISC_RATIO = 0.70

# Compact (F0014 / UI_DESIGN_STANDARD §7): width 50% of full, left anchor
COMPACT_WIDTH_RATIO = 0.50
# When compact hides EXT disc band, height may shrink (user: 尺寸同步减小)
COMPACT_HEIGHT_RATIO = 0.72


@dataclass(frozen=True, slots=True)
class Rect:
    x: int
    y: int
    w: int
    h: int

    def as_tuple(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.w, self.h


@dataclass(frozen=True, slots=True)
class SeatInteriorLayout:
    client_w: int
    client_h: int
    expanded: bool
    view_mode: str  # full | compact
    op: Rect
    ext: Rect | None
    op_info: Rect
    op_status: Rect
    op_play: Rect
    op_settings: Rect
    ext_top: Rect | None
    ext_bot: Rect | None
    # play zone split: melds+hand vs action strip
    play_hand: Rect
    play_actions: Rect


def _row_h(Ch: int) -> int:
    return max(22, min(40, int(round(Ch * 0.04))))


def compute_seat_interior(
    Cw: int,
    Ch: int,
    *,
    expanded: bool = True,
    view_mode: str = "full",
    info_h: int | None = None,
    settings_h: int | None = None,
    action_h: int | None = None,
) -> SeatInteriorLayout:
    """
    Strict proportions from design docs.

    OP_PLAY contains hand area + action bar (actions above OP_SETTINGS).
    """
    Cw = max(200, int(Cw))
    Ch = max(160, int(Ch))
    row = _row_h(Ch)
    info_h = int(info_h) if info_h is not None else row
    # settings: 2 rows
    settings_h = int(settings_h) if settings_h is not None else 2 * row
    info_h = max(20, info_h)
    settings_h = max(36, settings_h)
    # action strip hint from caller (optional floor); final size set after pl_h
    act_hint = int(action_h) if action_h is not None else 0

    vm = "compact" if str(view_mode).lower() in ("compact", "hand", "mini") else "full"
    # Compact: hide EXT disc → often collapse EXT or keep HUD only
    show_ext = bool(expanded) and vm == "full"
    # Also allow expanded compact with only top HUD (no disc) — use expanded flag
    if expanded and vm == "compact":
        show_ext = True  # HUD/log only; bot h=0
    if not expanded:
        show_ext = False

    if show_ext:
        Ow = int(Cw * OP_WIDTH_RATIO)
        Ow = max(120, min(Ow, Cw - 40))
        Ew = Cw - Ow
        op = Rect(0, 0, Ow, Ch)
        ext = Rect(Ow, 0, Ew, Ch)
        if vm == "compact":
            # full EXT height to top only (disc hidden)
            ext_top = Rect(Ow, 0, Ew, Ch)
            ext_bot = Rect(Ow, Ch, Ew, 0)
        else:
            et_h = int(Ch * EXT_HUD_RATIO)
            et_h = max(40, min(et_h, Ch - 40))
            eb_h = Ch - et_h
            ext_top = Rect(Ow, 0, Ew, et_h)
            ext_bot = Rect(Ow, et_h, Ew, eb_h)
    else:
        Ow = Cw
        op = Rect(0, 0, Ow, Ch)
        ext = None
        ext_top = None
        ext_bot = None

    # Design §3.1: rest after info+settings split 20:60
    rest = max(40, Ch - info_h - settings_h)
    st_h = int(rest * (STATUS_RATIO / (STATUS_RATIO + PLAY_RATIO)))
    pl_h = rest - st_h
    # clamp status/play ratio near 20:60 of flex
    # (info+settings ≈ 20% of Ch)
    y = 0
    op_info = Rect(0, y, Ow, info_h)
    y += info_h
    op_status = Rect(0, y, Ow, st_h)
    y += st_h
    op_play = Rect(0, y, Ow, pl_h)
    y += pl_h
    op_settings = Rect(0, y, Ow, max(settings_h, Ch - y))

    # Actions strip: **single row** (hint 50% | buttons 50%)
    row_act = max(22, min(36, int(round(Ch * 0.05))))
    if act_hint > 0:
        row_act = max(row_act, min(int(act_hint), 40))
    act_h = min(row_act, max(22, pl_h // 6))
    hand_h = max(20, pl_h - act_h)
    play_hand = Rect(0, op_play.y, Ow, hand_h)
    play_actions = Rect(0, op_play.y + hand_h, Ow, act_h)

    return SeatInteriorLayout(
        client_w=Cw,
        client_h=Ch,
        expanded=bool(expanded),
        view_mode=vm,
        op=op,
        ext=ext,
        op_info=op_info,
        op_status=op_status,
        op_play=op_play,
        op_settings=op_settings,
        ext_top=ext_top,
        ext_bot=ext_bot,
        play_hand=play_hand,
        play_actions=play_actions,
    )


def compact_window_size(full_w: int, full_h: int) -> tuple[int, int]:
    """UI_DESIGN §7 width 50%; height reduced when content removed (user)."""
    w = max(200, int(full_w * COMPACT_WIDTH_RATIO))
    h = max(160, int(full_h * COMPACT_HEIGHT_RATIO))
    return w, h
