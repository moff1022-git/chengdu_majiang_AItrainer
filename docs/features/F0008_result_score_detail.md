# F0008 — 主程序计分牌：各玩家积分明细

| 字段 | 值 |
|------|-----|
| **编号** | F0008 |
| **标题** | Main result scoreboard: per-seat score breakdown |
| **状态** | `Done` |
| **类型** | UI 增强（结算） |
| **依赖** | M05 `ScoreTransfer` / `score_events`、M07 `ResultView` |
| **关联** | `display/result_view.py`、`engine/blood_battle.GameResult`、`engine/score.py` |
| **授权** | 用户需求：主程序计分牌应完整显示各玩家的积分明细 |

---

## 1. 背景与动机

当前结算场景 `ResultView` 仅展示：

- 排名 + **总分**数字  
- 简短胡牌顺序（座位 / 番 / 自摸）  

缺少：

- 每一笔分变的 **来源与去向**（谁付谁、原因、番数、金额）  
- 终局标签（花猪 / 听牌 / 未听）与分变的对应关系  
- 便于复盘的 **按座位汇总明细**  

`state.score_events` 已在引擎中完整记录 `transfers`，只需汇入 `GameResult` 并在主窗计分牌渲染。

---

## 2. 需求

| # | 说明 |
|---|------|
| R1 | 结算页对 **每一名玩家** 展示：名次、座位、**总分** |
| R2 | 每位玩家下列出本局 **全部积分明细行**（有进有出） |
| R3 | 明细行可读：中文原因、对手座位、金额正负、有番时显示番数 |
| R4 | 附带终局标签摘要（花猪 / 有叫 / 未叫）与胡牌顺序（若有） |
| R5 | 窗口缩放时仍可读：明细可多列布局或缩小字号；行过多时纵向铺满可用区域，不截断关键总分 |
| R6 | **不改**计分规则本身；仅消费 `score_events` / `settle_tags` |

### Out of Scope

- 行牌中主桌实时弹出每笔分变动画（已有 hu/gang FX）  
- 座位窗结算页同步改造  
- 修改 `ScoreTransfer` 语义或底分公式  

---

## 3. 方案

### 3.1 数据：扩展 `GameResult`

```python
@dataclass
class GameResult:
    ...
    settle_tags: dict
    score_events: list[dict] = field(default_factory=list)  # NEW: type==score 的事件副本
```

`build_game_result(state)`：

```python
score_events = [e for e in (state.score_events or []) if e.get("type") == "score"]
```

`to_dict()` 同步包含 `score_events`（座位窗/日志兼容）。

### 3.2 明细构建（纯函数，无 pygame）

放在 `engine/score.py`（与 transfer 同源，便于单测）：

```text
build_score_ledger(score_events) -> dict[seat, list[ScoreLineDict]]
```

每条 line：

| 字段 | 含义 |
|------|------|
| `delta` | 对本座：`+amount` 收款 / `-amount` 付款 |
| `reason` | 原始 reason |
| `label` | 中文：自摸 / 点炮胡 / 明杠 / 暗杠 / 补杠 / 花猪 / 查叫 / … |
| `counterparty` | 对手座位 |
| `fan` | 可选 |
| `text` | 一行展示串，如 `+4 点炮胡(2番) ←S1` |

汇总校验：`sum(line.delta for line in ledger[s]) == scores[s]`（起点 0 时）。

### 3.3 UI：`ResultView`

布局（逻辑示意）：

```
本局结算 · 第 r/n 局
结束原因: wall_empty   花猪:S2  听:S0  未听:S1,S3
胡序: S2 点炮 1番 ←S0

┌─ #1 S1 总分 +8 ─────────────────┐
│  +2 点炮胡(1番) ←S0             │
│  +2 暗杠 ←S2                    │
│  …                              │
└─────────────────────────────────┘
… 其余座位按排名 …

L 回大厅   R 再来一局
```

- 按 `rankings` 顺序分块  
- 收入行偏金/绿，支出行偏红（颜色提示，非必须）  
- 宽窗：2 列玩家卡片；窄窗：1 列  
- 无明细时写「本局无分变」  

---

## 4. 影响面

| 层 | 影响 |
|----|------|
| engine | `GameResult` 字段 + ledger 纯函数；计分逻辑不变 |
| display | `ResultView` 重绘 |
| 兼容 | 旧 `GameResult(...)` 缺省 `score_events=[]`；`to_dict` 增字段向后兼容 |
| 训练/JSONL | 可选；本步不强制改 episode 日志格式 |

---

## 5. 文件清单

| 路径 | 变更 |
|------|------|
| `docs/features/F0008_result_score_detail.md` | 本规格 |
| `engine/score.py` | `REASON_LABELS` + `build_score_ledger` |
| `engine/blood_battle.py` | `GameResult.score_events`；`build_game_result` 填充 |
| `display/result_view.py` | 完整明细 UI |
| `tests/test_score_ledger.py` | ledger 聚合与文案 |
| `tests/test_result_view.py` | 绘制不抛错（dummy） |
| `docs/changelog.md` / `docs/features/README.md` | 回写 |

---

## 6. 验收

- [x] 任意完整对局结束，结算页每位玩家有总分 + 明细行（有分变时）  
- [x] 明细金额加总等于该座总分（从 0 起） — `test_ledger_matches_balances`  
- [x] 原因中文可读；含番的转移显示番数  
- [x] 花猪/查叫/杠/胡 均能出现在对应玩家明细中  
- [x] 相关 pytest 通过；dummy 绘制不崩溃  

---

## 7. 回滚

去掉 `ResultView` 明细绘制与 `GameResult.score_events` 即可；引擎计分不受影响。

---

## 8. 实现记录

| 日期 | 内容 |
|------|------|
| 2026-07-10 | `build_score_ledger` / `REASON_LABELS`；`GameResult.score_events`；`ResultView` 卡片式明细；`tests/test_score_ledger.py` + `test_result_view.py` |
