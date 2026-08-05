# F0053 仅暗杠Expectimax验证结果

日期：2026-08-04
结论：Rejected after multi-dataset validation

## 结果

|数据集|局数|F0053总分|旧`.50`总分|差值|改善/变差/相同|
|---|---:|---:|---:|---:|---:|
|主固定集|1000|293|282|+11|3/5/992|
|seed-a|4000|757|776|-19|8/13/3979|
|seed-b|4000|-455|-453|-2|15/15/3970|
|合并|9000|-|-|-10|26/33/8941|

合并均分差为-0.00111，固定随机种子的10000次配对bootstrap 95% CI约[-0.00867,+0.00667]。主集收益没有在独立数据集复现。

主1000局终局、steps、audit各1000份，零缺失和空文件。seed-a/seed-b各4000局终局完整，分片按固定数据集原顺序合并，game_id 4000个唯一且集合完全匹配。

## 决策

F0053不晋级；业务接入和专项测试回滚，正式 `nonhuman_optimized` 保持不变。证据保留在：

- `data/ai_capability/results/1000_trace_nonhuman_f0053_concealed_gate/`
- `data/ai_capability/results/4000_seed-a_f0053_concealed_gate/`
- `data/ai_capability/results/4000_seed-b_f0053_concealed_gate/`

本轮说明基于少量主集分叉设计杠型门禁仍会过拟合。后续应停止继续细分杠代理，转向能在全体决策上产生更密集信号的价值函数或终局回报学习。
