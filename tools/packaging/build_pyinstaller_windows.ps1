# Build Windows onedir with PyInstaller (F0025).
# Run from repo root or any cwd; requires .venv on Windows.
# Usage: .\tools\packaging\build_pyinstaller_windows.ps1
$ErrorActionPreference = "Stop"

$ROOT = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $ROOT

$PY = Join-Path $ROOT ".venv\Scripts\python.exe"
if (-not (Test-Path $PY)) {
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd) { $PY = $cmd.Source }
    else {
        Write-Error "Missing .venv and 'python' on PATH — see docs/packaging/WINDOWS_BUILD.md"
    }
    Write-Host "WARN: using system Python: $PY (prefer .venv)"
}

Write-Host "==> Installing PyInstaller (if needed)"
& $PY -m pip install -q "pyinstaller>=6.0"

$APP_VERSION = & $PY -c "from version import APP_VERSION; print(APP_VERSION)"
$APP_NAME = & $PY -c "from version import APP_NAME; print(APP_NAME)"
Write-Host "==> App version $APP_VERSION  name $APP_NAME"

$OUT = Join-Path $ROOT "dist\pyinstaller"
$WORK = Join-Path $ROOT "build\pyinstaller"
if (Test-Path $OUT) { Remove-Item -Recurse -Force $OUT }
if (Test-Path $WORK) { Remove-Item -Recurse -Force $WORK }
New-Item -ItemType Directory -Force -Path $OUT | Out-Null
New-Item -ItemType Directory -Force -Path $WORK | Out-Null

$ENTRY = Join-Path $ROOT "packaging\windows\pyinstaller_entry.py"
if (-not (Test-Path $ENTRY)) {
    Write-Error "Missing entry: $ENTRY"
}

Write-Host "==> PyInstaller onedir (windowed) → $OUT"
# Windows --add-data uses semicolon between source and dest
& $PY -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --onedir `
  --name $APP_NAME `
  --paths $ROOT `
  --distpath $OUT `
  --workpath $WORK `
  --specpath $WORK `
  --add-data "$ROOT\assets;assets" `
  --add-data "$ROOT\configs;configs" `
  --add-data "$ROOT\players\humanlike\parameter_registry_v2.json;players\humanlike" `
  --hidden-import app_paths `
  --hidden-import version `
  --hidden-import main `
  --hidden-import players.seat_window `
  --hidden-import players.human_proxy `
  --hidden-import players.registry `
  --hidden-import players.rule_ai_player `
  --hidden-import players.random_player `
  --hidden-import players.strategy_presets `
  --hidden-import display.app `
  --hidden-import display.asset_manager `
  --hidden-import engine.orchestrator `
  --hidden-import protocols.subprocess_transport `
  --hidden-import tkinter `
  --hidden-import pygame `
  --collect-submodules engine `
  --collect-submodules players `
  --collect-submodules display `
  --collect-submodules protocols `
  --exclude-module pygame.tests `
  --exclude-module pygame.examples `
  --exclude-module cv2 `
  $ENTRY

if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller failed with exit $LASTEXITCODE"
}

$APP_DIR = Join-Path $OUT $APP_NAME
$EXE = Join-Path $APP_DIR "$APP_NAME.exe"
if (-not (Test-Path $EXE)) {
    # PyInstaller 6 may nest differently
    $found = Get-ChildItem -Path $OUT -Recurse -Filter "$APP_NAME.exe" -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($found) {
        $EXE = $found.FullName
        $APP_DIR = $found.DirectoryName
    }
}

if (-not (Test-Path $EXE)) {
    Write-Error "EXE not found under $OUT"
}

Write-Host ""
Write-Host "Done. EXE: $EXE  (v$APP_VERSION)"

# Project-local release copy (gitignore)
$REL_DIR = Join-Path $ROOT "releases\windows"
$REL_APP = Join-Path $REL_DIR "$APP_NAME-PyInstaller"
New-Item -ItemType Directory -Force -Path $REL_DIR | Out-Null
if (Test-Path $REL_APP) { Remove-Item -Recurse -Force $REL_APP }
Copy-Item -Recurse -Force $APP_DIR $REL_APP
Write-Host "Copy: $REL_APP"

Write-Host ""
Write-Host "==> Smoke: --version / --seat-window --help"
& $EXE --version
& $EXE --seat-window --help

Write-Host ""
Write-Host "Run:  $EXE"
Write-Host "Logs: %APPDATA%\ChengduMahjongAITrainer\logs\"
Write-Host "Docs: docs/packaging/WINDOWS_BUILD.md"
