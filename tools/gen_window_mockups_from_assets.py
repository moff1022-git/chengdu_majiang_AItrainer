#!/usr/bin/env python3
"""Compose full MAIN / HUMAN / AI window mockups using project assets/ (green theme).

Output: docs/design/window_interiors/*_mockup_assets_green.jpg
Canvas: 1770x996 (2× 1080p default outer 885×498 for readable tiles)
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ROOT / "docs" / "design" / "window_interiors"
THEME = "green"

# 2× 1080p default outer (885×498) — proportions match design docs
CW, CH = 1770, 996

# Colors aligned with palette green
PANEL = (12, 32, 24, 230)
PANEL_SOLID = (18, 42, 32)
BAR = (10, 26, 18)
GOLD = (255, 220, 120)
TEXT = (245, 245, 235)
MUTED = (180, 200, 185)
BORDER = (70, 140, 100)


def font(size: int, bold: bool = False):
    path = "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


_cache: dict[str, Image.Image] = {}


def load(rel: str) -> Image.Image:
    key = rel
    if key in _cache:
        return _cache[key].copy()
    p = ASSETS / rel
    if not p.exists():
        # transparent placeholder
        im = Image.new("RGBA", (64, 64), (80, 80, 80, 180))
        _cache[key] = im
        return im.copy()
    im = Image.open(p).convert("RGBA")
    _cache[key] = im
    return im.copy()


def tile(suit: str, n: int) -> Image.Image:
    return load(f"tiles/{suit}/tile_{suit}_{n}_{THEME}.png")


def tile_back() -> Image.Image:
    return load(f"tiles/backs/tile_back_{THEME}.png")


def scale_w(im: Image.Image, w: int) -> Image.Image:
    if im.width == w:
        return im
    h = max(1, int(round(im.height * (w / im.width))))
    return im.resize((w, h), Image.Resampling.LANCZOS)


def scale_h(im: Image.Image, h: int) -> Image.Image:
    if im.height == h:
        return im
    w = max(1, int(round(im.width * (h / im.height))))
    return im.resize((w, h), Image.Resampling.LANCZOS)


def paste(base: Image.Image, im: Image.Image, xy: tuple[int, int], opacity: float = 1.0):
    if opacity < 1.0:
        a = im.split()[3]
        a = ImageEnhance.Brightness(a).enhance(opacity)
        im = im.copy()
        im.putalpha(a)
    base.alpha_composite(im, dest=xy)


def row_tiles(
    base: Image.Image,
    tiles: list[Image.Image],
    x: int,
    y: int,
    tw: int,
    gap: int = 2,
    max_w: int | None = None,
) -> int:
    """Paste horizontal tile row; return end x."""
    cx = x
    for t in tiles:
        s = scale_w(t, tw)
        if max_w is not None and cx + s.width > x + max_w:
            break
        paste(base, s, (cx, y))
        cx += s.width + gap
    return cx


def rounded_panel(base: Image.Image, box: tuple[int, int, int, int], fill=PANEL_SOLID, outline=BORDER):
    d = ImageDraw.Draw(base)
    x, y, w, h = box
    d.rounded_rectangle((x, y, x + w - 1, y + h - 1), radius=8, fill=fill, outline=outline, width=2)


def text(base: Image.Image, s: str, xy: tuple[int, int], size: int = 16, color=TEXT, bold=False):
    d = ImageDraw.Draw(base)
    d.text(xy, s, font=font(size, bold), fill=color)


def make_base_bg() -> Image.Image:
    bg = load(f"backgrounds/bg_table_{THEME}.png")
    # cover full canvas
    bg = bg.resize((CW, CH), Image.Resampling.LANCZOS)
    return bg.convert("RGBA")


def sample_hand(n: int = 13) -> list[Image.Image]:
    # mix of suits
    seq = [
        ("wan", 1), ("wan", 2), ("wan", 3), ("wan", 5),
        ("tong", 2), ("tong", 2), ("tong", 8),
        ("tiao", 3), ("tiao", 5), ("tiao", 7), ("tiao", 9),
        ("wan", 9), ("tong", 5), ("tiao", 1),
    ]
    return [tile(s, n) for s, n in seq[:n]]


def sample_discards(n: int = 12) -> list[Image.Image]:
    seq = [
        ("tong", 1), ("tong", 3), ("wan", 4), ("tiao", 2),
        ("wan", 6), ("tong", 7), ("tiao", 4), ("wan", 8),
        ("tong", 9), ("tiao", 6), ("wan", 7), ("tong", 4),
    ]
    return [tile(s, k) for s, k in seq[:n]]


def gen_main() -> Path:
    base = make_base_bg()
    # darken slightly for UI readability
    overlay = Image.new("RGBA", (CW, CH), (0, 20, 10, 40))
    base = Image.alpha_composite(base, overlay)
    d = ImageDraw.Draw(base)

    # layout 80/20
    Tw = int(CW * 0.80)
    Sw = CW - Tw
    # side panel
    side = Image.new("RGBA", (Sw, CH), (8, 22, 16, 235))
    base.alpha_composite(side, (Tw, 0))
    d.line([(Tw, 0), (Tw, CH)], fill=BORDER, width=3)

    # TABLE sectors labels + content
    # center dice
    D = int(min(Tw, CH) * 0.28)
    Dx, Dy = (Tw - D) // 2, (CH - D) // 2
    # dice panel
    dice_bg = Image.new("RGBA", (D, D), (20, 50, 35, 200))
    base.alpha_composite(dice_bg, (Dx, Dy))
    d.rounded_rectangle((Dx, Dy, Dx + D, Dy + D), radius=12, outline=GOLD, width=3)
    # two dice
    d1 = scale_w(load(f"dice/dice_4_{THEME}.png"), D // 3)
    d2 = scale_w(load(f"dice/dice_6_{THEME}.png"), D // 3)
    paste(base, d1, (Dx + D // 5, Dy + D // 3))
    paste(base, d2, (Dx + D // 2, Dy + D // 3))
    text(base, "掷骰区", (Dx + D // 2 - 30, Dy + 8), 14, GOLD, True)
    text(base, "牌墙 72", (Dx + D // 2 - 28, Dy + D - 28), 14, MUTED)

    # rays
    for a, b in (
        ((0, 0), (Dx, Dy)),
        ((Tw, 0), (Dx + D, Dy)),
        ((Tw, CH), (Dx + D, Dy + D)),
        ((0, CH), (Dx, Dy + D)),
    ):
        d.line([a, b], fill=(60, 100, 70, 180), width=1)

    # four player zones with tiles
    tw_hand = 36
    # bottom P1
    hand = sample_hand(13)
    row_tiles(base, hand, 80, CH - 90, tw_hand, gap=1, max_w=Tw - 160)
    paste(base, scale_w(load(f"players/avatar_1_{THEME}.png"), 40), (20, CH - 100))
    paste(base, scale_w(load(f"players/seat_south_{THEME}.png"), 36), (20, CH - 55))
    paste(base, scale_w(load(f"players/dealer_badge_{THEME}.png"), 28), (55, CH - 100))
    text(base, "玩家1 · 下  +1200", (70, CH - 105), 13, GOLD)

    # top P3
    backs = [tile_back() for _ in range(13)]
    row_tiles(base, backs, 80, 50, tw_hand - 4, gap=1, max_w=Tw - 160)
    paste(base, scale_w(load(f"players/avatar_3_{THEME}.png"), 36), (Tw - 70, 20))
    paste(base, scale_w(load(f"players/seat_north_{THEME}.png"), 32), (Tw - 70, 58))
    text(base, "玩家3 · 上", (Tw - 160, 28), 12, MUTED)

    # left P4 — vertical stack simplified as small column of backs
    ly = 160
    for i in range(8):
        tb = scale_w(tile_back(), 28)
        tb = tb.rotate(90, expand=True)
        paste(base, tb, (18, ly + i * (tb.height + 1)))
    paste(base, scale_w(load(f"players/avatar_4_{THEME}.png"), 32), (12, 120))
    text(base, "玩家4", (10, 100), 11, MUTED)

    # right P2
    rx = Tw - 70
    ly = 160
    for i in range(8):
        tb = scale_w(tile_back(), 28)
        tb = tb.rotate(-90, expand=True)
        paste(base, tb, (rx, ly + i * (tb.height + 1)))
    paste(base, scale_w(load(f"players/avatar_2_{THEME}.png"), 32), (Tw - 55, 120))
    text(base, "玩家2", (Tw - 70, 100), 11, MUTED)

    # center river discards near dice
    disc = sample_discards(8)
    row_tiles(base, disc, Dx - 20, Dy + D + 8, 28, gap=1, max_w=D + 80)

    # SIDE panels 35/30/35
    H_top = int(CH * 0.35)
    H_mid = int(CH * 0.30)
    H_bot = CH - H_top - H_mid
    sx = Tw + 8
    # top scores
    text(base, "玩家状态 · 积分", (sx, 12), 16, GOLD, True)
    paste(base, scale_w(load(f"icons/icon_score_{THEME}.png"), 22), (sx + 150, 10))
    rows = [
        ("S0 本家", "+1200", "万"),
        ("S1 AI", "-400", "筒"),
        ("S2 AI", "+100", "条"),
        ("S3 AI", "-900", "万"),
    ]
    yy = 48
    for name, sc, dq in rows:
        text(base, f"{name}  定缺{dq}  {sc}", (sx, yy), 13, TEXT)
        yy += 28
    text(base, "第 1/4 局 · 东风", (sx, yy + 8), 12, MUTED)

    # mid settings
    text(base, "设置开关", (sx, H_top + 10), 15, GOLD, True)
    paste(base, scale_w(load(f"icons/icon_settings_{THEME}.png"), 20), (sx + 100, H_top + 8))
    toggles = ["推理 HUD  [开]", "策略 HUD  [开]", "显示弃牌  [开]", "显示副露  [开]", "S0–S3 明牌"]
    yy = H_top + 42
    for t in toggles:
        d.rounded_rectangle((sx, yy, Tw + Sw - 12, yy + 24), radius=4, fill=(30, 60, 45), outline=BORDER)
        text(base, t, (sx + 8, yy + 4), 12, TEXT)
        yy += 30

    # bottom log
    text(base, "出牌日志", (sx, H_top + H_mid + 10), 15, GOLD, True)
    logs = [
        "S0 打 三万",
        "S1 碰 三万",
        "S1 打 五筒",
        "S2 过",
        "S3 打 二条",
        "S0 摸 · 打 九万",
    ]
    yy = H_top + H_mid + 40
    for line in logs:
        text(base, line, (sx, yy), 12, MUTED)
        yy += 22

    # title bar
    d.rectangle((0, 0, CW, 28), fill=(8, 20, 14, 220))
    text(base, "主窗口 MAIN · assets 翠玉青云 · 80%牌局 | 20%侧栏", (10, 6), 13, GOLD, True)

    out = OUT / "MAIN_mockup_assets_green.jpg"
    OUT.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out, "JPEG", quality=92)
    print("wrote", out, base.size)
    return out


def gen_human() -> Path:
    base = make_base_bg()
    overlay = Image.new("RGBA", (CW, CH), (0, 15, 8, 50))
    base = Image.alpha_composite(base, overlay)
    d = ImageDraw.Draw(base)

    Ow = int(CW * 0.67)
    Ew = CW - Ow
    # dim right panel base
    ext = Image.new("RGBA", (Ew, CH), (10, 28, 18, 240))
    base.alpha_composite(ext, (Ow, 0))
    d.line([(Ow, 0), (Ow, CH)], fill=BORDER, width=3)

    H_ROW = 36
    H_info = H_ROW
    H_set = 2 * H_ROW
    rest = CH - H_info - H_set - 8
    H_status = int(rest * 0.20 / 0.80)
    H_play = rest - H_status

    # INFO
    d.rectangle((0, 0, Ow, H_info), fill=BAR)
    text(base, "S0  人类操作  定缺:万  │  扩展 ‹", (12, 8), 15, GOLD, True)
    paste(base, scale_w(load(f"icons/icon_settings_{THEME}.png"), 22), (Ow - 40, 6))

    # STATUS
    y = H_info
    d.rectangle((0, y, Ow // 2 - 1, y + H_status), fill=(20, 45, 30))
    d.rectangle((Ow // 2, y, Ow - 1, y + H_status), fill=(22, 40, 35))
    # left discard focus
    big = scale_w(tile("wan", 5), 72)
    paste(base, big, (24, y + 20))
    text(base, "当前打出", (110, y + 18), 13, MUTED)
    text(base, "S1 打出  五万", (110, y + 42), 16, TEXT, True)
    paste(base, scale_w(load(f"icons/icon_remain_{THEME}.png"), 20), (110, y + 72))
    text(base, "牌墙剩余 68", (136, y + 74), 14, MUTED)
    # right score
    text(base, "局数  第 1 / 4 局", (Ow // 2 + 20, y + 28), 15, TEXT, True)
    paste(base, scale_w(load(f"icons/icon_score_{THEME}.png"), 22), (Ow // 2 + 20, y + 60))
    text(base, "本家得分  +1200", (Ow // 2 + 48, y + 62), 15, GOLD)

    # PLAY melds + hand + actions
    y = H_info + H_status
    H_meld = int(H_play * 0.32)
    H_hand = H_play - H_meld
    d.rectangle((0, y, Ow - 1, y + H_meld - 1), fill=(16, 38, 28))
    text(base, "副露", (12, y + 6), 13, GOLD)
    # pong of tong 2
    melds = [tile("tong", 2), tile("tong", 2), tile("tong", 2)]
    row_tiles(base, melds, 60, y + 28, 40, gap=2)

    y2 = y + H_meld
    d.rectangle((0, y2, Ow - 1, y2 + H_hand - 1), fill=(14, 36, 26))
    text(base, "手牌", (12, y2 + 4), 13, GOLD)
    # recommend badge on one tile
    hands = sample_hand(13)
    row_tiles(base, hands, 20, y2 + 28, 48, gap=2, max_w=Ow - 40)
    # action buttons
    btn_h = 48
    by = y2 + H_hand - btn_h - 8
    for i, key in enumerate(["pong", "gang_ming", "hu", "pass"]):
        btn = scale_h(load(f"buttons/btn_{key}_{THEME}.png"), btn_h)
        paste(base, btn, (20 + i * (btn.width + 12), by))

    # SETTINGS 2 rows
    y3 = H_info + H_status + H_play
    d.rectangle((0, y3, Ow - 1, CH - 1), fill=(12, 28, 22))
    text(base, "自动开始 [关]    对手牌预测 [开]", (16, y3 + 10), 14, TEXT)
    text(base, "出牌推荐 [开]    推荐标记 [开]", (16, y3 + 10 + H_ROW), 14, TEXT)

    # EXT top HUD 30% bottom disc 70%
    H_hud = int(CH * 0.30)
    d.rectangle((Ow, 0, CW - 1, H_hud - 1), fill=(18, 30, 24))
    text(base, "对手状态 HUD", (Ow + 12, 10), 15, GOLD, True)
    paste(base, scale_w(load(f"inference/tenpai_active_{THEME}.png"), 28), (Ow + 160, 6))
    hud_lines = [
        "S1  定缺筒  手13  副露1  -400",
        "S2  定缺条  手13  副露0  +100  听?",
        "S3  定缺万  手10  副露2  -900",
    ]
    yy = 48
    for line in hud_lines:
        text(base, line, (Ow + 12, yy), 13, TEXT)
        yy += 32

    d.rectangle((Ow, H_hud, CW - 1, CH - 1), fill=(14, 32, 22))
    text(base, "本家弃牌", (Ow + 12, H_hud + 8), 15, GOLD, True)
    discs = sample_discards(14)
    # grid
    tw = 36
    x0, y0 = Ow + 12, H_hud + 40
    cx, cy = x0, y0
    for i, t in enumerate(discs):
        s = scale_w(t, tw)
        if cx + s.width > CW - 8:
            cx = x0
            cy += s.height + 4
        paste(base, s, (cx, cy))
        cx += s.width + 3

    d.rectangle((0, 0, CW, 26), fill=(8, 18, 12))
    text(base, "人类窗口 play · assets green · OP67% | EXT33% 可折叠", (10, 5), 12, GOLD, True)

    out = OUT / "HUMAN_mockup_assets_green.jpg"
    base.convert("RGB").save(out, "JPEG", quality=92)
    print("wrote", out, base.size)
    return out


def gen_ai() -> Path:
    base = make_base_bg()
    overlay = Image.new("RGBA", (CW, CH), (0, 15, 8, 50))
    base = Image.alpha_composite(base, overlay)
    d = ImageDraw.Draw(base)

    Ow = int(CW * 0.67)
    Ew = CW - Ow
    ext = Image.new("RGBA", (Ew, CH), (10, 28, 18, 240))
    base.alpha_composite(ext, (Ow, 0))
    d.line([(Ow, 0), (Ow, CH)], fill=BORDER, width=3)

    H_ROW = 36
    H_info = H_ROW
    H_set = 2 * H_ROW
    rest = CH - H_info - H_set - 8
    H_status = int(rest * 0.20 / 0.80)
    H_play = rest - H_status

    d.rectangle((0, 0, Ow, H_info), fill=BAR)
    text(base, "S2  AI观战  rule_ai  定缺:条  │  只读  │  扩展 ‹", (12, 8), 14, GOLD, True)
    paste(base, scale_w(load(f"players/avatar_2_{THEME}.png"), 24), (Ow - 36, 5))

    y = H_info
    d.rectangle((0, y, Ow // 2 - 1, y + H_status), fill=(20, 45, 30))
    d.rectangle((Ow // 2, y, Ow - 1, y + H_status), fill=(22, 40, 35))
    big = scale_w(tile("tiao", 3), 72)
    paste(base, big, (24, y + 20))
    text(base, "当前打出", (110, y + 18), 13, MUTED)
    text(base, "S0 打出  三条", (110, y + 42), 16, TEXT, True)
    paste(base, scale_w(load(f"icons/icon_remain_{THEME}.png"), 20), (110, y + 72))
    text(base, "牌墙剩余 65", (136, y + 74), 14, MUTED)
    text(base, "局数  第 1 / 4 局", (Ow // 2 + 20, y + 28), 15, TEXT, True)
    paste(base, scale_w(load(f"icons/icon_score_{THEME}.png"), 22), (Ow // 2 + 20, y + 60))
    text(base, "本座得分  +100", (Ow // 2 + 48, y + 62), 15, GOLD)

    y = H_info + H_status
    H_meld = int(H_play * 0.32)
    H_hand = H_play - H_meld
    d.rectangle((0, y, Ow - 1, y + H_meld - 1), fill=(16, 38, 28))
    text(base, "副露（只读）", (12, y + 6), 13, GOLD)
    melds = [tile("wan", 8), tile("wan", 8), tile("wan", 8)]
    row_tiles(base, melds, 100, y + 30, 40, gap=2)

    y2 = y + H_meld
    d.rectangle((0, y2, Ow - 1, y2 + H_hand - 1), fill=(14, 36, 26))
    text(base, "手牌（只读 · 无操作条）", (12, y2 + 6), 13, GOLD)
    hands = sample_hand(13)
    row_tiles(base, hands, 20, y2 + 40, 50, gap=2, max_w=Ow - 40)
    # no buttons — empty bottom note
    text(base, "观战模式：不可点选 / 无碰杠胡过", (20, y2 + H_hand - 28), 12, MUTED)

    y3 = H_info + H_status + H_play
    d.rectangle((0, y3, Ow - 1, CH - 1), fill=(12, 28, 22))
    text(base, "自动开始 [开]    对手牌预测 [关]", (16, y3 + 10), 14, TEXT)
    text(base, "出牌推荐 [—]    AI策略: 当前S2 (下局生效)", (16, y3 + 10 + H_ROW), 14, TEXT)

    # EXT log 30% disc 70%
    H_log = int(CH * 0.30)
    d.rectangle((Ow, 0, CW - 1, H_log - 1), fill=(18, 28, 40))
    text(base, "AI 操作日志", (Ow + 12, 10), 15, GOLD, True)
    logs = [
        "摸 八万",
        "打 三条",
        "过（S0 出五万）",
        "碰 八万",
        "打 二筒",
        "定缺: 条",
    ]
    yy = 42
    for line in logs:
        text(base, f"· {line}", (Ow + 14, yy), 13, MUTED)
        yy += 26

    d.rectangle((Ow, H_log, CW - 1, CH - 1), fill=(14, 32, 22))
    text(base, "本家弃牌", (Ow + 12, H_log + 8), 15, GOLD, True)
    discs = sample_discards(12)
    tw = 36
    x0, y0 = Ow + 12, H_log + 40
    cx, cy = x0, y0
    for t in discs:
        s = scale_w(t, tw)
        if cx + s.width > CW - 8:
            cx = x0
            cy += s.height + 4
        paste(base, s, (cx, cy))
        cx += s.width + 3

    d.rectangle((0, 0, CW, 26), fill=(8, 18, 12))
    text(base, "AI窗口 watch · assets green · OP67% | EXT33% · 无操作条", (10, 5), 12, GOLD, True)

    out = OUT / "AI_mockup_assets_green.jpg"
    base.convert("RGB").save(out, "JPEG", quality=92)
    print("wrote", out, base.size)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    gen_main()
    gen_human()
    gen_ai()
    print("done", OUT)


if __name__ == "__main__":
    main()
