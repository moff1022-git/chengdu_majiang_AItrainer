# 进度快照

更新时间：`2026-08-05`
当前应用版本：`0.3.1`

## 本轮已完成

- F0059 Done：人类推荐遗留`use_f0011=True`不能重新启用F0011；三种当前推荐算法合同保持有效。
- 全仓按四片回归：`512 passed, 1 skipped`。
- Humanlike并发审计：12局workers 1/2/5耗时均约42秒，峰值RSS 56.64/77.50/102.91 MiB；线程无吞吐收益，正式批跑建议单线程。
- 已按范围形成5个提交：`a634142`、`ea05aa9`、`d1201ff`、`3d901da`、`e29db24`；运行数据和临时配置未纳入。

- F0057 Done：候选trace补齐`shanten`、`dingque_tiles`、`ukeire_faces`和`ukeire_public_count`，不改变候选评分与动作。
- F0058 Done：能力测试报告增加逐座正式人格参数快照；设置窗口雷达以显式顺序显示12项风格参数与7项水平参数，并锁定13种preset。
- 正式`nonhuman_optimized`入口复核固定数据集`fairness-20260802-fair-004/100`：`100/100`成功，s0总分`97`、胡`34`，与F0055一致。结果保存在`data/ai_capability/results/100_f0058_official_preset_smoke/`。
- 测试：F0057定向`26 passed`；F0058定向`38 passed`；Humanlike扩大回归`121 passed`。
- 全仓首失败复核：`300 passed`后，`tests/test_f0011_integrated.py::test_pipeline_f0011_flag`失败。该测试仍要求已被用户取消的人类推荐`F0011`标志为True，与当前“humanlike_v2/rule_ai/rule_ai_plus”推荐口径冲突，不属于F0057/F0058回归。
- 已审计F0040–F0058工作树范围；未提交、未推送、未清理其他改动。

## 权威文档

- `docs/features/F0056_promote_nonhuman_validated_stack.md`
- `docs/features/F0057_candidate_shanten_ukeire_audit.md`
- `docs/features/F0058_preset_ui_report_snapshot.md`
- `docs/status/nonhuman_f0055_result.md`

## 状态、偏差与风险

- 正式Nonhuman值：gang `.50`，speed/value/defense/flexibility `.40/.20/.25/.15`；正式入口与实验结果一致。
- 多局并发10/5的正式复核进程被系统无Python异常终止；串行100局稳定完成，说明功能正确但当前环境存在Humanlike并发内存峰值风险。
- `git diff --check`发现README、macOS打包文档/Spec的历史尾随空格；与本轮Humanlike功能无关，未擅自改动。
- 工作树混有Humanlike、打包、README、公平生成器及大数据产物，禁止整体提交。

## 提交范围建议

1. F0040–F0056：相关Approved/Done规格、Humanlike行为代码、配置与对应测试/小型统计文档。
2. F0057：`hand_analyzer.py`、`evaluator.py`、审计字段测试与F0057规格。
3. F0058：`settings_window.py`、`ai_capability_test.py`、报告/雷达测试与F0058规格。
4. README与macOS打包脚本/Spec/F0021文档独立提交，并先修复其`diff --check`尾随空格。
5. `fair_deal_generator.py`及`tests/tools/`独立提交；`.bak`、recommendation临时配置和大规模data/trace不纳入Git。

## 下一步完整任务清单

1. 将当前状态元数据提交并推送分支；产出远端可恢复基线。依赖：5个功能提交已完成。建议触发语：`推送当前分支`。
2. 另立Humanlike多进程批跑规格，按可用内存计算worker上限；产出Approved设计，不直接改runner。依赖：并发审计结论。建议触发语：`设计Humanlike多进程批跑方案`。
3. 在远端CI复跑全仓测试；产出独立环境验证。依赖：分支推送成功。建议触发语：`检查远端CI`。
