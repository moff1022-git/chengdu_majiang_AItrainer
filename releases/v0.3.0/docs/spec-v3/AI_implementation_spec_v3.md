# 成都麻将 AI 训练模拟器总实现规范 v3

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 版本 | 3.0.0 |
| 日期 | 2026-07-29 |
| 单元目录 | UNIT-CATALOG 1.0.0 Locked；96单元 |
| 详细规格覆盖 | 96/96；六份详细规格均为Locked；实现验收Not Evaluated |
| 测试规格覆盖 | 96/96；576个Locked父合同，细化为890个Locked测试卡；Not Implemented |
| 开发实施指南 | Locked；总体指南、96任务卡及现有代码迁移计划已建立 |
| 审计验收规范 | Locked；E0—E5、96×14验收清单、证据包与报告模板已建立 |
| 验收状态 | Not Evaluated |
| 跨文档锁定状态 | Locked；Open Critical 0 / High 0 |

## 1. 文档角色与唯一来源

本文只做架构汇总、导航、边界与追踪，不复制单元内部定义。发生差异时按以下优先级处理：

1. 两份锁定上游规则文档提供需求语义与来源，不回写。
2. [locked_unit_catalog.md](02-unit-catalog/locked_unit_catalog.md) 是单元ID、名称、类型、边界和依赖目录的唯一来源。
3. 下列单元规格是对应单元输入、输出、状态、公式、错误、测试与验收的唯一详细来源：
   - [RULE/STATE](03-unit-specs/deterministic_rule_state_specs.md)
   - [ALGO/SCORE](03-unit-specs/deterministic_algorithm_scoring_specs.md)
   - [HEUR](03-unit-specs/human_heuristic_specs.md)
   - [MODEL](03-unit-specs/probabilistic_model_specs.md)
   - [TRAIN](03-unit-specs/training_environment_specs.md)
   - [AUDIT](03-unit-specs/audit_specs.md)
4. 本文及追踪矩阵只引用、分组和描述跨单元关系；不得被实现者当作覆盖详细规格的第二定义。
5. 六份详细规格已由用户于2026-07-29明确批准；后续实现必须遵守其规范，验收状态仍需由代码、测试和运行证据单独证明。

锁定来源：

- `成都麻将AI人类化决策规则_v1.md`，SHA-256 `6cbb4d4465abfd947b6cf7f1783db99408089d4e1646849a3afe674114267992`。
- `成都麻将AI训练模拟器程序实现规范_v2.0.0.md`，SHA-256 `9bc4d4ea5278e09ae34a1efb5edfb3cbc295752ecf6b3ebe89b348210d670135`。

## 2. 功能目录概览

| 类别 | 数量 | 方法边界 | 详细规格 |
|---|---:|---|---|
| RULE | 16 | 成都麻将权威规则与合法状态效果 | RULE/STATE规格 |
| ALGO | 11 | 可精确复算的工程算法 | ALGO/SCORE规格 |
| HEUR | 23 | 无唯一正确答案的可调软策略 | HEUR规格 |
| MODEL | 5 | 校准概率与可训练策略/生命周期 | MODEL规格 |
| STATE | 12 | 权威/视图/认知/请求状态生命周期 | RULE/STATE规格 |
| SCORE | 6 | 零和转移、结算与累计排名 | ALGO/SCORE规格 |
| TRAIN | 9 | 复用生产引擎的训练接口 | TRAIN规格 |
| AUDIT | 14 | 日志、证据、回放、门禁 | AUDIT规格 |
| 合计 | 96 | 锁定DAG共221条直接边 | 96有详细规格 |

完整单元行、上下游和当前实现证据状态不在本文复制，直接使用锁定CSV及[dependency_graph.md](02-unit-catalog/dependency_graph.md)。

## 3. 模块架构与信息流

```text
配置/参数注册 ─→ Match/牌墙/权威状态 ─→ 确定规则与计分
                              │
                              ├─→ 白名单 PlayerView ─→ ALGO/HEUR/MODEL 决策
                              │                         └─→ 请求/合法动作
                              ├─→ TRAIN（复用同一生产引擎）
                              └─→ AUDIT（可持有隔离truth，不得回流策略）
```

模块目标归属以[规则→参数→单元→模块矩阵](07-traceability/rule_parameter_unit_matrix.csv)为准。GP/RP的名称、类型、范围、生命周期、可见性、consumer和边界测试索引见[60项参数注册矩阵](07-traceability/parameter_registry.csv)；该矩阵只索引锁定来源第17/18章及其hash，不构成第二套参数权威。矩阵中的module是目标责任域，不是现有实现已达成声明。

## 4. 确定性与概率性边界

| 层 | 允许行为 | 禁止替代 |
|---|---|---|
| RULE/STATE/SCORE | 同输入、状态、规则、版本、seed得到唯一状态/计分 | HEUR/MODEL不得改合法性、状态机、守恒或计分 |
| ALGO | 规范公式精确复算；命名RNG算法固定后可复现 | 训练模型不得替代向听、计数、mask、hash等 |
| HEUR | 合法近优域内允许多种人类化行为；参数/seed冻结后复现 | 不得宣称逐手唯一答案或读取隐藏信息 |
| MODEL-001～003 | 输出概率、校准误差和不确定性 | 隐藏truth不得进入线上输入；概率不得当规则事实 |
| MODEL-004/005 | 冻结推理、训练产物和生命周期 | 训练不确定性不得污染冻结环境转换 |
| TRAIN | 环境转换确定、训练过程可非确定 | 不得维护第二套规则引擎 |
| AUDIT | 可在隔离区读取truth做验证 | truth不得回流policy/reward potential |

## 5. 输入、输出与状态总边界

本文只声明跨层接口；逐字段schema由对应单元规格唯一规定。

| 边界 | 输入 | 输出 | 状态所有者 |
|---|---|---|---|
| 配置入口 | raw config、GP/RP/Profile、版本 | frozen config/hash、命名随机流 | STATE-010/ALGO-009/011 |
| 整场/单局 | match request、agents | immutable match context、RoundState | STATE-001/002/004/011 |
| 规则事件 | 权威state、actor、event | legal set、state transition/error | RULE-001～016 |
| 计分 | 胡杠/终局事实、番策略、账本 | ScoreTransfer、ledger、rank | SCORE-001～006 |
| 策略视图 | authoritative state、viewer、phase | immutable PlayerView | RULE-016/ALGO-010/STATE-005 |
| 决策 | PlayerView、legal set、profile/认知 | action distribution/rank/chosen legal action | ALGO/HEUR/MODEL/STATE-009 |
| 训练 | production engine、obs/mask/action | transition/reward/snapshot/data | TRAIN-001～009 |
| 审计 | state/decision/truth/evidence | logs/hash/replay/gates | AUDIT-001～014 |

权威状态、PlayerView、策略认知、模型标签truth与审计truth必须是不同所有权域；详细允许字段见RULE-016、STATE-002/005/006、MODEL和TRAIN规格。

## 6. 公式规范等级

| 等级 | 含义 | 可否直接实现/验收 |
|---|---|---|
| F0 上游语义 | 锁定文档中的自然语言规则 | 需映射到单元，不能单独作为代码公式 |
| F1 规范公式 | 已批准单元规格中的目标公式/状态转移 | Approved后是唯一实现与验收公式 |
| F2 基线公式 | 单元规格明确标注的历史/规则/回退基线 | 可兼容和对照，不证明F1已实现 |
| F3 可调启发式 | HEUR规格范围内的权重、阈值、修正 | 可校准；不得越过硬约束 |
| F4 可训练替换 | MODEL允许替换的软概率/评分 | 必须通过合法、可见、校准、回退门禁 |
| F5 评估公式 | AUDIT/评估器使用的指标与truth | 只产生证据，不进入策略输入或权威状态 |

当前六份详细规格均为Approved，其中F1已成为实现与验收的权威目标公式；现有代码是否符合仍为Not Evaluated。

## 7. 规则→参数→单元→模块追踪

完整96行矩阵见[rule_parameter_unit_matrix.csv](07-traceability/rule_parameter_unit_matrix.csv)。每行保留：

- 上游AU/章节引用；
- GP/RP引用或“无直接登记”；
- 稳定单元ID、类型、目标模块；
- 主要输入/输出、确定性/可训练/RNG与可见性；
- 详细规格路径及覆盖状态。

追踪关系不得反向推导：存在参数键、类名或模块路径不代表实现或验收通过。

对应的96单元可执行测试合同见[测试规格索引](05-test-spec/README.md)和[测试执行清单](05-test-spec/unit_test_manifest.csv)。每单元固定正常golden、边界、非法、性质/统计、重复性和生产入口集成六类测试；测试规格已由用户于2026-07-29明确批准，但计划测试文件和向量尚未实现，不构成E3证据。

11类方法适用性、逐用例字段和确定算法golden注册分别见[测试策略](05-test-spec/test_strategy.md)、[测试用例目录](05-test-spec/test_case_catalog.md)、[金标准向量](05-test-spec/golden_vectors.md)和[覆盖矩阵](05-test-spec/coverage_matrix.csv)。890个Approved TC测试卡是576个Approved父合同的细化，不重复计算业务覆盖率；批准测试定义不表示测试代码或向量已经实现。

## 8. 旧实现规范差异

| 差异 | v3处理 |
|---|---|
| 旧文档按大模块/章节组织，职责复合 | 锁定为96个可独立输入输出和验收的单元 |
| 规则、算法、启发式、概率模型混验 | 强制方法分类和证据隔离 |
| face牌与physical实体守恒未独立 | ALGO-001与STATE-011独立 |
| game_id随机流散落 | ALGO-011独立、命名域隔离 |
| PlayerView与权威state边界不足 | RULE-016/ALGO-010/STATE-005分离 |
| Q/向听/计分近似易冒充规范 | 规范公式与基线公式分级 |
| 查叫简化、呼叫转移/退税缺失 | 在SCORE规格中显式列为基线差距 |
| 人类化以单动作准确率判断 | HEUR改用允许行为范围、方向效应、regret和CI |
| 概率只看准确率 | MODEL强制Brier/log loss/ECE与可靠性 |
| 训练可能复制规则 | TRAIN强制复用生产Engine/Rule/State/Score |
| truth边界不完整 | policy、label、evaluator/audit truth分区 |
| 模型产物生命周期隐含 | MODEL-005独立 |
| 审计被视作一个Replay模块 | 拆为AUDIT-001～014，并由AUDIT规格统一定义 |

这张表只描述架构差异；具体公式/接口差异仍以各单元规格“基线与规范差异”章节为准。

## 9. AU-001～AU-096迁移记录

权威原因和ADD-001～004见[unit_migration_map.csv](02-unit-catalog/unit_migration_map.csv)。以下只保留旧ID、决策和新单元目标，不复制原因：

| 旧ID | 决策 | 新单元 |
|---|---|---|
| AU-001 | SPLIT | RULE-001|ALGO-006 |
| AU-002 | SPLIT | RULE-016|ALGO-010|STATE-005 |
| AU-003 | SPLIT | STATE-001|STATE-006|HEUR-020|MODEL-003 |
| AU-004 | SPLIT | STATE-010|ALGO-009|RULE-015|HEUR-003 |
| AU-005 | RENAME | HEUR-003 |
| AU-006 | SPLIT | RULE-005|RULE-014 |
| AU-007 | RENAME | MODEL-001 |
| AU-008 | SPLIT | ALGO-002|HEUR-004 |
| AU-009 | MERGE | HEUR-005 |
| AU-010 | SPLIT | RULE-002|ALGO-001 |
| AU-011 | RENAME | HEUR-001 |
| AU-012 | RENAME | HEUR-002 |
| AU-013 | SPLIT | RULE-003|RULE-004 |
| AU-014 | MERGE | HEUR-004|HEUR-005 |
| AU-015 | RENAME | HEUR-006 |
| AU-016 | MERGE | MODEL-001 |
| AU-017 | MERGE | HEUR-005|HEUR-007 |
| AU-018 | SPLIT | RULE-014|HEUR-009 |
| AU-019 | RENAME | HEUR-008 |
| AU-020 | SPLIT | HEUR-003|HEUR-022 |
| AU-021 | RENAME | HEUR-010 |
| AU-022 | SPLIT | RULE-015|HEUR-011 |
| AU-023 | SPLIT | ALGO-003|ALGO-004|ALGO-005 |
| AU-024 | RENAME | HEUR-009 |
| AU-025 | KEEP | HEUR-005 |
| AU-026 | SPLIT | HEUR-007|HEUR-019 |
| AU-027 | KEEP | HEUR-020 |
| AU-028 | SPLIT | HEUR-016|HEUR-018 |
| AU-029 | SPLIT | RULE-016|AUDIT-001|AUDIT-002 |
| AU-030 | RENAME | ALGO-005 |
| AU-031 | SPLIT | RULE-001|RULE-013 |
| AU-032 | SPLIT | RULE-010|RULE-011|RULE-012 |
| AU-033 | SPLIT | RULE-008|RULE-009|SCORE-003|HEUR-013 |
| AU-034 | SPLIT | RULE-007|HEUR-012 |
| AU-035 | SPLIT | RULE-006|ALGO-006|HEUR-005 |
| AU-036 | SPLIT | ALGO-002|HEUR-014 |
| AU-037 | SPLIT | MODEL-002|HEUR-015 |
| AU-038 | SPLIT | HEUR-017|HEUR-018|HEUR-023|AUDIT-002 |
| AU-039 | SPLIT | RULE-014|HEUR-020|SCORE-006 |
| AU-040 | SPLIT | SCORE-002|SCORE-003|SCORE-004|SCORE-005|SCORE-006 |
| AU-041 | SPLIT | HEUR-022|HEUR-020|MODEL-003|AUDIT-002 |
| AU-042 | SPLIT | HEUR-019|HEUR-021|HEUR-023|ALGO-008|STATE-012 |
| AU-043 | MERGE | STATE-004|AUDIT-008 |
| AU-044 | REMOVE | — |
| AU-045 | MERGE | STATE-010|ALGO-009 |
| AU-046 | RENAME | STATE-010 |
| AU-047 | RENAME | MODEL-003 |
| AU-048 | SPLIT | ALGO-009|AUDIT-011 |
| AU-049 | RENAME | ALGO-007 |
| AU-050 | SPLIT | ALGO-003|ALGO-004|MODEL-001|MODEL-002 |
| AU-051 | SPLIT | ALGO-009|AUDIT-011 |
| AU-052 | RENAME | RULE-001 |
| AU-053 | SPLIT | ALGO-001|ALGO-003|ALGO-004|ALGO-005|ALGO-006|AUDIT-005 |
| AU-054 | RENAME | AUDIT-013 |
| AU-055 | SPLIT | STATE-001|STATE-008|SCORE-006 |
| AU-056 | SPLIT | RULE-002|RULE-003|RULE-004|RULE-005|RULE-006|RULE-007|RULE-008|RULE-009|RULE-010|RULE-011|RULE-012|RULE-013|RULE-014 |
| AU-057 | KEEP | STATE-002 |
| AU-058 | SPLIT | ALGO-010|STATE-005 |
| AU-059 | SPLIT | HEUR-004|HEUR-005|HEUR-019|HEUR-020|HEUR-021|HEUR-023|ALGO-006|ALGO-007|MODEL-001|MODEL-002 |
| AU-060 | RENAME | RULE-013 |
| AU-061 | SPLIT | SCORE-002|SCORE-003|SCORE-004|SCORE-005 |
| AU-062 | SPLIT | AUDIT-001|AUDIT-002|AUDIT-003|AUDIT-004 |
| AU-063 | SPLIT | TRAIN-001|TRAIN-007 |
| AU-064 | RENAME | ALGO-001 |
| AU-065 | RENAME | RULE-005 |
| AU-066 | SPLIT | STATE-003|ALGO-001 |
| AU-067 | KEEP | ALGO-003 |
| AU-068 | RENAME | SCORE-001 |
| AU-069 | SPLIT | STATE-010|ALGO-009 |
| AU-070 | SPLIT | STATE-002|STATE-003|STATE-005|STATE-006|STATE-010 |
| AU-071 | SPLIT | STATE-004|AUDIT-001|AUDIT-005 |
| AU-072 | SPLIT | RULE-003|RULE-004|RULE-007|RULE-008|RULE-009|RULE-010|RULE-011|RULE-012|RULE-013 |
| AU-073 | SPLIT | STATE-009|ALGO-006|ALGO-007|ALGO-008|HEUR-019|HEUR-021|HEUR-023 |
| AU-074 | RENAME | ALGO-002 |
| AU-075 | SPLIT | ALGO-003|ALGO-004|MODEL-001|MODEL-002|HEUR-015 |
| AU-076 | SPLIT | HEUR-019|HEUR-020|ALGO-005|ALGO-007 |
| AU-077 | SPLIT | TRAIN-001|TRAIN-007|TRAIN-008|TRAIN-009|MODEL-004|MODEL-005 |
| AU-078 | KEEP | TRAIN-002 |
| AU-079 | SPLIT | TRAIN-003|TRAIN-004 |
| AU-080 | KEEP | TRAIN-005 |
| AU-081 | SPLIT | TRAIN-006|STATE-008 |
| AU-082 | SPLIT | AUDIT-001|AUDIT-003 |
| AU-083 | SPLIT | AUDIT-002|AUDIT-003|AUDIT-014 |
| AU-084 | SPLIT | AUDIT-004|ALGO-008 |
| AU-085 | MERGE | AUDIT-013 |
| AU-086 | SPLIT | TRAIN-006|TRAIN-007 |
| AU-087 | SPLIT | AUDIT-005|RULE-003|RULE-004|RULE-005|SCORE-001 |
| AU-088 | MERGE | AUDIT-006 |
| AU-089 | KEEP | AUDIT-007 |
| AU-090 | RENAME | AUDIT-008 |
| AU-091 | SPLIT | AUDIT-009|AUDIT-012 |
| AU-092 | KEEP | AUDIT-010 |
| AU-093 | MERGE | AUDIT-013 |
| AU-094 | REMOVE | — |
| AU-095 | SPLIT | ALGO-009|STATE-007|AUDIT-011 |
| AU-096 | REMOVE | — |

统计：SPLIT 56；RENAME 20；MERGE 9；KEEP 8；REMOVE 3。REMOVE项保留为治理规则，不是运行单元；新增的4个ADD单元不属于旧96行。

## 10. 实现与验收顺序

具体模块结构、公共接口、状态机、事件总线、调用顺序、任务卡及迁移门禁见[开发实施指南](04-development-guide/development_guide.md)、[96单元开发任务卡](04-development-guide/development_task_cards.md)和[迁移计划](04-development-guide/migration_plan.md)。这些文件只做实现导航，不覆盖单元规格。

1. 六份详细规格已批准；后续规则或接口变化必须先更新相应规格并重新批准。
2. 维持96/96详细覆盖和规则→参数→单元→模块追踪完整性。
3. 按锁定DAG实现：配置/随机流→Match/牌墙/状态→规则/算法/计分→视图→启发式/模型→训练→审计。
4. 为每单元建立直接测试、集成证据和运行证据；hard断言不得被平均分抵消。
5. 执行跨文档矛盾检查、生产/训练等价、确定性回放、信息泄漏、计分守恒和发布门禁。
6. 本文`Approved`只表示规范契约经用户批准；只有全部适用单元证据达标、冲突关闭且发布门禁通过，才能将实现/验收状态提升为Done或AUDITED。

## 11. 当前结论

逐单元证据等级与最终`AUDITED`判定必须采用[审计与验收标准](06-audit-acceptance/audit_standard.md)、[96单元验收清单](06-audit-acceptance/acceptance_checklist.md)、[证据包模板](06-audit-acceptance/evidence_template.md)和[审计报告模板](06-audit-acceptance/audit_report_template.md)。`AUDITED`要求同一scope下AC-01～14全部Passed且至少E4；外部效果或发布声明按适用项达到E5。

目录、迁移映射、96张详细规格、开发导航、细化测试和审计验收契约在结构上完整；两份锁定来源hash一致。用户已批准CDI-003涉及的核心文档，最终锁定复审为Critical 0 / High 0，现建议锁定spec-v3规范全集。该建议只针对规范，不表示实现、测试运行或发布已完成；这些证据仍为Not Evaluated。详见[跨文档一致性复审](08-review/cross_document_consistency_report.md)、[未解决问题](08-review/unresolved_issues.md)和[最终就绪报告](08-review/final_readiness_report.md)。
# SPEC-V3-3.0.1补丁摘要

本补丁解决试点8项High：Python同名模块路径策略、RULE-016/STATE-005错位章节、可执行fixture门禁、HEUR-019计算图、MODEL-001校准manifest、SCORE-001事件/幂等schema、AUDIT-003逐字节hash公式，以及E3试点与E4生产AUDITED边界。详细定义仍仅在对应单元规格、测试规格、开发指南和审计标准中；本文不复制替代。

# SPEC-V3-3.0.3试点公共合同

十个试点的逐字段I/O、单位、来源、默认/null、分支ID、解释和正式证据禁用值唯一引用`03-unit-specs/pilot_unit_contracts_3_0_3.md`。

# SPEC-V3-3.1.0批量开发公共契约

所有批量实施单元必须引用`contracts/common_contracts.md`、`data_visibility_contract.md`和`versioning_policy.md`及其JSON Schema。牌/状态/动作/候选/评分/决策/解释/参数/随机/错误/fixture不得由策略重复定义。
