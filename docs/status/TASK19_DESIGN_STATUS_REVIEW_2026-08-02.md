# Task 19 设计状态复核

日期：2026-08-02

## 结论

`design_status=WAITING_APPROVAL` 不等于“程序未实现”。它表示该单元在 Task 19 的设计门禁字段仍未获得 `APPROVED`，即使代码、测试或独立审计证据已经存在，也不会自动改变该字段。

当前主矩阵有 78 个等待批准单元，主要是状态/流程标记未同步，但不能据此断言全部已有实现。证据如下：

- `task19_unit_execution_matrix.csv` 的 `design_status` 与 `implementation_authorization` 是设计授权状态，不是运行时实现状态；78 个单元统一为 `WAITING_APPROVAL/WAITING_FOR_DESIGN_APPROVAL`，呈现批量初始化/未回写特征。
- 同一仓库的 `task19_progress_tracker.md` 已记录部分单元的独立审计结果。例如 `RULE-001` 显示 `AUDITED`、14/14、`PASS`，但矩阵仍为 `PARTIAL + WAITING_APPROVAL`；这证明至少存在状态回写滞后。
- `ALGO-002`、`STATE-002`、`STATE-003` 已是 `design_status=APPROVED`，但 `current_status` 仍为 `PARTIAL`，说明“设计批准”和“实现完成”是两个独立门槛。
- `HEUR-001`、`AUDIT-010` 等单元在 tracker 中仍为 `NOT_STARTED` 或没有实现证据，不能仅因相关模块存在就判定完成。

## 三类判定

### 1. 明确是标记/回写错误

具备独立证据（代码入口、定向测试或审计报告），但矩阵仍保持 `WAITING_APPROVAL`。代表：`RULE-001`，以及 tracker 中已标记 `AUDITED/PASS` 的规则和审计单元。应补做证据索引和状态回写，不应重写业务代码。

### 2. 部分实现，不能升级为完成

存在模块或基础接口，但缺少规则 v1 要求的完整语义、反例测试或复盘字段。代表：多数 `RULE-*`、`ALGO-*`、`STATE-*`、`SCORE-*`、`AUDIT-*`。应保持 `PARTIAL`，先完成设计批准和验收证据。

### 3. 确实未实现/仅脚手架

tracker 明确为 `NOT_STARTED`、`SCAFFOLDED` 或 `PATH-EXTERNAL-DATA` 且无对应实现/证据的单元。代表：`HEUR-016`（行为序列推断，`SCAFFOLDED`）、`HEUR-001`、`AUDIT-010`、`MODEL-005`、`AUDIT-012`。这些不能通过简单改状态解决。

## 与规则 v1 的主要偏差

1. 决策八阶段顺序尚无统一断言：合法性、状态识别、计划回顾、新信息、候选、收益风险、人格修正、执行记忆未在每次 trace 中分别标识。
2. 信息边界缺少机械白名单：需证明未使用对手暗手、未来牌墙和不可见结算信息。
3. 换三张、定缺、早中晚盘计划、碰杠胡风险、终局强制胡等规则章节与代码/反例测试尚未逐条闭环。
4. 人格预设已有参数，但“参数改变→可观察行为改变”的消融证据不足。
5. 完整复盘要求 steps/audit 成对存在；补跑流程曾只写 `games.jsonl`，说明完整性门禁尚未固化。

## 建议的状态修正流程

1. 以 `task19_unit_execution_matrix.csv` 的 81 个主单元为起点，结合 `task19_progress_tracker.md`、evidence manifest 和测试结果，生成去重后的权威清单；在此之前不预设总数为 96。
2. 对每个单元分别填充 `design_status`、`implementation_status`、`verification_status`、`audit_status`，禁止用一个 `current_status` 混合表达。
3. 只有设计包批准后才改 `design_status=APPROVED`；只有实现、测试、审计均满足门禁后才改 `current_status=INTEGRATED/DONE`。
4. 将已审计通过但未回写的单元列为 `STATE_STALE`，修正文档状态而不改业务代码。
5. 对 `NOT_STARTED/SCAFFOLDED` 单元建立独立实现任务，不得批量标记完成。

## 最终判断

78 个单元不是“全部未实现”，也不是“全部只是标记错误”。当前更准确的结论是：

- 一部分是设计批准状态未回写；
- 一部分是基础代码存在但语义/测试/审计不完整；
- 少数仍是脚手架或外部数据依赖，确实未完成。

在完成上述分层复核前，不应宣称 Task 19 的全部单元完成；当前唯一已核实的主矩阵规模是 81 个。
