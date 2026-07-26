# F0015 — 主窗口内部布局（左右分栏 · 牌局四分 · 侧栏三区）

| 字段 | 值 |
|------|-----|
| **编号** | F0015 |
| **标题** | Main window interior: 80/20 split, dice center, four player sectors, side panel |
| **状态** | **`Done`**（2026-07-21 随 F0018 实现） |
| **类型** | UI 设计 / 主窗信息架构 |
| **依赖** | UI_DESIGN_STANDARD（主窗外框）、F0007（历史实现，布局由本文取代） |
| **设计权威** | [`docs/design/MAIN_WINDOW_LAYOUT.md`](../design/MAIN_WINDOW_LAYOUT.md) |
| **程序修改** | [F0018](F0018_ui_design_to_code_change_plan.md) |
| **实现** | `display/main_interior.py`、`layout.py`、`table_view.py`、`side_scoreboard.py`、`play_log_panel.py` |

---

## 摘要

主窗客户区：

1. **左 80%** 实时牌局：中心正方形掷骰区；骰区四角连 TABLE 四角 → 四玩家区（下/右/上/左 = 玩家1–4）；每区 **从里到外** 弃牌 / 副露(2 行高) / 手牌(1 行高)  
2. **右 20%** 侧栏：上状态积分 · 中设置开关 · 下出牌日志  

细则、算法与验收见设计文档，不在此重复。

---

## 验收

见 `MAIN_WINDOW_LAYOUT.md` §7。

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | Draft；挂接 MAIN_WINDOW_LAYOUT v0.1 |
| 2026-07-21 | 用户确认三窗设计 + 示意图 → 设计 **Approved** |
| 2026-07-21 | MAIN_WINDOW_LAYOUT **v0.2**：玩家区从里到外弃牌→副露(2行)→手牌(1行) |
