"""
Per-seat window subprocess (tkinter — multi-process safe on Windows).

Pygame multi-display in many processes frequently drops S1/S3 under Windows.
Tkinter creates independent native windows reliably.

Modes:
  play  — human interactive (NDJSON decision)
  watch — AI / spectator seat (observation only)

  python -m players.seat_window --seat 0 --mode play --theme green
"""

from __future__ import annotations

import argparse
import os
import sys
import threading
import time
import traceback
from collections import deque
from pathlib import Path
from typing import Any

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Shared stdin queue
_line_queue: deque[str] = deque()
_reader_started = False
_queue_lock = threading.Lock()


def _crash_log(seat: int, mode: str, text: str) -> Path:
    try:
        from app_paths import logs_dir

        log_dir = logs_dir()
    except Exception:
        log_dir = Path(_ROOT) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / f"seat_{mode}_{seat}_crash.log"
    try:
        path.write_text(text, encoding="utf-8", errors="replace")
    except Exception:
        pass
    return path


def _start_stdin_reader() -> None:
    global _reader_started
    if _reader_started:
        return
    _reader_started = True

    def _bg() -> None:
        try:
            for line in sys.stdin:
                with _queue_lock:
                    _line_queue.append(line)
        except Exception:
            pass

    threading.Thread(target=_bg, daemon=True, name="seat-stdin").start()


def _drain_stdin_lines(max_lines: int = 64) -> list[str]:
    _start_stdin_reader()
    out: list[str] = []
    with _queue_lock:
        while _line_queue and len(out) < max_lines:
            out.append(_line_queue.popleft())
    return out


def _safe_emit(obj: dict) -> None:
    """
    Write one NDJSON line to the parent. On Windows, text-mode stdout pipes
    often raise OSError 22 on flush — use binary buffer instead.
    """
    from protocols.wire import encode_line

    line = encode_line(obj)
    data = line.encode("utf-8") if isinstance(line, str) else line
    try:
        buf = getattr(sys.stdout, "buffer", None)
        if buf is not None:
            buf.write(data)
            buf.flush()
            return
        sys.stdout.write(line if isinstance(line, str) else data.decode("utf-8"))
        sys.stdout.flush()
    except Exception as e1:
        # Last resort: raw fileno write (survives broken TextIOWrapper)
        try:
            fd = sys.stdout.fileno()
            os.write(fd, data if data.endswith(b"\n") else data + b"\n")
            return
        except Exception as e2:
            try:
                sys.stderr.write(f"[seat_window] emit failed: {e1} / {e2}\n")
                sys.stderr.flush()
            except Exception:
                pass


def _tile_png(theme: str, tid: str) -> Path | None:
    try:
        suit, rank_s = str(tid).split("_", 1)
        rank = int(rank_s)
    except Exception:
        return None
    p = (
        Path(_ROOT)
        / "assets"
        / "tiles"
        / suit
        / f"tile_{suit}_{rank}_{theme}.png"
    )
    return p if p.is_file() else None


def _label_tile(tid: str) -> str:
    """Short Chinese-ish label for text fallback."""
    try:
        suit, rank_s = str(tid).split("_", 1)
        mp = {"wan": "万", "tong": "筒", "tiao": "条"}
        return f"{rank_s}{mp.get(suit, suit)}"
    except Exception:
        return str(tid)[-4:]


def _dingque_label(raw: Any) -> str:
    """Public dingque suit → 万/筒/条."""
    if raw is None or raw == "" or raw == "None":
        return "未定缺"
    s = str(raw).lower()
    return {"wan": "万", "tong": "筒", "tiao": "条"}.get(s, s)


def _dingque_color(raw: Any) -> str:
    s = str(raw or "").lower()
    return {
        "wan": "#ff8a80",  # 万 — 红
        "tong": "#82b1ff",  # 筒 — 蓝
        "tiao": "#69f0ae",  # 条 — 绿
    }.get(s, "#cfd8dc")


def _status_hud_label(p: dict) -> tuple[str, str]:
    """Return (text, fg) for player status in opponent HUD."""
    st = str(p.get("status") or "active")
    if st == "finished":
        order = p.get("hu_order")
        order_s = f"第{order}家" if order is not None else "已胡"
        zimo = ""
        lw = p.get("last_win") or {}
        if isinstance(lw, dict):
            if lw.get("zimo"):
                zimo = "·自摸"
            elif lw.get("loser") is not None:
                zimo = f"·点炮S{lw.get('loser')}"
        return (f"★ 已胡 {order_s}{zimo}", "#ffd54f")
    if st == "active":
        return ("行牌中", "#b2ff59")
    return (st, "#eeeeee")


# Engine meld kinds → Chinese UI labels (副露类型提示)
_MELD_KIND_ZH: dict[str, str] = {
    "pong": "碰",
    "peng": "碰",
    "chow": "吃",
    "chi": "吃",
    "ming_gang": "明杠",
    "an_gang": "暗杠",
    "jia_gang": "加杠",
    "gang": "杠",
    "gang_ming": "明杠",
    "gang_an": "暗杠",
    "gang_jia": "加杠",
}


def meld_kind_label(kind: Any) -> str:
    """Map engine meld kind (pong/ming_gang/…) to Chinese display text."""
    k = str(kind or "").strip().lower()
    if not k:
        return "副露"
    if k in _MELD_KIND_ZH:
        return _MELD_KIND_ZH[k]
    if "jia" in k and "gang" in k:
        return "加杠"
    if "an" in k and "gang" in k:
        return "暗杠"
    if "ming" in k and "gang" in k:
        return "明杠"
    if "gang" in k:
        return "杠"
    if "pong" in k or "peng" in k:
        return "碰"
    if "chow" in k or "chi" in k:
        return "吃"
    return str(kind)


def selected_tile_tw(base_tw: int) -> int:
    """Selected hand tile width — same as base (border/color only; no enlarge).

    Enlarging selected tiles reflows the hand row and causes visible flicker.
    Highlight is done via bg/border in ``_apply_hand_selection_styles``.
    """
    base = max(12, int(base_tw))
    return max(12, base // 2 * 2)


def format_discard_actor(discard_seat: Any, self_seat: int) -> str:
    """Who played the current discard — for seat window focus panel."""
    if discard_seat is None or discard_seat == "" or discard_seat == "None":
        return "暂无出牌"
    try:
        ds = int(discard_seat)
    except (TypeError, ValueError):
        return "暂无出牌"
    if ds == int(self_seat):
        return f"本座 S{ds} 打出"
    return f"S{ds} 打出"


def remain_of_tile_from_view(
    view: dict | None,
    self_seat: int,
    tile_id: str | None,
    *,
    total: int = 4,
) -> int | None:
    """
    Estimate remaining copies of ``tile_id`` from a seat observation view.

    Counts: own hand + all public discard piles + all melds (3/4).
    Same privacy model as ``players.analysis.remain.remain_map``.
    Returns None if tile_id missing.
    """
    if tile_id is None or tile_id == "" or tile_id == "None":
        return None
    tid = str(tile_id)
    visible = 0
    for p in (view or {}).get("players") or []:
        if not isinstance(p, dict):
            continue
        try:
            ps = int(p.get("seat", -1))
        except (TypeError, ValueError):
            continue
        if ps == int(self_seat):
            for h in p.get("hand") or []:
                if str(h) == tid:
                    visible += 1
        for d in p.get("discard_pile") or []:
            if str(d) == tid:
                visible += 1
        for m in p.get("melds") or []:
            if not isinstance(m, dict):
                continue
            if str(m.get("tile_id") or "") != tid:
                continue
            kind = str(m.get("kind") or "").lower()
            visible += 4 if "gang" in kind else 3
    return max(0, int(total) - visible)


def format_remain_badge(remain: int | None) -> str:
    """Digit-only badge for tile corner (此牌剩余)."""
    if remain is None:
        return ""
    return str(max(0, int(remain)))


def format_discard_headline(
    discard_seat: Any,
    self_seat: int,
    tile_id: str | None = None,
) -> str:
    """One-line: actor + tile face, e.g. 'S2 打出 5万' / '暂无出牌'."""
    who = format_discard_actor(discard_seat, self_seat)
    if tile_id is None or tile_id == "" or tile_id == "None":
        return who
    if who == "暂无出牌":
        return who
    return f"{who} {_label_tile(str(tile_id))}"


def format_wall_remaining_line(wall_remaining: Any) -> str:
    """Current hand wall stock — e.g. '牌墙总剩余 48 张'."""
    if wall_remaining is None or wall_remaining == "" or wall_remaining == "—":
        return "牌墙总剩余 —"
    try:
        n = int(wall_remaining)
    except (TypeError, ValueError):
        return f"牌墙总剩余 {wall_remaining}"
    return f"牌墙总剩余 {max(0, n)} 张"


def format_round_line(round_index: int, num_rounds: int | None = None) -> str:
    """e.g. '当前局数: 第 2/4 局'."""
    r = max(1, int(round_index or 1))
    if num_rounds is None or int(num_rounds) <= 0:
        return f"当前局数: 第 {r} 局"
    n = max(1, int(num_rounds))
    return f"当前局数: 第 {r}/{n} 局"


def format_scoreboard_line(
    players: list | None,
    *,
    self_seat: int,
    multiline: bool = False,
) -> str:
    """
    Compact all-seat scores, e.g.
    '得分情况: ★S0:+12 S1:-3 …'  or multiline for side panel.
    """
    rows: list[tuple[int, int]] = []
    for p in players or []:
        if not isinstance(p, dict):
            continue
        try:
            s = int(p.get("seat", -1))
            sc = int(p.get("score", 0) or 0)
        except (TypeError, ValueError):
            continue
        if s < 0:
            continue
        rows.append((s, sc))
    rows.sort(key=lambda x: x[0])
    if not rows:
        return "得分情况:\n（暂无）" if multiline else "得分情况: （暂无）"
    parts: list[str] = []
    for s, sc in rows:
        mark = "★" if s == int(self_seat) else " "
        sign = f"{sc:+d}" if sc != 0 else "0"
        parts.append(f"{mark}S{s}:{sign}")
    if multiline:
        return "得分情况:\n" + "\n".join(parts)
    return "得分情况:  " + "  ".join(parts)


def _pick_tk_cjk_family(tkfont: Any) -> str:
    """Pick an installed Tk font family that can show Simplified Chinese.

    Windows: avoid ``tkfont.families()`` (can block seat subprocess startup).
    macOS / others: keep original families() scan (do not change mac behavior).
    """
    # --- Windows-only fast path ---
    if sys.platform == "win32":
        for name in ("Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "SimSun"):
            try:
                f = tkfont.Font(family=name, size=11)
                _ = f.metrics("linespace")
                return name
            except Exception:
                continue
        return "Segoe UI"

    # --- macOS / Linux: original enumeration path (unchanged) ---
    preferred = (
        "PingFang SC",
        "Hiragino Sans GB",
        "Heiti SC",
        "STHeiti",
        "Songti SC",
        "Arial Unicode MS",
        "Noto Sans CJK SC",
        "Noto Sans SC",
        "Microsoft YaHei UI",
        "Microsoft YaHei",
        "SimHei",
        "SimSun",
        "WenQuanYi Micro Hei",
    )
    try:
        available = set(tkfont.families())
    except Exception:
        available = set()
    for name in preferred:
        if name in available:
            return name
    try:
        return str(tkfont.nametofont("TkDefaultFont").cget("family"))
    except Exception:
        return "Helvetica"


class TkSeatApp:
    def __init__(
        self,
        *,
        seat: int,
        mode: str,
        theme: str,
        title: str,
        x: int,
        y: int,
        w: int,
        h: int,
    ) -> None:
        import tkinter as tk
        from tkinter import font as tkfont

        self.seat = seat
        self.mode = mode
        self.theme = theme
        self.tk = tk
        self.root = tk.Tk()
        self.root.title(title)
        from display.window_geometry import format_tk_geometry

        x, y = int(x), int(y)
        from display.interior_scale import (
            AI_REF_H,
            AI_REF_W,
            HUMAN_REF_H,
            HUMAN_REF_W,
            seat_scale,
        )

        # Complete-mode size: plan size capped ≤1080p full; min=max (do not enlarge)
        from display.window_geometry import clamp_outer_size

        kind = "human" if mode == "play" else "ai"
        w, h = clamp_outer_size(int(w), int(h), kind=kind)
        # Same client size as MAIN (plan outer → client); keep in sync with pygame
        from display.window_geometry import plan_to_matched_client_size

        w, h = plan_to_matched_client_size(w, h)
        # Windows only: snap obviously off-screen coords. macOS allows negative Y.
        if sys.platform == "win32":
            if y < -50:
                y = 40
            if x < -4000:
                x = 40
        self._geom_x = x
        self._geom_y = y
        self.root.geometry(format_tk_geometry(w, h, x, y))
        try:
            self.root.deiconify()
            self.root.lift()
            self.root.update_idletasks()
        except Exception:
            pass
        # Full mode: lock client size (min=max); prevent content-driven growth
        self.root.minsize(w, h)
        try:
            self.root.maxsize(w, h)
        except Exception:
            pass
        try:
            # Avoid OS/content stretching the frame beyond plan (height match MAIN)
            self.root.resizable(False, False)
        except Exception:
            pass
        self._full_locked_wh = (w, h)
        # Re-assert size after first map (Tk may ignore first geometry on macOS)
        try:
            self.root.after(100, lambda: self._reassert_locked_size())
        except Exception:
            pass
        self.root.configure(bg="#143528")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._photo_cache: dict[str, Any] = {}
        self._ui_family = _pick_tk_cjk_family(tkfont)
        ui_family = self._ui_family
        sc0 = seat_scale(w, h, mode=mode)
        self._seat_scale = sc0
        self._font = tkfont.Font(family=ui_family, size=sc0.font)
        self._font_lg = tkfont.Font(family=ui_family, size=sc0.font_lg, weight="bold")

        # F0016/F0017: body = OP 67% | EXT 33%; zones placed by _apply_interior_geometry
        self.ext_expanded = True
        self.view_mode = "full"  # full | compact (F0014)
        self._full_geom_wh: tuple[int, int] = (int(w), int(h))
        self.body_fr = tk.Frame(self.root, bg="#143528")
        self.body_fr.pack(fill="both", expand=True)
        self.body_fr.pack_propagate(False)
        self.op_col = tk.Frame(self.body_fr, bg="#143528")
        self.ext_col = tk.Frame(
            self.body_fr,
            bg="#0f1f18",
            highlightthickness=1,
            highlightbackground="#3a6a50",
        )
        # OP vertical zones (place; not free-flow pack)
        self.op_info_fr = tk.Frame(self.op_col, bg="#0a1914")
        self.op_status_fr = tk.Frame(self.op_col, bg="#143528")
        self.op_play_fr = tk.Frame(self.op_col, bg="#143528")
        self.op_settings_fr = tk.Frame(self.op_col, bg="#0d2818")
        self.play_hand_fr = tk.Frame(self.op_play_fr, bg="#143528")
        self.play_actions_fr = tk.Frame(self.op_play_fr, bg="#0c1c16")

        # Header + fold EXT + full/compact (OP_INFO)
        self.hdr_row = tk.Frame(self.op_info_fr, bg="#0a1914")
        self.hdr_row.pack(fill="x")
        self.hdr = tk.Label(
            self.hdr_row,
            text=f"座位 S{seat}  [{'人类操作' if mode == 'play' else 'AI 观战'}]",
            bg="#0a1914",
            fg="#fffff0",
            font=self._font_lg,
            anchor="w",
            padx=10,
            pady=4,
        )
        self.hdr.pack(side="left", fill="x", expand=True)
        # 完整 | 精简 切换 (F0014)
        self.mode_full_btn = tk.Label(
            self.hdr_row,
            text="完整",
            bg="#c9a227",
            fg="#1a1200",
            font=self._font,
            padx=8,
            pady=4,
            cursor="hand2",
        )
        self.mode_full_btn.pack(side="right", padx=(2, 4), pady=4)
        self.mode_full_btn.bind("<Button-1>", lambda _e: self._set_view_mode("full"))
        self.mode_compact_btn = tk.Label(
            self.hdr_row,
            text="精简",
            bg="#2a4034",
            fg="#c8e6c8",
            font=self._font,
            padx=8,
            pady=4,
            cursor="hand2",
        )
        self.mode_compact_btn.pack(side="right", padx=2, pady=4)
        self.mode_compact_btn.bind(
            "<Button-1>", lambda _e: self._set_view_mode("compact")
        )
        self.ext_toggle_btn = tk.Label(
            self.hdr_row,
            text="扩展 ‹",
            bg="#1b5e40",
            fg="#ffffff",
            font=self._font,
            padx=8,
            pady=4,
            cursor="hand2",
        )
        self.ext_toggle_btn.pack(side="right", padx=4, pady=4)
        self.ext_toggle_btn.bind("<Button-1>", lambda _e: self._toggle_ext_panel())
        self.settings_btn = tk.Label(
            self.hdr_row,
            text="设置 ▾",
            bg="#2e7d4f",
            fg="#ffffff",
            font=self._font,
            padx=10,
            pady=4,
            cursor="hand2",
        )
        self.settings_btn.pack(side="right", padx=4, pady=4)
        self.settings_btn.bind("<Button-1>", lambda _e: self._toggle_settings())

        self.status = tk.Label(
            self.op_info_fr,
            text="连接中 — 等待主程序…",
            bg="#0a1914",
            fg="#ffe08c",
            font=self._font,
            anchor="w",
            padx=10,
        )
        self.status.pack(fill="x")

        # 本座已胡横幅：挂在 op_info_fr（始终可见），勿 pack(before=meta_row)
        # — meta_row 在 op_status_fr，父级不同会导致 pack 静默失败。
        self.hu_banner = tk.Label(
            self.op_info_fr,
            text="",
            bg="#b71c1c",
            fg="#fff59d",
            font=self._font_lg,
            anchor="center",
            justify="center",
            padx=8,
            pady=8,
            wraplength=420,
        )
        self._hu_banner_packed = False

        # OP_SETTINGS — always bottom of OP (below action bar)
        self.settings_bar = tk.Frame(
            self.op_settings_fr,
            bg="#0d2818",
            highlightthickness=1,
            highlightbackground="#66bb6a",
        )
        self.settings_bar.pack(fill="both", expand=True, padx=2, pady=2)

        # Collapsible detailed settings panel (overlays above settings when open)
        self.settings_fr = tk.Frame(
            self.op_col,
            bg="#12261c",
            highlightthickness=1,
            highlightbackground="#4db6ac",
        )
        self._settings_open = False
        self.ai_type = "rule_ai" if mode != "play" else "human"
        self.ai_type_var = tk.StringVar(value=self.ai_type)
        # F0010 opponent hand prediction (default off)
        self.predict_opponents_enabled = False
        self._predict_fp: str | None = None
        self._predict_forecasts: list = []
        self._predict_joints: list = []  # JointHandScene cache for v2 continuity
        # F0012 discard recommendation marks (play mode; default on)
        self.recommend_marks_enabled = True
        self._recommendations: list = []  # from hints
        self._hand_cell_by_tid: dict = {}  # hand_index -> cell meta
        self._ukeire_overlay_key: tuple | None = None  # anti-flicker cache

        # Banner (status only; interactive controls live in action bar)
        self.ready_banner = tk.Label(
            self.op_info_fr,
            text="",
            bg="#1a4028",
            fg="#fff0a0",
            font=self._font_lg,
            anchor="w",
            padx=12,
            pady=4,
        )
        # not packed until ready

        # Action bar: bottom of OP_PLAY (above OP_SETTINGS) — design §3.4.2
        self.btn_fr = tk.Frame(self.play_actions_fr, bg="#0c1c16")
        self.btn_fr.pack(fill="both", expand=True)

        # OP_PLAY hand zone:
        # - mid_wrap: upper area (副露等)，不占手牌底栏
        # - hand_fr: 固定贴底（place）
        # - ukeire_bar: 半透明风格浮动层（place，不占流式高度）
        self.mid_wrap = tk.Frame(self.play_hand_fr, bg="#143528")
        # geometry via _layout_play_hand_zone
        self.mid_canvas = tk.Canvas(
            self.mid_wrap,
            bg="#143528",
            highlightthickness=0,
            bd=0,
        )
        # No permanent scrollbar gutter (user); wheel-scroll still works if content overflows
        self.mid_scroll = None
        self.mid_canvas.pack(side="left", fill="both", expand=True)

        self.mid = tk.Frame(self.mid_canvas, bg="#143528")
        self._mid_win = self.mid_canvas.create_window(
            (0, 0), window=self.mid, anchor="nw", tags="mid"
        )
        self.mid.bind("<Configure>", self._on_mid_content_configure)
        self.mid_canvas.bind("<Configure>", self._on_mid_canvas_configure)
        self.mid_canvas.bind("<Enter>", self._bind_mousewheel)
        self.mid_canvas.bind("<Leave>", self._unbind_mousewheel)
        self.mid.bind("<Enter>", self._bind_mousewheel)
        self.mid.bind("<Leave>", self._unbind_mousewheel)

        # F0010: opponent hand prediction (packed only when enabled)
        self.predict_fr = tk.Frame(
            self.mid,
            bg="#0a1f16",
            highlightthickness=1,
            highlightbackground="#26a69a",
        )
        self._predict_packed = False

        # OP_STATUS: STATUS_L 50% | STATUS_R 50% (place in _layout_status_halves)
        self.meta_row = tk.Frame(self.op_status_fr, bg="#143528")
        # filled via place in geometry pass

        # STATUS_L — 当前打出
        self.play_panel = tk.Frame(
            self.meta_row,
            bg="#1a2818",
            highlightthickness=1,
            highlightbackground="#ffc107",
        )
        self.play_title_lbl = tk.Label(
            self.play_panel,
            text="当前打出",
            bg="#1a2818",
            fg="#ffe082",
            font=self._font,
            anchor="w",
            padx=4,
            pady=0,
        )
        # title placed top-left; tile box is 95% of status height (see geometry)
        self.play_body = tk.Frame(self.play_panel, bg="#1a2818")
        # Tile host: fixed aspect box (h = 0.95 * status_h, w = h/1.4)
        self.play_tile_host = tk.Frame(
            self.play_body,
            bg="#0d1a12",
            highlightthickness=2,
            highlightbackground="#ffc107",
            bd=0,
        )
        self.play_tile_host.pack_propagate(False)
        self.play_tile_lbl = tk.Label(
            self.play_tile_host,
            text="—",
            bg="#0d1a12",
            fg="#90a4ae",
            font=self._font,
            bd=0,
        )
        self.play_tile_lbl.place(relx=0.5, rely=0.5, anchor="center")
        self._font_badge = tkfont.Font(
            family=ui_family, size=9, weight="bold"
        )
        self.play_remain_badge = tk.Label(
            self.play_tile_host,
            text="",
            bg="#b71c1c",
            fg="#ffffff",
            font=self._font_badge,
            padx=2,
            pady=0,
            bd=0,
        )
        self.play_info = tk.Frame(self.play_body, bg="#1a2818")
        self.play_who_lbl = tk.Label(
            self.play_info,
            text="暂无出牌",
            bg="#1a2818",
            fg="#fff8e1",
            font=self._font,
            anchor="w",
            justify="left",
        )
        self.play_who_lbl.pack(fill="x", anchor="w")
        self.play_wall_lbl = tk.Label(
            self.play_info,
            text=format_wall_remaining_line(None),
            bg="#1a2818",
            fg="#a5d6a7",
            font=self._font,
            anchor="w",
            justify="left",
        )
        self.play_wall_lbl.pack(fill="x", anchor="w", pady=(2, 0))
        self._play_tile_photo = None

        # STATUS_R — 局数 / 得分
        self.score_side = tk.Frame(
            self.meta_row,
            bg="#0f241c",
            highlightthickness=1,
            highlightbackground="#4db6ac",
        )
        self.round_lbl = tk.Label(
            self.score_side,
            text=format_round_line(1, 1),
            bg="#0f241c",
            fg="#80deea",
            font=self._font,
            anchor="w",
            padx=6,
            pady=2,
            wraplength=160,
            justify="left",
        )
        self.round_lbl.pack(fill="x")
        self.scoreboard_lbl = tk.Label(
            self.score_side,
            text="得分情况:\n（等待开局）",
            bg="#0f241c",
            fg="#ffe082",
            font=self._font,
            anchor="nw",
            padx=6,
            pady=2,
            wraplength=160,
            justify="left",
        )
        self.scoreboard_lbl.pack(fill="both", expand=True)
        self.score_lbl = tk.Label(
            self.score_side,
            text="本家: —",
            bg="#143528",
            fg="#ffdc64",
            font=self._font,
            anchor="w",
            padx=8,
            pady=4,
            wraplength=180,
            justify="left",
        )
        self.score_lbl.pack(fill="x", side="bottom")
        self._play_fp: tuple[Any, ...] | None = None
        self._play_badge_placed = False

        # OP_PLAY: melds in scroll mid; hand fixed at bottom of play_hand_fr
        self.meld_fr = tk.Frame(self.mid, bg="#143528")
        self.meld_fr.pack(fill="x", pady=2)
        # F0012: floating ukeire = Toplevel 50% alpha, sits just above hand row
        self.ukeire_bar = tk.Toplevel(self.root)
        self.ukeire_bar.withdraw()
        try:
            self.ukeire_bar.overrideredirect(True)
        except Exception:
            pass
        try:
            self.ukeire_bar.attributes("-alpha", 0.5)
        except Exception:
            try:
                self.ukeire_bar.attributes("-alpha", 0.50)
            except Exception:
                pass
        try:
            self.ukeire_bar.configure(bg="#1a4028")
        except Exception:
            pass
        self.ukeire_bar_title = tk.Label(
            self.ukeire_bar,
            text="可听进张",
            bg="#1a4028",
            fg="#c5e1a5",
            font=self._font,
            anchor="w",
            padx=6,
            pady=1,
        )
        self.ukeire_bar_title.pack(fill="x")
        self.ukeire_bar_body = tk.Frame(self.ukeire_bar, bg="#1a4028")
        self.ukeire_bar_body.pack(fill="both", expand=True, padx=4, pady=(0, 4))
        self.ukeire_bar_hint = tk.Label(
            self.ukeire_bar_body,
            text="选中听牌推荐后显示进张",
            bg="#1a4028",
            fg="#9ccc9c",
            font=self._font,
            anchor="w",
        )
        self.ukeire_bar_hint.pack(anchor="w")
        self._ukeire_float_visible = False
        # Hand fixed at bottom of real-time hand zone (not mid scroll content)
        self.hand_fr = tk.Frame(self.play_hand_fr, bg="#143528")
        self._hand_band_y = 0  # relative y of hand band in play_hand_fr

        # EXT column: top = opp HUD (play) or AI log (watch); bot = discards
        # Geometry via place in _apply_interior_geometry (30% / 70%)
        self.ext_top = tk.Frame(self.ext_col, bg="#0f241c")
        self.ext_bot = tk.Frame(self.ext_col, bg="#143528")

        if mode == "play":
            self.opp_hud_title = tk.Label(
                self.ext_top,
                text="对手状态 HUD",
                bg="#0f241c",
                fg="#c8e6c8",
                font=self._font,
                anchor="w",
                padx=6,
            )
            self.opp_hud_title.pack(fill="x", pady=(4, 0))
            self.opp_fr = tk.Frame(
                self.ext_top,
                bg="#0f241c",
                highlightthickness=1,
                highlightbackground="#3a6a50",
            )
            self.opp_fr.pack(fill="both", expand=True, pady=(0, 4), padx=2)
            self.ai_log_fr = None
            self.ai_log_list = None
        else:
            self.opp_hud_title = tk.Label(
                self.ext_top,
                text="AI 操作日志",
                bg="#0f241c",
                fg="#c8e6c8",
                font=self._font,
                anchor="w",
                padx=6,
            )
            self.opp_hud_title.pack(fill="x", pady=(4, 0))
            self.ai_log_fr = tk.Frame(self.ext_top, bg="#0a1812")
            self.ai_log_fr.pack(fill="both", expand=True, padx=2, pady=2)
            self.ai_log_list = tk.Listbox(
                self.ai_log_fr,
                bg="#0a1812",
                fg="#c8e6c8",
                font=self._font,
                highlightthickness=0,
                bd=0,
                activestyle="none",
            )
            self.ai_log_list.pack(fill="both", expand=True)
            # still create opp_fr (hidden) so dirty-update paths don't crash
            self.opp_fr = tk.Frame(self.ext_top, bg="#0f241c")
            self._ai_log_lines: list[str] = []
            self._ai_log_fp: Any = None

        self.disc_title = tk.Label(
            self.ext_bot,
            text="本家弃牌",
            bg="#143528",
            fg="#a5d6a7",
            font=self._font,
            anchor="w",
            padx=6,
        )
        self.disc_title.pack(fill="x")
        self.disc_fr = tk.Frame(self.ext_bot, bg="#143528")
        self.disc_fr.pack(fill="both", expand=True, pady=2, padx=2)

        # Initial strict place layout (67/33, 25/55, actions above settings)
        try:
            self._apply_interior_geometry()
        except Exception:
            pass

        # Selection by **hand index** (not tile_id) so duplicate tiles can be picked separately
        self.selected: list[int] = []
        self.hand_ids: list[str] = []
        self.last_obs = None
        self.pending_req = None
        self.pending_hints = None
        self.legal: list = []
        self.phase = "wait"
        self.status_note = "连接中 — 等待主程序…"
        self.awaiting_ready = False
        self._ready_sent = False
        self.ready_round = 1
        self.num_rounds = 1
        self.running = True
        # All seats (human + AI watch) default to **manual** confirm (F0004).
        # User may still tick「自动开始」per window for later rounds.
        self.auto_start = False
        self._banner_packed = False
        self._last_tile_click_tid: str | None = None
        self._last_tile_click_idx: int | None = None
        self._last_tile_click_t = 0.0
        self._hand_widgets: list = []
        self._hand_tile_widgets: list[tuple] = []  # (tid, widget, base_tw, hand_index)
        self.auto_var = tk.BooleanVar(value=bool(self.auto_start))
        self._build_settings_bar()
        self._build_settings_panel()
        # F0006 responsive layout
        self._last_layout_wh: tuple[int, int] = (0, 0)
        self._resize_after_id: Any = None
        # Anti-flicker: skip full rebuild when tiles/layout unchanged
        self._last_tiles_fp: Any = None
        self._last_opp_struct_fp: Any = None
        self._last_opp_values_fp: Any = None
        self._last_sel_fp: Any = None
        self._last_action_fp: Any = None
        self._last_layout_cw: int = 0
        self._cached_content_w: int = 0
        self._opp_cell_labels: list[dict] = []  # in-place opp HUD label refs
        self._render_after_id: Any = None
        self._render_pending_force: bool = False
        self._first_layout_done: bool = False
        # F0013 dirty-update pools (hand / discard faces)
        self._hand_layout_key: Any = None
        self._disc_layout_key: Any = None
        self._last_meld_key: Any = None
        self._disc_tile_widgets: list = []  # Label faces in discard strip

        self.root.bind("<Configure>", self._on_configure)
        self.root.update_idletasks()
        # User may freely move/resize after initial place (Windows parent used to
        # re-pin aggressively and break drag/focus).
        self._user_geometry_free = False
        self._geom_pin_until = time.time() + 2.5  # allow startup pin briefly
        try:
            from display.window_geometry import format_tk_geometry

            self.root.resizable(True, True)
            self.root.geometry(format_tk_geometry(w, h, x, y))
            self.root.lift()
            # Brief topmost only on Windows spawn; always clear.
            if sys.platform == "win32":
                try:
                    self.root.attributes("-topmost", True)
                except Exception:
                    pass
                self.root.after(250, self._win32_unlock_window_chrome)
            else:
                try:
                    self.root.attributes("-topmost", True)
                    self.root.after(
                        200, lambda: self.root.attributes("-topmost", False)
                    )
                except Exception:
                    pass
            # Correct multi-monitor Y drift (e.g. off by one main-screen height)
            self.root.after(50, self._correct_geometry_drift)
        except Exception:
            pass

        self.root.bind("<Return>", self._on_ready_key)
        self.root.bind("<KP_Enter>", self._on_ready_key)
        self.root.bind("<space>", self._on_ready_key)

        self.root.after(30, self._poll)

    def _win32_unlock_window_chrome(self) -> None:
        """Windows: ensure seat window can be moved, focused, and resized."""
        if sys.platform != "win32":
            return
        try:
            self.root.attributes("-topmost", False)
        except Exception:
            pass
        try:
            self.root.resizable(True, True)
        except Exception:
            pass
        try:
            self.root.grab_release()
        except Exception:
            pass
        try:
            # Re-enable HWND if a bad SetWindowPos left it disabled
            import ctypes

            hwnd = int(self.root.winfo_id())
            # winfo_id is the frame child on some Tk builds; walk to toplevel
            user32 = ctypes.windll.user32  # type: ignore[attr-defined]
            GW_OWNER = 4
            root_hwnd = user32.GetParent(hwnd) or hwnd
            # Climb to top-level
            cur = hwnd
            for _ in range(6):
                parent = user32.GetParent(cur)
                if not parent:
                    break
                cur = parent
            user32.EnableWindow(int(cur), True)
            # Clear TOPMOST bit if stuck
            GWL_EXSTYLE = -20
            WS_EX_TOPMOST = 0x00000008
            try:
                style = user32.GetWindowLongW(int(cur), GWL_EXSTYLE)
                if style & WS_EX_TOPMOST:
                    HWND_NOTOPMOST = -2
                    SWP_NOMOVE = 0x0002
                    SWP_NOSIZE = 0x0001
                    SWP_NOACTIVATE = 0x0010
                    user32.SetWindowPos(
                        int(cur),
                        HWND_NOTOPMOST,
                        0,
                        0,
                        0,
                        0,
                        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE,
                    )
            except Exception:
                pass
        except Exception:
            pass

    def _wire_click(self, widget, callback) -> None:
        """Wire button callback once (command preferred; mouse release as backup)."""
        lock = {"busy": False}

        def _cb(_event=None):
            if lock["busy"]:
                return "break"
            lock["busy"] = True
            try:
                callback()
            except Exception as e:
                try:
                    sys.stderr.write(f"[seat_window] click handler err: {e}\n")
                    sys.stderr.flush()
                except Exception:
                    pass
            finally:
                # allow next click shortly after
                try:
                    self.root.after(150, lambda: lock.__setitem__("busy", False))
                except Exception:
                    lock["busy"] = False
            return "break"

        try:
            widget.configure(command=_cb)
        except Exception:
            pass
        # Always bind release so Label-based colored buttons work (macOS Aqua
        # ignores tk.Button bg; we use Label/Frame for solid fill — F0006 fix).
        try:
            widget.bind("<ButtonRelease-1>", _cb)
        except Exception:
            pass
        for child in getattr(widget, "winfo_children", lambda: [])():
            try:
                child.bind("<ButtonRelease-1>", _cb)
            except Exception:
                pass

    def _make_colored_button(
        self,
        parent,
        text: str,
        *,
        command=None,
        bg: str = "#288250",
        fg: str = "white",
        active_bg: str | None = None,
        font=None,
        padx: int = 18,
        pady: int = 10,
        width: int | None = None,
    ):
        """
        Solid-color clickable control that shows bg on macOS and Windows.

        Native tk.Button under Aqua ignores ``bg``/``fg`` (looks like no fill).
        A Frame+Label paints the fill reliably on both platforms.
        """
        active_bg = active_bg or "#36a060"
        font = font or self._font
        outer = self.tk.Frame(
            parent,
            bg=bg,
            highlightbackground="#7dcea0",
            highlightthickness=1,
            bd=0,
            cursor="hand2",
        )
        lbl = self.tk.Label(
            outer,
            text=text,
            bg=bg,
            fg=fg,
            font=font,
            padx=padx,
            pady=pady,
            cursor="hand2",
            borderwidth=0,
        )
        if width is not None:
            lbl.configure(width=int(width))
        lbl.pack()

        def _set_color(color: str) -> None:
            try:
                outer.configure(bg=color, highlightbackground="#a8e6c0")
                lbl.configure(bg=color)
            except Exception:
                pass

        def _press(_e=None):
            _set_color(active_bg)

        def _leave(_e=None):
            _set_color(bg)

        for w in (outer, lbl):
            w.bind("<ButtonPress-1>", _press)
            w.bind("<Leave>", _leave)
            w.bind("<Enter>", lambda _e: _set_color(active_bg))

        if command is not None:
            self._wire_click(outer, command)
        # Keep label ref so GC does not drop bindings target
        outer._label = lbl  # type: ignore[attr-defined]
        return outer

    def _on_close(self) -> None:
        self.running = False
        try:
            self._hide_ukeire_float()
            self.ukeire_bar.destroy()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass

    def _reassert_locked_size(self) -> None:
        """Force client size back to locked plan (MAIN/human height match)."""
        if getattr(self, "view_mode", "full") != "full":
            return
        locked = getattr(self, "_full_locked_wh", None)
        if not locked:
            return
        ww, wh = int(locked[0]), int(locked[1])
        try:
            self.root.update_idletasks()
            cw = int(self.root.winfo_width() or 0)
            ch = int(self.root.winfo_height() or 0)
            xx = int(getattr(self, "_geom_x", self.root.winfo_x() or 0))
            yy = int(getattr(self, "_geom_y", self.root.winfo_y() or 0))
            from display.window_geometry import format_tk_geometry

            self.root.minsize(ww, wh)
            self.root.maxsize(ww, wh)
            try:
                self.root.resizable(False, False)
            except Exception:
                pass
            if cw != ww or ch != wh:
                # Tk may need a second geometry pass after widgets map
                self.root.geometry(format_tk_geometry(ww, wh, xx, yy))
                self.root.update_idletasks()
                cw2 = int(self.root.winfo_width() or 0)
                ch2 = int(self.root.winfo_height() or 0)
                # If still short, request larger geometry to win client height
                if ch2 < wh - 2:
                    boost = wh - ch2
                    self.root.geometry(
                        format_tk_geometry(ww, wh + boost, xx, yy)
                    )
                    self.root.update_idletasks()
                    self.root.geometry(format_tk_geometry(ww, wh, xx, yy))
                sys.stderr.write(
                    f"[seat_window] reassert size seat={self.seat} "
                    f"was {cw}x{ch} -> target {ww}x{wh} "
                    f"now {self.root.winfo_width()}x{self.root.winfo_height()}\n"
                )
                sys.stderr.flush()
        except Exception:
            pass

    def _apply_geometry(self, x: int, y: int, w: int, h: int) -> None:
        """Parent re-positioned this seat (layout screen change / reassert)."""
        from display.window_geometry import format_tk_geometry

        # Windows: after user has moved/resized, ignore parent re-pins so the
        # window stays movable/focusable and does not snap back.
        if sys.platform == "win32":
            if getattr(self, "_user_geometry_free", False):
                try:
                    sys.stderr.write(
                        f"[seat_window] set_geometry ignored (user moved) "
                        f"seat={self.seat}\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    pass
                return
            if time.time() > float(getattr(self, "_geom_pin_until", 0)):
                # Startup pin window elapsed — do not force again
                return

        from display.window_geometry import clamp_outer_size, plan_to_matched_client_size

        kind = "human" if self.mode == "play" else "ai"
        ww, wh = clamp_outer_size(int(w), int(h), kind=kind)
        ww, wh = plan_to_matched_client_size(ww, wh)
        xx, yy = int(x), int(y)
        # Windows only: snap off-screen plans. macOS retains signed multi-mon coords.
        if sys.platform == "win32":
            try:
                from display.window_geometry import WindowRect, clamp_rect_to_visible

                c = clamp_rect_to_visible(WindowRect(xx, yy, ww, wh))
                xx, yy, ww, wh = c.x, c.y, c.w, c.h
                ww, wh = clamp_outer_size(ww, wh, kind=kind)
            except Exception:
                if yy < -50:
                    yy = 40
        self._geom_x, self._geom_y = xx, yy
        if getattr(self, "view_mode", "full") == "full":
            self._full_locked_wh = (ww, wh)
            try:
                self.root.minsize(ww, wh)
                self.root.maxsize(ww, wh)
            except Exception:
                pass
        try:
            self.root.geometry(format_tk_geometry(ww, wh, xx, yy))
            self.root.deiconify()
            # Avoid lift() on Windows after startup — steals focus from user
            if sys.platform != "win32":
                self.root.lift()
            self.root.after(30, self._correct_geometry_drift)
            try:
                sys.stderr.write(
                    f"[seat_window] set_geometry seat={self.seat} "
                    f"{ww}x{wh}@({xx},{yy})\n"
                )
                sys.stderr.flush()
            except Exception:
                pass
        except Exception as e:
            try:
                sys.stderr.write(
                    f"[seat_window] set_geometry failed seat={self.seat}: {e}\n"
                )
                sys.stderr.flush()
            except Exception:
                pass

    def _correct_geometry_drift(self) -> None:
        """
        If the window landed ~one main-screen height away from the planned Y
        (Tk multi-monitor edge cases), shift it back once.
        """
        # Windows: do not fight the user after they move the window
        if sys.platform == "win32" and getattr(self, "_user_geometry_free", False):
            return
        from display.window_geometry import format_tk_geometry

        try:
            self.root.update_idletasks()
            planned_x = int(getattr(self, "_geom_x", 0))
            planned_y = int(getattr(self, "_geom_y", 0))
            ax = int(self.root.winfo_rootx())
            ay = int(self.root.winfo_rooty())
            # Title-bar / menu slop is usually < 80px; full-screen errors are ~900+
            dy = ay - planned_y
            dx = ax - planned_x
            sh = int(self.root.winfo_screenheight() or 1080)
            # Off by approximately one primary screen height (or virtual)
            screen_like = abs(abs(dy) - sh) < 160 or abs(abs(dy) - (sh - 28)) < 160
            big_drift = abs(dy) > 400
            if big_drift and (screen_like or abs(dy) > sh * 0.7):
                # Move planned coords so actual root matches plan (minus small chrome)
                new_y = planned_y - dy + (28 if dy > 0 else 0)
                new_x = planned_x - dx if abs(dx) > 200 else planned_x
                ww = max(320, int(self.root.winfo_width() or 400))
                wh = max(240, int(self.root.winfo_height() or 300))
                self._geom_x, self._geom_y = int(new_x), int(new_y)
                self.root.geometry(format_tk_geometry(ww, wh, new_x, new_y))
                try:
                    sys.stderr.write(
                        f"[seat_window] geometry drift fix seat={self.seat} "
                        f"dy={dy} sh={sh} -> y {planned_y} to {new_y}\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    pass
        except Exception:
            pass

    def _on_ready_key(self, _event=None):
        if self.awaiting_ready and not self._ready_sent:
            self.emit_ready(auto=False)
            return "break"

    def _on_ready_click(self) -> None:
        try:
            sys.stderr.write(
                f"[seat_window] ready_click seat={self.seat} "
                f"awaiting={self.awaiting_ready} sent={self._ready_sent} "
                f"auto_var={self.auto_var.get()}\n"
            )
            sys.stderr.flush()
        except Exception:
            pass
        self.auto_start = bool(self.auto_var.get())
        self.emit_ready(auto=False)

    def _on_auto_toggle(self) -> None:
        self.auto_start = bool(self.auto_var.get())
        try:
            sys.stderr.write(
                f"[seat_window] auto_toggle seat={self.seat} "
                f"auto={self.auto_start} awaiting={self.awaiting_ready}\n"
            )
            sys.stderr.flush()
        except Exception:
            pass
        self._emit_seat_settings()
        try:
            self._build_settings_bar()
        except Exception:
            pass
        if self.auto_start and self.awaiting_ready and not self._ready_sent:
            self.emit_ready(auto=True)

    def _build_settings_bar(self) -> None:
        """
        Always-visible compact settings: 自动开始 + AI 策略.

        macOS Aqua often ignores Checkbutton/Radiobutton colors; use high-contrast
        labels + simple toggle buttons so both features are always readable.
        """
        bar = self.settings_bar
        for c in bar.winfo_children():
            try:
                c.destroy()
            except Exception:
                pass

        self.tk.Label(
            bar,
            text="设置",
            bg="#0d2818",
            fg="#a5d6a7",
            font=self._font,
            padx=8,
            pady=4,
        ).pack(side="left")

        # --- Auto start toggle ---
        self.auto_var.set(bool(self.auto_start))
        auto_txt = "自动开始：开" if self.auto_start else "自动开始：关"
        auto_bg = "#2e7d32" if self.auto_start else "#455a64"
        self._auto_btn = self._make_colored_button(
            bar,
            auto_txt,
            command=self._toggle_auto_from_bar,
            bg=auto_bg,
            fg="white",
            active_bg="#388e3c" if self.auto_start else "#546e7a",
            font=self._font,
            padx=10,
            pady=4,
        )
        self._auto_btn.pack(side="left", padx=6, pady=4)

        # --- F0010 opponent hand predict toggle ---
        pred_on = bool(self.predict_opponents_enabled)
        pred_txt = "对手牌预测：开" if pred_on else "对手牌预测：关"
        pred_bg = "#00695c" if pred_on else "#455a64"
        self._pred_btn = self._make_colored_button(
            bar,
            pred_txt,
            command=self._toggle_predict_opponents,
            bg=pred_bg,
            fg="white",
            active_bg="#00897b" if pred_on else "#546e7a",
            font=self._font,
            padx=10,
            pady=4,
        )
        self._pred_btn.pack(side="left", padx=6, pady=4)

        # --- F0012 recommend discard marks (human play seat) ---
        if self.mode == "play":
            rec_on = bool(self.recommend_marks_enabled)
            rec_txt = "推荐标记：开" if rec_on else "推荐标记：关"
            rec_bg = "#6a1b9a" if rec_on else "#455a64"
            self._rec_btn = self._make_colored_button(
                bar,
                rec_txt,
                command=self._toggle_recommend_marks,
                bg=rec_bg,
                fg="white",
                active_bg="#8e24aa" if rec_on else "#546e7a",
                font=self._font,
                padx=10,
                pady=4,
            )
            self._rec_btn.pack(side="left", padx=6, pady=4)

        # --- AI strategy ---
        if self.mode == "play":
            self.tk.Label(
                bar,
                text="AI：人类座",
                bg="#0d2818",
                fg="#90a4ae",
                font=self._font,
                padx=8,
            ).pack(side="left")
        else:
            self.tk.Label(
                bar,
                text="AI 策略",
                bg="#0d2818",
                fg="#e0f2f1",
                font=self._font,
                padx=4,
            ).pack(side="left")
            try:
                from players.strategy_presets import list_strategy_ids, ui_choices

                choices = ui_choices()
                known = set(list_strategy_ids())
            except Exception:
                choices = [
                    ("rule_ai", "规则"),
                    ("random", "随机"),
                    ("current_s2", "当前S2"),
                ]
                known = {c[0] for c in choices}
            cur = self.ai_type if self.ai_type in known else "rule_ai"
            self.ai_type_var.set(cur)
            for key, label in choices:
                on = cur == key
                b = self._make_colored_button(
                    bar,
                    label + (" ✓" if on else ""),
                    command=lambda k=key: self._set_ai_from_bar(k),
                    bg="#1565c0" if on else "#37474f",
                    fg="white",
                    active_bg="#1976d2" if on else "#455a64",
                    font=self._font,
                    padx=8,
                    pady=4,
                )
                b.pack(side="left", padx=3, pady=4)
            self.tk.Label(
                bar,
                text="(下局生效)",
                bg="#0d2818",
                fg="#80cbc4",
                font=self._font,
            ).pack(side="left", padx=4)

        # Expand details
        more = self._make_colored_button(
            bar,
            "更多…",
            command=self._toggle_settings,
            bg="#1b5e20",
            fg="#fffde7",
            active_bg="#2e7d32",
            font=self._font,
            padx=8,
            pady=4,
        )
        more.pack(side="right", padx=6, pady=4)

    def _toggle_auto_from_bar(self) -> None:
        self.auto_start = not bool(self.auto_start)
        self.auto_var.set(self.auto_start)
        self._emit_seat_settings()
        self._build_settings_bar()
        if self._settings_open:
            self._build_settings_panel()
        if self.auto_start and self.awaiting_ready and not self._ready_sent:
            self.emit_ready(auto=True)
        self.status_note = (
            "已开启自动开始" if self.auto_start else "已关闭自动开始"
        )
        self._refresh_chrome()

    def _set_ai_from_bar(self, key: str) -> None:
        if self.mode == "play":
            return
        try:
            from players.strategy_presets import list_strategy_ids

            known = set(list_strategy_ids()) | {"rule_ai", "random"}
        except Exception:
            known = {"rule_ai", "random", "current_s2"}
        if key not in known:
            return
        self.ai_type = key
        self.ai_type_var.set(key)
        self._emit_seat_settings()
        self._build_settings_bar()
        if self._settings_open:
            self._build_settings_panel()
        self.status_note = f"AI 策略已设为 {key}（下局生效）"
        self._refresh_chrome()

    def _build_settings_panel(self) -> None:
        """Detailed settings body (packed when user opens 更多/设置)."""
        fr = self.settings_fr
        for c in fr.winfo_children():
            c.destroy()
        title = self.tk.Label(
            fr,
            text=f"座位 S{self.seat} 详细设置",
            bg="#12261c",
            fg="#b2dfdb",
            font=self._font_lg,
            anchor="w",
            padx=10,
            pady=6,
        )
        title.pack(fill="x")

        # Auto start
        row1 = self.tk.Frame(fr, bg="#12261c")
        row1.pack(fill="x", padx=10, pady=4)
        self.tk.Label(
            row1, text="自动开始", bg="#12261c", fg="#e0f2f1", font=self._font
        ).pack(side="left")
        self.auto_var.set(bool(self.auto_start))
        self._make_colored_button(
            row1,
            "开启" if self.auto_start else "关闭",
            command=self._toggle_auto_from_bar,
            bg="#2e7d32" if self.auto_start else "#546e7a",
            fg="white",
            active_bg="#388e3c",
            font=self._font,
            padx=12,
            pady=4,
        ).pack(side="left", padx=8)
        self.tk.Label(
            row1,
            text="本窗就绪时自动点确认开始",
            bg="#12261c",
            fg="#90a4ae",
            font=self._font,
        ).pack(side="left")

        # F0010 predict
        row_p = self.tk.Frame(fr, bg="#12261c")
        row_p.pack(fill="x", padx=10, pady=4)
        self.tk.Label(
            row_p, text="对手牌预测", bg="#12261c", fg="#e0f2f1", font=self._font
        ).pack(side="left")
        self._make_colored_button(
            row_p,
            "开启" if self.predict_opponents_enabled else "关闭",
            command=self._toggle_predict_opponents,
            bg="#00695c" if self.predict_opponents_enabled else "#546e7a",
            fg="white",
            active_bg="#00897b",
            font=self._font,
            padx=12,
            pady=4,
        ).pack(side="left", padx=8)
        self.tk.Label(
            row_p,
            text="Top-5 牌形+可信度；关则隐藏区域",
            bg="#12261c",
            fg="#90a4ae",
            font=self._font,
        ).pack(side="left")

        # AI strategy
        row2 = self.tk.Frame(fr, bg="#12261c")
        row2.pack(fill="x", padx=10, pady=6)
        self.tk.Label(
            row2, text="AI 策略", bg="#12261c", fg="#e0f2f1", font=self._font
        ).pack(side="left", anchor="n")
        ai_box = self.tk.Frame(row2, bg="#12261c")
        ai_box.pack(side="left", padx=10)
        if self.mode == "play":
            self.tk.Label(
                ai_box,
                text="人类操作（不可改 AI）",
                bg="#12261c",
                fg="#90a4ae",
                font=self._font,
            ).pack(anchor="w")
        else:
            try:
                from players.strategy_presets import get_preset, list_strategy_ids, ui_choices

                choices = ui_choices()
                known = set(list_strategy_ids())
            except Exception:
                choices = [
                    ("rule_ai", "规则AI"),
                    ("random", "随机AI"),
                    ("current_s2", "当前策略·S2"),
                ]
                known = {c[0] for c in choices}
                get_preset = lambda _k: None  # type: ignore
            cur = self.ai_type if self.ai_type in known else "rule_ai"
            self.ai_type_var.set(cur)
            for key, short in choices:
                on = cur == key
                preset = get_preset(key) if callable(get_preset) else None
                full = (
                    str(preset.get("label") or short)
                    if isinstance(preset, dict)
                    else short
                )
                self._make_colored_button(
                    ai_box,
                    ("● " if on else "○ ") + full,
                    command=lambda k=key: self._set_ai_from_bar(k),
                    bg="#1565c0" if on else "#37474f",
                    fg="white",
                    active_bg="#1976d2",
                    font=self._font,
                    padx=10,
                    pady=4,
                ).pack(anchor="w", pady=2)
            # show description for selected
            try:
                from players.strategy_presets import get_preset as _gp

                desc = (_gp(cur) or {}).get("description") or ""
                if desc:
                    self.tk.Label(
                        ai_box,
                        text=str(desc)[:80],
                        bg="#12261c",
                        fg="#90a4ae",
                        font=self._font,
                        wraplength=280,
                        justify="left",
                    ).pack(anchor="w", pady=(4, 0))
            except Exception:
                pass
            self.tk.Label(
                ai_box,
                text="（下局生效）",
                bg="#12261c",
                fg="#80cbc4",
                font=self._font,
            ).pack(anchor="w", pady=(2, 0))

        row3 = self.tk.Frame(fr, bg="#12261c")
        row3.pack(fill="x", padx=10, pady=(4, 8))
        close_btn = self._make_colored_button(
            row3,
            "收起",
            command=self._toggle_settings,
            bg="#37474f",
            fg="white",
            active_bg="#455a64",
            font=self._font,
            padx=12,
            pady=6,
        )
        close_btn.pack(side="right")

    def _apply_seat_column_widths(self) -> None:
        """Backward-compatible alias → strict interior place layout."""
        self._apply_interior_geometry()

    def _apply_interior_geometry(self) -> None:
        """
        Enforce design proportions with place (not free pack):

        - OP 67% | EXT 33% (or OP 100% if EXT folded)
        - OP: INFO / STATUS 20% flex / PLAY 60% flex / SETTINGS 2 rows
        - OP_PLAY: hand area + action bar (actions **above** settings)
        - EXT: top 30% / bot 70% (full); compact hides disc bot
        """
        from display.interior_scale import seat_scale
        from players.seat_layout_play import compute_seat_interior

        try:
            self.root.update_idletasks()
            cw = max(200, int(self.root.winfo_width()))
            ch = max(160, int(self.root.winfo_height()))
        except Exception:
            return

        sc = seat_scale(cw, ch, mode=self.mode)
        self._seat_scale = sc
        info_h = max(36, sc.font_lg + sc.font + 16)
        settings_h = max(40, sc.settings_h)
        action_h = max(16, sc.btn_h)

        vm = getattr(self, "view_mode", "full") or "full"
        expanded = bool(getattr(self, "ext_expanded", True))
        # Compact: still may show EXT top (HUD/log); disc hidden via layout
        li = compute_seat_interior(
            cw,
            ch,
            expanded=expanded,
            view_mode=vm,
            info_h=info_h,
            settings_h=settings_h,
            action_h=action_h,
        )

        # Horizontal OP | EXT
        try:
            self.op_col.place_forget()
            self.ext_col.place_forget()
        except Exception:
            pass
        self.op_col.place(x=li.op.x, y=li.op.y, width=li.op.w, height=li.op.h)
        if li.ext is not None:
            self.ext_col.place(
                x=li.ext.x, y=li.ext.y, width=li.ext.w, height=li.ext.h
            )
        else:
            try:
                self.ext_col.place_forget()
            except Exception:
                pass

        # OP vertical zones
        for fr, r in (
            (self.op_info_fr, li.op_info),
            (self.op_status_fr, li.op_status),
            (self.op_play_fr, li.op_play),
            (self.op_settings_fr, li.op_settings),
        ):
            try:
                fr.place(x=r.x, y=r.y, width=r.w, height=r.h)
            except Exception:
                pass

        # STATUS_L/R strict 50% + tile box 95% status height
        try:
            self._layout_status_halves(li.op_status.w, li.op_status.h)
        except Exception:
            pass

        # PLAY: hand then actions (design: actions bottom of OP_PLAY, above SETTINGS)
        try:
            # relative to op_play_fr
            self.play_hand_fr.place(
                x=0, y=0, width=li.op_play.w, height=li.play_hand.h
            )
            self.play_actions_fr.place(
                x=0,
                y=li.play_hand.h,
                width=li.op_play.w,
                height=li.play_actions.h,
            )
            self._layout_play_hand_zone(li.play_hand.w, li.play_hand.h)
        except Exception:
            pass

        # EXT 30/70 or compact full-top
        if li.ext is not None and li.ext_top is not None:
            try:
                self.ext_top.place(
                    x=0,
                    y=0,
                    width=li.ext.w,
                    height=max(1, li.ext_top.h),
                )
            except Exception:
                pass
            if li.ext_bot is not None and li.ext_bot.h > 0:
                try:
                    self.ext_bot.place(
                        x=0,
                        y=li.ext_top.h,
                        width=li.ext.w,
                        height=li.ext_bot.h,
                    )
                    self.ext_bot.lift()
                except Exception:
                    pass
            else:
                try:
                    self.ext_bot.place_forget()
                except Exception:
                    pass
        else:
            try:
                self.ext_top.place_forget()
                self.ext_bot.place_forget()
            except Exception:
                pass

        # Toggle labels
        try:
            if expanded and vm == "full":
                self.ext_toggle_btn.config(text="扩展 ‹")
            elif not expanded:
                self.ext_toggle_btn.config(text="扩展 ›")
            else:
                self.ext_toggle_btn.config(text="扩展 ‹")
        except Exception:
            pass
        try:
            if vm == "full":
                self.mode_full_btn.config(bg="#c9a227", fg="#1a1200")
                self.mode_compact_btn.config(bg="#2a4034", fg="#c8e6c8")
            else:
                self.mode_full_btn.config(bg="#2a4034", fg="#c8e6c8")
                self.mode_compact_btn.config(bg="#c9a227", fg="#1a1200")
        except Exception:
            pass

        self._last_interior_li = li
        # Status discard face must re-scale after zone resize
        try:
            self._play_fp = None
            if self.last_obs is not None:
                view = getattr(self.last_obs, "view", None) or {}
                if isinstance(view, dict):
                    self._update_current_discard_panel(view)
        except Exception:
            pass

    def _layout_play_hand_zone(self, zone_w: int, zone_h: int) -> None:
        """
        Hand fixed at bottom of OP_PLAY hand zone; upper mid for melds.
        Ukeire float is overlaid (not in flow).
        """
        zw = max(40, int(zone_w))
        zh = max(40, int(zone_h))
        # Hand width target: 14 tiles + ½ tile each side → tw = zone_w/15
        tw = self._hand_tile_width_14(max(40, zw - 4))
        # Fixed bottom band: one primary row height (14 tiles fit width)
        row_h = max(22, int(round(tw * 1.4)) + 4)
        hand_h = max(32, min(zh // 2, row_h + 8))
        hand_h = min(hand_h, max(32, zh - 24))
        top_h = max(20, zh - hand_h)
        try:
            self.mid_wrap.place(x=0, y=0, width=zw, height=top_h)
        except Exception:
            pass
        hand_y = zh - hand_h
        self._hand_band_y = hand_y
        self._hand_band_h = hand_h
        try:
            self.hand_fr.place(
                x=2, y=hand_y, width=max(20, zw - 4), height=hand_h
            )
        except Exception:
            pass
        # Keep floating ukeire just above hand if visible
        if getattr(self, "_ukeire_float_visible", False):
            try:
                self._place_ukeire_float(zw, zh)
            except Exception:
                pass

    def _place_ukeire_float(self, zone_w: int | None = None, zone_h: int | None = None) -> None:
        """50% alpha Toplevel, docked just above the hand strip."""
        if self.mode != "play":
            self._hide_ukeire_float()
            return
        try:
            self.root.update_idletasks()
            hx = int(self.hand_fr.winfo_rootx())
            hy = int(self.hand_fr.winfo_rooty())
            hw = max(80, int(self.hand_fr.winfo_width() or 200))
        except Exception:
            try:
                hx = int(self.root.winfo_rootx()) + 20
                hy = int(self.root.winfo_rooty()) + 120
                hw = 200
            except Exception:
                self._ukeire_float_visible = False
                return
        sc = getattr(self, "_seat_scale", None)
        face = int(sc.hand_tw) if sc is not None else 24
        float_h = max(44, min(face * 2 + 32, 100))
        float_w = max(120, min(int(hw * 0.98), hw))
        # Directly above hand display
        x = hx + max(0, (hw - float_w) // 2)
        y = max(0, hy - float_h - 2)
        try:
            self.ukeire_bar.geometry(f"{float_w}x{float_h}+{x}+{y}")
            try:
                self.ukeire_bar.attributes("-alpha", 0.5)
            except Exception:
                pass
            self.ukeire_bar.deiconify()
            self.ukeire_bar.lift()
            self._ukeire_float_visible = True
        except Exception:
            self._ukeire_float_visible = False

    def _hide_ukeire_float(self) -> None:
        try:
            self.ukeire_bar.withdraw()
        except Exception:
            try:
                self.ukeire_bar.place_forget()
            except Exception:
                pass
        self._ukeire_float_visible = False

    def _layout_status_halves(self, status_w: int, status_h: int) -> None:
        """
        STATUS_L | STATUS_R = 50% | 50% (strict place).
        Left tile frame: height = 95% of status_h, aspect fixed 1:1.4 (w:h).
        """
        sw = max(40, int(status_w))
        sh = max(24, int(status_h))
        gap = 2
        half = sw // 2
        # meta_row fills status
        try:
            self.meta_row.place(x=0, y=0, width=sw, height=sh)
        except Exception:
            return
        self.play_panel.place(x=0, y=0, width=half - gap // 2, height=sh)
        self.score_side.place(
            x=half + gap // 2, y=0, width=max(20, sw - half - gap // 2), height=sh
        )

        # Tile box: **h = 0.95 * status_h**, **w = h / 1.4** (fixed aspect)
        tile_box_h = max(14, int(round(sh * 0.95)))
        tile_box_w = max(10, int(round(tile_box_h / 1.4)))
        max_w = max(12, half - 8)
        if tile_box_w > max_w:
            # width-limited: keep aspect, height may be < 95% only if left half too narrow
            tile_box_w = max_w
            tile_box_h = max(14, int(round(tile_box_w * 1.4)))
            tile_box_h = min(tile_box_h, max(14, int(round(sh * 0.95))))

        self._status_tile_box = (tile_box_w, tile_box_h)
        ty = max(0, (sh - tile_box_h) // 2)
        # Body fills left half; children place absolute
        try:
            self.play_body.place(x=0, y=0, width=max(20, half - 2), height=sh)
        except Exception:
            pass
        try:
            # Title sits to the right of tile at top (does not steal tile height)
            self.play_title_lbl.place(
                x=tile_box_w + 6,
                y=2,
                width=max(20, half - tile_box_w - 12),
                height=max(12, min(16, sh // 6)),
            )
        except Exception:
            pass
        try:
            self.play_tile_host.place(
                x=2, y=ty, width=tile_box_w, height=tile_box_h
            )
            self.play_tile_host.configure(width=tile_box_w, height=tile_box_h)
        except Exception:
            pass

        info_x = tile_box_w + 6
        info_w = max(20, half - 10 - info_x)
        info_y = max(14, min(18, sh // 6) + 2)
        try:
            self.play_info.place(
                x=info_x,
                y=info_y,
                width=info_w,
                height=max(16, sh - info_y - 2),
            )
        except Exception:
            pass

        # Right panel wraplength
        try:
            wrap = max(60, (sw - half) - 16)
            self.round_lbl.configure(wraplength=wrap)
            self.scoreboard_lbl.configure(wraplength=wrap)
            if hasattr(self, "score_lbl"):
                self.score_lbl.configure(wraplength=wrap)
        except Exception:
            pass

    def _set_view_mode(self, mode: str) -> None:
        """F0014 full/compact: hide compact-only-hidden content + resize window."""
        from display.window_geometry import format_tk_geometry
        from players.seat_layout_play import compact_window_size

        mode = "compact" if str(mode).lower() in ("compact", "hand", "mini") else "full"
        prev = getattr(self, "view_mode", "full")
        if mode == prev:
            self._apply_interior_geometry()
            return
        self.view_mode = mode
        # Planned frame origin only (winfo_root* is client origin, below title bar)
        x = int(getattr(self, "_geom_x", 40))
        y = int(getattr(self, "_geom_y", 40))

        if mode == "full":
            fw, fh = getattr(
                self,
                "_full_locked_wh",
                getattr(self, "_full_geom_wh", (HUMAN_REF_W, HUMAN_REF_H)),
            )
            w, h = int(fw), int(fh)
            self.ext_expanded = True
            try:
                self.root.minsize(w, h)
                self.root.maxsize(w, h)
                self.root.resizable(False, False)
            except Exception:
                pass
        else:
            # remember full locked size once
            try:
                if prev == "full":
                    locked = getattr(self, "_full_locked_wh", None)
                    if locked:
                        self._full_geom_wh = locked
                    else:
                        self._full_geom_wh = (
                            max(200, int(self.root.winfo_width())),
                            max(160, int(self.root.winfo_height())),
                        )
            except Exception:
                pass
            fw, fh = getattr(
                self,
                "_full_locked_wh",
                getattr(self, "_full_geom_wh", (HUMAN_REF_W, HUMAN_REF_H)),
            )
            w, h = compact_window_size(int(fw), int(fh))
            # keep EXT open for HUD/log but disc band removed by layout
            self.ext_expanded = True
            try:
                # allow shrink for compact; still cannot exceed full locked
                self.root.minsize(w, h)
                self.root.maxsize(int(fw), int(fh))
                self.root.resizable(True, False)
            except Exception:
                pass

        try:
            self.root.geometry(format_tk_geometry(w, h, x, y))
            self._geom_x, self._geom_y = x, y
        except Exception:
            pass
        try:
            self.root.update_idletasks()
        except Exception:
            pass
        self._hand_layout_key = None
        self._disc_layout_key = None
        self._last_tiles_fp = None
        self._last_layout_wh = (0, 0)
        self._apply_seat_scale(w, h)
        self._apply_interior_geometry()
        try:
            if self.last_obs is not None:
                self._render_state(force=True)
        except Exception:
            pass

    def _toggle_ext_panel(self) -> None:
        self.ext_expanded = not bool(getattr(self, "ext_expanded", True))
        self._apply_interior_geometry()
        try:
            self._last_layout_cw = 0
            self._apply_responsive_layout()
        except Exception:
            pass

    def _append_ai_log(self, line: str) -> None:
        if self.mode == "play" or self.ai_log_list is None:
            return
        line = str(line).strip()
        if not line:
            return
        buf = getattr(self, "_ai_log_lines", None)
        if buf is None:
            self._ai_log_lines = []
            buf = self._ai_log_lines
        if buf and buf[-1] == line:
            return
        buf.append(line)
        if len(buf) > 80:
            del buf[:-80]
        try:
            self.ai_log_list.insert("end", line)
            if int(self.ai_log_list.size()) > 80:
                self.ai_log_list.delete(0)
            self.ai_log_list.see("end")
        except Exception:
            pass

    def _update_ai_log_from_obs(self, obs: dict) -> None:
        """Watch mode: derive log lines from observation deltas (no protocol change)."""
        if self.mode == "play":
            return
        try:
            me = int(self.seat)
            players = obs.get("players") or obs.get("seats") or []
            my = None
            for p in players:
                if int(p.get("seat", -1)) == me:
                    my = p
                    break
            if my is None and isinstance(obs.get("you"), dict):
                my = obs["you"]
            disc = list((my or {}).get("discards") or (my or {}).get("discard_pile") or [])
            n_disc = len(disc)
            prev_n = int(getattr(self, "_ai_prev_disc_n", 0) or 0)
            if n_disc > prev_n and disc:
                tid = disc[-1]
                if isinstance(tid, dict):
                    tid = tid.get("id") or tid.get("tile_id")
                self._append_ai_log(f"出 {tid}")
            self._ai_prev_disc_n = n_disc
            # melds growth
            melds = list((my or {}).get("melds") or [])
            n_m = len(melds)
            prev_m = int(getattr(self, "_ai_prev_meld_n", 0) or 0)
            if n_m > prev_m and melds:
                last = melds[-1]
                kind = last.get("kind") if isinstance(last, dict) else "?"
                self._append_ai_log(f"副露 {meld_kind_label(kind)}")
            self._ai_prev_meld_n = n_m
            st = str((my or {}).get("status") or "")
            if st == "finished" and not getattr(self, "_ai_logged_hu", False):
                lw = (my or {}).get("last_win") if isinstance(my, dict) else None
                extra = ""
                if isinstance(lw, dict):
                    if lw.get("zimo"):
                        extra = "·自摸"
                    elif lw.get("loser") is not None:
                        extra = f"·点炮S{lw.get('loser')}"
                    if lw.get("fan") is not None:
                        extra += f"·{lw.get('fan')}番"
                order = (my or {}).get("hu_order")
                order_s = f"第{order}家" if order is not None else ""
                self._append_ai_log(f"胡牌 {order_s}{extra}".strip())
                self._ai_logged_hu = True
                # Same prominent banner as human play window
                try:
                    self._show_self_hu_banner(my if isinstance(my, dict) else {})
                except Exception:
                    pass
            phase = str(obs.get("phase") or "")
            if phase and phase != getattr(self, "_ai_prev_phase", None):
                if phase in ("finished", "exchange", "deal"):
                    self._append_ai_log(f"阶段 {phase}")
                self._ai_prev_phase = phase
        except Exception:
            pass

    def _toggle_settings(self) -> None:
        if self._settings_open:
            try:
                self.settings_fr.place_forget()
            except Exception:
                pass
            try:
                self.settings_fr.pack_forget()
            except Exception:
                pass
            self._settings_open = False
            try:
                self.settings_btn.config(text="设置 ▾")
            except Exception:
                pass
            return
        self._build_settings_panel()
        # Overlay above OP_SETTINGS within OP column (parents differ from settings_bar)
        try:
            self.settings_fr.place_forget()
        except Exception:
            pass
        try:
            li = getattr(self, "_last_interior_li", None)
            if li is not None:
                # sit just above settings strip
                h = min(220, max(120, li.op_play.h // 2))
                y = max(0, li.op_settings.y - h)
                self.settings_fr.place(
                    x=0, y=y, width=li.op.w, height=h
                )
                self.settings_fr.lift()
            else:
                self.settings_fr.place(relx=0, rely=0.35, relwidth=0.67, relheight=0.35)
                self.settings_fr.lift()
        except Exception:
            try:
                self.settings_fr.pack(fill="x", padx=4, pady=2)
            except Exception:
                pass
        self._settings_open = True
        try:
            self.settings_btn.config(text="设置 ▴")
        except Exception:
            pass

    def _on_ai_type_change(self) -> None:
        if self.mode == "play":
            return
        self.ai_type = str(self.ai_type_var.get() or "rule_ai")
        self._emit_seat_settings()
        try:
            self._build_settings_bar()
        except Exception:
            pass
        self.status_note = f"AI 策略已设为 {self.ai_type}（下局生效）"
        self._refresh_chrome()

    def _emit_seat_settings(self) -> None:
        from protocols.wire import msg_seat_settings

        payload = msg_seat_settings(
            self.seat,
            auto_start=bool(self.auto_start),
            ai_type=None if self.mode == "play" else str(self.ai_type),
            predict_opponents=bool(self.predict_opponents_enabled),
        )
        try:
            _safe_emit(payload)
        except Exception:
            pass

    def _toggle_recommend_marks(self) -> None:
        self.recommend_marks_enabled = not bool(self.recommend_marks_enabled)
        self.status_note = (
            "已开启推荐出牌标记"
            if self.recommend_marks_enabled
            else "已关闭推荐出牌标记"
        )
        try:
            self._build_settings_bar()
        except Exception:
            pass
        self._ukeire_overlay_key = None
        # rec_key / recommend flag in tiles_fp → rebuild once when needed
        self._render_state(force=False)
        self._refresh_chrome()

    def _toggle_predict_opponents(self) -> None:
        self.predict_opponents_enabled = not bool(self.predict_opponents_enabled)
        self._emit_seat_settings()
        try:
            self._build_settings_bar()
        except Exception:
            pass
        if self.predict_opponents_enabled:
            self._show_predict_panel()
            self._predict_fp = None  # force refresh
            self._maybe_refresh_predict(force=True)
            self.status_note = "对手牌预测已开启"
        else:
            self._hide_predict_panel()
            self._predict_forecasts = []
            self._predict_joints = []
            self._predict_fp = None
            self.status_note = "对手牌预测已关闭"
        self._refresh_chrome()

    def _show_predict_panel(self) -> None:
        if self._predict_packed:
            return
        try:
            self.predict_fr.pack(fill="x", before=self.meta_row, pady=(2, 4), padx=2)
            self._predict_packed = True
        except Exception:
            try:
                self.predict_fr.pack(fill="x", pady=2, padx=2)
                self._predict_packed = True
            except Exception:
                pass

    def _hide_predict_panel(self) -> None:
        if not self._predict_packed:
            return
        try:
            self.predict_fr.pack_forget()
        except Exception:
            pass
        self._predict_packed = False
        for c in list(self.predict_fr.winfo_children()):
            try:
                c.destroy()
            except Exception:
                pass

    def _maybe_refresh_predict(self, *, force: bool = False) -> None:
        if not self.predict_opponents_enabled:
            return
        view = self.last_obs.view if self.last_obs else None
        if not isinstance(view, dict):
            return
        from players.analysis.hand_predict import (
            apply_oracle_accuracy,
            discard_fingerprint,
            predict_opponent_hands,
        )

        fp = discard_fingerprint(view)
        if not force and fp == self._predict_fp and self._predict_forecasts:
            return
        prev_fp = self._predict_fp
        self._predict_fp = fp
        # seed from fingerprint for stable-ish refresh across discards
        seed = abs(hash(fp)) % (2**31)
        last_discarder = None
        last_tile = None
        ls = view.get("last_discard_seat")
        if ls is not None:
            try:
                last_discarder = int(ls)
            except (TypeError, ValueError):
                last_discarder = None
        ld = view.get("last_discard")
        if isinstance(ld, dict):
            last_tile = ld.get("id") or f"{ld.get('suit')}_{ld.get('rank')}"
        elif ld is not None:
            last_tile = str(ld)
        # Continuity: pass previous joint scenes (v2); cold start has none
        prev_joints = list(self._predict_joints) if self._predict_joints else None
        prev_forecasts = (
            list(self._predict_forecasts) if self._predict_forecasts else None
        )
        if force and prev_fp is None:
            prev_joints = None
            prev_forecasts = None
        try:
            forecasts = predict_opponent_hands(
                view,
                self.seat,
                top_k=5,
                prev_joints=prev_joints,
                prev_forecasts=prev_forecasts,
                last_discarder=last_discarder,
                last_discard_tile=last_tile,
                seed=seed,
            )
            scenes = []
            if forecasts:
                scenes = list(getattr(forecasts[0], "_joint_scenes", None) or [])
            oracle = view.get("oracle_hands")
            if isinstance(oracle, dict):
                forecasts = apply_oracle_accuracy(forecasts, oracle)
            self._predict_forecasts = forecasts
            self._predict_joints = scenes
            # F0010-L: per-game prediction log for accuracy analysis
            try:
                self._log_predict_tick(
                    view=view,
                    forecasts=forecasts,
                    fp=fp,
                    last_discarder=last_discarder,
                    last_tile=last_tile,
                    used_continuity=bool(prev_joints),
                )
            except Exception as log_e:
                sys.stderr.write(f"[seat_window] predict log fail: {log_e}\n")
                sys.stderr.flush()
        except Exception as e:
            try:
                sys.stderr.write(f"[seat_window] predict fail: {e}\n")
                sys.stderr.flush()
            except Exception:
                pass
            return
        self._render_predict_panel()

    def _log_predict_tick(
        self,
        *,
        view: dict,
        forecasts: list,
        fp: str,
        last_discarder: int | None,
        last_tile: str | None,
        used_continuity: bool,
    ) -> None:
        from players.analysis.predict_log import get_predict_logger

        game_id = ""
        if self.last_obs is not None:
            game_id = str(getattr(self.last_obs, "game_id", "") or "")
        if not game_id:
            game_id = f"seat{self.seat}-unknown"
        oracle = view.get("oracle_hands") if isinstance(view, dict) else None
        remain = view.get("remain") if isinstance(view.get("remain"), dict) else None
        if remain is None:
            # Derive remain from public view (discards/melds/own hand) for baseline
            try:
                from players.analysis.hand_predict import _remain_from_view

                remain = _remain_from_view(view, self.seat)
            except Exception:
                remain = None
        meta: dict[int, dict] = {}
        for p in view.get("players") or []:
            try:
                s = int(p.get("seat", -1))
            except (TypeError, ValueError):
                continue
            if s == self.seat:
                continue
            disc = p.get("discard_pile") or []
            meta[s] = {
                "n_discards": len(disc),
                "n_melds": len(p.get("melds") or []),
                "dingque": p.get("dingque"),
            }
        seq = view.get("discard_seq")
        try:
            seq_i = int(seq) if seq is not None else None
        except (TypeError, ValueError):
            seq_i = None
        wr = view.get("wall_remaining")
        try:
            wr_i = int(wr) if wr is not None else None
        except (TypeError, ValueError):
            wr_i = None
        get_predict_logger(game_id).emit_tick(
            game_id=game_id,
            self_seat=self.seat,
            forecasts=forecasts,
            oracle_hands=oracle if isinstance(oracle, dict) else None,
            discard_fp=fp,
            discard_seq=seq_i,
            last_discarder=last_discarder,
            last_discard_tile=last_tile,
            phase=str(getattr(self, "phase", "") or view.get("phase") or ""),
            wall_remaining=wr_i,
            used_continuity=used_continuity,
            remain=remain,
            meta_by_seat=meta,
            source="seat_window",
        )

    def _format_hand_line(self, tiles: list[str]) -> str:
        """Compact CJK labels for predicted hand."""
        parts: list[str] = []
        for tid in tiles:
            try:
                suit, rank_s = str(tid).split("_", 1)
                r = int(rank_s)
                ch = {"wan": "万", "tong": "筒", "tiao": "条"}.get(suit, suit)
                parts.append(f"{r}{ch}")
            except Exception:
                parts.append(str(tid))
        return " ".join(parts)

    def _predict_is_early(self) -> bool:
        """True when opponents have few discards → coarse grain UI."""
        view = self.last_obs.view if self.last_obs else None
        if not isinstance(view, dict):
            return True
        from players.analysis.hand_predict import EARLY_DISCARD_THRESHOLD

        max_d = 0
        for p in view.get("players") or []:
            try:
                if int(p.get("seat", -1)) == self.seat:
                    continue
            except (TypeError, ValueError):
                continue
            max_d = max(max_d, len(p.get("discard_pile") or []))
        return max_d <= EARLY_DISCARD_THRESHOLD

    def _format_coarse_summary(self, h) -> str:
        """Suit bias + shanten + label without full tile list."""
        tiles = list(getattr(h, "tiles", None) or [])
        suit_cnt: dict[str, int] = {}
        name = {"wan": "万", "tong": "筒", "tiao": "条"}
        for tid in tiles:
            su = str(tid).split("_", 1)[0]
            suit_cnt[su] = suit_cnt.get(su, 0) + 1
        if suit_cnt:
            main = max(suit_cnt.items(), key=lambda x: (x[1], x[0]))[0]
            suit_s = f"偏{name.get(main, main)}({suit_cnt[main]}张)"
        else:
            suit_s = "花色不明"
        sh = getattr(h, "shanten_est", None)
        sh_s = f"向听≈{sh}" if sh is not None else "向听—"
        lab = getattr(h, "label", "") or ""
        bits = [suit_s, sh_s]
        if lab:
            bits.append(str(lab))
        return " · ".join(bits)

    def _render_predict_panel(self) -> None:
        if not self.predict_opponents_enabled or not self._predict_packed:
            return
        fr = self.predict_fr
        for c in list(fr.winfo_children()):
            try:
                c.destroy()
            except Exception:
                pass
        early = self._predict_is_early()
        hdr_txt = (
            "对手牌预测（开局粗测 · 花色/向听 · 信息不足）"
            if early
            else "对手牌预测（联合场景 · Top-5 · 牌张重合度）"
        )
        hdr = self.tk.Label(
            fr,
            text=hdr_txt,
            bg="#0a1f16",
            fg="#80cbc4",
            font=self._font_lg,
            anchor="w",
            padx=8,
            pady=4,
        )
        hdr.pack(fill="x")
        if not self._predict_forecasts:
            self.tk.Label(
                fr,
                text="等待牌局数据…",
                bg="#0a1f16",
                fg="#90a4ae",
                font=self._font,
                anchor="w",
                padx=8,
            ).pack(fill="x")
            return
        wrap_w = max(280, int(self.root.winfo_width() or 400) - 40)
        note = (
            "※ 准确度=与真牌的牌张重合度(F1)，非整手猜中；开局仅显示粗粒度"
            if early
            else "※ 准确度=牌张重合度(F1/Top-K最佳)，非整手 exact"
        )
        self.tk.Label(
            fr,
            text=note,
            bg="#0a1f16",
            fg="#78909c",
            font=self._font,
            anchor="w",
            padx=8,
        ).pack(fill="x")
        for fc in self._predict_forecasts:
            seat = getattr(fc, "seat", None)
            acc = getattr(fc, "accuracy", None)
            detail = getattr(fc, "accuracy_detail", None) or {}
            hint = getattr(fc, "strategy_hint", "") or ""
            acc_s = "—"
            if acc is not None:
                br = detail.get("best_rank")
                top1 = detail.get("top1_f1")
                acc_s = f"{int(round(float(acc) * 100))}% 最佳#{br or '—'}"
                if top1 is not None:
                    acc_s += f" Top1 {int(round(float(top1) * 100))}%"
            hint_s = f"  策略:{hint}" if hint else ""
            seat_hdr = self.tk.Label(
                fr,
                text=f"S{seat}  牌张重合度 {acc_s}{hint_s}",
                bg="#12352a",
                fg="#ffe082",
                font=self._font,
                anchor="w",
                padx=8,
                pady=2,
            )
            seat_hdr.pack(fill="x", padx=4, pady=(4, 0))
            hyps = list(getattr(fc, "hypotheses", []) or [])
            show = hyps[:3] if early else hyps
            for h in show:
                pct = int(round(float(h.confidence) * 100))
                sid = getattr(h, "scene_id", None) or h.rank
                lab = getattr(h, "label", "") or ""
                sh = getattr(h, "shanten_est", None)
                if early:
                    body = self._format_coarse_summary(h)
                    text = f"  #{h.rank:2d}  {pct:2d}%  [场景#{sid}]  {body}"
                else:
                    line = self._format_hand_line(list(h.tiles or []))
                    meta_bits = [f"场景#{sid}"]
                    if sh is not None:
                        meta_bits.append(f"向听{sh}")
                    if lab:
                        meta_bits.append(str(lab))
                    meta = " · ".join(meta_bits)
                    text = f"  #{h.rank:2d}  {pct:2d}%  [{meta}]  {line}"
                row = self.tk.Label(
                    fr,
                    text=text,
                    bg="#0a1f16",
                    fg="#e0f2f1",
                    font=self._font,
                    anchor="w",
                    padx=6,
                    justify="left",
                    wraplength=wrap_w,
                )
                row.pack(fill="x", padx=2)

    def emit_ready(self, *, auto: bool = False) -> None:
        from protocols.wire import msg_ready

        if self._ready_sent:
            return
        # Allow click even if flag glitched, as long as we are in ready UI
        if not self.awaiting_ready and self.phase not in ("ready_confirm", "wait"):
            try:
                sys.stderr.write(
                    f"[seat_window] emit_ready ignored seat={self.seat} "
                    f"phase={self.phase}\n"
                )
                sys.stderr.flush()
            except Exception:
                pass
            return

        self._ready_sent = True
        self.awaiting_ready = False
        try:
            sys.stderr.write(
                f"[seat_window] emit ready seat={self.seat} auto={auto}\n"
            )
            sys.stderr.flush()
        except Exception:
            pass
        _safe_emit(msg_ready(self.seat, auto=auto))
        self.phase = "wait"
        self.status_note = "已确认开始，等待全员确认 / 发牌…"
        self._hide_ready_banner()
        self._rebuild_action_bar()
        self._refresh_chrome()

    def emit_decision(self, action, request_id: str, reason: str = "human:click") -> None:
        from protocols.messages import Decision
        from protocols.wire import msg_decision

        try:
            sys.stderr.write(
                f"[seat_window] decision seat={self.seat} "
                f"{action.type.value if hasattr(action.type, 'value') else action.type} "
                f"req={request_id}\n"
            )
            sys.stderr.flush()
        except Exception:
            pass
        dec = Decision(request_id=request_id, action=action, reason=reason)
        _safe_emit(msg_decision(dec))

    def _show_ready(self) -> None:
        """Show banner + bottom ready controls inside the seat window."""
        self._ready_sent = False
        self.awaiting_ready = True
        self.phase = "ready_confirm"
        self.auto_var.set(bool(self.auto_start))
        self.ready_banner.config(
            text=(
                f"第 {self.ready_round}/{self.num_rounds} 局 — "
                f"请在窗口底部确认开始（回车亦可）"
            )
        )
        if not self._banner_packed:
            self.ready_banner.pack(fill="x", after=self.status)
            self._banner_packed = True
        role = "AI 观战" if self.mode != "play" else "人类"
        self.status_note = (
            f"【第 {self.ready_round}/{self.num_rounds} 局】{role}座请确认开始"
        )
        self._rebuild_action_bar()
        self._refresh_chrome()
        # Only auto-confirm when user checked「自动开始」(not by seat type)
        if self.auto_start:
            self.root.after(120, lambda: self.emit_ready(auto=True))

    def _hide_ready_banner(self) -> None:
        if self._banner_packed:
            try:
                self.ready_banner.pack_forget()
            except Exception:
                pass
            self._banner_packed = False

    def _on_mid_content_configure(self, _event=None) -> None:
        try:
            self.mid_canvas.configure(scrollregion=self.mid_canvas.bbox("all"))
        except Exception:
            pass

    def _on_mid_canvas_configure(self, event=None) -> None:
        try:
            w = int(event.width) if event is not None else int(self.mid_canvas.winfo_width())
            if w > 1:
                self.mid_canvas.itemconfigure(self._mid_win, width=w)
        except Exception:
            pass

    def _bind_mousewheel(self, _event=None) -> None:
        try:
            self.mid_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
            self.mid_canvas.bind_all("<Button-4>", self._on_mousewheel)
            self.mid_canvas.bind_all("<Button-5>", self._on_mousewheel)
        except Exception:
            pass

    def _unbind_mousewheel(self, _event=None) -> None:
        try:
            self.mid_canvas.unbind_all("<MouseWheel>")
            self.mid_canvas.unbind_all("<Button-4>")
            self.mid_canvas.unbind_all("<Button-5>")
        except Exception:
            pass

    def _on_mousewheel(self, event) -> None:
        try:
            if getattr(event, "num", None) == 4 or getattr(event, "delta", 0) > 0:
                self.mid_canvas.yview_scroll(-3, "units")
            elif getattr(event, "num", None) == 5 or getattr(event, "delta", 0) < 0:
                self.mid_canvas.yview_scroll(3, "units")
        except Exception:
            pass

    def _on_configure(self, event=None) -> None:
        """Debounced re-layout when the seat window is resized (F0006)."""
        try:
            if event is not None and event.widget is not self.root:
                return
        except Exception:
            pass
        try:
            self._apply_interior_geometry()
        except Exception:
            pass
        # Windows: if user dragged/resized after pin window, stop parent re-pins
        if sys.platform == "win32" and not getattr(self, "_user_geometry_free", False):
            try:
                if time.time() > float(getattr(self, "_geom_pin_until", 0)):
                    ax = int(self.root.winfo_rootx())
                    ay = int(self.root.winfo_rooty())
                    aw = int(self.root.winfo_width())
                    ah = int(self.root.winfo_height())
                    px = int(getattr(self, "_geom_x", ax))
                    py = int(getattr(self, "_geom_y", ay))
                    if abs(ax - px) > 24 or abs(ay - py) > 24:
                        self._user_geometry_free = True
                    # size change also counts as user free after pin window
                    if abs(aw - max(320, aw)) >= 0 and (
                        abs(aw - int(getattr(self, "_last_layout_wh", (aw, ah))[0])) > 16
                        or abs(ah - int(getattr(self, "_last_layout_wh", (aw, ah))[1])) > 16
                    ):
                        if time.time() > float(getattr(self, "_geom_pin_until", 0)) + 0.5:
                            self._user_geometry_free = True
            except Exception:
                pass
        if self._resize_after_id is not None:
            try:
                self.root.after_cancel(self._resize_after_id)
            except Exception:
                pass
        self._resize_after_id = self.root.after(80, self._apply_responsive_layout)

    def _force_relayout(self) -> None:
        """Recompute tile wrap only if usable width actually changed."""
        try:
            cw = self._content_width()
        except Exception:
            cw = 0
        if self._first_layout_done and abs(cw - self._last_layout_cw) < 12:
            return
        self._last_layout_wh = (0, 0)
        self._apply_responsive_layout()

    def _apply_seat_scale(self, ww: int | None = None, wh: int | None = None) -> None:
        """F0019: recompute S and apply font/tile budgets from client size."""
        from display.interior_scale import seat_scale
        from tkinter import font as tkfont

        try:
            if ww is None:
                ww = int(self.root.winfo_width())
            if wh is None:
                wh = int(self.root.winfo_height())
        except Exception:
            return
        if ww < 50 or wh < 50:
            return
        sc = seat_scale(ww, wh, mode=self.mode)
        prev = getattr(self, "_seat_scale", None)
        scale_changed = (
            prev is not None
            and (abs(prev.s - sc.s) > 0.04 or prev.hand_tw != sc.hand_tw)
        )
        self._seat_scale = sc
        # Fonts — configure in place (avoid replacing Font objects every paint)
        try:
            if prev is None or scale_changed or int(self._font.actual("size")) != sc.font:
                self._font.configure(size=sc.font)
                self._font_lg.configure(size=sc.font_lg)
                if hasattr(self, "_font_badge"):
                    self._font_badge.configure(
                        size=max(8, sc.font_lg - 1), weight="bold"
                    )
        except Exception:
            try:
                fam = getattr(self, "_ui_family", "Arial")
                self._font = tkfont.Font(family=fam, size=sc.font)
                self._font_lg = tkfont.Font(
                    family=fam, size=sc.font_lg, weight="bold"
                )
            except Exception:
                pass
        # Only invalidate tile pools when scale actually jumps (F0013 keep-alive)
        if scale_changed:
            try:
                self._photo_cache.clear()
            except Exception:
                pass
            self._hand_layout_key = None
            self._disc_layout_key = None
            self._last_tiles_fp = None

    def _apply_responsive_layout(self) -> None:
        self._resize_after_id = None
        try:
            ww = int(self.root.winfo_width())
            wh = int(self.root.winfo_height())
        except Exception:
            return
        if ww < 50 or wh < 50:
            return
        # Ignore tiny move-only noise; re-render when size changes
        if (ww, wh) == self._last_layout_wh:
            return
        self._last_layout_wh = (ww, wh)
        try:
            self._apply_seat_scale(ww, wh)
            self._apply_interior_geometry()
        except Exception:
            pass
        if self.last_obs is not None or self.awaiting_ready:
            try:
                self._render_state(force=True)
            except Exception:
                pass
        else:
            # Still refresh chrome fonts when idle
            try:
                self._refresh_chrome()
            except Exception:
                pass

    def _schedule_render(self, *, force: bool = False) -> None:
        """Coalesce rapid observation updates to one paint (anti-flicker)."""
        self._render_pending_force = self._render_pending_force or force
        if self._render_after_id is not None:
            try:
                self.root.after_cancel(self._render_after_id)
            except Exception:
                pass
        # Longer debounce: high-frequency obs was still flashing hand rebuilds
        self._render_after_id = self.root.after(80, self._flush_scheduled_render)

    def _flush_scheduled_render(self) -> None:
        self._render_after_id = None
        force = self._render_pending_force
        self._render_pending_force = False
        try:
            self._render_state(force=force)
        except Exception:
            pass

    def _content_width(self) -> int:
        """Usable width for hand tile rows (prefer fixed bottom hand_fr)."""
        try:
            hw = int(self.hand_fr.winfo_width() or 0)
            if hw >= 80:
                self._cached_content_w = hw
                return hw
        except Exception:
            pass
        try:
            li = getattr(self, "_last_interior_li", None)
            if li is not None and li.op_play.w > 40:
                w = max(100, int(li.op_play.w) - 8)
                self._cached_content_w = w
                return w
        except Exception:
            pass
        try:
            root_w = max(200, int(self.root.winfo_width()))
            from players.seat_layout_play import OP_WIDTH_RATIO

            if getattr(self, "ext_expanded", True):
                w = int(root_w * OP_WIDTH_RATIO) - 24
            else:
                w = root_w - 36
            w = max(100, w)
            self._cached_content_w = w
            return w
        except Exception:
            pass
        cached = int(getattr(self, "_cached_content_w", 0) or 0)
        return cached if cached >= 100 else 360

    def _hand_chrome_px(self) -> int:
        """Extra width per hand cell outside face (highlight L+R).

        Fixed chrome so select/unselect never reflows the 14-tile row.
        Budget: face ring ht=2 + face_hold ring ht=2 (each side).
        """
        return 8

    def _hand_tile_width_14(self, area_w: int | None = None) -> int:
        """
        Maximize face width so **14** tiles fit on one row.

        Side margins kept small (~3% of width total, min 4px each side), not half-tile
        (half-tile left too much empty space on the right).

            side_total ≈ max(8, W//16)
            tw = floor( (W - side_total) / 14 ) - chrome
        """
        if area_w is None:
            area_w = self._content_width()
        w = max(60, int(area_w))
        chrome = self._hand_chrome_px()
        # Tiny side gutters (~2–3% total); maximize face for 14 tiles
        side_total = max(4, w // 40)
        avail = max(40, w - side_total)
        tw = max(8, avail // 14 - chrome)
        if tw >= 12 and (tw % 2) == 1:
            tw -= 1
        while tw > 8:
            need = 14 * (tw + chrome)
            if need <= w - 2:
                break
            tw -= 1
        return max(8, tw)

    def _pack_tiles_wrapped(
        self,
        parent,
        tile_ids: list[str],
        *,
        tw: int,
        per_row: int,
        selected_set: set[str] | None = None,
        selected_indices: set[int] | None = None,
        clickable: bool = False,
        start_label: str | None = None,
        recommend_order: dict[str, int] | None = None,
        ukeire_by_tid: dict[str, list[str]] | None = None,
        focus_tid: str | None = None,
        use_hand_index: bool = False,
        gap: int | None = None,
    ) -> None:
        """Pack tiles into one or more rows (F0006 wrap). F0012: rec badge + ukeire.

        When ``use_hand_index`` is True (hand strip), selection uses hand index so
        duplicate tile_ids can be selected independently (换三张).
        Hand uses gap=0 (tiles flush).
        """
        selected_set = selected_set or set()
        selected_indices = selected_indices or set()
        recommend_order = recommend_order or {}
        ukeire_by_tid = ukeire_by_tid or {}
        # Hand: gap 0; other strips may keep small gap
        if gap is None:
            gap = 0 if use_hand_index else 2
        gap = max(0, int(gap))
        body = self.tk.Frame(parent, bg="#143528")
        body.pack(side="left", fill="both", expand=True)
        if start_label and not use_hand_index:
            self.tk.Label(
                body,
                text=start_label,
                bg="#143528",
                fg="#ffe096",
                font=self._font,
                anchor="w",
            ).pack(anchor="w")
        if not tile_ids:
            return
        per_row = max(1, int(per_row))
        side_m = int(getattr(self, "_hand_side_margin", 0) or 0) if use_hand_index else 0
        row_fr = None
        for i, tid in enumerate(tile_ids):
            if i % per_row == 0:
                row_fr = self.tk.Frame(body, bg="#143528")
                # center hand row: left half-tile spacer
                row_fr.pack(anchor="w", pady=0 if use_hand_index else 1)
                if side_m > 0:
                    self.tk.Frame(
                        row_fr, bg="#143528", width=side_m, height=1
                    ).pack(side="left")
            tid_s = str(tid)
            if use_hand_index:
                sel = i in selected_indices
            else:
                sel = tid_s in selected_set
            ord_n = recommend_order.get(tid_s)

            def _click(t=tid_s, idx=i, event=None):
                self._on_tile_click(t, hand_index=idx if use_hand_index else None)

            cmd = _click if clickable else None
            # cell: face only — ukeire waits go to floating panel (F0012)
            cell = self.tk.Frame(row_fr, bg="#143528")
            cell.pack(side="left", padx=gap, pady=0 if use_hand_index else 2)
            # Fixed ring thickness on face_hold so selection never reflows width
            face_hold = self.tk.Frame(
                cell,
                bg="#ff8f00" if (use_hand_index and sel) else "#143528",
                highlightthickness=2 if use_hand_index else 0,
                highlightbackground=(
                    "#ffeb3b" if (use_hand_index and sel) else "#143528"
                ),
                highlightcolor=(
                    "#ffeb3b" if (use_hand_index and sel) else "#143528"
                ),
            )
            face_hold.pack(side="top")
            b = self._tile_btn(
                face_hold,
                tid_s,
                selected=sel,
                cmd=cmd,
                tw=tw,
                compact=bool(use_hand_index),
            )
            b.pack()
            try:
                b._hand_index = int(i)  # type: ignore[attr-defined]
            except Exception:
                pass
            # F0012 rank badge bottom-right of main hand tile
            badge = None
            if clickable and ord_n:
                badge = self.tk.Label(
                    face_hold,
                    text=str(int(ord_n)),
                    bg="#ff6f00",
                    fg="#ffffff",
                    font=self._font,
                    bd=0,
                    padx=3,
                    pady=0,
                )
                try:
                    badge.place(relx=1.0, rely=1.0, anchor="se", x=-1, y=-1)
                except Exception:
                    badge.pack(side="bottom", anchor="e")
            if clickable and use_hand_index:
                self._hand_widgets.append(b)
                self._hand_tile_widgets.append((tid_s, b, int(tw), int(i)))
                self._hand_cell_by_tid[int(i)] = {
                    "cell": cell,
                    "face_hold": face_hold,
                    "badge": badge,
                    "order": ord_n,
                    "tid": tid_s,
                    "ukeire": list(ukeire_by_tid.get(tid_s) or []),
                }
        if clickable and use_hand_index:
            # Ensure double gold ring + dim others after rebuild
            try:
                self._apply_hand_selection_styles()
            except Exception:
                self._ukeire_overlay_key = None
                self._update_ukeire_overlays()

    def _photo(self, tid: str, tw: int = 36):
        # Snap to even sizes so cache does not explode under continuous resize
        tw = max(12, int(tw) // 2 * 2)
        key = f"{tid}:{tw}"
        if key in self._photo_cache:
            return self._photo_cache[key]
        path = _tile_png(self.theme, tid)
        if path is None:
            return None
        try:
            img = self._load_scaled_photo(str(path), tw)
            if img is None:
                return None
            self._photo_cache[key] = img
            return img
        except Exception:
            return None

    def _load_scaled_photo(self, path: str, tw: int):
        """
        Scale tile face so **width <= tw** (strict).

        Source assets are ~270px; earlier subsample left faces wider than the
        layout budget, so a full hand overflowed and was clipped.
        Prefer pygame smoothscale → PNG → PhotoImage; fall back to Tk subsample.
        """
        import math

        tw = max(12, int(tw))
        # 1) pygame smooth scale
        try:
            import base64
            import io

            import pygame

            if not pygame.get_init():
                pygame.init()
            surf = pygame.image.load(path)
            ow, oh = surf.get_size()
            if ow <= 0:
                raise ValueError("empty surface")
            th = max(1, int(round(tw * oh / float(ow))))
            if (ow, oh) != (tw, th):
                surf = pygame.transform.smoothscale(surf, (tw, th))
            bio = io.BytesIO()
            pygame.image.save(surf, bio)
            data = bio.getvalue()
            if data:
                b64 = base64.b64encode(data).decode("ascii")
                img = self.tk.PhotoImage(data=b64)
                if img.width() <= tw + 1:
                    return img
        except Exception:
            pass

        # 2) Tk integer subsample until width <= tw
        try:
            img = self.tk.PhotoImage(file=path)
            iw = max(1, img.width())
            if iw > tw:
                factor = max(1, int(math.ceil(iw / float(tw))))
                img = img.subsample(factor, factor)
            guard = 0
            while img.width() > tw and img.width() >= 2 and guard < 8:
                img = img.subsample(2, 2)
                guard += 1
            return img
        except Exception:
            return None

    def _clear(self, fr) -> None:
        for c in fr.winfo_children():
            c.destroy()

    def _tile_btn(
        self,
        parent,
        tid: str,
        *,
        selected: bool = False,
        cmd=None,
        tw: int = 36,
        compact: bool = False,
    ):
        """Tile face as Label (no extra Button chrome) so size matches layout tw."""
        # Hand compact: fixed ht so select/unselect never reflows 14-tile row.
        face_tw = max(8, int(tw))
        if face_tw >= 12 and (face_tw % 2) == 1:
            face_tw -= 1
        photo = self._photo(tid, face_tw)
        st = self._tile_face_style(selected=selected, compact=compact)
        bg, border = st["bg"], st["border"]
        bd, relief, ht = st["bd"], st["relief"], st["ht"]
        if photo is not None:
            b = self.tk.Label(
                parent,
                image=photo,
                bg=bg,
                bd=bd,
                relief=relief,
                highlightthickness=ht,
                highlightbackground=border,
                highlightcolor=border,
                cursor="hand2" if cmd else "arrow",
            )
            b.image = photo  # keep ref
        else:
            b = self.tk.Label(
                parent,
                text=_label_tile(tid),
                bg=bg,
                fg=st["fg"],
                font=self._font if compact else (self._font_lg if selected else self._font),
                width=max(2, face_tw // 10),
                bd=bd,
                relief=relief,
                highlightthickness=ht,
                highlightbackground=border,
                highlightcolor=border,
                cursor="hand2" if cmd else "arrow",
            )
        try:
            b._base_tw = int(tw)  # type: ignore[attr-defined]
            b._tid = str(tid)  # type: ignore[attr-defined]
            b._compact = bool(compact)  # type: ignore[attr-defined]
        except Exception:
            pass
        if cmd is not None:
            b.bind("<ButtonRelease-1>", lambda _e, c=cmd: c())
        return b

    def _tile_face_style(self, *, selected: bool, compact: bool = False) -> dict:
        """
        Face styles. Compact (hand) keeps constant outer size: always ht=2, bd=0.
        Selected = bright gold frame + warm bg (visible even under PhotoImage edges).
        """
        if compact:
            # Fixed geometry — unselected border matches table so ring is invisible
            ht, bd, relief = 2, 0, "flat"
        else:
            ht, bd = 3, 2
            relief = "raised" if selected else "solid"
        if selected:
            return {
                "bg": "#8d6e00",
                "border": "#ffeb3b",
                "bd": bd if compact else 2,
                "relief": "solid" if compact else relief,
                "ht": ht,
                "fg": "#fff59d",
            }
        return {
            "bg": "#1e3c28",
            # Match hand table so reserved chrome does not show a dark box
            "border": "#143528" if compact else "#2a4a34",
            "bd": bd,
            "relief": relief,
            "ht": ht,
            "fg": "#f0f0d8",
        }

    def _apply_cell_selection_chrome(self, hidx: int, *, selected: bool) -> None:
        """Gold ring on face_hold/cell (second frame outside the face Label)."""
        cell_info = self._hand_cell_by_tid.get(int(hidx))
        if not isinstance(cell_info, dict):
            return
        fh = cell_info.get("face_hold")
        cell = cell_info.get("cell")
        # Fixed thickness always → no reflow; color shows selection
        ring_ht = 2
        if selected:
            ring_bg = "#ff8f00"
            ring_border = "#ffeb3b"
            cell_bg = "#5d4037"
        else:
            ring_bg = "#143528"
            ring_border = "#143528"
            cell_bg = "#143528"
        for w, ht, bg, border in (
            (fh, ring_ht, ring_bg, ring_border),
            (cell, 0, cell_bg, cell_bg),
        ):
            if w is None:
                continue
            try:
                w.configure(
                    bg=bg,
                    highlightthickness=ht,
                    highlightbackground=border,
                    highlightcolor=border,
                )
            except Exception:
                pass

    def _update_tile_face(
        self,
        b,
        tid: str,
        *,
        selected: bool = False,
        tw: int = 36,
        cmd=None,
    ) -> None:
        """F0013: in-place update of an existing tile Label (no destroy)."""
        compact = bool(getattr(b, "_compact", False))
        face_tw = max(8, int(tw))
        if face_tw >= 12 and (face_tw % 2) == 1:
            face_tw -= 1
        photo = self._photo(str(tid), face_tw)
        st = self._tile_face_style(selected=selected, compact=compact)
        try:
            if photo is not None:
                b.configure(
                    image=photo,
                    text="",
                    bg=st["bg"],
                    bd=st["bd"],
                    relief=st["relief"],
                    highlightthickness=st["ht"],
                    highlightbackground=st["border"],
                    highlightcolor=st["border"],
                    cursor="hand2" if cmd else "arrow",
                )
                b.image = photo
            else:
                b.configure(
                    image="",
                    text=_label_tile(str(tid)),
                    bg=st["bg"],
                    fg=st["fg"],
                    font=self._font,
                    width=max(2, face_tw // 10),
                    bd=st["bd"],
                    relief=st["relief"],
                    highlightthickness=st["ht"],
                    highlightbackground=st["border"],
                    highlightcolor=st["border"],
                    cursor="hand2" if cmd else "arrow",
                )
            b._base_tw = int(tw)  # type: ignore[attr-defined]
            b._tid = str(tid)  # type: ignore[attr-defined]
            b._compact = compact  # type: ignore[attr-defined]
        except Exception:
            pass
        if cmd is not None:
            try:
                b.bind("<ButtonRelease-1>", lambda _e, c=cmd: c())
            except Exception:
                pass

    def _hand_layout_key_of(
        self, n: int, tw: int, per_row: int, *, recommend_on: bool
    ) -> tuple:
        return (int(n), int(tw), int(per_row), bool(recommend_on))

    def _try_inplace_hand(
        self,
        hand: list[str],
        *,
        tw: int,
        per_row: int,
        selected_indices: set[int],
        rec_order: dict[str, int],
        uke_map: dict[str, list[str]],
        recommend_on: bool,
    ) -> bool:
        """Update hand faces in place when pool layout matches. F0013."""
        n = len(hand)
        key = self._hand_layout_key_of(n, tw, per_row, recommend_on=recommend_on)
        if (
            key != self._hand_layout_key
            or len(self._hand_tile_widgets) != n
            or not self._hand_tile_widgets
        ):
            return False
        new_widgets: list[tuple] = []
        for i, tid in enumerate(hand):
            tid_s = str(tid)
            try:
                _old_tid, b, _old_tw, hi = self._hand_tile_widgets[i]
            except Exception:
                return False

            def _click(t=tid_s, idx=i, event=None):
                self._on_tile_click(t, hand_index=idx)

            self._update_tile_face(
                b,
                tid_s,
                selected=(i in selected_indices),
                tw=tw,
                cmd=_click,
            )
            try:
                b._hand_index = int(i)  # type: ignore[attr-defined]
            except Exception:
                pass
            new_widgets.append((tid_s, b, int(tw), int(i)))
            cell = self._hand_cell_by_tid.get(int(i))
            if isinstance(cell, dict):
                cell["tid"] = tid_s
                cell["order"] = rec_order.get(tid_s)
                cell["ukeire"] = list(uke_map.get(tid_s) or [])
        self._hand_tile_widgets = new_widgets
        self._hand_widgets = [w[1] for w in new_widgets]
        self._ukeire_overlay_key = None
        try:
            self._update_ukeire_overlays()
        except Exception:
            pass
        try:
            self._apply_hand_selection_styles()
        except Exception:
            pass
        return True

    def _try_inplace_disc(
        self, discs: list[str], *, tw: int, per_row: int
    ) -> bool:
        """Update discard faces in place when pool size/layout matches. F0013."""
        ids = [str(t) for t in discs]
        n = len(ids)
        key = (n, int(tw), int(per_row))
        if (
            key != self._disc_layout_key
            or len(self._disc_tile_widgets) != n
            or (n > 0 and not self._disc_tile_widgets)
        ):
            return False
        if n == 0:
            return True
        for i, tid in enumerate(ids):
            try:
                b = self._disc_tile_widgets[i]
            except Exception:
                return False
            self._update_tile_face(b, tid, selected=False, tw=tw, cmd=None)
        return True

    def _refresh_chrome(self) -> None:
        role = "人类操作" if self.mode == "play" else "AI 观战"
        rnd = format_round_line(self.ready_round, self.num_rounds)
        try:
            from version import APP_VERSION

            ver = f"  v{APP_VERSION}"
        except Exception:
            ver = ""
        self.hdr.config(
            text=f"座位 S{self.seat}  [{role}]  {rnd}  phase={self.phase}{ver}"
        )
        self.status.config(text=self.status_note)
        try:
            self.round_lbl.config(text=rnd)
        except Exception:
            pass

    def _update_round_score_panel(self, view: dict | None) -> None:
        """Refresh 局数 + 全员得分 + 本家摘要."""
        try:
            self.round_lbl.config(
                text=format_round_line(self.ready_round, self.num_rounds)
            )
        except Exception:
            pass
        players = (view or {}).get("players") if isinstance(view, dict) else None
        board = format_scoreboard_line(
            players if isinstance(players, list) else None,
            self_seat=self.seat,
            multiline=True,
        )
        try:
            self.scoreboard_lbl.config(text=board)
        except Exception:
            pass

    def _show_self_hu_banner(self, me: dict | None = None) -> None:
        """Big in-window notice when this seat has already hu'd (血战)."""
        me = me if isinstance(me, dict) else {}
        order = me.get("hu_order")
        lw = me.get("last_win") if isinstance(me.get("last_win"), dict) else {}
        fan = lw.get("fan") if lw else None
        if lw.get("zimo"):
            kind = "自摸"
        elif lw.get("loser") is not None:
            kind = f"点炮S{lw.get('loser')}"
        else:
            kind = "胡牌"
        fan_s = f" · {fan}番" if fan is not None else ""
        order_s = f"第{order}家" if order is not None else "已胡"
        text = (
            f"★★★  本座已胡 · {order_s}（{kind}{fan_s}）  ★★★\n"
            f"血战继续 — 本窗只读观战，其余玩家继续行牌"
        )
        try:
            # Keep wraplength ≈ content width so multi-line banner is readable
            try:
                ww = max(200, int(self.root.winfo_width() or 0) - 24)
                self.hu_banner.config(wraplength=ww)
            except Exception:
                pass
            self.hu_banner.config(text=text, bg="#b71c1c", fg="#fff59d")
            if not self._hu_banner_packed:
                # Pack under status in op_info_fr (always visible, not scroll mid)
                self.hu_banner.pack(fill="x", after=self.status, pady=(2, 4))
                self._hu_banner_packed = True
        except Exception as e:
            print(f"[seat_window] hu_banner show failed: {e}")

    def _hide_self_hu_banner(self) -> None:
        if not getattr(self, "_hu_banner_packed", False):
            return
        try:
            self.hu_banner.pack_forget()
        except Exception:
            pass
        self._hu_banner_packed = False

    def _opp_structure_fingerprint(self, opp_rows: list[dict]) -> tuple:
        """Seats / dingque / status / meld count — rebuild opp rows when these change."""
        rows = []
        for p in sorted(opp_rows, key=lambda x: int(x.get("seat", 0) or 0)):
            try:
                ps = int(p.get("seat", -1))
            except Exception:
                continue
            rows.append(
                (
                    ps,
                    str(p.get("dingque") or ""),
                    str(p.get("status") or "active"),
                    int(p.get("hu_order") or 0) if p.get("hu_order") is not None else 0,
                    len(p.get("melds") or []),
                )
            )
        return tuple(rows)

    def _opp_values_fingerprint(self, opp_rows: list[dict]) -> tuple:
        """Volatile fields updated in-place (score / hand_count) — never rebuild hand."""
        rows = []
        for p in sorted(opp_rows, key=lambda x: int(x.get("seat", 0) or 0)):
            try:
                ps = int(p.get("seat", -1))
            except Exception:
                continue
            rows.append(
                (
                    ps,
                    str(p.get("hand_count", "—")),
                    str(p.get("score", 0)),
                )
            )
        return tuple(rows)

    def _draw_opponent_hud(self, opp_rows: list[dict], cw: int) -> None:
        """Render other seats: 定缺 + 是否胡牌 + 手牌数/分 (public HUD)."""
        self._opp_cell_labels = []
        if not opp_rows:
            self.tk.Label(
                self.opp_fr,
                text="（暂无其他玩家数据）",
                bg="#0f241c",
                fg="#90a4ae",
                font=self._font,
                anchor="w",
                padx=8,
                pady=4,
            ).pack(fill="x")
            return

        # Header row
        hdr = self.tk.Frame(self.opp_fr, bg="#1b3a2c")
        hdr.pack(fill="x", padx=2, pady=(2, 0))
        for col, w in (
            ("座位", 6),
            ("定缺", 6),
            ("状态", 18),
            ("手牌", 5),
            ("副露", 5),
            ("分数", 6),
        ):
            self.tk.Label(
                hdr,
                text=col,
                bg="#1b3a2c",
                fg="#a5d6a7",
                font=self._font,
                width=w,
                anchor="w",
            ).pack(side="left", padx=2)

        for p in sorted(opp_rows, key=lambda x: int(x.get("seat", 0))):
            try:
                ps = int(p.get("seat", -1))
            except Exception:
                continue
            st_txt, st_fg = _status_hud_label(p)
            dq_raw = p.get("dingque")
            dq = _dingque_label(dq_raw)
            dq_fg = _dingque_color(dq_raw)
            is_hu = str(p.get("status") or "") == "finished"
            row_bg = "#3e2723" if is_hu else "#0f241c"
            row = self.tk.Frame(self.opp_fr, bg=row_bg)
            row.pack(fill="x", padx=2, pady=1)
            cells = [
                ("seat", f"S{ps}", "#fffde7", 6),
                ("dq", dq, dq_fg, 6),
                ("status", st_txt, st_fg, 18),
                ("hand_count", str(p.get("hand_count", "—")), "#e0e0e0", 5),
                ("melds", str(len(p.get("melds") or [])), "#e0e0e0", 5),
                ("score", str(p.get("score", 0)), "#ffecb3", 6),
            ]
            # seat_id must not collide with cell key "seat" (Label overwrite bug)
            refs: dict = {"seat_id": ps, "row": row, "is_hu": is_hu}
            for key, text, fg, width in cells:
                lbl = self.tk.Label(
                    row,
                    text=text,
                    bg=row_bg,
                    fg=fg,
                    font=self._font_lg if is_hu and key == "status" else self._font,
                    width=width,
                    anchor="w",
                )
                lbl.pack(side="left", padx=2)
                refs[key] = lbl
            self._opp_cell_labels.append(refs)

    def _update_opponent_hud_inplace(self, opp_rows: list[dict]) -> None:
        """Update score / hand_count / status text without destroying widgets."""
        if not self._opp_cell_labels:
            # No widgets yet — full draw path needed
            self._clear(self.opp_fr)
            self._draw_opponent_hud(opp_rows, self._content_width())
            return
        by_seat = {}
        for p in opp_rows:
            try:
                by_seat[int(p.get("seat", -1))] = p
            except Exception:
                continue
        for refs in self._opp_cell_labels:
            try:
                ps = int(refs.get("seat_id", refs.get("seat", -1)))
            except (TypeError, ValueError):
                # Legacy: "seat" was overwritten by Label — skip row safely
                continue
            p = by_seat.get(ps)
            if p is None:
                continue
            st_txt, st_fg = _status_hud_label(p)
            dq_raw = p.get("dingque")
            dq = _dingque_label(dq_raw)
            dq_fg = _dingque_color(dq_raw)
            is_hu = str(p.get("status") or "") == "finished"
            row_bg = "#3e2723" if is_hu else "#0f241c"
            updates = {
                "dq": (dq, dq_fg),
                "status": (st_txt, st_fg),
                "hand_count": (str(p.get("hand_count", "—")), "#e0e0e0"),
                "melds": (str(len(p.get("melds") or [])), "#e0e0e0"),
                "score": (str(p.get("score", 0)), "#ffecb3"),
            }
            row = refs.get("row")
            if row is not None:
                try:
                    row.configure(bg=row_bg)
                except Exception:
                    pass
            for key, (text, fg) in updates.items():
                lbl = refs.get(key)
                if lbl is None:
                    continue
                try:
                    font = (
                        self._font_lg
                        if is_hu and key == "status"
                        else self._font
                    )
                    lbl.configure(text=text, fg=fg, bg=row_bg, font=font)
                except Exception:
                    pass
            refs["is_hu"] = is_hu

    def _remain_count_for_tid(self, tid: str) -> int | None:
        """Prefer analysis remain map; fallback to public view count."""
        tid = str(tid)
        hints = self.pending_hints if isinstance(self.pending_hints, dict) else {}
        rem = hints.get("remain")
        if isinstance(rem, dict) and tid in rem:
            try:
                return max(0, int(rem[tid]))
            except Exception:
                pass
        view = None
        if self.last_obs is not None:
            view = getattr(self.last_obs, "view", None) or {}
        return remain_of_tile_from_view(view if isinstance(view, dict) else {}, self.seat, tid)

    def _remain_count_colors(self, count: int) -> tuple[str, str]:
        if count <= 0:
            return "#b71c1c", "#ffffff"
        if count == 1:
            return "#e65100", "#fffde7"
        return "#1b5e20", "#c8e6c9"

    def _ukeire_face_tw(self) -> int:
        """Ukeire face width (F0012/F0019): scales with seat S."""
        sc = getattr(self, "_seat_scale", None)
        if sc is not None:
            return max(10, int(sc.hand_tw))
        try:
            cw = int(self._content_width() or 0)
        except Exception:
            cw = 0
        # ~one tile per ~48px of content; clamp to readable range
        if cw >= 48:
            est = max(32, min(40, cw // 16))
        else:
            est = 36
        return max(32, min(40, int(est) // 2 * 2))

    def _update_ukeire_overlays(self) -> None:
        """F0012: full-width bar with readable winning tiles for focused tenpai rec.

        Remain count is packed **above** each face (never place-over the tile).
        All waits are shown — no single-hand-cell width clipping.
        """
        from players.analysis.discard_recommend import ukeire_for_focus

        if not self.recommend_marks_enabled or self.phase != "discard":
            focus_tid = None
            focus_idx = None
            uke_focus: list[str] = []
        else:
            focus_tid = None
            focus_idx = None
            if self.selected:
                try:
                    focus_idx = int(self.selected[0])
                    if 0 <= focus_idx < len(self.hand_ids):
                        focus_tid = str(self.hand_ids[focus_idx])
                except Exception:
                    focus_idx = None
            uke_focus = ukeire_for_focus(self._recommendations, focus_tid)

        face_tw = self._ukeire_face_tw()
        overlay_key = (
            focus_idx,
            focus_tid,
            tuple(uke_focus),
            bool(self.recommend_marks_enabled),
            self.phase,
            int(face_tw),
        )
        if overlay_key == self._ukeire_overlay_key:
            return
        self._ukeire_overlay_key = overlay_key

        body = getattr(self, "ukeire_bar_body", None)
        if body is None:
            return
        try:
            for c in list(body.winfo_children()):
                c.destroy()
        except Exception:
            pass

        title = getattr(self, "ukeire_bar_title", None)
        if not uke_focus:
            # No tiles → hide float (no layout squeeze)
            self._hide_ukeire_float()
            return

        try:
            if title is not None:
                n = len(uke_focus)
                title.configure(
                    text=f"可听进张 · 打 {focus_tid or '?'} 后可胡 {n} 种"
                )
        except Exception:
            pass

        # Show floating panel over hand zone
        self._place_ukeire_float()

        # Wrap rows so many waits stay fully visible (inside float width)
        try:
            cw = max(120, int(self.ukeire_bar.winfo_width() or 0) - 12)
            if cw < 80:
                cw = max(120, int(self._content_width() or 200) // 2)
        except Exception:
            cw = 200
        col_w = face_tw + 8
        per_row = max(1, cw // max(1, col_w))
        row_fr = None
        for i, ut in enumerate(uke_focus):
            if i % per_row == 0:
                row_fr = self.tk.Frame(body, bg="#1a4028")
                row_fr.pack(anchor="w", pady=1)
            col = self.tk.Frame(row_fr, bg="#1a4028")
            col.pack(side="left", padx=2)
            rem_n = self._remain_count_for_tid(str(ut))
            if rem_n is not None:
                bg, fg = self._remain_count_colors(int(rem_n))
                self.tk.Label(
                    col,
                    text=str(int(rem_n)),
                    bg=bg,
                    fg=fg,
                    font=self._font_lg,
                    bd=0,
                    padx=3,
                    pady=0,
                ).pack(side="top")
            else:
                self.tk.Label(
                    col,
                    text="·",
                    bg="#0d2818",
                    fg="#546e7a",
                    font=self._font,
                    bd=0,
                ).pack(side="top")
            ub = self._tile_btn(
                col, str(ut), selected=False, cmd=None, tw=face_tw
            )
            ub.pack(side="top", pady=(1, 0))

    def _apply_hand_selection_styles(self) -> None:
        """Update hand highlight in-place (border/color only; no size reflow).

        PhotoImage fills the Label, so bg alone is nearly invisible — use a
        fixed-thickness gold highlight ring on the face + face_hold wrapper.
        Unselected tiles dim slightly when any tile is selected.
        """
        sel_idx = {int(x) for x in self.selected}
        any_sel = bool(sel_idx)
        for item in self._hand_tile_widgets:
            if len(item) >= 4:
                tid, w, base_tw, hidx = item[0], item[1], int(item[2]), int(item[3])
            elif len(item) >= 3:
                tid, w, base_tw = item[0], item[1], int(item[2])
                hidx = int(getattr(w, "_hand_index", -1))
            else:
                tid, w = item[0], item[1]
                base_tw = int(getattr(w, "_base_tw", 36) or 36)
                hidx = int(getattr(w, "_hand_index", -1))
            selected = hidx in sel_idx
            # Hand compact chrome: fixed ht (must not reflow / widen cells)
            compact = bool(getattr(w, "_compact", True))
            st = self._tile_face_style(selected=selected, compact=compact)
            bg, border = st["bg"], st["border"]
            bd, relief, ht = st["bd"], st["relief"], st["ht"]
            # Dim non-selected faces when something is selected (contrast)
            if any_sel and not selected and compact:
                bg = "#0f2418"
                border = "#0f2418"
            try:
                if getattr(w, "image", None) is not None:
                    w.configure(
                        bg=bg,
                        bd=bd,
                        relief=relief,
                        highlightthickness=ht,
                        highlightbackground=border,
                        highlightcolor="#ffffff" if selected else border,
                    )
                else:
                    w.configure(
                        bg=bg,
                        fg="#fff59d" if selected else (
                            "#9e9e9e" if any_sel else "#f0f0d8"
                        ),
                        font=self._font,
                        bd=bd,
                        relief=relief,
                        highlightthickness=ht,
                        highlightbackground=border,
                        highlightcolor="#ffffff" if selected else border,
                    )
            except Exception:
                pass
            try:
                self._apply_cell_selection_chrome(hidx, selected=selected)
            except Exception:
                pass
        self._update_ukeire_overlays()

    def _sync_recommendations_from_hints(self) -> None:
        """Build F0012 recommendation list from pending_hints (same algo as proxy)."""
        from players.analysis.discard_recommend import build_discard_recommendations

        self._recommendations = []
        if not self.recommend_marks_enabled or self.phase != "discard":
            return
        hints = self.pending_hints if isinstance(self.pending_hints, dict) else None
        if not hints:
            return
        recs = hints.get("recommendations")
        if isinstance(recs, list) and recs:
            self._recommendations = list(recs)
            return
        ranks = hints.get("discard_ranks")
        if ranks:
            self._recommendations = build_discard_recommendations(ranks)

    def _place_remain_badge(self, remain: int | None) -> None:
        """Show digit-only remain badge at bottom-right of the tile face."""
        digit = format_remain_badge(remain)
        if not digit:
            try:
                self.play_remain_badge.place_forget()
            except Exception:
                pass
            self._play_badge_placed = False
            return
        # color by scarcity
        r = int(digit)
        if r <= 0:
            bg, fg = "#b71c1c", "#ffffff"
        elif r == 1:
            bg, fg = "#e65100", "#fffde7"
        else:
            bg, fg = "#1b5e20", "#c8e6c9"
        try:
            self.play_remain_badge.configure(text=digit, bg=bg, fg=fg)
            self.play_remain_badge.place(relx=1.0, rely=1.0, anchor="se", x=-1, y=-1)
            self._play_badge_placed = True
            # keep badge above tile label
            self.play_remain_badge.lift()
        except Exception:
            pass

    def _status_discard_tile_tw(self) -> int:
        """Face width from tile box: h = 0.95 * status_h, aspect 1:1.4 → w = h/1.4."""
        box = getattr(self, "_status_tile_box", None)
        if box and box[0] > 0:
            return max(12, int(box[0]) // 2 * 2)
        try:
            li = getattr(self, "_last_interior_li", None)
            st_h = int(li.op_status.h) if li is not None else 0
        except Exception:
            st_h = 0
        if st_h <= 0:
            sc = getattr(self, "_seat_scale", None)
            return max(14, int(sc.hand_tw) if sc else 26)
        tile_h = max(14, int(round(st_h * 0.95)))
        tw = max(12, int(round(tile_h / 1.4)))
        return max(12, min(tw, 48) // 2 * 2)

    def _update_current_discard_panel(self, view: dict) -> None:
        """Tile face + corner remain digit; one-line actor+tile; wall total."""
        view = view if isinstance(view, dict) else {}
        tid = view.get("last_discard")
        seat = view.get("last_discard_seat")
        wall_rem = view.get("wall_remaining")
        remain = remain_of_tile_from_view(
            view,
            self.seat,
            str(tid) if tid is not None else None,
        )
        tw = self._status_discard_tile_tw()
        fp = (str(tid) if tid is not None else None, seat, remain, wall_rem, tw)
        if fp == getattr(self, "_play_fp", None):
            return
        self._play_fp = fp
        headline = format_discard_headline(
            seat, self.seat, str(tid) if tid is not None else None
        )
        wall_line = format_wall_remaining_line(wall_rem)
        try:
            if tid is None or tid == "" or tid == "None":
                self.play_tile_lbl.configure(
                    image="",
                    text="—",
                    bg="#0d1a12",
                    fg="#90a4ae",
                    width=max(2, tw // 10),
                    height=2,
                )
                self._play_tile_photo = None
                self._place_remain_badge(None)
                self.play_who_lbl.configure(text=headline, fg="#b0bec5")
                self.play_wall_lbl.configure(text=wall_line, fg="#90a4ae")
            else:
                photo = self._photo(str(tid), tw)
                if photo is not None:
                    self.play_tile_lbl.configure(
                        image=photo,
                        text="",
                        bg="#2a1f00",
                        fg="#fff59d",
                    )
                    try:
                        self.play_tile_lbl.configure(width=0, height=0)
                    except Exception:
                        pass
                    self._play_tile_photo = photo
                    self.play_tile_lbl.image = photo
                else:
                    self.play_tile_lbl.configure(
                        image="",
                        text=_label_tile(str(tid)),
                        bg="#2a1f00",
                        fg="#fff59d",
                        width=6,
                        height=2,
                    )
                    self._play_tile_photo = None
                self._place_remain_badge(remain)
                try:
                    is_self = seat is not None and int(seat) == int(self.seat)
                except (TypeError, ValueError):
                    is_self = False
                actor_fg = "#ffeb3b" if is_self else "#e8f5e9"
                self.play_who_lbl.configure(text=headline, fg=actor_fg)
                self.play_wall_lbl.configure(text=wall_line, fg="#a5d6a7")
        except Exception:
            pass

    def _tiles_fingerprint(
        self,
        *,
        hand: list[str],
        melds: list,
        discs: list,
        cw: int,
        tw: int,
        per_row: int,
        disc_tw: int,
        disc_per: int,
        my_status: str = "active",
        phase: str | None = None,
    ) -> tuple:
        """Fingerprint for **hand/meld/disc layout only**.

        Opponent scores / hand_count are intentionally excluded — they update
        every turn and must not destroy/rebuild the hand strip (main flicker).
        """
        meld_key = tuple(
            (
                str(m.get("tile_id")),
                str(m.get("kind")),
            )
            for m in melds
            if isinstance(m, dict)
        )
        rec_key = tuple(
            (str(r.get("tile_id")), int(r.get("order") or 0))
            for r in (self._recommendations or [])
            if isinstance(r, dict)
        )
        return (
            tuple(hand),
            meld_key,
            tuple(str(t) for t in discs),
            int(cw // 8),  # bucket width: ignore 1–7px noise
            tw,
            per_row,
            disc_tw,
            disc_per,
            my_status,
            str(phase or self.phase or ""),
            rec_key,
            bool(self.recommend_marks_enabled),
        )

    def _action_fingerprint(self) -> tuple:
        legal_key = tuple(
            sorted(
                {
                    getattr(a.type, "value", str(a.type))
                    for a in (self.legal or [])
                }
            )
        )
        return (
            self.mode,
            self.phase,
            bool(self.awaiting_ready),
            bool(self._ready_sent),
            self.ready_round,
            legal_key,
            len(self.selected),
            self.pending_req is not None,
        )

    def _render_state(self, *, force: bool = False) -> None:
        self._refresh_chrome()

        view = self.last_obs.view if self.last_obs else {}
        me = None
        for p in view.get("players") or []:
            try:
                if int(p.get("seat", -1)) == self.seat:
                    me = p
                    break
            except Exception:
                continue

        if not view or me is None:
            self.score_lbl.config(text="本家: 等待主程序推送牌局数据…")
            self._update_round_score_panel(view if isinstance(view, dict) else {})
            self._update_current_discard_panel({})
            self._rebuild_action_bar(force=force)
            return

        my_status = str(me.get("status") or "active")
        my_dq = _dingque_label(me.get("dingque"))
        my_sc = me.get("score", 0)
        try:
            sc_i = int(my_sc)
            sc_s = f"{sc_i:+d}" if sc_i != 0 else "0"
        except (TypeError, ValueError):
            sc_s = str(my_sc)
        score_txt = (
            f"本家 S{self.seat}: {sc_s}  |  定缺: {my_dq}  |  "
            f"牌墙: {view.get('wall_remaining', '—')}"
        )
        if my_status == "finished":
            order = me.get("hu_order")
            score_txt += f"  |  ★已胡 第{order or '—'}家"
        self.score_lbl.config(text=score_txt)
        self._update_round_score_panel(view if isinstance(view, dict) else {})
        # 血战: 本座已胡 — 醒目横幅 + 状态栏
        if my_status == "finished":
            self._show_self_hu_banner(me)
            if self.phase not in ("finished", "game_end") and not self.awaiting_ready:
                if not str(self.status_note).startswith("已胡牌"):
                    self.status_note = (
                        f"已胡牌离桌 · 血战继续（观看其余玩家） "
                        f"胡序=第{me.get('hu_order') or '—'}家"
                    )
            # status_note may have changed after first _refresh_chrome
            try:
                self.status.config(text=self.status_note)
            except Exception:
                pass
        else:
            self._hide_self_hu_banner()

        # Always refresh current discard focus (even when hand fingerprint skips rebuild)
        self._update_current_discard_panel(view if isinstance(view, dict) else {})
        # F0010: refresh opponent hand predictions on discard cadence
        try:
            self._maybe_refresh_predict(force=False)
        except Exception:
            pass

        from players.view.responsive import compute_tile_grid
        from engine.tile import parse_tile, sorted_tiles

        # F0019: keep scale in sync even when obs arrives without Configure
        try:
            self._apply_seat_scale()
        except Exception:
            pass
        sc = getattr(self, "_seat_scale", None)
        if sc is None:
            from display.interior_scale import seat_scale

            sc = seat_scale(
                int(self.root.winfo_width() or 885),
                int(self.root.winfo_height() or 498),
                mode=self.mode,
            )
            self._seat_scale = sc

        cw = self._content_width()
        raw_hand = list(me.get("hand") or [])
        tiles = []
        keep = []
        for tid in raw_hand:
            try:
                tiles.append(parse_tile(str(tid)))
            except Exception:
                keep.append(str(tid))
        hand = [t.id for t in sorted_tiles(tiles)] + keep
        self.hand_ids = hand
        melds = list(me.get("melds") or [])
        discs = list(me.get("discard_pile") or [])[-24:]

        # Hand: 14 tiles + ½ tile margin each side → tw = cw/15; gap=0
        import math

        from players.view.responsive import TileGrid

        htw = self._hand_tile_width_14(cw)
        n_hand = len(hand)
        per_row = 14
        rows = 0 if n_hand == 0 else max(1, int(math.ceil(n_hand / float(per_row))))
        hand_grid = TileGrid(
            tw=htw,
            th=max(1, int(round(htw * 1.4))),
            per_row=per_row,
            rows=rows,
            gap=0,
            n=n_hand,
        )
        # Small side margin after maximizing 14 faces (center the strip)
        chrome = self._hand_chrome_px()
        used = 14 * (htw + chrome)
        self._hand_side_margin = max(0, (cw - used) // 2)
        # Ensure hand_fr is wide enough: prefer OP play width when content_w stale
        try:
            li = getattr(self, "_last_interior_li", None)
            if li is not None:
                need = 14 * (htw + self._hand_chrome_px()) + htw
                if int(li.op_play.w) - 4 > cw and need > cw:
                    cw2 = max(100, int(li.op_play.w) - 4)
                    htw2 = self._hand_tile_width_14(cw2)
                    if htw2 != htw:
                        htw = htw2
                        hand_grid = TileGrid(
                            tw=htw,
                            th=max(1, int(round(htw * 1.4))),
                            per_row=14,
                            rows=rows,
                            gap=0,
                            n=n_hand,
                        )
                        self._hand_side_margin = max(0, htw // 2)
                        self._cached_content_w = cw2
        except Exception:
            pass
        # Discard strip lives in EXT (~33% when expanded). Use stable geometry
        # (not live winfo) so F0013 dirty fingerprints do not thrash on first paints.
        try:
            root_w = max(200, int(self.root.winfo_width()))
        except Exception:
            from display.interior_scale import AI_REF_W, HUMAN_REF_W

            root_w = HUMAN_REF_W if self.mode == "play" else AI_REF_W
        if getattr(self, "ext_expanded", True):
            from players.seat_layout_play import OP_WIDTH_RATIO

            disc_cw = max(80, int(root_w * (1.0 - OP_WIDTH_RATIO)) - 8)
        else:
            disc_cw = max(80, cw)
        disc_grid = (
            compute_tile_grid(
                len(discs),
                disc_cw,
                min_tw=sc.disc_tw,
                max_tw=max(sc.disc_tw, int(round(sc.disc_tw * 1.2))),
                gap=max(1, sc.gap - 1),
                margin=max(2, sc.pad // 2),
                label_w=0,
                max_rows=8,
                cell_extra=max(2, sc.pad // 2),
            )
            if discs
            else None
        )

        opp_rows: list[dict] = []
        for p in view.get("players") or []:
            try:
                ps = int(p.get("seat", -1))
            except Exception:
                continue
            if ps == self.seat:
                continue
            if isinstance(p, dict):
                opp_rows.append(p)

        tiles_fp = self._tiles_fingerprint(
            hand=hand,
            melds=melds,
            discs=discs,
            cw=cw,
            tw=hand_grid.tw,
            per_row=hand_grid.per_row,
            disc_tw=disc_grid.tw if disc_grid else 0,
            disc_per=disc_grid.per_row if disc_grid else 0,
            my_status=my_status,
            phase=self.phase,
        )
        opp_struct_fp = self._opp_structure_fingerprint(opp_rows)
        opp_values_fp = self._opp_values_fingerprint(opp_rows)

        # F0012 recommendations for badges / ukeire (needed for inplace + rebuild)
        rec_order: dict[str, int] = {}
        uke_map: dict[str, list[str]] = {}
        if self.recommend_marks_enabled and self.phase == "discard":
            from players.analysis.discard_recommend import recommendation_order_map

            rec_order = recommendation_order_map(self._recommendations)
            for r in self._recommendations or []:
                if isinstance(r, dict) and r.get("is_tenpai"):
                    tid = str(r.get("tile_id") or "")
                    if tid:
                        uke_map[tid] = list(r.get("ukeire_tiles") or [])
        sel_indices = set(int(x) for x in self.selected)
        recommend_on = bool(
            self.recommend_marks_enabled and self.phase == "discard" and rec_order
        )
        meld_key = tuple(
            (str(m.get("tile_id")), str(m.get("kind")))
            for m in melds
            if isinstance(m, dict)
        )
        disc_ids = [str(t) for t in discs]
        disc_tw = disc_grid.tw if disc_grid else 0
        disc_per = disc_grid.per_row if disc_grid else 0

        # --- F0013 fast path: identical tiles fingerprint ---
        if (
            not force
            and tiles_fp == self._last_tiles_fp
            and self._hand_tile_widgets
        ):
            sel_fp = tuple(int(x) for x in self.selected)
            if sel_fp != self._last_sel_fp:
                self._apply_hand_selection_styles()
                self._last_sel_fp = sel_fp
            if (
                opp_struct_fp != self._last_opp_struct_fp
                or not self._opp_cell_labels
            ):
                self._clear(self.opp_fr)
                self._draw_opponent_hud(opp_rows, cw)
            elif opp_values_fp != self._last_opp_values_fp:
                self._update_opponent_hud_inplace(opp_rows)
            self._last_opp_struct_fp = opp_struct_fp
            self._last_opp_values_fp = opp_values_fp
            self._rebuild_action_bar(force=False)
            return

        # --- F0013 dirty path: layout-stable in-place face updates ---
        hand_ok = False
        disc_ok = False
        meld_ok = False
        if not force:
            hand_ok = self._try_inplace_hand(
                hand,
                tw=hand_grid.tw,
                per_row=hand_grid.per_row,
                selected_indices=sel_indices,
                rec_order=rec_order,
                uke_map=uke_map,
                recommend_on=recommend_on,
            )
            if discs and disc_grid is not None:
                disc_ok = self._try_inplace_disc(
                    disc_ids, tw=disc_tw, per_row=disc_per
                )
            elif not discs and self._disc_layout_key == (0, 0, 0):
                disc_ok = True
            meld_ok = meld_key == self._last_meld_key and (
                bool(melds) == bool(self.meld_fr.winfo_children())
            )

        if hand_ok and disc_ok and meld_ok and not force:
            if (
                opp_struct_fp != self._last_opp_struct_fp
                or not self._opp_cell_labels
            ):
                self._clear(self.opp_fr)
                self._draw_opponent_hud(opp_rows, cw)
            elif opp_values_fp != self._last_opp_values_fp:
                self._update_opponent_hud_inplace(opp_rows)
            self._last_tiles_fp = tiles_fp
            self._last_opp_struct_fp = opp_struct_fp
            self._last_opp_values_fp = opp_values_fp
            self._last_sel_fp = tuple(int(x) for x in self.selected)
            self._last_layout_cw = cw
            self._first_layout_done = True
            self._rebuild_action_bar(force=False)
            return

        # --- Full / partial rebuild ---
        if not hand_ok or force:
            self._clear(self.hand_fr)
            self._hand_widgets = []
            self._hand_tile_widgets = []
            self._hand_cell_by_tid = {}
            focus = None
            if self.selected:
                try:
                    fi = int(self.selected[0])
                    if 0 <= fi < len(hand):
                        focus = str(hand[fi])
                except Exception:
                    focus = None
            self._pack_tiles_wrapped(
                self.hand_fr,
                hand,
                tw=hand_grid.tw,
                per_row=hand_grid.per_row,
                selected_indices=sel_indices,
                clickable=True,
                start_label=None,
                recommend_order=rec_order,
                ukeire_by_tid=uke_map,
                focus_tid=focus,
                use_hand_index=True,
                gap=0,
            )
            self._hand_layout_key = self._hand_layout_key_of(
                len(hand), hand_grid.tw, hand_grid.per_row, recommend_on=recommend_on
            )

        if not meld_ok or force:
            self._clear(self.meld_fr)
            if melds:
                # Meld faces = same size as hand (AI windows were fixed tw=28 → overflow)
                meld_tw = int(hand_grid.tw) if hand_grid is not None else htw
                meld_tw = max(10, min(int(meld_tw), 40))
                if meld_tw >= 12 and (meld_tw % 2) == 1:
                    meld_tw -= 1
                self.tk.Label(
                    self.meld_fr,
                    text="副露",
                    bg="#143528",
                    fg="#ffe096",
                    font=self._font,
                ).pack(anchor="w")
                meld_row = self.tk.Frame(self.meld_fr, bg="#143528")
                meld_row.pack(anchor="w", fill="x")
                row_used = 0
                cur = self.tk.Frame(meld_row, bg="#143528")
                cur.pack(anchor="w")
                for m in melds:
                    if not isinstance(m, dict):
                        continue
                    tid = m.get("tile_id")
                    kind_raw = str(m.get("kind") or "")
                    kind_zh = meld_kind_label(kind_raw)
                    n = 4 if "gang" in kind_raw.lower() else 3
                    if not tid:
                        continue
                    # width estimate: n faces + chrome + kind label
                    est = n * (meld_tw + 4) + 20
                    if row_used > 0 and row_used + est > cw:
                        cur = self.tk.Frame(meld_row, bg="#143528")
                        cur.pack(anchor="w")
                        row_used = 0
                    box = self.tk.Frame(cur, bg="#143528")
                    box.pack(side="left", padx=3)
                    self.tk.Label(
                        box,
                        text=kind_zh,
                        bg="#143528",
                        fg="#c8dcc8",
                        font=self._font,
                    ).pack()
                    trow = self.tk.Frame(box, bg="#143528")
                    trow.pack()
                    for _ in range(n):
                        self._tile_btn(
                            trow,
                            str(tid),
                            tw=meld_tw,
                            compact=True,
                        ).pack(side="left", padx=0)
                    row_used += est
            self._last_meld_key = meld_key

        if not disc_ok or force:
            self._clear(self.disc_fr)
            self._disc_tile_widgets = []
            if discs and disc_grid is not None:
                self._pack_tiles_wrapped(
                    self.disc_fr,
                    disc_ids,
                    tw=disc_grid.tw,
                    per_row=disc_grid.per_row,
                    clickable=False,
                    start_label="弃牌",
                )
                # Collect face labels for next inplace update
                self._disc_tile_widgets = self._collect_face_labels(self.disc_fr)
                self._disc_layout_key = (
                    len(disc_ids),
                    int(disc_grid.tw),
                    int(disc_grid.per_row),
                )
            else:
                self._disc_layout_key = (0, 0, 0)

        # Opp HUD
        if (
            force
            or opp_struct_fp != self._last_opp_struct_fp
            or not self._opp_cell_labels
        ):
            self._clear(self.opp_fr)
            self._draw_opponent_hud(opp_rows, cw)
        elif opp_values_fp != self._last_opp_values_fp:
            self._update_opponent_hud_inplace(opp_rows)

        self._last_tiles_fp = tiles_fp
        self._last_opp_struct_fp = opp_struct_fp
        self._last_opp_values_fp = opp_values_fp
        self._last_sel_fp = tuple(int(x) for x in self.selected)
        self._last_layout_cw = cw
        self._first_layout_done = True

        self._rebuild_action_bar(force=force)
        # Refresh scrollregion only after a real tile rebuild (not every obs)
        try:
            self.mid.update_idletasks()
            self.mid_canvas.configure(scrollregion=self.mid_canvas.bbox("all"))
            cw_c = int(self.mid_canvas.winfo_width())
            if cw_c > 1:
                self.mid_canvas.itemconfigure(self._mid_win, width=cw_c)
                self._cached_content_w = max(100, cw_c - 4)
        except Exception:
            pass

    def _collect_face_labels(self, root_fr) -> list:
        """Collect tile face Labels under a strip (for discard inplace pool)."""
        out: list = []

        def _walk(w) -> None:
            try:
                kids = list(w.winfo_children())
            except Exception:
                return
            for c in kids:
                if hasattr(c, "_base_tw") and hasattr(c, "_tid"):
                    out.append(c)
                else:
                    _walk(c)

        _walk(root_fr)
        return out

    def _rebuild_action_bar(self, *, force: bool = False) -> None:
        """Clear and redraw bottom action buttons (skip if unchanged)."""
        fp = self._action_fingerprint()
        if not force and fp == self._last_action_fp and self.btn_fr.winfo_children():
            return
        self._last_action_fp = fp

        for w in list(self.btn_fr.winfo_children()):
            try:
                w.destroy()
            except Exception:
                pass
        self._btn_widgets = []

        # Ready confirm applies to **both** human and AI watch seats (F0004).
        # Must run before the watch-only early return, or AI never sees the button.
        if self.awaiting_ready and not self._ready_sent:
            self._draw_ready_controls()
            return

        if self.mode != "play":
            msg = (
                "只读观战 — 等待「开始确认」…"
                if not self.awaiting_ready
                else "只读观战 — 请点确认开始"
            )
            self._draw_action_row(msg, [], on_click=lambda _k: None)
            return

        self._draw_action_buttons()

    def _action_pad(self) -> tuple[int, int, int]:
        """(padx, pady, gap) for single-row compact buttons."""
        sc = getattr(self, "_seat_scale", None)
        if sc is None:
            return 4, 1, 3
        padx = max(2, min(6, sc.pad + 1))
        pady = max(0, min(2, sc.pad // 3))
        gap = max(2, min(6, sc.gap + 1))
        return padx, pady, gap

    def _action_btn_font(self):
        """Font for action buttons (single row)."""
        try:
            from tkinter import font as tkfont

            fam = getattr(self, "_ui_family", None) or self._font.actual("family")
            sz = int(self._font.actual("size") or 9)
            sz = max(7, min(10, sz))
            key = f"_font_btn_{sz}"
            f = getattr(self, key, None)
            if f is None:
                f = tkfont.Font(family=fam, size=sz)
                setattr(self, key, f)
            return f
        except Exception:
            return self._font

    def _action_strip_width(self) -> int:
        try:
            w = int(self.play_actions_fr.winfo_width() or 0)
            if w < 80:
                li = getattr(self, "_last_interior_li", None)
                w = int(li.op_play.w) if li is not None else self._content_width()
            return max(120, w)
        except Exception:
            return max(120, self._content_width())

    def _draw_action_row(
        self,
        hint: str,
        keys: list[tuple[str, Any]],
        *,
        on_click,
        left_extra=None,
    ) -> None:
        """
        Single-row strip: left 50% Chinese hint (left-aligned),
        right 50% buttons with even width/gap by count.
        """
        strip_w = self._action_strip_width()
        half = strip_w // 2
        pad = 2
        left = self.tk.Frame(self.btn_fr, bg="#0c1c16")
        right = self.tk.Frame(self.btn_fr, bg="#0c1c16")
        left.place(x=0, y=0, relheight=1.0, width=half)
        right.place(x=half, y=0, relheight=1.0, width=max(40, strip_w - half))

        btn_font = self._action_btn_font()
        # Left: text left-aligned, vertically centered via pack expand
        text_fr = self.tk.Frame(left, bg="#0c1c16")
        text_fr.pack(side="left", fill="both", expand=True, padx=(4, 2))
        self.tk.Label(
            text_fr,
            text=hint or " ",
            bg="#0c1c16",
            fg="#fff0a0",
            font=btn_font,
            anchor="w",
            justify="left",
        ).pack(side="left", fill="x", expand=True, anchor="w")

        if left_extra is not None:
            try:
                left_extra(text_fr)
            except Exception:
                pass

        n = len(keys)
        if n <= 0:
            self.tk.Label(
                right,
                text="",
                bg="#0c1c16",
            ).pack(fill="both", expand=True)
            return

        right_w = max(40, strip_w - half)
        # Even gaps: n buttons → (n+1) outer/inner gaps, prefer small fixed then remainder
        gap = max(2, min(8, right_w // max(12, n * 4)))
        inner = right_w - pad * 2 - gap * (n + 1)
        btn_w = max(28, inner // n)
        # residual gap distribute
        used = n * btn_w + (n + 1) * gap + pad * 2
        if used > right_w and n > 0:
            btn_w = max(24, (right_w - pad * 2 - gap * (n + 1)) // n)

        row = self.tk.Frame(right, bg="#0c1c16")
        row.pack(side="left", fill="both", expand=True, padx=pad, pady=1)
        # left spacer for first gap
        self.tk.Frame(row, bg="#0c1c16", width=gap).pack(side="left")
        padx_btn = max(1, min(4, btn_w // 10))
        for label, key in keys:
            cell = self.tk.Frame(row, bg="#0c1c16", width=btn_w, height=22)
            cell.pack(side="left", padx=(0, gap))
            cell.pack_propagate(False)
            b = self._make_colored_button(
                cell,
                str(label),
                command=lambda k=key: on_click(k),
                bg="#287848",
                fg="white",
                active_bg="#36a060",
                font=btn_font,
                padx=padx_btn,
                pady=0,
                width=None,
            )
            b.place(relx=0.5, rely=0.5, anchor="center")

    def _draw_ready_controls(self) -> None:
        """Single-row ready UI: left text, right checkbox + confirm."""
        role = "AI 观战" if self.mode != "play" else "人类操作"
        hint = f"第 {self.ready_round}/{self.num_rounds} 局 · {role}：请确认开始"
        self.auto_var.set(bool(self.auto_start))

        def _extra(text_fr) -> None:
            pass

        # Build right-side as pseudo-keys using custom draw
        strip_w = self._action_strip_width()
        half = strip_w // 2
        left = self.tk.Frame(self.btn_fr, bg="#0c1c16")
        right = self.tk.Frame(self.btn_fr, bg="#0c1c16")
        left.place(x=0, y=0, relheight=1.0, width=half)
        right.place(x=half, y=0, relheight=1.0, width=max(40, strip_w - half))
        btn_font = self._action_btn_font()
        self.tk.Label(
            left,
            text=hint,
            bg="#0c1c16",
            fg="#fff0a0",
            font=btn_font,
            anchor="w",
            justify="left",
        ).pack(side="left", fill="both", expand=True, padx=4)

        row = self.tk.Frame(right, bg="#0c1c16")
        row.pack(fill="both", expand=True, padx=2, pady=1)
        cb = self.tk.Checkbutton(
            row,
            text="自动",
            variable=self.auto_var,
            bg="#0c1c16",
            fg="#f0f5e6",
            selectcolor="#1e3c28",
            activebackground="#0c1c16",
            font=btn_font,
            cursor="hand2",
            command=self._on_auto_toggle,
        )
        cb.pack(side="left", padx=(2, 4))
        btn = self._make_colored_button(
            row,
            "确认开始",
            command=self._on_ready_click,
            bg="#288250",
            fg="white",
            active_bg="#36a060",
            font=btn_font,
            padx=4,
            pady=0,
            width=None,
        )
        btn.pack(side="left", padx=2, fill="y")

    def _draw_action_buttons(self) -> None:
        from engine.action import ActionType

        phase = self.phase
        legal = self.legal
        keys: list[tuple[str, Any]] = []
        if phase == "dingque":
            keys = [("万", "wan"), ("筒", "tong"), ("条", "tiao")]
        elif phase == "exchange":
            keys = [("确认换牌", "confirm_exchange"), ("自动三张", "auto_exchange")]
        else:
            type_set = {a.type for a in legal}
            mapping = [
                ("胡", ActionType.HU),
                ("碰", ActionType.PONG),
                ("明杠", ActionType.GANG_MING),
                ("暗杠", ActionType.GANG_AN),
                ("加杠", ActionType.GANG_JIA),
            ]
            for label, typ in mapping:
                if typ in type_set:
                    keys.append((label, typ))
            if ActionType.PASS in type_set and any(
                a.type != ActionType.PASS for a in legal
            ):
                keys.append(("过", ActionType.PASS))

        hint = ""
        if phase == "exchange":
            hint = f"换三张：已选 {len(self.selected)}/3 同花色"
        elif phase == "discard" and any(
            getattr(a, "type", None) == ActionType.DISCARD for a in legal
        ):
            n_rec = len(self._recommendations or []) if self.recommend_marks_enabled else 0
            if n_rec:
                hint = f"出牌：双击手牌 · 推荐 {n_rec} 张"
            else:
                hint = "出牌：双击手牌打出"
        elif phase == "response":
            hint = "可碰/杠/胡：点右侧按钮"
        elif phase == "dingque":
            hint = "定缺：选择 万 / 筒 / 条"
        else:
            hint = f"等待操作… {phase}"

        if not keys:
            self._draw_action_row(hint, [], on_click=lambda _k: None)
            return

        self._draw_action_row(
            hint,
            keys,
            on_click=lambda k: self._on_button(k),
        )

    def _build_exchange_action(self, *, auto: bool) -> Any | None:
        """Build EXCHANGE from selection or engine legal / auto pick."""
        from engine.action import Action, ActionType
        from engine.tile import parse_tile

        if not auto and len(self.selected) == 3:
            try:
                tids = []
                for idx in self.selected:
                    i = int(idx)
                    if 0 <= i < len(self.hand_ids):
                        tids.append(self.hand_ids[i])
                tiles = tuple(parse_tile(t) for t in tids)
                if len(tiles) == 3 and len({t.suit for t in tiles}) == 1:
                    return Action(ActionType.EXCHANGE, tiles=tiles)
            except Exception as e:
                try:
                    sys.stderr.write(f"[seat_window] exchange select fail: {e}\n")
                    sys.stderr.flush()
                except Exception:
                    pass

        for a in self.legal:
            if getattr(a, "type", None) == ActionType.EXCHANGE and len(a.tiles) == 3:
                return a

        # Last resort: pick from current hand
        if self.hand_ids:
            try:
                from engine.exchange import pick_same_suit_triple
                from engine.tile import parse_tile as pt

                hand = [pt(t) for t in self.hand_ids]
                triple = pick_same_suit_triple(hand)
                return Action(ActionType.EXCHANGE, tiles=tuple(triple))
            except Exception as e:
                try:
                    sys.stderr.write(f"[seat_window] auto triple fail: {e}\n")
                    sys.stderr.flush()
                except Exception:
                    pass
        return None

    def _on_button(self, key) -> None:
        from engine.action import Action, ActionType
        from engine.tile import Suit

        try:
            sys.stderr.write(
                f"[seat_window] button seat={self.seat} key={key!r} "
                f"phase={self.phase} pending={self.pending_req is not None} "
                f"sel={self.selected}\n"
            )
            sys.stderr.flush()
        except Exception:
            pass

        if self.mode != "play":
            return
        if self.pending_req is None:
            self.status_note = "尚未收到操作请求，请稍候…"
            self._refresh_chrome()
            return

        phase = self.phase
        legal = self.legal

        if phase == "dingque" and key in ("wan", "tong", "tiao"):
            self._submit(Action(ActionType.DINGQUE, suit=Suit(key)))
            return

        if key in ("confirm_exchange", "auto_exchange"):
            auto = key == "auto_exchange"
            act = self._build_exchange_action(auto=auto)
            if act is not None:
                self._submit(act)
            else:
                self.status_note = (
                    f"请先点选 3 张【同一花色】手牌（已选 {len(self.selected)}/3），"
                    f"或点「自动三张」"
                )
                self._refresh_chrome()
            return

        for a in legal:
            try:
                if a.type == key or a.type.value == getattr(key, "value", str(key)):
                    self._submit(a)
                    return
            except Exception:
                continue
            try:
                if isinstance(key, ActionType) and a.type == key:
                    self._submit(a)
                    return
            except Exception:
                continue

        self.status_note = f"无法执行: {key}"
        self._refresh_chrome()

    def _on_tile_click(self, tid: str, hand_index: int | None = None) -> None:
        from engine.action import Action, ActionType
        from engine.tile import parse_tile

        if self.mode != "play" or self.awaiting_ready:
            return
        # Resolve index: prefer explicit hand_index (duplicate-safe)
        idx: int | None = None
        if hand_index is not None:
            try:
                idx = int(hand_index)
            except Exception:
                idx = None
        if idx is None:
            # fallback: first matching id (legacy)
            try:
                idx = self.hand_ids.index(str(tid))
            except ValueError:
                idx = None
        if idx is not None and (idx < 0 or idx >= len(self.hand_ids)):
            idx = None
        tid_s = str(self.hand_ids[idx]) if idx is not None else str(tid)

        now = time.time()
        # Double-click discard (match same hand index when possible)
        same_click = (
            tid_s == self._last_tile_click_tid
            and (
                self._last_tile_click_idx is None
                or idx is None
                or idx == self._last_tile_click_idx
            )
        )
        if (
            self.phase == "discard"
            and self.pending_req is not None
            and same_click
            and (now - self._last_tile_click_t) * 1000 <= 400
        ):
            act = None
            for a in self.legal:
                if a.type == ActionType.DISCARD and a.tiles and a.tiles[0].id == tid_s:
                    act = a
                    break
            if act is None and any(a.type == ActionType.DISCARD for a in self.legal):
                try:
                    act = Action(ActionType.DISCARD, tiles=(parse_tile(tid_s),))
                except Exception:
                    act = None
            self._last_tile_click_tid = None
            self._last_tile_click_idx = None
            if act is not None:
                self._submit(act)
            else:
                self.status_note = "该牌当前不可出"
                self._refresh_chrome()
            return

        self._last_tile_click_tid = tid_s
        self._last_tile_click_idx = idx
        self._last_tile_click_t = now

        if self.phase == "exchange":
            if idx is None:
                self.status_note = "无法定位手牌位置"
                self._refresh_chrome()
                return
            if idx in self.selected:
                self.selected = [x for x in self.selected if int(x) != idx]
            elif len(self.selected) < 3:
                if self.selected:
                    try:
                        first_i = int(self.selected[0])
                        s0 = parse_tile(self.hand_ids[first_i]).suit
                        if parse_tile(tid_s).suit != s0:
                            self.status_note = "换三张必须同一花色（万/筒/条）"
                            self._refresh_chrome()
                            self._apply_hand_selection_styles()
                            return
                    except Exception:
                        pass
                self.selected.append(idx)
            else:
                self.status_note = "已选满 3 张，可点「确认换牌」"
            labels = [
                self.hand_ids[int(i)]
                for i in self.selected
                if 0 <= int(i) < len(self.hand_ids)
            ]
            self.status_note = (
                f"换三张已选 {len(self.selected)}/3：{', '.join(labels)}"
            )
            self._refresh_chrome()
            self._apply_hand_selection_styles()
            self._last_sel_fp = tuple(int(x) for x in self.selected)
            self._rebuild_action_bar(force=False)
            return

        # discard / other: single-select by index
        self.selected = [idx] if idx is not None else []
        if self.phase == "discard":
            self.status_note = f"已选 {tid_s}，再点一次（双击）打出"
        # Only chrome text + in-place selection/ukeire (no full tile rebuild)
        self._refresh_chrome()
        self._apply_hand_selection_styles()
        self._last_sel_fp = tuple(int(x) for x in self.selected)

    def _submit(self, act) -> None:
        if self.pending_req is None:
            self.status_note = "提交失败：无待处理请求"
            self._refresh_chrome()
            return
        rid = self.pending_req.request_id
        self.emit_decision(act, rid)
        self.pending_req = None
        self.legal = []
        self.selected = []
        # If this was a HU, show blood-battle continue immediately (don't wait
        # for obs — parent continues AI seats right away).
        from engine.action import ActionType as _AT

        if getattr(act, "type", None) == _AT.HU:
            self.status_note = "已胡牌 · 血战继续（其他玩家行牌中）…"
            # Immediate banner even before next observation arrives
            try:
                self._show_self_hu_banner(
                    {
                        "hu_order": None,
                        "last_win": {},
                    }
                )
                self.hu_banner.config(
                    text=(
                        "★★★  本座已胡！血战继续  ★★★\n"
                        "本窗转为观战 — 其余玩家继续摸打"
                    ),
                    bg="#b71c1c",
                    fg="#fff59d",
                )
            except Exception as e:
                print(f"[seat_window] immediate hu banner: {e}")
        else:
            self.status_note = "已提交，等待…"
        # Lightweight chrome update first so UI stays responsive while
        # observations stream in (avoids looking like the program froze).
        self._refresh_chrome()
        try:
            self.root.after(0, lambda: self._render_state(force=False))
        except Exception:
            self._render_state(force=False)

    def _try_auto_pass(self) -> None:
        from engine.action import ActionType

        if self.mode != "play" or self.pending_req is None:
            return
        if not self.legal or not all(a.type == ActionType.PASS for a in self.legal):
            return
        pass_act = next(a for a in self.legal if a.type == ActionType.PASS)
        self.emit_decision(
            pass_act, self.pending_req.request_id, reason="human:auto_pass"
        )
        self.pending_req = None
        self.legal = []
        self.selected = []
        self.status_note = "自动过牌…"
        self._render_state()

    def handle_msg(self, msg: dict) -> None:
        from protocols.wire import parse_action_request, parse_observation

        mtype = msg.get("type")
        if mtype == "shutdown":
            self.running = False
            self.root.after(0, self._on_close)
            return
        if mtype == "set_geometry":
            try:
                x = int(msg.get("x", 0))
                y = int(msg.get("y", 0))
                w = int(msg.get("w", 400))
                h = int(msg.get("h", 300))
            except (TypeError, ValueError):
                return
            self.root.after(0, lambda: self._apply_geometry(x, y, w, h))
            return
        if mtype == "ready_request":
            self.ready_round = int(msg.get("round") or 1)
            try:
                self.num_rounds = max(1, int(msg.get("num_rounds") or 1))
            except (TypeError, ValueError):
                self.num_rounds = 1
            try:
                sys.stderr.write(
                    f"[seat_window] ready_request seat={self.seat} "
                    f"round={self.ready_round}/{self.num_rounds} mode={self.mode} "
                    f"auto={self.auto_start}\n"
                )
                sys.stderr.flush()
            except Exception:
                pass
            try:
                self.root.after(
                    0,
                    lambda: self.round_lbl.config(
                        text=format_round_line(self.ready_round, self.num_rounds)
                    ),
                )
            except Exception:
                pass
            # Always rebuild ready UI on mainloop tick
            self.root.after(0, self._show_ready)
            return
        if mtype == "observation":
            try:
                self.last_obs = parse_observation(msg)
                if self.mode != "play":
                    try:
                        raw = msg if isinstance(msg, dict) else {}
                        payload = raw.get("observation") or raw.get("payload") or raw
                        if isinstance(payload, dict):
                            self._update_ai_log_from_obs(payload)
                    except Exception:
                        pass
                if self.pending_req is None and not self.awaiting_ready:
                    self.phase = self.last_obs.phase
                    self.status_note = (
                        f"已同步 game={str(self.last_obs.game_id)[:16]}…"
                    )
                # Debounce high-frequency obs to avoid destroy/rebuild flicker
                self._schedule_render(force=False)
                # One-time width measure after first paint only
                if not self._first_layout_done:
                    try:
                        self.root.after(80, self._force_relayout)
                    except Exception:
                        pass
            except Exception as e:
                self.status_note = f"observation 解析失败: {e}"
                self._refresh_chrome()
            return
        if mtype == "action_request":
            if self.mode != "play":
                return
            try:
                self.pending_req, self.pending_hints = parse_action_request(msg)
                self.legal = list(self.pending_req.legal_actions)
                self.phase = str(self.pending_req.phase)
                self.selected = []
                self._last_tile_click_tid = None
                self._last_tile_click_idx = None
                self._sync_recommendations_from_hints()
                if self.phase == "exchange":
                    self.status_note = (
                        "【换三张】点选手牌 3 张同花色 →「确认换牌」或「自动三张」"
                    )
                elif self.phase == "dingque":
                    self.status_note = "【定缺】点 万 / 筒 / 条"
                elif self.phase == "discard":
                    n_rec = len(self._recommendations or [])
                    if n_rec and self.recommend_marks_enabled:
                        self.status_note = (
                            f"【出牌】双击手牌打出 · 推荐标记 {n_rec} 张"
                            "（序号=优先序；听牌张点选可见进张）"
                        )
                    else:
                        self.status_note = "【出牌】双击手牌打出"
                elif self.phase == "response":
                    self.status_note = "【响应】碰/杠/胡 或 过"
                else:
                    self.status_note = f"请操作: {self.phase}"
                try:
                    sys.stderr.write(
                        f"[seat_window] action_request seat={self.seat} "
                        f"phase={self.phase} legal={len(self.legal)} "
                        f"rec={len(self._recommendations or [])}\n"
                    )
                    sys.stderr.flush()
                except Exception:
                    pass
                # Prefer fingerprint rebuild (rec_key in tiles_fp) — avoid force
                # full wipe when hand tiles unchanged (anti-flicker).
                self._render_state(force=False)
                self._rebuild_action_bar(force=True)
                self._try_auto_pass()
            except Exception as e:
                self.status_note = f"action_request 解析失败: {e}"
                try:
                    sys.stderr.write(f"[seat_window] action_request err: {e}\n")
                    sys.stderr.flush()
                except Exception:
                    pass
                self._refresh_chrome()
            return
        if mtype == "game_end":
            self.phase = "game_end"
            self.status_note = "本局结束 — 下一局需再次确认开始"
            self.awaiting_ready = False
            self._ready_sent = False
            self.pending_req = None
            self.pending_hints = None
            self._recommendations = []
            self.legal = []
            self._hide_ready_banner()
            self._render_state()
            return
        if mtype == "error":
            self.status_note = f"错误: {msg.get('message')}"
            self._refresh_chrome()

    def _poll(self) -> None:
        if not self.running:
            return
        from protocols.wire import decode_line

        for line in _drain_stdin_lines():
            try:
                msg = decode_line(line)
            except Exception:
                continue
            try:
                self.handle_msg(msg)
            except Exception as e:
                self.status_note = f"处理消息异常: {e}"
                self._refresh_chrome()
            if not self.running:
                return
        try:
            self.root.after(40, self._poll)
        except Exception:
            self.running = False

    def run(self) -> int:
        try:
            self.root.mainloop()
        except Exception:
            pass
        return 0


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="Seat window (play or watch)")
    parser.add_argument("--seat", type=int, required=True)
    parser.add_argument("--mode", choices=["play", "watch"], default="play")
    parser.add_argument("--theme", default="green", choices=["green", "blue"])
    parser.add_argument("--title", default=None)
    parser.add_argument("--x", type=int, default=None)
    parser.add_argument("--y", type=int, default=None)
    parser.add_argument("--width", type=int, default=None)
    parser.add_argument("--height", type=int, default=None)
    parser.add_argument("--num-players", type=int, default=4)
    args = parser.parse_args(argv)

    seat = int(args.seat)
    mode = args.mode

    try:
        return _run_window(args, seat, mode)
    except SystemExit:
        raise
    except BaseException:
        tb = traceback.format_exc()
        path = _crash_log(seat, mode, tb)
        try:
            sys.stderr.write(f"[seat_window] CRASH seat={seat} mode={mode}\n{tb}\n")
            sys.stderr.write(f"[seat_window] log: {path}\n")
            sys.stderr.flush()
        except Exception:
            pass
        return 1


def _log(msg: str) -> None:
    try:
        sys.stderr.write(msg + "\n")
        sys.stderr.flush()
    except Exception:
        pass


def _run_window(args: argparse.Namespace, seat: int, mode: str) -> int:
    from protocols.wire import msg_hello, msg_window_ready

    # Hello ASAP (binary-safe emit)
    _safe_emit(msg_hello(seat, os.getpid()))
    _log(f"[seat_window] hello sent seat={seat} mode={mode}")

    # Geometry from CLI — keep this path free of heavy imports
    if args.width is not None and args.height is not None:
        ww, wh = max(320, int(args.width)), max(240, int(args.height))
        wx = int(args.x) if args.x is not None else 40
        wy = int(args.y) if args.y is not None else 40
        _log(f"[seat_window] geom from CLI {ww}x{wh}@({wx},{wy})")
    else:
        ww, wh, wx, wy = 480, 360, 40 + seat * 48, 40 + seat * 36
        try:
            from display.window_geometry import plan_for_screen

            plan = plan_for_screen(max(2, min(4, getattr(args, "num_players", 4) or 4)))
            default_rect = plan.players.get(seat, plan.main)
            ww, wh = max(320, default_rect.w), max(240, default_rect.h)
            wx, wy = default_rect.x, default_rect.y
            _log(f"[seat_window] geom from plan {ww}x{wh}@({wx},{wy})")
        except Exception as e:
            _log(f"[seat_window] plan_for_screen failed: {e}")
        if args.x is not None:
            wx = int(args.x)
        if args.y is not None:
            wy = int(args.y)

    ww, wh = max(320, int(ww)), max(240, int(wh))
    wx, wy = int(wx), int(wy)
    # Windows only: reject large negative Y (off-screen). macOS multi-mon keeps negative Y.
    if sys.platform == "win32":
        if wy < -50:
            wy = 40
        if wx < -4000:
            wx = 40

    role = "Human" if mode == "play" else "AI-Watch"
    title = args.title or f"CMJ {role} S{seat}"
    _log(f"[seat_window] creating Tk '{title}' {ww}x{wh}@({wx},{wy})")

    if sys.platform == "win32":
        # Windows: create Tk *before* stdin reader thread (otherwise tk.Tk() can hang).
        try:
            app = TkSeatApp(
                seat=seat,
                mode=mode,
                theme=args.theme,
                title=title,
                x=wx,
                y=wy,
                w=ww,
                h=wh,
            )
        except Exception as e:
            _log(f"[seat_window] TkSeatApp FAILED: {e}")
            raise
        _log(f"[seat_window] Tk mapped seat={seat}")
        try:
            _start_stdin_reader()
            _log("[seat_window] stdin reader started")
        except Exception as e:
            _log(f"[seat_window] stdin reader err: {e}")
        # Optional visible clamp (Windows-only helper; no-op on other platforms)
        try:
            from display.window_geometry import WindowRect, clamp_rect_to_visible

            c = clamp_rect_to_visible(WindowRect(wx, wy, ww, wh))
            if (c.x, c.y, c.w, c.h) != (wx, wy, ww, wh):
                wx, wy, ww, wh = c.x, c.y, c.w, c.h
                app._apply_geometry(wx, wy, ww, wh)
                _log(f"[seat_window] post-clamp {ww}x{wh}@({wx},{wy})")
        except Exception as e:
            _log(f"[seat_window] post-clamp skip: {e}")
    else:
        # macOS / Linux: original order — stdin reader first, then Tk
        try:
            _start_stdin_reader()
            _log("[seat_window] stdin reader started")
        except Exception as e:
            _log(f"[seat_window] stdin reader err: {e}")
        try:
            app = TkSeatApp(
                seat=seat,
                mode=mode,
                theme=args.theme,
                title=title,
                x=wx,
                y=wy,
                w=ww,
                h=wh,
            )
        except Exception as e:
            _log(f"[seat_window] TkSeatApp FAILED: {e}")
            raise
        _log(f"[seat_window] Tk mapped seat={seat}")

    # Report *actual* client size after map + reassert (for MAIN height match)
    try:
        app.root.update_idletasks()
        if hasattr(app, "_reassert_locked_size"):
            app._reassert_locked_size()
        app.root.update_idletasks()
        aw = int(app.root.winfo_width() or ww)
        ah = int(app.root.winfo_height() or wh)
        ax = int(getattr(app, "_geom_x", wx))
        ay = int(getattr(app, "_geom_y", wy))
        ww, wh, wx, wy = aw, ah, ax, ay
        _log(f"[seat_window] actual client {ww}x{wh}@({wx},{wy})")
    except Exception as e:
        _log(f"[seat_window] actual size probe skip: {e}")

    _safe_emit(msg_window_ready(seat, x=wx, y=wy, w=ww, h=wh, title=title))
    _log(f"[seat_window] window_ready seat={seat} {ww}x{wh}@({wx},{wy})")

    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
