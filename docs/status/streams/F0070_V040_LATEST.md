# F0070 / v0.4.0 独立线进度

- 更新：2026-08-06
- 状态：Approved，独立分支/worktree已初始化
- 分支：`feature/f0070-v0.4.0`
- 目标版本：`0.4.0`
- 数据根：`data/experiments/f0070_v040/`
- 命名前缀：`f0070-v040-`
- 基线：v0.3.2 Task 19框架与Nonhuman防回退证据
- 禁止：引入F0069候选参数/数据；合并回`main`

## 下一步

1. 先编制WP-B6统一trace契约子规格，再编制WP-B1计划生命周期子规格。
2. 各WP子规格Approved后才实现对应业务代码。

## 初始化证据

- 分叉提交：`100ddfc2`
- `version.py`：`0.4.0`
- Task 19业务代码：仍为v0.3.2基线，本初始化未改框架
- 数据：未生成；本线后续只写`data/experiments/f0070_v040/`
- 本地目录已创建：`manifests/runs/reports/traces/artifacts/tmp`；`STREAM_ROOT.md`声明本线命名和禁止交叉写入。
- 工作区已迁移至Finder可见路径：`worktrees/f0070-v0.4.0/`；Git HEAD和本地数据不变。
