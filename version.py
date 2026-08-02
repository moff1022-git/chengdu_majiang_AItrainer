"""
Application version — single source of truth.

Bump rules: docs/VERSIONING.md
Do not hardcode version strings elsewhere; import from here.
"""

from __future__ import annotations

# SemVer: MAJOR.MINOR.PATCH[-prerelease]
APP_VERSION = "0.3.1"
APP_VERSION_INFO = (0, 3, 1)

APP_NAME = "ChengduMahjongAITrainer"
APP_NAME_ZH = "成都麻将AI训练器"
APP_BUNDLE_ID = "com.moff.chengdu-majiang-aitrainer"

# Human-readable one-liner for CLI / about
APP_DISPLAY = f"{APP_NAME_ZH} {APP_VERSION}"


def version_string() -> str:
    """Return APP_VERSION (stable API for packaging scripts)."""
    return APP_VERSION


def ua_string() -> str:
    """Short product identity for logs."""
    return f"{APP_NAME}/{APP_VERSION}"
