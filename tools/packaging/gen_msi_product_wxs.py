#!/usr/bin/env python3
"""
Generate Product.wxs as **GBK (cp936)** for WiX MSI Chinese display (F0027).

Windows Installer string tables are ANSI code-page based. For zh-CN use 936,
not UTF-8/65001 (which often shows as mojibake in ARP / Start Menu).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure repo root on path when run as script
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from version import APP_NAME, APP_NAME_ZH, APP_VERSION  # noqa: E402


def product_version(ver: str) -> str:
    if ver.count(".") == 2 and all(p.isdigit() for p in ver.split(".")):
        return f"{ver}.0"
    return ver


def build_wxs(
    *,
    product_name_zh: str,
    product_version: str,
    manufacturer: str,
) -> str:
    # All user-visible Chinese embedded here; file saved as gb2312/gbk.
    downgrade = "已安装更新的版本，无法降级安装。"
    feature_desc = "主程序、资源与座位窗依赖（PyInstaller onedir）"
    shortcut_desc = "成都麻将 AI 训练器"
    comments = "Chengdu Mahjong AI Trainer Windows x64 MSI (F0027)"

    # Escape XML special chars in dynamic strings
    def esc(s: str) -> str:
        return (
            s.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    name = esc(product_name_zh)
    manuf = esc(manufacturer)
    ver = esc(product_version)
    return f"""<?xml version="1.0" encoding="gb2312"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product
      Id="*"
      Name="{name}"
      Language="2052"
      Codepage="936"
      Version="{ver}"
      Manufacturer="{manuf}"
      UpgradeCode="A7B3C1D2-E4F5-6789-ABCD-EF0123456789">

    <Package
        InstallerVersion="500"
        Compressed="yes"
        InstallScope="perMachine"
        Platform="x64"
        Description="{name} {ver}"
        Comments="{esc(comments)}"
        Manufacturer="{manuf}" />

    <MajorUpgrade
        DowngradeErrorMessage="{esc(downgrade)}"
        Schedule="afterInstallInitialize" />

    <MediaTemplate EmbedCab="yes" CompressionLevel="high" />

    <Feature Id="MainFeature" Title="{name}" Level="1"
             Description="{esc(feature_desc)}">
      <ComponentGroupRef Id="AppFiles" />
      <ComponentRef Id="StartMenuShortcut" />
    </Feature>

    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFiles64Folder">
        <Directory Id="INSTALLDIR" Name="{esc(APP_NAME)}" />
      </Directory>
      <Directory Id="ProgramMenuFolder">
        <Directory Id="ApplicationProgramsFolder" Name="{name}" />
      </Directory>
    </Directory>

    <DirectoryRef Id="ApplicationProgramsFolder">
      <Component Id="StartMenuShortcut" Guid="B8C4D2E3-F5A6-7890-BCDE-F12345678901">
        <Shortcut
            Id="MainStartMenuShortcut"
            Name="{name}"
            Description="{esc(shortcut_desc)}"
            Target="[INSTALLDIR]{esc(APP_NAME)}.exe"
            WorkingDirectory="INSTALLDIR"
            Advertise="no" />
        <RemoveFolder Id="RemoveApplicationProgramsFolder" Directory="ApplicationProgramsFolder" On="uninstall" />
        <RegistryValue
            Root="HKCU"
            Key="Software\\ChengduMahjongAITrainer"
            Name="StartMenuShortcut"
            Type="integer"
            Value="1"
            KeyPath="yes" />
      </Component>
    </DirectoryRef>

    <Property Id="ARPURLINFOABOUT" Value="https://github.com/moff1022-git/chengdu_majiang_AItrainer" />
    <Property Id="ARPHELPLINK" Value="https://github.com/moff1022-git/chengdu_majiang_AItrainer/releases" />
  </Product>
</Wix>
"""


def main() -> int:
    p = argparse.ArgumentParser(description="Generate GBK Product.wxs for WiX MSI")
    p.add_argument("-o", "--output", type=Path, required=True, help="Output .wxs path")
    p.add_argument("--manufacturer", default="moff1022-git")
    args = p.parse_args()

    ver = product_version(APP_VERSION)
    text = build_wxs(
        product_name_zh=APP_NAME_ZH,
        product_version=ver,
        manufacturer=args.manufacturer,
    )
    # Windows code page 936 (GBK); gb2312 is the XML encoding label WiX accepts
    data = text.encode("gbk", errors="strict")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    print(f"Wrote {args.output} ({len(data)} bytes, gbk) name={APP_NAME_ZH!r} ver={ver}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
