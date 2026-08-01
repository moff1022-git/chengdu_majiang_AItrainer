# MODEL-001模拟范围训练与校准报告

日期：2026-07-30  
模型：`MODEL001-SIM-NB 1.0.0`  
结论：**SIMULATION_METRICS_RECORDED_NOT_PASSED_WITHOUT_APPROVED_THRESHOLDS**

## 实现

训练器只提取PlayerView公开的阶段、定缺、手牌张数、状态、turn bucket、风格、公开弃牌和副露计数，使用Laplace平滑的categorical Naive Bayes分别输出cleared、dominant和shape归一化概率。artifact不含restricted truth字段。

## Test指标（1551条/2局）

| 目标 | Accuracy | Brier | Log loss | ECE-10 |
|---|---:|---:|---:|---:|
| cleared | 0.866538 | 0.188193 | 0.330982 | 0.093272 |
| dominant | 0.460993 | 0.872141 | 2.337489 | 0.361693 |
| shape | 0.912959 | 0.157969 | 0.495658 | 0.120667 |

shape test truth全部为other，0.912959准确率不得解释为五类shape性能。

## 门禁判断

- 模拟训练、artifact生成、概率归一化、确定性重训和指标计算已完成。
- Locked测试规范没有冻结ECE/Brier/log-loss通过阈值，因此校准状态保持`NOT_EVALUATED_NO_APPROVED_THRESHOLD`。
- `external_validity=NOT_EVALUATED`；本报告不改变MODEL-001审计状态。
- artifact SHA-256：`6f674624779865d6108de5eafe0166e2d02fcec66214961dc3b6ee43e0cc6617`。

