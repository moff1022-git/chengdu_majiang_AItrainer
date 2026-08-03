from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = "parameter_registry_v2.json"


def test_windows_pyinstaller_script_includes_parameter_registry() -> None:
    text = (ROOT / "tools/packaging/build_pyinstaller_windows.ps1").read_text(
        encoding="utf-8"
    )
    assert REGISTRY in text


def test_windows_nuitka_script_includes_parameter_registry() -> None:
    text = (ROOT / "tools/packaging/build_nuitka_windows.ps1").read_text(
        encoding="utf-8"
    )
    assert REGISTRY in text


def test_windows_spec_includes_parameter_registry() -> None:
    text = (ROOT / "packaging/windows/ChengduMahjongAITrainer.spec").read_text(
        encoding="utf-8"
    )
    assert REGISTRY in text
