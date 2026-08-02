# ADR-0001 Agent 编排的无人值守开发流程

| 字段 | 值 |
|---|---|
| 状态 | **Accepted** |
| 日期 | 2026-07-31 |
| 范围 | Task 19 及后续 Docs-First 批次开发 |
| 不变项 | Engine 权威、Docs-First、Locked/Frozen、独立审计、Task17 历史 |

## 1. 问题

Task 19 已把角色拆为 Terminal 0～3，但实际流程仍由用户手动完成以下编排：

1. 把上一终端结果复制给下一终端；
2. 逐步发出“继续测试 / 修改 / 复审 / 审批 / 集成”指令；
3. 手动监视分支、worktree、progress delta 和 tracker 的状态；
4. 在没有新产品决策的情况下反复授权可恢复的常规工程动作。

这不是多 Agent 自动化，而是“多窗口 + 人工消息总线”。它产生三类浪费：

- 交接等待和上下文重建成本高于实际开发时间；
- 并行度由窗口数量决定，而不是由依赖图、写路径和共享接口决定；
- “独立审计”与“需用户点击启动审计”被误绑定，独立性没有提高，反而降低吞吐。

## 2. 决策建议

采用“单一 Orchestrator + 按需短生命 Agent”模式。用户批准一个有边界的批次目标后，Orchestrator 在不触发人工门禁时自动完成：

```text
Approved batch
  -> implementer agent
  -> deterministic tests / evidence
  -> fixer loop (bounded)
  -> reviewer agent
  -> remediation loop (bounded)
  -> independent auditor agent
  -> integration verifier
  -> tracker + LATEST + changelog
  -> one final delivery report
```

Agent 是可调度角色，不是长期人工窗口。Orchestrator 持有唯一任务状态，从 Git commit、测试产物和结构化 delta 传递上下文，不要求用户复制文本。

## 3. 用户干预门禁

默认不干预。仅在以下情形停止并请求用户决策：

| 门禁 | 需要用户的原因 |
|---|---|
| 产品/规则语义存在多个合理选项 | Agent 不得代替产品所有者决策 |
| 需修改 Locked/Frozen、公开接口或既有测试断言 | 超出已批准范围 |
| 发现范围外或来源不明的 dirty 改动且无法隔离 | 存在覆盖用户成果风险 |
| 需删除、重写历史、push/发布、外部数据或凭据 | 不可逆或外部影响 |
| 同一失败类别经 3 轮修复仍无法关闭 | 需要新决策或重规划 |
| 独立审计发现 P0/P1 或证据不可归属 | 不允许自动降低门禁 |

以下动作在已批准批次内应自动进行，不再逐步请示：

- 读取文档、编写授权范围内的代码与新测试；
- 运行定向/契约/全仓测试、生成 E4/E5、修复同范围失败；
- 创建批次内可恢复的 commit，启动只读复审和独立审计 Agent；
- 根据预先批准的集成顺序集成，原子更新 tracker 与收尾文档。

## 4. 并行策略

默认不为每个角色常驻一个分支或窗口。只在下列条件全部成立时并行：

1. 依赖图上不存在直接或间接依赖；
2. 写路径集合不相交；
3. 公共 DTO、错误码、PlayerView、状态、配置和 fixture 拥有者不冲突；
4. 每个任务可独立测试、取证、提交和回滚；
5. 预计计算时间明显高于 worktree/交接/集成成本。

否则使用一个分支内的串行 Agent 角色轮换。特别是 B2-A1 的 `STATE-002 -> STATE-003 -> ALGO-002` 是强依赖链，应保留一个 worktree，由 implementer/fixer/reviewer/auditor 分时处理，不应再拆成多个人工窗口。

并行数不固定为三个终端：

- `0`：没有 Approved 的可执行单元；
- `1`：强依赖、共享接口高风险或小任务；
- `2～N`：仅对无依赖且写集合互斥的长耗时任务。

## 5. 自动状态机

```text
WAITING_FOR_DESIGN_APPROVAL
  -> READY_FOR_IMPLEMENTATION       (owner-approved design exists)
  -> IMPLEMENTING
  -> VERIFYING
  -> REMEDIATING                    (bounded loop)
  -> READY_FOR_REVIEW
  -> REVIEW_REMEDIATION             (bounded loop)
  -> READY_FOR_INDEPENDENT_AUDIT
  -> AUDIT_REMEDIATION              (bounded loop)
  -> READY_FOR_INTEGRATION
  -> INTEGRATION_VERIFYING
  -> AUDITED / INTEGRATED / FAILED
```

每次转换必须由可机读证据触发，不由对话文字触发。证据至少包含 commit SHA、允许/禁止路径校验、测试 run ID、E4/E5 hash、AC 结果和 Agent 身份。

## 6. 安全和独立性

- Implementer 与 independent auditor 必须是不同 Agent 身份；审计 Agent 只读目标 commit 的干净导出。
- Reviewer/auditor 不直接修代码；只产出结构化 finding，由 fixer Agent 修复并重跑完整门禁。
- Orchestrator 不得以自动化为理由降低测试、AC、信息边界、复现或性能门禁。
- 有无人值守授权不等于有 push、发布、删除、外部数据或 Locked/Frozen 修改授权。
- 每个批次必须有最大修复轮数、最大 wall time 和可恢复检查点；超限后停在安全 commit 并报告。

## 7. Task 19 迁移方案

1. 保留现有 W01 分支和 worktree 作为可恢复资产，不继续增加常驻窗口。
2. Terminal 0 职责改为 Orchestrator，自动启动 implementer/reviewer/auditor/fixer 角色。
3. 对已有 W01 工作：MODEL-001 修复先自动独立复审；B2-A1 在原分支闭环；RULE-015/AUDIT-010/TRAIN-009 仅在真正所有者决策处请示。
4. 实现一个小型 orchestrator/progress tool 之前，可先由单一 Codex session 执行同一状态机，内部调度子 Agent；用户只收到门禁问题或最终报告。
5. 迁移后用一个 W01 批次度量：用户交互次数、Agent 等待时间、总 wall time、返工轮数、集成冲突和逃逸缺陷。

## 8. 验收条件

- 已 Approved 且无新语义决策的批次，可从实现自动推进到独立审计结论，中间用户交互为 0。
- 用户问题只包含多选一的产品/规则决策或明确扩权，不再是“是否继续下一步”。
- 无共享写路径或接口冲突，状态更新可从 commit/evidence 重建。
- 独立审计身份分离、只读导出和证据门禁不低于现有 Task 19 要求。
- 分支/worktree 数量由实际可并行任务动态确定，不再与 Terminal 角色数量绑定。

## 9. 未在本 ADR 中授权的事项

- 本 ADR 已由项目所有者于 2026-07-31 批准；Task 19 自此默认按本 ADR 的无人值守门禁运行。
- 未授权实现 orchestrator 工具、自动 commit/集成或任何业务代码。
- 未批准 RULE-015、AUDIT-010、TRAIN-009 的待决策语义。

## 10. 2026-08-01 持续调度补充决议

项目所有者要求解决“Agent 一轮完成后临时中断，必须再次人工发送继续”的问题，现追加授权实现最小 Root 调度工具和持续目标：

- 子 Agent 完成、复审 PASS/BLOCKED、验证或审计结束后，Root 必须自动计算并真实派发下一任务，不得只把 runtime 标成 `RUNNING`。
- 调度状态必须落盘，记录 wave、batch、gate、owner、真实 Agent 状态、修复轮数、下一动作和最后事件；对话不是恢复源。
- runtime 心跳只描述已真实派发的工作；没有活跃 Agent 时应显示 `READY_TO_DISPATCH` 或 `WAITING`，不得伪造 `RUNNING`。
- 当前 Task 19 注册为持续目标；只在 §3 的真实人工门禁或三轮同类失败时停止。
- 工具只维护调度/runtime 状态，不绕过 Docs-First、独立审计或 tracker 的 Terminal 0 权威。
