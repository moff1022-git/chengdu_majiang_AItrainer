# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for macOS — Chengdu Mahjong AI Trainer
# Prefer: bash tools/packaging/build_pyinstaller_macos.sh

from pathlib import Path

block_cipher = None

# SPECPATH is injected by PyInstaller when executing the spec
_spec = Path(SPECPATH).resolve()  # type: ignore[name-defined]
if _spec.name == "macos" or (_spec / "pyinstaller_entry.py").is_file():
    SPEC_DIR = _spec if _spec.is_dir() else _spec.parent
else:
    SPEC_DIR = _spec.parent
ROOT = SPEC_DIR.parents[1] if SPEC_DIR.name == "macos" else SPEC_DIR.parent
ENTRY = SPEC_DIR / "pyinstaller_entry.py"
if not ENTRY.is_file():
    ENTRY = ROOT / "packaging" / "macos" / "pyinstaller_entry.py"
    ROOT = ENTRY.parents[2]

datas = [
    (str(ROOT / "assets"), "assets"),
    (str(ROOT / "configs"), "configs"),
]

hiddenimports = [
    "app_paths",
    "main",
    "players",
    "players.seat_window",
    "players.human_proxy",
    "players.registry",
    "players.rule_ai_player",
    "players.random_player",
    "players.strategy_presets",
    "players.analysis",
    "players.analysis.discard_recommend",
    "display",
    "display.app",
    "display.asset_manager",
    "engine",
    "engine.orchestrator",
    "protocols",
    "protocols.subprocess_transport",
    "training",
    "tkinter",
    "pygame",
]

a = Analysis(  # type: ignore[name-defined]
    [str(ENTRY)],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)  # type: ignore[name-defined]

exe = EXE(  # type: ignore[name-defined]
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ChengduMahjongAITrainer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(  # type: ignore[name-defined]
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="ChengduMahjongAITrainer",
)

# Version from single source (version.py)
import sys

sys.path.insert(0, str(ROOT))
try:
    from version import APP_BUNDLE_ID, APP_NAME, APP_NAME_ZH, APP_VERSION
except Exception:
    APP_VERSION = "0.0.0"
    APP_NAME = "ChengduMahjongAITrainer"
    APP_NAME_ZH = "成都麻将AI训练器"
    APP_BUNDLE_ID = "com.moff.chengdu-majiang-aitrainer"

app = BUNDLE(  # type: ignore[name-defined]
    coll,
    name=f"{APP_NAME}.app",
    icon=None,
    bundle_identifier=APP_BUNDLE_ID,
    info_plist={
        "CFBundleDisplayName": APP_NAME_ZH,
        "CFBundleName": APP_NAME,
        "CFBundleShortVersionString": APP_VERSION,
        "CFBundleVersion": APP_VERSION,
        "NSHighResolutionCapable": True,
        "LSRequiresAquaSystemAppearance": False,
    },
)
