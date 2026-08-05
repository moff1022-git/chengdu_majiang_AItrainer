# F0060固定100局性能验收

- 日期：2026-08-05
- 数据集：`fairness-20260802-fair-004/100`
- 玩家：s0 `nonhuman_optimized`；s1–s3 `novice_balanced`

|执行方式|成功/失败|耗时|RSS|
|---|---:|---:|---:|
|serial / 1|100/0|341.241s|self 61.344 MiB|
|process / 2|100/0|168.367s|self 34.578 MiB；children max 51.250 MiB|

- 加速比：`2.027x`。
- 逐局终局深比较：`100/100`完全一致，比较scores、rankings、hu_sequence、finished_reason、wall_remaining、settle_tags和score_events。
- process保守估算总峰值：`34.578 + 2 × 51.250 = 137.078 MiB`，低于1024 MiB预算。
- 结论：process workers 2通过吞吐、一致性、成功率和内存门禁；Humanlike默认仍保持serial，process为显式可选。
- 原始验收JSON位于本地`data/ai_capability/results/f0060_acceptance/`，不入Git。
