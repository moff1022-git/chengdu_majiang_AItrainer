#!/usr/bin/env python3
"""Backup full program + docs to backup/<date>/ excluding caches and nested backups."""
from __future__ import annotations

import os
import shutil
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "venv",
    ".venv",
    "env",
    "node_modules",
    "backup",
    ".grok",
}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".pyd"}
EXCLUDE_NAMES = {".DS_Store", "Thumbs.db"}


def should_skip(path: Path) -> bool:
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        return True
    if any(p in EXCLUDE_DIRS for p in rel.parts):
        return True
    if path.name in EXCLUDE_NAMES:
        return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    return False


def main() -> Path:
    stamp = date.today().isoformat()
    backup_root = ROOT / "backup"
    dest = backup_root / stamp
    if dest.exists():
        dest = backup_root / f"{stamp}_{datetime.now().strftime('%H%M%S')}"

    dest.mkdir(parents=True, exist_ok=False)
    n_files = 0
    n_bytes = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dp = Path(dirpath)
        try:
            rel_dir = dp.relative_to(ROOT)
        except ValueError:
            continue
        if any(p in EXCLUDE_DIRS for p in rel_dir.parts):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            src = dp / fn
            if should_skip(src):
                continue
            rel = src.relative_to(ROOT)
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
            n_files += 1
            n_bytes += src.stat().st_size

    manifest = dest / "BACKUP_MANIFEST.txt"
    manifest.write_text(
        "\n".join(
            [
                "Backup of chengdu_majiang_AItrainer",
                f"Date folder: {dest.name}",
                f"Source: {ROOT}",
                f"Created: {datetime.now().isoformat(timespec='seconds')}",
                f"Files: {n_files}",
                f"Bytes: {n_bytes}",
                f"Excluded dirs: {sorted(EXCLUDE_DIRS)}",
                "Purpose: Pre-implementation snapshot before F0018 UI layout work",
                "Contents: full program source + docs + assets (no venv/git/cache/backup)",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"DEST={dest}")
    print(f"FILES={n_files}")
    print(f"BYTES={n_bytes}")
    print(f"MANIFEST={manifest}")
    return dest


if __name__ == "__main__":
    main()
