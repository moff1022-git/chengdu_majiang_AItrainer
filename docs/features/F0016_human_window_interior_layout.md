# F0016 — 人类玩家窗口内部布局

| 字段 | 值 |
|------|-----|
| **编号** | F0016 |
| **标题** | Human seat window interior: 67/33, op stack, foldable extension |
| **状态** | **`Done`**（2026-07-21 随 F0018 实现） |
| **类型** | UI 设计 |
| **依赖** | UI_DESIGN_STANDARD、F0012、F0014、F0015（主窗对照） |
| **设计权威** | [`docs/design/HUMAN_WINDOW_LAYOUT.md`](../design/HUMAN_WINDOW_LAYOUT.md) |
| **程序修改** | [F0018](F0018_ui_design_to_code_change_plan.md) |
| **实现** | `players/seat_layout_play.py`、`players/seat_window.py`（play 67/33 + 折叠） |

## 摘要

- 左 **67%** 操作区 / 右 **33%** 扩展区（可向左折叠）  
- 操作区：信息 1 行 → 状态 **20%**（打出|局分）→ 手牌 **60%**（副露+手牌+碰杠胡过）→ 设置 2 行  
- 扩展区：上 30% 对手 HUD，下 70% 本家弃牌  

细则见设计文档。

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | Draft v0.1 |
| 2026-07-21 | 用户 **确认人类窗口布局** → 设计 Approved；实现另令 |
