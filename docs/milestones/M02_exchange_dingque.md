# M02 — 换三张 + 定缺（开局阶段状态机）

| 字段 | 值 |
|------|-----|
| **编号** | M02 |
| **标题** | Exchange-three + Dingque opening phases |
| **状态** | `Done` |
| **依赖** | **M01 Done**（`create_dealt_game`、`GameState`、`derive_seeds.exchange_seed`） |
| **下一里程碑** | M03（向听 / 胡形 / 成都番型 + `fan_cap`） |
| **对应 PLAN** | §2.3 步骤 4–5、§11 M2、产品决议「首版必须换三张」 |

---

## 1. 目标

在 M01「发牌完成（`phase=dealt`）」之后，实现成都血战开局后半段的**引擎权威逻辑**（无 UI、无玩家进程）：

1. **换三张**：各家从手牌选出 **同花色 3 张** 交出；按可复现方向同时交换；换完后张数不变（庄 14 / 闲 13）。  
2. **定缺**：各家选择缺一门（万/筒/条）；全部选定后进入可开打状态。  
3. **阶段状态机**：明确 `phase` 迁移、合法提交、拒绝非法操作、JSON 可序列化与同 `game_id` 下方向可复现。  
4. 为 M04 行牌预留：`phase=ready`（或 `playing` 前哨）表示「开局流程结束、等待庄家首次出牌」。

本步**不**实现摸打、碰杠胡、向听、计分、UI。

---

## 2. 范围

### 2.1 In Scope

| 项 | 说明 |
|----|------|
| `engine/opening.py` | 开局阶段状态机：进入换三张、提交交换、结算交换、提交定缺、完成开局 |
| `engine/exchange.py` | 换三张方向解析、合法性校验、手牌多集合扣减/加入 |
| `engine/action.py` | 最小 `ActionType` / `Action`：`EXCHANGE`、`DINGQUE`（及已有占位可扩展） |
| `engine/config.py` | 扩展：`exchange_dir` 配置项 |
| `engine/state.py` | 扩展字段与 `phase` 校验；`schema_version` → **2**（兼容读 v1 仅 `dealt`） |
| `engine/game_id.py` | 消费 `exchange_seed`（仅当方向模式需要随机时；默认 `auto_dice` **不依赖** exchange_seed，见 §3.4） |
| 单元测试 | 见 §7 |
| 文档回写 | 本文件、milestones README、changelog |

### 2.2 Out of Scope

- 行牌、合法弃牌、碰杠胡、血战、查花猪计分（定缺对胡牌的约束在 M03/M04 使用 `dingque` 字段）  
- 玩家 `BasePlayer` / transport / Human UI  
- 换三张 UI 动画  
- 自动帮玩家选牌/选缺（引擎只校验与应用；可选 `helpers` 提供「建议」但不进本里程碑必做）  
- 修改 M01 发牌顺序（仍：发完即庄 14 闲 13，**庄家 14 张参与换三张**）

---

## 3. 设计

### 3.1 阶段与迁移

```text
dealt  ──begin_exchange()──►  exchange
                                  │
                                  │ 每家 submit_exchange(seat, 3 tiles)
                                  │ 全部到齐 ──resolve_exchange()──►  dingque
                                  │
                                  ▼
                              dingque
                                  │
                                  │ 每家 submit_dingque(seat, suit)
                                  │ 全部到齐 ──►  ready
                                  ▼
                               ready     # 开局完成；current_seat = dealer；等待行牌（M04）
```

| phase | 含义 | 允许的操作 |
|-------|------|------------|
| `dealt` | M01 发牌完成，尚未开换三张 | `begin_exchange` |
| `exchange` | 等待各家提交 3 张 | `submit_exchange`；不可定缺 |
| `dingque` | 交换已完成，等待定缺 | `submit_dingque` |
| `ready` | 开局结束 | 本步无操作（M04 开始行牌） |

非法 phase 上的调用 → `ValueError`（或专用 `OpeningError`，继承 `ValueError`）。

**同步模型（M02 默认）**：换三张与定缺均为「全员提交后再统一结算/推进」，无需座位轮转顺序。实现可在内部用 `pending_exchange: dict[int, list[Tile] | None]`、`pending` 标记。

### 3.2 换三张规则（成都）

| 规则 | 规格 |
|------|------|
| 张数 | 必须恰好 **3** 张 |
| 花色 | **三张同一 `Suit`**（万/筒/条） |
| 来源 | 必须均可从该座位当前 `hand` 中按**多重集合**扣除（允许手牌有 4 张同牌面时选 3 张等同面） |
| 时机 | 发牌后、定缺前；**庄家 14 张、闲家 13 张**均参与 |
| 张数守恒 | 结算后：庄仍 14、闲仍 13；墙不变 |
| 公开性 | 引擎可记录 `exchange_log`（各家交出的 3 张与方向）供日志；序列化可选 |

**提交表示**：`list[Tile]` 长度 3，或 3 个 tile id；顺序不敏感（校验时排序或 multiset）。

**不可**：不同花色混换、少于/多于 3 张、手牌不足、重复提交覆盖策略见下。

**重复提交**：同一 `seat` 在 `resolve` 前允许 **覆盖** 上一次选择（便于 Human 改选）；`resolve` 后不可再改。

### 3.3 交换方向

配置项 `EngineConfig.exchange_dir`：

| 值 | 含义 | 接收座位 |
|----|------|----------|
| `clockwise` | 顺时针（引擎定义） | `(seat + 1) % n` |
| `counterclockwise` | 逆时针 | `(seat - 1) % n` |
| `across` | 对家/对向 | `(seat + across_offset(n)) % n` |
| `auto_dice` | **默认**；由本局骰点决定 | 见下 |

**`across_offset(n)`**：

| n | offset | 说明 |
|---|--------|------|
| 4 | 2 | 标准对家 |
| 3 | 1 | 无严格对家；定义为 +1（与 clockwise 相同，文档标明） |
| 2 | 1 | 唯一对手 |

**`auto_dice` 映射**（用已有 `state.dice.total`，**不**再掷骰；同 `game_id` 可复现）：

```text
r = (dice.total) % 3
r == 0 → clockwise
r == 1 → across
r == 2 → counterclockwise
```

> 说明：PLAN 曾预留 `exchange_seed`；M02 **默认不使用** `exchange_seed`，避免与骰点双重随机。`exchange_seed` 仍保留供将来 `exchange_dir=random_seed` 扩展（本步不实现该枚举值）。

解析函数：

```python
def resolve_exchange_direction(state: GameState, config: EngineConfig) -> Literal["clockwise","counterclockwise","across"]:
    ...
```

结算：

```text
for each seat:
  offered[seat] = 3 tiles removed from hand[seat]
for each seat:
  target = dest(seat, direction, n)
  hand[target].extend(offered[seat])
```

原子性：先全部扣除再全部加入，避免中途校验失败导致半更新；失败则状态不变（或在拷贝上操作再替换）。

### 3.4 定缺规则

| 规则 | 规格 |
|------|------|
| 选项 | `wan` / `tong` / `tiao` 三选一 |
| 每家恰好一个 | `PlayerState.dingque: Suit` |
| 无「花色张数限制」 | 允许缺门仍有牌（行牌时需打出；花猪惩罚在计分里程碑） |
| 可覆盖 | `dingque` phase 内、未全员完成前允许改选 |
| 完成条件 | 全部座位 `dingque is not None` → `phase = ready` |

`ready` 时：

- `current_seat = dealer_seat`（可写入 `GameState.current_seat`，M01 无此字段则 **M02 新增**）  
- `turn_index` 仍为 0（或保持）  
- 庄家手牌 14，下一步（M04）为庄家弃牌而非摸牌

### 3.5 状态字段扩展

```text
GameState (schema_version = 2)
  ...M01 fields...
  phase: dealt | exchange | dingque | ready
  current_seat: int | null     # ready 后 = dealer_seat；更早可为 null 或 dealer
  exchange_dir_resolved: str | null   # 实际方向 clockwise|...
  pending_exchange: dict[str, list[tile_id]] | null
      # JSON 键用 seat 字符串 "0","1",...；未提交的座位不出现或值为 null
  exchange_resolved: bool      # 或仅靠 phase
  exchange_log: optional list  # [{from_seat, to_seat, tiles: [...]}] 结算后填充
```

`PlayerState.dingque`：M01 已有，继续使用。

**校验 `validate()` 扩展**：

| phase | 手牌张数 | dingque | pending |
|-------|----------|---------|---------|
| dealt / exchange | 庄14闲13 | 全 None | exchange 时可有 pending |
| dingque / ready | 庄14闲13 | dingque：可部分；ready：全有 | pending 空 |

### 3.6 公开 API

```python
# engine/opening.py

class OpeningError(ValueError): ...

def begin_exchange(state: GameState, config: EngineConfig | None = None) -> GameState:
    """dealt → exchange；解析并写入 exchange_dir_resolved。返回新状态或原地更新（实现二选一，推荐返回新状态/深拷贝风格以便测试，或文档写明 in-place）。"""

def submit_exchange(state: GameState, seat: int, tiles: list[Tile]) -> GameState:
    """校验并记录 pending；若全员已提交则自动 resolve → dingque。"""

def submit_dingque(state: GameState, seat: int, suit: Suit) -> GameState:
    """校验并写入 dingque；若全员完成 → ready。"""

def get_opening_status(state: GameState) -> dict:
    """{phase, waiting_seats, exchange_dir, ...} 便于 CLI/测试。"""

# 可选拆分（若 submit 不自动 resolve）：
def try_resolve_exchange(state) -> GameState: ...
def try_resolve_dingque(state) -> GameState: ...
```

**推荐**：`submit_*` 在全员就绪时**自动**推进 phase，减少调用方步骤。

编排便捷函数（测试/headless）：

```python
def run_opening_with_choices(
    state: GameState,  # phase=dealt
    exchanges: dict[int, list[Tile]],
    dingque: dict[int, Suit],
    config: EngineConfig | None = None,
) -> GameState:
    """begin → 各 seat 提交换牌 → 各 seat 定缺 → ready。非法则抛错。"""
```

### 3.7 Action 最小定义

```python
class ActionType(Enum):
    EXCHANGE = "exchange"
    DINGQUE = "dingque"
    # 后续 M04: DISCARD, PONG, ...

@dataclass(frozen=True)
class Action:
    type: ActionType
    tiles: tuple[Tile, ...] = ()   # EXCHANGE: 3 tiles
    suit: Suit | None = None       # DINGQUE
```

M02 不要求完整 `legal_actions` 引擎，但应提供：

```python
def validate_exchange_action(state, seat, action) -> None
def validate_dingque_action(state, seat, action) -> None
```

### 3.8 与 M01 兼容

- `create_dealt_game` **保持** `phase=dealt`，不自动换三张。  
- 读 `schema_version=1`：仅支持 `dealt` 快照；写入一律 `schema_version=2`。  
- `from_dict`：v1 缺省 `pending_exchange=null`、`current_seat=null`、`exchange_dir_resolved=null`。

### 3.9 2/3/4 人

规则路径一致：方向公式与全员提交模型相同；仅 `n` 变化。`across` 在 3 人时的语义见 §3.3（文档写清，避免争议）。

---

## 4. 接口与数据

### 4.1 配置

```python
@dataclass(frozen=True)
class EngineConfig:
    num_players: int = 4
    initial_score: int = 0
    exchange_dir: str = "auto_dice"  # clockwise|counterclockwise|across|auto_dice
```

非法 `exchange_dir` → `ValueError`。

### 4.2 JSON 片段（exchange 中）

```json
{
  "schema_version": 2,
  "phase": "exchange",
  "exchange_dir_resolved": "clockwise",
  "pending_exchange": {
    "0": ["wan_1", "wan_2", "wan_3"],
    "2": ["tong_5", "tong_5", "tong_6"]
  },
  "current_seat": null,
  "players": [
    {"seat": 0, "hand": ["..."], "dingque": null, "is_dealer": false}
  ]
}
```

### 4.3 错误表

| 情况 | 异常 |
|------|------|
| phase 不正确 | `OpeningError` |
| 交换张数≠3 / 不同花色 | `OpeningError` |
| 手牌不足 | `OpeningError` |
| seat 越界 | `OpeningError` |
| 定缺 suit 非法 | `OpeningError` |
| 在 dingque 提交 exchange | `OpeningError` |

---

## 5. 文件清单

| 路径 | 动作 |
|------|------|
| `engine/opening.py` | 新增 |
| `engine/exchange.py` | 新增 |
| `engine/action.py` | 新增 |
| `engine/config.py` | 修改：`exchange_dir` |
| `engine/state.py` | 修改：字段、`schema_version=2`、校验 |
| `engine/__init__.py` | 修改：导出 |
| `tests/test_exchange_dingque.py` | 新增 |
| `tests/test_state_serde.py` | 扩展 v2 往返（可选） |
| `docs/milestones/README.md` | M02 状态 |
| `docs/changelog.md` | 记录 |

---

## 6. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| T01 | `dealt → begin → exchange` | phase 正确；`exchange_dir_resolved` 已设 |
| T02 | `auto_dice` 与固定 dice.total 映射 | total%3 与方向表一致；同 game_id 稳定 |
| T03 | 合法换三张全员提交 | 自动进入 `dingque`；张数仍为庄14闲13 |
| T04 | 换牌后手牌 multiset | 自己失去 3 张、获得来源家 3 张 |
| T05 | 非法：混花色 / 2 张 / 手牌没有 | 抛错且状态不变（或等价） |
| T06 | 覆盖提交 | 二次 submit 覆盖 pending |
| T07 | 固定方向 `clockwise` | seat i 的牌到 i+1 |
| T08 | 定缺全员 | → `ready`；`current_seat==dealer` |
| T09 | 定缺覆盖 | 改选 suit 生效 |
| T10 | `run_opening_with_choices` 端到端 | dealt→ready；可序列化往返 |
| T11 | 2/3/4 人各跑通一轮 | 无异常、张数守恒 |
| T12 | v1 dealt 快照仍可读 | from_dict schema 1 |

```bash
pytest tests/test_exchange_dingque.py tests/test_tile_deck.py tests/test_game_id_repro.py tests/test_state_serde.py -q
```

（实现后全量回归，M01 不得破坏。）

---

## 7. 验收标准

- [x] `phase` 按 §3.1 迁移正确  
- [x] 换三张同花色 3 张校验严格；张数守恒  
- [x] `auto_dice` / 显式方向行为符合 §3.3；同 `game_id` 方向可复现  
- [x] 定缺完成后 `ready` 且 `current_seat == dealer_seat`  
- [x] JSON v2 往返成功；M01 测试仍通过  
- [x] 无 UI / 无行牌逻辑  
- [x] 2/3/4 人路径一致  

---

## 8. 风险与开放问题

| 项 | 默认决议（Review 可改） |
|----|------------------------|
| 庄家 14 张参与换三张 | **是**（与 M01 发牌衔接） |
| 3 人 `across` | **offset=1**（与顺时针相同） |
| `auto_dice` 映射 | **total % 3** → 顺/对/逆 |
| `exchange_seed` | M02 **不使用** |
| 状态更新风格 | 实现选用 **in-place 更新 state** 并返回同一引用，或纯函数返回副本——**推荐 in-place + 返回 state**，测试注意同一对象；若选纯函数须在实现备注写明 |

**开放问题 — 已关闭（用户确认 M02，2026-07-10）：**

| # | 决议 |
|---|------|
| 1 | **庄家 14 张参与换三张**（不改 M01 发牌顺序） |
| 2 | **`auto_dice`：`dice.total % 3`** → 顺时针 / 对家 / 逆时针 |
| 3 | 状态 API：**in-place 更新并返回同一 `state` 引用** |

---

## 9. 实现备注（编码后填写）

- 新增：`engine/opening.py`、`exchange.py`、`action.py`
- 扩展：`config.exchange_dir`、`state` schema v2（`current_seat` / `pending_exchange` / `exchange_log` / `exchange_dir_resolved`）
- 测试：`tests/test_exchange_dingque.py`；全量 **34 passed**（含 M01 回归）
- 状态更新：**in-place** 返回同一 `state`
- 偏差：无

---

## 10. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | `Review` | 首版规格，待用户确认 |
| 2026-07-10 | `Approved` | 用户确认 M02；开放问题按默认方案关闭 |
| 2026-07-10 | `Done` | 实现完成；pytest 34 passed |
