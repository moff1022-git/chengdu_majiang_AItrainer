"""Save / load full game state snapshots."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from engine.config import EngineConfig
from engine.state import GameState

FORMAT_NAME = "cmj_save"
FORMAT_VERSION = 1


class PersistenceError(ValueError):
    """Invalid or unsupported save file."""


def save_game(
    path: Path | str,
    state: GameState,
    *,
    config: EngineConfig | None = None,
    players_meta: list[dict] | None = None,
    crash_log: list[dict] | None = None,
    extra: dict | None = None,
) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    cfg = config or (
        EngineConfig.from_dict(state.config) if state.config else EngineConfig()
    )
    doc: dict[str, Any] = {
        "format": FORMAT_NAME,
        "format_version": FORMAT_VERSION,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "game_id": state.game_id,
        "schema_version": state.schema_version,
        "engine_config": cfg.to_dict(),
        "players_meta": list(players_meta or []),
        "crash_log": list(crash_log or []),
        "state": state.to_dict(),
    }
    if extra:
        doc["extra"] = extra
    path.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def load_game(path: Path | str) -> tuple[GameState, dict[str, Any]]:
    path = Path(path)
    if not path.is_file():
        raise PersistenceError(f"save not found: {path}")
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise PersistenceError(f"invalid json: {e}") from e
    if doc.get("format") != FORMAT_NAME:
        raise PersistenceError(f"unknown format: {doc.get('format')}")
    if int(doc.get("format_version", 0)) != FORMAT_VERSION:
        raise PersistenceError(
            f"unsupported format_version: {doc.get('format_version')}"
        )
    if "state" not in doc:
        raise PersistenceError("missing state")
    state = GameState.from_dict(doc["state"], strict=True)
    meta = {
        "saved_at": doc.get("saved_at"),
        "game_id": doc.get("game_id", state.game_id),
        "engine_config": doc.get("engine_config") or {},
        "players_meta": doc.get("players_meta") or [],
        "crash_log": doc.get("crash_log") or [],
        "extra": doc.get("extra") or {},
        "path": str(path),
    }
    return state, meta


def default_save_path(save_dir: Path | str, game_id: str) -> Path:
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in game_id)
    return Path(save_dir) / f"{safe}.json"
