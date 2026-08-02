"""Shared HUD helpers: score digits, FX banners, CJK-safe text."""

from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from display.asset_manager import AssetManager

# Probe string used to reject fonts that silently drop CJK glyphs.
_CJK_PROBE = "麻将胡"

# Prefer real font *files* (reliable on macOS). pygame.SysFont often matches a
# Latin-only face when given Windows names like "microsoftyahei".
# Prefer .ttf over .ttc where available — some SDL_ttf builds crash on TTC.
_FONT_FILE_CANDIDATES: tuple[str, ...] = (
    # macOS — prefer single-face TTF first
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/NISC18030.ttf",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    # Linux common
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/arphic/uming.ttc",
    # Windows
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\msyh.ttf",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
)

# SysFont names verified / likely to carry CJK (order matters).
_SYS_FONT_CANDIDATES: tuple[str, ...] = (
    # macOS (pygame lowercases / strips spaces)
    "stheitimedium",
    "stheitilight",
    "hiraginosansgb",
    "songtisc",
    "pingfangsc",
    "arialunicodems",
    # Windows
    "microsoftyahei",
    "msyh",
    "simhei",
    "simsun",
    "microsoftyaheiui",
    # Generic
    "notosanscjksc",
    "notosanscjk",
    "wqymicrohei",
)

# Cache only the *source* (never Font objects — they die after pygame.quit).
# Values: ("file", path) | ("sys", name) | ("default", None) | None (unresolved)
_font_source: tuple[str, str | None] | None = None


def blit_score(
    screen: pygame.Surface,
    assets: AssetManager,
    score: int,
    pos: tuple[int, int],
    size: str = "md",
) -> None:
    color = "gold" if score >= 0 else "neg"
    s = str(score)
    x, y = pos
    if score < 0:
        dig = assets.digit("-", "neg", size)
        dig = assets.scale_to_width(dig, 16 if size == "sm" else 22)
        screen.blit(dig, (x, y))
        x += dig.get_width() + 1
        s = str(abs(score))
    for ch in s:
        dig = assets.digit(ch, color, size)
        dig = assets.scale_to_width(dig, 16 if size == "sm" else 22)
        screen.blit(dig, (x, y))
        x += dig.get_width() + 1


class FxOverlay:
    def __init__(self) -> None:
        self.key: str | None = None
        self.until: float = 0.0

    def trigger(self, key: str, duration: float = 0.8) -> None:
        self.key = key
        self.until = time.time() + duration

    def draw(self, screen: pygame.Surface, assets: AssetManager) -> None:
        if not self.key or time.time() > self.until:
            self.key = None
            return
        try:
            fx = assets.fx(self.key)
        except FileNotFoundError:
            return
        fx = assets.scale_to_width(fx, 320)
        rect = fx.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(fx, rect)


def _font_supports_cjk(font: pygame.font.Font) -> bool:
    """Return True if font renders CJK with a plausible advance width."""
    try:
        probe = font.render(_CJK_PROBE, True, (255, 255, 255))
        # Latin-only / missing-glyph fallbacks produce a very narrow surface.
        # Three full-width Han chars should be roughly >= 1.5 * size wide.
        return probe.get_width() >= max(24, int(font.get_height() * 1.5))
    except Exception:
        return False


def _discover_font_source() -> tuple[str, str | None]:
    """Pick a machine-local CJK font source once per process."""
    # Prefer SysFont on macOS for STHeiti — avoids some TTC edge crashes and
    # still renders CJK correctly when the name is real (not a Latin alias).
    for name in _SYS_FONT_CANDIDATES:
        try:
            font = pygame.font.SysFont(name, 24)
        except Exception:
            continue
        if font is not None and _font_supports_cjk(font):
            return ("sys", name)

    for path in _FONT_FILE_CANDIDATES:
        if not path or not os.path.isfile(path):
            continue
        try:
            font = pygame.font.Font(path, 24)
        except Exception:
            continue
        if _font_supports_cjk(font):
            return ("file", path)

    return ("default", None)


def resolve_ui_font(size: int) -> pygame.font.Font | None:
    """Resolve a UI font that can draw Simplified Chinese on this machine.

    Font objects are created fresh each call so they remain valid after
    pygame.quit()/init() cycles (common in tests).
    """
    global _font_source

    if not pygame.font.get_init():
        try:
            pygame.font.init()
        except Exception:
            return None

    size = max(8, int(size))

    if _font_source is None:
        try:
            _font_source = _discover_font_source()
        except Exception:
            _font_source = ("default", None)

    kind, ref = _font_source
    try:
        if kind == "file" and ref:
            return pygame.font.Font(ref, size)
        if kind == "sys" and ref:
            return pygame.font.SysFont(ref, size)
        return pygame.font.Font(None, size)
    except Exception:
        try:
            return pygame.font.Font(None, size)
        except Exception:
            return None


def draw_text(
    screen: pygame.Surface,
    text: str,
    pos: tuple[int, int],
    *,
    size: int = 22,
    color: tuple[int, int, int] = (240, 240, 240),
) -> None:
    """Render text with CJK-capable multi-font fallback (never silent-fail)."""
    font = resolve_ui_font(size)
    if font is None:
        return
    try:
        surf = font.render(str(text), True, color)
        screen.blit(surf, pos)
    except Exception:
        pass
