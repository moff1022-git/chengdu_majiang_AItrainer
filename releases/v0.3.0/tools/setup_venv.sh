#!/usr/bin/env bash
# Create / repair project virtualenv and install requirements.
# Usage: bash tools/setup_venv.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Prefer 3.12+ (README); fall back to python3 if version ok
pick_python() {
  for c in python3.12 python3.13 python3.11 python3; do
    if command -v "$c" >/dev/null 2>&1; then
      ver="$("$c" -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")')"
      major="${ver%%.*}"
      minor="${ver#*.}"
      if [[ "$major" -gt 3 ]] || { [[ "$major" -eq 3 ]] && [[ "$minor" -ge 11 ]]; }; then
        echo "$c"
        return 0
      fi
    fi
  done
  echo ""
  return 1
}

PY="$(pick_python || true)"
if [[ -z "${PY}" ]]; then
  echo "ERROR: need Python 3.11+ on PATH (found none)."
  echo "  macOS: brew install python@3.12 python-tk@3.12"
  echo "  Or install pyenv and: pyenv install 3.12 && pyenv local 3.12"
  exit 1
fi

echo "Using: $PY ($("$PY" --version 2>&1))"

if [[ ! -d .venv ]] || [[ ! -x .venv/bin/python ]]; then
  echo "Creating .venv ..."
  "$PY" -m venv .venv
else
  echo ".venv exists — reusing"
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
# Optional but commonly used in this repo
python -m pip install -q 'numpy>=1.24' || true

echo ""
echo "=== verify ==="
python -c "import sys; print('python', sys.executable); print('version', sys.version.split()[0])"
python -c "import pygame; print('pygame', pygame.version.ver)"
python -c "import pytest; print('pytest ok')" 2>/dev/null || true
python -c "import tkinter; print('tkinter ok')" 2>/dev/null || echo "WARN: tkinter missing (macOS: brew install python-tk@3.12)"

echo ""
echo "Done. Permanent usage:"
echo "  source .venv/bin/activate"
echo "  # or always call: .venv/bin/python main.py ..."
echo "  # or install direnv + allow .envrc (auto-activate when cd here)"
