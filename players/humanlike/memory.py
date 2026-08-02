"""Finite memory over facts visible in PlayerView v2 only."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Any, Iterable, Mapping


def _canonical(value: Any) -> str:
    def thaw(item: Any) -> Any:
        if isinstance(item, Mapping):
            return {str(key): thaw(child) for key, child in item.items()}
        if isinstance(item, (list, tuple)):
            return [thaw(child) for child in item]
        return item

    return json.dumps(thaw(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


@dataclass(frozen=True, slots=True)
class VisibleToken:
    key: str
    category: str
    summary: str
    salience: float


@dataclass(slots=True)
class MemoryItem:
    key: str
    category: str
    summary: str
    first_seen_step: int
    last_seen_step: int
    strength: float
    salience: float
    exact: bool = True
    reinforcements: int = 1


@dataclass(frozen=True, slots=True)
class MemorySummary:
    exact: int
    fuzzy: int
    forgotten: int
    total: int
    logical_step: int

    def to_dict(self) -> dict[str, int]:
        return {
            "exact": self.exact,
            "fuzzy": self.fuzzy,
            "forgotten": self.forgotten,
            "total": self.total,
            "logical_step": self.logical_step,
        }


def extract_visible_tokens(payload: Mapping[str, Any]) -> tuple[VisibleToken, ...]:
    """Create stable tokens from public history/status without hidden inference."""
    tokens: list[VisibleToken] = []
    for index, event in enumerate(payload.get("discard_history") or []):
        if not isinstance(event, Mapping):
            continue
        seat = event.get("seat", "?")
        tile = event.get("tile") or event.get("tile_id") or event.get("face_id") or "?"
        key = f"discard:S{seat}:{tile}:{index}"
        tokens.append(VisibleToken(key, "discard", f"S{seat}:{tile}", 0.65))
    for player in payload.get("other_players") or []:
        if not isinstance(player, Mapping):
            continue
        seat = player.get("seat", "?")
        status = player.get("status")
        dingque = player.get("dingque")
        if status is not None:
            tokens.append(VisibleToken(f"status:S{seat}:{status}", "status", f"S{seat}:{status}", 1.0 if status != "active" else 0.55))
        if dingque is not None:
            tokens.append(VisibleToken(f"dingque:S{seat}:{dingque}", "dingque", f"S{seat}:{dingque}", 0.9))
        for meld_index, meld in enumerate(player.get("melds") or []):
            digest = hashlib.sha256(_canonical(meld).encode("utf-8")).hexdigest()[:12]
            tokens.append(VisibleToken(f"meld:S{seat}:{meld_index}:{digest}", "meld", f"S{seat}:{_canonical(meld)}", 1.0))
    last_event = payload.get("last_public_event")
    if isinstance(last_event, Mapping) and last_event:
        digest = hashlib.sha256(_canonical(last_event).encode("utf-8")).hexdigest()[:12]
        tokens.append(VisibleToken(f"recent:{digest}", "recent", _canonical(last_event), 1.0))
    unique = {token.key: token for token in tokens}
    return tuple(unique[key] for key in sorted(unique))


class MemoryStore:
    def __init__(self, *, initial_strength: float, forget_rate: float, salience_boost: float, capacity: int) -> None:
        self.initial_strength = float(initial_strength)
        self.forget_rate = float(forget_rate)
        self.salience_boost = float(salience_boost)
        self.capacity = max(1, int(capacity))
        self.items: dict[str, MemoryItem] = {}
        self.logical_step = 0
        self._last_event_index = 0
        self._fingerprint = ""
        self._previous_visible_keys: set[str] = set()
        self.forgotten_count = 0

    def update(self, event_index: int, tokens: Iterable[VisibleToken]) -> MemorySummary:
        token_list = tuple(tokens)
        fingerprint = hashlib.sha256("\n".join(token.key for token in token_list).encode("utf-8")).hexdigest()
        delta = max(0, int(event_index) - self._last_event_index)
        if fingerprint != self._fingerprint:
            delta = max(1, delta)
        if delta:
            decay = math.exp(-self.forget_rate * delta)
            for item in self.items.values():
                item.strength = max(0.0, min(1.0, item.strength * decay))
                if item.strength < 0.25:
                    item.exact = False
                    item.summary = item.category
            self.logical_step += delta
        current_keys = set()
        for token in token_list:
            current_keys.add(token.key)
            item = self.items.get(token.key)
            if item is None:
                self.items[token.key] = MemoryItem(
                    token.key,
                    token.category,
                    token.summary,
                    self.logical_step,
                    self.logical_step,
                    max(0.0, min(1.0, self.initial_strength + self.salience_boost * token.salience)),
                    token.salience,
                )
            elif token.key not in self._previous_visible_keys:
                item.strength = max(0.0, min(1.0, item.strength + self.salience_boost * token.salience))
                item.salience = token.salience
                item.summary = token.summary
                item.last_seen_step = self.logical_step
                item.exact = True
                item.reinforcements += 1
        if len(self.items) > self.capacity:
            victims = sorted(self.items.values(), key=lambda item: (item.strength, item.last_seen_step, item.key))
            for item in victims[: len(self.items) - self.capacity]:
                del self.items[item.key]
                self.forgotten_count += 1
        self._last_event_index = max(self._last_event_index, int(event_index))
        self._fingerprint = fingerprint
        self._previous_visible_keys = current_keys
        return self.summary()

    def summary(self) -> MemorySummary:
        exact = sum(item.exact for item in self.items.values())
        return MemorySummary(exact, len(self.items) - exact, self.forgotten_count, len(self.items), self.logical_step)

    def ranked_items(self) -> tuple[MemoryItem, ...]:
        return tuple(sorted(self.items.values(), key=lambda item: (-item.strength, -item.last_seen_step, item.key)))
