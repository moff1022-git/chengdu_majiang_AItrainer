# F0028-6 — 训练动作空间、观测、奖励与回归评估契约

| 字段 | 值 |
|------|----|
| **编号** | F0028-6 |
| **状态** | `Approved`（2026-07-29，用户授权编写、确认并实现） |
| **父功能** | [F0028 人类化 AI v2 实现方案](F0028_humanlike_ai_v2_implementation_plan.md) |
| **依赖** | F0028-1–5 `Done` |
| **输入版本** | CDMJ-AI-RULES 1.0.0 / PARAMS 1.0.0 / IMPL 2.0.0 |
| **基线** | APP 0.2.1 / state 5 / PlayerView 2 / persistence 1 / wire 1 / Audit 1 |
| **实现授权** | 已开放；本文件提交后自动编码 |

## 1. 目标

在现有单智能体 `ChengduMahjongEnv` 上新增版本化训练契约 v2：固定整数动作索引和等长 legal mask、完全由 PlayerView 构造的结构化观测块、显式非法动作处理、可选势能塑形与真实得分分离，以及可跨批次比较的训练回归指标。

本切片完成 F0028 六个工程切片，不引入具体强化学习框架，不复制规则引擎，不把训练 oracle 拼入策略观测。

## 2. 兼容策略

- `ChengduMahjongEnv(contract_version=1)` 保持现有默认：整数是当前 legal actions 列表下标，旧 observation keys 和 reward 行为不变。
- 显式 `contract_version=2` 启用固定 codec、mask、Observation v2、非法动作策略、奖励分解和 episode metrics。
- 旧 `encode_obs_vector()` 保留；新增 `encode_observation_v2()`，不静默改变已有模型输入长度。
- APP/state/PlayerView/persistence/wire 不升级；新增 `TRAINING_CONTRACT_VERSION=2` 和 `ACTION_CODEC_VERSION=2`。

## 3. 固定动作空间 v2

### 3.1 索引布局

| 区间 | 动作 | 数量 |
|------|------|------|
| 0 | PASS | 1 |
| 1 | HU | 1 |
| 2–28 | PONG(face) | 27 |
| 29–55 | MING_GANG(face) | 27 |
| 56–82 | AN_GANG(face) | 27 |
| 83–109 | BU_GANG(face) | 27 |
| 110–136 | DISCARD(face) | 27 |
| 137–631 | EXCHANGE(face_a, face_b, face_c) | 495 |
| 632–634 | DINGQUE(wan/tong/tiao) | 3 |

总长 `ACTION_SPACE_SIZE=635`。EXCHANGE 只编码同花色 1–9 的三张有放回多重组合；每门 `C(9+3-1,3)=165`，按 suit 顺序和 face tuple 字典序稳定排列。实体牌副本不进入动作索引。

### 3.2 Codec 契约

- `encode_action(Action) -> int`；`decode_action(index) -> Action`，所有合法结构 roundtrip。
- `legal_action_mask(actions) -> tuple[int,...]` 长度固定 635，值仅 0/1。
- 同一 face action 映射唯一；非法结构、混花交换、索引越界明确抛 `ActionCodecError`。
- mask 中每个 1 必须可 decode 且对应当前 legal action；当前 legal action 全部被 mask 覆盖。

## 4. Observation v2

`encode_observation_v2(filtered_obs, action_mask, cognitive=None)` 只读取 PlayerView/legacy 兼容投影的白名单字段，输出：

```text
observation_version = 2
hand_counts[27]
own_melds[]
dingque_one_hot[4][4]        # unknown/wan/tong/tiao
discard_counts[4][27]
discard_sequence[]           # seat, face index, claimed marker
public_melds[]
active_seats[4]
current_seat_one_hot[4]
dealer_seat_one_hot[4]
wall = {visibility, exact, lower, upper}
scores[4]                    # clip(score/100, -10, 10)
phase_one_hot[8]
action_mask[635]
cognitive?                   # 显式 opt-in，只接受策略自身摘要
```

- 2/3 人缺失座位用零向量/status absent，不改变形状。
- 不输出 `physical_hand`、他家 hand/revealed hidden、墙顺序、TrainingTruth 或 GameState。
- cognitive 默认关闭；开启时只允许 plan、memory counts、attention weights、emotion 和 RNG index 等自身 trace 摘要。
- 提供扁平数值向量入口；可变长 sequence/meld 块使用聚合计数进入 flat 版本，原结构仍保留供序列模型使用。

## 5. Env v2 非法动作与 step

新增 `TrainingContractConfig`：

```python
contract_version: 1 | 2
illegal_action_mode: "raise" | "terminate"
illegal_action_penalty: float <= 0
shaping_enabled: bool
shaping_gamma: 0..1
shaping_weights: shanten/live/dingque/risk
include_cognitive: bool
```

- v2 的整数始终由固定 codec decode；不再解释为 legal 列表位置。
- `raise`：生产/调试模式抛 `EnvError`，状态不变。
- `terminate`：RL 模式记录 `illegal_action=true`，返回配置负奖励并终止 episode；不得映射或自动重采样。
- dict/Action 输入仍支持，但必须通过 current legal mask 校验。
- observation 同时保留可读 `legal_actions`，权威机器接口为 `action_mask`。

## 6. 奖励 v2

每步返回：

```text
reward = base_reward + shaping_reward + illegal_penalty
info.base_reward
info.shaping_reward
info.illegal_penalty
info.true_score_delta
info.true_score
info.unshaped_episode_reward
info.shaped_episode_reward
```

- `base_reward` 沿用 RewardCalculator，保持旧训练语义。
- `true_score_delta`/`true_score` 直接来自引擎玩家分数，始终单独报告，不与 shaping 混淆。
- potential 只使用 learner PlayerView：标准/七对最小向听的归一化反值、公开可见等待代理、缺门清理进度、公开危险代理。
- `shaping_reward = gamma*potential(next_view)-potential(current_view)`；terminal potential 为 0。
- 默认 `shaping_enabled=false`，因此 v2 默认 reward 与 base reward 一致。
- 不单独奖励 PONG/GANG，不读取隐藏牌计算 shaping。

## 7. 回归指标 v2

`EpisodeMetricsV2` 至少输出：

- illegal_action_count/rate；hidden_leak_count；conservation_failure_count；
- true_score、rank、first_hu、hu、hua_zhu、no_ting；
- fan_total/average、pong/gang/pass_hu 计数与率；
- learner_steps、base/shaping/combined reward；finished_reason。

`TrainingMetricsAggregator` 聚合多 episode，固定字段和稳定排序，报告首胡率、胡牌率、花猪率、未叫率、平均番、碰/杠/过胡率、真实平均分、非法/泄漏/守恒率与复现摘要。指标只读结果、公开动作历史和引擎断言结果，不进入策略观测。

## 8. 文件与接口

新增：

- `training/action_codec_v2.py`
- `training/observations_v2.py`
- `training/reward_v2.py`
- `training/metrics_v2.py`
- `tests/humanlike_v2/test_training_contract_v2.py`

修改：

- `training/env.py`：显式 v2 参数、固定 index/mask、非法终止、reward 分解和 metrics。
- `training/__init__.py`、`training/spaces.py`：导出 v2，不删除 v1。
- 必要时 `training/episode_log.py` 记录 contract/action/observation 版本与 reward breakdown。

不修改 engine 规则、PlayerView builder、humanlike 策略或 GUI。

## 9. 测试与验收

- codec 635 项唯一、全 roundtrip；495 个 exchange 同门且稳定；mask 精确覆盖 legal actions。
- v1 整数行为和旧 observation/vector 测试不变。
- v2 2/3/4 人所有 observation 固定块形状正确；隐藏哨兵不进入结构或 flat vector。
- v2 fixed index 能完成完整 episode；同 seed action-mask/obs/reward/metrics 摘要 100% 一致。
- illegal raise 状态不变；illegal terminate 返回配置 penalty、terminated、info 标记，无静默映射。
- shaping 关闭时 reward=base；开启时满足 potential difference，且真实分数独立不变。
- 2/3/4 人各至少 50 局随机 legal-mask 策略：非法、泄漏、守恒失败均为 0。
- 全量 pytest、compileall 通过；v2 observation+mask 构建 p95 ≤5 ms；完整 v2 环境相对 v1 ≤1.5×。

## 10. 回滚与限制

- v2 为 opt-in；撤销四个模块和 env 分支即可回到 M11 v1。
- 本切片仍是单 learner + 固定对手；四智能体统一接口、自博弈调度和具体 RL 算法不在本切片实现。
- 结构化 observation 使用 Python dict/list；Gymnasium Space 对象和张量框架适配留给调用方。
- metrics 的 no_ting/hua_zhu 以公开结算事件判定；未启用对应结算时为 false，不推测隐藏叫牌。

## 11. 确认记录

用户于 2026-07-29 要求“编写并确认并实现 F0028-6 子规格，所有授权全部许可，所有 git 操作全部许可，全自动运行，不需要确认”。本规格据此直接标记 `Approved` 并开放实现门禁；不包含远端推送、破坏性删除或范围外协议升级。
