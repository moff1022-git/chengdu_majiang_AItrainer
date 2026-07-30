# Task 17：96 个单元审计状态重新明确

状态：**Completed / Clarification of Task 17 evidence rebaseline**  
日期：2026-07-30  
适用基线：`SPEC-V3-3.1.0`

## 技术结论

Task 17 对锁定目录中的 96 个单元重新取证后的唯一有效状态分布为：

| 状态 | 数量 | 占比 | 含义 |
|---|---:|---:|---|
| AUDITED | 9 | 9.4% | 规格、代码、直接测试、可归属运行和追踪证据形成闭环 |
| INTEGRATED | 1 | 1.0% | 已接入生产链并有工程证据，但专项验收门禁未闭合 |
| PARTIAL | 85 | 88.5% | 存在部分代码/测试线索，但锁定单元边界的直接测试或运行/验收证据不完整 |
| SCAFFOLDED | 1 | 1.0% | 只有规格与追踪骨架，未找到独立生产实现和当前可验证测试 |

以上合计 96。旧的“33 完成、61 部分、2 未实现”不得再用于描述 Spec v3 当前状态；M0 矩阵也只能作为候选路径索引。

## 证据口径决定了为什么只有 9 个 AUDITED

| 证据类别 | 已具备 | 未具备 | 解释 |
|---|---:|---:|---|
| 代码证据 | 95 | 1 | 仅 `HEUR-016` 未找到独立生产符号 |
| 测试证据 | 94 | 2 | `HEUR-016`、`AUDIT-010` 未找到当前可验证直接测试 |
| 可归属运行证据 | 10 | 86 | 这是绝大多数单元不能升级为 AUDITED 的主要原因 |
| 追踪证据 | 96 | 0 | 96 个单元均有规则→规格→实现目标链，但追踪存在不代表实现验收通过 |

AUDITED 必须同时满足四类证据并通过锁定验收条件。普通旧测试、相邻模块测试或候选生产符号只能证明“存在相关实现线索”，不能单独把单元提升为 AUDITED。

## 96 个单元的明确状态

下表按类别覆盖全部 96 个锁定 ID。表中未省略任何单元。

| 类别 | AUDITED | INTEGRATED | SCAFFOLDED | PARTIAL |
|---|---|---|---|---|
| RULE（16） | RULE-003、RULE-016 | — | — | RULE-001、RULE-002、RULE-004～RULE-015 |
| ALGO（11） | ALGO-001、ALGO-010 | — | — | ALGO-002～ALGO-009、ALGO-011 |
| HEUR（23） | HEUR-019 | — | HEUR-016 | HEUR-001～HEUR-015、HEUR-017、HEUR-018、HEUR-020～HEUR-023 |
| MODEL（5） | — | MODEL-001 | — | MODEL-002～MODEL-005 |
| STATE（12） | STATE-005 | — | — | STATE-001～STATE-004、STATE-006～STATE-012 |
| SCORE（6） | SCORE-001 | — | — | SCORE-002～SCORE-006 |
| TRAIN（9） | TRAIN-003 | — | — | TRAIN-001、TRAIN-002、TRAIN-004～TRAIN-009 |
| AUDIT（14） | AUDIT-003 | — | — | AUDIT-001、AUDIT-002、AUDIT-004～AUDIT-014 |

### 9 个 AUDITED 单元

`RULE-003`、`RULE-016`、`ALGO-001`、`ALGO-010`、`HEUR-019`、`STATE-005`、`SCORE-001`、`TRAIN-003`、`AUDIT-003`。

这些单元是 Task 14/15 试点中形成四类证据闭环并在 Task 17 重新验证后可维持 AUDITED 的单元。Task 17 没有把其他单元因“代码存在”或“测试通过”而批量升级。

### MODEL-001：唯一 INTEGRATED

`MODEL-001` 已有代码、测试、运行与追踪工程证据，生产规则 fallback 也已接入；但锁定验收还要求合规冻结校准发布，包括至少 10,000 个有效样本、隔离 label zone、分组防泄漏切分及 Brier/log loss/ECE 等指标。

因此它只能保持 INTEGRATED，不能标为 AUDITED。当前外部数据门禁编号为 `MODEL001-DATA-001`。不得用规则 fallback 生成标签后再评价同一 fallback。

### HEUR-016：唯一 SCAFFOLDED

`HEUR-016`（行为序列推断）有正式规格和追踪链，但 Task 17 未找到可核查的独立生产符号，也未找到当前可验证的直接测试或运行证据。它需要新增或明确隔离生产单元，并补齐单元、边界、集成和回放测试。

### 85 个 PARTIAL 单元

这些单元并非“完全未实现”。其中绝大多数已找到相关旧实现或测试候选，但尚未证明：

1. 实现严格对应锁定的 Spec v3 单元边界；
2. schema、错误码、参数、状态与审计字段全部符合规格；
3. 具有锁定单元的直接测试，而不是只被相邻功能间接覆盖；
4. 具有可归属的生产/集成/回放运行证据；
5. 同一版本范围内完成四类证据和 AC-01～AC-14 验收闭环。

因此 PARTIAL 是“有实现线索但未完成单元验收”，不是完成状态。

## 分类审计情况

| 类别 | 总数 | AUDITED | INTEGRATED | PARTIAL | SCAFFOLDED | 当前判断 |
|---|---:|---:|---:|---:|---:|---|
| RULE | 16 | 2 | 0 | 14 | 0 | 两个试点闭环，其余需直接规则/状态边界和运行证据 |
| ALGO | 11 | 2 | 0 | 9 | 0 | 编码守恒与 PlayerView 白名单闭环，其余需确定算法直接验收 |
| HEUR | 23 | 1 | 0 | 21 | 1 | Top-K 注意闭环；行为序列推断仍只有骨架 |
| MODEL | 5 | 0 | 1 | 4 | 0 | 工程接入不等于模型校准与外部效果通过 |
| STATE | 12 | 1 | 0 | 11 | 0 | PlayerView 状态载体闭环，其余需权威状态机证据 |
| SCORE | 6 | 1 | 0 | 5 | 0 | 分数账本守恒闭环，其余需逐事件/终局事务证据 |
| TRAIN | 9 | 1 | 0 | 8 | 0 | codec/mask 闭环，其余依赖生产等价训练链 |
| AUDIT | 14 | 1 | 0 | 13 | 0 | hash 链闭环，其余缺直接测试、运行或发布证据 |

## 风险与审计边界

- `BLOCKED` 单元为 0：Task 17 当时没有发现规格矛盾或必须重新发明业务规则的单元。
- 这不表示所有工作均可立即完成：Task 18 后续确认 `MODEL-001` 的外部校准数据缺口是实际数据门禁；它不阻断 B1～B3，但阻断相关模型校准和外部评价声明。
- 86 个单元标有 `REQUIRES_BOUNDARY_TEST`，表示涉及可见性、私有信息或全知信息边界，需要专项测试；这不是“已发现 86 个泄漏缺陷”。
- 缺口严重度字段分布为 HIGH 50、MEDIUM 45、LOW 1；该字段是补齐优先级，不是完成状态，也不能与 AUDITED/PARTIAL 直接互换。
- 候选索引中有 13 条失效引用已被剔除；未发现候选符号为 `pass` 或 `NotImplementedError`。
- 5 个单元建议仅拆分内部职责：`RULE-001`、`ALGO-002`、`ALGO-008`、`SCORE-004`、`AUDIT-009`。锁定外部门面和 ID 保持不变；没有必须合并的单元。

## 可执行批次

| 批次 | 数量 | 审计含义 |
|---|---:|---|
| B0-PILOT-ACCEPTANCE | 10 | 9 AUDITED + MODEL-001 INTEGRATED；不是 10 个全部 AUDITED |
| B1-DETERMINISTIC-KERNEL | 30 | 规则、核心算法、状态和计分内核，均需逐单元补证 |
| B2-DETERMINISTIC-COMPLETION | 9 | 其余确定算法与状态单元 |
| B3-HEURISTICS | 22 | 除 HEUR-019 外的启发式单元；包含 SCAFFOLDED 的 HEUR-016 |
| B4-MODELS-CALIBRATION | 4 | MODEL-002～005；另需处理 MODEL-001 数据门禁 |
| B5-TRAINING | 8 | 除已审计 TRAIN-003 外的训练单元 |
| B6-AUDIT-RELEASE | 13 | 除已审计 AUDIT-003 外的审计与发布单元 |

批次数量总计 96。批次只是推荐实施分组，不能作为批量状态升级依据；每个单元必须独立取得四类证据。

## 方法、完整性与复核结果

本说明直接使用 Task 17 的 `unit_rebaseline_summary.json`、`unit_gap_matrix_v3.csv`、`unit_catalog_v3.csv`、`unit_rebaseline_report.md` 和 JUnit 产物。复核确认：

- 机器可读矩阵恰有 96 行，单元 ID 覆盖 96/96；
- 分类数量为 RULE 16、ALGO 11、HEUR 23、MODEL 5、STATE 12、SCORE 6、TRAIN 9、AUDIT 14；
- 状态透视表与 summary JSON 完全一致；
- AU-001～AU-096 迁移覆盖为 96/96；
- Task 17 测试产物记录 387 tests：386 passed、1 skipped、0 failed、0 errors；
- 2026-07-30 本机初始化复验为 387 passed、0 failed，但该新测试运行不自动改变 Task 17 的逐单元状态，因为没有重新生成单元归属证据包。

## 限制与后续判定规则

本说明是对 Task 17 结果的重新解释和明确列示，不是 Task 17 之后的新一轮 96 单元实现审计。它没有重新判定当前工作树中后续代码改动是否足以提升单元状态。

后续任何状态升级必须在同一代码/规格版本范围内更新 `unit_gap_matrix_v3.csv` 或新的版本化审计矩阵，并保存直接测试、运行产物、追踪链及 AC 验收结果。未重新取证前，本文件中的 9/1/85/1 是当前权威解释。

## 来源

- `docs/spec-v3/audit/unit_rebaseline_summary.json`
- `docs/spec-v3/audit/unit_rebaseline_report.md`
- `docs/spec-v3/audit/unit_gap_matrix_v3.csv`
- `docs/spec-v3/audit/unit_catalog_v3.csv`
- `docs/spec-v3/audit/unit_dependency_graph.md`
- `docs/spec-v3/audit/task17_full_junit.xml`

