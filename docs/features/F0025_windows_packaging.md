# F0025 — Windows 打包（PyInstaller + Nuitka）

| 字段 | 值 |
|------|-----|
| **编号** | F0025 |
| **标题** | Windows packaging with PyInstaller and Nuitka |
| **状态** | **`Done`**（2026-07-26 实现脚本合入；本机构建验收见 WINDOWS_BUILD §4） |
| **关联代码** | `packaging/windows/*`、`tools/packaging/build_*_windows.*`、`app_paths.py`、`tests/test_app_paths.py` |
| **类型** | 工程交付：分发产物 + 构建脚本 + 路径/子进程冻结支持核对 |
| **文档** | [`docs/packaging/WINDOWS_BUILD.md`](../packaging/WINDOWS_BUILD.md) |
| **依赖** | F0005（Win/Mac 兼容已 Done）、F0021（macOS 打包：冻结入口 / `app_paths` / `--seat-window` 模式） |
| **版本线** | 应用版本以 `version.py` 为准（当前发布线 **0.2.1+**）；规则见 [`docs/VERSIONING.md`](../VERSIONING.md) |

---

## 1. 背景与动机

- macOS 已有 **F0021** + [`MACOS_BUILD.md`](../packaging/MACOS_BUILD.md) 与 Release 双包（PyInstaller / Nuitka）。
- 运行时兼容（屏幕、子进程 UTF-8、HWND、字体）已由 **F0005** 覆盖；**尚缺 Windows 冻结分发** 的构建脚本与操作手册。
- 本应用为 **多进程**（主程序 + 最多 4 个座位窗）；打包必须与 macOS 相同采用 **同一二进制 + `--seat-window` 再入**，且优先 **onedir**（避免 onefile 解压竞态）。

---

## 2. 目标

| ID | 目标 |
|----|------|
| G1 | 提供 **PyInstaller** Windows 构建脚本与说明，产出可运行的 **onedir**（`ChengduMahjongAITrainer.exe` + 依赖目录） |
| G2 | 提供 **Nuitka** Windows 构建脚本与说明，产出 **standalone** 目录（或等价可拷贝树） |
| G3 | 冻结后多座位子进程可用（`seat_window_command` → `[exe, --seat-window, …]`） |
| G4 | `assets/` + `configs/` 正确加载；日志/存档写入 **`%APPDATA%\ChengduMahjongAITrainer\`**（与现有 `app_paths.runtime_base` 一致） |
| G5 | 版本号从 `version.py` 读取（禁止脚本内硬编码第二套版本） |
| G6 | 操作手册可在 **纯 Windows 开发机** 按步骤复现；产物可 zip 上传 GitHub Release（可选，与 macOS 并列） |

### Out of Scope

| # | 项 |
|---|-----|
| O1 | Apple / macOS 打包（已有 F0021） |
| O2 | Linux 打包 |
| O3 | MSI / MSIX / Inno Setup / NSIS 安装器美化（**MSI 见 F0027**） |
| O4 | Authenticode 代码签名、Windows Store、SmartScreen 企业白名单 |
| O5 | 在 macOS 上 **交叉编译** 出 Windows 二进制（**不支持**；必须在 Windows 上构建） |
| O6 | 改变引擎规则、座位协议或 UI 布局 |

---

## 3. 设计

### 3.1 进程与入口（与 F0021 对齐）

```text
用户启动 ChengduMahjongAITrainer.exe
        │
        ▼
  packaging entry → main.main / gui
        │
        ├─ app_paths.resource_root() → assets, configs（onedir 旁 _internal 或 exe 旁）
        ├─ app_paths.logs_dir() → %APPDATA%\ChengduMahjongAITrainer\logs
        │
        ▼
  SeatUIHub / SubprocessTransport
        │
        └─ seat_window_command() → [exe, --seat-window, --seat N, ...]
                    │
                    ▼
              同一 exe 座位窗 (Tk)
```

| 点 | 约定 |
|----|------|
| 入口文件 | `packaging/windows/pyinstaller_entry.py`（内容可与 macOS entry 等价；含 `multiprocessing.freeze_support()`） |
| 再入 | `main.py` 已支持 argv 首参 `--seat-window` → `players.seat_window` |
| 禁止 | 冻结态再用 `python -m players.seat_window`（目标机无解释器） |
| 形态 | **onedir / standalone 目录**；默认不做 onefile |

### 3.2 资源与可写路径（代码现状）

| API | Windows 冻结行为（已实现） |
|-----|---------------------------|
| `resource_root()` | `_MEIPASS` 或 `exe` 旁 / `_internal` 含 `assets` |
| `runtime_base()` | `%APPDATA%\ChengduMahjongAITrainer`（或 `CHENGDU_MAHJONG_DATA`） |
| `seat_window_command()` | `[sys.executable, "--seat-window", …]` |

实现本 F 时：**以核对 + 单测补强为主**；仅当路径探测在 PyInstaller 6 / Nuitka Windows 布局下失败才改 `app_paths.py`。

### 3.3 PyInstaller（推荐首发）

| 项 | 约定 |
|----|------|
| 命令载体 | `tools/packaging/build_pyinstaller_windows.ps1`（首选）+ 可选 `.bat` 包装 |
| 关键开关 | `--windowed` / `--noconsole`、`--onedir`（默认）、`--name` = `APP_NAME` |
| 数据 | `--add-data "assets;assets"`、`configs;configs`（**分号**，非 macOS 冒号） |
| 收集 | `--collect-submodules` engine/players/display/protocols；hidden-import 座位/主循环相关；`tkinter`、`pygame` |
| 排除 | `pygame.tests` / `examples` / 无关重依赖（与 mac 脚本对齐） |
| 产出 | `dist/pyinstaller/ChengduMahjongAITrainer/`（含 `.exe`） |
| 本机副本 | `releases/windows/ChengduMahjongAITrainer-PyInstaller/`（gitignore，不进 git） |

### 3.4 Nuitka

| 项 | 约定 |
|----|------|
| 命令载体 | `tools/packaging/build_nuitka_windows.ps1` |
| 形态 | `--standalone`；插件 `--enable-plugin=tk-inter` |
| 数据 | `--include-data-dir=assets=assets` 等 |
| 控制台 | 关闭控制台窗口（等价 windowed；具体 flag 以 Nuitka 当前文档为准，写入 WINDOWS_BUILD） |
| 产出 | `dist/nuitka/...` → 同步 `releases/windows/*-Nuitka/` |
| 依赖 | Windows 上需可用的 C 编译器（MSVC Build Tools 或 MinGW，以 Nuitka 要求为准） |

### 3.5 分发与安全说明（文档义务）

- 默认 **不签名** → SmartScreen / 杀软可能告警；手册写明「本机构建 / 受信来源」处理方式。  
- 分发建议：zip 整个 onedir，Release 附件命名：  
  `ChengduMahjongAITrainer-{APP_VERSION}-windows-x64-PyInstaller.zip`  
  （架构以构建机为准：优先 **x64**；ARM64 Windows 若支持则单独命名。）

### 3.6 与 F0005 / F0021 关系

| 文档 | 关系 |
|------|------|
| F0005 | 运行时兼容；O4「installer/codesign」仍不在本 F |
| F0021 | 模式复用；入口/隐藏导入列表应对齐维护 |
| MACOS_BUILD §7 | 实现后改为指向本 F + WINDOWS_BUILD |

---

## 4. 交付清单（实现阶段）

| 路径 | 说明 |
|------|------|
| `docs/features/F0025_windows_packaging.md` | 本规格 |
| `docs/packaging/WINDOWS_BUILD.md` | 用户向操作手册 |
| `packaging/windows/pyinstaller_entry.py` | 统一入口 |
| `packaging/windows/ChengduMahjongAITrainer.spec` | 可选 spec |
| `tools/packaging/build_pyinstaller_windows.ps1` | PyInstaller 构建 |
| `tools/packaging/build_nuitka_windows.ps1` | Nuitka 构建 |
| `tools/packaging/build_pyinstaller_windows.bat` | 可选双击入口 |
| `.gitignore` | `releases/windows` 大产物（`*.exe` 树 / zip） |
| `tests/test_app_paths.py` | 必要时补 Windows 路径分支（可 mock platform） |
| `docs/features/README.md` / `changelog` / `LATEST` / `DOC_CODE_BASELINE` | 索引与基线 |
| `docs/packaging/MACOS_BUILD.md` §7 | 交叉链接 |

**不**强制本仓库在 CI 上跑 Windows 打包（无 runner 则本地手工）。

---

## 5. 验收标准

### 5.1 文档

- [x] F0025 + WINDOWS_BUILD 落盘  
- [x] 索引与 LATEST/changelog 更新  
- [x] 用户确认规格 → **`Approved`**（2026-07-26）

### 5.2 实现后（Windows 主机）

见 [`WINDOWS_BUILD.md`](../packaging/WINDOWS_BUILD.md) §验收。摘要：

| ID | 项 |
|----|-----|
| W1 | 双击 / 命令行启动大厅；版本为当前 `APP_VERSION` |
| W2 | 1H+3AI：主窗 + 4 座位窗 |
| W3 | 人类可出牌；ready / 再来一局 |
| W4 | 掷骰、出牌日志、弃牌多行（与 0.2.1 功能一致） |
| W5 | 牌面资源正常 |
| W6 | `%APPDATA%\ChengduMahjongAITrainer\logs\` 有日志 |
| W7 | 2H / 3H 模式可开（布局 B/D） |
| W8 | `exe --version` 与 `exe --seat-window --help` 冒烟通过 |

---

## 6. 测试计划

| ID | 用例 | 环境 |
|----|------|------|
| T1 | 既有 `pytest tests/test_app_paths.py` 等在 Win/Mac 开发态通过 | 双端 |
| T2 | 冻结路径：mock `sys.frozen` / `_MEIPASS` 时 `resource_root` / `seat_window_command` 形状正确 | 单测 |
| T3 | 人工：PyInstaller onedir 完整一局 | Windows |
| T4 | 人工：Nuitka standalone 完整一局（若编译环境可用） | Windows |

---

## 7. 风险与开放问题

| 风险 | 缓解 |
|------|------|
| 无 Windows 机无法验证 | 文档标明「构建与验收在 Windows」；Mac 仅可写脚本与文档 |
| SmartScreen / 杀软误报 | 文档说明；可选后续签名 |
| Nuitka 需 MSVC | 手册前置条件；PyInstaller 作默认首发 |
| `--add-data` 分隔符 | 脚本用 `;`；禁止从 mac 脚本原样复制 `:` |
| 中文路径 | 建议构建/运行路径尽量 ASCII；文档注明 OneDrive 中文路径风险 |
| 多显示器 / DPI | 仍遵循 F0001 逻辑像素；打包不引入 DPI 重写 |

**已锁定（Approved）**：

| # | 决议 |
|---|------|
| Q1 | **两套脚本都交付**（PyInstaller + Nuitka）；**Release 默认只挂 PyInstaller** zip；Nuitka 为可选/本机构建 |
| Q2 | 首发形态 **onedir x64**；不做 onefile、不做安装器（O3） |
| Q3 | 构建与验收 **仅 Windows 主机**（本仓库当前会话在 Win 上可实现） |

---

## 8. 回滚

删除 `packaging/windows/*` 与 `tools/packaging/build_*_windows.*`；文档状态回退；不影响 F0021 macOS 与运行时逻辑。

---

## 9. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-26 | Draft | 用户触发「Windows 打包」：先写规格与操作手册，**不**在本轮写脚本/构建 |
| 2026-07-26 | **Approved** | 用户「确认 F0025」：锁定 Q1–Q3；**仍不写代码**直至「实现 Windows 打包」 |
| 2026-07-26 | **Done** | 用户「实现 F0025」：`packaging/windows/*` + `build_*_windows.ps1` + bat + 单测；手册/索引同步 |
