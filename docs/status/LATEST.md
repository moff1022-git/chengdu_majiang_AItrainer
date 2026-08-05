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
- F0064已完成：全新1000局盲测两组均1000/1000且trace完整；Nonhuman +29但95% CI跨0。四种对手阵容8组固定100局均成功；F0057字段只读统计完成。

## 当前功能基线

- F0040–F0059：Nonhuman验证、候选审计、人格快照及推荐合同Done。
- F0060：受控多进程、恢复、完整trace隔离Done。
- F0061：GitHub pytest CI Done。
- F0062：固定测试编号、fixed deal、复盘CLI Done。
- F0063：真实SIGINT、无交互resume、trace完整性门禁和Linux RSS已验收（35,880 KiB）。
- F0064：盲测、多阵容与向听/进张审计已完成；盲测CI跨0，不晋级参数。
- F0065已启动主代理监控：新数据集`fairness-20260805-blind-002` 10000局，SHA `5d3dfc305e3df07d2b10b8c04682a4de456203f9d96eac73003c25e31354e50c`；Nonhuman完整trace/Expert长测后台运行，状态见`data/ai_capability/results/f0065_monitor/status.json`。
- F0065主盲测完成：Nonhuman 956、Expert -51，差值+1007，95% CI `[+0.0561,+0.1448]`；两组10000/10000成功，Nonhuman trace完整。
- F0065四阵容8组完成：novice +73、normal +126、skilled +123、expert +124；均1000/1000成功；全仓回归`525 passed, 1 skipped`。

## 状态与风险

- macOS Codex沙箱内process semaphore需授权；普通终端不受限制。
- `DEFAULT_WORKER_MIB=96`已有macOS证据；Linux精确RSS workflow已实现，结果待远端手动运行。
- data不进Git；固定数据集CLI即使在无本地manifest的干净检出中也会显示规范测试组编号（实际运行仍需先提供数据集工件）。
- CI run `31018377514` 在 `2c54363f` 上发现并修复测试组索引回归；修复提交后的最终CI待完成。

## 下一步完整任务清单

1. 新盲测数据集扩大配对样本。建议触发语：`扩大Nonhuman盲测`。
2. 多阵容扩大至每阵容1000局。建议触发语：`扩大多阵容验证`。
3. 深化候选分差与shanten/ukeire关联审计。建议触发语：`深化F0057审计`。
