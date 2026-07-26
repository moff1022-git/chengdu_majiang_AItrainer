# Discard Accuracy 指标（set20 / set50）

| 字段 | 值 |
|------|-----|
| 日期 | 2026-07-13 |
| 定义 | 本家 **oracle 手牌** 可见时，`rank_discards` top-1/top-3 是否命中 **实际弃出张** |
| 文献对照带 | 人类牌谱监督下 top-1 常报 **68%–88%**（任务同形但标签不同） |
| 我方行牌 | fixed set 仍为 **均匀随机合法弃牌**（保持 F0010 可复现） |
| 代码 | `players/analysis/discard_accuracy.py` |
| set20 日志 | `logs/predict/set20-20260713_103846/` |
| set50 日志 | `logs/predict/set50-20260713_104634/` |

---

## 1. 指标定义

| 指标 | 含义 |
|------|------|
| **top1 accuracy** | 模型第 1 推荐 == 实际弃牌 |
| **top3 accuracy** | 实际弃牌落在模型 top-3 |
| **MRR** | 1 / rank(actual) |
| **random baseline** | 均值 1/n_legal（合法 **去重 tile_id** 数） |
| **expert consistency** | 模型 top1 == 纯最小向听专家（非文献 acc，测模型与 shanten 贪心一致率） |

每决策写 `discard_acc.jsonl`；汇总 `DISCARD_ACCURACY.json` 并写入 `ANALYSIS.md`。

---

## 2. 总表

| 指标 | set20 (n=1120) | set50 (n=2800) | 文献带 |
|------|----------------|----------------|--------|
| **top1 accuracy** | **0.438** | **0.440** | 0.68–0.88 |
| top3 accuracy | **0.716** | **0.709** | 常更高 |
| random baseline | 0.432 | 0.436 | — |
| lift vs random | **+0.007** | **+0.004** | — |
| expert min-shanten consistency | **0.718** | **0.727** | — |
| mean n_legal | 5.16 | 5.22 | 日麻常 ~10–14 |
| mean rank of actual | 3.03 | 3.03 | — |

**解读**：在 **随机合法弃牌** 标签下，top1 ≈ random baseline（~44%），**远低于** 人类牌谱上的 68–88%。  
高 baseline 因血战 **定缺强制弃** 等使合法去重张数常只有 ~2–6 张，而非 14 选 1。

---

## 3. 分布区间

### set20 — 实际弃牌在模型排序中的名次

| | min | p10 | p25 | p50 | p75 | p90 | max |
|--|-----|-----|-----|-----|-----|-----|-----|
| rank | 1 | 1 | 1 | **2** | 4 | 8 | 13 |

### set20 — 按局 top1 accuracy

| | min | p10 | p25 | p50 | p75 | p90 | max | mean |
|--|-----|-----|-----|-----|-----|-----|-----|------|
| per-game top1 | 0.339 | 0.355 | 0.388 | **0.429** | 0.500 | 0.520 | 0.571 | **0.438** |

### set20 — 相位

| 相位 | n | top1 | top3 | baseline | expert |
|------|---|------|------|----------|--------|
| early | 240 | 0.308 | 0.871 | 0.368 | 0.767 |
| mid | 320 | **0.500** | 0.769 | 0.476 | 0.709 |
| late | 480 | 0.458 | 0.627 | 0.436 | 0.694 |
| deep | 80 | 0.463 | 0.575 | 0.418 | 0.750 |

### set50 — 按局 top1 / 相位摘要

| | min | p10 | p50 | p90 | max | mean |
|--|-----|-----|-----|-----|-----|------|
| per-game top1 | 0.339 | 0.357 | **0.438** | 0.520 | 0.589 | **0.440** |

| 相位 | n | top1 | top3 | baseline | expert |
|------|---|------|------|----------|--------|
| early | 600 | 0.358 | 0.860 | 0.380 | 0.780 |
| mid | 800 | **0.508** | 0.780 | 0.501 | 0.739 |
| late | 1200 | 0.438 | 0.608 | 0.429 | 0.690 |
| deep | 200 | 0.430 | 0.575 | 0.385 | 0.740 |

---

## 4. 与 68%–88% 文献如何对齐

| 条件 | 文献 | 本评估 |
|------|------|--------|
| 标签 | 人类高手实际弃牌 | **随机合法弃牌** |
| 合法集大小 | 通常近满手 | 定缺后常 **很小** → baseline 抬高 |
| 模型 | CNN/RL 模仿人类 | `rank_discards`（向听+进张−危险） |

**若要对齐文献数字**，需要：固定集改用 **人类牌谱回放** 或 **rule_ai 自洽标签下的交叉模型**，不能继续用随机弃牌当 label。

**expert consistency ~72%**：说明当前 `rank_discards` 约 3/4 决策与「最小向听」一致，其余被 ukeire/危险拉开——这是有意义的 **策略结构** 指标，不是文献 discard acc。

---

## 5. 复现

```bash
.venv/bin/python tools/eval_hand_predict.py --set 20
.venv/bin/python tools/eval_hand_predict.py --set 50
# → logs/predict/set*-*/DISCARD_ACCURACY.json
# → ANALYSIS.md 末尾 Discard accuracy 节
```
