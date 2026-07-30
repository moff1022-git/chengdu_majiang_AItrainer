# 任务15复修后批量开发准入审计

| 字段 | 结果 |
|---|---|
| 日期 | 2026-07-30（Asia/Shanghai） |
| 规范基线 | SPEC-V3-3.0.3 |
| 锁定集 | 39/39，set hash `aceb6ae980dd8a8cc98922d88f317c7e302b20b8098775791656e833ac813fa5` |
| 审计范围 | 原10个试点单元；未扩展其余86单元 |
| 准入结论 | **PASS** |

## 1. 对原任务清单1—5的修复

1. 新增锁定公共合同`pilot_unit_contracts_3_0_3.md`，逐单元定义字段名、类型、单位、来源、范围、默认/null、输出精度、88个分支ID及解释字段。
2. 重写证据生成器：从两份规则字节、冻结EngineConfig和9个代码文件计算真实SHA-256；使用真实UTC、dirty标记、game/event/seed引用；禁用`locked/pilot/unknown/TODO`占位值。
3. 补齐并接入原10单元：RULE查询门面、建墙守恒、PlayerView hash、注意力规范排序与解释、公开信息模型fallback、计分守恒/幂等账本、635 codec及审计链均有生产调用边。
4. 建立88分支ID覆盖矩阵；87个有直接自动化证据，98.9%≥90%。环境仍无`pytest-cov`，故该指标是规格关键分支覆盖，不是源码插桩覆盖。
5. 用固定`game_id=task15-fixed-seed-game`、`base_seed=45`运行两局：各43决策，最终状态hash与全record hash序列完全一致。

## 2. 准入指标

| 指标 | 实际 | 门槛 | 结果 |
|---|---:|---:|---|
| 试点实现完成率 | 100% | 100% | Pass |
| 测试通过率 | 100%（13/13；全量370 passed/1 skipped） | 100% | Pass |
| 关键分支覆盖率 | 98.9%（87/88） | ≥90% | Pass |
| 规则追溯覆盖率 | 100% | 100% | Pass |
| 输入输出定义完整率 | 100% | 100% | Pass |
| 公式可执行率 | 100% | 100% | Pass |
| 固定种子决策轨迹复现率 | 100% | 100% | Pass |
| 阻断级矛盾 | 0 | 0 | Pass |
| 未关闭High | 0 | 0 | Pass |

所有准入条件同时满足，因此项目具备按同一模板开展批量开发的条件。该PASS只授权进入下一阶段，不代表剩余86单元已经实现或通过审计。

## 3. 最终状态

| 状态 | 单元 |
|---|---|
| AUDITED | RULE-003、RULE-016、ALGO-001、ALGO-010、HEUR-019、STATE-005、SCORE-001、TRAIN-003、AUDIT-003 |
| INTEGRATED | MODEL-001 |

MODEL-001的规则fallback已完整接入并满足本批量开发准入；训练模型替换仍必须在后续模型阶段用冻结10000样本manifest验证ECE/Brier后才能标记AUDITED。该项是已分阶段的Low caveat，不是开放High或批量开发阻断项。

## 4. 证据

- 定向JUnit：`docs/spec-v3/reports/task15_targeted_junit.xml`，13 passed。
- 全量JUnit：`docs/spec-v3/reports/task15_full_junit.xml`，370 passed/1 skipped。
- 分支矩阵：`task15_branch_coverage.csv`，87/88。
- 单元运行证据：`task15_evidence/pilot_runtime.jsonl`，10×1000 warm samples，真实hash/UTC。
- 双跑比较：`task15_evidence/fixed_seed_replay_comparison.json`，`reproducible=true`。
- 两条完整链：`task15_evidence/run_a/`、`run_b/`；43 decisions；state hash `6ac439ec...ac8c`；record hash序列相同。

## 5. 代码与行为复核

- 未发现新增占位、`NotImplemented`或固定成功返回。
- RULE/ALGO/STATE/SCORE/TRAIN/AUDIT均保持确定性；HEUR输出候选来源、分量、修正、排名、选择和停止原因。
- MODEL递归拒绝`hand/physical_hand/oracle_hands/wall_order/label_zone/truth`，只由PlayerView公开字段形成fallback概率与解释。
- SCORE每笔支付接收保持ΣΔ=0；同event同payload幂等，不同payload返回稳定冲突错误。
- 两份原始规则文档未修改；用户其他未提交修改未清理或覆盖。

## 6. 结论边界与后续控制

允许开始批量开发，但每批仍必须执行Docs-First、逐字段合同、≥90%关键分支、真实运行hash、隐藏信息投毒和固定seed回放门禁。若后续单元没有这些证据，不得继承本次PASS或AUDITED状态。
