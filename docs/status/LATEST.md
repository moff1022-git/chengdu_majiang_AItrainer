# 进度快照

更新时间：`2026-08-05`
当前应用版本：`0.3.1`

## 本轮已完成

- F0060 Done：能力测试runner增加`serial/thread/process`执行器、spawn进程worker、workers与内存预算限制；Humanlike默认serial。
- 固定100局性能验收：serial 341.241秒，process workers 2为168.367秒，加速2.027x；两组100/100成功、逐局终局100%一致。
- process估算峰值137.078 MiB，低于1024 MiB预算。
- F0061 Done：新增GitHub Actions Python 3.12 pytest工作流，覆盖main、integration/**、codex/**和pull request。
- main远端CI通过：run `30967455466`，HEAD `b5a9b354`，Python 3.12全仓测试步骤成功。
- 本地全仓分片回归：`513 passed, 1 skipped`。
- 两个本地配置旁车继续保留并由gitignore排除；未删除用户运行状态。

## 当前功能基线

- F0040–F0056：Nonhuman联合验证栈Done；正式gang `.50`，权重`.40/.20/.25/.15`。
- F0057–F0059：候选审计、人格快照/雷达、人类推荐F0011退役合同Done。
- F0060：受控多进程批跑Done；process为显式可选，Humanlike默认serial。
- F0061：GitHub pytest CI Done。

## 状态与风险

- macOS Codex沙箱内Python process semaphore查询会被拒绝；授权后的正常终端运行不受此限制。
- 单进程全仓pytest在当前执行环境可能被外部终止；四片独立进程全部通过。
- capability和batch统一使用spawn-safe worker；历史`--threads`仍兼容，新接口推荐`--executor/--workers/--memory-budget-mib`。

## 下一步完整任务清单

1. 扩充F0060 Ctrl-C/process恢复和完整trace多进程集成测试。依赖：可控信号测试夹具。建议触发语：`补F0060恢复与trace测试`。
2. 根据机器内存校准`DEFAULT_WORKER_MIB=96`，形成macOS/CI两套基准。依赖：多进程RSS采样。建议触发语：`校准F0060内存模型`。
3. 将固定数据集CLI选择能力重新整合进当前runner。依赖：先审计F0038历史实现。建议触发语：`恢复测试编号和固定牌局CLI`。
