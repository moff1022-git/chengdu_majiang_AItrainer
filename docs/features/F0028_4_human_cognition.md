# F0028-4 — 人类化有限认知、人格、注意力与记忆

| 字段 | 值 |
|------|----|
| **编号** | F0028-4 |
| **状态** | `Done`（2026-07-29） |
| **父功能** | [F0028 人类化 AI v2 实现方案](F0028_humanlike_ai_v2_implementation_plan.md) |
| **依赖** | F0028-1–3 `Done`；Human 换三张人工阻塞已清零 |
| **输入版本** | CDMJ-AI-RULES 1.0.0 / PARAMS 1.0.0 / IMPL 2.0.0 |
| **协议基线** | State schema 5 / PlayerView 2 / persistence 1 / wire 1 |
| **实现授权** | 已执行并通过验收 |

## 1. 目标

在 F0028-3 的合法、只读 PlayerView v2、确定性评分策略之上，实现规则第 13–14 章要求的持续玩家差异：人格与水平修正、有限注意力、按可见事件步数衰减的记忆、计划惯性与重启、认知顺序检查、满意停止、近似方案内的有界扰动，以及可复现但不真实等待的思考时长。

“人类化”只能产生可解释的合法次优选择，不能制造规则错误、隐藏信息泄漏或不可回放随机。相同 PlayerView 序列、配置、game_id、seat 与决策序号必须得到相同认知状态、动作、思考时间和 trace。

## 2. 范围

### 2.1 In Scope

- `CognitiveState`：当前/备选计划、计划惯性、决策序号、RNG 游标、情绪、注意力、局内记忆和公开对手模糊印象。
- `MemoryStore`：只摄取 PlayerView 可见事实；按事件步数衰减、显著事件强化、遗忘后不无因恢复精确内容。
- `AttentionSelector`：全部可见对象显著度 → 稳定 Top-K → Top-K 内 softmax。
- 人格/水平：由既有 `PlayerProfile` 与 GP-024/025/026 调整容量、停止阈值、计划惯性、响应偏好、防守和误差上限。
- `CognitivePolicy`：按人类显著顺序检查候选，满意即停止；未满足时选择已检查最佳。
- `BoundedNoise`：仅在与认知选择基准分差不超过近似阈值的合法 ordinary 候选内扰动。
- `ThinkTimeModel`：输出 0..`GP-022.max_performance_delay_ms` 的可复现模型值，仅进入 trace/RP，不调用 sleep。
- 局间保留有限条公开行为印象；新局清除具体牌张、注意力和局内计划。

### 2.2 Out of Scope

- F0028-5 持久化审计格式、state/view hash 链、独立 replay reader。
- F0028-6 训练动作编码、奖励塑形、自博弈接口。
- 真实墙钟计时、系统调度耗时或 UI sleep。
- 读取 `GameState`、TrainingTruth、Oracle、他家暗牌、墙顺序或未公开终局牌。
- 修改规则引擎合法动作、计分、state schema、PlayerView、persistence 或 wire 版本。
- 为模拟失误执行非法动作、越过缺门强制、忽略 mandatory、完全随机出牌或跨轮剧烈改变人格。

## 3. 不变量

1. 最终动作严格等于 `request.legal_actions` 中一项；所有认知裁剪只作用于 legal ordinary。
2. mandatory 集完整保留。唯一 mandatory 直接执行，`stop_reason=mandatory`，不消费 RNG。
3. 所有认知输入来自 `DecisionContext`、配置和该策略过去实际收到的 PlayerView；不得回查引擎真值。
4. RNG 使用 SHA-256 派生，不使用 Python `hash()`、系统时间、进程 ID 或全局 random 状态。
5. 已遗忘事实在没有相同公开 token 再次出现时不能恢复 `exact=true`。
6. Top-K 之前计算全体显著度；Top-K 之后才 softmax。容量外事实仍可留在记忆，不伪装成从未发生。
7. 噪声只在近似方案集合内改变选择，且幅度不超过 GP-025 限制；明显分差顺序不可翻转。
8. 决策 trace 只含公开事实摘要和认知派生值，不含原始暗牌、墙顺序或跨座私有状态。

## 4. 数据模型

### 4.1 MemoryItem / MemorySnapshot

```python
MemoryItem(key, category, summary, first_seen_step, last_seen_step,
           strength, salience, exact, reinforcements)
```

- `key` 由公开 token 稳定构造，例如 `discard:S2:tong_5:17`、`meld:S1:pong:wan_3`、`status:S3:finished`。
- 每次决策先令 `delta=max(0, event_index-last_update_step)`，按
  `strength *= exp(-forget_rate * delta)` 衰减。
- 本次仍可见或新出现 token 使用
  `strength = clip(strength + salience_boost * salience, 0, 1)` 强化。
- `strength < 0.25` 时 `exact=false`；条目可保留模糊类别/计数，不保留精确座位与时点。只有新的公开 token 才能重新成为精确记忆。
- 容量为 `max(8, attention_capacity*4)`；超限按 `(strength, last_seen_step, key)` 稳定淘汰。

### 4.2 AttentionFocus

注意对象包括 mandatory 提示、当前合法动作牌面、最近公开事件、对手状态/副露、当前计划关键牌和记忆摘要。显著度由以下确定项组成并 clamp 到 `[0,4]`：

- mandatory 4.0；当前缺门/胡杠碰提示 3.0；最近事件 2.0；主要威胁 1.5；计划相关 1.2；普通旧事实 `memory_strength`。
- profile 的 `defense_awareness`、`big_hand_preference` 与 level 只作有界乘数 `[0.75,1.25]`。
- 按 `(-salience, stable_key)` 取 `attention_capacity`；仅入选项用温度 1 的稳定 softmax，权重和量化后允许 `1±1e-8`。

### 4.3 CognitiveState

```python
CognitiveState(game_id, decision_index, rng_index, memory,
               attention, primary_plan, backup_plan,
               plan_age, emotion, opponent_impressions)
```

- 新 `game_id`：清空具体牌张记忆、注意力、计划和情绪；保留最多 GP-024.cross_round_history 条公开行为聚合印象。
- 同局决策：计划若未触发重启则按 `profile.plan_persistence` 提高认知顺序；关键进张、听牌状态/阶段变化、公开碰杠胡、主计划变化或分数压力变化触发重启。
- 情绪是 `[-1,1]` 的轻度派生值，只由 PlayerView 公开比分/近期公开得失更新，再乘 `(1-emotional_stability)`；不读取隐藏结算原因。

## 5. 认知决策算法

### 5.1 人格与水平参数

既有 profile 不新增配置字段。level 映射固定为：

| level | 候选容量系数 | 满意阈值修正 | 注意容量系数 | 噪声系数 |
|-------|--------------|--------------|--------------|----------|
| novice | 0.55 | -0.15 | 0.60 | 1.00 |
| normal | 0.75 | -0.05 | 0.80 | 0.70 |
| skilled | 0.90 | 0.00 | 0.95 | 0.40 |
| expert | 1.00 | +0.05 | 1.00 | 0.20 |

style 修正：conservative 提前接受稳定/防守方案，aggressive 延后停止并提高 hand_value，balanced 不修正。最终阈值 clamp `[0.45,0.95]`。

### 5.2 候选认知顺序与满意停止

1. mandatory 按稳定动作键在最前；唯一 mandatory 直接返回。
2. ordinary 先按“上一计划一致 → 行动显著度 → 原始 Q → stable key”排序。
3. 实际检查数量由 level 容量系数和 GP-026 min/max 决定，保持确定，不随机增减。
4. 每检查一项，将 Q 映射为 `satisfaction=clip((Q+0.25)/1.5,0,1)`；若达到阈值立即停止。
5. 未停止则从已检查集合取最高原始 Q；未检查候选不能被选中。
6. 简单局面允许早停；存在多个高价值响应、后期高风险或计划重启时至少检查 `min_candidates`。

### 5.3 计划惯性与重启

- `choose_plan()` 的新计划与上一计划一致时增加 `plan_age`。
- 无重启事件且候选与上一计划一致时，认知排序获得最多 `0.04*plan_persistence` 的显著加成，不直接修改规则 Q。
- phase 改变、last_public_event 改变、主要计划改变、公开玩家状态改变或最高两项 Q 差小于 research threshold 时扩大到正常检查容量。
- 惯性不能覆盖缺门、mandatory、听牌破坏或超过 near-equivalent 范围的明显分差。

### 5.4 有界噪声与稳定 RNG

派生材料：

```text
SHA256(config_seed, GP-025.random_seed, game_id, seat,
       event_index, decision_index, rng_index, purpose)
```

取前 64 bit 映射到 `[0,1)`。每次实际取样递增 `rng_index`；未发生近似选择时 `rng_used=false`。

- 近似阈值 `near_threshold = 0.05 * GP-025.near_equal_randomness`。
- 仅从已检查 ordinary 且与基准分差 `<= near_threshold` 的集合采样。
- 各项权重为 `exp((Q-bestQ)/temperature)`，temperature 至少 `0.005`；人格偏好只施加 `[0.9,1.1]` 乘数。
- 实际扰动概率不超过 `max_error_probability * level_noise_factor`；否则保留认知基准。
- mandatory、单候选、非近似候选不消费 RNG。

### 5.5 思考时间

模型值由阶段基数、检查候选数、计划重启、分差接近度和 `thinking_speed` 得出，再加一份独立稳定抖动；clamp 到 `0..max_performance_delay_ms`。只写入 `think_time_ms` 和 RP-027，不 sleep，不影响 deadline 合法性。

## 6. 模块与接口

新增：

- `players/humanlike/memory.py`：公开 token 提取、衰减、强化、模糊化与容量管理。
- `players/humanlike/attention.py`：显著度、稳定 Top-K、softmax。
- `players/humanlike/cognition.py`：CognitiveState、人格参数、计划惯性/重启、跨局公开印象。
- `players/humanlike/policy.py`：稳定 RNG、满意停止、有界近似选择、思考时间和认知 trace。

修改：

- `evaluator.py` 暴露完整稳定评分，不在内部提前确定最终认知动作；保留 F0028-3 确定性评价兼容。
- `player.py` 在 observe/decide 生命周期更新 CognitiveState，调用认知 policy，并写 RP-024/025/027/028/029。
- `__init__.py` 导出必要公共类型；不修改 engine、protocol schema 或旧 AI。

## 7. Trace v2 与 RP 映射

Decision.analysis 升为内存 `trace_version=2`，保留 v1 字段并新增：

```json
{
  "policy": "humanlike_v2_cognitive",
  "memory": {"exact": 5, "fuzzy": 2, "forgotten": 1},
  "attention": [{"key": "...", "weight": 0.61}],
  "cognitive_order": [0, 2, 1],
  "checked_count": 2,
  "satisfaction_threshold": 0.67,
  "stop_reason": "satisficing|best_checked|mandatory",
  "rng_used": true,
  "rng_index_before": 3,
  "rng_index_after": 4,
  "noise_pool_size": 2,
  "think_time_ms": 184,
  "plan_restarted": false
}
```

| RP | F0028-4 写入 |
|----|---------------|
| RP-024 | 记忆摘要与公开跨局印象摘要 |
| RP-025 | AttentionFocus Top-K |
| RP-026 | 认知选择、检查集合、满意度和噪声摘要 |
| RP-027 | 模型思考时间、deadline、是否时间压力 |
| RP-028 | 人格、情绪、计划惯性与重启原因 |
| RP-029 | 完整内存 DecisionTrace v2 |

## 8. 测试与验收

### 8.1 单元/隔离

- 记忆按事件步数单调衰减；强化、模糊化、容量淘汰稳定；无提示不恢复 exact。
- 注意力严格先 Top-K 后 softmax；稳定同分键；权重和与容量门禁。
- 四 level 的候选容量、停止阈值和噪声上限符合表格；style 修正方向正确。
- 满意停止只检查认知顺序前缀；未触发时选 checked best；mandatory 零 RNG。
- 噪声不跨近似阈值、不越 legal、不覆盖 mandatory；同 seed 100% 重现，不同 seed 在允许池内产生差异。
- 计划惯性仅影响近似排序；关键事件触发重启。
- 思考时间有界、可复现且测试不 sleep。
- trace v2 完整、可规范 JSON、无私有哨兵；隐藏真值变化不改变输出。

### 8.2 集成/批跑/性能

- 同 PlayerView 序列双跑 action + cognitive trace 复现率 100%；跨 `PYTHONHASHSEED` 一致。
- 2/3/4 人各至少 50 局：非法动作、策略异常、牌守恒失败均为 0。
- profile 固定夹具体现可解释差异；不要求每个 seed 动作必不同，要求阈值/容量/偏好/噪声统计方向成立。
- 全量 pytest、compileall 通过；单决策 p95 ≤25 ms；四人批跑相对 RuleAI ≤3.5×。

## 9. 兼容、回滚与风险

- APP 0.2.1、state 5、PlayerView 2、persistence 1、wire 1 均不升级。
- `humanlike_v2` 仍为显式选配；删除四个认知模块并恢复 player/evaluator 接线即可回到 F0028-3。
- CognitiveState 不进入 GameState/存档；进程中断后认知状态不可恢复，完整持久化归 F0028-5。
- 当前 Observation 的 `event_index` 投影自 turn_index，多个同 turn 公开事件可能合并为一个认知步；本切片用公开快照 token 差异补强，协议级事件序列留待后续版本。
- 2/3 人模式仍使用 seat 对应的四座 profile 子集，不改变默认四人语义。

## 10. 确认记录

用户于 2026-07-29 指令“编写、确认并实现 F0028-4……全程自动实现，无需我的干预”，并补充“中途的所有授权，全部同意”。据此本规格在落盘时直接标记 `Approved`，实现门禁开放；授权不包含远端推送、破坏性删除或范围外协议升级。

## 11. 实现结果

- 已新增 `memory.py`、`attention.py`、`cognition.py`、`policy.py`，并接入 `HumanlikeV2Player` 与 RP-024–029。
- DecisionTrace 升为内存 v2；F0028-3 evaluator 的完整稳定评分保留为认知层输入。
- 记忆、注意力、满意停止、计划惯性、人格/情绪、有界 RNG 与思考时间均按本规格实现。
- 定向 52 passed；全量 332 passed / 1 skipped；2/3/4 人各 50 局零崩溃/非法动作。
- 双跑与跨 PYTHONHASHSEED 动作摘要一致；单决策 p95 1.1968 ms；相对 RuleAI 2.50×。
- 详细证据见 `docs/status/F0028_4_ACCEPTANCE_2026-07-29.md`。
