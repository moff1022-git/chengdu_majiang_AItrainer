# Spec v3 跨文档矛盾检查报告

| 字段 | 内容 |
|---|---|
| 日期 | 2026-07-29 |
| 结论 | **Superseded：最终复审Critical 0 / High 0；规范已锁定为SPEC-V3-3.0.0** |
| 输入 | locked catalog、六份单元规格、两份锁定来源、迁移表、依赖图 |
| 检查性质 | 文档结构/语义边界检查；不构成实现验收 |

## 1. 检查结果摘要

> 本报告最初用于总规范集成时的局部检查。2026-07-29完成的[全量跨文档一致性审计](cross_document_consistency_report.md)扩大到开发、细化测试和验收层，以下历史Passed仅保留当时检查语境；当前锁定判断以[未解决问题清单](unresolved_issues.md)和[最终就绪报告](final_readiness_report.md)为准。

| 检查 | 结果 | 证据 |
|---|---|---|
| 锁定来源hash | Passed | 两份当前SHA-256与authoritative manifest一致 |
| 锁定目录ID | Passed | 96行、96唯一ID |
| 类别数量 | Passed | RULE16/ALGO11/HEUR23/MODEL5/STATE12/SCORE6/TRAIN9/AUDIT14 |
| 已有详细规格ID重复 | Passed | 96个详细ID，无跨文件重复 |
| 已有详细规格多余ID | Passed | 0 |
| 详细规格完整性 | Passed | 96/96；AUDIT-001～AUDIT-014已覆盖 |
| 旧AU迁移 | Passed | AU-001～AU-096全覆盖、无缺号 |
| 迁移目标端点 | Passed | 非空new_unit_ids均应指向锁定目录；既有目录审查已通过 |
| 依赖端点/DAG | Passed（沿用锁定目录QA） | dependency_graph登记96节点、221边、无环 |
| 方法类型边界 | Passed | 确定规则/算法、启发式、概率/可训练模型、训练接口分开 |
| 详细规格状态 | Passed for implementation start | 六份均Approved；实现验收仍Not Evaluated |
| 公式等级 | Passed with baseline gaps | 规范/基线/启发式/模型/评估分级 |
| truth隔离 | Passed as specification | MODEL/TRAIN明确policy与restricted truth隔离 |
| 训练生产复用 | Passed as specification | TRAIN规定同一生产规则引擎 |
| 计分守恒 | Passed as specification | SCORE逐事件/层/总账ΣΔ=0 |
| 测试规格结构 | Passed / Approved | 96/96单元、576个唯一N/B/I/P/R/X测试ID；测试实现Not Implemented |
| 测试用例细化 | Passed / Approved catalog | 96×11适用性已判断；890个唯一TC测试卡；ALGO/SCORE 51个golden注册 |
| 开发任务卡结构 | Passed / Approved guide | 96/96单元均有代码位置、依赖、步骤、测试ID和完成定义 |
| 审计验收结构 | Passed / Approved standard | E0—E5累计定义；96单元×AC-01～14共1344项；AUDITED八项硬条件 |
| 状态枚举一致性 | Passed / Closed | STATE-004唯一RoundPhase，事件与Match状态已分层（CDI-001） |
| 证据等级一致性 | Passed / Closed | 正式E0—E5；历史EV隔离并保守迁移（CDI-002） |
| 参数范围注册 | Passed / Closed | 60项名称/范围/source/consumer/test机器注册（CDI-004） |
| 性能阈值来源 | Passed / Closed | 开发指南无第二套数值，验收只读单元规格（CDI-006） |
| 全集治理状态 | Passed / Closed | 总规范、开发、细化测试和审计验收核心文档均Approved（CDI-003） |

## 2. 缺口与潜在冲突

### CF-001 AUDIT详细规格缺失 — High / Closed

原检查发现锁定目录含AUDIT-001～014，而详细规格只覆盖82/96。现已新增 `03-unit-specs/audit_specs.md`，定义日志schema、hash链、回放、测试证据、指标、来源追踪、发布、外部评价、架构和证据保留接口，详细覆盖达到96/96。

关闭证据：AUDIT-001～014标题、统一23栏、目录端点和矩阵路径机器检查通过；批准状态由CF-002记录。

### CF-002 全部详细规格仍为Draft — Gate / Closed

原检查时六份规格均为Draft/Not Evaluated。用户已于2026-07-29明确批准spec-v3全部单元规格，六份文档现均为Approved；实现验收继续保持Not Evaluated，不与文档批准混同。

关闭证据：六份规格文档头、96行追踪矩阵均记录Approved；若后续修改详细定义，必须只改对应单元规格、重新批准并刷新本报告。

### CF-003 规范公式与现有基线不同 — Expected delta / Tracked

已明确差异包括七对向听distinct项、可见事件级去重、命名随机流域隔离、六分量Q、查大叫最大番、呼叫转移和退税。它们是显式“目标—基线差距”，不是两份权威定义互相冲突。

处理：实现时以Approved后的规范公式为目标；需要兼容旧回放时保留baseline_version，不得混报。

### CF-004 上游旧实现规范与v3边界粒度不同 — Resolved by precedence

旧实现规范按复合模块描述，v3按96单元拆分。总规范不复制造成第二套定义；锁定目录决定边界，单元规格决定细节，上游只作来源。

### CF-005 全量一致性审计新增开放项 — High / Partially Closed

扩大审计范围后发现的三项High现均关闭：CDI-001/002由一致性修复关闭，CDI-003由用户明确批准核心文档关闭；当前状态以最终复审报告为准。

## 3. 机器化检查方法

- CSV解析并检查目录行数/唯一ID/类型计数。
- Markdown按二级标题提取稳定单元ID，检查重复、多余和缺失。
- 迁移CSV检查AU-001～096连续覆盖。
- SHA-256核对两份锁定来源。
- 关键词/章节检查规范与基线公式、隐藏信息、校准、奖励溯源和生产复用。
- `git diff --check`检查Markdown/CSV空白错误。
- 测试清单检查96行唯一单元、每单元六类唯一测试ID、规格链接和计划路径格式。
- 用例目录检查覆盖矩阵Y项与唯一TC测试卡双向一致、每卡12个必填字段、同seed/泄漏/校准覆盖和golden来源。
- 开发任务卡检查96个唯一标题、依赖端点、建议代码/测试路径和Approved测试ID映射。
- 验收清单检查96个唯一单元、1344个唯一AC ID、每单元14项、方法类型AC-14和E0—E5/AUDITED条件完整性。

## 4. 不构成通过的事项

- 文件存在、标题完整、类名、测试名和历史EV3/EV4不证明当前E3/E4行为证据。
- 本轮未执行pytest、回放、训练、校准、性能或真人评估。
- 未验证当前代码是否满足已批准规范公式。
- 测试规格已Approved；计划中的`tests/spec_v3/`和JSONL向量尚未实现，不能计为E3。
- AUDIT规格虽已Approved，但运行证据仍为Not Evaluated，不能据此宣称发布审计通过。

## 5. 关闭条件

1. Locked状态与文件hash清单已生成。
2. M0已登记CF-003及其他基线差距；后续建立代码、测试和运行证据。
3. 实现证据另按AUDITED门禁评价，不能由规范锁定继承。
