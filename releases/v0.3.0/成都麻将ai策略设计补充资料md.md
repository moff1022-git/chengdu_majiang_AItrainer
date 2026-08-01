---
id: chatgpt_6a6883b9-c4d4-83ea-8db0-ddea8689e1d7
title: 成都麻将AI策略设计
source: chatgpt
url: "https://chatgpt.com/c/6a6883b9-c4d4-83ea-8db0-ddea8689e1d7"
created: "2026-07-31T15:51:27+08:00"
modified: "2026-07-31T15:51:27+08:00"
tags:
  - ai-conversation
  - chatgpt
message_count: 78
---

> [!QUESTION] User
> 已执行9项决策选A

> [!QUESTION] User
> 是否可以开始制定开发计划了

**ChatGPT:**

下面是整合后的完整 Task 19 提示词，已将权威进度文件改为 Markdown 格式，其他规划要求保持不变。

```
执行 Task 19：成都麻将 AI 训练模拟器剩余开发并行执行总计划。

本任务只编制计划、授权矩阵、并行执行方案和进度跟踪体系。

禁止：
- 修改业务代码；
- 修改既有测试断言；
- 开始 B2-A1 实现；
- 升级任何单元状态；
- 修改 Locked/Frozen 规格；
- 修改 Task 17 历史状态；
- 自动执行 git add、commit、stash、clean、reset、checkout 或删除操作。

==================================================
一、当前权威状态
==================================================

全部审计单元：96。

Task 18 当前状态：

AUDITED=15
INTEGRATED=1
PARTIAL=79
SCAFFOLDED=1

Task 17 历史状态必须保持：

AUDITED=9
INTEGRATED=1
PARTIAL=85
SCAFFOLDED=1

当前已 AUDITED 的 15 个单元：

RULE-003
RULE-016
ALGO-001
ALGO-009
ALGO-010
ALGO-011
HEUR-019
STATE-001
STATE-004
STATE-005
STATE-010
STATE-011
SCORE-001
TRAIN-003
AUDIT-003

剩余开发队列：

- 81 个唯一单元；
- PARTIAL=79；
- INTEGRATED=1：MODEL-001；
- SCAFFOLDED=1：HEUR-016。

当前依赖图：

- 节点数：96；
- 边数：207；
- 无环。

==================================================
二、B2-A1 已批准基线
==================================================

B2-A1-DESIGN-1.0.0 已批准。

实施顺序：

STATE-002 -> STATE-003 -> ALGO-002

批准情况：

- 12/12 决策批准，全部选择 Option A；
- 24/24 语义增量批准；
- 12/12 测试增量批准；
- 6/6 证据增量批准；
- 42/42 AC 定义批准，但尚未执行；
- 9/9 接口分类批准；
- 0 个 BREAKING_CHANGE；
- 43 个 Locked 参数引用批准；
- 6/6 信息边界定义批准。

B2-A1 当前授权状态：

READY_FOR_IMPLEMENTATION

本 Task 19 只编制计划，不得开始实现。

不得重新解释、替换或覆盖已经批准的 B2-A1 决策。

B2-A1 后续实施授权必须明确：

new_direct_test_files_authorized=true
new_test_cases_authorized=true
existing_test_assertion_changes_authorized=false
locked_frozen_changes_authorized=false
unit_status_changes_authorized=false

==================================================
三、Task 19 总目标
==================================================

建立剩余 81 个单元从当前状态到最终验收的完整执行总计划，并覆盖全部 96 个单元的动态进度跟踪。

计划必须支持：

1. 多 Git worktree；
2. 多 Codex 终端并行开发；
3. 文件级写入隔离；
4. 公共接口单一所有者；
5. 分批设计与审批；
6. 分批实现；
7. 分批测试；
8. 分批生成 E4/E5；
9. 分批独立审计；
10. 顺序集成；
11. 全仓回归；
12. 状态安全升级；
13. 阻塞和缺陷跟踪；
14. 接口变化后的重新规划；
15. 全部 96 个单元的动态进度展示。

不得只复制或重新排版旧的 23 批次表。

==================================================
四、重新验证剩余队列
==================================================

读取并交叉核对：

- task18_post_b1b_queue.csv
- task18_post_b1b_dependency_graph.json
- task18_next_batch_units.csv
- task18_current_status_view.json
- Task 18A 原始批次规划
- Task 18B 语义复核材料
- B1-A 最终设计、实现及审计结果
- B1-B 最终设计、实现及审计结果
- B2-A1 已批准完整设计包
- Spec v3 Locked/Frozen 规格
- 参数总表
- 接口总表
- 错误码表
- 信息边界总表
- 审计证据规范

验证：

- remaining_unit_count=81；
- unique_remaining_unit_count=81；
- duplicate_count=0；
- missing_count=0；
- unexpected_count=0；
- audited_unit_in_queue_count=0；
- dependency_graph_acyclic=true；
- 每个剩余单元都有完成路径；
- 每个剩余单元都有批次；
- MODEL-001 外部数据门禁只阻塞其校准和外部效果结论；
- MODEL-001 不得阻塞可独立开发的确定性单元；
- HEUR-016 保持 PATH-FULL-IMPLEMENTATION；
- Task 17 历史状态没有发生变化。

==================================================
五、划分开发轨道
==================================================

至少划分以下轨道：

TRACK-DETERMINISTIC：
状态、规则、算法、计分等确定性生产功能。

TRACK-HEURISTIC：
人类化启发式、做牌计划、风险、认知、有限认知和候选决策。

TRACK-MODEL：
MODEL-001 至 MODEL-005 的模型实现、接线、校准和回退。

TRACK-TRAINING：
训练数据、训练流水线、版本、回放和发布。

TRACK-AUDIT：
追踪、边界、复现、性能、校准和验收工具。

TRACK-EXTERNAL-DATA：
仅处理明确依赖模拟数据发布或现实数据发布的工作。

每个单元只能有一个主轨道，但可以记录跨轨依赖。

==================================================
六、重新形成执行批次
==================================================

为每个批次定义：

batch_id
batch_name
track_id
unit_ids
unit_count
internal_order
external_dependencies
in_batch_dependencies
unlocks
completion_path
design_status
implementation_status
audit_status
model001_gate
expected_shared_interfaces
global_document_impact

批次规则：

- 一般每批 1～4 个单元；
- 同批内部允许存在明确的顺序依赖；
- 每个单元必须能够独立取证和审计；
- 禁止将大量 PARTIAL 单元合并成一次未审查补丁；
- 禁止以批次整体 PASS 代替逐单元验收；
- 尚未完成语义审批的批次不得标记 READY_FOR_IMPLEMENTATION；
- 存在未批准接口决策时只能进入 WAITING_FOR_DESIGN_APPROVAL。

==================================================
七、建立并行执行组
==================================================

为每个批次增加：

parallel_wave_id
parallel_group_id
can_run_in_parallel
parallel_with
cross_batch_dependency
shared_file_risk
shared_interface_risk
shared_test_fixture_risk
shared_evidence_risk
integration_conflict_risk
recommended_terminal
integration_order

并行授权必须同时满足：

1. 所有外部依赖已经 AUDITED；
2. 或依赖属于同一 worktree 内的明确顺序实现；
3. 并行批次之间不存在直接依赖；
4. 并行批次之间不存在间接依赖；
5. 不修改相同业务文件；
6. 不修改相同测试文件；
7. 不同时拥有同一个公共接口；
8. 不同时修改状态总表；
9. 不同时修改 changelog；
10. 不同时修改全局审计矩阵；
11. 不依赖其他并行分支尚未合并的新接口；
12. 每批可以独立运行定向测试；
13. 每批可以独立生成 E4/E5；
14. 每批可以单独提交和回滚。

任一条件不满足：

can_run_in_parallel=false

不得只根据“依赖已满足”判断可以并行。

==================================================
八、文件所有权和写入边界
==================================================

为每个批次输出：

allowed_business_paths
allowed_test_paths
allowed_evidence_paths
allowed_design_paths
read_only_shared_paths
forbidden_paths
public_interface_owner
global_document_owner
expected_new_files
expected_modified_files

规则：

- 同一文件在同一 parallel_wave 中只能有一个写入者；
- Locked/Frozen 规格始终只读；
- Task 17 历史文件始终只读；
- Task 18/19 全局状态文件只能由 Terminal 0 修改；
- Task 19 权威进度文件只能由 Terminal 0 修改；
- changelog 只能由 Terminal 0 修改；
- 公共 DTO、枚举、错误码、PlayerView 和状态接口必须有唯一所有者；
- 开发终端发现范围外修改需求时必须停止；
- 范围外修改必须生成接口变更提案；
- 未批准前不得自行修改共享接口。

==================================================
九、终端和 worktree 规划
==================================================

默认终端：

Terminal 0：
计划控制、状态更新、进度跟踪、集成、全仓测试和审计协调。

Terminal 1：
确定性核心开发。

Terminal 2：
独立规则、计分或启发式开发。

Terminal 3：
训练、审计工具或独立复核。

默认最多同时运行 3 个开发 worktree。

为每个 parallel wave 输出：

baseline_commit
baseline_tag
worktree_directory
branch_name
assigned_batch
assigned_terminal
allowed_write_paths
startup_prompt_file
completion_conditions
commit_message
cherry_pick_order
targeted_test_order
contract_test_order
full_regression_checkpoint
evidence_checkpoint
independent_audit_checkpoint

不得在 dirty 主工作树中直接创建并行开发分支。

如果当前工作树不干净：

1. 列出 tracked modifications；
2. 列出 untracked files；
3. 区分已审计成果；
4. 区分待提交成果；
5. 区分无关用户修改；
6. 提出明确的检查点方案；
7. 不得自动执行任何 Git 写操作。

==================================================
十、B2-A1 特殊安排
==================================================

B2-A1 内部顺序必须保持：

STATE-002 -> STATE-003 -> ALGO-002

三个单元不得拆到不同 worktree 并行修改。

B2-A1 与其他批次并行的前提：

- 对方不修改 GameState；
- 不修改 PlayerState；
- 不修改 RoundRuntime；
- 不修改 PlayerViewV2；
- 不修改 shanten；
- 不修改 win_check；
- 不修改 hand_analyzer；
- 不修改共同测试 fixture；
- 不依赖 B2-A1 尚未合并的新接口。

从以下另外 9 个 DESIGN_REVIEW_READY 单元中检查可与 B2-A1 并行的候选：

ALGO-003
AUDIT-010
HEUR-006
RULE-006
RULE-015
STATE-006
TRAIN-002
TRAIN-004
TRAIN-009

必须实际检查候选代码文件、测试文件、公共接口和依赖关系后再判断。

不得直接假定它们可以并行。

==================================================
十一、实现授权状态
==================================================

每个批次只能处于以下一种状态：

PLANNING
WAITING_FOR_DESIGN_APPROVAL
READY_FOR_IMPLEMENTATION
IMPLEMENTING
IMPLEMENTED_PENDING_EVIDENCE
IMPLEMENTED_PENDING_INDEPENDENT_AUDIT
AUDIT_REMEDIATION
AUDITED
BLOCKED

授权规则：

- 允许新增直接测试文件；
- 允许新增直接测试用例；
- 禁止擅自修改既有测试断言；
- 修改既有测试断言必须单独批准；
- 允许新增 E4/E5 证据；
- 开发终端不得自行标记 AUDITED；
- 独立审计终端不得修改业务代码；
- 集成终端不得用全仓测试代替逐单元证据；
- 只有获得 Approved 设计包的批次才能进入 READY_FOR_IMPLEMENTATION。

==================================================
十二、每单元完成定义
==================================================

每个单元必须分别满足：

1. Approved/Locked 语义闭环；
2. 生产实现；
3. 直接测试；
4. 分支测试；
5. 异常测试；
6. 固定 seed 或确定性测试；
7. 性能测试；
8. 生产接线；
9. NORMAL E4；
10. BOUNDARY E4；
11. HARD_FAILURE E4；
12. DETERMINISM E4；
13. 每增量 E5；
14. AC-01～AC-14；
15. 信息边界测试；
16. 完整工件 SHA-256；
17. 定向回归；
18. 契约回归；
19. 全仓回归；
20. 独立审计；
21. 无开放 P0/P1 缺陷。

==================================================
十三、集成策略
==================================================

每个并行 wave 按以下顺序集成：

1. 各开发分支完成代码、测试和证据；
2. 各开发分支独立提交；
3. Terminal 0 检查修改范围；
4. 检查禁止路径；
5. 检查共享接口冲突；
6. 按依赖顺序逐个 cherry-pick；
7. 每次 cherry-pick 后运行该批定向测试；
8. 全部合并后运行契约测试；
9. 运行全仓测试；
10. 重新生成集成态 E4/E5；
11. 执行跨批次接口测试；
12. 执行信息边界测试；
13. 执行独立审计；
14. Terminal 0 统一更新状态和进度文件。

任何开发分支不得直接合并：

- Task 19 权威进度文件；
- Task 19 当前状态总表；
- Task 17 历史文件；
- 全局 changelog；
- 全局审计矩阵。

==================================================
十四、重规划触发条件
==================================================

发生以下情况必须暂停相关 wave：

- 新增 BREAKING_CHANGE；
- Locked/Frozen 规格矛盾；
- 公共接口所有权冲突；
- 两个并行批次需要修改同一文件；
- 出现新的依赖关系；
- 信息边界测试失败；
- 确定性测试失败；
- 性能阈值失败；
- 全仓测试基线下降；
- E4/E5 无法独立归属；
- MODEL-001 数据门禁被错误传播；
- 进度文件与实际证据不一致；
- 单元状态发生非法跳转。

暂停后生成：

replan_trigger_id
affected_batches
affected_units
current_evidence
required_decision
safe_resume_point
progress_tracker_impact

==================================================
十五、规划执行轮次
==================================================

禁止估算没有依据的人日或小时。

输出：

- parallel wave 总数；
- 每个 wave 的批次数；
- 每个 wave 的单元数；
- 串行关键路径；
- 可并行批次；
- 不可并行原因；
- 集成检查点；
- 审计检查点；
- 外部数据等待点；
- 每个 wave 完成后预计解除的依赖；
- 每个 wave 对总体进度的影响。

==================================================
十六、建立 Markdown 权威进度文件
==================================================

创建：

docs/spec-v3/task19/task19_progress_tracker.md

该文件是 Task 19 唯一权威动态进度视图。

必须包含全部 96 个审计单元，而不只是剩余 81 个单元。

每个单元只能出现一行。

只有 Terminal 0 可以修改该文件。

其他开发终端只能提交 progress delta，不得直接编辑权威进度文件。

==================================================
十七、Markdown 进度文件固定结构
==================================================

task19_progress_tracker.md 必须使用以下结构：

# Task 19 项目进度跟踪

## 元数据

- Authority:
- Unit count: 96
- Task 17 historical distribution:
- Task 18 initial distribution:
- Task 19 current distribution:
- Current parallel wave:
- Last updated:
- Status revision:
- Generated from:
- Evidence snapshot hash:

## 状态摘要

| status | count | percentage |
|---|---:|---:|
...

## 轨道摘要

| track_id | total | audited | active | blocked | progress |
|---|---:|---:|---:|---:|---:|
...

## 批次摘要

| batch_id | wave | total | status | progress | blockers | next_action |
|---|---|---:|---|---:|---|---|
...

## 96 个单元进度

固定表头：

| unit_id | unit_name | category | track_id | batch_id | parallel_wave_id | assigned_terminal | task17_status | task18_initial_status | task19_current_status | design | decision | implementation | direct_test | branch_test | exception_test | integration_test | information_boundary | determinism | performance | production_wiring | E4 | E5 | AC | defects | independent_audit | progress | blocker | next_action | latest_evidence | last_updated | revision |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|---|---|---|---|

## 当前阻塞项

| blocking_id | type | affected_units | reason | required_action | owner |
|---|---|---|---|---|---|
...

## 下一步执行队列

| priority | unit_id | batch_id | current_status | next_action | dependency |
|---:|---|---|---|---|---|
...

## 更新记录

| revision | updated_at | updated_by | delta_file | affected_units | summary |
|---:|---|---|---|---|---|
...

格式规则：

- 全部 96 个单元必须按固定 unit_id 自然顺序排列；
- AC 使用“通过数/总数”，例如 14/14；
- defects 使用“P0/P1/Other”，例如 0/0/2；
- progress 使用百分比，例如 56.25%；
- blocker 无阻塞时填写 NONE；
- latest_evidence 填写相对路径或证据 ID；
- 多个证据使用 `<br>` 分隔；
- next_action 必须简短、明确、可执行；
- 内容中的 `|` 必须转义为 `\|`；
- 禁止在 96 个单元明细表中插入额外说明行；
- 不得用合并单元格；
- 不得省略状态为 AUDITED 的历史单元。

==================================================
十八、进度字段状态枚举
==================================================

task19_current_status 只能使用：

PLANNING
WAITING_FOR_DESIGN_APPROVAL
READY_FOR_IMPLEMENTATION
IMPLEMENTING
IMPLEMENTED_PENDING_EVIDENCE
IMPLEMENTED_PENDING_INDEPENDENT_AUDIT
AUDIT_REMEDIATION
AUDITED
INTEGRATED
SCAFFOLDED
BLOCKED

各子状态只能使用：

NOT_REQUIRED
NOT_STARTED
IN_PROGRESS
PASS
FAIL
PARTIAL
WAITING_APPROVAL
BLOCKED

禁止使用：

- 基本完成；
- 大致通过；
- 接近完成；
- 已有框架；
- 应该可用；
- 可能通过。

==================================================
十九、进度百分比
==================================================

progress 必须根据证据门禁计算，禁止人工填写主观百分比。

每个适用门禁计为一项：

1. 设计批准；
2. 决策批准；
3. 业务实现；
4. 直接测试；
5. 分支测试；
6. 异常测试；
7. 集成测试；
8. 信息边界测试；
9. 确定性测试；
10. 性能测试；
11. 生产接线；
12. E4 四类证据；
13. E5 逐增量追踪；
14. AC 全部通过；
15. 无开放 P0/P1；
16. 独立审计通过。

计算：

progress =
已 PASS 的适用门禁数量
÷
全部适用门禁数量
×
100%

规则：

- 保留两位小数；
- NOT_REQUIRED 不进入分母；
- PARTIAL、IN_PROGRESS、FAIL、BLOCKED 不计为 PASS；
- AUDITED 必须为 100.00%；
- 100.00% 不得自动触发 AUDITED；
- 只有独立审计签署后才能标记 AUDITED；
- 未完成独立审计的单元最高显示 93.75%；
- MODEL-001 模拟数据完成不能代替外部有效性；
- Task 17 已 AUDITED 单元初始化为 100.00%；
- B1-A、B1-B 已独立审计单元初始化为 100.00%。

==================================================
二十、进度初始化
==================================================

初始化全部 96 个单元。

15 个当前 AUDITED 单元：

- task19_current_status=AUDITED；
- progress=100.00%；
- 引用已有审计报告和证据；
- 不得伪造不存在的历史字段。

MODEL-001：

- task17_status=INTEGRATED；
- task19_current_status=INTEGRATED；
- 记录模拟数据生成和工程接线证据；
- 外部校准不足记录为 EXTERNAL_DATA；
- 不得标记 AUDITED。

HEUR-016：

- task17_status=SCAFFOLDED；
- task19_current_status=SCAFFOLDED；
- 根据直接证据设置子状态；
- 不得因为存在框架自动升级。

其余 79 个 PARTIAL 单元：

- 根据现有证据逐项初始化；
- 候选代码不等于实现 PASS；
- 候选测试不等于测试 PASS；
- 无直接证据时使用 NOT_STARTED 或 PARTIAL；
- 每个非 AUDITED 单元必须填写 next_action。

==================================================
二十一、进度更新责任
==================================================

只有 Terminal 0 可以修改：

docs/spec-v3/task19/task19_progress_tracker.md

开发终端完成工作后，只能生成：

docs/spec-v3/task19/progress_deltas/<batch_id>_progress_delta.csv

或：

docs/spec-v3/task19/progress_deltas/<unit_id>_progress_delta.json

delta 至少包含：

unit_id
previous_status
proposed_status
completed_gate
evidence_reference
test_run_id
commit_sha
blocking_change
next_required_action
generated_at
generated_by

Terminal 0 必须先验证 delta，再更新权威 Markdown。

==================================================
二十二、动态刷新触发条件
==================================================

发生以下事件必须刷新进度文件：

1. 设计包生成；
2. 用户批准或拒绝决策；
3. 开始实现；
4. 生产代码完成；
5. 定向测试完成；
6. 契约测试完成；
7. 全仓测试完成；
8. E4 证据生成；
9. E5 追踪生成；
10. 发现 P0/P1 缺陷；
11. 缺陷关闭；
12. 独立审计开始；
13. 独立审计结束；
14. 单元状态升级；
15. 批次合并；
16. 依赖变化；
17. 接口变化；
18. 计划重排。

每次刷新必须：

- 增加 revision；
- 更新 Last updated；
- 更新 updated_by；
- 保留来源 delta；
- 重新计算 progress；
- 重新计算所有摘要；
- 重新执行完整性校验；
- 更新 Evidence snapshot hash；
- 不得修改 Task 17 历史字段。

==================================================
二十三、状态转换规则
==================================================

正常转换：

PLANNING
-> WAITING_FOR_DESIGN_APPROVAL
-> READY_FOR_IMPLEMENTATION
-> IMPLEMENTING
-> IMPLEMENTED_PENDING_EVIDENCE
-> IMPLEMENTED_PENDING_INDEPENDENT_AUDIT
-> AUDITED

异常转换：

任意非 AUDITED 状态
-> BLOCKED

IMPLEMENTING
-> WAITING_FOR_DESIGN_APPROVAL

仅限发现新的语义或接口决策。

IMPLEMENTED_PENDING_INDEPENDENT_AUDIT
-> AUDIT_REMEDIATION

仅限独立审计发现缺陷。

AUDIT_REMEDIATION
-> IMPLEMENTED_PENDING_INDEPENDENT_AUDIT

仅限修复、测试和证据重新生成完成。

开发终端不得提交 AUDITED。

AUDITED 不得由开发终端降级。

如果已审计单元后续发现问题：

- 保留历史审计结论；
- 新建 finding；
- 在当前视图记录风险；
- 由独立审计决定是否调整当前状态；
- 禁止静默改写历史状态。

==================================================
二十四、阻塞分类
==================================================

blocking_type 只能使用：

NONE
DEPENDENCY
DESIGN_DECISION
INTERFACE_DECISION
LOCKED_SPEC_CONFLICT
IMPLEMENTATION_DEFECT
TEST_FAILURE
EVIDENCE_MISSING
INFORMATION_BOUNDARY
DETERMINISM
PERFORMANCE
EXTERNAL_DATA
INTEGRATION_CONFLICT
AUDIT_FINDING

blocking_id 必须引用具体对象：

- decision_id；
- defect_id；
- dependency unit_id；
- data gate ID；
- audit finding ID；
- interface proposal ID。

不得填写“等待处理”“存在问题”等不可追踪文本。

==================================================
二十五、进度摘要
==================================================

task19_progress_summary.md 和 task19_master_plan.md 中的进度摘要必须从 task19_progress_tracker.md 确定性生成。

摘要至少包括：

- 总单元数；
- 各主状态数量；
- 各轨道完成数量；
- 各批次完成数量；
- 当前 parallel wave；
- 当前实施单元；
- 等待设计审批单元；
- 等待实现单元；
- 等待证据单元；
- 等待独立审计单元；
- BLOCKED 单元；
- AUDITED 单元；
- 总体证据门禁完成率；
- 当前串行关键路径；
- 下一步推荐动作。

不得手工维护相互独立的重复统计。

==================================================
二十六、进度工具设计
==================================================

规划一个不依赖 AI 的确定性工具：

tools/task19_progress.py

至少支持：

validate
summary
apply-delta
show-unit
show-batch
show-wave
list-blocked
list-next

要求：

- 只读取结构化 CSV、JSON 和固定格式 Markdown；
- 不调用网络；
- 不调用外部 AI；
- 不修改业务代码；
- 完整解析 Markdown 表格；
- 校验固定表头；
- 将 96 个单元转换为结构化内存记录；
- 应用 delta 后重新计算状态、百分比和摘要；
- 按固定顺序重新生成完整 Markdown；
- 使用临时文件和原子替换；
- 更新失败时原文件保持不变；
- 相同 delta 重复执行必须幂等；
- 拒绝非法状态转换；
- 拒绝开发终端提交 AUDITED；
- 拒绝修改 Task 17 历史字段；
- 固定输入必须产生字节一致输出；
- 稳定处理 Markdown 转义；
- 提供直接测试设计。

本 Task 19 规划阶段不实现该工具。

是否实现必须由 Task 19 执行授权单独决定。

可以规划内部缓存：

docs/spec-v3/task19/.task19_progress_state.json

但必须满足：

- 仅为工具内部缓存；
- 不是用户可见的权威文件；
- 不得取代 Markdown；
- 必须能够从 Markdown 完整重建；
- Markdown 与缓存不一致时，以 Markdown 为权威并报告错误；
- 是否创建由后续执行授权决定。

==================================================
二十七、进度验证
==================================================

生成：

docs/spec-v3/task19/task19_progress_validation.json

至少包含：

progress_tracker_format=MARKDOWN
progress_tracker_row_count=96
progress_tracker_unique_unit_count=96
progress_tracker_duplicate_count=0
progress_tracker_missing_unit_count=0
progress_tracker_unexpected_unit_count=0
progress_tracker_header_valid=true
progress_tracker_section_order_valid=true
progress_tracker_markdown_parse_error_count=0
progress_status_enum_error_count=0
progress_substatus_enum_error_count=0
progress_percent_formula_error_count=0
audited_not_100_percent_count=0
unaudited_with_100_percent_count=0
task17_status_mutation_count=0
missing_next_action_count=0
invalid_blocking_reference_count=0
missing_update_metadata_count=0
multiple_progress_file_writer_count=0
progress_summary_mismatch_count=0

全部错误计数必须为 0。

==================================================
二十八、Task 19 计划验证
==================================================

task19_plan_validation.json 至少验证：

unit_count=96
remaining_unit_count=81
unique_remaining_unit_count=81
current_audited_count=15
duplicate_count=0
missing_count=0
unexpected_count=0
dependency_graph_acyclic=true
every_remaining_unit_has_batch=true
every_batch_has_track=true
every_parallel_batch_has_disjoint_write_paths=true
every_shared_interface_has_one_owner=true
every_wave_has_integration_order=true
task17_history_modified=false
B2-A1_decisions_preserved=true
progress_tracking_ready=true
progress_tracker_format=MARKDOWN
progress_tracker_row_count=96
progress_tracker_writer=Terminal 0

==================================================
二十九、输出文件
==================================================

生成：

docs/spec-v3/task19/
  task19_master_plan.md
  task19_unit_execution_matrix.csv
  task19_batch_plan.csv
  task19_dependency_graph.json
  task19_parallel_wave_plan.csv
  task19_file_ownership_matrix.csv
  task19_interface_ownership.csv
  task19_worktree_plan.md
  task19_integration_plan.md
  task19_audit_plan.md
  task19_replan_rules.md
  task19_status_model.md
  task19_risk_register.csv
  task19_execution_authorization.json
  task19_plan_validation.json
  task19_progress_tracker.md
  task19_progress_schema.md
  task19_progress_update_policy.md
  task19_progress_summary.md
  task19_progress_validation.json
  task19_progress_tool_design.md
  progress_deltas/
    README.md
  prompts/
    terminal_0_integration.md
    terminal_1_wave_1.md
    terminal_2_wave_1.md
    terminal_3_wave_1.md

每个 Terminal 提示词必须明确：

- 负责批次；
- 负责单元；
- 基线 commit；
- worktree 和分支；
- 允许修改路径；
- 禁止修改路径；
- 可新增测试范围；
- 不得修改的既有测试；
- 必须生成的 E4/E5；
- 完成条件；
- 停止条件；
- 提交要求；
- 不得自行合并；
- 不得直接修改权威进度文件；
- 只能提交 progress delta。

==================================================
三十、最终结论
==================================================

最终只能输出以下之一：

TASK19_READY_FOR_PARALLEL_EXECUTION

或：

TASK19_WAITING_FOR_APPROVAL

如果存在以下任一情况，必须输出 TASK19_WAITING_FOR_APPROVAL：

- 并行批次写入路径冲突；
- 公共接口没有唯一所有者；
- 批次语义未批准但计划试图直接编码；
- 基线提交不明确；
- dirty 工作树无法安全隔离；
- 依赖关系无法解析；
- B2-A1 已批准决策被修改；
- 计划完整性检查失败；
- 进度文件不足 96 个唯一单元；
- 进度计算无法复现；
- 多个终端被授权修改权威进度文件；
- Task 17 历史状态发生变化。

最终报告必须明确输出：

final_decision
unit_count
remaining_unit_count
current_status_distribution
parallel_wave_count
first_wave_batches
first_wave_terminals
serial_critical_path
open_planning_blockers
worktree_baseline_ready
task17_history_modified
B2-A1_decisions_preserved
progress_tracking_ready
progress_tracker_format
progress_tracker_authority
progress_tracker_writer
progress_delta_format
progress_tool_implementation_authorized

固定值要求：

progress_tracker_format=MARKDOWN
progress_tracker_authority=docs/spec-v3/task19/task19_progress_tracker.md
progress_tracker_writer=Terminal 0
progress_delta_format=CSV_OR_JSON
progress_tool_implementation_authorized=false
task17_history_modified=false
B2-A1_decisions_preserved=true

不得在本任务中开始业务编码、测试实现、进度工具实现、Git 提交或状态升级。
```

> [!QUESTION] User
> 简要介绍一下这个提示词的任务清单，预计时间

> [!NOTE] ChatGPT
> 这个提示词执行的是“Task 19 全项目开发规划”，不进行业务编码。
> 
> 主要任务清单：
> 
> 1.  复核 96 个单元及剩余 81 个单元的状态、依赖和完整性。
>     
> 2.  将剩余单元划分为确定性、启发式、模型、训练、审计、外部数据等开发轨道。
>     
> 3.  重组小批次，明确内部顺序和跨批依赖。
>     
> 4.  识别可以同时开发的并行波次。
>     
> 5.  为每批限定允许修改的代码、测试和证据路径。
>     
> 6.  分配 Terminal 0～3 和对应 Git worktree。
>     
> 7.  制定合并、回归测试、E4/E5 取证和独立审计流程。
>     
> 8.  建立覆盖全部96个单元的 Markdown 动态进度表。
>     
> 9.  设计进度增量、状态转换、阻塞和重规划机制。
>     
> 10.  生成约20份规划文件及4份终端启动提示词。
>      
> 11.  自动检查单元数量、依赖无环、文件冲突、接口所有权和进度表一致性。
>      
> 12.  最终判断能否进入多终端并行开发。
>      
> 
> 预计执行时间：
> 
> -   仓库结构清晰、现有矩阵完整：约30～60分钟。
>     
> -   需要逐文件核对修改范围和公共接口：约1～2小时。
>     
> -   如果发现 dirty 工作树归属不清、接口冲突或旧矩阵不一致：可能需要2～4小时并停在 `TASK19_WAITING_FOR_APPROVAL`。
>     
> 
> 正常情况下，建议预留约1～2小时。最终产物只是开发总计划，不包含后续81个单元的实际编码时间。

> [!NOTE] ChatGPT
> 目前这10份核心文档逻辑基本一致，但 Task 19 还不能批准为可并行执行。它正确停在：
> 
> ```
> TASK19_WAITING_FOR_APPROVAL
> ```
> 
> 主要原因不是计划结构，而是缺少干净、可复现的 Git 基线。
> 
> 已确认：
> 
> -   当前状态保持 `15/1/79/1`。
>     
> -   剩余81个单元被规划为40个批次、14个 wave。
>     
> -   B2-A1 决策及顺序完整保留。
>     
> -   B2-A1 是当前唯一可直接实施的批次。
>     
> -   W01 的 Terminal 2、3 只能做设计，不能编码。
>     
> -   B2-A1 不与共享状态、PlayerView、RoundRuntime 的批次并行实现。
>     
> -   Terminal 0 独占进度表、状态、集成和全局文档。
>     
> -   Markdown 进度机制、状态转换、审计和重规划规则相互一致。
>     
> -   当前进度摘要数量可闭合为96：
>     
>     -   AUDITED 15
>         
>     -   READY 3
>         
>     -   WAITING DESIGN 76
>         
>     -   INTEGRATED 1
>         
>     -   SCAFFOLDED 1
>         
> 
> ## 尚不能终审的部分
> 
> 本批没有上传以下关键文件，因此暂时无法确认40个批次、14个 wave 和21.61%进度是否计算正确：
> 
> -   `task19_progress_tracker.md`
>     
> -   `task19_unit_execution_matrix.csv`
>     
> -   `task19_batch_plan.csv`
>     
> -   `task19_dependency_graph.json`
>     
> -   `task19_parallel_wave_plan.csv`
>     
> -   `task19_file_ownership_matrix.csv`
>     
> -   `task19_interface_ownership.csv`
>     
> -   `task19_risk_register.csv`
>     
> -   `task19_execution_authorization.json`
>     
> -   `task19_plan_validation.json`
>     
> -   `task19_progress_validation.json`
>     
> -   4份终端提示词
>     
> 
> ## 当前最重要的风险
> 
> `task19_worktree_plan.md` 中把以下范围概括为检查点候选：
> 
> ```
> docs/spec-v3/**
> tests/spec_v3/**
> tests/contracts/**
> ```
> 
> 这个范围过宽，不能直接用于 `git add`。其中可能混有尚未审计、其他任务或用户自己的修改。
> 
> 因此下一步不是直接提交，也不是创建 worktree，而是生成精确基线清单。
> 
> 可交给 Codex：
> 
> ```
> 执行 Task 19 clean checkpoint 只读预审。
> 
> 禁止执行：
> - git add
> - git commit
> - git tag
> - git stash
> - git clean
> - git reset
> - git checkout
> - 文件修改或删除
> 
> 目标：
> 
> 为 Task 19 W01 创建一份精确到单个文件的基线候选清单，供项目所有者批准。
> 
> 一、读取
> 
> - git status --short
> - git diff --name-status
> - git diff --stat
> - B1-A 最终证据 manifest
> - B1-B 最终证据 manifest
> - B2-A1 批准设计包
> - Task 19 全部规划输出
> - 当前测试报告
> - 当前状态视图
> 
> 二、逐文件分类
> 
> 每个 tracked modification 和 untracked file 必须单独分类为：
> 
> INCLUDE_AUDITED_RESULT
> INCLUDE_APPROVED_DESIGN
> INCLUDE_TASK19_PLAN
> EXCLUDE_USER_OR_UNRELATED
> EXCLUDE_ENVIRONMENT
> REQUIRES_OWNER_DECISION
> REQUIRES_AUDIT_RECHECK
> 
> 禁止使用目录通配范围代替逐文件分类。
> 
> 三、每个候选文件记录
> 
> path
> git_status
> classification
> source_task
> related_units
> approval_or_audit_reference
> evidence_manifest_reference
> sha256
> byte_size
> include_in_checkpoint
> reason
> risk
> owner_decision_required
> 
> 四、特别检查
> 
> - 文件是否出现在审计 manifest；
> - 当前 SHA-256 是否仍与审计时一致；
> - 审计后是否再次被修改；
> - 是否涉及多个任务；
> - 是否包含业务代码但没有审计归属；
> - 是否属于虚拟环境、缓存、模拟数据或大文件；
> - 是否包含秘密、令牌或本地机器路径；
> - 是否会导致 B1-A/B1-B/B2-A1 无法复现；
> - Task 19 规划文件是否全部生成；
> - 计划验证和进度验证是否 PASS。
> 
> 五、输出
> 
> docs/spec-v3/task19/checkpoint/
>   task19_checkpoint_candidate.csv
>   task19_checkpoint_include_paths.txt
>   task19_checkpoint_exclude_paths.txt
>   task19_checkpoint_owner_decisions.csv
>   task19_checkpoint_hash_validation.json
>   task19_checkpoint_review.md
>   task19_checkpoint_authorization.json
> 
> 六、授权结论
> 
> 只有满足以下条件才能输出：
> 
> CHECKPOINT_READY_FOR_OWNER_APPROVAL
> 
> - 所有文件逐项分类；
> - include 清单不含目录通配符；
> - 已审计文件哈希一致，或变更已经重新取证；
> - 无秘密和环境目录；
> - 所有 REQUIRES_OWNER_DECISION 已明确列出；
> - Task 19 完整规划文件和验证文件存在；
> - 没有执行任何 Git 写操作。
> 
> 否则输出：
> 
> CHECKPOINT_NOT_READY
> 
> 本任务不得创建 commit 或 tag。
> ```
> 
> 等精确清单生成后，用户只需批准 `include_paths.txt` 中的文件，再由 Terminal 0 建立 checkpoint。之后才能创建 W01 的三个 worktree。
> 
> 当前判断：
> 
> ```
> Task 19 计划结构：基本通过
> 进度体系：基本通过
> 并行开发授权：尚未通过
> 下一步：精确 checkpoint 预审
> ```

**ChatGPT:**

结论：这份预审成功完成了逐文件盘点，但现在还不能批准创建 checkpoint。

`CHECKPOINT_READY_FOR_OWNER_APPROVAL` 的准确含义是“可以进入所有者决策阶段”，不是“已经可以执行 Git 提交”。

关键数据：

-   共检查7,574个文件。
    
-   当前建议纳入117个。
    
-   当前排除7,457个。
    
-   仍有120个待处理：
    
    -   110个 `REQUIRES_OWNER_DECISION`
        
    -   10个 `REQUIRES_AUDIT_RECHECK`
        
-   没有执行 Git 写操作。
    
-   没有目录通配符。
    
-   未发现秘密模式。
    
-   Task 19 计划与进度验证均为 PASS。
    

## 当前不能直接批准的原因

### 1\. B1-A 的10个核心文件未纳入

包括：

```
engine/replay.py
players/humanlike/player.py
players/humanlike/settings_service.py
training/runner.py
engine/rng_v2.py
players/humanlike/config_v2.py
players/humanlike/state010.py
tests/spec_v3/test_b1a_algo009.py
tests/spec_v3/test_b1a_algo011.py
tests/spec_v3/test_b1a_state010.py
```

这些文件对应已经 AUDITED 的：

```
STATE-010
ALGO-009
ALGO-011
```

如果不将它们核验并纳入 checkpoint，Task 19 基线就可能缺失 B1-A 已审计实现，后续依赖图与实际代码不一致。

不能简单选择“排除”，应先补齐逐文件 SHA-256 和审计归属。

### 2\. 当前117个文件几乎都是文档

117个 include 中，真正的业务代码主要只有：

```
engine/deal.py
engine/match.py
engine/orchestrator.py
engine/round_state_machine.py
```

B1-A、部分 B1-B 测试以及许多当前生产代码仍未进入基线。仅提交这117个文件，很可能不能形成可运行的开发基线。

### 3\. 110个 owner decision 不能批量选择

其中混合了：

-   项目审计历史文档；
    
-   状态矩阵；
    
-   B1-B 审计材料；
    
-   MODEL-001 材料；
    
-   多任务共享业务代码；
    
-   测试代码；
    
-   可能属于其他功能分支的修改。
    

需要继续自动归属分析，不应要求用户人工逐个理解120个文件。

### 4\. `docs/changelog.md` 有本机绝对路径命中

它被列入 include，但哈希报告提示该文件包含本机路径。提交前应确认：

-   是必要历史记录，还是意外写入；
    
-   是否包含用户名或本机目录；
    
-   是否应改为仓库相对路径。
    

检查阶段不得直接修改。

## 下一步提示词

```
执行 Task 19 checkpoint owner-decision closure。

本任务继续保持只读。

禁止：
- git add
- git commit
- git tag
- git stash
- git clean
- git reset
- git checkout
- 修改或删除任何文件
- 批量把所有 owner decision 自动设为 include

目标：

将现有120个待决策文件进一步归属，补齐 B1-A/B1-B 已审计生产基线，形成项目所有者可以一次性批准的最终 checkpoint 方案。

一、输入

读取：

- task19_checkpoint_candidate.csv
- task19_checkpoint_owner_decisions.csv
- task19_checkpoint_include_paths.txt
- task19_checkpoint_exclude_paths.txt
- B1-A 全部设计、实现、测试、E4、E5、审计材料
- B1-B 全部设计、实现、测试、E4、E5、审计材料
- B2-A1 Approved 设计包
- MODEL-001 生成器、数据审计和决策材料
- Task 17/18 当前状态文件
- git diff
- git status
- 当前完整测试收集结果

二、优先处理10个 REQUIRES_AUDIT_RECHECK

针对以下文件：

engine/replay.py
players/humanlike/player.py
players/humanlike/settings_service.py
training/runner.py
engine/rng_v2.py
players/humanlike/config_v2.py
players/humanlike/state010.py
tests/spec_v3/test_b1a_algo009.py
tests/spec_v3/test_b1a_algo011.py
tests/spec_v3/test_b1a_state010.py

逐文件完成：

1. 查找 B1-A E5 中的代码符号和测试引用；
2. 确认文件与 STATE-010、ALGO-009、ALGO-011 的关系；
3. 计算当前完整 SHA-256；
4. 检查 B1-A 审计以后是否又被修改；
5. 检查修改内容是否超出 B1-A Approved 范围；
6. 运行只读 diff 分析；
7. 如果内容与已审计范围一致，生成补充 manifest；
8. 如果内容已经改变，保持 REQUIRES_AUDIT_RECHECK；
9. 不得仅因测试通过就认定哈希归属成立。

输出每个文件的：

path
related_unit
approved_symbols
current_sha256
audit_time_sha256
post_audit_modified
scope_match
required_tests
required_runtime_evidence
recommended_action
reason

三、处理110个 REQUIRES_OWNER_DECISION

将每个文件进一步归入以下一种：

INCLUDE_REQUIRED_PROJECT_HISTORY
INCLUDE_REQUIRED_PRODUCTION_BASELINE
INCLUDE_REQUIRED_TEST_BASELINE
INCLUDE_REQUIRED_MODEL001_BASELINE
INCLUDE_REQUIRED_TASK19_PLAN
EXCLUDE_UNRELATED_FEATURE
EXCLUDE_LOCAL_ENVIRONMENT
EXCLUDE_GENERATED_DATA
DEFER_TO_LATER_BATCH
REQUIRES_SPECIFIC_OWNER_DECISION
REQUIRES_AUDIT_RECHECK

分类必须基于：

- 文件 diff；
- 引用关系；
- 单元归属；
- 现有审计报告；
- 当前测试收集；
- 生产 import；
- Task 19 依赖；
- B2-A1 后续实现需要。

不得仅根据目录名称分类。

四、检查基线可运行性

根据最终 include 候选建立只读基线闭包分析：

1. 所有15个 AUDITED 单元的生产代码是否齐全；
2. 对应直接测试是否齐全；
3. B2-A1 所需依赖是否齐全；
4. Python import 闭包是否存在缺失；
5. 测试 fixture 是否齐全；
6. Locked/Frozen 权威文件是否齐全；
7. Task 19 全部计划文件是否齐全；
8. 当前状态文件是否齐全；
9. MODEL-001 工程接线是否会因排除文件而损坏；
10. 是否存在 include 文件依赖 excluded 文件。

如果存在 include→exclude 的必要依赖，checkpoint 不得授权。

五、检查本机路径

检查：

docs/changelog.md
docs/spec-v3/08-review/MAC_CONTINUATION_CHECK_2026-07-29.md

输出：

- 命中行；
- 是否包含秘密；
- 是否只是环境记录；
- 是否适合提交；
- 是否需要后续内容修正；
- 在不修改文件的前提下给出建议。

六、最终清单规则

最终 include 清单必须：

- 逐文件列出；
- 不包含通配符；
- 包含完整可运行的已审计生产基线；
- 包含 B1-A/B1-B 必要直接测试；
- 包含 B2-A1 Approved 设计包；
- 包含 Task 19 完整规划；
- 不包含虚拟环境；
- 不包含缓存；
- 不包含未批准模拟数据；
- 不包含无关 UI/feature 修改；
- 不包含无法解释的共享业务文件；
- 不存在必要的 include→exclude 依赖。

七、输出

docs/spec-v3/task19/checkpoint/
  task19_checkpoint_final_candidate.csv
  task19_checkpoint_final_include_paths.txt
  task19_checkpoint_final_exclude_paths.txt
  task19_checkpoint_deferred_paths.txt
  task19_checkpoint_b1a_supplemental_manifest.csv
  task19_checkpoint_runtime_closure.json
  task19_checkpoint_owner_decision_resolution.csv
  task19_checkpoint_local_path_findings.md
  task19_checkpoint_final_review.md
  task19_checkpoint_final_authorization.json

八、最终状态

只有以下条件全部满足，才能输出：

CHECKPOINT_READY_FOR_FINAL_APPROVAL

- owner decision 未解决数量为0；
- audit recheck 未解决数量为0；
- 已审计生产代码闭包完整；
- 已审计直接测试闭包完整；
- B2-A1 依赖闭包完整；
- include→exclude 必要依赖数量为0；
- 秘密命中为0；
- 环境目录纳入数量为0；
- Task 19 验证全部 PASS；
- 未执行任何 Git 写操作。

否则输出：

CHECKPOINT_DECISIONS_REMAIN

并列出准确的剩余决策，不得降低标准。
```

当前建议：不要直接批准117个 include，也不要排除全部120个待决策项。应先执行上述“决策收敛”，尤其补齐 B1-A 已审计代码基线。

> [!NOTE] ChatGPT
> 业务和测试基线已经闭环，120个待决策项也已全部解决。但还差一个很小的“自包含”问题，暂不建议立即提交。
> 
> ## 已通过的部分
> 
> -   最终候选：7,574个文件。
>     
> -   纳入：236个。
>     
> -   排除：7,337个。
>     
> -   延后：1个 `players/humanlike/belief.py`。
>     
> -   三份清单互不重叠、无重复、无通配符。
>     
> -   owner decision 未解决：0。
>     
> -   audit recheck 未解决：0。
>     
> -   B1-A 10个文件完成补充审计：
>     
>     -   36项直接测试连续运行两次通过；
>         
>     -   E5 42行；
>         
>     -   E4 12行；
>         
>     -   当前完整 SHA-256 已记录。
>         
> -   已审计生产代码闭包完整。
>     
> -   已审计直接测试闭包完整。
>     
> -   B2-A1 依赖闭包完整。
>     
> -   include→exclude 必要依赖为0。
>     
> -   环境目录纳入数为0。
>     
> -   秘密命中为0。
>     
> -   Task 19 计划和进度验证均通过。
>     
> 
> ## 剩余问题：最终审批材料没有进入自身清单
> 
> `task19_checkpoint_final_include_paths.txt` 中没有包含本轮生成的最终 checkpoint 审批材料，例如：
> 
> ```
> task19_checkpoint_final_review.md
> task19_checkpoint_final_authorization.json
> task19_checkpoint_runtime_closure.json
> task19_checkpoint_b1a_supplemental_manifest.csv
> task19_checkpoint_final_include_paths.txt
> task19_checkpoint_final_exclude_paths.txt
> task19_checkpoint_deferred_paths.txt
> task19_checkpoint_owner_decision_resolution.csv
> task19_checkpoint_final_candidate.csv
> task19_checkpoint_local_path_findings.md
> ```
> 
> 如果直接提交236个文件，Git 提交里没有保存“为什么正好提交这236个文件”的最终依据，后续无法从 checkpoint 自身完整重建审批过程。
> 
> 这不需要重新审计业务代码，只需进行一次元数据收口。
> 
> 可交给 Codex：
> 
> ```
> 执行 Task 19 checkpoint provenance self-containment finalization。
> 
> 本任务只更新 checkpoint 规划和审批材料，不修改业务代码、测试、Locked/Frozen 规格或状态。
> 
> 禁止执行：
> - git add
> - git commit
> - git tag
> - git stash
> - git clean
> - git reset
> - git checkout
> - 删除文件
> 
> 一、将以下最终 checkpoint 依据逐文件加入最终 include 清单
> 
> 使用仓库中的实际相对路径，不得使用通配符：
> 
> task19_checkpoint_final_review.md
> task19_checkpoint_final_authorization.json
> task19_checkpoint_runtime_closure.json
> task19_checkpoint_b1a_supplemental_manifest.csv
> task19_checkpoint_final_include_paths.txt
> task19_checkpoint_final_exclude_paths.txt
> task19_checkpoint_deferred_paths.txt
> task19_checkpoint_owner_decision_resolution.csv
> task19_checkpoint_final_candidate.csv
> task19_checkpoint_local_path_findings.md
> 
> 如果这些文件实际位于：
> 
> docs/spec-v3/task19/checkpoint/
> 
> 则使用完整仓库相对路径。
> 
> 二、处理自引用
> 
> task19_checkpoint_final_include_paths.txt 可以列出自身路径，但不得要求在自身内容中保存自身 SHA-256。
> 
> 对清单自身采用以下规则：
> 
> - path 必须存在于 include 清单；
> - byte_size 在最终生成后计算；
> - SHA-256 记录在独立的 provenance manifest 中；
> - provenance manifest 不记录自身 SHA-256；
> - 禁止构造无法收敛的循环哈希。
> 
> 三、生成最终 provenance manifest
> 
> 创建：
> 
> docs/spec-v3/task19/checkpoint/task19_checkpoint_provenance_manifest.csv
> 
> 字段：
> 
> path
> classification
> sha256
> byte_size
> source_task
> related_units
> evidence_reference
> generated_at
> included_in_checkpoint
> 
> 要求：
> 
> - 覆盖全部最终 include 文件；
> - SHA-256 均为实际当前文件计算结果；
> - 清单文件自身按前述非循环规则处理；
> - 不得使用短哈希；
> - 不得使用目录通配符。
> 
> 四、重新验证
> 
> 验证：
> 
> - 最终 include、exclude、deferred 两两无交集；
> - 所有路径唯一；
> - 所有 include 路径实际存在；
> - 所有 exclude/deferred 路径分类明确；
> - 最终审批材料全部纳入；
> - owner decision 未解决数为0；
> - audit recheck 未解决数为0；
> - include→exclude 必要依赖数为0；
> - 环境目录纳入数为0；
> - 秘密命中数为0；
> - 业务代码和测试文件哈希没有因为本任务发生变化；
> - Task 19 计划验证仍为 PASS；
> - Task 19 进度验证仍为 PASS。
> 
> 五、更新文件
> 
> 更新或生成：
> 
> - task19_checkpoint_final_include_paths.txt
> - task19_checkpoint_final_candidate.csv
> - task19_checkpoint_final_authorization.json
> - task19_checkpoint_final_review.md
> - task19_checkpoint_provenance_manifest.csv
> - task19_checkpoint_self_containment_validation.json
> 
> 六、最终授权
> 
> 只有全部验证通过，才能输出：
> 
> CHECKPOINT_AUTHORIZED_FOR_CREATION
> 
> 并记录：
> 
> checkpoint_include_count
> checkpoint_exclude_count
> checkpoint_deferred_count
> owner_decision_unresolved_count=0
> audit_recheck_unresolved_count=0
> missing_include_path_count=0
> provenance_artifact_missing_count=0
> business_hash_changed_count=0
> test_hash_changed_count=0
> git_write_operations_executed=false
> 
> 本任务不得创建 commit 或 tag。
> ```
> 
> 完成这个小步骤后，就可以由你明确授权 Terminal 0 按最终清单创建 checkpoint 和 tag，无需再次复核 B1-A/B1-B 业务语义。

> [!QUESTION] User
> 本轮已完成情况： - Commit：65e8dcb1679466c9e37d10e5a4299a09774332d9 - Parent：4a09a929b0f9011072d5b2f93da39f95a4c8d4a0 - Message：docs: finalize Task 19 checkpoint provenance - 提交文件：严格限定为批准的 6 个文件。 - 提交后 staged 文件：0。 - 未修改业务代码、测试、Locked/Frozen 规格或状态。 - 未创建 tag，未执行 stash、clean、reset、checkout 或删除。 - 当前最终授权：CHECKPOINT_AUTHORIZED_FOR_CREATION。 - 最终自包含 include 数量：248。 下一步完整任务清单： 1. 验证 commit 65e8dcb 中的 provenance manifest 和 248 项 include。 2. 批准创建 W01 baseline tag；建议触发语：批准创建 Task19 W01 baseline tag。 3. 从 65e8dcb 创建干净的 W01 worktree 和分支。 4. 按 Task 19 Wave 1 终端分工初始化并行环境。 5. 开始 B2-A1 实施，保持 STATE-002 → STATE-003 → ALGO-002 顺序。

**ChatGPT:**

当前流程正确，但不要立即创建 tag。先确认 `65e8dcb` 的完整提交树确实包含全部248项，而不是只确认本次新增的6个文件。

特别要确认：其余242项是否已经存在于父提交 `4a09a929` 或更早提交中，并且内容哈希与 provenance manifest 一致。

可先执行以下只读验证提示词：

```
执行 Task 19 W01 baseline commit 最终只读验证。

目标提交：

65e8dcb1679466c9e37d10e5a4299a09774332d9

预期父提交：

4a09a929b0f9011072d5b2f93da39f95a4c8d4a0

本任务不得创建 tag、branch 或 worktree，不得修改工作树。

禁止：

- git add
- git commit
- git tag
- git branch
- git worktree add/remove
- git stash
- git clean
- git reset
- git checkout
- 删除或修改仓库文件

一、提交身份验证

验证：

- commit 存在；
- commit SHA 完整匹配；
- parent 完整匹配；
- commit message 匹配；
- commit 对象有效；
- 当前仓库可读取该提交；
- 目标 baseline tag 尚不存在。

二、读取提交内的最终依据

必须从 commit 65e8dcb 的提交树中读取，而不是读取当前工作树：

- task19_checkpoint_final_include_paths.txt
- task19_checkpoint_final_exclude_paths.txt
- task19_checkpoint_deferred_paths.txt
- task19_checkpoint_provenance_manifest.csv
- task19_checkpoint_final_authorization.json
- task19_checkpoint_self_containment_validation.json
- task19_checkpoint_final_review.md

确认最终授权为：

CHECKPOINT_AUTHORIZED_FOR_CREATION

三、验证248项 include

对 include 清单逐项验证：

- 行数为248；
- 248个唯一仓库相对路径；
- 无空路径；
- 无绝对路径；
- 无目录通配符；
- 无重复；
- 每个路径都存在于 commit 65e8dcb 的 Git tree；
- 不得用当前 dirty 工作树中的同名文件代替；
- 不得有 include 路径只存在于工作树而不存在于 commit。

输出：

include_count
unique_include_count
missing_from_commit_count
unexpected_path_format_count
duplicate_count

全部异常计数必须为0。

四、验证 provenance manifest

逐项检查：

- manifest 覆盖所有需要哈希的 include 文件；
- manifest 中无额外未知路径；
- 每个 SHA-256 为64位小写十六进制；
- 对 commit 65e8dcb 中对应文件的原始字节重新计算 SHA-256；
- 与 manifest 完整一致；
- 按已批准的非循环规则处理 manifest 自身；
- 不接受当前工作树文件哈希作为提交树哈希。

输出：

manifest_row_count
manifest_missing_include_count
manifest_unexpected_path_count
invalid_sha256_count
commit_content_hash_mismatch_count
self_reference_rule_error_count

五、确认父提交闭包

本次 commit 只修改6个文件，因此必须确认：

- 其余242项已存在于父提交或本次提交的最终 tree；
- 不要求所有248项都由本次单一 commit 新增；
- 但最终 commit tree 必须完整包含248项；
- 所有必要生产代码、测试、fixture、规格、证据和 Task19 计划均存在。

分别统计：

introduced_by_target_commit
inherited_from_parent
modified_by_target_commit
missing_from_final_tree

missing_from_final_tree 必须为0。

六、验证基线闭包

确认 commit 65e8dcb 中存在：

- 15个 AUDITED 单元所需生产实现；
- 对应直接测试；
- B1-A 补充 manifest；
- B1-B 最终证据；
- B2-A1 Approved 设计包；
- B2-A1 三单元实施依赖；
- Task19 全部计划文件；
- task19_progress_tracker.md；
- Task19 plan validation；
- Task19 progress validation；
- W01 三个开发终端及 Terminal 0 提示词。

七、验证排除和延后项

确认：

- include/exclude/deferred 两两无交集；
- deferred 数量为1；
- deferred 文件为 players/humanlike/belief.py；
- 虚拟环境没有进入 include；
- 缓存和本地二进制没有进入 include；
- 不存在秘密文件进入 include。

八、验证计划状态

从提交树读取并确认：

- Task19 单元数为96；
- 当前状态为15/1/79/1；
- 剩余81个唯一单元；
- 依赖无环；
- B2-A1 决策保持；
- B2-A1 为 READY_FOR_IMPLEMENTATION；
- Task17 历史状态未修改；
- progress tracker 包含96个唯一单元；
- plan validation PASS；
- progress validation PASS。

九、工作树影响判断

当前主工作树允许仍有无关 dirty 文件，但必须确认：

- staged 文件为0；
- 248个 baseline include 文件没有未提交差异；
- 不存在 include 文件的未跟踪替代版本；
- 无关 dirty 文件不会进入从 commit 创建的新 worktree。

十、输出

生成只读验证报告，不写入仓库：

- /tmp/task19_w01_baseline_commit_validation.json
- /tmp/task19_w01_baseline_commit_validation.md

最终只允许输出：

W01_BASELINE_COMMIT_VERIFIED

或：

W01_BASELINE_COMMIT_NOT_VERIFIED

只有以下条件全部成立才允许 VERIFIED：

- commit/parent/message正确；
- 248个include全部存在于提交树；
- provenance哈希全部匹配；
- 缺失文件为0；
- include/exclude/deferred无交集；
- 生产、测试、设计、证据和计划闭包完整；
- Task19两个验证均PASS；
- 96单元进度表完整；
- Task17历史状态未修改；
- staged文件为0；
- tag尚未创建。

本任务不得创建 tag。
```

如果结果是：

```
W01_BASELINE_COMMIT_VERIFIED
```

下一步再发出明确授权：

```
批准创建 Task19 W01 baseline tag。
```

建议 tag 名称固定为：

```
task19-w01-baseline
```

并让创建任务先确认同名 tag 不存在，再将它精确指向：

```
65e8dcb1679466c9e37d10e5a4299a09774332d9
```

因此当前状态是：checkpoint 提交已经形成，但还处于“提交树最终验证”阶段，验证通过后才能创建 W01 worktree。

> [!QUESTION] User
> W01_BASELINE_COMMIT_VERIFIED - Commit：65e8dcb1679466c9e37d10e5a4299a09774332d9 - Parent：4a09a929b0f9011072d5b2f93da39f95a4c8d4a0 - Include：248/248，缺失、重复、格式异常均为 0。 - Provenance：248 行，哈希不匹配、非法 SHA-256、自引用错误均为 0。 - 父提交继承 242 项；目标提交修改 4 项、新增 2 项。 - Task 18 状态：15/1/79/1；进度表包含 96 个唯一单元。 - Staged 文件为 0；baseline include 工作树差异为 0。 - W01 baseline tag 尚不存在。 - 未修改仓库，报告仅写入： - /tmp/task19_w01_baseline_commit_validation.json - /tmp/task19_w01_baseline_commit_validation.md 本轮已完成情况：所有要求门禁均通过，未创建 tag、branch 或 worktree。

> [!NOTE] ChatGPT
> 验证已全部通过，现在可以批准创建 W01 baseline tag。建议先只创建 tag，不同时创建 branch/worktree，保持操作可单独验证。
> 
> 直接交给 Codex：
> 
> ```
> 批准创建 Task19 W01 baseline tag。
> 
> 目标 commit：
> 
> 65e8dcb1679466c9e37d10e5a4299a09774332d9
> 
> 创建 annotated tag：
> 
> task19-w01-baseline
> 
> Tag message：
> 
> Task 19 W01 verified baseline
> 
> 执行前必须验证：
> 
> 1. 当前仓库存在目标 commit；
> 2. commit SHA 完整匹配；
> 3. parent 为：
>    4a09a929b0f9011072d5b2f93da39f95a4c8d4a0
> 4. task19-w01-baseline 尚不存在；
> 5. staged 文件数量为0；
> 6. baseline 验证结论为：
>    W01_BASELINE_COMMIT_VERIFIED
> 7. 不得使用当前 HEAD 替代明确目标 commit。
> 
> 允许执行的唯一 Git 写操作：
> 
> git tag -a task19-w01-baseline 65e8dcb1679466c9e37d10e5a4299a09774332d9 -m "Task 19 W01 verified baseline"
> 
> 创建后验证：
> 
> - tag 类型为 annotated tag；
> - tag 名称准确；
> - tag peeled commit 精确等于：
>   65e8dcb1679466c9e37d10e5a4299a09774332d9
> - tag message 准确；
> - 未创建 branch；
> - 未创建 worktree；
> - 未修改文件；
> - staged 文件仍为0；
> - 未执行 push；
> - 未执行 add、commit、stash、clean、reset、checkout 或删除。
> 
> 最终输出：
> 
> W01_BASELINE_TAG_CREATED
> 
> 并报告：
> 
> tag_name
> tag_object
> peeled_commit
> tag_message
> staged_file_count
> branch_created
> worktree_created
> push_executed
> 
> 如果同名 tag 已存在但目标不一致，立即停止，不得覆盖或删除，输出：
> 
> W01_BASELINE_TAG_CONFLICT
> ```
> 
> 创建并验证成功后，下一阶段才是从 `task19-w01-baseline` 建立三个独立 worktree：
> 
> -   Terminal 1：B2-A1 实现；
>     
> -   Terminal 2：RULE-015 设计；
>     
> -   Terminal 3：AUDIT-010、TRAIN-009 设计。
>     
> 
> 当前状态：
> 
> ```
> Checkpoint commit：已验证
> Baseline tag：已获创建条件
> Branch/worktree：尚未授权创建
> 业务编码：尚未开始
> ```

> [!QUESTION] User
> W01_BASELINE_TAG_CREATED - tag_name: task19-w01-baseline - tag_object: bb5f74433aa2f9d1daa63f8ff42de95f2b7a9572 - peeled_commit: 65e8dcb1679466c9e37d10e5a4299a09774332d9 - tag_message: Task 19 W01 verified baseline - staged_file_count: 0 - branch_created: false - worktree_created: false - push_executed: false 本轮已完成情况：annotated tag 已精确指向验证提交；未修改文件，未执行 add、commit、push 或其他禁止操作。 下一步完整任务清单： 1. 从 task19-w01-baseline 创建干净 W01 worktree。 2. 创建批准的 W01 开发分支。 3. 初始化 Terminal 0–3 的 Wave 1 环境。 4. 按 STATE-002 → STATE-003 → ALGO-002 启动 B2-A1 实施。

**ChatGPT:**

Baseline tag 已正确建立。现在可以授权创建 W01 的三个开发 worktree 和分支，但本轮只初始化环境，不开始编码或设计修改。

直接交给 Codex：

```
执行 Task 19 Wave 1 worktree 与分支初始化。

权威 baseline：

tag：
task19-w01-baseline

peeled commit：
65e8dcb1679466c9e37d10e5a4299a09774332d9

本任务只创建已批准的 W01 分支和 worktree，不实施业务代码，不生成设计修改，不更新进度状态。

一、读取权威计划

从 baseline 提交读取：

- docs/spec-v3/task19/task19_worktree_plan.md
- docs/spec-v3/task19/task19_parallel_wave_plan.csv
- docs/spec-v3/task19/task19_file_ownership_matrix.csv
- docs/spec-v3/task19/task19_interface_ownership.csv
- docs/spec-v3/task19/prompts/terminal_0_integration.md
- docs/spec-v3/task19/prompts/terminal_1_wave_1.md
- docs/spec-v3/task19/prompts/terminal_2_wave_1.md
- docs/spec-v3/task19/prompts/terminal_3_wave_1.md

确认 W01 分工：

Terminal 1：
- batch：T19-B2A1
- branch：task19/w01-b2a1
- worktree：../wt-task19-t1-w01
- 任务：按 STATE-002 -> STATE-003 -> ALGO-002 顺序实施

Terminal 2：
- branch：task19/w01-design-deterministic
- worktree：../wt-task19-t2-w01
- 任务：RULE-015 design only

Terminal 3：
- branch：task19/w01-design-audit-training
- worktree：../wt-task19-t3-w01
- 任务：AUDIT-010、TRAIN-009 design only

Terminal 0：
- 只负责协调、验证、进度、集成和审计；
- 如果权威计划没有批准单独的 Terminal 0 worktree，不得自行创建；
- 当前 dirty 主工作树只能作为只读协调入口；
- 不得在 dirty 主工作树中实施或集成代码。

二、创建前检查

逐项验证：

1. task19-w01-baseline 存在；
2. tag 为 annotated tag；
3. peeled commit 精确等于目标 commit；
4. 三个目标 branch 均不存在；
5. 三个目标 worktree 目录均不存在；
6. 当前 staged 文件数为0；
7. 当前已有 dirty 文件不会被修改；
8. 三个 worktree 不位于仓库内部；
9. 不得覆盖现有目录；
10. 不得复用其他任务 branch。

任何 branch 或目录已经存在时立即停止，输出冲突详情，不得删除、覆盖或重命名现有内容。

三、允许执行的 Git 写操作

仅允许创建以下三个 branch/worktree：

git worktree add -b task19/w01-b2a1 ../wt-task19-t1-w01 task19-w01-baseline

git worktree add -b task19/w01-design-deterministic ../wt-task19-t2-w01 task19-w01-baseline

git worktree add -b task19/w01-design-audit-training ../wt-task19-t3-w01 task19-w01-baseline

禁止执行：

- git add
- git commit
- git merge
- git cherry-pick
- git rebase
- git push
- git stash
- git clean
- git reset
- git checkout
- git branch -D
- git tag 修改或删除
- git worktree remove
- 文件复制或删除

四、逐 worktree 验证

每个 worktree 必须验证：

- HEAD commit 等于：
  65e8dcb1679466c9e37d10e5a4299a09774332d9
- branch 名称正确；
- 工作树状态干净；
- staged=0；
- modified=0；
- untracked=0；
- Task 19 计划文件存在；
- 对应 Terminal 提示词存在；
- B2-A1 Approved 文件存在；
- Task 17 历史文件存在且未修改。

五、环境约束

- 不复制主工作树的 `.venv-macos`；
- 不复制缓存、data 或未跟踪文件；
- 不复制密钥、OAuth token 或 auth 文件；
- 不执行 direnv allow；
- 如果 worktree 中出现 `.envrc`，只报告其存在和哈希，不批准执行；
- 不安装依赖；
- 不运行网络命令；
- 不运行测试；
- 不启动 Codex 子任务；
- 不修改配置文件。

六、Terminal 启动说明

为用户输出每个终端的启动命令，但本任务不自动启动新的 Codex 会话。

示例：

Terminal 1：

cd ../wt-task19-t1-w01
codex

Terminal 2：

cd ../wt-task19-t2-w01
codex

Terminal 3：

cd ../wt-task19-t3-w01
codex

Terminal 0 保持当前协调会话，不得在 dirty 主工作树修改文件。

七、输出验证

输出：

W01_WORKTREES_INITIALIZED

并报告：

baseline_tag
baseline_commit
terminal_1_branch
terminal_1_worktree
terminal_1_head
terminal_1_clean
terminal_2_branch
terminal_2_worktree
terminal_2_head
terminal_2_clean
terminal_3_branch
terminal_3_worktree
terminal_3_head
terminal_3_clean
main_staged_count
main_dirty_preserved
direnv_execution_performed
dependency_installation_performed
test_execution_performed
business_code_modified
commit_created
push_executed

预期固定值：

main_staged_count=0
main_dirty_preserved=true
direnv_execution_performed=false
dependency_installation_performed=false
test_execution_performed=false
business_code_modified=false
commit_created=false
push_executed=false

如果任一目标 branch 或目录冲突，输出：

W01_WORKTREE_INITIALIZATION_BLOCKED

不得进行部分清理或覆盖。
```

初始化成功后，再分别打开三个终端。下一阶段的授权应分开执行：

-   Terminal 1：允许实施 B2-A1；
    
-   Terminal 2：只允许编制 RULE-015 设计包；
    
-   Terminal 3：只允许编制 AUDIT-010、TRAIN-009 设计包；
    
-   Terminal 0：只负责跟踪，不直接修改三个分支。

> [!QUESTION] User
> W01_WORKTREES_INITIALIZED - baseline_tag: task19-w01-baseline - baseline_commit: 65e8dcb1679466c9e37d10e5a4299a09774332d9 - terminal_1_branch: task19/w01-b2a1 - terminal_1_worktree: ../wt-task19-t1-w01 - terminal_1_head: 65e8dcb1679466c9e37d10e5a4299a09774332d9 - terminal_1_clean: true - terminal_2_branch: task19/w01-design-deterministic - terminal_2_worktree: ../wt-task19-t2-w01 - terminal_2_head: 65e8dcb1679466c9e37d10e5a4299a09774332d9 - terminal_2_clean: true - terminal_3_branch: task19/w01-design-audit-training - terminal_3_worktree: ../wt-task19-t3-w01 - terminal_3_head: 65e8dcb1679466c9e37d10e5a4299a09774332d9 - terminal_3_clean: true - main_staged_count: 0 - main_dirty_preserved: true - direnv_execution_performed: false - dependency_installation_performed: false - test_execution_performed: false - business_code_modified: false - commit_created: false - push_executed: false 三个 worktree 均含 .envrc，SHA-256 为 7a01c3e85f0b23b10367951fc70c5fb7f85af30eccd0538f117219431099d091；未执行 direnv allow。未复制虚拟环境、缓存或 data。 启动命令： cd ../wt-task19-t1-w01 codex cd ../wt-task19-t2-w01 codex cd ../wt-task19-t3-w01 codex 本轮已完成情况：三个批准分支和外部 worktree 已初始化并验证干净；Terminal 0 继续使用当前主工作树作只读协调入口。 下一步完整任务清单： 1. Terminal 1 按批准设计实施 STATE-002 → STATE-003 → ALGO-002。 2. Terminal 2 仅生成 RULE-015 设计包。 3. Terminal 3 仅生成 AUDIT-010、TRAIN-009 设计包。 4. 各终端独立提交，且只生成自己的 progress delta。 5. Terminal 0 完成范围、接口、测试、证据和提交审查后再决定集成。

> [!NOTE] ChatGPT
> 环境已正确初始化，现在可以同时启动三个终端。`.envrc` 暂时保持 blocked，不影响进入 Codex；不要直接执行 `direnv allow`。
> 
> 建议三个终端分别粘贴以下启动指令。
> 
> ### Terminal 1：B2-A1 实施
> 
> ```
> 你是 Task 19 Wave 1 Terminal 1。
> 
> 当前 worktree：
> ../wt-task19-t1-w01
> 
> 当前 branch：
> task19/w01-b2a1
> 
> baseline：
> task19-w01-baseline
> 65e8dcb1679466c9e37d10e5a4299a09774332d9
> 
> 首先完整读取并执行：
> 
> docs/spec-v3/task19/prompts/terminal_1_wave_1.md
> 
> 同时读取：
> 
> - B2-A1 Approved 完整设计包；
> - task19_file_ownership_matrix.csv；
> - task19_interface_ownership.csv；
> - task19_progress_update_policy.md；
> - Task 19 审计和集成规则。
> 
> 授权：
> 
> - 按 STATE-002 -> STATE-003 -> ALGO-002 顺序实施；
> - 允许新增批准范围内的业务代码；
> - 允许新增直接测试文件和测试用例；
> - 允许生成本批 E4/E5 和 progress delta；
> - 禁止修改既有测试断言；
> - 禁止修改 Locked/Frozen；
> - 禁止修改 Task 17 历史状态；
> - 禁止修改 Task 19 权威进度文件；
> - 禁止修改其他终端负责的文件；
> - 禁止自行标记 AUDITED；
> - 禁止合并、cherry-pick 或 push。
> 
> 实施顺序不可并行：
> 
> 1. STATE-002 实现及直接测试；
> 2. STATE-003 实现及直接测试；
> 3. ALGO-002 实现及直接测试；
> 4. 批次集成测试；
> 5. 四类 E4；
> 6. 逐增量 E5；
> 7. AC 执行；
> 8. 定向、契约和全仓回归；
> 9. 生成 T19-B2A1_progress_delta.csv；
> 10. 创建本分支独立提交。
> 
> 如果需要修改允许路径之外的共享接口，立即停止并生成接口变更提案。
> 
> 不得执行 direnv allow。先只读检查 .envrc；如运行测试确实需要环境配置，报告具体缺失项，不得自行授权。
> 
> 最终状态只能是：
> 
> IMPLEMENTED_PENDING_INDEPENDENT_AUDIT
> 
> 或明确的 BLOCKED。
> ```
> 
> ### Terminal 2：RULE-015 设计
> 
> ```
> 你是 Task 19 Wave 1 Terminal 2。
> 
> 当前 worktree：
> ../wt-task19-t2-w01
> 
> 当前 branch：
> task19/w01-design-deterministic
> 
> 首先完整读取并执行：
> 
> docs/spec-v3/task19/prompts/terminal_2_wave_1.md
> 
> 本轮只负责 RULE-015 设计闭环。
> 
> 允许：
> 
> - 读取规格、代码和测试；
> - 生成语义增量；
> - 生成测试增量；
> - 生成证据增量；
> - 生成 AC-01～AC-14；
> - 生成接口影响、参数、可见性和决策包；
> - 生成 progress delta；
> - 提交本分支设计成果。
> 
> 禁止：
> 
> - 修改业务代码；
> - 修改测试代码或断言；
> - 修改 Locked/Frozen；
> - 修改 Task 17 历史状态；
> - 修改 Task 19 权威进度文件；
> - 修改 B2-A1 文件；
> - 自行批准决策；
> - 自行标记 READY_FOR_IMPLEMENTATION 或 AUDITED；
> - 合并、cherry-pick 或 push。
> 
> 发现非唯一语义时必须生成决策选项，不得自行猜测。
> 
> 最终输出：
> 
> WAITING_FOR_DESIGN_APPROVAL
> 
> 如果没有任何待批准决策，也只能生成建议授权，由项目所有者批准后才能变为 READY_FOR_IMPLEMENTATION。
> ```
> 
> ### Terminal 3：AUDIT-010、TRAIN-009 设计
> 
> ```
> 你是 Task 19 Wave 1 Terminal 3。
> 
> 当前 worktree：
> ../wt-task19-t3-w01
> 
> 当前 branch：
> task19/w01-design-audit-training
> 
> 首先完整读取并执行：
> 
> docs/spec-v3/task19/prompts/terminal_3_wave_1.md
> 
> 本轮只负责：
> 
> - AUDIT-010 设计闭环；
> - TRAIN-009 设计闭环。
> 
> 分别为两个单元生成：
> 
> - 8条具体语义增量；
> - 4条直接测试增量；
> - 2条证据增量；
> - AC-01～AC-14；
> - 参数和输入输出定义；
> - 生产调用链；
> - 接口影响；
> - 信息边界；
> - 确定性和性能要求；
> - E4/E5 方案；
> - 决策包；
> - 独立 progress delta。
> 
> 禁止：
> 
> - 修改业务代码；
> - 修改测试代码或断言；
> - 将两个单元合并为一个验收结论；
> - 修改 Locked/Frozen；
> - 修改 Task 17 历史状态；
> - 修改 Task 19 权威进度文件；
> - 修改 Terminal 1 或2的文件；
> - 自行批准决策；
> - 自行标记 AUDITED；
> - 合并、cherry-pick 或 push。
> 
> 最终分别输出：
> 
> AUDIT-010：WAITING_FOR_DESIGN_APPROVAL
> TRAIN-009：WAITING_FOR_DESIGN_APPROVAL
> 
> 如果发现二者存在未记录依赖或共享接口冲突，停止相关设计并生成重规划触发记录。
> ```
> 
> 启动方式：
> 
> ```
> cd ../wt-task19-t1-w01
> codex
> ```
> ```
> cd ../wt-task19-t2-w01
> codex
> ```
> ```
> cd ../wt-task19-t3-w01
> codex
> ```
> 
> 三个终端可以同时运行。Terminal 0 此时只等待并收集结果，不要提前集成，也不要修改当前 dirty 主工作树。

> [!QUESTION] User
> 没有这个目录/wt-task19-t1-w01

> [!NOTE] ChatGPT
> 你查找的是：
> 
> ```
> /wt-task19-t1-w01
> ```
> 
> 这是根目录下的绝对路径；创建时使用的是：
> 
> ```
> ../wt-task19-t1-w01
> ```
> 
> 它表示“项目目录的上一级目录中的兄弟目录”，两者不同。
> 
> 先在原项目目录执行：
> 
> ```
> git worktree list
> ```
> 
> 或获取机器可读结果：
> 
> ```
> git worktree list --porcelain
> ```
> 
> 输出应该类似：
> 
> ```
> worktree /Users/moff/.../chengdu_majiang_AItrainer
> worktree /Users/moff/.../wt-task19-t1-w01
> branch refs/heads/task19/w01-b2a1
> ```
> 
> 然后复制输出中的完整路径进入：
> 
> ```
> cd "/实际完整路径/wt-task19-t1-w01"
> git status
> git branch --show-current
> git rev-parse HEAD
> ```
> 
> 预期：
> 
> ```
> branch: task19/w01-b2a1
> HEAD: 65e8dcb1679466c9e37d10e5a4299a09774332d9
> ```
> 
> 如果你当前就在原项目根目录，也可以：
> 
> ```
> cd ../wt-task19-t1-w01
> ```
> 
> 不要写成：
> 
> ```
> cd /wt-task19-t1-w01
> ```
> 
> 如果 `git worktree list` 中完全没有三个 worktree，说明之前的“初始化成功”报告不对应当前仓库或当前机器。此时不要重新创建，先执行：
> 
> ```
> pwd
> git rev-parse --show-toplevel
> git worktree list --porcelain
> ```
> 
> 把输出发来，再确定实际位置，避免创建重复 worktree。

> [!QUESTION] User
> 、

> [!NOTE] ChatGPT
> 请先在成都麻将项目根目录运行：
> 
> ```
> git worktree list --porcelain
> ```
> 
> 把完整输出发给我，我帮你定位三个 worktree 的实际目录。

> [!QUESTION] User
> moff@bogon chengdu_majiang_AItrainer % cd /Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t1-w01 direnv: error /Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t1-w01/.envrc is blocked. Run direnv allow to approve its content moff@bogon wt-task19-t1-w01 %

> [!NOTE] ChatGPT
> 已经成功进入 Terminal 1 的 worktree。`direnv` 提示只是 `.envrc` 尚未授权，不影响进入目录。
> 
> 先验证当前分支和提交：
> 
> ```
> git branch --show-current
> git rev-parse HEAD
> git status --short
> ```
> 
> 预期输出：
> 
> ```
> task19/w01-b2a1
> 65e8dcb1679466c9e37d10e5a4299a09774332d9
> ```
> 
> 并且 `git status --short` 没有输出。
> 
> 暂时不要执行：
> 
> ```
> direnv allow
> ```
> 
> 直接启动：
> 
> ```
> codex
> ```
> 
> 进入 Codex 后，粘贴之前提供的“Terminal 1：B2-A1 实施”提示词即可。`direnv` 未授权只可能影响项目环境变量；如果测试时报告缺少具体环境配置，再单独检查 `.envrc`。

> [!QUESTION] User
> 本轮已完成情况： - 已完整读取终端提示、B2-A1 Approved 设计包、所有权矩阵、接口矩阵、进度政策及审计/集成规则。 - 已确认 branch、baseline/tag 正确，初始工作树干净。 - 已只读检查 .envrc，未执行 direnv allow。 - 已完成 STATE-002 初版实现和直接测试草案： - engine/round_state_store.py - tests/spec_v3/t19-b2a1_state002.py - Python 3.12 语法检查及 git diff --check 通过。 - 未进入 STATE-003/ALGO-002，未生成证据、delta 或提交；未修改禁止路径、Locked/Frozen、Task 17 或权威进度文件。 阻塞原因： - .venv/bin/python 不存在。 - 系统 pytest 使用 Python 3.9.6，不能加载项目的 dataclass(slots=True)。 - /opt/homebrew/bin/python3.12 可用，但未安装 pytest。 - 串行要求规定 STATE-002 直接测试完成后才能进入 STATE-003，因此不能继续。 - 当前草案尚未通过 pytest，存在待验证风险，不应提交。 下一步完整任务清单： 1. 提供 Python 3.10+ 且包含 pytest 的项目环境；产出可用测试解释器；依赖：环境配置；建议触发语：环境已准备好，继续 T19-B2A1 2. 执行并修正 STATE-002 直接测试；产出 STATE-002 PASS；依赖：步骤 1。 3. 实现并测试 STATE-003；产出代码与直接测试 PASS；依赖：STATE-002 PASS。 4. 实现并测试 ALGO-002；产出代码与直接测试 PASS；依赖：STATE-003 PASS。 5. 依序完成批次集成、四类 E4、逐增量 E5、42 项 AC、定向/契约/全仓回归；依赖：三个单元实现完成。 6. 生成 T19-B2A1_progress_delta.csv 并创建独立提交；依赖：全部验证通过。

> [!NOTE] ChatGPT
> 不需要复制虚拟环境，也不需要执行 `direnv allow`。可以直接复用原项目目录中的 `.venv-macos` 测试解释器。
> 
> 另外发现一个必须先修正的问题：
> 
> ```
> tests/spec_v3/t19-b2a1_state002.py
> ```
> 
> 不符合 pytest 默认的 `test_*.py` 收集规则，而且文件名包含连字符。应改为：
> 
> ```
> tests/spec_v3/test_t19_b2a1_state002.py
> ```
> 
> 否则定向指定路径可能运行，但全仓回归不会自动收集它。
> 
> ## 先验证原项目解释器
> 
> 在 Terminal 1 worktree 中执行：
> 
> ```
> TEST_PY="/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer/.venv-macos/bin/python"
> 
> "$TEST_PY" --version
> "$TEST_PY" -m pytest --version
> ```
> 
> 预期为 Python 3.12.x 且能显示 pytest 版本。
> 
> 再确认解释器可以加载关键依赖：
> 
> ```
> "$TEST_PY" -c "import pytest; print(pytest.__version__)"
> ```
> 
> 这只复用原项目的虚拟环境，不会把 `.venv-macos` 纳入 worktree 或 Git。
> 
> ## 给 Terminal 1 的继续提示词
> 
> ```
> 环境已准备好，继续 T19-B2A1。
> 
> 测试解释器固定为：
> 
> /Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer/.venv-macos/bin/python
> 
> 禁止：
> 
> - 执行 direnv allow；
> - 复制虚拟环境；
> - 创建或提交虚拟环境；
> - 使用系统 Python 3.9；
> - 安装或升级依赖；
> - 修改 Locked/Frozen；
> - 修改既有测试断言；
> - 提前进入 STATE-003。
> 
> 一、解释器预检
> 
> 执行：
> 
> TEST_PY="/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer/.venv-macos/bin/python"
> 
> "$TEST_PY" --version
> "$TEST_PY" -m pytest --version
> 
> 必须确认：
> 
> - Python >= 3.10；
> - pytest 可以导入；
> - 解释器来自原项目 .venv-macos；
> - 不依赖当前 blocked .envrc。
> 
> 如果失败，立即停止并报告准确错误，不得自行安装依赖。
> 
> 二、修正测试文件命名
> 
> 当前草案：
> 
> tests/spec_v3/t19-b2a1_state002.py
> 
> 必须安全重命名为：
> 
> tests/spec_v3/test_t19_b2a1_state002.py
> 
> 确认：
> 
> - 测试文件以 test_ 开头；
> - 文件名不包含连字符；
> - 全仓 pytest 可以自动收集；
> - 不修改测试语义；
> - 不新增重复测试文件。
> 
> 三、完成 STATE-002
> 
> 使用固定解释器运行：
> 
> "$TEST_PY" -m pytest -q \
>   tests/spec_v3/test_t19_b2a1_state002.py \
>   tests/spec_v3/test_state_004.py \
>   tests/spec_v3/test_state_011.py \
>   --maxfail=1
> 
> 根据 Approved STATE-002 设计修正实现或新增测试。
> 
> 不得为了通过测试降低断言。
> 
> STATE-002 必须完成：
> 
> - authority DTO/schema；
> - immutable snapshot；
> - read/write capability；
> - event id 幂等；
> - changed-payload rejection；
> - stale-version/CAS conflict；
> - commit-once；
> - audit 原子性；
> - outbox commit 后重试；
> - 精确回滚；
> - terminal/phase 访问；
> - legacy v5 adapter；
> - PlayerView 信息边界；
> - 直接、边界和异常测试。
> 
> 四、收集确认
> 
> 定向测试通过后，执行：
> 
> "$TEST_PY" -m pytest --collect-only -q | grep "test_t19_b2a1_state002"
> 
> 必须确认新测试被默认全仓收集。
> 
> 然后运行相关契约测试：
> 
> "$TEST_PY" -m pytest -q \
>   tests/contracts \
>   tests/spec_v3/test_t19_b2a1_state002.py \
>   --maxfail=1
> 
> 五、进入下一单元的门禁
> 
> 只有以下条件全部满足才能进入 STATE-003：
> 
> - STATE-002 直接测试全部 PASS；
> - 相关 STATE-004/STATE-011 回归 PASS；
> - 契约测试 PASS；
> - 新测试可以被默认收集；
> - git diff --check PASS；
> - 没有修改禁止路径；
> - 没有修改既有测试断言；
> - 没有未解决 STATE-002 P0/P1 缺陷。
> 
> 通过后记录 STATE-002 实际测试命令、passed/failed/skipped、Python 和 pytest 版本，再按批准顺序进入 STATE-003。
> 
> 本阶段不要提交；完成 STATE-002、STATE-003、ALGO-002 及批次证据后再创建本批独立提交。
> ```
> 
> 如果原项目的 `.venv-macos/bin/python` 不存在，再考虑用 Python 3.12 新建独立环境；目前优先复用已经跑过463项测试的原环境，风险最低。

> [!QUESTION] User
> WAITING_FOR_DESIGN_APPROVAL 本轮已完成：RULE-015 设计闭环包、8 条语义增量、4 条测试增量、2 条证据增量、AC-01～AC-14、接口/参数/可见性矩阵、12 项待批准决策及 progress delta。提交： 7022756。 验证：CSV/JSON 解析及 git diff --check 通过；工作树干净。未修改业务代码、测试、Locked/Frozen、Task 17、权威进度、B2-A1、LATEST 或 changelog。 下一步完整任务清单：项目所有者审批 RULE015-DEC-001～012 → Terminal 0 记录设计授权并等待 STATE-010 接口落地 → 单独授权实现。建议触发语：批准 RULE-015 设计决 策。

> [!NOTE] ChatGPT
> Terminal 2 已按范围完成，当前保持 `WAITING_FOR_DESIGN_APPROVAL` 是正确的。不要仅凭“12项决策完成”直接批准，因为还需要确认每项推荐选项及接口影响。
> 
> 当前也不要把提交 `7022756` 合并到集成分支。
> 
> 下一步应先让 Terminal 0 对设计提交做只读范围检查，并输出12项决策摘要：
> 
> ```
> 执行 RULE-015 设计提交只读审批预审。
> 
> 设计分支：
> 
> task19/w01-design-deterministic
> 
> 设计提交：
> 
> 7022756
> 
> 禁止：
> 
> - cherry-pick
> - merge
> - rebase
> - 修改文件
> - 更新权威进度
> - 标记 READY_FOR_IMPLEMENTATION
> - 批准任何决策
> 
> 一、验证提交
> 
> 确认：
> 
> - 提交存在并取得完整 commit SHA；
> - 提交基于 task19-w01-baseline；
> - 分支工作树干净；
> - 只修改 RULE-015 允许的设计、证据规划和 progress delta 路径；
> - 未修改业务代码；
> - 未修改测试；
> - 未修改 Locked/Frozen；
> - 未修改 Task 17；
> - 未修改 B2-A1；
> - 未修改权威进度、LATEST 或 changelog。
> 
> 二、检查设计包完整性
> 
> 确认存在并可解析：
> 
> - RULE-015 设计评审；
> - 8条语义增量；
> - 4条测试增量；
> - 2条证据增量；
> - AC-01～AC-14；
> - 接口影响矩阵；
> - 参数矩阵；
> - 可见性矩阵；
> - 决策矩阵；
> - 审批表；
> - progress delta。
> 
> 检查：
> 
> - delta ID 唯一；
> - AC ID 唯一；
> - 每条语义都有测试和证据规划；
> - 每条 AC 有可量化输入和预期输出；
> - 没有通用占位描述；
> - 没有自行修改 Locked 定义。
> 
> 三、输出12项决策摘要
> 
> 对 RULE015-DEC-001～012 分别输出：
> 
> decision_id
> question
> option_a
> option_b
> option_c
> recommended_option
> recommendation_reason
> behavior_impact
> compatibility_impact
> interface_impact
> test_impact
> affected_units
> blocking_scope
> 
> 不得替项目所有者选择。
> 
> 四、重点核对 STATE-010
> 
> 确认“等待 STATE-010 接口落地”的准确含义：
> 
> - 如果指已经 AUDITED 的 STATE-010 现有接口，列出准确代码符号和 commit；
> - 如果需要 STATE-010 新接口，必须分类为 ADDITIVE_INTERFACE 或 BREAKING_CHANGE；
> - 如果新接口尚未批准，RULE-015 实现不得授权；
> - 不得把已 AUDITED 状态误写为尚未实现；
> - 不得让 RULE-015 修改 STATE-010 的已审计语义。
> 
> 五、结论
> 
> 输出：
> 
> RULE015_DESIGN_READY_FOR_OWNER_DECISION
> 
> 或：
> 
> RULE015_DESIGN_REVIEW_FAILED
> 
> 如果通过，附上项目所有者可以直接填写的12项选择表，但不得自动批准或集成。
> ```
> 
> 预审通过后，把12项决策摘要发给我，或者直接上传：
> 
> -   决策矩阵；
>     
> -   设计评审；
>     
> -   接口影响矩阵；
>     
> -   审批表。
>     
> 
> 我再判断是否可以全部选推荐项，尤其要检查所谓“STATE-010接口落地”是否会影响已审计基线。当前 Terminal 1 可以继续处理 B2-A1，Terminal 3 也可以继续设计，不需要等待 RULE-015 审批。

> [!QUESTION] User
> 已完成两个单元的独立设计闭环，未发现未记录依赖或共享接口冲突，未触发重规划。 本轮已完成情况 - AUDIT-010：完成 8 条语义增量、4 条直接测试增量、2 条证据增量、AC-01～AC-14、DTO、生产调用链、接口影响、信息边界、确定性/性能、E4/E5 及 5 项 PENDING 决策。 - TRAIN-009：完成同等结构设计，并形成 6 项 PENDING 决策。 - 分别生成独立 progress delta，状态保持不变。 - 静态校验通过：两包均为 8/4/2/14；JSON 有效；git diff --check 通过。 - 未修改业务代码、测试、Locked/Frozen、Task 17、Task 19 权威进度、changelog 或其他终端文件；未提交、合并、cherry-pick 或 push。 - 风险：所有决策尚待项目负责人明确批准，当前不允许实施，也不构成任何 AC Passed 或 AUDITED 结论。 交付物： - docs/spec-v3/task19/design/T19-A04/AUDIT-010_design_package.md - docs/spec-v3/task19/design/T19-A04/AUDIT-010_decision_package.md - docs/spec-v3/task19/progress_deltas/AUDIT-010_progress_delta.json - docs/spec-v3/task19/design/T19-T03/TRAIN-009_design_package.md - docs/spec-v3/task19/design/T19-T03/TRAIN-009_decision_package.md - docs/spec-v3/task19/progress_deltas/TRAIN-009_progress_delta.json 下一步完整任务清单 1. 项目负责人逐项审核 AUDIT-010 的 A04-DEC-001～005；产出明确审批记录；依赖本设计包；建议触发语：批准 AUDIT-010 设计决策 2. 项目负责人逐项审核 TRAIN-009 的 T03-DEC-001～006；产出明确审批记录；依赖本设计包；建议触发语：批准 TRAIN-009 设计决策 3. Terminal 0 独立校验并吸收两个 progress delta；产出权威 tracker revision；依赖审批或保持等待状态；建议触发语：集成 Terminal 3 progress delta 4. 设计获批后另行授权实施；产出业务实现、直接测试与 E4/E5；依赖对应单元全部决策 Approved；建议触发语：实现 AUDIT-010 / 实现 TRAIN-009 5. 实施完成后分别独立审计，不得合并验收结论；产出逐单元 AC/E4/E5 审计；依赖实现交付；建议触发语：独立审计 AUDIT-010 / 独立审计 TRAIN-009 AUDIT-010：WAITING_FOR_DESIGN_APPROVAL TRAIN-009：WAITING_FOR_DESIGN_APPROVAL

> [!NOTE] ChatGPT
> Terminal 3 的设计范围和状态处理正确。当前两个单元都应保持：
> 
> ```
> WAITING_FOR_DESIGN_APPROVAL
> ```
> 
> 但与 Terminal 2 不同，Terminal 3 尚未提交。下一步应先在 Terminal 3 分支形成两个独立提交，再进行所有者审批。不要现在由 Terminal 0 吸收 progress delta。
> 
> 建议两个单元分别提交，保持可独立审查和集成。
> 
> ### Terminal 3 提交提示词
> 
> ```
> 执行 Terminal 3 设计成果分单元提交。
> 
> 当前分支：
> 
> task19/w01-design-audit-training
> 
> 禁止：
> 
> - 修改设计内容；
> - 修改业务代码；
> - 修改测试；
> - 修改 Locked/Frozen；
> - 修改 Task 17；
> - 修改 Task 19 权威进度；
> - 合并、cherry-pick、rebase 或 push；
> - 标记 READY_FOR_IMPLEMENTATION 或 AUDITED。
> 
> 一、提交前验证
> 
> 确认只存在以下6个预期文件：
> 
> AUDIT-010：
> 
> - docs/spec-v3/task19/design/T19-A04/AUDIT-010_design_package.md
> - docs/spec-v3/task19/design/T19-A04/AUDIT-010_decision_package.md
> - docs/spec-v3/task19/progress_deltas/AUDIT-010_progress_delta.json
> 
> TRAIN-009：
> 
> - docs/spec-v3/task19/design/T19-T03/TRAIN-009_design_package.md
> - docs/spec-v3/task19/design/T19-T03/TRAIN-009_decision_package.md
> - docs/spec-v3/task19/progress_deltas/TRAIN-009_progress_delta.json
> 
> 确认：
> 
> - 没有其他 modified/untracked 文件；
> - 两包分别为8条语义、4条测试、2条证据、14条AC；
> - AUDIT-010有5项PENDING决策；
> - TRAIN-009有6项PENDING决策；
> - JSON有效；
> - git diff --check通过；
> - progress delta没有要求状态升级；
> - Task 17和权威tracker未修改。
> 
> 如果存在范围外文件，立即停止。
> 
> 二、提交 AUDIT-010
> 
> 只暂存 AUDIT-010的3个文件。
> 
> 提交信息：
> 
> task19(T19-A04): design AUDIT-010
> 
> 提交后记录完整commit SHA。
> 
> 三、提交 TRAIN-009
> 
> 只暂存 TRAIN-009的3个文件。
> 
> 提交信息：
> 
> task19(T19-T03): design TRAIN-009
> 
> 提交后记录完整commit SHA。
> 
> 四、提交后验证
> 
> 确认：
> 
> - 两个提交均以task19-w01-baseline为祖先；
> - 每个提交只包含对应单元的3个文件；
> - 工作树干净；
> - staged=0；
> - 未修改业务代码或测试；
> - 未执行push；
> - 两个单元状态仍为WAITING_FOR_DESIGN_APPROVAL。
> 
> 最终输出：
> 
> TERMINAL3_DESIGN_COMMITS_CREATED
> 
> 并报告：
> 
> audit010_commit
> audit010_changed_paths
> train009_commit
> train009_changed_paths
> worktree_clean
> staged_count
> push_executed
> ```
> 
> 提交完成后，下一步应做决策预审，而不是直接说“全部批准”。因为当前还看不到11项决策的具体选项。
> 
> 请将以下两个文件上传给我：
> 
> -   `AUDIT-010_decision_package.md`
>     
> -   `TRAIN-009_decision_package.md`
>     
> 
> 或者让 Terminal 0 只读输出每项决策的：
> 
> ```
> decision_id
> 问题
> Option A/B/C
> 推荐选项
> 推荐理由
> 接口影响
> 兼容性影响
> 测试影响
> 未批准时阻塞范围
> ```
> 
> 审批完成之前：
> 
> -   Terminal 1 可以继续 B2-A1；
>     
> -   Terminal 2、3保持等待；
>     
> -   Terminal 0不要在当前 dirty 主工作树 cherry-pick；
>     
> -   progress delta先保留在各设计分支，待设计提交通过范围审查后再统一吸收。

**ChatGPT:**

该预审结论正确：`RULE015_DESIGN_REVIEW_FAILED`。提交范围合规，但设计内容未达到所有者审批入口，不能批准12项决策。

其中需要特别修正一处：progress delta 不能在同一个提交中记录“包含它自己的 commit SHA”，否则会形成循环——修改 SHA 字段会改变提交 SHA。应采用两次提交：

1.  先提交修订后的设计包，获得 `design_commit_sha`。
    
2.  再更新 progress delta，使其引用该设计提交，然后单独提交 delta。
    

## Terminal 2 修复提示词

```
执行 RULE-015 设计包审计修复。

当前分支：

task19/w01-design-deterministic

问题提交：

7022756ef65e51eab185a7569394f0ad78d8863a

当前状态：

RULE015_DESIGN_REVIEW_FAILED

本任务只修订设计文件，不修改业务代码和测试。

禁止：

- 修改 Locked/Frozen；
- 修改 STATE-010 已审计实现；
- 修改业务代码；
- 修改测试代码或断言；
- 修改 Task 17；
- 修改 Task 19 权威进度；
- 修改 B2-A1；
- 修改 LATEST 或 changelog；
- 合并、cherry-pick、rebase、push；
- 自行批准决策；
- 标记 READY_FOR_IMPLEMENTATION 或 AUDITED；
- amend 或重写提交7022756。

一、修复决策矩阵

对 RULE015-DEC-001～012，每项必须包含：

decision_id
question
option_a
option_b
option_c
recommended_option
recommendation_reason
compatibility_impact
interface_impact
test_impact
affected_units
blocked_units
selected_option
approval_status

要求：

- Option C 必须是有实际行为差异的可实施选项；
- 禁止使用“其他”“待定”“MISSING”“由用户决定”等占位项；
- 三个选项必须互斥；
- 每个选项必须说明异常行为、兼容性和测试影响；
- selected_option 保持空；
- approval_status=PENDING；
- 不得自动选择推荐项。

二、修正 STATE-010 依赖

权威事实：

STATE-010 已 AUDITED，并在 baseline 中存在以下生产接口：

- PARAMETER_REGISTRY
- resolve_parameters(...)
- FrozenGlobalParameters.snapshot
- FrozenGlobalParameters.commit(...)
- SeatRuntimeStore.snapshot(...)
- SeatRuntimeStore.version(...)
- SeatRuntimeStore.update(...)
- SeatRuntimeStore.finalize(...)
- HumanlikeV2Player._set_rp(...)

不得再描述为“STATE-010 接口尚未合并”或“等待 STATE-010 落地”。

推荐设计方向：

- RULE-015 复用现有 FrozenGlobalParameters.snapshot；
- 在 RULE-015 自己的 additive facade 内，对 GP-011/012/013 做只读投影；
- 不新增 STATE-010 专用 DTO；
- 不修改 STATE-010 的60参数闭集、CAS、生命周期、错误码或版本语义。

如果仍保留“新增 STATE-010 专用 DTO/API”作为决策选项：

- 必须分类为 ADDITIVE_INTERFACE；
- 必须列出接口 owner；
- 必须列出消费者和兼容测试；
- 未批准前阻塞实现。

任何改变 STATE-010 已审计行为的方案必须分类为 BREAKING_CHANGE，并阻止实现。

三、拆分参数与可见性矩阵

废止或 supersede：

RULE-015_parameter_visibility.csv

分别生成：

RULE-015_parameter_matrix.csv
RULE-015_visibility_matrix.csv

参数矩阵至少包含：

parameter_id
name
type
minimum
maximum
allowed_values
default
null_semantics
scope
locked_source
state010_source
consumer
validation_rule
error_code
decision_dependency

要求：

- 每个参数引用准确的 Locked/registry 来源；
- 不得发明缺失数值；
- 缺失唯一值时绑定具体 decision_id；
- 明确 GP-011、GP-012、GP-013；
- 明确性能参数是规则参数还是验收参数。

可见性矩阵至少包含：

boundary_id
actor
input_field
visibility_class
allowed_source
forbidden_source
projection
consumer
leakage_test
expected_result
error_code
related_ac

至少覆盖：

- 玩家自己的公开/私有输入；
- 对手公开副露；
- 对手暗手；
- 牌墙顺序；
- raw seed；
- restricted audit payload；
- TrainingTruth/oracle；
- STATE-010完整快照；
- RULE-015只读参数投影；
- 计番结果的公开范围。

四、重写 AC-01～AC-14

每条 AC 独立记录：

ac_id
unit_id
requirement
precondition
quantified_input
operation
expected_output
expected_error_code
state_before
state_after
version_before
version_after
determinism_oracle
performance_oracle
visibility_oracle
test_reference
e4_reference
e5_reference
decision_dependency
pass_rule

禁止一句话概括。

每条 AC 必须可以机械判断 PASS/FAIL。

必须覆盖：

- policy schema；
- catalog；
- contains；
- exclusive；
- compatible/independent；
- resolution order；
- cap；
- unknown fan；
- disabled fan；
- relation validation；
- canonical order；
- 纯查询/版本不变；
- 性能；
- E4/E5及生产接线。

AC-12性能必须定义：

- 解释器和平台记录方式；
- 数据集或输入规模；
- warmup次数；
- measured run次数；
- P95计算方法；
- 超时或异常计入方式；
- DEC-012选项对应阈值；
- 固定输入和可复现要求。

在 DEC-012 未批准前，AC-12状态为 WAITING_APPROVAL，不得伪造固定阈值。

五、细化 E4

不得用一个聚合行替代四类运行证据。

至少分别定义：

E4-RULE015-NORMAL
E4-RULE015-BOUNDARY
E4-RULE015-HARD-FAILURE
E4-RULE015-DETERMINISM

每个场景记录：

evidence_id
scenario_class
production_call_site
input_description
input_hash_rule
precondition
operation
intermediate_state
expected_output
expected_error_code
version_before
version_after
visibility_assertion
determinism_assertion
latency_measurement
artifact_hash_rule
related_semantic_deltas
related_ac

场景要求：

NORMAL：
典型复合番目录、关系解析、封顶及生产调用链。

BOUNDARY：
空目录、单番、contains链、exclusive并列、cap=0或边界值。

HARD_FAILURE：
unknown fan、关系环、非法矩阵、非法参数或不完整catalog，且不得发布部分结果。

DETERMINISM：
输入顺序变化、映射顺序变化、跨进程重复，输出ID顺序和规范哈希一致。

六、生成独立审批表

新增：

RULE-015_approval_form.md

包含：

- 设计版本；
- 12项决策；
- 每项推荐选项；
- selected_option；
- owner approval；
- approval date；
- semantic deltas 8/8；
- test deltas 4/4；
- evidence deltas 2/2；
- AC definitions 14/14；
- interface classifications；
- parameter definitions；
- visibility boundaries；
- implementation authorization；
- Locked/Frozen unchanged确认。

当前必须保持：

Approval status: PENDING
business_code_authorized: false

七、第一阶段提交：设计修复

修订完成后验证：

- 8条语义增量；
- 4条测试增量；
- 2条证据增量；
- 14条量化AC；
- 12项决策均有A/B/C；
- 独立参数矩阵存在；
- 独立可见性矩阵存在；
- 审批表存在；
- STATE-010描述准确；
- E4四类场景分别定义；
- JSON/CSV可解析；
- git diff --check通过；
- 无范围外修改。

第一阶段不要修改 progress delta 中的 commit SHA。

只提交设计文件，提交信息：

task19(T19-D02): remediate RULE-015 design gate

记录完整 SHA 为：

rule015_design_commit_sha

八、第二阶段提交：progress delta闭环

取得 rule015_design_commit_sha 后，更新：

docs/spec-v3/task19/progress_deltas/RULE-015_progress_delta.json

字段要求：

- evidence/design commit引用 rule015_design_commit_sha；
- proposed_status=WAITING_FOR_DESIGN_APPROVAL；
- 不得请求READY_FOR_IMPLEMENTATION；
- next_required_action=OWNER_DECISION；
- generated_at更新；
- generated_by=Terminal 2；
- 明确该delta所在提交不是design_commit本身。

只提交progress delta，提交信息：

task19(T19-D02): bind RULE-015 design progress

记录第二个完整SHA为：

rule015_delta_commit_sha

禁止尝试在delta中记录包含它自身的commit SHA。

九、最终验证

确认：

- 原提交7022756保持不变；
- 两个新增提交均以baseline为祖先；
- 设计提交不包含progress delta修改；
- delta提交只包含progress delta；
- 工作树干净；
- staged=0；
- 未修改业务代码或测试；
- 未push；
- 状态仍为WAITING_FOR_DESIGN_APPROVAL。

最终输出：

RULE015_DESIGN_REMEDIATION_COMPLETED

并报告：

rule015_design_commit_sha
rule015_design_changed_paths
rule015_delta_commit_sha
rule015_delta_changed_paths
decision_count
option_c_missing_count
ac_count
unquantified_ac_count
e4_scenario_count
parameter_matrix_valid
visibility_matrix_valid
approval_form_present
state010_dependency_corrected
worktree_clean
```

修复完成后，再由 Terminal 0 对两个新提交做只读预审。只有预审通过，项目所有者才审批12项决策。当前不需要暂停 Terminal 1 或 Terminal 3。

> [!QUESTION] User
> TERMINAL3_DESIGN_COMMITS_CREATED - audit010_commit: 74a39ca23879eb04ea47a12f4b77224f4251b433 - audit010_changed_paths: 3 - docs/spec-v3/task19/design/T19-A04/AUDIT-010_decision_package.md - docs/spec-v3/task19/design/T19-A04/AUDIT-010_design_package.md - docs/spec-v3/task19/progress_deltas/AUDIT-010_progress_delta.json - train009_commit: 8632d128f005694c38f1d0e5c0e1092afd22a257 - train009_changed_paths: 3 - docs/spec-v3/task19/design/T19-T03/TRAIN-009_decision_package.md - docs/spec-v3/task19/design/T19-T03/TRAIN-009_design_package.md - docs/spec-v3/task19/progress_deltas/TRAIN-009_progress_delta.json - worktree_clean: true - staged_count: 0 - push_executed: false 本轮已完成：两个提交均以 task19-w01-baseline 为祖先，各自只包含对应三文件；未修改业务代码、测试、Locked/Frozen、Task 17 或权威 tracker。两单元仍为 WAITING_FOR_DESIGN_APPROVAL。 下一步完整任务清单： 1. Terminal 0 校验并集成两个提交；依赖上述 SHA；建议触发语：集成 Terminal 3 设计提交 2. 项目负责人分别审批 PENDING 决策；产出独立审批记录；建议触发语：审批 AUDIT-010 和 TRAIN-009 设计 3. 审批后另行授权实现；当前不得标记 READY_FOR_IMPLEMENTATION 或 AUDITED。

**ChatGPT:**

两个提交结构合规，但下一步不应直接“集成”。应先由 Terminal 0 对两个单元分别做只读审批入口审查，避免重复 RULE-015 的设计深度问题。

还要重点检查 progress delta 是否存在“提交 SHA 自引用”或仍为 `PENDING`。设计包与 delta 同处一个提交时，delta 不能可靠记录包含自身的 commit SHA。

可交给 Terminal 0：

```
执行 Terminal 3 两个设计提交的只读审批入口审查。

提交：

AUDIT-010：
74a39ca23879eb04ea47a12f4b77224f4251b433

TRAIN-009：
8632d128f005694c38f1d0e5c0e1092afd22a257

baseline：

task19-w01-baseline
65e8dcb1679466c9e37d10e5a4299a09774332d9

本任务只读，不得集成或修改文件。

禁止：

- cherry-pick
- merge
- rebase
- 修改设计文件
- 修改权威进度
- 批准决策
- 标记 READY_FOR_IMPLEMENTATION
- 创建业务代码或测试
- push

一、提交结构验证

分别确认：

- 两个提交存在；
- 均以baseline为祖先；
- AUDIT-010提交只包含其3个文件；
- TRAIN-009提交只包含其3个文件；
- 如果TRAIN-009提交以AUDIT-010提交为父提交，记录后续集成顺序；
- 没有业务代码、测试、Locked/Frozen、Task17或权威tracker修改。

二、逐单元设计完整性

分别验证：

- 8条具体语义增量；
- 4条直接测试增量；
- 2条证据增量；
- AC-01～AC-14；
- DTO和字段定义；
- 输入、输出和错误码；
- 生产调用链；
- 接口影响；
- 参数定义；
- 信息边界；
- 确定性；
- 性能；
- 四类E4；
- 逐增量E5；
- 独立审批记录或审批入口。

不得因为文档中出现“8/4/2/14”就认定通过，必须检查内容是否可执行、可量化、可机械判断。

三、决策检查

AUDIT-010：

A04-DEC-001～005

TRAIN-009：

T03-DEC-001～006

每项必须具有：

decision_id
question
option_a
option_b
option_c
recommended_option
recommendation_reason
compatibility_impact
interface_impact
test_impact
affected_units
blocked_units
selected_option
approval_status

要求：

- 每项至少具有完整、互斥、可实施的选项；
- 禁止使用“其他”“待定”“由用户决定”等占位选项；
- selected_option为空；
- approval_status=PENDING；
- 未替项目所有者选择。

四、AC检查

每条AC必须定义：

- 前置条件；
- 量化输入；
- 操作；
- 预期输出；
- 预期错误码；
- 状态或版本变化；
- 测试oracle；
- E4/E5引用；
- 决策依赖；
- 明确PASS规则。

汇总：

ac_count
unquantified_ac_count
missing_error_oracle_count
missing_test_binding_count
missing_evidence_binding_count

五、E4/E5检查

每单元至少独立定义：

NORMAL
BOUNDARY
HARD_FAILURE
DETERMINISM

每类必须有：

- 生产调用点；
- 输入；
- 前置状态；
- 操作；
- 预期输出；
- 错误码；
- 版本变化；
- 延迟测量；
- 工件哈希规则；
- 相关语义和AC。

不得用一个聚合描述代替四类场景。

六、接口和边界检查

AUDIT-010重点检查：

- 审计输入来自哪些生产证据；
- 是否只读；
- 是否会修改业务状态；
- 审计失败是否影响业务提交；
- 如何验证E4/E5、AC和SHA-256；
- 审计工具自身的确定性和错误码；
- 独立审计人与开发者边界。

TRAIN-009重点检查：

- RNG版本和坐标；
- replay及训练运行入口；
- 数据和模型artifact边界；
- 隐藏信息与restricted label zone；
- 相同seed的跨进程复现；
- 训练失败、恢复和部分artifact处理；
- 是否依赖MODEL-001外部有效性；
- 外部数据门禁是否被错误传播。

七、progress delta检查

分别检查：

- proposed_status必须为WAITING_FOR_DESIGN_APPROVAL；
- 不得请求READY_FOR_IMPLEMENTATION；
- 不得请求AUDITED；
- next action必须是OWNER_DECISION；
- 不得含有无法成立的自身commit SHA；
- 如果commit_sha为PENDING，标记P2并要求后续metadata提交；
- 如果commit_sha声称等于包含delta的同一提交，标记循环引用错误；
- 推荐使用design_artifact_hash或两阶段提交闭环。

八、输出独立结论

分别输出：

AUDIT010_DESIGN_READY_FOR_OWNER_DECISION
或
AUDIT010_DESIGN_REVIEW_FAILED

TRAIN009_DESIGN_READY_FOR_OWNER_DECISION
或
TRAIN009_DESIGN_REVIEW_FAILED

不得使用一个合并结论代替两个单元。

如果通过，分别输出项目所有者决策表。

如果失败，分别列出：

finding_id
severity
affected_file
affected_section
required_fix
blocking_scope

九、集成建议

只输出建议，不执行：

- 两提交后续cherry-pick顺序；
- 是否需先生成修复提交；
- 是否需单独的approval提交；
- progress delta何时由Terminal 0吸收。

本轮不得cherry-pick。
```

只有两个设计包分别通过上述预审后，才进入项目所有者审批。审批后应在 Terminal 3 分支生成独立审批记录或授权提交，最后由 Terminal 0 按顺序集成，不能现在直接把 `WAITING_FOR_DESIGN_APPROVAL` 当作实现授权。

**ChatGPT:**

两个失败结论成立。Terminal 3 的提交范围没有问题，但设计深度与 RULE-015 出现了相同缺陷，说明第一版设计模板过于概括。

当前不要审批、集成或吸收 progress delta。应让 Terminal 3 在现有分支上分别生成修复提交，并保持两个单元独立。

## Terminal 3 修复提示词

```
执行 Terminal 3 的 AUDIT-010、TRAIN-009 设计门禁修复。

当前分支：

task19/w01-design-audit-training

baseline：

task19-w01-baseline
65e8dcb1679466c9e37d10e5a4299a09774332d9

原始提交：

AUDIT-010：
74a39ca23879eb04ea47a12f4b77224f4251b433

TRAIN-009：
8632d128f005694c38f1d0e5c0e1092afd22a257

当前结论：

AUDIT010_DESIGN_REVIEW_FAILED
TRAIN009_DESIGN_REVIEW_FAILED

本任务只修复设计包，不实现业务代码和测试。

禁止：

- amend或重写原提交；
- 修改业务代码；
- 修改测试代码或断言；
- 修改Locked/Frozen；
- 修改Task 17；
- 修改Task 19权威tracker；
- 修改B2-A1或RULE-015；
- 修改LATEST或changelog；
- 自行批准决策；
- 标记READY_FOR_IMPLEMENTATION或AUDITED；
- merge、cherry-pick、rebase、push。

==================================================
一、通用修复标准
==================================================

两个单元必须分别满足：

1. 8条具体语义增量；
2. 4条直接测试增量；
3. 2条证据增量；
4. AC-01～AC-14；
5. 完整字段级DTO；
6. 完整错误码表；
7. 逐接口影响矩阵；
8. 参数矩阵；
9. 可见性矩阵；
10. 四个独立E4场景；
11. 逐增量E5绑定；
12. 独立审批表；
13. 所有非唯一语义均有编号决策；
14. 每项决策都有完整A/B/C选项；
15. progress delta采用非循环提交引用。

不得用自然语言概述替代结构化定义。

==================================================
二、决策包修复
==================================================

AUDIT-010至少覆盖：

A04-DEC-001～005

TRAIN-009至少覆盖：

T03-DEC-001～006

如果修复中发现新的非唯一行为，必须新增连续decision ID，不得隐藏在正文中。

每项决策必须包含：

decision_id
question
option_a
option_b
option_c
recommended_option
recommendation_reason
compatibility_impact
interface_impact
test_impact
affected_units
blocked_units
selected_option
approval_status

要求：

- A/B/C必须互斥、具体、可实施；
- Option C不能是“其他”“待定”“由用户决定”；
- selected_option保持空；
- approval_status=PENDING；
- 不得预填项目所有者选择；
- 每个选项必须说明错误、回滚、兼容和测试影响。

==================================================
三、AC-01～AC-14修复
==================================================

两个单元的每条AC必须分别记录：

ac_id
requirement
precondition
quantified_input
operation
expected_output
expected_error_code
state_before
state_after
version_before
version_after
test_oracle
visibility_oracle
determinism_oracle
performance_oracle
test_reference
e4_reference
e5_reference
decision_dependency
pass_rule

要求：

- 每条AC可以机械判断PASS/FAIL；
- 每条AC有明确输入规模或边界；
- 每条AC有错误码或明确NOT_APPLICABLE；
- 每条AC绑定直接测试；
- 每条AC绑定E4或E5；
- 禁止使用“符合预期”“正确处理”等概括性pass_rule；
- 未批准决策依赖的AC标记WAITING_APPROVAL，不得伪造PASS。

==================================================
四、E4/E5修复
==================================================

每个单元分别定义：

E4-<UNIT>-NORMAL
E4-<UNIT>-BOUNDARY
E4-<UNIT>-HARD-FAILURE
E4-<UNIT>-DETERMINISM

每个场景必须包含：

evidence_id
scenario_class
production_call_site
precondition
quantified_input
operation
intermediate_state
expected_output
expected_error_code
version_before
version_after
visibility_assertion
determinism_assertion
latency_measurement
artifact_hash_rule
related_semantic_deltas
related_ac

禁止将四类场景写在同一个聚合行中。

E5必须逐行绑定：

delta_id
source_reference
acceptance_ids
code_symbols
test_references
runtime_evidence_ids
artifact_hash_rule
expected_result

==================================================
五、AUDIT-010专项修复
==================================================

建立字段级DTO/schema，至少定义：

AuditRequest
AuditSubject
EvidenceReference
AuditIdentity
AuditCapability
SignatureReference
AuditFinding
AuditResult
RetentionRecord
AuditOutboxRecord

每个字段定义：

field_name
type
required
default
null_semantics
minimum
maximum
allowed_values
visibility
canonicalization
validation_error

不得保存或展示真实私钥、token或secret。

SignatureReference只能包含安全引用，例如：

key_id
algorithm
signature
signed_payload_hash
signer_identity_id

不得包含private key material。

建立完整错误码表，至少处理：

- 非法审计主体；
- 缺失证据；
- 哈希不匹配；
- 签名无效；
- 自审计禁止；
- 身份/能力不足；
- 重复请求；
- 冲突请求；
- append-only写入失败；
- retention spool失败；
- 非法状态转换；
- 不支持的schema/version。

建立逐接口矩阵，分别分类：

- audit service；
- signer adapter；
- identity/capability provider；
- AUDIT-014 adapter；
- evidence reader；
- finding writer；
- append-only journal；
- retention spool；
- outbox；
- progress/audit report exporter。

分类只能使用：

REUSE_AS_IS
COMPATIBLE_ADAPTER
ADDITIVE_INTERFACE
BREAKING_CHANGE
DECISION_REQUIRED

每个接口必须有唯一owner。

机械定义独立性：

- developer_identity_id；
- auditor_identity_id；
- allowed_capabilities；
- forbidden_self_audit=true；
- same_identity rejection；
- signer key reference；
- reviewer role；
- approval role；
- independent signature；
- 审计终端只读业务代码；
- 审计失败不得回滚已提交业务状态。

定义事务边界：

1. 业务authority已经提交；
2. 审计器只读证据；
3. finding写入append-only记录；
4. finding写入失败不得修改业务状态；
5. 部分写入必须回滚或进入明确恢复队列；
6. outbox/retention失败必须有稳定错误和重试语义；
7. 重复audit request必须幂等；
8. changed-payload duplicate必须拒绝。

新增：

AUDIT-010_interface_matrix.csv
AUDIT-010_dto_schema.csv
AUDIT-010_error_matrix.csv
AUDIT-010_parameter_matrix.csv
AUDIT-010_visibility_matrix.csv
AUDIT-010_acceptance_matrix.csv
AUDIT-010_e4_matrix.csv
AUDIT-010_e5_plan.csv
AUDIT-010_approval_form.md

审批表当前必须：

approval_status=PENDING
business_code_authorized=false

==================================================
六、TRAIN-009专项修复
==================================================

首先只读检查：

engine/rng_v2.py::STREAMS

列出实际已批准stream，不得假设存在名为domain的stream。

RNG方案必须形成明确决策：

方案类型只能是以下之一：

1. 绑定现有、语义匹配的已批准stream；
2. 使用现有stream加新的版本化coordinate/domain label，但不修改STREAMS闭集；
3. 新增stream并分类为ADDITIVE_INTERFACE；
4. 改变已有stream语义则分类为BREAKING_CHANGE并阻止实现。

不得声称完全复用ALGO-011，同时又使用不存在的stream。

精确定义随机坐标，至少包含：

rng_version
master_seed_ref
match_id
game_id
round_id
episode_id
worker_assignment_id
environment_variant_id
stream_name
coordinate_index
purpose_label

要求：

- 相同版本化输入跨进程字节稳定；
- worker执行顺序变化不改变固定episode结果；
- worker数量变化的行为必须明确；
- episode assignment规则必须固定；
- 禁止读取未来状态或restricted label；
- 不得记录raw seed到策略视图。

Observation接口必须形成编号决策：

- 复用现有schema；
- 使用compatible adapter；
- 新增additive extension；
- 迁移旧schema；
- 如果改变Frozen字段则明确BREAKING_CHANGE。

不得保留“若extension不可用则迁移”这类未编号描述。

建立字段级DTO/schema，至少定义：

DomainRandomizationRequest
DomainRandomizationCoordinate
EnvironmentVariant
EpisodeAssignment
ObservationEnvelope
RestrictedArtifactReference
TrainingRunRequest
TrainingRunResult
ReplayManifest
PartialArtifact
RecoveryRecord

建立完整artifact事务规则：

1. 写入临时文件；
2. 完整校验；
3. fsync；
4. 原子rename；
5. manifest/hash最后提交；
6. 失败时不得发布最终artifact；
7. partial artifact保留或删除策略必须唯一；
8. 重启恢复规则；
9. orphan temporary处理；
10. replay拒绝不完整manifest；
11. 重复run幂等；
12. changed-payload duplicate拒绝；
13. 失败不得污染已发布版本；
14. restricted artifact不得进入policy feature目录。

明确MODEL-001门禁：

- MODEL-001外部有效性只限制校准和外部效果声明；
- 不阻塞TRAIN-009规则域随机化工程实现；
- 不阻塞确定性replay；
- 不得把模拟数据称为现实有效性证据；
- restricted label zone必须物理隔离。

新增：

TRAIN-009_interface_matrix.csv
TRAIN-009_dto_schema.csv
TRAIN-009_error_matrix.csv
TRAIN-009_parameter_matrix.csv
TRAIN-009_visibility_matrix.csv
TRAIN-009_acceptance_matrix.csv
TRAIN-009_e4_matrix.csv
TRAIN-009_e5_plan.csv
TRAIN-009_approval_form.md

审批表当前必须：

approval_status=PENDING
business_code_authorized=false

==================================================
七、AUDIT-010设计修复提交
==================================================

先只修复AUDIT-010。

不要在本提交中修改AUDIT-010 progress delta。

验证：

- 决策均有A/B/C；
- 未编号歧义为0；
- 14条AC全部量化；
- 缺失错误oracle为0；
- 缺失测试绑定为0；
- 缺失证据绑定为0；
- E4场景数为4；
- DTO字段完整；
- 接口逐项分类；
- 独立性规则可机械验证；
- approval form存在且PENDING；
- git diff --check通过。

提交信息：

task19(T19-A04): remediate AUDIT-010 design gate

记录完整SHA：

audit010_design_remediation_commit

==================================================
八、AUDIT-010 delta提交
==================================================

取得audit010_design_remediation_commit后，单独修改：

AUDIT-010_progress_delta.json

要求：

- 引用audit010_design_remediation_commit；
- proposed_status=WAITING_FOR_DESIGN_APPROVAL；
- next_required_action=OWNER_DECISION；
- 不得记录包含delta自身的commit SHA；
- 可增加design_commit_sha字段；
- generated_at更新；
- generated_by=Terminal 3。

提交信息：

task19(T19-A04): bind AUDIT-010 design progress

记录：

audit010_delta_commit

==================================================
九、TRAIN-009设计修复提交
==================================================

然后只修复TRAIN-009。

不要在本提交中修改TRAIN-009 progress delta。

验证标准与AUDIT-010相同，并额外确认：

- 不存在虚构RNG stream；
- RNG兼容分类明确；
- Observation决策已编号；
- artifact原子性完整；
- MODEL-001门禁隔离明确；
- restricted artifact边界完整。

提交信息：

task19(T19-T03): remediate TRAIN-009 design gate

记录：

train009_design_remediation_commit

==================================================
十、TRAIN-009 delta提交
==================================================

取得train009_design_remediation_commit后，单独修改：

TRAIN-009_progress_delta.json

要求：

- 引用train009_design_remediation_commit；
- proposed_status=WAITING_FOR_DESIGN_APPROVAL；
- next_required_action=OWNER_DECISION；
- 不得引用delta自身提交SHA。

提交信息：

task19(T19-T03): bind TRAIN-009 design progress

记录：

train009_delta_commit

==================================================
十一、最终验证
==================================================

确认：

- 四个新增提交均以baseline为祖先；
- 原始两个提交保持不变；
- 每个设计修复提交不包含progress delta；
- 每个delta提交只修改对应delta；
- 两单元互不修改对方文件；
- 工作树干净；
- staged=0；
- 未修改业务代码和测试；
- 未push；
- 两个单元仍为WAITING_FOR_DESIGN_APPROVAL。

最终输出：

TERMINAL3_DESIGN_REMEDIATION_COMPLETED

并分别报告：

audit010_design_remediation_commit
audit010_delta_commit
audit010_decision_count
audit010_missing_option_c_count
audit010_unquantified_ac_count
audit010_e4_scenario_count

train009_design_remediation_commit
train009_delta_commit
train009_decision_count
train009_missing_option_c_count
train009_unquantified_ac_count
train009_e4_scenario_count

unresolved_unnumbered_decision_count
business_code_modified
test_modified
worktree_clean
push_executed
```

修复后 Terminal 0 必须分别复审，不能因为两者在同一分支就合并审批。只有各自通过后，才向项目所有者提供独立决策表。

> [!QUESTION] User
> 本轮已完成情况： - 完成 STATE-002、STATE-003、ALGO-002 实现及直接测试。 - 生成本批 E4、E5、AC 和测试运行记录：docs/spec-v3/task19/evidence/T19-B2A1/T19-B2A1_test_runs.md。 - 固定环境：Python 3.12.13、pytest 9.1.1；未使用 .envrc 或系统 Python。 - 测试结果：STATE-002 16 passed；契约 24 passed；STATE-003 联合门禁 40 passed；ALGO-002 23 passed；批次集成 63 passed；最终定向 47 passed；最终契约 36 passed。 - 默认收集确认 STATE-002 的 8 个测试；git diff --check PASS。 - 未修改任何既有文件或测试断言，仅新增 B2-A1 授权路径文件。 - 未生成 progress delta、未提交、未标记 AUDITED、未更新 LATEST.md/changelog；这些均因明确禁止修改权威/全局状态而保留。 阻塞原因： - 全仓回归在收集阶段失败： tests/spec_v3/test_model_001.py 无法从 players/humanlike/belief.py 导入 model_001_rule_baseline。 - 已确认该缺陷存在于 baseline 65e8dcb...，不是 B2-A1 引入。 - 相关文件属于其他批次/共享范围，本终端无权修改。 - 因全仓回归未通过，不能生成完成 delta、创建提交或进入 IMPLEMENTED_PENDING_INDEPENDENT_AUDIT。 下一步完整任务清单： 1. Terminal 0/对应 owner 修复或集成 baseline 的 MODEL-001 缺失符号；产出全仓可收集基线；依赖：共享文件授权；建议触发语：修复并集成 MODEL-001 baseline 缺口 2. 回到本 worktree 重跑全仓回归；产出 passed/failed/skipped 记录；依赖：步骤 1；建议触发语：baseline 缺口已修复，继续 T19-B2A1 全仓回归 3. 若全仓 PASS，刷新最终 E4/E5/AC SHA 与测试记录；产出最终证据包。 4. 生成 T19-B2A1_progress_delta.csv；产出三单元 IMPLEMENTED_PENDING_INDEPENDENT_AUDIT 提案。 5. 执行范围检查并创建本分支独立提交；依赖：全仓 PASS 和证据闭环。 6. 交由 Terminal 0 集成及独立审计；不得由本终端自行标记 AUDITED。

**ChatGPT:**

这个阻塞处理正确，不能由 Terminal 1 越权修改 `belief.py`。它证明此前 checkpoint 的：

```
include_to_exclude_required_dependency_count=0
```

结论不完整：baseline 纳入了 `test_model_001.py`，却延后了它直接依赖的 `players/humanlike/belief.py` 新实现。

这属于 Task 19 基线缺陷，不是 B2-A1 缺陷，也不应降低“全仓回归必须通过”的验收标准。

## 正确处理方式

1.  保留原 tag `task19-w01-baseline`，不得移动或覆盖。
    
2.  从原 baseline 建立独立 MODEL-001 修复 worktree。
    
3.  只修复缺失生产符号及必要直接证据。
    
4.  全仓验证通过后形成修复提交。
    
5.  创建新 tag `task19-w01-baseline-r1`。
    
6.  将修复提交按授权引入 Terminal 1。
    
7.  再继续 B2-A1 全仓回归和提交。
    

Terminal 2、3 的设计工作可以继续，不受影响。

## 基线修复提示词

```
执行 Task 19 W01 MODEL-001 baseline 缺口诊断与最小修复。

已确认失败：

tests/spec_v3/test_model_001.py

无法从：

players/humanlike/belief.py

导入：

model_001_rule_baseline

原baseline：

task19-w01-baseline
65e8dcb1679466c9e37d10e5a4299a09774332d9

问题性质：

- 缺陷存在于baseline；
- 不是B2-A1引入；
- players/humanlike/belief.py此前被DEFER_TO_LATER_BATCH；
- test_model_001.py却被纳入baseline；
- 原include→exclude依赖闭包结论需要修正；
- MODEL-001状态必须继续保持INTEGRATED；
- 不得借此升级MODEL-001审计状态。

一、创建独立修复环境

先验证以下目标不存在：

branch：
task19/w01-baseline-repair-model001

worktree：
../wt-task19-t0-model001-repair

如果不存在，允许执行：

git worktree add \
  -b task19/w01-baseline-repair-model001 \
  ../wt-task19-t0-model001-repair \
  task19-w01-baseline

不得在当前dirty主工作树修复。

如果branch或目录已存在，停止并报告，不得覆盖或删除。

二、只读诊断

在修复worktree中读取：

- tests/spec_v3/test_model_001.py
- baseline中的players/humanlike/belief.py
- MODEL-001 Locked规格
- probabilistic_model_specs.md
- MODEL-001模拟标签合同
- MODEL-001生成器审计材料
- MODEL-001信息边界合同
- Task19 checkpoint deferred记录
- 原主工作树中deferred belief.py的当前版本，只读比较
- git diff形式的来源差异

确认：

1. test_model_001.py要求的准确函数签名；
2. 输入DTO；
3. 输出DTO；
4. 概率字段和顺序；
5. deterministic fallback行为；
6. 是否只读取PlayerView/公开信息；
7. 是否禁止墙牌、对手暗手、raw seed、future truth和restricted label；
8. 缺失函数是否存在于原dirty工作树版本；
9. 该函数依赖哪些其他未纳入文件；
10. 能否形成单文件最小兼容修复。

不得直接复制整个dirty文件覆盖baseline。

三、修复决策门禁

只有满足以下条件才允许实现：

- Locked规格已唯一规定函数行为；
- test_model_001.py与Locked规格一致；
- 缺失符号属于MODEL-001已声明的确定性rule fallback；
- 不需要修改Locked/Frozen；
- 不需要修改测试断言；
- 不依赖未批准的隐藏字段；
- 不引入外部数据声明；
- 不改变MODEL-001的INTEGRATED状态；
- 可以通过最小additive修复完成。

如果任一条件不满足，停止并输出：

MODEL001_BASELINE_REPAIR_NEEDS_DECISION

四、最小实现范围

优先只允许修改：

players/humanlike/belief.py

允许新增专用测试文件：

tests/spec_v3/test_t19_model001_baseline_repair.py

禁止修改：

- tests/spec_v3/test_model_001.py既有断言；
- B2-A1代码和测试；
- Task17历史状态；
- Locked/Frozen；
- MODEL-001标签合同；
- 模拟数据；
- Task19权威tracker；
- LATEST；
- changelog；
- 其他业务文件。

如果必须修改第二个生产文件，立即停止并生成接口影响报告。

五、实现要求

model_001_rule_baseline必须：

- 使用明确版本化输入；
- 只消费批准的PlayerView/公开字段；
- 不读取GameState authority对象；
- 不读取墙牌顺序；
- 不读取对手暗手；
- 不读取raw seed；
- 不读取未来事件；
- 不读取restricted label zone；
- 不调用训练artifact；
- 不调用网络或外部AI；
- 固定输入产生字节稳定输出；
- 概率字段完整；
- 每个概率有效；
- 分类概率按合同规范化；
- malformed输入返回稳定错误；
- 不修改调用者输入；
- 不修改任何游戏状态；
- 不改变现有MODEL-001校准结论。

六、测试

使用项目批准的Python 3.12测试解释器。

依次运行：

1. 缺失导入复现；
2. tests/spec_v3/test_model_001.py；
3. 新增直接修复测试；
4. MODEL-001信息边界测试；
5. PlayerView合同测试；
6. 确定性重复测试；
7. fresh-process重复测试；
8. 全仓collection；
9. 全仓pytest。

记录：

- Python版本；
- pytest版本；
- collected；
- passed；
- failed；
- skipped；
- skip原因；
- 运行时间；
- 完整命令。

不得为了通过测试修改既有断言。

七、闭包修正

生成：

docs/spec-v3/task19/checkpoint/remediation/
  T19-W01-MODEL001_baseline_gap_report.md
  T19-W01-MODEL001_dependency_closure.json
  T19-W01-MODEL001_test_results.md
  T19-W01-MODEL001_evidence_manifest.csv
  T19-W01-MODEL001_repair_authorization.json

明确修正：

- 原deferred分类为什么错误；
- belief.py现在是否必须进入baseline；
- 是否仍有include→exclude依赖；
- 修复后的必要生产闭包；
- MODEL-001状态仍为INTEGRATED；
- Task17历史状态未修改。

八、提交门禁

只有以下条件全部满足才能提交：

- test_model_001.py PASS；
- 新直接测试PASS；
- 信息边界PASS；
- 确定性PASS；
- 全仓collection PASS；
- 全仓pytest无失败；
- 所有skip有解释且与修复无关；
- git diff --check PASS；
- 修改范围合规；
- 无P0/P1；
- 证据manifest完整；
- MODEL-001状态未升级。

提交信息：

fix(model001): restore deterministic baseline fallback

输出完整：

model001_repair_commit

不得创建或移动tag，不得push。

九、最终状态

成功时输出：

MODEL001_BASELINE_REPAIR_READY_FOR_INDEPENDENT_REVIEW

不得自行输出AUDITED或修改Task19权威状态。
```

## 修复后的集成原则

修复提交通过独立复核后：

-   不移动 `task19-w01-baseline`；
    
-   新建 `task19-w01-baseline-r1` 指向修复提交；
    
-   Terminal 1 经明确授权后 cherry-pick 修复提交；
    
-   Terminal 1 不修改该修复内容，只重跑全仓测试；
    
-   B2-A1提交只包含B2-A1自己的新增文件；
    
-   集成顺序必须是“MODEL-001基线修复 → B2-A1实现”。
    

当前 B2-A1 应记录为：

```
IMPLEMENTED_PENDING_BASELINE_REPAIR
```

而不是 `BLOCKED` 或 `IMPLEMENTED_PENDING_INDEPENDENT_AUDIT`。修复完成前不要生成最终progress delta。

> [!QUESTION] User
> RULE015_DESIGN_REMEDIATION_COMPLETED - rule015_design_commit_sha: 683dcd7d38db166b141b26d858227d2fba90b0f7 - rule015_design_changed_paths: 10 paths under docs/spec-v3/task19/design/T19-D02/ - rule015_delta_commit_sha: f9bfdf27cc08dd28a34f6bbfb6da43d71a051b6c - rule015_delta_changed_paths: docs/spec-v3/task19/progress_deltas/RULE-015_progress_delta.json - decision_count: 12 - option_c_missing_count: 0 - ac_count: 14 - unquantified_ac_count: 0 - e4_scenario_count: 4 - parameter_matrix_valid: true - visibility_matrix_valid: true - approval_form_present: true - state010_dependency_corrected: true - worktree_clean: true 原提交 7022756ef65e51eab185a7569394f0ad78d8863a 保持不变。设计提交仅包含设计文件；delta 提交仅包含 progress delta。状态仍为 WAITING_FOR_DESIGN_APPROVAL，12 项 决策均未选择且为 PENDING。未修改业务代码、测试、Locked/Frozen、Task 17、权威进度、B2-A1、LATEST 或 changelog；未 push。 本轮目标全部完成，无未完成项或范围偏差。下一步完整任务：项目所有者审议 RULE015-DEC-001～012；产出为明确的逐项选择与审批记录，依赖当前设计修复包，建议触发语： 批准 RULE-015 设计决策。

> [!NOTE] ChatGPT
> RULE-015 修复结果在结构上已满足再次进入审批预审的条件，但还不能直接执行“批准 RULE-015 设计决策”。需要 Terminal 0 确认修复内容，而不只是核对计数。
> 
> 当前状态应继续保持：
> 
> ```
> WAITING_FOR_DESIGN_APPROVAL
> business_code_authorized=false
> ```
> 
> 交给 Terminal 0：
> 
> ```
> 执行 RULE-015 修复设计包最终只读审批预审。
> 
> 提交链：
> 
> 原始设计：
> 7022756ef65e51eab185a7569394f0ad78d8863a
> 
> 设计修复：
> 683dcd7d38db166b141b26d858227d2fba90b0f7
> 
> Progress delta：
> f9bfdf27cc08dd28a34f6bbfb6da43d71a051b6c
> 
> baseline：
> 
> task19-w01-baseline
> 65e8dcb1679466c9e37d10e5a4299a09774332d9
> 
> 本任务只读。
> 
> 禁止：
> 
> - cherry-pick
> - merge
> - rebase
> - 修改文件
> - 批准决策
> - 更新权威tracker
> - 标记READY_FOR_IMPLEMENTATION
> - 实现业务代码或测试
> - push
> 
> 一、提交链与范围
> 
> 验证：
> 
> - 三个提交都存在；
> - 均以baseline为祖先；
> - 原始提交保持不变；
> - 设计修复提交只包含T19-D02设计文件；
> - delta提交只包含RULE-015_progress_delta.json；
> - delta中的design_commit_sha准确等于683dcd7...；
> - delta没有引用包含自身的commit SHA；
> - proposed_status=WAITING_FOR_DESIGN_APPROVAL；
> - next_required_action=OWNER_DECISION；
> - 没有修改业务代码、测试、Locked/Frozen、Task17、B2-A1、LATEST、changelog或权威进度。
> 
> 二、复核原有缺陷关闭情况
> 
> 逐项验证并输出PASS/FAIL：
> 
> - 独立approval form存在；
> - 12项决策均有A/B/C；
> - Option C均具体、互斥、可实施；
> - recommendation_reason完整；
> - compatibility/interface/test impact完整；
> - affected_units和blocked_units完整；
> - selected_option为空；
> - approval_status=PENDING；
> - 14条AC均有量化输入；
> - 14条AC均有操作和预期输出；
> - 错误码定义完整；
> - test oracle完整；
> - E4/E5绑定完整；
> - decision dependency完整；
> - 机械PASS规则完整；
> - 参数矩阵独立有效；
> - 可见性矩阵独立有效；
> - E4分别定义NORMAL、BOUNDARY、HARD_FAILURE、DETERMINISM；
> - STATE-010已准确表述为AUDITED；
> - RULE-015不修改STATE-010已审计语义；
> - GP-011/012/013采用已批准接口方案或明确决策分类。
> 
> 三、语义一致性检查
> 
> 重点检查：
> 
> 1. contains替代语义是否避免双计；
> 2. exclusive优先级是否稳定；
> 3. compatible与independent是否有明确差异；
> 4. 关系解析顺序是否唯一；
> 5. cap发生在关系解析前还是后；
> 6. unknown和disabled fan错误语义；
> 7. 关系矩阵是否要求完整、对称或有向；
> 8. contains图是否禁止环；
> 9. canonical ordering是否跨进程稳定；
> 10. RULE-015是否保持纯查询；
> 11. authority version是否不变；
> 12. 现有compute_fan兼容适配是否明确；
> 13. SCORE-002/004/005及HEUR-011影响是否完整；
> 14. 性能AC是否给出固定环境、warmup、样本数、P95方法和异常计入方式。
> 
> 四、决策可审批性
> 
> 对RULE015-DEC-001～012分别输出：
> 
> decision_id
> question
> option_a
> option_b
> option_c
> recommended_option
> recommendation_reason
> preferred_option_risk
> compatibility_impact
> interface_impact
> test_impact
> affected_units
> blocked_units
> terminal0_recommendation
> 
> 不得替项目所有者选择。
> 
> 如果推荐选项依赖其他未批准决策，必须列出依赖关系和建议审批顺序。
> 
> 五、最终结论
> 
> 只允许输出：
> 
> RULE015_DESIGN_READY_FOR_OWNER_DECISION
> 
> 或：
> 
> RULE015_DESIGN_REVIEW_FAILED
> 
> 如果通过，生成一份项目所有者可直接填写的决策表：
> 
> decision_id,selected_option,owner_comment
> 
> selected_option保持空。
> 
> 本轮不得集成或更新进度。
> ```
> 
> 如果结论为 `RULE015_DESIGN_READY_FOR_OWNER_DECISION`，再把12项完整决策表发给我或上传以下文件：
> 
> -   `RULE-015_decision_matrix.csv`
>     
> -   `RULE-015_approval_form.md`
>     
> -   `RULE-015_interface_impact.csv`
>     
> 
> 届时才能判断是否适合12项全部采用推荐选项，还是需要逐项调整。

**ChatGPT:**

预审结果合理。RULE-015 只剩两个实质性 P1，已经不需要再次重写整个设计包。

E5 口径应沿用 B1-A/B1-B 已采用的标准：

```
8 semantic + 4 test + 2 evidence = 14行
```

AC 不应额外生成14行 E5。AC 应通过每条 E5 的 `acceptance_ids` 外键覆盖，最终验证14个 AC 都至少被一行 E5 引用。这样不会产生14/26/28三种口径。

## Terminal 2 最终修复提示词

```
执行 RULE-015 第二轮、最终审批入口修复。

当前分支：

task19/w01-design-deterministic

现有提交链：

7022756ef65e51eab185a7569394f0ad78d8863a
683dcd7d38db166b141b26d858227d2fba90b0f7
f9bfdf27cc08dd28a34f6bbfb6da43d71a051b6c

当前结论：

RULE015_DESIGN_REVIEW_FAILED

剩余阻塞：

R015-R2-F001：E5覆盖口径矛盾
R015-R2-F002：AC-12缺少冻结性能环境
R015-R2-F003：E4性能环境引用不具体

本任务只修复上述问题。

禁止：

- 修改业务代码；
- 修改测试；
- 修改Locked/Frozen；
- 修改STATE-010；
- 修改Task17；
- 修改权威tracker；
- 修改B2-A1；
- 修改其他设计语义；
- 改变12项决策的A/B/C内容；
- 预填selected_option；
- 批准DEC-012；
- amend或重写已有提交；
- merge、rebase、cherry-pick、push。

一、统一E5口径

RULE-015的E5必须固定为14行：

- 8条semantic delta；
- 4条test delta；
- 2条evidence delta。

禁止为AC另外生成14条E5行。

E5每行必须包含：

unit_id
delta_id
delta_type
source_reference
acceptance_ids
code_symbols
test_references
runtime_evidence_ids
artifact_hash_rule
expected_result

delta_type只能是：

SEMANTIC
TEST
EVIDENCE

行数必须为：

semantic=8
test=4
evidence=2
total=14

AC覆盖规则：

- AC-01～AC-14通过acceptance_ids被E5引用；
- 每个AC至少被一行E5覆盖；
- 不要求每个AC单独形成E5行；
- 不允许未知AC ID；
- 不允许遗漏任何evidence delta；
- 不允许重复delta_id；
- E5行数和AC覆盖数必须分别计算。

修正以下全部相关表述：

- RULE-015_evidence_deltas.csv
- RULE-015_acceptance_matrix.csv中的AC-14
- RULE-015_e5计划或矩阵；
- RULE-015_design_review.md；
- RULE-015_approval_form.md；
- 其他提到26或28行E5的设计文件。

最终验证：

e5_row_count=14
semantic_e5_count=8
test_e5_count=4
evidence_e5_count=2
unique_delta_id_count=14
covered_ac_count=14
missing_ac_reference_count=0
unknown_ac_reference_count=0
missing_evidence_delta_count=0

二、生成冻结性能环境manifest

新增设计文件：

docs/spec-v3/task19/design/T19-D02/RULE-015_performance_environment.json

不得凭记忆填写环境。

使用只读命令采集当前批准测试环境：

- Python实现、完整版本和build；
- OS名称、版本和build；
- CPU架构；
- CPU型号；
- 逻辑CPU数；
- 计时器；
- pytest版本；
- 当前解释器绝对路径只用于采集，不写入最终可移植manifest；
- 不执行direnv allow；
- 不安装依赖；
- 不运行网络命令。

Manifest至少包含：

schema_version
environment_id
captured_at
os_name
os_version
os_build
architecture
cpu_model
logical_cpu_count
python_implementation
python_version
python_build
pytest_version
timer
process_count
thread_count
hash_seed_policy
warmup_iterations
measurement_iterations
repeat_count
percentile_method
exception_treatment
load_isolation
input_fixture_reference
input_fixture_sha256
threshold_decision_id
threshold_status
allowed_environment_variation
informational_environment_policy

固定规则：

- process_count=1；
- thread_count=1；
- timer=time.perf_counter_ns；
- percentile_method=nearest-rank P95，明确排序和索引规则；
- 异常、超时按正无穷处理；
- input fixture必须是稳定、版本化、带SHA-256的代表性复合番输入；
- threshold_decision_id=RULE015-DEC-012；
- threshold_status=PENDING_OWNER_DECISION；
- 不得在批准前固定2/5/10 ms之一；
- reference环境上的阈值用于硬验收；
- 非reference环境只生成informational结果，不得据此判FAIL；
- 不得把本机绝对路径写入可移植环境身份；
- 不得包含用户名、token或秘密。

environment_id必须根据规范化环境字段生成稳定ID，例如：

RULE015-PERF-REF-V1-<canonical-hash-prefix>

不得手写随机ID。

三、修正AC-12

AC-12必须引用：

RULE-015_performance_environment.json中的environment_id

并定义：

- 固定输入fixture及SHA-256；
- warmup次数；
- measurement次数；
- repeat次数；
- 单进程、单线程；
- 计时器；
- P95算法；
- 异常处理；
- DEC-012阈值选择；
- reference环境硬门禁；
- 非reference环境informational；
- 环境不匹配时的稳定结果：
  ENVIRONMENT_MISMATCH / NOT_AUTHORITATIVE
- 在DEC-012未批准前：
  AC-12=WAITING_APPROVAL
- 不得预先标记PASS。

四、修正E4性能引用

NORMAL和适用的DETERMINISM E4必须引用同一个：

performance_environment_id

禁止继续使用：

AC-12 environment
current machine
runtime environment
approved environment

等模糊描述。

E4必须记录：

performance_environment_id
fixture_sha256
warmup_iterations
measurement_iterations
repeat_count
observed_p95_ns
selected_threshold_ns
threshold_decision_id
authoritative_environment_match
performance_result

在DEC-012未批准前：

selected_threshold_ns=null
performance_result=WAITING_APPROVAL

五、审批表保持PENDING

确认：

- RULE015-DEC-001～012仍为PENDING；
- selected_option全部为空；
- DEC-012推荐可以保持B，但不得自动选择；
- approval_status=PENDING；
- business_code_authorized=false；
- RULE-015状态仍为WAITING_FOR_DESIGN_APPROVAL。

六、设计修复提交

本提交只允许修改T19-D02设计文件，并新增性能环境manifest。

不得修改progress delta。

验证：

- E5固定14行；
- 14个AC全部覆盖；
- 性能环境manifest有效JSON；
- 无本机绝对路径；
- 无秘密；
- AC-12引用准确environment_id；
- E4引用同一environment_id；
- DEC-012仍PENDING；
- git diff --check通过。

提交信息：

task19(T19-D02): close RULE-015 approval gate

记录完整SHA：

rule015_final_design_commit_sha

七、metadata提交

取得rule015_final_design_commit_sha后，只修改：

docs/spec-v3/task19/progress_deltas/RULE-015_progress_delta.json

要求：

- design_commit_sha更新为rule015_final_design_commit_sha；
- proposed_status=WAITING_FOR_DESIGN_APPROVAL；
- next_required_action=OWNER_DECISION；
- generated_at更新；
- 不得记录delta自身提交SHA；
- 不得申请READY_FOR_IMPLEMENTATION。

提交信息：

task19(T19-D02): bind final RULE-015 design progress

记录：

rule015_final_delta_commit_sha

八、最终验证

确认：

- 既有三个提交不变；
- 两个新提交均以baseline为祖先；
- design提交不修改progress delta；
- delta提交只修改progress delta；
- 工作树干净；
- staged=0；
- 未修改业务代码或测试；
- 未push。

最终输出：

RULE015_FINAL_DESIGN_GATE_REMEDIATED

并报告：

rule015_final_design_commit_sha
rule015_final_delta_commit_sha
e5_row_count
semantic_e5_count
test_e5_count
evidence_e5_count
covered_ac_count
missing_ac_reference_count
performance_environment_id
performance_manifest_valid
ac12_environment_reference_valid
e4_environment_reference_valid
dec012_status
worktree_clean
```

完成后再做一次范围很小的 Terminal 0 复审，只检查这三个 finding。通过后即可正式审批12项决策。DEC-001～011目前都倾向推荐 A；DEC-012推荐 B，但应等环境 manifest 通过后再最终确认。

> [!QUESTION] User
> MODEL001_BASELINE_REPAIR_READY_FOR_INDEPENDENT_REVIEW model001_repair_commit=7b8f27e38a3bbb158b276d478024eea70354ef8b 本轮已完成情况： - 在独立 branch task19/w01-baseline-repair-model001 和 worktree ../wt-task19-t0-model001-repair 完成修复。 - 仅修改 /Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t0-model001-repair/players/humanlike/belief.py，新增专用直接测试及五份 remediation 证据。 - 修复 include→exclude 依赖闭包：包含 test_model_001.py 时，belief.py 必须纳入 baseline。 - MODEL-001 保持 INTEGRATED，未升级为 AUDITED；未修改 Task 17、Locked/Frozen、tracker、LATEST 或 changelog。 - 全仓 collection：458 tests collected。 - 全仓回归：457 passed、0 failed、1 unrelated macOS Tk skip，42.31s。 - git diff --check、范围、manifest hash、JSON/CSV 校验全部通过；提交后 worktree 干净。 - 未创建或移动 tag，未 push。 证据入口：/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t0-model001-repair/docs/spec-v3/task19/checkpoint/remediation/T19-W01- MODEL001_baseline_gap_report.md。 下一步完整任务清单： 1. 对 commit 7b8f27e 执行独立审查；产出 repair review 结论；建议触发语：独立审查 MODEL-001 baseline repair commit 7b8f27e 2. Terminal 0 按授权集成修复提交；依赖：独立审查通过。 3. 在 B2-A1 worktree 重跑全仓回归；产出解除 blocker 的完整结果；建议触发语：MODEL-001 repair 已集成，继续 T19-B2A1 4. 刷新 B2-A1 E4/E5/AC、生成 progress delta 并创建独立提交。 5. 由 Terminal 0 集成 B2-A1 并安排独立审计；本终端不得自行标记 AUDITED。

**ChatGPT:**

修复结果已达到独立审查入口，但不能仅凭开发分支自报结果创建 `task19-w01-baseline-r1`。下一步应由独立审查会话只读检查提交内容、信息边界、测试真实性和证据一致性。

## 独立审查提示词

```
独立审查 MODEL-001 baseline repair commit。

目标提交：

7b8f27e38a3bbb158b276d478024eea70354ef8b

原baseline：

task19-w01-baseline
65e8dcb1679466c9e37d10e5a4299a09774332d9

预期状态：

MODEL-001=INTEGRATED

本任务为独立只读审查。

禁止：

- 修改业务代码；
- 修改测试；
- 修改证据；
- cherry-pick；
- merge；
- rebase；
- 创建或移动tag；
- 修改Task17；
- 修改Task19权威tracker；
- 标记MODEL-001为AUDITED；
- push。

一、提交身份与范围

验证：

- 提交存在；
- parent精确等于原baseline，或明确列出实际parent；
- 原baseline是祖先；
- branch为task19/w01-baseline-repair-model001；
- 列出完整changed paths；
- 生产代码只修改players/humanlike/belief.py；
- 只新增专用修复测试和五份remediation证据；
- 没有修改test_model_001.py既有断言；
- 没有修改Locked/Frozen、Task17、tracker、LATEST或changelog；
- 工作树干净；
- 未push。

任何范围外业务修改均阻止通过。

二、缺陷复现与因果验证

在原baseline上只读确认：

- tests/spec_v3/test_model_001.py导入失败；
- 缺失符号为model_001_rule_baseline；
- 失败不是B2-A1引入；
- belief.py此前错误地被DEFER_TO_LATER_BATCH；
- test_model_001.py已被纳入baseline；
- 原include→exclude依赖闭包结论确实错误。

在修复提交上确认：

- 导入成功；
- 没有通过删除、跳过或弱化测试解决；
- 修复直接针对缺失生产符号；
- 没有隐藏其他依赖缺口。

三、实现规格检查

检查model_001_rule_baseline的准确签名和行为。

必须符合MODEL-001合同：

输出：

- p_cleared；
- dominant_suit_probs；
- shape_probs；
- 版本和必要元数据。

验证：

- p_cleared范围合法；
- dominant_suit_probs顺序固定；
- shape_probs顺序固定；
- 每组概率非负；
- 概率和满足合同；
- mixed/other行为明确；
- malformed输入返回稳定错误；
- 不修改调用者输入；
- 固定输入输出稳定；
- 不依赖网络、AI或模型artifact；
- 不以模拟标签作为运行时truth；
- 不改变现有fallback语义之外的功能。

四、信息边界

必须证明只读取批准的PlayerView或公开字段。

禁止读取：

- GameState完整authority；
- 对手暗手；
- 墙牌顺序；
- 未公开物理牌；
- raw seed；
- future event；
- 终局回填truth；
- restricted_label_zone；
- TrainingTruth；
- oracle；
- 模型训练artifact。

执行静态import/符号检查和动态隐藏字段扰动测试。

验证同一可见状态下：

- 改变对手暗手不改变输出；
- 改变墙牌顺序不改变输出；
- 改变raw seed不改变输出；
- 改变restricted labels不改变输出；
- 改变公开信息时允许按规则变化。

任何隐藏信息泄漏均为P0并阻止通过。

五、确定性和兼容性

验证：

- 同输入100次结果一致；
- fresh-process结果一致；
- mapping插入顺序变化不改变输出；
- worker/调用顺序变化不改变输出；
- canonical序列化字节稳定；
- 旧调用方兼容；
- 未引入随机状态；
- 未改变MODEL-001模拟标签合同；
- 未改变MODEL-001状态。

六、测试复跑

使用与修复报告相同的Python 3.12环境。

独立运行：

1. 专用修复测试；
2. tests/spec_v3/test_model_001.py；
3. PlayerView及信息边界测试；
4. MODEL-001相关合同测试；
5. 全仓collection；
6. 全仓pytest；
7. 至少一次fresh-process确定性运行。

记录：

- Python版本；
- pytest版本；
- 完整命令；
- collected；
- passed；
- failed；
- skipped；
- skip node ID；
- skip原因；
- duration。

预期参考：

collection=458
passed=457
failed=0
skipped=1

如果数量不同，必须解释测试树或环境差异，不能仅凭“全绿”通过。

macOS Tk skip必须确认与MODEL-001无关。

七、证据检查

检查五份remediation证据：

- baseline gap report；
- dependency closure；
- test results；
- evidence manifest；
- repair authorization。

确认：

- JSON/CSV可解析；
- SHA-256均为64位小写十六进制；
- manifest哈希与当前提交树内容一致；
- test命令和结果一致；
- 没有使用当前dirty主工作树文件替代提交树文件；
- include→exclude必要依赖修正为belief.py纳入；
- MODEL-001仍为INTEGRATED；
- Task17历史状态未修改。

八、缺陷和结论

输出finding表：

finding_id
severity
affected_file
affected_symbol
evidence
required_fix
blocking_scope

只有以下条件全部满足才能输出：

MODEL001_BASELINE_REPAIR_INDEPENDENT_REVIEW_PASS

- 修改范围合规；
- 缺陷因果成立；
- 实现符合合同；
- 信息边界通过；
- 确定性通过；
- 兼容性通过；
- 专用测试通过；
- 全仓collection通过；
- 全仓无失败；
- skip已解释且无关；
- 证据哈希一致；
- 无开放P0/P1；
- MODEL-001保持INTEGRATED；
- Task17历史状态未修改。

否则输出：

MODEL001_BASELINE_REPAIR_INDEPENDENT_REVIEW_FAIL

本任务不得创建tag或执行集成。
```

审查通过后的顺序应是：

1.  创建新 annotated tag `task19-w01-baseline-r1`，精确指向 `7b8f27e...`，不移动原 tag。
    
2.  将修复提交引入 Terminal 1 的 B2-A1 分支。
    
3.  Terminal 1 重跑全仓回归。
    
4.  B2-A1 刷新E4/E5/AC并提交。
    
5.  Terminal 0按“baseline repair → B2-A1”顺序集成。
    

当前 MODEL-001 仍然只是 `INTEGRATED`；这次修复只修复基线闭包，不等于完成其校准审计。

> [!QUESTION] User
> TERMINAL3_DESIGN_REMEDIATION_COMPLETED - audit010_design_remediation_commit: 123118d0ca42dae0a455088ccc50668ccf631b00 - audit010_delta_commit: 589e5aa13a5fa37e10a9fe2754969a8e28b6c37e - audit010_decision_count: 5 - audit010_missing_option_c_count: 0 - audit010_unquantified_ac_count: 0 - audit010_e4_scenario_count: 4 - train009_design_remediation_commit: 644d9d820448b5de6ac1d0821ddf384756502883 - train009_delta_commit: 1c1da899d361ed0e927a16a4c4afcfd7876e6e86 - train009_decision_count: 7 - train009_missing_option_c_count: 0 - train009_unquantified_ac_count: 0 - train009_e4_scenario_count: 4 - unresolved_unnumbered_decision_count: 0 - business_code_modified: false - test_modified: false - worktree_clean: true - staged_count: 0 - push_executed: false 本轮已完成： - 两单元均补齐字段级 DTO、错误码、接口/参数/可见性矩阵、量化 AC、四类独立 E4、逐增量 E5 和 PENDING 审批表。 - TRAIN-009 按实际 STREAMS 闭集修正 RNG 设计；不存在虚构 domain stream。 - 四个新提交均以 task19-w01-baseline 为祖先；原始两个提交未重写。 - 两个 delta 只引用前置设计提交，不循环引用自身。 - 两单元仍为 WAITING_FOR_DESIGN_APPROVAL，下一步均为 OWNER_DECISION。 下一步完整任务清单： 1. Terminal 0 独立复核四个提交和设计门禁；产出复审结论；建议触发语：复审 Terminal 3 设计门禁修复 2. 项目负责人分别选择 AUDIT-010 五项、TRAIN-009 七项决策；产出独立审批记录；建议触发语：审批 AUDIT-010 和 TRAIN-009 决策 3. 审批后另行判断实施授权；当前不得标记 READY_FOR_IMPLEMENTATION 或 AUDITED。

**ChatGPT:**

修复结果已达到再次复审入口。TRAIN-009 从6项增加为7项决策是合理的，只要新增项用于消除原先未编号的 Observation/RNG 接口歧义，并已记录依赖影响。

当前仍不能直接审批，先执行 Terminal 0 的最终只读复审。

```
复审 Terminal 3 设计门禁修复。

baseline：

task19-w01-baseline
65e8dcb1679466c9e37d10e5a4299a09774332d9

原始提交：

AUDIT-010：
74a39ca23879eb04ea47a12f4b77224f4251b433

TRAIN-009：
8632d128f005694c38f1d0e5c0e1092afd22a257

修复提交：

AUDIT-010 design：
123118d0ca42dae0a455088ccc50668ccf631b00

AUDIT-010 delta：
589e5aa13a5fa37e10a9fe2754969a8e28b6c37e

TRAIN-009 design：
644d9d820448b5de6ac1d0821ddf384756502883

TRAIN-009 delta：
1c1da899d361ed0e927a16a4c4afcfd7876e6e86

本任务只读。

禁止：

- 修改文件；
- cherry-pick；
- merge；
- rebase；
- 批准决策；
- 修改权威tracker；
- 标记READY_FOR_IMPLEMENTATION；
- 实现业务代码或测试；
- push。

一、提交链和修改范围

验证六个提交：

- 均存在；
- 均以baseline为祖先；
- 原始提交没有被重写；
- 每个design remediation提交只修改对应单元设计目录；
- 每个delta提交只修改对应progress delta；
- delta中的design_commit_sha准确指向前置design remediation commit；
- delta没有引用包含自身的commit SHA；
- 两个单元之间没有交叉修改；
- 没有业务代码、测试、Locked/Frozen、Task17、B2-A1、RULE-015、LATEST、changelog或权威tracker修改。

记录实际parent链，并给出未来可安全cherry-pick顺序，但本轮不得执行。

二、AUDIT-010门禁复核

必须分别验证：

- semantic delta=8；
- test delta=4；
- evidence delta=2；
- AC=14；
- decision=5；
- missing Option C=0；
- unquantified AC=0；
- E4场景=4；
- E5口径唯一；
- approval form=PENDING；
- business_code_authorized=false。

检查5项决策均包含：

decision_id
question
option_a
option_b
option_c
recommended_option
recommendation_reason
compatibility_impact
interface_impact
test_impact
affected_units
blocked_units
selected_option
approval_status

要求：

- A/B/C互斥、具体、可实施；
- selected_option为空；
- approval_status=PENDING；
- 不存在正文中的未编号决策。

检查字段级DTO：

- 字段名；
- 类型；
- 必填；
- 默认值；
- null语义；
- 范围；
- 枚举；
- canonicalization；
- visibility；
- validation error。

重点检查：

1. 审计器只读业务authority；
2. 审计失败不回滚已提交业务状态；
3. finding append-only；
4. finding部分写入失败语义；
5. retention spool失败和恢复；
6. outbox幂等；
7. changed-payload duplicate拒绝；
8. signer只存key reference，不包含私钥；
9. developer与auditor身份不可相同；
10. capability可机械验证；
11. self-audit稳定拒绝；
12. AUDIT-014 adapter接口分类；
13. 每个共享接口有唯一owner；
14. 无真实token、私钥或本机秘密。

三、TRAIN-009门禁复核

必须验证：

- semantic delta=8；
- test delta=4；
- evidence delta=2；
- AC=14；
- decision=7；
- missing Option C=0；
- unquantified AC=0；
- E4场景=4；
- E5口径唯一；
- approval form=PENDING；
- business_code_authorized=false。

解释新增第7项决策：

- 对应哪一个原未编号歧义；
- 为什么必须独立决策；
- 与原6项是否重复；
- affected/blocked units；
- 审批顺序。

检查实际：

engine/rng_v2.py::STREAMS

确认：

- 设计引用的stream真实存在；
- 不存在虚构domain stream；
- 如果新增stream，明确为ADDITIVE_INTERFACE；
- 如果改变旧stream语义，明确为BREAKING_CHANGE并阻止实现；
- RNG coordinate字段完整；
- 相同episode跨进程稳定；
- worker调度顺序不改变结果；
- worker数量变化语义明确；
- raw seed不进入策略视图。

检查Observation接口：

- 所有替代行为均有编号decision；
- compatible adapter/additive/breaking分类准确；
- 不得隐式修改Frozen schema。

检查artifact事务：

1. temporary write；
2. 完整校验；
3. fsync；
4. atomic rename；
5. manifest/hash最后发布；
6. partial artifact策略；
7. 重启恢复；
8. orphan temporary处理；
9. incomplete manifest拒绝；
10. duplicate run幂等；
11. changed-payload duplicate拒绝；
12. 失败不污染已发布版本；
13. restricted artifact物理隔离；
14. replay拒绝不完整artifact。

检查MODEL-001门禁：

- 外部有效性只限制校准和外部效果声明；
- 不阻塞规则域随机化实现；
- 不阻塞确定性replay；
- 模拟数据不被描述为现实有效性；
- MODEL-001状态保持INTEGRATED。

四、AC/E4/E5机械性

两个单元分别检查：

- 14条AC全部具有量化输入；
- 14条AC全部具有操作、输出和错误码；
- test oracle完整；
- visibility oracle完整；
- determinism oracle完整；
- performance oracle完整；
- decision dependency完整；
- pass_rule可以机械执行；
- 每个AC至少被测试或E4/E5绑定；
- E4分别为NORMAL、BOUNDARY、HARD_FAILURE、DETERMINISM；
- 每个E4包含生产调用点、前态、输入、操作、输出、错误码、版本、延迟、哈希规则；
- E5覆盖8 semantic、4 test、2 evidence；
- 不允许遗漏evidence delta；
- 不允许未知AC引用。

分别输出：

semantic_count
test_delta_count
evidence_delta_count
ac_count
unquantified_ac_count
missing_error_oracle_count
missing_test_binding_count
missing_evidence_binding_count
e4_scenario_count
e5_row_count
missing_e5_delta_count
unknown_ac_reference_count

五、progress delta

分别确认：

- proposed_status=WAITING_FOR_DESIGN_APPROVAL；
- next_required_action=OWNER_DECISION；
- design_commit_sha正确；
- 不含自身SHA循环；
- 不请求READY_FOR_IMPLEMENTATION；
- 不请求AUDITED；
- generated_by=Terminal 3；
- 两个delta可以独立吸收。

六、独立结论

必须分别输出：

AUDIT010_DESIGN_READY_FOR_OWNER_DECISION
或
AUDIT010_DESIGN_REVIEW_FAILED

TRAIN009_DESIGN_READY_FOR_OWNER_DECISION
或
TRAIN009_DESIGN_REVIEW_FAILED

不得用一个合并结论代替。

如果失败，输出逐项finding。

如果通过，分别输出完整所有者决策表：

decision_id
question
option_a
option_b
option_c
recommended_option
recommendation_reason
approval_order
selected_option
owner_comment

selected_option和owner_comment必须为空。

七、集成建议

只输出未来建议，不执行：

- 六个现有提交的cherry-pick顺序；
- owner approval commit位置；
- progress delta吸收时点；
- 实施授权前置条件。

本轮不得修改或集成任何内容。
```

只有两个单元分别得到 `DESIGN_READY_FOR_OWNER_DECISION` 后，才进行所有者审批。即使其中一个通过、另一个失败，也应允许通过的单元单独审批，不能强制捆绑。

> [!QUESTION] User
> MODEL001_BASELINE_REPAIR_INDEPENDENT_REVIEW_FAIL 修改范围、因果链、信息边界、确定性和测试均通过，但发现一个 P1 合同缺陷及一个 P1 证据闭包缺陷，因此不能独立签署通过。 Findings finding_id M001-R-F001 severity P1 affected_file players/humanlike/belief.py affected_symbol model_001_rule_baseline evidence Locked 要求 entropy ∈ [0, ln K]；无证据输入实际返回 2.995732，超过 ln(5)=1.609438 required_fix 分别定义各任务 entropy，或按合同明确的联合分布计算并给出合法上界；增加准确边界测试 blocking_scope MODEL-001 contract ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── finding_id M001-R-F002 severity P1 affected_file T19-W01-MODEL001_evidence_manifest.csv affected_symbol remediation evidence closure evidence Manifest 只有 6 行，未记录 baseline gap report、dependency closure、test results、repair authorization 及 manifest 自身的哈希/非循环规则 required_fix 补充五份 remediation 工件的完整 SHA-256；manifest 自身采用明确非循环规则 blocking_scope Evidence integrity ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── finding_id M001-R-F003 severity P2 affected_file tests/spec_v3/test_t19_model001_baseline_repair.py affected_symbol probability metadata tests evidence 测试只验证概率范围与分布和，没有验证 uncertainty 合同范围、固定数组语义标签和 mixed/other 映射 required_fix 增加 entropy、类别顺序、mixed/other 及最大/最小证据测试 blocking_scope Direct test completeness 提交与范围 - Commit：7b8f27e38a3bbb158b276d478024eea70354ef8b - Parent：精确等于 baseline 65e8dcb1679466c9e37d10e5a4299a09774332d9 - Branch：task19/w01-baseline-repair-model001 - Worktree：clean - 生产修改：仅 players/humanlike/belief.py - 新增：1 个专用测试、5 个 remediation 工件 - tests/spec_v3/test_model_001.py：未修改 - Locked/Frozen、Task 17、tracker、LATEST、changelog：未修改 - MODEL-001：保持 INTEGRATED 因果验证 - 原 baseline 独立归档运行准确复现： - ImportError - 缺失符号：model_001_rule_baseline - Baseline include 包含 tests/spec_v3/test_model_001.py。 - Baseline deferred 清单包含 players/humanlike/belief.py。 - 因此原 include→exclude 闭包结论确实错误。 - 修复直接增加缺失生产符号，未删除、skip 或弱化既有测试。 - 问题早于 B2-A1，B2-A1 未参与修改。 实现检查 通过： - p_cleared 在 [0,1]。 - dominant_suit_probs 为固定长度 4，非负且和为 1。 - shape_probs 为固定长度 5，非负且和为 1。 - 输入不变。 - malformed schema/version 返回稳定 PolicyInputError。 - 无网络、AI、模型 artifact、RNG 或训练标签运行时依赖。 - 输出按 seat 排序。 - 规则 fallback 版本和输入版本存在。 - 固定公开输入稳定。 失败： - uncertainty 将 4 类 suit entropy 与 5 类 shape entropy直接相加，最大值为 ln(4)+ln(5)=ln(20)；Locked 当前要求 entropy [0,lnK]，现输出没有说明 K=20，且字段是 单一标量。 - mixed/other 的数组位置只能从 Locked 文档推断，输出没有类别顺序元数据；这是测试完整性风险。 信息边界 通过： - 静态 import 未发现 GameState、网络、AI、模型 artifact 或随机状态。 - 禁止字段递归拒绝： - 对手暗手 - 墙序 - raw seed - future event - restricted label - TrainingTruth/oracle - PlayerView/visibility 合同测试通过。 - 隐藏字段无法进入正常请求；注入时返回 FORBIDDEN_FEATURE。 - 改变公开弃牌允许并确实改变 p_cleared。 - 未发现隐藏信息泄漏，P0 finding 为 0。 确定性与兼容性 - 同输入 100 次：1 个唯一 canonical 输出。 - Mapping 插入顺序置换：输出一致。 - Fresh process 5 次：同一 SHA-256 f58cc0e5a0c28cbc4c02f234046d6697b3c9c686af351ea7d86786d6c725c2a7 - 专用报告中的另一固定输入复现 SHA-256： fe9f7c75eccace910ec4d87c79dd66e1b4b7a8a38d5038995e83640bc1e2abdd - 未引入全局 RNG、缓存隐状态或 worker 顺序依赖。 - 既有 MODEL-001 调用形式兼容。 - 模拟标签合同未修改。 测试结果 环境： - Python 3.12.13 - pytest 9.1.1 结果： Gate Result ━━━━━━━━━━━━━━━━━━━━━━━━━━ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Baseline reproduction ImportError，符合缺陷描述 ────────────────────────── ───────────────────────────────── 专用修复测试 9 passed ────────────────────────── ───────────────────────────────── 既有 MODEL-001 测试 1 passed ────────────────────────── ───────────────────────────────── PlayerView/边界/合同组合 34 passed ────────────────────────── ───────────────────────────────── Collection 458 collected ────────────────────────── ───────────────────────────────── 沙箱全仓运行 453 passed, 4 failed, 1 skipped ────────────────────────── ───────────────────────────────── 非沙箱独立全仓复跑 457 passed, 0 failed, 1 skipped ────────────────────────── ───────────────────────────────── Fresh process 5/5 hash 一致 4 个沙箱失败均为外部 worktree 写权限 PermissionError，非业务失败；非沙箱同命令全部通过。 唯一 skip： - tests/test_f0013_dirty_update.py:122 - 原因：macOS Tk 在 Tk() 构造时可能中止进程。 - 与 MODEL-001 无关。 证据检查 - 两个 JSON 可解析。 - Manifest 中现有 6 个 SHA-256 均为 64 位小写十六进制，并与目标 commit tree 完全一致。 - 未使用 dirty 主工作树文件。 - 但 manifest 没有覆盖五份 remediation 证据自身，未满足本次要求的完整证据包闭包。 本轮已完成情况：完成 commit-tree、baseline 缺陷复现、合同、信息边界、确定性、兼容性、测试及证据独立审查；未修改、集成、push 或改变状态。 下一步完整任务清单： 1. 修正 uncertainty 合同实现并补齐 entropy 边界测试。 2. 明确并测试 dominant suit 与 shape 数组顺序、mixed/other 行为。 3. 补齐五份 remediation 工件的 provenance manifest。 4. 重新运行专用、合同、collection 和全仓测试。 5. 提交修复后重新执行独立审查；MODEL-001 仍保持 INTEGRATED。

**ChatGPT:**

独立审查发现的 entropy 问题不是普通代码错误，而是 Locked 文档存在解释缺口：

```
输出只有一个 uncertainty 字段
但同时存在：
p_cleared（二分类）
dominant_suit_probs（4分类）
shape_probs（5分类）
并规定 entropy ∈ [0, ln K]
却没有定义单一 uncertainty 对应哪个 K
```

因此不能直接把当前值截断到 `ln(5)`，也不能随意只保留某一个任务的熵。

## 推荐合同解释

建议采用联合多任务熵：

```
uncertainty
= H(cleared)
+ H(dominant_suit)
+ H(shape)
```

把三个任务看作独立输出的联合分布：

```
K = 2 × 4 × 5 = 40
```

因此：

```
uncertainty ∈ [0, ln(40)]
```

当前实现只计算了：

```
ln(4) + ln(5) = ln(20)
```

还遗漏了 `p_cleared` 的二分类熵。

同时增加可解释元数据：

```
uncertainty_components:
  cleared_entropy
  dominant_suit_entropy
  shape_entropy
  joint_entropy
  joint_class_count=40
```

并明确类别顺序：

```
dominant_suit_labels:
[wan, tong, tiao, mixed]

shape_labels:
[standard, seven_pairs, all_pongs, pure_suit, other]
```

这能保持原来的单一 `uncertainty` 数值字段，同时用附加字段解释其组成，兼容性相对最好。

建议项目所有者先明确批准：

```
批准 MODEL-001 uncertainty 采用联合多任务熵方案：
uncertainty=H(cleared)+H(dominant_suit)+H(shape)，K=40；
保留标量 uncertainty，并新增分项 entropy 和固定类别顺序元数据。
```

批准后交给修复终端：

```
执行 MODEL-001 baseline repair 审计缺陷修复。

目标分支：

task19/w01-baseline-repair-model001

原修复提交：

7b8f27e38a3bbb158b276d478024eea70354ef8b

独立审查结论：

MODEL001_BASELINE_REPAIR_INDEPENDENT_REVIEW_FAIL

待修复：

M001-R-F001：uncertainty合同
M001-R-F002：证据manifest闭包
M001-R-F003：类别顺序和entropy测试

已批准合同解释：

1. uncertainty是三个任务独立输出联合分布的熵；
2. uncertainty =
   H(cleared) +
   H(dominant_suit) +
   H(shape)；
3. K=2×4×5=40；
4. uncertainty范围为[0,ln(40)]；
5. 保留标量uncertainty；
6. 新增分项entropy元数据；
7. dominant suit顺序固定为：
   wan,tong,tiao,mixed；
8. shape顺序固定为：
   standard,seven_pairs,all_pongs,pure_suit,other。

禁止：

- 修改Locked/Frozen原文件；
- 修改test_model_001.py既有断言；
- 修改Task17；
- 修改MODEL-001状态；
- 修改tracker、LATEST或changelog；
- 引入网络、AI、模型artifact或restricted labels；
- amend原提交；
- 创建或移动tag；
- push。

一、生成解释决策记录

新增：

docs/spec-v3/task19/checkpoint/remediation/MODEL001_uncertainty_interpretation_approval.md

记录：

- 原始歧义；
- 批准方案；
- 联合分布假设；
- K=40；
- 数学定义；
- 数值稳定规则；
- 类别顺序；
- 兼容性；
- 测试要求；
- MODEL-001继续为INTEGRATED；
- 不修改Locked原文。

二、修正实现

只修改：

players/humanlike/belief.py

定义二分类熵：

H(cleared) =
-p ln(p)
-(1-p) ln(1-p)

定义分类熵：

H(P) =
-Σ p_i ln(p_i)

数值规则：

- 0×ln(0)按0处理；
- 所有输入必须有限；
- 概率必须在[0,1]；
- 分布和误差≤1e-9；
- 不得通过截断隐藏非法概率；
- 浮点误差只允许使用明确的小epsilon；
- 最终uncertainty必须满足：
  0≤uncertainty≤ln(40)+epsilon。

输出增加：

dominant_suit_labels
shape_labels
uncertainty_components

uncertainty_components至少包含：

cleared_entropy
dominant_suit_entropy
shape_entropy
joint_entropy
joint_class_count

要求：

joint_entropy必须等于uncertainty；
joint_class_count=40。

三、补充直接测试

只修改或补充专用测试：

tests/spec_v3/test_t19_model001_baseline_repair.py

不得修改既有test_model_001.py。

测试至少覆盖：

1. 三个任务均为确定分布：
   uncertainty=0；

2. cleared均匀、suit均匀、shape均匀：
   uncertainty=ln(40)；

3. cleared确定、suit均匀、shape均匀：
   uncertainty=ln(20)；

4. 概率含0时不产生NaN；

5. 所有entropy有限且非负；

6. joint_entropy等于三个component之和；

7. dominant_suit_labels准确为：
   wan,tong,tiao,mixed；

8. shape_labels准确为：
   standard,seven_pairs,all_pongs,pure_suit,other；

9. mixed索引固定为3；

10. other索引固定为4；

11. 无证据输入不得产生任何类别概率1；

12. 最大/最小公开证据输入；

13. malformed概率和非法有限值稳定拒绝；

14. 100次重复和fresh-process稳定。

四、修复证据manifest

更新：

T19-W01-MODEL001_evidence_manifest.csv

覆盖：

- belief.py；
- 专用测试；
- baseline gap report；
- dependency closure；
- test results；
- repair authorization；
- uncertainty interpretation approval；
- 其他实际remediation工件。

每个普通工件记录：

path
sha256
byte_size
source_commit_or_worktree
classification
hash_rule

SHA-256必须为64位小写十六进制。

Manifest自身采用明确非循环规则：

- manifest中包含自身路径；
- sha256字段为null；
- hash_rule=SELF_NON_CIRCULAR_EXCLUDED；
- 不得伪造自身哈希；
- manifest外层完整性由最终修复提交的Git tree/blob绑定。

在报告中明确说明：

Git commit tree绑定manifest本身；
manifest绑定其余remediation工件；
因此不存在循环哈希。

五、重新生成证据

更新：

- baseline gap report；
- dependency closure；
- test results；
- repair authorization；
- evidence manifest。

确认：

- include→exclude依赖已修复；
- belief.py必须进入baseline-r1；
- MODEL-001保持INTEGRATED；
- Task17历史状态未修改；
- 不声称外部校准通过。

六、测试

使用Python 3.12批准环境运行：

1. 专用修复测试；
2. tests/spec_v3/test_model_001.py；
3. PlayerView和信息边界测试；
4. 合同测试；
5. 100次确定性；
6. fresh-process确定性；
7. 全仓collection；
8. 全仓pytest。

记录：

- Python；
- pytest；
- collected；
- passed；
- failed；
- skipped；
- skip node和原因；
- duration。

全仓必须0 failed。

七、提交

只有全部测试、manifest和diff检查通过才能提交。

提交信息：

fix(model001): align fallback uncertainty contract

不得amend原提交。

记录：

model001_repair_remediation_commit

八、最终输出

MODEL001_BASELINE_REPAIR_REMEDIATED

并报告：

model001_repair_remediation_commit
uncertainty_contract
joint_class_count
minimum_uncertainty
maximum_uncertainty
entropy_boundary_tests
category_order_tests
manifest_artifact_count
manifest_self_hash_rule
full_collection
full_passed
full_failed
full_skipped
model001_status
task17_history_modified
worktree_clean
```

修复后必须重新进行独立审查。只有复审通过，才能创建 `task19-w01-baseline-r1`；不能复用第一次失败的独立审查结论。

> [!QUESTION] User
> 请你后续生成的提示词均明确告知在哪个终端运行

> [!NOTE] ChatGPT
> 明白。后续生成的每个提示词，我都会在开头明确标注：
> 
> ```
> 运行终端：
> Terminal 0 / Terminal 1 / Terminal 2 / Terminal 3 / 独立审计终端
> 
> 运行目录：
> <完整worktree路径>
> 
> 目标分支：
> <branch>
> 
> 任务性质：
> 只读审查 / 设计 / 实现 / 修复 / 集成 / 独立审计
> ```
> 
> 当前任务对应关系：
> 
> | 任务 | 运行终端 | 目录 |
> | --- | --- | --- |
> | MODEL-001基线修复 | 独立修复终端 | ../wt-task19-t0-model001-repair |
> | MODEL-001独立复审 | 新建独立审计会话，不使用修复会话 | 只读访问修复worktree或commit |
> | B2-A1实现 | Terminal 1 | ../wt-task19-t1-w01 |
> | RULE-015设计修复 | Terminal 2 | ../wt-task19-t2-w01 |
> | AUDIT-010/TRAIN-009设计修复 | Terminal 3 | ../wt-task19-t3-w01 |
> | 计划、进度、集成 | Terminal 0 | 当前主项目目录；在dirty状态下保持只读 |
> 
> 刚才的 MODEL-001 修复提示词应在以下位置运行：
> 
> ```
> 运行终端：MODEL-001独立修复终端
> 运行目录：
> /Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t0-model001-repair
> 
> 目标分支：
> task19/w01-baseline-repair-model001
> 
> 任务性质：
> 修复独立审查发现的合同和证据问题
> ```
> 
> 同时我会明确区分：
> 
> -   “独立修复终端”可以修改授权范围内的代码。
>     
> -   “独立审计终端”只能读取和运行验证，不能修复。
>     
> -   Terminal 0 只有在明确集成授权后才能执行 cherry-pick、更新进度或创建 tag。
>     
> -   Terminal 1～3 不得直接修改权威 tracker 或自行标记 `AUDITED`。

> [!QUESTION] User
> TERMINAL3_DESIGN_REMEDIATION_COMPLETED - audit010_design_remediation_commit: 123118d0ca42dae0a455088ccc50668ccf631b00 - audit010_delta_commit: 589e5aa13a5fa37e10a9fe2754969a8e28b6c37e - audit010_decision_count: 5 - audit010_missing_option_c_count: 0 - audit010_unquantified_ac_count: 0 - audit010_e4_scenario_count: 4 - train009_design_remediation_commit: 644d9d820448b5de6ac1d0821ddf384756502883 - train009_delta_commit: 1c1da899d361ed0e927a16a4c4afcfd7876e6e86 - train009_decision_count: 7 - train009_missing_option_c_count: 0 - train009_unquantified_ac_count: 0 - train009_e4_scenario_count: 4 - unresolved_unnumbered_decision_count: 0 - business_code_modified: false - test_modified: false - worktree_clean: true - staged_count: 0 - push_executed: false 本轮已完成： - 两单元均补齐字段级 DTO、错误码、接口/参数/可见性矩阵、量化 AC、四类独立 E4、逐增量 E5 和 PENDING 审批表。 - TRAIN-009 按实际 STREAMS 闭集修正 RNG 设计；不存在虚构 domain stream。 - 四个新提交均以 task19-w01-baseline 为祖先；原始两个提交未重写。 - 两个 delta 只引用前置设计提交，不循环引用自身。 - 两单元仍为 WAITING_FOR_DESIGN_APPROVAL，下一步均为 OWNER_DECISION。 下一步完整任务清单： 1. Terminal 0 独立复核四个提交和设计门禁；产出复审结论；建议触发语：复审 Terminal 3 设计门禁修复 2. 项目负责人分别选择 AUDIT-010 五项、TRAIN-009 七项决策；产出独立审批记录；建议触发语：审批 AUDIT-010 和 TRAIN-009 决策 3. 审批后另行判断实施授权；当前不得标记 READY_FOR_IMPLEMENTATION 或 AUDITED。

**ChatGPT:**

下一步是在 Terminal 0 执行只读复审，不在 Terminal 3 继续操作。

```
运行终端：
Terminal 0

运行目录：
/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer

目标分支：
不切换分支；保持当前主工作树和当前分支不变

任务性质：
只读复审 Terminal 3 的 AUDIT-010、TRAIN-009 设计修复

禁止：
- checkout或switch
- cherry-pick
- merge
- rebase
- 修改文件
- git add/commit
- 修改权威tracker
- 批准决策
- 标记READY_FOR_IMPLEMENTATION
- push
- stash/clean/reset
```

在 Terminal 0 的 Codex 中粘贴：

```
复审 Terminal 3 的 AUDIT-010、TRAIN-009 设计门禁修复。

运行约束：

- 当前为Terminal 0；
- 当前主工作树可能dirty，只允许只读；
- 不得切换当前分支；
- 必须使用git show、git diff-tree、git merge-base等只读命令检查目标提交；
- 不得使用当前工作树同名文件代替目标commit tree内容。

Baseline：

task19-w01-baseline
65e8dcb1679466c9e37d10e5a4299a09774332d9

原始提交：

AUDIT-010：
74a39ca23879eb04ea47a12f4b77224f4251b433

TRAIN-009：
8632d128f005694c38f1d0e5c0e1092afd22a257

修复提交：

AUDIT-010 design：
123118d0ca42dae0a455088ccc50668ccf631b00

AUDIT-010 delta：
589e5aa13a5fa37e10a9fe2754969a8e28b6c37e

TRAIN-009 design：
644d9d820448b5de6ac1d0821ddf384756502883

TRAIN-009 delta：
1c1da899d361ed0e927a16a4c4afcfd7876e6e86

一、提交和范围

验证：

- 六个提交均存在；
- 均以baseline为祖先；
- 原始提交未重写；
- design remediation只修改对应设计目录；
- delta提交只修改对应progress delta；
- delta中的design_commit_sha准确指向前置design提交；
- delta不存在自身SHA循环；
- 两个单元没有交叉修改；
- 没有业务代码、测试、Locked/Frozen、Task17、B2-A1、RULE-015、LATEST、changelog或权威tracker修改。

输出实际parent链和未来建议cherry-pick顺序，但不得执行。

二、AUDIT-010独立复审

验证：

- semantic=8；
- test delta=4；
- evidence delta=2；
- AC=14；
- decisions=5；
- missing Option C=0；
- unquantified AC=0；
- E4=4；
- E5覆盖口径唯一；
- approval form=PENDING；
- business_code_authorized=false；
- 未编号决策=0。

重点检查：

- DTO字段级类型、必填、默认、null和错误码；
- 每条AC有输入、操作、输出、错误码和机械PASS规则；
- NORMAL/BOUNDARY/HARD_FAILURE/DETERMINISM分别定义；
- signer只保存key reference，不保存私钥；
- developer和auditor身份隔离；
- self-audit稳定拒绝；
- 审计器只读业务authority；
- 审计失败不回滚业务提交；
- finding append-only；
- retention spool/outbox失败和重试语义；
- 每个共享接口有唯一owner；
- AUDIT-014 adapter分类准确；
- 无秘密或隐藏信息泄漏。

三、TRAIN-009独立复审

验证：

- semantic=8；
- test delta=4；
- evidence delta=2；
- AC=14；
- decisions=7；
- missing Option C=0；
- unquantified AC=0；
- E4=4；
- E5覆盖口径唯一；
- approval form=PENDING；
- business_code_authorized=false；
- 未编号决策=0。

重点检查：

- 新增第7项决策确实解决原未编号歧义；
- 不与其他6项重复；
- 实际读取baseline中engine/rng_v2.py::STREAMS；
- 设计没有引用不存在的domain stream；
- 新增stream分类为ADDITIVE_INTERFACE；
- 改变旧stream语义分类为BREAKING_CHANGE；
- episode/worker/environment/coordinate定义完整；
- worker调度顺序变化不改变固定episode输出；
- Observation接口所有分支均有编号决策；
- temporary write、校验、fsync、atomic rename、manifest最后发布完整；
- partial/orphan artifact恢复规则完整；
- restricted artifact与policy feature物理隔离；
- MODEL-001外部有效性不阻塞工程实现；
- MODEL-001仍为INTEGRATED。

四、AC/E4/E5统计

每个单元分别输出：

semantic_count
test_delta_count
evidence_delta_count
ac_count
decision_count
missing_option_c_count
unquantified_ac_count
missing_error_oracle_count
missing_test_binding_count
missing_evidence_binding_count
e4_scenario_count
e5_row_count
missing_e5_delta_count
unknown_ac_reference_count
unresolved_unnumbered_decision_count

五、progress delta

分别确认：

- proposed_status=WAITING_FOR_DESIGN_APPROVAL；
- next_required_action=OWNER_DECISION；
- design_commit_sha正确；
- 无自身SHA循环；
- 不请求READY_FOR_IMPLEMENTATION；
- 不请求AUDITED；
- 两个delta能够独立吸收。

六、分别给出结论

只能分别输出：

AUDIT010_DESIGN_READY_FOR_OWNER_DECISION
或
AUDIT010_DESIGN_REVIEW_FAILED

TRAIN009_DESIGN_READY_FOR_OWNER_DECISION
或
TRAIN009_DESIGN_REVIEW_FAILED

不得以一个汇总结论代替。

如果失败，逐项输出：

finding_id
severity
affected_commit
affected_file
affected_section
required_fix
blocking_scope

如果通过，分别输出所有者决策表：

decision_id
question
option_a
option_b
option_c
recommended_option
recommendation_reason
approval_order
selected_option
owner_comment

selected_option和owner_comment保持空。

七、集成建议

只输出建议，不执行：

- 六个提交的cherry-pick顺序；
- owner approval commit应位于哪个提交之后；
- progress delta吸收时点；
- 实施授权前置条件。

本轮不得修改、集成、批准或更新任何状态。
```

如果两个结论都通过，再把 Terminal 0 输出的12项决策表发给我：AUDIT-010共5项，TRAIN-009共7项。届时再逐项确定审批选项。

> [!QUESTION] User
> RULE015_FINAL_DESIGN_GATE_REMEDIATED - rule015_final_design_commit_sha: b786a61393924bfffb2902085740acc67d18a926 - rule015_final_delta_commit_sha: 026f81d3c8902297e84bec4d94897ff374d2f145 - e5_row_count: 14 - semantic_e5_count: 8 - test_e5_count: 4 - evidence_e5_count: 2 - covered_ac_count: 14 - missing_ac_reference_count: 0 - performance_environment_id: RULE015-PERF-REF-V1-078dc25252299f3c - performance_manifest_valid: true - ac12_environment_reference_valid: true - e4_environment_reference_valid: true - dec012_status: PENDING - worktree_clean: true 既有三个提交保持不变。设计提交仅修改 T19-D02 设计文件；metadata 提交仅修改 progress delta。12 项决策仍未选择，状态保持 WAITING_FOR_DESIGN_APPROVAL，未 push。 下一步：项目所有者审批 RULE015-DEC-001～012，建议触发语：批准 RULE-015 最终设计决策。

**ChatGPT:**

现在应先由 Terminal 0 做最后一次只读复审，只检查上一轮剩余的三个 finding。通过后才能由项目所有者批准12项决策。

```
运行终端：
Terminal 0

运行目录：
/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer

目标分支：
不切换分支；保持当前主工作树不变

任务性质：
RULE-015 最终设计门禁只读复审
```

在 Terminal 0 的 Codex 中粘贴：

```
执行 RULE-015 最终设计门禁只读复审。

当前为Terminal 0。

禁止：

- checkout/switch；
- cherry-pick；
- merge；
- rebase；
- 修改文件；
- git add/commit；
- 更新权威tracker；
- 批准决策；
- 标记READY_FOR_IMPLEMENTATION；
- push；
- stash/clean/reset。

必须直接读取目标commit tree，不得以当前dirty工作树同名文件代替。

Baseline：

task19-w01-baseline
65e8dcb1679466c9e37d10e5a4299a09774332d9

完整提交链：

原始设计：
7022756ef65e51eab185a7569394f0ad78d8863a

第一轮设计修复：
683dcd7d38db166b141b26d858227d2fba90b0f7

第一轮delta：
f9bfdf27cc08dd28a34f6bbfb6da43d71a051b6c

最终设计修复：
b786a61393924bfffb2902085740acc67d18a926

最终delta：
026f81d3c8902297e84bec4d94897ff374d2f145

一、提交范围

验证：

- 五个提交均存在；
- 均以baseline为祖先；
- 既有提交未被重写；
- b786a613只修改T19-D02设计文件；
- 026f81d3只修改RULE-015_progress_delta.json；
- 最终delta的design_commit_sha准确等于b786a613完整SHA；
- 最终delta无自身SHA循环；
- proposed_status=WAITING_FOR_DESIGN_APPROVAL；
- next_required_action=OWNER_DECISION；
- 没有业务代码、测试、Locked/Frozen、STATE-010、Task17、B2-A1、LATEST、changelog或权威tracker修改。

二、复核R015-R2-F001

确认E5口径唯一为：

8 semantic
+ 4 test
+ 2 evidence
= 14行

验证：

e5_row_count=14
semantic_e5_count=8
test_e5_count=4
evidence_e5_count=2
unique_delta_id_count=14
covered_ac_count=14
missing_ac_reference_count=0
unknown_ac_reference_count=0
missing_evidence_delta_count=0

确认：

- AC不额外生成14条E5行；
- AC通过acceptance_ids外键覆盖；
- 设计文件中不存在26行或28行口径；
- AC-14、evidence delta、approval form和design review表述一致。

三、复核R015-R2-F002

读取并验证：

RULE-015_performance_environment.json

确认：

- JSON有效；
- environment_id为：
  RULE015-PERF-REF-V1-078dc25252299f3c
- environment_id由规范化字段稳定生成；
- 没有用户名、本机绝对路径、token或秘密；
- OS、architecture、CPU、Python和pytest字段完整；
- timer明确；
- process_count=1；
- thread_count=1；
- warmup、measurement、repeat完整；
- percentile_method明确为nearest-rank P95；
- 异常/超时处理明确；
- fixture reference和SHA-256完整；
- threshold_decision_id=RULE015-DEC-012；
- threshold_status=PENDING_OWNER_DECISION；
- 未提前固定2/5/10ms；
- reference环境为硬验收；
- 非reference环境只生成informational结果；
- allowed variation定义明确。

重新计算environment_id所需canonical hash，确认与manifest ID一致。

四、复核R015-R2-F003

检查AC-12和四类E4：

- AC-12引用准确的performance_environment_id；
- NORMAL E4引用同一ID；
- DETERMINISM或适用性能场景引用同一ID；
- 不存在“current environment”“AC-12 environment”等模糊引用；
- fixture SHA一致；
- warmup/measurement/repeat一致；
- P95算法一致；
- DEC-012仍为PENDING；
- selected_threshold为空或null；
- performance_result=WAITING_APPROVAL；
- 环境不匹配结果为NOT_AUTHORITATIVE或已定义的稳定状态；
- AC-12未提前标记PASS。

五、确认其余门禁未回退

抽查确认：

- decision=12；
- missing Option C=0；
- selected_option全部为空；
- approval_status全部PENDING；
- AC=14；
- unquantified AC=0；
- E4=4；
- 独立参数矩阵有效；
- 独立可见性矩阵有效；
- STATE-010仍准确表述为AUDITED；
- 不修改STATE-010语义；
- approval form=PENDING；
- business_code_authorized=false。

六、最终结论

只有三个原finding全部关闭，才能输出：

RULE015_DESIGN_READY_FOR_OWNER_DECISION

否则输出：

RULE015_DESIGN_REVIEW_FAILED

如果通过，输出项目所有者决策表：

decision_id
question
option_a
option_b
option_c
recommended_option
recommendation_reason
approval_order
selected_option
owner_comment

selected_option和owner_comment保持空。

同时明确建议：

- DEC-001～DEC-005先审批；
- DEC-006依赖DEC-003～005；
- DEC-007依赖DEC-006；
- DEC-008依赖DEC-002；
- DEC-009依赖DEC-003～005；
- DEC-010依赖DEC-002、004；
- DEC-011不得选择会写回STATE-010的breaking方案；
- DEC-012必须根据已冻结performance environment审批。

本轮不得修改、批准、集成或更新进度。
```

如果结果为：

```
RULE015_DESIGN_READY_FOR_OWNER_DECISION
```

再把12项决策表发给我。根据目前预审信息，预计 DEC-001～011 推荐选择 A，DEC-012推荐选择 B，但仍应以最终决策表的完整内容为准。

> [!QUESTION] User
> 如何保存当前4个终端的任务进度，便于我到windows电脑上继续

**ChatGPT:**

最可靠的方法是：把每个终端的进度保存到各自 Git 分支并推送到私有远程仓库，然后在 Windows 重新创建 worktree。不要直接用 OneDrive 复制这些 worktree，因为 Git 的 worktree 元数据包含 Mac 绝对路径，跨系统容易损坏。

## 一、各终端分别保存

### Terminal 1：保存未完成的 B2-A1

运行目录：

```
/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t1-w01
```

Terminal 1 当前有尚未提交的实现，需要创建明确的 WIP 迁移提交。这个提交只用于跨电脑保存，不表示验收通过。

在 Terminal 1 的 Codex 中运行：

```
运行终端：Terminal 1
任务性质：跨机器WIP保存

当前分支：
task19/w01-b2a1

停止继续开发。

1. 检查git status和git diff；
2. 确认只包含B2-A1授权路径；
3. 新增一份：
   docs/spec-v3/task19/handoffs/W01/terminal_1_b2a1_handoff.md

记录：
- baseline；
- 当前branch和HEAD；
- STATE-002/003/ALGO-002完成情况；
- 测试命令和结果；
- MODEL-001 baseline blocker；
- 尚未完成的全仓回归、E4/E5/AC/delta；
- Windows继续时的准确下一步；
- 明确IMPLEMENTED_PENDING_BASELINE_REPAIR；
- 明确不是AUDITED或最终提交。

4. 精确暂存本终端授权文件和handoff文件；
5. 禁止git add .；
6. 创建提交：

git commit -m "wip(task19-b2a1): preserve cross-machine handoff"

7. 报告完整commit SHA；
8. 不更新权威tracker；
9. 不标记实现完成；
10. 不push，由Terminal 0统一push。
```

### Terminal 2：RULE-015

运行目录：

```
.../wt-task19-t2-w01
```

它已经提交且工作树干净。只需确认：

```
git status --short
git branch --show-current
git log --oneline -6
```

如果需要更完整的迁移说明，可新增并提交：

```
docs/spec-v3/task19/handoffs/W01/terminal_2_rule015_handoff.md
```

记录下一步是 Terminal 0 最终复审，而不是继续修改设计。

### Terminal 3：AUDIT-010、TRAIN-009

运行目录：

```
.../wt-task19-t3-w01
```

同样确认：

```
git status --short
git branch --show-current
git log --oneline -8
```

handoff 应记录四个修复提交及下一步 Terminal 0 复审。

### MODEL-001 修复分支

虽然不属于原三个开发终端，也必须一起保存：

```
branch:
task19/w01-baseline-repair-model001
```

记录：

-   原修复提交 `7b8f27e...`
    
-   独立审查失败的3个 findings
    
-   已批准/待执行的联合熵修复方案
    
-   尚未创建 `task19-w01-baseline-r1`
    

## 二、Terminal 0 统一检查并推送

运行终端：

```
Terminal 0
```

先检查远程仓库：

```
git remote -v
```

如果已有私有远程 `origin`，确认所有分支存在：

```
git branch --list "task19/*"
git tag -l "task19-w01*"
```

然后推送明确分支，不要使用 `git push --all`：

```
git push origin task19/w01-b2a1
git push origin task19/w01-design-deterministic
git push origin task19/w01-design-audit-training
git push origin task19/w01-baseline-repair-model001
git push origin task19-w01-baseline
```

注意：

-   不推送 `.venv-macos`、缓存或模拟数据目录。
    
-   不推送当前主工作树未归属的 dirty 修改。
    
-   不创建或推送尚不存在的 `task19-w01-baseline-r1`。
    
-   远程仓库建议设为 Private。
    

推送后验证：

```
git ls-remote --heads origin "task19/*"
git ls-remote --tags origin "task19-w01*"
```

## 三、Windows 恢复

在 Windows 先克隆或更新仓库：

```
git clone <PRIVATE_REPOSITORY_URL> chengdu_majiang_AItrainer
cd chengdu_majiang_AItrainer
git fetch origin --prune --tags
```

重新创建 worktree：

```
git worktree add ..\wt-task19-t1-w01 -b task19/w01-b2a1 origin/task19/w01-b2a1

git worktree add ..\wt-task19-t2-w01 -b task19/w01-design-deterministic origin/task19/w01-design-deterministic

git worktree add ..\wt-task19-t3-w01 -b task19/w01-design-audit-training origin/task19/w01-design-audit-training

git worktree add ..\wt-task19-model001-repair -b task19/w01-baseline-repair-model001 origin/task19/w01-baseline-repair-model001
```

然后在每个目录启动 Codex，并让它先读取对应的 handoff 文件。

## 四、Windows 环境要重建

Mac 的虚拟环境不能复制到 Windows。Windows 需要单独创建 Python 3.12 环境：

```
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

具体依赖安装命令应以仓库现有说明为准。不要复制：

```
.venv-macos/
.envrc授权状态
.git/worktrees/
Mac绝对路径配置
```

最终迁移完成标准：

-   四个任务分支都已推送；
    
-   baseline tag已推送；
    
-   Terminal 1 WIP已提交；
    
-   各分支工作树干净；
    
-   Windows能重新创建worktree；
    
-   每个分支有handoff说明；
    
-   没有把WIP误标为完成或AUDITED。

> [!NOTE] ChatGPT
> 当前结果可以拆成两条并行工作：
> 
> -   AUDIT-010 已可进入所有者审批。
>     
> -   TRAIN-009 只需修复一处 progress delta 元数据。
>     
> 
> ## 任务一：修复 TRAIN-009 delta
> 
> ```
> 运行终端：
> Terminal 3
> 
> 运行目录：
> /Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t3-w01
> 
> 目标分支：
> task19/w01-design-audit-training
> 
> 任务性质：
> 仅修复 TRAIN-009 progress delta 元数据
> ```
> 
> 在 Terminal 3 Codex 中运行：
> 
> ```
> 修复 TRAIN-009 progress delta 覆盖 T03-DEC-007。
> 
> 前置提交：
> 
> 1c1da899d361ed0e927a16a4c4afcfd7876e6e86
> 
> 只允许修改：
> 
> docs/spec-v3/task19/progress_deltas/TRAIN-009_progress_delta.json
> 
> 修复：
> 
> 将blocking_change中：
> 
> T03-DEC-001..006 remain PENDING
> 
> 改为准确覆盖：
> 
> T03-DEC-001..007 remain PENDING
> 
> 同时确认：
> 
> - design_commit_sha仍为：
>   644d9d820448b5de6ac1d0821ddf384756502883
> - proposed_status=WAITING_FOR_DESIGN_APPROVAL；
> - next_required_action=OWNER_DECISION；
> - 不记录delta自身commit SHA；
> - 不请求READY_FOR_IMPLEMENTATION；
> - 不请求AUDITED；
> - 其他字段不发生无关变化。
> 
> 禁止：
> 
> - 修改设计包；
> - 修改业务代码或测试；
> - 修改Locked/Frozen；
> - 修改Task17或权威tracker；
> - amend已有提交；
> - push。
> 
> 验证JSON有效、git diff --check通过后，创建metadata-only提交：
> 
> git commit -m "task19(T19-T03): include DEC-007 in TRAIN-009 progress"
> 
> 最终输出：
> 
> TRAIN009_PROGRESS_DELTA_REMEDIATED
> 
> 并报告：
> 
> train009_delta_remediation_commit
> changed_paths
> design_commit_sha
> pending_decision_range
> proposed_status
> worktree_clean
> staged_count
> push_executed
> ```
> 
> 修复后，在 Terminal 0 做只读复审。
> 
> ## 任务二：审批 AUDIT-010
> 
> 5项推荐方案整体合理。我的建议是：
> 
> | 决策 | 建议 |
> | --- | --- |
> | A04-DEC-001 | A |
> | A04-DEC-002 | A |
> | A04-DEC-003 | A |
> | A04-DEC-004 | A |
> | A04-DEC-005 | A |
> 
> 原因简要如下：
> 
> -   DEC-001 A：结构化 node/edge 行最适合流式检查和断链定位。
>     
> -   DEC-002 A：SHA-256 加外部签名引用，能证明身份又不保存秘密。
>     
> -   DEC-003 A：当前规模下采用更严格性能和内存门禁。
>     
> -   DEC-004 A：业务 authority 与留存系统解耦，同时保留持久重试能力。
>     
> -   DEC-005 A：适合持续开发阶段，以提交时间、scope和环境共同判断证据新鲜度。C的精确候选版本哈希更适合最终发布审计，但会过早绑定 release candidate。
>     
> 
> 如果你同意，可以直接回复：
> 
> ```
> 批准 AUDIT-010 设计决策：
> A04-DEC-001=A
> A04-DEC-002=A
> A04-DEC-003=A
> A04-DEC-004=A
> A04-DEC-005=A
> ```
> 
> 收到你的明确批准后，下一份提示词将在以下位置运行：
> 
> ```
> 运行终端：Terminal 3
> 运行目录：.../wt-task19-t3-w01
> 任务性质：写入 AUDIT-010 独立审批记录并创建 approval commit
> ```
> 
> 现在不要由 Terminal 0 cherry-pick；等 AUDIT-010 approval commit 和 TRAIN-009 delta 修复复审都完成后再安排集成。

> [!QUESTION] User
> RULE015_FINAL_DESIGN_GATE_REMEDIATED - rule015_final_design_commit_sha: b786a61393924bfffb2902085740acc67d18a926 - rule015_final_delta_commit_sha: 026f81d3c8902297e84bec4d94897ff374d2f145 - e5_row_count: 14 - semantic_e5_count: 8 - test_e5_count: 4 - evidence_e5_count: 2 - covered_ac_count: 14 - missing_ac_reference_count: 0 - performance_environment_id: RULE015-PERF-REF-V1-078dc25252299f3c - performance_manifest_valid: true - ac12_environment_reference_valid: true - e4_environment_reference_valid: true - dec012_status: PENDING - worktree_clean: true 既有三个提交保持不变。设计提交仅修改 T19-D02 设计文件；metadata 提交仅修改 progress delta。12 项决策仍未选择，状态保持 WAITING_FOR_DESIGN_APPROVAL，未 push。 下一步：项目所有者审批 RULE015-DEC-001～012，建议触发语：批准 RULE-015 最终设计决策。 ─ Worked for 6m 32s ─────────────────────────────────────────────────────────────

> [!NOTE] ChatGPT
> 这是 Terminal 2 的修复结果，不是 Terminal 0 的独立复审结论。因此暂时不要直接批准12项决策。
> 
> 下一步：
> 
> ```
> 运行终端：
> Terminal 0
> 
> 运行目录：
> /Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer
> 
> 目标分支：
> 不切换分支
> 
> 任务性质：
> RULE-015 最终设计只读复审
> ```
> 
> 在 Terminal 0 中执行上一轮给出的“RULE-015最终设计门禁只读复审”提示词，重点核对：
> 
> -   `b786a613...` 只修改设计文件；
>     
> -   `026f81d3...` 只修改progress delta；
>     
> -   E5口径固定为8+4+2=14；
>     
> -   14项AC全部覆盖；
>     
> -   性能环境ID可重算；
>     
> -   AC-12与E4引用同一环境；
>     
> -   DEC-012仍为PENDING；
>     
> -   没有业务代码、测试或全局状态修改。
>     
> 
> 预期结论应为：
> 
> ```
> RULE015_DESIGN_READY_FOR_OWNER_DECISION
> ```
> 
> 只有得到该结论后，再审批：
> 
> ```
> RULE015-DEC-001～011：预计选择A
> RULE015-DEC-012：预计选择B
> ```
> 
> 目前状态仍正确：
> 
> ```
> RULE-015=WAITING_FOR_DESIGN_APPROVAL
> business_code_authorized=false
> ```

> [!QUESTION] User
> 给出“RULE-015最终设计门禁只读复审”提示词

**ChatGPT:**

```
运行终端：
Terminal 0

运行目录：
/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer

目标分支：
不切换分支；保持当前主工作树和当前分支不变

任务性质：
RULE-015 最终设计门禁只读复审

任务目标：
只读复核 RULE-015 最终设计修复是否关闭剩余审批入口缺陷，并判断是否可以提交项目所有者审批。

禁止：

- git checkout或switch；
- git cherry-pick；
- git merge；
- git rebase；
- git add或commit；
- git stash、clean或reset；
- 修改、创建或删除仓库文件；
- 更新Task 19权威tracker；
- 批准任何决策；
- 标记READY_FOR_IMPLEMENTATION；
- 修改Task17、Locked/Frozen；
- 实现业务代码或测试；
- push；
- 使用当前dirty工作树中的同名文件替代目标commit tree内容。

所有检查必须直接读取目标commit tree。

Baseline：

tag：
task19-w01-baseline

commit：
65e8dcb1679466c9e37d10e5a4299a09774332d9

RULE-015提交链：

原始设计：
7022756ef65e51eab185a7569394f0ad78d8863a

第一轮设计修复：
683dcd7d38db166b141b26d858227d2fba90b0f7

第一轮progress delta：
f9bfdf27cc08dd28a34f6bbfb6da43d71a051b6c

最终设计修复：
b786a61393924bfffb2902085740acc67d18a926

最终progress delta：
026f81d3c8902297e84bec4d94897ff374d2f145

==================================================
一、提交身份、祖先和范围
==================================================

验证：

1. 五个提交均存在；
2. 五个提交均以task19-w01-baseline为祖先；
3. 原始提交和第一轮修复提交未被重写；
4. 输出每个提交的完整parent；
5. b786a613只修改：
   docs/spec-v3/task19/design/T19-D02/
   下的RULE-015设计文件；
6. 026f81d3只修改：
   docs/spec-v3/task19/progress_deltas/RULE-015_progress_delta.json；
7. 最终delta中的design_commit_sha完整等于：
   b786a61393924bfffb2902085740acc67d18a926；
8. 最终delta不记录包含自身的commit SHA；
9. proposed_status=WAITING_FOR_DESIGN_APPROVAL；
10. next_required_action=OWNER_DECISION；
11. 没有请求READY_FOR_IMPLEMENTATION或AUDITED；
12. 没有修改业务代码；
13. 没有修改测试代码或既有断言；
14. 没有修改Locked/Frozen；
15. 没有修改STATE-010；
16. 没有修改Task17；
17. 没有修改B2-A1；
18. 没有修改Task19权威tracker；
19. 没有修改LATEST或changelog；
20. Terminal 2 worktree当前干净；
21. 主工作树staged文件数为0。

任一禁止范围发生修改，立即输出失败。

==================================================
二、复核 E5 统一口径
==================================================

RULE-015的E5权威口径必须唯一为：

8 semantic
+ 4 test
+ 2 evidence
= 14行

验证：

e5_row_count=14
semantic_e5_count=8
test_e5_count=4
evidence_e5_count=2
unique_delta_id_count=14
covered_ac_count=14
missing_ac_reference_count=0
unknown_ac_reference_count=0
missing_evidence_delta_count=0
duplicate_delta_id_count=0

检查：

1. AC不额外生成14条E5行；
2. AC-01～AC-14通过acceptance_ids外键覆盖；
3. 每个AC至少被一行E5引用；
4. 2个evidence delta均存在；
5. E5中不存在未知AC；
6. 不存在26行或28行口径；
7. RULE-015_design_review.md口径一致；
8. RULE-015_evidence_deltas.csv口径一致；
9. RULE-015_acceptance_matrix.csv中的AC-14口径一致；
10. RULE-015_approval_form.md口径一致；
11. 所有其他T19-D02文件中的E5表述一致。

发现任何不同口径即判定失败。

==================================================
三、复核冻结性能环境 manifest
==================================================

读取目标commit tree中的：

docs/spec-v3/task19/design/T19-D02/RULE-015_performance_environment.json

验证：

1. JSON有效；
2. environment_id准确为：
   RULE015-PERF-REF-V1-078dc25252299f3c；
3. environment_id由规范化环境字段稳定生成；
4. 按设计定义重新生成canonical bytes；
5. 重新计算hash prefix；
6. 计算结果与environment_id一致；
7. 不得只检查字符串格式；
8. schema_version存在；
9. captured_at存在；
10. os_name、os_version、os_build完整；
11. architecture完整；
12. cpu_model完整；
13. logical_cpu_count完整；
14. python_implementation完整；
15. python_version完整；
16. python_build完整；
17. pytest_version完整；
18. timer=time.perf_counter_ns；
19. process_count=1；
20. thread_count=1；
21. hash_seed_policy明确；
22. warmup_iterations为明确正整数；
23. measurement_iterations为明确正整数；
24. repeat_count为明确正整数；
25. percentile_method明确为nearest-rank P95；
26. nearest-rank索引规则明确；
27. 异常和超时按正无穷处理；
28. load_isolation定义明确；
29. input_fixture_reference存在；
30. input_fixture_sha256为64位小写十六进制；
31. fixture实际存在于设计包或明确的版本化位置；
32. 重新计算fixture SHA-256并匹配；
33. threshold_decision_id=RULE015-DEC-012；
34. threshold_status=PENDING_OWNER_DECISION；
35. 未提前选择2ms、5ms或10ms；
36. reference环境结果用于硬验收；
37. 非reference环境只生成informational结果；
38. allowed_environment_variation明确；
39. informational_environment_policy明确；
40. 不包含用户名；
41. 不包含本机绝对路径；
42. 不包含token、密钥或其他秘密；
43. 不依赖.envrc授权；
44. 不依赖网络查询。

如果canonical hash算法或字段集合未明确到可重算，判定失败。

==================================================
四、复核 AC-12
==================================================

检查RULE-015_acceptance_matrix.csv中的AC-12。

必须验证：

1. AC-12引用准确的performance_environment_id：
   RULE015-PERF-REF-V1-078dc25252299f3c；
2. 引用同一个fixture；
3. fixture SHA-256一致；
4. warmup次数与manifest一致；
5. measurement次数与manifest一致；
6. repeat次数与manifest一致；
7. process_count=1；
8. thread_count=1；
9. timer一致；
10. P95算法一致；
11. 异常处理一致；
12. threshold_decision_id=RULE015-DEC-012；
13. DEC-012未批准前selected_threshold为空或null；
14. DEC-012未批准前AC-12=WAITING_APPROVAL；
15. 未提前标记PASS；
16. reference环境匹配时才允许硬门禁；
17. 非reference环境输出NOT_AUTHORITATIVE或设计规定的等价稳定结果；
18. 环境不匹配不得误判性能FAIL；
19. 环境不匹配不得误判性能PASS；
20. pass_rule可以机械执行；
21. performance oracle可以机器复现。

==================================================
五、复核 E4 性能环境引用
==================================================

检查四类E4：

- NORMAL；
- BOUNDARY；
- HARD_FAILURE；
- DETERMINISM。

验证：

1. E4总场景数为4；
2. NORMAL引用同一performance_environment_id；
3. DETERMINISM或适用性能场景引用同一ID；
4. fixture SHA与manifest一致；
5. warmup/measurement/repeat一致；
6. timer一致；
7. P95方法一致；
8. threshold_decision_id一致；
9. DEC-012未批准前selected_threshold_ns=null；
10. DEC-012未批准前performance_result=WAITING_APPROVAL；
11. 环境匹配字段可机械判断；
12. 非reference环境结果为informational；
13. 不存在以下模糊引用：
    - current environment
    - runtime environment
    - AC-12 environment
    - approved environment
    - local machine
14. E4与AC-12不存在不同性能口径。

==================================================
六、确认其他设计门禁未回退
==================================================

抽查并验证：

decision_count=12
missing_option_c_count=0
selected_option_count=0
pending_decision_count=12
ac_count=14
unquantified_ac_count=0
e4_scenario_count=4
parameter_matrix_valid=true
visibility_matrix_valid=true
approval_form_present=true
business_code_authorized=false
state010_status=AUDITED
state010_semantics_modified=false

同时检查：

1. 12项决策均有A/B/C；
2. Option C均具体、互斥、可实施；
3. recommendation_reason完整；
4. compatibility impact完整；
5. interface impact完整；
6. test impact完整；
7. affected units完整；
8. blocked units完整；
9. selected_option全部为空；
10. approval_status全部PENDING；
11. 14条AC均有量化输入；
12. 14条AC均有操作和预期输出；
13. 14条AC均有错误码或明确NOT_APPLICABLE；
14. test oracle完整；
15. E4/E5绑定完整；
16. decision dependency完整；
17. 机械PASS规则完整；
18. 参数矩阵独立；
19. 可见性矩阵独立；
20. STATE-010准确描述为AUDITED；
21. RULE-015只复用FrozenGlobalParameters.snapshot；
22. RULE-015不修改STATE-010的60参数闭集；
23. 不修改STATE-010 CAS、版本、生命周期和错误码；
24. DEC-011 Option C继续标记为BREAKING_CHANGE；
25. 未批准DEC-011 C不得实施；
26. approval form仍为PENDING；
27. 没有产生实现授权。

==================================================
七、12项决策的可审批性
==================================================

逐项检查：

RULE015-DEC-001
RULE015-DEC-002
RULE015-DEC-003
RULE015-DEC-004
RULE015-DEC-005
RULE015-DEC-006
RULE015-DEC-007
RULE015-DEC-008
RULE015-DEC-009
RULE015-DEC-010
RULE015-DEC-011
RULE015-DEC-012

对每项输出：

decision_id
question
option_a
option_b
option_c
recommended_option
recommendation_reason
compatibility_impact
interface_impact
test_impact
affected_units
blocked_units
approval_dependencies
terminal0_recommendation

确认审批顺序：

1. DEC-001；
2. DEC-002；
3. DEC-003～005；
4. DEC-006；
5. DEC-007；
6. DEC-008；
7. DEC-009；
8. DEC-010；
9. DEC-011；
10. DEC-012。

特别检查：

- DEC-006依赖DEC-003～005；
- DEC-007依赖DEC-006；
- DEC-008依赖DEC-002；
- DEC-009依赖DEC-003～005；
- DEC-010依赖DEC-002和DEC-004；
- DEC-011不得未经额外授权选择写回STATE-010的breaking方案；
- DEC-012只能在性能环境manifest通过后审批。

==================================================
八、最终结论
==================================================

只有以下条件全部满足才能输出：

RULE015_DESIGN_READY_FOR_OWNER_DECISION

条件：

- 提交链和范围全部通过；
- R015-R2-F001关闭；
- R015-R2-F002关闭；
- R015-R2-F003关闭；
- E5口径唯一；
- 性能环境ID可重算；
- fixture哈希匹配；
- AC-12引用正确；
- E4引用正确；
- 其他设计门禁没有回退；
- 12项决策具备完整审批信息；
- 无开放P1；
- business_code_authorized=false；
- 权威状态未修改。

否则输出：

RULE015_DESIGN_REVIEW_FAILED

失败时逐项报告：

finding_id
severity
affected_commit
affected_file
affected_section
evidence
required_fix
blocking_scope

==================================================
九、通过后的所有者决策表
==================================================

如果通过，输出：

decision_id,selected_option,owner_comment
RULE015-DEC-001,,
RULE015-DEC-002,,
RULE015-DEC-003,,
RULE015-DEC-004,,
RULE015-DEC-005,,
RULE015-DEC-006,,
RULE015-DEC-007,,
RULE015-DEC-008,,
RULE015-DEC-009,,
RULE015-DEC-010,,
RULE015-DEC-011,,
RULE015-DEC-012,,

selected_option和owner_comment保持空。

同时输出Terminal 0建议，但不得替项目所有者填写。

本任务不得：

- 修改文件；
- 集成提交；
- 写入审批结果；
- 更新progress tracker；
- 标记READY_FOR_IMPLEMENTATION；
- 创建实现授权。
```

> [!QUESTION] User
> MODEL001_BASELINE_REPAIR_REMEDIATED - model001_repair_remediation_commit: 2eeecb98a77e61e19489611c1b051eee8613d2be - uncertainty_contract: H(cleared) + H(dominant_suit) + H(shape) - joint_class_count: 40 - minimum_uncertainty: 0 - maximum_uncertainty: ln(40) - entropy_boundary_tests: PASS — 0、ln(20)、ln(40)、零概率及非法概率 - category_order_tests: PASS — suit=wan,tong,tiao,mixed; shape=standard,seven_pairs,all_pongs,pure_suit,other - manifest_artifact_count: 12 - manifest_self_hash_rule: SELF_NON_CIRCULAR_EXCLUDED - full_collection: 468 - full_passed: 467 - full_failed: 0 - full_skipped: 1 - model001_status: INTEGRATED - task17_history_modified: false - worktree_clean: true 本轮完成： - 修复 M001-R-F001/F002/F003。 - 新增批准解释记录并保持 Locked/Frozen 原文不变。 - 专用测试 19 passed；既有 MODEL-001 测试 1 passed；合同与信息边界 28 passed。 - 100 次同进程及 5 次 fresh-process 输出稳定。 - 唯一 skip 是既有 macOS Tk 安全跳过，与本修复无关。 - 创建新提交，未 amend 7b8f27e，未 tag、push 或升级 MODEL-001 状态。 下一步完整任务清单： 1. 独立复审 remediation commit 2eeecb9；产出审查结论；建议触发语：独立复审 MODEL-001 remediation commit 2eeecb9 2. 审查通过后由 Terminal 0 集成 7b8f27e 与 2eeecb9；依赖：独立复审 PASS。 3. 在 B2-A1 worktree 重跑全仓回归并解除 MODEL-001 blocker。 4. 刷新 B2-A1 E4/E5/AC、生成 progress delta 和独立提交。 5. 交由 Terminal 0 集成及独立审计；不得自行标记 AUDITED。

**ChatGPT:**

下一步应使用新的独立审计会话，不能在 MODEL-001 修复会话中自审。

```
运行终端：
独立审计终端（建议新开 Terminal 4）

运行目录：
/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t0-model001-repair

目标分支：
task19/w01-baseline-repair-model001

目标提交：
2eeecb98a77e61e19489611c1b051eee8613d2be

任务性质：
MODEL-001 baseline remediation 独立只读复审
```

在新开的 Codex 会话中粘贴：

```
独立复审 MODEL-001 remediation commit。

当前角色：

- 独立审计者；
- 不是修复实现者；
- 只能读取代码、规格、提交和证据；
- 可以运行测试；
- 不得修改任何文件。

Baseline：

task19-w01-baseline
65e8dcb1679466c9e37d10e5a4299a09774332d9

第一轮修复提交：

7b8f27e38a3bbb158b276d478024eea70354ef8b

第一轮独立审查：

MODEL001_BASELINE_REPAIR_INDEPENDENT_REVIEW_FAIL

Remediation提交：

2eeecb98a77e61e19489611c1b051eee8613d2be

预期状态：

MODEL-001=INTEGRATED

禁止：

- 修改业务代码；
- 修改测试；
- 修改证据；
- git add/commit；
- cherry-pick；
- merge；
- rebase；
- checkout/switch；
- 创建或移动tag；
- 修改Task17；
- 修改Task19权威tracker；
- 标记MODEL-001为AUDITED；
- push；
- stash/clean/reset；
- 执行direnv allow。

所有静态检查必须基于目标commit tree，不得使用dirty主工作树的同名文件。

==================================================
一、提交身份、祖先和范围
==================================================

验证：

1. baseline存在；
2. 7b8f27e存在；
3. 2eeecb9存在；
4. 7b8f27e的parent为baseline；
5. 2eeecb9的parent为7b8f27e，或报告实际parent；
6. baseline是两个修复提交的祖先；
7. 原提交7b8f27e未被amend或重写；
8. 列出2eeecb9全部changed paths；
9. 生产代码修改仅限批准的belief.py；
10. 测试修改仅限专用MODEL-001修复测试；
11. 没有修改test_model_001.py既有断言；
12. 没有修改Locked/Frozen原文；
13. 没有修改Task17；
14. 没有修改Task19权威tracker；
15. 没有修改LATEST或changelog；
16. 没有创建模型artifact或模拟数据；
17. worktree干净；
18. staged=0；
19. 未push。

任何范围外业务修改均阻止通过。

==================================================
二、审批依据
==================================================

检查：

MODEL001_uncertainty_interpretation_approval.md

确认：

1. 明确记录原合同歧义；
2. 明确记录批准方案：
   uncertainty =
   H(cleared)
   + H(dominant_suit)
   + H(shape)；
3. joint_class_count=40；
4. 范围为[0,ln(40)]；
5. 保留标量uncertainty；
6. 增加分项entropy元数据；
7. 类别顺序固定；
8. 兼容性影响明确；
9. MODEL-001继续为INTEGRATED；
10. 不修改Locked原文；
11. approval_basis确实来自项目所有者授权，而不是开发者自行批准或模型自行推断。

如果缺少明确项目所有者审批依据，输出P1 finding，不得自行补写。

==================================================
三、关闭 M001-R-F001
==================================================

检查model_001_rule_baseline实现。

必须验证：

uncertainty =
cleared_entropy
+ dominant_suit_entropy
+ shape_entropy

二分类熵：

H(cleared) =
-p ln(p)
-(1-p) ln(1-p)

分类熵：

H(P) =
-Σ p_i ln(p_i)

验证：

1. 0×ln(0)按0处理；
2. 不产生NaN；
3. 不产生正负无穷；
4. 输入概率必须有限；
5. 概率范围为[0,1]；
6. 分布归一误差≤1e-9；
7. 非法概率稳定拒绝；
8. 不通过截断掩盖非法输入；
9. joint_class_count=40；
10. minimum uncertainty=0；
11. maximum uncertainty=ln(40)；
12. joint_entropy等于三个component之和；
13. 标量uncertainty等于joint_entropy；
14. 浮点误差规则明确；
15. 结果符合批准解释记录。

重新独立计算以下oracle：

- 三任务确定分布：0；
- cleared确定、suit和shape均匀：ln(20)；
- 三任务全部均匀：ln(40)；
- 包含零概率；
- 非法负概率；
- 大于1概率；
- 非有限概率；
- 分布和不等于1。

不得只依赖开发者测试中的预期常量。

==================================================
四、关闭 M001-R-F003
==================================================

验证输出元数据：

dominant_suit_labels准确为：

wan
tong
tiao
mixed

shape_labels准确为：

standard
seven_pairs
all_pongs
pure_suit
other

验证：

- suit数组长度=4；
- shape数组长度=5；
- mixed索引=3；
- other索引=4；
- 标签和概率位置逐项对应；
- canonical序列化保留固定顺序；
- mapping插入顺序不影响输出；
- 无证据输入不得让任一类别概率等于1；
- 最小证据和最大公开证据场景已测试；
- 旧调用者对原字段保持兼容；
- 新增元数据为additive；
- 不修改模拟标签合同。

==================================================
五、信息边界回归
==================================================

重新确认修复没有破坏已通过的信息边界。

禁止读取：

- GameState authority；
- 对手暗手；
- 墙牌顺序；
- raw seed；
- future event；
- restricted label zone；
- TrainingTruth；
- oracle；
- 模型artifact；
- 网络；
- 外部AI；
- 全局RNG或隐藏缓存。

运行：

- 静态import检查；
- 禁止字段递归注入；
- 对手暗手扰动；
- 墙牌顺序扰动；
- raw seed扰动；
- restricted label扰动；
- 公开弃牌变化。

要求：

- 隐藏信息变化不改变正常输出；
- 禁止字段注入稳定返回FORBIDDEN_FEATURE；
- 公开信息变化允许按规则改变输出；
- P0信息泄漏finding=0。

==================================================
六、确定性与兼容性
==================================================

验证：

- 同输入100次输出一致；
- fresh-process至少5次一致；
- mapping顺序置换一致；
- 输出seat顺序稳定；
- canonical bytes稳定；
- SHA-256稳定；
- 不依赖worker调度顺序；
- 不引入随机状态；
- 既有MODEL-001调用兼容；
- fallback版本字段完整；
- input schema/version完整；
- malformed schema返回稳定PolicyInputError；
- MODEL-001状态不变。

==================================================
七、关闭 M001-R-F002
==================================================

检查：

T19-W01-MODEL001_evidence_manifest.csv

验证：

1. manifest_artifact_count与实际一致；
2. 普通工件均有完整SHA-256；
3. SHA-256均为64位小写十六进制；
4. byte_size准确；
5. path为仓库相对路径；
6. 当前commit tree重新计算哈希完全匹配；
7. 覆盖belief.py；
8. 覆盖专用测试；
9. 覆盖baseline gap report；
10. 覆盖dependency closure；
11. 覆盖test results；
12. 覆盖repair authorization；
13. 覆盖uncertainty解释批准记录；
14. 覆盖其他实际remediation工件；
15. manifest自身路径存在；
16. manifest自身sha256为null或设计规定的空值；
17. manifest自身hash_rule准确为：
    SELF_NON_CIRCULAR_EXCLUDED；
18. 没有伪造manifest自身哈希；
19. Git commit tree/blob负责绑定manifest自身；
20. manifest负责绑定其余工件；
21. 不存在循环哈希；
22. JSON/CSV均可解析；
23. 没有使用dirty主工作树文件替代commit tree文件。

输出：

manifest_row_count
manifest_regular_hashed_count
manifest_self_rule_count
missing_artifact_count
unexpected_artifact_count
invalid_sha256_count
hash_mismatch_count
self_reference_error_count

==================================================
八、测试独立复跑
==================================================

使用批准的Python 3.12环境。

不得安装或升级依赖。

分别运行：

1. 专用MODEL-001修复测试；
2. tests/spec_v3/test_model_001.py；
3. 合同测试；
4. PlayerView和信息边界测试；
5. entropy边界测试；
6. 类别顺序测试；
7. 100次同进程确定性；
8. 5次fresh-process确定性；
9. 全仓collection；
10. 全仓pytest。

记录：

python_version
pytest_version
full_commands
collection_count
passed
failed
skipped
skip_node_id
skip_reason
duration

开发报告参考值：

collection=468
passed=467
failed=0
skipped=1

如果数量不同：

- 列出新增、缺失或未收集测试；
- 判断是否由commit tree、插件或环境差异导致；
- 不得仅凭全绿通过。

唯一允许参考skip：

tests/test_f0013_dirty_update.py中的macOS Tk安全跳过。

必须确认与MODEL-001无关。

如果沙箱产生外部worktree写权限失败：

- 单独记录；
- 在批准的非沙箱测试环境复跑同一命令；
- 不得把真实业务失败误归类为沙箱问题。

==================================================
九、状态与声明
==================================================

确认：

- MODEL-001仍为INTEGRATED；
- 没有标记AUDITED；
- 没有声称外部校准通过；
- 没有声称现实有效性；
- 模拟数据仍只适用于SIMULATION；
- Task17历史状态未修改；
- 修复只恢复baseline生产闭包和fallback合同。

==================================================
十、Findings
==================================================

输出：

finding_id
severity
affected_commit
affected_file
affected_symbol
evidence
required_fix
blocking_scope

重点判断：

- 原M001-R-F001是否关闭；
- 原M001-R-F002是否关闭；
- 原M001-R-F003是否关闭；
- 是否产生新的P0/P1；
- 是否存在审批依据缺失；
- 是否存在证据哈希不一致。

==================================================
十一、最终结论
==================================================

只有以下条件全部满足才能输出：

MODEL001_BASELINE_REPAIR_INDEPENDENT_REVIEW_PASS

条件：

- 提交范围合规；
- 项目所有者审批依据有效；
- M001-R-F001关闭；
- M001-R-F002关闭；
- M001-R-F003关闭；
- entropy合同实现正确；
- 类别顺序正确；
- 信息边界通过；
- 确定性通过；
- 兼容性通过；
- manifest闭包完整；
- 专用测试通过；
- 合同测试通过；
- 全仓collection通过；
- 全仓0 failed；
- skip已解释且无关；
- 无开放P0/P1；
- MODEL-001保持INTEGRATED；
- Task17历史状态未修改。

否则输出：

MODEL001_BASELINE_REPAIR_INDEPENDENT_REVIEW_FAIL

本任务不得：

- 修改或修复文件；
- 创建tag；
- 集成提交；
- 更新tracker；
- 改变任何审计状态。
```

复审通过后，下一项操作才是在 Terminal 0 创建：

```
task19-w01-baseline-r1
```

该tag应精确指向：

```
2eeecb98a77e61e19489611c1b051eee8613d2be
```

不得移动或覆盖原来的 `task19-w01-baseline`。

**ChatGPT:**

只剩一个明确的设计一致性问题。建议采用审查报告的第一种方案：DEC-012 的 A/B/C 只改变性能阈值，三项统一使用冻结环境规定的：

```
warmup=100
measurement=1000
repeat=5
```

没有必要为 Option C 创建第二套性能环境。

## 修复提示词

```
运行终端：
Terminal 2

运行目录：
/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t2-w01

目标分支：
task19/w01-design-deterministic

任务性质：
RULE-015 最后一项设计一致性修复
```

在 Terminal 2 Codex 中粘贴：

```
修复 RULE015-DEC-012 Option C 与冻结性能环境不一致的问题。

当前开放finding：

R015-R3-F001

当前最终设计提交：

b786a61393924bfffb2902085740acc67d18a926

当前最终delta：

026f81d3c8902297e84bec4d94897ff374d2f145

批准的修复方向：

DEC-012的A/B/C只允许改变性能阈值。

三个选项统一使用冻结性能环境：

performance_environment_id：
RULE015-PERF-REF-V1-078dc25252299f3c

warmup_iterations=100
measurement_iterations=1000
repeat_count=5

禁止：

- 修改业务代码；
- 修改测试；
- 修改Locked/Frozen；
- 修改STATE-010；
- 修改Task17；
- 修改Task19权威tracker；
- 修改B2-A1；
- 修改其他11项决策；
- 修改E5口径；
- 重新生成不同环境ID；
- 预填selected_option；
- 批准DEC-012；
- amend已有提交；
- merge、rebase、cherry-pick或push。

一、修复DEC-012

将DEC-012三个选项统一为：

Option A：
P95 ≤ 2ms；
warmup=100；
measurement=1000；
repeat=5。

Option B：
P95 ≤ 5ms；
warmup=100；
measurement=1000；
repeat=5。

Option C：
P95 ≤ 10ms；
warmup=100；
measurement=1000；
repeat=5。

要求：

- A/B/C只在阈值上不同；
- 三项引用同一performance_environment_id；
- 三项引用同一fixture及SHA-256；
- 三项使用相同计时器；
- 三项使用相同nearest-rank P95算法；
- 三项使用相同异常/超时处理；
- 三项使用相同单进程、单线程约束；
- recommended_option仍为B；
- selected_option保持空；
- approval_status=PENDING；
- 不得提前固定最终threshold。

二、检查所有引用

检查并仅在必要时同步修复：

- RULE-015_decision_matrix.csv；
- RULE-015_acceptance_matrix.csv中的AC-12；
- RULE-015_e4_scenarios.csv；
- RULE-015_performance_environment.json；
- RULE-015_design_review.md；
- RULE-015_approval_form.md；
- 其他T19-D02中引用DEC-012的设计文件。

最终必须满足：

- 不存在200 warmups；
- 不存在2000 measurements；
- 所有性能场景均为100/1000/5；
- environment ID保持不变；
- fixture SHA保持不变；
- AC-12保持WAITING_APPROVAL；
- E4 performance_result保持WAITING_APPROVAL；
- selected_threshold仍为空或null；
- 设计中不存在第二套性能环境。

三、设计修复提交

本提交只允许修改：

docs/spec-v3/task19/design/T19-D02/

不得修改progress delta。

执行：

- CSV/JSON解析检查；
- 全目录搜索200和2000旧口径；
- environment ID重算；
- fixture SHA重算；
- AC-12/E4/DEC-012交叉一致性检查；
- git diff --check。

确认无其他变化后提交：

git commit -m "task19(T19-D02): align RULE-015 performance options"

记录：

rule015_performance_fix_commit

四、metadata提交

取得rule015_performance_fix_commit后，只修改：

docs/spec-v3/task19/progress_deltas/RULE-015_progress_delta.json

要求：

- design_commit_sha更新为rule015_performance_fix_commit；
- proposed_status=WAITING_FOR_DESIGN_APPROVAL；
- next_required_action=OWNER_DECISION；
- 不引用delta自身commit SHA；
- 不请求READY_FOR_IMPLEMENTATION；
- generated_at更新；
- 其他字段无无关变化。

提交：

git commit -m "task19(T19-D02): bind aligned RULE-015 performance design"

记录：

rule015_performance_delta_commit

五、最终验证

确认：

- 两个新提交均以baseline为祖先；
- 既有提交未改写；
- design提交只修改T19-D02；
- delta提交只修改progress delta；
- DEC-012 A/B/C分别为2/5/10ms；
- 三项均为100/1000/5；
- environment ID未改变；
- selected_option为空；
- DEC-012=PENDING；
- 工作树干净；
- staged=0；
- 未修改业务代码或测试；
- 未push。

最终输出：

RULE015_PERFORMANCE_OPTIONS_ALIGNED

并报告：

rule015_performance_fix_commit
rule015_performance_delta_commit
option_a_threshold_ms
option_b_threshold_ms
option_c_threshold_ms
warmup_iterations
measurement_iterations
repeat_count
performance_environment_id
remaining_200_count
remaining_2000_count
dec012_status
worktree_clean
```

完成后下一步在 Terminal 0 只需复审 `R015-R3-F001` 是否关闭；无需再重审已经通过的E5、STATE-010和其余11项决策。

> [!QUESTION] User
> TRAIN009_PROGRESS_DELTA_REMEDIATED - train009_delta_remediation_commit: cdd5177f35ddc81c39508f646f7eec7552ab4565 - changed_paths: docs/spec-v3/task19/progress_deltas/TRAIN-009_progress_delta.json - design_commit_sha: 644d9d820448b5de6ac1d0821ddf384756502883 - pending_decision_range: T03-DEC-001..007 - proposed_status: WAITING_FOR_DESIGN_APPROVAL - worktree_clean: true - staged_count: 0 - push_executed: false 本轮仅修复一行 metadata；父提交为 1c1da899d361ed0e927a16a4c4afcfd7876e6e86，未修改设计、代码、测试或权威状态。 下一步：Terminal 0 可只读复审新提交；建议触发语：复审 TRAIN-009 delta 修复提交。

> [!NOTE] ChatGPT
> 下一步在 Terminal 0 进行范围很小的只读复审，只检查 TRAIN-009 progress delta。
> 
> ```
> 运行终端：
> Terminal 0
> 
> 运行目录：
> /Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer
> 
> 目标分支：
> 不切换分支；保持当前主工作树不变
> 
> 任务性质：
> TRAIN-009 progress delta 修复提交只读复审
> ```
> 
> 在 Terminal 0 Codex 中粘贴：
> 
> ```
> 复审 TRAIN-009 delta 修复提交。
> 
> 目标提交：
> 
> cdd5177f35ddc81c39508f646f7eec7552ab4565
> 
> 预期parent：
> 
> 1c1da899d361ed0e927a16a4c4afcfd7876e6e86
> 
> TRAIN-009设计提交：
> 
> 644d9d820448b5de6ac1d0821ddf384756502883
> 
> Baseline：
> 
> task19-w01-baseline
> 65e8dcb1679466c9e37d10e5a4299a09774332d9
> 
> 本任务只读。
> 
> 禁止：
> 
> - checkout或switch；
> - 修改文件；
> - git add/commit；
> - cherry-pick；
> - merge；
> - rebase；
> - 更新权威tracker；
> - 批准决策；
> - 标记READY_FOR_IMPLEMENTATION；
> - push；
> - stash/clean/reset。
> 
> 必须读取目标commit tree，不得使用当前dirty工作树同名文件。
> 
> 一、提交身份和范围
> 
> 验证：
> 
> 1. cdd5177f存在；
> 2. parent精确为1c1da899；
> 3. baseline为其祖先；
> 4. 只修改：
>    docs/spec-v3/task19/progress_deltas/TRAIN-009_progress_delta.json；
> 5. 没有修改设计文件；
> 6. 没有修改业务代码；
> 7. 没有修改测试；
> 8. 没有修改Locked/Frozen；
> 9. 没有修改Task17；
> 10. 没有修改权威tracker、LATEST或changelog；
> 11. Terminal 3 worktree干净；
> 12. 主工作树staged=0。
> 
> 二、修复Finding T009-RR-001
> 
> 读取修复前后delta并验证：
> 
> - 修复前blocking_change只覆盖T03-DEC-001..006；
> - 修复后准确覆盖T03-DEC-001..007；
> - 不遗漏DEC-007；
> - 不出现DEC-008或其他未知decision；
> - pending_decision_count=7；
> - decision ID集合精确为：
>   T03-DEC-001
>   T03-DEC-002
>   T03-DEC-003
>   T03-DEC-004
>   T03-DEC-005
>   T03-DEC-006
>   T03-DEC-007。
> 
> 三、其余字段未回退
> 
> 确认：
> 
> - design_commit_sha完整等于：
>   644d9d820448b5de6ac1d0821ddf384756502883；
> - proposed_status=WAITING_FOR_DESIGN_APPROVAL；
> - next_required_action=OWNER_DECISION；
> - 不记录delta自身commit SHA；
> - 不存在SHA循环；
> - 不请求READY_FOR_IMPLEMENTATION；
> - 不请求AUDITED；
> - generated_by=Terminal 3；
> - JSON有效；
> - 除必要metadata和generated_at外没有无关字段变化；
> - delta现在可以独立吸收。
> 
> 四、确认设计门禁引用
> 
> 只读确认此前已通过的TRAIN-009设计结论没有被该metadata提交修改：
> 
> - design decision count=7；
> - missing Option C=0；
> - unquantified AC=0；
> - E4=4；
> - E5=14；
> - unresolved unnumbered decision=0；
> - approval form=PENDING；
> - business_code_authorized=false。
> 
> 不需要重新全面审计设计内容，只确认提交没有改变设计tree。
> 
> 五、最终结论
> 
> 只有全部检查通过才能输出：
> 
> TRAIN009_PROGRESS_DELTA_REVIEW_PASS
> 
> 否则输出：
> 
> TRAIN009_PROGRESS_DELTA_REVIEW_FAIL
> 
> 失败时报告：
> 
> finding_id
> severity
> affected_file
> affected_field
> evidence
> required_fix
> blocking_scope
> 
> 通过时同时确认：
> 
> TRAIN009_DESIGN_READY_FOR_OWNER_DECISION
> 
> 并输出7项决策ID清单，但不得替项目所有者选择。
> 
> 本轮不得：
> 
> - 修改或集成文件；
> - 吸收progress delta；
> - 批准决策；
> - 更新tracker；
> - 创建实施授权。
> ```
> 
> 通过后，AUDIT-010和TRAIN-009就都具备所有者审批入口，可以分别审批，仍不需要等待RULE-015。

> [!QUESTION] User
> TRAIN009_PROGRESS_DELTA_REVIEW_PASS TRAIN009_DESIGN_READY_FOR_OWNER_DECISION 验证结果 - 目标提交存在：cdd5177f35ddc81c39508f646f7eec7552ab4565 - parent 精确为：1c1da899d361ed0e927a16a4c4afcfd7876e6e86 - baseline 65e8dcb1679466c9e37d10e5a4299a09774332d9 是其祖先。 - 唯一修改路径为 docs/spec-v3/task19/progress_deltas/TRAIN-009_progress_delta.json。 - 与前一提交相比仅修改 blocking_change 一行，未修改 generated_at 或其他字段。 - TRAIN-009 设计树与 644d9d820448b5de6ac1d0821ddf384756502883 完全一致。 - 未修改设计、业务代码、测试、Locked/Frozen、Task 17、权威 tracker、LATEST 或 changelog。 - Terminal 3 worktree 干净；主工作树 staged 文件数为 0。 Finding 关闭 T009-RR-001 已关闭： - 修复前：T03-DEC-001..006 remain PENDING - 修复后：T03-DEC-001..007 remain PENDING - pending decision 数：7 - 未遗漏 DEC-007 - 未出现 DEC-008 或未知决策 决策 ID 精确集合： T03-DEC-001 T03-DEC-002 T03-DEC-003 T03-DEC-004 T03-DEC-005 T03-DEC-006 T03-DEC-007 Delta 门禁 - JSON 有效 - design_commit_sha=644d9d820448b5de6ac1d0821ddf384756502883 - commit_sha 同样指向设计提交，不记录 delta 自身 SHA - 无 SHA 循环 - proposed_status=WAITING_FOR_DESIGN_APPROVAL - next_required_action=OWNER_DECISION - generated_by=Terminal 3 - 未请求 READY_FOR_IMPLEMENTATION - 未请求 AUDITED - delta 现在可由 Terminal 0 独立吸收，但本轮未执行吸收 设计引用确认 check result ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ━━━━━━━━━ decision_count 7 ────────────────────────────────────── ───────── missing_option_c_count 0 ────────────────────────────────────── ───────── unquantified_ac_count 0 ────────────────────────────────────── ───────── e4_scenario_count 4 ────────────────────────────────────── ───────── e5_row_count 14 ────────────────────────────────────── ───────── unresolved_unnumbered_decision_count 0 ────────────────────────────────────── ───────── approval_form PENDING ────────────────────────────────────── ───────── business_code_authorized false 本轮已完成情况 完成目标提交的只读身份、范围、前后差异、设计树及门禁引用复审。未修改、集成或批准任何内容，未更新权威状态。 下一步完整任务清单 1. 项目所有者填写 TRAIN-009 七项决策；产出独立 approval commit。 2. Terminal 0 只读复核 approval commit；依赖七项选择完整且无接口冲突。 3. Terminal 0 按批准的提交顺序集成设计、delta remediation 和 approval commit。 4. 验证 delta 后再更新权威 tracker；当前不得标记 READY_FOR_IMPLEMENTATION。 5. 实现仍需单独明确授权；本次复审不构成业务编码授权。

> [!NOTE] ChatGPT
> TRAIN-009 已具备所有者审批入口。现在 AUDIT-010 和 TRAIN-009 都可审批，但应分别形成审批记录。
> 
> AUDIT-010 的5项决策内容已经完整，可以先批准。建议全部选择 A：
> 
> ```
> 批准 AUDIT-010 设计决策：
> 
> A04-DEC-001=A
> A04-DEC-002=A
> A04-DEC-003=A
> A04-DEC-004=A
> A04-DEC-005=A
> ```
> 
> TRAIN-009 目前只有决策 ID，没有看到7项 A/B/C 的具体内容。不要盲目全部选推荐项。先由 Terminal 0 提取完整决策表。
> 
> ```
> 运行终端：
> Terminal 0
> 
> 运行目录：
> /Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer
> 
> 目标分支：
> 不切换分支
> 
> 任务性质：
> 只读提取 TRAIN-009 所有者决策表
> ```
> 
> 在 Terminal 0 Codex 中粘贴：
> 
> ```
> 从目标commit tree只读提取TRAIN-009完整所有者决策表。
> 
> TRAIN-009设计提交：
> 
> 644d9d820448b5de6ac1d0821ddf384756502883
> 
> 最终delta修复提交：
> 
> cdd5177f35ddc81c39508f646f7eec7552ab4565
> 
> 当前结论：
> 
> TRAIN009_DESIGN_READY_FOR_OWNER_DECISION
> 
> 禁止：
> 
> - 修改文件；
> - checkout/switch；
> - cherry-pick；
> - merge；
> - rebase；
> - git add/commit；
> - 更新tracker；
> - 批准决策；
> - 标记READY_FOR_IMPLEMENTATION；
> - push。
> 
> 必须读取目标commit tree，不得使用当前工作树同名文件。
> 
> 一、提取7项决策
> 
> 按审批顺序输出：
> 
> T03-DEC-001
> T03-DEC-002
> T03-DEC-003
> T03-DEC-004
> T03-DEC-005
> T03-DEC-006
> T03-DEC-007
> 
> 每项必须完整输出：
> 
> decision_id
> question
> option_a
> option_b
> option_c
> recommended_option
> recommendation_reason
> compatibility_impact
> interface_impact
> test_impact
> affected_units
> blocked_units
> approval_dependencies
> terminal0_recommendation
> selected_option
> owner_comment
> 
> selected_option和owner_comment保持空。
> 
> 二、重点解释
> 
> 明确说明每项选择会如何影响：
> 
> - engine/rng_v2.py::STREAMS；
> - 是否需要ADDITIVE_INTERFACE；
> - 是否触发BREAKING_CHANGE；
> - Observation兼容；
> - episode assignment；
> - worker count变化；
> - artifact原子发布；
> - partial/orphan恢复；
> - restricted artifact隔离；
> - MODEL-001外部数据门禁；
> - TRAIN-009后续测试和E4/E5。
> 
> 三、审批顺序
> 
> 输出准确依赖顺序。
> 
> 如果某项依赖前一项选择，明确写出：
> 
> depends_on_decision
> required_selected_option
> 
> 不得把存在依赖的7项作为无序批量选择。
> 
> 四、风险建议
> 
> 对每项给出：
> 
> recommended_option
> alternative_risk
> breaking_change_risk
> implementation_complexity
> audit_risk
> 
> 如果推荐选项需要新增stream或接口，必须明确说明它是：
> 
> REUSE_AS_IS
> COMPATIBLE_ADAPTER
> ADDITIVE_INTERFACE
> BREAKING_CHANGE
> DECISION_REQUIRED
> 
> 五、输出可填写表
> 
> 最后输出：
> 
> decision_id,selected_option,owner_comment
> T03-DEC-001,,
> T03-DEC-002,,
> T03-DEC-003,,
> T03-DEC-004,,
> T03-DEC-005,,
> T03-DEC-006,,
> T03-DEC-007,,
> 
> 本任务不得审批、修改、集成或更新状态。
> ```
> 
> 把7项完整决策表发给我后，我可以逐项判断，不建议在未看到选项前直接批准 TRAIN-009。审批完成后，审批记录和 approval commit 应在：
> 
> ```
> 运行终端：Terminal 3
> 运行目录：.../wt-task19-t3-w01
> ```
> 
> 中分别生成，不能由 Terminal 0 代替项目所有者做选择。

> [!QUESTION] User
> MODEL001_BASELINE_REPAIR_INDEPENDENT_REVIEW_FAIL Findings finding_id M001-R2-F004 severity P1 affected_commit 2eeecb98a77e61e19489611c1b051eee8613d2be affected_file / symbol /tmp/model001-audit.J37nbi/docs/spec-v3/task19/checkpoint/remediation/MODEL001_uncertainty_interpretation_approval.md:3 evidence 文档自称 APPROVED INTERPRETATION，但没有项目所有者身份、明确授权语句、时间或可追溯授权引用；无法证明 approval_basis 来自项目所有者。 required_fix 由项目所有者明确批准该解释并提交可追溯审批依据；之后重新独立审查。 blocking_scope 阻止 remediation PASS ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── finding_id M001-R2-F005 severity P1 affected_commit 2eeecb98a77e61e19489611c1b051eee8613d2be affected_file / symbol /tmp/model001-audit.J37nbi/players/humanlike/belief.py:35, _MODEL_001_FORBIDDEN_FIELDS evidence 递归注入 GameState、TrainingTruth、model_artifact 均被接受并返回正常结果，而非稳定返回 FORBIDDEN_FEATURE。这些值当前未影响输出，故未 证实 P0 泄漏。 required_fix 扩充禁止字段规范化和递归拒绝测试，覆盖全部明确禁止的信息类型。 blocking_scope 阻止信息边界与总体 PASS P0 findings：0。开放 P1 findings：2。 原 Findings 状态 - M001-R-F001：技术实现已关闭。独立 oracle 验证 H(cleared)+H(suit)+H(shape)、零概率、ln(20)、ln(40)、有限性、范围、归一误差和非法概率拒绝均正确。 - M001-R-F002：已关闭。Manifest 闭包、哈希、大小和 self-rule 全部正确。 - M001-R-F003：已关闭。标签、长度、索引、固定顺序、additive 元数据和旧字段兼容均正确。 - 总体仍失败：缺少可证明的所有者审批，且禁止字段递归注入合同不完整。 提交与范围 - Baseline tag 为 annotated tag；task19-w01-baseline^{} 正确解析到 65e8dcb1679466c9e37d10e5a4299a09774332d9。 - 7b8f27e^ = 65e8dcb...；2eeecb9^ = 7b8f27e...；baseline 是两者祖先，原修复提交未被重写。 - Remediation changed paths 共 8 个： - players/humanlike/belief.py - tests/spec_v3/test_t19_model001_baseline_repair.py - MODEL001_uncertainty_interpretation_approval.md - baseline gap report - dependency closure - evidence manifest - repair authorization - test results - 生产代码仅修改批准的 belief.py；测试仅修改专用 remediation 测试。 - test_model_001.py、Locked/Frozen、模拟标签合同、Task17、Task19 tracker、LATEST.md、changelog 均未修改。 - 未创建模型 artifact 或模拟数据。 - 主 worktree 干净；staged=0。 - 当前分支无 upstream，远端 refs 不包含 2eeecb9：可验证范围内未 push。 Manifest manifest_row_count=12 manifest_regular_hashed_count=11 manifest_self_rule_count=1 missing_artifact_count=0 unexpected_artifact_count=0 invalid_sha256_count=0 hash_mismatch_count=0 self_reference_error_count=0 Manifest 自身使用准确的 SELF_NON_CIRCULAR_EXCLUDED，sha256=null、byte_size=null；其余 11 个工件均由完整小写 SHA-256 绑定。 测试结果 环境： Python 3.12.13 pytest 9.1.1 目标 commit 通过 git archive 2eeecb9 导出到 /tmp/model001-audit.J37nbi；所有静态检查、哈希和测试均在那里执行，未读取 dirty 同名文件。 主要命令及结果： python -m pytest -p no:cacheprovider -q -rs tests/spec_v3/test_t19_model001_baseline_repair.py 19 passed in 0.43s python -m pytest -p no:cacheprovider -q -rs tests/spec_v3/test_model_001.py 1 passed in 0.04s python -m pytest -p no:cacheprovider -q -rs tests/contracts \ tests/humanlike_v2/test_player_view_v2.py \ tests/humanlike_v2/test_deterministic_policy.py \ tests/spec_v3/test_rule_016.py tests/spec_v3/test_algo_010.py 30 passed in 0.17s python -m pytest -p no:cacheprovider --collect-only -q 468 tests collected in 0.74s python -m pytest -p no:cacheprovider -q -rs 467 passed, 1 skipped in 43.34s 唯一 skip： tests/test_f0013_dirty_update.py:122 macOS Tk() construction safety skip 该 skip 与 MODEL-001 无关。Collection 和完整结果精确匹配开发参考值；无沙箱业务失败。 状态确认 - MODEL-001 保持 INTEGRATED，未标记 AUDITED。 - 未声称外部校准或现实有效性。 - 模拟数据用途仍限于 SIMULATION。 - Task17 历史状态未修改。 - 修复范围仍是 baseline 生产闭包及 fallback 合同恢复。 本轮已完成情况 - 目标：独立复审 remediation commit。 - 交付物：本回复中的只读审计结果；仓库文件无修改。 - 状态变更：无；MODEL-001 仍为 INTEGRATED。 - 未完成/偏差：由于两个开放 P1，不满足 PASS 门禁。 - 风险：所有者审批 provenance 不可证；禁止字段表可能继续遗漏语义别名。 下一步完整任务清单 1. 立即下一步：项目所有者明确批准 uncertainty interpretation；产出可追溯审批记录；依赖当前 P1；建议触发语：批准 MODEL-001 uncertainty interpretation。 2. 修复信息边界：补齐 GameState、TrainingTruth、模型 artifact 及别名的递归拒绝；产出代码和专用测试；依赖 Approved 修复规格；建议触发语：修复 MODEL-001 禁止字 段注入。 3. 更新 remediation manifest 和测试证据；依赖修复提交完成；建议触发语：刷新 MODEL-001 remediation 证据。 4. 重新独立复审同一门禁集；依赖新 remediation commit；建议触发语：独立复审新的 MODEL-001 remediation commit。 5. 仅在复审 PASS 后继续 Task19 队列；不得提前标记 AUDITED 或修改权威 tracker。

**ChatGPT:**

本次失败结论合理：F004 是审批取证缺口，F005 是真实的信息边界缺陷。现在不能集成 MODEL-001 修复，也不能解除 B2-A1 阻塞。

先由你以项目所有者身份明确回复以下授权语句：

```
批准 MODEL-001 uncertainty interpretation。

OWNER-DECISION-ID：MODEL001-UNCERTAINTY-001
批准内容：
uncertainty = H(cleared) + H(dominant_suit) + H(shape)

其中：
- cleared 类别数为 2；
- dominant_suit 固定顺序为 wan、tong、tiao、mixed，类别数为 4；
- shape 固定顺序为 standard、seven_pairs、all_pongs、pure_suit、other，类别数为 5；
- 联合类别数 K = 2 × 4 × 5 = 40；
- uncertainty 数值范围为 [0, ln(40)]；
- 允许保留各分量 entropy 作为解释性元数据；
- 本批准仅用于 MODEL-001 deterministic fallback 的合同解释和测试；
- 不代表批准外部校准、现实有效性或将 MODEL-001 升级为 AUDITED。

同时批准修复 MODEL-001 信息边界：
递归拒绝 GameState、TrainingTruth、model artifact 以及经大小写、下划线、连字符、空格和常见字段包装变化形成的语义别名。违规输入必须稳定返回 FORBIDDEN_FEATURE。

批准人：项目所有者
批准日期：以提交审批记录时的当前日期为准
```

你明确发送上述批准后，在 MODEL-001 修复终端运行下面的提示词。

* * *

## MODEL-001 第三轮修复提示词

**运行终端：** MODEL-001 Baseline Repair Terminal **运行目录：** `/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t0-model001-repair` **目标分支：** `task19/w01-baseline-repair-model001` **任务性质：** 经所有者批准的定向修复；允许修改限定代码、专用测试和 remediation 证据；禁止集成和状态升级

```
执行 MODEL-001 remediation 第三轮修复，关闭独立审计发现：

- M001-R2-F004：所有者审批 provenance 不可证明
- M001-R2-F005：禁止信息类型及其语义别名可通过递归输入

前置条件：

1. 当前分支必须为：
   task19/w01-baseline-repair-model001

2. 当前 HEAD 必须包含：
   7b8f27e38a3bbb158b276d478024eea70354ef8b
   2eeecb98a77e61e19489611c1b051eee8613d2be

3. 开始前检查：
   git status --short
   git branch --show-current
   git log --oneline -5

4. 如工作树存在非本任务修改，立即停止并报告。

一、记录项目所有者审批

将项目所有者刚刚明确发送的批准原文写入独立审批记录，不得自行改写批准结论。

审批记录至少包含：

- decision_id=MODEL001-UNCERTAINTY-001
- status=APPROVED
- approver_role=PROJECT_OWNER
- 批准原文
- 批准日期和记录日期
- uncertainty 精确定义
- K=40 及 [0,ln(40)] 范围
- 固定类别顺序
- 适用范围
- 明确排除外部校准、现实有效性和 AUDITED 升级
- 所有者消息的可追溯来源说明
- 被替代或补充的旧解释记录
- 本审批记录对应的实现提交及证据关系

不得继续使用无法证明来源的“APPROVED INTERPRETATION”自声明。
旧文件若保留，必须明确标注其审批依据已由新的 owner decision 补充，不得伪造历史审批时间。

二、修复递归禁止信息检测

仅在批准范围内修改：

- players/humanlike/belief.py
- tests/spec_v3/test_t19_model001_baseline_repair.py
- MODEL-001 remediation 审批、测试、manifest 和相关证据文件

不得修改：

- Locked/Frozen 规格
- tests/spec_v3/test_model_001.py
- 模拟标签合同
- Task 17 历史状态
- Task 19 权威 tracker
- LATEST.md
- changelog
- 其他批次业务代码或测试断言

完善禁止信息检测，使输入树任意深度中的以下内容均被拒绝：

1. GameState；
2. TrainingTruth；
3. model artifact；
4. 对手暗手；
5. 墙牌顺序；
6. raw seed；
7. future event；
8. restricted label；
9. oracle/training truth；
10.现有合同明确禁止的其他类型。

检测范围至少覆盖：

- Mapping 的键和值；
- list、tuple、set 中的元素；
- 嵌套 DTO/dataclass/object 的公开字段；
- 类型名称；
- schema/type/kind/class/name 等包装字段；
- 大小写变化；
- snake_case、kebab-case、空格和紧凑写法；
- 已批准的常见语义别名。

采用统一、确定性的名称规范化方法，例如：

- Unicode/字符串稳定转换；
- casefold；
- 去除或统一空格、下划线和连字符；
- 显式别名映射到禁止语义类别。

不得采用会把正常牌局公开字段大量误判为禁止信息的宽泛子字符串规则。

发现禁止信息后必须：

- 返回或抛出合同规定的 PolicyInputError；
- error_code 精确为 FORBIDDEN_FEATURE；
- 错误结果不泄露禁止字段的具体值；
- 同一输入重复执行结果完全一致；
- 在任何概率计算前拒绝输入。

三、补充直接测试

至少增加以下测试：

1. 顶层及多层嵌套 GameState；
2. GameState、game_state、game-state、GAME STATE、gamestate；
3. TrainingTruth 及同类规范化变体；
4. model_artifact、model-artifact、ModelArtifact；
5. 禁止名称出现在 key、value、type/kind/class/name 包装字段；
6. 禁止对象出现在 list、tuple 和嵌套 Mapping；
7. 现有对手暗手、墙顺序、raw seed、future event、restricted label 和 oracle；
8. 每项均稳定产生 FORBIDDEN_FEATURE；
9. 错误消息不得包含注入的秘密值；
10. 合法公开 PlayerView 输入不得被误拒绝；
11. 正常公开字段的近似名称不得产生明显误报；
12. 输入对象不得被修改；
13. 相同输入 100 次结果一致；
14. 新检查不得改变已批准的概率、entropy 和类别顺序合同。

测试必须验证真实生产入口，不得仅测试复制到测试文件中的辅助逻辑。

四、刷新证据闭包

更新：

- owner approval/provenance 记录；
- baseline gap report；
- dependency closure；
- repair authorization；
- test results；
- remediation evidence manifest。

Manifest 要求：

- 覆盖本轮全部 remediation 工件；
- 普通文件记录实际 SHA-256 和 byte size；
- manifest 自身继续采用 SELF_NON_CIRCULAR_EXCLUDED；
- 不得填写 manifest 自身的伪造哈希；
- 不得引用工作树之外或尚未提交的临时文件；
- 所有路径必须是仓库相对路径。

五、验证

使用项目 Python 3.12 环境执行：

1. 专用 remediation 测试；
2. 既有 MODEL-001 测试；
3. contracts、PlayerView 和信息边界测试；
4. pytest collection；
5. 全仓回归；
6. git diff --check；
7. manifest 哈希、大小、缺失项和 self-rule 校验；
8. 同进程 100 次确定性检查；
9. fresh-process 至少 5 次 canonical hash 检查。

不得使用 skip、xfail、删除测试或弱化断言规避失败。

六、提交规则

全部验证通过后创建一个新的 remediation 提交，不得 amend 或重写：

- 7b8f27e
- 2eeecb9

提交信息建议：

fix(model001): close approval and forbidden-input findings

使用显式路径 git add，不得使用 git add .。

不得：

- merge；
- cherry-pick；
- push；
- 创建或移动 tag；
- 更新权威 tracker；
- 将 MODEL-001 标记为 AUDITED；
- 声称外部校准已经完成。

七、最终报告

必须输出：

MODEL001_BASELINE_REPAIR_R3_READY_FOR_INDEPENDENT_REVIEW

并列明：

- 新提交完整 SHA；
- parent SHA；
- 修改路径；
- owner decision ID；
- 审批记录路径；
- 禁止语义类别清单；
- 别名规范化规则；
- 新增测试数量及结果；
- collection/passed/failed/skipped；
- manifest 行数及哈希验证结果；
- MODEL-001 状态仍为 INTEGRATED；
- worktree_clean；
- staged_count；
- push_executed=false。

最后给出下一步：

在独立审计终端只读复审新的 remediation commit。
不得由本终端自行宣告审计 PASS。
```

顺序必须是：你明确批准 → 修复终端提交 R3 → 独立审计终端复审 → PASS 后才由 Terminal 0 集成。

> [!QUESTION] User
> 在哪个终端运行

> [!NOTE] ChatGPT
> 分成两步，使用两个不同终端。
> 
> 1.  所有者批准：直接在当前 ChatGPT 对话中发送，不在任何 Codex 终端运行。
>     
> 
> 请先回复：
> 
> ```
> 批准 MODEL-001 uncertainty interpretation，并批准修复 MODEL-001 禁止字段注入。
> 
> OWNER-DECISION-ID：MODEL001-UNCERTAINTY-001
> ```
> 
> 2.  修复任务：在 MODEL-001 修复终端运行，也就是之前创建修复提交 `7b8f27e` 和 `2eeecb9` 的终端。
>     
> 
> ```
> cd "/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t0-model001-repair"
> codex
> ```
> 
> 目标分支应为：
> 
> ```
> task19/w01-baseline-repair-model001
> ```
> 
> 进入 Codex 后，先确认：
> 
> ```
> git branch --show-current
> git status --short
> git log --oneline -3
> ```
> 
> 确认分支正确、工作树干净且包含 `2eeecb9` 后，再粘贴上一条回复中的“MODEL-001 第三轮修复提示词”。
> 
> 修复提交完成后，独立复审必须换一个全新的 Codex 会话（建议 Terminal 4），不能在修复终端自审。

> [!QUESTION] User
> 批准 MODEL-001 uncertainty interpretation，并批准修复 MODEL-001 禁止字段注入。 OWNER-DECISION-ID：MODEL001-UNCERTAINTY-001

> [!NOTE] ChatGPT
> 所有者决策已明确。现在可以执行 MODEL-001 第三轮修复。
> 
> -   运行终端：MODEL-001 Baseline Repair Terminal
>     
> -   运行目录：`/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t0-model001-repair`
>     
> -   目标分支：`task19/w01-baseline-repair-model001`
>     
> -   任务性质：经所有者批准的定向修复
>     
> 
> 先进入正确目录：
> 
> ```
> cd "/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t0-model001-repair"
> codex
> ```
> 
> 然后将我上一条回复中的“MODEL-001 第三轮修复提示词”完整粘贴到该 Codex 会话中，并在提示词最前面补充：
> 
> ```
> 项目所有者现已明确批准：
> 
> 批准 MODEL-001 uncertainty interpretation，并批准修复 MODEL-001 禁止字段注入。
> 
> OWNER-DECISION-ID：MODEL001-UNCERTAINTY-001
> 
> 该批准仅授权：
> 1. uncertainty 合同解释的可追溯记录；
> 2. MODEL-001 禁止字段及语义别名的递归拒绝修复；
> 3. 对应专用测试和 remediation 证据刷新。
> 
> 不得据此升级 MODEL-001 的 INTEGRATED 状态，不代表外部校准或现实有效性已经完成。
> ```
> 
> 修复完成后，不要在该终端自行审计。下一步应在全新的 Terminal 4 中执行独立复审。

> [!NOTE] ChatGPT
> 这份附件不是 MODEL-001 第三轮修复结果，而是 **TRAIN-009 七项待审批决策表**。内容完整，依赖关系清楚，可以进入项目所有者审批。
> 
> 建议选择：
> 
> | 决策 | 建议 | 核心理由 |
> | --- | --- | --- |
> | T03-DEC-001 | A | 复用 training_noise，避免增加或破坏 RNG stream |
> | T03-DEC-002 | B | 通过公开 DomainSummary adapter 保持 Observation v2 不变 |
> | T03-DEC-003 | A | 使用人工批准的有限 tuple，最容易证明组合合法 |
> | T03-DEC-004 | A | 与 DEC-003 的有限目录匹配，保留总体 5ms 预算 |
> | T03-DEC-005 | A | 不兼容 profile 硬拒绝，避免静默行为变化 |
> | T03-DEC-006 | A | 保留24小时诊断窗口，同时限制存储生命周期 |
> | T03-DEC-007 | A | worker ID 不进入坐标，保证 1-vs-N 逐 episode 等价 |
> 
> 如果接受，请直接在当前 ChatGPT 对话回复：
> 
> ```
> 批准 TRAIN-009 设计决策：
> 
> T03-DEC-001=A
> T03-DEC-002=B
> T03-DEC-003=A
> T03-DEC-004=A
> T03-DEC-005=A
> T03-DEC-006=A
> T03-DEC-007=A
> 
> OWNER-DECISION-ID：TRAIN009-DESIGN-001
> 
> 批准范围仅限 TRAIN-009 设计合同和后续审批记录，不构成业务代码实施授权，不允许将 TRAIN-009 标记为 READY_FOR_IMPLEMENTATION 或 AUDITED。
> ```
> 
> 审批后写入审批记录的位置是：
> 
> -   运行终端：Terminal 3
>     
> -   运行目录：`/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t3-w01`
>     
> -   目标分支：`task19/w01-design-audit-training`
>     
> -   任务性质：仅生成 TRAIN-009 approval commit，不得实施代码
>     
> 
> MODEL-001 第三轮修复仍应在 MODEL-001 Repair Terminal 单独执行，两项任务不要混用终端。

> [!QUESTION] User
> 批准 TRAIN-009 设计决策： T03-DEC-001=A T03-DEC-002=B T03-DEC-003=A T03-DEC-004=A T03-DEC-005=A T03-DEC-006=A T03-DEC-007=A OWNER-DECISION-ID：TRAIN009-DESIGN-001 批准范围仅限 TRAIN-009 设计合同和后续审批记录，不构成业务代码实施授权，不允许将 TRAIN-009 标记为 READY_FOR_IMPLEMENTATION 或 AUDITED。

**ChatGPT:**

TRAIN-009 七项设计决策已由项目所有者明确批准。现在只生成审批记录提交，不实施业务代码。

-   运行终端：Terminal 3
    
-   运行目录：`/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t3-w01`
    
-   目标分支：`task19/w01-design-audit-training`
    
-   任务性质：TRAIN-009 所有者审批记录提交；禁止编码和状态升级
    

先进入终端：

```
cd "/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t3-w01"
codex
```

然后粘贴以下提示词：

```
执行 TRAIN-009 项目所有者设计决策记录任务。

运行终端：Terminal 3
运行目录：
/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t3-w01

目标分支：
task19/w01-design-audit-training

任务性质：
仅记录已经明确作出的项目所有者决策并创建独立 approval commit。
本任务不授权业务代码实施，不授权 READY_FOR_IMPLEMENTATION 或 AUDITED 状态。

一、项目所有者原始批准

必须将以下批准内容完整、准确地写入可追溯审批记录，不得修改选择，不得自行增加授权范围：

批准 TRAIN-009 设计决策：

T03-DEC-001=A
T03-DEC-002=B
T03-DEC-003=A
T03-DEC-004=A
T03-DEC-005=A
T03-DEC-006=A
T03-DEC-007=A

OWNER-DECISION-ID：TRAIN009-DESIGN-001

批准范围仅限 TRAIN-009 设计合同和后续审批记录，不构成业务代码实施授权，不允许将 TRAIN-009 标记为 READY_FOR_IMPLEMENTATION 或 AUDITED。

approver_role：
PROJECT_OWNER

二、执行前门禁

执行：

git branch --show-current
git status --short
git log --oneline --decorate -12

必须确认：

1. 当前分支精确为：
   task19/w01-design-audit-training

2. 工作树干净。

3. 以下提交均存在于当前历史中或可从当前分支验证：
   - TRAIN-009 原始设计提交：
     8632d128f005694c38f1d0e5c0e1092afd22a257
   - TRAIN-009 remediation 设计提交：
     644d9d820448b5de6ac1d0821ddf384756502883
   - TRAIN-009 原 delta：
     1c1da899d361ed0e927a16a4c4afcfd7876e6e86
   - TRAIN-009 delta 修复：
     cdd5177f35ddc81c39508f646f7eec7552ab4565

4. 七项决策当前确实全部为 PENDING。

5. 设计树与提交
   644d9d820448b5de6ac1d0821ddf384756502883
   一致，除后续 metadata 修复外没有未审查的设计变化。

任一条件不满足，立即停止，不修改文件，并报告：
TRAIN009_APPROVAL_GATE_BLOCKED

三、审批记录要求

读取 TRAIN-009 现有 decision package、design package、approval form、progress delta 和 Task 19 进度政策。

优先更新现有 TRAIN-009 approval form；如果没有独立 approval form，则在：

docs/spec-v3/task19/design/T19-T03/

创建命名明确的独立审批文件，例如：

TRAIN-009_owner_approval.md

审批记录必须包含：

1. unit_id：TRAIN-009
2. owner_decision_id：TRAIN009-DESIGN-001
3. decision_status：APPROVED
4. approver_role：PROJECT_OWNER
5. 七项决策的完整选择
6. 每项选择对应的批准后合同摘要
7. 决策依赖验证结果
8. 批准范围
9. 明确的非授权事项
10. 记录日期
11. 设计依据提交：
    644d9d820448b5de6ac1d0821ddf384756502883
12. delta 修复依据提交：
    cdd5177f35ddc81c39508f646f7eec7552ab4565
13. 审批记录待 Terminal 0 独立复核
14. business_code_authorized=false
15. ready_for_implementation_authorized=false
16. audited_authorized=false

不得伪造项目所有者姓名、签名、邮件、账号或历史时间。
批准来源只能记录为本轮项目所有者明确授权文本及其 decision ID。

四、逐项写入批准结果

必须精确记录：

T03-DEC-001=A
- 使用现有 training_noise。
- 通过版本化 consumer_kind=domain_randomization 和 purpose label 隔离。
- 不新增 domain_randomization STREAM。
- 不改变 training_noise 既有语义。

T03-DEC-002=B
- 使用兼容 adapter。
- 通过 out-of-band public DomainSummary 包装 Observation v2。
- 不修改 Frozen Observation v2。
- restricted selection proof、raw seed 和隐藏配置不得进入公开 summary。

T03-DEC-003=A
- 训练域仅使用有限、人工批准的完整 GP-008..010 tuple。
- 未知 tuple 返回 DOMAIN_VARIANT_UNKNOWN。
- 失败时不得推进 RNG 或状态。

T03-DEC-004=A
- 在批准 catalog 不超过64个 variants 时，采样 P95≤1ms。
- 超限返回 PERFORMANCE_BUDGET_EXCEEDED。
- reset 不得发布。
- 性能环境和测量方法仍须由后续实施证据绑定。

T03-DEC-005=A
- 不兼容 requested profile 硬拒绝。
- 返回 PROFILE_INCOMPATIBLE。
- RNG 和状态不变。
- 不允许静默 fallback 或“最近 profile”替换。

T03-DEC-006=A
- 临时工件隔离保留24小时。
- 记录 RecoveryRecord 后删除。
- 失败返回 ARTIFACT_RECOVERY_FAILED。
- 不得覆盖已发布版本。

T03-DEC-007=A
- episode variant coordinate 排除 worker ID。
- assignment manifest 只能改变执行 worker。
- 固定 episode 在 1-vs-N 下的 domain/state/observation/mask/reward/done/log hash 必须一致。

五、依赖一致性检查

机械验证：

- DEC-004 依赖 DEC-003=A，目录上限与性能规模相符。
- DEC-005 依赖 DEC-002=B、DEC-003=A，硬拒绝路径不要求 fallback profile 输出。
- DEC-007 依赖 DEC-001=A，worker ID 不得进入 training_noise 的 episode variant coordinate。
- 七项选择不存在共享接口冲突。
- 不要求修改 Frozen Observation v2。
- 不要求向 STREAMS 新增 domain_randomization。
- 不改变 MODEL-001 状态或外部数据门禁。

将检查结果写入审批记录。

六、允许修改范围

只允许修改或新增 TRAIN-009 审批记录所必需的文件，且必须位于：

docs/spec-v3/task19/design/T19-T03/

除非 Task 19 已批准政策明确要求，否则本轮不要修改既有 progress delta。

禁止修改：

- 业务代码
- 测试代码或测试断言
- Locked/Frozen 规格
- Task 17 历史文件
- Task 19 权威 progress tracker
- LATEST.md
- changelog.md
- AUDIT-010 文件
- RULE-015 文件
- B2-A1 文件
- MODEL-001 文件
- 现有设计提交历史
- 已有提交内容

如果现有 approval form 和 decision package 都必须更新才能形成完整审批闭包，可以修改二者，但必须在最终报告逐一说明原因。

七、验证

至少执行：

- Markdown/结构完整性检查
- 七个决策 ID 唯一性检查
- 七项 selected_option 完整性检查
- 选择集合精确等于 A、B、A、A、A、A、A
- PENDING 遗留计数检查
- 依赖一致性检查
- 非授权字段检查
- git diff --check
- git status --short
- 修改路径范围检查

审批记录中不得声称：

- 已实现；
- 测试已通过；
- E4/E5 已生成；
- AC 已 Passed；
- READY_FOR_IMPLEMENTATION；
- AUDITED。

八、提交

验证通过后，使用显式文件路径执行 git add。
禁止使用：

git add .
git add -A

创建一个独立提交，建议提交信息：

docs(task19): approve TRAIN-009 design decisions

不得 amend、merge、cherry-pick、push、创建 tag 或更新其他分支。

九、最终输出

输出：

TRAIN009_OWNER_APPROVAL_COMMIT_CREATED

并报告：

- approval_commit_sha
- parent_sha
- owner_decision_id=TRAIN009-DESIGN-001
- selected_options=A,B,A,A,A,A,A
- changed_paths
- decision_count=7
- pending_decision_count
- dependency_validation
- business_code_authorized=false
- ready_for_implementation_authorized=false
- audited_authorized=false
- worktree_clean
- staged_count
- push_executed=false

下一步必须写明：

由 Terminal 0 对 approval commit 进行只读复审。
在 Terminal 0 复审通过并完成后续明确授权前，不得实施 TRAIN-009。
```

完成后，把 Terminal 3 的输出发给我。下一步将在 **Terminal 0** 生成只读审批复审提示词。

> [!QUESTION] User
> RULE015_PERFORMANCE_OPTIONS_ALIGNED - rule015_performance_fix_commit: 5d925e5fe64d3ab11bc2f3a629e541a4b2ea9c26 - rule015_performance_delta_commit: 2064eaa91dea42e97c33966583858cb350e942eb - option_a_threshold_ms: 2 - option_b_threshold_ms: 5 - option_c_threshold_ms: 10 - warmup_iterations: 100 - measurement_iterations: 1000 - repeat_count: 5 - performance_environment_id: RULE015-PERF-REF-V1-078dc25252299f3c - remaining_200_count: 0 - remaining_2000_count: 0 - dec012_status: PENDING - worktree_clean: true 设计提交仅修改两个 T19-D02 CSV；metadata 提交仅修改 progress delta。既有提交未改写，未修改业务代码或测试，未 push。状态仍为 WAITING_FOR_DESIGN_APPROVAL。 下一步：项目所有者审议 RULE015-DEC-001～012；建议触发语：批准 RULE-015 最终设计决策。

**ChatGPT:**

现在不要直接审批。先按既定门禁，由 Terminal 0 对这两个提交进行一次窄范围只读复审，确认 `R015-R3-F001` 已关闭。

-   运行终端：Terminal 0
    
-   运行目录：`/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer`
    
-   目标分支：当前主协调分支，仅只读
    
-   任务性质：RULE-015 性能选项修复的只读复审；禁止修改、集成或审批
    

进入 Terminal 0：

```
cd "/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer"
codex
```

粘贴以下提示词：

```
执行 RULE-015 最终设计门禁的窄范围只读复审。

运行终端：Terminal 0
运行目录：
/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer

任务性质：
只读审查 Terminal 2 提交的 RULE-015 性能选项对齐修复。
不得修改工作树，不得集成，不得审批决策，不得更新权威状态。

目标提交：

1. 性能选项设计修复：
   5d925e5fe64d3ab11bc2f3a629e541a4b2ea9c26

2. progress delta metadata 修复：
   2064eaa91dea42e97c33966583858cb350e942eb

待关闭 finding：

R015-R3-F001

原缺陷：
RULE015-DEC-012 的 Option C 使用 warmup=200、measurement=2000，
而性能 manifest、AC-12 和 E4 使用 warmup=100、measurement=1000、
repeat=5，导致三个选项并非仅阈值不同。

批准的修复目标：

- Option A：P95 ≤ 2ms
- Option B：P95 ≤ 5ms
- Option C：P95 ≤ 10ms
- 三个选项统一：
  - warmup_iterations=100
  - measurement_iterations=1000
  - repeat_count=5
  - performance_environment_id=
    RULE015-PERF-REF-V1-078dc25252299f3c
  - 使用相同 fixture、计时口径和 P95 计算方法
- DEC-012 仍为 PENDING
- 不得借此次修复改变其他11项决策

一、只读安全门禁

开始前执行：

git status --short
git branch --show-current
git rev-parse 5d925e5fe64d3ab11bc2f3a629e541a4b2ea9c26
git rev-parse 2064eaa91dea42e97c33966583858cb350e942eb

主工作树可能存在用户未提交修改。必须保留这些修改，不得执行：

- git add
- git commit
- git merge
- git cherry-pick
- git checkout
- git switch
- git reset
- git clean
- git stash
- git restore
- git tag
- git push

审查必须基于目标 commit tree，不能把主工作树同名文件当作证据。
可使用 git show、git diff、git ls-tree、git archive 和临时目录。

二、提交身份与祖先检查

确认：

1. 两个目标提交存在。
2. task19-w01-baseline 是其祖先。
3. metadata 提交的祖先链包含设计修复提交；如不是直接 parent，列明中间提交。
4. 原有提交未被重写。
5. 两个提交均来自 RULE-015 Terminal 2 的设计分支历史。
6. 未移动或重建 task19-w01-baseline tag。

三、修改范围检查

验证设计修复提交：

- 只修改两个获准的 T19-D02 CSV；
- 不修改业务代码；
- 不修改测试；
- 不修改 Locked/Frozen；
- 不修改 Task 17；
- 不修改权威 Task 19 tracker；
- 不修改 LATEST.md 或 changelog；
- 不修改其他单元文件。

验证 metadata 提交：

- 只修改 RULE-015 progress delta；
- 不修改设计正文、代码、测试或全局状态。

报告每个提交的准确 changed paths。

四、R015-R3-F001 精确复审

从目标 commit tree 读取：

- RULE015-DEC-012 三个选项；
- performance manifest；
- parameter/interface/acceptance matrices；
- AC-12；
- E4 性能场景；
- E5 中相关引用；
- 最新 progress delta。

逐项验证：

1. Option A 阈值精确为2ms。
2. Option B 阈值精确为5ms。
3. Option C 阈值精确为10ms。
4. A/B/C 的 warmup 均为100。
5. A/B/C 的 measurement 均为1000。
6. A/B/C 的 repeat 均为5。
7. 三者引用同一 performance_environment_id。
8. 三者使用相同 fixture。
9. 三者使用相同 P95 统计定义。
10. 三者除阈值外不存在隐藏的测量参数差异。
11. T19-D02 中不再残留旧值200和2000。
12. AC-12 与 manifest 的测量配置一致。
13. E4 与 manifest 的环境和测量配置一致。
14. E5 仍为14行：
    - semantic=8
    - test=4
    - evidence=2
15. 14项 AC 仍全部被引用。
16. DEC-012 状态仍为 PENDING。
17. DEC-001～011 的选项、状态和语义未发生变化。
18. RULE-015 状态仍为 WAITING_FOR_DESIGN_APPROVAL。

不得只依赖提交报告中的计数，必须从目标 commit tree 独立计算。

五、metadata 检查

验证最新 progress delta：

- JSON 有效；
- unit_id=RULE-015；
- proposed_status=WAITING_FOR_DESIGN_APPROVAL；
- next_required_action=OWNER_DECISION；
- design_commit_sha 或等价字段指向正确的最新设计修复提交；
- 不循环引用 delta 自身；
- DEC-012 仍为 PENDING；
- 不请求 READY_FOR_IMPLEMENTATION；
- 不请求 AUDITED；
- 不声称业务实现或测试已经完成。

六、审查结论规则

仅当全部检查通过时，输出：

RULE015_PERFORMANCE_OPTIONS_REVIEW_PASS
RULE015_DESIGN_READY_FOR_OWNER_DECISION

并明确：

- R015-R3-F001=CLOSED
- open_P0_count=0
- open_P1_count=0
- DEC-001..012 均可进入项目所有者审批
- 此结论不构成所有者审批
- 此结论不构成业务代码实施授权

如任一条件不满足，输出：

RULE015_PERFORMANCE_OPTIONS_REVIEW_FAIL

并列明：

- finding_id
- severity
- commit
- affected_file/row
- evidence
- required_fix
- blocking_scope

不得自行修复。

七、最终报告

报告：

- design_fix_commit
- metadata_commit
- parent/ancestor validation
- changed paths
- A/B/C 阈值
- warmup/measurement/repeat
- performance_environment_id
- remaining old-value count
- AC/E4/E5 一致性
- DEC-012 状态
- RULE-015 当前状态
- 主工作树 staged count
- repository_modified=false
- integration_executed=false
- owner_approval_executed=false

本轮禁止创建任何仓库文件；审查结果只在终端回复中输出。
```

复审通过后，再由你审批 `RULE015-DEC-001～012`。届时我会根据最终设计包给出完整的逐项选择表，而不是只发送一句笼统的“批准”。

> [!QUESTION] User
> RULE015_PERFORMANCE_OPTIONS_REVIEW_PASS RULE015_DESIGN_READY_FOR_OWNER_DECISION - R015-R3-F001=CLOSED - open_P0_count=0 - open_P1_count=0 - DEC-001..012 均可进入项目所有者审批 - 此结论不构成所有者审批或业务代码实施授权 提交验证 item result ━━━━━━━━━━━━━━━━━━━━━━━━━━━ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ design_fix_commit 5d925e5fe64d3ab11bc2f3a629e541a4b2ea9c26 ─────────────────────────── ────────────────────────────────────────────────── design parent 026f81d3c8902297e84bec4d94897ff374d2f145 ─────────────────────────── ────────────────────────────────────────────────── metadata_commit 2064eaa91dea42e97c33966583858cb350e942eb ─────────────────────────── ────────────────────────────────────────────────── metadata parent 5d925e5fe64d3ab11bc2f3a629e541a4b2ea9c26 ─────────────────────────── ────────────────────────────────────────────────── baseline ancestor PASS ─────────────────────────── ────────────────────────────────────────────────── Terminal 2 branch history PASS ─────────────────────────── ────────────────────────────────────────────────── baseline tag target 65e8dcb1679466c9e37d10e5a4299a09774332d9，未移动 ─────────────────────────── ────────────────────────────────────────────────── main staged count 0 设计修复仅修改： docs/spec-v3/task19/design/T19-D02/RULE-015_decision_matrix.csv docs/spec-v3/task19/design/T19-D02/RULE-015_parameter_matrix.csv Metadata 提交仅修改： docs/spec-v3/task19/progress_deltas/RULE-015_progress_delta.json 未触及业务代码、测试、Locked/Frozen、Task 17、其他单元、权威 tracker、LATEST 或 changelog。 性能对齐 option threshold warmup measurement repeats environment ━━━━━━━━ ━━━━━━━━━━━━ ━━━━━━━━ ━━━━━━━━━━━━━ ━━━━━━━━━ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ A P95 ≤ 2ms 100 1000 5 RULE015-PERF-REF-V1-078dc25252299f3c ──────── ──────────── ──────── ───────────── ───────── ────────────────────────────────────── B P95 ≤ 5ms 100 1000 5 RULE015-PERF-REF-V1-078dc25252299f3c ──────── ──────────── ──────── ───────────── ───────── ────────────────────────────────────── C P95 ≤ 10ms 100 1000 5 RULE015-PERF-REF-V1-078dc25252299f3c 三个选项还统一使用： - Fixture SHA-256：e4fcdfdc63edd1eb23996f168a865e601f6c0a7b9f84ccc8c2811ecd5f5c5895 - Timer：time.perf_counter_ns - 单进程、单线程 - 每个 repeat 使用 nearest-rank P95 - 最终取 5 个 repeat P95 的最大值 - 异常和超时按正无穷处理 除阈值外未发现隐藏测量参数差异。T19-D02 中旧 warmup=200、measurement=2000 残留数为 0。 一致性 check result ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ AC count 14 ─────────────────────────────────── ────────────────────────────────────────────────────── AC-12 vs manifest PASS：100/1000/5、相同 fixture/environment/timer/P95 ─────────────────────────────────── ────────────────────────────────────────────────────── E4 count 4 ─────────────────────────────────── ────────────────────────────────────────────────────── NORMAL performance reference PASS：100/1000/5 ─────────────────────────────────── ────────────────────────────────────────────────────── DETERMINISM performance reference PASS：100/1000/5 ─────────────────────────────────── ────────────────────────────────────────────────────── BOUNDARY/HARD_FAILURE NOT_APPLICABLE，无独立性能判断 ─────────────────────────────────── ────────────────────────────────────────────────────── E5 rows 14 ─────────────────────────────────── ────────────────────────────────────────────────────── E5 composition semantic=8、test=4、evidence=2 ─────────────────────────────────── ────────────────────────────────────────────────────── unique E5 delta IDs 14 ─────────────────────────────────── ────────────────────────────────────────────────────── covered AC IDs 14/14 ─────────────────────────────────── ────────────────────────────────────────────────────── DEC-012 PENDING，未选择 ─────────────────────────────────── ────────────────────────────────────────────────────── DEC-001..011 与父提交字节级语义不变 ─────────────────────────────────── ────────────────────────────────────────────────────── RULE-015 status WAITING_FOR_DESIGN_APPROVAL 最新 progress delta： - JSON 有效 - unit_id=RULE-015 - proposed_status=WAITING_FOR_DESIGN_APPROVAL - next_required_action=OWNER_DECISION - 设计引用指向 5d925e5fe64d3ab11bc2f3a629e541a4b2ea9c26 - 未引用 delta 自身 - 12 项决策仍全部未选择 - business_code_authorized=false - 未声称测试或实现完成 - 未请求 READY_FOR_IMPLEMENTATION 或 AUDITED 执行确认 - repository_modified=false - integration_executed=false - owner_approval_executed=false 本轮已完成情况 完成两个目标提交的窄范围只读复审，确认性能选项已统一、原 finding 已关闭且其他设计门禁未回退。未修改、集成或审批任何内容。 下一步完整任务清单 1. 项目所有者按依赖顺序审批 RULE-015 的 DEC-001..012。 2. Terminal 2 将明确选择写入独立 approval commit，不得同时实现代码。 3. Terminal 0 只读复核 approval commit 的完整性和决策依赖。 4. 审批复核通过后，再另行决定设计提交和 progress delta 的集成。 5. 业务实现与 READY_FOR_IMPLEMENTATION 状态仍需单独明确授权。

**ChatGPT:**

RULE-015 已通过最终设计门禁，但现在还不能安全地直接写“全部选 A”。目前缺少 DEC-001～011 的完整选项文本、依赖关系和影响说明。先由 Terminal 0 从已验证的目标提交树提取所有12项决策，再由你逐项批准。

-   运行终端：Terminal 0
    
-   运行目录：`/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer`
    
-   目标分支：当前主协调分支，仅只读
    
-   任务性质：提取 RULE-015 所有者决策表；不审批、不修改、不集成
    

在 Terminal 0 的 Codex 中粘贴：

```
执行 RULE-015 项目所有者决策表提取任务。

运行终端：Terminal 0
运行目录：
/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/chengdu_majiang_AItrainer

任务性质：
只读提取 RULE015-DEC-001～012 的完整决策内容，供项目所有者审批。
不得修改仓库、不得选择选项、不得集成、不得更新状态。

权威设计提交：

5d925e5fe64d3ab11bc2f3a629e541a4b2ea9c26

配套 metadata 提交：

2064eaa91dea42e97c33966583858cb350e942eb

已通过门禁：

RULE015_PERFORMANCE_OPTIONS_REVIEW_PASS
RULE015_DESIGN_READY_FOR_OWNER_DECISION
R015-R3-F001=CLOSED
open_P0_count=0
open_P1_count=0

一、只读要求

开始前执行：

git status --short
git branch --show-current
git rev-parse 5d925e5fe64d3ab11bc2f3a629e541a4b2ea9c26
git rev-parse 2064eaa91dea42e97c33966583858cb350e942eb

必须从目标 commit tree 读取文件，不能使用主工作树中的同名 dirty 文件作为权威证据。

禁止执行：

- git add
- git commit
- git merge
- git cherry-pick
- git checkout
- git switch
- git reset
- git clean
- git stash
- git restore
- git tag
- git push

不得创建仓库内报告文件。

二、提取范围

从以下目标提交树范围读取 RULE-015 的：

- decision package；
- decision matrix；
- approval form；
- design package；
- interface matrix；
- parameter matrix；
- acceptance matrix；
- visibility matrix；
- performance manifest；
- progress delta。

必须提取：

RULE015-DEC-001
RULE015-DEC-002
RULE015-DEC-003
RULE015-DEC-004
RULE015-DEC-005
RULE015-DEC-006
RULE015-DEC-007
RULE015-DEC-008
RULE015-DEC-009
RULE015-DEC-010
RULE015-DEC-011
RULE015-DEC-012

三、每项决策必须输出的字段

对每项决策逐一输出：

1. decision_id
2. question
3. option_a 完整文本
4. option_b 完整文本
5. option_c 完整文本
6. recommended_option
7. recommendation_reason
8. compatibility_impact
9. interface_impact
10. test_impact
11. affected_units
12. blocked_units
13. approval_dependencies
14. required_selected_option
15. alternative_risk
16. breaking_change_risk
17. implementation_complexity
18. audit_risk
19. Terminal 0 的建议，但不得替代项目所有者选择
20. selected_option 必须保持空白
21. owner_comment 必须保持空白

不得概括或省略选项中的：

- 数值阈值；
- 错误码；
- 回滚行为；
- 状态变化；
- 输入输出约束；
- 接口版本；
- 可见性边界；
- 确定性要求；
- 性能配置；
- 依赖条件。

四、决策依赖顺序

生成依赖表：

order,decision_id,depends_on_decision,required_selected_option

检查：

- 是否存在环；
- 哪些决策可以独立审批；
- 哪些决策必须等待前置选项；
- 是否存在某一选择导致接口 breaking change；
- 是否存在某一选择需要其他单元 owner 再批准；
- 是否存在选择会修改 Locked/Frozen；
- 是否存在选择会改变 STATE-010 或其他共享接口。

如果12项设计之间存在冲突，必须明确报告，不能推荐直接审批。

五、DEC-012 特别验证

必须从最终提交确认：

- A=P95≤2ms
- B=P95≤5ms
- C=P95≤10ms
- warmup=100
- measurement=1000
- repeats=5
- environment_id=
  RULE015-PERF-REF-V1-078dc25252299f3c
- 相同 fixture、timer 和 P95 规则
- 三个选项仅阈值不同
- DEC-012=PENDING

六、推荐结果

完成提取后，给出一张推荐选择表：

decision_id,recommended_option,reason,dependency_satisfied,owner_attention

推荐必须以目标提交中的方案及当前共享接口事实为依据。

不得仅因为多数决策推荐 A 就自动建议“全部 A”。
如建议与设计包的 recommended_option 不一致，必须说明理由和证据。

七、可填写审批表

最后输出：

decision_id,selected_option,owner_comment
RULE015-DEC-001,,
RULE015-DEC-002,,
RULE015-DEC-003,,
RULE015-DEC-004,,
RULE015-DEC-005,,
RULE015-DEC-006,,
RULE015-DEC-007,,
RULE015-DEC-008,,
RULE015-DEC-009,,
RULE015-DEC-010,,
RULE015-DEC-011,,
RULE015-DEC-012,,

八、最终状态

必须输出：

RULE015_OWNER_DECISION_TABLE_EXTRACTED

并确认：

- decision_count=12
- missing_option_count
- missing_dependency_count
- dependency_cycle_count
- selected_option_count=0
- DEC-012 configuration
- repository_modified=false
- integration_executed=false
- approval_executed=false
- RULE-015 status=WAITING_FOR_DESIGN_APPROVAL

本任务不构成项目所有者审批，也不构成业务代码实施授权。
```

把提取结果发给我后，我会帮你核对推荐选项，并生成一段可以直接批准的12项决策文本。随后才在 **Terminal 2** 创建独立 approval commit。

> [!QUESTION] User
> MODEL001_BASELINE_REPAIR_R3_READY_FOR_INDEPENDENT_REVIEW - 新提交：badea8e63a76eaf5bdc0c5aa12344f3b4a3c8b6f - Parent：2eeecb98a77e61e19489611c1b051eee8613d2be - Owner decision：MODEL001-UNCERTAINTY-001 - 审批记录：docs/spec-v3/task19/checkpoint/remediation/MODEL001_owner_decision_MODEL001-UNCERTAINTY-001.md:1 修改路径共 9 个： - players/humanlike/belief.py - tests/spec_v3/test_t19_model001_baseline_repair.py - 新 owner decision 记录 - 既有 uncertainty interpretation 记录 - baseline gap report - dependency closure - evidence manifest - repair authorization - test results 禁止语义类别覆盖 GameState、TrainingTruth、model artifact、对手暗手、牌墙及顺序、raw/master seed、future event、restricted label/truth、oracle、私有记忆及既有 禁止类别。 别名规范化规则：Unicode NFKC → casefold() → 移除空格、下划线和连字符 → 与显式规范化别名集合精确匹配。扫描 Mapping 键和值、list/tuple/set、dataclass 公开字段、 对象公开字段、slots 和类型名称；不使用宽泛子字符串匹配。 验证结果： - 专用测试：42 passed；较 R2 增加 23 个 collected cases。 - 既有 MODEL-001、contracts、PlayerView、信息边界：31 passed。 - 确定性：同进程 100 次、fresh-process 5 次均得到 bc94bf0ae97fb089d4bd65d5c787073b11156e9a7c153ff992d83c1eccc72cc8。 - Collection：491。 - 全仓：490 passed、0 failed、1 skipped，42.84s。 - 唯一 skip：既有 macOS Tk 安全跳过，与 MODEL-001 无关。 - git diff --check：通过。 - Manifest：13 行；12 个普通哈希、1 个 self rule；缺失、非法 SHA、哈希/大小不匹配、自引用及解析错误均为 0。 本轮已完成情况 - 两项 R2 finding 已按授权修复并形成独立新提交。 - MODEL-001 仍为 INTEGRATED，未标记 AUDITED。 - 未修改 Locked/Frozen、既有 test_model_001.py、模拟标签合同、Task17、Task19 tracker、LATEST 或 changelog。 - 未声称外部校准或现实有效性。 - worktree_clean=true - staged_count=0 - push_executed=false - 未创建或移动 tag。 下一步完整任务清单 1. 立即下一步：在独立审计终端只读复审 commit badea8e63a76eaf5bdc0c5aa12344f3b4a3c8b6f；建议触发语：独立复审 MODEL-001 R3 remediation commit badea8e。 2. 审计者从目标 commit tree 重算 manifest、递归注入、确定性、collection 和全仓结果。 3. 仅独立审计全部门禁通过后宣告审计 PASS；本终端不自行宣告。 4. MODEL-001 后续仍需独立的外部校准与现实有效性工作，且在完成前保持 INTEGRATED。

**ChatGPT:**

R3 已具备独立复审条件。现在换一个全新的 Codex 会话执行，不能在修复终端自审。

-   运行终端：Terminal 4（新建独立审计终端）
    
-   运行目录：`/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t0-model001-repair`
    
-   目标提交：`badea8e63a76eaf5bdc0c5aa12344f3b4a3c8b6f`
    
-   任务性质：只读独立审计；禁止修改、修复、提交或集成
    

打开新的系统终端窗口：

```
cd "/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t0-model001-repair"
codex
```

粘贴以下提示词：

```
执行 MODEL-001 R3 remediation commit 的独立只读复审。

运行终端：Terminal 4，全新的独立审计 Codex 会话
运行目录：
/Users/moff/Library/CloudStorage/OneDrive-共享的库-Onedrive/chatgpt/wt-task19-t0-model001-repair

目标提交：
badea8e63a76eaf5bdc0c5aa12344f3b4a3c8b6f

预期 parent：
2eeecb98a77e61e19489611c1b051eee8613d2be

任务性质：
独立、只读、从目标 commit tree 重新取证。
不得信任开发终端报告中的计数。
不得读取 dirty 同名文件作为证据。
不得修复、提交、集成、push、创建 tag 或更新状态。

一、历史 finding

必须重新检查并分别判定：

M001-R-F001
- uncertainty 合同错误；
- R2 声称已关闭。

M001-R-F002
- remediation evidence manifest 闭包不完整；
- R2 声称已关闭。

M001-R-F003
- entropy、类别顺序、mixed/other 等测试不完整；
- R2 声称已关闭。

M001-R2-F004
- APPROVED INTERPRETATION 缺少可证明的项目所有者批准依据；
- R3 声称通过 owner decision
  MODEL001-UNCERTAINTY-001 关闭。

M001-R2-F005
- GameState、TrainingTruth、model_artifact 等递归注入未被拒绝；
- R3 声称通过禁止语义规范化和递归扫描关闭。

任何一项未满足均不得输出总体 PASS。

二、只读安全门禁

开始前执行：

git status --short
git branch --show-current
git rev-parse badea8e63a76eaf5bdc0c5aa12344f3b4a3c8b6f
git rev-parse badea8e63a76eaf5bdc0c5aa12344f3b4a3c8b6f^
git merge-base --is-ancestor task19-w01-baseline badea8e63a76eaf5bdc0c5aa12344f3b4a3c8b6f

禁止执行：

- git add
- git commit
- git merge
- git cherry-pick
- git checkout
- git switch
- git reset
- git clean
- git stash
- git restore
- git tag
- git push
- 修改任何仓库文件

使用 git archive 将目标提交导出到全新的 /tmp 临时目录。
所有源码检查、manifest 校验和测试必须在该导出目录中执行。

不得使用 repair worktree 中未提交文件补足证据。

三、提交身份和范围

验证：

1. 目标提交存在。
2. parent 精确为 2eeecb98...。
3. 7b8f27e、2eeecb9、badea8e 均以原 baseline 为祖先。
4. 原提交未被 amend 或重写。
5. task19-w01-baseline annotated tag 未移动。
6. R3 修改路径精确可解释。
7. 生产代码仅修改获准的：
   players/humanlike/belief.py
8. 测试仅修改专用 remediation 测试。
9. 未修改：
   - tests/spec_v3/test_model_001.py
   - Locked/Frozen
   - 模拟标签合同
   - Task 17
   - Task 19 tracker
   - LATEST.md
   - changelog
   - 外部校准状态
10. 未创建模型 artifact 或把模拟数据宣称为现实有效性证据。

列出目标提交相对 parent 的全部 changed paths。

四、所有者批准复审

读取：

docs/spec-v3/task19/checkpoint/remediation/MODEL001_owner_decision_MODEL001-UNCERTAINTY-001.md

以及既有 uncertainty interpretation、repair authorization、gap report、test results 和 manifest。

验证审批记录至少包含：

- owner_decision_id=MODEL001-UNCERTAINTY-001
- status=APPROVED
- approver_role=PROJECT_OWNER
- 明确批准 uncertainty interpretation
- 明确批准禁止字段注入修复
- uncertainty=H(cleared)+H(dominant_suit)+H(shape)
- 类别数2、4、5
- K=40
- 范围[0,ln(40)]
- suit固定顺序：
  wan,tong,tiao,mixed
- shape固定顺序：
  standard,seven_pairs,all_pongs,pure_suit,other
- 不授权外部校准或现实有效性结论
- 不授权升级为 AUDITED
- 可追溯的批准原文或准确引用
- 没有伪造项目所有者姓名、签名、账号、邮件或历史时间

检查旧 uncertainty interpretation 文件是否已明确绑定新的 owner decision，不再仅靠自称 APPROVED 构成审批依据。

如果只能看到开发者自行撰写的“已批准”，却没有项目所有者批准原文、decision ID及范围，则 M001-R2-F004 仍保持 OPEN。

五、信息边界静态检查

检查 players/humanlike/belief.py 的生产实现，确认：

1. 使用确定性名称规范化：
   - Unicode NFKC
   - casefold()
   - 移除空格、下划线、连字符
   - 与显式规范化别名集合精确匹配

2. 不使用容易误判正常公开字段的宽泛 substring 规则。

3. 递归扫描至少覆盖：
   - Mapping 键和值
   - list
   - tuple
   - set/frozenset，如合同支持
   - dataclass 公开字段
   - 对象公开字段
   - slots
   - 类型名称
   - schema/type/kind/class/name 包装结构

4. 防止：
   - 无限递归
   - 自引用对象导致崩溃
   - 恶意 property getter 被不安全执行
   - 不稳定 set 遍历影响错误结果
   - 输入对象被修改
   - 错误信息泄露秘密值

5. 禁止检测发生在概率计算、缓存更新或状态推进之前。

6. 违规稳定返回合同规定的：
   PolicyInputError
   error_code=FORBIDDEN_FEATURE

六、独立递归注入测试

不要只运行开发者测试。审计者必须另外编写临时 oracle/测试脚本，保存于 /tmp，不写入仓库。

至少测试以下禁止语义及变体：

- GameState
- game_state
- game-state
- GAME STATE
- gamestate
- TrainingTruth
- training_truth
- training-truth
- model_artifact
- model-artifact
- ModelArtifact
- opponent concealed hand
- wall order
- raw seed
- master seed
- future event
- restricted label
- restricted truth
- oracle
- private memory
- 既有明确禁止类别

每类至少注入到：

- 顶层 key
- 顶层 value
- 三层以上嵌套 Mapping
- list
- tuple
- set，如入口接受
- type/kind/class/name 包装字段
- dataclass 字段
- slots 对象
- 自定义对象公开字段
- 对象类型名称

验证：

- 全部返回 FORBIDDEN_FEATURE；
- 不返回正常概率结果；
- 不推进任何状态或 RNG；
- 不泄露注入的秘密值；
- 同一输入重复执行结果一致；
- 输入在执行前后不变。

同时构造合法公开输入和合理近似名称，检查没有明显误报。

如果某种容器在正式输入 schema 中明确不被接受，可以返回稳定 schema 错误；但禁止信息不得穿透并产生正常输出。

七、uncertainty 独立数学验证

使用与生产实现独立的 oracle 重算：

H(p) = -Σ p_i ln(p_i)，其中0概率项贡献0。

验证：

- H(cleared)
- H(dominant_suit)
- H(shape)
- uncertainty 为三者之和
- 最小值0
- 合法边界 ln(20)
- 最大值 ln(40)
- 输出有限
- 数值容差明确
- 非法概率、负值、NaN、Inf及未归一分布稳定拒绝
- 概率数组固定长度和固定类别顺序
- mixed/other 映射准确
- 旧字段兼容性未回退

不得以调用生产 entropy 辅助函数作为独立 oracle。

八、确定性与兼容性

验证：

- 同一公开输入运行100次，canonical 输出唯一；
- Mapping 插入顺序变化不影响输出；
- fresh process 至少5次 hash 相同；
- 不依赖网络、外部AI、模型 artifact或训练标签；
- 不使用隐式 RNG；
- 不读取 GameState、TrainingTruth或隐藏信息；
- 既有 MODEL-001 正常调用形式仍兼容；
- MODEL-001 仍为 deterministic fallback；
- MODEL-001 状态仍为 INTEGRATED。

九、Manifest 独立重算

读取目标 commit tree 中的 remediation evidence manifest。

独立验证：

- 总行数；
- 普通哈希行数；
- self-rule 行数；
- 每个普通文件存在；
- SHA-256 为64位小写十六进制；
- 实际 SHA-256 完全匹配；
- byte size 完全匹配；
- 无遗漏的 remediation 工件；
- 无意外路径；
- manifest 自身精确使用：
  SELF_NON_CIRCULAR_EXCLUDED
- manifest 自身的 sha256 和 byte_size 按规则为空；
- 不引用 /tmp、绝对路径、dirty worktree 或未提交文件；
- owner decision 审批记录已纳入 manifest。

十、测试执行

使用 Python 3.12 和项目 pytest 环境，在 git archive 导出目录运行：

1. 专用测试：
   tests/spec_v3/test_t19_model001_baseline_repair.py

2. 既有 MODEL-001：
   tests/spec_v3/test_model_001.py

3. contracts、PlayerView和相关信息边界组合。

4. 全仓 collection：
   python -m pytest -p no:cacheprovider --collect-only -q

5. 全仓回归：
   python -m pytest -p no:cacheprovider -q -rs

6. git diff/check 等价的提交树静态检查。

预期参考值仅用于发现差异，不可直接照抄：

- 专用测试：42 passed
- 相关组合：31 passed
- collection：491
- 全仓：490 passed、0 failed、1个既有macOS Tk安全跳过

若实际计数不同，必须解释差异。
不得使用新增 skip、xfail、删除测试或弱化断言使门禁通过。

十一、结论规则

只有满足以下全部条件才能输出：

MODEL001_BASELINE_REPAIR_R3_INDEPENDENT_REVIEW_PASS

- open P0=0
- open P1=0
- M001-R-F001=CLOSED
- M001-R-F002=CLOSED
- M001-R-F003=CLOSED
- M001-R2-F004=CLOSED
- M001-R2-F005=CLOSED
- 所有者审批可追溯
- 信息边界独立注入测试通过
- uncertainty 独立 oracle 通过
- manifest 闭包通过
- collection和全仓测试通过
- 没有状态越权

同时明确：

- PASS 仅允许进入 Terminal 0 集成评估；
- MODEL-001 仍为 INTEGRATED；
- PASS 不代表外部校准或现实有效性完成；
- 不得标记 AUDITED。

如任一条件失败，输出：

MODEL001_BASELINE_REPAIR_R3_INDEPENDENT_REVIEW_FAIL

每个 finding 必须包含：

- finding_id
- severity
- affected_commit
- affected_file/symbol
- evidence
- required_fix
- blocking_scope

审计终端不得自行修复。

十二、最终报告

列明：

- audited_commit
- parent
- baseline ancestry
- changed paths
- owner decision验证
- 五个历史 finding 状态
- forbidden semantic coverage
- 独立注入测试结果
- uncertainty oracle结果
- deterministic hashes
- manifest统计
- 专用、相关、collection和全仓测试结果
- skipped测试及原因
- open P0/P1数量
- MODEL-001状态
- repository_modified=false
- integration_executed=false
- tag_created=false
- push_executed=false

本轮审计结果仅在终端回复中输出，不创建仓库报告文件。
```

若复审 PASS，下一步是在 **Terminal 0** 评估并集成 `7b8f27e → 2eeecb9 → badea8e`，同时保留原 baseline tag 不动。