# 进度快照

> 2026-07-26 — **座位窗：胡牌提示 + 副露尺寸/中文**

## 本轮

| 项 | 说明 |
|----|------|
| 1 胡牌提示 | `hu_banner` 改挂 `op_info_fr`（修复跨父级 pack 失败）；本座 finished / 点胡立即显示；AI 窗同步 |
| 2 副露尺寸 | 与手牌同宽（不再固定 28px），AI 小窗完整显示 |
| 3 副露中文 | `pong→碰`、`ming_gang→明杠`、`an_gang→暗杠`、`jia_gang→加杠` |
| 代码 | `players/seat_window.py` |
| 测试 | `tests/test_seat_ui.py` · `meld_kind_label` |

## 基线

| 项 | 状态 |
|----|------|
| F0020 2H/3H | Done |
| 手牌选中金框 | Done |

## 下一步

| 序 | 动作 | 建议触发语 |
|----|------|------------|
| 1 | 本机胡一局确认红底横幅 | `play --players human,rule_ai,...` |
| 2 | AI 窗有碰/杠时看副露是否与手牌同大、中文标签 | 观战一局 |
| 3 | push（若需） | `push` |
