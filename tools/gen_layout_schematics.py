#!/usr/bin/env python3
"""Generate layout schematics for UI_DESIGN_STANDARD v1.3.

- Layout canvas = 85% of work area (exact image size)
- Layouts A / B / C (landscape only)
- Tiers: 720p, 1080p, 2160p
- Unified style; each window labeled with px size
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "design" / "layout_schematics"

BG = (40, 44, 50)
GRID = (52, 56, 64)
TEXT = (236, 239, 244)
TEXT_DIM = (160, 168, 180)
FRAME = (90, 96, 108)

ROLE = {
    "AI": {
        "fill": (36, 58, 72),
        "border": (64, 168, 192),
        "title": (120, 210, 230),
        "bar": (24, 40, 50),
    },
    "MAIN": {
        "fill": (42, 52, 40),
        "border": (120, 180, 100),
        "title": (170, 220, 140),
        "bar": (30, 40, 28),
    },
    "HUMAN": {
        "fill": (58, 48, 36),
        "border": (220, 170, 80),
        "title": (255, 210, 120),
        "bar": (48, 38, 26),
    },
}

# tier: work, canvas, MAIN, AI
TIERS = {
    "720p": {
        "work": (1280, 720),
        "canvas": (1180, 664),
        "main": (590, 332),
        "ai": (295, 166),
    },
    "1080p": {
        "work": (1920, 1080),
        "canvas": (1770, 996),
        "main": (885, 498),
        "ai": (442, 249),
    },
    "2160p": {
        "work": (3840, 2160),
        "canvas": (3540, 1991),
        "main": (1770, 995),
        "ai": (885, 497),
    },
}


def fonts(scale: float = 1.0):
    def sz(n: int) -> int:
        return max(10, int(round(n * scale)))

    try:
        return (
            ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", sz(18)),
            ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", sz(16)),
            ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", sz(13)),
            ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", sz(11)),
        )
    except Exception:
        f = ImageFont.load_default()
        return f, f, f, f


def text_size(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0], b[3] - b[1]


def draw_win(draw, x, y, w, h, role, label, fonts_t):
    _tf, body_f, small_f, tiny_f = fonts_t
    if w < 4 or h < 4:
        return
    st = ROLE[role]
    draw.rectangle((x, y, x + w - 1, y + h - 1), fill=st["fill"], outline=st["border"], width=3)
    th = min(max(18, h // 8), max(22, int(h * 0.12)))
    th = min(th, h - 4)
    draw.rectangle((x + 1, y + 1, x + w - 2, y + th), fill=st["bar"])
    draw.text((x + 8, y + max(2, th // 5)), label, font=small_f, fill=st["title"])
    size_label = f"{w}×{h}"
    tw, tht = text_size(draw, size_label, body_f)
    cx = x + max(0, (w - tw) // 2)
    cy = y + th + max(0, (h - th - tht) // 2)
    draw.text((cx, cy), size_label, font=body_f, fill=TEXT)
    tw2, _ = text_size(draw, size_label, tiny_f)
    draw.text((x + w - tw2 - 6, y + h - 16), size_label, font=tiny_f, fill=TEXT_DIM)


def place_ai_row(ox, oy, Lw, n, Wa, Ha, Hm):
    """Return list of (x,y,w,h) for n AIs across upper half, evenly spaced."""
    band_y = oy + max(0, (Hm - Ha) // 2)
    total_w = n * Wa
    gap_free = Lw - total_w
    g_ai = max(0, gap_free // (n + 1))
    margin_x = (gap_free - (n - 1) * g_ai) // 2
    out = []
    for i in range(n):
        x = ox + margin_x + i * (Wa + g_ai)
        out.append((x, band_y, Wa, Ha))
    return out


def place_ai_top_left(ox, oy, Wm, Hm, n, Wa, Ha):
    """n AIs in top-left Wm×Hm box, horizontal even."""
    box_w, box_h = Wm, Hm
    total_w = n * Wa
    gap_free = max(0, box_w - total_w)
    g_ai = max(0, gap_free // (n + 1))
    margin_x = (gap_free - (n - 1) * g_ai) // 2
    band_y = oy + max(0, (box_h - Ha) // 2)
    out = []
    for i in range(n):
        x = ox + margin_x + i * (Wa + g_ai)
        out.append((x, band_y, Wa, Ha))
    return out


def render(tier: str, layout: str) -> Path:
    t = TIERS[tier]
    Lw, Lh = t["canvas"]
    Wm, Hm = t["main"]
    Wa, Ha = t["ai"]
    Wm2 = Lw - Wm
    # font scale with canvas
    scale = Lw / 1770.0
    ft = fonts(scale)

    im = Image.new("RGB", (Lw, Lh), BG)
    d = ImageDraw.Draw(im)
    step = max(40, Lw // 40)
    for gx in range(0, Lw, step):
        d.line([(gx, 0), (gx, Lh - 1)], fill=GRID, width=1)
    for gy in range(0, Lh, step):
        d.line([(0, gy), (Lw - 1, gy)], fill=GRID, width=1)
    d.rectangle((0, 0, Lw - 1, Lh - 1), outline=FRAME, width=2)

    mode_name = {
        "A": "3AI+1人类",
        "B": "2AI+2人类",
        "C": "4AI+0人类",
    }[layout]
    title = f"布局{layout} · {mode_name} · 完整 · {tier} · 画布{Lw}×{Lh}"

    # MAIN always bottom-left
    main_xy = (0, Lh - Hm, Wm, Hm)
    draw_win(d, *main_xy, "MAIN", "MAIN · Full", ft)

    if layout == "A":
        # human bottom-right
        draw_win(d, Wm, Lh - Hm, Wm2, Hm, "HUMAN", "人类1 · Full", ft)
        for i, box in enumerate(place_ai_row(0, 0, Lw, 3, Wa, Ha, Hm)):
            seats = ("S3", "S2", "S1")
            draw_win(d, *box, "AI", f"AI {seats[i]} · Full", ft)
    elif layout == "B":
        draw_win(d, Wm, Lh - Hm, Wm2, Hm, "HUMAN", "人类1 · Full", ft)
        draw_win(d, Wm, 0, Wm2, Hm, "HUMAN", "人类2 · Full", ft)
        for i, box in enumerate(place_ai_top_left(0, 0, Wm, Hm, 2, Wa, Ha)):
            draw_win(d, *box, "AI", f"AI · Full", ft)
    elif layout == "C":
        for i, box in enumerate(place_ai_row(0, 0, Lw, 4, Wa, Ha, Hm)):
            draw_win(d, *box, "AI", f"AI{i} · Full", ft)
        # empty BR — light label
        _tf, body_f, small_f, tiny_f = ft
        d.text(
            (Wm + 12, Lh - Hm + 12),
            "（右下空 · 无人类）",
            font=small_f,
            fill=TEXT_DIM,
        )

    # footer
    foot_h = max(22, int(24 * scale))
    d.rectangle((0, Lh - foot_h, Lw - 1, Lh - 1), fill=(28, 30, 34))
    _, _, _, tiny_f = ft
    d.text((8, Lh - foot_h + 4), title, font=tiny_f, fill=TEXT)
    meta = f"MAIN/人类 {Wm}×{Hm} · AI {Wa}×{Ha} · 85%画布 · 统一样式"
    mw, _ = text_size(d, meta, tiny_f)
    d.text((Lw - mw - 8, Lh - foot_h + 4), meta, font=tiny_f, fill=TEXT_DIM)

    OUT.mkdir(parents=True, exist_ok=True)
    name = f"{layout}_{tier}_full.jpg"
    path = OUT / name
    im.save(path, "JPEG", quality=92, optimize=True)
    print(f"wrote {name} {im.size[0]}x{im.size[1]}")
    return path


def main():
    if OUT.exists():
        for p in list(OUT.glob("*.jpg")) + list(OUT.glob("*.png")):
            p.unlink()
            print("deleted", p.name)
        # remove subdirs leftovers
        for sub in OUT.iterdir():
            if sub.is_dir():
                for p in sub.glob("*"):
                    p.unlink()
                sub.rmdir()

    for tier in ("720p", "1080p", "2160p"):
        for layout in ("A", "B", "C"):
            render(tier, layout)

    # verify sizes
    for tier, conf in TIERS.items():
        cw, ch = conf["canvas"]
        for layout in ("A", "B", "C"):
            path = OUT / f"{layout}_{tier}_full.jpg"
            im = Image.open(path)
            assert im.size == (cw, ch), (path.name, im.size, (cw, ch))
    print("OK", OUT, "9 images")


if __name__ == "__main__":
    main()
