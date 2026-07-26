# F0001 — 主程序 / 玩家窗口几何与动态缩放

| 字段 | 值 |
|------|-----|
| **编号** | F0001 |
| **标题** | Window geometry: resizable main + player windows within 2K |
| **状态** | `Done` |
| **类型** | 功能增强（UI） |
| **依赖** | M07（display）、M09（human 子进程窗口） |
| **关联** | `PLAN.md` §4 资源/缩放、§10 显示架构；`docs/milestones/M07` / `M09` |

> **流程说明（2026-07-10）**  
> 本需求在会话中曾**先改代码、后补规格**，违反 `docs/DEVELOPMENT.md` Docs-First。  
> 本文档现为该需求的**权威规格**；后续任何几何/默认尺寸/排布变更须**先改本文 → 确认 → 再改代码**。

---

## 1. 背景与动机

M07 将主程序固定为 **1280×720** 不可缩放；M09 Human 子进程固定 **960×640**、无统一定位。用户要求：

1. **主程序与玩家程序窗口均可动态调整大小**（用户拖拽边缘）。  
2. **初始化排布**：主程序**居中**；玩家程序按座位分布在**四个方向**。  
3. **整体控制在 2K 分辨率以内**（工作区 ≤ **2560×1440**），且在更小桌面上不溢出。

---

## 2. 目标

| # | 目标 |
|---|------|
| G1 | 定义「工作区」= `min(主显示器分辨率, 2560×1440)`，在桌面内居中 |
| G2 | 主窗口初始尺寸与位置由工作区计算，**居中** |
| G3 | 玩家窗口（Human 子进程）按座位映射到 **下 / 右 / 上 / 左**，环绕主窗虚拟占位 |
| G4 | 主窗与玩家窗均以 `pygame.RESIZABLE` 打开；内容布局随客户区尺寸重算 |
| G5 | 首选尺寸放不下时，**等比缩小**主窗与玩家窗，使整组包围盒落在工作区内 |
| G6 | 纯逻辑几何可单测（不依赖真实开窗） |

---

## 3. 范围

### 3.1 In Scope

| 项 | 说明 |
|----|------|
| `display/window_geometry.py` | 工作区、窗口计划、SDL 定位、可缩放开窗辅助 |
| `display/layout.py` | 基准 1280×720；`Layout.from_window(w,h)` 缩放牌面尺寸 |
| `display/app.py` | 主窗居中 + RESIZABLE + `VIDEORESIZE` |
| `display/lobby_view.py` / `result_view.py` / `table_view.py` | 按 `screen.get_size()` 排版，禁止写死仅 1280×720 热区 |
| `players/human_player.py` | CLI：`--x/--y/--width/--height/--num-players`；可缩放 |
| `players/human_proxy.py` | `on_join` 时注入几何 CLI 参数 |
| `players/view/player_view.py` | 手牌/按钮随窗口宽度/高度自适应 |
| 测试 | `tests/test_window_geometry.py` |
| 文档 | 本规格、`PLAN.md` §10、changelog、features 索引 |

### 3.2 Out of Scope

- 多显示器精细布局（仅主屏 `GetSystemMetrics` / `display.Info`）  
- 记住用户上次窗口尺寸（持久化 preferences）  
- 主 GUI 与 Human 窗「对接边吸附」动画  
- 非 Human 的 AI 不单独开窗（仍在主程序 table 内绘制）  
- 触摸/高 DPI 独立缩放策略（沿用系统 DPI + pygame 像素坐标）

---

## 4. 设计

### 4.1 启动流程（强制）

**任何完整 UI 会话必须按此顺序：**

```text
1. detect_current_monitor()
     → 判定「运行命令所在屏幕」（多显示器）
     优先级：
       a) 控制台窗口 GetConsoleWindow → MonitorFromWindow
       b) 前台窗口 GetForegroundWindow → MonitorFromWindow
       c) 鼠标位置 GetCursorPos → MonitorFromPoint
       d) 回退主显示器
2. detect_screen()
     → 该监视器的工作区 rcWork（不含任务栏）：origin (left,top) + width/height
3. plan_for_screen(N)
     → 基于该工作区计算「唯一」WindowPlan（主窗 + 全部座位）
4. 打开主程序 / 各座位窗口 → 全部落在该屏幕工作区内
```

- **禁止**主程序、人类代理、AI Hub 各自独立重算导致坐标不一致。  
- **禁止**在布局前调用 `SetProcessDPIAware` 混用物理/逻辑像素。  
- 坐标统一为 **Windows 逻辑像素 / 监视器工作区**，与默认子进程一致。  
- 控制台打印：  
  `[display] monitor #? work WxH@(ox,oy) via console|foreground|cursor|primary`  
  `[display] plan main=... seat0=...`

### 4.2 工作区（2K 上限，相对于当前监视器）

```text
mon_left, mon_top, mon_w, mon_h  ← 当前监视器 rcWork
work_w = min(mon_w, 2560)
work_h = min(mon_h, 1440)
work_x = mon_left + (mon_w - work_w) // 2
work_y = mon_top  + (mon_h - work_h) // 2
```

所有**初始**窗口位置与包围盒必须落在 `work` 矩形内（允许边距 `MARGIN`）。

### 4.2 默认尺寸（缩放前）

| 窗口 | 宽 | 高 | 最小（RESIZE 下限） |
|------|----|----|---------------------|
| 主程序 | 1280 | 720 | 800 × 480 |
| 玩家程序 | 720 | 480 | 480 × 360 |

间距：`GAP = 16`（主窗与玩家窗之间）、`MARGIN = 12`（工作区内边距）。

### 4.3 初始化排布

```text
              [座位2  top]
[座位3 left]  [ 主程序 center ]  [座位1 right]
              [座位0  bottom]
```

| 座位 seat | 屏幕方位 Slot | 相对主窗 |
|-----------|---------------|----------|
| 0 | bottom | 主窗下方，水平居中于主窗 |
| 1 | right | 主窗右侧，垂直居中于主窗 |
| 2 | top | 主窗上方，水平居中于主窗 |
| 3 | left | 主窗左侧，垂直居中于主窗 |

**人数变体**：

- 2 人：seat0 → bottom，seat1 → top  
- 3 人：seat0 → bottom，seat1 → right，seat2 → left  
- 4 人：上表  

仅玩家窗、无主 GUI 时（如 headless 引擎 + Human）：仍按「虚拟主窗占位在工作区中心」计算玩家位置，保证四向语义一致。

### 4.4 放不下时的缩放

```text
need_w / need_h = 主尺寸 + 各侧玩家尺寸 + GAP
scale = min(1, avail_w/need_w, avail_h/need_h)
主、玩家宽高 *= scale（再 clamp 到最小尺寸；极端小屏可再压一轮）
```

### 4.5 动态调整（运行时）

| 端 | 行为 |
|----|------|
| 主程序 | `pygame.RESIZABLE`；处理 `VIDEORESIZE` → 更新 `Layout` / TableView / 背景缩放 |
| 玩家程序 | 同上；`PlayerView` 用手牌数与客户区宽度估算牌宽 |

用户拖大超过 2K **允许**（2K 约束仅作用于**初始化排布**，避免开局溢出；不强制运行时锁死）。

### 4.6 子进程传参

`HumanPlayerProxy.on_join` → `SubprocessTransport.extra_args`：

```text
--x --y --width --height --num-players N
```

由 `compute_window_plan(N).players[seat]` 生成；`human_player` 缺省参数时自行 `compute_window_plan` 兜底。

### 4.7 模块职责

| 模块 | 职责 |
|------|------|
| `window_geometry` | 纯几何 + 开窗辅助；**禁止**依赖 engine 状态 |
| `layout` | 客户区内牌桌/座位槽布局（相对窗口） |
| `app` / `human_player` | 应用几何计划并响应 resize |

与 table 内 `seat_to_slot(focus)` **不同**：后者是牌桌视角相对本家；本功能是**操作系统窗口**在屏幕上的方位。

---

## 5. 接口与数据

### 5.1 公开 API（`display/window_geometry.py`）

```python
MAX_WORK_W, MAX_WORK_H = 2560, 1440

@dataclass(frozen=True)
class WindowRect:
    x: int; y: int; w: int; h: int

@dataclass(frozen=True)
class WindowPlan:
    work: WindowRect
    main: WindowRect
    players: dict[int, WindowRect]  # seat -> rect
    scale: float

def desktop_size() -> tuple[int, int]: ...
def work_area(desktop: tuple[int, int] | None = None) -> WindowRect: ...
def seat_slot(seat: int, num_players: int = 4) -> Literal["bottom","right","top","left"]: ...
def compute_window_plan(
    num_players: int = 4,
    *,
    include_main: bool = True,
    desktop: tuple[int, int] | None = None,
    main_size: tuple[int, int] | None = None,
    player_size: tuple[int, int] | None = None,
) -> WindowPlan: ...
def open_resizable_window(size, *, pos=None, caption=None, min_size=None) -> Surface: ...
def plan_cli_args(rect: WindowRect) -> list[str]: ...
```

### 5.2 `Layout.from_window(width, height)`

相对 1280×720 取 `s = min(w/1280, h/720)`（下限约 0.5），缩放 `tile_w` / `tile_small_w` / `tile_tiny_w`。

### 5.3 Human CLI

| 参数 | 含义 |
|------|------|
| `--seat` | 座位（必填） |
| `--x` `--y` | 初始左上角（屏坐标） |
| `--width` `--height` | 初始客户区 |
| `--num-players` | 参与排布的人数（默认 4） |
| `--theme` | green / blue |

---

## 6. 影响面

| 区域 | 影响 |
|------|------|
| engine | 无 |
| training | 无 |
| display | 是（几何 + 视图自适应） |
| players/human | 是（窗口参数） |
| assets | 无新资源；背景仍 smoothscale 填客户区 |

### 兼容性

- CLI 无新必选参数；缺省行为变为「居中 + 可缩放」  
- 旧固定分辨率假设的点击测试需用动态 rect（lobby/result 已改）  
- headless / dummy 驱动：几何单测不调用 `set_mode` 亦可跑 `compute_window_plan`

---

## 7. 文件清单

| 路径 | 动作 |
|------|------|
| `docs/features/F0001_window_geometry.md` | 本规格 |
| `docs/features/README.md` | 索引 |
| `PLAN.md` §10 / 目录 | 同步约定 |
| `display/window_geometry.py` | 新增 |
| `display/layout.py` | 修改 |
| `display/app.py` | 修改 |
| `display/lobby_view.py` | 修改 |
| `display/result_view.py` | 修改 |
| `display/table_view.py` | 修改 |
| `players/human_player.py` | 修改 |
| `players/human_proxy.py` | 修改 |
| `players/view/player_view.py` | 修改 |
| `tests/test_window_geometry.py` | 新增 |
| `README.md` | 用户说明 |

---

## 8. 测试计划

### 8.1 自动化（pytest）

| ID | 用例 | 期望 |
|----|------|------|
| G01 | `work_area(3840×2160)` | 2560×1440 居中 |
| G02 | `work_area(1920×1080)` | 1920×1080 原点 |
| G03 | 4p plan @ 2560×1440 | 包围盒 ⊆ work；主中心≈work 中心 |
| G04 | 四向相对关系 | bottom 在主下、top 在主上、left/right 在两侧 |
| G05 | 小屏 1366×768 | 不溢出 work；scale≤1 |
| G06 | `Layout.from_window` | 大窗 tile≥基准；小窗 tile≤基准且≥下限 |
| R01 | 全量回归 | 通过 |

### 8.2 用户验收（人工）

完整步骤、命令与通过标准见：**[F0001_user_test_plan.md](F0001_user_test_plan.md)**（U01–U22）。

---

## 9. 验收标准

- [x] 主程序启动于工作区中心，可拖拽缩放，场景可重绘  
- [x] Human 玩家窗按座位四向初始定位（参数可注入）  
- [x] 初始整组布局 ≤2K 工作区；小屏自动缩小  
- [x] lobby / table / result / player_view 不依赖写死 1280×720 热区  
- [x] 几何单测通过；全量回归通过  
- [x] 本规格落盘且 PLAN/索引同步  

---

## 10. 回滚思路

1. 删除或停用 `window_geometry` 调用，恢复 `set_mode((1280,720))` / `(960,640)`。  
2. 去掉 human CLI 几何参数（子进程仍可启动）。  
3. 保留 `Layout.from_window` 或退回固定 `Layout()` —— 布局自适应可独立回滚。

---

## 11. 实现备注

- 实现路径与上文一致（2026-07-10）。  
- 2K 约束仅初始化；用户可手动拖到更大。  
- Windows 下定位依赖 `SDL_VIDEO_WINDOW_POS`（`set_mode` 前设置）。  
- 桌面分辨率：优先 `ctypes.windll.user32.GetSystemMetrics`，回退 1920×1080。  

---

## 12. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | 代码先于文档 | 违规实现（应避免） |
| 2026-07-10 | `Done` | 补齐本规格为权威；代码与验收已对齐 |
| 2026-07-11 | `Done`（补丁） | 见 §13；与 F0005 联合修订 macOS 多屏/线程安全 |

---

## 13. 修订 2026-07-11（多屏 · Tk 几何 · 线程安全）

> **状态**：`Done` 补丁；与 [`F0005_win_mac_compat.md`](F0005_win_mac_compat.md) §10、[`docs/status/2026-07-11.md`](../status/2026-07-11.md) 一致。  
> **性质**：行为澄清与缺陷修复（非扩大 Out of Scope 的「精细多显示器产品化」）。

### 13.1 布局权威流程（更新）

```text
1. detect_screen()     # 光标/控制台「当前屏」（macOS: CoreGraphics）
2. plan_for_screen(N, screen=…)  # 唯一 WindowPlan
3. 主窗：主线程 set SDL_VIDEO_WINDOW_POS + set_mode（禁止后台线程 set_mode）
4. 座位：CLI --x/--y/--width/--height；运行中 msg set_geometry
5. reassert_plan_windows(..., include_main=False)  # 父进程后台只 reassert 座位
```

- 主程序与 `SeatUIHub` **共用**同一 `WindowPlan` 实例/快照；ready 等待期间不因点座位而重测光标屏。  
- 会话内可锁定 `_session_layout_screen`，开局 `relock` 时再 `detect_screen()`。

### 13.2 主窗定位（macOS 强制约束）

| 允许 | 禁止 |
|------|------|
| `SDL_VIDEO_WINDOW_POS` + **主线程** `pygame.display.set_mode` | `pygame._sdl2.Window.position` / `.size` 读写（SEGV） |
| 主线程 `_pin_main_window` | 中途 `display.quit()` 再 init 换屏（易 SEGV / 破坏 surface） |
| Windows `HWND` `SetWindowPos` | 后台引擎线程调用 `force_window_placement` 碰主窗 |

### 13.3 座位 Tk 几何（负坐标）

- 几何串必须使用 **绝对坐标** 形式：`{w}x{h}+{x}+{y}`；当 `y<0` 时为 `...+x+-y`（例 `469x708+1928+-724`）。  
- **禁止** 生成 `...+x-y`（Tk 语义为「距底边 y」，会导致 Y 下移约一整屏）。  
- CLI 负 Y：`--y=-724`（避免 `--y` `-724` 被拆成选项）。  
- 辅助：`format_tk_geometry()`、`plan_cli_args()`；映射后可 best-effort 校正约一屏高度漂移。  
- 协议：主→座 `set_geometry`（见 wire）；Hub `apply_window_plan`。

### 13.4 Out of Scope 澄清

F0001 §3.2「多显示器精细布局」仍 **Out of Scope**（无记忆窗位、无吸附动画、无保证所有排列像素级完美）。  
本补丁仅规定：**当前屏检测 + 共 plan + 线程安全 + Tk 负 Y 正确性**。

### 13.5 验收增量

- [x] 后台 `start_all` / `reassert` 后主程序不因 `set_mode` SEGV  
- [x] `format_tk_geometry` 负 Y 单测  
- [x] 人工：四座 Y 不整体低一整主屏高度（副屏上方布局）
