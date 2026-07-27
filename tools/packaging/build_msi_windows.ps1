# Build Windows x64 MSI (WiX 3.14) from PyInstaller onedir — F0027.
# Prerequisites: Windows; PyInstaller onedir (builds if missing).
# Usage: .\tools\packaging\build_msi_windows.ps1
# Optional: -SkipPyInstaller  (require existing dist\pyinstaller\...)
param(
    [switch]$SkipPyInstaller
)
$ErrorActionPreference = "Stop"

$ROOT = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $ROOT

function Get-Python {
    $venvPy = Join-Path $ROOT ".venv\Scripts\python.exe"
    if (Test-Path $venvPy) { return $venvPy }
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    Write-Error "No Python found (.venv or PATH)."
}

$PY = Get-Python
Write-Host "Python: $PY"

$APP_VERSION = & $PY -c "from version import APP_VERSION; print(APP_VERSION)"
$APP_NAME = & $PY -c "from version import APP_NAME; print(APP_NAME)"
$APP_NAME_ZH = & $PY -c "from version import APP_NAME_ZH; print(APP_NAME_ZH)"
# MSI Product Version: up to 4 numeric parts
$ProductVersion = if ($APP_VERSION -match '^\d+\.\d+\.\d+$') { "$APP_VERSION.0" } else { $APP_VERSION }
$Manufacturer = "moff1022-git"

Write-Host "==> App $APP_NAME v$APP_VERSION  MSI ProductVersion=$ProductVersion"

# --- PyInstaller onedir ---
$AppDir = Join-Path $ROOT "dist\pyinstaller\$APP_NAME"
$Exe = Join-Path $AppDir "$APP_NAME.exe"
if (-not (Test-Path $Exe)) {
    if ($SkipPyInstaller) {
        Write-Error "Missing $Exe and -SkipPyInstaller set. Run build_pyinstaller_windows.ps1 first."
    }
    Write-Host "==> PyInstaller onedir missing; building..."
    & (Join-Path $ROOT "tools\packaging\build_pyinstaller_windows.ps1")
    if (-not (Test-Path $Exe)) {
        Write-Error "Still missing $Exe after PyInstaller build."
    }
}

# --- WiX 3.14 binaries ---
$WixRoot = Join-Path $env:LOCALAPPDATA "wix314"
$Heat = Join-Path $WixRoot "heat.exe"
$Candle = Join-Path $WixRoot "candle.exe"
$Light = Join-Path $WixRoot "light.exe"

if (-not ((Test-Path $Heat) -and (Test-Path $Candle) -and (Test-Path $Light))) {
    Write-Host "==> Downloading WiX 3.14 binaries..."
    $zip = Join-Path $env:TEMP "wix314-binaries.zip"
    $url = "https://github.com/wixtoolset/wix3/releases/download/wix3141rtm/wix314-binaries.zip"
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
    if (Test-Path $WixRoot) { Remove-Item -Recurse -Force $WixRoot }
    New-Item -ItemType Directory -Force -Path $WixRoot | Out-Null
    Expand-Archive -Path $zip -DestinationPath $WixRoot -Force
    if (-not (Test-Path $Candle)) {
        Write-Error "WiX extract failed; candle.exe not at $Candle"
    }
    Write-Host "WiX installed to $WixRoot"
}

# WiX 3 candle/light mishandle spaces in paths (CNDL0117). Stage under ASCII temp.
$StageRoot = Join-Path $env:TEMP "chengdu_msi_$APP_VERSION"
$Work = Join-Path $StageRoot "wixobj"
$StageApp = Join-Path $StageRoot "app"
$OutDir = Join-Path $ROOT "dist\msi"
if (Test-Path $StageRoot) { Remove-Item -Recurse -Force $StageRoot }
New-Item -ItemType Directory -Force -Path $Work | Out-Null
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

Write-Host "==> Stage onedir → $StageApp (ASCII path for WiX)"
Copy-Item -Recurse -Force $AppDir $StageApp

$ProductWxsSrc = Join-Path $ROOT "packaging\windows\msi\Product.wxs"
$ProductWxs = Join-Path $StageRoot "Product.wxs"
Copy-Item -Force $ProductWxsSrc $ProductWxs
$HarvestWxs = Join-Path $StageRoot "AppFiles.wxs"
$MsiName = "$APP_NAME-$APP_VERSION-windows-x64.msi"
$MsiPath = Join-Path $OutDir $MsiName
$StageMsi = Join-Path $StageRoot $MsiName

Write-Host "==> heat: harvest $StageApp"
& $Heat dir $StageApp `
    -cg AppFiles `
    -gg `
    -scom `
    -sreg `
    -sfrag `
    -srd `
    -dr INSTALLDIR `
    -var var.SourceDir `
    -out $HarvestWxs
if ($LASTEXITCODE -ne 0) { Write-Error "heat failed ($LASTEXITCODE)" }

Write-Host "==> candle"
Push-Location $StageRoot
try {
    # Run from stage dir so -out . is space-free; define SourceDir without spaces
    & $Candle -nologo -arch x64 `
        "-dSourceDir=$StageApp" `
        "-dProductVersion=$ProductVersion" `
        "-dProductNameZh=$APP_NAME_ZH" `
        "-dManufacturer=$Manufacturer" `
        -out "$Work\\" `
        $ProductWxs `
        $HarvestWxs
    if ($LASTEXITCODE -ne 0) { Write-Error "candle failed ($LASTEXITCODE)" }

    Write-Host "==> light"
    $ProductObj = Join-Path $Work "Product.wixobj"
    $HarvestObj = Join-Path $Work "AppFiles.wixobj"
    # Suppress noisy ICE60 (font language) if any; fail on real errors
    & $Light -nologo -sice:ICE60 -out $StageMsi $ProductObj $HarvestObj
    if ($LASTEXITCODE -ne 0) { Write-Error "light failed ($LASTEXITCODE)" }
}
finally {
    Pop-Location
}

Copy-Item -Force $StageMsi $MsiPath

if (-not (Test-Path $MsiPath)) {
    Write-Error "MSI not created: $MsiPath"
}

# Project-local copy (gitignore covers releases/windows/** except README)
$RelDir = Join-Path $ROOT "releases\windows"
New-Item -ItemType Directory -Force -Path $RelDir | Out-Null
$RelMsi = Join-Path $RelDir $MsiName
Copy-Item -Force $MsiPath $RelMsi

$mb = [math]::Round((Get-Item $MsiPath).Length / 1MB, 1)
Write-Host ""
Write-Host "Done. MSI: $MsiPath  ($mb MB)"
Write-Host "Copy: $RelMsi"
Write-Host ""
Write-Host "Install (elevated):"
Write-Host "  msiexec /i `"$MsiPath`""
Write-Host "Silent:"
Write-Host "  msiexec /i `"$MsiPath`" /qn"
Write-Host "Uninstall (after install, use ARP or):"
Write-Host "  msiexec /x `"$MsiPath`""
Write-Host "Docs: docs/packaging/WINDOWS_BUILD.md · F0027"
