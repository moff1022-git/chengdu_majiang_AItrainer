"""Unified asset loading from project assets/ (ASSETS.md contract)."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pygame

Theme = Literal["green", "blue"]

def _default_assets() -> Path:
    try:
        from app_paths import assets_dir

        return assets_dir()
    except Exception:
        return Path(__file__).resolve().parent.parent / "assets"


class AssetManager:
    def __init__(
        self,
        root: Path | str | None = None,
        theme: str = "green",
        *,
        strict: bool = True,
    ) -> None:
        self.root = Path(root) if root else _default_assets()
        if theme not in ("green", "blue"):
            raise ValueError(f"theme must be green|blue, got {theme!r}")
        self.theme: Theme = theme  # type: ignore[assignment]
        self.strict = strict
        self._cache: dict[str, pygame.Surface] = {}
        self._scaled: dict[str, pygame.Surface] = {}

    def set_theme(self, theme: str) -> None:
        if theme not in ("green", "blue"):
            raise ValueError(f"theme must be green|blue, got {theme!r}")
        if theme == self.theme:
            return
        self.theme = theme  # type: ignore[assignment]
        self._cache.clear()
        self._scaled.clear()

    def path_for(self, *parts: str) -> Path:
        return self.root.joinpath(*parts)

    def _cache_key(self, rel: str, themed: bool) -> str:
        if themed:
            return f"{self.theme}:{rel}"
        return f"raw:{rel}"

    def load(self, rel: str, *, themed: bool = False) -> pygame.Surface:
        key = self._cache_key(rel, themed)
        if key in self._cache:
            return self._cache[key]
        path = self.root / rel
        if not path.is_file():
            if self.strict:
                raise FileNotFoundError(f"asset not found: {path}")
            surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            surf.fill((200, 50, 50, 180))
            self._cache[key] = surf
            return surf
        surf = pygame.image.load(str(path))
        # convert_alpha requires a display mode; keep raw surface in headless/dummy tests
        try:
            if pygame.display.get_surface() is not None:
                surf = surf.convert_alpha()
        except pygame.error:
            pass
        self._cache[key] = surf
        return surf

    def _t(self, template: str) -> str:
        return template.format(theme=self.theme)

    def tile(self, suit: str, rank: int) -> pygame.Surface:
        rel = f"tiles/{suit}/tile_{suit}_{rank}_{self.theme}.png"
        return self.load(rel)

    def tile_back(self) -> pygame.Surface:
        return self.load(f"tiles/backs/tile_back_{self.theme}.png")

    def tile_placeholder(self) -> pygame.Surface:
        return self.load("tiles/backs/tile_placeholder.png")

    def button(self, key: str) -> pygame.Surface:
        return self.load(f"buttons/btn_{key}_{self.theme}.png")

    def bg(self, which: str) -> pygame.Surface:
        return self.load(f"backgrounds/bg_{which}_{self.theme}.png")

    def avatar(self, n: int) -> pygame.Surface:
        return self.load(f"players/avatar_{n}_{self.theme}.png")

    def seat_badge(self, direction: str) -> pygame.Surface:
        return self.load(f"players/seat_{direction}_{self.theme}.png")

    def dealer_badge(self) -> pygame.Surface:
        return self.load(f"players/dealer_badge_{self.theme}.png")

    def dice(self, n: int) -> pygame.Surface:
        return self.load(f"dice/dice_{n}_{self.theme}.png")

    def icon(self, key: str) -> pygame.Surface:
        if key == "logo":
            return self.load(f"icons/logo_{self.theme}.png")
        return self.load(f"icons/icon_{key}_{self.theme}.png")

    def fx(self, key: str) -> pygame.Surface:
        return self.load(f"effects/fx_{key}_{self.theme}.png")

    def danger(self, level: str) -> pygame.Surface:
        return self.load(f"inference/danger_{level}_{self.theme}.png")

    def inference(self, key: str) -> pygame.Surface:
        return self.load(f"inference/{key}_{self.theme}.png")

    def strategy_asset(self, key: str) -> pygame.Surface:
        return self.load(f"strategy/{key}_{self.theme}.png")

    def digit(self, char: str, color: str, size: str) -> pygame.Surface:
        # char: 0-9 or minus
        name = char if char != "-" else "minus"
        return self.load(f"fonts/numbers/digit_{name}_{color}_{size}.png")

    def char_glyph(self, key: str, size: str) -> pygame.Surface:
        return self.load(f"fonts/chars/char_{key}_{size}_{self.theme}.png")

    def scale_to_width(self, surf: pygame.Surface, w: int) -> pygame.Surface:
        key = f"id{id(surf)}:w{w}:th{self.theme}"
        # better key by content path not available; use size + id of source
        src_key = f"{surf.get_width()}x{surf.get_height()}:w{w}:{id(surf)}"
        if src_key in self._scaled:
            return self._scaled[src_key]
        if surf.get_width() == w:
            self._scaled[src_key] = surf
            return surf
        h = max(1, int(surf.get_height() * (w / surf.get_width())))
        out = pygame.transform.smoothscale(surf, (w, h))
        self._scaled[src_key] = out
        return out

    def scale_to_size(
        self, surf: pygame.Surface, size: tuple[int, int]
    ) -> pygame.Surface:
        key = f"{surf.get_width()}x{surf.get_height()}:{size[0]}x{size[1]}:{id(surf)}"
        if key in self._scaled:
            return self._scaled[key]
        out = pygame.transform.smoothscale(surf, size)
        self._scaled[key] = out
        return out
