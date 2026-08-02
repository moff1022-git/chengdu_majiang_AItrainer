"""
Window sizes and positions for main + seat player windows (F0001 / F0018 / F0020).

Design goals (UI_DESIGN_STANDARD v1.4+):
- Layout canvas = 85% of capped work area, centered
- MAIN 25% bottom-left (layout D: body grid); human full / AI 6.25%
- Modes A (1H3AI) / B (2H2AI) / C (0H4AI) / D (3H1AI)
- Windows remain RESIZABLE after open
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass
from typing import Literal

# Legacy F0001 hard cap (work_area / sanitize helpers)
MAX_WORK_W = 2560
MAX_WORK_H = 1440

# F0018 layout canvas cap (UI_DESIGN_STANDARD §3.1)
LAYOUT_CAP_W = 3840
LAYOUT_CAP_H = 2160
LAYOUT_AREA_RATIO = 0.85
_SQRT_LAYOUT = math.sqrt(LAYOUT_AREA_RATIO)

# 1080p complete-mode outer sizes = min AND max for default plan (do not enlarge)
# UI_DESIGN_STANDARD §8.2 1080p row; user: 完整模式尺寸为最小，请不要扩大
FULL_MAIN_W, FULL_MAIN_H = 885, 498
FULL_HUMAN_W, FULL_HUMAN_H = 885, 498
# AI original complete size (do NOT enlarge height — only reposition if needed)
FULL_AI_W, FULL_AI_H = 442, 249
# 1080p layout canvas used as size basis when real canvas is larger
FULL_CANVAS_W, FULL_CANVAS_H = 1770, 996
# Extra vertical pad between AI bottom and MAIN/human top (title bar / shadow)
DECORATION_PAD_Y = 28

# Title-bar / frame chrome (content vs outer). Plan (w,h) = **outer** frame
# for layout alignment; toolkits often size the **client** area.
# Empirically both pygame and Tk on macOS need the same client height so
# outer frames match; we subtract chrome when applying plan → client.
def platform_frame_chrome_y() -> int:
    if sys.platform == "darwin":
        return 28
    if sys.platform == "win32":
        return 31  # approximate SM_CYCAPTION + border
    return 0


def plan_to_client_size(w: int, h: int) -> tuple[int, int]:
    """
    Convert plan outer size to toolkit client size.

    Layout plan uses outer frames so MAIN and seat windows **look** the same
    height. Pygame ``set_mode`` and Tk ``geometry WxH`` both size the client
    (content) area on macOS/Windows; OS adds a title bar outside. Using the
    same client size for both keeps outer frames matched.
    """
    ww = max(160, int(w))
    hh = max(140, int(h))
    # Keep plan height as client height (same for pygame + Tk).
    # Outer ≈ client + chrome for both → equal outers when clients equal.
    return ww, hh


def plan_to_matched_client_size(w: int, h: int) -> tuple[int, int]:
    """Alias — both toolkits share identical client (w,h) from plan."""
    return plan_to_client_size(w, h)

# Preferred defaults (scaled down on small desktops)
BASE_MAIN_W = 960
BASE_MAIN_H = 540
BASE_PLAYER_W = 520
BASE_PLAYER_H = 340

MIN_MAIN_W, MIN_MAIN_H = 560, 340
MIN_PLAYER_W, MIN_PLAYER_H = 360, 260

GAP = 8
MARGIN = 8

Slot = Literal["bottom", "right", "top", "left"]
LayoutMode = Literal["A", "B", "C", "D"]

SEAT_TO_SLOT: dict[int, Slot] = {
    0: "bottom",
    1: "right",
    2: "top",
    3: "left",
}


@dataclass(frozen=True, slots=True)
class WindowRect:
    x: int
    y: int
    w: int
    h: int

    @property
    def right(self) -> int:
        return self.x + self.w

    @property
    def bottom(self) -> int:
        return self.y + self.h

    def as_tuple(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.w, self.h


@dataclass(frozen=True, slots=True)
class WindowPlan:
    work: WindowRect
    main: WindowRect
    players: dict[int, WindowRect]
    scale: float
    screen_w: int = 0
    screen_h: int = 0
    screen_source: str = ""
    layout_mode: str = ""
    canvas: WindowRect | None = None


@dataclass(frozen=True, slots=True)
class ScreenInfo:
    """
    Usable region of the *current* monitor (where the command was run).

    IMPORTANT: Do NOT call SetProcessDPIAware here. Parent and child
    pygame processes must share the same coordinate space (typically
    Windows *logical* pixels).
    """

    width: int
    height: int
    source: str  # win32_console | win32_foreground | win32_cursor | win32_primary | ...
    origin_x: int = 0
    origin_y: int = 0
    monitor_index: int = -1  # best-effort enumeration index, -1 unknown


def _win32_monitor_work_from_handle(hmonitor) -> tuple[int, int, int, int] | None:
    """Return (left, top, width, height) of monitor work area, or None."""
    import ctypes

    class RECT(ctypes.Structure):
        _fields_ = [
            ("left", ctypes.c_long),
            ("top", ctypes.c_long),
            ("right", ctypes.c_long),
            ("bottom", ctypes.c_long),
        ]

    class MONITORINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_ulong),
            ("rcMonitor", RECT),
            ("rcWork", RECT),
            ("dwFlags", ctypes.c_ulong),
        ]

    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(MONITORINFO)
    ok = ctypes.windll.user32.GetMonitorInfoW(hmonitor, ctypes.byref(mi))  # type: ignore[attr-defined]
    if not ok:
        return None
    left = int(mi.rcWork.left)
    top = int(mi.rcWork.top)
    right = int(mi.rcWork.right)
    bottom = int(mi.rcWork.bottom)
    w, h = right - left, bottom - top
    if w < 320 or h < 240:
        return None
    return left, top, w, h


def _win32_monitor_index(hmonitor) -> int:
    """Enumerate monitors to assign a stable 0-based index (best-effort)."""
    import ctypes

    found = {"i": -1, "n": 0}
    try:
        CB = ctypes.WINFUNCTYPE(
            ctypes.c_int,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_void_p,
        )

        def _cb(hmon, _hdc, _lprc, _lp):  # type: ignore[no-untyped-def]
            try:
                if ctypes.cast(hmon, ctypes.c_void_p).value == ctypes.cast(
                    hmonitor, ctypes.c_void_p
                ).value:
                    found["i"] = found["n"]
            except Exception:
                if hmon == hmonitor:
                    found["i"] = found["n"]
            found["n"] += 1
            return 1

        ctypes.windll.user32.EnumDisplayMonitors(  # type: ignore[attr-defined]
            0, 0, CB(_cb), 0
        )
    except Exception:
        return -1
    return int(found["i"])


def _detect_screen_win32() -> ScreenInfo | None:
    """
    Detect the monitor where the CLI / user is currently working.

    Priority: console window → foreground window → cursor → primary monitor.
    """
    if sys.platform != "win32":
        return None
    import ctypes

    user32 = ctypes.windll.user32  # type: ignore[attr-defined]
    kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
    MONITOR_DEFAULTTONULL = 0
    MONITOR_DEFAULTTOPRIMARY = 1
    MONITOR_DEFAULTTONEAREST = 2

    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    hmon = None
    source = "win32_primary"

    # a) Console window (where the command was run)
    try:
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            hmon = user32.MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)
            if hmon:
                source = "win32_console"
    except Exception:
        hmon = None

    # b) Foreground window
    if not hmon:
        try:
            hwnd = user32.GetForegroundWindow()
            if hwnd:
                hmon = user32.MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)
                if hmon:
                    source = "win32_foreground"
        except Exception:
            hmon = None

    # c) Cursor position
    if not hmon:
        try:
            pt = POINT()
            if user32.GetCursorPos(ctypes.byref(pt)):
                hmon = user32.MonitorFromPoint(pt, MONITOR_DEFAULTTONEAREST)
                if hmon:
                    source = "win32_cursor"
        except Exception:
            hmon = None

    # d) Primary monitor
    if not hmon:
        try:
            # MonitorFromPoint(0,0) often primary on left-origin layouts
            pt = POINT(0, 0)
            hmon = user32.MonitorFromPoint(pt, MONITOR_DEFAULTTOPRIMARY)
            source = "win32_primary"
        except Exception:
            hmon = None

    if not hmon:
        return None

    work = _win32_monitor_work_from_handle(hmon)
    if work is None:
        return None
    left, top, w, h = work
    idx = _win32_monitor_index(hmon)
    return ScreenInfo(
        width=w,
        height=h,
        source=source,
        origin_x=left,
        origin_y=top,
        monitor_index=idx,
    )


def _macos_menu_dock_insets(full_h: int) -> tuple[int, int]:
    """
    Return (menu_inset, dock_inset) in pixels for the main screen.

    Uses AppKit visibleFrame when available. Avoid calling this from pure-Tk
    seat children if it misbehaves; main/hub process is fine.
    """
    menu_default = 28 if full_h >= 600 else 0
    dock_default = 80 if full_h >= 800 else 0
    try:
        from AppKit import NSScreen  # type: ignore

        scr = NSScreen.mainScreen()
        if scr is None:
            return menu_default, dock_default
        full = scr.frame()
        vis = scr.visibleFrame()
        # Cocoa: origin bottom-left. Dock on bottom → vis.origin.y > 0.
        dock = max(0, int(round(float(vis.origin.y))))
        menu = max(
            0,
            int(
                round(
                    float(full.size.height)
                    - float(vis.size.height)
                    - float(vis.origin.y)
                )
            ),
        )
        if menu < 16:
            menu = menu_default
        # Visible frame can be zero dock when dock auto-hide
        if dock < 0:
            dock = 0
        if dock == 0 and full_h >= 800:
            # Still reserve a small pad so SDL does not fight the Dock
            dock = min(dock_default, 48)
        return menu, dock
    except Exception:
        return menu_default, dock_default


def _screen_info_from_bounds(
    *,
    left: float,
    top: float,
    full_w: float,
    full_h: float,
    source: str,
    idx: int,
) -> ScreenInfo | None:
    """Build ScreenInfo with menu-bar + dock insets from full display bounds."""
    w = int(round(full_w))
    h = int(round(full_h))
    if w < 640 or h < 480:
        return None
    ox = int(round(left))
    oy = int(round(top))
    menu_inset, dock_inset = _macos_menu_dock_insets(h)
    if sys.platform != "darwin":
        menu_inset = 28 if h >= 600 else 0
        dock_inset = 0
    work_top = oy + menu_inset
    work_h = h - menu_inset - dock_inset
    if work_h < 480:
        work_top = oy
        work_h = max(480, h - menu_inset)
    return ScreenInfo(
        width=w,
        height=work_h,
        source=source,
        origin_x=ox,
        origin_y=work_top,
        monitor_index=idx,
    )


def _list_screens_macos() -> list[ScreenInfo]:
    """
    Enumerate displays via CoreGraphics (no AppKit/NSApplication).

    Do **not** call NSApplication.sharedApplication here — it breaks Tk in the
    same process (and seat_window is pure Tk). CGDisplayBounds matches Tk
    global top-left coordinates on modern macOS.
    """
    if sys.platform != "darwin":
        return []
    import ctypes
    import ctypes.util

    lib_name = ctypes.util.find_library("CoreGraphics")
    if not lib_name:
        return []
    cg = ctypes.CDLL(lib_name)

    class CGPoint(ctypes.Structure):
        _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]

    class CGSize(ctypes.Structure):
        _fields_ = [("width", ctypes.c_double), ("height", ctypes.c_double)]

    class CGRect(ctypes.Structure):
        _fields_ = [("origin", CGPoint), ("size", CGSize)]

    max_displays = 16
    DisplayID = ctypes.c_uint32
    displays = (DisplayID * max_displays)()
    count = ctypes.c_uint32(0)
    cg.CGGetActiveDisplayList.argtypes = [
        ctypes.c_uint32,
        ctypes.POINTER(DisplayID),
        ctypes.POINTER(ctypes.c_uint32),
    ]
    cg.CGGetActiveDisplayList.restype = ctypes.c_int32
    if cg.CGGetActiveDisplayList(max_displays, displays, ctypes.byref(count)) != 0:
        return []
    if count.value <= 0:
        return []

    cg.CGDisplayBounds.argtypes = [DisplayID]
    cg.CGDisplayBounds.restype = CGRect
    cg.CGMainDisplayID.argtypes = []
    cg.CGMainDisplayID.restype = DisplayID
    main_id = int(cg.CGMainDisplayID())

    out: list[ScreenInfo] = []
    for i in range(int(count.value)):
        did = int(displays[i])
        b = cg.CGDisplayBounds(DisplayID(did))
        src = "macos_main" if did == main_id else f"macos_display_{i}"
        info = _screen_info_from_bounds(
            left=float(b.origin.x),
            top=float(b.origin.y),
            full_w=float(b.size.width),
            full_h=float(b.size.height),
            source=src,
            idx=i,
        )
        if info is not None:
            out.append(info)
    return out


def format_tk_geometry(w: int, h: int, x: int, y: int) -> str:
    """
    Tk geometry with absolute signed coordinates for multi-monitor.

    Critical: ``f\"{w}x{h}+{x}+{y}\"`` with y=-20 yields ``...+10+-20`` (good).
    Using ``%+d`` alone can yield ``...+10-20`` which means “20px from bottom”.
    """
    ww = max(160, int(w))
    hh = max(140, int(h))
    xx = int(x)
    yy = int(y)
    return f"{ww}x{hh}+{xx}+{yy}"


def list_monitor_work_areas() -> list[WindowRect]:
    """All monitor work areas in virtual-screen coordinates (Windows)."""
    if sys.platform != "win32":
        sc = detect_screen()
        return [WindowRect(sc.origin_x, sc.origin_y, sc.width, sc.height)]
    try:
        import ctypes

        user32 = ctypes.windll.user32  # type: ignore[attr-defined]

        class RECT(ctypes.Structure):
            _fields_ = [
                ("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long),
            ]

        class MONITORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_ulong),
                ("rcMonitor", RECT),
                ("rcWork", RECT),
                ("dwFlags", ctypes.c_ulong),
            ]

        out: list[WindowRect] = []

        @ctypes.WINFUNCTYPE(
            ctypes.c_int,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.POINTER(RECT),
            ctypes.c_void_p,
        )
        def _cb(hmon, _hdc, _lprc, _lp):  # type: ignore[no-untyped-def]
            mi = MONITORINFO()
            mi.cbSize = ctypes.sizeof(MONITORINFO)
            if user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
                w = int(mi.rcWork.right - mi.rcWork.left)
                h = int(mi.rcWork.bottom - mi.rcWork.top)
                if w >= 200 and h >= 160:
                    out.append(
                        WindowRect(
                            int(mi.rcWork.left),
                            int(mi.rcWork.top),
                            w,
                            h,
                        )
                    )
            return 1

        user32.EnumDisplayMonitors(0, 0, _cb, 0)
        if out:
            return out
    except Exception:
        pass
    sc = detect_screen()
    return [WindowRect(sc.origin_x, sc.origin_y, sc.width, sc.height)]


def clamp_rect_to_visible(rect: WindowRect) -> WindowRect:
    """
    Ensure a window rect is fully inside some monitor work area.

    **Windows only.** macOS keeps global multi-display coords (negative Y is
    valid) and must not be rewritten here.
    """
    if sys.platform != "win32":
        return rect
    areas = list_monitor_work_areas()
    if not areas:
        return rect
    w = max(160, min(int(rect.w), max(a.w for a in areas) - 16))
    h = max(140, min(int(rect.h), max(a.h for a in areas) - 16))
    x, y = int(rect.x), int(rect.y)

    def _inside(a: WindowRect) -> bool:
        # center of rect on this monitor?
        cx = x + w // 2
        cy = y + h // 2
        return a.x <= cx < a.x + a.w and a.y <= cy < a.y + a.h

    target = next((a for a in areas if _inside(a)), None)
    if target is None:
        # Prefer primary-like (origin closest to 0,0) then largest
        target = min(
            areas,
            key=lambda a: (abs(a.x) + abs(a.y), -(a.w * a.h)),
        )
        x = target.x + 8
        y = target.y + 8
    # Clamp into target work area
    x = min(max(x, target.x), target.x + target.w - w)
    y = min(max(y, target.y), target.y + target.h - h)
    return WindowRect(x, y, w, h)


def sanitize_window_plan(plan: WindowPlan) -> WindowPlan:
    """Clamp main + every seat into visible monitor work areas (Windows only)."""
    if sys.platform != "win32":
        return plan
    main = clamp_rect_to_visible(plan.main)
    players = {s: clamp_rect_to_visible(r) for s, r in plan.players.items()}
    return WindowPlan(
        work=plan.work,
        main=main,
        players=players,
        scale=plan.scale,
        screen_w=plan.screen_w,
        screen_h=plan.screen_h,
        screen_source=plan.screen_source,
        layout_mode=plan.layout_mode,
        canvas=plan.canvas,
    )


def _detect_screen_macos() -> ScreenInfo | None:
    """
    Detect the display under the mouse cursor via CoreGraphics (no PyObjC).

    Work area ≈ full display bounds with a small top inset for the menu bar.
    Dock is not subtracted (best-effort; see F0005).
    """
    if sys.platform != "darwin":
        return None
    import ctypes
    import ctypes.util

    lib_name = ctypes.util.find_library("CoreGraphics")
    if not lib_name:
        return None
    cg = ctypes.CDLL(lib_name)

    class CGPoint(ctypes.Structure):
        _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]

    class CGSize(ctypes.Structure):
        _fields_ = [("width", ctypes.c_double), ("height", ctypes.c_double)]

    class CGRect(ctypes.Structure):
        _fields_ = [("origin", CGPoint), ("size", CGSize)]

    # Cursor location
    cg.CGEventCreate.argtypes = [ctypes.c_void_p]
    cg.CGEventCreate.restype = ctypes.c_void_p
    cg.CGEventGetLocation.argtypes = [ctypes.c_void_p]
    cg.CGEventGetLocation.restype = CGPoint

    event = cg.CGEventCreate(None)
    mx = my = None
    if event:
        try:
            pt = cg.CGEventGetLocation(event)
            mx, my = float(pt.x), float(pt.y)
        finally:
            try:
                cf_name = ctypes.util.find_library("CoreFoundation")
                if cf_name:
                    cf = ctypes.CDLL(cf_name)
                    cf.CFRelease.argtypes = [ctypes.c_void_p]
                    cf.CFRelease.restype = None
                    cf.CFRelease(event)
            except Exception:
                pass

    screens = _list_screens_macos()
    if not screens:
        return None

    # Map cursor → display (rebuild bounds from ScreenInfo + menu inset)
    if mx is not None and my is not None:
        for sc in screens:
            # Work area uses menu inset; match against full-ish vertical span
            left = sc.origin_x
            top = sc.origin_y - (28 if sc.height >= 572 else 0)
            right = left + sc.width
            bottom = top + sc.height + (28 if sc.height >= 572 else 0)
            if left <= mx < right and top <= my < bottom:
                return ScreenInfo(
                    width=sc.width,
                    height=sc.height,
                    source="macos_cursor",
                    origin_x=sc.origin_x,
                    origin_y=sc.origin_y,
                    monitor_index=sc.monitor_index,
                )

    for sc in screens:
        if sc.source == "macos_main":
            return sc
    return screens[0]


def is_landscape_screen(info: ScreenInfo) -> bool:
    """True when work area is landscape or near-square (suitable for 2×3 grid)."""
    return info.width * 1.05 >= info.height


def score_layout_screen(info: ScreenInfo) -> tuple:
    """
    Higher is better for the full main+4-seat grid.

    Prefer landscape, large area, primary, non-negative origin (stable desktop).
    """
    landscape = 1 if is_landscape_screen(info) else 0
    area = int(info.width) * int(info.height)
    primary = 1 if "main" in info.source or info.monitor_index == 0 else 0
    # Penalize displays that sit above the primary (negative Y) — common with
    # portrait secondaries and causes seats to appear "missing" on the laptop.
    non_neg_y = 1 if info.origin_y >= -40 else 0
    non_neg_x = 1 if info.origin_x >= -40 else 0
    return (landscape, non_neg_y, non_neg_x, primary, area)


def pick_layout_screen(
    candidates: list[ScreenInfo],
    *,
    preferred: ScreenInfo | None = None,
) -> ScreenInfo:
    """
    Choose the monitor for the full UI grid.

    Default: stay on the preferred/current screen (cursor, console, or main
    window). Only fall back to another candidate when preferred is missing or
    impossibly small.
    """
    if preferred is not None and preferred.width >= 640 and preferred.height >= 480:
        return preferred
    if not candidates:
        return preferred or ScreenInfo(1920, 1080, "default")
    return max(candidates, key=score_layout_screen)


def screen_containing_point(x: int, y: int) -> ScreenInfo | None:
    """Best-effort: which known monitor contains global point (x, y)."""
    screens: list[ScreenInfo] = []
    if sys.platform == "darwin":
        try:
            screens = _list_screens_macos()
        except Exception:
            screens = []
    if not screens:
        try:
            sc = detect_screen()
            screens = [sc]
        except Exception:
            return None
    for sc in screens:
        # Expand slightly for menu-bar inset so y just below top still matches
        left = sc.origin_x
        top = sc.origin_y - 40
        right = left + sc.width
        bottom = sc.origin_y + sc.height + 40
        if left <= x < right and top <= y < bottom:
            return ScreenInfo(
                width=sc.width,
                height=sc.height,
                source=f"{sc.source}+point",
                origin_x=sc.origin_x,
                origin_y=sc.origin_y,
                monitor_index=sc.monitor_index,
            )
    return None


def detect_main_window_screen() -> ScreenInfo | None:
    """
    Best-effort: monitor containing the main pygame window.

    On macOS we deliberately do **not** query ``pygame._sdl2`` (SEGV class).
    Returns None unless a safe API is available.
    """
    # Reading/writing pygame._sdl2.Window is unsafe on macOS pygame 2.6 —
    # even ``from_display_module()`` has been associated with later event-loop
    # SIGSEGV. Leave placement to SDL_VIDEO_WINDOW_POS only.
    return None


def detect_layout_screen(*, prefer_main: bool = False) -> ScreenInfo:
    """
    Screen for main + seat plan = **current cursor/console monitor**.

    Always follows ``detect_screen()`` so windows open on the screen the user
    is working on (including portrait secondaries). ``prefer_main`` is unused
    (main-window probe disabled on macOS for stability).
    """
    _ = prefer_main
    current = detect_screen()
    if current.width >= 640 and current.height >= 480:
        return current
    candidates: list[ScreenInfo] = []
    if sys.platform == "darwin":
        try:
            candidates = _list_screens_macos()
        except Exception:
            candidates = []
    if not candidates:
        return current if current.width >= 320 else ScreenInfo(1920, 1080, "default")
    return pick_layout_screen(candidates, preferred=current)


def _detect_screen_pygame() -> ScreenInfo | None:
    try:
        import pygame

        if not pygame.get_init():
            pygame.init()
        if not pygame.display.get_init():
            pygame.display.init()
        info = pygame.display.Info()
        if info.current_w > 0 and info.current_h > 0:
            return ScreenInfo(int(info.current_w), int(info.current_h), "pygame")
    except Exception:
        pass
    return None


def detect_screen() -> ScreenInfo:
    """
    Step 1: which monitor is the command on, and its work-area size/origin.

    Uses logical metrics so SDL_VIDEO_WINDOW_POS matches child processes.
    Platform dispatch (F0005): win32 / darwin / pygame / default.
    """
    if sys.platform == "win32":
        try:
            info = _detect_screen_win32()
            if info is not None and info.width >= 640 and info.height >= 480:
                return info
        except Exception:
            pass
        # Fallback: primary work area via SPI
        try:
            import ctypes

            class RECT(ctypes.Structure):
                _fields_ = [
                    ("left", ctypes.c_long),
                    ("top", ctypes.c_long),
                    ("right", ctypes.c_long),
                    ("bottom", ctypes.c_long),
                ]

            r = RECT()
            ok = ctypes.windll.user32.SystemParametersInfoW(  # type: ignore[attr-defined]
                0x0030, 0, ctypes.byref(r), 0
            )
            if ok:
                w = int(r.right - r.left)
                h = int(r.bottom - r.top)
                if w >= 640 and h >= 480:
                    return ScreenInfo(
                        w,
                        h,
                        "win32_workarea_primary",
                        origin_x=int(r.left),
                        origin_y=int(r.top),
                    )
            user32 = ctypes.windll.user32  # type: ignore[attr-defined]
            w = int(user32.GetSystemMetrics(0))
            h = int(user32.GetSystemMetrics(1))
            if w > 0 and h > 0:
                return ScreenInfo(w, h, "win32")
        except Exception:
            pass

    if sys.platform == "darwin":
        try:
            info = _detect_screen_macos()
            if info is not None and info.width >= 640 and info.height >= 480:
                return info
        except Exception:
            pass

    info = _detect_screen_pygame()
    if info is not None:
        return info
    return ScreenInfo(1920, 1080, "default")


def desktop_size() -> tuple[int, int]:
    info = detect_screen()
    return info.width, info.height


def work_area(
    desktop: tuple[int, int] | None = None,
    *,
    origin: tuple[int, int] = (0, 0),
) -> WindowRect:
    if desktop is None:
        sc = detect_screen()
        dw, dh = sc.width, sc.height
        ox0, oy0 = sc.origin_x, sc.origin_y
    else:
        dw, dh = int(desktop[0]), int(desktop[1])
        ox0, oy0 = origin
    # Cap to 2K; work area origin stays at monitor work-area origin
    ww = min(dw, MAX_WORK_W)
    wh = min(dh, MAX_WORK_H)
    # If capped smaller than desktop, center within the work region.
    # Use signed offsets (not max(0,…)) so secondary monitors with negative
    # global origin (macOS) keep the work rect fully on that display.
    ox = ox0 + max(0, (dw - ww) // 2)
    oy = oy0 + max(0, (dh - wh) // 2)
    # Portrait / tall monitors: top-aligned usable slice on *that* display
    # (still relative to oy0, which may be negative in global coords).
    if dh > dw * 1.2 and wh < dh:
        oy = oy0 + min(80, max(0, (dh - wh) // 8))
    return WindowRect(ox, oy, ww, wh)


def plan_for_screen(
    num_players: int = 4,
    *,
    screen: ScreenInfo | None = None,
    include_main: bool = True,
    prefer_layout: bool = True,
    human_seats: list[int] | None = None,
    layout_mode: str | None = "auto",
    scale: float = 1.0,
) -> WindowPlan:
    """
    Step 2 of full UI: one WindowPlan from detected screen for ALL windows.

    By default uses ``detect_layout_screen()`` (prefer landscape primary) so
    portrait secondaries do not own the grid. F0018: pass ``human_seats`` for A/B/C.
    """
    if screen is not None:
        sc = screen
    elif prefer_layout:
        sc = detect_layout_screen()
    else:
        sc = detect_screen()
    plan = compute_window_plan(
        num_players,
        include_main=include_main,
        desktop=(sc.width, sc.height),
        origin=(sc.origin_x, sc.origin_y),
        human_seats=human_seats,
        layout_mode=layout_mode,
        scale=scale,
    )
    out = WindowPlan(
        work=plan.work,
        main=plan.main,
        players=plan.players,
        scale=plan.scale,
        screen_w=sc.width,
        screen_h=sc.height,
        screen_source=sc.source,
        layout_mode=plan.layout_mode,
        canvas=plan.canvas,
    )
    # Windows live detect only: snap onto real monitor work areas.
    # Skip when caller passed an explicit ScreenInfo (unit tests / macOS fixtures).
    if sys.platform == "win32" and screen is None:
        return sanitize_window_plan(out)
    return out


def plan_to_dict(plan: WindowPlan) -> dict:
    def _r(r: WindowRect) -> dict:
        return {"x": r.x, "y": r.y, "w": r.w, "h": r.h}

    d = {
        "screen_w": plan.screen_w,
        "screen_h": plan.screen_h,
        "screen_source": plan.screen_source,
        "work": _r(plan.work),
        "main": _r(plan.main),
        "players": {str(s): _r(r) for s, r in plan.players.items()},
        "scale": plan.scale,
        "layout_mode": plan.layout_mode,
    }
    if plan.canvas is not None:
        d["canvas"] = _r(plan.canvas)
    return d


def rect_from_plan_dict(plan_dict: dict, seat: int) -> WindowRect | None:
    players = plan_dict.get("players") or {}
    raw = players.get(str(seat)) or players.get(seat)
    if not isinstance(raw, dict):
        return None
    try:
        return WindowRect(
            int(raw["x"]),
            int(raw["y"]),
            int(raw["w"]),
            int(raw["h"]),
        )
    except Exception:
        return None


def log_plan(plan: WindowPlan, prefix: str = "[display]") -> None:
    print(
        f"{prefix} monitor work {plan.screen_w}x{plan.screen_h} "
        f"@({plan.work.x},{plan.work.y}) via {plan.screen_source} "
        f"| main={plan.main.w}x{plan.main.h}@({plan.main.x},{plan.main.y})"
    )
    for s in sorted(plan.players):
        r = plan.players[s]
        print(f"{prefix}   seat{s}: {r.w}x{r.h}@({r.x},{r.y})")


def log_screen(info: ScreenInfo, prefix: str = "[display]") -> None:
    mon = f"#{info.monitor_index}" if info.monitor_index >= 0 else "?"
    print(
        f"{prefix} current monitor {mon}: "
        f"{info.width}x{info.height} origin=({info.origin_x},{info.origin_y}) "
        f"via {info.source}"
    )


def seat_slot(seat: int, num_players: int = 4) -> Slot:
    if num_players == 2:
        return "bottom" if seat == 0 else "top"
    if num_players == 3:
        return ("bottom", "right", "left")[seat % 3]
    return SEAT_TO_SLOT.get(seat % 4, "bottom")


# ---------------------------------------------------------------------------
# F0018 / UI_DESIGN_STANDARD v1.3 — multi-window outer geometry
# ---------------------------------------------------------------------------


def layout_canvas(
    W: int,
    H: int,
    *,
    origin: tuple[int, int] = (0, 0),
    cap_w: int = LAYOUT_CAP_W,
    cap_h: int = LAYOUT_CAP_H,
) -> WindowRect:
    """
    85% area canvas, centered in work W×H; work capped at 2160p before scale.

    Area ratio canvas/(Wc×Hc) ∈ [0.84, 0.86] with s=sqrt(0.85).
    """
    ox, oy = int(origin[0]), int(origin[1])
    W, H = max(1, int(W)), max(1, int(H))
    Wc = min(W, int(cap_w))
    Hc = min(H, int(cap_h))
    Lw = int(round(Wc * _SQRT_LAYOUT))
    Lh = int(round(Hc * _SQRT_LAYOUT))
    Lw = max(160, Lw)
    Lh = max(120, Lh)
    Ox_c = ox + (W - Lw) // 2
    Oy_c = oy + (H - Lh) // 2
    return WindowRect(Ox_c, Oy_c, Lw, Lh)


def window_sizes(Lw: int, Lh: int) -> dict[str, int | tuple[int, int]]:
    """MAIN/human 25% (half×half); AI 6.25% (quarter×quarter) — original sizes."""
    Lw, Lh = max(1, int(Lw)), max(1, int(Lh))
    Wm = Lw // 2
    Hm = Lh // 2
    Wm2 = Lw - Wm
    Hm2 = Lh - Hm
    Wa = Lw // 4
    Ha = Lh // 4
    return {
        "Wm": Wm,
        "Hm": Hm,
        "Wm2": Wm2,
        "Hm2": Hm2,
        "Wa": Wa,
        "Ha": Ha,
        "main_w": Wm,
        "main_h": Hm,
        "human_w": Wm2,
        "human_h": Hm,  # must equal main_h
        "ai_w": Wa,
        "ai_h": Ha,
    }


def resolve_layout_mode(
    n_human: int,
    n_ai: int,
) -> LayoutMode | None:
    """Map player counts → A/B/C/D (F0020); unsupported configs return None."""
    nh, na = int(n_human), int(n_ai)
    if nh == 1 and na == 3:
        return "A"
    if nh == 2 and na == 2:
        return "B"
    if nh == 0 and na == 4:
        return "C"
    if nh == 3 and na == 1:
        return "D"
    return None


def to_compact(rect: WindowRect) -> WindowRect:
    """精简: width 50%, height unchanged, left edge fixed."""
    return WindowRect(int(rect.x), int(rect.y), max(1, int(rect.w) // 2), int(rect.h))


def clamp_outer_size(
    w: int,
    h: int,
    *,
    kind: str = "main",
) -> tuple[int, int]:
    """
    Clamp outer window size: never larger than 1080p complete mode.

    kind: main | human | ai
    Smaller plans (720p) keep their smaller w/h.
    """
    w, h = max(1, int(w)), max(1, int(h))
    if kind == "ai":
        return min(w, FULL_AI_W), min(h, FULL_AI_H)
    # main and human share full complete size
    return min(w, FULL_MAIN_W), min(h, FULL_MAIN_H)


def _cap_rect(r: WindowRect, *, kind: str) -> WindowRect:
    w, h = clamp_outer_size(r.w, r.h, kind=kind)
    return WindowRect(r.x, r.y, w, h)


def _cap_plan_windows(
    main: WindowRect,
    players: dict[int, WindowRect],
    *,
    human_seats: list[int],
) -> tuple[WindowRect, dict[int, WindowRect]]:
    """Cap MAIN/human/AI outer frames to 1080p complete sizes (no enlarge)."""
    main = _cap_rect(main, kind="main")
    hs = set(int(s) for s in human_seats)
    out: dict[int, WindowRect] = {}
    for s, r in players.items():
        kind = "human" if int(s) in hs else "ai"
        out[int(s)] = _cap_rect(r, kind=kind)
    return main, out


def _equalize_main_human_heights(
    main: WindowRect,
    players: dict[int, WindowRect],
    *,
    human_seats: list[int],
) -> tuple[WindowRect, dict[int, WindowRect]]:
    """
    Force every human window to use the same height as MAIN.

    Bottom-row humans also share MAIN's y (side-by-side row).
    Top-row humans (layout B) keep their y, only h is equalized.
    """
    h = int(main.h)
    main = WindowRect(int(main.x), int(main.y), int(main.w), h)
    out = dict(players)
    for s in human_seats:
        s = int(s)
        if s not in out:
            continue
        r = out[s]
        # Bottom row: same y as MAIN
        if int(r.y) + int(r.h) // 2 >= int(main.y):
            out[s] = WindowRect(int(r.x), int(main.y), int(r.w), h)
        else:
            out[s] = WindowRect(int(r.x), int(r.y), int(r.w), h)
    return main, out


def _ai_band_rects(
    n: int,
    *,
    ox: int,
    oy: int,
    band_w: int,
    Wa: int,
    Ha: int,
    floor_y: int | None = None,
) -> list[WindowRect]:
    """
    Horizontally distribute n AI windows — **original Ha**, **top-aligned**.

    Do not enlarge height. If bottom would cross MAIN, **move up** (keep Ha).
    """
    n = max(0, int(n))
    if n == 0:
        return []
    Wa = max(80, int(Wa))
    Ha = max(80, min(int(Ha), FULL_AI_H))
    band_w = max(Wa, int(band_w))
    limit_bottom = (
        int(floor_y) - DECORATION_PAD_Y - GAP
        if floor_y is not None
        else None
    )
    # Default: top of band
    ai_y = int(oy)
    ai_h = Ha
    if limit_bottom is not None and ai_y + ai_h > limit_bottom:
        # Move up only (keep size); clamp to band top
        ai_y = int(limit_bottom - ai_h)
        if ai_y < oy:
            ai_y = int(oy)
            # Last resort only if even top-aligned still collides: keep size, clip y
            if ai_y + ai_h > limit_bottom:
                ai_y = max(int(oy), int(limit_bottom - ai_h))

    total_w = n * Wa
    gap_free = max(0, band_w - total_w)
    g_ai = max(0, gap_free // (n + 1))
    margin_x = max(0, (gap_free - (n - 1) * g_ai) // 2)
    out: list[WindowRect] = []
    for i in range(n):
        x = ox + margin_x + i * (Wa + g_ai)
        out.append(WindowRect(x, ai_y, Wa, ai_h))
    return out


def _ensure_ai_above_bottom_row(
    main: WindowRect,
    players: dict[int, WindowRect],
    *,
    human_seats: list[int],
    canvas_top: int | None = None,
) -> dict[int, WindowRect]:
    """If AI still crosses MAIN top: move up, keep height (do not enlarge)."""
    hs = set(int(s) for s in human_seats)
    floor_y = int(main.y)
    for s in hs:
        r = players.get(int(s))
        if r is not None and int(r.y) >= int(main.y) - 2:
            floor_y = min(floor_y, int(r.y))
    limit = floor_y - DECORATION_PAD_Y - GAP
    top_min = int(canvas_top) if canvas_top is not None else None
    out = dict(players)
    for s, r in list(out.items()):
        if int(s) in hs:
            continue
        if r.bottom <= limit:
            continue
        # Move up, preserve height
        new_y = int(limit - int(r.h))
        if top_min is not None:
            new_y = max(new_y, top_min)
        out[int(s)] = WindowRect(int(r.x), new_y, int(r.w), int(r.h))
    return out


def plan_mode_A(
    canvas: WindowRect,
    *,
    human_seats: list[int],
    ai_seats: list[int],
) -> tuple[WindowRect, dict[int, WindowRect]]:
    """3 AI + 1 human: MAIN left-bottom, human right-bottom, 3 AI top band."""
    sz = window_sizes(canvas.w, canvas.h)
    Wm, Hm = int(sz["Wm"]), int(sz["Hm"])
    Wm2, Wa, Ha = int(sz["Wm2"]), int(sz["Wa"]), int(sz["Ha"])
    ox, oy = canvas.x, canvas.y
    main = WindowRect(ox, oy + (canvas.h - Hm), Wm, Hm)
    players: dict[int, WindowRect] = {}
    hs = list(human_seats)[:1]
    if hs:
        players[int(hs[0])] = WindowRect(
            ox + Wm, oy + (canvas.h - Hm), Wm2, Hm
        )
    for seat, rect in zip(
        ai_seats,
        _ai_band_rects(
            len(ai_seats),
            ox=ox,
            oy=oy,
            band_w=canvas.w,
            Wa=Wa,
            Ha=Ha,
            floor_y=main.y,
        ),
    ):
        players[int(seat)] = rect
    return main, players


def plan_mode_B(
    canvas: WindowRect,
    *,
    human_seats: list[int],
    ai_seats: list[int],
) -> tuple[WindowRect, dict[int, WindowRect]]:
    """2 AI + 2 human: humans right column; 2 AI in left-top quarter."""
    sz = window_sizes(canvas.w, canvas.h)
    Wm, Hm = int(sz["Wm"]), int(sz["Hm"])
    Wm2, Wa, Ha = int(sz["Wm2"]), int(sz["Wa"]), int(sz["Ha"])
    ox, oy = canvas.x, canvas.y
    main = WindowRect(ox, oy + (canvas.h - Hm), Wm, Hm)
    players: dict[int, WindowRect] = {}
    hs = list(human_seats)[:2]
    if len(hs) >= 1:
        players[int(hs[0])] = WindowRect(
            ox + Wm, oy + (canvas.h - Hm), Wm2, Hm
        )
    if len(hs) >= 2:
        # Top-right human: same height as MAIN
        players[int(hs[1])] = WindowRect(ox + Wm, oy, Wm2, Hm)
    for seat, rect in zip(
        ai_seats,
        _ai_band_rects(
            len(ai_seats),
            ox=ox,
            oy=oy,
            band_w=Wm,
            Wa=Wa,
            Ha=Ha,
            floor_y=main.y,
        ),
    ):
        players[int(seat)] = rect
    return main, players


def plan_mode_C(
    canvas: WindowRect,
    *,
    ai_seats: list[int],
) -> tuple[WindowRect, dict[int, WindowRect]]:
    """4 AI + 0 human: MAIN left-bottom; 4 AI top band; right-bottom empty."""
    sz = window_sizes(canvas.w, canvas.h)
    Wm, Hm = int(sz["Wm"]), int(sz["Hm"])
    Wa, Ha = int(sz["Wa"]), int(sz["Ha"])
    ox, oy = canvas.x, canvas.y
    main = WindowRect(ox, oy + (canvas.h - Hm), Wm, Hm)
    players: dict[int, WindowRect] = {}
    for seat, rect in zip(
        ai_seats,
        _ai_band_rects(
            len(ai_seats),
            ox=ox,
            oy=oy,
            band_w=canvas.w,
            Wa=Wa,
            Ha=Ha,
            floor_y=main.y,
        ),
    ):
        players[int(seat)] = rect
    return main, players


def plan_mode_D(
    canvas: WindowRect,
    *,
    human_seats: list[int],
    ai_seats: list[int],
) -> tuple[WindowRect, dict[int, WindowRect]]:
    """
    3 human + 1 AI (F0020 layout D).

    Top band: AI (Wa×Ha). Body 2×2:
      H[1] | H[2]
      MAIN | H[0]
    """
    sz = window_sizes(canvas.w, canvas.h)
    Wa, Ha = int(sz["Wa"]), int(sz["Ha"])
    ox, oy = int(canvas.x), int(canvas.y)
    Lw, Lh = int(canvas.w), int(canvas.h)
    gap = int(GAP)
    body_top = oy + Ha + gap
    body_h = max(80, Lh - Ha - gap)
    row_h = body_h // 2
    row_h2 = body_h - row_h
    col_w = Lw // 2
    col_w2 = Lw - col_w

    main = WindowRect(ox, body_top + row_h, col_w, row_h2)
    players: dict[int, WindowRect] = {}
    hs = list(human_seats)[:3]
    # H[0] right-bottom, H[1] left-top body, H[2] right-top body
    if len(hs) >= 1:
        players[int(hs[0])] = WindowRect(
            ox + col_w, body_top + row_h, col_w2, row_h2
        )
    if len(hs) >= 2:
        players[int(hs[1])] = WindowRect(ox, body_top, col_w, row_h)
    if len(hs) >= 3:
        players[int(hs[2])] = WindowRect(
            ox + col_w, body_top, col_w2, row_h
        )
    # Single AI top band, left-aligned
    if ai_seats:
        players[int(ai_seats[0])] = WindowRect(ox, oy, Wa, Ha)
    return main, players


def plan_layout_abc(
    num_players: int = 4,
    *,
    human_seats: list[int] | None = None,
    desktop: tuple[int, int] | None = None,
    origin: tuple[int, int] = (0, 0),
    scale: float = 1.0,
) -> WindowPlan | None:
    """
    Build WindowPlan for layout A/B/C/D (F0020). Returns None if unsupported.
    """
    n = max(1, min(4, int(num_players)))
    if human_seats is None:
        human_seats = [0] if n >= 1 else []
    else:
        human_seats = [int(s) for s in human_seats if 0 <= int(s) < n]
    # unique preserve order
    seen: set[int] = set()
    hs: list[int] = []
    for s in human_seats:
        if s not in seen:
            seen.add(s)
            hs.append(s)
    human_seats = hs
    all_seats = list(range(n))
    ai_seats = [s for s in all_seats if s not in seen]
    mode = resolve_layout_mode(len(human_seats), len(ai_seats))
    if mode is None:
        return None

    if desktop is None:
        sc = detect_screen()
        dw, dh = sc.width, sc.height
        ox0, oy0 = sc.origin_x, sc.origin_y
    else:
        dw, dh = int(desktop[0]), int(desktop[1])
        ox0, oy0 = origin

    # Cap work for layout at 2160p; place canvas centered in full W×H
    canvas = layout_canvas(dw, dh, origin=(ox0, oy0))
    # Size basis: never larger than 1080p canvas so outer windows ≤ §8.2 1080p
    # (user: 完整模式尺寸为最小，请不要扩大). Must stay inside real canvas.
    size_basis = canvas
    if canvas.w > FULL_CANVAS_W or canvas.h > FULL_CANVAS_H:
        Lw = min(int(canvas.w), FULL_CANVAS_W)
        Lh = min(int(canvas.h), FULL_CANVAS_H)
        size_basis = WindowRect(
            canvas.x + (canvas.w - Lw) // 2,
            canvas.y + (canvas.h - Lh) // 2,
            Lw,
            Lh,
        )
    # Do not apply S>1 enlarge for default plan (scale arg ignored if >1)
    _ = scale  # reserved; enlargement disabled

    if mode == "A":
        main, players = plan_mode_A(
            size_basis, human_seats=human_seats, ai_seats=ai_seats
        )
    elif mode == "B":
        main, players = plan_mode_B(
            size_basis, human_seats=human_seats, ai_seats=ai_seats
        )
    elif mode == "D":
        main, players = plan_mode_D(
            size_basis, human_seats=human_seats, ai_seats=ai_seats
        )
    else:
        main, players = plan_mode_C(size_basis, ai_seats=ai_seats)

    main, players = _cap_plan_windows(main, players, human_seats=human_seats)
    # A/B: equalize bottom-row human with MAIN. D: body grid already paired.
    if mode != "D":
        main, players = _equalize_main_human_heights(
            main, players, human_seats=human_seats
        )
    # AI: move up if needed; never grow height (A/B/C). D AI is above body.
    if mode != "D":
        canvas_top = int(size_basis.y)
        players = _ensure_ai_above_bottom_row(
            main,
            players,
            human_seats=human_seats,
            canvas_top=canvas_top,
        )

    # work rect: full desktop slice used for containment (not 2K F0001 cap)
    work = WindowRect(ox0, oy0, dw, dh)
    pref_mw = BASE_MAIN_W
    sc_factor = min(1.0, main.w / max(pref_mw, 1))
    return WindowPlan(
        work=work,
        main=main,
        players=players,
        scale=sc_factor,
        layout_mode=mode,
        canvas=canvas,
    )


def compute_window_plan(
    num_players: int = 4,
    *,
    include_main: bool = True,
    desktop: tuple[int, int] | None = None,
    main_size: tuple[int, int] | None = None,
    player_size: tuple[int, int] | None = None,
    origin: tuple[int, int] = (0, 0),
    human_seats: list[int] | None = None,
    layout_mode: str | None = "auto",
    scale: float = 1.0,
) -> WindowPlan:
    """
    Multi-window plan (F0018).

    Default for 4 seats: UI_DESIGN_STANDARD layout A/B/C from ``human_seats``.
    Pass ``layout_mode=\"legacy\"`` for the old 2×3 grid (compat).
    """
    n = max(2, min(4, int(num_players)))
    if layout_mode != "legacy" and n == 4:
        plan = plan_layout_abc(
            n,
            human_seats=human_seats,
            desktop=desktop,
            origin=origin,
            scale=scale,
        )
        if plan is not None:
            if not include_main:
                # keep players; shrink main to unused stub
                plan = WindowPlan(
                    work=plan.work,
                    main=WindowRect(plan.main.x, plan.main.y, 1, 1),
                    players=plan.players,
                    scale=plan.scale,
                    layout_mode=plan.layout_mode,
                    canvas=plan.canvas,
                )
            return plan

    # --- legacy grid (2–3 seats or explicit legacy) ---
    work = work_area(desktop, origin=origin)
    g = GAP
    m = MARGIN
    ix = work.x + m
    iy = work.y + m
    iw = max(300, work.w - 2 * m)
    ih = max(240, work.h - 2 * m)

    col_w = max(160, (iw - 2 * g) // 3)
    row_h = max(140, (ih - g) // 2)
    col_w3 = iw - 2 * (col_w + g)
    row_h2 = ih - (row_h + g)

    def cell(col: int, row: int, span_cols: int = 1) -> WindowRect:
        x = ix + col * (col_w + g)
        y = iy + row * (row_h + g)
        if span_cols == 1:
            w = col_w3 if col == 2 else col_w
        else:
            w = iw - col * (col_w + g)
        h = row_h2 if row == 1 else row_h
        return WindowRect(x, y, max(160, w), max(140, h))

    players: dict[int, WindowRect] = {}

    if n == 2:
        main = WindowRect(
            ix + (col_w + g),
            iy + row_h + g,
            iw - (col_w + g),
            row_h2,
        )
        players[1] = cell(2, 0)
        players[0] = WindowRect(ix, iy + row_h + g, col_w, row_h2)
    elif n == 3:
        players[0] = WindowRect(ix, iy + row_h + g, col_w, row_h2)
        players[1] = cell(2, 0)
        players[2] = cell(1, 0)
        main = WindowRect(
            ix + (col_w + g),
            iy + row_h + g,
            iw - (col_w + g),
            row_h2,
        )
    else:
        players[3] = cell(0, 0)
        players[2] = cell(1, 0)
        players[1] = cell(2, 0)
        players[0] = WindowRect(ix, iy + row_h + g, col_w, row_h2)
        main = WindowRect(
            ix + (col_w + g),
            iy + row_h + g,
            iw - (col_w + g),
            row_h2,
        )

    if not include_main:
        main = WindowRect(ix + (col_w + g), iy + row_h + g, col_w, row_h2)

    pref_mw = (main_size or (BASE_MAIN_W, BASE_MAIN_H))[0]
    scale_f = min(1.0, main.w / max(pref_mw, 1))

    def _clamp(r: WindowRect) -> WindowRect:
        w = min(r.w, work.w - 2 * m)
        h = min(r.h, work.h - 2 * m)
        x = min(max(r.x, work.x + m), work.x + work.w - w - m)
        y = min(max(r.y, work.y + m), work.y + work.h - h - m)
        return WindowRect(x, y, w, h)

    main = _clamp(main)
    players = {s: _clamp(r) for s, r in players.items()}
    return WindowPlan(
        work=work, main=main, players=players, scale=scale_f, layout_mode="legacy"
    )


def set_sdl_window_pos(x: int, y: int) -> None:
    """
    Set SDL window position env.

    On macOS, ``SDL_VIDEO_WINDOW_POS`` places the **content** top-left, while
    Tk ``geometry +y`` is the **outer frame** top. Content is ~title-bar below
    the outer top, so we push SDL Y down by chrome to align outer tops with Tk.
    """
    xx, yy = int(x), int(y)
    if sys.platform == "darwin":
        yy = yy + platform_frame_chrome_y()
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{xx},{yy}"


def clear_sdl_window_pos() -> None:
    os.environ.pop("SDL_VIDEO_WINDOW_POS", None)


def open_resizable_window(
    size: tuple[int, int],
    *,
    pos: tuple[int, int] | None = None,
    caption: str | None = None,
    min_size: tuple[int, int] | None = None,
):
    import pygame

    if not pygame.get_init():
        pygame.init()
    if not pygame.display.get_init():
        pygame.display.init()

    if pos is not None:
        set_sdl_window_pos(pos[0], pos[1])
    flags = pygame.RESIZABLE
    screen = pygame.display.set_mode(size, flags)
    if caption:
        pygame.display.set_caption(caption)
    # min_size via _sdl2 is optional and unsafe on some macOS builds — skip
    _ = min_size
    # Position already applied via SDL_VIDEO_WINDOW_POS + set_mode.
    # Do NOT call force_window_placement here again (would double set_mode).
    # Leave env set so later set_mode keeps the anchor.
    return screen


def _get_pygame_window():
    """
    Current pygame display window if available via safe APIs only.

    Never import ``pygame._sdl2`` — on macOS that path causes intermittent
    SIGSEGV in the event loop even when only reading.
    """
    import pygame

    if hasattr(pygame.display, "get_window"):
        try:
            return pygame.display.get_window()
        except Exception:
            return None
    return None


def _force_window_placement_pygame(x: int, y: int, w: int, h: int) -> bool:
    """
    macOS/Linux placement: env pos + set_mode only.

    Do **not**:
      - write pygame._sdl2.Window attributes (SEGV)
      - call display.quit()/reinit mid-session (stale surfaces / SEGV)
    """
    try:
        import pygame

        set_sdl_window_pos(int(x), int(y))
        os.environ.pop("SDL_VIDEO_CENTERED", None)
        ww = max(160, int(w))
        hh = max(140, int(h))
        if not pygame.get_init():
            pygame.init()
        if not pygame.display.get_init():
            pygame.display.init()
        pygame.display.set_mode((ww, hh), pygame.RESIZABLE)
        return True
    except Exception:
        return False


def force_window_placement(x: int, y: int, w: int, h: int) -> bool:
    """
    Force the current pygame window to (x,y,w,h).

    Windows: HWND SetWindowPos.
    Other: SDL_VIDEO_WINDOW_POS + set_mode only (stable on macOS).
    """
    set_sdl_window_pos(int(x), int(y))
    if sys.platform == "win32":
        try:
            import pygame

            info = pygame.display.get_wm_info()
            hwnd = info.get("window") if info else None
            if not hwnd:
                return _force_window_placement_pygame(x, y, w, h)
            return force_hwnd_placement(int(hwnd), x, y, w, h)
        except Exception:
            return False
    return _force_window_placement_pygame(x, y, w, h)


def raise_main_window() -> bool:
    """Best-effort front; never touches _sdl2."""
    try:
        import pygame

        if sys.platform == "win32":
            try:
                import ctypes

                info = pygame.display.get_wm_info()
                hwnd = info.get("window") if info else None
                if hwnd:
                    user32 = ctypes.windll.user32  # type: ignore[attr-defined]
                    user32.SetForegroundWindow(int(hwnd))
                    user32.BringWindowToTop(int(hwnd))
                    return True
            except Exception:
                pass
        return True
    except Exception:
        return False


def force_hwnd_placement(hwnd: int, x: int, y: int, w: int, h: int) -> bool:
    """Win32 Show + SetWindowPos for an arbitrary HWND. No-op on non-Windows."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes

        user32 = ctypes.windll.user32  # type: ignore[attr-defined]
        HWND_TOP = 0
        SWP_SHOWWINDOW = 0x0040
        SWP_FRAMECHANGED = 0x0020
        # Do NOT use HWND_TOPMOST — leaves windows sticky and hard to focus.
        SW_SHOW = 5
        SW_RESTORE = 9
        user32.ShowWindow(int(hwnd), SW_RESTORE)
        user32.ShowWindow(int(hwnd), SW_SHOW)
        # Enable window (in case a prior bad place left it disabled)
        user32.EnableWindow(int(hwnd), True)
        ok = user32.SetWindowPos(
            int(hwnd),
            HWND_TOP,
            int(x),
            int(y),
            max(160, int(w)),
            max(140, int(h)),
            SWP_SHOWWINDOW | SWP_FRAMECHANGED,
        )
        return bool(ok)
    except Exception:
        return False


def force_placement_by_title(
    title_substr: str, x: int, y: int, w: int, h: int, *, require_visible: bool = False
) -> bool:
    """
    Find a top-level window whose title contains title_substr and place it.
    Used by the parent process to re-assert seat window geometry after spawn.
    Windows-only (F0005); macOS seat windows rely on Tk --geometry at spawn.
    """
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32  # type: ignore[attr-defined]
        found: list[int] = []
        needle = title_substr.lower()

        @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        def _enum(hwnd, _lp):  # type: ignore[no-untyped-def]
            if require_visible and not user32.IsWindowVisible(hwnd):
                return True
            # top-level only
            if user32.GetParent(hwnd):
                return True
            buf = ctypes.create_unicode_buffer(512)
            user32.GetWindowTextW(hwnd, buf, 512)
            title = buf.value or ""
            if needle and needle in title.lower():
                found.append(int(hwnd))
            return True

        user32.EnumWindows(_enum, 0)
        if not found:
            return False
        ok_any = False
        for hwnd in found:
            if force_hwnd_placement(hwnd, x, y, w, h):
                ok_any = True
        return ok_any
    except Exception:
        return False


def find_hwnds_for_pid(pid: int) -> list[int]:
    """All top-level HWNDs owned by process pid (Windows only)."""
    if sys.platform != "win32":
        return []
    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32  # type: ignore[attr-defined]
        found: list[int] = []
        target = int(pid)

        @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        def _enum(hwnd, _lp):  # type: ignore[no-untyped-def]
            proc_id = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(proc_id))
            if int(proc_id.value) != target:
                return True
            # Top-level only (skip owned/child tool windows when parent set)
            if user32.GetParent(hwnd):
                return True
            found.append(int(hwnd))
            return True

        user32.EnumWindows(_enum, 0)
        return found
    except Exception:
        return []


def pick_main_hwnd_for_pid(pid: int) -> int | None:
    """
    Choose the real seat UI window for a pid.

    Must NOT move/resize IME / TtkMonitor / Default IME windows — doing so on
    Windows breaks focus, drag, and resize for the process.
    """
    if sys.platform != "win32":
        return None
    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32  # type: ignore[attr-defined]
        skip_titles = {
            "",
            "msctfime ui",
            "default ime",
            "ttkmonitorwindow",
            "gdi+ window",
        }
        best: tuple[int, int] | None = None  # (score, hwnd)

        for hwnd in find_hwnds_for_pid(pid):
            if not user32.IsWindowVisible(hwnd):
                continue
            buf = ctypes.create_unicode_buffer(512)
            user32.GetWindowTextW(hwnd, buf, 512)
            title = (buf.value or "").strip()
            tlow = title.lower()
            if tlow in skip_titles or tlow.startswith("ime"):
                continue
            # Window rect area
            class RECT(ctypes.Structure):
                _fields_ = [
                    ("left", ctypes.c_long),
                    ("top", ctypes.c_long),
                    ("right", ctypes.c_long),
                    ("bottom", ctypes.c_long),
                ]

            rc = RECT()
            if not user32.GetWindowRect(hwnd, ctypes.byref(rc)):
                continue
            area = max(0, int(rc.right - rc.left)) * max(0, int(rc.bottom - rc.top))
            if area < 80 * 60:
                continue
            score = area
            if "cmj" in tlow or "seat" in tlow or "human" in tlow or "watch" in tlow:
                score += 10_000_000
            if best is None or score > best[0]:
                best = (score, int(hwnd))
        return best[1] if best else None
    except Exception:
        return None


def force_placement_by_pid(
    pid: int, x: int, y: int, w: int, h: int, *, timeout_s: float = 3.0
) -> bool:
    """
    Wait briefly for the main seat window of pid, then place only that HWND.
    Windows-only. Never touches IME/tool windows (focus/resize safe).
    """
    if sys.platform != "win32":
        return False
    import time as _time

    deadline = _time.time() + max(0.2, float(timeout_s))
    hwnd: int | None = None
    while _time.time() < deadline:
        hwnd = pick_main_hwnd_for_pid(pid)
        if hwnd:
            break
        _time.sleep(0.08)
    if not hwnd:
        return False
    return force_hwnd_placement(hwnd, x, y, w, h)


def reassert_plan_windows(
    plan: WindowPlan,
    *,
    seat_pids: dict[int, int] | None = None,
    include_main: bool = False,
) -> dict[str, bool]:
    """
    Parent-side: force windows to planned rects.

    **include_main=False by default** — calling ``force_window_placement``
    (``set_mode``) from the seat-spawn **background thread** crashes pygame
    on macOS (SIGSEGV / abort). Main window must be pinned only on the
    pygame main thread via ``MahjongApp._pin_main_window``.
    """
    results: dict[str, bool] = {}
    if include_main:
        # Only safe when invoked on the pygame/main thread (Windows HWND OK too).
        results["main"] = force_window_placement(
            plan.main.x, plan.main.y, plan.main.w, plan.main.h
        )
        if not results["main"] and sys.platform == "win32":
            results["main"] = force_placement_by_title(
                "主程序", plan.main.x, plan.main.y, plan.main.w, plan.main.h
            )
    else:
        results["main"] = False  # skipped (caller pins on main thread)
    seat_pids = seat_pids or {}
    for seat, rect in plan.players.items():
        rect = clamp_rect_to_visible(rect)
        ok = False
        if sys.platform == "win32":
            pid = seat_pids.get(seat)
            if pid:
                ok = force_placement_by_pid(
                    pid, rect.x, rect.y, rect.w, rect.h, timeout_s=0.8
                )
            if not ok:
                # Titles: "CMJ Human S0" / "CMJ AI-Watch S1"
                ok = force_placement_by_title(
                    f" S{seat}", rect.x, rect.y, rect.w, rect.h
                )
            if not ok:
                ok = force_placement_by_title(
                    f"S{seat}", rect.x, rect.y, rect.w, rect.h
                )
        # macOS/Linux: seat Tk geometry / set_geometry wire (not HWND)
        results[f"S{seat}"] = bool(ok)
    return results


def plan_cli_args(rect: WindowRect) -> list[str]:
    # Use --y=-724 form so negative Y is never parsed as a new flag
    return [
        "--x",
        str(int(rect.x)),
        f"--y={int(rect.y)}",
        "--width",
        str(int(rect.w)),
        "--height",
        str(int(rect.h)),
    ]


def windows_overlap(a: WindowRect, b: WindowRect, pad: int = 0) -> bool:
    return not (
        a.right + pad <= b.x
        or b.right + pad <= a.x
        or a.bottom + pad <= b.y
        or b.bottom + pad <= a.y
    )
