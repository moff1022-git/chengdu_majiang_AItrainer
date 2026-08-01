# F0027 — Windows MSI 安装程序

| 字段 | 值 |
|------|-----|
| **编号** | F0027 |
| **标题** | Windows MSI installer (WiX) over PyInstaller onedir |
| **状态** | **`Done`**（WiX 3.14 MSI 脚本与实现已落地） |
| **类型** | 工程交付：MSI 安装包 + 构建脚本 |
| **依赖** | F0025（Windows PyInstaller onedir） |
| **文档** | [`docs/packaging/WINDOWS_BUILD.md`](../packaging/WINDOWS_BUILD.md) §MSI |
| **关联代码** | `tools/packaging/build_msi_windows.ps1`、`packaging/windows/msi/*` |
| **版本线** | `version.py` → MSI `Product/@Version`（补第四段 `.0`） |

---

## 1. 背景

- F0025 **O3** 曾将 MSI/安装器列为 Out of Scope；现用户要求 **MSI**。
- 已有 zip 分发（onedir）；MSI 便于「安装到 Program Files、开始菜单、卸载」。

## 2. 目标

| ID | 目标 |
|----|------|
| G1 | 从 **PyInstaller onedir** 生成 **x64 per-machine MSI** |
| G2 | 默认安装目录：`%ProgramFiles%\ChengduMahjongAITrainer\` |
| G3 | 开始菜单快捷方式（启动主程序 exe） |
| G4 | 控制面板 /「应用和功能」可卸载（MajorUpgrade） |
| G5 | 版本号来自 `version.py`，不硬编码第二套 |
| G6 | 一键脚本：`tools/packaging/build_msi_windows.ps1` |

### Out of Scope

| # | 项 |
|---|-----|
| O1 | Authenticode 签名（F0025 O4） |
| O2 | MSIX / Store / Inno / NSIS（本 F 仅 MSI） |
| O3 | 自定义复杂 UI 皮肤 / 多语言完整本地化（可中文产品名） |
| O4 | 将 Nuitka 树另打 MSI（可选后续；默认 **仅 PyInstaller**） |
| O5 | macOS / Linux 安装器 |

## 3. 设计

```text
PyInstaller onedir (F0025)
        │
        ▼
  heat.exe harvest → AppFiles.wxs
  Product.wxs（固定 UpgradeCode）
        │
        ▼
  candle + light (WiX 3.14 binaries)
        │
        ▼
  ChengduMahjongAITrainer-{ver}-windows-x64.msi
```

| 项 | 约定 |
|----|------|
| 工具 | **WiX Toolset 3.14** 二进制包（脚本自动下载到 `%LOCALAPPDATA%\wix314`，不进 git） |
| 范围 | `InstallScope=perMachine` · `Platform=x64` |
| UpgradeCode | 固定 GUID（同一产品线升级） |
| ProductCode | `*` 自动 |
| 压缩 | `MediaTemplate EmbedCab=yes`（单文件 MSI） |
| 快捷方式 | 开始菜单「成都麻将AI训练器」→ `ChengduMahjongAITrainer.exe` |
| 数据 | 运行时日志仍写 `%APPDATA%\…`（`app_paths`，不写 Program Files） |
| **中文** | `Language=2052` + **`Codepage=936`（GBK）**；构建时 `gen_msi_product_wxs.py` 写 GBK 源（**禁止** 65001/UTF-8 入库，否则 ARP 乱码） |

## 4. 交付清单

| 路径 | 说明 |
|------|------|
| `docs/features/F0027_windows_msi.md` | 本规格 |
| `packaging/windows/msi/Product.wxs` | 产品骨架（变量由 candle `-d` 注入） |
| `tools/packaging/build_msi_windows.ps1` | 下载 WiX / heat / candle / light |
| `docs/packaging/WINDOWS_BUILD.md` | §MSI 手册 |
| README / changelog / LATEST / 索引 | 同步 |

## 5. 验收

| ID | 项 |
|----|-----|
| M1 | 脚本生成 `dist\msi\*.msi` |
| M2 | 双击/ `msiexec /i` 安装到 Program Files |
| M3 | 开始菜单可启动大厅 |
| M4 | 卸载干净（快捷方式与目录移除；AppData 日志可保留） |
| M5 | 更高版本 MSI 可 MajorUpgrade（同 UpgradeCode） |

## 6. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-26 | Approved + Done | 用户要求创建 MSI；WiX 3.14 + PyInstaller onedir |
