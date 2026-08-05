# 进度快照

更新时间：`2026-08-05`
当前应用版本：`0.3.1`

## 本轮已完成

- 完成Nonhuman相较Expert差距定位全链路复盘报告：区分旧基线`-559`、规则排障、被否决方向、Expert上限恢复及9000局跨数据集超越证据。
- 当前目标口径更新：正式Nonhuman已通过项目内Expert跨数据集晋级门禁；下一阶段转为全新盲测、多阵容泛化和持续防回退，不宣称理论全局最优。
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

1. 修复F0063 Linux RSS workflow的仓库模块路径，重新触发并记录RSS；当前run `30973389287`因`ModuleNotFoundError: engine`失败。建议触发语：`继续F0063 Linux验收`。
2. 在全新未参与调参的数据集做正式Nonhuman vs Expert盲测。依赖：F0063闭环。建议触发语：`执行Nonhuman全新盲测`。
3. 执行novice/normal/skilled/expert混合阵容分层验证。依赖：任务2报告合同。建议触发语：`执行Nonhuman多阵容验证`。
4. 只读分析F0057新增shanten/ukeire审计字段，定位剩余可泛化差距。依赖：任务2新trace。建议触发语：`分析Nonhuman新审计字段`。
