# F0002 — 完整对局 UI：座位窗可操作 + AI 座位窗展示

| 字段 | 值 |
|------|-----|
| **编号** | F0002 |
| **标题** | Seat windows: human interactive + AI watch + main spectate |
| **状态** | `Done` |
| **类型** | 缺陷修复 + 功能增强（UI） |
| **依赖** | M09 Human 子进程、F0001 窗口几何、主程序 live 双窗（2026-07-10） |
| **关联** | `players/human_player.py`、`PlayerView`、`display/app.py` live 模式 |

---

## 1. 背景与问题（用户反馈）

在 `python main.py human`（1 人类 + 3 AI）下：

| # | 现象 | 期望 |
|---|------|------|
| P1 | 人类玩家窗口**只有背景**，无可操作图形（手牌/按钮/文字） | 本家手牌、分数、操作按钮、阶段提示完整可点 |
| P2 | **其他 AI 没有座位窗口** | 每个座位一个玩家窗（AI 为只读观战窗，非人类操作） |

另：主程序全局观战窗应继续保留（已有）。

---

## 2. 根因分析（实现前结论）

### 2.1 P1 人类窗空白

综合代码审查，高概率组合根因：

1. **协议数据到达偏晚或 stdin 每帧只读一行**，在 Windows 管道下若处理不及时，界面长期停在 `phase=wait` 且 `view={}`，仅能画背景。  
2. **`PlayerView` 强依赖 observation**：无 `me.hand` 时不画牌；无 `legal` 时不画按钮；文案依赖 `SysFont`，在部分环境下对比度/字体弱，观感像「只有背景」。  
3. **引擎未在 `on_join` 后立刻推送开局 observation**，人类窗在首轮 `action_request` 前缺少可渲染状态。  
4. **计分数字资源异常**时 `blit_score` 未兜底，可能导致后续绘制中断（需 try/兜底）。

### 2.2 P2 AI 无窗

**设计缺口（非偶然 bug）**：当前仅 `HumanPlayerProxy` 拉起子进程；`rule_ai` / `random` 为进程内决策，**从未创建座位窗口**。完整 UI 需要显式的 **AI 只读座位窗（watch）**。

---

## 3. 目标

| ID | 目标 |
|----|------|
| G1 | 人类座位窗：始终有清晰 HUD 骨架；收到状态后显示手牌与合法操作控件 |
| G2 | 完整 UI 模式（含 human、非 headless）：**每座位一窗** + **主程序一窗** |
| G3 | AI 座位窗：只读，随对局刷新公开/本家视角信息（本家手牌对 AI 窗为该 AI 自己的手牌） |
| G4 | 窗口几何继续遵循 F0001（主居中、座位四向、≤2K 初始工作区） |
| G5 | headless 模式不拉起任何座位窗 |

---

## 4. 范围

### 4.1 In Scope

| 项 | 说明 |
|----|------|
| 统一座位窗进程 | `players/seat_window.py`（或扩展 `human_player`）：`--mode play\|watch` |
| 人类 play 模式 | 交互：换三张/定缺/出牌/碰杠胡过 |
| AI watch 模式 | 只收 observation / game_end / shutdown，不回 decision |
| SeatUIHub | 主进程管理 AI 观战子进程；广播 observation |
| 引擎钩子 | 状态变化后通知 Hub（及保证人类 proxy 首包 observation） |
| PlayerView 加固 | 空状态骨架、字体兜底、资源失败不中断整帧 |
| 人类 stdin | 每帧抽干管道；启动即「连接中」UI |
| 文档 | 本规格、README/UAT 同步 |
| 测试 | 协议/Hub 单元级；渲染不依赖真实开窗可用 dummy |

### 4.2 Out of Scope

- AI 窗内人工改招（仍由引擎内 rule_ai/random 决策）  
- 超过 1 个 human  
- 远程网络座位窗  

---

## 5. 设计

### 5.1 窗口拓扑（4 人 + 主程序）

```text
              [座位2 watch 上]
[座位3 watch 左]  [主程序观战 中]  [座位1 watch 右]
              [座位0 play 下]   ← human 默认
```

- 主程序：`display/app.py` 现有 live 线程 + 牌桌  
- 座位 0 human：`play` 子进程（可操作）  
- 座位 1–3 AI：`watch` 子进程（只读）  

### 5.2 协议

沿用 NDJSON stdout/stdin。

| 方向 | play（人类） | watch（AI 窗） |
|------|--------------|----------------|
| 子→父 | hello, decision, error | hello |
| 父→子 | observation, action_request, game_end, shutdown | observation, game_end, shutdown |

watch 收到 `action_request` 应忽略（不回复）。

### 5.3 SeatUIHub（主进程）

```text
start(num_players, human_seat, theme, geometry_plan):
  for seat != human_seat:
    spawn python -m players.seat_window --mode watch --seat S ...
    wait hello

broadcast(state):
  for each watch transport:
    send observation(filter for that seat)

shutdown():
  send shutdown; terminate
```

人类子进程仍由 `HumanPlayerProxy` 管理（`--mode play`）。

### 5.4 广播时机

在 `PlayerGameRunner`（或 live 封装）中于以下节点 `broadcast`：

1. 全体 `on_join` 且 `dealt` 之后（**首包**，修复 P1）  
2. 每次换三张/定缺提交后  
3. `start_play` 后  
4. 每次 `do_draw` / `apply_action` 后  
5. 终局前  

人类路径：`HumanPlayerProxy.observe` 仍随 `decide` 前发送；另 **Hub 不重复发给 human 窗**（避免双写）。人类首包：在 `on_join` 完成后、进入 exchange 循环前，对 human 也 `observe(build_observation)` 一次。

### 5.5 PlayerView / 座位窗渲染

- 无数据：深色面板 + 「等待主程序 / 连接中」+ 座位号（绝不允许「纯背景无字」）  
- 有 hand：绘制手牌与选中框  
- 有 legal / phase：绘制按钮  
- `draw_text`：`Font` 失败时回退 `pygame.font.Font(None, size)`  
- `blit_score` / 单牌：失败画占位矩形，不抛穿  

### 5.6 CLI

```bash
python main.py human --theme green
# → 主程序 + 4 座位窗（1 play + 3 watch）
```

`players/human_player.py` 保留为 `play` 模式入口别名（兼容），内部转 `seat_window`。

---

## 6. 文件清单

| 路径 | 动作 |
|------|------|
| `docs/features/F0002_seat_windows_full_ui.md` | 本规格 |
| `players/seat_window.py` | 新增统一座位窗 |
| `players/seat_ui_hub.py` | 新增 AI watch 管理 + 广播 |
| `players/human_player.py` | 委托 seat_window play / 兼容 CLI |
| `players/human_proxy.py` | 启动参数 `--mode play`；join 后可推首包 |
| `players/view/player_view.py` | 空状态与兜底绘制 |
| `engine/orchestrator.py` | 状态变更回调 / 人类首包 obs |
| `display/app.py` | live 模式创建 Hub 并挂钩 |
| `tests/test_seat_ui_hub.py` | 新增 |
| `README.md` / UAT | 同步期望：4 座位窗 |

---

## 7. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| S01 | watch hello + 忽略 action_request | 不崩溃 |
| S02 | hub 启动 3 watch（mock） | 3 hello |
| S03 | PlayerView 空 view 绘制 | 含「等待」类文案（逻辑测或结构断言） |
| S04 | 人工：`main.py human` | 1 主 + 4 座位；人类可点牌 |
| R01 | 无 human 的 AI 观战 | 不强制 4 座位窗 |
| R02 | `--headless` | 无座位窗 |

---

## 8. 验收标准

- [x] 人类窗在连接后可见手牌与换三张/定缺控件（非纯背景）— PlayerView 骨架 + 首包 obs  
- [x] 3 个 AI 座位窗出现在 F0001 方位，并随对局刷新 — SeatUIHub  
- [x] 主程序观战窗正常  
- [ ] 人类可完成至少：换三张 → 定缺 → 一次弃牌（**请人工确认**）  
- [x] headless 行为不变  
- [x] 相关自动化测试通过（`tests/test_seat_ui.py` 等）  

### 实现备注

- `players/seat_window.py`：统一 play/watch；stdin 队列抽干；hello 先于 pygame  
- `players/seat_ui_hub.py`：AI watch 子进程 + broadcast  
- `PlayerGameRunner.on_state_change` + join 后首包 observation  
- `PlayerView`：空状态面板、字体/贴图兜底  

### 补丁（仅见主+S1+S2）

分区不重叠布局；Hub 容错；人类窗优先。  

### 补丁（先检测分辨率再设全部窗口）

**用户要求**：先检查当前屏幕分辨率，再设置所有窗口大小与位置。  

**决议**（对齐 F0001 §4.1）：

1. `detect_screen()` 用 **SPI_GETWORKAREA**（逻辑像素，不含任务栏）  
2. **禁止** `SetProcessDPIAware` 混用物理/逻辑坐标（否则子窗开到屏外，只剩主窗+S2）  
3. `plan_for_screen(N)` 一次生成全窗；主/人类/AI **共用** plan  

### 人类操作交互（出牌 / 过牌）

| 场景 | 交互 |
|------|------|
| 响应阶段**仅有「过」** | **自动过**，不弹确认、不点按钮 |
| 响应阶段有碰/杠/胡 | 显示对应按钮；**过** 一点即过（无需二次确认） |
| 弃牌阶段 | **双击**手牌直接出牌；**不显示**「确认出牌」按钮 |
| 弃牌阶段有暗杠/加杠/自摸胡 | 显示对应按钮，一点即执行 |  

---

## 9. 回滚

- 去掉 Hub 创建即可回到「仅 human 单窗」  
- `seat_window` play 路径可独立保留作为 human 修复  

---

## 10. 修订 2026-07-11（设置条 · 几何）

| 项 | 规定 |
|----|------|
| 设置 UI | 标题下**常显**「自动开始」「AI 策略」按钮条（非仅折叠面板）；详见 F0004 |
| 几何 | 使用 F0001 §13：`format_tk_geometry`、负 Y CLI、`set_geometry` 热迁移 |
| 与 F0005 | 禁止在座位 reassert 路径里碰主 pygame 窗 |

---

## 11. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | `Approved` | 用户两问题确认；文档先行后实现 |
| 2026-07-10 | `Done` | 代码实现；待人工验收换三张→弃牌 |
| 2026-07-10 | 补丁 | 不重叠布局 + Hub 容错 + 人类窗优先启动 |
| 2026-07-11 | 补丁 | §10 设置条常显 + 几何引用 F0001/F0004 |
