# 进度快照

> 2026-07-26 — **F0021 macOS 打包（PyInstaller + Nuitka）Done**

## 本轮

| 项 | 说明 |
|----|------|
| 目标 | 生成 mac 版打包（PyInstaller 与 Nuitka）+ 文档 |
| 规格 | `docs/features/F0021_macos_packaging.md` · **Done** |
| 手册 | `docs/packaging/MACOS_BUILD.md` |
| 脚本 | `tools/packaging/build_pyinstaller_macos.sh` · `build_nuitka_macos.sh` |
| 代码 | `app_paths.py`；资源/子进程路径；`main --seat-window` |
| 产物 | `dist/pyinstaller/…app`（~199MB）· `dist/nuitka/…app`（~97MB） |
| 冒烟 | 两款二进制 `--seat-window --help` 正常 |

## 怎么构建

```bash
bash tools/packaging/build_pyinstaller_macos.sh
bash tools/packaging/build_nuitka_macos.sh
open dist/pyinstaller/ChengduMahjongAITrainer.app
# 或
open dist/nuitka/ChengduMahjongAITrainer.app
```

## 基线

| 项 | 状态 |
|----|------|
| F0020 2H/3H | Done |
| 手牌选中 / 胡牌横幅 / 副露中文 | Done |

## 下一步

| 序 | 动作 | 建议触发语 |
|----|------|------------|
| 1 | 双击 .app 完整开局验收（1H+3AI） | 目视打包版 |
| 2 | （可选）加应用图标 / codesign | `打包签名` |
| 3 | （可选）Windows 打包文档 | `Windows 打包` |
