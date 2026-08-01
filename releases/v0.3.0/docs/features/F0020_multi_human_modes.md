# F0020 — 多人人类模式（2 人类 / 3 人类）

| 字段 | 值 |
|------|-----|
| **编号** | F0020 |
| **标题** | Multi-human play modes (2H+2AI, 3H+1AI) |
| **状态** | **`Done`**（2026-07-26 用户确认并实现） |
| **类型** | 功能增强：人数配置 + 窗口布局 + 多代理协议 |
| **依赖** | F0001 / F0002 / F0004 / F0005 / F0018；几何权威 [`UI_DESIGN_STANDARD`](../design/UI_DESIGN_STANDARD.md) **v1.4+** |
| **关联代码**（实现阶段） | `display/window_geometry.py`、`display/app.py`、`players/seat_ui_hub.py`、`players/human_proxy.py`、`players/registry.py`、`main.py`、大厅选人 UI（若有） |
| **取代 / 扩展** | 解除 M09「仅 1 个 human」硬限制；扩展 UI 规范原 Out of Scope「3 人类局」 |

---

## 0. 背景

### 0.1 现状（实现侧）

| 能力 | 现状 |
|------|------|
| 引擎 4 座 | 已支持 4 座位规则（与是否 human 无关） |
| CLI `--players` | 可写多个 `human` 字符串，但主流程按 **单一** `human_seat` 绑定 |
| `SeatUIHub` | 构造参数 `human_seat: int \| None`（单座） |
| 窗口布局 | A=1H3AI、B=2H2AI、C=0H4AI；**无 3H 布局** |
| M09 | 首版硬限制 **1 个 human** |

### 0.2 目标

| ID | 目标 |
|----|------|
| G1 | 支持 **2 人类 + 2 AI**（布局 **B**）：可启动、可就绪、可轮流操作 |
| G2 | 支持 **3 人类 + 1 AI**（布局 **D**，新建）：同上 |
| G3 | 窗口初始 plan：**MAIN + 全部座位窗同屏完整显示**（几何见 UI 规范 v1.4） |
| G4 | 每人独立 play 子进程 / 独立座位窗；ready / decide 互不串座 |
| G5 | Docs-First：本规格 **Approved** 前不写业务代码（已满足） |

### 0.3 非目标（Out of Scope）

| 项 | 说明 |
|----|------|
| 4 人类 + 0 AI 专属新拓扑 | 可复用 C 的「无 AI」座位全 human，或后续 F；**本规格不强制 4H 布局** |
| 竖屏拓扑 | 仍不做 |
| 改麻将规则 / 人数改 2–3 人牌局 | 仍为 **4 座位** 血战；仅「谁是人类操作」变化 |
| 网络远程人类 | 仍为本机多进程 |
| 本轮出设计效果图 | 可选；文字+ASCII 为准 |

---

## 1. 产品配置表

固定 `num_players = 4`。`human` = play 座位窗；其余为 AI watch。

| 模式 ID | 人类数 | AI 数 | 布局 ID | CLI 示例（座位顺序 S0..S3） |
|---------|--------|-------|---------|------------------------------|
| **1H** | 1 | 3 | **A** | `human,rule_ai,rule_ai,rule_ai` |
| **2H** | 2 | 2 | **B** | `human,human,rule_ai,rule_ai` |
| **3H** | 3 | 1 | **D** | `human,human,human,rule_ai` |
| **0H** | 0 | 4 | **C** | `rule_ai,rule_ai,rule_ai,rule_ai` |

### 1.1 座位指派规则

```text
human_seats = [ i | players[i] 的类型为 human ]  # 保持出现顺序
ai_seats    = [ i | i not in human_seats ]

布局由 (len(human_seats), len(ai_seats)) 映射：
  (1,3) → A
  (2,2) → B
  (3,1) → D
  (0,4) → C
  其它 → 不支持（启动时报错并提示合法组合）
```

**人类窗落位顺序**（与 `human_seats` 列表下标对应，而非绝对 seat id）：

| 布局 | Human 槽位 | 含义 |
|------|------------|------|
| A | H[0] | 右下 |
| B | H[0] 右下；H[1] 右上 | |
| D | H[0] 右下；H[1] 左上（body）；H[2] 右上（body） | 见 §2.3 |

例：`--players rule_ai,human,human,rule_ai` → `human_seats=[1,2]`，布局 B；H[0]=S1 右下，H[1]=S2 右上。

### 1.2 入口与大厅

| 入口 | 行为 |
|------|------|
| CLI | `main.py play\|human --players ...` 解析多个 `human` |
| 大厅 UI | 须能选择 1/2/3 个「人类」座位（实现阶段；文档先定义合法组合） |
| 快捷 | 可保留 `main.py human` = 默认 1H3AI；新增文档示例 2H/3H 命令 |

---

## 2. 窗口布局（摘要 · 权威在 UI 规范 v1.4）

画布、85%、MAIN 左下、人类/AI 完整尺寸公式：**以 [`UI_DESIGN_STANDARD.md`](../design/UI_DESIGN_STANDARD.md) v1.4 为准**。本节只固定模式语义。

### 2.1 布局 B — 2 人类 + 2 AI（沿用并冻结）

```text
┌── AI ──┬── AI ──┬  人类 H[1] 25% ─┐
├────────┴───┬────┴─────────────────┤
│ MAIN 25%   │  人类 H[0] 25%       │
└────────────┴──────────────────────┘
```

- MAIN：左下 `Wm×Hm`  
- H[0]：右下 `Wm2×Hm`（与 MAIN **同高同底边**）  
- H[1]：右上 `Wm2×Hm`  
- AI×2：左上象限内顶对齐横排，`Wa×Ha`，不压 MAIN  

### 2.2 布局 A / C

不变（1H / 0H）。

### 2.3 布局 D — 3 人类 + 1 AI（新建）

**问题**：若坚持「每人 25% + MAIN 25%」共 100%，则无空间给 AI。  
**决议**：为 AI 预留 **顶带**（高 `Ha=⌊Lh/4⌋`），下方 **body** 做 2×2 四分：

```text
Ha = Lh // 4
GAP = 8（与实现一致即可）
body_top = Oy_c + Ha + GAP
body_h   = Lh - Ha - GAP
row_h    = body_h // 2
col_w    = Lw // 2
col_w2   = Lw - col_w
row_h2   = body_h - row_h
```

```text
┌──────────── AI（顶带，Wa×Ha，顶对齐/可水平居中或左缘）────────────┐
├─────────────────────┬────────────────────────────────────────────┤
│  人类 H[1]          │  人类 H[2]                                 │
│  col_w × row_h      │  col_w2 × row_h                            │
├─────────────────────┼────────────────────────────────────────────┤
│  MAIN               │  人类 H[0]                                 │
│  col_w × row_h2     │  col_w2 × row_h2                           │
└─────────────────────┴────────────────────────────────────────────┘
```

| 窗 | 位置（相对画布） |
|----|------------------|
| AI | `y=Oy_c`，`h=Ha`，`w=Wa`；`x` 默认水平居中于画布，或左对齐 `Ox_c`（实现二选一，**默认左对齐与 A 带一致**） |
| H[1] | `x=Ox_c, y=body_top, w=col_w, h=row_h` |
| H[2] | `x=Ox_c+col_w, y=body_top, w=col_w2, h=row_h` |
| MAIN | `x=Ox_c, y=body_top+row_h, w=col_w, h=row_h2` |
| H[0] | `x=Ox_c+col_w, y=body_top+row_h, w=col_w2, h=row_h2` |

**尺寸说明**：

- 布局 D 下 MAIN / 人类 **不再强制「画布 25%」**，而改为 **body 四分格**（约各 18%–22% 量级，随 Ha 变化）。  
- **同排同高**：顶排 H[1]/H[2] 同 `row_h`；底排 MAIN/H[0] 同 `row_h2`。  
- AI 仍为 `Wa×Ha`（约 6.25%），**禁止**为塞 3H 而放大 AI 高度。  
- 精简：人类宽 = 完整宽//2，左锚；高不变。  

### 2.4 精简模式（2H/3H）

- 与 UI 规范 §7 一致：宽 50%、高不变、左锚。  
- 多人类同时精简时，仍须保证 **不重叠**（实现可用更小默认或允许用户拖动；初始 plan 用完整尺寸）。  

---

## 3. 运行时架构（实现约束）

### 3.1 多 Human 代理

| 组件 | 要求 |
|------|------|
| `HumanPlayerProxy` | **每人类一座** 一实例；可共享 `window_plan` 字典 |
| `SeatUIHub` | 由 `human_seat` 改为 **`human_seats: list[int]`**；`mode_for(seat)`：seat∈human_seats → play，否则 watch |
| 子进程 | 每 play 座独立 `python -m players.seat_window --mode play` |
| Transport | 每座独立 NDJSON；ready / decision 带 `seat` |

### 3.2 Ready（F0004）

- **所有座位**（含 AI 观战窗）仍需确认开始（与现一致）。  
- 多人类：**任一人类未 ready 则不进入行牌**（与现 wait_all_ready 语义一致，仅 human 数量增加）。  

### 3.3 行牌阻塞

- 引擎仍按当前 `acting_seat` 请求决策。  
- 仅当 `acting_seat ∈ human_seats` 时阻塞对应 proxy；其它人类窗只收 observation（可操作 UI 禁用至轮到己方）。  

### 3.4 大厅 / focus

- `focus_seat`：默认第一个 human；可切换。  
- 主桌方位：仍以 `focus_seat` 或固定 S0 为「下」——**默认第一个 human 为视角锚点**（实现时写死并单测）。  

---

## 4. CLI 与验收命令（实现后）

```bash
# 2 人类 + 2 AI
.venv/bin/python main.py play --players human,human,rule_ai,rule_ai --theme green

# 3 人类 + 1 AI
.venv/bin/python main.py play --players human,human,human,rule_ai --theme green

# 非法
.venv/bin/python main.py play --players human,human,human,human  # 4H：本规格可不实现或仅警告
```

### 4.1 验收清单

| ID | 用例 | 期望 |
|----|------|------|
| T1 | 2H 启动 | 布局 B；2 play + 2 watch；MAIN 左下 |
| T2 | 3H 启动 | 布局 D；3 play + 1 watch；AI 顶带；MAIN 左下 body |
| T3 | 2H ready | 四窗都确认后开局 |
| T4 | 3H ready | 同上 |
| T5 | 2H 轮流 | 仅当前 human 座可提交 discard/response |
| T6 | plan 单元测 | `resolve_layout_mode(2,2)==B`，`(3,1)==D`；外框无重叠 |
| T7 | 回归 1H | 布局 A 行为与现网一致 |

---

## 5. 实现切片（已落地）

> 2026-07-28 回归修正：M09 `tests/test_human_wire.py` 的“最多 1 human”历史断言已更新为本规格的“2H/3H 允许，4H 拒绝”。

| 序 | 切片 | 内容 | 状态 |
|----|------|------|------|
| 1 | **Doc 合入** | UI 规范 v1.4 已含 B/D；本 F0020 Approved | Done |
| 2 | **Geom-D** | `plan_mode_D` + `resolve_layout_mode(3,1)` | Done |
| 3 | **Hub-MH** | `human_seats: list[int]`；多 play 生成 | Done |
| 4 | **App-MH** | `_human_seats` 全链路；多 transport attach | Done |
| 5 | **Proxy** | 多 human 注册与 attach_transport | Done |
| 6 | **Lobby** | 预设 2H/3H | Done（最小） |
| 7 | **Tests** | 几何 B/D + registry + hub mode_for | Done（单元） |

---

## 6. 风险

| 风险 | 缓解 |
|------|------|
| 3H 下 MAIN/人类变小，操作拥挤 | D 专用 body 四分；允许精简/拖动；最低分辨率写进 UI 规范 |
| 多进程 CPU | 已有 F0013 节流；3 play 更重，默认关闭预测 |
| 与「仅 1 human」测试冲突 | 单测拆分 1H/2H/3H |

---

## 7. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-26 | **Review** | 用户要求「更新 2/3 人类模式，先文档后代码」；本规格落盘；**不写代码** |
| 2026-07-26 | **Approved + Done** | 用户「确认并实现 F0020」：几何 D、Hub 多 human、app 多 attach、大厅 2H/3H、单元测 |
