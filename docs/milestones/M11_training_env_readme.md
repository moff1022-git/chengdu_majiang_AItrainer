# M11 — 训练环境（类 Gym）+ 项目 README

| 字段 | 值 |
|------|-----|
| **编号** | M11 |
| **标题** | ChengduMahjongEnv + project README |
| **状态** | `Done` |
| **依赖** | **M01–M10 Done**（引擎、Reward、JSONL、runner、存档） |
| **下一里程碑** | 无（路线图收尾）；后续可迭代 RL 算法仓库外置 |
| **对应 PLAN** | §6 训练支持、§7 Reward、`training/env.py`、§11 M11 |

---

## 1. 目标

对外提供**可训练的单智能体接口**与**完整使用文档**，收束 Docs-First 全路线图：

1. **`training/env.py`**：类 Gym API（`reset` / `step` / `legal_actions` / `close`），学习座位 vs 固定对手。  
2. **观察编码（可选轻量）**：dict 观察 + 可选扁平向量辅助（不强依赖 gym/numpy；若有 numpy 则提供 `obs_vector`）。  
3. **与 Reward / JSONL 集成**：step 返回 dense reward；episode 结束 sparse；可挂 `EpisodeLogger`。  
4. **`README.md`**：安装、规则摘要、目录、CLI、Python API、训练示例、里程碑索引。  
5. **回归与验收**：env 可跑通随机 policy 终局；文档命令可复制执行。

本步**不**实现：完整 PPO/DQN 训练循环、torch/tf 依赖、多智能体同时反传的复杂 PettingZoo 全套（可预留接口说明）。

---

## 2. 范围

### 2.1 In Scope

| 项 | 说明 |
|----|------|
| `training/env.py` | `ChengduMahjongEnv` |
| `training/spaces.py`（可选） | action 索引映射、obs keys 文档 |
| `training/runner.py` | 可选增加 env 批跑示例入口 |
| `README.md` | 项目根完整说明 |
| `requirements.txt` | 注释/可选 numpy；**不强制** gymnasium |
| 测试 | `tests/test_env.py`：reset/step/legal/done |
| docs | M11 Done + 总路线图收尾说明 |

### 2.2 Out of Scope

- 安装 gymnasium 为硬依赖（可用 duck-typed API）  
- 分布式 workers / Ray  
- 把 Human 嵌进 env.step  

---

## 3. 设计

### 3.1 环境语义

```text
学习座位 learner_seat（默认 0）
其余座位：固定对手 BasePlayer（默认 rule_ai 或 random，可配置）

一局 = 从 dealt 经 opening 到 finished
env 只在 learner 需要 Decision 时返回 observation 并等待 step(action)
对手在 learner 之间自动 decide+apply
```

**自动阶段**：`draw` 引擎自动摸；opening 换三张/定缺由对手策略或 **learner 也需 act**（定缺/换三张也进入 step）。

### 3.2 API

```python
class ChengduMahjongEnv:
    def __init__(
        self,
        *,
        learner_seat: int = 0,
        num_players: int = 4,
        opponent_spec: str = "rule_ai",  # 每个对手类型
        opponents: str | None = None,    # 完整串如 "rule_ai,random,rule_ai" 不含 learner
        reward_config: RewardConfig | None = None,
        engine_config: EngineConfig | None = None,
        log_dir: Path | None = None,
        seed: int | None = None,
    ): ...

    def reset(
        self, game_id: str | None = None, *, seed: int | None = None
    ) -> dict:
        """Start episode; advance until learner must act. Return obs dict."""

    def step(self, action: Action | dict) -> tuple[dict, float, bool, bool, dict]:
        """
        Gymnasium-style: obs, reward, terminated, truncated, info
        (若需 Gym 旧式可用 wrapper 合并 terminated|truncated → done)
        """

    def legal_actions(self) -> list[Action]: ...
    def legal_action_dicts(self) -> list[dict]: ...
    def close(self) -> None: ...

    @property
    def state(self) -> GameState: ...
    @property
    def episode_result(self) -> GameResult | None: ...
```

#### 3.2.1 Observation dict（稳定键）

```python
{
  "game_id": str,
  "seat": int,
  "phase": str,
  "view": dict,              # filter_state_for_seat 结果
  "legal_actions": [dict],   # Action.to_dict()
  "request_id": str,
}
```

可选：

```python
def encode_obs_vector(obs: dict) -> list[float]:
    # 手牌 27-dim counts + melds rough + wall_remaining + phase one-hot ...
```

无 numpy 时返回 `list[float]`；有 numpy 返回 `np.ndarray`。

#### 3.2.2 Action 输入

- `Action` 实例，或  
- `dict`（`Action.from_dict`），或  
- `int` 索引进当前 `legal_actions()`（非法 index → 抛错）

#### 3.2.3 Reward

- 在 learner 的 `step` 内：apply 后冲刷 `ScoreService` 事件，用 `RewardCalculator.on_transfers` 累加 **仅 learner 座位** 的 dense reward。  
- `terminated=True`（局结束）时加上 `on_game_end` 中 learner 分量。  
- `truncated=True`：步数上限（可选 `max_episode_steps`）。

#### 3.2.4 info 字段

```python
{
  "fan": optional,
  "score": int,              # learner current score
  "score_delta": int,        # since last step
  "phase": str,
  "result": optional dict,   # when done
  "raw_score_events": [...], # optional thin
}
```

### 3.3 内部实现要点

```text
reset:
  create_dealt_game / opponents = create_player(...) per non-learner seat
  Learner 不入 BasePlayer.decide 路径；env 外置 action
  begin_exchange → _advance_until_learner_or_done

_advance_until_learner_or_done:
  while not done:
    # opening
    if phase exchange/dingque:
      if next seat is learner and not yet submitted: yield obs
      else: opp decide → submit_exchange / submit_dingque
    # playing
    if phase draw: do_draw
    if phase discard/response and seat == learner: yield obs
    if phase discard/response and seat != learner: opp.decide + apply_action
    if phase finished: terminate
```

**与现有编排关系（重要）**：

| 现有类 | 能否直接用 | 说明 |
|--------|------------|------|
| `PlayerGameRunner.run()` | **否** | 一气呵成整局，无法在 learner 决策点暂停 |
| `InteractiveRunner.setup()` | **否** | setup 内已对**所有座位**完成换三张/定缺；与「learner 参与 opening」冲突 |
| `PlayerGameRunner` 私有方法 | **可复用思路** | `_play_seat_action` / opening decide 逻辑可内联或抽 helper；env 自建状态机循环 |
| `GameSession` | **是** | apply 后计分/reward 与 session 一致（或 env 内直接 ScoreService + RewardCalculator） |

Learner 座位在 **opening（换三张/定缺）与 playing** 均可能被询问。

对手：`create_player(opponent_spec)` 每座独立 seed；`human` **禁止**作为 env 对手。

### 3.4 与现有模块关系

| 模块 | 使用 |
|------|------|
| `engine/*` | 权威状态与规则 |
| `RewardCalculator` | step reward |
| `EpisodeLogger` | 可选 log_dir |
| `analyze_for_seat` | 不强制；可在 info 挂 analysis |
| `display` | **禁止** import |

### 3.5 示例脚本（README 内嵌）

```python
from training.env import ChengduMahjongEnv
from engine.action import Action

env = ChengduMahjongEnv(opponent_spec="random", num_players=4, seed=0)
obs = env.reset(game_id="train-demo-1")
done = False
while not done:
    legal = env.legal_actions()
    action = legal[0]  # or your policy
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
print(env.episode_result.scores)
env.close()
```

随机策略压测：

```bash
python -c "from training.env import smoke_random_episode; smoke_random_episode()"
```

### 3.6 README.md 结构

1. 项目简介（成都麻将血战 / AI 训练）  
2. 功能列表（引擎、AI、GUI、Human、存档、训练）  
3. 环境要求（Python 3.11+、pygame）  
4. 安装：`pip install -r requirements.txt`  
5. 快速开始：  
   - `python main.py train ...`  
   - `python main.py play ...`  
   - `python main.py human ...`  
   - env 代码示例  
6. 目录结构  
7. 规则要点与配置（fan_cap、crash、reward）  
8. 里程碑索引 → `docs/milestones/README.md`  
9. 开发规范 → `docs/DEVELOPMENT.md`  
10. 许可证占位（若无则写 Internal / TBD）  

### 3.7 requirements.txt

```text
pygame>=2.5
pytest>=7.0
# optional for vector obs:
# numpy>=1.24
# optional Gym API branding only — not required:
# gymnasium>=0.29
```

---

## 4. 文件清单

| 路径 | 动作 |
|------|------|
| `training/env.py` | 新增 |
| `training/spaces.py` | 可选新增 |
| `training/__init__.py` | 导出 Env |
| `README.md` | 新增/重写 |
| `tests/test_env.py` | 新增 |
| `docs/milestones/README.md` | M11 状态 |
| `docs/changelog.md` | 记录 |
| `PLAN.md` §15 | 可选标注路线图完成 |

---

## 5. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| E01 | reset 返回 obs 含 legal_actions | 非空 list 或 opening 合法 |
| E02 | random policy 至 done | terminated，有 result |
| E03 | step 非法 action | 抛错 |
| E04 | 同 game_id reset 两次 | 引擎开局可复现（dealt hands 一致若从同一点比较） |
| E05 | reward 为 float | 类型正确 |
| E06 | 不 import display/pygame 于 env 路径 | 纯逻辑（pygame 可不装时 env 仍可测——若项目已依赖 pygame 可忽略） |
| R01 | 全量回归 | 通过 |

```bash
pytest tests/ -q
python -c "from training.env import smoke_random_episode; print(smoke_random_episode())"
```

---

## 6. 验收标准

- [x] `ChengduMahjongEnv` 支持 reset/step/legal_actions 跑通一局  
- [x] 对手自动行动；learner 仅在自己决策点 step  
- [x] Reward 与 M05 配置一致可调  
- [x] README 覆盖安装与主要 CLI/API  
- [x] 全量测试通过（**114 passed**）  
- [x] 路线图 M01–M11 文档闭环  

---

## 7. 风险与开放问题

| 项 | 默认决议 |
|----|----------|
| Gym 依赖 | **不强制** gymnasium |
| API 风格 | **Gymnasium 5-tuple** step |
| 对手默认 | **rule_ai** |
| Opening | learner **参与** 换三张/定缺 step |

**开放问题 → 已确认（2026-07-10）：**

| # | 决议 |
|---|------|
| 1 | step 返回 **Gymnasium 5 元组** `(obs, reward, terminated, truncated, info)` |
| 2 | 默认对手 **`rule_ai`**（可用 `opponent_spec` / `opponents` 覆盖） |
| 3 | 根 **README 以中文为主**（CLI/API 标识符保持英文） |

---

## 8. 实现备注（编码后填写）

- 新增 `training/env.py`：`ChengduMahjongEnv`、`smoke_random_episode`、`EnvError`
- 新增 `training/spaces.py`：换三张合法枚举、`encode_obs_vector`、OBS_KEYS
- 自建 opening+play 推进循环（不用 `PlayerGameRunner.run` / `InteractiveRunner.setup`）
- 新增 `tests/test_env.py`（E01–E06 + 扩展）
- 根 `README.md` 中文；`training/__init__.py` 导出 Env
- 全量 **114 passed**

---

## 9. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | `Review` | 首版规格，待用户确认 |
| 2026-07-10 | `Approved` | 用户确认；开放问题按默认决议锁定 |
| 2026-07-10 | `Done` | 实现 env + 测试 + README；114 passed |
