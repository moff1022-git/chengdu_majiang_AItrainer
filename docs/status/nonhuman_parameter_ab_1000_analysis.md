# Nonhuman 参数 A/B（固定牌局 1000 局）

## 数据与复盘门禁

两组均使用 `fairness-20260802-fair-004` 的同一 1000 个 game_id，复现模式为 `fixed_deal`。每组均生成 1000/1000 `games.jsonl`、1000/1000 `*.steps.jsonl` 与 1000/1000 `*.audit.jsonl`，旧结果未删除。

## 结果（s0）

|组别|改动|总分|胡牌局|花猪局|
|---|---|---:|---:|---:|
|原始 nonhuman|基线|−277|317|53|
|A claims/gang|`peng_preference=0.50`, `gang_preference=0.50`|−237|318|53|
|B persistence|保持 claims/gang=0.70/0.85，`plan_persistence=0.40`|−277|317|53|

对照席位在三组中保持 novice_balanced。第一次错误注入目录 `1000_trace_nonhuman_balanced_claims` 使用了 preset_id 覆盖临时配置，已标记为无效证据且保留。

## 结论

A 组相对基线增加 40 分、胡牌局 +1，但花猪数不变，说明碰/杠偏好对本数据集的主要影响是结算得分与少量牌局路径，不是花猪根因。B 组在 0.40 persistence 下与原始 nonhuman 汇总指标完全相同（分数、胡牌、花猪及各席胡牌数均一致）；因此“频繁换型”在该固定牌局和当前实现中未显示为主要损失来源。需要进一步按相同 game_id 的逐手 trace 对齐，检查 persistence 是否实际改变候选选择；若首处分叉数为零，则该参数未进入决策路径。

## 逐局逐手对齐与规则门禁

按相同 `game_id` 对齐 s0 决策：claims/gang 组在 28 局出现 357 次动作差异，主要为 `discard↔pass`（271 次），另有 gang 与弃牌、碰、胡的少量分叉；花猪数仍为 53。`plan_persistence=0.40` 组与原始 nonhuman 逐手完全一致（0 局、0 次分叉），因此当前实现和牌局下该参数没有形成有效决策分叉。

已增加 F0040 胡牌强制性门禁测试：低满意阈值和候选容量限制不会延迟或丢弃合法 HU；HU 是否可放弃仅由 GP-009 过胡许可决定。相关测试 `20 passed`。

## 产物

- `data/ai_capability/results/1000_trace_nonhuman_balanced_claims_v2/`
- `data/ai_capability/results/1000_trace_nonhuman_plan_persistence_040/`

## F0041 审计重跑

当前代码已重新完成两组 1000 局固定牌局：`1000_trace_audit_baseline` 与 `1000_trace_audit_persistence040`。两组均 1000/1000 games、steps、audit，新增审计记录包含 `plan_state` 与 `hu_rule` 字段；旧结果目录保留不覆盖。
