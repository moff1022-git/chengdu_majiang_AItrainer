# F0034 Task 19 持续无人值守调度

Status: **Approved**（用户于 2026-08-01 明确要求实现）

## 目标

消除 Agent 一轮完成到下一门禁真实派发之间的人工“继续”操作。Root 持有唯一可恢复调度状态；监控器区分真实运行、等待 Agent、可派发和人工阻塞。

## 范围

- 新增可机读调度快照 `docs/status/task19_orchestrator_state.json`。
- 扩展 `tools/task19_agent_runtime.py`，支持真实 dispatch、complete、finding 和 next-gate 事件。
- runtime 的 `RUNNING` 仅由 dispatch 产生；complete 自动进入下一门禁的 `READY_TO_DISPATCH`，Root 必须真实派发后才恢复 RUNNING。
- 监控器读取调度快照；只要 wave 存在 `DISPATCHED/RUNNING/REMEDIATING/REVIEWING/VERIFYING/AUDITING` 工作即显示运行中。
- 保存修复轮数；同类 finding 第三次才进入人工门禁。

## 非范围

- 工具不能自行创建 Codex 子 Agent；真实 Agent 派发仍由 Root 会话的 Agent 调度能力执行。
- 不修改 Task 19 产品规则、Locked/Frozen 规格或审计门禁。
- 不执行 push、发布、删除或历史重写。

## 验收

1. 完成事件能产生确定的下一门禁和 `READY_TO_DISPATCH` 状态。
2. dispatch 后 runtime 和 orchestrator 快照原子一致，监控显示对应 wave `RUNNING`。
3. finding 自动进入 `REMEDIATING` 并累计轮数；第三次同类 finding 标人工确认。
4. stale 历史 Agent 不影响当前 wave。
5. 单元测试覆盖状态转换、恢复、监控投影和人工门禁。
