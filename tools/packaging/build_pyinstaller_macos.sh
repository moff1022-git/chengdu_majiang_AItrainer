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

APP_VERSION="$("$PY" -c 'from version import APP_VERSION; print(APP_VERSION)')"
BUNDLE_ID="$("$PY" -c 'from version import APP_BUNDLE_ID; print(APP_BUNDLE_ID)')"
APP_NAME="$("$PY" -c 'from version import APP_NAME; print(APP_NAME)')"
echo "==> App version ${APP_VERSION}"

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
  --name "${APP_NAME}" \
  --osx-bundle-identifier "${BUNDLE_ID}" \
  --paths "$ROOT" \
  --distpath "$OUT" \
  --workpath "$WORK" \
  --specpath "$WORK" \
  --add-data "${ROOT}/assets:assets" \
  --add-data "${ROOT}/configs:configs" \
  --hidden-import app_paths \
  --hidden-import version \
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
echo "Done. Artifacts (app version ${APP_VERSION}):"
ls -la "$OUT" || true
APP="$OUT/${APP_NAME}.app"
# PyInstaller 6 may nest onedir then BUNDLE, or put .app at dist root
if [[ ! -d "$APP" ]]; then
  APP="$(find "$OUT" -maxdepth 3 -name "${APP_NAME}.app" -type d | head -1 || true)"
fi

if [[ -n "${APP:-}" && -d "$APP" ]]; then
  # Stamp Info.plist short version from version.py
  PLIST="$APP/Contents/Info.plist"
  if [[ -f "$PLIST" ]]; then
    /usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString ${APP_VERSION}" "$PLIST" 2>/dev/null \
      || /usr/libexec/PlistBuddy -c "Add :CFBundleShortVersionString string ${APP_VERSION}" "$PLIST" 2>/dev/null \
      || true
    /usr/libexec/PlistBuddy -c "Set :CFBundleVersion ${APP_VERSION}" "$PLIST" 2>/dev/null \
      || /usr/libexec/PlistBuddy -c "Add :CFBundleVersion string ${APP_VERSION}" "$PLIST" 2>/dev/null \
      || true
  fi
  echo ""
  echo "App: $APP  (v${APP_VERSION})"
  echo "Run:"
  echo "  open \"$APP\""
  echo "  \"$APP/Contents/MacOS/${APP_NAME}\""
  echo ""
  echo "Clear quarantine if needed:"
  echo "  xattr -cr \"$APP\""
  BIN="$APP/Contents/MacOS/${APP_NAME}"
  if [[ -x "$BIN" ]]; then
    echo "==> Smoke: --version / --seat-window --help"
    "$BIN" --version 2>&1 | head -5 || true
    "$BIN" --seat-window --help 2>&1 | head -12 || true
  fi
else
  echo "WARN: .app not found; listing $OUT" >&2
  find "$OUT" -maxdepth 4 2>/dev/null | head -60
fi

# Project-local release copy (alongside Nuitka)
if [[ -n "${APP:-}" && -d "$APP" ]]; then
  REL_DIR="${ROOT}/releases/macos"
  REL_APP="${REL_DIR}/${APP_NAME}-PyInstaller.app"
  mkdir -p "$REL_DIR"
  rm -rf "$REL_APP"
  cp -R "$APP" "$REL_APP"
  xattr -cr "$REL_APP" 2>/dev/null || true
  echo "App (project):  $REL_APP"
fi

echo ""
echo "Docs: docs/packaging/MACOS_BUILD.md · docs/VERSIONING.md"
echo "Logs (when frozen): ~/Library/Application Support/ChengduMahjongAITrainer/logs/"
