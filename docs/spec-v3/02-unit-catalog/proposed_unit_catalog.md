# Spec v3 建议功能单元目录

| 字段 | 内容 |
|---|---|
| 文档 ID | SV3-CATALOG-20260729-001 |
| 状态 | Draft / Boundary review complete |
| 日期 | 2026-07-29 |
| 输入 | 两份锁定来源、96 项证据矩阵、当前代码模块与测试结构 |
| 稳定 ID | 分类前缀 + 三位单调编号；编号不表达实现状态 |
| 最终单元总数 | **96** |

## 1. 目录规则

本目录的 96 个新单元与旧审计行数相同纯属重构结果，不维持“一旧行一新单元”的假设。每个单元只有一个主要职责、一组可冻结输入、一组可观察输出和一种主要方法分类。一个单元的详细规格仍需按 `UNIT_SPEC_TEMPLATE.md` 展开原子断言；本目录不代表实现通过。

`RULE` 只承载权威状态转换；`ALGO` 只承载确定性计算；`HEUR` 只承载人工人类化策略；`MODEL` 只承载概率或可训练模型；`STATE` 管理生命周期；`SCORE` 管理真实账本；`TRAIN` 管理训练契约；`AUDIT` 管理证据、追踪和发布门禁。

## 2. 确定性规则（16）

| 新 ID | 单一职责 | 主要输入 → 输出 | 独立验收 |
|---|---|---|---|
| RULE-001 | 规则、参数、不变量与合法性裁决优先级 | ruleset/config/state → authoritative legal set or explicit rejection | 冲突配置及非法动作表驱动测试 |
| RULE-002 | 换三张同花色、方向与提交合法性 | concealed physical tiles + direction → accepted exchange or error | 方向×花色×实体牌用例 |
| RULE-003 | 定缺未清时的强制出牌约束 | hand + dingque → legal discards | 缺门存在/清空边界 |
| RULE-004 | 定缺、死叫与胡牌资格约束 | hand + dingque + waits → hu eligibility | 清缺/未清/死叫用例 |
| RULE-005 | 座位、庄家与活动顺序 | seats + dealer + active set + actor → next actor | 2/3/4 人及退出轮转 |
| RULE-006 | 摸牌、可选响应与出牌标准顺序 | phase + actor + wall → next phase/action request | 每阶段状态转换表 |
| RULE-007 | 碰牌资格、执行与后续出牌 | discard + responders + hands → meld/turn | 合法/非法碰及让序 |
| RULE-008 | 明杠、暗杠与补杠资格及执行 | hand/meld/discard → gang transition | 三类杠与补牌守恒 |
| RULE-009 | 补杠抢杠胡窗口与解析 | bugang intent + responders → hu or gang | 抢杠/无人抢/多人抢 |
| RULE-010 | 自摸、点炮与抢杠胡资格 | state + winning tile + source → legal hu set | 三类胡及反例 |
| RULE-011 | 过胡设置、持续与恢复 | declined hu + phase/events → pass-hu state | 恢复模式矩阵 |
| RULE-012 | 强制胡与最后阶段必胡 | legal hu + GP rule + wall state → forced action | 开关及尾牌边界 |
| RULE-013 | 多人响应确定性优先级 | response set + GP-008 → resolved actions | 返回时序置换不变 |
| RULE-014 | 血战胡后退出、继续与终止 | hu result + active seats + wall → active set/end | 第1/2/3胡与荒牌 |
| RULE-015 | 启用番型、互斥/叠加与封顶规则 | ruleset + hand facts → applicable fan policy | 配置组合 golden cases |
| RULE-016 | 局中与终局公开信息范围 | phase + seat + event → visible field set | 白名单/禁止字段矩阵 |

## 3. 确定性算法（11）

| 新 ID | 单一职责 | 主要输入 → 输出 | 独立验收 |
|---|---|---|---|
| ALGO-001 | face/physical tile 编码、投影与所有权守恒 | physical regions → face views + conservation result | 108 张唯一性和迁移用例 |
| ALGO-002 | 手牌分解、向听、弃牌向听与等待形状 | concealed faces + melds → analyses | 标准/七对/特殊边界 |
| ALGO-003 | 去重可见牌与未见牌聚合 | PlayerView → visible/unseen counts | 被认领弃牌去重用例 |
| ALGO-004 | 墙内活牌区间或估计 | unseen + public allocations → live estimate | 上下界、归一与极端状态 |
| ALGO-005 | 逐座剩余摸牌机会估计 | active order + wall + response assumptions → draw interval | 碰杠胡后重算 |
| ALGO-006 | mandatory 分类、候选上限与稳定排序 | legal actions + context → mandatory/candidate set | 唯一动作、强制项不裁剪 |
| ALGO-007 | 六分量候选 Q 评价 | normalized features + weights → Q components/total | 分量、范围、权重与 tie-break |
| ALGO-008 | seed、噪声、思考时间与随机流确定派生 | game_id/seat/decision/config → reproducible samples | 跨进程/hash-seed 重现 |
| ALGO-009 | 配置类型/范围/版本校验、迁移与 canonical hash | raw config → frozen config/hash or explicit error | 旧版迁移与未知组合拒绝 |
| ALGO-010 | PlayerView 白名单构建 | authoritative state + seat + phase → PlayerView | 隐藏字段不存在及冻结 |
| ALGO-011 | game_id 到牌墙、骰子及子随机流的确定映射 | game_id + versions → named RNG streams | 同 ID 同流、域隔离（新增） |

## 4. 人类化启发式（23）

| 新 ID | 单一职责 | 主要输入 → 输出 | 独立验收 |
|---|---|---|---|
| HEUR-001 | 换三张候选评价 | legal triples + hand/public features → ranked triples | 强结构保护与送牌敏感场景 |
| HEUR-002 | 定缺花色评价 | hand structure + public context → ranked suits | 0张、少而散、清一色反例 |
| HEUR-003 | 动态风格调节 | profile + score/stage/hand → effective style knobs | 保守/激进方向效应 |
| HEUR-004 | 初始做牌方向形成 | initial analysis + profile → primary/backup direction | 不同牌型初始场景 |
| HEUR-005 | 主备计划生命周期 | observations + current plan → retain/switch/restart | 惯性、阈值与可推翻性 |
| HEUR-006 | 定缺花色环境评估 | all public dingque/melds → suit environment | 四家组合表 |
| HEUR-007 | 公开事件驱动的逐家方向更新 | prior hypotheses + events → heuristic direction evidence | 事件序列差分 |
| HEUR-008 | 整场比分与剩余局效用调节 | standings + rounds left → match utility modifiers | 领先/落后/末局 |
| HEUR-009 | 先胡、做大和血战顺序效用 | hu order + hand value + risk → speed/value preference | 第几胡收益场景 |
| HEUR-010 | 多目标冲突复核 | speed/fan/risk/plan/match signals → resolved preference | 冲突权重与持续复核 |
| HEUR-011 | 番型边际做牌价值 | enabled fan policy + hand path → marginal value | 封顶前后与互斥 |
| HEUR-012 | 碰牌策略评价 | legal peng + structure/exposure/turn → accept/pass score | 速度、暴露、后续弃牌 |
| HEUR-013 | 杠牌策略评价 | legal gang + score/risk/rob context → accept/pass score | 明暗补杠风险 |
| HEUR-014 | 出牌牌效与结构保留策略 | analyzed hand + legal discards → strategic rank | 清缺、听前/听后、拆搭 |
| HEUR-015 | 防守偏好与安全牌选择 | per-seat risk + loss + profile → defensive rank | 多家风险与安全牌 |
| HEUR-016 | 行为序列推断 | ordered public actions → behavioral cues | 顺序变化与阶段对照 |
| HEUR-017 | 思考节奏生成 | complexity + profile + deadline → planned think time | 范围、复现、无真实 sleep 契约 |
| HEUR-018 | 安全牌储备、扣牌与信息表达 | hand/public threats/self exposure → retention preference | 一阶与二阶行为场景 |
| HEUR-019 | Top-K 有限注意分配 | visible cues + capacity → attended items | mandatory 进入、容量与稳定性 |
| HEUR-020 | 有界记忆衰减与强化 | visible events + memory config → memory snapshot | 衰减、显著强化、不精确恢复 |
| HEUR-021 | 有限推演与满意停止 | candidates + budget/threshold → checked set/stop reason | 深度、预算、停止条件 |
| HEUR-022 | 人格、水平与情绪状态消费 | profile + short state → decision modifiers | 座位独立及方向效应 |
| HEUR-023 | 有界近似选择与人类失误 | checked candidates + bounded noise → chosen legal action | 合法性、误差上限、复现 |

## 5. 概率与可训练模型（5）

| 新 ID | 单一职责 | 主要输入 → 输出 | 独立验收 |
|---|---|---|---|
| MODEL-001 | 逐对手归一化方向/牌型假设 | public evidence + prior → posterior hypotheses | 每座独立、和为1、不确定性下限 |
| MODEL-002 | 逐对手听牌/等待/损失风险模型 | public evidence + hypotheses → risk distribution | 校准、分层与反例 |
| MODEL-003 | 仅公开信息的跨局对手画像学习 | match history + bounded state → next profile | 冷启动、历史上限、复现 |
| MODEL-004 | 可训练策略输入输出契约 | observation + mask + parameters → action distribution/value | mask 合法性和冻结推理 |
| MODEL-005 | 训练模型产物版本、冻结和评估生命周期 | training run + data/config hashes → frozen model card/artifact | 训练/评估隔离与版本拒绝（新增） |

## 6. 状态管理（12）

| 新 ID | 单一职责 | 主要输入 → 输出 | 独立验收 |
|---|---|---|---|
| STATE-001 | Match 配置冻结、玩家装配与整场控制 | match request → immutable match context | seat/profile/round/seed 冻结 |
| STATE-002 | 权威 RoundState 存储与授权访问 | atomic events → authoritative state | save/read ownership contract |
| STATE-003 | PlayerRoundState 手牌、副露、定缺与过胡状态 | rule transitions → player state | 字段一致性与生命周期 |
| STATE-004 | CONFIGURED→SETTLED 状态机 | current phase + event → next phase or error | 全转换表及非法跳转 |
| STATE-005 | 不可变 PlayerView 状态载体 | builder output → frozen seat view | mutation rejection与schema |
| STATE-006 | 策略侧认知运行态初始化与归档 | round start/end → cognition state/snapshot | 不进入权威 GameState |
| STATE-007 | 存档 schema 持久化与迁移 | state v1–v5 → current state or error | 真实/合成迁移夹具 |
| STATE-008 | 跨局比分、认知和 episode 状态继承 | round result → next-round context | 允许/禁止继承字段 |
| STATE-009 | 决策请求上下文与生命周期 | phase + PlayerView + legal set → request/result | 超期、重复、错误 seat |
| STATE-010 | GP/RP/Profile 注册与生命周期 | source config + phase → owned parameter state | 唯一性、逐座化、归档 |
| STATE-011 | 牌墙构建、洗牌与初始发牌 | named RNG + player count → wall/hands | 108张守恒与发牌数量（新增） |
| STATE-012 | 策略超时、崩溃与合法默认动作回退 | request + deadline/failure + legal set → fallback result | 超时/异常/唯一动作（新增） |

## 7. 真实计分（6）

| 新 ID | 单一职责 | 主要输入 → 输出 | 独立验收 |
|---|---|---|---|
| SCORE-001 | 分数账本分层与守恒 | score events → ledger/before/after | 每事件零和及层级一致 |
| SCORE-002 | 自摸、点炮与抢杠胡计分 | hu facts + fan policy → hu transfers | 三类胡及多人支付 |
| SCORE-003 | 明/暗/补杠与呼叫转移计分 | gang events + rules → gang transfers | 杠类型、抢杠与转移 |
| SCORE-004 | 花猪、查大叫与退税终局调整 | end state + rules → adjustments | 顺序、资格与边界 |
| SCORE-005 | 封顶、互斥和转移结算顺序 | raw components + cap policy → final transfers | 封顶前后次序 |
| SCORE-006 | 单局总分、整场累计与排名 | ledgers + prior standings → result/rank | 守恒、并列及提前终止 |

## 8. 训练环境（9）

| 新 ID | 单一职责 | 主要输入 → 输出 | 独立验收 |
|---|---|---|---|
| TRAIN-001 | 复用生产规则的训练包装 | engine config + agents → training transition | 与生产边界等价 |
| TRAIN-002 | Observation v2 编码 | PlayerView + optional cognition → fixed observation | schema、范围、泄漏 |
| TRAIN-003 | 固定动作 codec 与 legal mask | legal actions → action ids/mask | encode/decode 双射 |
| TRAIN-004 | 非法训练动作处理契约 | action id + mask + mode → raise/terminate/penalty | 各模式精确结果 |
| TRAIN-005 | 真实得分与可见势能奖励契约 | transition + visible potential → reward components | shaping 分离与默认关闭 |
| TRAIN-006 | 单 learner reset/step/mask/clone/restore | env state + learner action → transition/snapshot | round-trip restore |
| TRAIN-007 | 多玩家 ActionMap 与自博弈调度 | joint observations/actions → joint transition | 同步动作与座位轮换 |
| TRAIN-008 | 离线 BC 与回放 RL 数据消费 | versioned trajectories → batches/updates | split、mask、版本契约 |
| TRAIN-009 | 房规、profile 与行为域随机化 | domain seed + allowed ranges → sampled domain | 可复现及越界拒绝 |

## 9. 审计与证据（14）

| 新 ID | 单一职责 | 主要输入 → 输出 | 独立验收 |
|---|---|---|---|
| AUDIT-001 | 全原子规则事件日志 | state transition → public payload/private refs | 事件覆盖与历史不可变 |
| AUDIT-002 | AI 决策解释日志 | decision pipeline → view/memory/plan/scores/action trace | 字段完整与敏感边界 |
| AUDIT-003 | canonical hash 链与篡改检测 | ordered records + hashes → verified/rejected | 篡改、截断、重排 |
| AUDIT-004 | 同配置/seed/事件的确定性回放 | retained artifact → replay comparison | state/action/score 一致 |
| AUDIT-005 | 每事件强制不变量执行 | post-event state → pass or explicit failure | 守恒、actor、legal、view、账本 |
| AUDIT-006 | 直接规则与接口测试证据门禁 | assertion catalog + test results → coverage status | 测试正文与断言语义复核 |
| AUDIT-007 | 属性式生成、缩减与不变量证据 | generators + seeds → minimized failures/report | 状态空间与缩减可复核 |
| AUDIT-008 | 锁定来源逐章 golden-case 对照 | source clauses + cases → per-clause result | 0–18章及profile允许集 |
| AUDIT-009 | 工程与行为回归指标 | retained runs → metric report/CI | 合法、复现、性能、风格 |
| AUDIT-010 | 来源→参数→实现→测试全链追踪 | catalogs/manifests → trace matrix | 断链、版本和公式元数据 |
| AUDIT-011 | 版本、迁移与发布物完整性 | release candidate → manifest/gate result | schema/test/migration/hash/tag |
| AUDIT-012 | 强度、真人相似和学习效果外部评价 | frozen datasets + policies → statistics/CI | E5、盲测与 Not Evaluated |
| AUDIT-013 | 模块依赖、接口与信息流架构契约 | source graph + interfaces → violations/report | 禁止反向依赖和 oracle 泄漏 |
| AUDIT-014 | 证据数据保留、脱敏与新鲜度管理 | run artifacts + policy → retained manifest | current-run/report-only/敏感数据 |

## 10. 数量核对

| 分类 | 数量 |
|---|---:|
| RULE | 16 |
| ALGO | 11 |
| HEUR | 23 |
| MODEL | 5 |
| STATE | 12 |
| SCORE | 6 |
| TRAIN | 9 |
| AUDIT | 14 |
| **合计** | **96** |

其中 4 个单元来自旧 96 项未独立覆盖的要求：STATE-011、ALGO-011、STATE-012、MODEL-005。旧项到新项的逐行关系以 `unit_migration_map.csv` 为权威。

