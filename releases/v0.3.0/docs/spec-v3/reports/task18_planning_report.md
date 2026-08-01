# Task 18A：87 个非 AUDITED 单元缺口分型与批次规划报告

状态：**Completed / planning evidence only**  
权威来源：`docs/spec-v3/audit/task17_96_unit_audit_clarification.md`  
当前工作树测试：387 passed，0 failed，0 skipped，234.46s

## 技术摘要

Task 17 的 9/1/85/1 状态未改变。87 个非 AUDITED 单元已完成逐行分型、主要完成路径分配和无重复批次归属。由于 Task 17 对 85 个 PARTIAL 只确认了候选实现/测试线索，没有证明完整 Locked 语义，本计划保守地不把任何 PARTIAL 标成 `PATH-EVIDENCE-ONLY`、`PATH-TEST-CLOSURE` 或 `PATH-INTEGRATION-CLOSURE`。

| 主要完成路径 | 单元数 |
|---|---|
| PATH-EXTERNAL-DATA | 3 |
| PATH-FULL-IMPLEMENTATION | 1 |
| PATH-SEMANTIC-COMPLETION | 83 |

`PATH-SEMANTIC-COMPLETION` 包含仍需逐字段验证并可能补齐语义的单元；这不表示必须重写全部候选实现。`HEUR-016` 是唯一完整实现路径。`MODEL-001`、`MODEL-005`、`AUDIT-012` 以外部数据/产物/效果证据为主要完成路径，其中只有 MODEL-001 的规则 fallback 已形成 INTEGRATED 工程链。

## 范围、数据与定义

分析总体是 SPEC-V3-3.1.0 的 96 个锁定单元；待规划总体是剔除 9 个 AUDITED 后的 87 个唯一 unit_id。输入以 Task 17 gap matrix 为行粒度，以 Task 15 试点证据、Task 16 Frozen 契约、96 单元规格卡及当前代码/测试目录为约束来源。布尔缺口表示“仍需闭合的验收条件”，不表示已确认缺陷；主要完成路径表示当前最主要的闭合方式，不排除同一单元具有多个缺口。

## 缺口分布

| 缺口类型 | 单元数 |
|---|---|
| gap_spec | 0 |
| gap_code | 86 |
| gap_direct_test | 86 |
| gap_branch_test | 87 |
| gap_integration | 86 |
| gap_runtime | 86 |
| gap_trace | 86 |
| gap_boundary | 78 |
| gap_reproducibility | 86 |
| gap_model_data | 7 |
| gap_performance | 86 |
| gap_atomicity | 5 |

`gap_spec=0`：96 个 Locked 单元规格和追踪端点齐全，当前未发现必须先做规则决策的单元。`gap_direct_test=86` 使用 Locked 单元直接验收口径；MODEL-001 已有直接工程测试，其缺口是校准分支与外部数据。其余单元即使 Task 17 找到旧测试候选，也不等于直接测试闭环。`gap_boundary` 只表示专项测试要求，不表示泄漏已发生。

## 关键分型

- 只补证据且不改业务代码：当前为 0。原因是 Task 17 没有证明任何 PARTIAL 的完整生产语义；未来批次复核若证明语义完整，可在新证据下改走 evidence-only，但不能在 Task 18A 预判。
- 需要语义补全：83。应优先复用候选实现，只补锁定语义缺口，禁止无关重构。
- 需要完整实现：1，即 `HEUR-016`。
- 主要外部数据路径：3，即 `MODEL-001`、`MODEL-005`、`AUDIT-012`。
- 含 `GAP-MODEL-DATA`：7，即 MODEL-001～005、TRAIN-008、AUDIT-012；其中工程准备和确定性 fallback 可继续。
- 原子性内部拆分复核：5，即 RULE-001、ALGO-002、ALGO-008、SCORE-004、AUDIT-009；只拆内部职责，不改变 Locked ID/门面。

## 第一批

立即执行 `B1-A = STATE-010, ALGO-009, ALGO-011`。真实依赖根是 STATE-010；完成并独立审计 STATE-010 后，ALGO-009 与 ALGO-011 可并行开发与取证。

## 方法与限制

分型直接继承 Task 17 的代码、测试、运行、追踪、依赖、风险和原子性字段，并对 Task 15 试点与 Task 16 Frozen 契约进行约束复核。Task 18A 没有重跑逐单元生产 trace，因此所有状态保持不变；本报告是执行计划，不是新的 AUDITED 判定。

稳健性检查包括：96/87集合差、状态透视、分类计数、批次并集/交集、逐单元依赖顺序、批次依赖顺序、MODEL-001与HEUR-016特例、86个边界测试标记覆盖及每批入口/出口字段完整性。主要限制是 Task 17 对多数单元只保留候选实现/测试线索，因此本计划宁可归入语义补全，也不无证据推断为 evidence-only。

## 建议下一步

启动 B1-A 的 Docs-First 实施与独立审计。实现阶段只能修改该批范围，测试阶段补直接/分支/边界/回放，审计阶段再决定三个单元是否逐个达到 AUDITED。

下一条可直接用于开发的 Codex 提示词：

```text
执行成都麻将AI训练模拟器 Task 18 B1-A：仅处理 STATE-010、ALGO-009、ALGO-011。以 docs/spec-v3/plans/development_batches_v3.md、task18_gap_classification.csv、Task 16 Frozen 公共契约和 Locked 单元规格为权威。先按 STATE-010 → ALGO-009/ALGO-011 的批内拓扑核实现有代码与测试；规格已 Approved/Locked 后再补齐最小业务语义，不做无关重构。为每个单元分别补直接、关键分支、异常、固定 seed、性能、生产接线、运行 trace、追踪及信息边界测试，运行定向/契约/全仓回归。开发交付与独立审计分开；没有四类证据和 AC-01～AC-14 闭环不得标 AUDITED。不得修改其他 Task 17 状态，不得让 MODEL-001 数据门禁阻塞本批。
```

## 进一步问题

- B1-A 实施取证后，哪些候选实现可被证明语义完整并转为 test/evidence closure，而无需继续改业务逻辑？
- MODEL-001 合规冻结数据由谁提供、采用何种来源许可与玩家/牌局分组键？
- 独立审计执行者与开发执行者如何在仓库证据包中记录分离签名？
