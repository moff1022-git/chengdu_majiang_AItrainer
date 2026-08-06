# F0069-A0 主代理全自动编排契约

- 状态：Approved（用户于2026-08-06明确要求“主代理总控、自动生成任务子代理、自动授权、全自动运行”）
- 日期：2026-08-06
- 适用线：F0069 / v0.3.3
- 依赖：F0069、ADR-0002、`docs/DEVELOPMENT.md`
- 性质：流程与授权规格；本文件不授权修改业务代码或启动正式实验

## 1. 目标

F0069后续工作采用单一主代理总控。主代理读取仓库权威状态，拆分有界任务，按依赖自动生成子代理，收集证据并决定推进、返工或停在人工门禁。用户无需为已批准规格内的普通派发、测试、恢复和文档回写逐步确认。

“全自动”只表示在既有权限、已批准规格和本产品线范围内不中断推进；不表示绕过Codex平台审批、操作系统权限、Docs-First门禁或扩大任务范围。

## 2. 现有能力审计

可复用的契约来自现有Task 19工具，但当前实现仍为Task 19专用，不能直接作为F0069运行器：

- `tools/task19_agent_runtime.py`：原子状态写入、Agent生命周期、同类finding计数、三次重复后`BLOCKED`、幂等`resume_queue`与`human_gates`。
- `tools/task19_monitor.py`：只读选择权威worktree、tracker聚合、心跳过期识别和人工确认提示；不会改变任务状态。
- `tests/test_task19_agent_runtime.py`：覆盖READY/DISPATCHED持久化、第三次同类finding转人工门禁、重启恢复与幂等键。

F0069只能复用这些状态机思想。若要新增通用或F0069运行器，必须在A1预注册Approved后另行写实现规格和测试，不得直接修改Task 19权威状态文件。

## 3. 角色与自动派生

主代理是唯一调度者和状态写入协调者；子代理不互相宣布阶段完成，也不扩大范围。

| 角色 | 自动创建条件 | 输入 | 输出 | 完成门禁 |
|---|---|---|---|---|
| Spec Agent | 下一工作包缺少Approved子规格 | 上游Approved规格、当前基线 | 仅`docs/`规格草案 | 独立Review无P0/P1 |
| Spec Reviewer | Spec Agent产出就绪 | 草案、上游约束 | finding清单与结论 | PASS后主代理才可按授权规则批准 |
| Implementer | 对应实现规格已Approved | 精确范围、验收命令 | 代码/配置/测试/证据 | 定向测试通过且diff范围合规 |
| Evidence Runner | 预注册manifest冻结且实现已验收 | 固定SHA/seed/test_id/预算 | 原始结果、完整性报告 | 配对完整率与失败门禁通过 |
| Independent Auditor | 候选提交和证据就绪 | clean archive或固定HEAD | 独立审计报告 | P0/P1=0；不得与Implementer同一代理 |
| Release Agent | A6晋级决定已Approved | 审计通过的固定SHA | 发布清单/候选产物 | 版本、changelog、LATEST与资产一致 |

主代理最多按平台可用并发槽派生子代理；同一文件存在写冲突风险的任务串行。长实验不得占用代理等待：交由可恢复前台执行会话或仓库定义的runner，主代理周期性读取checkpoint。

## 4. 状态机和依赖

每个工作项采用以下状态：

`PLANNED → READY_TO_DISPATCH → DISPATCHED → RUNNING → REVIEW → COMPLETED`

失败进入`REMEDIATING`并派生修复代理；相同规范化finding连续三次仍未解决进入`BLOCKED`，不得以换代理或改名清零计数。人工门禁进入`HUMAN_GATE`。阶段只允许在依赖工作项`COMPLETED`且证据SHA匹配时推进。

F0069固定顺序为A0（本契约）→ A1预注册 → A2粗筛 → A3有限交互/选择 → A4多阵容护栏 → A5一次性盲测 → A6晋级或回滚。A2及以后可在工作包内部并行，但不得跨越前置门禁。

## 5. 自动授权矩阵

用户的全自动指令预授权以下低风险、范围内动作：

- 创建、终止和重派有界子代理；读取仓库；更新本线文档与运行状态。
- 在Approved规格内编辑代码、配置和测试，运行测试、lint、只读审计及预注册实验。
- 在`data/experiments/f0069_v033/`写入可恢复实验数据；安全停止、断点续跑和失败局补跑。
- 对已有Approved规格的机械性状态推进；独立Review PASS后，将完全复述上游既定语义的子规格从Review推进Approved。
- 创建本线提交和本地tag候选，仅当对应阶段规格明确要求且审计通过；是否推送/发布仍受下列边界约束。

下列事项绝不自动授权，必须停止并请求用户或平台确认：

- Codex/操作系统显示的提权、sandbox、Keychain、GUI控制或其他平台权限提示；主代理不得替用户点击或声称已批准。
- 推送远端、创建/合并PR、发布Release、删除远端、覆盖或删除不可恢复数据，除非用户另有明确授权且平台允许。
- 新语义、Out of Scope、修改Engine/Task 19框架、引入F0070内容、跨产品线合并或改变统计主终点/盲测集。
- 泄露秘密、降低安全门禁、跳过独立审计、在读到盲测结果后改预注册。
- 三次同类finding、证据SHA不一致、数据污染、无法证明幂等、资源预算将明显越界。

## 6. 幂等、恢复与监控

每项派发必须持久化：`stream + work_item + gate + candidate_sha/config_sha/spec_sha + attempt`。相同幂等键不得重复创建并行子代理或重复消费实验结果。

新会话恢复顺序：

1. 读取`docs/status/LATEST.md`、本线stream LATEST、changelog及相关Approved规格。
2. 核对当前分支、HEAD、唯一数据根及最近checkpoint；忽略旧session心跳，不把心跳当权威完成证据。
3. 重建未完成工作项的resume queue；存在任何human gate时只暂停受影响的依赖链，其他独立安全任务可继续。
4. 对DISPATCHED/RUNNING项先验证输出、进程和幂等键，再决定接管、重派或标记完成。
5. 每个闭环写回本线LATEST；有实质交付追加changelog；不得只保存在聊天记录。

监控必须只读。`STALE`只表示需要reconcile，不等于失败；只有可验证产物和验收结果能驱动`COMPLETED`。

## 7. 并发与文件所有权

- 主代理派发时声明允许写入的路径；默认一个文件同一时刻只有一个owner。
- Spec Reviewer和Auditor只读，不与被审对象共享实现职责。
- 实验子代理使用唯一`run_id`和临时目录，完成后以manifest引用，不覆盖原始数据。
- 发现工作树有用户或其他代理的未知修改时保留修改；有重叠则暂停该项并交由主代理协调。
- F0069所有写入限制在本worktree及`data/experiments/f0069_v033/`，禁止写入F0070 worktree/数据根。

## 8. F0069启动队列

1. A1 Spec Agent：冻结精确参数点、候选上限、train/select/blind的seed与test_id、Holm方法、最小效应、资源预算和停止条件。
2. A1 Spec Reviewer：独立核查防泄漏、样本量、可复现性、权限边界和Out of Scope。
3. 主代理仅在A1无P0/P1且未新增语义时自动标记Approved；否则形成human gate。
4. A1 Approved后才允许派生Implementer实现必要manifest/runner适配；本A0不构成该实现授权。

## 9. 验收标准

- [x] 主代理为唯一总控，子代理按角色和依赖自动生成。
- [x] 自动授权范围与不可绕过的平台/人工门禁明确分离。
- [x] 幂等键、断点恢复、STALE协调和三次同类finding规则明确。
- [x] F0069与Task 19/F0070状态、代码、数据完全隔离。
- [x] 明确本轮仅文档，A1 Approved之前不得修改业务代码或启动正式实验。

## 10. 回滚

若该编排模式造成重复派发、越界写入或状态源冲突，立即停止自动派发，将受影响项标记`HUMAN_GATE`，保留全部日志和原始产物，以最近一个可验证的stream LATEST和固定HEAD重建队列。不得通过删除证据恢复“干净”状态。
