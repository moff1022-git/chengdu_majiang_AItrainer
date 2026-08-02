# M04 — 血战行牌状态机、合法动作、一炮多响

| 字段 | 值 |
|------|-----|
| **编号** | M04 |
| **标题** | Blood-battle play loop / legal actions / multi-ron |
| **状态** | `Done` |
| **依赖** | **M01–M03 Done**（发牌、开局、向听/胡/番） |
| **下一里程碑** | M05（计分落地、Reward、JSONL 轨迹） |
| **对应 PLAN** | §2.4–2.5、§3 动作/会话、§11 M4 |

---

## 1. 目标

在 `phase=ready` 之后，实现成都血战**行牌引擎权威逻辑**（无 UI、无玩家进程、无完整分账）：

1. **摸打循环**：活跃玩家摸牌 → 自摸/暗杠/补杠/弃牌。  
2. **弃牌响应**：其他活跃玩家可胡 / 碰 / 明杠 / 过；优先级与**一炮多响**。  
3. **血战到底**：胡牌者 `status=finished` 离桌；仅剩 1 人活跃或牌墙尽 → 终局。  
4. **合法动作集** `legal_actions(seat)`：供后续 AI / Human / 训练使用。  
5. **可序列化**对局中状态 + 可 headless 用随机合法动作跑完全局（不崩溃）。

本步**不**实现：实际金币分账细节与花猪查叫金额（M05）、BasePlayer、Pygame、日志 JSONL 完整管线（M05 可接事件列表）。

**计分占位**：胡/杠时调用 M03 `compute_fan`，在 `GameState` 写入 `last_score_events`（结构体），**可先用 `2**fan * base` 简易改分**，完整规则表留给 M05 替换同一接口。

---

## 2. 范围

### 2.1 In Scope

| 项 | 说明 |
|----|------|
| `engine/action.py` | 扩展 `DISCARD/PASS/PONG/GANG_*/HU` |
| `engine/rules.py` | 规则开关：`multi_ron`、是否必须先打缺等 |
| `engine/legal.py` | `legal_actions(state, seat) -> list[Action]` |
| `engine/turn.py` / `blood_battle.py` | 行牌状态机：摸、弃、响应、胡、离桌、终局 |
| `engine/events.py` | 领域事件（可选轻量 list 挂在 state） |
| `engine/state.py` | 扩展行牌字段；`schema_version` → **3** |
| `engine/config.py` | `multi_ron: bool = True`、`base_score: int = 1` |
| `engine/session.py` | 最小 `GameSession`：`start_from_ready` / `step` / `apply` |
| 测试 | 固定牌型脚本 + 随机合法动作 N 局终局 |

### 2.2 Out of Scope

- 换三张/定缺（已是 M02；本步从 `ready` 进入）  
- 完整查花猪/查大叫/退税（M05；终局可发 `game_end` 事件占位）  
- 玩家模块、显示、训练 env  
- 抢杠胡完整时序（**首版实现**：补杠宣告后给其他家可 `HU` 抢杠；见 §3.6）  
- 海底特殊动画  

---

## 3. 设计

### 3.1 阶段扩展

| phase | 含义 |
|-------|------|
| `ready` | 开局完成，等待进入行牌（`start_play`） |
| `draw` | 当前活跃座应摸牌（或庄家首巡免摸已有 14 张） |
| `discard` | 当前座应弃牌（手牌为 14 或 11+… 模 3 余 2） |
| `response` | 弃牌/补杠后，等待其他座响应 |
| `finished` | 本局结束 |

迁移概要：

```text
ready ──start_play()──► discard   # 庄家 14 张，直接弃牌（不摸）
                          │
                          │ DISCARD
                          ▼
                       response ──(全过)──► draw(下家) ──► discard
                          │
                          │ HU (一炮多响可多人)
                          ▼
                       结算占位 → 胡者 finished → 若活跃≤1 或 … → finished
                          │
                          │ PONG / GANG_MING
                          ▼
                       discard（碰/杠者，杠后多摸 1）
```

### 3.2 玩家状态

```text
PlayerState.status:
  active    — 未胡，参与摸打
  finished  — 已胡离桌
  # bankrupt 预留，M04 不做
```

`hu_order: int | None` — 第几个胡（1-based）。  
`last_win: dict | None` — 番、形式、自摸/点炮摘要。

### 3.3 行牌相关 GameState 字段

```text
schema_version: 3
phase: ready|draw|discard|response|finished
current_seat: int
wall: list[Tile]              # 剩余牌墙（M01 起已有）
last_discard: Tile | None
last_discard_seat: int | None
response_seats: list[int]     # 仍需响应的座位（response 阶段）
pending_claims: dict[int, Action]  # 已提交的响应（可覆盖至锁定）
response_deadline_mode: "sync_all"  # 全员提交后按优先级结算（与换三张类似，便于 AI）
last_draw_tile: Tile | None   # 本巡摸牌（杠上花检测）
after_gang_draw: bool         # 刚杠后摸牌
qiang_gang_context: {seat, tile} | None
active_seats(): list[int]
finished_reason: "last_one"|"wall_empty"|"manual"|null
score_events: list[dict]      # 占位事件
turn_index: int               # 每成功弃牌/胡 +1
```

副露：将 `PlayerState.melds` 规范为 `MeldView` 可序列化 dict（`kind` + `tile_id`），与 M03 对齐。

### 3.4 动作类型

```python
class ActionType(str, Enum):
    EXCHANGE = "exchange"
    DINGQUE = "dingque"
    DISCARD = "discard"
    PASS = "pass"
    PONG = "pong"
    GANG_MING = "gang_ming"   # 直杠（手 3 + 弃牌）
    GANG_AN = "gang_an"       # 暗杠
    GANG_JIA = "gang_jia"     # 补杠（已碰 + 摸/手第 4 张）
    HU = "hu"
```

```python
@dataclass(frozen=True)
class Action:
    type: ActionType
    tiles: tuple[Tile, ...] = ()  # DISCARD: 1 tile; GANG_AN: 1 face; ...
    suit: Suit | None = None
    # 可选 claim 目标默认 last_discard
```

### 3.5 合法动作规则

#### 3.5.1 `discard` 阶段（仅 `current_seat` 且 active）

| 动作 | 条件 |
|------|------|
| `DISCARD(tile)` | `tile` 在手牌中；**建议强制**：若仍有缺门牌，则只能弃缺门（成都常见；**本规格采用强制打缺**） |
| `GANG_AN` | 手牌某牌面 ≥4 |
| `GANG_JIA` | 已有该牌 `pong` 副露且手牌有第 4 张 |
| `HU` | 当前手牌（已含摸进）`is_winning_hand`；可为自摸 |

摸牌后进入 `discard`；庄家第一巡无摸已在 `discard`。

#### 3.5.2 `draw` 阶段

引擎自动摸 1 张给 `current_seat`（不需玩家 Action），然后：

- 若墙空：进入流局终局流程（`finished_reason=wall_empty`）  
- 否则进 `discard`

`legal_actions` 在 `draw` 返回空列表；由 `session.step()` 自动执行摸牌。

#### 3.5.3 `response` 阶段（非弃牌者、active）

对 `last_discard`：

| 动作 | 条件 |
|------|------|
| `HU` | 手牌 + 弃牌 可胡，且无缺门残留 |
| `PONG` | 手牌该牌面 ≥2 |
| `GANG_MING` | 手牌该牌面 ≥3 |
| `PASS` | 总是合法 |

**无吃。**

补杠抢杠：`qiang_gang_context` 非空时，仅允许 `HU` / `PASS`（不可碰该张）。

### 3.6 响应结算与一炮多响

**同步收集模型（默认）**：

1. 进入 `response` 时，`response_seats =` 所有可行动的 active 他座（至少能 PASS；若某人仅 PASS 也要提交或引擎自动 PASS——**规格：必须显式 PASS 或有可主行动作时提交**；测试可用 auto-pass 辅助）。  
2. 每位提交 1 个 Action（可覆盖）。  
3. 全员提交后 `resolve_response()`：  
   - 收集所有 `HU` → 若 `multi_ron`：**全部生效**（按座位从弃牌者下家起逆时针排序记 `hu_order`）；若 `not multi_ron`：只取离弃牌者最近的下家方向一人。  
   - 若有人胡：点炮者不碰杠；胡者 finished；**弃牌不进入点炮者牌河？** 标准：弃牌进入弃牌者 `discard_pile`，已在 DISCARD 时写入。  
   - 若无人胡但有 `GANG_MING` 或 `PONG`：取**距离弃牌者最近的下家优先**（逆时针最近）；杠优先于碰若同一人；不同人时按座位优先。  
   - 全 `PASS`：下家摸牌。

**优先级**（多人冲突）：

```text
HU (multi) > 单人 HU > GANG_MING/PONG（近者优先）> PASS
```

同一座位不会同时提交多个；不同座位：胡可多人；碰杠仅一人成功。

### 3.7 血战终局

在每次胡后与每次摸牌前检查：

1. `active_count <= 1` → `phase=finished`，`finished_reason=last_one`  
2. 牌墙空且无法再摸 → 当前若需摸则 `finished_reason=wall_empty`（查叫占位事件）

`GameResult` 最小结构：

```python
@dataclass
class GameResult:
    game_id: str
    rankings: list[int]          # seat by score desc
    scores: dict[int, int]
    hu_sequence: list[dict]
    finished_reason: str
    wall_remaining: int
```

### 3.8 简易计分占位（可被 M05 替换）

```python
def apply_hu_score_placeholder(state, winners: list[int], loser: int | None, zimo: bool, fan: int):
    pts = (2 ** fan) * config.base_score
    if zimo:
        for s in active_except_winner:
            transfer(s, winner, pts)  # 每家付 pts；或多家赢家分别算
    else:
        transfer(loser, winner, pts)  # 一炮多响：对每位赢家各付一次
```

杠分占位：固定 `base_score` 即时转移（明细 M05）。

### 3.9 强制打缺

`legal_discards`：

- 若手牌存在 `dingque` 花色 → 只能弃这些牌  
- 否则任意手牌  

胡牌时 M03 已禁止残留缺门。

### 3.10 Session API

```python
class GameSession:
    def __init__(self, state: GameState, config: EngineConfig | None = None): ...
    
    def start_play(self) -> GameState:
        """ready → discard（庄家）"""

    def legal_actions(self, seat: int) -> list[Action]: ...

    def apply(self, seat: int, action: Action) -> GameState:
        """校验合法性后应用；自动执行 draw 链、response resolve"""

    def step_auto_draw(self) -> GameState:
        """phase==draw 时摸牌"""

    def is_terminal(self) -> bool: ...

    def result(self) -> GameResult: ...
```

辅助：

```python
def play_random_game(game_id, seed_players_rng, max_steps=10000) -> GameResult:
    """从 create_dealt_game + opening 快捷到终局；用固定 rng 选合法动作"""
```

开局快捷：

```python
def build_ready_game(game_id, exchanges, dingque, config) -> GameState:
    # M01+M02 组合；测试用
```

### 3.11 与 M03 集成

| 时机 | 调用 |
|------|------|
| 自摸检查 | `is_winning_hand(hand, melds, dingque)` |
| 点炮检查 | `hand + [discard]` |
| 番 | `compute_fan(..., context=WinContext(is_zimo=..., is_gang_shang_hua=after_gang_draw, is_qiang_gang=...))` |
| 听牌提示（可选） | `shanten` — 本步不强制 |

### 3.12 规则配置

```python
@dataclass
class EngineConfig:
    ...
    multi_ron: bool = True
    base_score: int = 1
    force_discard_dingque: bool = True
```

---

## 4. 文件清单

| 路径 | 动作 |
|------|------|
| `engine/action.py` | 扩展 |
| `engine/rules.py` | 新增 |
| `engine/legal.py` | 新增 |
| `engine/blood_battle.py` | 新增（状态机核心） |
| `engine/events.py` | 新增（轻量） |
| `engine/session.py` | 新增 |
| `engine/state.py` | 扩展 v3 |
| `engine/config.py` | 扩展 |
| `engine/__init__.py` | 导出 |
| `tests/test_blood_battle.py` | 新增 |
| `tests/test_legal_actions.py` | 新增 |
| docs | README / changelog / 本文件 |

---

## 5. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| B01 | ready→start_play | phase=discard，current=dealer |
| B02 | 弃牌→全 PASS→下家摸打 | 座位轮转正确 |
| B03 | 点炮单人胡 | winner finished，score_events 非空 |
| B04 | 一炮多响 multi_ron=True | 多名 finished |
| B05 | multi_ron=False | 仅最近下家胡 |
| B06 | 碰后手牌张数与 turn | 碰者 discard |
| B07 | 明杠/暗杠/补杠 | 副露正确；杠后摸牌 |
| B08 | 强制打缺 | legal 不含非缺门（当有缺门时） |
| B09 | 血战两人胡后第三人继续 | active 轮转 |
| B10 | 只剩 1 人 | finished |
| B11 | 随机合法动作 50 局 | 均 `is_terminal` 无异常 |
| B12 | v2 ready 状态可加载并开打 | 兼容 |
| L01 | legal 与 apply 拒绝非法 | 抛错 |

```bash
pytest tests/ -q
```

---

## 6. 验收标准

- [x] 从 `ready` 可完整行牌至 `finished`  
- [x] `legal_actions` 覆盖摸打响应关键动作且无吃  
- [x] 一炮多响默认开，可关  
- [x] 胡牌离桌、活跃人数终局条件正确  
- [x] 强制打缺生效  
- [x] 使用 M03 胡判/番；占位计分可改分  
- [x] 随机 50 局无崩溃  
- [x] M01–M03 回归通过  
- [x] 无 UI / 无 BasePlayer  

---

## 7. 风险与开放问题

| 项 | 默认决议 |
|----|----------|
| 响应模型 | **同步全员提交再结算**（非实时抢） |
| 强制打缺 | **是** |
| 一炮多响 | **默认 True** |
| 计分 | **2^fan 占位**，M05 替换 |
| 庄家首巡 | **不摸，直接弃牌** |

**开放问题 — 已关闭（用户确认 M04，2026-07-10）：**

| # | 决议 |
|---|------|
| 1 | 响应采用 **同步全员提交再结算**（便于 AI/训练） |
| 2 | **强制打缺**（有缺门只能弃缺门） |
| 3 | M04 占位计分 **`2**fan * base_score`**，M05 可替换同一接口 |

---

## 8. 实现备注（编码后填写）

- 新增：`blood_battle.py`、`legal.py`、`session.py`、`rules.py`、`events.py`
- 扩展：`action` 行牌类型、`state` schema **v3**、`config` multi_ron/base_score/force_discard_dingque
- 入口：`build_ready_game` / `GameSession` / `play_random_game`
- 测试：`test_blood_battle.py`、`test_legal_actions.py`；全量 **62 passed**
- 偏差：无

---

## 9. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | `Review` | 首版规格，待用户确认 |
| 2026-07-10 | `Approved` | 用户确认 M04；开放问题按默认方案关闭 |
| 2026-07-10 | `Done` | 实现完成；pytest 62 passed |
