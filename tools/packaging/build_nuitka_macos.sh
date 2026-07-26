#!/usr/bin/env bash
# Build macOS app/standalone with Nuitka.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

PY="${ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "ERROR: missing $PY — run: bash tools/setup_venv.sh" >&2
  exit 1
fi

echo "==> Installing Nuitka (if needed)"
"$PY" -m pip install -q "nuitka>=2.0" ordered-set zstandard

OUT="${ROOT}/dist/nuitka"
rm -rf "$OUT"
mkdir -p "$OUT"

ENTRY="${ROOT}/packaging/macos/pyinstaller_entry.py"
# Nuitka needs entry under a path it can compile; keep project root on PYTHONPATH
export PYTHONPATH="${ROOT}${PYTHONPATH:+:$PYTHONPATH}"

echo "==> Nuitka standalone + app bundle → $OUT"
# Note: first build is slow (C compile).
set +e
"$PY" -m nuitka \
  --standalone \
  --macos-create-app-bundle \
  --macos-app-name="成都麻将AI训练器" \
  --macos-app-icon=none \
  --enable-plugin=tk-inter \
  --include-package=engine \
  --include-package=players \
  --include-package=display \
  --include-package=protocols \
  --include-package=training \
  --include-module=main \
  --include-module=app_paths \
  --include-data-dir="${ROOT}/assets=assets" \
  --include-data-dir="${ROOT}/configs=configs" \
  --output-dir="$OUT" \
  --output-filename=ChengduMahjongAITrainer \
  --assume-yes-for-downloads \
  "$ENTRY"
STATUS=$?
set -e

if [[ $STATUS -ne 0 ]]; then
  echo ""
  echo "WARN: app-bundle build failed (exit $STATUS). Retrying standalone without --macos-create-app-bundle..."
  "$PY" -m nuitka \
    --standalone \
    --enable-plugin=tk-inter \
    --include-package=engine \
    --include-package=players \
    --include-package=display \
    --include-package=protocols \
    --include-package=training \
    --include-module=main \
    --include-module=app_paths \
    --include-data-dir="${ROOT}/assets=assets" \
    --include-data-dir="${ROOT}/configs=configs" \
    --output-dir="$OUT" \
    --output-filename=ChengduMahjongAITrainer \
    --assume-yes-for-downloads \
    "$ENTRY"
fi

# Nuitka names the .app after the entry script (pyinstaller_entry.app) — normalize
if [[ -d "$OUT/pyinstaller_entry.app" ]]; then
  rm -rf "$OUT/ChengduMahjongAITrainer.app"
  mv "$OUT/pyinstaller_entry.app" "$OUT/ChengduMahjongAITrainer.app"
fi

echo ""
echo "Done. Artifacts under $OUT:"
ls -la "$OUT" || true
find "$OUT" -maxdepth 3 \( -name "*.app" -o -name "ChengduMahjongAITrainer*" \) 2>/dev/null | head -40

APP="$OUT/ChengduMahjongAITrainer.app"
if [[ -d "$APP" ]]; then
  echo ""
  echo "App: $APP"
  echo "NOTE: Nuitka aborts if the .app lives under non-ASCII paths (e.g. Chinese OneDrive)."
  echo "Smoke-test via /tmp copy:"
  rm -rf /tmp/ChengduMahjongAITrainer.app
  cp -R "$APP" /tmp/ChengduMahjongAITrainer.app
  BIN="/tmp/ChengduMahjongAITrainer.app/Contents/MacOS/ChengduMahjongAITrainer"
  if [[ -x "$BIN" ]]; then
    echo "==> Smoke: --seat-window --help (from /tmp)"
    "$BIN" --seat-window --help 2>&1 | head -16 || true
  fi
  echo "Recommended run:"
  echo "  cp -R \"$APP\" /Applications/"
  echo "  open /Applications/ChengduMahjongAITrainer.app"
fi

echo ""
echo "Docs: docs/packaging/MACOS_BUILD.md"
echo "Logs (frozen): ~/Library/Application Support/ChengduMahjongAITrainer/logs/"
