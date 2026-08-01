# F0007 — 主程序桌面布局、统一牌面与控制面板

| 字段 | 值 |
|------|-----|
| **编号** | F0007 |
| **标题** | Main table uniform tiles + responsive wrap + control panel |
| **状态** | `Done`（**主桌内部分区由 F0015/F0018 取代**；统一牌面/换行/控制开关仍有效） |
| **类型** | UI 增强 |
| **依赖** | F0001 几何、F0006 座位窗响应式算法、M07/M08 显示与 HUD |
| **关联** | `display/table_view.py`、`display/layout.py`、`display/control_panel.py`、`display/app.py` |
| **授权** | 用户需求：主窗牌面统一加大、随窗换行、防遮挡、控制面板 |
| **后继** | 布局骨架 → [F0015](F0015_main_window_interior_layout.md) / [F0018](F0018_ui_design_to_code_change_plan.md) |

---

## 1. 需求

| # | 说明 |
|---|------|
| R1 | 各玩家**手牌与弃牌**牌面**同一尺寸**（不再 tiny/small/大 混用） |
| R2 | 牌面有**最小宽**；窗口变大可略放大至上限；**禁止**小于最小值；放不下则**加行/加列** |
| R3 | 头像、分数、相位、推理 HUD、策略 HUD、控制面板**分区**，减少互相遮挡 |
| R4 | 主窗**控制面板**（可点）：各座是否明牌、推理开关、策略 HUD 开关、弃牌区开关等 |

---

## 2. 设计

### 2.1 统一牌面

- `MIN_TABLE_TW = 36`，`MAX_TABLE_TW = 52`  
- `tile_w = clamp(scale(window), MIN, MAX)`  
- 手牌 / 副露 / 弃牌均用 **同一 `tile_w`**  
- 左右座仍旋转 ±90° 朝向桌心；单元格尺寸按旋转后宽高推进  

### 2.2 分区布局（逻辑像素）

```
┌──────────────────────── content ────────────────┬─ panel ─┐
│ top hand band (wrap rows)                       │ 控制面板 │
│ L hand │     center: wall + river               │ 明牌开关 │
│ cols   │     (discards wrap)                    │ 推理     │
│        │                                        │ 策略     │
│ bottom hand band (wrap rows)                    │ 弃牌     │
└─────────────────────────────────────────────────┴──────────┘
```

- 右侧固定面板宽约 200–220px  
- 上下手牌带高度随行数增长，但夹在安全边距内  
- 推理/策略 HUD 改到面板下方或紧贴面板左侧，**不覆盖**底/顶手牌带  

### 2.3 控制面板项

| 控件 | 默认 | 行为 |
|------|------|------|
| 明牌 S0–S3 | 开（full 观战） | 关则该座画牌背 |
| 推理 HUD | 随 `show_hud` | 开/关 `analyze` 叠加 |
| 策略 HUD | 随 `show_hud` | 开/关策略条 |
| 显示弃牌 | 开 | 关则不画弃牌 |
| 收起面板 | 开 | 可点「«」收成窄条 |

快捷键（可选保留）：`H` 总 HUD；`1–4` 焦点座。

### 2.4 算法

复用 `players.view.responsive.compute_tile_grid`，调用时 **`min_tw == max_tw == tile_w`**（固定尺寸只换行），或本地 `pack_fixed(n, area, cell, gap)`。

---

## 3. 文件清单

| 路径 | 变更 |
|------|------|
| `docs/features/F0007_main_table_ui_panel.md` | 本规格 |
| `display/layout.py` | 分区几何、统一 tile_w |
| `display/table_view.py` | 统一牌面 + 换行 + 防遮挡 |
| `display/control_panel.py` | 新增 |
| `display/app.py` | 点击/状态联动 |
| `display/inference_hud.py` / `strategy_hud.py` | 位置避让面板 |
| `tests/test_table_layout.py` | 统一尺寸、换行、面板 hit |
| `docs/changelog.md` | 实现后 |

---

## 4. 验收

- [x] 手牌与弃牌视觉同宽  
- [x] 缩窄主窗：牌不小于 36px，多行/多列  
- [x] 面板开关影响明牌与推理  
- [x] 面板在右侧，内容区避让  
- [x] 相关 pytest 通过  

---

## 5. 实现记录

| 日期 | 内容 |
|------|------|
| 2026-07-10 | `layout` 统一 tile_w；`table_view` 分区换行；`control_panel`；app 点击联动；`tests/test_table_layout.py` |
