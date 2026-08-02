# F0006 — 玩家视窗响应式布局（随窗缩放 / 牌面换行）

| 字段 | 值 |
|------|-----|
| **编号** | F0006 |
| **标题** | Seat window responsive layout: scale + wrap |
| **状态** | `Done` |
| **类型** | 功能增强（UI） |
| **依赖** | F0002 座位窗、F0004 确认开始、F0005 双端兼容 |
| **关联** | `players/seat_window.py`（Tk 权威路径）、`players/view/player_view.py`（pygame 渲染路径） |
| **授权** | 用户需求：显示元素随窗口大小动态调整；牌面一排不全可换行 |

---

## 1. 背景与问题

当前座位窗内容多为 **单行 `pack(side=left)` / 单行坐标推进**：

- 窗口变窄时手牌/弃牌/副露被裁切或挤出可视区  
- 窗口变高时空白浪费，元素不重排  
- 用户期望：**所有显示元素随窗口大小动态分布**；牌面一排显示不完整时 **新增一排**

权威交互路径为 **tkinter `TkSeatApp`**（F0002 后）；`PlayerView` 仍用于部分绘制与测试，须保持算法一致。

---

## 2. 目标

| ID | 目标 |
|----|------|
| G1 | 窗口 **Resize** 后，手牌 / 副露 / 弃牌 / 操作按钮按可用宽度 **重算尺寸与行列** |
| G2 | 手牌：优先合理牌宽；一排放不下时 **自动换行**（可多行） |
| G3 | 弃牌、副露组同样可换行；按钮栏一行放不下时换行或增高底栏 |
| G4 | 点选/双击出牌的 hit-test 与可见布局一致（`hand_rects` / Tk 控件） |
| G5 | 不改变引擎协议与规则，仅 UI 布局 |

---

## 3. 范围

### In Scope

| # | 项 |
|---|-----|
| S1 | 共享布局算法：`tile_tw` / `per_row` / `rows` 计算 |
| S2 | `TkSeatApp`：`<Configure>` 防抖后重排；手牌/弃牌/副露多行；牌宽随宽缩放 |
| S3 | `PlayerView`：`_draw_hand` / 弃牌 / 按钮多行；`hand_rects` 正确 |
| S4 | 单元测试：给定宽高与 N 张牌，断言换行与不越界 |
| S5 | 规格 + changelog |

### Out of Scope

| # | 项 |
|---|-----|
| O1 | 主程序全局桌 `TableView` 全席响应式（可后续 F） |
| O2 | 动画过渡 |
| O3 | 用户自定义牌面 DPI 配置文件 |

---

## 4. 设计

### 4.1 布局算法（共享）

模块建议：`players/view/responsive.py`

```text
compute_tile_grid(n, area_width, *, min_tw, max_tw, gap, margin, label_w)
  → TileGrid(tw, th, per_row, rows, used_width)

策略：
1. 有效宽度 W = max(80, area_width - margin - label_w)
2. 从 max_tw 递减到 min_tw：若 n <= floor(W / (tw+gap)) → 单行该 tw
3. 否则取 min_tw（或 max(min_tw, W//8)），per_row = max(1, W//(tw+gap))，rows = ceil(n/per_row)
4. th ≈ tw * 1.4
```

可选高度约束：若 `rows * (th+gap) > hand_area_h`，略减 `tw` 再算（下限 `min_tw`）。

### 4.2 Tk 座位窗

| 区域 | 行为 |
|------|------|
| 手牌 | 标签 + 多行 `Frame`；每行 `side=left` 放牌按钮 |
| 副露 | 各组可横向排列；组过多时组间换行 |
| 弃牌 | 与手牌同算法（更小 `max_tw`） |
| 底栏按钮 | 横向排列，超出时换第二行 |
| 触发 | `root.bind("<Configure>")`，宽高变化且防抖 ~80ms 后 `_render_state`（保留 selection / pending） |

牌面缩放：`PhotoImage` 按目标 `tw` 缓存（已有 `_photo` key 含 tw）。

### 4.3 PlayerView（pygame）

| 区域 | 行为 |
|------|------|
| 手牌 | 自底栏向上排；多行时 **底行靠近按钮**，上行叠在其上 |
| 弃牌 | 自左向右，满行换行 |
| 按钮 | `bar_h` 随行数增高；`button_rects` 更新 |
| 副露 | 在手牌区上方，可换行 |

### 4.4 数据流

```
Resize / observation
    → 读 client width/height
    → compute_tile_grid(...)
    → 重绘控件或 surface
    → hit-test 使用新 rects
```

---

## 5. 文件清单

| 路径 | 变更 |
|------|------|
| `docs/features/F0006_seat_responsive_layout.md` | 本规格 |
| `docs/features/README.md` | 索引 |
| `players/view/responsive.py` | 新增算法 |
| `players/view/player_view.py` | 手牌/弃牌/按钮响应式 |
| `players/seat_window.py` | Configure 重排 + 多行 pack |
| `tests/test_responsive_layout.py` | 算法与绘制 smoke |
| `docs/changelog.md` | 实现后 |
| `docs/status/LATEST.md` | 实现后 |

---

## 6. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| T1 | `n=14, width=400` → `rows>=2` 或 `tw` 缩小后仍 `per_row*rows >= n` | 通过 |
| T2 | `n=5, width=800` → 单行、较大 `tw` | 通过 |
| T3 | PlayerView dummy surface 窄宽绘制后 `len(hand_rects)==n` 且 rect 不水平越界 | 通过 |
| T4 | 既有 seat / f0004 回归 | 通过 |

---

## 7. 验收标准

- [x] 缩小座位窗：手牌自动换行，牌面仍完整可见（可滚动区外无硬裁切整行）  
- [x] 放大座位窗：牌面变大或回单行，不重叠  
- [x] 弃牌/副露随宽换行  
- [x] 人类双击出牌 / 点选换三张在换行后仍正确（hit 与控件重建一致）  
- [x] 自动化测试 T1–T4 绿（全量 151 passed）  

---

## 8. 风险

| 风险 | 缓解 |
|------|------|
| Configure 风暴导致卡顿 | 防抖 80ms；尺寸未变不重绘 |
| PhotoImage 缓存膨胀 | tw 对齐偶数 |
| pack 与 hit 不一致 | 共享 `compute_tile_grid`；PlayerView 用 `hand_rects` |

---

## 9. 实现记录

| 日期 | 内容 |
|------|------|
| 2026-07-10 | `responsive.py`；Tk `Configure` 重排；PlayerView 多行手牌/弃牌/按钮；`tests/test_responsive_layout.py`；**151 passed** |
| 2026-07-10 | 修复牌面裁切：源图严格缩放到 `tw`、`cell_extra` 计边距、中区 Canvas 滚动、observation 二次布局；**152 passed** |
| 2026-07-10 | 策略改为**不缩小于 min_tw**（手牌默认 36）：宽则放大、窄则加行；AI 座改为手动确认开始 |
