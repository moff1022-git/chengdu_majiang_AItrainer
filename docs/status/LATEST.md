# 进度快照

> 2026-07-26 — **F0023 主窗每轮掷骰定庄展示**

## 本轮

| 项 | 说明 |
|----|------|
| 目标 | 每轮开始前掷骰，主窗口显示过程与结果 |
| 规格 | `docs/features/F0023_main_dice_roll_display.md` · Done |
| 实现 | 确认后 sleep 播动画 → 再 `PlayerGameRunner`；桌心真实 d1/d2 + 庄家 |
| 代码 | `display/dice_fx.py`、`table_view.py`、`app.py` |
| 规则 | 未改；仍 `roll_dice(dice_seed)` 可复现 |

## 体验路径

```bash
.venv/bin/python main.py play --players human,rule_ai,rule_ai,rule_ai
# 座位窗确认开始 → 主窗掷骰动画 → 换三张/行牌
```

## 下一步

| 序 | 动作 | 建议触发语 |
|----|------|------------|
| 1 | 本机开一局看掷骰 | 目视验收 |
| 2 | 可选座位窗同步骰点 | 新需求 |
