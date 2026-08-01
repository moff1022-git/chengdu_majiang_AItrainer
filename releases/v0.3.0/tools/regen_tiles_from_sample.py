#!/usr/bin/env python3
"""Rebuild wan/tong/tiao tile faces from assets/tiles/sample.jpg onto clean templates.

Templates:
  assets/tiles/tile_clean_green.png
  assets/tiles/tile_clean_blue.png

Output (54 files, 270x378 RGBA):
  assets/tiles/{wan,tong,tiao}/tile_{suit}_{1-9}_{green|blue}.png

Usage (repo root):
  .venv/bin/python tools/regen_tiles_from_sample.py
"""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent / "assets" / "tiles"
SAMPLE = ROOT / "sample.jpg"
TEMPLATES = {
    "green": ROOT / "tile_clean_green.png",
    "blue": ROOT / "tile_clean_blue.png",
}
TARGET_W, TARGET_H = 270, 378

SEEDS: dict[tuple[str, int], tuple[int, int]] = {
    ("tong", 1): (94, 80),
    ("tong", 2): (94, 139),
    ("tong", 3): (94, 199),
    ("tong", 4): (94, 258),
    ("tong", 5): (94, 318),
    ("tong", 6): (172, 80),
    ("tong", 7): (172, 139),
    ("tong", 8): (172, 199),
    # keep same row cy as tong 6-8 (172); avoid higher boxes that include stray top lines
    ("tong", 9): (172, 258),
    ("tiao_s", 1): (260, 80),
    ("tiao_s", 2): (260, 139),
    ("tiao_s", 3): (260, 199),
    ("tiao_s", 4): (260, 260),
    ("tiao_s", 5): (260, 321),
    ("tiao_s", 6): (344, 79),
    ("tiao_s", 7): (344, 139),
    ("tiao_s", 8): (344, 200),
    ("tiao_s", 9): (344, 260),
    ("wan", 1): (518, 78),
    ("wan", 2): (518, 138),
    ("wan", 3): (518, 197),
    ("wan", 4): (518, 256),
    ("wan", 5): (518, 316),
    ("wan", 6): (597, 78),
    ("wan", 7): (597, 138),
    ("wan", 8): (597, 197),
    ("wan", 9): (597, 256),
}

# sample sheet 条 order is 2..9 then bird(1)
TIAO_POS_TO_RANK = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 1}


def detect_auto_boxes(gray: np.ndarray) -> list[tuple[int, int, int, int]]:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    boxes: list[tuple[int, int, int, int]] = []
    _, bw = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    bw2 = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel, iterations=2)
    for mode in (cv2.RETR_TREE, cv2.RETR_LIST, cv2.RETR_EXTERNAL):
        for c in cv2.findContours(bw2, mode, cv2.CHAIN_APPROX_SIMPLE)[0]:
            x, y, bw_, bh = cv2.boundingRect(c)
            if 45 <= bw_ <= 72 and 60 <= bh <= 95 and 1.1 <= bh / max(bw_, 1) <= 1.85:
                boxes.append((y, x, y + bh, x + bw_))
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    for thr in ((30, 100), (50, 150), (20, 80)):
        edges = cv2.dilate(cv2.Canny(blur, thr[0], thr[1]), kernel, iterations=1)
        for c in cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
            x, y, bw_, bh = cv2.boundingRect(c)
            if 48 <= bw_ <= 72 and 65 <= bh <= 95 and 1.1 <= bh / max(bw_, 1) <= 1.85:
                boxes.append((y, x, y + bh, x + bw_))
    boxes = sorted(boxes, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]), reverse=True)
    kept: list[tuple[int, int, int, int]] = []
    for b in boxes:
        y0, x0, y1, x1 = b
        a1 = (y1 - y0) * (x1 - x0)
        ok = True
        for k in kept:
            iy0, ix0 = max(y0, k[0]), max(x0, k[1])
            iy1, ix1 = min(y1, k[2]), min(x1, k[3])
            inter = max(0, iy1 - iy0) * max(0, ix1 - ix0)
            a2 = (k[2] - k[0]) * (k[3] - k[1])
            if inter / max(min(a1, a2), 1) > 0.35:
                ok = False
                break
        if ok:
            kept.append(b)
    return kept


def score_rect(gray: np.ndarray, y0: int, x0: int, bh: int, bw: int) -> float:
    h, w = gray.shape
    y1, x1 = y0 + bh, x0 + bw
    if y0 < 1 or x0 < 1 or y1 >= h - 1 or x1 >= w - 1:
        return -1e9
    t = float(gray[y0 : y0 + 2, x0:x1].mean())
    b = float(gray[y1 - 2 : y1, x0:x1].mean())
    l = float(gray[y0:y1, x0 : x0 + 2].mean())
    r = float(gray[y0:y1, x1 - 2 : x1].mean())
    interior = float(gray[y0 + 6 : y1 - 6, x0 + 6 : x1 - 6].mean())
    border = (t + b + l + r) / 4.0
    side_var = float(np.var([t, b, l, r]))
    return interior - border * 1.2 - side_var * 0.05


def refine_box(gray: np.ndarray, cy: int, cx: int) -> tuple[int, int, int, int]:
    best_s = -1e9
    best = (cy - 36, cx - 27, cy + 36, cx + 27)
    for bh in range(70, 82):
        for bw in range(52, 62):
            for dy in range(-14, 15, 2):
                for dx in range(-14, 15, 2):
                    y0 = cy - bh // 2 + dy
                    x0 = cx - bw // 2 + dx
                    s = score_rect(gray, y0, x0, bh, bw)
                    if s > best_s:
                        best_s = s
                        best = (y0, x0, y0 + bh, x0 + bw)
    return best


def nearest(cy: int, cx: int, boxes: list, maxdist: float = 50.0):
    best = None
    bestd = 1e9
    for b in boxes:
        bcy = (b[0] + b[2]) / 2
        bcx = (b[1] + b[3]) / 2
        d = ((bcy - cy) ** 2 + (bcx - cx) ** 2) ** 0.5
        if d < bestd:
            bestd = d
            best = b
    if bestd <= maxdist:
        return best
    return None


def _snap_row_boxes(
    boxes: dict[int, tuple[int, int, int, int]], ranks: range
) -> dict[int, tuple[int, int, int, int]]:
    """Force a horizontal row of tiles to share the same y0/y1 (median of peers)."""
    rows = [boxes[r] for r in ranks if r in boxes]
    if len(rows) < 2:
        return boxes
    y0s = sorted(b[0] for b in rows)
    y1s = sorted(b[2] for b in rows)
    # median
    mid = len(rows) // 2
    y0m = y0s[mid]
    y1m = y1s[mid]
    # prefer the mode of heights ~72 from majority
    heights = sorted(b[2] - b[0] for b in rows)
    h_m = heights[mid]
    if y1m - y0m != h_m:
        y1m = y0m + h_m
    out = dict(boxes)
    for r in ranks:
        if r not in out:
            continue
        y0, x0, y1, x1 = out[r]
        # keep width; if outlier height or y, snap
        if abs((y0 + y1) / 2 - (y0m + y1m) / 2) > 4 or abs((y1 - y0) - h_m) > 4:
            out[r] = (y0m, x0, y1m, x1)
        else:
            out[r] = (y0m, x0, y1m, x1)
    return out


def localize_all(gray: np.ndarray) -> dict[tuple[str, int], tuple[int, int, int, int]]:
    auto = detect_auto_boxes(gray)
    raw: dict[tuple, tuple] = {}
    for key, (cy, cx) in SEEDS.items():
        b = nearest(cy, cx, auto, 45)
        if b is None or (b[2] - b[0]) < 70:
            b = refine_box(gray, cy, cx)
        raw[key] = b

    # --- wan second row (6-9): prefer peers 6/8/9; never allow wan7 vertical drift ---
    wan_row2: dict[int, tuple[int, int, int, int]] = {}
    for r in range(6, 10):
        cy, cx = SEEDS[("wan", r)]
        cand = [
            b
            for b in auto
            if 555 <= (b[0] + b[2]) / 2 <= 630
            and abs((b[1] + b[3]) / 2 - cx) < 32
            and 50 <= (b[3] - b[1]) <= 62
            and 68 <= (b[2] - b[0]) <= 78
        ]
        if cand:
            wan_row2[r] = min(cand, key=lambda b: abs((b[1] + b[3]) / 2 - cx))
        else:
            wan_row2[r] = raw[("wan", r)]
    # Use y from median of ranks that look consistent (prefer 6,8,9 over outlier 7)
    peers = [wan_row2[r] for r in (6, 8, 9) if r in wan_row2]
    if peers:
        y0m = int(np.median([b[0] for b in peers]))
        y1m = int(np.median([b[2] for b in peers]))
        # expected x centers from seeds / spacing
        for r in range(6, 10):
            cy, cx = SEEDS[("wan", r)]
            y0, x0, y1, x1 = wan_row2[r]
            # if this box's vertical center drifted > 6px from row, rebuild from seed x + row y
            if abs((y0 + y1) / 2 - (y0m + y1m) / 2) > 6:
                bw = int(np.median([b[3] - b[1] for b in peers]))
                x0n = int(round(cx - bw / 2))
                wan_row2[r] = (y0m, x0n, y1m, x0n + bw)
            else:
                wan_row2[r] = (y0m, x0, y1m, x1)
    wan_row2 = _snap_row_boxes(wan_row2, range(6, 10))
    for r, b in wan_row2.items():
        raw[("wan", r)] = b

    # Snap wan first row 1-5
    wan_row1 = {r: raw[("wan", r)] for r in range(1, 6)}
    wan_row1 = _snap_row_boxes(wan_row1, range(1, 6))
    for r, b in wan_row1.items():
        raw[("wan", r)] = b

    # Snap tong second row (6-9) to shared vertical band — fixes tong9 top-line leak
    tong_row2 = {r: raw[("tong", r)] for r in range(6, 10)}
    # Prefer auto boxes on y~172 band for tong 6-9
    for r in range(6, 10):
        cy, cx = SEEDS[("tong", r)]
        cand = [
            b
            for b in auto
            if 150 <= (b[0] + b[2]) / 2 <= 195
            and abs((b[1] + b[3]) / 2 - cx) < 35
            and 50 <= (b[3] - b[1]) <= 62
            and 68 <= (b[2] - b[0]) <= 78
        ]
        if cand:
            tong_row2[r] = min(cand, key=lambda b: abs((b[1] + b[3]) / 2 - cx))
    tong_row2 = _snap_row_boxes(tong_row2, range(6, 10))
    for r, b in tong_row2.items():
        raw[("tong", r)] = b

    # Snap tong first row 1-5 similarly
    tong_row1 = {r: raw[("tong", r)] for r in range(1, 6)}
    tong_row1 = _snap_row_boxes(tong_row1, range(1, 6))
    for r, b in tong_row1.items():
        raw[("tong", r)] = b

    out: dict[tuple[str, int], tuple[int, int, int, int]] = {}
    for r in range(1, 10):
        out[("tong", r)] = raw[("tong", r)]
        out[("wan", r)] = raw[("wan", r)]
        out[("tiao", TIAO_POS_TO_RANK[r])] = raw[("tiao_s", r)]
    return out


def _strip_frame_lines(alpha: np.ndarray, lum: np.ndarray, sat: np.ndarray) -> np.ndarray:
    """Remove thin gray/black frame remnants (esp. top/bottom borders) from ink mask.

    Never strip chromatic ink (color numbers/symbols) — only low-sat gray frames.
    """
    h, w = alpha.shape
    out = alpha.copy()
    # Rows that look like horizontal border: dark, low sat, span most of width
    for y in range(h):
        row_a = out[y] > 20
        if not row_a.any():
            continue
        row_lum = lum[y]
        row_sat = sat[y]
        # strict low-sat only — blue/red/green strokes have sat >> 0.12
        dark_gray = (row_lum < 190) & (row_sat < 0.12) & row_a
        if not dark_gray.any():
            continue
        # near-full-width thin line
        if dark_gray.mean() > 0.50 and float(row_sat[row_a].mean()) < 0.12:
            near_edge = y < h * 0.12 or y > h * 0.88
            if near_edge:
                out[y, dark_gray] = 0
                continue
            prev_ink = float((out[max(0, y - 2) : y] > 20).mean()) if y > 0 else 0
            next_ink = float((out[y + 1 : min(h, y + 3)] > 20).mean()) if y + 1 < h else 0
            if prev_ink < 0.12 and next_ink < 0.12:
                out[y, dark_gray] = 0
    # Only clear outermost 1px (sample frame bleed) — 2px ate wan digits
    out[:1, :] = 0
    out[-1:, :] = 0
    out[:, :1] = 0
    out[:, -1:] = 0
    return out


def extract_ink_rgba(bgr: np.ndarray) -> Image.Image:
    h, w = bgr.shape[:2]
    # Slightly larger inset to drop sample tile frame
    m = max(3, int(round(min(h, w) * 0.13)))
    core = bgr[m : h - m, m : w - m]
    if core.size == 0:
        return Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    rgb = cv2.cvtColor(core, cv2.COLOR_BGR2RGB).astype(np.float32)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = (mx - mn) / np.maximum(mx, 1.0)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    is_bg = ((lum > 238) & (sat < 0.14)) | (mn > 248)
    # Prefer chromatic ink; pure gray dark only if not a full-width border
    is_ink = (~is_bg) & ((sat > 0.08) | ((lum < 200) & (sat > 0.04)))
    alpha = np.zeros_like(lum, dtype=np.float32)
    alpha[is_ink] = 255.0
    near = cv2.dilate(is_ink.astype(np.uint8), np.ones((3, 3), np.uint8), 1).astype(bool)
    fringe = near & (~is_ink) & (~is_bg)
    strength = np.clip((235 - lum) / 90.0, 0, 1) * 0.65 + np.clip(sat / 0.35, 0, 1) * 0.35
    alpha[fringe] = strength[fringe] * 210.0
    alpha = _strip_frame_lines(alpha, lum, sat)

    rgba = np.dstack([r, g, b, alpha])
    ys, xs = np.where(alpha > 12)
    if len(ys) == 0:
        return Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    y0, y1 = max(0, int(ys.min()) - 1), min(rgba.shape[0], int(ys.max()) + 2)
    x0, x1 = max(0, int(xs.min()) - 1), min(rgba.shape[1], int(xs.max()) + 2)
    return Image.fromarray(np.clip(rgba[y0:y1, x0:x1], 0, 255).astype(np.uint8), "RGBA")


def face_rect(template: Image.Image) -> tuple[int, int, int, int]:
    a = np.array(template)
    alpha = (a[:, :, 3] > 128).astype(np.uint8)
    er = cv2.erode(alpha, np.ones((17, 17), np.uint8), iterations=2)
    ys, xs = np.where(er > 0)
    if len(ys) == 0:
        w, h = template.size
        return 26, 30, w - 26, h - 30
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def composite_tile(
    template: Image.Image,
    pattern: Image.Image,
    *,
    target_scale: float | None = None,
) -> Image.Image:
    """Place pattern on face. If target_scale set, use it for consistent size within a suit."""
    out = template.copy().convert("RGBA")
    fx0, fy0, fx1, fy1 = face_rect(template)
    fw, fh = fx1 - fx0, fy1 - fy0
    max_w, max_h = int(fw * 0.80), int(fh * 0.80)
    pw, ph = pattern.size
    if pw < 1 or ph < 1:
        return out
    if target_scale is not None:
        scale = float(target_scale)
        # still clamp to face
        scale = min(scale, max_w / pw, max_h / ph)
    else:
        scale = min(max_w / pw, max_h / ph)
    nw, nh = max(1, int(round(pw * scale))), max(1, int(round(ph * scale)))
    pat = pattern.resize((nw, nh), Image.Resampling.LANCZOS)
    arr = np.array(pat).astype(np.float32)
    rgb = arr[:, :, :3]
    mean = rgb.mean(axis=2, keepdims=True)
    rgb = np.clip(mean + (rgb - mean) * 1.06, 0, 255)
    rgb = np.clip(rgb * 0.96, 0, 255)
    pat = Image.fromarray(np.dstack([rgb, arr[:, :, 3]]).astype(np.uint8), "RGBA")
    x = fx0 + (fw - nw) // 2
    y = fy0 + (fh - nh) // 2
    out.alpha_composite(pat, dest=(x, y))
    return out


def _suit_target_scales(
    patterns: dict[tuple[str, int], Image.Image],
    template: Image.Image,
) -> dict[str, float]:
    """
    Per-suit common scale so ranks share similar visual size.
    Uses median of fit-to-face scales within each suit.
    """
    fx0, fy0, fx1, fy1 = face_rect(template)
    fw, fh = fx1 - fx0, fy1 - fy0
    max_w, max_h = int(fw * 0.80), int(fh * 0.80)
    by_suit: dict[str, list[float]] = {"wan": [], "tong": [], "tiao": []}
    for (suit, _rank), pat in patterns.items():
        pw, ph = pat.size
        if pw < 1 or ph < 1:
            continue
        by_suit[suit].append(min(max_w / pw, max_h / ph))
    out: dict[str, float] = {}
    for suit, scales in by_suit.items():
        if not scales:
            continue
        scales_s = sorted(scales)
        out[suit] = float(scales_s[len(scales_s) // 2])
    return out


def main() -> None:
    bgr = cv2.imread(str(SAMPLE))
    if bgr is None:
        raise SystemExit(f"cannot read {SAMPLE}")
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    mapping = localize_all(gray)

    dbg = bgr.copy()
    for (suit, rank), (y0, x0, y1, x1) in mapping.items():
        cv2.rectangle(dbg, (x0, y0), (x1, y1), (0, 0, 255), 2)
        cv2.putText(
            dbg,
            f"{suit[0]}{rank}",
            (x0, max(12, y0 - 2)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 0, 255),
            1,
        )
    cv2.imwrite(str(ROOT / "_sample_mapped.png"), dbg)
    for r in range(6, 10):
        print(f"tong{r} box", mapping[("tong", r)])
    for r in range(6, 10):
        print(f"wan{r} box", mapping[("wan", r)])

    templates = {th: Image.open(p).convert("RGBA") for th, p in TEMPLATES.items()}

    # Extract patterns once
    patterns: dict[tuple[str, int], Image.Image] = {}
    for (suit, rank), (y0, x0, y1, x1) in sorted(mapping.items()):
        patterns[(suit, rank)] = extract_ink_rgba(bgr[y0:y1, x0:x1])

    # Consistent scale per suit (use green template face metrics)
    suit_scale = _suit_target_scales(patterns, templates["green"])
    print("suit scales", {k: round(v, 3) for k, v in suit_scale.items()})
    for r in range(1, 10):
        p = patterns[("tong", r)]
        print(f"  tong{r} pattern {p.size}")

    n = 0
    for (suit, rank), pattern in sorted(patterns.items()):
        for theme, tmpl in templates.items():
            tile = composite_tile(
                tmpl, pattern, target_scale=suit_scale.get(suit)
            )
            assert tile.size == (TARGET_W, TARGET_H)
            path = ROOT / suit / f"tile_{suit}_{rank}_{theme}.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            tile.save(path, "PNG")
            n += 1
    print(f"wrote {n} files under {ROOT}")

    for theme in ("green", "blue"):
        collage = Image.new("RGBA", (9 * 92, 3 * 130), (36, 40, 44, 255))
        for si, suit in enumerate(("wan", "tong", "tiao")):
            for rank in range(1, 10):
                p = ROOT / suit / f"tile_{suit}_{rank}_{theme}.png"
                im = Image.open(p).convert("RGBA").resize((86, 120), Image.Resampling.LANCZOS)
                collage.paste(im, ((rank - 1) * 92 + 3, si * 130 + 5), im)
        path = ROOT / f"_tiles_regen_preview_{theme}.png"
        collage.save(path)
        print("preview", path)


if __name__ == "__main__":
    main()
