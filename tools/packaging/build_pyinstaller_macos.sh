#!/usr/bin/env bash
# Build macOS app with PyInstaller (onedir + .app bundle).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

PY="${ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "ERROR: missing $PY — run: bash tools/setup_venv.sh" >&2
  exit 1
fi

echo "==> Installing PyInstaller (if needed)"
"$PY" -m pip install -q "pyinstaller>=6.0"

OUT="${ROOT}/dist/pyinstaller"
WORK="${ROOT}/build/pyinstaller"
rm -rf "$OUT" "$WORK"
mkdir -p "$OUT" "$WORK"

ENTRY="${ROOT}/packaging/macos/pyinstaller_entry.py"
SPEC="${ROOT}/packaging/macos/ChengduMahjongAITrainer.spec"

echo "==> PyInstaller (CLI onedir + windowed app) → $OUT"
# CLI path is more reliable across PyInstaller 6.x than custom collect_all in .spec
"$PY" -m PyInstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name ChengduMahjongAITrainer \
  --osx-bundle-identifier com.moff.chengdu-majiang-aitrainer \
  --paths "$ROOT" \
  --distpath "$OUT" \
  --workpath "$WORK" \
  --specpath "$WORK" \
  --add-data "${ROOT}/assets:assets" \
  --add-data "${ROOT}/configs:configs" \
  --hidden-import app_paths \
  --hidden-import main \
  --hidden-import players.seat_window \
  --hidden-import players.human_proxy \
  --hidden-import players.registry \
  --hidden-import players.rule_ai_player \
  --hidden-import players.random_player \
  --hidden-import players.strategy_presets \
  --hidden-import display.app \
  --hidden-import display.asset_manager \
  --hidden-import engine.orchestrator \
  --hidden-import protocols.subprocess_transport \
  --hidden-import tkinter \
  --hidden-import pygame \
  --collect-submodules engine \
  --collect-submodules players \
  --collect-submodules display \
  --collect-submodules protocols \
  --exclude-module pygame.tests \
  --exclude-module pygame.examples \
  --exclude-module cv2 \
  "$ENTRY"

# Also keep a reference build via .spec (optional second target)
if [[ "${BUILD_SPEC:-0}" == "1" ]]; then
  echo "==> Extra build via .spec"
  "$PY" -m PyInstaller \
    --noconfirm \
    --distpath "${OUT}-spec" \
    --workpath "${WORK}-spec" \
    "$SPEC"
fi

echo ""
echo "Done. Artifacts:"
ls -la "$OUT" || true
APP="$OUT/ChengduMahjongAITrainer.app"
# PyInstaller 6 may nest onedir then BUNDLE, or put .app at dist root
if [[ ! -d "$APP" ]]; then
  APP="$(find "$OUT" -maxdepth 3 -name 'ChengduMahjongAITrainer.app' -type d | head -1 || true)"
fi

if [[ -n "${APP:-}" && -d "$APP" ]]; then
  echo ""
  echo "App: $APP"
  echo "Run:"
  echo "  open \"$APP\""
  echo "  \"$APP/Contents/MacOS/ChengduMahjongAITrainer\""
  echo ""
  echo "Clear quarantine if needed:"
  echo "  xattr -cr \"$APP\""
  # Smoke: binary exists and --help / seat-window -h
  BIN="$APP/Contents/MacOS/ChengduMahjongAITrainer"
  if [[ -x "$BIN" ]]; then
    echo "==> Smoke: --seat-window --help"
    "$BIN" --seat-window --help 2>&1 | head -20 || true
  fi
else
  echo "WARN: .app not found; listing $OUT" >&2
  find "$OUT" -maxdepth 4 2>/dev/null | head -60
fi

echo ""
echo "Docs: docs/packaging/MACOS_BUILD.md"
echo "Logs (when frozen): ~/Library/Application Support/ChengduMahjongAITrainer/logs/"
