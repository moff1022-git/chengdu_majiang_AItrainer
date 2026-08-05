# 1000 局 nonhuman / expert 逐局对照分析

日期：2026-08-03
数据集：`fairness-20260802-fair-004`，固定牌局 `1000` 局
比较对象：同一 `game_id` 的两次运行，仅 s0 预设不同

## 数据完整性

- nonhuman：`1000/1000` 成功，`1000/1000` 完整 trace，`trace_completeness=PASS`。
- expert：`1000/1000` 成功，`1000/1000` 完整 trace，`trace_completeness=PASS`。
- 两组使用同一固定牌局集 SHA-256：`0fd86428e8709c16b5e7e06280335dc82de602e9d4bbb9e48a70379d4f1a1cae`。
- 对照只改变 s0：nonhuman 为 `nonhuman_optimized`；expert 为 `expert_balanced`；s1–s3 均为 `novice_balanced`。

## 总体结果

|指标|nonhuman s0|expert s0|差异|
|---|---:|---:|---:|
|胜局|317|358|-41|
|胜率|31.70%|35.80%|-4.10 pp|
|Top1|294|298|-4|
|总分|-277|282|-559|
|均分|-0.277|0.282|-0.559|
|花猪局|53|40|+13|
|听牌终局|240|231|+9|
|胡牌事件|317|358|-41|
|牌墙耗尽|845|849|-4|

逐局配对结果：nonhuman 相对 expert 得分更高 `183` 局、更低 `216` 局、相同 `601` 局；平均配对差 `-0.559` 分。排名相同的 640 局平均差仅 `-0.098`，排名发生变化的 360 局平均差为 `-1.378`，说明损失主要发生在改变胜负/名次的关键局，而不是统一的座位偏差。

## 决策行为差异

### 同一状态前缀的逐手对齐

对两组 trace 按 `game_id + state_hash_before + seat=0` 对齐。只有状态哈希相同才视为“同一手牌”；第一次动作分叉之后，不再把后续状态误当作同一手牌比较。

- 两组共有 `37197` 个相同 s0 决策状态。
- 其中 `622` 局发生至少一次动作分叉，且所有首处分叉都发生在 `discard` 阶段。
- 首处分叉动作类型：`598` 次为不同弃牌，`24` 次为 nonhuman 选择 `gang_an/gang_jia` 而 expert 选择 `discard`。
- 因此差异不是由换三张或定缺第一步造成，而是从第一轮行牌的局部弃牌/杠选择开始。

逐手分叉后的候选排序显示，nonhuman 经常把较高 `hand_value` 放在第一位；expert 更常用 `defense`/`flexibility` 的平衡来打破候选差距。例如同一局 `000000` 的同一状态：

|候选|hand_value|defense|flexibility|nonhuman 分|expert 分|选择|
|---|---:|---:|---:|---:|---:|---|
|弃 `wan_8`|0.865|0.760|0.329|0.7677|0.7278|nonhuman|
|弃 `wan_1`|0.745|0.880|0.429|0.7537|0.7428|expert|

该差异可由权重直接解释：nonhuman aggressive 风格的 hand-value 权重为 `0.45`、defense 为 `0.25`；expert_balanced 的 hand-value 为 `0.25`、defense 为 `0.25`，speed/flexibility 权重也不同。nonhuman 的高牌值优势足以抵消防守较差，导致选择 `wan_8`；expert 选择更安全的 `wan_1`。

另一类同状态分叉是 nonhuman 选择价值更高但更激进的中张/杠动作。622 局首分叉中计划标签分布为：两边都 `fast_win` 256 局、nonhuman `value_hand` 而 expert `fast_win` 82 局、nonhuman `balanced` 而 expert `fast_win` 64 局、nonhuman `clear_dingque` 而 expert `fast_win` 8 局；这说明差异主要是策略权重改变了计划选择，而非随机噪声。

以下为 s0 完整 trace 中的动作计数：

|动作|nonhuman|expert|变化|
|---|---:|---:|---:|
|discard|15098|14688|+410|
|pong|1520|1422|+98|
|gang_ming|159|142|+17|
|gang_jia|129|119|+10|
|gang_an|69|68|+1|
|hu|317|358|-41|
|pass|38009|37225|+784|

nonhuman 的关键特征是“更积极地碰/杠，但最终胡牌更少”。这与其预设参数一致：`peng_preference=0.70`、`gang_preference=0.85`、`big_hand_preference=0.80`、`defense_awareness=0.45`、`plan_persistence=0.05`，决策权重为 hand value `0.45`、defense `0.25`、speed `0.20`。参数名为 optimized 并不代表已经按牌局收益校准；当前 evaluator 仍是局部候选评分，不是全局最优搜索。

nonhuman 的胡牌减少并伴随花猪增加：花猪从 `40` 增至 `53` 局。花猪局 s0 平均分约为 `-22.9`，是总分恶化的高损失尾部。这个结果优先指向定缺清除、碰/杠后牌型方向和进张保持之间的联动，而不是公平发牌问题。

## 性能问题

- nonhuman 报告总耗时：`4539.744 s`；expert：`2784.428 s`。
- s0 平均响应：nonhuman `315.400 ms`、expert `157.231 ms`；P95：`696.517 ms` 对 `374.650 ms`。
- nonhuman 固定 `14` 候选、搜索深度 `8`、注意力容量 `64`，但动作收益没有同步提升，说明当前搜索成本主要增加了计算时间，未形成可观测的收益优势。

## 已确认的问题

1. `nonhuman_optimized` 不是已证明的最优策略，只是高搜索/高进攻参数组合；报告中的“optimized”容易造成能力预期错误。
2. `peng/gang` 偏好与 `plan_persistence=0.05` 共同作用，可能频繁改变牌型方向，增加碰后低质量牌型和花猪风险；逐手证据中 nonhuman 相对 expert 多 `98` 次 pong、`17` 次明杠、`10` 次加杠。
3. `hand_value=0.45` 的局部评分没有充分惩罚“未清定缺”和“碰后丢失听牌/进张”；应检查 `hand_analyzer` 对这些特征的权重和候选过滤顺序。逐手分叉已显示 nonhuman 选择 hand_value 较高、defense 较低的牌。
4. `hu` 的 `satisficing` 次数 nonhuman 为 205、expert 为 231；需要检查高阈值 `satisfaction_threshold=1.0` 是否导致可胡时等待更高价值，或在候选生成阶段被错误排除。强制胡牌仍应由规则层保证。
5. 搜索深度从 4 提升到 8 造成约 2 倍响应时间，但没有带来更高胜率；应增加剪枝、缓存和终局收益回测，而不是继续提高深度。

## 参数实际生效审计

trace 还暴露出配置合同问题：

- 历史 nonhuman 配置写入 `configured_search_depth=8`，但每个已对齐决策的 `effective_search_depth=4`；`effective_search_depth()` 以 `level=expert` 的普通上限截断了 nonhuman 的 8。任务 1 已修复，后续新运行会按 nonhuman 上限保留 8。
- 历史 nonhuman 配置写入 `satisfaction_threshold=1.0`，trace 实际记录为 `0.95`。任务 1 已修复，后续新运行会按 nonhuman 上限保留 1.0。
- nonhuman 的 `level/style` 在 schema 中被落成 `expert/aggressive`，预设身份只能从外围 preset 字段识别；若运行路径丢失 preset_id，无法仅凭 profile 区分“expert_aggressive”和“nonhuman_optimized”。

因此 nonhuman 当前并不是“14 候选、深度 8、阈值 1.0”的真实策略，而是“14 候选、有效深度 4、阈值 0.95、aggressive 权重”的混合策略。这个实现偏差必须先修复或明确记录，之后才有意义讨论参数调优。

## 建议的下一步验证（不等同于已修复）

1. 对 1000 局 trace 统计每次 s0 discard 前后的：定缺牌数量、向听/进张、候选最高分与第二名差值、是否碰后首次出牌；按花猪局与非花猪局分层。
2. 做固定牌局离线 replay A/B：仅将 `peng_preference/gang_preference` 恢复到 balanced，其他 nonhuman 参数不变，验证花猪和胡牌是否回落/恢复。
3. 做第二个 A/B：保留 nonhuman 搜索深度，但将 `plan_persistence` 提升到 `0.35–0.45`，检验频繁换型是否是主要损失来源。
4. 对 `satisfaction_threshold` 和 `hu` 候选强制性增加规则测试，确认“可胡时不因价值阈值而延迟/放弃”只受规则允许的过胡语义控制。
5. 增加搜索 profiling：缓存同一公开状态的 `analyze_action`，记录每局候选数、剪枝数、搜索节点和决策耗时；验收目标是 nonhuman s0 P95 不超过 expert 的 1.5 倍，同时胜率/总分不下降。
6. 先修复 effective 参数审计：让 nonhuman 的 search-depth/threshold 采用明确的 nonhuman 上限，或在报告中如实输出截断后的有效值；增加配置值与 trace 有效值一致性测试。

## 结论

当前证据支持：nonhuman 输局主要由策略参数与 evaluator 的局部目标错配造成，表现为进攻动作增加、胡牌减少、花猪增加和计算变慢；不支持“固定牌局不公平”或“s0 初始牌明显更差”的结论。下一步应先做上述固定数据 A/B 和 trace 特征分层，再决定是否修改人格参数、候选评分或搜索实现。
