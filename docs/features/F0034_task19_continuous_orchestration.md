# F0034 Task 19 持续无人值守调度

Status: **Approved**（用户于 2026-08-01 明确要求实现；同日确认为 CLI 重启后自动续跑，不使用外部自动唤醒程序）

## 目标

消除 Agent 一轮完成到下一门禁真实派发之间的人工“继续”操作。Root 持有唯一可恢复调度状态；监控器区分真实运行、等待 Agent、可派发和人工阻塞。

同时消除对单个 session transcript 的依赖：会话存活时由 Root 连续调度；CLI 关闭期间任务暂停，用户下次启动 Codex CLI 进入本仓库后，自动从仓库权威状态恢复并续跑，不需要再输入“继续 Task 19”。

## 调度与重启恢复

### 已授权的可判定门禁自动放行

项目所有者已统一授权 Task 19 的常规验证、修复、复审、审计及平台/Git 强制确认。对已经有明确通过口径、仅因旧 session 等待确认而停留的可判定门禁，Startup Reconciler 必须自动采用已批准口径并继续；不得把这类门禁留在 `HUMAN_DECISION`。

- TRAIN-005 使用已通过且不改变权威业务语义的 `contract-transition` workload 口径自动恢复。
- 只有真正的新产品语义选择、Locked/Frozen 冲突、第三次同类 finding 或 ADR-0001 明确人工门禁继续停止。

### 会话内：Root Orchestrator

- 消费 Agent 完成、finding、验证和审计事件，自动派发下一门禁。
- 在每个状态转换后原子写入 orchestrator/runtime 快照，并在闭环时同步 tracker 与 `LATEST.md`。
- 使用 `batch + gate + candidate_sha + attempt` 作为幂等键，避免恢复后重复实施或重复集成。

### CLI 重启后：Startup Reconciler

- 新 session 进入本仓库时，按 `AGENTS.md` 指定的读取顺序执行 Task 19 startup reconcile。
- 如调度快照显示 Task 19 未完成且无真正人工门禁，Root 立即恢复 Goal，清理过期 Agent 投影，并续派未完成门禁。
- 对已登记的可判定人工门禁，先执行授权策略归一化，再计算恢复队列。
- 优先使用 `codex resume --last`保留上一 session 上下文；即使恢复的 transcript 不可用，新 session 也必须能仅依赖仓库状态续跑。
- 恢复动作由已启动的 Codex 执行，不安装、注册或运行任何外部自动唤醒程序。

## 恢复协议

1. 按 `docs/status/LATEST.md` → Task 19 tracker → `task19_orchestrator_state.json` → `task19_agent_runtime.json` 的顺序读取；对话 transcript 不是权威状态。
2. 比较 integration worktree HEAD、candidate/evidence SHA、门禁状态、心跳和锁，先 reconcile，后派发。
3. 对 `DISPATCHED/REMEDIATING` 但没有活跃 Agent 的工作，根据幂等键续派；已存在对应 candidate/evidence 时不重复生成。
4. 同类 finding 第三次、Locked/Frozen 冲突或 ADR-0001 真正人工门禁时，写入 `BLOCKED/confirm=YES`，重启后不自动续派该门禁。
5. Task 19 已完成或无可派发工作时，启动 reconcile 不创建新 Agent。

## 系统边界

- CLI 关闭期间没有 Codex 执行主体，Task 19 暂停；这是用户明确选择的边界。
- “自动继续”指用户重启 Codex CLI 后不需要另外发送续跑指令，不指 CLI 关闭期间自动重启 Codex。

## 范围

- 新增可机读调度快照 `docs/status/task19_orchestrator_state.json`。
- 扩展 `tools/task19_agent_runtime.py`，支持真实 dispatch、complete、finding 和 next-gate 事件。
- runtime 的 `RUNNING` 仅由 dispatch 产生；complete 自动进入下一门禁的 `READY_TO_DISPATCH`，Root 必须真实派发后才恢复 RUNNING。
- 监控器读取调度快照；只要 wave 存在 `DISPATCHED/RUNNING/REMEDIATING/REVIEWING/VERIFYING/AUDITING` 工作即显示运行中。
- 保存修复轮数；同类 finding 第三次才进入人工门禁。
- 定义跨 session 恢复协议、幂等键和真正人工门禁停机条件。
- 在仓库启动基线中登记 Task 19 未完成时的自动 reconcile 行为。

## 非范围

- 工具不能自行创建 Codex 子 Agent；真实 Agent 派发仍由 Root 会话的 Agent 调度能力执行。
- 不修改 Task 19 产品规则、Locked/Frozen 规格或审计门禁。
- 不执行 push、发布、删除或历史重写。
- 不实现、安装或启动 `launchd`、Task Scheduler、常驻守护进程或其他外部自动唤醒程序。
- 不使用 `danger-full-access`，不在仓库中保存认证信息或 token。

## 验收

1. 完成事件能产生确定的下一门禁和 `READY_TO_DISPATCH` 状态。
2. dispatch 后 runtime 和 orchestrator 快照原子一致，监控显示对应 wave `RUNNING`。
3. finding 自动进入 `REMEDIATING` 并累计轮数；第三次同类 finding 标人工确认。
4. stale 历史 Agent 不影响当前 wave。
5. 单元测试覆盖状态转换、恢复、监控投影和人工门禁。
6. 模拟 CLI 退出并由用户重启后，Startup Reconciler 能在无重复派发的前提下恢复未完成门禁。
7. 真正人工门禁在重启后仍停止续派并在监控器中显示；非人工门禁不需要用户再输入“继续”。
