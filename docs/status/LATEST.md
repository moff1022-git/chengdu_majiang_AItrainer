# 进度快照

更新时间：`2026-08-05`
当前应用版本：`0.3.1`

## 本轮已完成

- F0060恢复/trace增强：process改为有界任务调度，stop后不再提交新任务；resume按game_id去重。
- process完整trace固定2局smoke：2/2成功，每局独立目录均有steps、audit和终局JSON。
- 完成worker内存校准：`DEFAULT_WORKER_MIB=96`相对实测51.25 MiB保留1.87倍安全系数，维持不变。
- F0062 Done：恢复测试编号、数据集规模、fixed deal与完整复盘CLI；config/report绑定数据集SHA与复现方式。
- 最新先前文档提交CI已通过：main run `30967645984`，HEAD `95794f09`。
- 本轮全仓分片回归：`518 passed, 1 skipped`。

## 当前功能基线

- F0040–F0059：Nonhuman验证、候选审计、人格快照及推荐合同Done。
- F0060：受控多进程、恢复、完整trace隔离Done。
- F0061：GitHub pytest CI Done。
- F0062：固定测试编号、fixed deal、复盘CLI Done。

## 状态与风险

- macOS Codex沙箱内process semaphore需授权；普通终端不受限制。
- `DEFAULT_WORKER_MIB=96`已有macOS证据；Linux精确RSS尚未采样，继续采用保守值。
- data不进Git，固定数据集CLI在无本地manifest时不会显示测试编号选项。

## 下一步完整任务清单

1. 为process模式增加真实SIGINT子进程集成测试，而非仅stop回调单元测试。依赖：可控慢worker夹具。建议触发语：`补真实SIGINT集成测试`。
2. 在Linux runner增加小规模RSS采样，校准CI worker模型。依赖：不延长常规pytest门禁。建议触发语：`增加Linux内存采样任务`。
3. 为fixed dataset增加报告trace完整性计数和缺失门禁。依赖：F0062现有trace目录合同。建议触发语：`增加trace完整性报告门禁`。
