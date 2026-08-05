# F0065 Nonhuman 长时无人值守验证与主代理监控

- 状态：Done
- 日期：2026-08-05

## 目标

执行既定任务1–9，并以最低终端/token输出完成长时、可恢复、可审计的10000局盲测和多阵容验证。主代理负责启动、阶段轮询、异常分类、自动resume和最终文档/Git闭环。

## 执行合同

- CLI增加`--yes`免交互确认和`--list-test-groups`数据集索引；默认交互行为不变。
- 固定使用预注册的新test_id/seed，运行后不得按结果换seed。
- 每个运行目录保存config、checkpoint、games、summary/report；完整trace仅用于Nonhuman主盲测，其他组默认终局记录以控制耗时与磁盘。
- 监控只读取checkpoint、games行数、失败原因和进程退出码；不打印逐局进度。
- 可恢复环境/中断错误自动`--resume`；配置、SHA、规则、trace门禁错误停止对应阶段并报告，禁止静默改变口径。
- 状态落盘到`data/ai_capability/results/f0065_monitor/status.json`；data不进入Git。

## 阶段

1. 索引CLI与定向测试；2. 10000局数据生成/复现/公平预检；3. Nonhuman/Expert盲测；4. 配对统计；5. 四阵容A/B；6. 阵容汇总；7. F0057只读聚合；8. 文档闭环；9. 全仓回归、提交、推送、CI。

## 批准记录

用户要求完善任务1–9并由主代理监控、报告进度、处理异常、确保自动完成，据此Approved。

## 验收结果

- 新盲测10000局：Nonhuman 956、Expert -51，差值+1007，配对均分+0.1007，95% CI `[+0.0561,+0.1448]`；两组10000/10000成功，Nonhuman trace完整10000/10000。
- 四阵容各1000局配对：novice +73、normal +126、skilled +123、expert +124；八组均1000/1000成功。
- F0057主盲测只读聚合：4,182,443候选记录，shanten均值2.0491、dingque_tiles均值0.4547、ukeire_public_count均值0.3696，三个字段覆盖率100%。
- 本地全仓回归：525 passed、1 skipped；最终修复提交`3aacf911`已推送integration与main；远程CI run `31019704124`成功（其前置修复验证见`31019337103`）。
