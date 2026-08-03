# Build Windows standalone with Nuitka (F0025).
# Requires C compiler (MSVC Build Tools or MinGW). Prefer PyInstaller if MSVC missing.
# Usage: .\tools\packaging\build_nuitka_windows.ps1
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

Write-Host "==> Installing Nuitka (if needed)"
& $PY -m pip install -q "nuitka>=2.0" ordered-set zstandard

$APP_VERSION = & $PY -c "from version import APP_VERSION; print(APP_VERSION)"
$APP_NAME = & $PY -c "from version import APP_NAME; print(APP_NAME)"
Write-Host "==> App version $APP_VERSION  name $APP_NAME"

$OUT = Join-Path $ROOT "dist\nuitka"
if (Test-Path $OUT) { Remove-Item -Recurse -Force $OUT }
New-Item -ItemType Directory -Force -Path $OUT | Out-Null

$ENTRY = Join-Path $ROOT "packaging\windows\pyinstaller_entry.py"
if (-not (Test-Path $ENTRY)) {
    Write-Error "Missing entry: $ENTRY"
}

$env:PYTHONPATH = if ($env:PYTHONPATH) { "$ROOT;$env:PYTHONPATH" } else { $ROOT }

Write-Host "==> Nuitka standalone → $OUT"
# First build is slow (C compile + link). --lto=no keeps link time reasonable.
# --windows-console-mode=disable may fail on some Nuitka/gcc combos; we retry.
$common = @(
    "--standalone",
    "--lto=no",
    "--enable-plugin=tk-inter",
    "--include-package=engine",
    "--include-package=players",
    "--include-package=display",
    "--include-package=protocols",
    "--include-package=training",
    "--include-module=main",
    "--include-module=app_paths",
    "--include-module=version",
    "--include-data-dir=${ROOT}\assets=assets",
    "--include-data-dir=${ROOT}\configs=configs",
    "--include-data-file=${ROOT}\players\humanlike\parameter_registry_v2.json=players/humanlike/parameter_registry_v2.json",
    "--output-dir=$OUT",
    "--output-filename=$APP_NAME.exe",
    "--assume-yes-for-downloads",
    $ENTRY
)

& $PY -m nuitka --windows-console-mode=disable @common
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "WARN: Nuitka with --windows-console-mode=disable failed (exit $LASTEXITCODE)."
    Write-Host "Retrying without console-mode (gcc may still be downloading on first run)..."
    & $PY -m nuitka @common
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Nuitka failed with exit $LASTEXITCODE (need MSVC or allow MinGW auto-download)"
    }
}

# Nuitka often produces pyinstaller_entry.dist/
$DIST = Join-Path $OUT "pyinstaller_entry.dist"
if (-not (Test-Path $DIST)) {
    $DIST = Get-ChildItem -Path $OUT -Directory -Filter "*.dist" -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty FullName
}

$EXE = $null
if ($DIST -and (Test-Path $DIST)) {
    $cand = Join-Path $DIST "$APP_NAME.exe"
    if (Test-Path $cand) { $EXE = $cand }
    else {
        $found = Get-ChildItem -Path $DIST -Filter "*.exe" | Select-Object -First 1
        if ($found) { $EXE = $found.FullName }
    }
}
if (-not $EXE) {
    $found = Get-ChildItem -Path $OUT -Recurse -Filter "$APP_NAME.exe" -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($found) {
        $EXE = $found.FullName
        $DIST = $found.DirectoryName
    }
}

if (-not $EXE -or -not (Test-Path $EXE)) {
    Write-Error "Nuitka EXE not found under $OUT"
}

Write-Host ""
Write-Host "Done. EXE: $EXE  (v$APP_VERSION)"

# Project-local release copy
$REL_DIR = Join-Path $ROOT "releases\windows"
$REL_APP = Join-Path $REL_DIR "$APP_NAME-Nuitka"
New-Item -ItemType Directory -Force -Path $REL_DIR | Out-Null
if (Test-Path $REL_APP) { Remove-Item -Recurse -Force $REL_APP }
Copy-Item -Recurse -Force $DIST $REL_APP
Write-Host "Copy: $REL_APP"

Write-Host ""
Write-Host "==> Smoke: --version / --seat-window --help"
& $EXE --version
& $EXE --seat-window --help

Write-Host ""
Write-Host "Run:  $EXE"
Write-Host "Logs: %APPDATA%\ChengduMahjongAITrainer\logs\"
Write-Host "Docs: docs/packaging/WINDOWS_BUILD.md"
