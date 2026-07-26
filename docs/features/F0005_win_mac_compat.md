# F0005 — Windows / macOS 代码兼容

| 字段 | 值 |
|------|-----|
| **编号** | F0005 |
| **标题** | Win32 / macOS cross-platform compatibility |
| **状态** | `Done` |
| **类型** | 兼容性 / 缺陷修复 + 小增强 |
| **依赖** | F0001 窗口几何、F0002 座位窗、CJK 字体回退（changelog 2026-07-10） |
| **关联** | `display/window_geometry.py`、`display/hud_common.py`、`protocols/subprocess_transport.py`、`players/seat_window.py`、`players/seat_ui_hub.py` |
| **授权** | 用户指令「兼容检查并修复 + 文档优先」：本规格落盘后同轮实现 |

---

## 1. 背景与动机

产品需在 **Windows** 与 **macOS**（含 Mac Studio）双端可运行：

- 主程序 Pygame 观战窗
- 座位窗（tkinter 子进程）
- 子进程 NDJSON 协议
- 中文 UI 文案

历史实现以 **Windows 为主力**（`ctypes.windll`、微软雅黑、Win32 `SetWindowPos`）。在 macOS 上出现：

1. 屏幕检测误走 Win32 路径（异常吞掉后回退 `pygame` / 默认 1920×1080，**多显示器 origin 失真**）
2. 父进程 `force_placement_by_*` 全为 HWND，**Mac 上恒 False**（座位窗依赖 Tk 初始 geometry，主窗依赖 `SDL_VIDEO_WINDOW_POS`）
3. CJK 字体只列 Windows 族名 → 假匹配（已部分修复，本规格固化）
4. 子进程 `Popen`：Windows 缺省编码可能非 UTF-8；`creationflags` 应仅在 win32 传入

---

## 2. 范围

### In Scope

| # | 项 |
|---|-----|
| S1 | `detect_screen()` **按平台分发**：win32 / darwin / 其他 |
| S2 | macOS：用 CoreGraphics（ctypes，**不**强制 PyObjC）检测**光标所在显示器** bounds 作为工作区近似 |
| S3 | 窗口强制布局：win32 保持 HWND；非 win32 用 **pygame Window API**（主窗）或 **跳过并依赖初始 geometry**（座位 Tk） |
| S4 | 子进程：`encoding=utf-8`、`errors=replace`；`creationflags` 仅 win32 |
| S5 | CJK：pygame + tk 字体回退表覆盖 Win/Mac（巩固既有修复） |
| S6 | 单测：平台分发不崩溃、Mac 探测有合理尺寸、字体探针、subprocess kwargs 构造 |

### Out of Scope

| # | 项 |
|---|-----|
| O1 | Linux 多显示器精细工作区（保留 pygame / default 回退即可） |
| O2 | 重写座位窗为统一 GUI 框架 |
| O3 | DPI 感知切换（继续 **逻辑像素** 约定，见 F0001） |
| O4 | 打包 installer / codesign |

---

## 3. 设计

### 3.1 屏幕检测

```
detect_screen()
  ├─ win32  → _detect_screen_win32() → SPI / GetSystemMetrics 回退
  ├─ darwin → _detect_screen_macos()  # CoreGraphics + 光标点
  └─ else   → pygame.display.Info / default 1920×1080
```

**macOS 算法（S2）**：

1. `CGEventCreate` + `CGEventGetLocation` 得光标点  
2. `CGGetActiveDisplayList` 枚举显示器  
3. `CGDisplayBounds(displayID)` 找包含光标的显示器  
4. 工作区：`origin=(bounds.x, bounds.y)`，`width/height=bounds`；顶部减去 **menu bar 启发式 28px**（可见区近似，不要求像素级 dock 避让）  
5. `source`：`macos_cursor` | `macos_main`  
6. 失败则回退 pygame / default（**禁止**再调 `windll`）

**Windows**：保持现有 console → foreground → cursor → primary 优先级。

### 3.2 窗口强制布局

| API | Windows | macOS |
|-----|---------|-------|
| `force_hwnd_placement` / `find_hwnds_for_pid` / `force_placement_by_title` / `force_placement_by_pid` | 保持 | **立即返回 False**（不调 windll） |
| `force_window_placement`（当前 pygame 主窗） | HWND | **仅** `SDL_VIDEO_WINDOW_POS` + `set_mode`；**禁止** `pygame._sdl2.Window` 读写 |
| `reassert_plan_windows` | 可选 HWND 座位 | 默认 **`include_main=False`**；座位靠 Tk/`set_geometry`；**禁止**后台线程 pin 主窗 |
| 座位窗初始位置 | CLI `--x/y/width/height` | **同左**（权威）；负 Y 用 `format_tk_geometry` / `--y=-N` |

`open_resizable_window`：设置 `SDL_VIDEO_WINDOW_POS` 后 `set_mode`（**不要**在 macOS 上依赖 `_sdl2` 或 `display.quit` 重开）。

### 3.3 子进程 I/O

`SubprocessTransport.start`：

```python
kwargs = dict(
    ...,
    text=True,
    encoding="utf-8",
    errors="replace",
    bufsize=1,
)
if sys.platform == "win32":
    kwargs["creationflags"] = CREATE_NEW_PROCESS_GROUP
    env["SDL_VIDEODRIVER"] = "windows"
    env["SDL_RENDER_DRIVER"] = "software"
# macOS: 不强制 SDL_VIDEODRIVER（避免覆盖可用驱动）
```

环境变量：`PYTHONIOENCODING=utf-8`、`PYGAME_HIDE_SUPPORT_PROMPT=1` 双端保留。

### 3.4 CJK 字体（固化）

| 层 | 策略 |
|----|------|
| pygame `resolve_ui_font` | 优先 SysFont 真 CJK 名 + 字体文件路径（Mac STHeiti/Arial Unicode；Win msyh/simhei）；探针「麻将胡」；**不缓存 Font 对象** |
| tk `seat_window` | `_pick_tk_cjk_family`：PingFang SC / 雅黑 / … |

---

## 4. 文件清单

| 路径 | 变更 |
|------|------|
| `docs/features/F0005_win_mac_compat.md` | 本规格 |
| `docs/features/README.md` | 索引 |
| `display/window_geometry.py` | 平台分发 + macOS 检测 + 非 Win 强制布局 |
| `protocols/subprocess_transport.py` | encoding / creationflags |
| `display/hud_common.py` | 已实现则仅核对文档对齐；缺则补 |
| `players/seat_window.py` | 已实现 Tk 字体回退则核对 |
| `tests/test_window_geometry.py` | 平台 no-crash、detect 合理 |
| `tests/test_cjk_font.py` | 已有则保留 |
| `tests/test_subprocess_compat.py` | 可选：编码参数 / platform kwargs |
| `docs/changelog.md` | 实现后追加 |
| `docs/status/LATEST.md` | 实现后快照 |

---

## 5. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| T1 | `detect_screen()` 在当前 OS 返回 `width>=640, height>=480` | 通过 |
| T2 | win32 专有函数在非 win32 上调用不抛、返回 False/None | 通过 |
| T3 | `compute_window_plan` 仍网格不重叠（回归） | 通过 |
| T4 | CJK `resolve_ui_font` 探针通过（有系统 CJK 时） | 通过；无 CJK 环境 skip 或 xfail 文档化 |
| T5 | 构造 `SubprocessTransport` 启动参数逻辑：非 win32 不带 creationflags（单元测内部 helper 或 mock） | 通过 |
| T6 | 人工：`python main.py human` 在 Mac / Windows 四窗位置合理、中文可读 | 验收 |

---

## 6. 验收标准

- [x] 规格 `Approved` 后实现与文档一致  
- [x] `pytest tests/test_window_geometry.py tests/test_cjk_font.py tests/test_subprocess_compat.py` 及相关兼容测通过  
- [x] macOS：`detect_screen().source` 为 `macos_*` 或合理回退，且 **不再尝试 windll**（本机验证 `macos_cursor`）  
- [x] Windows：HWND 路径保留；非 win32 早退  
- [x] 子进程 `encoding=utf-8` + win32-only `creationflags`  
- [x] 座位窗几何由 CLI/Tk 决定；Mac 不依赖 HWND reassert  

---

## 7. 风险与开放问题

| 风险 | 缓解 |
|------|------|
| CoreGraphics ctypes 签名随系统变化 | 宽 except + pygame 回退 |
| menu bar / Dock 启发式不准 | 文档声明近似；**勿**在座位 Tk 进程里调 `NSApplication.sharedApplication`（与 Tk 冲突） |
| SDL 多显示器 `WINDOW_POS` 不可靠 | 接受 best-effort；座位以 Tk 为准；主窗仅主线程 pin |
| `_sdl2` / 后台 `set_mode` | **硬禁止**（见 §10）；实测 SEGV |
| 无显示器 CI | dummy 驱动 + default 尺寸 |

**开放问题**：macOS 主窗与座位在复杂排列下仍可能不完全同屏（见 F0001 §13.4）。

---

## 8. 回滚

还原 `window_geometry.detect_screen` / `force_*` 与 `subprocess_transport.start` 本特性 diff；字体回退可独立保留。

---

## 9. 实现记录

| 日期 | 内容 |
|------|------|
| 2026-07-10 | 文档 Approved → 实现；`window_geometry` 平台分发 + CoreGraphics macOS；`subprocess_transport` UTF-8；`seat_ui_hub` 非 Win 视 Tk 已布局；测试 T1–T5；相关 **27 passed**（含既有 seat/f0004/human） |
| 2026-07-11 | §3.2 / §10 修订：禁用 `_sdl2`；后台 reassert 不碰主窗；Tk 负 Y；`SDL_AUDIODRIVER=dummy` 默认 |

---

## 10. 修订 2026-07-11（macOS 稳定性硬规则）

> 与 [`F0001_window_geometry.md`](F0001_window_geometry.md) §13、[`docs/status/2026-07-11.md`](../status/2026-07-11.md) 对齐。

### 10.1 硬规则（实现必须遵守）

1. **禁止** `from pygame._sdl2...` 对 `Window` 做 position/size/focus 读写（含 `from_display_module` 探测后赋值）。  
2. **禁止** 在引擎/座位 spawn **后台线程**调用 `pygame.display.set_mode` / `force_window_placement` 作用于主窗。  
3. **禁止** 为换屏执行 `pygame.display.quit()` + 再 init（易 SEGV）。  
4. 主窗 pin：仅 `MahjongApp` 主循环线程 `_pin_main_window`。  
5. 座位：`SeatUIHub.reassert_placements` → `reassert_plan_windows(include_main=False)` + `apply_window_plan`（`set_geometry`）。  
6. 入口：`main.py` 可默认 `SDL_AUDIODRIVER=dummy`、启用 faulthandler；崩溃落 `logs/main_crash.log`。

### 10.2 验收增量

- [x] 四座 spawn 完成后主进程不 SEGV  
- [x] `detect_screen` 仍为 `macos_*` 分发、不触 windll  
- [x] geometry / f0004 相关测通过
