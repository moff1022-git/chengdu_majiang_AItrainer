# 进度快照

更新时间：`2026-08-05`
当前应用版本：`0.3.1`

## 本轮已完成

- F0063实现真实SIGINT安全恢复：worker中断不再打印traceback，CLI返回130并保留已完成结果；`--resume`无交互恢复原配置。
- 固定100局process完整复盘验收：100/100成功、100个唯一game_id、100/100 trace三件套、完整性门禁PASS。
- 报告JSON/Markdown统一绑定测试编号、数据集SHA、fixed_deal、完整复盘和四座人格参数快照。
- GitHub Actions增加手动Linux RSS smoke，不延长常规push门禁。
- 本轮定向测试：`25 passed`；全仓回归：`522 passed, 1 skipped`。

## 当前功能基线

- F0040–F0059：Nonhuman验证、候选审计、人格快照及推荐合同Done。
- F0060：受控多进程、恢复、完整trace隔离Done。
- F0061：GitHub pytest CI Done。
- F0062：固定测试编号、fixed deal、复盘CLI Done。
- F0063：真实SIGINT、无交互resume、trace完整性门禁已实现；Linux RSS CI待本提交推送后验收。

## 状态与风险

- macOS Codex沙箱内process semaphore需授权；普通终端不受限制。
- `DEFAULT_WORKER_MIB=96`已有macOS证据；Linux精确RSS workflow已实现，结果待远端手动运行。
- data不进Git，固定数据集CLI在无本地manifest时不会显示测试编号选项。

## 下一步完整任务清单

1. 推送F0063实现并手动运行Linux RSS workflow，记录RSS和CI run。依赖：远端Actions。建议触发语：`完成F0063 Linux验收`。
2. 根据Linux RSS结果复核`DEFAULT_WORKER_MIB=96`安全系数；仅在证据要求时调整。依赖：任务1。
3. 将F0063状态置Done并同步DOC_CODE_BASELINE/changelog。依赖：任务1–2。
