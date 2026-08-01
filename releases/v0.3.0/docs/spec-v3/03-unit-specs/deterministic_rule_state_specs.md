# RULE-* 与 STATE-* 确定性单元完整规格卡

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 版本 | 0.1 |
| 日期 | 2026-07-29 |
| 覆盖范围 | 锁定目录中的 RULE-001～RULE-016、STATE-001～STATE-012 |
| 单元数 | 28（16 确定规则 + 12 状态管理） |
| 验收状态 | Not Evaluated |

## 使用约定

本文逐单元采用用户指定的23项统一模板。锁定来源文档保持只读；详细来源映射继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 与 [unit_migration_map.csv](../02-unit-catalog/unit_migration_map.csv)。本文定义目标契约，不宣称现有实现、测试或运行证据已经通过。

所有单元均受统一确定性契约约束：在输入值、初始状态、规则/参数版本、代码版本和命名随机种子相同的前提下，输出值、错误码、状态转移、规范序日志载荷与确定性指纹必须唯一；线程调度、容器迭代次序、玩家响应返回顺序和墙钟时间不得改变结果。STATE-011 是本组唯一消费随机数的单元，但只能消费 ALGO-011 分配的命名随机流。

全局 hard 不变量：

1. 108张实体牌以唯一 physical tile ID 表示；任一已提交事件后，手牌、副露、未领取弃牌、牌墙、交换/杠/胡过渡区及规则定义的和牌占用区并集恰为完整牌集，且两两不重叠。
2. 权威行动必须来自当前合法行动集；actor、phase、request/window 与 state_version 一致。
3. 胡后玩家退出摸打和响应活动集；牌墙耗尽或活动玩家不足2时停止产生新行动请求。
4. PlayerView 与策略/训练输入不得包含对手暗手、牌墙顺序、oracle truth 或其他未列入白名单的私有字段。
5. 任一失败原子回滚；错误必须使用稳定错误码并可审计。

## RULE-001 规则、参数、不变量与合法性裁决优先级

### 1. 单元ID与名称

`RULE-001` — 规则、参数、不变量与合法性裁决优先级。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `authoritative legal set or explicit rejection`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 规则、参数、不变量与合法性裁决优先级 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-002、STATE-010、ALGO-009；下游：ALGO-006、AUDIT-005、RULE-007/008/010/013、STATE-009、TRAIN-001/003。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-001 行及其 AU/章节锚点为准；参数：GP-002、GP-008～GP-010、GP-001～GP-027。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `ruleset/config/state`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

读取冻结规则版本→校验配置→校验阶段/actor/状态不变量→由专属规则单元生成候选→取交集并规范排序→非法则拒绝→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `authoritative legal set or explicit rejection`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

合法集只能来自权威状态和已批准规则；策略不得扩张合法集；冲突优先级为不变量>房规>配置>策略；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`CFG_CONFLICT、STATE_INVARIANT、ILLEGAL_ACTION、UNSUPPORTED_RULE_VERSION`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-001, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

冲突配置、非法 seat/phase/action、唯一动作、候选顺序置换、同输入复算；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-001-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-001-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-001-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-002 换三张同花色、方向与提交合法性

### 1. 单元ID与名称

`RULE-002` — 换三张同花色、方向与提交合法性。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `accepted exchange or error`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 换三张同花色、方向与提交合法性 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-003、STATE-011、ALGO-001；下游：HEUR-001。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-002 行及其 AU/章节锚点为准；参数：GP-005、GP-006、RP-001、RP-002。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `concealed physical tiles + direction`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

核对 exchange 阶段/活动座→解析3个实体牌ID→验证均在本手且互异→验证同花色→验证方向映射→原子移除全部提交牌并按方向加入→排序→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `accepted exchange or error`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

每座恰交3张同花色实体牌；先全移除后全加入；交换前后108张实体牌集合不变；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`WRONG_PHASE、INVALID_SEAT、EXCHANGE_COUNT、MIXED_SUIT、TILE_NOT_OWNED、DUPLICATE_TILE、INVALID_DIRECTION`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

收集按 `request/window_id + seat` 去重；结果按座位环序和规则优先级规范化，禁止以线程/网络返回先后决胜。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-002, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

方向×人数×花色；混色/重复/越权；提交顺序置换；交换前后实体ID守恒；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-002-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-002-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-002-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-003 定缺未清时的强制出牌约束

### 1. 单元ID与名称

`RULE-003` — 定缺未清时的强制出牌约束。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `legal discards`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 定缺未清时的强制出牌约束 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-003；下游：HEUR-002、HEUR-014。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-003 行及其 AU/章节锚点为准；参数：GP-002、RP-003。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `hand + dingque`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

确认 discard 阶段及当前座→枚举手牌实体牌→若强制清缺且仍持缺门，仅保留缺门牌→按牌面去重但保留可执行实体映射→规范排序输出→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `legal discards`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

仍持缺门时不得打非缺门；清空后不再施加该限制；不得给非活动座动作；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`WRONG_PHASE、NOT_ACTOR、DINGQUE_UNSET、STATE_INVARIANT`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-003, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

缺门0/1/多张、同牌多实体、开关矩阵、胡后座、顺序置换；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-003-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-003-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-003-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-004 定缺、死叫与胡牌资格约束

### 1. 单元ID与名称

`RULE-004` — 定缺、死叫与胡牌资格约束。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `hu eligibility`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 定缺、死叫与胡牌资格约束 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-003、ALGO-002；下游：SCORE-004。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-004 行及其 AU/章节锚点为准；参数：GP-002、RP-003。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `hand + dingque + waits`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

验证候选和牌结构→检查定缺已清→按冻结房规判定有效听口/死叫状态→输出可胡布尔、原因和适用上下文→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `hu eligibility`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

持有缺门牌不得胡；胡资格与番数/计分分离；死叫判定使用同一冻结规则版本；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`DINGQUE_NOT_CLEARED、NOT_WINNING、DEAD_WAIT、INVALID_WIN_SOURCE`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-004, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

清缺/未清、空等待、牌墙已耗尽等待、不同和牌来源、同输入复算；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-004-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-004-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-004-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-005 座位、庄家与活动顺序

### 1. 单元ID与名称

`RULE-005` — 座位、庄家与活动顺序。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `next actor`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 座位、庄家与活动顺序 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-002；下游：ALGO-005、RULE-014。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-005 行及其 AU/章节锚点为准；参数：校验座位为0..N-1且庄家唯一→验证 actor 活动→从actor后一个座按环序扫描→跳过已胡/退出座→返回首个活动座或终止标志。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `seats + dealer + active set + actor`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

座位编号整场不变；庄家唯一；next actor 必在活动集；同活动集与actor结果唯一→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `next actor`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

INVALID_SEAT_SET、INVALID_DEALER、ACTOR_INACTIVE、NO_ACTIVE_SUCCESSOR；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`2/3/4人、座0跨界、连续退出、仅1/0活动座、不同集合顺序`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-005, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-005-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-005-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-005-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-006 摸牌、可选响应与出牌标准顺序

### 1. 单元ID与名称

`RULE-006` — 摸牌、可选响应与出牌标准顺序。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `next phase/action request`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 摸牌、可选响应与出牌标准顺序 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-004、STATE-011；下游：AUDIT-006。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-006 行及其 AU/章节锚点为准；参数：ready由庄家进入discard→无副露后续轮到者先draw→摸后进入本座discard并提供自摸/杠/弃牌→弃牌后有响应者进入response→无人/全过则下家draw→碰后响应者discard→杠后补摸再discard。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `phase + actor + wall`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

除庄家初始14张外，活动座通常先摸后打；一次只存在一个当前actor或一个响应窗口；牌墙不得负数→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `next phase/action request`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

WRONG_PHASE、NOT_ACTOR、EMPTY_WALL、PENDING_RESPONSE、ILLEGAL_TRANSITION；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`完整阶段表、庄家首打、普通摸打、碰后打、杠后补摸、空墙`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-006, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-006-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-006-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-006-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-007 碰牌资格、执行与后续出牌

### 1. 单元ID与名称

`RULE-007` — 碰牌资格、执行与后续出牌。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `meld/turn`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 碰牌资格、执行与后续出牌 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：RULE-001、STATE-003；下游：HEUR-012、RULE-013。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-007 行及其 AU/章节锚点为准；参数：确认响应窗口与未被消费弃牌→响应者活动且非出牌者→手中同牌面至少2个实体→经RULE-013获胜→从手牌移除2张并与弃牌组成pong→标记弃牌被领取→当前座改为碰者并进入discard。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `discard + responders + hands`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

碰副露恰3个同牌面且实体ID唯一；来源弃牌只消费一次；碰者不得先摸直接出牌→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `meld/turn`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

PONG_NOT_ALLOWED、INSUFFICIENT_TILES、DISCARD_CONSUMED、RESPONSE_LOST；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`合法/不足/同座、多人竞争让序、实体ID守恒、碰后phase/actor`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-007, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-007-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-007-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-007-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-008 明杠、暗杠与补杠资格及执行

### 1. 单元ID与名称

`RULE-008` — 明杠、暗杠与补杠资格及执行。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `gang transition`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 明杠、暗杠与补杠资格及执行 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：RULE-001、STATE-003、STATE-011；下游：识别明杠/暗杠/补杠→分别验证弃牌+手3张、手4张、既有碰+手1张→处理补杠抢杠窗口→获准后原子形成/升级4张副露→记杠事件→从牌墙补1张→进入杠者discard。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-008 行及其 AU/章节锚点为准；参数：杠组恰4个同牌面唯一实体；补牌只在杠最终成立后；抢杠成功不得成立补杠；全局牌张守恒。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `hand/meld/discard`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

GANG_NOT_ALLOWED、INSUFFICIENT_TILES、MELD_NOT_FOUND、EMPTY_WALL、QIANG_GANG_PENDING→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `gang transition`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

三类杠正反例、杠尾空墙、补杠被抢、实体守恒、重复提交；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`undefined`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-008, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-008-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-008-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-008-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-009 补杠抢杠胡窗口与解析

### 1. 单元ID与名称

`RULE-009` — 补杠抢杠胡窗口与解析。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `hu or gang`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 补杠抢杠胡窗口与解析 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：RULE-008、RULE-010；下游：冻结补杠意图和实体牌→向所有有抢杠胡资格活动座建窗口→收齐/超时回退响应→存在胡则按多人胡规则结算且取消补杠→否则提交补杠并补摸。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-009 行及其 AU/章节锚点为准；参数：窗口未决时不得修改碰副露或补摸；只允许HU/PASS；多个合法胡不得被返回时序吞掉。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `bugang intent + responders`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

INVALID_BUGANG、INVALID_RESPONSE、RESPONSE_INCOMPLETE、STALE_WINDOW→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `hu or gang`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

无人可抢、全过、单/多人抢、响应乱序、超时、重复响应；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`undefined`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

收集按 `request/window_id + seat` 去重；结果按座位环序和规则优先级规范化，禁止以线程/网络返回先后决胜。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-009, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-009-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-009-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-009-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-010 自摸、点炮与抢杠胡资格

### 1. 单元ID与名称

`RULE-010` — 自摸、点炮与抢杠胡资格。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `legal hu set`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 自摸、点炮与抢杠胡资格 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：RULE-001、STATE-003、ALGO-002；下游：校验来源为self_draw/discard/qiang_gang→构造恰当候选手牌→检查活动状态、定缺清空、和牌结构及过胡限制→输出所有合法胡座及原因。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-010 行及其 AU/章节锚点为准；参数：同一胜牌/来源不得重复计入；非活动座不得胡；资格判定不包含响应优先或计分。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `state + winning tile + source`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

INVALID_WIN_SOURCE、NOT_WINNING、DINGQUE_NOT_CLEARED、PASS_HU_BLOCKED、PLAYER_INACTIVE→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `legal hu set`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

三类胡、假胡、未清缺、已过胡、已胡座、多人同炮；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`undefined`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-010, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-010-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-010-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-010-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-011 过胡设置、持续与恢复

### 1. 单元ID与名称

`RULE-011` — 过胡设置、持续与恢复。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `pass-hu state`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 过胡设置、持续与恢复 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：RULE-010、STATE-003；下游：在合法HU窗口选择PASS时记录门槛/来源/事件→后续候选胡按冻结恢复模式比较→仅在规定事件（如本座摸牌或更高资格）清除/更新→归档原因。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-011 行及其 AU/章节锚点为准；参数：未获得合法胡机会的PASS不设置过胡；状态仅属于该玩家；恢复不得因他人事件误触发。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `declined hu + phase/events`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

PASS_HU_INVALID、STALE_WINDOW、INVALID_RECOVERY_MODE→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `pass-hu state`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

合法过胡/普通过、他人摸打、本座摸牌、较高/相同资格、存档恢复；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`undefined`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-011, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-011-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-011-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-011-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-012 强制胡与最后阶段必胡

### 1. 单元ID与名称

`RULE-012` — 强制胡与最后阶段必胡。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `forced action`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 强制胡与最后阶段必胡 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：RULE-010、STATE-011；下游：取得合法动作集→读取强制胡/尾牌必胡开关及牌墙边界→条件满足则将HU设为唯一动作→否则保留原合法集→记录强制原因。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-012 行及其 AU/章节锚点为准；参数：只可强制已合法的HU；不得由策略绕过；相同墙状态和配置产生唯一结果。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `legal hu + GP rule + wall state`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

FORCED_HU_NOT_LEGAL、INVALID_WALL_STATE、CONFIG_CONFLICT→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `forced action`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

开关四象限、墙余0/1/边界、多个HU上下文、非法HU不得强制；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`undefined`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-012, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-012-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-012-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-012-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-013 多人响应确定性优先级

### 1. 单元ID与名称

`RULE-013` — 多人响应确定性优先级。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `resolved actions`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 多人响应确定性优先级 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：RULE-001、RULE-007、RULE-009、RULE-010；下游：验证响应均属于同一窗口且合法→按HU>GANG>PONG>PASS分级→HU按一炮多响配置保留全部或按座位环序选定→同级碰/杠按距出牌者环序决胜→输出规范序动作和未获胜响应原因。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-013 行及其 AU/章节锚点为准；参数：解析与响应到达顺序无关；每响应座至多一项最终响应；同一弃牌至多由一个非HU副露消费。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `response set + GP-008`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

RESPONSE_WINDOW_MISMATCH、DUPLICATE_RESPONSE、ILLEGAL_RESPONSE、INCOMPLETE_RESPONSE、PRIORITY_CONFLICT→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `resolved actions`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

全排列乱序、胡/杠/碰竞争、一炮多响开关、同级环序、重复/缺失响应；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`undefined`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

收集按 `request/window_id + seat` 去重；结果按座位环序和规则优先级规范化，禁止以线程/网络返回先后决胜。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-013, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-013-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-013-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-013-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-014 血战胡后退出、继续与终止

### 1. 单元ID与名称

`RULE-014` — 血战胡后退出、继续与终止。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `active set/end`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 血战胡后退出、继续与终止 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：RULE-005、RULE-010、STATE-004；下游：确认胡结果→将胡者标finished并从摸打/响应活动集移除→记录唯一胡序→若活动座至少2且墙非空则按环序继续→否则以三家胡/不足2人/牌墙耗尽原因结束并进入结算。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-014 行及其 AU/章节锚点为准；参数：胡者仍可公开观察但不得再摸打响应；每座最多胡一次；终止后不再产生行动请求。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `hu result + active seats + wall`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

DUPLICATE_HU、PLAYER_INACTIVE、INVALID_ACTIVE_SET、ROUND_ALREADY_FINISHED→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `active set/end`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

第1/2/3胡、多人同炮后活动数、仅2/3人局、荒牌、胡后错误响应；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`undefined`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-014, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-014-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-014-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-014-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-015 启用番型、互斥/叠加与封顶规则

### 1. 单元ID与名称

`RULE-015` — 启用番型、互斥/叠加与封顶规则。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `applicable fan policy`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 启用番型、互斥/叠加与封顶规则 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-010；下游：HEUR-011、SCORE-002、SCORE-004、SCORE-005。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-015 行及其 AU/章节锚点为准；参数：校验番型配置→从手牌事实匹配启用番型→执行互斥/替代规则→按固定次序叠加→应用封顶策略→输出番型ID、原始番、有效番和排除理由。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `ruleset + hand facts`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

禁用番型不得计入；互斥只保留规则指定项；封顶次序固定；不得由策略估值改变权威结果→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `applicable fan policy`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

UNKNOWN_FAN、FAN_CONFIG_CONFLICT、MISSING_HAND_FACT、CAP_OUT_OF_RANGE；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`每番型golden、互斥对、叠加组合、封顶前后、未知配置`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-015, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-015-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-015-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-015-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## RULE-016 局中与终局公开信息范围

### 1. 单元ID与名称

`RULE-016` — 局中与终局公开信息范围。

### 2. 类型

确定规则；`method_class=deterministic_rule`；不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `visible field set`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 局中与终局公开信息范围 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-004、STATE-010；下游：ALGO-010、AUDIT-013、MODEL-003。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 RULE-016 行及其 AU/章节锚点为准；参数：按phase与观察seat选择字段白名单→公开本人手牌、公共副露/弃牌/状态及允许的墙数量→隐藏他家暗手、墙序、私有认知、受限truth→终局仅按规则扩展→输出字段集合和敏感级别。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

权威引擎请求合法性判定或应用对应事件；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `phase + seat + event`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

不持有跨事件可变策略状态；只读取冻结规则快照、输入状态版本和本次临时判定上下文。

### 11. 完整处理流程

默认拒绝未登记字段；局中任何策略视图不得含对手暗手/墙序/oracle；座位间仅self字段不同→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `visible field set`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

FIELD_NOT_WHITELISTED、VISIBILITY_LEAK、INVALID_VIEWER、INVALID_PHASE；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`逐phase/逐seat矩阵、嵌套字段、终局扩展、序列化旁路、四座交叉泄漏`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=RULE-016, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(RULE-016-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(RULE-016-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(RULE-016-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## STATE-001 Match 配置冻结、玩家装配与整场控制

### 1. 单元ID与名称

`STATE-001` — Match 配置冻结、玩家装配与整场控制。

### 2. 类型

状态管理；`catalog_type=state_management`；确定性、不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `immutable match context`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 Match 配置冻结、玩家装配与整场控制 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：ALGO-009、ALGO-011、STATE-010；下游：HEUR-003/008、SCORE-006、STATE-004/006/008、TRAIN-001。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 STATE-001 行及其 AU/章节锚点为准；参数：GP-001～GP-027、RP-001～RP-033。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

创建整场请求；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `match request`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

生命周期字段至少含 `version`、`phase/status`、`owner`、`created_event`、`updated_event`；具体领域字段见输入输出与流程。

### 11. 完整处理流程

校验match请求→固定版本/hash/命名seed→装配唯一座位与profile→冻结局数/初分/规则→逐局派生context→收集结果直到完成→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `immutable match context`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

match_id内规则/座位/profile/主seed不可变；局间仅STATE-008白名单字段继承；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`INVALID_MATCH_REQUEST、DUPLICATE_SEAT、CONFIG_MUTATION、SEED_MISSING`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=STATE-001, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

2/3/4座、重复profile、局数边界、中途修改拒绝、相同请求复算；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(STATE-001-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(STATE-001-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(STATE-001-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## STATE-002 权威 RoundState 存储与授权访问

### 1. 单元ID与名称

`STATE-002` — 权威 RoundState 存储与授权访问。

### 2. 类型

状态管理；`catalog_type=state_management`；确定性、不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `authoritative state`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 权威 RoundState 存储与授权访问 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-004、STATE-011；下游：ALGO-010、AUDIT-001、RULE-001/005、SCORE-001、STATE-003/007。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 STATE-002 行及其 AU/章节锚点为准；参数：RP-001～RP-023、RP-001～RP-033。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

创建、读取、迁移或提交对应状态；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `atomic events`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

生命周期字段至少含 `version`、`phase/status`、`owner`、`created_event`、`updated_event`；具体领域字段见输入输出与流程。

### 11. 完整处理流程

接收单一已验证原子事件→在事务副本应用→执行不变量→成功则递增event/version并原子发布→读者按权限获取快照/视图→失败不提交→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `authoritative state`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

单写者；事件版本单调；失败零部分写；策略不得获得权威可变引用；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`VERSION_CONFLICT、UNAUTHORIZED_READ、INVALID_EVENT、INVARIANT_FAILED`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

收集按 `request/window_id + seat` 去重；结果按座位环序和规则优先级规范化，禁止以线程/网络返回先后决胜。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=STATE-002, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

CAS冲突、失败回滚、快照隔离、重复事件、并发读写；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(STATE-002-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(STATE-002-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(STATE-002-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## STATE-003 PlayerRoundState 手牌、副露、定缺与过胡状态

### 1. 单元ID与名称

`STATE-003` — PlayerRoundState 手牌、副露、定缺与过胡状态。

### 2. 类型

状态管理；`catalog_type=state_management`；确定性、不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `player state`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 PlayerRoundState 手牌、副露、定缺与过胡状态 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-002、ALGO-001；下游：ALGO-002、RULE-002/003/004/007/008/010/011。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 STATE-003 行及其 AU/章节锚点为准；参数：GP-011～GP-020、RP-001～RP-033。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

创建、读取、迁移或提交对应状态；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `rule transitions`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

生命周期字段至少含 `version`、`phase/status`、`owner`、`created_event`、`updated_event`；具体领域字段见输入输出与流程。

### 11. 完整处理流程

按seat定位玩家→按已验证事件变更hand/meld/dingque/pass_hu/status/hu_order→规范排序→校验实体唯一及字段组合→提交给STATE-002→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `player state`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

手牌/副露实体不重叠；status=finished不得再获牌；hu_order唯一；dingque仅合法花色；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`PLAYER_NOT_FOUND、DUPLICATE_TILE、INVALID_MELD、INVALID_STATUS、INVALID_HU_ORDER`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=STATE-003, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

全字段生命周期、重复实体、碰杠迁移、过胡恢复、胡后写入拒绝；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(STATE-003-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(STATE-003-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(STATE-003-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## STATE-004 CONFIGURED→SETTLED 状态机

### 1. 单元ID与名称

`STATE-004` — CONFIGURED→SETTLED 状态机。

### 2. 类型

状态管理；`catalog_type=state_management`；确定性、不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `next phase or error`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 CONFIGURED→SETTLED 状态机 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-001；下游：AUDIT-001/005、RULE-006/014/016、STATE-002/009、TRAIN-001。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 STATE-004 行及其 AU/章节锚点为准；参数：GP-001～GP-027、RP-001～RP-033。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

创建、读取、迁移或提交对应状态；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `current phase + event`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

生命周期字段至少含 `version`、`phase/status`、`owner`、`created_event`、`updated_event`；具体领域字段见输入输出与流程。

### 11. 完整处理流程

按转换表处理CONFIGURED→DEALT→EXCHANGE(可跳过)→DINGQUE→READY→DRAW/DISCARD/RESPONSE循环→FINISHED→SETTLED；每事件验证来源phase与guard→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `next phase or error`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

phase单调遵循转换图；SETTLED吸收；任一时刻仅一个权威phase；非法跳转零写入；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`ILLEGAL_TRANSITION、GUARD_FAILED、TERMINAL_STATE、EVENT_PHASE_MISMATCH`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=STATE-004, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

每条合法边、每条非法跳边、exchange开关、响应循环、终止吸收；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(STATE-004-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(STATE-004-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(STATE-004-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## STATE-005 不可变 PlayerView 状态载体

### 1. 单元ID与名称

`STATE-005` — 不可变 PlayerView 状态载体。

### 2. 类型

状态管理；`catalog_type=state_management`；确定性、不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `frozen seat view`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 不可变 PlayerView 状态载体 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：ALGO-010；下游：ALGO-003、HEUR-006/007/016/020、MODEL-001、STATE-006/009、TRAIN-002。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 STATE-005 行及其 AU/章节锚点为准；参数：验证builder输出符合RULE-016 schema→深冻结嵌套集合→附view/schema/state版本与seat→计算稳定hash→交付只读对象。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

创建、读取、迁移或提交对应状态；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `builder output`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

生命周期字段至少含 `version`、`phase/status`、`owner`、`created_event`、`updated_event`；具体领域字段见输入输出与流程。

### 11. 完整处理流程

构建后不可变；无权威对象引用；hash覆盖全部字段；只含白名单→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `frozen seat view`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

VIEW_SCHEMA_INVALID、MUTATION_ATTEMPT、LEAK_DETECTED、VERSION_MISMATCH；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`深层mutation、四座差异、序列化往返、hash稳定、隐藏字段扫描`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=STATE-005, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(STATE-005-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(STATE-005-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(STATE-005-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## STATE-006 策略侧认知运行态初始化与归档

### 1. 单元ID与名称

`STATE-006` — 策略侧认知运行态初始化与归档。

### 2. 类型

状态管理；`catalog_type=state_management`；确定性、不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `cognition state/snapshot`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 策略侧认知运行态初始化与归档 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-001、STATE-005、STATE-010；下游：AUDIT-002、HEUR-005/019/020/022、STATE-008。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 STATE-006 行及其 AU/章节锚点为准；参数：RP-001～RP-033。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

创建、读取、迁移或提交对应状态；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `round start/end`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

生命周期字段至少含 `version`、`phase/status`、`owner`、`created_event`、`updated_event`；具体领域字段见输入输出与流程。

### 11. 完整处理流程

按seat/profile/RP初始化策略私有认知→仅用PlayerView事件更新→决策期间版本化→局末生成不可变摘要→仅经STATE-008白名单继承→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `cognition state/snapshot`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

认知态不得写入/影响权威合法性；不得包含oracle；每座隔离；相同输入序列结果唯一；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`COGNITION_INIT_FAILED、VIEW_VERSION_STALE、ORACLE_INPUT、CROSS_SEAT_ACCESS`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=STATE-006, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

四座隔离、同事件复算、乱序拒绝、局末归档、GameState字段扫描；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(STATE-006-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(STATE-006-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(STATE-006-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## STATE-007 存档 schema 持久化与迁移

### 1. 单元ID与名称

`STATE-007` — 存档 schema 持久化与迁移。

### 2. 类型

状态管理；`catalog_type=state_management`；确定性、不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `current state or error`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 存档 schema 持久化与迁移 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-002、ALGO-009；下游：AUDIT-004、AUDIT-011。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 STATE-007 行及其 AU/章节锚点为准；参数：GP-001。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

创建、读取、迁移或提交对应状态；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `state v1–v5`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

生命周期字段至少含 `version`、`phase/status`、`owner`、`created_event`、`updated_event`；具体领域字段见输入输出与流程。

### 11. 完整处理流程

读取schema_version→校验支持范围→逐版本顺序迁移且记录步骤→构造当前状态→运行完整不变量→规范序列化与hash；未知或损坏输入拒绝→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `current state or error`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

迁移不跳版；原输入不变；成功结果为当前schema；相同字节与版本结果唯一；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`UNSUPPORTED_SCHEMA、MIGRATION_FAILED、CORRUPT_SAVE、HASH_MISMATCH`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=STATE-007, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

v1..v5真实/合成夹具、缺字段、未知未来版、重复迁移幂等、往返；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(STATE-007-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(STATE-007-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(STATE-007-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## STATE-008 跨局比分、认知和 episode 状态继承

### 1. 单元ID与名称

`STATE-008` — 跨局比分、认知和 episode 状态继承。

### 2. 类型

状态管理；`catalog_type=state_management`；确定性、不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `next-round context`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 跨局比分、认知和 episode 状态继承 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-001、SCORE-006、STATE-006；下游：MODEL-003。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 STATE-008 行及其 AU/章节锚点为准；参数：GP-001～GP-027、RP-024～RP-032。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

创建、读取、迁移或提交对应状态；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `round result`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

生命周期字段至少含 `version`、`phase/status`、`owner`、`created_event`、`updated_event`；具体领域字段见输入输出与流程。

### 11. 完整处理流程

验证局结果已settled→累计比分/排名→按白名单提取认知摘要和episode计数→重置局内手牌/墙/phase/过胡→派生下一局ID/seed→生成context→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `next-round context`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

不得继承手牌、牌墙、响应窗、过胡等局内状态；累计分守恒；继承字段有版本；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`ROUND_NOT_SETTLED、CARRYOVER_FORBIDDEN、SCORE_MISMATCH、EPISODE_VERSION`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=STATE-008, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

允许/禁止字段矩阵、多局累计、断点恢复、末局无next、相同序列复算；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(STATE-008-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(STATE-008-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(STATE-008-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## STATE-009 决策请求上下文与生命周期

### 1. 单元ID与名称

`STATE-009` — 决策请求上下文与生命周期。

### 2. 类型

状态管理；`catalog_type=state_management`；确定性、不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `request/result`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 决策请求上下文与生命周期 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-004、STATE-005、RULE-001；下游：ALGO-006/008、AUDIT-002、HEUR-017/019、STATE-012、TRAIN-003。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 STATE-009 行及其 AU/章节锚点为准；参数：创建唯一request_id并冻结seat/phase/view/legal/version/deadline→置pending→接收一次结果→校验request/seat/version/legal→提交resolved或转STATE-012→归档。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

创建、读取、迁移或提交对应状态；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `phase + PlayerView + legal set`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

生命周期字段至少含 `version`、`phase/status`、`owner`、`created_event`、`updated_event`；具体领域字段见输入输出与流程。

### 11. 完整处理流程

每请求最多一次有效结果；过期/重复/错seat不改变状态；legal与view版本绑定→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `request/result`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

REQUEST_EXPIRED、DUPLICATE_RESULT、WRONG_SEAT、STALE_VIEW、ACTION_NOT_LEGAL；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`正常、超期、重复、错座、旧view、并发返回、唯一动作`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

收集按 `request/window_id + seat` 去重；结果按座位环序和规则优先级规范化，禁止以线程/网络返回先后决胜。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=STATE-009, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

undefined；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(STATE-009-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(STATE-009-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(STATE-009-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## STATE-010 GP/RP/Profile 注册与生命周期

### 1. 单元ID与名称

`STATE-010` — GP/RP/Profile 注册与生命周期。

### 2. 类型

状态管理；`catalog_type=state_management`；确定性、不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `owned parameter state`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 GP/RP/Profile 注册与生命周期 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：无；下游：ALGO-007/009/011、HEUR-003/022、RULE-001/015/016、STATE-001/006、TRAIN-009。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 STATE-010 行及其 AU/章节锚点为准；参数：GP-001～GP-027、RP-001～RP-033。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

创建、读取、迁移或提交对应状态；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `source config + phase`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

生命周期字段至少含 `version`、`phase/status`、`owner`、`created_event`、`updated_event`；具体领域字段见输入输出与流程。

### 11. 完整处理流程

注册唯一ID/schema/owner/scope/default/range→解析全局及逐座profile→校验并冻结GP→每局初始化RP→记录版本/hash→按生命周期归档或重置→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `owned parameter state`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

ID唯一；GP整场冻结；RP仅在授权事件变化；逐座参数不得串座；未知字段显式拒绝；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`DUPLICATE_PARAMETER、UNKNOWN_PARAMETER、OUT_OF_RANGE、LIFECYCLE_VIOLATION、PROFILE_MISMATCH`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=STATE-010, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

全ID覆盖、默认/边界、未知/重复、四座差异、冻结修改、hash稳定；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(STATE-010-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(STATE-010-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(STATE-010-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## STATE-011 牌墙构建、洗牌与初始发牌

### 1. 单元ID与名称

`STATE-011` — 牌墙构建、洗牌与初始发牌。

### 2. 类型

状态管理；`catalog_type=state_management`；确定性、不可训练。使用随机数但随机流必须命名、种子必须冻结。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `wall/hands`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 牌墙构建、洗牌与初始发牌 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：ALGO-011；下游：ALGO-001/004/005、RULE-002/006/008/012、STATE-002。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 STATE-011 行及其 AU/章节锚点为准；参数：无直接登记。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

新局初始化；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `named RNG + player count`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

生命周期字段至少含 `version`、`phase/status`、`owner`、`created_event`、`updated_event`；具体领域字段见输入输出与流程。

### 11. 完整处理流程

构建108个唯一实体牌ID→使用shuffle命名随机流一次性洗牌→确定庄家→按冻结顺序每闲家13张、庄家14张→余牌保持严格顺序为wall→校验并发布→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `wall/hands`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

任一时刻108实体牌恰出现一次（手牌+副露+弃牌+墙+过渡+和牌占用）；初发4人墙55张；同game_id/规则/seed唯一；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`INVALID_PLAYER_COUNT、RNG_STREAM_MISSING、DECK_DUPLICATE、DEAL_COUNT、CONSERVATION_FAILED`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

单写者提交；多人输入先按事件ID和seat规范排序。并发读只见已提交快照，重复/迟到事件显式拒绝。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=STATE-011, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

108唯一、各座13/庄14、墙55、2/3/4人、同seed复现、不同seed、边界守恒；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(STATE-011-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(STATE-011-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(STATE-011-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。

## STATE-012 策略超时、崩溃与合法默认动作回退

### 1. 单元ID与名称

`STATE-012` — 策略超时、崩溃与合法默认动作回退。

### 2. 类型

状态管理；`catalog_type=state_management`；确定性、不可训练。不自行消费随机数。

### 3. 功能目标

在冻结输入、初始状态、规则版本与命名种子下，唯一产生 `fallback result`；相同输入、状态、规则和种子必须得到逐字段相同结果或同一错误码。

### 4. 职责范围

负责 策略超时、崩溃与合法默认动作回退 的权威判定、原子状态效果、确定性输出、失败回滚和审计字段；上游：STATE-009、ALGO-006；下游：AUDIT-006。

### 5. 明确不负责的内容

不负责策略偏好、启发式打分、模型训练、UI呈现及下游计分；不绕过相邻单元职责，不读取超出 RULE-016 的策略可见信息。

### 6. 来源规则与参数

来源以锁定目录 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 STATE-012 行及其 AU/章节锚点为准；参数：GP-024～GP-026、RP-024～RP-029。歧义必须新增决策记录，不静默推断。

### 7. 触发事件

决策失败或截止时刻；事件必须携带唯一 `event_id`、`game_id`、`state_version` 和规则/配置哈希。

### 8. 前置条件

规则与配置已校验并冻结；输入schema正确；seat、phase、actor、版本匹配；上游状态不变量已通过；所引用实体牌ID存在且归属明确。

### 9. 输入字段、类型、范围、可见性

| 字段 | 类型/范围 | 可见性 |
|---|---|---|
| domain_input | `request + deadline/failure + legal set`；非空且符合冻结schema | 权威私有；策略提交部分不得超出PlayerView |
| game_id / event_id | UTF-8非空稳定ID | 审计可见 |
| state_version | uint64，必须等于当前版本 | 权威私有 |
| ruleset_hash / seed_ref | 已注册hash/命名流引用 | 项目元数据；种子值私有 |
| actor/seat（适用时） | int，`0 <= seat < num_players` | 公开seat，权限私有 |

### 10. 内部状态

生命周期字段至少含 `version`、`phase/status`、`owner`、`created_event`、`updated_event`；具体领域字段见输入输出与流程。

### 11. 完整处理流程

识别timeout/crash/protocol/非法返回→冻结失败原因→若唯一合法动作直接选取，否则调用确定性默认排序→校验仍在原legal set→以fallback标记完成请求→审计→执行全局守恒/权限/版本检查→原子提交并写审计；任一步失败均不产生部分状态。

### 12. 状态转移

`RECEIVED → VALIDATED → RESOLVED → COMMITTED`；失败为 `RECEIVED|VALIDATED → REJECTED`。提交仅一次，版本成功时加1；REJECTED不改权威版本。

### 13. 输出字段、类型、范围

| 字段 | 类型/范围 |
|---|---|
| result | `fallback result`；规范排序、无歧义 |
| accepted | bool |
| next_state_version | uint64；成功=current+1，纯查询可=current |
| reason/error_code | 稳定枚举；成功为null |
| audit_ref | 非空事件引用 |
| deterministic_fingerprint | 输入/状态/规则/seed/result的稳定hash |

### 14. 后置条件

成功输出满足schema并已通过全部不变量；状态变更原子可回放；失败时权威状态逐字段不变；下游只能消费已提交版本。

### 15. 不变量

回退动作必合法；不使用隐藏信息；失败类型和候选相同则结果唯一；原迟到结果不得覆盖；此外，全局实体牌守恒、合法actor、版本单调、隐藏信息隔离和同输入确定性均为 hard gate。

### 16. 异常和错误码

`NO_LEGAL_FALLBACK、FALLBACK_ILLEGAL、REQUEST_ALREADY_RESOLVED、POLICY_TIMEOUT、POLICY_CRASH`；通用：`SCHEMA_INVALID`、`VERSION_CONFLICT`、`UNAUTHORIZED`、`DETERMINISM_VIOLATION`、`INVARIANT_FAILED`。未知错误不得伪装成功。

### 17. 并发或多人响应处理

收集按 `request/window_id + seat` 去重；结果按座位环序和规则优先级规范化，禁止以线程/网络返回先后决胜。

### 18. 日志字段

`timestamp_utc, game_id, round_id, event_id, unit_id=STATE-012, request/window_id, actor_seat, phase_before, phase_after, state_version_before, state_version_after, ruleset_hash, config_hash, seed_stream_ref, input_hash, result_hash, accepted, error_code, latency_us`。私有牌仅记录受控引用/hash。

### 19. 单元测试要求

超时/异常/坏协议/非法动作、唯一动作、多动作稳定排序、迟到竞争、空合法集；另须覆盖错误码精确值、失败零写入、100次复算指纹一致、输入容器/多人返回顺序置换不变、隐藏字段投毒不影响策略可见输出。

### 20. 验收标准

- [ ] 正常、边界、反例、版本冲突和失败路径全部通过。
- [ ] hard不变量逐事件执行，牌张守恒与信息隔离零失败。
- [ ] 相同输入/状态/规则/种子重复及回放结果逐字段一致。
- [ ] 多人/并发排列测试与串行权威结果一致。
- [ ] 证据达到E3（单元/契约）；P0集成路径达到E4；当前为 `Not Evaluated`。

### 21. 代码证据占位

`TODO(STATE-012-CODE)`：记录实现路径、符号、commit、逐断言映射；当前目录中的历史状态仅为候选，不作为本卡验收结论。

### 22. 测试证据占位

`TODO(STATE-012-TEST)`：记录测试路径、测试名、命令、环境、原始输出、结果hash；未进行本卡独立运行验收。

### 23. 运行证据占位

`TODO(STATE-012-RUN)`：保留OS/Python/commit、规则与配置hash、game_id/seed引用、运行命令、日志/回放产物和SHA-256；当前为 `Not Evaluated`。
# 3.0.1 试点澄清：RULE-016与STATE-005

## 3.0.2 RULE-003查询版本语义

`legal_discards`是纯查询：成功时`next_state_version=current_state_version`，不提交、不增版本、不写GameState；失败同样零写入。只有下游权威`apply_action`在再次验证后才可原子提交并使版本+1。查询audit必须记录`operation_kind=query,state_version_before=state_version_after`。

## RULE-016错误与测试契约（替代原第16、19节错位内容）

- 稳定错误码：`FIELD_NOT_WHITELISTED`（请求字段未登记）、`VISIBILITY_LEAK`（输出含对手暗手/墙序/oracle）、`INVALID_VIEWER`（viewer不在`[0,num_players)`）、`INVALID_PHASE`（phase不在冻结枚举），另适用通用错误码。
- 必测：逐phase×四seat白名单矩阵、嵌套未知字段默认删除、finished不公开墙序、序列化旁路、四座交叉泄漏、truth成对投毒、100次复算和输入键顺序置换。正常fixture中S0只见S0暗手；非法viewer=4（四人局）精确返回`INVALID_VIEWER`。

## STATE-005错误与测试契约（替代原第16、19节错位内容）

- 稳定错误码：`VIEW_SCHEMA_INVALID`、`MUTATION_ATTEMPT`、`LEAK_DETECTED`、`VERSION_MISMATCH`，另适用通用错误码。
- 必测：mapping/list/tuple三层深冻结、四座仅self字段不同、canonical序列化往返、全部字段hash稳定、隐藏字段递归扫描、mutation失败零写入、100次复算。hash输入固定为`view_version,state_version,seat,phase,payload`的canonical JSON UTF-8字节。
