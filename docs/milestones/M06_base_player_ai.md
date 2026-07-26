# M06 — BasePlayer、Random/Rule AI、多玩家 Session 编排

| 字段 | 值 |
|------|-----|
| **编号** | M06 |
| **标题** | Pluggable players + AI baselines + multi-agent session |
| **状态** | `Done` |
| **依赖** | **M01–M05 Done**（引擎权威、legal_actions、计分、JSONL） |
| **下一里程碑** | M07（AssetManager + 主程序显示） |
| **对应 PLAN** | §1.1 职责边界、§3.3–3.4 玩家接口、§5 通信、§11 M6 |

---

## 1. 目标

在引擎之上建立**可插拔玩家层**，使主程序可编排 2–4 名决策者完成完整血战局（含开局换三张/定缺）：

1. **`protocols/`**：Observation / ActionRequest / Decision 消息契约；InProcess 传输。  
2. **`players/base_player.py`**：标准抽象接口（observe / decide / 生命周期）。  
3. **`RandomPlayer`**：均匀随机合法动作（基线 + 测试）。  
4. **`RuleAIPlayer`**：轻量规则 AI（优先胡/杠/碰；弃牌优先缺门与孤张；附 `reason`）。  
5. **`PlayerOrchestrator` / 扩展 `GameSession`**：按相位向对应座位请求决策并 `apply`；支持 headless 训练模式。  
6. **注册表 + 工厂**：`PLAYER_REGISTRY`；CLI/API 字符串 `"random,rule_ai,rule_ai,random"` 组装。  
7. **视角过滤**：Observation 仅含本家手牌；对手只见 `hand_count` 与公开副露/弃牌。

本步**不**实现：Human 独立窗口/子进程（M09）、Pygame 渲染（M07）、完整 analysis HUD（M08）、崩溃策略完整化（M10 可增强）。

---

## 2. 范围

### 2.1 In Scope

| 项 | 说明 |
|----|------|
| `protocols/messages.py` | Observation, ActionRequest, Decision, 序列化 |
| `protocols/transport.py` | `InProcessTransport`（直接调用） |
| `protocols/view_filter.py` | `filter_state_for_seat(state, seat) -> dict` |
| `players/base_player.py` | `BasePlayer` ABC |
| `players/random_player.py` | 随机合法动作 |
| `players/rule_ai_player.py` | 规则启发 AI |
| `players/registry.py` | 名称 → 类 / 工厂 |
| `engine/orchestrator.py` 或扩展 `session.py` | 多玩家对局循环 |
| `training/runner.py` | 支持 `--players rule_ai×4` 等 |
| 测试 | 过滤隐私、4 AI 终局、Decision.reason 非空 |

### 2.2 Out of Scope

- `human_player` GUI / 子进程 transport  
- `players/analysis/*` 完整危险度面板（RuleAI 可内嵌极简启发式，不建 HUD）  
- 显示层、存档回放 UI  
- 超时 kill / 替换玩家（接口预留 `timeout_ms`；默认无限）  

---

## 3. 设计

### 3.1 职责边界（重申）

| 层 | 做 | 不做 |
|----|----|------|
| `engine/` | 规则、合法集、apply、计分 | 策略决策 |
| `players/` | 决策与 reason | 改 wall/私改状态 |
| `protocols/` | 消息与过滤 | 规则逻辑 |

玩家**只能**通过 `Decision.action` 回传；引擎 `legal_actions` 校验，非法 → `PlayError`（编排层可记日志并回退 PASS/随机，**首版直接抛错**便于测）。

### 3.2 消息契约

```python
@dataclass
class Observation:
    game_id: str
    self_seat: int
    phase: str
    view: dict              # 过滤后的状态 JSON 兼容 dict
    # view 含：本家 hand 全量；他家 hand 仅 count；wall 仅 remaining 数量

@dataclass
class ActionRequest:
    request_id: str
    seat: int
    phase: str
    legal_actions: list[Action]   # 引擎权威列表
    deadline_ms: int | None = None

@dataclass
class Decision:
    request_id: str
    action: Action
    reason: str
    analysis: dict | None = None  # 可选：shanten, candidates
    think_ms: int | None = None
```

`Action` 沿用 `engine.action.Action`（可 to_dict/from_dict）。

### 3.3 视角过滤规则

对 `self_seat`：

| 字段 | 本家 | 他家 |
|------|------|------|
| hand | 完整 tile ids | **省略**，仅 `hand_count` |
| melds / discard_pile / score / dingque / status | 可见 | 可见 |
| wall | 仅 `wall_remaining: int` | 同 |
| pending_exchange | 仅本家提交内容；他家是否已提交 bool | — |
| 他手牌内容 | 永不下发 | — |

实现：`build_observation(state, seat) -> Observation`，内部 `state.to_dict()` 深拷贝后改写。

### 3.4 BasePlayer

```python
class BasePlayer(ABC):
    def __init__(self, name: str = "", player_id: str | None = None, *, seed: int | None = None): ...
    
    @abstractmethod
    def on_join(self, seat: int, config: dict) -> None: ...

    def observe(self, observation: Observation) -> None:
        """默认缓存 last_observation。"""

    @abstractmethod
    def decide(self, request: ActionRequest) -> Decision: ...

    def on_event(self, event: dict) -> None: ...
    def on_game_end(self, result: dict) -> None: ...
    def shutdown(self) -> None: ...
```

- `training_mode: bool = True`：不渲染、不 sleep。  
- `rng: random.Random`：由 seed 派生，不污染引擎 seed。

### 3.5 RandomPlayer

```text
decide:
  action = rng.choice(request.legal_actions)
  reason = f"random:{action.type}"
```

开局 `exchange` / `dingque` 阶段：若编排扩展到 opening（见 §3.8），legal 由编排构造：

- 换三张：从本家 hand 用 `pick_same_suit_triple` 或随机同花色 3 张  
- 定缺：随机 Suit  

### 3.6 RuleAIPlayer（轻量）

优先级（discard 阶段）：

1. 若 legal 含 `HU` → 胡  
2. 若含 `GANG_AN` / `GANG_JIA` → 杠（可配置偏好）  
3. 否则弃牌：  
   - 强制缺门已由 legal 保证  
   - 在 legal discards 中优先：孤张 > 边张 > 中张（简单计数）；可调用 `shanten` 选使向听不升的弃牌（**建议做**：对每个 legal discard 试拆一手算 shanten，取最小）  
4. response：`HU` > `GANG_MING` > `PONG` > `PASS`（可配置是否主动碰）

```text
reason 示例: "rule:hu" | "rule:discard_min_shanten:wan_3" | "rule:pass"
analysis: {"shanten": 2, "candidates": [...]}  # 可选
```

### 3.7 注册表

```python
PLAYER_REGISTRY = {
    "random": RandomPlayer,
    "rule_ai": RuleAIPlayer,
    # "human": 预留 M09
}

def create_player(spec: str, *, seat: int, seed: int | None = None) -> BasePlayer:
    # spec: "random" | "rule_ai" | "rule_ai:name=Bot1"
```

### 3.8 编排器 `PlayerGameRunner`

相对现有 `play_random_game` 的升级：

```python
class PlayerGameRunner:
    def __init__(
        self,
        players: list[BasePlayer],  # len = num_players
        config: EngineConfig,
        *,
        game_id: str | None = None,
        logger: EpisodeLogger | None = None,
        reward_calc: RewardCalculator | None = None,
    ): ...

    def run(self) -> GameResult:
        """
        1. create_dealt_game
        2. opening: 对每个 seat 请求换三张 / 定缺（通过扩展 legal 或专用 request）
        3. start_play
        4. loop: draw 自动；discard/response 调对应 player.decide
        5. result + on_game_end
        """
```

#### 3.8.1 开局决策

引擎 opening 当前是同步 API `submit_exchange`。编排方式：

**方案 A（推荐）**：`PlayerGameRunner` 在 `dealt` 后：

1. `begin_exchange`  
2. 对每个 seat：构造 `ActionRequest`，`legal` = 候选三张列表（或由玩家返回 3 tiles，编排校验同花色）  
3. `submit_exchange`  
4. 定缺同理  

为简单起见，M06 为 opening 增加辅助：

```python
# engine/opening_legal.py 或 opening.py
def legal_exchange_choices(hand) -> list[list[Tile]]:  # 可简化：不枚举全部，由玩家自选后 validate
def suggest is not required
```

玩家 `decide` 在 `phase=exchange` 时：`Action(EXCHANGE, tiles=(t1,t2,t3))`  
`phase=dingque`：`Action(DINGQUE, suit=...)`

扩展 `legal_actions` **或** 在 orchestrator 单独分支（**推荐 orchestrator 分支**，避免污染行牌 legal）。

### 3.9 主循环伪代码

```text
while not terminal:
  if phase == draw: auto_draw; continue
  if phase == discard:
    seat = current_seat
    obs = build_observation(state, seat)
    players[seat].observe(obs)
    req = ActionRequest(..., legal=legal_actions(state, seat))
    dec = players[seat].decide(req)
    log decision
    apply(seat, dec.action)
  if phase == response:
    for seat in response_seats not yet claimed:
      ... decide & apply  # 同步：可顺序询问，全部提交后引擎 resolve
```

响应阶段：与引擎「同步 pending」一致——编排器对每个 `response_seats` 各调用一次 `decide` 再 `apply`。

### 3.10 Decision 日志

EpisodeLogger 增加：

```json
{"type": "decision", "seat": 0, "request_id": "...", "action": {...}, "reason": "...", "analysis": {...}}
```

### 3.11 training.runner 扩展

```bash
python -m training.runner --games 20 --players rule_ai,rule_ai,random,random --log-dir logs/ai
```

默认仍 random×N；有 `--players` 时走 `PlayerGameRunner`。

### 3.12 与后续里程碑

| M07+ | 衔接 |
|------|------|
| M07 | 主程序显示观战；玩家仍 headless |
| M08 | RuleAI / analysis 填 Decision.analysis |
| M09 | HumanPlayer + SubprocessTransport 实现同一 BasePlayer |
| M10 | decide 超时 → crash policy |

---

## 4. 文件清单

| 路径 | 动作 |
|------|------|
| `protocols/__init__.py` | 新增 |
| `protocols/messages.py` | 新增 |
| `protocols/view_filter.py` | 新增 |
| `protocols/transport.py` | 新增 InProcess |
| `players/__init__.py` | 新增 |
| `players/base_player.py` | 新增 |
| `players/random_player.py` | 新增 |
| `players/rule_ai_player.py` | 新增 |
| `players/registry.py` | 新增 |
| `engine/orchestrator.py` | 新增 `PlayerGameRunner` |
| `training/runner.py` | 扩展 CLI |
| `tests/test_players.py` | 新增 |
| `tests/test_view_filter.py` | 新增 |
| docs | 状态更新 |

---

## 5. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| P01 | view_filter 隐藏他家 hand | dict 无他家 tile 列表 |
| P02 | RandomPlayer 动作合法 | 100 次 decide ⊆ legal |
| P03 | RuleAI 有 HU 必胡 | 构造 request 仅含 HU+… |
| P04 | 4×rule_ai 一局终局 | phase finished 无异常 |
| P05 | 4×mixed random/rule_ai ×10 局 | 全终局 |
| P06 | Decision.reason 非空 | 始终 |
| P07 | JSONL 含 decision 行 | logger 开启时 |
| P08 | 回归 M01–M05 | 通过 |

```bash
pytest tests/ -q
python -m training.runner --games 5 --players rule_ai,rule_ai,rule_ai,rule_ai --log-dir logs/_m06
```

---

## 6. 验收标准

- [x] BasePlayer + random + rule_ai 可注册组装  
- [x] Observation 视角隔离正确  
- [x] PlayerGameRunner 完成 opening + 血战终局  
- [x] Decision 带 reason；可选 analysis  
- [x] runner 支持 `--players`  
- [x] M01–M05 回归通过  
- [x] 无 Human UI、无 Pygame  

---

## 7. 风险与开放问题

| 项 | 默认决议 |
|----|----------|
| 非法 Decision | **抛错**（不静默改 PASS） |
| RuleAI 碰牌 | 默认 **碰**（response 优先于 PASS） |
| Opening legal 枚举 | 不枚举全部三张组合；玩家提交后 `validate_exchange_tiles` |
| InProcess only | M06 仅进程内 |

**开放问题 — 已关闭（用户确认 M06，2026-07-10）：**

| # | 决议 |
|---|------|
| 1 | RuleAI response 默认 **主动碰/明杠**（优先于 PASS） |
| 2 | 非法 Decision **直接抛错**（不静默替换） |
| 3 | Opening（换三张/定缺）**统一走 decide** |

---

## 8. 实现备注（编码后填写）

- 新增：`protocols/`（messages, view_filter, transport）、`players/`（base, random, rule_ai, registry）
- 新增：`engine/orchestrator.py`（`PlayerGameRunner` / `run_players_game`）
- `training.runner`：`--players rule_ai,random,...`；原人数参数改为 `--num-players`
- 测试：`test_players.py`、`test_view_filter.py`；全量回归通过

---

## 9. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | `Review` | 首版规格，待用户确认 |
| 2026-07-10 | `Approved` | 用户确认 M06；开放问题按默认方案关闭 |
| 2026-07-10 | `Done` | 实现完成 |
