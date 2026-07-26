# M09 — Human 玩家子进程隔离 + JSON Transport

| 字段 | 值 |
|------|-----|
| **编号** | M09 |
| **标题** | Human player subprocess + SubprocessTransport |
| **状态** | `Done` |
| **依赖** | **M01–M08 Done**（BasePlayer、protocols、analysis HUD、display AssetManager） |
| **下一里程碑** | M10（存档 / 回放 / 崩溃策略增强） |
| **对应 PLAN** | §5.3–5.4 玩家加入与进程模型、Human 强制子进程决议 |
| **后续增强** | 玩家窗初始位置/尺寸/可缩放 → **[F0001](../features/F0001_window_geometry.md)** |

---

## 1. 目标

实现**可玩的人类玩家**，与主程序**进程隔离**：

1. **`players/human_player.py`**：独立可执行模块（`python -m players.human_player`），自有 Pygame 窗口，本家视角（窗口几何见 F0001）。  
2. **`protocols/subprocess_transport.py`（或扩展 transport）**：主进程 ↔ 子进程 **stdin/stdout 一行 JSON** 协议。  
3. **`HumanPlayerProxy`（主进程内）**：实现 `BasePlayer` 接口，内部持有子进程；`decide` 阻塞直到子进程回 Decision。  
4. **注册表**：`PLAYER_REGISTRY["human"]`；支持  
   `python main.py play --players human,rule_ai,rule_ai,rule_ai`。  
5. **交互**：定缺、换三张、点选手牌弃牌、点按钮碰/杠/胡/过；可选显示 M08 analysis HUD（本家）。  
6. **生命周期**：对局结束 `on_game_end` + `shutdown` 终止子进程；子进程崩溃时主进程得到明确错误（完整 crash policy 留给 M10，本步至少检测并抛错/结束局）。

本步**不**实现：完整崩溃替换策略表、存档断点续玩、远程 Socket agent。

---

## 2. 范围

### 2.1 In Scope

| 项 | 说明 |
|----|------|
| `protocols/wire.py` | JSON 编解码：obs / request / decision / event / shutdown / hello |
| `protocols/subprocess_transport.py` | 拉起/通信/关闭子进程 |
| `players/human_proxy.py` | 主进程 BasePlayer 代理 |
| `players/human_player.py` | 子进程入口 + 本家 GUI 循环 |
| `players/view/player_view.py` | 本家桌面渲染（可复用 display 组件） |
| `players/registry.py` | 注册 `human` |
| `engine/orchestrator.py` | 对 human 使用 Subprocess 路径；超时可选 |
| `main.py` | play/gui 支持 human 在玩家串中 |
| 测试 | wire 编解码；proxy mock pipe；无真实 GUI 的协议单元测试 |

### 2.2 Out of Scope

- 多个人类座位同时各开窗口（**允许 1 个 human** 为首版硬限制；>1 可报错或顺序支持但测试仅 1）  
- M10 的 replace_player / abort_restart 完整配置  
- 触摸手势、动画高级特效  

---

## 3. 设计

### 3.1 进程拓扑

```text
主进程 (engine + orchestrator + 可选观战 main window)
    │
    │  spawn: python -m players.human_player --seat 0 --theme green
    │  stdin/stdout: NDJSON
    ▼
子进程 (Human GUI only)
    - 不 import 引擎状态机权威
    - 只根据 Observation/ActionRequest 渲染与回 Decision
```

**约束**：

- 子进程与主进程 **不得共享** 同一 Pygame display（Windows 上尤其重要）。  
- 若 `main.py play` 同时开观战窗 + human 窗：允许两窗口；观战窗仍驱动 AI 步进，human 决策时主循环 **阻塞在 proxy.decide**（观战窗可显示 “Waiting for human…”）。  

**推荐首版交互模式（开放问题默认）**：

- **`main.py play --players human,...`**：主进程 **不** 开观战 GUI，仅 headless 引擎 + human 子窗口（避免双窗口复杂度）。  
- 观战 GUI 仍只用于纯 AI：`--players rule_ai,...`。  

可选后续：`--spectate-with-human` 双窗。

### 3.2 线协议（NDJSON）

每行一个 JSON object，UTF-8，字段 `type` 区分：

| type | 方向 | 载荷 |
|------|------|------|
| `hello` | 子→主 | `{seat, version, pid}` 启动就绪 |
| `observation` | 主→子 | Observation.to_dict() |
| `action_request` | 主→子 | ActionRequest.to_dict() |
| `decision` | 子→主 | Decision.to_dict() |
| `event` | 主→子 | 可选广播 |
| `game_end` | 主→子 | result dict |
| `shutdown` | 主→子 | `{}` |
| `error` | 双向 | `{message}` |

**同步约定**：

1. 主进程 `observe` → 发 `observation`（可不要求 ACK）。  
2. 主进程 `decide` → 发 `action_request`，**阻塞读**直到 `decision` 且 `request_id` 匹配。  
3. 超时：`timeout_ms`（默认 **120000**）；超时抛 `HumanTimeoutError`（M10 再挂 crash policy；M09 结束对局）。  

### 3.3 HumanPlayerProxy（主进程）

```python
class HumanPlayerProxy(BasePlayer):
    def __init__(self, ..., theme: str = "green", timeout_ms: int = 120_000): ...
    def on_join(self, seat, config):
        # spawn subprocess with --seat --theme
    def observe(self, obs):
        transport.send_observation(obs)
    def decide(self, req) -> Decision:
        return transport.request_decision(req)  # blocking
    def on_game_end(self, result):
        transport.send_game_end(result)
    def shutdown(self):
        transport.shutdown()  # terminate process
```

`create_player("human")` → `HumanPlayerProxy`（不是子进程内类）。

### 3.4 子进程 GUI（human_player.py）

#### 3.4.1 启动

```bash
python -m players.human_player --seat 0 --theme green [--title "Seat 0"]
```

流程：

1. init pygame 独立窗口（建议 960×640 或 1280×720）  
2. stdout 写 `hello`  
3. 循环：读 stdin 行 → 更新 state view / pending request → 渲染 → 处理点击/键盘 → 若用户确认动作则写 `decision`

#### 3.4.2 本家视角渲染

复用：

- `AssetManager`  
- `analyze_for_seat` **不可用完整 GameState** 时：在 observation.view 上做轻量分析，或主进程在 request 中附带 `analysis` 可选字段  

**推荐**：主进程在发 `action_request` 前若 phase=discard 且 seat=human，调用 `analyze_for_seat` 把 `analysis` 塞进 request 扩展字段 `hints`（wire 可选），子进程只渲染。

子进程手牌：

- 点击选中 → 再点确认弃牌，或双击弃牌  
- 底部按钮：胡/碰/明杠/暗杠/补杠/过（按 legal 高亮）  
- 定缺：三门按钮  
- 换三张：点选 3 张同花色后确认  

`reason` 固定 `"human:click"` 或带简述。

#### 3.4.3 合法动作约束

子进程只允许提交 `legal_actions` 中的动作；UI 禁用非法按钮。

### 3.5 Orchestrator 改动

```python
# 创建 players 时 human 已是 Proxy（含子进程）
# decide 路径不变：player.decide(req)
# run() finally: 对所有 players shutdown()
```

`InteractiveRunner`：若含 human，`step_once` 在 human 座位会阻塞——GUI 观战模式下 **不建议** 与 human 混用（见 §3.1）。  
`PlayerGameRunner.run()`：**支持** human + AI headless 主进程。

### 3.6 main.py

```bash
# 人机对战（主进程无观战窗）
python main.py human --seat 0 --players human,rule_ai,rule_ai,rule_ai --theme green

# 或复用 play 检测 human 则走 headless engine
python main.py play --players human,rule_ai,rule_ai,rule_ai
```

若 `play` 含 human 且用户期望窗口：仅 human 子窗；主进程日志打到 console。

### 3.7 错误与崩溃

| 情况 | M09 行为 |
|------|----------|
| 子进程启动失败 | 抛错，不开始局 |
| decide 超时 | `HumanTimeoutError`，runner 结束局 `finished_reason=human_timeout` |
| 子进程意外退出 | 读 stdout 失败 → 同上类错误 |
| 非法 decision | 主进程校验失败 → 再请求一次或抛错（默认 **抛错**） |

### 3.8 安全

- 子进程只读协议消息，不执行任意代码  
- 不传递整墙明细给 human 以外座位（已有 view_filter）  

---

## 4. 文件清单

| 路径 | 动作 |
|------|------|
| `protocols/wire.py` | 新增 |
| `protocols/subprocess_transport.py` | 新增 |
| `players/human_proxy.py` | 新增 |
| `players/human_player.py` | 新增（`__main__`） |
| `players/view/__init__.py` | 新增 |
| `players/view/player_view.py` | 新增本家渲染 |
| `players/registry.py` | 注册 human |
| `engine/orchestrator.py` | shutdown/human 兼容 |
| `main.py` | `human` 子命令或 play 分支 |
| `tests/test_human_wire.py` | 协议与 mock |
| docs | 状态 |

---

## 5. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| H01 | wire roundtrip Decision | 字段一致 |
| H02 | mock transport decide | request_id 匹配 |
| H03 | proxy spawn + hello | 超时内收到 hello（可对 fake script） |
| H04 | 假子进程脚本回固定 PASS | 整局或单步 apply 成功 |
| H05 | registry human | create_player 返回 Proxy |
| H06 | 回归 M01–M08 | 通过 |

真实 GUI 人工验收：换三张、定缺、打牌、碰胡。

```bash
pytest tests/ -q
python main.py play --players human,rule_ai,rule_ai,rule_ai
```

---

## 6. 验收标准

- [x] `human` 注册并可与 3 AI 完成对局  
- [x] 子进程独立窗口，主进程引擎权威  
- [x] NDJSON 协议稳定；decide 阻塞与 request_id 匹配  
- [x] 合法动作 UI 约束；Decision 含 reason  
- [x] shutdown 能杀掉子进程  
- [x] 超时/崩溃有明确错误  
- [x] M01–M08 回归通过  

---

## 7. 风险与开放问题

| 项 | 默认决议 |
|----|----------|
| 双窗口 | 含 human 时主进程 **不开** 观战窗 |
| human 数量 | 首版 **最多 1** |
| 超时 | 默认 **120s** |
| 分析 | 主进程计算 hints 下发 |

**开放问题 — 已关闭（用户确认 M09，2026-07-10）：**

| # | 决议 |
|---|------|
| 1 | 含 human 时主进程 **不开观战 GUI**（仅 human 子窗口） |
| 2 | 首版 **最多 1 个 human** |
| 3 | 决策超时默认 **120s** |

---

## 8. 实现备注（编码后填写）

- 新增：`protocols/wire.py`、`subprocess_transport.py`
- 新增：`players/human_proxy.py`、`human_player.py`、`view/player_view.py`
- 注册 `human`；`main.py play` 含 human 时走 headless 引擎 + 子窗
- 测试：`test_human_wire.py`（含 fake 子进程）；全量 **98 passed**

---

## 9. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | `Review` | 首版规格，待用户确认 |
| 2026-07-10 | `Approved` | 用户确认 M09；开放问题按默认方案关闭 |
| 2026-07-10 | `Done` | 实现完成 |
