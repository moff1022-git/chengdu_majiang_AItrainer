# F0010 — 座位窗：对手牌形推理预测

| 字段 | 值 |
|------|-----|
| **编号** | F0010 |
| **标题** | Seat window: opponent hand-shape prediction (top-5 + confidence + accuracy) |
| **状态** | `Done`（UI/协议 + **算法 v2**） |
| **类型** | 功能增强（UI + analysis + 协议） |
| **依赖** | F0002 座位窗、F0004 设置条、F0006 响应式布局、M08 analysis 骨架、engine 公共可见信息 |
| **关联** | `players/analysis/*`、`players/seat_window.py`、`players/seat_ui_hub.py`、`protocols/wire.py`、`display/app.py` live 广播 |
| **授权** | 用户需求（docs-first）：玩家窗对手牌推理；完整显示另三家预测手牌；按可能性排序 5 组牌形+可信度%；每出一张牌更新；主程序提供实际手牌算准确度；开关控制显示区 |

---

## 1. 背景与动机

现有 M08 / `estimate_opponents` 仅给出粗粒度 **听牌概率 + 可能等牌**，**不**输出完整手牌假设，也不做「预测 vs 实牌」校准。

训练器场景需要：

1. 在**本座座位窗**看到对其余三家的 **手牌形态假设**（完整 13/14 张语义下的牌组）；  
2. 每家按可能性给出 **Top-5 组**，附 **可信度 %**；  
3. **每次有人出牌**后刷新预测；  
4. 主进程持有全知状态时，回传 **实际手牌**，计算并展示 **预测准确度**（训练反馈，非线上防作弊）。

---

## 2. 目标

| ID | 目标 |
|----|------|
| G1 | 本座座位窗可展示 **另三家** 的对手牌预测面板 |
| G2 | **每家**显示 **最多 5 组** 预测手牌（牌形/牌集合），按可能性 **降序** |
| G3 | 每组显示 **可信度百分比**（0–100，组内相对或归一化见 §4.3） |
| G4 | 完整展示预测手牌内容（可缩略多行，但须可读出 tile_id / 万筒条+点） |
| G5 | **任意座位打出一张牌**（公共 `last_discard` 变化）后，**重新计算**三家各 5 组 |
| G6 | 主程序可下发 **实际手牌**（全知），本窗计算并显示 **准确度** 指标 |
| G7 | **开关**打开/关闭本功能；关闭后 **同步隐藏** 预测显示区域（不占布局） |
| G8 | 不改变引擎规则与计分；预测算法可迭代，接口稳定 |

---

## 3. 范围

### 3.1 In Scope

| # | 项 |
|---|-----|
| S1 | 预测数据模型：`OpponentHandHypothesis` / `OpponentHandForecast` |
| S2 | 预测引擎：基于 **本座可见信息** 生成每家 Top-5（初版可用启发式；接口预留替换） |
| S3 | 座位窗 UI：三家预测区 + 每家 5 行牌形 + 可信度 + 准确度条/数字 |
| S4 | 刷新触发：observation 中 `last_discard` / `last_discard_seat` / 相关公共字段变化 |
| S5 | 主→座协议：可选 `oracle_hands`（实际手牌）用于准确度 |
| S6 | 开关：座位设置条 + `seat_settings` 同步偏好；关则卸载/隐藏预测区域 |
| S7 | 单测：模型排序、归一化、准确度公式、开关隐藏逻辑（无 GUI 可测部分） |

### 3.2 Out of Scope

| # | 项 |
|---|-----|
| O1 | 主程序 Table 上的同款预测 HUD（可后续 F0011） |
| O2 | 完美贝叶斯 / 深度学习推理（初版不强制；允许启发式） |
| O3 | 用 oracle 手牌 **生成** 预测（禁止：准确度必须可区分「盲推」与「偷看」） |
| O4 | 网络对战防作弊保证（本产品为 **AI 训练器**，oracle 仅本地反馈） |
| O5 | 音效 / 复杂动画 |
| O6 | 改变 legal_actions 或引擎发牌 |

---

## 4. 设计

### 4.1 信息边界（强制）

| 数据 | 用途 | 来源 |
|------|------|------|
| 公共可见：全员弃牌、副露、定缺、牌墙剩余、本家手牌、last_discard… | **生成** Top-5 预测 | observation / 本座 view |
| 各对手 **真实手牌** | **仅**算准确度，不参与生成假设 | 主进程全知 state → 专用字段下发 |

```
                    ┌─────────────────────┐
  可见信息 ────────►│  predict_opponents  │──► Top-5 × 3 seats + conf%
                    └─────────────────────┘
  实际手牌 ────────►│  score_accuracy     │──► accuracy metrics（可选）
                    └─────────────────────┘
```

### 4.2 数据模型

```text
OpponentHandHypothesis
  rank: int                 # 1..5
  tiles: list[str]          # tile_id 列表，长度与当前该座应有手牌张数一致（见 §4.4）
  confidence: float         # 0.0..1.0（展示时 ×100 为百分比）
  label: str                # 可选简述，如「一向听偏清一色」

OpponentHandForecast
  seat: int                 # 被预测座位
  hypotheses: list[OpponentHandHypothesis]  # 长度 ≤ 5，已按 confidence 降序
  accuracy: float | null    # 0..1 或 null（无 oracle 时）
  accuracy_detail: dict     # 可选：best_match_rank, tile_f1, exact_set 等

SeatOpponentPredictSnapshot
  self_seat: int
  forecasts: list[OpponentHandForecast]  # 另三家
  discard_seq: int          # 单调序号，对应刷新世代
  enabled: bool
```

### 4.3 可信度百分比

- 预测器对每个对手输出最多 **5** 个假设，各带非负权重 `w_i`。  
- **归一化**（默认）：  
  `confidence_i = w_i / sum(w_j)`（sum=0 时均分或全 0）。  
- UI 显示：`round(confidence_i * 100)` + `%`，总和约 100%（舍入误差 ≤ 1pp 可接受）。  
- 文档要求：排序严格 `confidence` 降序；同权时按 `tiles` 字典序稳定排序。

### 4.4 手牌张数

- 活跃未胡：预测 `tiles` 长度 = **当前该座应有手牌数**（与 engine 一致：通常 13，轮到其出牌且已摸牌时为 14；已副露则相应减少）。  
- 已胡 / 非 active：不生成预测或显示「已离桌」。  
- 初版允许用「13 − 3×副露组数」近似，并在 observation 中优先使用服务端给出的 `hand_count`（若有）。

### 4.5 刷新时机

| 触发 | 行为 |
|------|------|
| 本座收到 observation，且 `last_discard` 或 `last_discard_seat` 或 `discard_seq` 变化 | 重算三家 Top-5 |
| 开局首帧 observation（尚无出牌） | 可算一版「开局先验」5 组 |
| 开关从关→开 | 立即用最新 observation 算一版 |
| 开关开→关 | **停止计算**；**隐藏**预测区域（pack_forget / 高度 0） |

「每出一张牌即更新」= 以 **全局最近一次出牌事件** 为节拍，不是仅本家出牌。

### 4.6 准确度（相对实际手牌）

主进程在 **功能开启** 且 **训练/观战全知合法** 时，向座位下发：

```json
{
  "type": "observation",
  "...": "...",
  "oracle_hands": {
    "0": ["wan_1", "..."],
    "1": ["..."],
    "2": ["..."],
    "3": ["..."]
  }
}
```

- 本座自己的 oracle 可省略。  
- **默认准确度公式**（可配置，初版固定）：  
  对每个对手 seat：  
  1. 取 Top-5 中与真实手牌 **多重集合 Jaccard / F1** 最高的一组 `best`；  
  2. `tile_f1 = 2|P∩T| / (|P|+|T|)`（多重集合按 tile_id 计数）；  
  3. `accuracy = tile_f1`（0..1），UI 文案为 **「牌张重合度」**（非整手猜中率）；  
  4. 展示：`best_rank`、`top1_f1`（可选）。  
- 另可选 **exact_set**：预测集合与真实完全一致则为 1 else 0（次要；预期近 0）。  
- **无** `oracle_hands` 时：`accuracy = null`，UI 显示「—」。  
- **开局粗粒度**（对手最大弃牌数 ≤ `EARLY_DISCARD_THRESHOLD`=2）：UI 仅展示 Top-3 的花色偏向 + 向听 + 策略，不铺满 13 张牌面。

> 安全说明：仅本地训练器使用；文档标明 oracle 不得用于预测生成。

### 4.7 预测算法

**接口**（稳定，实现可换体）：

```python
def predict_opponent_hands(
    state_view: dict | GameState,  # 仅本座可见过滤后的状态
    self_seat: int,
    *,
    top_k: int = 5,
    prev_forecasts: list[OpponentHandForecast] | None = None,
    prev_joints: list[JointHandScene] | None = None,  # v2：联合场景连续性
    last_discarder: int | None = None,
    last_discard_tile: str | None = None,
    seed: int | None = None,
) -> list[OpponentHandForecast]:
    ...
```

#### 4.7.1 初版（v1，已实现）问题 — 用户指出且属实

| # | 问题 | 现状（v1） |
|---|------|------------|
| P1 | **无时间连续性** | 每次出牌用新 seed 从 remain **重新随机采样**；不维护「上一拍的 Top-5 牌形」；预测与**完整弃牌序列**无因果链 |
| P2 | **弃牌记录利用极弱** | 仅对「最近 6 张弃牌 id 是否仍出现在假设手中」做线性惩罚；不分析弃牌顺序、斩花色、留搭子等 |
| P3 | **无策略模型** | 不假定对手「打安全牌 / 攻一门 / 清一色 / 快听」等基本策略 |
| P4 | **无听牌→胡牌方向** | 不估计向听、不约束「越打越进张/听牌」；假设可像任意一堆牌，与行牌目标脱节 |
| P5 | **对手之间无互斥** | 各家独立从同一 `remain` 采样，**可重复占用同一张「未见面」**（例如三家预测都握 2 张 `wan_5`，而 remain 仅 2），牌池守恒被破坏 |

结论：v1 适合占位与 UI 联调，**不适合**作为「推理预测」语义；须升级为 **v2**。

#### 4.7.2 修订算法 v2（目标行为，已实现）

**状态**：`Done` — 用户发「实现」后落地；联合场景 + 连续性 + 策略 + 向听 + 互斥。

##### A. 每家维护「对手模型状态」（跨出牌连续）

对每个对手 seat 在本局内维护（座位窗进程内存，不写盘）：

```text
OpponentTrack
  seat: int
  discard_timeline: list[tile_id]     # 该家按时间序完整弃牌
  meld_snapshot: list[meld]           # 当前副露
  dingque: suit | null
  hand_count: int
  hypotheses: list[HypothesisState]   # 上一拍存活的 Top-K（可 >5 候选池（内部））
  strategy: StrategyBelief            # 策略信念（见 B）
  shanten_belief: float | null        # 估计向听（越小越接近听）
  last_update_fp: str                 # discard 指纹
```

**连续性规则（强制）**：

1. 全局每出一张牌（任意人出）：  
   - 若出牌者是该对手：对其 **所有存活假设** 做 **一致性过滤**（见 C），再 **从过滤后集合重采样/修补** 至 Top-5。  
   - 若出牌者是别人：更新 remain；对假设做「该牌是否本应从其手中出现」的软约束，并微调权重。  
2. **禁止**在无 `prev_forecasts` 时每拍完全独立重随机当作默认行为；开局可冷启动一次，之后必须 `prev_forecasts` 或内部 `OpponentTrack`。  
3. 若过滤后假设数 < 3：允许 **受限重生**（仍须满足 C 的硬约束），不得整盘无约束重开。

##### B. 对手基本策略信念 `StrategyBelief`

用弃牌 + 副露 + 定缺 **在线更新** 若干互斥/可叠策略的软权重（初值均匀，每出牌更新）：

| 策略标签 | 可见信号（示例） |
|----------|------------------|
| `attack_clear` 攻一门/清 | 弃牌长期偏某两色，另一色几乎打光 |
| `dump_dingque` 先打定缺 | 前段大量定缺色 |
| `safe_fold` 防守 | 中后期大量字面安全/现物，副露少 |
| `fast_meld` 快副露 | 副露数↑、弃牌散 |
| `honors_trim`（成都无字牌可忽略） | — |

策略用于：

- **生成先验**：采样时按策略偏置牌池（如 `attack_clear` 提高主攻花色权重）；  
- **打分**：假设手牌与当前策略信念一致则加权。

##### C. 弃牌连续性硬/软约束

对假设手牌多重集合 \(H\)、该家新弃牌 \(d\)：

| 约束 | 类型 | 规则 |
|------|------|------|
| C1 打出必须曾可在手 | **硬** | 更新前 \(H\) 中应含 \(d\) 至少 1 张；过滤后 \(H' = H \setminus \{d\}\)（多重）再补摸入候选 |
| C2 定缺 | **硬（有定缺后）** | \(H\) 中不应含定缺花色（或权重→0） |
| C3 与已亮副露不冲突 | **硬** | 剩余手牌张数 = hand_count；牌池不超 remain |
| C4 弃牌时序 | **软** | 早期打光某色 → 后期假设不该仍大量持有该色；「现物」后降权危险搭子 |
| C5 进张方向 | **软** | 估计向听 \(\hat{s}\)：出牌后 \(\hat{s}\) 不应系统性变差；偏好「向听不增」的后继手牌 |

**补摸模型（对手摸打简化）**：  
当该家打出 \(d\) 后，从 remain（剔除 \(d\) 与可见）按策略加权抽 1 张 \(t_{\text{draw}}\) 补入假设，使张数回到 `hand_count`；多假设可对应不同 \(t_{\text{draw}}\)。

##### D. 听牌 → 胡牌运行方向

对每个假设手牌 \(H\)（+ 已知副露）计算：

- \(\hat{s}(H)\)：向听数（复用 `engine` 向听，**仅对手假设 + 副露**，无偷看真手）；  
- 听牌时 \(\hat{s}=0\)，并枚举/近似听口 `waits`；  
- 权重乘子：  
  - 中局：略偏好 \(\hat{s}\) 较小；  
  - 牌墙变少：加大「低向听 / 已听」权重；  
  - 与 `likely_waits`（M08）可交叉验证加分。

**叙事目标**：预测列表应体现「对手在往听、往胡走」，而非静态随机一手牌。

##### E. 跨对手牌池互斥（强制）

**原则**：未在「公共可见」中出现的每张牌实例，在全局上只能分给 **一个** 隐藏位置（某对手手牌 **或** 牌墙）。对「三家手牌」的联合预测必须 **近似守恒**：

\[
\forall t:\quad
\underbrace{\mathrm{vis}(t)}_{\text{已见}}
+ \sum_{s \neq \mathrm{self}} \mathrm{count}(H_s, t)
+ \underbrace{w(t)}_{\text{归因牌墙}}
\;\le\; 4
\]

其中 \(H_s\) 为该拍对座位 \(s\) 的**一条**联合假设中的手牌多重集合。实现上采用下面可计算的约定。

**E1. 联合假设（Joint assignment）**

- Top-5 **不再**定义为「三家各自独立 Top-5 的笛卡尔积」。  
- 每一条对外展示的「场景」是一组 **联合赋值**：  
  \(\mathcal{J}_k = (H_{s1}, H_{s2}, H_{s3})\)（另三家各一手），且 \(\mathcal{J}_k\) 内三家手牌对任意 `tile_id` **多重集合之和不超过 remain(t)**。  
- UI 仍可 **按座位分栏** 展示，但每个 rank \(k\) 的三家手牌必须来自 **同一** \(\mathcal{J}_k\)（同场景、互斥一致）。  
  - 若 UI 暂只能按「每家 5 行」展示：取 \(\mathcal{J}_1..\mathcal{J}_{5}\) 中该家的 \(H\)，并标注「场景 #k」；**禁止**把 A 的场景 #1 与 B 的场景 #3 拼成看似同时成立的画面而不声明冲突。

**E2. 生成顺序（推荐实现）**

1. 计算 `remain`（见 §4.1）。  
2. 决定对手处理顺序：建议 **信息多者优先**（副露多 / 弃牌长 / 手牌张数少者先定），或固定 seat 升序以保证可复现。  
3. 采样/更新第 1 家 \(H_{a}\) 时池 = remain。  
4. 采样第 2 家 \(H_{b}\) 时池 = remain **减去** \(H_{a}\) 占用（多重）。  
5. 第 3 家同理。  
6. 剩余池归隐式「牌墙」。  
7. 对整组 \(\mathcal{J}\) 打分 = 各家连续性/策略/向听分之和（或乘积的 log），再在联合层归一化得到场景可信度；分到各家行上的 % 可用「该场景 conf」或「边缘边缘化」（见 E4）。

**E3. 与连续性（§C）的衔接**

- 上一拍联合场景 \(\mathcal{J}\) 在出牌后：先对该出牌家做 C1 过滤，再在 **更新后的 remain 与其他家已占用** 下修补；  
- 若 A 打出 \(d\)：先从 \(H_A\) 去掉 \(d\)，再从「remain + 释放」中补摸；**不得**从仍被 \(H_B\) 占用的额度里偷牌。

**E4. 边缘展示（可选，UI）**

若需「每家独立 5 行」的边缘分布：对所有联合场景按 conf 加权，对座位 \(s\) 的某种手牌型 \(H\) 求和边缘概率，再取该家 Top-5。  
**注意**：边缘 Top-1 之间仍可能互斥冲突；UI 默认优先 **联合场景 #1…#5** 展示，边缘模式作为高级选项。

**E5. v1 对照**

| | v1 | v2 |
|--|----|----|
| 各家采样 | 独立、可重复占 remain | **串行扣减 / 联合场景** |
| 同一 `wan_5` remain=1 | 可被三家同时预测持有 | 至多一家持有 1 张 |

##### F. 可信度与 Top-5

- **联合场景**权重 \(w_k\) = 连续性 × 策略 × 向听方向 × 互斥可行（不可行场景 \(w=0\)）；  
- 归一化同 §4.3；取 Top-5 **场景**。  
- 分栏展示时标明场景编号；各家 confidence 默认等于所属场景 conf（联合展示）或 E4 边缘值。  
- UI 可选：策略标签、估计向听（`label` / `shanten_est`）。

##### H. 与准确度的关系

- 仍禁止用 oracle **生成**假设。  
- v2 准确度：对每个对手，在 **联合场景 Top-5** 中取该家分量与真牌的最佳 tile F1（与 §4.6 一致）；预期高于 v1。  
- 可选联合指标：三家 F1 平均（同一场景下同时评估）。

##### I. 实现落点（v2 编码时）

| 路径 | 变更 |
|------|------|
| `players/analysis/hand_predict.py` | `OpponentTrack`、连续性、策略、向听、**联合互斥采样** |
| `players/analysis/types` / 输出结构 | 可选 `JointHandScene`：`scene_id` + 三家 `H` + conf |
| `players/seat_window.py` | 缓存上一拍 **联合** forecasts；按场景展示 |
| `tests/test_hand_predict.py` | 连续性；**互斥：Σ_s count(H_s,t) ≤ remain(t)**；向听方向 |

---

### 4.7.3 版本策略

| 版本 | 状态 | 说明 |
|------|------|------|
| v1 | 已废弃 | 独立随机采样；问题见 §4.7.1 |
| v2 / v2.1 | Done | 联合场景 + 连续性 + 策略 + 向听 + 排序校准 + 早期粗粒度 |
| **v2.2 抬 F1** | **Done** | **波束联合搜索**（信息多者优先展开）；快评分筛候选 + 满向听终评；**局部换张精炼**；配额/后验采样；目标抬 Top-1 / best tile-F1 |

#### 4.7.4 v2.2 算法要点（抬 F1）

1. **波束（beam）联合赋值**：按信息量排序座位；对每个 beam 节点为当前座位采样多手 → 快分 → 扣 remain → 保留 Top-B 联合部分赋值。  
2. **终评**：对存活联合场景用完整 `_score_hand`（含向听）重打分，温度 softmax 出 conf。  
3. **精炼**：对 Top 场景在剩余池上做有限次「换一张」爬山，提高结构/花色/向听一致分。  
4. **连续性**：prev 场景仍 C1 演化后并入候选池，与 beam 结果合并取 Top-K。  
5. **性能**：快评默认不算向听；beam 宽与每步采样数有上限（见代码常量）。

### 4.8 UI（座位窗）

```
┌─────────────────────────────────────────┐
│ 标题 …  [设置]                           │
│ 设置条：… [对手牌预测：开/关]              │
├─────────────────────────────────────────┤
│ … 既有：当前打出 / 局数 / 得分 / 手牌 …     │
├─ 对手牌预测（仅 enabled）────────────────┤
│ S1  准确度 62%  (匹配#2)                  │
│  #1  28%  🀇🀈…（完整手牌一行或多行）      │
│  #2  15%  …                               │
│  …                                        │
│  #5   8%  …                               │
│ S2  …                                     │
│ S3  …                                     │
└─────────────────────────────────────────┘
```

| 规则 | 说明 |
|------|------|
| 位置 | 建议在「当前打出 / 得分」与「本家手牌」之间，或 mid 可滚动区顶部独立 Frame |
| 关闭 | `pack_forget` 整个预测 Frame；不留空白占位 |
| 牌面 | 优先小牌图；过窄可改用缩写文本 `1万 2万 …` |
| 性能 | 预测计算放后台线程或限频（≤ 1 次 / discard 事件）；UI 主线程只应用结果 |
| watch / play | 均支持（观战同样需要推理展示） |

### 4.9 开关

| 层 | 行为 |
|----|------|
| UI | 设置条 Toggle「对手牌预测」 |
| 状态 | `self.predict_opponents_enabled: bool`（默认 **False**，避免默认重 CPU） |
| 协议 | `seat_settings` 增加可选字段 `predict_opponents: bool`（会话记忆，不写盘） |
| 主进程 | 仅当 **至少一个** 座位开启时，observation 附加 `oracle_hands`（减负）；否则不下发 |

---

## 5. 协议与兼容

| 方向 | 字段 | 兼容 |
|------|------|------|
| obs 扩展 | `oracle_hands?: { "seat": [tile_id,…] }` | 旧座位忽略未知字段 |
| obs 扩展 | `discard_seq?: int`（可选，主进程全局出牌序号） | 无则用 last_discard 指纹 |
| seat_settings | `predict_opponents?: bool` | 旧主进程忽略 |

不改动 `ready` / `decision` 语义。

---

## 5.1 预测日志与准确率分析（F0010-L）

| 字段 | 值 |
|------|-----|
| **状态** | `Done` |
| **目的** | 每局落盘预测 tick；量化准确率；诊断偏低原因 |

### 日志路径

| 来源 | 路径 |
|------|------|
| 座位窗（开启预测时） | `logs/predict/{game_id}.jsonl` |
| 离线评估工具 | `logs/predict/eval-{stamp}/…` |

### 记录触发

每次座位窗成功刷新对手预测（discard 指纹变化）写一行 `type=predict_tick`。  
离线 `tools/eval_hand_predict.py` 对完整对局逐步采样同样格式。

### 行字段（核心）

`game_id, self_seat, discard_fp, phase, wall_remaining, used_continuity,`  
`opponents[]: seat, accuracy(best F1), top1_f1, best_rank, exact_set, n_discards, n_melds, strategy_hint, suit_match, true_shanten, pred_shanten, random_baseline_f1`

### 分析输出

`analyze_predict_logs` / CLI → 汇总 mean F1、按信息量分桶、best_rank 分布、相对随机基线增益、根因列表；可写 `ANALYSIS.md`。

---

## 6. 文件清单（实现阶段）

| 路径 | 变更 |
|------|------|
| `docs/features/F0010_seat_opponent_hand_predict.md` | 本规格 |
| `docs/features/README.md` | 索引 |
| `players/analysis/hand_predict.py`（新） | `predict_opponent_hands` + `score_accuracy` |
| `players/analysis/predict_log.py` | JSONL 写入 + 日志聚合分析 |
| `players/analysis/predict_eval.py` | 无头对局逐步评估 |
| `tools/eval_hand_predict.py` | CLI：跑评估 + 出分析报告 |
| `players/analysis/types.py` | 假设/预测数据类型 |
| `players/analysis/pipeline.py` | 可选挂接（或座位窗独立调用） |
| `players/seat_window.py` | 预测 UI + 开关 + 刷新 + 日志 |
| `players/seat_ui_hub.py` / `view_filter` / obs 构建 | 按需注入 `oracle_hands` |
| `protocols/wire.py` / observation 序列化 | 字段文档化 |
| `tests/test_hand_predict.py`（新） | 排序、归一化、准确度、长度 |
| `tests/test_predict_log.py` | 日志/分析 |
| `docs/changelog.md` | 实现后追加 |

---

## 7. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| T1 | 合成可见状态，固定 seed 预测 | 每家 ≤5 组，confidence 降序，和≈1 |
| T2 | `tiles` 长度符合 hand_count 规则 | 通过 |
| T3 | 给定 oracle 与假设列表 | `tile_f1` 公式正确 |
| T4 | 预测函数 **不读** oracle 字段（契约：接口无 oracle 参数） | 代码审查 + 测 |
| T5 | 开关 False 时不创建预测 Frame（或 pack 状态） | 单元/冒烟 |
| T6 | 连续两次不同 last_discard 触发两次 discard_seq/世代 | 通过 |
| T7 | 人工：开预测→出牌→列表更新；关预测→区域消失 | 验收 |

---

## 8. 验收标准

- [x] 规格 `Approved` 后实现  
- [x] 另三家各最多 5 组完整预测手牌 + 可信度 %  
- [x] 每出一张牌（全局 last_discard 变）后刷新  
- [x] 有 oracle 时显示准确度；预测计算未使用 oracle  
- [x] 开关关闭后预测区域不可见  
- [x] 相关 pytest 通过；不破坏既有 F0004/F0009  
- [x] changelog + 本规格状态 → `Done`  

---

## 9. 风险与开放问题

| 风险 | 缓解 |
|------|------|
| 组合爆炸 / 卡顿 | top_k=5、限频、后台线程、默认关闭 |
| 启发式质量差 | 接口可替换；准确度暴露真实水平 |
| 竖屏座位空间不足 | 可滚动；关闭即释放 |
| oracle 泄露观感 | 文档标明训练器用途；默认关预测 |
| 手牌张数与引擎不一致 | 优先服务端 `hand_count` / 与 melds 对齐 |

**开放问题（已确认 2026-07-11）**：

1. **默认开关**：**关**（按规格）。  
2. **准确度公式**：**tile 多重集合 F1**，对 Top-5 取最佳匹配（按规格）。  
3. **oracle 下发**：仅对 **已打开预测** 的座位下发 `oracle_hands`（按规格建议）。  

---

## 10. 回滚

1. 设置默认关；隐藏 UI 入口。  
2. 停止下发 `oracle_hands`。  
3. 删除/停用 `hand_predict.py` 与座位预测 Frame。  

---

## 11. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-11 | `Review` | 用户提出需求；文档先行，待确认后实现 |
| 2026-07-11 | `Approved` | 用户确认；开放问题按默认方案锁定；**尚未实现代码** |
| 2026-07-11 | `Done` | 实现 hand_predict + 座位 UI/开关 + oracle_hands；`tests/test_hand_predict.py` |
| 2026-07-11 | 算法 v2 `Review` | 用户指出 v1 缺连续性/策略/听胡方向；写入 §4.7.1–4.7.2 |
| 2026-07-11 | 算法 v2 增补 | **跨对手手牌互斥**（联合场景 / 串行扣 remain）；§4.7.2 E |
| 2026-07-11 | 算法 v2 `Done` | `hand_predict` 重写：JointHandScene / StrategyBelief / 连续性 C1 / 向听；seat_window 缓存 prev_joints；UI 场景#·策略·向听；测试含互斥与连续 |
| 2026-07-11 | 日志/分析 `Done` | §5.1：`predict_log` + `eval_hand_predict`；座位窗写 `logs/predict/{game_id}.jsonl`；15 局评估见 `docs/status/F0010_predict_accuracy_analysis.md` |
| 2026-07-11 | 准确率修正 v2.1 | 去排序噪声；弃牌时序硬约束；向听/结构加权；连续性优先；早期粗粒度 UI；准确度改「牌张重合度」 |
| 2026-07-12 | v2.2 抬 F1 | 相位自适应：早期均匀多样本+强多样性；中期混合；后期 beam/精炼/向听终评+连续性加强；花色 ensemble + greedy MAP + MMR Top-K |
