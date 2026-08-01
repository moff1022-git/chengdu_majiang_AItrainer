# Spec v3 现有代码迁移计划

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 迁移对象 | 当前engine/players/training/audit实现 → 96单元目标架构 |
| 前置条件 | 单元规格与测试规格均Approved |
| 当前证据 | Not Evaluated；本计划不宣称现有代码符合v3 |

## 1. 迁移目标

在保持当前可玩、可保存和既有入口可回滚的前提下，把复合模块逐步抽取为96个可独立测试、追踪和验收的单元。迁移使用“盘点→特征冻结→新门面→适配器→影子比较→切换单写→退役旧路径”，禁止一次性重写或长期双权威。

## 2. 当前代码基线与目标归属

| 当前区域 | 当前候选职责 | v3目标 | 迁移原则 |
|---|---|---|---|
| `engine/state.py` | GameState/PlayerState/序列化 | STATE-001～004/011及domain schema | 先冻结旧schema golden，再抽不可变子状态和显式迁移器 |
| `engine/session.py`、`orchestrator.py` | 编排、自动步进、玩家调用 | runtime command handler/state machine/event bus | 保留外部入口，内部改调用新门面；最后删除直接状态写入 |
| `engine/rules.py`、`legal.py`、`blood_battle.py` | 规则、合法性、状态效果混合 | RULE-001～016 | 先抽纯裁决，再把effects改为事件；不复制旧规则 |
| `engine/deal.py`、`deck.py`、`dice.py`、`exchange.py`、`opening.py` | game_id、洗牌、发牌、换牌、开局 | STATE-011、RULE-002/005、ALGO-001/011 | 固定历史game_id golden；命名随机域替换散落RNG |
| `engine/shanten.py`、`hand_utils.py`、`win_check.py` | 手牌分析与胡形 | ALGO-002及RULE-004/010 | 分离“数学事实”与“房规资格”；规范公式另立版本 |
| `engine/fan.py`、`score.py`、`reward.py` | 番、计分、奖励部分耦合 | SCORE-001～006、TRAIN-004 | 真实分只用整数ScoreTransfer；reward只消费账本/显式势能 |
| `players/view/player_view.py`、`humanlike/view.py` | 玩家视图 | RULE-016、ALGO-010、STATE-005 | 白名单投影单写；旧Observation经adapter，不再传GameState |
| `players/analysis/` | 剩余牌、危险、对手推断、建议 | ALGO-003～007、MODEL-001/002、HEUR相关 | 确定算法与概率模型物理拆包；隐藏truth只用于离线标签 |
| `players/humanlike/` | 认知、计划、候选、策略和回放 | STATE-006～009、HEUR-001～023、MODEL-003/004 | 先锁输入schema，再按决策顺序抽取；保留HumanlikeV2Player门面 |
| `training/` | env/action/obs/reward/runner | TRAIN-001～009 | env只包装生产runtime；删除任何复制/简化的状态转换 |
| `engine/audit.py`、`replay.py`、`invariants.py` | 日志、hash、回放、不变量 | AUDIT-001～014 | 保持旧日志reader，新增版本化writer；以迁移工具升级证据 |

“候选职责”仅用于定位，不是实现通过结论。正式复用前必须在96单元差距矩阵中记录代码符号、行为证据和偏差。

## 3. 迁移分类方法

每个单元只能选择以下主分类之一，并可附带风险标签：

| 分类 | 定义 | 动作 |
|---|---|---|
| REUSE | 现有行为与Approved规格逐项一致，接口仅需搬迁 | 保留实现，增加门面/测试/证据 |
| ADAPT | 核心行为可用，但schema、可见性、错误或依赖不符 | 新接口包裹，影子比较后切换 |
| REWRITE | 规范公式/状态所有权/信息边界实质不符 | 新实现；旧实现仅作baseline对照，不作oracle |
| ADD | 当前没有独立实现 | 按DAG新建，禁止从下游复制逻辑 |
| RETIRE | 旧职责已被新单元替代或违反边界 | 迁移调用方后删除/封存 |

风险标签：`RULE_DELTA`、`SCHEMA_BREAK`、`RNG_BREAK`、`REPLAY_BREAK`、`VISIBILITY`、`SCORE`、`PERFORMANCE`、`DATA_MIGRATION`。

## 4. 双轨与切换策略

迁移期间只允许“新实现主写、旧实现影子读比较”或“旧实现主写、新实现影子计算”之一；不得两边同时写权威状态、账本或日志。影子输出必须隔离，不能影响玩家视图、动作、reward或比分。

每个切换点使用版本化feature flag，仅在测试、开发或明确迁移环境开启；生产默认值由Approved阶段决议决定。flag必须带owner、移除阶段和审计字段，禁止永久保留不受测的双路径。

## 5. 分阶段迁移

### M0 现状盘点与冻结

动作：建立96行实现差距矩阵；记录当前类/函数、测试、配置、日志、存档和已知差异；冻结代表性game_id、存档、事件、计分和PlayerView样本。

完成条件：

- 96单元均有REUSE/ADAPT/REWRITE/ADD/RETIRE分类及负责人、风险、代码符号。
- 当前测试命令、结果、环境和commit已保存为baseline，不冒充v3证据。
- 关键golden输入及SHA-256可复核；未解决歧义列为blocker。

回滚：无行为修改，删除盘点产物即可。

### M1 公共domain、配置与随机数

动作：新增不可变公共结构、VersionBundle、canonical serializer、UnitError、配置冻结与NamedRandomStreams；旧`engine.game_id/deck/dice`经adapter调用。

完成条件：

- 旧/新入口同game_id下牌墙、骰子及已冻结随机域一致，或差异已按新规范显式版本化。
- 配置未知键/越界/版本错稳定失败；运行中不可变。
- 禁止全局RNG和Python`hash()`的架构检查通过。

回滚：切回旧门面；保留新schema reader但不写新格式。

### M2 权威状态、规则与事件总线

动作：抽取StateStore、RuleEngine、command handler、reducer、响应窗口和提交后事件总线；把旧session/orchestrator内部写操作改为命令。

完成条件：

- 牌张守恒、开局、换三张、定缺、摸打、碰杠胡、多人响应、过胡、胡后退出、墙终止合同通过。
- 每条命令只有一次原子commit；重复/旧版本/非法输入不改变state hash。
- 同步订阅顺序固定，异步订阅者不能改变权威结果。

回滚：入口adapter切回旧session；新日志标记aborted migration run，禁止混入正式链。

### M3 确定分析、PlayerView与计分账本

动作：拆分ALGO纯函数、白名单PlayerView、ScoreTransfer/ledger；旧analysis和score调用新门面。

完成条件：

- 向听、进张、可见/未见、等待、摸牌机会及规范Q golden通过。
- 任意视图投毒测试无隐藏信息；策略侧无GameState引用。
- 胡/杠/终局每个原子事件、层和本局`ΣΔ=0`，重放不重复入账。

回滚：只允许在未写正式新账本前回切；发生正式账本写入后必须用补偿迁移，不得直接覆盖。

### M4 Humanlike认知与启发式

动作：保留`HumanlikeV2Player`外部接口，内部按view→cognition→analysis→candidate→plan→score→choice→explanation重排；逐个抽HEUR和STATE认知单元。

完成条件：

- illegal/mandatory/visibility违例为0；固定配置/seed逐字段复现。
- 候选上限、满意停止、扰动、人类失误和思考时间均在Approved范围。
- 统计方向效应、regret和95% CI按卡报告；无真人数据不宣称真人相似。

回滚：切回旧policy adapter；不得把新认知状态反写旧格式而丢字段。

### M5 概率模型与生命周期

动作：拆线上feature schema、离线label schema、规则基线、推理门面、artifact registry和校准报告；旧opponent_model经门面访问。

完成条件：

- 隐藏truth投毒被loader拒绝；牌局级切分无泄漏。
- 概率范围/归一化、Brier/log loss/ECE、可靠性和不确定性完整。
- 模型缺失、OOD、超时、版本错均回退规则基线且仍合法。

回滚：禁用模型artifact，直接使用版本化规则基线；不改变线上schema。

### M6 训练环境

动作：将env重构为生产runtime adapter，统一Observation/action codec/mask/reward；补自博弈、对手池、快照、并行和数据manifest。

完成条件：

- 训练与生产逐事件状态、合法集、分数、终止原因golden一致。
- policy observation不含truth；evaluator/label区权限隔离。
- reward每项追踪ScoreTransfer或`γΦ(o')-Φ(o)`；同seed回放一致。

回滚：停止新训练run；已生成数据按manifest标deprecated，禁止混入兼容数据集。

### M7 审计、证据与发布

动作：统一事件/决策日志、canonical hash链、回放、不变量、测试证据、追踪、发布与保留；旧audit reader兼容历史版本。

完成条件：

- 96单元来源→参数→实现→测试→证据无断链。
- 篡改、乱序、缺失、过期、泄漏均不能Passed；hard失败不可抵消。
- 发布物manifest、代码/config/model/schema hash及回滚包完整。

回滚：发布门禁失败即停止发布；已签审计记录append superseding记录，禁止覆盖。

### M8 旧路径退役

动作：删除或封存适配器、feature flag、直接状态写入、第二分析/计分/随机路径；完成存档和配置迁移工具。

完成条件：

- 架构扫描无禁止依赖、第二规则引擎、全局RNG和oracle回流。
- 旧存档/配置在支持窗口内可读并产生明确迁移报告；新格式只由单一writer产生。
- 全量测试、确定回放、性能、跨平台和发布审计通过。

回滚：使用前一已签发布物和数据备份；新格式提供只读导出到兼容交换格式，禁止破坏性降级。

## 6. 存档、配置、日志和模型兼容

- 存档：读取旧schema→验证hash→纯迁移函数链→新schema→保存migration manifest；原文件只读保留。
- 配置：旧键映射必须显式、可审计；未知/歧义键拒绝，禁止猜测默认值后静默成功。
- 日志：旧日志不重写hash；新reader输出标准事件并标`source_format`，无法证明连续性则`complete=false`。
- 模型：artifact绑定feature/label/config/code版本；不兼容直接回退，不在线临时转换权重。
- 训练数据：不同schema/version分区；迁移数据保留原始行hash和转换代码hash。

## 7. 差异与冲突处理

发现“现有代码符合旧行为但不符合Approved v3”时，先在差距矩阵标`Conflict`并引用单元规格；不得擅自把旧行为写回规范。若产品决议要保留旧行为，则先修改对应Approved规格、测试规格、追踪矩阵和本计划并重新批准，再实施。

## 8. 每批提交门禁

每批必须包含：相关任务卡状态、代码路径、Approved测试ID、执行命令/结果、环境与hash、迁移/回滚说明、旧路径处置。禁止把多个未冻结接口的大阶段揉成一次提交；禁止用删除失败测试、放宽阈值或增加永久skip关闭迁移。

## 9. 关联文档

- [开发实施指南](development_guide.md)
- [96单元开发任务卡](development_task_cards.md)
- [Approved测试规格](../05-test-spec/README.md)
- [跨文档冲突报告](../08-review/spec_conflict_report.md)
