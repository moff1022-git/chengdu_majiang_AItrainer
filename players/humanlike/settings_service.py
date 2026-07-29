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


def config_summary(path: str | Path | None = None) -> dict[str, Any]:
    source = Path(path) if path else default_config_path()
    config = load_config(source)
    return {"parameter_version": config.parameter_version, "config_hash": config.config_hash, "mtime": source.stat().st_mtime}


def launch_settings_window(path: str | Path | None = None) -> subprocess.Popen:
    cmd = [sys.executable, "-m", "players.humanlike.settings_window"]
    if path:
        cmd += ["--config", str(path)]
    return subprocess.Popen(cmd, cwd=str(Path(__file__).resolve().parents[2]))

