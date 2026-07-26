#!/usr/bin/env python3
"""Unified interior layout schematics for MAIN / HUMAN / AI windows.

Uses 1080p multi-window default outer size from UI_DESIGN_STANDARD:
  MAIN / Human Full = 885 x 498
AI schematic uses the same outer size as Human for readability of interior
proportions (67/33 etc.); multi-window AI outer may be smaller (6.25%).
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "design" / "window_interiors"

# 1080p default seat/main outer (UI_DESIGN_STANDARD §8.2)
W, H = 885, 498

BG = (40, 44, 50)
GRID = (52, 56, 64)
TEXT = (236, 239, 244)
TEXT_DIM = (160, 168, 180)
FRAME = (100, 106, 118)

COLORS = {
    "table": ((36, 72, 52), (80, 160, 110)),
    "side": ((32, 40, 56), (100, 140, 200)),
    "op": ((36, 58, 72), (64, 168, 192)),
    "ext": ((58, 48, 36), (220, 170, 80)),
    "dice": ((50, 45, 30), (220, 190, 100)),
    "p1": ((45, 55, 70), (120, 180, 220)),
    "p2": ((50, 45, 60), (180, 140, 200)),
    "p3": ((40, 55, 50), (120, 200, 160)),
    "p4": ((55, 50, 40), (200, 160, 100)),
    "info": ((30, 36, 42), (140, 150, 160)),
    "status": ((38, 48, 58), (100, 160, 200)),
    "play": ((34, 52, 44), (100, 180, 120)),
    "set": ((42, 40, 50), (160, 140, 200)),
    "hud": ((48, 40, 40), (200, 120, 100)),
    "disc": ((36, 48, 40), (120, 180, 100)),
    "log": ((40, 42, 55), (140, 150, 220)),
    "meld": ((40, 50, 48), (100, 160, 140)),
    "hand": ((32, 48, 40), (90, 170, 110)),
    "act": ((50, 40, 40), (200, 120, 90)),
}


def fonts(scale: float = 1.0):
    def s(n: int) -> int:
        return max(9, int(round(n * scale)))

    try:
        return (
            ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", s(14)),
            ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", s(12)),
            ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", s(10)),
            ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", s(9)),
        )
    except Exception:
        f = ImageFont.load_default()
        return f, f, f, f


def tsize(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0], b[3] - b[1]


def box(draw, x, y, w, h, key, title, size_txt, ft, multiline: str | None = None):
    fill, border = COLORS[key]
    title_f, body_f, small_f, tiny_f = ft
    if w < 2 or h < 2:
        return
    draw.rectangle((x, y, x + w - 1, y + h - 1), fill=fill, outline=border, width=2)
    th = min(22, max(14, h // 6))
    draw.rectangle((x + 1, y + 1, x + w - 2, y + th), fill=tuple(c // 2 for c in fill))
    draw.text((x + 4, y + 2), title, font=small_f, fill=border)
    # size center
    tw, tht = tsize(draw, size_txt, body_f)
    cx = x + max(0, (w - tw) // 2)
    cy = y + th + max(0, (h - th - tht) // 2 - (8 if multiline else 0))
    draw.text((cx, cy), size_txt, font=body_f, fill=TEXT)
    if multiline:
        lines = multiline.split("\n")
        yy = cy + tht + 2
        for line in lines:
            lw, lh = tsize(draw, line, tiny_f)
            draw.text((x + max(0, (w - lw) // 2), yy), line, font=tiny_f, fill=TEXT_DIM)
            yy += lh + 1
    # corner size
    tw2, _ = tsize(draw, size_txt, tiny_f)
    draw.text((x + w - tw2 - 3, y + h - 12), size_txt, font=tiny_f, fill=TEXT_DIM)


def canvas(title: str, subtitle: str):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for gx in range(0, W, 40):
        d.line([(gx, 0), (gx, H - 1)], fill=GRID, width=1)
    for gy in range(0, H, 40):
        d.line([(0, gy), (W - 1, gy)], fill=GRID, width=1)
    d.rectangle((0, 0, W - 1, H - 1), outline=FRAME, width=2)
    ft = fonts(W / 885.0)
    foot = 20
    d.rectangle((0, H - foot, W - 1, H - 1), fill=(28, 30, 34))
    _, _, _, tiny = ft
    d.text((6, H - 16), title, font=tiny, fill=TEXT)
    mw, _ = tsize(d, subtitle, tiny)
    d.text((W - mw - 6, H - 16), subtitle, font=tiny, fill=TEXT_DIM)
    return im, d, ft, foot


def save(im: Image.Image, name: str):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    im.save(path, "JPEG", quality=92, optimize=True)
    print(f"wrote {path.name} {im.size[0]}x{im.size[1]}")
    return path


def gen_main():
    """MAIN: 80/20, dice center, 4 sectors, side 35/30/35."""
    im, d, ft, foot = canvas(
        "主窗口内部 · 完整 · 外框885×498(1080p默认)",
        "80% TABLE | 20% SIDE · MAIN_WINDOW_LAYOUT v0.1 已确认",
    )
    usable_h = H - foot
    Tw = int(W * 0.80)
    Sw = W - Tw
    # TABLE
    box(d, 0, 0, Tw, usable_h, "table", "TABLE 实时牌局", f"{Tw}×{usable_h}", ft, "占比 80%")
    # DICE square
    D = int(min(Tw, usable_h) * 0.28)
    Dx = (Tw - D) // 2
    Dy = (usable_h - D) // 2
    box(d, Dx, Dy, D, D, "dice", "DICE 掷骰", f"{D}×{D}", ft, "正方形·同心")
    # Draw corner rays lightly
    TL, TR, BR, BL = (0, 0), (Tw, 0), (Tw, usable_h), (0, usable_h)
    dTL, dTR, dBR, dBL = (Dx, Dy), (Dx + D, Dy), (Dx + D, Dy + D), (Dx, Dy + D)
    for a, b in ((TL, dTL), (TR, dTR), (BR, dBR), (BL, dBL)):
        d.line([a, b], fill=(90, 120, 100), width=1)
    # Approximate sector labels (bounding midpoints)
    sectors = [
        ("p1", "玩家1 下", (Tw // 2 - 40, usable_h - 36, 80, 28)),
        ("p2", "玩家2 右", (Tw - 70, usable_h // 2 - 20, 60, 40)),
        ("p3", "玩家3 上", (Tw // 2 - 40, 8, 80, 28)),
        ("p4", "玩家4 左", (8, usable_h // 2 - 20, 60, 40)),
    ]
    for key, lab, (x, y, w, h) in sectors:
        box(d, x, y, w, h, key, lab, f"扇区", ft)
    # SIDE
    H_top = int(usable_h * 0.35)
    H_mid = int(usable_h * 0.30)
    H_bot = usable_h - H_top - H_mid
    box(d, Tw, 0, Sw, H_top, "side", "SIDE上 状态积分", f"{Sw}×{H_top}", ft, "35%")
    box(d, Tw, H_top, Sw, H_mid, "set", "SIDE中 设置开关", f"{Sw}×{H_mid}", ft, "30%")
    box(d, Tw, H_top + H_mid, Sw, H_bot, "log", "SIDE下 出牌日志", f"{Sw}×{H_bot}", ft, "35%")
    return save(im, "MAIN_interior_1080p.jpg")


def gen_human():
    im, d, ft, foot = canvas(
        "人类窗口内部 · play · 外框885×498(1080p默认)",
        "OP67% | EXT33%可折叠 · HUMAN_WINDOW_LAYOUT 已确认",
    )
    usable_h = H - foot
    Ow = int(W * 0.67)
    Ew = W - Ow
    H_ROW = max(28, min(40, int(usable_h * 0.04)))
    H_info = H_ROW
    H_set = 2 * H_ROW
    rest = usable_h - H_info - H_set
    H_status = int(rest * 0.20 / 0.80)
    H_play = rest - H_status
    y = 0
    box(d, 0, y, Ow, H_info, "info", "OP_INFO 玩家信息", f"{Ow}×{H_info}", ft, "1行")
    y += H_info
    # status L/R
    box(d, 0, y, Ow // 2, H_status, "status", "状态L 打出/谁/牌墙", f"{Ow//2}×{H_status}", ft, "25%半")
    box(d, Ow // 2, y, Ow - Ow // 2, H_status, "status", "状态R 局数/得分", f"{Ow-Ow//2}×{H_status}", ft, "25%半")
    y += H_status
    # play: melds 35% hand 65% of H_play
    H_meld = int(H_play * 0.35)
    H_hand = H_play - H_meld
    box(d, 0, y, Ow, H_meld, "meld", "副露区", f"{Ow}×{H_meld}", ft, "PLAY上")
    y += H_meld
    H_hand_tiles = int(H_hand * 0.72)
    H_act = H_hand - H_hand_tiles
    box(d, 0, y, Ow, H_hand_tiles, "hand", "手牌区", f"{Ow}×{H_hand_tiles}", ft, "可点选")
    y += H_hand_tiles
    box(d, 0, y, Ow, H_act, "act", "碰/杠/胡/过", f"{Ow}×{H_act}", ft, "无吃")
    y += H_act
    box(d, 0, y, Ow, H_set, "set", "设置 2行", f"{Ow}×{H_set}", ft, "自动开始/预测/推荐")
    # EXT
    H_hud = int(usable_h * 0.30)
    H_disc = usable_h - H_hud
    box(d, Ow, 0, Ew, H_hud, "hud", "EXT上 对手HUD", f"{Ew}×{H_hud}", ft, "30%")
    box(d, Ow, H_hud, Ew, H_disc, "disc", "EXT下 本家弃牌", f"{Ew}×{H_disc}", ft, "70% 可折叠")
    return save(im, "HUMAN_interior_1080p.jpg")


def gen_ai():
    im, d, ft, foot = canvas(
        "AI窗口内部 · watch · 外框885×498(示意;多窗AI可更小)",
        "OP67% | EXT33% · 只读手牌 · AI_WINDOW_LAYOUT v0.1",
    )
    usable_h = H - foot
    Ow = int(W * 0.67)
    Ew = W - Ow
    H_ROW = max(28, min(40, int(usable_h * 0.04)))
    H_info = H_ROW
    H_set = 2 * H_ROW
    rest = usable_h - H_info - H_set
    H_status = int(rest * 0.20 / 0.80)
    H_play = rest - H_status
    y = 0
    box(d, 0, y, Ow, H_info, "info", "OP_INFO AI信息", f"{Ow}×{H_info}", ft, "只读·策略")
    y += H_info
    box(d, 0, y, Ow // 2, H_status, "status", "状态L 打出/谁/牌墙", f"{Ow//2}×{H_status}", ft, "25%半")
    box(d, Ow // 2, y, Ow - Ow // 2, H_status, "status", "状态R 局数/得分", f"{Ow-Ow//2}×{H_status}", ft, "25%半")
    y += H_status
    H_meld = int(H_play * 0.35)
    H_hand = H_play - H_meld
    box(d, 0, y, Ow, H_meld, "meld", "副露区", f"{Ow}×{H_meld}", ft, "只读")
    y += H_meld
    box(d, 0, y, Ow, H_hand, "hand", "手牌区(只读)", f"{Ow}×{H_hand}", ft, "无操作条")
    y += H_hand
    box(d, 0, y, Ow, H_set, "set", "设置 2行", f"{Ow}×{H_set}", ft, "自动开始/预测/策略")
    H_log = int(usable_h * 0.30)
    H_disc = usable_h - H_log
    box(d, Ow, 0, Ew, H_log, "log", "EXT上 AI操作日志", f"{Ew}×{H_log}", ft, "30%")
    box(d, Ow, H_log, Ew, H_disc, "disc", "EXT下 本家弃牌", f"{Ew}×{H_disc}", ft, "70% 可折叠")
    return save(im, "AI_interior_1080p.jpg")


def main():
    if OUT.exists():
        for p in list(OUT.glob("*.jpg")) + list(OUT.glob("*.png")):
            p.unlink()
            print("deleted", p.name)
    gen_main()
    gen_human()
    gen_ai()
    print("OK", OUT)


if __name__ == "__main__":
    main()
