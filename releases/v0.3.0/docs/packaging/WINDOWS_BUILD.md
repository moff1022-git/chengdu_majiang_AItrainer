# Windows 打包指南（PyInstaller · Nuitka）

| 字段 | 值 |
|------|-----|
| **平台** | Windows 10/11 **x64**（优先；ARM64 另标） |
| **构建机** | **必须在 Windows 上构建**（不支持从 macOS 交叉编译） |
| **入口** | `main.py`（GUI 默认；座位窗 `--seat-window`） |
| **数据** | `assets/`、`configs/` 打入包；运行时日志写到 `%APPDATA%\ChengduMahjongAITrainer\logs\` |
| **工具** | [PyInstaller](https://pyinstaller.org/) · [Nuitka](https://nuitka.net/) |
| **脚本（实现后）** | `tools/packaging/build_pyinstaller_windows.ps1` · `build_nuitka_windows.ps1` |
| **规格** | [`docs/features/F0025_windows_packaging.md`](../features/F0025_windows_packaging.md) |
| **版本** | [`version.py`](../../version.py)（**0.2.1+**）；规则 [`docs/VERSIONING.md`](../VERSIONING.md) |
| **本机副本** | `releases/windows/*`（不进 git） |
| **对照** | macOS：[`MACOS_BUILD.md`](MACOS_BUILD.md) |

> **状态**：F0025 = **`Done`**；一键脚本已合入。优先用 §2.1 / §3.1 脚本；§2.2 / §3.2 手动命令为等价参考。

---

## 0. 架构要点（打包必读）

本应用是 **多进程**：

| 进程 | 职责 |
|------|------|
| 主程序 | Pygame 大厅 / 主桌；`SeatUIHub` 广播 |
| 座位窗 ×4 | Tk `players.seat_window`（play / watch） |

开发态：`python -m players.seat_window ...`  
**打包态**：同一可执行文件再拉起自身并带 **`--seat-window`**（见 `app_paths.seat_window_command`）。

因此必须：

1. 把 `assets/`、`configs/` 作为数据文件打进包  
2. 冻结后能正确解析资源路径（`app_paths.resource_root`）  
3. 可写目录用 `app_paths.logs_dir()` → **`%APPDATA%\ChengduMahjongAITrainer\logs`**（勿写进 Program Files 只读区）  
4. 优先 **onedir / standalone 目录**，避免 onefile 解压竞态（多子进程）  
5. 入口调用 **`multiprocessing.freeze_support()`**（Windows spawn 必要）

运行时兼容（HWND、UTF-8 管道、字体）见 **F0005**，不在本指南重复实现。

---

## 1. 前置条件

### 1.1 系统

- Windows 10 或 11，**64-bit**  
- 建议构建路径尽量 **纯 ASCII**（避免 `C:\用户\中文\…` 类路径踩坑）  
- 已装 **Git**；可选 Windows Terminal

### 1.2 Python 与依赖

在 **PowerShell** 或 **cmd** 中（仓库根目录）：

```powershell
cd C:\path\to\chengdu_majiang_AItrainer

# 若有 setup 脚本用其创建 venv；否则：
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt   # 或按项目 README / tools/setup 安装 pygame numpy pytest 等

# 打包工具
pip install "pyinstaller>=6.0"
# Nuitka 可选：
pip install "nuitka>=2.0" ordered-set zstandard
```

Nuitka 额外需要 **C 编译器**（任选其一，以 [Nuitka 文档](https://nuitka.net/doc/user-manual.html) 为准）：

- Visual Studio Build Tools（MSVC），或  
- MinGW64  

**仅 PyInstaller** 时通常不需要完整 MSVC。

### 1.3 执行策略（PowerShell）

若脚本被策略拦截：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

## 2. PyInstaller（推荐首发）

### 2.1 一键脚本（实现后）

```powershell
.\tools\packaging\build_pyinstaller_windows.ps1
```

预期产出：

```text
dist\pyinstaller\
  ChengduMahjongAITrainer\
    ChengduMahjongAITrainer.exe
    _internal\          # 依赖与数据（PyInstaller 6 常见）
    ...

releases\windows\
  ChengduMahjongAITrainer-PyInstaller\   # 项目内副本（gitignore）
```

### 2.2 手动等价命令（当前即可在 Win 上试）

> **注意**：`--add-data` 在 Windows 上用 **分号 `;`** 分隔 `源;目标`（macOS 用冒号 `:`）。

入口文件：优先使用即将落地的 `packaging\windows\pyinstaller_entry.py`；在其未提交前，可临时使用已有 macOS 入口（逻辑等价）：

```text
packaging\macos\pyinstaller_entry.py
```

```powershell
$ROOT = (Get-Location).Path
$PY = Join-Path $ROOT ".venv\Scripts\python.exe"
$APP_NAME = & $PY -c "from version import APP_NAME; print(APP_NAME)"
$ENTRY = Join-Path $ROOT "packaging\windows\pyinstaller_entry.py"

& $PY -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --onedir `
  --name $APP_NAME `
  --paths $ROOT `
  --distpath (Join-Path $ROOT "dist\pyinstaller") `
  --workpath (Join-Path $ROOT "build\pyinstaller") `
  --add-data "$ROOT\assets;assets" `
  --add-data "$ROOT\configs;configs" `
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
```

| 选项 | 原因 |
|------|------|
| `--windowed` | 无黑色控制台窗口 |
| `--onedir` | 多子进程稳定；便于调试缺文件 |
| `--add-data …;…` | 资源进包（Windows 分隔符） |
| `--collect-submodules …` | 动态 import 不漏模块 |
| entry | 统一主 GUI / `--seat-window` |

### 2.3 运行

```powershell
.\dist\pyinstaller\ChengduMahjongAITrainer\ChengduMahjongAITrainer.exe
# 冒烟
.\dist\pyinstaller\ChengduMahjongAITrainer\ChengduMahjongAITrainer.exe --version
.\dist\pyinstaller\ChengduMahjongAITrainer\ChengduMahjongAITrainer.exe --seat-window --help
```

日志目录：

```text
%APPDATA%\ChengduMahjongAITrainer\logs\
```

在资源管理器地址栏输入：`%APPDATA%\ChengduMahjongAITrainer\logs`

### 2.4 打包为 zip（Release 附件建议）

```powershell
$VER = & .\.venv\Scripts\python.exe -c "from version import APP_VERSION; print(APP_VERSION)"
$SRC = "dist\pyinstaller\ChengduMahjongAITrainer"
$ZIP = "dist\ChengduMahjongAITrainer-$VER-windows-x64-PyInstaller.zip"
Compress-Archive -Path $SRC -DestinationPath $ZIP -Force
```

### 2.5 常见问题

| 现象 | 处理 |
|------|------|
| 座位窗不出现 | 查 `%APPDATA%\…\logs\human_seat*_stderr.log`；确认 exe 支持 `--seat-window` |
| 无牌面 / 缺资源 | 确认 onedir 内有 `assets`（可能在 `_internal\assets`）；可设 `CHENGDU_MAHJONG_ROOT` |
| 闪退无窗 | 临时去掉 `--windowed` 重打一次看控制台；或查 `logs\main_crash.log` |
| SmartScreen「未知发布者」 | 本机构建：更多信息 → 仍要运行；对外需 Authenticode（OOS） |
| 杀软误报 | 加白名单；优先 onedir 完整目录分发 |
| 子进程起不来 | 确认未使用 onefile；检查 `CREATE_NEW_PROCESS_GROUP` 仅 win32（F0005） |
| 中文乱码（日志） | 管道已 UTF-8；若第三方工具打开日志选 UTF-8 |

---

## 3. Nuitka

### 3.1 一键脚本（实现后）

```powershell
.\tools\packaging\build_nuitka_windows.ps1
```

### 3.2 手动等价（standalone）

```powershell
$ROOT = (Get-Location).Path
$PY = Join-Path $ROOT ".venv\Scripts\python.exe"
$ENTRY = Join-Path $ROOT "packaging\windows\pyinstaller_entry.py"

& $PY -m nuitka `
  --standalone `
  --windows-console-mode=disable `
  --enable-plugin=tk-inter `
  --include-package=engine `
  --include-package=players `
  --include-package=display `
  --include-package=protocols `
  --include-package=training `
  --include-package-data=pygame `
  --include-data-dir=assets=assets `
  --include-data-dir=configs=configs `
  --output-dir=dist\nuitka `
  --output-filename=ChengduMahjongAITrainer.exe `
  $ENTRY
```

| 选项 | 原因 |
|------|------|
| `--standalone` | 自带依赖，可拷到无 Python 的 PC |
| `--windows-console-mode=disable` | 无控制台（flag 名随 Nuitka 版本可能微调，以官方文档为准） |
| `--enable-plugin=tk-inter` | 座位窗 Tk |
| `--include-data-dir` | assets / configs |

首次编译较慢。若启动失败，用终端运行生成的 `.exe` 看 stderr。

### 3.3 注意

- 与 PyInstaller 相同：子进程靠 `--seat-window` 再入。  
- 路径尽量 ASCII。  
- 若 pygame 缺动态库，按 Nuitka 报错补 `--include-module` / 数据。  
- **MSVC 未装**时优先只用 PyInstaller。

---

## 4. 验收清单

| ID | 项 | 期望 |
|----|----|------|
| W1 | 双击 / 命令行启动 | 大厅出现；标题/CLI 为当前 `APP_VERSION` |
| W2 | 开始 1H+3AI | 主窗 + 4 座位窗 |
| W3 | 确认后掷骰 | 主窗中心动画 → 庄家（F0023） |
| W4 | 人类可出牌 | 座位窗操作正常 |
| W5 | 出牌日志 | 右侧有摸/打/碰等中文明细（F0024） |
| W6 | 弃牌 | 多行排列，无右侧滚动条 |
| W7 | 牌面 / 主题 | green/blue 资源正常 |
| W8 | 日志目录 | `%APPDATA%\ChengduMahjongAITrainer\logs` 有文件 |
| W9 | 再来一局 | Hub 复用 / 就绪确认仍可用 |
| W10 | 2H / 3H | 布局 B/D 可开（F0020） |
| W11 | 冒烟 CLI | `--version`、`--seat-window --help` |

---

## 5. 未签名分发

本仓库默认 **不** 配置 Authenticode。内部分发：

- zip 整个 onedir 目录  
- 告知用户：SmartScreen 可能提示；从可信渠道获取  

对外商店级发布需签名与安装器（不在本指南 / F0025 范围）。

---

## 6. 环境变量

| 变量 | 含义 |
|------|------|
| `CHENGDU_MAHJONG_ROOT` | 覆盖资源根（含 assets/configs） |
| `CHENGDU_MAHJONG_DATA` | 覆盖可写数据根（logs/saves） |
| `APPDATA` | 系统默认 Roaming 根；冻结态 `runtime_base` 依赖它 |

---

## 7. 与 macOS 的差异摘要

| 项 | Windows | macOS |
|----|---------|-------|
| 构建机 | 必须 Windows | 必须 macOS |
| 产物 | `.exe` + onedir | `.app` bundle |
| `--add-data` | `src;dest` | `src:dest` |
| 可写数据 | `%APPDATA%\ChengduMahjongAITrainer` | `~/Library/Application Support/…` |
| 隔离/门禁 | SmartScreen / 杀软 | Gatekeeper / quarantine |
| 入口 freeze_support | **关键** | 建议保留 |

---

## 8. MSI 安装程序（F0027 · WiX 3.14）

从 **PyInstaller onedir** 生成 per-machine **x64 MSI**（安装到 Program Files、开始菜单、可卸载）。

### 8.1 一键构建

```powershell
# 若尚无 onedir，会先调用 build_pyinstaller_windows.ps1
.\tools\packaging\build_msi_windows.ps1

# 已有 onedir 时：
.\tools\packaging\build_msi_windows.ps1 -SkipPyInstaller
```

产出：

```text
dist\msi\ChengduMahjongAITrainer-{APP_VERSION}-windows-x64.msi
releases\windows\…（本地副本，gitignore）
```

脚本会在首次运行时下载 **WiX 3.14 binaries** 到 `%LOCALAPPDATA%\wix314\`（不进 git）。

### 8.2 安装 / 卸载

**需要管理员权限**（安装到 Program Files + 公共开始菜单）。双击 MSI 时应弹出 UAC。

```powershell
# 安装（管理员 / UAC）
msiexec /i dist\msi\ChengduMahjongAITrainer-0.2.1-windows-x64.msi

# 静默（必须在已提升的终端）
msiexec /i dist\msi\ChengduMahjongAITrainer-0.2.1-windows-x64.msi /qn

# 卸载
msiexec /x dist\msi\ChengduMahjongAITrainer-0.2.1-windows-x64.msi
```

| 项 | 说明 |
|----|------|
| 默认目录 | `%ProgramFiles%\ChengduMahjongAITrainer\` |
| 开始菜单 | `成都麻将AI训练器`（公共菜单） |
| 向导 UI | **WixUI 中文**（许可协议 → 安装目录 → 安装） |
| 产品名编码 | GBK 代码页 936（见 §8.3） |
| 日志 | `%APPDATA%\ChengduMahjongAITrainer\logs\` |

常见错误：

| 代码 | 含义 | 处理 |
|------|------|------|
| **1925** | 无足够权限为「所有用户」安装 | 右键 MSI → **以管理员身份运行**，或同意 UAC |
| **1603** | 致命错误（多为权限或文件占用） | 关已运行的游戏进程后管理员重装 |
| **1639** | 命令行参数无效 | 路径含空格时对 MSI 路径加引号 |

规格：[`docs/features/F0027_windows_msi.md`](../features/F0027_windows_msi.md)

### 8.3 中文显示（代码页）

Windows Installer 字符串表按 **ANSI 代码页** 存储，**不是 UTF-8**。简体中文 MSI 必须：

| 项 | 值 |
|----|-----|
| `Product/@Language` | **2052**（zh-CN） |
| `Product/@Codepage` | **936**（GBK） |
| 源 `Product.wxs` | 构建时由 `gen_msi_product_wxs.py` 写成 **GBK** |

若使用 `Codepage=65001`（UTF-8）或 UTF-8 源文件直接 candle，控制面板/开始菜单中文常显示为**乱码**。  
修复后请重新执行 `build_msi_windows.ps1` 再安装验证。

### 8.4 注意

- 仅包装 **PyInstaller** 树（Nuitka 另打 MSI 不在 F0027 范围）。  
- 未签名 → SmartScreen 可能提示。  
- 升级：同一 `UpgradeCode`，更高 `ProductVersion` 可 MajorUpgrade。

---

## 9. 实现进度（文档同步）

| 项 | 状态 |
|----|------|
| F0025 规格 | **Done** |
| F0027 MSI | **Done**（WiX 3.14 + heat/candle/light） |
| 本手册 | 已写 |
| `packaging/windows/*` | **已合入** |
| `build_*_windows.ps1` / `.bat` | **已合入**（含 `build_msi_windows.ps1`） |
| 本机 Win 验收 | 脚本含 `--version` / `--seat-window --help` 冒烟；完整 W1–W11 人工开局 |
| GitHub Release Win zip | **已上传** v0.2.1（PyInstaller + Nuitka） |
| GitHub Release MSI | 可选（构建后 `gh release upload`） |

构建触发：

```powershell
.\tools\packaging\build_pyinstaller_windows.ps1
.\tools\packaging\build_nuitka_windows.ps1   # 需 MSVC/MinGW
.\tools\packaging\build_msi_windows.ps1      # MSI（F0027）
```
