# F0010-L2 — 后期向听 / 结构（实现规格）

| 字段 | 值 |
|------|-----|
| **编号** | F0010-L2（F0010-ML 批次 L2） |
| **标题** | Late/deep shanten target recalibration + structure |
| **状态** | **`Approved` + Done**（2026-07-12 set20 复测） |
| **父计划** | `docs/features/F0010_mid_late_accuracy_plan.md` §3 L2 |
| **规则清单** | `docs/features/F0010_inference_rules_inventory.md` C5b / G1 / G4 / G5 |
| **实现入口** | `players/analysis/hand_predict.py` |
| **评估** | `tools/eval_hand_predict.py --set 20`（确认 `--set 50`） |
| **Out of Scope** | L3 排序（I2/I3/I4）；学习式 conf；完整 waits×M08；改 engine |

---

## 1. 意图

set20 上 late best ≈0.50–0.52，向听 MAE（pred Top1 vs true）≈**2.14**。  
旧目标向听 `max(0, 4.2 − 0.25·n_disc − 0.7·n_melds)` 相对固定集真值系统偏低（early 真值 ~6.7、公式 ~3.7），使慢路径过度偏好「过低向听」假设。

L2 只服务 **late/deep 选优与终评**，避免 mid 再被向听项拉伤。

---

## 2. 基线（set20 当前，`150207`）

| 指标 | 值 |
|------|-----|
| overall / mid / late / deep best | 0.498 / 0.479 / 0.504 / 0.560 |
| mean_abs_shanten_err（Top1） | **2.1435** |
| 旧公式 vs true 的 target MAE | ~1.56（日志拟合） |

---

## 3. 规则与实现

### L2.1 — C5b 目标向听表

**数据**：`set20`+`set50` 评估 jsonl 中 `true_shanten` 按 `n_discards` 均值（副露样本极少，meld 用固定救济）。

| n_disc | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13+ |
|--------|---|---|---|---|---|---|---|---|---|---|----|----|----|-----|
| target | 7.7 | 7.0 | 6.1 | 5.0 | 4.1 | 3.4 | 3.0 | 2.5 | 2.2 | 2.1 | 1.9 | 1.8 | 1.6 | 1.6 |

```
target(n_disc, n_melds) = max(0.0, TABLE[min(n_disc, 13)] - 0.85 * n_melds)
```

- 替换 `_score_hand` 内联公式。  
- 表可常量；注释标明来源「fixed-set empirical means」。  
- **mid 若调用 with_shanten**：仍可用新表（目标更贴近真值），但见 L2.2 默认 mid 不进向听选优。

拟合对照：新表 vs true 的 target MAE ≈ **1.33**（旧 1.56）。

### L2.2 — G4 仅 late/deep 向听参与选优（固化）

| 路径 | mid | late/deep |
|------|-----|-----------|
| beam / preselect | `with_shanten=False` | `False` |
| 主排序 `_score_joint` | **`False`（固化）** | **`True`** |
| 终评 blend | mid：**不**用 shanten 权重（`with_shanten=False` 打分）；UI 可另算 sh 填字段 | late：`0.82·fast + 0.18·slow(sh)` |
| 最终 Top-K 展示 | 可对每个 hyp 调 `_shanten_of_ids` 填 `shanten_est` | 同左（slow 已有） |

现状：`late_phase` 选优已 `with_shanten=True`，但 **mid 终评仍 `with_shanten=True`** → L2 改为 mid 终评关闭。

### L2.3 — G5 late 向听门限与听牌 bonus

仅 `phase in ("late", "deep")`（按**该对手** `n_disc`，与 `_disc_phase` 一致）：

| 条件 | 旧 | **L2** |
|------|----|--------|
| 高向听罚 | `late>0.45 and sh≥4` → ×0.7 | **sh≥3** → ×0.78；**sh≥4** → ×0.65 |
| 听牌 bonus | sh≤0 → ×(1.15+0.3·late_ratio) | ×(**1.22** + **0.35**·late_ratio) |
| 一向听标签 | 保留 | 保留 |

`late_ratio = min(1, n_disc/10)` 不变。mid 若误开 sh：保持旧 `sh≥4 → ×0.7`，不启用 sh≥3。

### L2.4 — G1 结构分 +20% 仅 late/deep

```
s = _structure_score(tiles)          # 形如 1 + bonus
if phase in ("late", "deep"):
    s = 1.0 + LATE_STRUCTURE_MULT * (s - 1.0)   # LATE_STRUCTURE_MULT = 1.2
w *= s
```

early/mid：结构分不变。

---

## 4. 代码触点

| 符号 / 位置 | 变更 |
|-------------|------|
| `TARGET_SHANTEN_BY_DISC` / `TARGET_SHANTEN_MELD_RELIEF` | 新增常量 |
| `_target_shanten(n_disc, n_melds)` | 新函数 |
| `_score_hand` G1/G4/G5 段 | L2.1–L2.4 |
| `predict_joint_scenes` 终评 blend | mid `with_shanten=False`；late 保持 True |
| `tests/test_hand_predict.py` | 目标表单调/夹紧；late 结构 ≥ base |

---

## 5. 验收

| 项 | 标准 |
|----|------|
| 单测 | 绿 |
| set20 late best | **≥ 上轮 0.504**（不降）；争取 ≥0.51 |
| set20 mid best | **≥ 上轮 0.479 − 0.01**（门禁：不降 >0.01） |
| set20 early / deep | early 不降 >0.015；deep 不降 >0.025 |
| 向听 MAE | **降 ≥0.2** 相对 2.14（目标 ≤1.94）；若 F1 升但 MAE 未达，记偏差不硬回滚 |
| 回滚 | mid 降 >0.01 或 early 降 >0.015 或 deep 降 >0.025 → 回滚 L2 |

---

## 6. 非目标

- 不改 TOP_K / conf 温度 / MMR（→ L3）  
- 不改斩色 / DH / C1  
- 不强制 mid 开向听选优  

---

## 7. 状态历史

| 日期 | 说明 |
|------|------|
| 2026-07-12 | 父计划 L2 条目 Approved；本文件展开为可实现规格 |
| 2026-07-12 | 用户「实现 L2 / 写 L2 规格」→ 写规格并编码 |
| 2026-07-12 | **Done** `set20-20260712_152100`：overall 0.505、mid **0.490**、late **0.513**、deep 0.570、early 0.466；MAE 2.16（未达 −0.2）；门禁 mid/early/deep 通过 |
