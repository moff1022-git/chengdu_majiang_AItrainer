# F0017 — AI 玩家窗口内部布局

| 字段 | 值 |
|------|-----|
| **编号** | F0017 |
| **标题** | AI seat window interior: 67/33, read-only hand, AI log extension |
| **状态** | **`Done`**（2026-07-21 随 F0018 实现） |
| **类型** | UI 设计 |
| **依赖** | UI_DESIGN_STANDARD、HUMAN_WINDOW_LAYOUT / F0016、F0014 |
| **设计权威** | [`docs/design/AI_WINDOW_LAYOUT.md`](../design/AI_WINDOW_LAYOUT.md) |
| **程序修改** | [F0018](F0018_ui_design_to_code_change_plan.md) |
| **实现** | `players/seat_window.py`（watch 67/33 + AI 日志 + 弃牌 EXT） |

## 摘要

- 左 **67%** / 右 **33%**（可向左折叠），与人类窗同构  
- 操作区：信息 1 行 → 状态 **20%** → 手牌 **60%**（**仅副露+只读手牌，无碰杠胡过**）→ 设置 2 行  
- 扩展区：上 **30% AI 操作日志** · 下 **70% 本家弃牌**（人类窗上区为对手 HUD）  

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | Draft v0.1 |
| 2026-07-21 | 用户确认三窗设计 + 示意图 → 设计 **Approved** |
