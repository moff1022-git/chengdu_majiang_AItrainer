# F0010 对手牌预测准确率分析

- ticks: **5600**  |  opponent-samples: **16800**  |  games: **50**
- mean best-of-TopK F1: **0.5113**
- mean Top-1 F1: **0.436**
- mean random-baseline F1: **0.369**
- mean lift (best − baseline): **0.1423**
- exact_set rate: **0.0**
- main-suit match rate: **0.5302**

## best_rank 分布（最佳匹配落在第几名）

- rank 1: 7774
- rank 2: 2824
- rank 3: 2216
- rank 4: 1856
- rank 5: 2130

## 按弃牌信息量分桶（mean best F1）

- deep(>12 disc): n=1932  best_f1=0.5943  top1=0.5155  lift=0.1826
- early(≤2 disc): n=2868  best_f1=0.467  top1=0.3688  lift=0.1116
- late(7-12 disc): n=7200  best_f1=0.5182  top1=0.4636  lift=0.1456
- mid(3-6 disc): n=4800  best_f1=0.494  top1=0.4028  lift=0.1395

## 连续性 on/off

- cold_start: n=300  best_f1=0.4451  lift=0.0895
- with_continuity: n=16500  best_f1=0.5125  lift=0.1433

## 向听诊断（S0）

- Top1 向听 MAE: **2.1088**
- 有符号误差 mean(pred−true): **-1.5383** （负=预测偏近听）
- 假近听率 (pred ≤ true−2): **0.3756**
- best-F1 假设的向听 MAE: **2.0083**
- deep(>12 disc): n=1932  MAE=1.5083
- early(≤2 disc): n=2868  MAE=4.9805
- late(7-12 disc): n=7200  MAE=1.0431
- mid(3-6 disc): n=4800  MAE=2.2333

## 准确率偏低的主要原因

1. 信息量分桶显示后期好于早期（0.467 → 0.5182），早期冷启动贡献了平均偏低。
2. 预测向听与真实向听平均绝对误差≈2.1088：听牌方向约束未对齐真牌结构。
3. exact_set 命中率≈0.00%（预期极低）：不宜用「整手全中」衡量算法；tile F1 / 花色 / 向听更合适。

## 改进建议

1. 开局几巡可只显示花色/向听粗粒度，完整 Top-K 延后。
2. 用真实向听分布做软标签；副露后手牌张数/搭子结构约束加严。
3. 文档与 UI 准确度说明改为「牌张重合度」，避免误解为猜中整副牌。

## Discard accuracy（文献式 top-1 / top-3）

- samples: **2800**  |  games: **50**
- **top1 accuracy: 0.44**  (literature band often **0.68–0.88** on human logs)
- top3 accuracy: **0.7086**
- mean MRR: **0.6064**  |  mean rank of actual: **3.0318**
- random baseline (mean 1/n_legal): **0.4359**  | lift: **0.0041**
- expert min-shanten consistency (model top1 == min-shanten): **0.7268**
- mean n_legal unique tiles: **5.215**

### Rank of actual discard (lower better)

- min=1.0  p10=1.0  p25=1.0  p50=2.0  p75=4.0  p90=8.0  max=13.0

### Per-game top1 accuracy distribution

- min=0.3393  p10=0.3571  p25=0.3929  p50=0.4375  p75=0.4643  p90=0.5196  max=0.5893  mean=0.44

### By phase (discarder's n_discards before this action)

- deep(>12 disc): n=200  top1=0.43  top3=0.575  mrr=0.5611  baseline=0.3849  expert=0.74
- early(≤2 disc): n=600  top1=0.3583  top3=0.86  mrr=0.6092  baseline=0.3796  expert=0.78
- late(7-12 disc): n=1200  top1=0.4375  top3=0.6075  mrr=0.5722  baseline=0.4291  expert=0.69
- mid(3-6 disc): n=800  top1=0.5075  top3=0.78  mrr=0.6669  baseline=0.5012  expert=0.7388

> Eval play is uniform random legal discards; top1_accuracy is expected near random_baseline_mean. expert_min_shanten_consistency measures how often rank_discards top1 equals pure min-shanten (own-hand oracle).
> Literature: 0.68–0.88 top-1 on human labels (not random play)
