"""Replay sessions from full snapshots or steps JSONL."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

from engine.persistence import PersistenceError, load_game
from engine.state import GameState


class ReplaySession:
    """
    Frame-based replay.

    Supports:
    - single save file (one frame)
    - steps JSONL with kind=snapshot rows
    """

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self._frames: list[GameState] = []
        self._index = 0
        self._load()

    def _load(self) -> None:
        p = self.path
        if not p.exists():
            raise PersistenceError(f"replay path not found: {p}")
        if p.suffix == ".jsonl" or p.name.endswith(".steps.jsonl"):
            self._load_steps(p)
        else:
            state, _meta = load_game(p)
            self._frames = [state]

    def _load_steps(self, path: Path) -> None:
        frames: list[GameState] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("kind") == "snapshot" and "state" in row:
                frames.append(GameState.from_dict(row["state"], strict=False))
            elif row.get("type") == "state" and "state" in row:
                frames.append(GameState.from_dict(row["state"], strict=False))
        if not frames:
            raise PersistenceError(f"no snapshots in {path}")
        self._frames = frames

    def __len__(self) -> int:
        return len(self._frames)

    @property
    def index(self) -> int:
        return self._index

    def frame(self, i: int) -> GameState:
        if i < 0 or i >= len(self._frames):
            raise IndexError(i)
        self._index = i
        return self._frames[i]

    def current(self) -> GameState:
        return self._frames[self._index]

    def step_forward(self) -> GameState:
        if self._index + 1 < len(self._frames):
            self._index += 1
        return self._frames[self._index]

    def step_back(self) -> GameState:
        if self._index > 0:
            self._index -= 1
        return self._frames[self._index]

    def iter_frames(self) -> Iterator[GameState]:
        yield from self._frames


class StepRecorder:
    """Append decision + periodic full snapshots to a JSONL file."""

    def __init__(self, path: Path | str, *, snapshot_every: int = 1) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.snapshot_every = max(1, snapshot_every)
        self._i = 0
        self.path.write_text("", encoding="utf-8")

    def record_snapshot(self, state: GameState) -> None:
        row = {
            "i": self._i,
            "kind": "snapshot",
            "state": state.to_dict(),
        }
        self._append(row)
        self._i += 1

    def record_decision(
        self,
        seat: int,
        action: dict,
        reason: str,
        *,
        state: GameState | None = None,
    ) -> None:
        row: dict[str, Any] = {
            "i": self._i,
            "kind": "decision",
            "seat": seat,
            "action": action,
            "reason": reason,
        }
        self._append(row)
        self._i += 1
        if state is not None and (self._i % self.snapshot_every == 0):
            self.record_snapshot(state)

    def _append(self, row: dict) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
