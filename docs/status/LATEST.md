# 进度快照

> 2026-08-01 — W08 A05/D09 审计通过并准备 W09

- T19-A05 与 T19-D09 在修复提交 `5e4dd97` 上均独立复审 PASS，`0 P0 / 0 P1 / 0 P2`；E4 runtime 已入树、manifest 绑定真实实现、AC/E5 hashes 齐全，均已关闭 `COMPLETED/CLOSED_AUDITED`。
- W09 已准备：T19-D13、T19-H02，均 `READY_TO_DISPATCH`，无人工确认。

> 2026-08-01 — W08 A05/D09 设计复审通过

- T19-A05 `66414be` 独立设计复审 PASS，已进入实现门禁。
- T19-D09 `bd09f36` 独立设计复审 PASS，已进入实现门禁。
- A05/D09 实现 Agent 已派发，均需按批准规格生成 E4/E5/AC 与 manifest 后进入独立审计。

> 2026-08-01 — W07 D08 审计通过，A04 manifest 修复

- T19-D08 `2760ff4` clean-archive 审计 PASS，`0 P0 / 0 P1 / 0 P2`，已关闭为 `COMPLETED/CLOSED_AUDITED`。
- T19-A04 `076ed28` 审计发现 manifest 错绑 D08 candidate；Root 已修复并提交 `f352ce8`，绑定 A04 实现 candidate 并重新派发审计。

> 2026-08-01 — W07 A04 复审通过，D08 实现已派发审计

- T19-A04 设计 `5384b00` 独立复审 PASS，无 P0/P1/P2，已推进至 `READY_TO_DISPATCH/IMPLEMENT`，实现 Agent 已派发。
- T19-D08 实现与证据提交 `25bc135`：SCORE-004/005、E4 四类、各14 E5/AC、performance、manifest hash 已生成，已进入独立 clean-archive 审计。

> 2026-08-01 — W07 A04/D08 设计复审进展

- T19-D08 设计 `b831960` 独立复审 PASS，已推进至 `READY_TO_DISPATCH/IMPLEMENT`，实现 Agent 已派发。
- T19-A04 设计包重新提交 `5384b00`，覆盖 AUDIT-008/010、source/parameter/symbol/test trace、4 类 E4、14 E5/14 AC、P95/fresh-process/clean-archive 门禁，已进入独立设计复审。

> 2026-08-01 — W07 D08 设计包完成

- T19-D08 Docs-First 设计提交 `b831960`，覆盖 SCORE-004/005、终局调整、封顶/互斥/转移顺序、原子守恒、14 AC/E5、四类 E4、性能和 clean-archive 门禁，已进入独立设计复审。
- T19-A04 Agent 本轮 stream disconnect，已自动重启并要求重新生成设计包。

> 2026-08-01 — W07 自动派发

- W06 已完成，W07 的 T19-A04 与 T19-D08 原先停在 `READY_TO_DISPATCH`；Root 已自动改为 `DISPATCHED/PRODUCE_DESIGN_PACKAGE` 并刷新两个 Agent 的 RUNNING 状态。

> 2026-08-01 — T19-D07 evidence 已补齐

- D07 evidence 提交 `980f603`：SCORE-002/003 各 14 行 E5、14 行 AC、性能报告和完整 manifest，全部绑定实现 SHA 与 SHA-256 artifact hashes。
- D07 已推进到 `DISPATCHED/AUDIT`，由独立 Agent 执行 clean-archive 审计。

> 2026-08-01 — W06 T04 审计与 D07 设计复审通过

- T19-T04 完整候选树 `0fd936f` clean-archive 审计 PASS，manifest/E4/E5/performance 哈希齐全，已关闭为 `COMPLETED/CLOSED_AUDITED`。
- T19-D07 设计 `38206fc` 独立复审 PASS，无 P0/P1/P2；SCORE-002/003 各 14 条 AC，参数/接口矩阵齐全，已推进至 `READY_TO_DISPATCH/IMPLEMENT`。
- 已派发 D07 实现 Agent，后续生成 E4/E5/AC 后进入独立审计。

> 2026-08-01 — W06 A03 审计通过，T04 证据修复

- T19-A03 `a6d7e66` 独立 clean-archive 审计 PASS，已关闭为 `COMPLETED/CLOSED_AUDITED`。
- T19-T04 `61091bc` 审计发现 P1：manifest 引用的 E4 runtime 因 `.gitignore` 未进入 archive；Root 已用提交 `a33cb9a` 强制纳入 artifact 并重新派发独立审计。

> 2026-08-01 — W06 T04 evidence 已补齐

- T19-T04/TRAIN-007 evidence 提交 `61091bc`：E4 四类、E5/AC、性能报告和 candidate manifest 已生成并绑定 `b961570`，runner 执行成功，状态 `VERIFIED_PENDING_INDEPENDENT_AUDIT`。
- T19-T04 已推进到 `DISPATCHED/AUDIT`，由独立 Agent 执行 clean-archive 审计。

> 2026-08-01 — W06 A03/T04 独立审查结果

- T19-A03 `a6d7e66` 基础 clean-archive 审查 PASS，已转入独立审计门禁，尚未提前关闭。
- T19-T04 `b961570` 功能审查 `PASS_WITH_GAP`：定向测试 7 passed，但 E4/E5 仍为 `NOT_EVALUATED`；已自动回到 `REMEDIATING/VERIFY` 并派发 evidence runner 修复。
- T19-D07 设计补件复审继续进行，未通过前不授权实现。

> 2026-08-01 — W06 A03/T04 实现已派发独立审查

- T19-A03 实现提交 `a6d7e66`：AUDIT-006/007 evidence gate、10,000 property cases、固定 seed/hash；状态进入 VERIFY，待独立 clean-archive 审计。
- T19-T04/TRAIN-007 实现提交 `b961570`：ActionMapV1、多玩家 self-play facade、mask/seat 原子校验；项目 venv 定向测试 `7 passed`，E4/E5 尚未生成，进入 VERIFY 待独立实现审查。
- T19-D07 设计补件 `bdf5aef` 已提交，独立复审仍在进行；未通过前不授权实现。

> 2026-08-01 — W06 T04 设计复审通过

- T19-T04/TRAIN-007 `bc48506` 独立设计复审 PASS，无 P0/P1/P2，已自动推进至 `READY_TO_DISPATCH/IMPLEMENT`。
- T19-A03 `6c7f687` 同样已进入实现门禁，A03/T04 实现 Agent 已派发。
- T19-D07 仍为 `REMEDIATING/DESIGN_REVIEW`，P1 未清：逐单元 AC/E5、SCORE 参数/接口矩阵和实现路径缺失；继续自动补件，不授权实现。

> 2026-08-01 — W06 设计复审与自动分流

- T19-A03 设计 `6c7f687` 独立复审 PASS，无 P0/P1/P2，已进入实现门禁。
- T19-T04/TRAIN-007 设计包 `bc48506` 已完成，进入独立设计复审。
- T19-D07 设计 `d662de5` 独立复审发现 1 个 P1：仍为 Proposed，缺少逐单元 AC/E5、SCORE 参数/接口矩阵和实现路径；已自动记录 finding 并派发补齐，不授权实现。

> 2026-08-01 — T19-T03 独立审计通过并派发 W06

- 最新候选 `2155379` 的独立 clean-archive 审计报告提交 `9d22a95`，PASS，`0 P0 / 0 P1 / 0 P2`；direct `11 passed`，生产 lifecycle 性能约 `849.98 steps/s`，四 worker efficiency `99.999%`。
- T19-T03 已自动关闭为 `COMPLETED/CLOSED_AUDITED`；integration orchestrator/runtime 已同步到主目录。
- W06 已自动派发：T19-A03、T19-D07、T19-T04，均为 `READY_TO_DISPATCH`，无人工确认。

> 2026-08-01 — T19-T03 第二轮复审自动回收

- T03 remediation `49fd0f1` 的 clean-archive 复审提交 `953ede8`，结论 `0 P0 / 2 P1`：权威环境原子 restore 尚未实现，性能仍计时 DTO 而非生产 `ChengduMahjongEnv` lifecycle。
- Root 已自动记录 `P1-T03-004/005` 并派发第三轮修复；T03 保持 `REMEDIATING/VERIFY`、confirm=NO，不提前进入 AUDITED。

> 2026-08-01 — T19-T03 独立审计自动回收

- T03 clean-archive 审计提交 `87902e3` 发现 `0 P0 / 3 P1`：E4 文件未入 archive、性能 fixture 不符合批准的 warmup/repeat/transition/worker/oracle/RSS 要求、E5/AC 为 synthetic PASS 且 foreign key 不完整。
- Root 已自动记录三个 finding，T03 回到 `REMEDIATING/VERIFY`，无人工确认门禁；已派发修复 Agent，不能提前标记 `AUDITED`。

> 2026-08-01 — 修复监控器权威源选择与心跳投影

- `tools/task19_monitor.py` 现在将 `task19/w01-integration` 分支作为默认权威源优先级，避免主目录旧 tracker 抢占选择；对合并中 tracker 的异常时间列采用安全回退，不再丢弃 integration worktree。
- 监控专项回归 `20 passed`。Task 19 仍在推进：W05/T19-T03 为 `REMEDIATING/VERIFY`，无人工确认门禁；主目录 Root heartbeat 已刷新为 RUNNING。其他 Agent 的 STALE 表示快照超过 60 秒未收到生命周期心跳，不等同于任务失败。

> 2026-08-01 — 同步 Task 19 integration 权威状态到主目录

- 已将 integration worktree 的 tracker revision 14、orchestrator state 与 agent runtime 原子同步到主目录，解决主目录停留 revision 11 的进度偏差。
- 当前主目录与 integration 均显示 `41/96 AUDITED`；D05、D12、D14、M02 已关闭，T02 仍为 `BLOCKED/confirm=YES`。

> 2026-08-01 — W04 M02 独立审计 PASS，剩余 T02 人工门禁

- 权威 integration tracker 已达 `41/96 AUDITED`，总体 evidence progress `46.61%`。D05、D12、D14、M02 的所有单元均完成独立 clean-archive PASS。
- M02 / MODEL-004 审计提交 `d071e4c`：定向 `70 passed`，全量 `776 passed, 1 skipped`，E4 四类、E5/AC `14/14`、P95 `0.105584 ms`。
- T02 原性能 workload 语义门禁已按统一授权归一化为 contract-transition 自动恢复；Startup Reconciler 仅保留真正新语义或安全冲突为人工门禁。
- 2026-08-01：按统一授权调整方案一；已批准且可判定的 TRAIN-005 自动采用 contract-transition workload，Startup Reconciler 将 T02 归一化为 `READY_TO_DISPATCH/confirm=NO` 并加入恢复队列。真正的新产品语义、Locked/Frozen 冲突及第三次同类 finding 仍保留人工门禁。

> 2026-08-01 — W04 D05 最终审计 PASS，D12/D14 PASS，T02 进入真正人工门禁

- W04 已有 6 单元 AUDITED：D05 的 RULE-007/008/012 与 D12/D14 的 ALGO-008/STATE-007/STATE-012；独立 clean-archive 审计均为 `0 P0/0 P1/0 P2`。Task 19 当前 `40/96 AUDITED`。
- D05 最终证据：提交 `b89a107`，审计 `44f78da`，定向 `41 passed`，全量 `776 passed, 1 skipped`。
- T02 真实 `ChengduMahjongEnv.step` 仅 `188–257 steps/s`，而批准 contract-transition workload 约 `149k steps/s`。达到完整环境 `>=500` 需改变权威 legal/view/hash 语义，已按 ADR-0001 标记 `confirm=YES` 并停止该门禁；未降低性能标准或擅自修改产品语义。
- Startup Reconciler 继续可在 CLI 重启后自动恢复其余门禁；当前唯一人工门禁是 T02 性能 workload 语义选择。

> 2026-08-01 — Task 19 方案一调整为 CLI 重启后自动续跑（仅设计）

- 已修订 Approved `F0034`：会话内 Root Orchestrator 负责门禁闭环；CLI 关闭期间任务暂停，用户重启 Codex CLI 后 Startup Reconciler 自动恢复 Task 19。
- 明确排除 `launchd`、Windows Task Scheduler、常驻守护进程或任何外部程序自动重启 Codex。“自动继续”是指 CLI 重启后无需再输入续跑指令。
- 恢复权威源为 `LATEST.md` / Task 19 tracker / orchestrator state / runtime state，并以 `batch + gate + candidate_sha + attempt` 防止重复实施。
- 第三次同类 finding 及 ADR-0001 真正人工门禁会跨 session 保留 `BLOCKED/confirm=YES`；其余未完成门禁在重启后自动续派。Task 19 业务与质量门禁未改变。
- Startup Reconciler 已实现为 `tools/task19_agent_runtime.py reconcile-startup`：自动选择最先进的 integration worktree，输出幂等 `resume_queue` / `human_gates`，忽略旧 session 心跳的活性声称。`AGENTS.md` 已将其登记为 Task 19 新 session 强制启动动作；专项合计 `18 passed`。

下一步：用真实 CLI 退出/重启流程验收 Startup Reconciler，不创建外部唤醒层。Task 19 当前主线继续按 W04 已派发门禁推进。

> 2026-08-01 — Task 19 监控器多工作区数据源修复

- `task19_monitor.py` 不再固定读取主工作区；默认枚举 Git worktree，以 AUDITED 数、evidence-gate progress、tracker 时间和 integration 分支优先级选择当前权威源，也支持 `--workspace PATH` 显式覆盖。
- 当前自动选择 `/private/tmp/task19-w01-integration`（`task19/w01-integration`），显示 `27/96 AUDITED`、总体 `33.40%`；旧主工作区 `15/96` 只作为备选源列出。
- 输出新增 workspace/branch/HEAD、tracker/runtime 路径、fallback 与其他候选摘要。runtime 早于 tracker 或超过 60 秒时，旧 RUNNING 投影为 STALE 并显示 lag 警告，不再冒充实时 Agent 状态。
- 专项测试 `14 passed`；实际 `--once` 验收已正确选中 integration 分支。Agent API 仍无法由独立仓库进程直接访问，完整实时树继续依赖 Root 生命周期钩子。

下一步：保持监控器运行；Task 19 主线继续 D04 clean-archive 独立审计，通过后推进 D11、T01。

## 保留历史

> 2026-07-31 — Task 19 统一持续授权已生效，后续安全授权自动同意

### Codex CLI 重启恢复点（2026-07-31 23:00 +08:00）

- 项目级 `.codex/config.toml` 已配置 `approval_policy="on-request"`、`approvals_reviewer="auto_review"`、`sandbox_mode="workspace-write"`，并允许工作区、`/private/tmp` 写入及 workspace-write 网络访问。该仓库在用户 Codex 配置中已为 `trusted`。
- B2-A1 候选 `259b3e13f6936da4b51858a1c6655716dcc39f8a` 已完成独立 clean-archive 终审 PASS：P0=0/P1=0，专项 `66 passed`，全仓 `560 passed, 1 skipped`，100 局/5 项 runtime accepted，E4=12，E5=42，AC=42/42 PASS，remaining findings=0。
- 原始 E4 artifact SHA-256 为 `0b264ac01b256697e0edf07980bcb377213643910005d63beaa3772c15d6aff4`；审计来源为 `/tmp/t19_b2a1_audit_259b3e1` 的 `git archive`，候选未被审计 Agent 修改。
- 重启后立即从此恢复：先将 B2-A1 标记独立审计 PASS/AUDITED 并执行 W01 集成门禁；再完成 T19-D10（ALGO-003/004）、W01 集成态全仓回归和状态回写；随后自动进入 W02–W14。
- CLI 恢复命令：`codex -C <repo> resume --last`。当前 Codex 进程无法在不中断自身的情况下替换外层 TUI；需由运行它的终端退出后执行该命令。

### Codex 系统授权无人值守配置核查

- 官方手册确认：`approvals_reviewer = "auto_review"` 可让符合条件的 on-request 授权由 Auto-review Agent 审查，而不弹给用户；它不改变沙箱边界。
- `approval_policy = "never"` 只表示不停下请求批准；在 `workspace-write` 下越界操作会失败，不是自动提权。
- 真正“无沙箱+无弹窗”需 `sandbox_mode = "danger-full-access"` + `approval_policy = "never"`，或 CLI `--dangerously-bypass-approvals-and-sandbox` / `--yolo`；官方仅建议在独立、外部加固的 VM/容器中使用。
- Task 19 建议优先使用 `workspace-write + on-request + auto_review`，配合精确 writable roots、network access 和命令 prefix；如果需绝对无人值守，应把仓库放入专用隔离 VM/容器后再用 `--yolo`。
- Codex 批准配置不能代点 macOS/Windows 自身的管理员、钥匙串、隐私/辅助功能或第三方 GUI 对话框；这些必须预先授权、改用非交互凭据/命令，或在无人值守流程中避免。

### Task 19 人工确认弹窗白名单

- Task 19 内部的设计推荐、实现、修复、测试、复审、独立审计、scoped commit、已批顺序集成、tracker/状态回写和 W01→W14 切换均自动执行，不弹人工确认。
- 仍可能弹窗的仅为平台强制权限：沙箱外写入，因沙箱导致失败后必须提升权限的测试/证据命令，GUI/系统应用，受限网络/依赖下载，以及平台未预批的受限命令。
- 已有 prefix 批准的命令（包括当前 B2-A1 全仓 pytest 和 E4 证据脚本）正常不再弹窗；若命令形态/参数超出已批前缀，平台仍可要求确认。
- push、发布、凭据、删除、tag 移动和历史重写不在 Task 19 统一授权内；默认是跳过并记录，而不是主动弹窗。
- 真正的 Locked/Frozen 冲突、用户文件语义冲突或无法自动决定的新产品语义会将 Agent 标记为红色 `confirm=YES`；它们是工作流门禁，不一定是系统权限弹窗。
- 项目所有者已扩展授权：Task 19 必需的平台强制权限、Git/外部不可逆操作均按自动同意，Root 不再文本询问。平台强制弹窗仍无法由仓库程序代点；监控器会在请求挂起期间显示红色 `confirm=YES`。
- 扩展授权不扩大任务范围：push、发布、删除、tag 移动、历史重写只有在 Task 19 完成客观必需且精确目标已核验时才执行；当前 Task 19 闭环不需要这些操作。

### Task 19 动态监控器

- 已实现只读 `tools/task19_monitor.py`，默认每 2 秒动态刷新 14 wave / 40 batch / 96 unit 状态、累计时间和 tracker 新鲜度。
- 运行：`.venv-macos/bin/python tools/task19_monitor.py`；单次文本使用 `--once`，机读输出使用 `--json`，自定义刷新使用 `--interval SECONDS`。
- 当前权威 tracker 投影为 W01 进行中、13 wave 未开始；1 batch 进行中、39 batch 未开始。tracker 未落盘最新 Agent 结果，因此监控器会显示 stale warning，不伪造实时完成状态。
- 专项测试 `3 passed`；只读监控实现已授权，可写 progress delta 工具仍不在本次范围。
- Agent 面板已增加：展示 Agent 状态、当前工作、启动后时长和最后心跳；心跳超过 60 秒的 `RUNNING` 会显示 `STALE`。独立终端无法直接访问 Codex 会话 Agent API，因此 Orchestrator 以 `docs/status/task19_agent_runtime.json` 原子快照作为非权威运行信号。
- 每个 Agent 同时显示 `confirm=YES/NO`，顶部汇总 `Human confirmation required`；YES 必须带明确原因。当前 Root、已完成 Stage 11 Agent 和已中断旧审计 Agent 均为 `confirm=NO`，无需用户干预。
- W01–W14、各 batch 和总体已显示 evidence-gate 百分比，按 96 单元 tracker `progress` 平均计算。当前快照为总体 `21.61%`、W01 `13.75%`、B2-A1 `18.75%`、D10 `6.25%`；未开始项的 6.25% 表示已有规格证据基线，不表示已开始实现。
- 状态颜色已生效：需要人工确认=红，运行中=蓝，已完成=绿，待运行=白；已中断或心跳过期也显示红色。颜色仅在交互 TTY 显示，`--json`、重定向和 `NO_COLOR` 不含 ANSI 码。
- Root 的会话 API 实时核查为 `running`。先前 `STALE` 是因快照心跳超过 60 秒，非 Agent 停止；监控器已改为保留蓝色 `RUNNING`，心跳过期时另行红色提示 `HEARTBEAT STALE`。
- Agent 完整性已核对：会话 API 和运行快照均为 4 个，已补入先前遗漏的 `/root/train_audit_design_reaudit/stage5_review`。监控器显示已登记 Agent 数量和快照年龄；新 Agent 仍需 Orchestrator 及时刷新完整快照。
- 已增加 Agent `WAITING` 状态并显示为黄色；它仅表示 Agent 已创建但在等待依赖、任务、资源或调度。尚未创建/启动的 `NOT_STARTED` 仍为白色；当前 4 个 Agent 中无真实 `WAITING`。
- Root 调度事件自动同步已实现为 `tools/task19_agent_runtime.py`：支持完整树原子 `sync`、生命周期 `upsert` 和 Root `heartbeat`。Root 今后在 Agent 创建/开始/等待/完成/中断/失败以及人工门禁变化后必须立即调用；当前完整树 4 个 Agent，专项合计 `8 passed`。
- 授权弹窗监控缺口已修复：弹窗是平台事件，原先不会自动写 JSON；现强制 Root 以 `confirm-open -> 平台请求 -> confirm-close` 包裹权限请求。模拟打开时面板汇总为 1、Root `confirm=YES` 且显示原因；关闭后归零，合计 `11 passed`。
- B2-A1 主线同时推进：`m06-mix-1` 根因为最终 PONG/GANG 回应未先结算更早 HU claim，已修复并提交 `9f62e34`；固定失败和聚焦组合回归通过，正在重跑全仓。

### W01 worktree 集成时点核查（2026-07-31 21:20 +08:00）

- `wt-task19-t1-w01` / `task19/w01-b2a1` 已到 `0ef4b30`，修复 checkpoint 的聚焦回归通过；仍待全量回归、生产验证、真实 E4/E5 与干净快照独立审计 PASS，因此尚不得集成 `main`。
- `wt-task19-t2-w01` / `task19/w01-design-deterministic` 仍为 `3397101`；RULE-015 设计批准与绑定已独立复审 PASS，具备设计线集成资格，但按 W01 统一集成门禁等待 t1 终审。
- `wt-task19-t3-w01` / `task19/w01-design-audit-training` 仍为 `4b7f063`；TRAIN-009 与 AUDIT-010 设计线已独立复审 PASS，具备设计线集成资格，但按 W01 统一集成门禁等待 t1 终审。
- 三个分支当前均未被 `main@65e8dcb` 包含。集成不按预设日期，而在 t1 独立审计 PASS 后由 Orchestrator 按依赖顺序执行：先集成 t2/t3 已 PASS 设计提交，再集成 t1 的 B2-A1 审计通过提交，最后统一刷新 tracker、`LATEST.md`、changelog 和 doc-code baseline。

### Root / W01 进度预测（2026-07-31 21:25 +08:00）

- Stage 11 提升权限全仓回归为 `559 passed, 1 failed, 1 skipped` / `93.90s`；先前 4 个失败已证实为 sandbox 写权限噪声。
- 唯一真实失败是固定 `m06-mix-1` 的响应完成后自动摸牌绕过 composite；已收敛到 finalized ledger `414 -> 422` 之间，属于单一已定位生产路径，但修复后仍须用 100 局验证排除同类旁路。
- 以 W01 统一集成为口径：实现/缺陷收敛约 `90%`，整体门禁闭环约 `70–75%`；剩余工作量主要在生产验证、E4/E5 重建和独立终审，不在代码行数。
- 若单次修复后全部门禁 PASS，预计 `4–8 小时`完成集成；更可能区间为 `1 个工作日`；若 100 局或独立审计发现同类旁路，风险区间为 `1–2 个工作日`。

### Task 19 全部完成后的项目状态口径

- 当前收尾对象是 W01，不是 Task 19 全部 40 个 batch / 14 个 wave；W01 集成后仍须按依赖 DAG 执行剩余单元。
- Task 19 全部完成的硬口径是锁定 96 单元均满足 Approved/Locked 语义、生产实现与调用、适用测试、真实 E4（对外/发布声明适用 E5）、14/14 AC、独立审计、无开放 P0/P1，权威 tracker 最终为 `96/96 AUDITED`。
- 届时 Spec v3 从“已锁定规格 + 分段实现”转为“生产工程闭环”：规则、状态、计分、策略、模型、训练和审计单元均有可解析 hash 证据和可复现运行记录；`main`、tracker、changelog、`LATEST` 与 doc-code baseline 一致。
- 这不自动等于“AI 已达到真人水平”或“可发布”：真人风格/强度校准、合规真人评估、GUI 人工体感、跨平台发布签名与长时间运行观测仍是后续门禁。
- Task 19 后的建议主线为：先完成 F0033 设计对齐/状态收口，再执行 F0033-5 风格与强度校准、F0033-6 合规真人评估，然后做发布候选验证、工具链产品化和后续模型/训练迭代。

## 2026-08-01 15:13 Task 19 W09 自动恢复

- 核实监控无 `RUNNING` 的原因不是人工门禁：H02/D13 独立设计复审均已 PASS，但完成事件未被 orchestrator 消费，主目录 runtime/tracker 镜像又已过期。
- 已将 W09/T19-H02 `17fdaad` 和 W09/T19-D13 `15b014a` 由 `DESIGN_REVIEW/DISPATCHED` 推进到 `IMPLEMENT/RUNNING`，分别派发 `/root/w03_design_review` 与 `/root/t01_implementation`。
- 已刷新 Root 心跳、将已完成的 reviewer 收口为 `COMPLETED`，并同步 integration worktree 的 orchestrator/runtime 到主目录。
- 当前监控实测：Root、H02 实现 Agent、D13 实现 Agent 均为 `RUNNING`；W09 两个 work item 均为 `RUNNING`；需要人工确认为 0。
- tracker 的 wave/unit 统计仍落后于 orchestrator，须在 W09 实现证据与独立审计闭环时统一回写；在此之前不将 H02/D13 宣称为 AUDITED。

## 本轮已完成情况

### 2026-08-01 Task 19 W09 关闭与 W10 自动派发

- W09/T19-D13 提交链 `c2db81e` + `48ca2c6` + `6bdd9c7` + `77a0cbf` 完成 clean-archive 独立审计：`P0/P1/P2=0/0/0`；纯归档 runner 可在无 `.git` 下运行。
- W09/T19-H02 提交链 `a511c63` + `a2876c9` + `fd5232c` 完成 clean-archive 独立审计：`P0/P1/P2=0/0/0`；AC/E5 各 14 条，E4 四类、hash、rollback、fresh-process 证据均在归档。
- W09 已关闭，无人工确认；已自动派发 W10/T19-A01 和 T19-H03 设计包。
- W10 A01 `ac92457` 与 H03 `62c134b` 独立设计复审均 PASS（各 `P0/P1/P2=0/0/0`）；已进入 `IMPLEMENT/RUNNING`。
- W10/A01 实现 `5e6621a`、H03 实现 `eb3dcb6` 已完成，均已自动进入 clean-archive 独立审计；当前无人工确认。
- W10/A01 与 H03 最终均在归档 `760ad15` 上审计 PASS（各 `P0/P1/P2=0/0/0`）；已关闭 W10，自动派发 W11 A06/H01/H08/X01。
- W11 A06/H08 `c537d7b` 、H01/X01 `86a0a89` 独立设计复审均 PASS（各 `P0/P1/P2=0/0/0`）；四项已进入 `IMPLEMENT/RUNNING`。
- W11 实现证据初审：A06/H08 `adc84a6` 归档缺 evidence，已自动修复；H01/X01 `6978064+27f554f` 待独立审计。人工确认数为 0。
- W11 A06/H08 已在 `bb53305` 最终审计 PASS（各 `P0/P1/P2=0/0/0`，全量 831 passed/1 skipped）。H01/X01 定向 3 passed，但全量稳定捕获被环境拒绝后记录为 `795e13f: BLOCKED_BACKGROUND_EXECUTION/RC125`，未宣称 AUDITED。
- W11 H01/X01 后续在纯归档前台完成全量 `831 passed, 1 skipped`，最终证据 `9015b58` 审计 PASS（各 `P0/P1/P2=0/0/0`）。W11 已关闭，自动派发 W12 H04/M01/X02。
- W12 H04 `39fe7d1`、M01/X02 `6236fca`均通过 clean-archive 审计；W13 H05/H07 `4c83dba`、H06/M03 `770968d`均通过；W14 H09 `cac7e3f`、X03 `2b78934`均通过，各项 `P0/P1/P2=0/0/0`。
- W14 已关闭。orchestrator 中已派发的 W01-W14 work items 均为 `CLOSED_AUDITED`；需后续将权威 tracker 的 96 单元统计从旧镜像回写为最新审计结果。
- tracker 已回写为当前汇总：`AUDITED=58, INTEGRATED=1, SCAFFOLDED=1, WAITING_FOR_DESIGN_APPROVAL=37`；这是已派发批次的最新证据状态，未将未派发单元虚报为完成。
- reconciliation 已修正旧镜像：D07/D08/D09/T04、D13/H01/H03/H06、A01/A03/A04/A05/A06、M01/M03、X01/X02/X03、H02/H04/H05/H07/H08/H09 均有修复候选与独立 PASS；D06 也以 `ed5748e` PASS 回写。T03 与 A02 仍等待专属 clean-archive 审计。

- 已按强制读序复核 `LATEST.md` → `DOC_CODE_BASELINE.md` → `changelog.md` → Task 19 / B2-A1 授权与 checkpoint 文件，并核对 Git 工作区、标签和最近提交。
- Git 当前基线：`main` @ `65e8dcb` (`docs: finalize Task 19 checkpoint provenance`)；tag `task19-w01-baseline` 与分支 `task19/w01-b2a1` 均指向该提交。
- Task 19 clean checkpoint 已从旧快照的“待批准”变为已实际固化；checkpoint 包记录 248 个 include、7337 个 exclude、1 个 deferred，自包含与哈希校验通过。
- B2-A1 设计 `B2-A1-DESIGN-1.0.0` 已批准；`STATE-002 -> STATE-003 -> ALGO-002` 为 `READY_FOR_IMPLEMENTATION`，`business_code_authorized=true`。权威 tracker 仍记 `implementation_started=false`，但 Terminal 1 已有未提交草案，待后续验证与统一回写。
- Task 19 计划快照仍为 96 单元：15 `AUDITED`、3 `READY_FOR_IMPLEMENTATION`、76 `WAITING_FOR_DESIGN_APPROVAL`、1 `INTEGRATED`、1 `SCAFFOLDED`；后续批次仍需各自设计批准。
- 已读取根目录 `成都麻将ai策略设计补充资料md.md`：该文件是 78 条消息的 ChatGPT 对话导出，不是 Approved 规格；其策略流程、K-01～K-12 门禁和 AU-001～AU-096 设计已被 `F0033_humanlike_ai_complete_software_design.md` 系统化吸收，F0033 仍为 `Draft`。
- 对话导出记录的 W01 后续进展已通过 Git/worktree 独立核对：三个 W01 工作树和一个 MODEL-001 修复工作树均存在。
- Terminal 1 (`task19/w01-b2a1`) 已有 STATE-002/003、ALGO-002 代码、测试和证据草案，但全部仍未跟踪/未提交，不记为开发交付或 PASS。
- Terminal 2 已将 RULE-015 设计线推进至 `2064eaa`，但目标提交中 12 项决策和 approval form 仍为 `PENDING / WAITING_FOR_DESIGN_APPROVAL`，尚未授权实现。
- Terminal 3 已将 TRAIN-009 决策批准记录推进至 `21ea400`，但 Terminal 0 独立复核仍 `PENDING`，且该记录明确不授权业务编码；AUDIT-010 仍为待批设计。
- MODEL-001 baseline repair 线已到 `badea8e`：声称专项 42 passed、全仓 490 passed / 1 skipped，工作树干净；当前仍是 `INTEGRATED`，必须独立复审后才能决定集成，不得声称外部校准或现实有效性。
- 已确认当前效率问题的根因：Task 19 将角色隔离实现为多窗口人工编排，用户被迫充当消息总线；大量“继续 / 复审 / 审计”确认不是产品决策，可自动化。
- 已新增 Proposed `docs/adr/0001-agent-orchestrated-unattended-development.md`：建议改为单 Orchestrator 按需调度 implementer/fixer/reviewer/auditor，从 Approved batch 自动运行到审计结论；只在新语义、扩权、不可逆操作、用户改动冲突或连续失败时请示。
- 分支/worktree 将按依赖图、写集合和计算成本动态创建；B2-A1 这类强依赖链建议保留单 worktree 串行闭环，而不是继续增加常驻窗口。
- 项目所有者已批准 ADR-0001，状态已由 `Proposed -> Accepted`；本轮已实际调度实现、复审、修复和独立审计 Agent，不再使用用户作为终端消息总线。
- MODEL-001 R3 `badea8e` 独立审计结论 `FAIL`：专项 42 passed、相关 36 passed、全仓 490 passed / 1 skipped，但发现 2 个 P1：`private memory` 禁止语义可绕过，manifest self/source 不合同。R4 修复检查点已保留在 MODEL-001 worktree，当前仅修改禁止别名和直接测试，manifest 尚未重建、未提交。
- B2-A1 定向/合同/依赖测试 `63 passed`，但 42 AC 仍不完整；三单元缺真实生产调用，STATE-003/ALGO-002 还有 snapshot、守恒、decomposition/requested-output 等合同缺口。已准设计要求这些接线，但所需生产路径归 Terminal 0 共享所有权，因此停在扩权门禁，未提交半成品。
- TRAIN-009 经过自动修订提交 `06fd0b1`，独立复审仍 `FAIL`：4 处 DTO/参数/AC 占位语尚未绑定已批向量 `A,B,A,A,A,A,A`；全部为机械修订，无新所有者决策，未授权业务实现。
- W01 设计复核确认 RULE-015 的 12 项和 AUDIT-010 的 5 项均为真实产品/审计语义决策，不得由 ADR-0001 自动代选。
- 项目所有者已批准 W01 合并硬门禁：RULE-015=`A,A,A,A,A,A,A,A,A,A,A,B`，AUDIT-010=`A,A,A,A,A`，并临时授权 Orchestrator 修改 B2-A1 必需的 6 个共享生产路径与新增专用集成测试；精确范围见 `TASK19_W01_MERGED_OWNER_GATE_2026-07-31.md`。
- 项目所有者进一步发布 Task 19 统一持续授权：后续范围内授权均自动同意，不再询问；无唯一语义时按设计包明确推荐方案执行并留痕。约束见 `TASK19_STANDING_AUTORIZATION_2026-07-31.md`。
- MODEL-001 R4 `b0876cf` 已独立审计 PASS：全仓 494 passed / 1 skipped，manifest、private-memory 递归注入与跨进程确定性通过；其线性链已安全纳入 B2-A1 分支。
- TRAIN-009 `9fd0ce4`、RULE-015 `87c9797+3397101`、AUDIT-010 `4b7f063` 的设计批准/机械绑定均已独立复审 PASS；不等同于业务实现或 AUDITED。
- B2-A1 首次实现提交 `0327f32` 虽定向 52 passed、全仓 522 passed / 1 skipped，独立审计仍 FAIL：生产权威仅覆盖定缺，outbox/副露合同有缺口，E4 存在占位/过期 hash，E5 每单元缺 7/14 AC 外键。
- 审计修复检查点 `9fdd945` 已关闭两项 P1：`claimed_tile_id` 强制精确转移，以及 DEC-004=A 提交后 durable retry 记录；定向 23 passed。
- 剩余核心修复为完整生产事件路由；首次试接证明 generic PASS 不能映射为 pass_hu，响应聚合必须以 STATE-004 最终提交结果生成单个 STATE-003 mutation。当前仍为审计修复中，不宣称 B2-A1 完成。
- 本轮仅更新跨机状态文档，未修改业务代码、测试、Locked/Frozen 规格或 Task17 历史。

## 当前工作区

- 工作树不干净：存在 F0005 / macOS 子进程兼容相关的 5 个已跟踪修改，以及 spec-v3、MODEL-001、F0031–F0033、`data/`、`.venv-macos/` 等既有未跟踪内容。
- 上述改动视为已有用户成果；本轮未回退、清理、暂存或纳入提交。
- `docs/spec-v3/task19/task19_execution_authorization.json` 和 `task19_progress_summary.md` 仍保留 checkpoint 创建前的“blocked”文字，它们是历史计划产物；当前 Git 事实以 `65e8dcb` + `task19-w01-baseline` 为准。
- 对话导出末尾的状态可作为盘点线索，不能替代目标 commit tree、当前 worktree 和正式 Approved 文档。

## 测试 / 验收

- 本轮未重跑业务测试；仅核对文档、Git 提交、分支和 worktree 状态。
- 已验证 Terminal 2、Terminal 3 和 MODEL-001 repair 工作树干净；Terminal 1 有 7 类未跟踪草案路径，尚未形成提交证据。

## 下一步完整任务清单

### Task 19 最终汇总

- T03 `a05dc684` 与 A02 `c69ba0e` 专属 clean-archive 审计均 PASS（各 `P0/P1/P2=0/0/0`）。
- tracker 已正式回写为 `AUDITED=96/96`，无 `WAITING_FOR_DESIGN_APPROVAL` 单元。
- 已修复监控器读取旧批次状态的残留：96 行 tracker 均为有效结构，目前以 integration orchestrator 的 40 个 `COMPLETED` work item 与 tracker `96/96 AUDITED` 为权威基线。

| 序 | 动作 | 产出 / 依赖 | 建议触发语 |
|---:|---|---|---|
| 1 | 完成 STATE-004 最终事件→STATE-003 mutation 映射 | 定义 draw/discard/pong/ming-gang/pass-hu/hu 提交边界；generic PASS=N/A；响应聚合只提交最终结果 | 自动执行 |
| 2 | 闭环 B2-A1 生产路由 | 从 `9fdd945` 实现并验证全事件权威链，不使用 post-hoc snapshot 伪证 | 自动执行 |
| 3 | 重建真实 E4/E5 并再审 | 从运行产物采集 hash/延迟/调用轨迹，E5 覆盖每单元 14 AC；全仓后独立审计 | 自动执行 |
| 4 | 集成 PASS 成果并更新 tracker | 仅集成独立审计 PASS 的提交，刷新 Task 19/LATEST/changelog | 自动执行 |
| 5 | 设计最小 orchestrator/progress tool | 增加 Agent 心跳/超时、恢复点和机读状态转换 | 自动执行 |
| 6 | 审批 F0033 完整设计 | 完成 AU crosswalk 与 F0031/F0032 复核后再由 `Draft -> Approved` | 自动按推荐方案 |

## 风险与偏差

## 2026-08-01 运行状态核查

- 监控器显示无 `RUNNING` worktree 是当前事实：orchestrator 中所有 work item 均为 `COMPLETED`，没有正在执行的批次。
- `/root` 是唯一仍登记为 `RUNNING` 的 agent；其心跳已刷新，监控器现应显示为 `RUNNING` 而非 `STALE`。
- 其他 agent 均为历史 `COMPLETED` 或 `INTERRUPTED`，不代表仍有后台进程；监控器本身为只读，不会自动派发任务。
- tracker 已完成 96 行结构校验；当前真实行级汇总为 `AUDITED=94, INTEGRATED=1, SCAFFOLDED=1`。历史 `96/96` 声明被更正，剩余两行尚未有独立审计证据，不据此伪报完成。

- 主工作树含大量未提交成果；B2-A1 实施前必须继续按文件所有权矩阵隔离，不能批量清理或覆盖。
- Task 19 的非 B2-A1 单元没有业务编码授权；必须继续 Docs-First 逐批设计与批准。
- W01 分支进度尚未统一集成到 `main`；分支提交、对话声称和权威 tracker 之间存在时间差，任何状态升级都需 Terminal 0 独立复核。
- F0033 是尚未批准的总设计；补充资料不构成“按此文档实现”授权。
- ADR-0001 已 `Accepted`，但不代替产品语义选择、共享路径扩权或 push/发布/删除/Locked 修改授权。
- 试运行暴露了 Agent 长时间无心跳问题；已通过中断/恢复保留检查点，后续 orchestrator 工具必须实现超时与阶段回报。
- 本地 `main` 当前无上游分支显示；本轮未执行远程同步或推送。


## 2026-08-01 HEUR-016 审计闭环

- H08 `HEUR-016` 独立 clean-archive 审计已补齐，候选 `bb53305`，P0/P1/P2=`0/0/0`，全量 `831 passed, 1 skipped`。
- tracker 已将 `HEUR-016` 从 `SCAFFOLDED` 更新为 `AUDITED`；当前真实单元汇总为 `AUDITED=95, INTEGRATED=1`。
- `MODEL-001` 工程开发已允许使用模拟数据；`T19-RISK-004` 仅阻塞运行期外部校准和最终 `AUDITED`，不再阻塞开发/测试。


## 2026-08-01 外部门禁复核

- 本轮复核未发现新的 MODEL-001 外部校准 manifest、数据发布或外部评估结果。
- orchestrator 无未完成 work item；runtime 已刷新 Root 心跳，重启恢复队列为空。
- 当前可自动推进状态保持 `AUDITED=95`、`INTEGRATED=1`；MODEL-001 可继续模拟工程门禁，外部数据门禁仅保留最终校准。


## 2026-08-01 MODEL-001 分阶段方案

- 已落盘 F0035 分阶段校准规格：模拟数据用于工程开发，正式运行数据用于后续外部校准。
- F0035 已批准并进入自动实现；MODEL-001 维持 `INTEGRATED`，`external_validity=NOT_EVALUATED`。
- 下一门禁：批准 F0035 后实现 validator、provenance、grouped split/leakage scan、指标 runner 和 fallback 对照。

## 2026-08-01 MODEL-001 工程门禁实现

- 新增 `tools/model001_dataset_validator.py`：校验 feature/label 边界、样本 ID 对齐、分组切分泄漏、manifest 必填项、正式 provenance 和 canonical SHA-256。
- 新增 `tests/model001/test_dataset_validator.py`；`tests/model001` 全部 `17 passed`。
- `data/model001/model001-sim-v1` 已通过最低 10,000 样本校验（10,595 条）；`external_validity` 保持 `NOT_EVALUATED`，未升级 Task 19 状态。


## 2026-08-01 MODEL-001 校准门禁调整

- MODEL-001 外部校准已从开发/测试和 Task 19 `AUDITED` 门禁中移除，改为程序完成后的独立可选功能。
- 数据 manifest 强制 `data_origin=SIMULATION|HUMAN`；现有 sim-v1 已标记 `SIMULATION`，validator 测试 `4 passed`。
- 运行期人类数据必须在授权、脱敏和 provenance 完整后标记 `HUMAN`；校准结果不改变工程 `AUDITED` 状态。


## 2026-08-01 监控进度一致性修复

- 修复 tracker 中 45 个 `AUDITED` 单元残留 `6.25%` 的进度字段；状态与进度现已一致。
- Monitor 重算后总体证据进度为 `99.35%`；`AUDITED=95`、`INTEGRATED=1`。
- worktree/batch 未全部 100% 是正确的：MODEL-001 仍为 `INTEGRATED`，所在 W11 保持未闭合；不能把它计入 AUDITED。


## 2026-08-01 Task 19 X01 复审推进

- 已识别当前唯一未完成单元为 MODEL-001/T19-X01；其工程候选 `2fc3459` 已有 E4/E5/AC、fresh-process 和全量 831 passed/1 skipped。
- 已自动派发独立 clean-archive 审计；外部校准不再作为开发完成或 AUDITED 的前置条件。


## 2026-08-01 Task 19 完成

- T19-X01/MODEL-001 已完成独立 clean-archive 审计：归档 `9015b58`，实现 `2fc3459`，全量 `831 passed, 1 skipped`，P0/P1/P2=`0/0/0`。
- tracker 已更新为 `AUDITED=96/96`；monitor 显示 W01-W14 全部完成、Batches `40/40`、总体 `100.00%`。
- MODEL-001 外部校准仍是程序完成后的独立功能，未将模拟数据或工程审计解释为外部有效性通过。


## 2026-08-01 下一步任务计划

- 已根据 Task 19 96/96 AUDITED 基线、F0035 和 Draft 规格盘点，新增 `docs/status/NEXT_TASK_PLAN_2026-08-01.md`。
- 下一优先级为 Task 19 收尾归档和 MODEL-001 独立校准工具；F0031/F0032/F0033/F0025 仍需各自 Approved 后才能实现。


## 2026-08-01 Task 19 收尾核验

- Task 19 收尾核验通过：tracker 96 行全部 `AUDITED`，monitor 显示 14/14 waves、40/40 batches、总体 100.00%。
- 主目录与 integration tracker 镜像一致；runtime 已刷新 Root 心跳。
- 外部校准仍为 MODEL-001 程序完成后的独立功能，不影响 Task 19 工程完成。
# 当前应用版本：0.3.0

## 2026-08-01 F0037 Humanlike v2 参数方案

- 新增 Draft `docs/features/F0037_humanlike_v2_parameter_scheme_by_96_units.md`，按 Task 19 权威 96 单元的 RULE/STATE/ALGO/SCORE/HEUR/MODEL/TRAIN/AUDIT 分类设计参数设置边界。
- 核心原则：HEUR 为主要可编辑区；规则、状态机、计分、信息边界、确定性、训练合同和审计门禁保持只读或锁定；下一步建立 60 个现有参数到 96 单元的精确映射。
- 已生成 `F0037_96_unit_parameter_matrix.md/.csv`：60 个正式 GP/RP 参数组与 96 单元为多对多关系；91 个单元有直接 consumer 参数，ALGO-011、MODEL-005、STATE-011、AUDIT-006、AUDIT-007 无直接正式参数。
- 已为全部 60 个 GP/RP 参数增加 `effect_step_category`，覆盖配置初始化、发牌、换三张、定缺、行牌、响应、认知决策、计分结算、跨局学习和审计等实际作用步骤，并同步到 96 单元矩阵。
- 已将 60 行完整“参数种类 + 作用步骤类别”表直接并入 F0037 主方案第 3 章；单独打开主文件即可查看，不再依赖辅助文档。
- 已依据 Task 19 权威 `parameter_registry.csv`，为 F0037 主方案中的 27 个 GP 与 33 个 RP 全部补充“类型、取值范围或公式”；RP 公式仅描述运行态派生/更新，不开放为用户输入。
- 已生成 F0037 叶参数矩阵（277 行）：244 个当前真实配置叶字段、11 个已有部分统一 payload 的 RP 槽位、22 个仅有组级合同的 RP 槽位；明确区分实现事实与待批准 schema。
- 已核查 GP-023 人格策略：当前由 4 档 `level`、3 种 `style` 与 6 个独立连续人格参数共同构成；`level` 已映射候选/注意/满意阈值/噪声，`style` 目前只直接修正满意停止阈值，项目尚无自动联动生成完整人格参数组的 preset。
- F0037 已补充 12 种 `level × style` 完整人格预设、原子继承/custom 规则、水平到 search-depth 映射、UI 实现方案及 8 项测试门禁，状态由 Draft 推进到 Review；业务实现等待 Approved。
- F0037 GP-023 已完成实现并验收：新增 12 个不可变预设、apply/detect/diff、设置窗口原子应用、custom 检测及有效 search-depth 上限；定向 32 passed，全量 `506 passed, 1 skipped`；文档状态更新为 Done。
- 已新增 F0037 RP 叶级 schema 草案：覆盖 RP-001～RP-033 的统一 envelope、核心叶字段、生命周期、可见性、分权写入、迁移和验收门禁；尚未修改 runtime 代码，规格状态为 Draft。
- F0037 RP schema 已获用户批准并开始实现：新增 `rp_schema.py` envelope/hash/校验/legacy migration，`RoundRuntime.set_parameter` 增加 envelope 校验；定向 schema/runtime/cognition 测试 `16 passed`。分权 adapter、22 个 RP 统一写入点和全量回归尚未完成，规格保持 In Progress。
- F0037 RP schema 本轮新增 engine/player_policy/audit 分权写入 adapter，并接入 Humanlike 写入路径；定向 `18 passed`，全量 `511 passed, 1 skipped`。为保持旧读取器兼容，Humanlike 当前仍在 adapter 后保留裸 payload 覆盖；22 个 RP 统一写入点尚未全部完成，规格继续保持 In Progress。
- F0037 RP schema 本轮完成 envelope 持久化路径：RoundRuntime 建局、事件、决策、终局均写入 envelope；新增 `envelope_snapshot()`，旧 `snapshot()` 透明返回 payload；Humanlike 不再裸 payload 覆盖。定向 `18 passed`，全量 `511 passed, 1 skipped`。22 个 RP 的完整业务写入点仍需后续补齐，规格保持 In Progress。
- F0037 RP schema 已完成本轮验收：事件驱动公共 RP 镜像、隐藏字段拦截、幂等 hash、旧快照兼容和分权写入均通过；定向 `21 passed`，全量 `514 passed, 1 skipped`。schema 文档状态更新为 Done；部分 RP 仍是事件镜像/占位，不宣称完整业务计算。
- 已完成 F0037 后续任务 1–5：事件镜像/派生入口、schema 核心校验、visibility/幂等/迁移测试和 Task 20 独立回归均通过。Task 20 run `task20-20260802_000300`，96/96 units、14 waves、40 batches，校验码 `47C2B4BDBA3569F7`，结果 `514 passed, 1 skipped`。
- 已完成 RP 真实公共投影派生任务 1–5：新增 `public_derivation.py`，覆盖 RP-010、RP-018～RP-022；隐藏真值输入硬拒绝，Humanlike 仅消费公开投影。定向 `20 passed`，全量 `521 passed, 1 skipped`；Task20 run `task20-20260802_001439`，96/96 units、14 waves、40 batches，校验码 `D99B1482DFA2B868`。
- 已完成 RP 真实派生后续任务 1–5：RP-018 使用自身手牌和权威 shanten/ukeire，RP-019 使用 MODEL-001 公开 posterior，RP-020 使用公开风险聚合，新增四座隔离测试和 12 预设固定输入报告 `docs/status/F0037_12_PRESET_COMPARISON.md`。全量 `525 passed, 1 skipped`；Task20 run `task20-20260802_001956`，校验码 `64A377458C3A4C87`。
- 已完成 F0037 UI/存档后续：新增 RP envelope/payload 双视图、F0037-RP-1.0 存档 round-trip 与旧裸 payload migration；定向 `12 passed`，全量 `526 passed, 1 skipped`。12 预设 smoke 生成于 `data/ai_capability/results/f0037_12_presets_smoke/summary.json`，但 runner 尚未动态注入 preset，仅可作为运行验证，不能作为能力差异结论。
- 已完成任务 1–4：支持 per-player `humanlike_preset` 注入、真实加载 12 预设 smoke、存档双视图/迁移测试、提交范围盘点；新增 preset 注入测试。全量 `527 passed, 1 skipped`。建议提交范围已盘点，未执行 Git commit。

## 2026-08-01 Task 20 规格批准

- 已编制并批准 `docs/milestones/M20_task19_independent_full_regression.md`。
- Task 20 目标：独立测试 Task 19 全部 96 units、14 waves、40 batches，继承 ADR-0001/F0034 的无人值守自动调度与 CLI 重启恢复方式，不重复使用 Task 19 通过证据。
- 当前仅完成规格编制，尚未实现 Task 20 runner；下一步为实现独立 runtime、调度器、证据归档和全量测试入口。

## 2026-08-01 Task 20 调度器实现

- 新增 `tools/task20_runner.py`：独立读取 Task 19 96 单元范围，生成运行 manifest/校验码，自动执行 pytest、失败重试、独立 evidence、summary 和时间戳最终报告。
- 新增 `tests/test_task20_runner.py`；Task 20 smoke 通过 `2 passed`，实际运行产物位于 `docs/spec-v3/task20/runs/task20-20260801_222640/`，校验码 `0DFC4039A2B18A3F`。
- 本次 smoke 使用显式 `--pytest tests/test_task20_runner.py` 验证调度链；尚未宣称 Task 19 全量业务回归完成。Task 19 状态保持不变。

## 2026-08-01 Task 20 全量回归完成

- 独立运行 `task20-20260801_223106` 已完成，覆盖 Task 19 范围 `96/96 units`、`14/14 waves`、`40/40 batches`。
- 全量测试结果：`498 passed, 1 skipped`，首轮通过，未触发重试；运行耗时约 `51.059s`。
- 独立校验码：`4F0FADE25BED5AE4`；报告位于 `docs/spec-v3/task20/runs/task20-20260801_223106/task20_final_report_20260801_223157.md`，96 条 unit 结果位于同目录 `evidence/unit_results.jsonl`。
- 本次回归未发现可复现失败，Task 19 `96/96 AUDITED` 状态保持不变。


## 2026-08-01 AI 类型盘点

- 已盘点当前 player registry 与 strategy presets，新增 `docs/status/AI_TYPE_CATALOG_AND_PLAN_2026-08-01.md`。
- 当前基础 player_type：`human`、`random`、`rule_ai`、`humanlike_v2`；`rule_ai_plus` 是 `rule_ai + F0011` 兼容预设，不是独立 Player 类。
- 下一步先批准 AI 类型规范，再统一 resolver、运行身份 metadata 和人工 UI 验收。


## AI 类型规格对比更新

- 已补充 humanlike_v2 与其他 AI 类型的规则 v1 对比：覆盖 random、rule_ai、rule_ai_plus、humanlike_v2 的合法性、状态、计划、记忆、人格、风险和人类化偏差。


## 2026-08-01 AI 类型重命名

- `current_s2` 已统一重命名为规范入口 `rule_ai_plus`，配置文件迁移为 `configs/strategies/rule_ai_plus.json`。
- registry、strategy presets、座位 UI、测试和项目文档已同步；`rule_ai_plus` 仍基于 `RuleAIPlayer + F0011/S2`。


## 2026-08-01 Task 19 重启恢复核验

- `reconcile-startup` 返回 `task19_incomplete=false`、`resume_queue=[]`、`human_gates=[]`；无需要续派的 Task 19 工作。
- 监控器确认 96/96 AUDITED、14/14 waves、40/40 batches、100.00%。

## 2026-08-01 F0036 AI 能力测试工具

- 已按 F0036 实现 `tools/ai_capability_test.py`：复用权威 engine、固定 game_id、四座 AI、实时进度/ETA、Ctrl-C checkpoint/resume、JSONL/JSON/CSV/Markdown 报告。
- 固定 game_id 优先读取 `data/ai_capability/fixed_game_sets/<N>_games/logs`；当前仓库已生成 100 局数据，缺少数量时沿用 `batch-20260301-N` 序列补齐。
- 测试 `tests/test_ai_capability_test.py`：2 passed；100 局混合 AI 验收已运行 24 局后中断，结果保存在 `data/ai_capability/results/100_random_rule_ai_rule_ai_plus_humanlike_v2/`，可用 `--resume` 继续。
- 已增加 `--mode capability --target <AI> --games <N>` 单目标评估模式：三种基线 × 四个座位轮换，共 12 个子实验，输出 `capability_report.md`/`capability_summary.json`。
- 回归测试现为 `3 passed`；能力模式 smoke 已验证首个子实验可持续写入结果，手动中断后保留子实验 checkpoint，未改变 Task 19 状态。
- 测试启动前新增耗时确认：显示实验数量、总局数和预计分钟数；取消后回到参数选择，不启动对局。回归测试现为 `4 passed`。
- 交互参数已改为编号菜单选择：模式、局数、目标 AI 和普通模式的 s0-s3 AI 均不再要求输入文字；回归测试现为 `5 passed`。
- 普通模式和能力评估模式均新增终端 ASCII 实时进度条，显示总百分比；能力模式同时显示当前子实验和局数。回归测试现为 `6 passed`。
- capability 模式进度行新增明确的“总局数 已完成/总局数”字段，例如 `总局数 125/1200`；回归测试现为 `7 passed`。
- capability 模式最终汇总报告改为带启动时间的 `capability_report_YYYYMMDD_HHMMSS.md`；同时保留 `capability_report.md` 最新指针。回归测试现为 `8 passed`。
- 普通与 capability 测试均新增唯一校验码：由局数、固定 game_id 清单、模式和玩家配置 SHA-256 派生；进度行、配置、summary 和报告均记录。回归测试现为 `9 passed`。
- capability 模式进度行已补充动态“已运行”和“剩余约”时间，ETA 按实际已完成局数计算；回归测试保持 `9 passed`。
- 修复 capability 长测暴露的 STATE-004 响应恢复原子性缺陷：失败动作回滚后，fallback PASS 现在也通过受保护事务提交，不再在事务外部分修改 `pending_claims`。固定失败序列与回滚测试通过；全量 `501 passed, 1 skipped`。
- 2026-08-02 F0037 任务 3-4：完成 RP 存档 envelope/payload 双视图 UI；F0037 相关参数矩阵、RP schema/公开派生、12 预设及逐座注入已整理为独立提交范围。全量回归 `527 passed, 1 skipped`；其他工作区改动未纳入。
