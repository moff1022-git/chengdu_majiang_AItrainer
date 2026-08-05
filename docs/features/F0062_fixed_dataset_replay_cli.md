# F0062固定测试编号与复盘CLI恢复

- 状态：Done
- 日期：2026-08-05

## 目标

把`data/fairness/<test-id>/manifest.json`固定数据集重新接入当前F0060 runner，恢复测试编号选择、固定牌局复现和完整复盘，同时保持高性能game_id模式可选。

## CLI与交互

- `--test-id ID`：选择manifest；交互batch模式列出可用ID，也允许“不使用固定数据集”。
- `--dataset-games N`：必须与`--games`一致且存在于manifest。
- `--replay-fixed-deal`：向engine注入wall/hands/dealer；未开启时仅使用数据集game_id。
- `--replay-trace`：隐含fixed deal，每局写入独立`traces/<game_id>/`，包含steps、audit和终局存档。
- config/report绑定test_id、数据集SHA、artifact、复现方式、executor/workers和trace完整性。

## 恢复合同

- resume读取原config，不允许CLI静默改变数据集、复现方式、executor或worker。
- 以game_id去重并计算pending，不能假设`games.jsonl`恰为连续前缀。
- Ctrl-C停止提交新任务后写checkpoint与部分报告；已完成局不得重复。
- process trace目录按game_id隔离，子进程不得写共享文件。

## 验收

- manifest/hash/局数校验与错误路径测试；
- fixed deal与game_id模式config/report元数据正确；
- process trace每个成功局有steps/audit/终局文件；
- 模拟中断+resume无重复game_id；
- 固定100局serial/process结果一致；全仓回归通过。

## 批准记录

用户“执行任务1-4”明确授权恢复测试编号、固定牌局及复盘CLI，据此Approved。

## 验收记录

- manifest/test_id/dataset SHA/局数/唯一game_id校验已接入。
- batch CLI恢复`--test-id --dataset-games --replay-fixed-deal --replay-trace`，交互模式可选择可用test ID。
- resume读取config绑定并按game_id计算pending，不假设连续前缀。
- process trace smoke 2/2成功，每局生成steps/audit/终局文件。
- runner定向`22 passed`；全仓分片`518 passed, 1 skipped`。
