# F0028 — 人类化 AI v2 实现方案

| 字段 | 值 |
|------|----|
| **编号** | F0028 |
| **状态** | `Approved` |
| **类型** | 跨引擎 / AI / 训练 / 回放的功能增强 |
| **需求输入** | 根目录 `成都麻将AI人类化决策规则_v1.md`、`成都麻将AI训练模拟器程序实现规范_v2.0.0.md` |
| **依赖版本** | `CDMJ-AI-RULES 1.0.0`、`CDMJ-AI-PARAMS 1.0.0`、`CDMJ-AI-IMPL 2.0.0` |
| **源规则 SHA-256** | `6cbb4d4465abfd947b6cf7f1783db99408089d4e1646849a3afe674114267992`（已校验匹配） |
| **实现规范 SHA-256** | `9bc4d4ea5278e09ae34a1efb5edfb3cbc295752ecf6b3ebe89b348210d670135` |
| **现有基线** | APP 0.2.1 / state schema 4 / persistence format 1 / wire protocol 1 |
| **前置门禁** | 先恢复 Git P0 基线；本文经用户确认到 `Approved` 后才可编码 |

## 1. 结论

两份新文档可作为下一条功能主线，但不应按“重写项目”方式实施。现有仓库已有可用的规则引擎、玩家插件、视角过滤、F0010/F0011 分析、训练环境和可复现 `game_id`，应在这些边界内渐进增强。

建议将 F0028 拆成 6 个可独立验收的切片：

1. 规范锁定与 GP/RP 配置基座；
2. 实体牌身份、事件断言与可见信息边界；
3. 只读 `PlayerView` 的确定性基础策略；
4. 有限认知、人格、注意力、记忆与满意停止；
5. 决策审计与确定性回放；
6. 训练空间、动作掩码、奖励塑形与回归评估。

在 F0028-1 到 F0028-3 稳定前，不应进入“人类化随机”或强化学习，否则无法区分规则错误、信息泄漏与策略扰动。

## 2. 与现有项目的差距

| 领域 | 现有能力 | 新规范要求 | 判定 |
|------|----------|------------|------|
| 规则引擎 | 换三张、定缺、碰杠胡、血战、计分已实现 | 完整 GP-001–GP-027 配置驱动与追踪 | 部分具备，需配置扩展；不重写引擎 |
| 牌模型 | `Tile` 表示 27 种牌面，4 张同面牌无实体 ID | `tile_id=tile_type*4+copy_index` 与 108 张唯一性 | 缺口较大，需兼容迁移 |
| 状态 | `GameState` schema 4，实现牌局与计分事件 | GP/RP、分层账本、pass-hu、认知状态、事件索引 | 部分具备，不应把 AI 私有记忆放入引擎权威状态 |
| 信息隔离 | `filter_state_for_seat` 隐藏他家手牌与牌墙 | 可配置 `PlayerViewBuilder`、泄漏审计 | 基础已有，需强类型、白名单化和自动审计 |
| 现有 RuleAI | 胡/杠/碰固定优先，出牌用向听或 F0011 | 有限候选、计划、对手信念、注意/记忆、满意停止、有界扰动 | 仅是基础策略，缺人类化认知层 |
| F0010/F0011 | 对手预测、进张、危险、综合弃牌已实现 | 作为 belief/threat/feature 输入 | 高价值复用，需去除直接依赖全知 `GameState` 的生产策略路径 |
| 回放 | 快照 + 决策 JSONL | 事件前后 hash、view hash、config hash、RNG 位置、决策 trace | 不足，尚不能验证完整确定性 |
| 训练 | 单座 learner env、轻量观测向量、奖励结算 | 结构化动作、固定 mask、势能塑形、多智能体/自博弈、评估指标 | 基础已有，需分阶段扩展 |
| 人数 | 现有规格支持 2/3/4 人，F0020 支持 1–3 human | 新规则文档默认四人 | 保留现有能力；新 v2 默认只为 4 人 profile，不删除 2/3 人 |

## 3. 兼容与架构决议

### 3.1 保留现有目录和权威边界

- 不采用新规范中的独立 `src/` 示例树，以免复制第二套引擎。
- `engine/` 继续是规则和真实状态权威。
- `protocols/` 负责 PlayerView / action / wire schema。
- `players/analysis/` 复用为手牌、对手、危险和计划特征层。
- 新建 `players/humanlike/` 作为人类化认知策略，不把记忆/情绪写入 `engine/`。
- `training/` 继续包装同一引擎，不复制规则逻辑。

### 3.2 新功能默认为显式 profile

新增 `humanlike_v2` 玩家类型/策略 profile。在完成回归验证前，不直接替换 `rule_ai` 或 `current_s2`，以保留现有比较基线和回滚路径。

### 3.3 版本线分离

- APP SemVer 仍只由 `version.py` 管理。
- `CDMJ-AI-RULES` / `PARAMS` / `IMPL` 作为策略规范版本，不等同于 APP 版本。
- state schema、persistence format、wire protocol 仅在实际字段不兼容变更时单独升级。

### 3.4 规则与认知状态分离

`GameState` 不保存“AI 以为什么”。对手信念、记忆、注意、计划、情绪属于某个策略实例的 `CognitiveState`；需要确定性回放时，以独立策略快照/日志存储。

## 4. 分阶段实施

### F0028-1：规范锁定与 GP/RP 配置基座

**目标**：先把新文档变成可校验、可追踪、不会静默漂移的工程输入。

**计划路径**：

- `configs/humanlike_v2/default.json`：完整 GP-001–GP-027 默认配置与四个玩家 profile。
- `players/humanlike/config.py`：强类型 `GlobalParameters`、`PlayerProfile`、范围/枚举/权重校验。
- `players/humanlike/runtime.py`：RP-001–RP-033 的初始化、生命周期和更新入口。
- `players/humanlike/traceability.py`：`parameter_id -> schema_path -> consumer -> tests` 机械可查映射。
- `configs/humanlike_v2/compatibility.json`：支持的 RULES/PARAMS/IMPL 组合。

**验收**：27 个 GP 与 33 个 RP 无缺失、无重号；非法范围/未知版本/权重不归一明确失败；配置规范化后 hash 稳定。

### F0028-2：实体牌、事件断言与 PlayerView v2

**目标**：建立规范所需的 108 张实体牌守恒和可验证信息隔离。

**设计**：

- 保留 `Tile(suit, rank)` 作为牌面值对象，新增内部 `PhysicalTile(id, face)` 或等价 ID 层。
- 引擎位置使用实体 ID；现有 AI/UI 边界仍可投影为 `wan_1` 等牌面 ID。
- 为 schema 4 读档提供确定的 copy index 补全迁移；新写入格式是否升 schema/format 在实现前单独确认。
- 将 `protocols/view_filter.py` 从“先 `state.to_dict()` 再删字段”改为显式白名单 `PlayerViewBuilder`，避免新私有字段意外泄漏。
- 实现 GP-021 可见性选项：牌墙精确/区间、暗杠、胡后亮牌、换牌方向、思考时间。
- 每个引擎原子事件后执行牌张守恒、状态机、账本与合法动作断言。

**验收**：108 个实体 ID 唯一且每张只在一个位置；各牌面总数始终 4；泄漏检查为 0；老存档迁移可重复。

### F0028-3：只读 PlayerView 的确定性基础策略

**目标**：先建立不带认知噪声的 v2 策略，使规则、特征和行为可回归。

**计划路径**：

- `players/humanlike/view.py`：强类型 `PlayerView`、`DecisionContext`。
- `players/humanlike/hand_analyzer.py`：复用 `engine.shanten` 和 F0011 进张/牌效。
- `players/humanlike/belief.py`：由可见牌、弃牌、副露、定缺生成主观分布，复用 F0010 思路，禁止 oracle 参与策略。
- `players/humanlike/plan.py`：主计划/备选计划、速胡/牌型/防守/比分效用。
- `players/humanlike/candidates.py`：强制动作不受 GP-026 候选上限影响。
- `players/humanlike/evaluator.py`：实现规范 Q(action) 归一化评价，该阶段 `bounded_noise=0`。
- `players/humanlike/player.py`：新增 `humanlike_v2` profile，继续通过 `BasePlayer` / `ActionRequest` 接入。

**强制改造**：当前 `RuleAIPlayer` 可从 `_engine_state` 调用 `analyze_for_seat(GameState, ...)`；`humanlike_v2` 不得使用此通道。F0010/F0011 要复用时，必须增加仅接受 `PlayerView` 的入口。

**验收**：全部选择均在 legal mask 中；同一视图+配置+种子输出相同 action/trace；批量自博弈非法动作率 0。

### F0028-4：人类化有限认知

**目标**：在确定性基础策略上增加规则文档第 13–14 章的人类差异，而不制造非法动作或全知信息。

**组件**：

- `CognitiveState`：主/备计划、计划惯性、对手模型、记忆、注意力、情绪与跨局模糊印象。
- `MemoryStore`：按可见事件步数衰减，已遗忘精确信息不得无因恢复。
- `AttentionSelector`：先显著度 Top-K，再在 Top-K 内 softmax。
- `CandidateSearch`：候选容量、有限展开深度、计划惯性和重启搜索。
- `SatisficingPolicy`：按认知顺序检查，达阈值立即停止；未达阈值才选已检查最佳。
- `BoundedNoise`：仅在近似方案内扰动；种子从 game_id / seat / round / decision index 派生。
- `ThinkTimeModel`：输出可复现思考时间；测试/训练可不真实 sleep。

**验收**：不同 profile 在固定案例中形成可稳定解释的行为分布差异；同种子复现率 100%；扰动不越过合法性与强制动作。

### F0028-5：审计日志与确定性回放

**目标**：能回答“AI 当时看到什么、想了什么、为何停止、用了哪个随机位置”。

**改造**：

- 扩展 `engine/replay.py` 的快照回放为事件/决策审计格式。
- 日志包含 config hash、state before/after hash、PlayerView hash、legal actions、候选与评分、停止理由、RNG stream/index、最终 action。
- 公开事件与私有诊断分开写入；策略输入字段不得包含终局 oracle。
- 定义 replay/audit 格式版本与兼容读取策略。

**验收**：从初始种子+配置+事件重放得到相同状态 hash、动作和结算；历史 PlayerView 不因终局信息被覆写。

### F0028-6：训练空间与回归评估

**目标**：在现有 `ChengduMahjongEnv` 上建立稳定、可版本化的训练契约。

**改造**：

- 定义固定动作索引：PASS/HU/PONG/GANG/DISCARD/EXCHANGE/DINGQUE，并生成等长 legal mask。
- 扩展观测为版本化块：手牌、副露、定缺、弃牌序列、活跃玩家、牌墙可见性、过胡、比分、内部认知状态（可选）。
- 非法动作不静默映射；生产模式报错，RL 模式按配置惩罚+重采样或终止。
- 奖励以真实结算为主，势能塑形仅使用 PlayerView 可得特征；同时报告未塑形真实得分。
- 优先完成单智能体固定对手，然后才扩展四智能体自博弈和离线回放训练。

**验收指标**：非法动作率 0、泄漏率 0、牌守恒失败率 0、同种子 trace 复现率 100%，并报告首胡率/胡牌率/花猪率/未叫率/番数/碰杠过胡率和 profile 差异。

## 5. 预计文件清单

### 5.1 新增

- `configs/humanlike_v2/default.json`
- `configs/humanlike_v2/compatibility.json`
- `players/humanlike/__init__.py`
- `players/humanlike/config.py`
- `players/humanlike/runtime.py`
- `players/humanlike/view.py`
- `players/humanlike/hand_analyzer.py`
- `players/humanlike/belief.py`
- `players/humanlike/plan.py`
- `players/humanlike/candidates.py`
- `players/humanlike/evaluator.py`
- `players/humanlike/memory.py`
- `players/humanlike/attention.py`
- `players/humanlike/policy.py`
- `players/humanlike/player.py`
- `players/humanlike/trace.py`
- `protocols/player_view_v2.py`
- `training/action_codec_v2.py`
- `training/observations_v2.py`
- `training/metrics_v2.py`
- `tests/humanlike_v2/` 分阶段测试集

### 5.2 预计修改

- `engine/tile.py`、`engine/deck.py`、`engine/state.py`、`engine/persistence.py`
- `engine/events.py`、`engine/legal.py`、`engine/blood_battle.py`、`engine/score.py`
- `protocols/view_filter.py`、`protocols/messages.py`、`protocols/wire.py`
- `players/registry.py`、`players/analysis/*`、`configs/strategies/presets.json`
- `engine/replay.py`、`training/env.py`、`training/spaces.py`、`training/episode_log.py`、`training/runner.py`

具体修改路径在每个切片实施前的子规格中锁定，不授权一次性修改上述全部文件。

## 6. 测试与验收策略

| 类型 | 必须覆盖 |
|------|----------|
| 单元测试 | GP/RP 校验、实体牌、视图白名单、特征、候选、满意停止、记忆衰减、动作编码 |
| 规则回归 | 换三张、定缺、碰/明暗补杠、抢杠胡、一炮多响、过胡、三家胡、流局、花猪/查叫/退税/呼叫转移/封顶 |
| 属性测试 | 108 张守恒、同牌面 4 张、选择属于 legal mask、无泄漏、同种子同 trace |
| 对照测试 | 规则文档第 0–18 章案例；不同 profile 使用“允许行为集”而非强制唯一动作 |
| 批量测试 | 固定 seed 集、现有 `rule_ai/current_s2` 与 `humanlike_v2` 的行为/性能对比 |
| 兼容测试 | schema 1–4 旧存档读取、wire v1 兼容、2/3/4 人玩法、Human 子进程 |

本功能每个切片必须先跑当前安全无头回归集；Tk 硬崩溃用例须先完成环境隔离，不能作为 F0028 的随机失败源。

## 7. 范围

### 7.1 In Scope

- 完整 GP/RP 工程映射。
- 实体牌守恒、可见信息审计、决策可复现。
- 新 `humanlike_v2` 策略 profile，包括基础与有限认知阶段。
- 扩展现有训练环境和回归指标。
- 保留 F0010/F0011 能力并逐步迁移为 PlayerView-only 输入。

### 7.2 Out of Scope

- 本轮文档阶段不修改业务代码。
- 不一次性重写 `engine/`。
- 不复制第二套规则引擎或新建平行 `src/` 树。
- 不引入 PyTorch 或具体深度学习框架；训练契约与算法解耦。
- 不改变当前 UI 布局和打包主线。
- 不删除 2/3 人模式、多 human 或现有 AI profile。
- 不在 Git 基线损坏时执行大规模 schema 迁移。

## 8. 回滚与发布

- `humanlike_v2` 为显式选配；关闭后回到 `rule_ai/current_s2`。
- 新观测/动作 codec 带版本，旧 env 入口在过渡期保留。
- 新 schema/format/wire 如需升级，必须提供向前读取或明确迁移工具。
- 不在中间切片将 `humanlike_v2` 设为默认玩家。
- 发布时包含三个 CDMJ 版本、源文档 hash、配置 hash、观测/动作/replay 格式版本、测试报告和已知差异。

## 9. 风险与开放问题

### 9.1 主要风险

1. **实体牌迁移面大**：状态、存档、协议、UI 和测试都依赖牌面 ID，必须使用内部 ID + 外部牌面投影的兼容层。
2. **现有分析的全知入口**：F0010 的 oracle 评估和 `RuleAIPlayer._engine_state` 是训练器的既有能力，但不能进入 v2 生产策略输入。
3. **规则参数与旧 `EngineConfig` 重叠**：应通过适配层映射，不同时存在两个可互相矛盾的权威配置。
4. **可复现与真实耗时冲突**：思考时间应记录模型值，不应用系统调度耗时作为策略随机输入。
5. **性能**：Top-K 信念+有限展开+四智能体可显著增大自博弈成本，需为每个阶段设定决策耗时和吞吐量基线。

### 9.2 已批准决议

2026-07-28 用户确认 F0028 方案，以下决议锁定：

1. 按 6 个切片渐进实施，不一次性完整改造。
2. `humanlike_v2` 先作为新 profile，不直接替换 `current_s2`。
3. 实体牌 ID 迁移列为 F0028 必做，用于去重、守恒和审计。
4. 首个验收 profile 为“普通中等水平、中性风格”。

## 10. 审批后的执行顺序

1. 恢复 Git 基线并修复已知测试门禁。
2. 先为 F0028-1 补充字段级 GP/RP 映射附录，然后实现与验收。
3. 每个切片完成后回写实现差异、测试结果和下一切片门禁；不允许跨切片“顺便”实现。

## 11. 本文验收标准

- [x] 新规则文件 hash 与实现规范绑定值一致。
- [x] 已对照现有 engine / protocols / players / analysis / training / replay 代码。
- [x] 已说明复用、改造、新增与不重写的边界。
- [x] 已给出切片顺序、代码路径、测试、回滚和风险。
- [x] 用户确认本方案（2026-07-28，`Review` → `Approved`）。
- [ ] Git P0 基线已恢复。
