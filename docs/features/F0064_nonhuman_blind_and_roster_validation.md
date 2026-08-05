# F0064 Nonhuman 全新盲测、多阵容与向听进张审计

- 状态：Approved
- 日期：2026-08-05

## 目标

在不复用F0054/F0055调参数据的前提下，验证正式`nonhuman_optimized`相对`expert_balanced`的泛化，并检查优势是否依赖s1-s3均为novice。基于F0057新字段做只读解释，不在本功能调参。

## 数据与实验合同

1. 生成全新公平固定数据集`fairness-20260805-blind-001`，1000局，seed/test-id均不得与主集、seed-a、seed-b相同；生成前冻结本规格，运行后不得按结果换seed。
2. 盲测A/B使用同一1000局：A组s0=`nonhuman_optimized`，B组s0=`expert_balanced`；s1-s3均`novice_balanced`。两组保存games及完整steps/audit/终局trace。
3. 多阵容使用同一数据集固定前100局，分别令s1-s3为novice/normal/skilled/expert balanced；每个阵容运行Nonhuman与Expert配对，共8组。保存games；Nonhuman组保存完整trace以供只读分析。
4. 所有比较按game_id配对，报告总分、胡、自摸、花猪、点炮、配对均分差与bootstrap 95% CI；失败局必须为0。
5. F0057只读分析按阵容统计s0 discard候选的shanten、dingque_tiles、ukeire_public_count、首二名分差及终局结果关联；不得把终局、真实未来牌墙或对手暗手作为运行时输入。

## 门禁与解释边界

- 盲测成功门禁：Nonhuman总分高于Expert且配对bootstrap 95% CI下界大于0；若CI跨0，报告为证据不足，不得声称失败或成功。
- 多阵容只作为泛化分层，不以100局单组结果修改正式preset；任何参数变更必须另立规格。
- 不删除或覆盖历史数据；测试输出放入新的独立目录。
- 不声称有限样本证明理论全局最优。

## 验收

- 新数据集可复现、SHA绑定、守恒和公平检查PASS；
- 盲测2×1000及阵容8×100按固定牌局完成，或对未完成项明确记录可恢复路径；
- 生成盲测、多阵容和F0057字段只读报告；
- 更新LATEST、DOC_CODE_BASELINE和changelog。

## 批准记录

用户在完整进展报告后明确要求“执行任务1-4”，即Linux RSS、全新盲测、多阵容和F0057只读分析，据此Approved并授权实现与运行。
