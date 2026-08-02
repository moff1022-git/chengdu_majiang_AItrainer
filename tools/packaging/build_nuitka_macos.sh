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

APP_VERSION="$("$PY" -c 'from version import APP_VERSION; print(APP_VERSION)')"
APP_NAME_ZH="$("$PY" -c 'from version import APP_NAME_ZH; print(APP_NAME_ZH)')"
APP_NAME="$("$PY" -c 'from version import APP_NAME; print(APP_NAME)')"
echo "==> App version ${APP_VERSION}"

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
  --macos-app-name="${APP_NAME_ZH}" \
  --macos-app-version="${APP_VERSION}" \
  --macos-app-icon=none \
  --enable-plugin=tk-inter \
  --include-package=engine \
  --include-package=players \
  --include-package=display \
  --include-package=protocols \
  --include-package=training \
  --include-module=main \
  --include-module=app_paths \
  --include-module=version \
  --include-data-dir="${ROOT}/assets=assets" \
  --include-data-dir="${ROOT}/configs=configs" \
  --include-data-file="${ROOT}/players/humanlike/parameter_registry_v2.json=players/humanlike/parameter_registry_v2.json" \
  --output-dir="$OUT" \
  --output-filename="${APP_NAME}" \
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
    --include-module=version \
    --include-data-dir="${ROOT}/assets=assets" \
    --include-data-dir="${ROOT}/configs=configs" \
    --include-data-file="${ROOT}/players/humanlike/parameter_registry_v2.json=players/humanlike/parameter_registry_v2.json" \
    --output-dir="$OUT" \
    --output-filename="${APP_NAME}" \
    --assume-yes-for-downloads \
    "$ENTRY"
fi

# Nuitka names the .app after the entry script (pyinstaller_entry.app) — normalize
if [[ -d "$OUT/pyinstaller_entry.app" ]]; then
  rm -rf "$OUT/${APP_NAME}.app"
  mv "$OUT/pyinstaller_entry.app" "$OUT/${APP_NAME}.app"
fi

echo ""
echo "Done. Artifacts under $OUT (v${APP_VERSION}):"
ls -la "$OUT" || true
find "$OUT" -maxdepth 3 \( -name "*.app" -o -name "${APP_NAME}*" \) 2>/dev/null | head -40

APP="$OUT/${APP_NAME}.app"
if [[ -d "$APP" ]]; then
  RESOURCE_ROOT="$APP/Contents/MacOS"
  echo "==> Verify bundled runtime resources"
  test -d "$RESOURCE_ROOT/assets"
  test -d "$RESOURCE_ROOT/configs"
  test -f "$RESOURCE_ROOT/players/humanlike/parameter_registry_v2.json"

  # Project-local release copy (easier to find than dist/nuitka/)
  REL_DIR="${ROOT}/releases/macos"
  REL_APP="${REL_DIR}/${APP_NAME}-Nuitka.app"
  mkdir -p "$REL_DIR"
  rm -rf "$REL_APP"
  cp -R "$APP" "$REL_APP"
  xattr -cr "$REL_APP" 2>/dev/null || true
  echo ""
  echo "App (build):    $APP  (v${APP_VERSION})"
  echo "App (project):  $REL_APP"
  echo "NOTE: Nuitka aborts if the .app lives under non-ASCII paths (e.g. Chinese OneDrive)."
  echo "Smoke-test via /tmp copy:"
  rm -rf "/tmp/${APP_NAME}.app"
  cp -R "$APP" "/tmp/${APP_NAME}.app"
  BIN="/tmp/${APP_NAME}.app/Contents/MacOS/${APP_NAME}"
  if [[ -x "$BIN" ]]; then
    echo "==> Smoke: --version / --seat-window --help (from /tmp)"
    "$BIN" --version
    "$BIN" --seat-window --help >/dev/null
  fi
  echo "Recommended run (ASCII path):"
  echo "  cp -R \"$REL_APP\" /Applications/"
  echo "  open /Applications/${APP_NAME}.app"
else
  echo "ERROR: Nuitka .app not found under $OUT" >&2
  exit 1
fi

echo ""
echo "Docs: docs/packaging/MACOS_BUILD.md · docs/VERSIONING.md"
echo "Logs (frozen): ~/Library/Application Support/ChengduMahjongAITrainer/logs/"
