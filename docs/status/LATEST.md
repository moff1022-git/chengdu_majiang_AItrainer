# 进度快照

更新时间：`2026-08-05`
当前应用版本：`0.3.1`

## 本轮已完成

- F0066跨种子验证：复用两个预注册独立盲测SHA，共11000局固定牌局配对；Nonhuman相对Expert总分`+1036`、均分`+0.09418`、bootstrap 95% CI `[+0.04991,+0.13755]`。
- 两个数据集均为正向；合并胡牌`+154`、自摸`+74`、花猪`-16`、点炮`-28`，零容差方向护栏全部通过。
- 新增`tools/nonhuman_regression_gate.py`：数据结构错误/门槛失败/通过分别退出2/1/0；CI小样本不依赖本地大数据。
- F0057深化只读审计：完整扫描F0065 Nonhuman trace中571,186次s0决策、1,151,998个候选；shanten、dingque_tiles、ukeire_public_count覆盖率100%，不作因果声称。
- 生成`0.3.1-f0066-rc` clean source/evidence候选、manifest和SHA-256；不修改版本、不覆盖正式tag/Release。
- 本地全仓回归：`529 passed, 1 skipped`。

## 当前功能基线

- F0040–F0059：Nonhuman参数验证、候选审计、人格快照和推荐合同Done。
- F0060–F0063：多进程、CI、固定数据集复盘、SIGINT/trace/RSS门禁Done。
- F0064–F0065：新盲测、四阵容8×1000、主盲测10000局和无人值守闭环Done。
- F0066：跨种子防回退、F0057深化审计和发布候选已实现；远端提交/CI待完成。

## 关键证据

- 结果报告：`docs/status/f0066_cross_seed_and_f0057_result.md`。
- 本地证据：`data/ai_capability/results/f0066_monitor/`（不进Git）。
- source ZIP：`1a99783b1fcdcb3ee8acdaedcc3b910db5d4d8f24543cae087ba3eecc795dfb8`。
- evidence ZIP：`41fd63e1a6c1fce278fb678544312f0b668d1aa17bf0c6066f40d3f8cbc848a3`。

## 风险与限制

- 现有审计为观察关联，不能证明单字段对得分的因果影响。
- `data/`和`releases/`按策略不进Git；跨机需单独传输固定数据及候选归档。
- 发布候选仍使用应用版本0.3.1，仅为F0066验证快照；正式升版需另立发版规格。

## 下一步完整任务清单

1. 提交F0066并推送`integration/v0.3.1-humanlike`与`main`，等待最终CI。建议触发语：自动执行中，无需人工操作。
2. 若要正式发布候选，确定新SemVer并按`docs/VERSIONING.md`建立发版规格。建议触发语：`制定下一版本发布方案`。
3. 若要研究因果影响，预注册单参数随机A/B并生成独立固定数据集。建议触发语：`设计F0057因果A/B`。
