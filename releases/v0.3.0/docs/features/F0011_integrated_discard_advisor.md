# F0011 — 综合出牌顾问：对手预测 × 剩余牌 × 本家进张/番型 × 防放炮

| 字段 | 值 |
|------|-----|
| **编号** | F0011 |
| **标题** | Integrated discard advisor (F0010 + remain + offense + defense) |
| **状态** | **`Done`（A1–A6）**（用户「直接确认 a1-a6 并全部实现」） |
| **动机** | 用户要求：对手牌预测 + 对手「不要的牌」+ remain + 本家可能摸牌，综合指导拆牌/出牌；**抬胡率/高分胡，降放炮率** |
| **依赖** | F0010 联合预测、`remain_map`、`rank_discards`、`danger`、`estimate_opponents`、`engine.shanten` / `fan` |
| **非目标（本版）** | 端到端 RL；改血战计分规则；替代 engine 合法性 |

---

## 1. 实现前缺口（历史；A1–A6 已落地）

| 模块 | 实现前缺口 | 现状（v0.2.1） |
|------|------------|----------------|
| **F0010** `hand_predict` | 未接入本家出牌排序 | `integrated_discard` / `pipeline` 已接联合场景 |
| **strategy** `rank_discards` | 无 F0010 / 番期望 | F0011 路径已综合 |
| **danger** | 粗 `likely_waits` | 仍可用；F0011 增强防放炮项 |
| **fan** | 出牌建议未估期望番 | A 系列已纳入 |

**结论（历史）**：曾缺「对手不要什么 / 摸什么 / 胡多大」贯通；**现已 Done**。

---

## 2. 目标产品行为

对本家每个合法出牌候选 \(t\)，输出统一分：

\[
S(t) = \underbrace{S_{\text{攻}}(t)}_{\text{向听·进张·番}} 
- \underbrace{S_{\text{防}}(t)}_{\text{放炮风险}}
+ \underbrace{S_{\text{废}}(t)}_{\text{对手不要/安全}}
\]

| 子目标 | 含义 |
|--------|------|
| 抬胡率 | 打 \(t\) 后向听不升、有效进张（× remain）尽量大 |
| 抬高分胡 | 进张路径偏向高番形态（清一色/碰碰/卡心五等，按现 fan 表可估） |
| 降放炮 | 避开对手高置信听口；优先现物与「对手斩色/不要的张」 |

相位（本家视角，可用墙张或巡目）：

| 相位 | 权重倾向 |
|------|----------|
| **前** | 攻：拆搭效率、定缺；防：轻；废：中（试探安全） |
| **中** | 攻防平衡；开始吃 F0010 听口与斩色废张 |
| **后** | 防权重大幅上升；攻：听牌进张 × 期望番 |

---

## 3. 核心新概念：对手「不要的牌」\(U\)

对每个对手 \(s\)、联合场景 \(\mathcal{J}_k\)（F0010 Top-K，权重 \(w_k\)）：

### 3.1 场景内废张信号（排除其定缺色可另标「必打完」）

| 信号 | 定义（示意） | 来源 |
|------|--------------|------|
| 斩色色 \(D_s\) | 已弃该色 ≥K 且近窗仍出（复用 M2 `_dumped_suits`） | 弃牌时间线 |
| 已亮现物 | \(t\) 已在河/副露出现 | remain / discards |
| 假设手 \(H_{s,k}\) 外的「冷门」 | \(t \notin H_{s,k}\) 且同色邻接密度低 | F0010 场景 |
| 非听口 | \(t \notin \mathrm{ukeire}(H_{s,k})\)（当向听=0） | engine ukeire |
| 定缺色 | 有定缺后该色 **必不用于胡**（对本家：打出较安全，但本家自己定缺另论） | dingque |

### 3.2 边际「安全/废张」分

对候选打出 \(t\)：

\[
S_{\text{废}}(t) = \sum_s \sum_k w_k \cdot \Big(
\alpha \cdot \mathbf{1}[t \in D_s]
+ \beta \cdot \mathbf{1}[t \text{ 现物}]
+ \gamma \cdot \mathbf{1}[t \notin H_{s,k}]
+ \delta \cdot \mathbf{1}[t \notin \mathrm{waits}_{s,k}]
\Big)
\]

- **安全出牌**：\(S_{\text{废}}\) 高且 \(S_{\text{防}}\) 低。  
- **危险**（即使效率高）：高 \(S_{\text{防}}\)（见 §4）。

---

## 4. 放炮风险 \(S_{\text{防}}\)（升级 danger）

### 4.1 用 F0010 替换/增强 waits

对场景 \(k\)、对手 \(s\)：

- 若 \(\mathrm{sh}(H_{s,k})=0\)：\(\mathrm{waits}_{s,k} = \mathrm{ukeire}(H_{s,k})\)  
- 若 \(\mathrm{sh}=1\)：可选「一向听危险张」= 进张后可听的集合近似（二期）  
- 场景加权听口概率：

\[
P_{\text{ron}}(t) \approx \sum_s \sum_k w_k \cdot p_{\text{tenpai},s,k} \cdot \mathbf{1}[t \in \mathrm{waits}_{s,k}]
\]

### 4.2 危险等级（替换粗邻张）

| 等级 | 条件（示意） |
|------|----------------|
| critical | \(P_{\text{ron}}\) 高 **或** 多对手场景同时听 \(t\) |
| high | 单对手高 conf 场景听 \(t\) |
| medium | 一向听热区 / 非现物中张 |
| low/safe | 现物或高 \(S_{\text{废}}\) 且 \(P_{\text{ron}}\) 低 |

**防放炮**：\(S_{\text{防}}(t) = \mathrm{Penalty}(\mathrm{level}(t))\)（可沿用 `DANGER_PENALTY` 表，系数按相位放大后期）。

---

## 5. 进攻 \(S_{\text{攻}}\)：拆牌 + 摸牌 + 高分

对打出 \(t\) 后手 \(H' = H\setminus\{t\}\)：

| 项 | 计算 | 作用 |
|----|------|------|
| 向听 | \(\mathrm{sh}(H')\) | 越小越好 |
| 有效进张数 | \(\sum_{u \in \mathrm{ukeire}(H')} \mathrm{remain}(u)\)（**排除**被 F0010 高概率锁在对手手里的张：可选扣减） | 抬胡率 |
| 摸牌竞争 | \(\mathrm{remain}_{\text{eff}}(u) = \max(0, \mathrm{remain}(u) - \sum_{s,k} w_k \mathrm{count}(H_{s,k},u))\) | 对手「还握着」的进张贬值 |
| 期望番 | 对主要进张 \(u\)：估胡形番期望 \(E[\mathrm{fan} \mid H'+u]\) 的加权（可用简化：清一色进度、对子数、中张等 proxy，二期接 fan 全表） | 抬高分胡 |
| 拆搭代价 | 若 \(t\) 拆唯一顺/对，额外罚（与 F0010-DH 组合思想对称：**本家**不应乱拆） | 前中期形 |

示意：

\[
S_{\text{攻}}(t) = -a\cdot \mathrm{sh}(H')
+ b\cdot \mathrm{ukeire\_eff}(H')
+ c\cdot E[\mathrm{fan}]
- d\cdot \mathrm{break\_cost}(t)
\]

相位：\(a,b,c,d\) 前中后不同（后：\(a,c\) 大；前：\(d\) 相对重要）。

---

## 6. 综合决策流程（推荐实现顺序）

```
可见状态 + 本家手
    │
    ├─► F0010 predict_joint_scenes → {J_k, w_k, H_s,k}
    ├─► remain / remain_eff（扣对手场景占用）
    ├─► 对每个合法 t:
    │      H' = hand \ t
    │      S攻(t), S防(t), S废(t)
    │      S(t) = S攻 - S防 + S废
    └─► 排序 → best / second / avoid
             UI：推荐打、危险标、可选「安全进张」说明
```

| 接入点 | 变更 |
|--------|------|
| `players/analysis/strategy.py` | `rank_discards` 增加 F0010 可选输入与新分项 |
| `players/analysis/danger.py` | `rate_discard_danger` 支持 F0010 waits |
| `players/analysis/pipeline.py` | `analyze_for_seat` 可选 `use_f0010=True` |
| `players/analysis/hand_predict.py` | 导出「斩色 / 场景边际」工具函数（不循环依赖） |
| 座位窗 / 主 HUD | 展示综合推荐（可开关，默认关以免 CPU） |
| 新模块（建议） | `players/analysis/integrated_discard.py` 承载公式，避免 strategy 过重 |

---

## 7. 分批实施计划

| 批次 | 内容 | 产出 | 验收 |
|------|------|------|------|
| **A0** | 文档 Approved；接口草图 | 本文件 | 用户确认 |
| **A1** | `remain_eff` + F0010 场景加权 waits → 升级 danger | `danger.py` + 单测 | 现物/听口危险排序合理 |
| **A2** | \(S_{\text{废}}\)：斩色∪非假设手∪非听口 | `integrated_discard.py` | 安全张排序↑ |
| **A3** | \(S_{\text{攻}}\)：ukeire_eff + 拆搭代价；接现有 shanten | 同上 | 进张张数不劣化 |
| **A4** | 期望番 proxy（清一色进度等） | 轻量 fan proxy | 高分路径倾向可测 |
| **A5** | pipeline 开关 + 座位/主 HUD | UI | 可关、可耗时上限 |
| **A6** | 固定集 + 对局指标：自摸/点炮/放炮/均番（需 rule_ai 对局） | 评测脚本 | 相对基线放炮率↓或均番↑ |

**Out of Scope 首批**：完整枚举所有番型期望、多线程重算每拍 F0010（可复用座位窗已算结果）。

---

## 8. 与 F0010 / DH 的关系

| 能力 | 角色 |
|------|------|
| F0010 联合场景 | 提供 \(H_{s,k}\)、权重、斩色、听口原料 |
| F0010-DH | 约束**对手模型**自身一致性（出牌–手牌） |
| **F0011** | 用上述模型服务**本家**出牌：攻 + 防 + 废 |

不替代 F0010；是「预测 → 决策」的上层。

---

## 9. 风险

| 风险 | 缓解 |
|------|------|
| F0010 每拍 CPU | 默认关；或沿用已算 forecasts；限 Top-3 场景 |
| 预测错导致「假安全」 | 防分用上界/多场景；现物优先；后期提高防权重 |
| 期望番过拟合 | A4 仅 proxy，A6 用对局均番验收 |
| 循环依赖 | F0010 工具函数下沉 `hand_predict` 纯函数；integrated 单向依赖 |

---

## 10. 开放问题（确认时锁定）

| # | 问题 | 默认建议 |
|---|------|----------|
| Q1 | 默认是否开启综合顾问？ | **关**（开关，与 F0010 类似） |
| Q2 | 防权重后期放大倍数？ | **×1.5～2.0**（墙<30 时） |
| Q3 | remain_eff 是否扣对手场景占用？ | **是**（A3） |
| Q4 | 期望番用 proxy 还是全 fan？ | **先 proxy，后接 fan** |
| Q5 | 与 rule_ai 出牌是否共用？ | **二期**；一期仅 analysis/HUD |

---

## 11. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-12 | `Review` | 用户提出综合攻防+摸牌+高分+降放炮；文档先行 |
| 2026-07-12 | **Approved + Done A1–A6** | 用户确认全实现：`integrated_discard` / danger 升级 / pipeline 开关 / `tools/eval_f0011.py` |

---

## 12. 建议触发语

| 说法 | 动作 |
|------|------|
| `确认 F0011` / `Approved F0011` | 状态→Approved，仍不写代码 |
| `实现 F0011 A1` | 升级 danger + F0010 waits |
| `实现 F0011 A2` | \(S_{\text{废}}\) |
| `实现 F0011 A3` | \(S_{\text{攻}}\) + remain_eff |
