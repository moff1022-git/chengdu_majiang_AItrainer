# Spec v3 跨文档一致性复审报告

| 字段 | 内容 |
|---|---|
| 日期 | 2026-07-29 |
| 范围 | `docs/spec-v3/`全部文档与CSV |
| 性质 | 文档结构、语义边界与可审计性复审；未修改或运行业务代码 |
| 本轮修复/批准 | CDI-001、CDI-002、CDI-004、CDI-006均Closed；CDI-003核心文档均Approved |
| 总结论 | **Passed；规范已锁定为SPEC-V3-3.0.0，Critical 0 / High 0** |
| 其他开放项 | Medium 1 / Low 1 |

## 1. 复审方法与规模

- 以`locked_unit_catalog.csv`的96个唯一新单元ID为基准，对详细规格、开发任务卡、父测试规格、manifest、coverage、验收清单和追踪矩阵做双向集合检查。
- 检查576个父测试ID、890个细化TC ID、1344个唯一AC ID及AU-001～AU-096迁移端点。
- 解析60行参数注册表，复核ID、名称/范围、source hash、consumer和边界测试ID。
- 定向扫描RoundPhase、正式/历史证据等级、性能阈值、公式、I/O、隐藏truth及HEUR唯一性表述。
- 检查报告链接与Markdown/CSV空白；没有执行pytest、训练、回放或程序运行。

## 2. 结构检查结果

| 检查 | 结果 | 数字/证据 |
|---|---|---|
| 锁定目录ID | Passed | 96行、96唯一 |
| 详细规格 | Passed | 96/96，无重复、缺失或多余 |
| 开发任务卡 | Passed | 96/96 |
| 父测试规格 | Passed | 96/96；576/576唯一 |
| 细化测试目录 | Passed structurally | 890/890唯一TC，与coverage的Y项一致 |
| 验收清单 | Passed | 96/96；1344唯一AC，每单元14项 |
| 追踪矩阵 | Passed | 96/96，与目录集合一致 |
| 旧96迁移 | Passed | AU-001～096连续唯一；非空目标端点均有效 |
| 参数注册 | Passed | GP 27 + RP 33；60唯一、连续、均有consumer/test |

## 3. 用户指定检查逐项结论

### 3.1 单元ID是否唯一

Passed。目录和各派生层内部均无重复；跨层相同ID是追踪关系，不是重复定义。

### 3.2 每个单元是否出现在目录、规格、开发、测试和验收文档中

Passed，全部96/96；各层没有缺失或额外单元。

### 3.3 参数名称和范围是否一致

Passed。新增`07-traceability/parameter_registry.csv`，逐行登记60项参数的名称、类型/范围、生命周期、可见性、锁定来源章节/hash、consumer及边界测试。内容取自锁定上游第17/18章，60行source hash均为`6cbb4d4465abfd947b6cf7f1783db99408089d4e1646849a3afe674114267992`；consumer非空，测试端点全部存在。该表只是索引，不覆盖来源或Approved单元规格。CDI-004关闭。

### 3.4 公式是否重复且不一致

Passed as specification。未发现两份Approved详细规格对同一单元给出不同F1公式；总规范只定义F0～F5等级，开发和测试仅引用。golden目录登记Approved示例，不取得公式权威。实际JSONL和运行复算仍未实现。

### 3.5 输入输出定义是否一致

Passed as documentation。目录与`rule_parameter_unit_matrix.csv`的96项主要输入/输出逐字段一致；开发、父测试和细化用例从目录/规格派生。代码接口未在本轮审计。

### 3.6 状态枚举是否一致

Passed。唯一权威`RoundPhase`来自Approved STATE-004：`CONFIGURED→DEALT→EXCHANGE→DINGQUE→READY→DRAW/DISCARD/RESPONSE→FINISHED→SETTLED`。开发指南已删除第二套phase，将创建、提交、解析、关闭等改为领域事件并提供事件—phase映射；STATE-001的`match_status=CREATED/ACTIVE/COMPLETED`属于独立字段，禁止与RoundPhase互赋。CDI-001关闭。

### 3.7 测试是否覆盖全部验收条件

Passed as planned coverage，Not Implemented as evidence。96单元均判断11类测试适用性；AC-07/08/09/12/13/14有测试计划，AC-01～06/10/11还需规格、静态调用链、绑定、日志和追踪证据。计划文件不等于E3/E4运行证据。

### 3.8 审计项是否存在无法提供的证据

没有逻辑上不可能的检查；纯函数AC-06可用无副作用证明。正式等级已统一为E0—E5，语义只由审计标准定义。旧矩阵的EV0—EV5仅保留为legacy字段/历史标记，并规定保守迁移；report-only最高E2，禁止直接去掉`V`升级。CDI-002关闭。当前计划实现/运行产物缺失仍使大部分AC保持Not Evaluated，见CDI-005。

### 3.9 旧96项是否全部迁移

Passed。AU-001～096完整连续；REMOVE项保留治理意义；ADD-001～004补齐新边界。

### 3.10 是否存在孤立规则

未发现完全孤立单元。STATE-010与AUDIT-010是有意根节点；`发布门禁`是4个AUDIT行的治理sink，不是单元，仍由CDI-007跟踪schema标型。

### 3.11 是否存在孤立测试

未发现。576个父测试、890个TC及1344个AC均有唯一单元归属。自动化文件未实现属于就绪缺口，不是孤立测试。

### 3.12 是否存在未被调用的实现要求

文档DAG无consumerless单元，但尚未用生产trace证明建议入口实际被调用。AC-04仍需M0实现差距审计与运行证据，见CDI-005。

### 3.13 是否违反隐藏信息隔离

未发现规范层授权泄漏。policy只可读PlayerView/公开历史；restricted truth仅供隔离标签、评估或审计，不得回流。96/96均规划隐藏信息差分测试和AC-13。实现/日志/loader尚未按v3运行审计。

### 3.14 是否把启发式误写为唯一确定输出

Passed。23个HEUR卡以允许域、方向效应、regret、分布和95% CI验收；mandatory唯一动作、稳定tie-break和同seed复现只约束合法性/回放，不建立逐手专家唯一oracle。

## 4. 修复验证

| issue | 状态 | 关闭证据 |
|---|---|---|
| CDI-001 状态枚举冲突 | Closed | STATE-004唯一RoundPhase；指南事件映射；旧枚举只留在历史review描述 |
| CDI-002 证据等级冲突 | Closed | 正式E0—E5；legacy EV隔离；source inventory与audit standard语义一致 |
| CDI-004 参数范围不可机检 | Closed | 60行参数注册表，source/consumer/test端点检查通过 |
| CDI-006 双重性能阈值 | Closed | 指南删除5/20/5/50ms，AC-12只读Approved单元规格 |

## 5. 当前开放问题

| issue | severity | 影响 |
|---|---|---|
| CDI-005 新实现/测试/运行证据尚不存在 | Medium / Readiness | 96单元不能按新标准标AUDITED |
| CDI-007 治理sink混入消费者字段 | Low | 机器DAG尚未显式区分unit与governance sink |

CDI-003已关闭：总规范、开发指南/任务卡/迁移计划、细化测试策略/目录/golden、审计标准/清单及两份模板均已由用户明确批准。批准仅冻结文档契约，未提升实现证据。

## 6. 结论

CDI-001～004及CDI-006均已关闭；Critical=0、High=0。用户已据此正式锁定spec-v3为`SPEC-V3-3.0.0`。CDI-005与CDI-007继续登记；锁定不表示实现、测试运行、AUDITED或发布通过，M0结果仍为E1 / Not Evaluated。
# 3.0.1补丁复审（2026-07-29）

对SPF-001/002/003/006/007/008/010/011执行定向跨文档复审：路径语义、错误码/测试章节、fixture、HEUR计算图、MODEL校准、SCORE事件、AUDIT hash与E3/E4门禁均已有唯一权威定义和下游引用；Open Critical=0，Open High=0。仍有4项Medium记录于`specification_feedback.md`，不建议据此宣称相关单元生产AUDITED。
