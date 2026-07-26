# 进度快照

> 2026-07-26 — **F0020 多人人类模式：Done**

## 本轮

| 项 | 说明 |
|----|------|
| 目标 | 确认并实现 F0020：2H+2AI（布局 B）、3H+1AI（布局 D） |
| 规格 | `docs/features/F0020_multi_human_modes.md` → **Done** |
| 布局规范 | `docs/design/UI_DESIGN_STANDARD.md` v1.4（A/B/C/D） |
| 代码 | 几何 D、Hub 多 human、app 多 attach、大厅 2H/3H 预设 |
| 测试 | `tests/test_f0020_multi_human.py` + 相关几何/registry；41 passed |

## 模式摘要

| 模式 | 布局 | CLI |
|------|------|-----|
| 1H+3AI | A | `human,rule_ai,rule_ai,rule_ai` |
| **2H+2AI** | **B** | `human,human,rule_ai,rule_ai` |
| **3H+1AI** | **D** | `human,human,human,rule_ai` |
| 0H+4AI | C | `rule_ai,rule_ai,rule_ai,rule_ai` |

## 关键代码

| 路径 | 变更 |
|------|------|
| `display/window_geometry.py` | `plan_mode_D`、`resolve (3,1)→D` |
| `players/seat_ui_hub.py` | `human_seats` 列表；`start_all`/`ensure_all` → dict |
| `players/registry.py` | 允许多 human（≤3） |
| `display/app.py` | 多 human plan + 全座 attach |
| `display/lobby_view.py` | 2H/3H 预设 |
| `tests/test_f0020_multi_human.py` | 新测 |

## 下一步

| 序 | 动作 | 产出 | 建议触发语 |
|----|------|------|------------|
| 1 | 本机目视 2H/3H 开局 | 确认窗口拓扑与 ready | `play --players human,human,rule_ai,rule_ai` |
| 2 | 可选：精简模式多 H 不重叠强化 | 文档/小补丁 | `F0020 精简` |
| 3 | 可选：4 人类拓扑 | 新 feature 文档 | `开始 F00xx 4人类` |
| 4 | 推送 origin（若尚未） | 远程同步 | `push` |
