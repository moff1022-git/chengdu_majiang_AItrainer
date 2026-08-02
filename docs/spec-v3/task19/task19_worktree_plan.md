# Task 19 worktree 与终端计划

禁止在当前 dirty 主工作树直接创建并行开发分支。当前 tracked modifications 与 untracked files 见本次 `git status --short`；其中 docs/spec-v3、B1-A/B1-B/B2-A1 和 Task19 文件属于待固化成果，其他产品/UI/训练改动可能是用户或其他任务成果，不能自动归类或暂存。

## 检查点方案

1. 用户确认已审计成果和 Task19 计划的精确文件清单。
2. Terminal 0 只读复核 SHA-256、测试基线和状态矩阵。
3. 经用户单独授权后精确 `git add -- <approved paths>`，创建 checkpoint commit 与 `task19-baseline-*` tag。
4. 从该 clean commit 创建最多三个开发 worktree；本任务不执行任何 Git 写操作。

## 当前 dirty 清单分类

- 已审计/已批准但尚未进入当前 commit：`docs/spec-v3/**`、`engine/match.py`、`engine/rng_v2.py`、`engine/round_state_machine.py`、`tests/spec_v3/**`、`tests/contracts/**` 及 B1-A/B1-B/B2-A1 相关生成工具。这些需要按证据 manifest 再确认后进入检查点候选。
- Task19 待提交计划成果：`docs/spec-v3/task19/**` 与 `tools/generate_task19_plan.py`。
- 已跟踪且无法仅凭 Task19 安全归属：`engine/deal.py`、`engine/orchestrator.py`、`engine/legal.py`、`engine/score.py`、PlayerView/players/training 相关修改、`docs/features/**`、`tests/test_subprocess_compat.py`。必须由用户确认来源，不能自动纳入或排除。
- 未跟踪且可能属于其他任务/环境：`.venv-macos/`、`data/`、F0031/F0032/F0033、MODEL-001 与其他工具/测试目录。不得自动 add、stash、clean 或删除。

因此 `423326ec...` 只能作为取证 commit，不能直接作为并行开发内容基线；`baseline_commit/tag` 保持 PENDING。

| wave | baseline_commit | baseline_tag | worktree_directory | branch_name | batch | terminal | completion / integration |
|---|---|---|---|---|---|---|---|
| W01 | PENDING_CHECKPOINT | PENDING | ../wt-task19-t1-w01 | task19/w01-b2a1 | T19-B2A1 | Terminal 1 | 单分支内部顺序三单元；定向->契约->E4/E5->delta |
| W01 | PENDING_CHECKPOINT | PENDING | ../wt-task19-t2-w01 | task19/w01-design-deterministic | RULE-015 design only | Terminal 2 | 仅设计包，无业务代码 |
| W01 | PENDING_CHECKPOINT | PENDING | ../wt-task19-t3-w01 | task19/w01-design-audit-training | AUDIT-010/TRAIN-009 design only | Terminal 3 | 仅设计包，无业务代码 |

每个后续 wave 从上一集成检查点创建，分支不得修改权威进度、changelog、全局审计矩阵或 Task17 文件。commit message 使用 `task19(<batch>): <deliverable>`；cherry-pick 顺序严格取 `task19_parallel_wave_plan.csv.integration_order`。
