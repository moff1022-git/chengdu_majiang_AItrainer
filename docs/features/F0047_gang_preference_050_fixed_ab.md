# F0047 gang_preference=0.50 固定牌局 A/B

Status: Done

## 背景与动机

F0043 权重修正组的磁盘权威结果为 s0 171 分、358 次胡牌、126 次自摸、41 次花猪；此前状态文档中的 185 分系过期统计。与 Expert 的 282 分相比，净差 111 分，其中 `hu_zimo` 净收益差 -98、`hua_zhu` -32、点炮 -9，杠类部分抵消。逐局首处分叉已有 27 局表现为 Nonhuman 杠而 Expert 弃牌，杠后牌墙路径会改变后续自摸与付款关系。

## 方案

- 固定数据集：`fairness-20260802-fair-004`，1000 局；
- s0 保持 F0043 决策权重：speed .35 / hand_value .25 / defense .25 / flexibility .15；
- 仅把 `gang_preference` 从 .85 调整为 Expert balanced 的 .50；
- 其余 Nonhuman 参数不变：peng .70、big_hand .80、defense .45、plan persistence .05；
- s1-s3 为 `novice_balanced`；
- 不修改正式人格预设，不覆盖旧结果；
- 保存 games、每局 steps 与 audit，以及完整参数快照。

## Out of Scope

- 不同时调整 peng、big hand、defense 或 plan persistence；
- 不修改杠规则或 evaluator 代码；
- 不把离线反事实作为最终结论。

## 验收

- 1000/1000 局成功；games/steps/audit 各 1000；
- 参数快照确认唯一实验变量为 `gang_preference=.50`；
- 比较总分、胡牌、自摸、花猪、点炮、各 score-event 净收益及稳定性；
- 与 F0043 权重组和 Expert 使用同一 game_id 逐局比较。

## 实现与验收结果

1000/1000 成功，games/steps/audit 各 1000；56,024 个 s0 决策参数快照全部确认 `gang_preference=.50`。s0 得分 282，与 Expert 的 1000 个终局结果逐局一致；详见 `docs/status/nonhuman_gang_preference_ab_result.md`。
