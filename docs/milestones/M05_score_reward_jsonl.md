# M05 — 正式计分、Reward 系统、JSONL 轨迹日志

| 字段 | 值 |
|------|-----|
| **编号** | M05 |
| **标题** | Score / Reward / Episode JSONL logging |
| **状态** | `Done` |
| **依赖** | **M01–M04 Done**（行牌、`compute_fan`、`GameResult`、`score_events` 占位） |
| **下一里程碑** | M06（BasePlayer + random/rule_ai + 完整 Session 编排） |
| **对应 PLAN** | §2.6–2.7、§3.6 Reward、§6.3 日志、§7 Reward 系统、§11 M5 |

---

## 1. 目标

把 M04 的 **`2**fan` 占位计分** 升级为可配置的**成都血战计分模块**，并打通训练友好的 **Reward** 与 **JSONL 逐步日志**：

1. **`engine/score.py`**：自摸 / 点炮（含一炮多响）/ 杠分 / 终局查叫与花猪；所有分变写入统一 `ScoreTransfer` 记录。  
2. **替换** `blood_battle` 内联占位结算，改为调用 `ScoreService`（接口稳定，便于单测与 M11 env）。  
3. **`engine/reward.py` + `configs/reward_default.json`**：由分变与终局排名计算 step / episode reward。  
4. **`training/episode_log.py`（或 `engine/logger.py`）**：按局写出 JSONL（game_start / decision 可选 / score / reward / game_end）。  
5. **headless 批跑入口**：`python -m training.runner` 或 `session` 辅助：N 局随机对局写日志不崩溃。

本步**不**实现：BasePlayer 决策接口（M06）、UI、完整 RL 训练循环（只提供日志与 reward 信号）。

---

## 2. 范围

### 2.1 In Scope

| 项 | 说明 |
|----|------|
| `engine/score.py` | 计分规则、`ScoreTransfer`、`apply_hu` / `apply_gang` / `settle_end` |
| `engine/reward.py` | `RewardConfig` / `RewardCalculator` |
| `configs/reward_default.json` | 默认权重 |
| `configs/score_default.json` | 底分、杠分表、花猪/查叫倍数（可选，或并入 EngineConfig） |
| `training/episode_log.py` | JSONL writer |
| `training/runner.py` | 最小批跑（随机合法动作 + 写日志） |
| 改造 `blood_battle.py` | 去掉内联 `2**fan`，改调 score 模块 |
| 扩展 `GameResult` | 含 transfers 摘要、是否流局、各家是否听牌/花猪标记 |
| 扩展 `EngineConfig` | score/reward 相关键或路径 |
| 测试 | 固定牌型分账夹具 + reward + jsonl 读写 |

### 2.2 Out of Scope

- 玩家策略（M06）  
- 显示金币动画（M07）  
- 完整 Gym env.step 封装（M11 可薄包一层本步 API）  
- 网络对战  

---

## 3. 设计

### 3.1 计分数据模型

```python
@dataclass(frozen=True)
class ScoreTransfer:
    reason: str           # hu_zimo | hu_dianpao | gang_ming | gang_an | gang_jia
                          # | hua_zhu | cha_jiao | tax | ...
    from_seat: int
    to_seat: int
    amount: int           # 正数：from 付给 to
    fan: int | None = None
    meta: dict = field(default_factory=dict)

@dataclass
class ScoreEvent:
    turn_index: int
    transfers: list[ScoreTransfer]
    balances_after: dict[int, int]   # seat -> score
```

所有 `PlayerState.score` 变更**必须**经 `ScoreService.apply_transfers`，并 append 到 `state.score_events`（升级结构：可继续用 list[dict]，序列化兼容）。

### 3.2 胡牌计分（替换占位）

设 `base = config.base_score`（默认 1），`pts = base * (2 ** fan)`（`fan` 已 `fan_cap`）。

| 类型 | 规则（默认） |
|------|----------------|
| **点炮** | 点炮者向**每位**胡牌者支付 `pts_w`（一炮多响分别算番） |
| **自摸** | 每位**仍 active 且非赢家**的玩家向胡家支付 `pts`（血战：已胡者不再付） |

> 与 M04 占位一致处保留；差异以本表为准。若配置 `zimo_pay_all_including_finished=false`（默认）。

### 3.3 杠分（默认表，可配置）

| 杠类型 | 默认 |
|--------|------|
| 明杠（直杠） | 点杠者付 `base * gang_ming_mult`（默认 mult=2）给杠者 |
| 补杠 | 三家各付 `base * gang_jia_mult`（默认 1）；血战仅 active 付 |
| 暗杠 | 三家各付 `base * gang_an_mult`（默认 2）；仅 active |

M04 当前未实现杠分转移 → **M05 补上**（在 `GANG_*` resolve 后调用）。

### 3.4 终局结算（`settle_end`）

触发：`phase=finished` 且 `finished_reason in {last_one, wall_empty}`（`max_steps` 也可跑简化结算）。

#### 3.4.1 花猪（hua_zhu）

- 定义：终局时 `status=active` 且手牌（+副露）仍含 `dingque` 花色。  
- 惩罚：花猪向**每位非花猪玩家**支付 `base * hua_zhu_mult * (2 ** hua_zhu_fan)`  
  - 默认：`hua_zhu_fan = 3`（或配置为固定 `hua_zhu_fixed`）  
- 已胡者可收花猪（默认 **是**）。

#### 3.4.2 查叫（cha_jiao）

- 仅当流局或墙尽导致多人未胡时（`wall_empty` 或配置开启的 last_one 旁支）。  
- **有叫**：`shanten(hand, melds, dingque).shanten == 0` 且非花猪。  
- **未叫**：active 且非花猪且 shanten > 0。  
- 默认：每位未叫者向每位有叫者支付 `base * (2 ** max_fan_ting)`  
  - `max_fan_ting`：对听牌形枚举 `ukeire` 中最大可能胡番的近似；**首版简化**：有叫收 `base * cha_jiao_mult`（默认 mult=1），或固定按「听牌按平胡 0 番 → 1 倍底」）。  
- **推荐首版简化（开放问题默认）**：  
  - 有叫：不付叫  
  - 未叫：向每个有叫者付 `base * (2 ** 0) = base`  
  - 花猪不再参与查叫（已单独罚）

#### 3.4.3 退税

- 首版：**不做**杠退税（可配置 `gang_tax=false`）；预留接口。

### 3.5 ScoreService API

```python
class ScoreService:
    def __init__(self, config: EngineConfig, score_table: dict | None = None): ...

    def apply_hu_zimo(self, state, winner: int, fan: int) -> list[ScoreTransfer]: ...
    def apply_hu_dianpao(self, state, winners: list[int], loser: int, fans: dict[int,int]) -> list[ScoreTransfer]: ...
    def apply_gang(self, state, kind: str, gang_seat: int, from_seat: int | None) -> list[ScoreTransfer]: ...
    def settle_end(self, state) -> list[ScoreTransfer]: ...
    def apply_transfers(self, state, transfers: list[ScoreTransfer]) -> None: ...
```

`blood_battle` 在胡/杠路径调用上述方法，**删除** `_transfer` 内联 `2**fan` 重复逻辑（可保留 `_transfer` 为 score 内部工具）。

### 3.6 Reward 系统

#### 3.6.1 配置 `configs/reward_default.json`

```json
{
  "hu_fan_scale": 1.0,
  "deal_in_penalty": 1.0,
  "rank_bonus": [3.0, 1.0, -1.0, -3.0],
  "gang_scale": 0.1,
  "final_score_scale": 0.01,
  "step_penalty": 0.0,
  "liuju_penalty": 0.0,
  "use_engine_score_as_reward": false,
  "hua_zhu_scale": 1.0,
  "cha_jiao_scale": 1.0
}
```

#### 3.6.2 RewardCalculator

```python
@dataclass
class RewardConfig:
    ...  # 与 JSON 字段一致
    @classmethod
    def load(cls, path: Path | None = None) -> RewardConfig: ...

class RewardCalculator:
    def __init__(self, config: RewardConfig): ...
    
    def on_transfers(self, transfers: list[ScoreTransfer]) -> dict[int, float]:
        """Dense reward per seat from this scoring event."""
        # use_engine_score_as_reward: reward[s] += delta_score * final_score_scale inverse
        # else: map reason → hu_fan_scale * fan, deal_in_penalty, gang_scale, ...
    
    def on_game_end(self, result: GameResult, state: GameState) -> dict[int, float]:
        """Sparse: rank_bonus + final_score_scale * score + liuju_penalty."""
    
    def reset(self) -> None: ...
```

`GameSession` / `play_random_game` / `training.runner` 在每次 score 后调用 `on_transfers`，终局调用 `on_game_end`，结果写入日志行 `type=reward`。

### 3.7 JSONL 日志

#### 3.7.1 路径

```text
logs/{run_id}/{game_id}.jsonl
```

`run_id` 默认 `cmjrun-{utc}-{rand}` 或 CLI 指定。

#### 3.7.2 行类型（最小集）

| type | 时机 | 主要字段 |
|------|------|----------|
| `game_start` | 局开始 | game_id, seed, config, players meta |
| `deal` | 可选 | hands（训练可开 `log_private=true`） |
| `phase` | 可选 | phase 变更 |
| `action` | 每次 apply | seat, action, legal_count |
| `score` | 计分后 | transfers, balances |
| `reward` | 计分/终局后 | seat_rewards |
| `game_end` | 终局 | GameResult + settle tags |

**隐私**：默认 headless 训练 `log_private=true` 写全手牌；若 false 则仅公开信息。

#### 3.7.3 API

```python
class EpisodeLogger:
    def __init__(self, run_dir: Path, game_id: str, *, log_private: bool = True): ...
    def emit(self, type: str, **payload) -> None: ...
    def close(self) -> None: ...
```

一行一个 JSON object，UTF-8，`ensure_ascii=False`。

### 3.8 Runner

```python
# training/runner.py
def run_random_batch(
    n_games: int,
    *,
    log_dir: Path,
    reward_path: Path | None = None,
    num_players: int = 4,
    seed: int = 0,
) -> dict:  # summary stats
```

CLI（可选最小）：

```bash
python -m training.runner --games 100 --log-dir logs/demo --seed 0
```

### 3.9 与 M04 兼容

- `play_random_game` 增加可选 `logger` / `reward_calc` 参数。  
- 旧测试不依赖具体分值的保持通过；新增分账夹具测试。  
- `schema_version`：**保持 3** 或升 **4**（若 score_events 结构 breaking）。  
  - **决议：升至 4**，from_dict 仍读 3（score_events 元素兼容 dict）。

### 3.10 模块依赖

```text
blood_battle ──► score ──► state.score / score_events
                │
                └──► reward (可选旁路)
session / runner ──► EpisodeLogger
fan (M03) ──► score (只消费 fan 整数)
shanten (M03) ──► settle_end 查叫
```

---

## 4. 文件清单

| 路径 | 动作 |
|------|------|
| `engine/score.py` | 新增 |
| `engine/reward.py` | 新增 |
| `engine/blood_battle.py` | 修改：接入 ScoreService；杠分 |
| `engine/session.py` | 修改：logger/reward 钩子 |
| `engine/state.py` | 小改：schema 4 可选 |
| `engine/config.py` | 扩展 score 相关默认 |
| `configs/reward_default.json` | 新增 |
| `configs/score_default.json` | 新增 |
| `training/__init__.py` | 新增 |
| `training/episode_log.py` | 新增 |
| `training/runner.py` | 新增 |
| `tests/test_score.py` | 新增 |
| `tests/test_reward.py` | 新增 |
| `tests/test_episode_log.py` | 新增 |
| docs | README / changelog / 本文件 |

---

## 5. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| SC01 | 点炮 fan=2 | loser -4base, winner +4base（base=1 → ±4） |
| SC02 | 一炮多响两家 | loser 付两次 |
| SC03 | 自摸 | 各 active 非己付 |
| SC04 | 暗杠 | active 他家付 gang_an |
| SC05 | 花猪 | 有缺门 active 被罚 |
| SC06 | 查叫简化 | 未叫付有叫 |
| RW01 | deal_in reward | 点炮座位负向 |
| RW02 | rank_bonus | 终局名次 |
| RW03 | use_engine_score_as_reward | 与分差一致比例 |
| LG01 | jsonl 行可解析 | game_start…game_end |
| LG02 | runner 10 局 | 文件存在且无异常 |
| RG01 | 全量回归 M01–M04 | 通过 |

```bash
pytest tests/ -q
python -m training.runner --games 10 --log-dir logs/_test
```

---

## 6. 验收标准

- [x] 胡/杠/终局分变均经 `ScoreService`，无 blood_battle 内联魔法数分账  
- [x] 花猪 + 简化查叫生效且可配置  
- [x] Reward 配置文件可调且反映到 `on_transfers` / `on_game_end`  
- [x] JSONL 含 score/reward/game_end；runner 批跑成功  
- [x] M01–M04 回归通过  
- [x] 无 UI / 无玩家策略模块  

---

## 7. 风险与开放问题

| 项 | 默认决议 |
|----|----------|
| 自摸付分对象 | 仅 **仍 active 的非赢家** |
| 查叫 | **简化**：未叫付有叫各 `base`；不做最大番搜索 |
| 杠退税 | **不做** |
| schema | **升 4**（兼容读 3） |
| 日志默认 | 训练 runner **log_private=true** |

**开放问题 — 已关闭（用户确认 M05，2026-07-10）：**

| # | 决议 |
|---|------|
| 1 | 查叫采用 **简化版**（未叫付有叫各 `base`；不做听牌最大番精确计算） |
| 2 | **schema 升至 4**（兼容读取 v3） |
| 3 | 批跑入口 **`python -m training.runner`**（暂不接 main.py CLI） |

---

## 8. 实现备注（编码后填写）

- 新增：`engine/score.py`、`engine/reward.py`、`training/episode_log.py`、`training/runner.py`
- 配置：`configs/score_default.json`、`configs/reward_default.json`
- 改造：`blood_battle` 接入 `ScoreService`；`session.play_random_game_logged`
- schema：**v4**（`end_settled` / `settle_tags`）
- 测试：`test_score` / `test_reward` / `test_episode_log`；全量 **74 passed**

---

## 9. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | `Review` | 首版规格，待用户确认 |
| 2026-07-10 | `Approved` | 用户确认 M05；开放问题按默认方案关闭 |
| 2026-07-10 | `Done` | 实现完成；pytest 74 passed |
