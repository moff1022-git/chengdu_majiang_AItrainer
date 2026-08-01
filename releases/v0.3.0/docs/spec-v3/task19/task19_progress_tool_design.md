# tools/task19_progress.py / task19_monitor.py 设计

| 字段 | 值 |
|---|---|
| 状态 | Approved |
| 批准日期 | 2026-07-31 |
| 批准指令 | 用户要求生成动态任务状态程序 |

命令：`validate`, `summary`, `apply-delta`, `show-unit`, `show-batch`, `show-wave`, `list-blocked`, `list-next`。只解析结构化 CSV/JSON 和固定 Markdown；完整校验表头/章节/96行/枚举/公式/转换/Task17；使用临时文件、fsync 与原子替换；以 delta 唯一摘要实现幂等；拒绝开发终端提交 AUDITED。

内部缓存 `.task19_progress_state.json` 可选且非权威，必须能从 Markdown 重建；不一致时报错并以 Markdown 为准。直接测试设计覆盖 Markdown 转义、重复 delta、非法转换、错误 writer、原子失败、稳定字节输出和摘要一致性。

## 动态监控器

`tools/task19_monitor.py` 是只读视图，不实现 `apply-delta`，不改 tracker 或 Git：

- 默认每 2 秒刷新终端；`--once` 输出一次，`--json` 供其他工具读取。
- 展示 14 个 wave 及 40 个 batch 的 `COMPLETED / IN_PROGRESS / NOT_STARTED`，同时汇总 96 单元的权威 tracker 状态。
- wave/batch 状态只由 tracker 单元状态投影；存在任意活动状态则为进行中，全部 `AUDITED` 才是已完成。
- 总体、wave 和 batch 进度百分比取所属单元权威 tracker `progress` 的算术平均，保留 2 位小数；这是 evidence-gate 完成度，不是墙钟时间或 ETA。
- 运行时间起点默认取 Task 19 checkpoint 授权文件的时间；可用 `--started-at ISO-8601` 显式覆盖。
- 同时显示数据最后更新时间和“状态可能滞后”警告，避免把 Agent 运行态伪装成 tracker 已落盘状态。
- 读取 `docs/status/task19_agent_runtime.json` 显示 Agent 名称、状态、当前工作、首次登记时间、已运行时间、最后心跳、是否需要人工确认及原因。该文件是 Orchestrator 写入的运行快照，不是审计证据或进度权威。
- `requires_human_confirmation` 只能由 Orchestrator 在存在真实人工门禁时显式置 `true`，并必须提供 `confirmation_reason`；`STALE`、`INTERRUPTED` 或测试失败不自动等于需要人工确认。
- Agent 面板显示快照登记数和快照年龄；Orchestrator 每次创建、完成、中断 Agent 或收到心跳时必须刷新完整树，不得仅追加当前层。

### Orchestrator 运行快照钩子

`tools/task19_agent_runtime.py` 是 Root 调度事件的必须钩子：

- `sync FILE`：用 Agent API 列表生成的 JSON 数组/对象原子替换完整 Agent 树。
- `upsert NAME STATUS CURRENT_WORK`：在创建、开始、等待、完成、中断、失败或人工门禁变化后更新单 Agent，保留其他已登记 Agent。
- `heartbeat`：在 Root 每次调度循环、用户交互和长命令完成后刷新 Root 心跳。
- `confirm-open NAME REASON`：Root/Agent 发起任何平台权限或真实人工门禁前必须先写入；监控器立即显示红色 `confirm=YES` 和原因。
- `confirm-close NAME`：权限/门禁获批、拒绝、取消或超时后必须在处理结果前立即清除；若请求仍挂起则不得清除。
- 写入使用同目录临时文件、`fsync` 和 `os.replace`；写前验证 schema、Agent 名唯一、状态枚举、ISO-8601 时间、WAITING 原因和人工确认原因。
- 仓库工具不能自主访问 Codex Agent API；因此 Root 必须在 Agent 调度工具返回后立即执行上述钩子。
- 平台授权弹窗不会自动写入仓库；所以权限请求的强制顺序是 `confirm-open -> 发起平台请求 -> confirm-close -> 处理结果`。
- Agent 快照超过 60 秒时，监控器保留 Orchestrator 最后明确登记的状态，另行显示 `HEARTBEAT STALE`；心跳新鲜度不得覆盖 Agent 状态。独立终端无法直接访问 Codex Agent API，因此也不得把旧快照声称为实时 API 状态。
- 交互 TTY 用 ANSI 颜色标识状态：需要人工确认为红色（最高优先级），运行中为蓝色，已完成为绿色，等待中 `WAITING` 为黄色，尚未启动 `NOT_STARTED` 为白色；中断为红色，心跳过期作为独立红色警告。非 TTY、`--json` 和 `NO_COLOR` 环境禁用颜色。
- Agent `WAITING` 表示 Agent 已创建，但正在等待依赖、任务、资源或 Orchestrator 继续调度；必须在 `current_work` 说明等待对象，不得与 `NOT_STARTED` 混用。

### 多工作区数据源选择（2026-08-01 修订）

- 监控器不得固定读取启动目录的 tracker。默认通过 `git worktree list --porcelain` 枚举可读工作区，只接受同时存在 Task 19 tracker、wave plan 且 tracker 可解析为 96 个唯一单元的候选。
- 自动选择顺序为：`AUDITED` 单元数、96 单元平均 evidence-gate progress、tracker 最新时间、文件修改时间；完全相同时优先 `task19/*integration*` 分支。用户可用 `--workspace PATH` 明确覆盖。
- 输出必须显示所选 workspace、branch、HEAD、tracker/runtime 文件路径，并列出其他有效候选及其 audited/progress，避免把主工作区旧 tracker 误称为当前状态。
- Agent runtime 默认从所选 workspace 读取；若不存在，可回退到所有有效工作区中 `updated_at` 最新的快照，但必须显示来源与 `runtime_fallback=true`。
- runtime 快照早于所选 tracker 或超过 60 秒时，监控器必须显示 source-lag 警告；旧 `RUNNING` 只能显示为 `STALE`，不得冒充实时 Agent 状态。该规则不改变原始快照文件。
- `--json` 必须暴露数据源元数据、候选摘要和 lag 标志，供自动测试与外部监控验证。

`task19_monitor.py` 实现授权为 `true`；可写的 `task19_progress.py apply-delta` 仍不在本次授权范围。
