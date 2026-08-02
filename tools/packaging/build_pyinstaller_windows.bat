@echo off
REM Double-click / cmd entry for Windows PyInstaller build (F0025).
cd /d "%~dp0..\.."
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build_pyinstaller_windows.ps1"
exit /b %ERRORLEVEL%
