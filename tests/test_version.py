"""Application version single source (docs/VERSIONING.md)."""

from __future__ import annotations

import re

import version


def test_app_version_semver_shape() -> None:
    assert re.match(
        r"^\d+\.\d+\.\d+([.-][0-9A-Za-z.-]+)?$",
        version.APP_VERSION,
    ), version.APP_VERSION
    assert version.APP_VERSION_INFO == tuple(
        int(x) for x in version.APP_VERSION.split("-")[0].split(".")[:3]
    )


def test_version_helpers() -> None:
    assert version.version_string() == version.APP_VERSION
    assert version.APP_VERSION in version.APP_DISPLAY
    assert version.APP_NAME
    assert version.APP_BUNDLE_ID.startswith("com.")


def test_cli_version_flag() -> None:
    import subprocess
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    r = subprocess.run(
        [sys.executable, str(root / "main.py"), "--version"],
        capture_output=True,
        text=True,
        cwd=str(root),
        check=False,
    )
    assert r.returncode == 0
    out = (r.stdout or "") + (r.stderr or "")
    assert version.APP_VERSION in out
