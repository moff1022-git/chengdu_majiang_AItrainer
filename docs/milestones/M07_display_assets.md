# M07 — AssetManager 与主程序全局显示

| 字段 | 值 |
|------|-----|
| **编号** | M07 |
| **标题** | AssetManager + main display (lobby / table / result) |
| **状态** | `Done` |
| **依赖** | **M01–M06 Done**；`assets/` + `assets/ASSETS.md` |
| **下一里程碑** | M08（analysis + strategy HUD 叠加） |
| **对应 PLAN** | §4 资源加载、§10 显示架构、§11 M7 |
| **后续增强** | 窗口居中/可缩放/2K 工作区 → **[F0001](../features/F0001_window_geometry.md)**（M07 交付固定 1280×720 后由 F0001 覆盖） |

---

## 1. 目标

用 **Pygame** 把已有 `assets/` 接到主程序，提供**可选的可视化观战/演示**（上帝视角或公开信息视角），与 headless 训练路径完全解耦：

1. **`display/asset_manager.py`**：统一路径、主题 green/blue、懒加载缓存、缩放 API（与 ASSETS.md 一致）。  
2. **`layout.py`**：1280×720 **基准**布局（座位、手牌区、弃牌区、分数、剩余牌）；窗口动态几何见 F0001。  
3. **`lobby_view` / `table_view` / `result_view`**：大厅配置 → 对局桌面 → 结算。  
4. **`hud_common`**：分数数字拼接、简易特效横幅（碰/杠/胡/流局）。  
5. **`main.py`**：CLI 分发 — 默认/显式 `gui` 开窗口；`train` 保持 headless。  
6. **观战回放环**：用 `PlayerGameRunner` 或逐步 `apply` 驱动 AI 自对弈，画面刷新状态。

本步**不**实现：Human 独立交互窗口（M09）、推理/策略 HUD 完整面板（M08）、音效。

---

## 2. 范围

### 2.1 In Scope

| 项 | 说明 |
|----|------|
| `display/asset_manager.py` | 资源加载核心 |
| `display/layout.py` | 布局常量与 rect 计算 |
| `display/hud_common.py` | 数字分、特效 |
| `display/lobby_view.py` | 主题、人数、玩家类型、开始 |
| `display/table_view.py` | 桌面渲染（观战） |
| `display/result_view.py` | 结算榜 |
| `display/app.py` | Pygame 主循环、场景切换 |
| `main.py` | 入口 CLI |
| `requirements.txt` | 启用 `pygame>=2.5` |
| 测试 | AssetManager 路径/缓存/主题（可无 display surface：`pygame` 用 dummy 驱动） |

### 2.2 Out of Scope

- `players/view` 本家视角完整版（可与 table 共用 AssetManager；M09 Human 再用）  
- `inference/*` `strategy/*` 策略叠加（M08 在 table 上挂 HUD）  
- 子进程 Human  
- 高保真动画时间轴（特效横幅显示 N ms 即可）  

---

## 3. 设计

### 3.1 依赖与 headless 安全

```text
requirements.txt:
  pytest>=7.0
  pygame>=2.5
  # numpy 仍注释，待需要时启用
```

- 单元测试：`os.environ.setdefault("SDL_VIDEODRIVER", "dummy")` 后 `pygame.init()`。  
- `training.runner` / orchestrator **不** import display（避免强制开窗）。  
- `main.py train` 不加载 `display.app`。

### 3.2 AssetManager

```python
class AssetManager:
    def __init__(self, root: Path | None = None, theme: str = "green"):
        # root 默认：项目根 / assets
        ...

    def set_theme(self, theme: Literal["green", "blue"]) -> None: ...
    def path_for(self, *parts) -> Path: ...
    def load(self, rel: str) -> Surface:  # 缓存 key=theme+rel 或无主题文件
    def tile(self, suit: str, rank: int) -> Surface: ...
    def tile_back(self) -> Surface: ...
    def tile_placeholder(self) -> Surface: ...
    def button(self, key: str) -> Surface: ...  # hu,pong,pass,...
    def bg(self, which: str) -> Surface: ...     # table|lobby|result
    def avatar(self, n: int) -> Surface: ...     # 1..4
    def seat_badge(self, dir: str) -> Surface: ...
    def dealer_badge(self) -> Surface: ...
    def dice(self, n: int) -> Surface: ...
    def icon(self, key: str) -> Surface: ...
    def fx(self, key: str) -> Surface: ...
    def digit(self, char: str, color: str, size: str) -> Surface: ...
    def char_glyph(self, key: str, size: str) -> Surface: ...
    def scale_to_width(self, surf: Surface, w: int) -> Surface: ...
```

路径规则严格对齐 `ASSETS.md`：

```text
tiles/{suit}/tile_{suit}_{n}_{theme}.png
tiles/backs/tile_back_{theme}.png
buttons/btn_{key}_{theme}.png
backgrounds/bg_{which}_{theme}.png
...
```

缺失文件：抛 `FileNotFoundError` 并带完整路径（开发期不静默占位，除非 `strict=False` 返回纯色 Surface）。

### 3.3 布局（1280×720）

| 区域 | 说明 |
|------|------|
| 背景 | `bg_table` 缩放铺满 |
| 下（本家/东起映射 seat 0 可配置） | 手牌横排；观战模式可显示正面或按 spectator 模式 |
| 上/左/右 | 对手：牌背 + 副露 + 弃牌区 |
| 中央 | 剩余牌数 icon + digits；骰子（开局动画可选） |
| 四角/边 | 头像、庄标、分数 |
| 底栏 | 设置/退出 icon（lobby 更完整） |

**观战模式**：

- `SpectatorMode.FULL`：所有手牌正面（调试/复盘）  
- `SpectatorMode.PUBLIC`：仅本配置「焦点座位」正面，其余牌背（默认焦点=东/seat0）

M07 默认 **FULL**（便于演示 AI 自对弈）；lobby 可切换。

座位映射：屏幕下=逻辑 `seat_offset` 起顺时针/逆时针（配置 `seat_screen_order`）。

### 3.4 场景状态机

```text
LOBBY ──Start──► TABLE (running game)
TABLE ──终局──► RESULT
RESULT ──再来/返回──► LOBBY 或 再开一局 TABLE
任意 Esc/退出 icon ──► quit
```

### 3.5 Lobby

- 背景 `bg_lobby` + logo  
- 控件（Pygame 简易：键盘/点击热区，不必完整 GUI 框架）：  
  - 主题 green/blue  
  - 人数 2/3/4  
  - 玩家类型串（默认 `rule_ai`×N）  
  - 观战 FULL/PUBLIC  
  - **开始** → 启动 `PlayerGameRunner` 于后台线程 **或** 主线程步进（推荐 **主线程固定步/帧驱动** 避免 Pygame 线程问题）  

**推荐驱动模型**：

```text
每帧：
  处理事件
  if game_pending_step and time_ok:
      orchestrator.step_once()  # 新增单步 API，或内部队列
  table_view.draw(state)
  flip
```

为降低复杂度，M07 可：

**方案 A（推荐）**：`PlayerGameRunner` 增加 `step()` 生成器/协程式逐步推进；GUI 每 N ms 调一次直到 `finished`。  
**方案 B**：整局 headless 跑完再只显示 result（体验差，不推荐）。  

规格采用 **方案 A**：在 `orchestrator` 增加 `InteractiveRunner` 或 `PlayerGameRunner` 的 `start()` + `step_once() -> bool`（done）。

### 3.6 Table 渲染内容（最低）

| 元素 | 资源 |
|------|------|
| 桌布 | bg_table |
| 各家手牌 | tile / tile_back |
| 副露 | tile 小尺寸横排 |
| 弃牌 | tile 更小 |
| 头像+庄 | avatar, dealer_badge |
| 分数 | digit gold/neg + md |
| 剩余墙 | icon_remain + digits |
| 最近事件 | fx_* 居中淡出 0.8s |
| phase 文字 | 可用 pygame.font 后备（assets 汉字有限） |

### 3.7 Result

- 背景 `bg_result`  
- 排名、分数（digits）、胡牌顺序摘要  
- 按钮：返回大厅 / 再来一局（confirm 图）

### 3.8 main.py CLI

```bash
# 图形大厅
python main.py
python main.py gui --theme green

# 直接观战一局 AI
python main.py play --players rule_ai,rule_ai,rule_ai,rule_ai --theme blue

# headless（M05/M06）
python main.py train --games 10 --players rule_ai,random,random,rule_ai
```

### 3.9 InteractiveRunner（引擎侧小扩展）

```python
class InteractiveRunner:
    """Like PlayerGameRunner but exposes step_once for GUI pump."""
    def setup(self) -> GameState: ...   # deal+opening+start_play 或分步
    def step_once(self) -> bool:
        """Advance one decision or auto-draw; return True if finished."""
    @property
    def state(self) -> GameState: ...
    @property
    def result(self) -> GameResult | None: ...
```

Opening 亦可分多 step（每位玩家一次 decide），GUI 可快速连点跳过（`auto_speed`）。

### 3.10 性能

- 背景缩放结果缓存  
- 牌面缩放到固定显示宽（如 48px）缓存 `tile|theme|w`  
- 目标 ≥30 FPS 空闲；AI 步进可限速 100–500 ms/动作可配置  

---

## 4. 文件清单

| 路径 | 动作 |
|------|------|
| `display/__init__.py` | 新增 |
| `display/asset_manager.py` | 新增 |
| `display/layout.py` | 新增 |
| `display/hud_common.py` | 新增 |
| `display/lobby_view.py` | 新增 |
| `display/table_view.py` | 新增 |
| `display/result_view.py` | 新增 |
| `display/app.py` | 新增主循环 |
| `engine/orchestrator.py` | 扩展 InteractiveRunner |
| `main.py` | 新增 CLI |
| `requirements.txt` | pygame |
| `tests/test_asset_manager.py` | 新增 |
| docs | 状态 |

---

## 5. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| A01 | AssetManager 加载 wan_1 green | Surface 非空 |
| A02 | 主题切换后路径变 blue | 缓存失效且可加载 |
| A03 | tile_placeholder 无主题 | 存在 |
| A04 | 缺文件 strict | FileNotFoundError |
| A05 | dummy 驱动 init app 不崩溃 | 可构造 AssetManager |
| I01 | InteractiveRunner 整局 step | finished |
| R01 | 全量回归无 display 的测试 | 通过 |

GUI 人工验收（非 CI 强制）：大厅→开局→见牌→结算。

```bash
pytest tests/ -q
# 人工: python main.py play --players rule_ai,rule_ai,rule_ai,rule_ai
```

---

## 6. 验收标准

- [x] AssetManager 覆盖 ASSETS 主类资源 API，双主题可切换  
- [x] Lobby / Table / Result 三场景可切换  
- [x] AI 观战可视觉跟完一局  
- [x] `main.py train` 仍 headless、不依赖窗口  
- [x] pygame 写入 requirements  
- [x] M01–M06 回归通过  
- [x] 无 Human 操作打牌、无 M08 策略 HUD  

---

## 7. 风险与开放问题

| 项 | 默认决议 |
|----|----------|
| GUI 驱动 | **InteractiveRunner.step_once** 主线程 |
| 观战默认 | **FULL** 手牌可见 |
| 字体不足 | phase/UI 文案用 `pygame.font` SysFont 中文若失败则英文 |
| 点击 | Lobby 热区 + 键盘快捷键（1 开始、T 主题） |

**开放问题 — 已关闭（用户确认 M07，2026-07-10）：**

| # | 决议 |
|---|------|
| 1 | 观战默认 **FULL**（所有手牌可见；PUBLIC 可配置） |
| 2 | AI 步进默认间隔 **200ms** |
| 3 | Lobby：**命令行参数 + 简易键盘**；鼠标点「开始/主题」即可 |

---

## 8. 实现备注（编码后填写）

- 新增：`display/asset_manager|layout|hud_common|lobby|table|result|app.py`
- 新增：`main.py`（gui / play / train）
- 扩展：`InteractiveRunner`（`setup` + `step_once`）
- `requirements.txt`：`pygame>=2.5`
- 测试：`test_asset_manager.py`；全量 **87 passed**
- convert_alpha 在无 display surface 时跳过（dummy 测试友好）

---

## 9. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | `Review` | 首版规格，待用户确认 |
| 2026-07-10 | `Approved` | 用户确认 M07；开放问题按默认方案关闭 |
| 2026-07-10 | `Done` | 实现完成 |
