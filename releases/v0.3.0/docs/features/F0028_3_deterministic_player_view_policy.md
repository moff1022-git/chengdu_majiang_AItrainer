# F0028-3 — 基于 PlayerView v2 的确定性基础策略

| 字段 | 值 |
|------|----|
| **编号** | F0028-3 |
| **状态** | `Done`（2026-07-29） |
| **父功能** | [F0028 人类化 AI v2 实现方案](F0028_humanlike_ai_v2_implementation_plan.md) |
| **依赖** | F0028-1、F0028-2 `Done` |
| **输入版本** | CDMJ-AI-RULES 1.0.0 / PARAMS 1.0.0 / IMPL 2.0.0 |
| **协议基线** | State schema 5 / PlayerView 2 / persistence 1 / wire 1 |
| **实现门禁** | 已执行并通过验收 |

## 1. 背景与目标

F0028-1 已提供 GP/RP 配置和追踪基座，F0028-2 已建立实体牌守恒、PlayerView v2 白名单和训练真值隔离。本切片实现一个可注册、可批跑、完全确定的 `humanlike_v2` 基础玩家，用于验证规则输入、特征计算和动作选择；它不是最终的人类化认知模型。

策略只能读取 `PlayerViewV2`、`ActionRequest`、已批准配置和自己的 `RoundRuntime`。相同规范化输入必须得到相同动作与基础 trace，不依赖调用顺序、集合遍历、墙内牌、他家暗牌或训练 Oracle。

## 2. 范围

### 2.1 In Scope

- 将 `Observation.view` 中的 PlayerView v2 转为强类型只读 `DecisionContext`。
- 为换三张、定缺、出牌、响应建立确定性候选生成、特征提取、归一化评分和稳定决胜规则。
- 仅从可见牌、公开副露、弃牌、定缺、比分和墙余量建立基础 `PublicBelief`。
- 复用 `engine.shanten`、F0010/F0011 中可改造成纯 PlayerView 输入的牌效/危险思想，不调用全知分析入口。
- 注册选配 `humanlike_v2` 玩家；不替换 `rule_ai`、`current_s2` 或已有默认 profile。
- 将决策摘要写入 RP 生命周期并返回可测试的 `Decision.analysis`。
- 覆盖 2/3/4 人局；默认四座 profile 仍按 F0028-1 配置。

### 2.2 Out of Scope

- 记忆衰减、注意力 Top-K、情绪、习惯、计划惯性和跨局学习。
- 满意停止、重新搜索、有限展开树和近似方案随机选择。
- `bounded_noise`、模拟思考时长和真实 sleep；本切片固定 `bounded_noise=0`。
- F0028-5 的持久化审计格式、RNG 游标和状态 hash 回放。
- F0028-6 的固定训练动作空间、奖励塑形和多智能体训练。
- 修改规则引擎合法动作、计分、PlayerView v2 字段或 state schema。
- 使用 `TrainingTruth`、终局 Oracle、`GameState`、牌墙顺序或其他座位暗牌。

## 3. 强制边界与不变量

1. `HumanlikeV2Player` 不得定义、接收或读取 `_engine_state`；生产策略路径不得导入 `training.oracle`。
2. 策略入口不得调用接受 `GameState` 的 `analyze_for_seat`；复用分析逻辑必须拆成只接受显式可见值的纯函数。
3. 最终动作必须与 `request.legal_actions` 中某一项按 `Action.to_dict()` 完全相等，不自行构造未获授权动作。
4. request seat、PlayerView self seat 和玩家绑定 seat 必须一致；view version 必须为 2；不一致立即失败。
5. 候选、特征和 trace 均不得修改 view、request、配置或 runtime 快照。
6. 所有排序都有显式稳定键，不以集合或映射的偶然遍历顺序决胜。
7. 无合法动作、未知阶段、畸形视图或动作无法映射时明确抛出 `PolicyInputError`。

## 4. 模块设计

| 模块 | 职责 | 输出 |
|------|------|------|
| `players/humanlike/view.py` | 校验 PlayerView v2 和 ActionRequest，生成冻结上下文 | `DecisionContext` |
| `players/humanlike/hand_analyzer.py` | 向听、定缺、有效进张、结构与灵活性 | `HandFeatures` |
| `players/humanlike/belief.py` | 由本手和公开事件按 4-copy 守恒扣牌 | `PublicBelief` |
| `players/humanlike/plan.py` | 生成本决策的主/备计划标签 | `PlanSnapshot` |
| `players/humanlike/candidates.py` | 合法动作规范化、强制集分类和稳定截断 | `CandidateSet` |
| `players/humanlike/evaluator.py` | 分量归一化、加权效用和确定性选择 | `EvaluationResult` |
| `players/humanlike/player.py` | BasePlayer 生命周期、配置装配、RP 写入 | `HumanlikeV2Player` |

`engine_adapter.py` 只用于确认 GP 与引擎配置一致，不成为策略读取引擎状态的通道。

## 5. 接口与数据契约

### 5.1 DecisionContext

```python
@dataclass(frozen=True, slots=True)
class DecisionContext:
    request_id: str
    seat: int
    phase: str
    event_index: int
    view: PlayerViewV2
    legal_actions: tuple[Action, ...]
    profile: PlayerProfile
    config_hash: str
```

`build_decision_context(observation, request, *, bound_seat, profile, config_hash)` 必须从消息外壳按 PlayerView v2 白名单重建冻结对象，不得回查 GameState。

### 5.2 PublicBelief

```python
@dataclass(frozen=True, slots=True)
class PublicBelief:
    visible_counts: tuple[int, ...]       # 27 项
    unseen_counts: tuple[int, ...]        # 4 - visible
    opponent_suit_pressure: tuple[tuple[float, float, float], ...]
    danger_by_face: tuple[float, ...]     # 27 项，[0,1]
```

- 可见计数只含本家实体手牌、公开副露、弃牌及 GP-021 公开的亮牌；同一实体 ID 只计一次。
- 暗杠牌面 hidden 时只使用公开数量信息，不猜具体牌面，不从实体 ID 反推。
- 计数超出 0..4 立即失败，不截断掩盖坏输入。
- 若 F0010 函数不能剥离全知输入，本切片实现小型纯函数并保留替换点。

### 5.3 候选、强制动作与稳定键

- `mandatory`：唯一合法动作、不能过的自摸胡及配置明确要求的强制动作；不受 GP-026 上限裁剪。
- `ordinary`：其余合法动作，包括可过胡、碰杠、弃牌、换牌、定缺。
- `max_candidates` 只裁剪 ordinary；按预评分降序、稳定动作键升序截取。最终集合非空且为 legal actions 子集。

稳定动作键：`(action_type_order, suit_or_empty, sorted(tile_face_ids))`。固定动作序为 `hu, gang_an, gang_jia, gang_ming, pong, discard, exchange, dingque, pass`；它只处理完全同分，不替代效用。

### 5.4 特征、计划与评价

四个分量归一化到 `[0,1]`：

- `speed`：动作后向听改善和有效进张；有缺门牌时优先清缺。
- `hand_value`：清一色、七对、对对胡等可见结构的可达性代理，不宣称精确番值。
- `defense`：公开危险度的反向值。
- `flexibility`：对子、搭子、孤张和剩余有效牌对应的后续选择空间。

本决策计划标签固定为 `clear_dingque / fast_win / value_hand / balanced / defend`，由固定阈值和稳定优先级生成，不跨决策保存惯性。

```text
Q(a) = w_speed*speed + w_hand_value*hand_value
     + w_defense*defense + w_flexibility*flexibility
     + action_adjustment(a)
```

- 权重来自 GP-026；F0028-1 已保证和为 1。
- 离散响应修正受 profile 的碰、杠、大牌、防守倾向调节。
- 分量先 clamp；Q 量化到小数点后 8 位，按 `(Q 降序, stable_action_key 升序)` 选择。
- 本切片不消费 RNG；配置 seed 仅作 trace 上下文。

| 阶段 | 决策约束 |
|------|----------|
| exchange | 仅评价 legal EXCHANGE；先满足同花色，再优化清缺/牌效 |
| dingque | 张数少优先，其次结构价值低，最后 wan/tong/tiao |
| response | 强制 HU 先处理；其余 HU/GANG/PONG/PASS 统一评价 |
| discard | 强制 HU 先处理；GANG/DISCARD 统一评价；缺门未清时合法缺门弃牌必须优先 |

### 5.5 DecisionTrace v1（内存契约）

`Decision.analysis` 至少包含：

```json
{
  "trace_version": 1,
  "policy": "humanlike_v2_deterministic",
  "view_version": 2,
  "config_hash": "...",
  "event_index": 12,
  "phase": "discard",
  "plan": {"primary": "fast_win", "backup": "balanced"},
  "belief_summary": {"visible_total": 39},
  "candidates": [{"action": {"type": "discard", "tiles": ["wan_1"]}, "mandatory": false, "features": {"speed": 0.8, "hand_value": 0.4, "defense": 0.7, "flexibility": 0.6}, "score": 0.655}],
  "selected_action": {"type": "discard", "tiles": ["wan_1"]},
  "stop_reason": "deterministic_argmax",
  "rng_used": false
}
```

候选按实际比较顺序写出；不得包含暗牌、墙顺序或 Oracle。F0028-5 可包装持久化格式，但不得追溯改变本字段语义。

### 5.6 RP 映射

| RP | 写入内容 |
|----|----------|
| RP-014 | legal actions 与 deadline |
| RP-015 | 冻结 PlayerView 摘要/hash 输入 |
| RP-016 | PublicBelief 摘要 |
| RP-017 | HandFeatures |
| RP-018 | PlanSnapshot |
| RP-023 | CandidateSet 摘要 |
| RP-026 | EvaluationResult |
| RP-029 | 所选动作与基础 trace |

不得把 RoundRuntime 写入 GameState 或 PlayerView。

## 6. 注册、兼容与版本

- 新类型标识 `humanlike_v2`，仅增加选配入口，不改变旧 AI 默认行为。
- registry/CLI/大厅由现有权威工厂装配配置和 seat profile，不新建平行 registry。
- 旧存档不保存策略私有状态；恢复时按配置重建玩家。
- APP、state schema、persistence、wire、PlayerView 版本均不升级。
- 未知 profile 或版本组合明确失败。

## 7. 计划文件

新增：`players/humanlike/{view,hand_analyzer,belief,plan,candidates,evaluator,player}.py`，以及对应 `tests/humanlike_v2/test_*.py` 和批跑测试。

预计修改：`players/humanlike/__init__.py`、现有玩家 registry/工厂、必要的 `players/analysis/` 纯函数入口、CLI/大厅 AI 枚举，以及父规格、索引、LATEST、基线、changelog、PLAN。

不得修改 `engine/blood_battle.py` 规则行为。若必须修改引擎或 PlayerView v2 字段，停止编码，先修订并重新确认本规格。

## 8. 测试计划

### 8.1 单元与隔离

- view version、seat、phase、合法动作映射及畸形输入拒绝。
- 27 种牌面 visible/unseen 守恒；暗杠 hidden 不泄漏。
- 向听/进张固定夹具、定缺强制优先、四阶段黄金案例。
- mandatory 不被裁剪；ordinary 稳定截断；8 位量化和同分 stable key。
- trace 完整且不含哨兵私有字段。
- 同输入重复 100 次，action 与规范化 trace 完全一致。
- 改变 Oracle/暗牌/墙序但保持 PlayerView 相同，输出不变。
- 不同 `PYTHONHASHSEED` 子进程固定夹具输出一致。
- monkeypatch 全知分析/TrainingTruth 为抛错仍可决策；AST 审计无 `_engine_state`/Oracle。

### 8.2 集成、批跑与性能

- registry 可选 `humanlike_v2`，旧 AI 默认不变。
- 2/3/4 人各至少 50 局固定 seed：非法动作、异常决策、牌守恒失败均为 0。
- 同批 seed 两次 action 序列一致；全量 pytest、compileall 通过。
- 4 人 headless 单决策 p95 ≤20 ms；相对同提交 rule_ai 批跑墙钟 ≤3 倍，验收报告记录平台。

## 9. 验收标准

- [x] 仅使用 PlayerView v2、ActionRequest、配置和自身 runtime。
- [x] `humanlike_v2` 可显式注册，旧 AI 默认不变。
- [x] 输出动作均严格属于 legal actions，非法动作率 0。
- [x] 重复、跨 hash seed、双批自对弈 action/trace 复现率 100%。
- [x] 相同 PlayerView 下隐藏真值变化不改变决策。
- [x] mandatory 不受 GP-026 上限影响。
- [x] 四阶段、同分规则和 trace 泄漏测试通过，`rng_used=false`。
- [x] 2/3/4 人各 50 局通过规则、守恒、异常和性能门禁。
- [x] 全量测试与 compileall 无回归。
- [x] 验收报告及所有状态文档回写完成。

## 10. 回滚思路

`humanlike_v2` 是选配注册项；撤销注册和新模块即可回滚，旧 AI 不受影响。本切片无数据/协议迁移。纯 PlayerView 分析新入口若回归，可独立回滚并保留旧入口。

## 11. 已确认决议

| 项 | 已批准决议 |
|----|----------|
| 可过胡 | 仅不可过胡为 mandatory；可过胡参加效用比较 |
| 候选上限 | 不裁剪 mandatory，只裁剪 ordinary |
| 确定性 seed | 不消费 RNG，`rng_used=false` |
| belief 精度 | 不输出精确他手，只输出公开计数、花色压力和危险度 |
| trace 落盘 | 本切片仅内存契约；持久化归 F0028-5 |
| 版本 | 保持 PlayerView 2 / wire 1 / state 5 / persistence 1 |

以上六项已由用户于 2026-07-29 一并确认。本次确认仅开放实现门禁，没有修改业务代码。

## 12. 实现结果与差异

- 已实现 `view / belief / hand_analyzer / plan / candidates / evaluator / player` 七个策略模块，并通过现有 registry 与策略 presets 注册 `humanlike_v2`。
- orchestrator 的全知 `_engine_state` 兼容注入缩窄为仅 `RuleAIPlayer`；humanlike_v2 实例从未接收该属性。
- Observation 外壳仍是 wire 1 的 legacy mapping，因此 `view.py` 按 PlayerView v2 白名单重建冻结对象；没有升级 wire 或 PlayerView 版本。
- 原计划的多个测试文件合并为 `test_deterministic_policy.py` 与 `test_humanlike_player_integration.py`，覆盖范围不减。
- F0010/F0011 现有全知入口没有被调用；本切片使用独立、纯可见输入启发式，保留后续替换点。
- 最终全量测试 321 passed / 1 skipped；compileall 通过。
- 最终 2/3/4 人各 50 局共 150 局、23392 次决策，策略崩溃和非法动作均为 0。
- 跨 `PYTHONHASHSEED=1/777` 的三局动作摘要 SHA-256 均为 `e541199f51e9c1c3c2702555c3d7b606204176acaab6fe79d51ab1c0b9b53d2b`。
- macOS arm64 / Python 3.12.13：单决策 p95 2.87 ms；10 局四人批跑相对 RuleAI 2.222×，均通过门禁。
