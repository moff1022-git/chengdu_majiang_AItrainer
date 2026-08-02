# AUDIT-* 日志、证据与验收审计完整规格

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 版本 | 0.1 |
| 日期 | 2026-07-29 |
| 覆盖 | AUDIT-001～AUDIT-014 |
| 单元数 | 14 |
| 验收 | Not Evaluated |

## 总体审计原则

审计层可以在隔离权限下读取权威私有状态或评估truth，但只能生成证据和门禁结果，不得回流策略、PlayerView、模型线上输入、训练势能或权威状态。Passed必须来自可核查行为证据；未找到、过期或不适用的证据分别使用Not Evaluated、Failed或经批准的N/A，不得由总分抵消hard失败。

## AUDIT-001 全原子规则事件日志

### 1. 单元ID与名称

AUDIT-001 — 全原子规则事件日志；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

每个权威原子事件恰一条；公开载荷遵循RULE-016，私有牌只存受控引用。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

已提交state transition及事件前后hash。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成public_payload+private_refs→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

public_payload+private_refs；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

EVENT_SCHEMA_INVALID,EVENT_MISSING,PRIVATE_DATA_LEAK；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-001、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

事件覆盖100%，顺序/重复/缺失测试，历史不可变。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-001-CODE)：实现路径/符号/commit；TODO(AUDIT-001-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-001-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-001-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-002 AI决策解释日志

### 1. 单元ID与名称

AUDIT-002 — AI决策解释日志；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

每次策略决策恰一条，候选裁剪/修正/扰动/回退可重建，truth不进解释输入。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

request、PlayerView hash、认知/计划、候选分量、选择。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成view/memory/plan/scores/action_trace→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

view/memory/plan/scores/action_trace；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

TRACE_INCOMPLETE,VIEW_HASH_MISMATCH,ILLEGAL_SELECTED_ACTION,SENSITIVE_FIELD；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-002、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

字段完整100%，选择可重算100%，敏感泄漏0。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-002-CODE)：实现路径/符号/commit；TODO(AUDIT-002-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-002-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-002-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-003 canonical hash链与篡改检测

### 1. 单元ID与名称

AUDIT-003 — canonical hash链与篡改检测；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

record_hash=SHA256(canonical(record_without_hash)+prev_hash)；genesis绑定run manifest。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

按event_index排序的AUDIT-001/002记录。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成verified或首个failure index/reason→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

verified或首个failure index/reason；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

HASH_MISMATCH,CHAIN_TRUNCATED,CHAIN_REORDERED,GENESIS_MISMATCH；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-003、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

单字节篡改/截断/重排检出100%，原链通过100%。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-003-CODE)：实现路径/符号/commit；TODO(AUDIT-003-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-003-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-003-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-004 同配置/seed/事件的确定性回放

### 1. 单元ID与名称

AUDIT-004 — 同配置/seed/事件的确定性回放；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

从初始快照重放相同事件；比较canonical hashes并在首个差异停止。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

已验证artifact、配置/model/seed版本。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成逐事件state/action/score/log比较→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

逐事件state/action/score/log比较；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

REPLAY_VERSION,REPLAY_INPUT_MISSING,STATE_MISMATCH,ACTION_MISMATCH,SCORE_MISMATCH；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-004、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

确定性单元逐字段一致；跨进程/PYTHONHASHSEED一致。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-004-CODE)：实现路径/符号/commit；TODO(AUDIT-004-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-004-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-004-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-005 每事件强制不变量执行

### 1. 单元ID与名称

AUDIT-005 — 每事件强制不变量执行；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

固定次序检查牌张守恒→phase/actor→legal→活动座→view隔离→账本零和→版本单调。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

每个post-event权威state、legal/view/ledger引用。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成pass或稳定InvariantViolation→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

pass或稳定InvariantViolation；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

OWNERSHIP_DUPLICATE,PHASE_ACTOR,ILLEGAL_COMMIT,VIEW_LEAK,SCORE_NOT_ZERO_SUM；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-005、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

所有事件执行率100%，故障注入检出100%，失败零提交。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-005-CODE)：实现路径/符号/commit；TODO(AUDIT-005-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-005-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-005-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-006 直接规则与接口测试证据门禁

### 1. 单元ID与名称

AUDIT-006 — 直接规则与接口测试证据门禁；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

测试名不计证据；必须解析/人工复核断言正文与目标断言的直接关系，记录EV等级。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

原子断言目录、测试源码语义、运行结果。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成逐断言coverage status→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

逐断言coverage status；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

ASSERTION_UNMAPPED,TEST_BODY_MISSING,RESULT_STALE,EVIDENCE_TOO_LOW；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-006、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

hard断言直接证据100%，失败/Not Evaluated不被平均抵消。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-006-CODE)：实现路径/符号/commit；TODO(AUDIT-006-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-006-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-006-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-007 属性式生成、缩减与不变量证据

### 1. 单元ID与名称

AUDIT-007 — 属性式生成、缩减与不变量证据；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

合法生成→事件序列→AUDIT-005；失败按固定shrink顺序缩减并保留seed/replay。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

版本化generator、命名seed、状态约束、不变量。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成minimized failures+生成报告→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

minimized failures+生成报告；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

GENERATOR_INVALID,SEED_MISSING,SHRINK_NON_REPRODUCIBLE,PROPERTY_FAILED；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-007、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

P0属性各≥10000例或批准预算，失败100%可复现/可缩减。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-007-CODE)：实现路径/符号/commit；TODO(AUDIT-007-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-007-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-007-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-008 锁定来源逐章golden-case对照

### 1. 单元ID与名称

AUDIT-008 — 锁定来源逐章golden-case对照；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

每条来源至少映射一个单元断言和正/边界/反例；治理条款可N/A-with-approval。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

两份锁定来源条款、参数/profile允许集、golden cases。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成per-clause Passed/Failed/Not Evaluated→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

per-clause Passed/Failed/Not Evaluated；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

CLAUSE_UNMAPPED,CASE_MISSING,EXPECTED_AMBIGUOUS,SOURCE_HASH_MISMATCH；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-008、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

0–18章适用条款覆盖100%，未决歧义不得Passed。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-008-CODE)：实现路径/符号/commit；TODO(AUDIT-008-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-008-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-008-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-009 工程与行为回归指标

### 1. 单元ID与名称

AUDIT-009 — 工程与行为回归指标；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

按预注册分母计算合法/复现/性能/风格/收益；工程硬门禁与行为软指标分开。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

冻结runs、基线、环境/config/model hashes。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成metric report+95% CI→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

metric report+95% CI；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

RUN_INCOMPATIBLE,METRIC_DENOMINATOR,BASELINE_MISSING,CI_FAILED；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-009、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

非法/泄漏0、复现100%；性能/行为按对应规格阈值与CI。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-009-CODE)：实现路径/符号/commit；TODO(AUDIT-009-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-009-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-009-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-010 来源→参数→实现→测试全链追踪

### 1. 单元ID与名称

AUDIT-010 — 来源→参数→实现→测试全链追踪；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

source→clause→parameter→unit→assertion→module/symbol→test→run evidence全链，每节点版本化。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

source/catalog/parameter registry/code/test/evidence manifests。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成trace matrix+broken links→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

trace matrix+broken links；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

TRACE_BREAK,DUPLICATE_ID,UNKNOWN_PARAMETER,FORMULA_VERSION_MISSING；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-010、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

96单元目录覆盖100%，所有Approved hard断言无断链。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-010-CODE)：实现路径/符号/commit；TODO(AUDIT-010-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-010-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-010-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-011 版本、迁移与发布物完整性

### 1. 单元ID与名称

AUDIT-011 — 版本、迁移与发布物完整性；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

依次版本一致→迁移→测试证据→模型兼容→artifact hash/signature→tag；任一失败拒绝。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

release candidate、schema/迁移、测试、artifact/hash/tag。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成manifest+gate result→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

manifest+gate result；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

VERSION_MISMATCH,MIGRATION_GATE,TEST_GATE,ARTIFACT_HASH,TAG_MISMATCH；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-011、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

所有硬门禁通过才Approved；发布物清单/hash覆盖100%。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-011-CODE)：实现路径/符号/commit；TODO(AUDIT-011-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-011-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-011-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-012 强度、真人相似和学习效果外部评价

### 1. 单元ID与名称

AUDIT-012 — 强度、真人相似和学习效果外部评价；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

按F0031分层评价；无合规真人数据时G5 Not Evaluated，禁止工程测试代替。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

冻结数据集、策略/模型、盲测计划、runs。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成statistics+CI+结论等级→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

statistics+CI+结论等级；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

DATASET_NOT_FROZEN,LEAKED_TEST,BLINDING_FAILED,SAMPLE_TOO_SMALL,NOT_EVALUATED_REQUIRED；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-012、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

预注册阈值与95% CI；真人相似无数据不下结论。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-012-CODE)：实现路径/符号/commit；TODO(AUDIT-012-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-012-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-012-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-013 模块依赖、接口与信息流架构契约

### 1. 单元ID与名称

AUDIT-013 — 模块依赖、接口与信息流架构契约；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

静态依赖+运行canary检查engine权威、players可插拔、training复用engine、truth不回流policy。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

source import graph、runtime接口、数据流schema。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成violations/report→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

violations/report；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

FORBIDDEN_IMPORT,INTERFACE_BREAK,ORACLE_FLOW,SECOND_RULE_ENGINE；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-013、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

禁止边0、oracle泄漏0、公开接口兼容100%。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-013-CODE)：实现路径/符号/commit；TODO(AUDIT-013-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-013-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-013-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。

## AUDIT-014 证据数据保留、脱敏与新鲜度管理

### 1. 单元ID与名称

AUDIT-014 — 证据数据保留、脱敏与新鲜度管理；类型：日志审计；规格状态：Approved；实现验收：Not Evaluated。来源、GP/RP和依赖以锁定目录对应行唯一为准。

### 2. 审计目标

分类→脱敏→内容hash→新鲜度等级current/report-only/stale→保留/删除日期与访问级别。本单元产生证据或门禁结果，不改变被审计的权威游戏状态、策略选择或真实分数。

### 3. 职责范围

负责输入证据的schema验证、规范化、检查、失败定位、结果签名和保留引用；只判断本单元目录边界内的审计问题。

### 4. 明确不负责

不实现房规、算法、启发式、模型或训练逻辑；不把类名、接口、占位函数、测试名称或文件存在当作行为通过证据；不让审计truth回流策略。

### 5. 输入与数据类型

run artifacts、retention/redaction policy、敏感分类。通用字段：run/game/round/event/request ID，uint64序号，UTC时间，规则/config/code/model/schema hashes，环境manifest和evidence freshness。

### 6. 输入可见性与权限

审计器可按最小权限读取private truth用于验证，但公开报告只含白名单字段、聚合或hash。policy/PlayerView/reward potential通道不得读取审计私有字段。

### 7. 前置条件

来源hash、schema/version和run manifest已冻结；输入完整且按稳定ID关联；若依赖运行证据，必须声明current-run/report-only/stale-cache及环境。

### 8. 触发事件

每次对应原子事件、决策、测试run、回放、发布候选或证据保留动作触发；批量审计必须保留每个原子检查结果，不能只存总分。

### 9. 审计处理流程

解析→schema/版本→canonical排序→执行本卡检查→定位首个失败及全部可继续检查→生成retained manifest→签名/hash→交AUDIT-014保留。失败不得修改原输入。

### 10. 输出格式与范围

retained manifest；包含status∈Passed/Failed/Not Evaluated/N/A-with-approval、severity、error_code、finding列表、checked/failed counts、input/output hash、evidence refs。hard失败不能被平均抵消。

### 11. 状态与生命周期

RECEIVED→VALIDATED→CHECKED→SIGNED→RETAINED；失败进入REJECTED但仍保留失败证据。历史记录append-only；更正通过新记录supersedes旧记录。

### 12. 确定性与随机数

给定相同输入、版本和seed，结果逐字段一致。除AUDIT-007使用ALGO-011命名生成流外不得使用随机数；抽样必须记录总体、分母、seed和选择算法。

### 13. 不变量

证据链可追溯；输入不可变；私有truth不回流；未知/缺证据为Not Evaluated而非Passed；时间、线程、容器顺序不改变规范结果。

### 14. 异常和错误码

PII_UNREDACTED,PRIVATE_TILE_EXPOSED,RETENTION_EXPIRED,FRESHNESS_UNKNOWN,MANIFEST_INCOMPLETE；通用：SCHEMA_INVALID、VERSION_CONFLICT、EVIDENCE_MISSING、EVIDENCE_STALE、HASH_MISMATCH、UNAUTHORIZED、AUDIT_INTERNAL。未知异常不得伪装通过。

### 15. 并发与顺序

多worker结果按(run_id,event_index,unit_id,check_id)规范归并；重复ID拒绝；迟到结果产生新revision，不覆盖已签名记录。响应返回顺序不得影响结论。

### 16. 日志与审计自身字段

timestamp_utc、audit_unit=AUDIT-014、audit_version、run/environment hashes、input refs/hash、check IDs、status/severity/error、first_failure、counts、latency、output hash、prev/record hash、retention class。

### 17. 隐私、脱敏和保留

实体牌、隐藏手牌、墙序、真人身份和原始策略truth按private/restricted分类；公开物只保留必要聚合。保留期限、访问者、加密位置、删除/归档动作写manifest。

### 18. 单元测试要求

正常、边界、非法schema、缺字段、版本错、篡改、重复/乱序、权限拒绝、私有字段投毒、失败可复现及canonical hash golden；测试须断言正文行为。

### 19. 属性与集成测试

对记录顺序/序列化等价做metamorphic；与上下游单元做契约测试；故障注入必须命中预期稳定错误码且被审计链保留。

### 20. 性能目标

在线原子审计P95≤1ms（回放/属性/外部评价等离线单元按manifest预算）；不得让日志阻塞权威引擎，背压时显式失败/降级且不丢hard事件。

### 21. 验收标准

敏感泄漏0、manifest覆盖100%、过期证据不得支撑当前通过。此外schema有效100%、确定复现100%、私有truth回流0、hard失败不误报Passed、所有结论带可核查路径/符号/命令或artifact。

### 22. 代码与测试证据占位

TODO(AUDIT-014-CODE)：实现路径/符号/commit；TODO(AUDIT-014-TEST)：测试路径/断言/命令/输出；当前均Not Evaluated。

### 23. 运行与保留证据占位

TODO(AUDIT-014-RUN)：环境、配置、命令、原始输出、hash；TODO(AUDIT-014-RETENTION)：manifest、敏感等级、新鲜度和保留位置；未找到时必须写“未找到”。
# 3.0.1 AUDIT-003逐字节hash公式

record必须显式含`previous_record_hash`。令`B=canonical_json_utf8(record_without_record_hash)`，则`record_hash=SHA256(B)`；禁止在B后再次拼接previous hash。链关系仅由B内部的`previous_record_hash`字段表达。genesis该字段为null；后续必须等于前一记录`record_hash`。canonical JSON固定UTF-8、键Unicode码点升序、无空白、禁止NaN/Inf。golden：对象`{"a":1,"previous_record_hash":null}`的B逐字节等于该ASCII文本；任何实现必须同时固化B与SHA-256向量。
