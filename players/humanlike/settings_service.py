"""Validated persistence and launcher for the Humanlike v2 settings editor."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from app_paths import configs_dir
from players.humanlike.config import HumanlikeConfig, load_config
from players.humanlike.config_v2 import FrozenConfigV2, freeze_v2, migrate_1_1_to_2_0, validate_and_freeze


def default_config_path() -> Path:
    return configs_dir() / "humanlike_v2" / "default.json"


def read_raw(path: str | Path | None = None) -> dict[str, Any]:
    source = Path(path) if path else default_config_path()
    data = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("configuration root must be an object")
    return data


def validate_raw(data: dict[str, Any], *, target: str | Path | None = None) -> HumanlikeConfig:
    destination = Path(target) if target else default_config_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".humanlike_validate_", suffix=".json", dir=destination.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        return load_config(name, destination.with_name("compatibility.json"))
    finally:
        try:
            os.unlink(name)
        except OSError:
            pass


def save_raw(data: dict[str, Any], path: str | Path | None = None) -> HumanlikeConfig:
    destination = Path(path) if path else default_config_path()
    config = validate_raw(data, target=destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        shutil.copy2(destination, destination.with_suffix(destination.suffix + ".bak"))
    fd, name = tempfile.mkstemp(prefix=".humanlike_save_", suffix=".json", dir=destination.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, destination)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return config


def validate_and_migrate_v2(data: dict[str, Any], *, source_hash: str | None = None) -> FrozenConfigV2:
    """Production v2 validation entry; caller decides whether to persist the result."""
    if data.get("parameter_version") == "CDMJ-AI-PARAMS 1.1.0":
        # Reuse the established 60-field validator before migration; v2 never
        # weakens the Locked v1.1 field/range/cross-constraint contract.
        validate_raw(data)
        migrated = migrate_1_1_to_2_0(data, source_hash=source_hash)
    else:
        migrated = data
    return validate_and_freeze(migrated, source_hash=source_hash)[0]


def save_v2_raw(data: dict[str, Any], path: str | Path, *, source_hash: str | None = None) -> FrozenConfigV2:
    """Atomically persist canonical v2 bytes; this writer never emits v1."""
    destination = Path(path)
    frozen = validate_and_migrate_v2(data, source_hash=source_hash)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".humanlike_v2_", suffix=".json", dir=destination.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(frozen.canonical_bytes)
            stream.write(b"\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, destination)
    finally:
        if os.path.exists(name):
            os.unlink(name)
    return frozen


def config_summary(path: str | Path | None = None) -> dict[str, Any]:
    source = Path(path) if path else default_config_path()
    config = load_config(source)
    return {"parameter_version": config.parameter_version, "config_hash": config.config_hash, "mtime": source.stat().st_mtime}


def launch_settings_window(path: str | Path | None = None) -> subprocess.Popen:
    cmd = [sys.executable, "-m", "players.humanlike.settings_window"]
    if path:
        cmd += ["--config", str(path)]
    return subprocess.Popen(cmd, cwd=str(Path(__file__).resolve().parents[2]))
