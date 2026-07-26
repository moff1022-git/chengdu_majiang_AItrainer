# M08 — 分析推理模块 + 策略/推理 HUD

| 字段 | 值 |
|------|-----|
| **编号** | M08 |
| **标题** | Analysis pipeline + inference/strategy HUD |
| **状态** | `Done` |
| **依赖** | **M01–M07 Done**（shanten/win、AssetManager、TableView、RuleAI） |
| **下一里程碑** | M09（Human 子进程 + transport） |
| **对应 PLAN** | `players/analysis/*`、`players/view/*`、ASSETS §10–11、§11 M8 |

---

## 1. 目标

在玩家侧提供**可复用的局面分析**，并在主程序观战桌面上叠加 **推理 HUD / 策略 HUD**（使用 `assets/inference/*`、`assets/strategy/*`）：

1. **`players/analysis/`**：剩余牌、危险度、对手听牌估计、弃牌策略建议（纯逻辑，无 Pygame）。  
2. **统一分析结果结构** `AnalysisSnapshot`，供 RuleAI、JSONL `decision.analysis`、HUD 共用。  
3. **`display` 或 `players/view` 的 HUD 绘制**：向听徽章、危险角标、最优/次优/避免标记、策略面板、对手听牌灯。  
4. **接入**：  
   - RuleAI 用 analysis 填 `Decision.analysis`（增强 M06 启发式）。  
   - TableView / App 对 **焦点座位** 显示 HUD（默认观战 FULL 时焦点 seat 可切换）。  
5. **性能**：单次分析对 13–14 张手牌 < 50ms（目标）；可缓存至 state 变更。

本步**不**实现：Human 独立窗口完整交互（M09 可复用 analysis + HUD 组件）、精确贝叶斯手牌推断、神经网络。

---

## 2. 范围

### 2.1 In Scope

| 项 | 说明 |
|----|------|
| `players/analysis/remain.py` | 可见牌统计 → 每张 0–4 剩余 |
| `players/analysis/danger.py` | 弃牌危险度等级 |
| `players/analysis/opponent_model.py` | 粗粒度听牌/伺胡估计 |
| `players/analysis/strategy.py` | 弃牌排序、向听、进张、建议 |
| `players/analysis/pipeline.py` | `analyze_for_seat(state, seat) -> AnalysisSnapshot` |
| `display/asset_manager.py` | 扩展 `danger()` / `inference()` / `strategy()` 加载 |
| `display/inference_hud.py` | 推理叠加绘制 |
| `display/strategy_hud.py` | 策略叠加绘制 |
| `display/table_view.py` / `app.py` | 接入 HUD；快捷键切换焦点座 / 开关 HUD |
| `players/rule_ai_player.py` | 可选调用 pipeline 丰富 analysis |
| 测试 | remain 守恒、danger 等级边界、strategy 排序稳定、HUD 不抛错（dummy） |

### 2.2 Out of Scope

- 完整对手手牌穷举 / Monte-Carlo 大规模模拟（可预留接口，M08 用启发式）  
- Human 操作绑定（M09）  
- 修改引擎规则  

---

## 3. 设计

### 3.1 AnalysisSnapshot

```python
@dataclass
class AnalysisSnapshot:
    seat: int
    shanten: int
    ukeire: list[str]              # tile ids
    ukeire_count: int              # 理论张数合计（按 remain 截断）
    remain: dict[str, int]         # tile_id -> 0..4 still in wall+unknown
    danger: dict[str, str]         # tile_id -> danger level
    discard_ranks: list[DiscardAdvice]
    opponents: list[OpponentHint]
    generated_ms: float

@dataclass
class DiscardAdvice:
    tile_id: str
    rank: int                      # 1=best
    shanten_after: int
    ukeire_after: int
    danger: str
    score: float                   # 综合分，越大越好
    mark: str                      # best|second|avoid|none

@dataclass
class OpponentHint:
    seat: int
    tenpai_prob: float             # 0..1 启发式
    tenpai_level: str              # active|unknown  → 资源灯
    likely_waits: list[str]        # 最多 5 个估计伺胡
```

### 3.2 remain.py

**可见集合**：本家 hand + 所有 melds + 所有 discard_pile +（FULL 观战可选计入其他手牌——**分析 API 默认仅用公开信息 + 本家手牌**，与玩家视角一致）。

```text
full_count[tile] = 4
remain[tile] = 4 - visible_count[tile]
```

输出 27 种牌面的剩余；不可见为「可能在他家或墙」。

### 3.3 danger.py

对「若打出 tile_id」的危险度（启发式，可配置权重）：

| 信号 | 权重方向 |
|------|----------|
| 该牌已被多家弃过 / 现物 | 更安全 → safe/low |
| 对手刚有副露且该牌靠近其弃牌断裂 | 升高 |
| 对手 `tenpai_prob` 高且牌在其 likely_waits | critical/high |
| 筋牌/两面相关粗规则 | medium |
| 缺省 | unknown 或 low |

等级集合：`critical|high|medium|low|safe|unknown`（对齐 ASSETS）。

**默认表**（可调）：

```text
if in all_discards and count>=1 and not in any_likely_wait: safe/low
if any opponent tenpai_prob>=0.6 and tile in likely_waits: critical
elif tenpai_prob>=0.4 and near wait: high
...
```

### 3.4 opponent_model.py

对每个他座 active：

- 输入：副露、弃牌、手牌张数、是否已定缺。  
- `tenpai_prob`：  
  - 副露多 + 弃牌后期 → 升高  
  - 简单：`min(1.0, 0.15 * num_melds + 0.02 * discards + (0.2 if late_game))`  
- `likely_waits`：基于「弃牌断筋、副露指向」的极简生成（可为空）。  
- `tenpai_level`：`tenpai_prob >= 0.5` → `active` else `unknown`。

### 3.5 strategy.py

对焦点座位、当前若处于可弃牌（或假设 14 张手牌）：

1. 枚举 unique tile 弃牌候选（若有 legal_actions 则仅 legal discards）。  
2. 对每个候选：`shanten_after`、`ukeire` 规模、`danger`。  
3. 综合分：

```text
score = -4 * shanten_after + 0.15 * ukeire_count - danger_penalty[level]
```

4. 排序：  
   - rank1 → `mark_best`  
   - rank2 → `mark_second`  
   - danger in {critical,high} 且非 best → `mark_avoid`（可叠加）  
5. 面板数据：当前 shanten、deal_in 粗风险（best 弃牌的 danger 映射 0–100）、expectation ≈ ukeire_count。

**无合法弃牌时**（他座行牌）：只算当前 shanten/ukeire/对手提示，不画弃牌角标。

### 3.6 pipeline.py

```python
def analyze_for_seat(
    state: GameState,
    seat: int,
    *,
    legal_discards: list[Action] | None = None,
) -> AnalysisSnapshot: ...
```

纯函数；不修改 state。

### 3.7 AssetManager 扩展

```python
def danger(self, level: str) -> Surface: ...
def inference(self, key: str) -> Surface:  # panel, tenpai_active, remain_bar, ...
def strategy_asset(self, key: str) -> Surface:  # panel, mark_best, shanten_badge, ...
```

路径：

```text
inference/danger_{level}_{theme}.png
inference/infer_panel_{theme}.png
inference/tenpai_active_{theme}.png
...
strategy/strategy_panel_{theme}.png
strategy/mark_best_{theme}.png
...
```

### 3.8 HUD 绘制

#### inference_hud.py

- 对手头像旁：`tenpai_active` / `tenpai_unknown`  
- 可选：侧栏 `infer_panel` + 文字 likely_waits（SysFont）  
- 本家手牌右上角：`danger_*` 小角标（仅焦点座 + 有 discard 分析时）

#### strategy_hud.py

- 手牌上方 `strategy_panel`  
- 上叠：shanten 数字（digit sm）、ukeire 数  
- 手牌：`mark_best` / `mark_second` / `mark_avoid`  
- 可选 `deal_in_bar` 作底图 + 文字百分比  

**与 TableView 协作**：`TableView.draw(..., analysis: AnalysisSnapshot | None)` 在画完手牌后调 HUD；或 App 在 table.draw 后叠加。

推荐：

```python
# app / table
analysis = analyze_for_seat(state, focus_seat, legal_discards=...)
table.draw(screen, state, fx, analysis=analysis)
```

### 3.9 App 交互

| 键 | 行为 |
|----|------|
| `H` | 开关 HUD 显示 |
| `1`–`4` | 焦点座位 0–3（并刷新 analysis） |
| `A` | 强制刷新 analysis 缓存 |

步进时：仅当 `focus_seat` 的手牌/phase 变化时重算（简单：每 step_once 后若 HUD 开则重算）。

### 3.10 RuleAI 增强

```text
decide discard:
  snap = analyze_for_seat(...)
  pick snap.discard_ranks[0]
  analysis = asdict(snap) 精简
```

保持非法不发生：仍必须 ⊆ legal_actions。

### 3.11 日志

Decision.analysis 可含：

```json
{
  "shanten": 1,
  "best": "wan_3",
  "danger": {"wan_3": "low"},
  "ukeire_count": 12
}
```

体积控制：不写完整 remain 除非 `verbose_analysis=true`。

---

## 4. 文件清单

| 路径 | 动作 |
|------|------|
| `players/analysis/__init__.py` | 新增 |
| `players/analysis/remain.py` | 新增 |
| `players/analysis/danger.py` | 新增 |
| `players/analysis/opponent_model.py` | 新增 |
| `players/analysis/strategy.py` | 新增 |
| `players/analysis/pipeline.py` | 新增 |
| `display/inference_hud.py` | 新增 |
| `display/strategy_hud.py` | 新增 |
| `display/asset_manager.py` | 扩展 |
| `display/table_view.py` | 接入 analysis |
| `display/app.py` | HUD 开关/焦点 |
| `players/rule_ai_player.py` | 可选 pipeline |
| `tests/test_analysis.py` | 新增 |
| docs | 状态 |

---

## 5. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| AN01 | remain 总和 | 可见后 remain 在 0..4 |
| AN02 | 现物弃牌 | danger 偏 safe/low |
| AN03 | strategy 排序 | best 的 shanten_after 为最小之一 |
| AN04 | analyze 不改 state | id 前后一致 |
| AN05 | RuleAI analysis 非空 | decide 含 shanten/best |
| AN06 | Asset danger/strategy 可加载 | Surface ok |
| R01 | 全量回归 | 通过 |

```bash
pytest tests/ -q
# 人工: python main.py play 后按 H / 1-4 看 HUD
```

---

## 6. 验收标准

- [x] `analyze_for_seat` 输出完整 AnalysisSnapshot  
- [x] 危险度 / 策略标记使用 ASSETS 对应 PNG  
- [x] 观战桌面可开关 HUD、切换焦点座  
- [x] RuleAI Decision.analysis 含关键字段  
- [x] 分析模块无 Pygame 依赖（可被 headless import）  
- [x] M01–M07 回归通过  

---

## 7. 风险与开放问题

| 项 | 默认决议 |
|----|----------|
| 对手模型 | **启发式**，非精确 |
| HUD 默认 | **开启**（观战演示） |
| 分析视角 | **本家手牌 + 公开信息**（与玩家一致） |
| 性能 | 每步重算；若卡顿再加缓存 |

**开放问题 — 已关闭（用户确认 M08，2026-07-10）：**

| # | 决议 |
|---|------|
| 1 | HUD 默认 **开** |
| 2 | 分析 **不看** 他家手牌（即使 FULL 观战，保持玩家视角） |
| 3 | RuleAI 弃牌路径 **强制使用** pipeline |

---

## 8. 实现备注（编码后填写）

- 新增：`players/analysis/*`（remain/danger/opponent/strategy/pipeline）
- 新增：`display/inference_hud.py`、`strategy_hud.py`；AssetManager 扩展
- 接入：TableView/App（H / 1–4 / A）；RuleAI + orchestrator `_engine_state`
- 测试：`test_analysis.py`；全量 **93 passed**

---

## 9. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | `Review` | 首版规格，待用户确认 |
| 2026-07-10 | `Approved` | 用户确认 M08；开放问题按默认方案关闭 |
| 2026-07-10 | `Done` | 实现完成 |
