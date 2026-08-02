# macOS 打包指南（PyInstaller · Nuitka）

| 字段 | 值 |
|------|-----|
| **平台** | macOS 12+（arm64 / x86_64；本文在 **Apple Silicon arm64** 上验证流程） |
| **入口** | `main.py`（GUI 默认 `gui`；座位窗 `--seat-window`） |
| **数据** | `assets/`、`configs/`、`players/humanlike/parameter_registry_v2.json` 打入包；运行时日志写到 `~/Library/Application Support/ChengduMahjongAITrainer/` |
| **工具** | [PyInstaller](https://pyinstaller.org/) · [Nuitka](https://nuitka.net/) |
| **脚本** | `tools/packaging/build_pyinstaller_macos.sh` · `tools/packaging/build_nuitka_macos.sh` |
| **规格** | [`docs/features/F0021_macos_packaging.md`](../features/F0021_macos_packaging.md) |
| **版本** | 应用版本见 [`version.py`](../../version.py)（当前发布线 **0.3.1**）；规则 [`docs/VERSIONING.md`](../VERSIONING.md) |
| **本机副本** | `releases/macos/*-PyInstaller.app` · `*-Nuitka.app`（不进 git） |

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

1. 把 `assets/`、`configs/` 和 Humanlike 参数注册表作为数据文件打进包
2. 冻结后能正确解析资源路径（`app_paths.resource_root`）  
3. 可写目录用 `app_paths.logs_dir()`（勿写进 `.app` 只读区）  
4. 优先 **onedir / 应用包目录结构**，避免 onefile 解压竞态（多子进程）

---

## 1. 前置条件

```bash
cd /path/to/chengdu_majiang_AItrainer
bash tools/setup_venv.sh          # Python ≥3.11 + pygame + pytest
source .venv/bin/activate         # 或始终用 .venv/bin/python

# 打包工具（按需）
.venv/bin/pip install "pyinstaller>=6.0"
.venv/bin/pip install "nuitka>=2.0" ordered-set zstandard
# Nuitka 可选：加速 / 更完整的 C 编译（Homebrew）
# brew install ccache
```

建议在 **干净的 venv** 中打包（与开发同一 `.venv` 亦可）。

---

## 2. PyInstaller（推荐首发）

### 2.1 一键脚本

```bash
bash tools/packaging/build_pyinstaller_macos.sh
```

产出（默认）：

```text
dist/pyinstaller/
  ChengduMahjongAITrainer.app     # 可双击（windowed）
  ChengduMahjongAITrainer/        # onedir 目录（与 .app 内容对应）
```

实测（arm64，本机）：约 **200MB** 级；构建约 20–40s（已装依赖时）。
### 2.2 手动等价命令

```bash
.venv/bin/pyinstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name ChengduMahjongAITrainer \
  --osx-bundle-identifier com.moff.chengdu-majiang-aitrainer \
  --paths . \
  --add-data "assets:assets" \
  --add-data "configs:configs" \
  --add-data "players/humanlike/parameter_registry_v2.json:players/humanlike" \
  --hidden-import players.seat_window \
  --hidden-import players.human_proxy \
  --hidden-import players.registry \
  --hidden-import display.app \
  --hidden-import tkinter \
  --collect-all pygame \
  --collect-submodules engine \
  --collect-submodules players \
  --collect-submodules display \
  --collect-submodules protocols \
  --collect-submodules training \
  packaging/macos/pyinstaller_entry.py
```

说明：

| 选项 | 原因 |
|------|------|
| `--windowed` | 生成 `.app`，无终端黑框 |
| `--add-data assets/configs/parameter_registry_v2.json` | 运行资源进包 |
| `--collect-all pygame` | SDL 动态库与数据 |
| `--collect-submodules …` | 避免动态 import 漏模块 |
| `pyinstaller_entry.py` | 统一入口：主 GUI / `--seat-window` |

Spec 文件：`packaging/macos/ChengduMahjongAITrainer.spec`（脚本优先用 entry + 参数；spec 便于自定义图标）。

### 2.3 运行

```bash
open dist/pyinstaller/ChengduMahjongAITrainer.app
# 或
./dist/pyinstaller/ChengduMahjongAITrainer.app/Contents/MacOS/ChengduMahjongAITrainer
```

日志：

```text
~/Library/Application Support/ChengduMahjongAITrainer/logs/
```

### 2.4 常见问题

| 现象 | 处理 |
|------|------|
| 座位窗不出现 | 查 `logs/human_seat*_stderr.log`；确认二进制支持 `--seat-window` |
| 无牌面 / 缺资源 | 检查包内是否有 `assets/`；环境变量 `CHENGDU_MAHJONG_ROOT` 可强制根目录 |
| 被 Gatekeeper 拦截 | 本机构建：系统设置 → 隐私与安全性 → 仍要打开；或 `xattr -cr dist/...app` |
| 体积大 | pygame 资源 + SDL；正常数百 MB 级 |

---

## 3. Nuitka

### 3.1 一键脚本

```bash
bash tools/packaging/build_nuitka_macos.sh
```

产出：

```text
dist/nuitka/
  ChengduMahjongAITrainer.app   # 构建输出（脚本会把 pyinstaller_entry.app 重命名）
  pyinstaller_entry.build/      # 中间产物（可删）

releases/macos/
  ChengduMahjongAITrainer-Nuitka.app   # 同步到项目内便于查找（.gitignore，不进 git）
  README.md
```

实测（arm64）：首次约 1–3 分钟（视机器与 ccache）。

### 3.2 手动等价（standalone + app bundle）

```bash
.venv/bin/python -m nuitka \
  --standalone \
  --macos-create-app-bundle \
  --macos-app-name="成都麻将AI训练器" \
  --enable-plugin=tk-inter \
  --include-package=engine \
  --include-package=players \
  --include-package=display \
  --include-package=protocols \
  --include-package=training \
  --include-package-data=pygame \
  --include-data-dir=assets=assets \
  --include-data-dir=configs=configs \
  --include-data-file=players/humanlike/parameter_registry_v2.json=players/humanlike/parameter_registry_v2.json \
  --output-dir=dist/nuitka \
  --output-filename=ChengduMahjongAITrainer \
  packaging/macos/pyinstaller_entry.py
```

| 选项 | 原因 |
|------|------|
| `--standalone` | 自带依赖，可拷到无 Python 的 Mac |
| `--macos-create-app-bundle` | 生成 `.app` |
| `--enable-plugin=tk-inter` | 座位窗 Tk |
| `--include-data-dir` / `--include-data-file` | assets、configs 和 Humanlike 参数注册表 |

首次编译较慢（C 编译）；后续增量会快一些。

### 3.3 注意

- Nuitka 对 pygame 偶发需额外 `--include-module`；脚本里已加常见项。  
- 若 app 启动失败，先用 **standalone 目录** 在终端运行看 stderr。  
- 与 PyInstaller 相同：子进程靠 `--seat-window` 再入。  
- **路径必须是 ASCII（重要）**：Nuitka 运行时解析二进制目录时，若 `.app` 位于含**中文/空格特殊字符**的路径（例如 OneDrive「共享的库」）下，会直接 `abort`（SIGABRT）。  
  - 构建可在原仓库进行；**运行前请复制到纯英文路径**，例如：  
    ```bash
    cp -R dist/nuitka/ChengduMahjongAITrainer.app /Applications/
    open /Applications/ChengduMahjongAITrainer.app
    # 或
    cp -R dist/nuitka/ChengduMahjongAITrainer.app /tmp/
    /tmp/ChengduMahjongAITrainer.app/Contents/MacOS/ChengduMahjongAITrainer --seat-window --help
    ```  
  - PyInstaller 产物在中文路径下一般仍可运行；Nuitka 更敏感。
---

## 4. 验收清单

| ID | 项 | 期望 |
|----|----|------|
| P1 | 双击 / 命令行启动 | 大厅出现；标题/CLI 为当前 `APP_VERSION` |
| P2 | 开始 1H+3AI | 主窗 + 4 座位窗 |
| P3 | 确认后掷骰 | 主窗中心动画 → 庄家（F0023） |
| P4 | 人类可出牌 | 座位窗操作正常 |
| P5 | 出牌日志 | 右侧有摸/打/碰等中文明细（F0024） |
| P6 | 弃牌 | 多行排列，无右侧滚动条 |
| P7 | 牌面 / 主题 | green/blue 资源正常 |
| P8 | 日志目录 | Application Support 下有 logs |
| P9 | 再来一局 | Hub 复用 / 就绪确认仍可用 |
| P10 | 运行资源门禁 | assets、configs、Humanlike 参数注册表均存在；缺失时脚本失败 |

---

## 5. 未签名分发（可选）

本仓库默认 **不** 配置 Apple Developer 签名与公证。内部分发：

```bash
# 去掉隔离属性（仅受信来源）
xattr -cr dist/pyinstaller/ChengduMahjongAITrainer.app
```

对外发布需：`codesign` + `notarytool`（不在本指南范围）。

---

## 6. 环境变量

| 变量 | 含义 |
|------|------|
| `CHENGDU_MAHJONG_ROOT` | 覆盖资源根（含 assets/configs） |
| `CHENGDU_MAHJONG_DATA` | 覆盖可写数据根（logs/saves） |

---

## 7. 与 Windows 的关系

F0005 兼容逻辑仍在代码中；**本文件仅覆盖 macOS 打包命令与产物**。  
Windows 打包规格与手册：

- 规格：[`docs/features/F0025_windows_packaging.md`](../features/F0025_windows_packaging.md)  
- 手册：[`docs/packaging/WINDOWS_BUILD.md`](WINDOWS_BUILD.md)  

须在 **Windows 主机** 构建；模式同为 onedir + `--seat-window` 再入。
