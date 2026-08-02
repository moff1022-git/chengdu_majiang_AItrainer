# F0023 — 主窗口每轮开局掷骰展示

| 字段 | 值 |
|------|-----|
| **编号** | F0023 |
| **标题** | Main window dice roll process & result each hand |
| **状态** | **`Done`**（2026-07-26） |
| **类型** | UI + 开局时序 |
| **依赖** | `engine/dice.py`、`create_dealt_game`（`game_id` → 可复现骰点） |
| **代码** | `display/dice_fx.py`、`display/table_view.py`、`display/app.py` |

## 目标

| ID | 说明 |
|----|------|
| G1 | **每轮开始前**主窗口播放掷骰过程（双骰面切换动画） |
| G2 | 动画结束后显示 **真实骰点** 与 **庄家座位**（与引擎 `state.dice` 一致） |
| G3 | 不改变定庄规则：`dealer = (d1+d2-1) % n`，种子来自 `game_id` |
| G4 | 事件日志一行摘要：`掷骰 d1+d2=total → 庄家 Sx` |

## 时序

```text
座位窗 ready 全员确认
    → 由 game_id 派生 dice（与 create_dealt_game 相同）
    → 主窗 DiceRollFx 开启动画（~2s）
    → 后台线程 sleep 等待动画（座位先不进入行牌）
    → PlayerGameRunner.run() 发牌 / 换三张…
```

## 主窗表现

- 桌心掷骰区：动画中快速切换 1–6 面；结束后定格 d1/d2  
- 文案：`掷骰定庄中…` → `点数 d1+d2=T · 庄家 Sx`  
- 牌墙剩余数在动画结束后仍显示  

## Out of Scope

- 改骰子概率或定庄公式  
- 座位窗同步播动画（可选后续）  
