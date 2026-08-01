# F0033 成都麻将 Humanlike AI 完整软件设计

| 字段 | 内容 |
|---|---|
| Feature ID | F0033 |
| 状态 | **Draft** |
| 文档类型 | 完整软件设计 / 需求归一化 / 量化验收基线 |
| 需求源 | `成都麻将AI人类化决策规则_v1.md`、`成都麻将AI训练模拟器程序实现规范_v2.0.0.md` |
| 审计源 | `docs/status/SPEC_IMPLEMENTATION_AUDIT_2026-07-29.md`（96 单元） |
| 配套规格 | F0028 系列、F0030、F0031、F0032 |

## 1. 设计目标与权威性

本文把两份源规格和实现审计归一为一份可开发、可测试、可度量的软件设计。它保留全部 96 个审计单元，并为每个单元定义处理流程和量化目标。

本文处于 Draft，不改变现有代码权威性。批准后，冲突优先级为：引擎不变量与成都麻将权威房规 > 本文批准条款 > 参数配置 > 实现便利。未知版本、未知房规或不可恢复的数据不得静默降级。

设计不使用单一“人类化总分”。发布结论分别报告：规则正确性、有限信息、风格可辨识、策略强度、真人相似、学习效果、性能与复现。

## 2. 系统边界与模块

| 模块 | 责任 | 禁止事项 |
|---|---|---|
| Match Controller | 冻结配置、创建 game_id/seed、组织单局或整场、汇总排名 | 不直接修改牌或代替规则引擎裁决 |
| Rule Engine | 发换定、摸打碰杠胡、血战终止、合法动作和状态转移 | 不调用 Humanlike 策略 |
| State Store | 保存完整权威状态、实体牌、事件序号和账本 | 不向策略暴露隐藏状态 |
| Player View Builder | 从权威状态按白名单构建座位视图 | 不采用“全状态序列化后删字段” |
| Humanlike Policy | 记忆、注意、分析、信念、计划、候选、评价、停止和选择 | 不接收 GameState/oracle |
| Action Resolver | 合并多人响应并按房规确定解析 | 不依赖子进程返回先后顺序 |
| Scoring | 胡杠事件、终局调整、总分和排名 | 不把训练塑形写入真实账本 |
| Audit/Replay | 记录版本、哈希、视图、候选、RNG、动作和结算 | 不用终局信息覆写历史视图 |
| Training Wrapper | 复用生产规则、固定 observation/action/mask/reward 契约 | 不维护第二套规则语义 |
| Evaluation | 执行 F0031 指标和 F0032 数据质量门禁 | 不向被测策略传递 evaluation truth |

依赖方向：Controller → Engine/Resolver/Scoring；Engine → State；View 只读 State；Policy 只读 View；Training/Evaluation 通过公开接口组合模块。任何反向依赖必须以 ADR 批准。

## 3. 权威数据与版本

- 实体牌：face 0～26，physical tile 0～107；守恒按 physical id 验证。
- 状态：当前 `GameState schema 5`；保存前后实体牌所有权、活动座位、阶段、账本一致。
- 策略输入：PlayerView v2 白名单；隐藏字段必须不存在而不是置空。
- 动作：action codec v2 固定 635 维，`legal_action_mask` 为机器权威，结构动作供人读。
- 版本：RULES、PARAMS、IMPL、state、PlayerView、codec、training contract 分线记录。
- 配置：27 个 GP 和 4 座 profile 冻结、强类型校验、canonical JSON hash；运行期不原地修改。
- 运行态：33 个 RP 按 match/round/decision 生命周期更新；每个 consumer 和归档策略可追踪。

## 4. 端到端处理流程

### 4.1 整场与单局

1. Controller 加载并验证版本组合、房规、玩家配置和 seed；失败则在创建状态前终止。
2. Engine 创建实体牌墙、定庄、发牌；每个原子事件后执行不变量断言与哈希。
3. 依次执行换三张、定缺、血战主循环；活动座位随胡牌状态确定更新。
4. 每个决策点先构建座位 PlayerView，再生成完整合法动作集。
5. 唯一合法或 mandatory 动作直接返回；否则进入 Humanlike 决策管线。
6. Resolver 确定解析响应；Engine 原子应用；Scoring 追加不可变账本事件。
7. 终局执行花猪、查叫、退税、呼叫转移和封顶等启用规则，输出分数与排名。
8. Audit 封存事件、决策和哈希链；Controller 按批准策略更新跨局公开画像。

### 4.2 Humanlike 单次决策

```text
PlayerView + legal actions + frozen config + RP snapshot
  → mandatory check
  → memory decay/update
  → bounded attention selection
  → own-hand structural analysis
  → per-opponent public belief update
  → primary/backup plan review
  → legal candidate generation
  → bounded look-ahead and Q decomposition
  → satisfactory-stop check
  → bounded, seeded human-like perturbation
  → chosen action + reason + private trace
```

Q 的权威设计为：`Q = w_speed*S + w_live*L + w_fan*F - w_risk*R + w_plan*P + w_match*M + ε`。六个主项归一到 `[0,1]`，权重非负且按版本归一；`ε` 有界、可复现，并受强制动作、明显劣势、分差和技能等级约束。每一项必须输出值、依据、版本和输入字段集合。

### 4.3 对手信念与信息边界

每个活动对手独立维护假设分布：花色压力、清一色、七对、对对胡、听牌及等待类别。先验由公开房规和阶段给出，只用弃牌、副露、定缺、响应与公开结算作更新；归一化后总概率误差 ≤`1e-9`。无法区分时保留不确定性，不把“未见牌”当作“墙内牌”。

### 4.4 计划、记忆与学习

- 主/备计划在每次新观测后复核；只有触发阈值达到才切换，避免逐步抖动。
- 记忆按可见事件步指数衰减；显著事件提高短期权重；容量溢出按最低有效权重淘汰。
- RP-033 只消费批准的公开局后摘要，按有界学习率更新下一局画像；原始暗牌和终局后才揭示但局中不可见的信息不得反写历史决策。

### 4.5 训练与评估

训练 wrapper 复用 Engine/View/Resolver/Scoring；每一步返回 observation、mask、真实奖励、塑形奖励、done 和审计引用。评估使用冻结 seed、座位轮换和 F0032 数据；策略进程只接收 policy_view，evaluation_truth 由评估器独占。

## 5. 全局量化门禁

| ID | 指标 | 目标 |
|---|---|---|
| K-01 | 非法动作、隐藏信息泄漏、实体守恒、状态断言、未处理异常 | 全部为 0 |
| K-02 | 同版本/配置/seed 的墙、状态、动作、结算和 trace hash | 100% 一致 |
| K-03 | 96 个 AU 登记与实现/测试/结果追踪 | 100% |
| K-04 | AU 内 hard 子断言 | 100% 通过；不得平均抵消 |
| K-05 | 2/3/4 人安全批跑 | 各 ≥200 局；K-01 全通过 |
| K-06 | 单决策性能 | p95 ≤25 ms；报告 p50/p95/p99 |
| K-07 | PlayerView observation+mask | p95 ≤5 ms |
| K-08 | 四人批跑相对 RuleAI | wall time ≤3.5× |
| K-09 | 风格主指标 | 方向一致率 ≥80%，`|Cliff's δ|≥0.33` 且 95% CI 不跨 0 |
| K-10 | 强度非劣 | 配对标准化净分差 95% CI 下界 >-0.10 SD |
| K-11 | 真人相似 | 冻结上下文加权 JSD ≤0.15；核心层 ≤0.20；数据不足则 Not Evaluated |
| K-12 | 学习效果 | 对手动作 Brier score 相对无学习改善 ≥5%，且收益不劣 |

统计比较使用冻结测试集、配对 seed、座位均衡和双侧 95% bootstrap CI（≥10,000 次）。硬规则使用零容忍，不使用统计豁免。

## 6. AU-001～AU-050：人类化规则设计与目标

下表保留审计报告的原始单元边界。一个单元包含多项要求时，各子项均为 hard assertion；单元状态取最弱子项。

| AU | 功能 | 具体流程 | 量化目标 / 证据 |
|---|---|---|---|
| AU-001 | 范围与合法性优先 | View→legal→mandatory；唯一合法动作跳过策略评分 | 2/3/4 人各 200 局非法动作 0；唯一合法动作直出率 100% |
| AU-002 | 可见信息边界 | State→白名单 View→Policy；oracle 独立传给 evaluator | 禁止字段出现/读取 0；字段快照 100% 匹配 PlayerView v2 |
| AU-003 | 游戏开始 | 读取规则/座位/局号→初始化 round RP→载入有界公开印象 | 初始化必填率 100%；跨局只保留批准字段；相同输入 hash 一致 |
| AU-004 | 学习规则 | GP 房规解析→兼容矩阵→各模块 adapter→profile 派生 | 27 GP 登记/consumer/test 100%；受支持组合 golden case 100% |
| AU-005 | 风格动态变化 | 比分/局数/牌质/对手特征→动态权重→候选/深度/风险 | 预注册主指标满足 K-09；领先/落后方向案例 ≥80% 一致 |
| AU-006 | 定庄与座位 | seed 掷骰→庄家→座位关系→active ring→胡后重排 | 固定 seed 复现 100%；轮转/胡后顺序 golden case 100% |
| AU-007 | 独立对手模型 | 每座独立 prior→公开事件 Bayesian update→归一化 | 对手状态串扰 0；概率和误差 ≤1e-9；早期熵不低于批准下限 |
| AU-008 | 初始手牌整理 | 实体手牌→face counts→结构枚举→普通/七对/清一色候选 | 13/14 张校验 100%；标准/七对向听 golden 100%；Top-N 召回 ≥95% |
| AU-009 | 初步计划可修正 | 初始计划→每观测复核→阈值触发主备切换 | 强反例切换率 100%；弱扰动保持率 ≥90%；trace 完整 100% |
| AU-010 | 换三张合法性 | 枚举同花色三张→选择→方向转移→实体归属→重算 | 非同花色选择 0；实体重复/丢失 0；方向与接收重算 100% |
| AU-011 | 换牌策略 | 结构保护→弱张排序→送牌风险→近似方案扰动 | 强刻/顺/对保护案例 ≥95%；弱张优先 ≥80%；K-09 适用 |
| AU-012 | 定缺选择 | 统计三门→0 张优先→结构/清缺成本→自然牌型修正 | 0 张花色选择 100%；规则场景通过 100%；风格方向 ≥80% |
| AU-013 | 清缺约束 | 缺门未清→legal 只留缺门牌→禁胡→后期花猪风险 | 清缺硬违例 0；缺门未清胡牌 0；花猪率不劣基准 2pp |
| AU-014 | 动态做牌方向 | 每次 View 更新速度/价值/风险→重评方向 | 指定转向场景方向一致率 ≥80%；无输入变化计划 hash 100% 稳定 |
| AU-015 | 花色环境 | 汇总各家定缺/公开牌→计算两门供需压力→进入 live/plan | 全部批准定缺组合 golden 100%；实体去重计数误差 0 |
| AU-016 | 逐家方向假设 | 对每座维护两门/清一色/七对/对对胡/听牌假设 | 假设集合完整率 100%；归一误差 ≤1e-9；合成标签 Brier 优于先验 ≥5% |
| AU-017 | 动态调整 | 手牌/弃牌/副露/阶段事件→更新 belief/plan/Q | 每类事件至少正反案例；应该变化的主项变化率 100%；无关项稳定 |
| AU-018 | 胡牌人数 | HU 事件→active ring→剩余机会/风险/顺序效用重算 | 状态重算 100%；已胡座位后续摸打 0；指定 Q 方向 ≥80% |
| AU-019 | 比分与剩余局 | match score/rounds left→名次效用 M→风险权重 | 领先防守、落后追分场景 K-09；M 在 `[0,1]` 且单调 100% |
| AU-020 | 玩家风格与水平 | profile→注意 K/深度/噪声/风险/牌型偏好 | 三档单调性 100%；风格分类 macro-F1 ≥0.65；G1 不退化 |
| AU-021 | 冲突与复核 | S/L/F/R/P/M 归一→加权→冲突理由→持续复核 | 六项 trace 完整 100%；权重和误差 ≤1e-9；冲突案例 100% 可解释 |
| AU-022 | 全番型配置 | 读取启用/互斥/叠加/封顶→估计边际番值→F | 禁用番型贡献 0；官方计番夹具 100%；封顶后边际值为 0 |
| AU-023 | 活牌与摸牌机会 | visible 去重→unseen→墙内分配估计→剩余摸牌区间 | `unseen != live` 类型隔离 100%；真值覆盖率 ≥95%；区间宽度分层报告 |
| AU-024 | 先胡与顺序 | 即时胡收益/继续做大/血战暴露→比较 Q | 强制胡 100%；可选胡场景方向 ≥80%；净分满足 K-10 |
| AU-025 | 主/备计划 | 生成 primary/backup→保存切换条件→事件后复核 | 双计划非空率 100%；触发切换/非触发保持 golden 100% |
| AU-026 | 算牌顺序 | own hand→visible inventory→逐家 belief→phase/hu update | 管线顺序 trace 100%；隐藏输入 0；更新后概率归一 100% |
| AU-027 | 有限记忆 | event token→显著度→指数衰减→容量淘汰→模糊读取 | 衰减单调 100%；容量不超限；遗忘后精确恢复次数 0；复现 100% |
| AU-028 | 行为序列与反观察 | 弃牌/响应序列→趋势特征→对手假设；自身暴露→风险修正 | 顺序置换敏感案例 ≥80%；二阶风险方向 ≥80%；不使用未来事件 |
| AU-029 | 局中/终局信息边界 | 决策时 view hash 冻结→终局另记 truth→历史不可变 | 历史 view 覆写 0；hash 链有效 100%；private 文件权限检查 100% |
| AU-030 | 剩余机会 | wall/active ring/位置→各座摸牌上下界→事件后重算 | 合成真值落入区间 ≥95%；碰杠胡后更新率 100%；上下界合法 100% |
| AU-031 | 响应优先 | 收集响应→过滤合法→按 GP-008/座位顺序确定解析 | 全组合矩阵 100%；返回时序排列结果一致 100%；非法响应 0 |
| AU-032 | 胡牌响应 | 识别自摸/点炮/抢杠→强制/可选→过胡状态→恢复 | 路径 golden 100%；强制胡违例 0；过胡模式状态转换 100% |
| AU-033 | 杠牌响应 | 枚举明/暗/补杠→抢杠窗口→收益风险→应用/补牌/计分 | 三杠+抢杠+转移案例 100%；守恒/账本失败 0；选择效应 K-09 |
| AU-034 | 碰牌响应 | legal pong→结构/速度/暴露/让序→后续弃牌预评估 | 碰后合法状态 100%；多因素 trace 100%；profile 方向 K-09 |
| AU-035 | 摸牌后判断 | 新摸牌 View→胡→杠→出牌合法候选→计划重评 | 决策优先案例 100%；每次请求使用新 view hash；超时默认合法 100% |
| AU-036 | 出牌管线 | 清缺过滤→向听/进张→听前后规则→结构保留→排序 | golden 100%；最优合法候选覆盖 ≥99%；非法/漏候选 0 |
| AU-037 | 防守风险 | 逐家听牌概率×等待概率×损失→聚合 R→安全牌排序 | R 范围 `[0,1]`；合成危险排序 AUC ≥0.75；逐家 trace 100% |
| AU-038 | 人类表现 | 节奏/有限理性/扣牌/表达/多轮计划→有界扰动 | G1 不退化；节奏分布目标 K-11；错误上限由 level 配置且实测偏差 ≤2pp |
| AU-039 | 胡后处理 | 标记 HU_EXITED→退出摸打→按房规公开→继续观测→结算 | 已胡后主动动作 0；公开字段 100% 符合 GP；得分事件完整 100% |
| AU-040 | 终局计分 | 汇总胡杠→花猪/查叫/退税/转移→封顶→排名 | 权威房规矩阵 golden 100%；账本和为 0（零和配置）；排名确定 100% |
| AU-041 | 玩家模型 | profile+情绪+记忆→决策参数→局后公开摘要→解释 | 配置消费覆盖 100%；情绪范围合法；跨局字段白名单 100%；K-09 |
| AU-042 | 有限认知 | attention Top-K→有限候选/深度→满意停止→扰动/超时 | K/深度上限 100%；停止理由完整；复现 100%；p95 满足 K-06 |
| AU-043 | 总体流程 | 配置→发牌→换牌→定缺→血战→结算→归档 | 2/3/4 人各 200 局完成率 100%；K-01/K-02 全通过 |
| AU-044 | 阶段边界 | rule/profile 策略保持可插拔；学习能力显式 feature flag | 未启用能力调用 0；基准策略行为 hash 不变；范围声明完整 100% |
| AU-045 | GP 注册 | schema 加载→唯一 ID→类型/范围/consumer→hash/trace | GP-001～027 恰好 27；重复/未知/越界拒绝率 100% |
| AU-046 | RP 注册 | 生命周期创建→事件更新→决策快照→round/match 归档 | RP-001～033 恰好 33；生命周期测试 100%；未初始化读取 0 |
| AU-047 | RP-033 学习输出 | 公开摘要→有界历史→学习率更新→Profile_next→持久化 | 隐藏字段 0；状态 hash 复现 100%；Brier 改善 ≥5%；收益满足 K-10 |
| AU-048 | 数值校验 | parse→类型/枚举/范围/权重/版本/冲突校验→冻结 | 非法夹具拒绝 100%；NaN/Inf 0；错误含字段路径 100% |
| AU-049 | 六项 Q 评价 | 计算 S/L/F/R/P/M→归一加权→ε→排序/trace | 六项非缺失 100%；范围/权重和合法 100%；消融方向案例 ≥80% |
| AU-050 | 概率约束 | prior→公开证据更新→归一→死叫/活牌边界→置信度 | 概率和误差 ≤1e-9；死叫误判 hard cases 0；未见/墙内混用 0 |

## 7. AU-051～AU-096：程序实现设计与目标

| AU | 功能 | 具体流程 | 量化目标 / 证据 |
|---|---|---|---|
| AU-051 | 版本与源绑定 | 启动→读取三版本/源 hash→兼容矩阵→接受或拒绝 | 已知组合接受 100%；未知/源 hash 不符拒绝 100%；trace 必填 100% |
| AU-052 | 冲突裁决 | 收集规则/参数/不变量→按优先级解析→冲突显式错误 | 冲突夹具拒绝 100%；静默默认 0；错误列出冲突字段 100% |
| AU-053 | IR-001～018 | 逐项注册不变量→绑定检查点→事件后执行→审计结果 | 18 项登记/consumer/test 100%；hard IR 失败 0；失败可重放 100% |
| AU-054 | 九模块架构 | 接口注入→按依赖方向调用→禁止跨边界访问 | 架构契约测试 100%；Policy→GameState 引用 0；循环依赖 0 |
| AU-055 | Match Controller | 锁 GP/profile/seed→创建玩家→循环 round→终止/排名 | 配置锁定 100%；2/3/4 人及多局终止案例 100%；seed 可追踪 100% |
| AU-056 | Rule Engine | 发换定→主循环→响应→血战终止→settled | 状态机合法路径 100%；非法转移拒绝 100%；K-01 全通过 |
| AU-057 | State Store | 事务前快照→原子应用→断言→提交/hash；失败回滚 | partial commit 0；schema 5 round-trip 100%；未授权读取测试 100% |
| AU-058 | Player View | 按 seat/GP 白名单投影→冻结→hash→交付 | 禁止字段 0；新增 state 字段默认不进入 view；构建 p95 ≤5 ms |
| AU-059 | Humanlike Policy | memory→attention→analysis→belief→plan→candidate→Q→stop→noise→trace | 管线阶段 trace 完整 100%；相同输入复现 100%；K-06/K-09 |
| AU-060 | Action Resolver | 收集带 seat 的响应→校验→GP-008 排序→原子结果 | 网络/进程返回全排列结果一致 100%；重复/过期 response 拒绝 100% |
| AU-061 | Scoring | 规则事件→GP-011～020→ledger entry→终局调整→result | 每个 GP 至少正反边界案例；账本可对账 100%；塑形污染 0 |
| AU-062 | Replay/Audit | 写 event/state/view/config/candidate/RNG/score hash→验证链→复演 | 必填完整 100%；篡改检出 100%；动作/结算复演一致 100% |
| AU-063 | Training Wrapper | 生产 Engine reset→View obs→mask→step→reward→multi-agent adapter | 单智能体可用 100%；声明多智能体模式 golden 100%；规则分叉 0 |
| AU-064 | 牌编码 | face↔physical 构造→所有权迁移→face 投影 | 0～26/0～107 双射规则 100%；实体重复/缺失 0；旧档迁移稳定 100% |
| AU-065 | 玩家与活动顺序 | 固定 seat→status 转移→active ring→next actor | seat 不重编号 100%；HU_EXITED actor 0；轮转案例 100% |
| AU-066 | 手牌与组合 | concealed ids→counts→meld/dingque/pass-hu 一致更新 | 手牌张数/组合断言失败 0；三类杠/碰/胡迁移案例 100% |
| AU-067 | 可见牌 | own/discard/meld/hu/gang physical ids 去重→face 聚合 | 同一实体重复计数 0；公开计数与事件重放一致 100% |
| AU-068 | 计分对象 | match_before→ledger→end_adjust→result→match_after | 五层字段完整 100%；前后分差=ledger+adjust 100%；来源可追踪 |
| AU-069 | 配置模型 | 加载 27 GP/4 profile→强类型→冻结→canonical hash | 完整/唯一/范围测试 100%；运行期 mutation 0；跨平台 hash 一致 |
| AU-070 | Round/Player/View 状态 | 创建 round truth→逐座 player RP→逐决策 view snapshot | 三层串扰 0；33 RP 生命周期 100%；view 无 truth 字段 100% |
| AU-071 | 状态机与事件 | CONFIGURED→...→SETTLED；每事件 validate/apply/assert/hash | 合法边覆盖 100%；非法边拒绝 100%；每原子事件 hash/断言率 100% |
| AU-072 | 合法行动与解析 | phase/state→枚举动作→定缺/无吃/过胡过滤→mask→resolver | codec 与结构动作一致 100%；mask 假阳/假阴 0；全响应路径 100% |
| AU-073 | AI 决策管线 | immutable context→mandatory→bounded search→stop→noise | context mutation 0；mandatory 正确 100%；候选/停止/噪声上限 100% |
| AU-074 | 手牌分析 | counts→普通/七对/启用特殊型→Top-N 拆解→弃牌向听/等待 | 标准/七对 golden 100%；弃牌向听准确率 100%；Top-N 召回 ≥95% |
| AU-075 | 信念与风险 | unseen/live 分层→清缺/牌型 prior→Bayes update→逐家 danger | 概率合法 100%；真值合成集 Brier 改善 ≥5%；危险排序 AUC ≥0.75 |
| AU-076 | 注意/记忆/摸牌/Q | Top-K→衰减记忆→机会区间→六项 Q→有界选择 | K/容量/深度上限 100%；区间覆盖 ≥95%；Q 完整 100% |
| AU-077 | 训练模式 | mode registry→能力检查→创建规则/学习玩家→运行/归档 | 每个宣称模式至少 50 局无 K-01 失败；未实现模式明确拒绝 100% |
| AU-078 | 观测空间 | PlayerView→固定块编码→可选认知→mask→shape validate | 2/3/4 shape 100% 固定；NaN/Inf/隐藏哨兵 0；p95 ≤5 ms |
| AU-079 | 动作空间 | 结构动作↔635 codec→legal mask→step 校验→非法策略 | round-trip 100%；合法 mask 精确 100%；raise/惩罚模式案例 100% |
| AU-080 | 奖励 | ledger delta→base reward→PlayerView potential shaping→分项输出 | base 与真实得分一致 100%；truth 泄漏 0；base+shaping 对账 100% |
| AU-081 | Episode | reset single/match→step loop→round boundary→合法继承→done | 单局/整场终止案例 100%；只继承批准状态；clone/restore 一致 100% |
| AU-082 | 事件日志 | 原子事件→public payload→private before/after/config hash→append | 每事件日志覆盖 100%；必填/顺序/hash 链有效 100%；敏感字段隔离 |
| AU-083 | AI 决策日志 | view/memory/attention/plan/legal/candidate/Q/stop/RNG/action/time→append | 正式决策记录完整 100%；chosen∈legal 100%；历史不可变 100% |
| AU-084 | 确定性回放 | 加载版本/config/seed/events→重建→逐步比 hash→结算 | ≥50 seeds/配置动作、状态、墙、结算一致 100%；首差异可定位 |
| AU-085 | 核心接口 | Controller 通过 RuleEngine/ViewBuilder/Policy/Scoring protocol 组合 | 接口契约测试 100%；替身实现可注入；内部类型泄漏 0 |
| AU-086 | 训练接口 | reset/step/mask/clone/restore→多玩家 ActionMap | API 契约 100%；clone 后分支可复现；无动作玩家 mask 全零 100% |
| AU-087 | 每事件断言 | apply 后检查守恒/张数/actor/status/dingque/legal/view/ledger/FSM | 所有原子事件执行率 100%；随机合法局失败 0；错误含 event index |
| AU-088 | 单元测试清单 | 按规则路径生成正/反/边界 fixture→执行→绑定 AU | 列明路径覆盖 100%；hard case 通过 100%；每 AU 至少一直接测试或批准 N/A |
| AU-089 | 属性测试 | 生成随机合法局→每步断言→保存最小反例 seed | 2/3/4 人各 ≥10,000 随机步；守恒/mask/泄漏/复现失败 0 |
| AU-090 | 章节对照测试 | 源章节→GP/RP→固定场景→profile 允许行为集 | 两源规范章节登记 100%；96 AU crosswalk 100%；案例通过 100% |
| AU-091 | 回归指标 | 批跑→规则率/复现/打法/风格/真人指标→版本比较 | K-01/K-02；K-09/K-10；真人数据可用时 K-11，否则 Not Evaluated |
| AU-092 | 源规则追踪 | clause→AU→GP/RP→module/consumer/test→result artifact | 规范条款登记 100%；孤立参数/无 consumer 0；链接失效 0 |
| AU-093 | 项目结构 | domain packages→公开接口→依赖检查→构建/测试 | Engine/AI/Training/Replay 分层；禁止依赖 0；跨平台 import 100% |
| AU-094 | 实施顺序 | 规则基线→视图隔离→基础策略→认知→训练；逐阶段 gate | 前序 gate 未过不进入后序；每阶段文档/代码/测试三件套完整 100% |
| AU-095 | 版本与兼容 | 变更分类→升级对应版本→迁移/兼容矩阵→发布校验 | 未知组合拒绝 100%；支持矩阵测试 100%；发布物 schema/迁移/测试齐全 |
| AU-096 | 完成定义 | 聚合 96 AU 状态→执行 hard gates→生成分层结论→批准发布 | AU 登记 96/96；hard assertion 100% 通过；未评估效果显式列出；K-01/K-02 |

## 8. 功能状态机与错误处理

权威阶段至少包括 `CONFIGURED → DEALT → EXCHANGING → DINGQUE → PLAYING → SETTLING → SETTLED`。事件携带 `game_id/event_index/actor/type/public_payload`；应用顺序固定为 validate → snapshot → apply → invariant → score/audit → commit。断言失败时不得留下部分状态。

错误分级：

| 类别 | 示例 | 行为 |
|---|---|---|
| ConfigurationError | 未知版本、非法 GP、冲突房规 | 创建牌局前失败，输出字段路径 |
| IllegalAction | action 不在合法集、过期响应 | 拒绝且不修改状态；训练按配置 raise 或惩罚终止 |
| InvariantViolation | 守恒、actor、账本、状态机失败 | 中止本局、保存最小重放证据，不自动继续 |
| ViewLeakage | 白名单外字段或 oracle 进入策略 | 整批验收失败，标为安全缺陷 |
| ReplayMismatch | hash/动作/结算不一致 | 在首个差异事件停止并报告版本/seed |
| DatasetQualityError | 主键、标签合法性、split 泄漏失败 | 数据 release quarantine，禁止正式评价 |

## 9. 配置、RP 与 trace 契约

- 每个 GP：ID、类型、默认值、合法范围、规则语义、consumer、测试和版本。
- 每个 RP：ID、owner seat、生命周期、初始化、更新事件、归档、是否允许跨局。
- 每次决策 trace：版本/config hash、view hash、legal、mandatory、memory、attention、hand features、belief、plan、candidate、六项 Q、stop、RNG、chosen、reason、estimated time。
- trace 是私有审计数据，不进入普通 PlayerView；字段缺失使 AU-021/AU-059/AU-083 失败。

## 10. 评估数据与统计设计

使用 F0032 的 DS-Golden、DS-Sim、DS-Human-Pilot、DS-Human-Eval 和 DS-Challenge。最小分析粒度为一次决策；`policy_view`、`action_label`、`evaluation_truth` 分文件隔离。

- 规则/架构单元：golden/contract/property tests，输出 pass/fail 和失败计数。
- 行为单元：固定配对场景，输出方向率、Cliff's delta 和 CI。
- 强度单元：每候选×基准×人数 ≥1,000 配对局，座位均衡。
- 真人单元：正式测试至少 10,000 合法决策、200 局、30 玩家；不足只作探索。
- 学习单元：每对手条件 ≥500 配对重复局、≥20 独立对手策略。

所有指标必须声明分母、排除规则、上下文分层、版本和数据 hash。无数据输出 Not Evaluated，不填 0，不用其他指标代替。

## 11. 测试与发布门禁

测试层次：单元 → contract → golden → property → deterministic replay → batch simulation → behavior A/B → strength league → human offline evaluation → Windows/macOS acceptance。

发布报告按 AU 列出 `Passed / Failed / Not Evaluated / N/A-approved`。hard AU 不允许 N/A；任一 hard assertion 失败阻断发布。AU 总览只报告状态计数，不将不同证据类型加权成总分。

跨平台至少要求：Windows 和 macOS 各执行配置加载、PlayerView、Human 子进程、决策复现、审计写读和性能 smoke；平台相关进程参数仅在对应 OS 传入。

## 12. 实施切片

| 切片 | 内容 | 完成定义 |
|---|---|---|
| F0033-1 | 冻结 96 AU registry、子断言、metric registry | 96/96 有 owner、gate、公式、数据、阈值、测试计划 |
| F0033-2 | 补齐规则/房规 golden matrix | AU-001～013、031～040、051～072 hard case 100% |
| F0033-3 | 补齐信念、Q、计划和行为场景 | AU-014～030、041～050、073～076 可量化 |
| F0033-4 | 补齐审计、训练、接口与属性测试 | AU-077～096 工程结论可自动生成 |
| F0033-5 | 校准 DS-Sim 风格与强度目标 | K-09/K-10 阈值经基线审批 |
| F0033-6 | 接入合规真人评估和 RP-033 | K-11/K-12 可判定；无数据保持 Not Evaluated |

## 13. 批准条件与实现边界

- [ ] 确认本文为两份源规格的统一实现设计，但不删除或改写源文件；
- [ ] 确认 AU-001～AU-096 与审计报告 96 行一一对应；
- [ ] 确认复合 AU 的内部子断言均为 hard，不允许平均通过；
- [ ] 确认权威房规矩阵、受支持人数与版本组合；
- [ ] 确认 K-09～K-12 是待基线校准的目标，当前不代表实测达成；
- [ ] 确认未实现训练模式和 RP-033 必须显式拒绝或 Not Evaluated；
- [ ] 状态由 Draft 更新为 Approved 后，方可按 F0033-1 开始编码。

本文覆盖的是软件可验证行为。真人相似结论仅在获授权、具代表性的冻结数据范围内成立；策略强度非劣不等于真人高手水平；确定性思考时间模型不等于真实 wall-clock sleep；完整 trace 不授权向玩家界面公开隐藏审计数据。
