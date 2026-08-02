# Task 18B-R1：B1-A 实现设计独立复审

状态：**SUPERSEDED BY R3: IMPLEMENTATION_READY**  
范围：STATE-010、ALGO-009、ALGO-011；未修改业务代码、测试断言、Locked规格、Frozen契约或Task 17/18A状态。
当前回归基线：Windows Python 3.12.10，387 passed，0 failed，0 skipped，154.91s。

> 后续批准记录：2026-07-30九项决策均选择A并批准，决策版本`B1-A-DECISIONS 1.0.0`；Frozen v2提案随后以`B1-A-FROZEN-V2 1.0.0`批准。最终门禁结论以`B1-A_R3_readiness_review.md`的`IMPLEMENTATION_READY`为准。

## 技术结论

原Task 18B的`IMPLEMENTATION_READY`不能成立。原delta把生产语义、测试和证据混在同一编号中，AC使用同一句泛化条件，且对canonical数字/Unicode、迁移版本图、默认值与null、旧/新随机版本选择、并发逻辑坐标作了无来源推断。R1已拆为24条semantic delta、12条test delta和6条evidence delta；测试/证据不再计作生产语义完成。

STATE-010有可编码子集，但ALGO-009与ALGO-011的字节级/回放级选择会固化长期兼容行为。依据STATE-010规格§6“歧义必须新增决策记录，不静默推断”，B1-A整体在这些决策批准前不得开始编码。

## 三个单元的真实生产语义缺口

- **STATE-010**：缺完整60项ParameterDefinition、逐字段required/default/nullable、GP与match的冻结门禁、33项RP授权生命周期/归档、owner/seat隔离、统一事务/CAS/失败零写入、结果信封及策略投影。
- **ALGO-009**：现有loader不是Locked顺序；仅有单条兼容迁移；缺完整迁移图、废弃/extensions策略、逐字段缺省/null策略、数字与Unicode canonical bytes、统一错误/原子事务和明确fallback语义。
- **ALGO-011**：仅有legacy master+XOR三流；缺规范v2域隔离、版本选择、版本化流注册、纯逻辑坐标、无共享index的并发确定性、原子错误和SeedTrace安全投影。

## 必须先批准的规格决策

| 决策ID | 未冻结问题 | 影响单元 | 最小批准内容 |
|---|---|---|---|
| SPEC-DECISION-STATE-DEFAULTS | 60项逐字段 required/default/nullable 未完整冻结 | STATE-010, ALGO-009 | 逐字段三列和值；明确缺失与null |
| SPEC-DECISION-RP-ARCHIVE | RP归档载荷、保留期及跨局继承边界不完整 | STATE-010 | 33项archive/reset/carry规则 |
| SPEC-DECISION-MIGRATION-GRAPH | 支持版本的完整节点/逐边迁移/废弃字段图未冻结 | ALGO-009 | 每条from→to及字段变换golden |
| SPEC-DECISION-EXTENSIONS | extensions元素schema、排序、hash和迁移策略未冻结 | ALGO-009 | 容器schema及canonical参与规则 |
| SPEC-DECISION-CANONICAL-NUMBER | float/Decimal/整数/-0/指数准确字节规则未冻结 | ALGO-009 | 选定算法和跨语言golden |
| SPEC-DECISION-CANONICAL-UNICODE | Unicode正规化、转义及键序基准未冻结 | ALGO-009 | NFC与否、码点/UTF-16/UTF-8排序、转义golden |
| SPEC-DECISION-CONFIG-FALLBACK | 启动/热重载失败是否继续旧配置未冻结 | ALGO-009 | 两场景的accepted/active/error语义 |
| SPEC-DECISION-RNG-VERSION | 缺省版本、旧/新回放版本选择未冻结 | ALGO-011 | 新录制、旧缺字段、新回放各选择规则 |
| SPEC-DECISION-RNG-COORDINATE | consumer/logical index坐标schema未冻结 | ALGO-011 | 坐标字段、稳定ID与重试语义 |


## STATE-010：60个准确参数ID与生命周期来源

ID闭集为`GP-001..GP-027`和`RP-001..RP-033`，准确展开如下。字段具体范围以parameter_registry.csv为准；该表有range/lifecycle，但没有把每个嵌套字段完整结构化为required/default/nullable，因此不能由实现者补猜。

| ID | 名称 | scope | Locked生命周期摘要 |
|---|---|---|---|
| GP-001 | 规则版本 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-002 | 规则集标识 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-003 | 整场游戏配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-004 | 牌组配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-005 | 换三张配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-006 | 定缺配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-007 | 基本动作配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-008 | 多人响应优先级 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-009 | 胡牌权限配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-010 | 牌墙与终止配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-011 | 番型目录 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-012 | 番型关系 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-013 | 番数和封顶配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-014 | 自摸结算配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-015 | 杠分配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-016 | 呼叫转移配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-017 | 查花猪配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-018 | 查大叫配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-019 | 退税配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-020 | 庄家配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-021 | 信息可见性配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-022 | 时间控制配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-023 | AI玩家基础档案 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-024 | 记忆与学习配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-025 | 人类化行为配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-026 | 有限认知配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| GP-027 | 收益与比赛目标配置 | match_global | 整场创建时加载、校验并冻结；仅新match/规则版本可变 |
| RP-001 | 本局标识 | round_dynamic | 开局创建 |
| RP-002 | 座位与庄家状态 | round_dynamic | 开局创建，胡牌后更新轮转 |
| RP-003 | 当前比分与本局目标 | round_dynamic | 开局创建，计分事件后更新 |
| RP-004 | 初始手牌 | round_dynamic | 发牌后固定记录 |
| RP-005 | 换三张状态 | round_dynamic | 换牌阶段更新后固定 |
| RP-006 | 四家定缺状态 | round_dynamic | 定缺后固定，清缺进度动态更新 |
| RP-007 | 当前手牌 | round_dynamic | 摸牌、出牌、碰杠后更新 |
| RP-008 | 公开组合状态 | round_dynamic | 任一玩家碰杠后更新 |
| RP-009 | 弃牌历史 | round_dynamic | 每次出牌后更新 |
| RP-010 | 可见牌统计 | round_dynamic | 公开牌变化后更新 |
| RP-011 | 牌墙与轮次状态 | round_dynamic | 每次摸牌、杠后补牌后更新 |
| RP-012 | 存活玩家与胡牌状态 | round_dynamic | 任一玩家胡牌后更新 |
| RP-013 | 当前事件 | round_dynamic | 每个操作事件创建 |
| RP-014 | 合法行动与响应窗口 | round_dynamic | 每次需要决策时创建 |
| RP-015 | 过胡与权限状态 | round_dynamic | 放弃胡牌或恢复事件后更新 |
| RP-016 | 手牌结构状态 | round_dynamic | 摸打、碰杠、方向变化后更新 |
| RP-017 | 当前做牌计划 | round_dynamic | 定缺后创建，每次复核后更新 |
| RP-018 | 听牌与活牌状态 | round_dynamic | 手牌和可见牌变化后更新 |
| RP-019 | 对手推测状态 | round_dynamic | 对手公开行为后更新 |
| RP-020 | 威胁与安全状态 | round_dynamic | 公开信息和局势变化后更新 |
| RP-021 | 剩余机会状态 | round_dynamic | 轮次、碰杠、胡牌后更新 |
| RP-022 | 牌局阶段 | round_dynamic | 随轮次和玩家状态更新 |
| RP-023 | 候选行动集合 | round_dynamic | 每次决策时创建 |
| RP-024 | 当前注意力状态 | round_dynamic | 每次事件后更新 |
| RP-025 | 当前记忆状态 | round_dynamic | 公开事件后更新 |
| RP-026 | 当前搜索状态 | round_dynamic | 每次决策时创建 |
| RP-027 | 本次操作剩余时间 | round_dynamic | 决策窗口中动态更新 |
| RP-028 | 当前人格与情绪修正 | round_dynamic | 开局创建，重要结果后更新 |
| RP-029 | 行动历史与决策记录 | round_dynamic | 每次决策后追加 |
| RP-030 | 本局计分事件 | round_dynamic | 胡牌、杠牌和转移后更新 |
| RP-031 | 终局公开信息 | round_dynamic | 胡牌或流局公开时更新 |
| RP-032 | 本局结算结果 | round_dynamic | 结算后固定 |
| RP-033 | 跨局学习输出 | round_dynamic | 结算和复盘后生成 |

### 字段与状态机

- ParameterDefinition字段：`parameter_id,parameter_version,type,unit,min,max,default,nullable,visibility,source,value`。在逐字段决策批准前，不得把缺失统一解释为默认。
- 缺失必填→`SCHEMA_INVALID/PARAM_*`；显式null且nullable=false→`PARAM_NULL`；类型正确但闭区间外→`OUT_OF_RANGE/PARAM_RANGE`；未注册ID/字段→`UNKNOWN_PARAMETER/PARAM_UNKNOWN`。四者失败均零写入。
- GP在STATE-001创建immutable match context前冻结；冻结后整个match只读，新match/新规则版本才可创建新GP快照。
- RP在round start创建；只在parameter_registry声明的事件更新；round settlement后finalize并归档；新局创建新实例，不隐式携带瞬时值。归档载荷/跨局继承仍需决策。
- 四座owned state必须含owner_seat并分别冻结；seat事件只能写本座授权项。
- 事务状态机：`RECEIVED→VALIDATED→RESOLVED→COMMITTED`；`RECEIVED|VALIDATED→REJECTED`。成功CAS一次且version+1，失败snapshot/hash/version逐字段不变。

## ALGO-009：准确流水线与canonical门禁

Locked顺序是：`parse → version identify → stepwise migrate → apply declared defaults → type/range → cross constraints → reject unknown → canonical bytes/hash → freeze/commit`。迁移在临时对象完成，任何失败`result=null`且active config/文件不变。

当前只能冻结的canonical共同部分是UTF-8、键排序、紧凑无空白、禁止NaN/Inf、SHA-256小写hex。Unicode正规化/转义/键比较、整数与float/Decimal编码、指数、尾零和`-0`未给唯一规范，所以不能把Python `json.dumps`行为升级成跨语言Locked规范。性能§8的`1MB≤50ms`可作为ALGO-009 Locked阈值；其他无阈值项只能记录P50/P95/P99基线。

未知普通字段必须拒绝；废弃字段只能由明确source-version迁移消费；extensions不得当普通未知字段，但其元素schema、排序、hash参与和迁移仍需决策。启动失败/热重载失败均不得伪装accepted；是否显式继续上一有效配置等待决策。

## ALGO-011：legacy兼容与并发确定性

- `legacy-v1`路径原样保留当前`master=BLAKE2b(id,8)`及dice/exchange XOR，现有shuffle/dice/exchange/deal golden必须零变化。
- 新规范版本使用Locked公式，走独立版本化入口；禁止让新公式覆盖legacy函数。
- 新录制应显式持久化algorithm/rng version；旧回放和缺失版本的选择未冻结，批准前不设置默认。
- 流注册表按版本不可变、名称唯一；未知流=`STREAM_UNKNOWN`；新增流不能改变已有流。
- 并发派生必须是无状态纯函数，坐标来自稳定`stream_name + logical consumer + logical event + draw index`，调用者显式传入；禁止共享mutable stream index、worker完成序号、线程/进程号或系统时间。坐标准确schema仍需决策。

## SeedTrace字段级可见性

完整矩阵见`B1-A_seed_visibility_matrix.csv`。策略不得取得`master_seed`、原始`stream_name`、`index_before/after`、原始`seed_hash`或consumer/logical index；只能取得`rng_used`及不可逆、不可关联未来流的opaque trace reference。完整Frozen SeedTrace只允许引擎、受限trainer controller和审计使用，持久化必须受限。若现有DecisionResult schema强制把完整SeedTrace传给策略，则属于接口冲突，必须另提Frozen变更，而不是放宽可见性。

## 接口影响复评

不再统一判为NO_INTERFACE_CHANGE。内部ParameterDefinition/FrozenConfig和实现既有Frozen SeedTrace属于NO_INTERFACE_CHANGE；新增可选audit字段和内部结果信封属于COMPATIBLE_EXTENSION；向Frozen SeedTrace增加必填坐标字段属于BREAKING_CHANGE_REQUIRED，已明确禁止，改用独立受限审计扩展。逐项见`B1-A_interface_impact.csv`。

## AC复核规则

更新后的42条AC每条都有具体oracle。函数存在、日志存在、测试可调用均不算业务正确性。AC-12：ALGO-009使用Locked `1MB≤50ms`阈值；STATE-010/ALGO-011没有Locked阈值，只记录硬件、样本、P50/P95/P99基线，不作pass/fail。AC-10的E4必须从上述真实生产调用链采集；test-only facade不合格。

## 最终门禁

**BLOCKED_BY_SPEC_DECISION**。不允许开始B1-A整体编码。可以准备决策提案和不改代码的golden向量草案；必须先批准上表9项决策，再复审接口投影和42条AC，才可改为IMPLEMENTATION_READY。
