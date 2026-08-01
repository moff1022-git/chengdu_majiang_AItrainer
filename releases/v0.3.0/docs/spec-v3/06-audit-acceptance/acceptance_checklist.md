# Spec v3 96单元验收清单

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 单元覆盖 | 96/96 |
| 验收检查 | 1344项：每单元AC-01～AC-14 |
| 当前总体状态 | NOT_EVALUATED |

本清单是[audit_standard.md](audit_standard.md)的逐单元展开。全部检查均为hard；纯函数的状态写回项必须证明无副作用，不能N/A。代码路径均为开发任务卡建议位置，需经差距审计改为实际路径后才形成E2证据。

## RULE-001 规则、参数、不变量与合法性裁决优先级

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_001.py`；存在不代表通过 |
| 上游依赖 | `STATE-002|STATE-010|ALGO-009` |
| 参数绑定 | `GP-002, GP-008～GP-010、GP-008～GP-010、GP-001～GP-027` |
| 来源规则 | AU-001 人类化决策规则：第 0—6 章 / 0. 范围与合法性优先；AU-031 人类化决策规则：第 7—14 章 / 9.1 响应优先；AU-052 程序实现规范：第 0—10 章 / 1.3 冲突裁决 |
| 父测试合同 | T-RULE-001-N01、T-RULE-001-B01、T-RULE-001-I01、T-RULE-001-P01、T-RULE-001-R01、T-RULE-001-X01 |
| 细化测试卡 | `TC-RULE-001-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_001.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-001-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-001-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-001-01`～`AC-RULE-001-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-002 换三张同花色、方向与提交合法性

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_002.py`；存在不代表通过 |
| 上游依赖 | `STATE-003|STATE-011|ALGO-001` |
| 参数绑定 | `GP-005, GP-006, RP-001, RP-002、GP-002～GP-020` |
| 来源规则 | AU-010 人类化决策规则：第 0—6 章 / 5. 换三张合法性；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine |
| 父测试合同 | T-RULE-002-N01、T-RULE-002-B01、T-RULE-002-I01、T-RULE-002-P01、T-RULE-002-R01、T-RULE-002-X01 |
| 细化测试卡 | `TC-RULE-002-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_002.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-002-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-002-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-002-01`～`AC-RULE-002-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-003 定缺未清时的强制出牌约束

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_003.py`；存在不代表通过 |
| 上游依赖 | `STATE-003` |
| 参数绑定 | `GP-002, RP-003、GP-002～GP-020、GP-008～GP-010、无直接GP/RP；测试追踪` |
| 来源规则 | AU-013 人类化决策规则：第 0—6 章 / 6. 清缺约束；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine；AU-072 程序实现规范：第 0—10 章 / 8. 合法行动与解析；AU-087 程序实现规范：第 11—19 章 / 14.1 每事件断言 |
| 父测试合同 | T-RULE-003-N01、T-RULE-003-B01、T-RULE-003-I01、T-RULE-003-P01、T-RULE-003-R01、T-RULE-003-X01 |
| 细化测试卡 | `TC-RULE-003-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_003.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-003-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-003-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-003-01`～`AC-RULE-003-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-004 定缺、死叫与胡牌资格约束

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_004.py`；存在不代表通过 |
| 上游依赖 | `STATE-003|ALGO-002` |
| 参数绑定 | `GP-002, RP-003、GP-002～GP-020、GP-008～GP-010、无直接GP/RP；测试追踪` |
| 来源规则 | AU-013 人类化决策规则：第 0—6 章 / 6. 清缺约束；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine；AU-072 程序实现规范：第 0—10 章 / 8. 合法行动与解析；AU-087 程序实现规范：第 11—19 章 / 14.1 每事件断言 |
| 父测试合同 | T-RULE-004-N01、T-RULE-004-B01、T-RULE-004-I01、T-RULE-004-P01、T-RULE-004-R01、T-RULE-004-X01 |
| 细化测试卡 | `TC-RULE-004-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_004.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-004-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-004-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-004-01`～`AC-RULE-004-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-005 座位、庄家与活动顺序

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_005.py`；存在不代表通过 |
| 上游依赖 | `STATE-002` |
| 参数绑定 | `GP-003、GP-002～GP-020、RP-006～RP-018、无直接GP/RP；测试追踪` |
| 来源规则 | AU-006 人类化决策规则：第 0—6 章 / 3. 定庄与座位；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine；AU-065 程序实现规范：第 0—10 章 / 4.2 玩家与活动顺序；AU-087 程序实现规范：第 11—19 章 / 14.1 每事件断言 |
| 父测试合同 | T-RULE-005-N01、T-RULE-005-B01、T-RULE-005-I01、T-RULE-005-P01、T-RULE-005-R01、T-RULE-005-X01 |
| 细化测试卡 | `TC-RULE-005-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_005.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-005-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-005-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-005-01`～`AC-RULE-005-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-006 摸牌、可选响应与出牌标准顺序

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_006.py`；存在不代表通过 |
| 上游依赖 | `STATE-004|STATE-011` |
| 参数绑定 | `RP-023～RP-029、GP-002～GP-020` |
| 来源规则 | AU-035 人类化决策规则：第 7—14 章 / 9.5 摸牌后判断；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine |
| 父测试合同 | T-RULE-006-N01、T-RULE-006-B01、T-RULE-006-I01、T-RULE-006-P01、T-RULE-006-R01、T-RULE-006-X01 |
| 细化测试卡 | `TC-RULE-006-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_006.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-006-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-006-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-006-01`～`AC-RULE-006-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-007 碰牌资格、执行与后续出牌

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_007.py`；存在不代表通过 |
| 上游依赖 | `RULE-001|STATE-003` |
| 参数绑定 | `GP-008, GP-023、GP-002～GP-020、GP-008～GP-010` |
| 来源规则 | AU-034 人类化决策规则：第 7—14 章 / 9.4 碰牌响应；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine；AU-072 程序实现规范：第 0—10 章 / 8. 合法行动与解析 |
| 父测试合同 | T-RULE-007-N01、T-RULE-007-B01、T-RULE-007-I01、T-RULE-007-P01、T-RULE-007-R01、T-RULE-007-X01 |
| 细化测试卡 | `TC-RULE-007-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_007.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-007-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-007-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-007-01`～`AC-RULE-007-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-008 明杠、暗杠与补杠资格及执行

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_008.py`；存在不代表通过 |
| 上游依赖 | `RULE-001|STATE-003|STATE-011` |
| 参数绑定 | `GP-014～GP-020、GP-002～GP-020、GP-008～GP-010` |
| 来源规则 | AU-033 人类化决策规则：第 7—14 章 / 9.3 杠牌响应；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine；AU-072 程序实现规范：第 0—10 章 / 8. 合法行动与解析 |
| 父测试合同 | T-RULE-008-N01、T-RULE-008-B01、T-RULE-008-I01、T-RULE-008-P01、T-RULE-008-R01、T-RULE-008-X01 |
| 细化测试卡 | `TC-RULE-008-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_008.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-008-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-008-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-008-01`～`AC-RULE-008-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-009 补杠抢杠胡窗口与解析

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_009.py`；存在不代表通过 |
| 上游依赖 | `RULE-008|RULE-010` |
| 参数绑定 | `GP-014～GP-020、GP-002～GP-020、GP-008～GP-010` |
| 来源规则 | AU-033 人类化决策规则：第 7—14 章 / 9.3 杠牌响应；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine；AU-072 程序实现规范：第 0—10 章 / 8. 合法行动与解析 |
| 父测试合同 | T-RULE-009-N01、T-RULE-009-B01、T-RULE-009-I01、T-RULE-009-P01、T-RULE-009-R01、T-RULE-009-X01 |
| 细化测试卡 | `TC-RULE-009-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_009.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-009-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-009-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-009-01`～`AC-RULE-009-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-010 自摸、点炮与抢杠胡资格

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_010.py`；存在不代表通过 |
| 上游依赖 | `RULE-001|STATE-003|ALGO-002` |
| 参数绑定 | `GP-009, GP-010、GP-002～GP-020、GP-008～GP-010` |
| 来源规则 | AU-032 人类化决策规则：第 7—14 章 / 9.2 胡牌响应；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine；AU-072 程序实现规范：第 0—10 章 / 8. 合法行动与解析 |
| 父测试合同 | T-RULE-010-N01、T-RULE-010-B01、T-RULE-010-I01、T-RULE-010-P01、T-RULE-010-R01、T-RULE-010-X01 |
| 细化测试卡 | `TC-RULE-010-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_010.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-010-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-010-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-010-01`～`AC-RULE-010-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-011 过胡设置、持续与恢复

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_011.py`；存在不代表通过 |
| 上游依赖 | `RULE-010|STATE-003` |
| 参数绑定 | `GP-009, GP-010、GP-002～GP-020、GP-008～GP-010` |
| 来源规则 | AU-032 人类化决策规则：第 7—14 章 / 9.2 胡牌响应；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine；AU-072 程序实现规范：第 0—10 章 / 8. 合法行动与解析 |
| 父测试合同 | T-RULE-011-N01、T-RULE-011-B01、T-RULE-011-I01、T-RULE-011-P01、T-RULE-011-R01、T-RULE-011-X01 |
| 细化测试卡 | `TC-RULE-011-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_011.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-011-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-011-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-011-01`～`AC-RULE-011-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-012 强制胡与最后阶段必胡

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_012.py`；存在不代表通过 |
| 上游依赖 | `RULE-010|STATE-011` |
| 参数绑定 | `GP-009, GP-010、GP-002～GP-020、GP-008～GP-010` |
| 来源规则 | AU-032 人类化决策规则：第 7—14 章 / 9.2 胡牌响应；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine；AU-072 程序实现规范：第 0—10 章 / 8. 合法行动与解析 |
| 父测试合同 | T-RULE-012-N01、T-RULE-012-B01、T-RULE-012-I01、T-RULE-012-P01、T-RULE-012-R01、T-RULE-012-X01 |
| 细化测试卡 | `TC-RULE-012-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_012.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-012-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-012-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-012-01`～`AC-RULE-012-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-013 多人响应确定性优先级

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_013.py`；存在不代表通过 |
| 上游依赖 | `RULE-001|RULE-007|RULE-009|RULE-010` |
| 参数绑定 | `GP-008～GP-010、GP-002～GP-020、RP-024～RP-032` |
| 来源规则 | AU-031 人类化决策规则：第 7—14 章 / 9.1 响应优先；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine；AU-060 程序实现规范：第 0—10 章 / 3.6 Action Resolver；AU-072 程序实现规范：第 0—10 章 / 8. 合法行动与解析 |
| 父测试合同 | T-RULE-013-N01、T-RULE-013-B01、T-RULE-013-I01、T-RULE-013-P01、T-RULE-013-R01、T-RULE-013-X01 |
| 细化测试卡 | `TC-RULE-013-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_013.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-013-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-013-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-013-01`～`AC-RULE-013-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-014 血战胡后退出、继续与终止

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_014.py`；存在不代表通过 |
| 上游依赖 | `RULE-005|RULE-010|STATE-004` |
| 参数绑定 | `GP-003、RP-018, RP-021、GP-011～GP-020、GP-002～GP-020` |
| 来源规则 | AU-006 人类化决策规则：第 0—6 章 / 3. 定庄与座位；AU-018 人类化决策规则：第 7—14 章 / 7.9 胡牌人数；AU-039 人类化决策规则：第 7—14 章 / 11. 胡后处理；AU-056 程序实现规范：第 0—10 章 / 3.2 Rule Engine |
| 父测试合同 | T-RULE-014-N01、T-RULE-014-B01、T-RULE-014-I01、T-RULE-014-P01、T-RULE-014-R01、T-RULE-014-X01 |
| 细化测试卡 | `TC-RULE-014-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_014.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-014-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-014-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-014-01`～`AC-RULE-014-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-015 启用番型、互斥/叠加与封顶规则

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_015.py`；存在不代表通过 |
| 上游依赖 | `STATE-010` |
| 参数绑定 | `GP-001～GP-027、GP-011～GP-020` |
| 来源规则 | AU-004 人类化决策规则：第 0—6 章 / 2. 学习规则；AU-022 人类化决策规则：第 7—14 章 / 7.14 全番型配置 |
| 父测试合同 | T-RULE-015-N01、T-RULE-015-B01、T-RULE-015-I01、T-RULE-015-P01、T-RULE-015-R01、T-RULE-015-X01 |
| 细化测试卡 | `TC-RULE-015-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_015.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-015-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-015-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-015-01`～`AC-RULE-015-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## RULE-016 局中与终局公开信息范围

| 字段 | 内容 |
|---|---|
| 类型 | 确定规则 |
| 代码入口候选 | `engine/rules/rule_016.py`；存在不代表通过 |
| 上游依赖 | `STATE-004|STATE-010` |
| 参数绑定 | `GP-021、GP-021, RP-031` |
| 来源规则 | AU-002 人类化决策规则：第 0—6 章 / 0. 可见信息边界；AU-029 人类化决策规则：第 7—14 章 / 8.8 信息边界 |
| 父测试合同 | T-RULE-016-N01、T-RULE-016-B01、T-RULE-016-I01、T-RULE-016-P01、T-RULE-016-R01、T-RULE-016-X01 |
| 细化测试卡 | `TC-RULE-016-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_rule_016.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-RULE-016-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-RULE-016-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-RULE-016-01`～`AC-RULE-016-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## ALGO-001 face/physical tile 编码、投影与所有权守恒

| 字段 | 内容 |
|---|---|
| 类型 | 确定算法 |
| 代码入口候选 | `engine/analysis/algo_001.py`；存在不代表通过 |
| 上游依赖 | `STATE-011` |
| 参数绑定 | `GP-005, GP-006, RP-001, RP-002、GP-001～GP-027, RP-001～RP-033、RP-003～RP-005、GP-011～GP-020` |
| 来源规则 | AU-010 人类化决策规则：第 0—6 章 / 5. 换三张合法性；AU-053 程序实现规范：第 0—10 章 / 2. IR-001～018；AU-064 程序实现规范：第 0—10 章 / 4.1 牌编码；AU-066 程序实现规范：第 0—10 章 / 4.3 手牌与组合 |
| 父测试合同 | T-ALGO-001-N01、T-ALGO-001-B01、T-ALGO-001-I01、T-ALGO-001-P01、T-ALGO-001-R01、T-ALGO-001-X01 |
| 细化测试卡 | `TC-ALGO-001-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_algo_001.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-ALGO-001-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-ALGO-001-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：Approved规范golden、顺序置换、跨进程复算0偏差；浮点仅卡内误差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-ALGO-001-01`～`AC-ALGO-001-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## ALGO-002 手牌分解、向听、弃牌向听与等待形状

| 字段 | 内容 |
|---|---|
| 类型 | 确定算法 |
| 代码入口候选 | `engine/analysis/algo_002.py`；存在不代表通过 |
| 上游依赖 | `STATE-003` |
| 参数绑定 | `RP-003～RP-005、RP-003～RP-005, RP-019` |
| 来源规则 | AU-008 人类化决策规则：第 0—6 章 / 4. 初始手牌整理；AU-036 人类化决策规则：第 7—14 章 / 10.1–10.5 出牌；AU-074 程序实现规范：第 0—10 章 / 10.1 手牌分析 |
| 父测试合同 | T-ALGO-002-N01、T-ALGO-002-B01、T-ALGO-002-I01、T-ALGO-002-P01、T-ALGO-002-R01、T-ALGO-002-X01 |
| 细化测试卡 | `TC-ALGO-002-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_algo_002.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-ALGO-002-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-ALGO-002-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：Approved规范golden、顺序置换、跨进程复算0偏差；浮点仅卡内误差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-ALGO-002-01`～`AC-ALGO-002-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## ALGO-003 去重可见牌与未见牌聚合

| 字段 | 内容 |
|---|---|
| 类型 | 确定算法 |
| 代码入口候选 | `engine/analysis/algo_003.py`；存在不代表通过 |
| 上游依赖 | `STATE-005|ALGO-001` |
| 参数绑定 | `RP-014～RP-018, RP-021、RP-006～RP-018、GP-001～GP-027, RP-001～RP-033、GP-001～GP-027` |
| 来源规则 | AU-023 人类化决策规则：第 7—14 章 / 7.15 活牌与摸牌机会；AU-050 人类化决策规则：第 15—18 章与参数 / 18. 概率约束；AU-053 程序实现规范：第 0—10 章 / 2. IR-001～018；AU-067 程序实现规范：第 0—10 章 / 4.4 可见牌；AU-075 程序实现规范：第 0—10 章 / 10.2–10.5 信念/风险 |
| 父测试合同 | T-ALGO-003-N01、T-ALGO-003-B01、T-ALGO-003-I01、T-ALGO-003-P01、T-ALGO-003-R01、T-ALGO-003-X01 |
| 细化测试卡 | `TC-ALGO-003-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_algo_003.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-ALGO-003-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-ALGO-003-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：Approved规范golden、顺序置换、跨进程复算0偏差；浮点仅卡内误差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-ALGO-003-01`～`AC-ALGO-003-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## ALGO-004 墙内活牌区间或估计

| 字段 | 内容 |
|---|---|
| 类型 | 确定算法 |
| 代码入口候选 | `engine/analysis/algo_004.py`；存在不代表通过 |
| 上游依赖 | `ALGO-003|STATE-011` |
| 参数绑定 | `RP-014～RP-018, RP-021、RP-006～RP-018、GP-001～GP-027, RP-001～RP-033、GP-001～GP-027` |
| 来源规则 | AU-023 人类化决策规则：第 7—14 章 / 7.15 活牌与摸牌机会；AU-050 人类化决策规则：第 15—18 章与参数 / 18. 概率约束；AU-053 程序实现规范：第 0—10 章 / 2. IR-001～018；AU-075 程序实现规范：第 0—10 章 / 10.2–10.5 信念/风险 |
| 父测试合同 | T-ALGO-004-N01、T-ALGO-004-B01、T-ALGO-004-I01、T-ALGO-004-P01、T-ALGO-004-R01、T-ALGO-004-X01 |
| 细化测试卡 | `TC-ALGO-004-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_algo_004.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-ALGO-004-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-ALGO-004-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：Approved规范golden、顺序置换、跨进程复算0偏差；浮点仅卡内误差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-ALGO-004-01`～`AC-ALGO-004-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## ALGO-005 逐座剩余摸牌机会估计

| 字段 | 内容 |
|---|---|
| 类型 | 确定算法 |
| 代码入口候选 | `engine/analysis/algo_005.py`；存在不代表通过 |
| 上游依赖 | `RULE-005|STATE-011` |
| 参数绑定 | `RP-014～RP-018, RP-021、RP-018, RP-021、GP-001～GP-027, RP-001～RP-033、GP-021, RP-001～RP-023` |
| 来源规则 | AU-023 人类化决策规则：第 7—14 章 / 7.15 活牌与摸牌机会；AU-030 人类化决策规则：第 7—14 章 / 8.9 剩余机会；AU-053 程序实现规范：第 0—10 章 / 2. IR-001～018；AU-076 程序实现规范：第 0—10 章 / 10.6–10.9 注意/记忆/摸牌/Q |
| 父测试合同 | T-ALGO-005-N01、T-ALGO-005-B01、T-ALGO-005-I01、T-ALGO-005-P01、T-ALGO-005-R01、T-ALGO-005-X01 |
| 细化测试卡 | `TC-ALGO-005-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_algo_005.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-ALGO-005-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-ALGO-005-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：Approved规范golden、顺序置换、跨进程复算0偏差；浮点仅卡内误差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-ALGO-005-01`～`AC-ALGO-005-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## ALGO-006 mandatory 分类、候选上限与稳定排序

| 字段 | 内容 |
|---|---|
| 类型 | 确定算法 |
| 代码入口候选 | `engine/analysis/algo_006.py`；存在不代表通过 |
| 上游依赖 | `RULE-001|STATE-009` |
| 参数绑定 | `GP-002, GP-008～GP-010、RP-023～RP-029、GP-001～GP-027, RP-001～RP-033、GP-023～GP-027, RP-001～RP-033、GP-023～GP-027, RP-019～RP-029` |
| 来源规则 | AU-001 人类化决策规则：第 0—6 章 / 0. 范围与合法性优先；AU-035 人类化决策规则：第 7—14 章 / 9.5 摸牌后判断；AU-053 程序实现规范：第 0—10 章 / 2. IR-001～018；AU-059 程序实现规范：第 0—10 章 / 3.5 Human-like Policy；AU-073 程序实现规范：第 0—10 章 / 9. AI 决策管线 |
| 父测试合同 | T-ALGO-006-N01、T-ALGO-006-B01、T-ALGO-006-I01、T-ALGO-006-P01、T-ALGO-006-R01、T-ALGO-006-X01 |
| 细化测试卡 | `TC-ALGO-006-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_algo_006.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-ALGO-006-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-ALGO-006-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：Approved规范golden、顺序置换、跨进程复算0偏差；浮点仅卡内误差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-ALGO-006-01`～`AC-ALGO-006-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## ALGO-007 六分量候选 Q 评价

| 字段 | 内容 |
|---|---|
| 类型 | 确定算法 |
| 代码入口候选 | `engine/analysis/algo_007.py`；存在不代表通过 |
| 上游依赖 | `ALGO-002|ALGO-003|ALGO-005|STATE-010` |
| 参数绑定 | `GP-025, RP-019～RP-029、GP-023～GP-027, RP-001～RP-033、GP-023～GP-027, RP-019～RP-029、GP-021, RP-001～RP-023` |
| 来源规则 | AU-049 人类化决策规则：第 15—18 章与参数 / 18. Q 评价；AU-059 程序实现规范：第 0—10 章 / 3.5 Human-like Policy；AU-073 程序实现规范：第 0—10 章 / 9. AI 决策管线；AU-076 程序实现规范：第 0—10 章 / 10.6–10.9 注意/记忆/摸牌/Q |
| 父测试合同 | T-ALGO-007-N01、T-ALGO-007-B01、T-ALGO-007-I01、T-ALGO-007-P01、T-ALGO-007-R01、T-ALGO-007-X01 |
| 细化测试卡 | `TC-ALGO-007-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_algo_007.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-ALGO-007-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-ALGO-007-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：Approved规范golden、顺序置换、跨进程复算0偏差；浮点仅卡内误差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-ALGO-007-01`～`AC-ALGO-007-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## ALGO-008 seed、噪声、思考时间与随机流确定派生

| 字段 | 内容 |
|---|---|
| 类型 | 确定算法 |
| 代码入口候选 | `engine/analysis/algo_008.py`；存在不代表通过 |
| 上游依赖 | `ALGO-011|STATE-009` |
| 参数绑定 | `GP-024～GP-026, RP-024～RP-029、GP-023～GP-027, RP-019～RP-029、GP-001～GP-027` |
| 来源规则 | AU-042 人类化决策规则：第 7—14 章 / 14. 有限认知；AU-073 程序实现规范：第 0—10 章 / 9. AI 决策管线；AU-084 程序实现规范：第 11—19 章 / 12.3 确定性回放 |
| 父测试合同 | T-ALGO-008-N01、T-ALGO-008-B01、T-ALGO-008-I01、T-ALGO-008-P01、T-ALGO-008-R01、T-ALGO-008-X01 |
| 细化测试卡 | `TC-ALGO-008-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_algo_008.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-ALGO-008-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-ALGO-008-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：Approved规范golden、顺序置换、跨进程复算0偏差；浮点仅卡内误差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-ALGO-008-01`～`AC-ALGO-008-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## ALGO-009 配置类型/范围/版本校验、迁移与 canonical hash

| 字段 | 内容 |
|---|---|
| 类型 | 确定算法 |
| 代码入口候选 | `engine/analysis/algo_009.py`；存在不代表通过 |
| 上游依赖 | `STATE-010` |
| 参数绑定 | `GP-001～GP-027、GP-001` |
| 来源规则 | AU-004 人类化决策规则：第 0—6 章 / 2. 学习规则；AU-045 人类化决策规则：第 15—18 章与参数 / 17. GP 注册；AU-048 人类化决策规则：第 15—18 章与参数 / 18. 数值校验；AU-051 程序实现规范：第 0—10 章 / 0–1. 版本与源绑定；AU-069 程序实现规范：第 0—10 章 / 5. 配置模型；AU-095 程序实现规范：第 11—19 章 / 18. 版本/兼容 |
| 父测试合同 | T-ALGO-009-N01、T-ALGO-009-B01、T-ALGO-009-I01、T-ALGO-009-P01、T-ALGO-009-R01、T-ALGO-009-X01 |
| 细化测试卡 | `TC-ALGO-009-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_algo_009.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-ALGO-009-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-ALGO-009-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：Approved规范golden、顺序置换、跨进程复算0偏差；浮点仅卡内误差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-ALGO-009-01`～`AC-ALGO-009-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## ALGO-010 PlayerView 白名单构建

| 字段 | 内容 |
|---|---|
| 类型 | 确定算法 |
| 代码入口候选 | `engine/analysis/algo_010.py`；存在不代表通过 |
| 上游依赖 | `RULE-016|STATE-002` |
| 参数绑定 | `GP-021` |
| 来源规则 | AU-002 人类化决策规则：第 0—6 章 / 0. 可见信息边界；AU-058 程序实现规范：第 0—10 章 / 3.4 Player View |
| 父测试合同 | T-ALGO-010-N01、T-ALGO-010-B01、T-ALGO-010-I01、T-ALGO-010-P01、T-ALGO-010-R01、T-ALGO-010-X01 |
| 细化测试卡 | `TC-ALGO-010-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_algo_010.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-ALGO-010-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-ALGO-010-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：Approved规范golden、顺序置换、跨进程复算0偏差；浮点仅卡内误差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-ALGO-010-01`～`AC-ALGO-010-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## ALGO-011 game_id 到牌墙、骰子及子随机流的确定映射

| 字段 | 内容 |
|---|---|
| 类型 | 确定算法 |
| 代码入口候选 | `engine/analysis/algo_011.py`；存在不代表通过 |
| 上游依赖 | `STATE-010` |
| 参数绑定 | `无直接登记` |
| 来源规则 | 实现规范 §12.3；规则文档 §14.10–14.11 |
| 父测试合同 | T-ALGO-011-N01、T-ALGO-011-B01、T-ALGO-011-I01、T-ALGO-011-P01、T-ALGO-011-R01、T-ALGO-011-X01 |
| 细化测试卡 | `TC-ALGO-011-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_algo_011.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-ALGO-011-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-ALGO-011-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：Approved规范golden、顺序置换、跨进程复算0偏差；浮点仅卡内误差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-ALGO-011-01`～`AC-ALGO-011-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-001 换三张候选评价

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_001.py`；存在不代表通过 |
| 上游依赖 | `RULE-002|ALGO-002|ALGO-003` |
| 参数绑定 | `GP-023～GP-026` |
| 来源规则 | AU-011 人类化决策规则：第 0—6 章 / 5. 换牌策略 |
| 父测试合同 | T-HEUR-001-N01、T-HEUR-001-B01、T-HEUR-001-I01、T-HEUR-001-P01、T-HEUR-001-R01、T-HEUR-001-X01 |
| 细化测试卡 | `TC-HEUR-001-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_001.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-001-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-001-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-001-01`～`AC-HEUR-001-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-002 定缺花色评价

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_002.py`；存在不代表通过 |
| 上游依赖 | `RULE-003|ALGO-002` |
| 参数绑定 | `RP-003～RP-005` |
| 来源规则 | AU-012 人类化决策规则：第 0—6 章 / 6. 定缺选择 |
| 父测试合同 | T-HEUR-002-N01、T-HEUR-002-B01、T-HEUR-002-I01、T-HEUR-002-P01、T-HEUR-002-R01、T-HEUR-002-X01 |
| 细化测试卡 | `TC-HEUR-002-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_002.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-002-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-002-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-002-01`～`AC-HEUR-002-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-003 动态风格调节

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_003.py`；存在不代表通过 |
| 上游依赖 | `STATE-001|STATE-010|HEUR-022` |
| 参数绑定 | `GP-001～GP-027、GP-023～GP-027、GP-023～GP-026` |
| 来源规则 | AU-004 人类化决策规则：第 0—6 章 / 2. 学习规则；AU-005 人类化决策规则：第 0—6 章 / 2. 风格动态变化；AU-020 人类化决策规则：第 7—14 章 / 7.11 玩家风格/水平 |
| 父测试合同 | T-HEUR-003-N01、T-HEUR-003-B01、T-HEUR-003-I01、T-HEUR-003-P01、T-HEUR-003-R01、T-HEUR-003-X01 |
| 细化测试卡 | `TC-HEUR-003-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_003.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-003-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-003-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-003-01`～`AC-HEUR-003-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-004 初始做牌方向形成

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_004.py`；存在不代表通过 |
| 上游依赖 | `ALGO-002|HEUR-022` |
| 参数绑定 | `RP-003～RP-005、RP-019, RP-020、GP-023～GP-027, RP-001～RP-033` |
| 来源规则 | AU-008 人类化决策规则：第 0—6 章 / 4. 初始手牌整理；AU-014 人类化决策规则：第 7—14 章 / 7.1 做牌方向；AU-059 程序实现规范：第 0—10 章 / 3.5 Human-like Policy |
| 父测试合同 | T-HEUR-004-N01、T-HEUR-004-B01、T-HEUR-004-I01、T-HEUR-004-P01、T-HEUR-004-R01、T-HEUR-004-X01 |
| 细化测试卡 | `TC-HEUR-004-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_004.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-004-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-004-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-004-01`～`AC-HEUR-004-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-005 主备计划生命周期

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_005.py`；存在不代表通过 |
| 上游依赖 | `HEUR-004|STATE-006` |
| 参数绑定 | `RP-019, RP-020、RP-006～RP-020、RP-023～RP-029、GP-023～GP-027, RP-001～RP-033` |
| 来源规则 | AU-009 人类化决策规则：第 0—6 章 / 4. 初步计划可修正；AU-014 人类化决策规则：第 7—14 章 / 7.1 做牌方向；AU-017 人类化决策规则：第 7—14 章 / 7.4–7.8 动态调整；AU-025 人类化决策规则：第 7—14 章 / 7.17 主/备计划；AU-035 人类化决策规则：第 7—14 章 / 9.5 摸牌后判断；AU-059 程序实现规范：第 0—10 章 / 3.5 Human-like Policy |
| 父测试合同 | T-HEUR-005-N01、T-HEUR-005-B01、T-HEUR-005-I01、T-HEUR-005-P01、T-HEUR-005-R01、T-HEUR-005-X01 |
| 细化测试卡 | `TC-HEUR-005-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_005.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-005-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-005-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-005-01`～`AC-HEUR-005-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-006 定缺花色环境评估

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_006.py`；存在不代表通过 |
| 上游依赖 | `STATE-005` |
| 参数绑定 | `RP-006～RP-018` |
| 来源规则 | AU-015 人类化决策规则：第 7—14 章 / 7.2 花色环境 |
| 父测试合同 | T-HEUR-006-N01、T-HEUR-006-B01、T-HEUR-006-I01、T-HEUR-006-P01、T-HEUR-006-R01、T-HEUR-006-X01 |
| 细化测试卡 | `TC-HEUR-006-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_006.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-006-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-006-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-006-01`～`AC-HEUR-006-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-007 公开事件驱动的逐家方向更新

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_007.py`；存在不代表通过 |
| 上游依赖 | `HEUR-006|STATE-005|MODEL-001` |
| 参数绑定 | `RP-006～RP-020、RP-003～RP-021` |
| 来源规则 | AU-017 人类化决策规则：第 7—14 章 / 7.4–7.8 动态调整；AU-026 人类化决策规则：第 7—14 章 / 8.1–8.4 算牌顺序 |
| 父测试合同 | T-HEUR-007-N01、T-HEUR-007-B01、T-HEUR-007-I01、T-HEUR-007-P01、T-HEUR-007-R01、T-HEUR-007-X01 |
| 细化测试卡 | `TC-HEUR-007-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_007.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-007-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-007-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-007-01`～`AC-HEUR-007-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-008 整场比分与剩余局效用调节

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_008.py`；存在不代表通过 |
| 上游依赖 | `STATE-001|SCORE-006` |
| 参数绑定 | `GP-027, RP-022` |
| 来源规则 | AU-019 人类化决策规则：第 7—14 章 / 7.10 比分/剩余局 |
| 父测试合同 | T-HEUR-008-N01、T-HEUR-008-B01、T-HEUR-008-I01、T-HEUR-008-P01、T-HEUR-008-R01、T-HEUR-008-X01 |
| 细化测试卡 | `TC-HEUR-008-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_008.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-008-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-008-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-008-01`～`AC-HEUR-008-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-009 先胡、做大和血战顺序效用

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_009.py`；存在不代表通过 |
| 上游依赖 | `ALGO-002|ALGO-005|HEUR-008` |
| 参数绑定 | `RP-018, RP-021、RP-022, RP-023` |
| 来源规则 | AU-018 人类化决策规则：第 7—14 章 / 7.9 胡牌人数；AU-024 人类化决策规则：第 7—14 章 / 7.16 先胡/顺序 |
| 父测试合同 | T-HEUR-009-N01、T-HEUR-009-B01、T-HEUR-009-I01、T-HEUR-009-P01、T-HEUR-009-R01、T-HEUR-009-X01 |
| 细化测试卡 | `TC-HEUR-009-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_009.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-009-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-009-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-009-01`～`AC-HEUR-009-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-010 多目标冲突复核

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_010.py`；存在不代表通过 |
| 上游依赖 | `ALGO-007|HEUR-005|HEUR-008` |
| 参数绑定 | `RP-019, RP-020, RP-024～RP-029` |
| 来源规则 | AU-021 人类化决策规则：第 7—14 章 / 7.12–7.13 冲突与复核 |
| 父测试合同 | T-HEUR-010-N01、T-HEUR-010-B01、T-HEUR-010-I01、T-HEUR-010-P01、T-HEUR-010-R01、T-HEUR-010-X01 |
| 细化测试卡 | `TC-HEUR-010-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_010.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-010-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-010-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-010-01`～`AC-HEUR-010-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-011 番型边际做牌价值

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_011.py`；存在不代表通过 |
| 上游依赖 | `RULE-015|ALGO-002` |
| 参数绑定 | `GP-011～GP-020` |
| 来源规则 | AU-022 人类化决策规则：第 7—14 章 / 7.14 全番型配置 |
| 父测试合同 | T-HEUR-011-N01、T-HEUR-011-B01、T-HEUR-011-I01、T-HEUR-011-P01、T-HEUR-011-R01、T-HEUR-011-X01 |
| 细化测试卡 | `TC-HEUR-011-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_011.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-011-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-011-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-011-01`～`AC-HEUR-011-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-012 碰牌策略评价

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_012.py`；存在不代表通过 |
| 上游依赖 | `RULE-007|ALGO-002` |
| 参数绑定 | `GP-008, GP-023` |
| 来源规则 | AU-034 人类化决策规则：第 7—14 章 / 9.4 碰牌响应 |
| 父测试合同 | T-HEUR-012-N01、T-HEUR-012-B01、T-HEUR-012-I01、T-HEUR-012-P01、T-HEUR-012-R01、T-HEUR-012-X01 |
| 细化测试卡 | `TC-HEUR-012-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_012.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-012-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-012-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-012-01`～`AC-HEUR-012-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-013 杠牌策略评价

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_013.py`；存在不代表通过 |
| 上游依赖 | `RULE-008|RULE-009|SCORE-003|MODEL-002` |
| 参数绑定 | `GP-014～GP-020` |
| 来源规则 | AU-033 人类化决策规则：第 7—14 章 / 9.3 杠牌响应 |
| 父测试合同 | T-HEUR-013-N01、T-HEUR-013-B01、T-HEUR-013-I01、T-HEUR-013-P01、T-HEUR-013-R01、T-HEUR-013-X01 |
| 细化测试卡 | `TC-HEUR-013-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_013.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-013-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-013-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-013-01`～`AC-HEUR-013-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-014 出牌牌效与结构保留策略

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_014.py`；存在不代表通过 |
| 上游依赖 | `RULE-003|ALGO-002|HEUR-005` |
| 参数绑定 | `RP-003～RP-005, RP-019` |
| 来源规则 | AU-036 人类化决策规则：第 7—14 章 / 10.1–10.5 出牌 |
| 父测试合同 | T-HEUR-014-N01、T-HEUR-014-B01、T-HEUR-014-I01、T-HEUR-014-P01、T-HEUR-014-R01、T-HEUR-014-X01 |
| 细化测试卡 | `TC-HEUR-014-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_014.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-014-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-014-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-014-01`～`AC-HEUR-014-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-015 防守偏好与安全牌选择

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_015.py`；存在不代表通过 |
| 上游依赖 | `MODEL-002|HEUR-022` |
| 参数绑定 | `RP-006～RP-018、GP-001～GP-027` |
| 来源规则 | AU-037 人类化决策规则：第 7—14 章 / 10.6 防守风险；AU-075 程序实现规范：第 0—10 章 / 10.2–10.5 信念/风险 |
| 父测试合同 | T-HEUR-015-N01、T-HEUR-015-B01、T-HEUR-015-I01、T-HEUR-015-P01、T-HEUR-015-R01、T-HEUR-015-X01 |
| 细化测试卡 | `TC-HEUR-015-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_015.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-015-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-015-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-015-01`～`AC-HEUR-015-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-016 行为序列推断

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_016.py`；存在不代表通过 |
| 上游依赖 | `STATE-005|HEUR-020` |
| 参数绑定 | `RP-006～RP-017` |
| 来源规则 | AU-028 人类化决策规则：第 7—14 章 / 8.6–8.7 行为序列/反观察 |
| 父测试合同 | T-HEUR-016-N01、T-HEUR-016-B01、T-HEUR-016-I01、T-HEUR-016-P01、T-HEUR-016-R01、T-HEUR-016-X01 |
| 细化测试卡 | `TC-HEUR-016-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_016.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-016-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-016-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-016-01`～`AC-HEUR-016-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-017 思考节奏生成

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_017.py`；存在不代表通过 |
| 上游依赖 | `STATE-009|ALGO-008|HEUR-022` |
| 参数绑定 | `GP-024～GP-026, RP-024～RP-029` |
| 来源规则 | AU-038 人类化决策规则：第 7—14 章 / 10.7–10.13 人类表现 |
| 父测试合同 | T-HEUR-017-N01、T-HEUR-017-B01、T-HEUR-017-I01、T-HEUR-017-P01、T-HEUR-017-R01、T-HEUR-017-X01 |
| 细化测试卡 | `TC-HEUR-017-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_017.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-017-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-017-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-017-01`～`AC-HEUR-017-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-018 安全牌储备、扣牌与信息表达

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_018.py`；存在不代表通过 |
| 上游依赖 | `HEUR-015|HEUR-016` |
| 参数绑定 | `RP-006～RP-017、GP-024～GP-026, RP-024～RP-029` |
| 来源规则 | AU-028 人类化决策规则：第 7—14 章 / 8.6–8.7 行为序列/反观察；AU-038 人类化决策规则：第 7—14 章 / 10.7–10.13 人类表现 |
| 父测试合同 | T-HEUR-018-N01、T-HEUR-018-B01、T-HEUR-018-I01、T-HEUR-018-P01、T-HEUR-018-R01、T-HEUR-018-X01 |
| 细化测试卡 | `TC-HEUR-018-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_018.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-018-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-018-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-018-01`～`AC-HEUR-018-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-019 Top-K 有限注意分配

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_019.py`；存在不代表通过 |
| 上游依赖 | `STATE-006|STATE-009` |
| 参数绑定 | `RP-003～RP-021、GP-024～GP-026, RP-024～RP-029、GP-023～GP-027, RP-001～RP-033、GP-023～GP-027, RP-019～RP-029、GP-021, RP-001～RP-023` |
| 来源规则 | AU-026 人类化决策规则：第 7—14 章 / 8.1–8.4 算牌顺序；AU-042 人类化决策规则：第 7—14 章 / 14. 有限认知；AU-059 程序实现规范：第 0—10 章 / 3.5 Human-like Policy；AU-073 程序实现规范：第 0—10 章 / 9. AI 决策管线；AU-076 程序实现规范：第 0—10 章 / 10.6–10.9 注意/记忆/摸牌/Q |
| 父测试合同 | T-HEUR-019-N01、T-HEUR-019-B01、T-HEUR-019-I01、T-HEUR-019-P01、T-HEUR-019-R01、T-HEUR-019-X01 |
| 细化测试卡 | `TC-HEUR-019-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_019.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-019-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-019-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-019-01`～`AC-HEUR-019-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-020 有界记忆衰减与强化

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_020.py`；存在不代表通过 |
| 上游依赖 | `STATE-006|STATE-005` |
| 参数绑定 | `RP-001～RP-033、GP-024, RP-024、GP-011～GP-020、GP-023～GP-027, RP-024～RP-033、GP-023～GP-027, RP-001～RP-033、GP-021, RP-001～RP-023` |
| 来源规则 | AU-003 人类化决策规则：第 0—6 章 / 1. 游戏开始；AU-027 人类化决策规则：第 7—14 章 / 8.5 有限记忆；AU-039 人类化决策规则：第 7—14 章 / 11. 胡后处理；AU-041 人类化决策规则：第 7—14 章 / 13. 玩家模型；AU-059 程序实现规范：第 0—10 章 / 3.5 Human-like Policy；AU-076 程序实现规范：第 0—10 章 / 10.6–10.9 注意/记忆/摸牌/Q |
| 父测试合同 | T-HEUR-020-N01、T-HEUR-020-B01、T-HEUR-020-I01、T-HEUR-020-P01、T-HEUR-020-R01、T-HEUR-020-X01 |
| 细化测试卡 | `TC-HEUR-020-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_020.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-020-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-020-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-020-01`～`AC-HEUR-020-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-021 有限推演与满意停止

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_021.py`；存在不代表通过 |
| 上游依赖 | `ALGO-006|ALGO-007|HEUR-019` |
| 参数绑定 | `GP-024～GP-026, RP-024～RP-029、GP-023～GP-027, RP-001～RP-033、GP-023～GP-027, RP-019～RP-029` |
| 来源规则 | AU-042 人类化决策规则：第 7—14 章 / 14. 有限认知；AU-059 程序实现规范：第 0—10 章 / 3.5 Human-like Policy；AU-073 程序实现规范：第 0—10 章 / 9. AI 决策管线 |
| 父测试合同 | T-HEUR-021-N01、T-HEUR-021-B01、T-HEUR-021-I01、T-HEUR-021-P01、T-HEUR-021-R01、T-HEUR-021-X01 |
| 细化测试卡 | `TC-HEUR-021-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_021.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-021-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-021-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-021-01`～`AC-HEUR-021-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-022 人格、水平与情绪状态消费

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_022.py`；存在不代表通过 |
| 上游依赖 | `STATE-006|STATE-010` |
| 参数绑定 | `GP-023～GP-026、GP-023～GP-027, RP-024～RP-033` |
| 来源规则 | AU-020 人类化决策规则：第 7—14 章 / 7.11 玩家风格/水平；AU-041 人类化决策规则：第 7—14 章 / 13. 玩家模型 |
| 父测试合同 | T-HEUR-022-N01、T-HEUR-022-B01、T-HEUR-022-I01、T-HEUR-022-P01、T-HEUR-022-R01、T-HEUR-022-X01 |
| 细化测试卡 | `TC-HEUR-022-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_022.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-022-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-022-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-022-01`～`AC-HEUR-022-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## HEUR-023 有界近似选择与人类失误

| 字段 | 内容 |
|---|---|
| 类型 | 启发式策略 |
| 代码入口候选 | `players/humanlike/heuristics/heur_023.py`；存在不代表通过 |
| 上游依赖 | `ALGO-006|ALGO-007|ALGO-008|HEUR-022` |
| 参数绑定 | `GP-024～GP-026, RP-024～RP-029、GP-023～GP-027, RP-001～RP-033、GP-023～GP-027, RP-019～RP-029` |
| 来源规则 | AU-038 人类化决策规则：第 7—14 章 / 10.7–10.13 人类表现；AU-042 人类化决策规则：第 7—14 章 / 14. 有限认知；AU-059 程序实现规范：第 0—10 章 / 3.5 Human-like Policy；AU-073 程序实现规范：第 0—10 章 / 9. AI 决策管线 |
| 父测试合同 | T-HEUR-023-N01、T-HEUR-023-B01、T-HEUR-023-I01、T-HEUR-023-P01、T-HEUR-023-R01、T-HEUR-023-X01 |
| 细化测试卡 | `TC-HEUR-023-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_heur_023.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-HEUR-023-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-HEUR-023-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-HEUR-023-01`～`AC-HEUR-023-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## MODEL-001 逐对手归一化方向/牌型假设

| 字段 | 内容 |
|---|---|
| 类型 | 概率模型 |
| 代码入口候选 | `players/humanlike/models/model_001.py`；存在不代表通过 |
| 上游依赖 | `ALGO-003|HEUR-020|STATE-005` |
| 参数绑定 | `RP-006～RP-017、RP-006～RP-018、GP-023～GP-027, RP-001～RP-033、GP-001～GP-027` |
| 来源规则 | AU-007 人类化决策规则：第 0—6 章 / 3. 独立对手模型；AU-016 人类化决策规则：第 7—14 章 / 7.3 逐家方向；AU-050 人类化决策规则：第 15—18 章与参数 / 18. 概率约束；AU-059 程序实现规范：第 0—10 章 / 3.5 Human-like Policy；AU-075 程序实现规范：第 0—10 章 / 10.2–10.5 信念/风险 |
| 父测试合同 | T-MODEL-001-N01、T-MODEL-001-B01、T-MODEL-001-I01、T-MODEL-001-P01、T-MODEL-001-R01、T-MODEL-001-X01 |
| 细化测试卡 | `TC-MODEL-001-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_model_001.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-MODEL-001-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-MODEL-001-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：冻结切分Brier/log loss/ECE/可靠性/不确定性及规则回退达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-MODEL-001-01`～`AC-MODEL-001-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## MODEL-002 逐对手听牌/等待/损失风险模型

| 字段 | 内容 |
|---|---|
| 类型 | 概率模型 |
| 代码入口候选 | `players/humanlike/models/model_002.py`；存在不代表通过 |
| 上游依赖 | `MODEL-001|ALGO-003|ALGO-004` |
| 参数绑定 | `RP-006～RP-018、GP-023～GP-027, RP-001～RP-033、GP-001～GP-027` |
| 来源规则 | AU-037 人类化决策规则：第 7—14 章 / 10.6 防守风险；AU-050 人类化决策规则：第 15—18 章与参数 / 18. 概率约束；AU-059 程序实现规范：第 0—10 章 / 3.5 Human-like Policy；AU-075 程序实现规范：第 0—10 章 / 10.2–10.5 信念/风险 |
| 父测试合同 | T-MODEL-002-N01、T-MODEL-002-B01、T-MODEL-002-I01、T-MODEL-002-P01、T-MODEL-002-R01、T-MODEL-002-X01 |
| 细化测试卡 | `TC-MODEL-002-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_model_002.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-MODEL-002-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-MODEL-002-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：冻结切分Brier/log loss/ECE/可靠性/不确定性及规则回退达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-MODEL-002-01`～`AC-MODEL-002-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## MODEL-003 仅公开信息的跨局对手画像学习

| 字段 | 内容 |
|---|---|
| 类型 | 概率模型 |
| 代码入口候选 | `players/humanlike/models/model_003.py`；存在不代表通过 |
| 上游依赖 | `HEUR-020|STATE-008|RULE-016` |
| 参数绑定 | `RP-001～RP-033、GP-023～GP-027, RP-024～RP-033、RP-033` |
| 来源规则 | AU-003 人类化决策规则：第 0—6 章 / 1. 游戏开始；AU-041 人类化决策规则：第 7—14 章 / 13. 玩家模型；AU-047 人类化决策规则：第 15—18 章与参数 / 17. RP-033 学习输出 |
| 父测试合同 | T-MODEL-003-N01、T-MODEL-003-B01、T-MODEL-003-I01、T-MODEL-003-P01、T-MODEL-003-R01、T-MODEL-003-X01 |
| 细化测试卡 | `TC-MODEL-003-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_model_003.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-MODEL-003-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-MODEL-003-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：冻结切分Brier/log loss/ECE/可靠性/不确定性及规则回退达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-MODEL-003-01`～`AC-MODEL-003-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## MODEL-004 可训练策略输入输出契约

| 字段 | 内容 |
|---|---|
| 类型 | 可训练模型 |
| 代码入口候选 | `players/humanlike/models/model_004.py`；存在不代表通过 |
| 上游依赖 | `TRAIN-002|TRAIN-003` |
| 参数绑定 | `GP-008～GP-010` |
| 来源规则 | AU-077 程序实现规范：第 11—19 章 / 11.1 训练模式 |
| 父测试合同 | T-MODEL-004-N01、T-MODEL-004-B01、T-MODEL-004-I01、T-MODEL-004-P01、T-MODEL-004-R01、T-MODEL-004-X01 |
| 细化测试卡 | `TC-MODEL-004-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_model_004.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-MODEL-004-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-MODEL-004-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：冻结切分Brier/log loss/ECE/可靠性/不确定性及规则回退达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-MODEL-004-01`～`AC-MODEL-004-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## MODEL-005 训练模型产物版本、冻结和评估生命周期

| 字段 | 内容 |
|---|---|
| 类型 | 可训练模型 |
| 代码入口候选 | `players/humanlike/models/model_005.py`；存在不代表通过 |
| 上游依赖 | `MODEL-004|TRAIN-008|AUDIT-011` |
| 参数绑定 | `无直接登记` |
| 来源规则 | 实现规范 §11.1、§18.3 |
| 父测试合同 | T-MODEL-005-N01、T-MODEL-005-B01、T-MODEL-005-I01、T-MODEL-005-P01、T-MODEL-005-R01、T-MODEL-005-X01 |
| 细化测试卡 | `TC-MODEL-005-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_model_005.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-MODEL-005-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-MODEL-005-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：冻结切分Brier/log loss/ECE/可靠性/不确定性及规则回退达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-MODEL-005-01`～`AC-MODEL-005-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## STATE-001 Match 配置冻结、玩家装配与整场控制

| 字段 | 内容 |
|---|---|
| 类型 | 状态管理 |
| 代码入口候选 | `engine/state/state_001.py`；存在不代表通过 |
| 上游依赖 | `ALGO-009|ALGO-011|STATE-010` |
| 参数绑定 | `RP-001～RP-033、GP-001～GP-027` |
| 来源规则 | AU-003 人类化决策规则：第 0—6 章 / 1. 游戏开始；AU-055 程序实现规范：第 0—10 章 / 3.1 Match Controller |
| 父测试合同 | T-STATE-001-N01、T-STATE-001-B01、T-STATE-001-I01、T-STATE-001-P01、T-STATE-001-R01、T-STATE-001-X01 |
| 细化测试卡 | `TC-STATE-001-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_state_001.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-STATE-001-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-STATE-001-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-STATE-001-01`～`AC-STATE-001-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## STATE-002 权威 RoundState 存储与授权访问

| 字段 | 内容 |
|---|---|
| 类型 | 状态管理 |
| 代码入口候选 | `engine/state/state_002.py`；存在不代表通过 |
| 上游依赖 | `STATE-004|STATE-011` |
| 参数绑定 | `RP-001～RP-023、RP-001～RP-033` |
| 来源规则 | AU-057 程序实现规范：第 0—10 章 / 3.3 State Store；AU-070 程序实现规范：第 0—10 章 / 6. Round/Player/View 状态 |
| 父测试合同 | T-STATE-002-N01、T-STATE-002-B01、T-STATE-002-I01、T-STATE-002-P01、T-STATE-002-R01、T-STATE-002-X01 |
| 细化测试卡 | `TC-STATE-002-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_state_002.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-STATE-002-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-STATE-002-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-STATE-002-01`～`AC-STATE-002-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## STATE-003 PlayerRoundState 手牌、副露、定缺与过胡状态

| 字段 | 内容 |
|---|---|
| 类型 | 状态管理 |
| 代码入口候选 | `engine/state/state_003.py`；存在不代表通过 |
| 上游依赖 | `STATE-002|ALGO-001` |
| 参数绑定 | `GP-011～GP-020、RP-001～RP-033` |
| 来源规则 | AU-066 程序实现规范：第 0—10 章 / 4.3 手牌与组合；AU-070 程序实现规范：第 0—10 章 / 6. Round/Player/View 状态 |
| 父测试合同 | T-STATE-003-N01、T-STATE-003-B01、T-STATE-003-I01、T-STATE-003-P01、T-STATE-003-R01、T-STATE-003-X01 |
| 细化测试卡 | `TC-STATE-003-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_state_003.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-STATE-003-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-STATE-003-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-STATE-003-01`～`AC-STATE-003-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## STATE-004 CONFIGURED→SETTLED 状态机

| 字段 | 内容 |
|---|---|
| 类型 | 状态管理 |
| 代码入口候选 | `engine/state/state_004.py`；存在不代表通过 |
| 上游依赖 | `STATE-001` |
| 参数绑定 | `GP-001～GP-027, RP-001～RP-033、RP-030～RP-032` |
| 来源规则 | AU-043 人类化决策规则：第 15—18 章与参数 / 15. 总体流程；AU-071 程序实现规范：第 0—10 章 / 7. 状态机/事件 |
| 父测试合同 | T-STATE-004-N01、T-STATE-004-B01、T-STATE-004-I01、T-STATE-004-P01、T-STATE-004-R01、T-STATE-004-X01 |
| 细化测试卡 | `TC-STATE-004-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_state_004.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-STATE-004-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-STATE-004-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-STATE-004-01`～`AC-STATE-004-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## STATE-005 不可变 PlayerView 状态载体

| 字段 | 内容 |
|---|---|
| 类型 | 状态管理 |
| 代码入口候选 | `engine/state/state_005.py`；存在不代表通过 |
| 上游依赖 | `ALGO-010` |
| 参数绑定 | `GP-021、RP-001～RP-033` |
| 来源规则 | AU-002 人类化决策规则：第 0—6 章 / 0. 可见信息边界；AU-058 程序实现规范：第 0—10 章 / 3.4 Player View；AU-070 程序实现规范：第 0—10 章 / 6. Round/Player/View 状态 |
| 父测试合同 | T-STATE-005-N01、T-STATE-005-B01、T-STATE-005-I01、T-STATE-005-P01、T-STATE-005-R01、T-STATE-005-X01 |
| 细化测试卡 | `TC-STATE-005-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_state_005.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-STATE-005-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-STATE-005-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-STATE-005-01`～`AC-STATE-005-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## STATE-006 策略侧认知运行态初始化与归档

| 字段 | 内容 |
|---|---|
| 类型 | 状态管理 |
| 代码入口候选 | `engine/state/state_006.py`；存在不代表通过 |
| 上游依赖 | `STATE-001|STATE-005|STATE-010` |
| 参数绑定 | `RP-001～RP-033` |
| 来源规则 | AU-003 人类化决策规则：第 0—6 章 / 1. 游戏开始；AU-070 程序实现规范：第 0—10 章 / 6. Round/Player/View 状态 |
| 父测试合同 | T-STATE-006-N01、T-STATE-006-B01、T-STATE-006-I01、T-STATE-006-P01、T-STATE-006-R01、T-STATE-006-X01 |
| 细化测试卡 | `TC-STATE-006-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_state_006.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-STATE-006-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-STATE-006-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-STATE-006-01`～`AC-STATE-006-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## STATE-007 存档 schema 持久化与迁移

| 字段 | 内容 |
|---|---|
| 类型 | 状态管理 |
| 代码入口候选 | `engine/state/state_007.py`；存在不代表通过 |
| 上游依赖 | `STATE-002|ALGO-009` |
| 参数绑定 | `GP-001` |
| 来源规则 | AU-095 程序实现规范：第 11—19 章 / 18. 版本/兼容 |
| 父测试合同 | T-STATE-007-N01、T-STATE-007-B01、T-STATE-007-I01、T-STATE-007-P01、T-STATE-007-R01、T-STATE-007-X01 |
| 细化测试卡 | `TC-STATE-007-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_state_007.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-STATE-007-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-STATE-007-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-STATE-007-01`～`AC-STATE-007-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## STATE-008 跨局比分、认知和 episode 状态继承

| 字段 | 内容 |
|---|---|
| 类型 | 状态管理 |
| 代码入口候选 | `engine/state/state_008.py`；存在不代表通过 |
| 上游依赖 | `STATE-001|SCORE-006|STATE-006` |
| 参数绑定 | `GP-001～GP-027、RP-024～RP-032` |
| 来源规则 | AU-055 程序实现规范：第 0—10 章 / 3.1 Match Controller；AU-081 程序实现规范：第 11—19 章 / 11.5 Episode |
| 父测试合同 | T-STATE-008-N01、T-STATE-008-B01、T-STATE-008-I01、T-STATE-008-P01、T-STATE-008-R01、T-STATE-008-X01 |
| 细化测试卡 | `TC-STATE-008-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_state_008.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-STATE-008-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-STATE-008-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-STATE-008-01`～`AC-STATE-008-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## STATE-009 决策请求上下文与生命周期

| 字段 | 内容 |
|---|---|
| 类型 | 状态管理 |
| 代码入口候选 | `engine/state/state_009.py`；存在不代表通过 |
| 上游依赖 | `STATE-004|STATE-005|RULE-001` |
| 参数绑定 | `GP-023～GP-027, RP-019～RP-029` |
| 来源规则 | AU-073 程序实现规范：第 0—10 章 / 9. AI 决策管线 |
| 父测试合同 | T-STATE-009-N01、T-STATE-009-B01、T-STATE-009-I01、T-STATE-009-P01、T-STATE-009-R01、T-STATE-009-X01 |
| 细化测试卡 | `TC-STATE-009-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_state_009.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-STATE-009-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-STATE-009-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-STATE-009-01`～`AC-STATE-009-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## STATE-010 GP/RP/Profile 注册与生命周期

| 字段 | 内容 |
|---|---|
| 类型 | 状态管理 |
| 代码入口候选 | `engine/state/state_010.py`；存在不代表通过 |
| 上游依赖 | `无` |
| 参数绑定 | `GP-001～GP-027、RP-001～RP-033` |
| 来源规则 | AU-004 人类化决策规则：第 0—6 章 / 2. 学习规则；AU-045 人类化决策规则：第 15—18 章与参数 / 17. GP 注册；AU-046 人类化决策规则：第 15—18 章与参数 / 17. RP 注册；AU-069 程序实现规范：第 0—10 章 / 5. 配置模型；AU-070 程序实现规范：第 0—10 章 / 6. Round/Player/View 状态 |
| 父测试合同 | T-STATE-010-N01、T-STATE-010-B01、T-STATE-010-I01、T-STATE-010-P01、T-STATE-010-R01、T-STATE-010-X01 |
| 细化测试卡 | `TC-STATE-010-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_state_010.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-STATE-010-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-STATE-010-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-STATE-010-01`～`AC-STATE-010-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## STATE-011 牌墙构建、洗牌与初始发牌

| 字段 | 内容 |
|---|---|
| 类型 | 状态管理 |
| 代码入口候选 | `engine/state/state_011.py`；存在不代表通过 |
| 上游依赖 | `ALGO-011` |
| 参数绑定 | `无直接登记` |
| 来源规则 | 实现规范 §4.1、§7.2；规则文档 §1/§4 |
| 父测试合同 | T-STATE-011-N01、T-STATE-011-B01、T-STATE-011-I01、T-STATE-011-P01、T-STATE-011-R01、T-STATE-011-X01 |
| 细化测试卡 | `TC-STATE-011-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_state_011.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-STATE-011-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-STATE-011-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-STATE-011-01`～`AC-STATE-011-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## STATE-012 策略超时、崩溃与合法默认动作回退

| 字段 | 内容 |
|---|---|
| 类型 | 状态管理 |
| 代码入口候选 | `engine/state/state_012.py`；存在不代表通过 |
| 上游依赖 | `STATE-009|ALGO-006` |
| 参数绑定 | `GP-024～GP-026, RP-024～RP-029` |
| 来源规则 | 规则文档 §14.11；实现规范 §9.3 |
| 父测试合同 | T-STATE-012-N01、T-STATE-012-B01、T-STATE-012-I01、T-STATE-012-P01、T-STATE-012-R01、T-STATE-012-X01 |
| 细化测试卡 | `TC-STATE-012-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_state_012.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-STATE-012-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-STATE-012-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-STATE-012-01`～`AC-STATE-012-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## SCORE-001 分数账本分层与守恒

| 字段 | 内容 |
|---|---|
| 类型 | 计分 |
| 代码入口候选 | `engine/scoring/score_001.py`；存在不代表通过 |
| 上游依赖 | `STATE-002` |
| 参数绑定 | `GP-011～GP-020, RP-022～RP-023、无直接GP/RP；测试追踪` |
| 来源规则 | AU-068 程序实现规范：第 0—10 章 / 4.5 计分对象；AU-087 程序实现规范：第 11—19 章 / 14.1 每事件断言 |
| 父测试合同 | T-SCORE-001-N01、T-SCORE-001-B01、T-SCORE-001-I01、T-SCORE-001-P01、T-SCORE-001-R01、T-SCORE-001-X01 |
| 细化测试卡 | `TC-SCORE-001-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_score_001.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-SCORE-001-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-SCORE-001-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件/层/本局确定复现且ΣΔ=0；账本幂等 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-SCORE-001-01`～`AC-SCORE-001-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## SCORE-002 自摸、点炮与抢杠胡计分

| 字段 | 内容 |
|---|---|
| 类型 | 计分 |
| 代码入口候选 | `engine/scoring/score_002.py`；存在不代表通过 |
| 上游依赖 | `RULE-010|RULE-015|SCORE-001` |
| 参数绑定 | `GP-023～GP-026, RP-024～RP-033、GP-001～GP-027` |
| 来源规则 | AU-040 人类化决策规则：第 7—14 章 / 12. 终局计分；AU-061 程序实现规范：第 0—10 章 / 3.7 Scoring |
| 父测试合同 | T-SCORE-002-N01、T-SCORE-002-B01、T-SCORE-002-I01、T-SCORE-002-P01、T-SCORE-002-R01、T-SCORE-002-X01 |
| 细化测试卡 | `TC-SCORE-002-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_score_002.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-SCORE-002-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-SCORE-002-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件/层/本局确定复现且ΣΔ=0；账本幂等 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-SCORE-002-01`～`AC-SCORE-002-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## SCORE-003 明/暗/补杠与呼叫转移计分

| 字段 | 内容 |
|---|---|
| 类型 | 计分 |
| 代码入口候选 | `engine/scoring/score_003.py`；存在不代表通过 |
| 上游依赖 | `RULE-008|RULE-009|SCORE-001` |
| 参数绑定 | `GP-014～GP-020、GP-023～GP-026, RP-024～RP-033、GP-001～GP-027` |
| 来源规则 | AU-033 人类化决策规则：第 7—14 章 / 9.3 杠牌响应；AU-040 人类化决策规则：第 7—14 章 / 12. 终局计分；AU-061 程序实现规范：第 0—10 章 / 3.7 Scoring |
| 父测试合同 | T-SCORE-003-N01、T-SCORE-003-B01、T-SCORE-003-I01、T-SCORE-003-P01、T-SCORE-003-R01、T-SCORE-003-X01 |
| 细化测试卡 | `TC-SCORE-003-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_score_003.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-SCORE-003-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-SCORE-003-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件/层/本局确定复现且ΣΔ=0；账本幂等 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-SCORE-003-01`～`AC-SCORE-003-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## SCORE-004 花猪、查大叫与退税终局调整

| 字段 | 内容 |
|---|---|
| 类型 | 计分 |
| 代码入口候选 | `engine/scoring/score_004.py`；存在不代表通过 |
| 上游依赖 | `RULE-004|RULE-015|SCORE-001` |
| 参数绑定 | `GP-023～GP-026, RP-024～RP-033、GP-001～GP-027` |
| 来源规则 | AU-040 人类化决策规则：第 7—14 章 / 12. 终局计分；AU-061 程序实现规范：第 0—10 章 / 3.7 Scoring |
| 父测试合同 | T-SCORE-004-N01、T-SCORE-004-B01、T-SCORE-004-I01、T-SCORE-004-P01、T-SCORE-004-R01、T-SCORE-004-X01 |
| 细化测试卡 | `TC-SCORE-004-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_score_004.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-SCORE-004-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-SCORE-004-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件/层/本局确定复现且ΣΔ=0；账本幂等 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-SCORE-004-01`～`AC-SCORE-004-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## SCORE-005 封顶、互斥和转移结算顺序

| 字段 | 内容 |
|---|---|
| 类型 | 计分 |
| 代码入口候选 | `engine/scoring/score_005.py`；存在不代表通过 |
| 上游依赖 | `RULE-015|SCORE-002|SCORE-003|SCORE-004` |
| 参数绑定 | `GP-023～GP-026, RP-024～RP-033、GP-001～GP-027` |
| 来源规则 | AU-040 人类化决策规则：第 7—14 章 / 12. 终局计分；AU-061 程序实现规范：第 0—10 章 / 3.7 Scoring |
| 父测试合同 | T-SCORE-005-N01、T-SCORE-005-B01、T-SCORE-005-I01、T-SCORE-005-P01、T-SCORE-005-R01、T-SCORE-005-X01 |
| 细化测试卡 | `TC-SCORE-005-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_score_005.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-SCORE-005-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-SCORE-005-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件/层/本局确定复现且ΣΔ=0；账本幂等 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-SCORE-005-01`～`AC-SCORE-005-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## SCORE-006 单局总分、整场累计与排名

| 字段 | 内容 |
|---|---|
| 类型 | 计分 |
| 代码入口候选 | `engine/scoring/score_006.py`；存在不代表通过 |
| 上游依赖 | `SCORE-001|SCORE-005|STATE-001` |
| 参数绑定 | `GP-011～GP-020、GP-023～GP-026, RP-024～RP-033、GP-001～GP-027` |
| 来源规则 | AU-039 人类化决策规则：第 7—14 章 / 11. 胡后处理；AU-040 人类化决策规则：第 7—14 章 / 12. 终局计分；AU-055 程序实现规范：第 0—10 章 / 3.1 Match Controller |
| 父测试合同 | T-SCORE-006-N01、T-SCORE-006-B01、T-SCORE-006-I01、T-SCORE-006-P01、T-SCORE-006-R01、T-SCORE-006-X01 |
| 细化测试卡 | `TC-SCORE-006-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_score_006.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-SCORE-006-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-SCORE-006-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：逐事件/层/本局确定复现且ΣΔ=0；账本幂等 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-SCORE-006-01`～`AC-SCORE-006-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## TRAIN-001 复用生产规则的训练包装

| 字段 | 内容 |
|---|---|
| 类型 | 训练接口 |
| 代码入口候选 | `training/train_001.py`；存在不代表通过 |
| 上游依赖 | `STATE-001|STATE-004|RULE-001` |
| 参数绑定 | `GP-003、GP-008～GP-010` |
| 来源规则 | AU-063 程序实现规范：第 0—10 章 / 3.9 Training wrapper；AU-077 程序实现规范：第 11—19 章 / 11.1 训练模式 |
| 父测试合同 | T-TRAIN-001-N01、T-TRAIN-001-B01、T-TRAIN-001-I01、T-TRAIN-001-P01、T-TRAIN-001-R01、T-TRAIN-001-X01 |
| 细化测试卡 | `TC-TRAIN-001-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_train_001.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-TRAIN-001-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-001-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：生产等价、reward溯源、回放/快照/并行指标达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-TRAIN-001-01`～`AC-TRAIN-001-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## TRAIN-002 Observation v2 编码

| 字段 | 内容 |
|---|---|
| 类型 | 训练接口 |
| 代码入口候选 | `training/train_002.py`；存在不代表通过 |
| 上游依赖 | `STATE-005|ALGO-010` |
| 参数绑定 | `GP-011～GP-020` |
| 来源规则 | AU-078 程序实现规范：第 11—19 章 / 11.2 观测空间 |
| 父测试合同 | T-TRAIN-002-N01、T-TRAIN-002-B01、T-TRAIN-002-I01、T-TRAIN-002-P01、T-TRAIN-002-R01、T-TRAIN-002-X01 |
| 细化测试卡 | `TC-TRAIN-002-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_train_002.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-TRAIN-002-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-002-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：生产等价、reward溯源、回放/快照/并行指标达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-TRAIN-002-01`～`AC-TRAIN-002-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## TRAIN-003 固定动作 codec 与 legal mask

| 字段 | 内容 |
|---|---|
| 类型 | 训练接口 |
| 代码入口候选 | `training/train_003.py`；存在不代表通过 |
| 上游依赖 | `RULE-001|STATE-009` |
| 参数绑定 | `RP-022, RP-033` |
| 来源规则 | AU-079 程序实现规范：第 11—19 章 / 11.3 动作空间 |
| 父测试合同 | T-TRAIN-003-N01、T-TRAIN-003-B01、T-TRAIN-003-I01、T-TRAIN-003-P01、T-TRAIN-003-R01、T-TRAIN-003-X01 |
| 细化测试卡 | `TC-TRAIN-003-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_train_003.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-TRAIN-003-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-003-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：生产等价、reward溯源、回放/快照/并行指标达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-TRAIN-003-01`～`AC-TRAIN-003-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## TRAIN-004 非法训练动作处理契约

| 字段 | 内容 |
|---|---|
| 类型 | 训练接口 |
| 代码入口候选 | `training/train_004.py`；存在不代表通过 |
| 上游依赖 | `TRAIN-003` |
| 参数绑定 | `RP-022, RP-033` |
| 来源规则 | AU-079 程序实现规范：第 11—19 章 / 11.3 动作空间 |
| 父测试合同 | T-TRAIN-004-N01、T-TRAIN-004-B01、T-TRAIN-004-I01、T-TRAIN-004-P01、T-TRAIN-004-R01、T-TRAIN-004-X01 |
| 细化测试卡 | `TC-TRAIN-004-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_train_004.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-TRAIN-004-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-004-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：生产等价、reward溯源、回放/快照/并行指标达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-TRAIN-004-01`～`AC-TRAIN-004-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## TRAIN-005 真实得分与可见势能奖励契约

| 字段 | 内容 |
|---|---|
| 类型 | 训练接口 |
| 代码入口候选 | `training/train_005.py`；存在不代表通过 |
| 上游依赖 | `SCORE-001|TRAIN-002` |
| 参数绑定 | `RP-030～RP-032` |
| 来源规则 | AU-080 程序实现规范：第 11—19 章 / 11.4 奖励 |
| 父测试合同 | T-TRAIN-005-N01、T-TRAIN-005-B01、T-TRAIN-005-I01、T-TRAIN-005-P01、T-TRAIN-005-R01、T-TRAIN-005-X01 |
| 细化测试卡 | `TC-TRAIN-005-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_train_005.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-TRAIN-005-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-005-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：生产等价、reward溯源、回放/快照/并行指标达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-TRAIN-005-01`～`AC-TRAIN-005-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## TRAIN-006 单 learner reset/step/mask/clone/restore

| 字段 | 内容 |
|---|---|
| 类型 | 训练接口 |
| 代码入口候选 | `training/train_006.py`；存在不代表通过 |
| 上游依赖 | `TRAIN-001|TRAIN-002|TRAIN-003|TRAIN-005` |
| 参数绑定 | `RP-024～RP-032、RP-030～RP-032` |
| 来源规则 | AU-081 程序实现规范：第 11—19 章 / 11.5 Episode；AU-086 程序实现规范：第 11—19 章 / 13.5 训练接口 |
| 父测试合同 | T-TRAIN-006-N01、T-TRAIN-006-B01、T-TRAIN-006-I01、T-TRAIN-006-P01、T-TRAIN-006-R01、T-TRAIN-006-X01 |
| 细化测试卡 | `TC-TRAIN-006-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_train_006.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-TRAIN-006-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-006-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：生产等价、reward溯源、回放/快照/并行指标达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-TRAIN-006-01`～`AC-TRAIN-006-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## TRAIN-007 多玩家 ActionMap 与自博弈调度

| 字段 | 内容 |
|---|---|
| 类型 | 训练接口 |
| 代码入口候选 | `training/train_007.py`；存在不代表通过 |
| 上游依赖 | `TRAIN-006|RULE-013` |
| 参数绑定 | `GP-003、GP-008～GP-010、RP-030～RP-032` |
| 来源规则 | AU-063 程序实现规范：第 0—10 章 / 3.9 Training wrapper；AU-077 程序实现规范：第 11—19 章 / 11.1 训练模式；AU-086 程序实现规范：第 11—19 章 / 13.5 训练接口 |
| 父测试合同 | T-TRAIN-007-N01、T-TRAIN-007-B01、T-TRAIN-007-I01、T-TRAIN-007-P01、T-TRAIN-007-R01、T-TRAIN-007-X01 |
| 细化测试卡 | `TC-TRAIN-007-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_train_007.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-TRAIN-007-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-007-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：生产等价、reward溯源、回放/快照/并行指标达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-TRAIN-007-01`～`AC-TRAIN-007-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## TRAIN-008 离线 BC 与回放 RL 数据消费

| 字段 | 内容 |
|---|---|
| 类型 | 训练接口 |
| 代码入口候选 | `training/train_008.py`；存在不代表通过 |
| 上游依赖 | `TRAIN-002|TRAIN-003|AUDIT-014` |
| 参数绑定 | `GP-008～GP-010` |
| 来源规则 | AU-077 程序实现规范：第 11—19 章 / 11.1 训练模式 |
| 父测试合同 | T-TRAIN-008-N01、T-TRAIN-008-B01、T-TRAIN-008-I01、T-TRAIN-008-P01、T-TRAIN-008-R01、T-TRAIN-008-X01 |
| 细化测试卡 | `TC-TRAIN-008-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_train_008.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-TRAIN-008-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-008-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：生产等价、reward溯源、回放/快照/并行指标达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-TRAIN-008-01`～`AC-TRAIN-008-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## TRAIN-009 房规、profile 与行为域随机化

| 字段 | 内容 |
|---|---|
| 类型 | 训练接口 |
| 代码入口候选 | `training/train_009.py`；存在不代表通过 |
| 上游依赖 | `STATE-010|ALGO-011` |
| 参数绑定 | `GP-008～GP-010` |
| 来源规则 | AU-077 程序实现规范：第 11—19 章 / 11.1 训练模式 |
| 父测试合同 | T-TRAIN-009-N01、T-TRAIN-009-B01、T-TRAIN-009-I01、T-TRAIN-009-P01、T-TRAIN-009-R01、T-TRAIN-009-X01 |
| 细化测试卡 | `TC-TRAIN-009-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_train_009.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-TRAIN-009-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-TRAIN-009-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：生产等价、reward溯源、回放/快照/并行指标达标 | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-TRAIN-009-01`～`AC-TRAIN-009-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-001 全原子规则事件日志

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_001.py`；存在不代表通过 |
| 上游依赖 | `STATE-004|STATE-002` |
| 参数绑定 | `GP-021, RP-031、GP-004、RP-030～RP-032、RP-024～RP-032` |
| 来源规则 | AU-029 人类化决策规则：第 7—14 章 / 8.8 信息边界；AU-062 程序实现规范：第 0—10 章 / 3.8 Replay/Audit；AU-071 程序实现规范：第 0—10 章 / 7. 状态机/事件；AU-082 程序实现规范：第 11—19 章 / 12.1 事件日志 |
| 父测试合同 | T-AUDIT-001-N01、T-AUDIT-001-B01、T-AUDIT-001-I01、T-AUDIT-001-P01、T-AUDIT-001-R01、T-AUDIT-001-X01 |
| 细化测试卡 | `TC-AUDIT-001-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_001.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-001-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-001-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-001-01`～`AC-AUDIT-001-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-002 AI 决策解释日志

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_002.py`；存在不代表通过 |
| 上游依赖 | `STATE-009|STATE-006|ALGO-007` |
| 参数绑定 | `GP-021, RP-031、GP-024～GP-026, RP-024～RP-029、GP-023～GP-027, RP-024～RP-033、GP-004、RP-024～RP-032` |
| 来源规则 | AU-029 人类化决策规则：第 7—14 章 / 8.8 信息边界；AU-038 人类化决策规则：第 7—14 章 / 10.7–10.13 人类表现；AU-041 人类化决策规则：第 7—14 章 / 13. 玩家模型；AU-062 程序实现规范：第 0—10 章 / 3.8 Replay/Audit；AU-083 程序实现规范：第 11—19 章 / 12.2 AI 决策日志 |
| 父测试合同 | T-AUDIT-002-N01、T-AUDIT-002-B01、T-AUDIT-002-I01、T-AUDIT-002-P01、T-AUDIT-002-R01、T-AUDIT-002-X01 |
| 细化测试卡 | `TC-AUDIT-002-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_002.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-002-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-002-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-002-01`～`AC-AUDIT-002-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-003 canonical hash 链与篡改检测

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_003.py`；存在不代表通过 |
| 上游依赖 | `AUDIT-001|AUDIT-002` |
| 参数绑定 | `GP-004、RP-024～RP-032` |
| 来源规则 | AU-062 程序实现规范：第 0—10 章 / 3.8 Replay/Audit；AU-082 程序实现规范：第 11—19 章 / 12.1 事件日志；AU-083 程序实现规范：第 11—19 章 / 12.2 AI 决策日志 |
| 父测试合同 | T-AUDIT-003-N01、T-AUDIT-003-B01、T-AUDIT-003-I01、T-AUDIT-003-P01、T-AUDIT-003-R01、T-AUDIT-003-X01 |
| 细化测试卡 | `TC-AUDIT-003-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_003.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-003-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-003-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-003-01`～`AC-AUDIT-003-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-004 同配置/seed/事件的确定性回放

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_004.py`；存在不代表通过 |
| 上游依赖 | `AUDIT-003|ALGO-008|STATE-007` |
| 参数绑定 | `GP-004、GP-001～GP-027` |
| 来源规则 | AU-062 程序实现规范：第 0—10 章 / 3.8 Replay/Audit；AU-084 程序实现规范：第 11—19 章 / 12.3 确定性回放 |
| 父测试合同 | T-AUDIT-004-N01、T-AUDIT-004-B01、T-AUDIT-004-I01、T-AUDIT-004-P01、T-AUDIT-004-R01、T-AUDIT-004-X01 |
| 细化测试卡 | `TC-AUDIT-004-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_004.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-004-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-004-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-004-01`～`AC-AUDIT-004-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-005 每事件强制不变量执行

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_005.py`；存在不代表通过 |
| 上游依赖 | `STATE-004|ALGO-001|RULE-001|SCORE-001` |
| 参数绑定 | `GP-001～GP-027, RP-001～RP-033、RP-030～RP-032、无直接GP/RP；测试追踪` |
| 来源规则 | AU-053 程序实现规范：第 0—10 章 / 2. IR-001～018；AU-071 程序实现规范：第 0—10 章 / 7. 状态机/事件；AU-087 程序实现规范：第 11—19 章 / 14.1 每事件断言 |
| 父测试合同 | T-AUDIT-005-N01、T-AUDIT-005-B01、T-AUDIT-005-I01、T-AUDIT-005-P01、T-AUDIT-005-R01、T-AUDIT-005-X01 |
| 细化测试卡 | `TC-AUDIT-005-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_005.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-005-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-005-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-005-01`～`AC-AUDIT-005-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-006 直接规则与接口测试证据门禁

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_006.py`；存在不代表通过 |
| 上游依赖 | `AUDIT-005` |
| 参数绑定 | `无直接GP/RP；测试生成` |
| 来源规则 | AU-088 程序实现规范：第 11—19 章 / 14.2 单元测试清单 |
| 父测试合同 | T-AUDIT-006-N01、T-AUDIT-006-B01、T-AUDIT-006-I01、T-AUDIT-006-P01、T-AUDIT-006-R01、T-AUDIT-006-X01 |
| 细化测试卡 | `TC-AUDIT-006-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_006.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-006-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-006-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-006-01`～`AC-AUDIT-006-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-007 属性式生成、缩减与不变量证据

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_007.py`；存在不代表通过 |
| 上游依赖 | `AUDIT-005|ALGO-011` |
| 参数绑定 | `无直接GP/RP；测试生成` |
| 来源规则 | AU-089 程序实现规范：第 11—19 章 / 14.3 属性测试 |
| 父测试合同 | T-AUDIT-007-N01、T-AUDIT-007-B01、T-AUDIT-007-I01、T-AUDIT-007-P01、T-AUDIT-007-R01、T-AUDIT-007-X01 |
| 细化测试卡 | `TC-AUDIT-007-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_007.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-007-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-007-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-007-01`～`AC-AUDIT-007-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-008 锁定来源逐章 golden-case 对照

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_008.py`；存在不代表通过 |
| 上游依赖 | `AUDIT-006|AUDIT-010` |
| 参数绑定 | `GP-001～GP-027, RP-001～RP-033` |
| 来源规则 | AU-043 人类化决策规则：第 15—18 章与参数 / 15. 总体流程；AU-090 程序实现规范：第 11—19 章 / 14.4 章节对照测试 |
| 父测试合同 | T-AUDIT-008-N01、T-AUDIT-008-B01、T-AUDIT-008-I01、T-AUDIT-008-P01、T-AUDIT-008-R01、T-AUDIT-008-X01 |
| 细化测试卡 | `TC-AUDIT-008-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_008.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-008-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-008-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-008-01`～`AC-AUDIT-008-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-009 工程与行为回归指标

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_009.py`；存在不代表通过 |
| 上游依赖 | `AUDIT-004|TRAIN-006` |
| 参数绑定 | `RP-030～RP-033` |
| 来源规则 | AU-091 程序实现规范：第 11—19 章 / 14.5 回归指标 |
| 父测试合同 | T-AUDIT-009-N01、T-AUDIT-009-B01、T-AUDIT-009-I01、T-AUDIT-009-P01、T-AUDIT-009-R01、T-AUDIT-009-X01 |
| 细化测试卡 | `TC-AUDIT-009-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_009.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-009-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-009-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-009-01`～`AC-AUDIT-009-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-010 来源→参数→实现→测试全链追踪

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_010.py`；存在不代表通过 |
| 上游依赖 | `无` |
| 参数绑定 | `GP-001～GP-027, RP-001～RP-033` |
| 来源规则 | AU-092 程序实现规范：第 11—19 章 / 15. 源规则追踪 |
| 父测试合同 | T-AUDIT-010-N01、T-AUDIT-010-B01、T-AUDIT-010-I01、T-AUDIT-010-P01、T-AUDIT-010-R01、T-AUDIT-010-X01 |
| 细化测试卡 | `TC-AUDIT-010-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_010.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-010-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-010-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-010-01`～`AC-AUDIT-010-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-011 版本、迁移与发布物完整性

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_011.py`；存在不代表通过 |
| 上游依赖 | `ALGO-009|STATE-007|AUDIT-006|AUDIT-010` |
| 参数绑定 | `GP-001～GP-027、GP-001` |
| 来源规则 | AU-048 人类化决策规则：第 15—18 章与参数 / 18. 数值校验；AU-051 程序实现规范：第 0—10 章 / 0–1. 版本与源绑定；AU-095 程序实现规范：第 11—19 章 / 18. 版本/兼容 |
| 父测试合同 | T-AUDIT-011-N01、T-AUDIT-011-B01、T-AUDIT-011-I01、T-AUDIT-011-P01、T-AUDIT-011-R01、T-AUDIT-011-X01 |
| 细化测试卡 | `TC-AUDIT-011-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_011.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-011-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-011-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-011-01`～`AC-AUDIT-011-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-012 强度、真人相似和学习效果外部评价

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_012.py`；存在不代表通过 |
| 上游依赖 | `AUDIT-009|AUDIT-014|MODEL-005` |
| 参数绑定 | `RP-030～RP-033` |
| 来源规则 | AU-091 程序实现规范：第 11—19 章 / 14.5 回归指标 |
| 父测试合同 | T-AUDIT-012-N01、T-AUDIT-012-B01、T-AUDIT-012-I01、T-AUDIT-012-P01、T-AUDIT-012-R01、T-AUDIT-012-X01 |
| 细化测试卡 | `TC-AUDIT-012-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_012.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-012-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-012-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-012-01`～`AC-AUDIT-012-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-013 模块依赖、接口与信息流架构契约

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_013.py`；存在不代表通过 |
| 上游依赖 | `RULE-016|ALGO-010|TRAIN-001` |
| 参数绑定 | `GP-001～GP-027, RP-001～RP-033、GP-001～GP-027、无直接GP/RP；架构约束` |
| 来源规则 | AU-054 程序实现规范：第 0—10 章 / 3. 九模块架构；AU-085 程序实现规范：第 11—19 章 / 13.1–13.4 接口；AU-093 程序实现规范：第 11—19 章 / 16. 项目结构 |
| 父测试合同 | T-AUDIT-013-N01、T-AUDIT-013-B01、T-AUDIT-013-I01、T-AUDIT-013-P01、T-AUDIT-013-R01、T-AUDIT-013-X01 |
| 细化测试卡 | `TC-AUDIT-013-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_013.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-013-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-013-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-013-01`～`AC-AUDIT-013-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

## AUDIT-014 证据数据保留、脱敏与新鲜度管理

| 字段 | 内容 |
|---|---|
| 类型 | 日志审计 |
| 代码入口候选 | `engine/audit/audit_014.py`；存在不代表通过 |
| 上游依赖 | `AUDIT-001|AUDIT-002` |
| 参数绑定 | `RP-024～RP-032` |
| 来源规则 | AU-083 程序实现规范：第 11—19 章 / 12.2 AI 决策日志 |
| 父测试合同 | T-AUDIT-014-N01、T-AUDIT-014-B01、T-AUDIT-014-I01、T-AUDIT-014-P01、T-AUDIT-014-R01、T-AUDIT-014-X01 |
| 细化测试卡 | `TC-AUDIT-014-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）` |
| 自动化模块 | `tests/spec_v3/test_audit_014.py` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
| `AC-AUDIT-014-01` | 规格完整 | E1 | Not Evaluated | Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-02` | 非占位实现 | E2 | Not Evaluated | 真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-03` | 代码入口 | E2 | Not Evaluated | 建议主文件存在稳定可导入门面；版本/schema/error契约一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-04` | 实际调用方 | E4 | Not Evaluated | 非测试生产调用方静态边+完整运行trace均命中入口 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-05` | 参数绑定 | E4 | Not Evaluated | GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-06` | 状态写回 | E4 | Not Evaluated | 纯函数无副作用，或只经权威入口原子commit；失败hash不变 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-07` | 单元测试 | E3 | Not Evaluated | Approved N/UT及适用参数/属性测试current-run通过并直接断言行为 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-08` | 边界测试 | E3 | Not Evaluated | Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-09` | 集成测试 | E4 | Not Evaluated | Approved X/IT通过生产门面；上下游schema/version/hash兼容 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-10` | 运行日志 | E4 | Not Evaluated | 实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-11` | 追踪关系 | E4 | Not Evaluated | 来源→参数→单元→代码→测试→运行无断链 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-12` | 性能 | E4 | Not Evaluated | 冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-13` | 隐藏信息隔离 | E4 | Not Evaluated | 白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0 | TODO(evidence_id/path/hash) |
| `AC-AUDIT-014-14` | 确定性或统计指标 | E4 | Not Evaluated | 按单元方法类别执行确定、统计、校准或生产等价指标：canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI | TODO(evidence_id/path/hash) |

### 单元AUDITED判定

- [ ] `AC-AUDIT-014-01`～`AC-AUDIT-014-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。
