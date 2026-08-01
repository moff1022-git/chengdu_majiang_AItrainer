# Task 19 剩余开发并行执行总计划

最终规划状态：`TASK19_WAITING_FOR_APPROVAL`。计划结构完整，但 dirty 主工作树尚未固化为 clean checkpoint，不能安全创建并行 worktree。

## 基线与范围

- 当前 commit：`423326ecf6e602f9c1c3392dd2a844b1e61ce9b3`；该 commit 不包含当前工作树中的全部已审计/已批准成果。
- Task 18 当前状态：15 AUDITED / 1 INTEGRATED / 79 PARTIAL / 1 SCAFFOLDED。
- 剩余 81 单元已重分为 40 个 1～4 单元批次和 14 个依赖 wave；不以批次 PASS 替代逐单元 AC/E4/E5/审计。
- B2-A1 决策完整保留，仍按 STATE-002 -> STATE-003 -> ALGO-002，且允许新增直接测试文件/用例，禁止改既有断言。

## 执行模型

Terminal 0 独占全局计划、权威进度、接口提案、集成、全仓回归和审计协调。Terminal 1～3 只在 clean baseline worktree 中修改批次授权路径，提交批次代码/测试/E4/E5和 progress delta。每个批次经历设计审批、实现、证据、独立审计和 Terminal 0 状态升级。

首个可实施批次只有 `T19-B2A1`。首波另外可隔离候选 `AUDIT-010/RULE-015/TRAIN-002/TRAIN-004/TRAIN-009` 只能并行做设计审查；`ALGO-003/HEUR-006/STATE-006/RULE-006` 因共享 PlayerView、RoundRuntime、orchestrator 或状态接口，不与 B2-A1 并行实现。

串行关键路径：B2-A1 -> RULE-001/005 -> RULE-004/010/011 -> RULE-009/013/014 -> SCORE-002/003 -> SCORE-004/005 -> SCORE-006 -> STATE-006/008 -> MODEL-002/003 -> HEUR-013/015 -> HEUR-018 -> AUDIT-006/007 -> AUDIT-010/008 -> AUDIT-009/011 -> MODEL-005 -> AUDIT-012。

## 完成定义

每单元分别满足 Approved/Locked 语义、生产实现、直接/分支/异常/确定性/性能/集成/信息边界测试、生产接线、四类 E4、逐增量 E5、14/14 AC、完整 SHA-256、定向/契约/全仓回归、独立审计和无开放 P0/P1。开发终端不得标记 AUDITED。

## 当前阻塞

1. `T19-RISK-001`：dirty 主工作树需人工区分并固化检查点。建议在用户确认后由 Terminal 0 精确暂存已审计与 Task19 计划成果，创建 checkpoint commit/tag；无关用户修改不得纳入或清理。
2. `T19-RISK-002`：除 B2-A1 外均需 Docs-First 设计审批。
3. `T19-RISK-004`：MODEL-001 等外部数据门禁只保留在外部数据轨道。

进度权威仅为 `task19_progress_tracker.md`；摘要由该文件确定性生成。
