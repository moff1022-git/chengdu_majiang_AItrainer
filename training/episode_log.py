"""JSONL episode logger for RL / analysis."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class EpisodeLogger:
    def __init__(
        self,
        run_dir: Path | str,
        game_id: str,
        *,
        log_private: bool = True,
    ) -> None:
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.game_id = game_id
        self.log_private = log_private
        self.path = self.run_dir / f"{game_id}.jsonl"
        self._fp = self.path.open("w", encoding="utf-8")

    def emit(self, type: str, **payload: Any) -> None:
        row = {"type": type, **payload}
        if not self.log_private:
            row.pop("hands", None)
        self._fp.write(json.dumps(row, ensure_ascii=False) + "\n")
        self._fp.flush()

    def close(self) -> None:
        if self._fp and not self._fp.closed:
            self._fp.close()

    def __enter__(self) -> EpisodeLogger:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
