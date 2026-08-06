from pathlib import Path


def test_macos_builds_accept_restored_venv_name():
    for name in ("build_pyinstaller_macos.sh", "build_nuitka_macos.sh"):
        text = (Path("tools/packaging") / name).read_text()
        assert '.venv/bin/python' in text
        assert '.venv-macos/bin/python' in text
        assert '[[ -x "$PY" ]] ||' in text
