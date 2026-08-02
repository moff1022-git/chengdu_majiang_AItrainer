# Task 17：96 单元真实基线复审报告

状态：**Completed / Evidence Rebaseline**

## 结论

本次从锁定的 96 单元目录重新取证，状态分布为：{"AUDITED": 9, "INTEGRATED": 1, "PARTIAL": 85, "SCAFFOLDED": 1}。
旧的“33/61/2”统计未作为状态输入。M0 矩阵仅作为候选路径索引；脚本逐项验证当前文件、Python AST 符号、生产调用线索和测试函数。
除任务14/15已经形成四类证据闭环的单元外，旧代码即使含相关语义也只记为 PARTIAL，直到锁定边界、直接测试、完整流程运行和追溯证据全部补齐。

## 审计方法

- 规格：核对目录、详细规格、规则参数追踪矩阵，确认 96 个 ID 唯一且均有正式定义。
- 代码：逐个验证候选文件与 AST 符号；失效引用不进入 `code_refs`。
- 测试：逐个验证测试文件/测试函数；计划中的文件若当前不存在，不计证据。
- 运行：仅接受单元可归属的真实运行产物；普通测试文件存在不等于运行证据。
- 追溯：逐项建立规则→详细规格→目标模块链；AUDITED 仍要求四类证据同时存在。
- 安全：带 VISIBILITY 或私有/隐藏/全知语义的单元标为 `REQUIRES_BOUNDARY_TEST`，不等同于已发现泄漏。
- 占位：对候选符号检查空 `pass` 与 `NotImplementedError`；固定返回值不自动判占位，以免误判合法常量函数。

## 可直接验收与阻塞

可直接维持 AUDITED：`RULE-003`, `RULE-016`, `ALGO-001`, `ALGO-010`, `HEUR-019`, `STATE-005`, `SCORE-001`, `TRAIN-003`, `AUDIT-003`。
BLOCKED：无。当前差距均可通过既定实施/测试/证据流程关闭，未发现必须发明业务规则的矛盾。
`MODEL-001` 保持 INTEGRATED：代码、测试、运行与追溯存在，但任务15确认其模型校准验收尚未满足，不能提升为 AUDITED。

## 原子性、拆分与合并

- `RULE-001`：规则裁决、参数解析和不变量执行具有不同变化轴；进入实现批次前确认是否保留门面并拆为内部组件。建议只拆内部组件，保留锁定单元门面和 ID。
- `ALGO-002`：牌型拆解、普通/七对向听、弃牌向听和等待形状应以同一门面下的独立纯函数实现。建议只拆内部组件，保留锁定单元门面和 ID。
- `ALGO-008`：随机流派生、噪声与思考时间应共享种子契约但分离算法职责。建议只拆内部组件，保留锁定单元门面和 ID。
- `SCORE-004`：花猪、查大叫、退税是同一终局事务内三类独立调整，需分别留守恒证据。建议只拆内部组件，保留锁定单元门面和 ID。
- `AUDIT-009`：工程回归与行为回归指标的数据源、阈值和执行频率不同，建议拆为两个内部检查器。建议只拆内部组件，保留锁定单元门面和 ID。

未发现必须合并的单元。

## 主要差距

- 需继续实施或补证的单元：87 个。
- 当前具备代码证据：95 个；测试证据：94 个；运行证据：10 个；追溯证据：96 个。
- 候选索引中已失效、未被继承的路径/符号/测试引用：13 条。
- 被明确识别为 `pass`/`NotImplementedError` 的候选符号引用：0 条。
- 最大系统性缺口是非试点单元缺少锁定边界的直接测试和单元归属明确的运行证据，而不是规格目录缺失。

## 推荐开发批次

- **B0-PILOT-ACCEPTANCE**（10）：`RULE-003`, `RULE-016`, `ALGO-001`, `ALGO-010`, `HEUR-019`, `MODEL-001`, `STATE-005`, `SCORE-001`, `TRAIN-003`, `AUDIT-003`
- **B1-DETERMINISTIC-KERNEL**（30）：`RULE-001`, `RULE-002`, `RULE-004`, `RULE-005`, `RULE-006`, `RULE-007`, `RULE-008`, `RULE-009`, `RULE-010`, `RULE-011`, `RULE-012`, `RULE-013`, `RULE-014`, `RULE-015`, `ALGO-006`, `ALGO-009`, `ALGO-011`, `STATE-001`, `STATE-004`, `STATE-006`, `STATE-007`, `STATE-008`, `STATE-010`, `STATE-011`, `STATE-012`, `SCORE-002`, `SCORE-003`, `SCORE-004`, `SCORE-005`, `SCORE-006`
- **B2-DETERMINISTIC-COMPLETION**（9）：`ALGO-002`, `ALGO-003`, `ALGO-004`, `ALGO-005`, `ALGO-007`, `ALGO-008`, `STATE-002`, `STATE-003`, `STATE-009`
- **B3-HEURISTICS**（22）：`HEUR-001`, `HEUR-002`, `HEUR-003`, `HEUR-004`, `HEUR-005`, `HEUR-006`, `HEUR-007`, `HEUR-008`, `HEUR-009`, `HEUR-010`, `HEUR-011`, `HEUR-012`, `HEUR-013`, `HEUR-014`, `HEUR-015`, `HEUR-016`, `HEUR-017`, `HEUR-018`, `HEUR-020`, `HEUR-021`, `HEUR-022`, `HEUR-023`
- **B4-MODELS-CALIBRATION**（4）：`MODEL-002`, `MODEL-003`, `MODEL-004`, `MODEL-005`
- **B5-TRAINING**（8）：`TRAIN-001`, `TRAIN-002`, `TRAIN-004`, `TRAIN-005`, `TRAIN-006`, `TRAIN-007`, `TRAIN-008`, `TRAIN-009`
- **B6-AUDIT-RELEASE**（13）：`AUDIT-001`, `AUDIT-002`, `AUDIT-004`, `AUDIT-005`, `AUDIT-006`, `AUDIT-007`, `AUDIT-008`, `AUDIT-009`, `AUDIT-010`, `AUDIT-011`, `AUDIT-012`, `AUDIT-013`, `AUDIT-014`

批次内仍应按依赖图拓扑排序；每个单元在升级 AUDITED 前必须重新收集四类证据。

## 审计边界

本任务未修改业务代码、业务测试断言或规则文档；只生成新审计基线。失效候选引用保留为生成过程统计，不回写旧 M0 文件，以避免把历史线索改写成当前事实。

## 当前测试执行

Python 3.12 全量测试：386 passed、1 skipped、0 failed；JUnit：`docs/spec-v3/audit/task17_full_junit.xml`。

## 可复现命令

```bash
python3 tools/task17_rebaseline.py
PYTHONPYCACHEPREFIX=/tmp/task17_pycache .venv-macos/bin/python -m pytest -q --junitxml=docs/spec-v3/audit/task17_full_junit.xml
```
