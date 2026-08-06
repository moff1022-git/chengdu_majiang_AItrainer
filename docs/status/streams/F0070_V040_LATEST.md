# F0070 / v0.4.0 独立线进度

- 更新：2026-08-06
- 状态：主规格Approved；编排契约Review；独立分支/worktree已初始化
- 分支：`feature/f0070-v0.4.0`
- 目标版本：`0.4.0`
- 数据根：`data/experiments/f0070_v040/`
- 命名前缀：`f0070-v040-`
- 基线：v0.3.2 Task 19框架与Nonhuman防回退证据
- 禁止：引入F0069候选参数/数据；合并回`main`

## 下一步

1. 审阅并批准`docs/features/F0070_agent_orchestration_contract.md`；当前仅形成文档，不授权编排器或业务代码修改。
2. 编制WP-B6统一trace契约子规格，再编制WP-B1计划生命周期子规格。
3. 各WP子规格Approved后，由主代理按DAG自动生成规格/实现/验证/审计子代理；平台审批、破坏性/外部动作、最终盲测与新语义仍保留人工门禁。

## 本轮恢复基线

- 已只读核对`tools/task19_agent_runtime.py`：支持原子状态、finding计数、幂等恢复队列和人工门禁识别，不负责实际创建子代理。
- 已只读核对`tools/task19_monitor.py`：只读聚合tracker/runtime/orchestrator，过期心跳投影为STALE，不负责派发或授权。
- 新增Review契约：`docs/features/F0070_agent_orchestration_contract.md`。
- 本轮未修改业务代码、编排工具、数据或实验结果，未提交、未推送。

## 初始化证据

- 分叉提交：`100ddfc2`
- `version.py`：`0.4.0`
- Task 19业务代码：仍为v0.3.2基线，本初始化未改框架
- 数据：未生成；本线后续只写`data/experiments/f0070_v040/`
- 本地目录已创建：`manifests/runs/reports/traces/artifacts/tmp`；`STREAM_ROOT.md`声明本线命名和禁止交叉写入。
- 工作区已迁移至Finder可见路径：`worktrees/f0070-v0.4.0/`；Git HEAD和本地数据不变。
