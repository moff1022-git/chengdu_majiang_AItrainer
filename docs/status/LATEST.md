# 进度快照

> 2026-07-26 — **F0025 Windows 打包文档 Draft**

## 本轮

| 项 | 说明 |
|----|------|
| 目标 | Windows 打包（Docs-First） |
| 规格 | [`docs/features/F0025_windows_packaging.md`](../features/F0025_windows_packaging.md) → **Draft** |
| 手册 | [`docs/packaging/WINDOWS_BUILD.md`](../packaging/WINDOWS_BUILD.md) |
| 应用版本 | **0.2.1**（未升版；本轮仅文档） |
| 代码 | **未改业务**；打包脚本待 Approved 后实现 |
| 远程 | 已 commit 并 push（F0025 Draft 文档基线） |

## 要点

- 与 F0021 同模式：**onedir + 同一 exe `--seat-window` 再入**
- 必须在 **Windows 主机** 构建（无 macOS 交叉编译）
- 可写数据：`%APPDATA%\ChengduMahjongAITrainer\`（`app_paths` 已支持）
- `--add-data` 用 **`;`**；优先 PyInstaller，Nuitka 需 MSVC/MinGW
- Out of scope：MSI 安装器、Authenticode、Linux

## 版本线

| 线 | 值 |
|----|-----|
| APP | **0.2.1** |
| schema | 4 |
| format | 1 |
| wire | 1 |

## 打包 / 下载

| 位置 | 说明 |
|------|------|
| **GitHub Release v0.2.1** | macOS zip（PyInstaller / Nuitka） |
| Windows 产物 | **尚未构建**；见 F0025 |
| 本机 `releases/macos/` | macOS `.app` 副本（gitignore） |

## 下一步

| 序 | 动作 | 建议触发语 |
|----|------|------------|
| 1 | 审阅并批准 F0025 + WINDOWS_BUILD | `确认 F0025` / `确认文档` |
| 2 | 实现 `packaging/windows/*` + `build_*_windows.ps1` | `实现 Windows 打包` |
| 3 | 在 Windows 机按手册构建并验收 W1–W11 | `验收 Windows 包` |
| 4 | 可选：Release 附加 windows-x64 zip | `上传 Windows Release` |
