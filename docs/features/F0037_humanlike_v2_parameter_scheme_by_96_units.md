# F0037 Humanlike v2 参数设置方案（按 96 单元分类）

Status: Done

Approval: 用户于 2026-08-01 指令“执行任务1-5”，明确包含批准 F0037 及按批准规格实现。

## 1. 目标与原则

以 Task 19 权威 tracker 的 96 个单元为索引设计 Humanlike v2 参数面板。参数分为四级：

- `EDITABLE`：玩家风格/启发式参数，可按 s0-s3 独立设置。
- `ADVANCED`：高级实验参数，默认折叠并受范围/联动校验。
- `READ_ONLY`：规则、状态、算法基础、模型版本、审计和训练契约，只展示当前值/hash。
- `HIDDEN_RUNTIME`：隐藏真值、运行时记忆、随机流内部状态和隐私数据，不进入编辑 UI。

总体原则：规则正确性、合法性、信息边界、确定性、账本和审计不可通过“人类化参数”关闭；Humanlike 只能改变合法候选之间的偏好、搜索预算和有界扰动。

## 2. 分类概览

完整逐单元多对多清单见：

- `docs/features/F0037_96_unit_parameter_matrix.md`
- `docs/features/F0037_96_unit_parameter_matrix.csv`
- `docs/features/F0037_parameter_step_categories.md`
- `docs/features/F0037_parameter_step_categories.csv`
- `docs/features/F0037_leaf_parameter_matrix.md`
- `docs/features/F0037_leaf_parameter_matrix.csv`
- `docs/features/F0037_rp_leaf_schema.md`

矩阵由权威 `parameter_registry.csv.consumer_unit_ids` 反向生成，不将 RP 运行态误当成可编辑 UI 参数；每个参数另标注其主要“作用步骤类别”。

| 类别 | 单元数 | 设置策略 | 主要参数页 |
|---|---:|---|---|
| RULE | 16 | 房规只读；少量策略响应偏好独立于规则 | 规则摘要、响应偏好 |
| STATE | 12 | schema/状态机只读；认知生命周期可配置 | 认知状态、跨局记忆、崩溃回退 |
| ALGO | 11 | 编码/白名单/seed 锁定；评价预算和候选上限高级可调 | 候选、评价、随机性 |
| SCORE | 6 | 权威计分只读；策略对分值/名次的效用可调 | 比分效用 |
| HEUR | 23 | Humanlike 核心可编辑区 | 开局、计划、攻防、记忆、人格、节奏 |
| MODEL | 5 | 模型合同/版本只读；公开信息模型阈值高级可调 | 对手模型、模型产物 |
| TRAIN | 9 | 生产参数只读；训练专用域随机化另页 | 训练与评估 |
| AUDIT | 14 | 全部只读或开关仅能增加记录，不能关闭强制证据 | 审计与追踪 |

## 3. 全部参数的作用步骤、类型、取值范围与公式

下表是主方案的组成部分。作用步骤类别表示参数在牌局生命周期中主要发挥作用的位置；类型、取值范围或公式直接取自 Task 19 权威参数注册表。GP 是可冻结配置组，RP 是运行态组且默认只读。RP 的公式描述状态如何派生或更新，不代表可由用户直接输入。一个参数可以被多个 96 单元消费。

| 参数     | 名称        | 参数种类    | 作用步骤类别            | 类型、取值范围或公式                                                                                                                                                                                                                           |
| ------ | --------- | ------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| GP-001 | 规则版本      | 全局配置 GP | 配置加载与整场初始化        | 字符串与布尔值；`rule_version="CDMJ-AI-RULES 1.0.0"`；`parameter_version="CDMJ-AI-PARAMS 1.0.0"`；`locked=true`。不允许空值。                                                                                                                         |
| GP-002 | 规则集标识     | 全局配置 GP | 配置加载与整场初始化        | 枚举与字符串；`ruleset="chengdu_xuezhan_daodi"`为必选；`platform_ruleset_id`长度1—128字符；可选扩展列表长度0—64。                                                                                                                                             |
| GP-003 | 整场游戏配置    | 全局配置 GP | 整场初始化与跨局控制        | 结构体；`total_rounds`整数1—10000；`starting_score`整数-1,000,000,000—1,000,000,000；排名方式为`total_score`、`rank_points`或`custom`；提前结束阈值可关闭，开启时与得分使用相同范围。                                                                                         |
| GP-004 | 牌组配置      | 全局配置 GP | 牌墙构建与发牌           | 固定牌组结构；花色只能为`wan`、`tong`、`tiao`；点数1—9；每种牌4张；牌种27种；总牌数固定108。规则版本1.0.0不允许扩展牌。                                                                                                                                                          |
| GP-005 | 换三张配置     | 全局配置 GP | 换三张               | 布尔、整数和枚举；`enabled`为布尔值；启用时`exchange_count=3`、`same_suit_required=true`；方向为`left`、`right`、`opposite`、`dice`或`random`；来源可见性由[GP-021](#gp-021)控制。                                                                                       |
| GP-006 | 定缺配置      | 全局配置 GP | 定缺                | 布尔和枚举；`enabled=true`；缺门只能为`wan`、`tong`、`tiao`；`force_discard_missing_suit`为布尔值；`allow_hu_before_cleared=false`；定缺提交时限服从[GP-022](#gp-022)。                                                                                            |
| GP-007 | 基本动作配置    | 全局配置 GP | 行牌与合法动作           | 动作开关集合；`draw`、`discard`、`peng`、`ming_gang`、`an_gang`、`bu_gang`、`qiang_gang_hu`取`true/false`；`chi=false`为锁定值。                                                                                                                         |
| GP-008 | 多人响应优先级   | 全局配置 GP | 多人响应解析            | 有序枚举；`hu`必须高于碰杠；`gang`与`peng`的先后由平台规则明确，允许`hu > gang > peng > pass`或`hu > peng/gang_by_seat > pass`；`multi_hu`取`true/false`；同级座位优先为`nearest_from_discarder`或平台确定性顺序。                                                                 |
| GP-009 | 胡牌权限配置    | 全局配置 GP | 胡牌资格与响应           | 枚举和整数；过胡模式为`none`、`until_self_draw`、`until_value_increase`或`platform_custom`；点炮、自摸、抢杠胡可放弃开关为布尔值；强制胡牌剩余张阈值为整数0—4，0表示关闭。                                                                                                               |
| GP-010 | 牌墙与终止配置   | 全局配置 GP | 牌墙推进与终局判定         | 整数和枚举；总牌数固定108；四家发牌共53张后，标准剩余牌墙为55张；终止胡牌家数固定3；保留尾牌数0—16；杠后补牌来源为`wall_tail`或平台指定位置。                                                                                                                                                   |
| GP-011 | 番型目录      | 全局配置 GP | 番型识别与结算           | 番型数组；番型数量1—128；每个番型ID长度1—64字符且唯一；启用状态为布尔值；成立条件必须能由公开规则和手牌状态确定。                                                                                                                                                                       |
| GP-012 | 番型关系      | 全局配置 GP | 番型识别与结算           | 关系矩阵；任意番型对关系取`compatible`、`exclusive`、`contains`或`independent`；矩阵规模与[GP-011](#gp-011)一致；关系不得循环矛盾。                                                                                                                                    |
| GP-013 | 番数和封顶配置   | 全局配置 GP | 番型识别与结算           | 整数结构体；单番值0—64；基础分1—1,000,000；封顶番0—64，0表示不按番封顶；单次结算绝对值不得超过1,000,000,000；封顶外杠分开关为布尔值。                                                                                                                                                  |
| GP-014 | 自摸结算配置    | 全局配置 GP | 胡牌计分              | 枚举和整数；自摸模式为`add_base`、`add_fan`、`fixed_bonus`或`none`；附加番0—16；固定奖励0—1,000,000；支付范围为`all_active_opponents`或平台指定集合。                                                                                                                     |
| GP-015 | 杠分配置      | 全局配置 GP | 杠牌计分              | 整数和枚举；明杠、暗杠、补杠单位分各为0—1,000,000；支付方式为`discarder_only`、`all_active_opponents`或`custom`；结算时点为`immediate`或`round_end`。                                                                                                                   |
| GP-016 | 呼叫转移配置    | 全局配置 GP | 呼叫转移结算            | 布尔和枚举；`enabled`为布尔值；转移范围为`latest_gang_only`、`all_related_gang_score`或`custom`；一炮多响方式为`copy_to_each_winner`、`split`或`custom`。                                                                                                         |
| GP-017 | 查花猪配置     | 全局配置 GP | 终局花猪结算            | 布尔和整数；`enabled`为布尔值；花猪赔付番0—64或固定分0—1,000,000；支付对象为`all_non_hu_non_huazhu`、`all_eligible`或`custom`。                                                                                                                                   |
| GP-018 | 查大叫配置     | 全局配置 GP | 终局查大叫             | 布尔和枚举；`enabled`为布尔值；死叫处理为`valid`或`invalid`；估值方式为`actual_live_wait`、`maximum_possible_fan`或`custom`；赔付上限服从[GP-013](#gp-013)。                                                                                                          |
| GP-019 | 退税配置      | 全局配置 GP | 终局退税              | 布尔和枚举；`enabled`为布尔值；退回范围为`all_gang_income`、`untransferred_gang_income`、`selected_events`或`custom`；退回额不能超过对应已入账额。                                                                                                                     |
| GP-020 | 庄家配置      | 全局配置 GP | 庄家与座位管理           | 枚举和整数；定庄方式为`dice`、`rotate`、`winner`或`custom`；庄家加番0—16；庄家固定加分0—1,000,000；连庄次数0—10000，0表示不连庄。                                                                                                                                          |
| GP-021 | 信息可见性配置   | 全局配置 GP | PlayerView构建与信息隔离 | 可见性开关集合；每个信息项取`hidden`、`public_exact`或`public_partial`；AI可见级别不得高于人类界面；部分可见项必须定义公开粒度。                                                                                                                                                 |
| GP-022 | 时间控制配置    | 全局配置 GP | 决策时间控制与超时回退       | 时间结构体；出牌时限250—600000毫秒；响应时限250—600000毫秒；表现延迟0—时限的80%；超时动作为`auto_pass`、`auto_hu`、`safe_discard`或平台合法默认值。                                                                                                                              |
| GP-023 | AI玩家基础档案  | 全局配置 GP | 玩家初始化与人格策略        | AI档案结构体；水平为`novice`、`normal`、`skilled`、`expert`；风格为`conservative`、`balanced`、`aggressive`；所有连续特征取0—1；四名玩家档案数量固定4。                                                                                                                    |
| GP-024 | 记忆与学习配置   | 全局配置 GP | 认知记忆与跨局学习         | 记忆结构体；初始记忆强度0—1；遗忘率0—1；事件显著度0—1；跨局历史长度0—10000局；隐藏信息学习开关固定为`false`。                                                                                                                                                                   |
| GP-025 | 人类化行为配置   | 全局配置 GP | 候选评价与人类化选择        | 人类化结构体；情绪稳定度、习惯强度、失误概率上限、近似随机强度均为0—1；随机种子为0—\(2^{64}-1\)的整数；相同种子和相同输入必须可复现。                                                                                                                                                          |
| GP-026 | 有限认知配置    | 全局配置 GP | 有限注意、搜索与思考节奏      | 认知结构体；最大候选数1—14；最小候选数1—最大候选数；搜索深度0—8层；注意力容量1—64项；满意停止阈值0—1；重新搜索阈值0—1；决策权重各为0—1且总和必须为1。                                                                                                                                               |
| GP-027 | 收益与比赛目标配置 | 全局配置 GP | 比分、名次与整场效用        | 目标结构体；单局收益、整场收益、排名、风险和稳定性权重各为0—1且总和为1；目标名次1—4；领先或落后触发分差0—1,000,000,000。                                                                                                                                                              |
| RP-001 | 本局标识      | 运行态 RP  | 本局初始化与审计标识        | 结构体；`round_index`为1—[GP-003](#gp-003)总局数；事件序号0—1,000,000；开局时\(round\_index=previous\_round+1\)，\(t=0\)；每处理一个原子事件后\(t\leftarrow t+1\)。                                                                                                |
| RP-002 | 座位与庄家状态   | 运行态 RP  | 本局初始化与座位管理        | 玩家编号0—3；活动顺序长度1—4；初始座位由[GP-020](#gp-020)产生。玩家\(p\)胡牌后，\(Active_t=Active_{t-1}\setminus\{p\}\)，下一玩家为当前顺序中下一名仍在\(Active_t\)的玩家。                                                                                                        |
| RP-003 | 当前比分与本局目标 | 运行态 RP  | 整场比分到本局目标转换       | 四人整数分数；单项-1,000,000,000—1,000,000,000；目标强度0—1；\(Score_t(p)=\operatorname{clip}(Score_{t-1}(p)+\Delta_t(p),-10^9,10^9)\)。分差\(Gap_t(p,q)=Score_t(p)-Score_t(q)\)。求稳或追分强度由分差、剩余局数和[GP-027](#gp-027)目标归一化到0—1。                           |
| RP-004 | 初始手牌      | 运行态 RP  | 发牌后初始分析           | 27维整数向量；各维0—4；总张数庄家14、闲家13；\(H_0(x)=DealCount(x)\)，并满足\(\sum_xH_0(x)\in\{13,14\}\)。初始结构由[RP-016](#rp-016)的结构函数计算。                                                                                                                    |
| RP-005 | 换三张状态     | 运行态 RP  | 换三张决策与执行          | 换出、换入各3张；方向枚举；\(H_{after}(x)=H_{before}(x)-Out(x)+In(x)\)，其中\(\sum_xOut(x)=\sum_xIn(x)=3\)，且换出牌满足[GP-005](#gp-005)的同花色约束。                                                                                                            |
| RP-006 | 四家定缺状态    | 运行态 RP  | 定缺决策与清缺约束         | 四个花色枚举；清缺概率0—1；自己清缺为确定布尔值；自己的缺门剩余数\(M_t=\sum_{x\in missingSuit}H_t(x)\)，自己清缺状态\(Cleared_t=I(M_t=0)\)。对手清缺状态只能依据公开弃牌形成置信度，不得使用其隐藏手牌。                                                                                                  |
| RP-007 | 当前手牌      | 运行态 RP  | 摸牌、出牌与手牌分析        | 27维整数向量；各维0—4；手牌总数依动作合法变化；\(H_t=H_{t-1}+Draw_t-Discard_t-RemoveToMeld_t\)。碰牌、明杠、暗杠和补杠分别按规则从手牌移入公开或隐藏组合；杠后补牌作为新的\(Draw_t\)事件处理。                                                                                                       |
| RP-008 | 公开组合状态    | 运行态 RP  | 碰杠后公开组合更新         | 每名玩家公开组合0—4组；类型枚举；\(Melds_t(p)=Melds_{t-1}(p)\cup NewMeld_t(p)\)。补杠时将对应碰组状态由`peng`替换为`bu_gang`，不得同时保留两个重复组。                                                                                                                          |
| RP-009 | 弃牌历史      | 运行态 RP  | 弃牌事件与行为序列更新       | 事件列表；长度0—108加杠后动作扩展；\(Discards_t=Discards_{t-1}\mathbin{\Vert}(p,x,t,source,time)\)，其中不可见字段按[GP-021](#gp-021)置为空，而不是填入服务器真实值。                                                                                                        |
| RP-010 | 可见牌统计     | 运行态 RP  | 可见牌聚合与活牌估计        | 27维整数向量；各维0—4；\(V_t(x)=H_t(x)+D_t(x)+OpenMeld_t(x)+PublicHu_t(x)+PublicGang_t(x)\)，重复展示的同一实体牌只计一次。未见上界\(U_t(x)=4-V_t(x)\)。                                                                                                           |
| RP-011 | 牌墙与轮次状态   | 运行态 RP  | 牌墙推进与阶段判断         | 牌墙余量0—108；轮次0—1,000,000；估计上下界0—108；精确可见时\(W_t=W_{t-1}-DrawCount_t\)。不可见时维护区间：\(W_t^{min}=W_{t-1}^{min}-MaxDraw_t\)，\(W_t^{max}=W_{t-1}^{max}-MinDraw_t\)，并限制在0—108。                                                                  |
| RP-012 | 存活玩家与胡牌状态 | 运行态 RP  | 血战胡后状态与终止判断       | 活动玩家集合大小1—4；胡牌顺序0—3；\(Active_t=Active_{t-1}\setminus Winners_t\)。每名新赢家的胡牌序号为此前已胡人数加1；一炮多响按同一事件记录相同时间但独立序号或平台并列规则。                                                                                                                    |
| RP-013 | 当前事件      | 运行态 RP  | 当前原子事件处理          | 单事件结构体；类型枚举；\(Event_t=(type,actor,tile,source,timestamp,publicPayload)\)。类型只能为`deal`、`exchange`、`dingque`、`draw`、`discard`、`peng`、`gang`、`hu`、`settlement`或平台已注册扩展。                                                                  |
| RP-014 | 合法行动与响应窗口 | 运行态 RP  | 合法候选与响应窗口         | 合法行动集合；大小1—20；截止时间戳；\(Legal_t=RuleEngine(State_t,[GP\text{-}002\ldots GP\text{-}022])\)。候选集必须满足\(Candidates_t\subseteq Legal_t\)。                                                                                                    |
| RP-015 | 过胡与权限状态   | 运行态 RP  | 过胡与胡牌权限判断         | 状态枚举；状态为`free`、`passed_hu_locked`、`value_limited`或`forced_hu`。状态转移由[GP-009](#gp-009)定义：过胡事件进入锁定态，规定的自摸或价值变化事件恢复为`free`。                                                                                                              |
| RP-016 | 手牌结构状态    | 运行态 RP  | 手牌结构与向听分析         | 结构体；向听数-1—13；组合数0—4；对子数0—7；结构质量0—1；对每个允许牌型\(k\)计算向听数\(S_k(H_t,Melds_t)\)，总体向听\(S_t=\min_k S_k\)。胡牌时\(S_t=-1\)，听牌时\(S_t=0\)。结构质量由有效搭子、对子用途和重叠结构归一化到0—1。                                                                               |
| RP-017 | 当前做牌计划    | 运行态 RP  | 做牌计划形成与切换         | 方向枚举及置信度0—1；主计划1个；备选计划0—3个；对方向\(d\)：\(C_t(d)=\operatorname{Normalize}((1-\alpha_d)C_{t-1}(d)+\alpha_dE_t(d))\)，\(\alpha_d\in[0,1]\)来自[GP-026](#gp-026)，\(E_t(d)\in[0,1]\)为本轮证据。最高置信方向为主方向，但受规则中的观察、确定和放弃阈值约束。                        |
| RP-018 | 听牌与活牌状态   | 运行态 RP  | 听牌、等待与活牌评估        | 等待集合0—27种；单牌未见数0—4；总活牌0—108；概率0—1；对等待牌\(x\)，\(Live_t(x)=\max(0,4-V_t(x))\)。总活牌\(L_t=\sum_{x\in Wait_t}Live_t(x)\)。若\(L_t=0\)，则`dead_wait=true`。下一次从未知牌中获得任一等待牌的近似概率为\(P_{next}=\frac{L_t}{\sum_xU_t(x)}\)。                           |
| RP-019 | 对手推测状态    | 运行态 RP  | 逐对手方向与牌型推测        | 每名对手的假设概率分布；各概率0—1且和为1；对假设\(h\)和新公开证据\(e_t\)：\(P_t(h)=\frac{P(e_t\mid h)P_{t-1}(h)}{\sum_jP(e_t\mid h_j)P_{t-1}(h_j)+\varepsilon}\)。证据似然只能由公开行为模型产生。                                                                                 |
| RP-020 | 威胁与安全状态   | 运行态 RP  | 威胁、放铳损失与安全评估      | 每名对手、每种牌的风险0—1；综合风险0—1；\(R_t(p,x)=P_t(p\text{已听})\times P_t(x\text{为其等待}\mid p\text{已听})\times LossNorm_t(p)\)。多家综合风险\(R_t(x)=1-\prod_{p\in Active_t,p\ne self}(1-R_t(p,x))\)。                                                       |
| RP-021 | 剩余机会状态    | 运行态 RP  | 逐座剩余摸牌机会估计        | 剩余摸牌次数0—108；时间压力0—1；若轮转稳定，自己的近似剩余摸牌数\(N_t^{self}=\left\lceil\frac{W_t-offset_t}{\lvert Active_t\rvert}\right\rceil\)，其中\(offset_t\)为轮到自己前的活动玩家数。碰杠和胡牌后按新顺序重新计算。时间压力\(Pressure_t=1-\frac{N_t^{self}}{N_{start}^{self}+\varepsilon}\)。 |
| RP-022 | 牌局阶段      | 运行态 RP  | 早中晚局阶段判定          | 枚举；阶段强度0—1；剩余比例\(q_t=W_t/W_{start}\)。默认：\(q_t>0.70\)为`early`，\(0.35<q_t\le0.70\)为`middle`，\(0.10<q_t\le0.35\)为`late`，\(q_t\le0.10\)为`endgame`。阈值可在[GP-026](#gp-026)内调整，但必须单调。                                                        |
| RP-023 | 候选行动集合    | 运行态 RP  | 候选生成、裁剪与排序        | 候选集合；数量1—[GP-026](#gp-026)最大候选数；\(Candidates_t=Prune(Legal_t,Plan_t,Attention_t,Profile)\)。必须保留所有规则强制行动；其余按显著度排序截取前\(K\)项，\(K\)由水平和局面复杂度在配置范围内确定。                                                                                    |
| RP-024 | 当前注意力状态   | 运行态 RP  | 有限注意分配            | 注意力对象权重0—1；权重和为1；对象数不超过注意力容量；对对象\(i\)，\(A_t(i)=\frac{\exp(Salience_t(i)/\tau)}{\sum_j\exp(Salience_t(j)/\tau)}\)，温度\(\tau\in[0.05,5]\)由[GP-026](#gp-026)配置。只保留权重最高的注意力容量项。                                                           |
| RP-025 | 当前记忆状态    | 运行态 RP  | 有限记忆衰减与强化         | 每条记忆强度0—1；记忆条目0—10000；\(M_t(i)=\operatorname{clip}(M_{t-1}(i)e^{-\lambda\Delta t}+\rho\cdot Salience_t(i),0,1)\)，\(\lambda,\rho\in[0,1]\)来自[GP-024](#gp-024)。回忆成功率等于当前记忆强度；隐藏信息不得创建记忆条目。                                             |
| RP-026 | 当前搜索状态    | 运行态 RP  | 有限推演与满意停止         | 搜索深度0—8；已检查数0—候选数；停止质量0—1；实际深度\(D_t=\min(D_{profile},D_{time},D_{complexity})\)。当最佳候选满意度\(Sat(best)\ge\theta_{stop}\)、全部候选检查完成或剩余时间达到安全阈值时停止。                                                                                        |
| RP-027 | 本次操作剩余时间  | 运行态 RP  | 思考预算与剩余时间         | 毫秒整数0—[GP-022](#gp-022)时限；\(TimeLeft_t=\max(0,Deadline_t-Now_t)\)。当\(TimeLeft_t\le DefaultMargin\)时调用合法默认动作；`DefaultMargin`范围0—时限的50%。                                                                                               |
| RP-028 | 当前人格与情绪修正 | 运行态 RP  | 人格、水平与情绪修正        | 情绪和风格偏移-1—1；0为基础档案；\(E_t=\operatorname{clip}(\gamma E_{t-1}+\beta Outcome_t,-1,1)\)，\(\gamma\in[0,1]\)为情绪保留率，\(\beta\in[0,1]\)为事件影响率，\(Outcome_t\in[-1,1]\)为标准化结果。                                                                   |
| RP-029 | 行动历史与决策记录 | 运行态 RP  | 动作选择、解释与决策审计      | 追加日志；条目0—1,000,000；\(Trace_t=Trace_{t-1}\mathbin{\Vert}Record_t\)。记录必须包含事件号、可见输入快照哈希、候选、选择、理由、搜索停止原因和随机种子位置。                                                                                                                         |
| RP-030 | 本局计分事件    | 运行态 RP  | 局内计分事件处理          | 四人计分账本；单项-1,000,000,000—1,000,000,000；\(Ledger_t(p)=Ledger_{t-1}(p)+HuDelta_t(p)+GangDelta_t(p)+TransferDelta_t(p)\)。每个零和结算事件应满足\(\sum_p\Delta_t(p)=0\)，平台非零和奖励须单独标记。                                                                |
| RP-031 | 终局公开信息    | 运行态 RP  | 终局公开信息与审计         | 公开信息集合；最多108张及相关状态；\(Reveal_t=Reveal_{t-1}\cup PublicPayload(Event_t,GP\text{-}021)\)。公开集合只能增加；错误撤回必须作为带版本的更正事件处理。                                                                                                                   |
| RP-032 | 本局结算结果    | 运行态 RP  | 单局结算与整场累计         | 四人最终本局分；单项-1,000,000,000—1,000,000,000；\(RoundResult(p)=Ledger_{end}(p)+HuazhuDelta(p)+DajiaoDelta(p)+TaxRefundDelta(p)+OtherLegalDelta(p)\)，其中退税支付者为负、接收者为正，并应用[GP-013](#gp-013)规定的封顶顺序。通常要求四人总和为0。                                 |
| RP-033 | 跨局学习输出    | 运行态 RP  | 跨局画像学习与训练输出       | 学习输出向量；每个特征0—1；历史长度受[GP-024](#gp-024)限制；对可学习特征\(f\)：\(Profile_{next}(f)=(1-\eta)Profile_{prev}(f)+\eta Observation_t(f)\)，\(\eta\in[0,1]\)。未公开信息对应的\(Observation\)必须为空且不得参与更新。                                                       |
## 4. RULE（16）

| 单元 | 设置建议 |
|---|---|
| RULE-001 | `READ_ONLY`：规则优先级、合法性优先、禁止吃牌；显示 ruleset hash |
| RULE-002 | `READ_ONLY` 合法性；`EDITABLE` 换牌结构保护、危险传递权重 |
| RULE-003 | `READ_ONLY`：缺门未清强制弃牌，不允许关闭 |
| RULE-004 | `READ_ONLY`：死叫与胡牌资格；策略仅可调整做叫偏好 |
| RULE-005 | `READ_ONLY`：座位、庄家和活动顺序 |
| RULE-006 | `READ_ONLY`：摸牌/响应/出牌顺序 |
| RULE-007 | `EDITABLE`：碰牌倾向、结构破坏容忍、碰后速度收益阈值 |
| RULE-008 | `EDITABLE`：明杠/暗杠/补杠风险偏好；资格与执行只读 |
| RULE-009 | `READ_ONLY` 抢杠窗口；`EDITABLE` 补杠风险惩罚 |
| RULE-010 | `READ_ONLY` 胡牌资格；`EDITABLE` 可选胡/做大取舍（强制胡除外） |
| RULE-011 | `READ_ONLY`：过胡设置/恢复语义；可显示当前状态但不可直接编辑运行态 |
| RULE-012 | `READ_ONLY`：强制胡与末段必胡 |
| RULE-013 | `READ_ONLY`：多人响应优先级 |
| RULE-014 | `READ_ONLY`：血战退出、继续与终止 |
| RULE-015 | `READ_ONLY` 番型/封顶；`EDITABLE` 番型追求偏好，不改变计分 |
| RULE-016 | `READ_ONLY`：公开信息范围；隐藏信息开关固定 false |

## 5. STATE（12）

| 单元 | 设置建议 |
|---|---|
| STATE-001 | `READ_ONLY`：整场冻结配置和玩家装配摘要 |
| STATE-002 | `READ_ONLY`：权威 RoundState 和访问控制 |
| STATE-003 | `READ_ONLY`：手牌/副露/定缺/过胡运行态 |
| STATE-004 | `READ_ONLY`：状态机和恢复策略；显示异常计数 |
| STATE-005 | `READ_ONLY`：PlayerView version、config hash |
| STATE-006 | `EDITABLE`：每局认知初始化、跨局保留强度、归档容量 |
| STATE-007 | `READ_ONLY`：存档 schema 与迁移版本 |
| STATE-008 | `EDITABLE`：跨局比分敏感度、公开印象保留局数 |
| STATE-009 | `ADVANCED`：思考时间上下限、决策预算；请求生命周期只读 |
| STATE-010 | `READ_ONLY` GP/RP 注册；profile 字段进入对应页面编辑 |
| STATE-011 | `READ_ONLY`：牌墙、洗牌、发牌和 game_id seed |
| STATE-012 | `ADVANCED`：AI 超时阈值；合法 fallback 策略只读 |

## 6. ALGO（11）

| 单元 | 设置建议 |
|---|---|
| ALGO-001 | `READ_ONLY`：牌编码与所有权守恒 |
| ALGO-002 | `READ_ONLY` 算法；`ADVANCED` 标准/七对/清一色方向效用权重 |
| ALGO-003 | `READ_ONLY`：可见牌去重和未见牌聚合 |
| ALGO-004 | `ADVANCED`：活牌估计保守系数、区间使用偏好 |
| ALGO-005 | `ADVANCED`：逐座摸牌机会折扣 |
| ALGO-006 | `ADVANCED`：候选上限、近似候选阈值；mandatory 永不裁剪 |
| ALGO-007 | `EDITABLE`：六分量 Q 权重（速度/价值/防守/灵活性/计划/认知成本），合计和范围强校验 |
| ALGO-008 | `EDITABLE`：噪声幅度、近似池阈值、思考时间；seed 派生算法只读 |
| ALGO-009 | `READ_ONLY`：版本、迁移、canonical hash |
| ALGO-010 | `READ_ONLY`：PlayerView 白名单 |
| ALGO-011 | `READ_ONLY`：game_id 到牌墙/骰子/随机流映射 |

## 7. SCORE（6）

| 单元 | 设置建议 |
|---|---|
| SCORE-001～005 | `READ_ONLY`：账本、胡/杠/终局调整、封顶和结算顺序；仅显示规则摘要 |
| SCORE-006 | `EDITABLE`：领先/落后敏感度、名次效用、剩余局权重；不得改变真实分数 |

## 8. HEUR（23，核心编辑区）

| 单元 | 建议参数组 |
|---|---|
| HEUR-001 | 换牌：弱张、对子/刻子/顺子保护、送牌危险、来源线索权重 |
| HEUR-002 | 定缺：数量、孤张、结构损失、清一色潜力、清缺成本 |
| HEUR-003 | 动态风格：保守/平衡/激进基线与切换敏感度 |
| HEUR-004 | 初始方向：速度/价值/七对/清一色/普通型权重 |
| HEUR-005 | 主备计划：惯性、重启阈值、备用计划数量 |
| HEUR-006 | 缺门环境：剩余量、对手压力、预计清缺轮数 |
| HEUR-007 | 逐家方向更新：公开事件显著度、置信衰减 |
| HEUR-008 | 整场效用：比分差、剩余局、名次风险敏感度 |
| HEUR-009 | 血战顺序：先胡/做大/继续收益权重 |
| HEUR-010 | 多目标冲突：复核阈值、最大复核候选数 |
| HEUR-011 | 番型边际价值：目标番型偏好与机会成本 |
| HEUR-012 | 碰牌：速度收益、结构损失、暴露成本、防守影响 |
| HEUR-013 | 杠牌：即时收益、放铳/抢杠风险、牌墙变化 |
| HEUR-014 | 出牌：向听、进张、形状、结构保护、计划一致性 |
| HEUR-015 | 防守：危险容忍、安全牌权重、领先时防守增益 |
| HEUR-016 | 行为推断：观察窗口、证据权重、最低置信度 |
| HEUR-017 | 思考节奏：基础时长、复杂度系数、抖动幅度 |
| HEUR-018 | 信息表达：安全牌储备、扣牌倾向、暴露成本 |
| HEUR-019 | 注意：Top-K、温度、显著度阈值 |
| HEUR-020 | 记忆：容量、初始强度、衰减率、强化率、跨局长度 |
| HEUR-021 | 有限推演：深度/宽度/预算、满意停止阈值 |
| HEUR-022 | 人格与状态：level、style、碰/杠/大牌偏好、防守意识、计划坚持、思考速度、情绪上限 |
| HEUR-023 | 人类失误：近似分差、选择温度、最大噪声；合法性和明显优势保护锁定 |

## 9. MODEL（5）

| 单元 | 设置建议 |
|---|---|
| MODEL-001 | `ADVANCED`：公开方向假设先验、更新率、最低样本；数据来源只读 `SIMULATION/HUMAN` |
| MODEL-002 | `ADVANCED`：听牌概率阈值、等待损失权重、fallback 强度 |
| MODEL-003 | `EDITABLE`：公开画像保留局数、衰减、最小置信度；玩家身份不可手工伪造 |
| MODEL-004 | `READ_ONLY`：训练输入输出 schema、feature version |
| MODEL-005 | `READ_ONLY`：模型 artifact/hash/冻结/外部评价状态；仅允许选择已批准 artifact |

## 10. TRAIN（9）

| 单元 | 设置建议 |
|---|---|
| TRAIN-001～008 | `READ_ONLY`：生产规则复用、Observation、codec/mask、非法动作、reward、env、自博弈、BC/RL 合同；训练页面只显示版本和状态 |
| TRAIN-009 | `ADVANCED` 且训练专用：房规/profile/行为域随机化范围；不得影响普通对局默认配置 |

## 11. AUDIT（14）

| 单元 | 设置建议 |
|---|---|
| AUDIT-001～005 | `READ_ONLY` 强制日志、解释、hash、回放、不变量；允许增加详细度，不允许关闭最低证据 |
| AUDIT-006～011 | `READ_ONLY` 测试、属性、golden、回归、追踪、发布完整性状态 |
| AUDIT-012 | `READ_ONLY` 外部评价状态；未评价必须明确显示 `NOT_EVALUATED` |
| AUDIT-013 | `READ_ONLY` 模块依赖与信息流边界 |
| AUDIT-014 | `ADVANCED`：保留期限、脱敏级别、导出范围；必须满足隐私/新鲜度下限 |

## 12. GP-023 十二种人格预设

### 12.1 组合模型

人格预设由 `level × style` 笛卡尔积组成，共 4 × 3 = 12 种。预设不是新的持久化字段，而是对现有 `players[s].profile`、GP-025 和 GP-026 叶字段的一次原子赋值：

- `level` 决定认知能力、候选容量、搜索深度、注意容量和最大误差。
- `style` 决定碰/杠/做大/防守/计划/速度偏好，以及评价权重和满意停止基线。
- UI 根据当前字段是否与某个预设完全相等，派生显示 `preset_id`；`preset_id` 不写入 JSON。
- 用户修改任一预设控制字段后，派生显示立即变成 `custom`，但保留当前 `level`、`style` 标签。
- 再次选择预设时，必须先展示将被覆盖字段的差异，确认后一次性写入同一座位；不得部分写入。

### 12.2 水平基线

| level | 候选范围 `min/max` | 搜索深度 | 注意容量 | 满意阈值基线 | 最大误差概率 | 近似随机强度 | 功能差异 |
|---|---|---:|---:|---:|---:|---:|---|
| `novice` | 2 / 6 | 1 | 8 | 0.62 | 0.060 | 0.12 | 搜索浅、观察少、较早停止、近似选择误差最多 |
| `normal` | 3 / 8 | 2 | 12 | 0.72 | 0.040 | 0.08 | 当前默认中等认知预算 |
| `skilled` | 4 / 10 | 3 | 16 | 0.77 | 0.025 | 0.05 | 搜索更深、注意更广、噪声更低 |
| `expert` | 5 / 12 | 4 | 20 | 0.82 | 0.015 | 0.03 | 最高预设预算和最低误差，仍受合法性及时间门禁约束 |

`search_depth` 的有效值固定为：

\[
D_{effective}=\min(D_{configured},D_{level}),\quad
D_{level}\in\{novice:1,normal:2,skilled:3,expert:4\}.
\]

本映射补足 Task 19 “水平影响搜索深度”的实现缺口。任何水平都必须保持合法动作率 100%，不得读取隐藏信息；水平只影响合法候选内的认知预算与有界误差。

### 12.3 风格基线

| style | 碰 | 杠 | 做大 | 防守 | 计划坚持 | 思考速度 | 满意阈值修正 | 决策权重 `速度/价值/防守/灵活` |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `conservative` | 0.35 | 0.30 | 0.25 | 0.80 | 0.70 | 0.50 | -0.04 | 0.25 / 0.20 / 0.40 / 0.15 |
| `balanced` | 0.50 | 0.50 | 0.45 | 0.55 | 0.55 | 0.55 | 0.00 | 0.35 / 0.25 / 0.25 / 0.15 |
| `aggressive` | 0.70 | 0.75 | 0.75 | 0.35 | 0.45 | 0.65 | +0.04 | 0.40 / 0.35 / 0.10 / 0.15 |

风格预设还写入 GP-025：`emotional_stability` 分别为 0.85 / 0.70 / 0.55，`habit_strength` 分别为 0.65 / 0.55 / 0.45；`random_seed` 保留原座位值，不得被预设覆盖。GP-024 记忆和 GP-027 比赛目标不属于人格预设，不随预设变化。

### 12.4 十二种完整组合

组合值按“水平基线提供认知参数 + 风格基线提供人格与决策权重”构成；下表给出最终可观察效果。连续字段的精确值以 12.2、12.3 两表为准。

| preset_id | 水平 | 风格 | 主要效果 |
|---|---|---|---|
| `novice_conservative` | novice | conservative | 少量浅搜索、较早接受安全方案、碰杠和做大最低、误差最高 |
| `novice_balanced` | novice | balanced | 少量浅搜索、中性取舍、存在明显但有界的近似误差 |
| `novice_aggressive` | novice | aggressive | 少量浅搜索但偏碰杠做大，防守较低，容易呈现冲动进攻 |
| `normal_conservative` | normal | conservative | 中等搜索、显著防守和计划惯性，领先或危险时更稳健 |
| `normal_balanced` | normal | balanced | 当前默认基准，攻守、速度和计划惯性居中 |
| `normal_aggressive` | normal | aggressive | 中等搜索、偏碰杠和价值牌，较少选择防守动作 |
| `skilled_conservative` | skilled | conservative | 较深搜索配合高防守，减少无效副露和高风险杠 |
| `skilled_balanced` | skilled | balanced | 较深搜索、较低误差、综合牌效稳定 |
| `skilled_aggressive` | skilled | aggressive | 较深搜索后主动追求速度和价值，进攻并非盲目随机 |
| `expert_conservative` | expert | conservative | 最大搜索预算下控制风险，最少噪声，偏安全最优解 |
| `expert_balanced` | expert | balanced | 最大搜索预算、最低误差、综合评价最稳定 |
| `expert_aggressive` | expert | aggressive | 最大搜索预算下主动追求副露和做大，仍保留合法性与明显优势保护 |

### 12.5 冲突与继承规则

1. 选择预设时，GP-023 的 `level/style` 与六个连续人格字段、GP-025 的四个非 seed 行为字段、GP-026 的候选/搜索/注意/阈值/权重必须原子更新。
2. `random_seed`、GP-024、GP-027、规则配置、座位编号和画像名称不被预设覆盖；名称可由用户独立修改。
3. 字段与预设不完全匹配时显示 `custom`，禁止用标签假装参数仍属于预设。
4. `min_candidates <= max_candidates`，两组权重和均为 1；所有连续人格值必须在 0..1。
5. 强制动作、合法集合、信息隔离、计分和确定性审计优先于任何人格参数。

## 13. 实现方案与测试门禁

批准后按以下范围实施：

- 新增纯数据预设注册表，提供 12 个不可变预设和 `apply/detect/diff` 三个纯函数。
- 设置窗口在每个座位增加两级编号/下拉选择：水平、风格；展示派生预设名和覆盖差异，原子应用后仍允许叶字段微调。
- 认知策略增加 `search_depth` 的水平上限，并把有效深度写入 RP-026/决策 trace；不扩大合法候选集。
- 不新增配置 schema 字段，不修改参数版本；保存仍走 F0029 validator、原子替换、备份与 config hash。

验收测试：

1. 12 个预设均通过现有严格配置校验，权重和为 1，范围全部合法。
2. `apply` 只修改目标座位及规定字段，保留 seed、名称、GP-024、GP-027 和其他三座。
3. `detect(apply(preset)) == preset_id`；任一控制字段微调后返回 `custom`。
4. novice → expert 的有效候选、注意容量、搜索深度单调不降，噪声单调不升。
5. conservative → aggressive 的碰、杠、做大单调上升，防守和计划坚持单调下降。
6. 同 game_id、同预设和同 seed 可复现；12 个预设均保持合法动作率 100%。
7. UI 取消覆盖不改配置，确认覆盖后保存/重载一致；四座独立设置。
8. 回归运行 Humanlike v2 定向测试和全量测试，不改变 Task 19 `AUDITED` 状态。

## 14. UI 信息架构

建议页面顺序：`玩家画像` → `开局策略` → `计划与攻防` → `有限认知` → `对手模型` → `节奏与噪声` → `整场效用` → `规则/版本（只读）` → `训练（高级）` → `审计（只读）`。

每个字段必须显示：参数 ID、关联 unit、当前值、默认值、范围/枚举、作用座位、下局生效标记、锁定原因和测试引用。保存继续复用 F0029 的严格 validator、原子替换、备份和 config hash。

## 15. 下一阶段

1. 评审并批准 `F0037_rp_leaf_schema.md`，再按其拆分实现任务。
2. RP schema 实现不得把 GP-023 人格预设字段混入 RP 运行态合同。
