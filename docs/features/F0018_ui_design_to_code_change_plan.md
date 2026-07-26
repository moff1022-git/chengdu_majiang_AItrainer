# F0018 — UI 设计文档 → 程序修改计划

| 字段 | 值 |
|------|-----|
| **编号** | F0018 |
| **标题** | Map 4 UI design docs to code changes (implementation plan) |
| **状态** | **`Done`**（2026-07-21 实现 P0–P8） |
| **类型** | 程序修改 / 实现计划（**布局与 UI 呈现**） |
| **依赖** | 四份 UI 设计（下表）；F0001/F0005/F0007 既有实现 |
| **权威设计** | 见 §1 关联表 |
| **实现** | P0–P8 已落地；见 `docs/status/LATEST.md` / changelog |
| **范围定性** | **不是改玩法/规则功能**，而是 **调整布局与 UI 呈现**（见 §0） |

---

## 0. 范围边界（强制 · 布局/UI vs 功能）

### 0.1 本次任务 **是**

| 类别 | 内容 |
|------|------|
| **窗口几何** | 多窗 A/B/C 落位、85% 画布、25%/6.25% 外框、精简宽 50% |
| **分区骨架** | 主窗 80/20、侧栏上中下；座位窗 67/33、折叠；玩家区条带顺序与行高 |
| **控件搬迁** | 把**已有**能力（手牌、副露、弃牌、碰杠胡过、设置开关、对手 HUD、推荐角标、进张、就绪确认等）放进新分区 |
| **呈现增强** | 用现有状态/事件 **展示** 出牌日志、AI 操作日志（不新增引擎规则） |
| **资源** | 继续只用项目 **`assets/`** 画 UI |

### 0.2 本次任务 **不是**（禁止当成本次范围）

| 类别 | 说明 |
|------|------|
| **麻将规则 / 计分 / 血战流程** | 不改 engine 规则语义 |
| **AI 决策策略** | 不改 rule_ai / F0010–F0011 算法目标（仅 UI 展示与落位） |
| **合法动作集合** | 碰杠胡过仍由引擎/协议给出；UI 只负责显示与点击提交 |
| **新玩法功能** | 不新增换三张规则、番型、人数规则等 |
| **协议语义重做** | 可增 **展示用** 日志字段/缓冲；不借机改 action 语义 |

### 0.3 与「已有功能」的关系

| 已有能力 | 本次做法 |
|----------|----------|
| F0004 就绪确认 | **保留**，改放置区域 |
| F0012 推荐/进张 | **保留**，迁入新 OP_PLAY |
| F0013 脏更新 | **保留**，适配新控件树 |
| F0007 主桌明牌/HUD 开关 | **保留**，迁到 SIDE 中部 |
| 主窗/AI「日志」 | **展示层**：聚合已有 observation/state 变化，**非**新玩法 |

> **一句话**：改的是 **怎么摆、怎么看**；不是 **怎么打牌、怎么算分**。

---

## 1. 四份 UI 设计与程序文档关联

| # | UI 设计文档 | 状态 | 关联功能规格 | 程序域 | 职责边界 |
|---|-------------|------|--------------|--------|----------|
| D1 | [`docs/design/UI_DESIGN_STANDARD.md`](../design/UI_DESIGN_STANDARD.md) | 示意图已确认 | （几何权威；无单独 F） | **多窗外框** | 屏上 MAIN + 座位窗 **位置/尺寸**（85% 画布、A/B/C、25%/6.25%） |
| D2 | [`docs/design/MAIN_WINDOW_LAYOUT.md`](../design/MAIN_WINDOW_LAYOUT.md) | 已确认 v0.2 | [F0015](F0015_main_window_interior_layout.md) **Approved 设计** | **主窗内部** | 客户区 80/20、DICE、四扇区条带、侧栏三区 |
| D3 | [`docs/design/HUMAN_WINDOW_LAYOUT.md`](../design/HUMAN_WINDOW_LAYOUT.md) | 已确认 | [F0016](F0016_human_window_interior_layout.md) **Approved 设计** | **人类座位窗内部** | play：67/33、折叠、操作四段 |
| D4 | [`docs/design/AI_WINDOW_LAYOUT.md`](../design/AI_WINDOW_LAYOUT.md) | 已确认 | [F0017](F0017_ai_window_interior_layout.md) **Approved 设计** | **AI 座位窗内部** | watch：同构分栏、无操作条、日志+弃牌 |

### 1.1 与既有程序/规格文档

| 既有文档/模块 | 与 UI 设计关系 | 修改策略 |
|---------------|----------------|----------|
| `PLAN.md` §显示 | 总架构 | 实现后回写「多窗几何 v1.3 + 三窗内部」摘要 |
| F0001 窗口几何 | 工作区检测、旧网格 | **扩展** `window_geometry`：新 plan_mode_A/B/C，不删检测 API |
| F0005 Win/Mac | 平台约束 | 遵守；新 plan 仍隔离 win32 HWND |
| F0007 主桌面板 | 旧主窗布局 | **迁移/替换** 为 D2；F0007 标 Superseded-by F0015 或修订 Done 注记 |
| F0012/F0013/F0014 | 推荐、脏更新、元素 | **保留能力**，迁入新分区骨架 |
| `assets/ASSETS.md` | 牌/按钮/骰子 | **唯一图形资源库**；主窗/座位窗必须从仓库根目录 `assets/` 加载（见 §1.3） |

### 1.2 文档依赖方向

```text
UI_DESIGN_STANDARD (D1 外框)
        │
        ├── MAIN_WINDOW_LAYOUT (D2)  ←── F0015
        ├── HUMAN_WINDOW_LAYOUT (D3) ←── F0016
        └── AI_WINDOW_LAYOUT (D4)    ←── F0017
                    │
                    ▼
         F0018 本程序修改计划（切片 / 文件 / 验收）
                    │
                    ▼
              业务代码 + 测试
```

冲突时：**已确认 UI 设计 > 本计划 > 旧 F0007 布局描述**。

### 1.3 程序资源库（强制）

| 项 | 约定 |
|----|------|
| **唯一资源根目录** | 仓库根下 **`assets/`**（与 `assets/ASSETS.md` 契约一致） |
| **主程序（pygame）** | `display/asset_manager.py`：`_DEFAULT_ASSETS = <project_root>/assets`；`AssetManager(root=None)` 即用此目录 |
| **座位窗（Tk）** | 牌面/主题资源相对 **`assets/`** 解析（不得改指向其它资源树） |
| **主题** | `green` / `blue` 后缀，见 ASSETS.md |
| **禁止** | 从包外绝对路径、网络 URL、或第二套平行资源目录加载运行时 UI 图（测试 mock 除外） |

**确认（代码事实）**：`AssetManager` 默认根为 `Path(__file__).parent.parent / "assets"`，即项目目录 **`assets/`**。UI 改造（F0015–17）与示意脚本均须继续遵守。

---

## 2. 现状程序 vs 设计（缺口摘要）

详见此前对照；本计划只列 **必须改** 点。

| 设计 | 现状程序 | 必须修改 |
|------|----------|----------|
| D1 85% 画布 + A/B/C 固定比例 | `compute_window_plan` 2×3 网格 | 重写/新增 plan 函数 |
| D2 80/20 + DICE + 四角扇区 + 弃/副露/手条带 | `layout.py` band + 固定宽面板 | 重写主桌几何与绘制 |
| D2 SIDE 上积分/中开关/下日志 | 控制面板几乎满栏、无日志 | 侧栏三区 + 日志数据源 |
| D3 67/33 + 折叠 | `seat_window` 纵向 pack | play 骨架重构 |
| D4 同构无操作条 + AI 日志 | watch 共用纵向栈，无日志 UI | watch 骨架 + 日志通道 |

---

## 3. 程序修改清单（按文件）

### 3.1 D1 — 多窗外框（UI_DESIGN_STANDARD）

| 文件 | 动作 | 说明 |
|------|------|------|
| `display/window_geometry.py` | **改** | 新增 `layout_canvas(W,H)`、`window_sizes(Lw,Lh)`、`plan_mode_A/B/C`；保留 `detect_screen` / sanitize；旧 `compute_window_plan` 网格可保留兼容或委托新 plan |
| `players/seat_ui_hub.py` | **改** | 启动/重置用新 plan；按 n_human/n_ai 选 A/B/C；`set_geometry` |
| `display/app.py` | **改** | MAIN 矩形用 plan.main；resize 可选重 plan / 仅重置时应用 |
| `players/human_proxy.py` | **改** | 注入 CLI 几何来自新 plan |
| `tests/test_window_geometry.py` | **改/增** | 85% 面积比、三档 px、A/B/C 不重叠、>2160p 封顶 |

### 3.2 D2 — 主窗内部（MAIN_WINDOW_LAYOUT / F0015）

| 文件 | 动作 | 说明 |
|------|------|------|
| `display/layout.py` | **改** | `MainInteriorLayout`：TABLE 80%、SIDE 20%、DICE 方区、四扇区多边形/包围盒、每区 ZONE_HAND/MELD/DISC 厚度（1 行/2 行/剩余） |
| `display/table_view.py` | **改** | 按新几何绘制四家；条带顺序从里到外弃→副露→手 |
| `display/control_panel.py` | **改** 或拆 | 改为 SIDE 中部；高度 30% 预算；保留折叠可选 |
| **新** `display/side_scoreboard.py`（建议） | **增** | SIDE_TOP 四家状态积分 |
| **新** `display/play_log_panel.py`（建议） | **增** | SIDE_BOT 出牌日志 UI |
| `display/app.py` | **改** | 组装三区；从 **现有** state/回调 **展示** 日志（不改引擎规则） |
| live / 状态回调 | **轻改** | 仅把已发生的动作 **格式化进 UI 缓冲**；禁止改 action 合法性或计分 |
| `tests/test_table_layout.py` | **改/增** | 80/20、DICE 同心、条带厚度 |

### 3.3 D3 — 人类窗内部（HUMAN_WINDOW_LAYOUT / F0016）

| 文件 | 动作 | 说明 |
|------|------|------|
| `players/seat_window.py` | **大改** | play 路径：左右 67/33；OP 四段；EXT 上 HUD 30% 下弃牌 70%；折叠状态机 |
| `players/view/responsive.py` | **复用** | 手牌/弃牌换行算法不变，改父容器与可用宽 |
| F0012/F0013 逻辑 | **迁** | 推荐角标、ukeire、脏更新挂到新 OP_PLAY / 不毁折叠 |
| `tests/test_f0013_*.py` / seat UI | **改** | 适配新控件树；增折叠与比例测 |

### 3.4 D4 — AI 窗内部（AI_WINDOW_LAYOUT / F0017）

| 文件 | 动作 | 说明 |
|------|------|------|
| `players/seat_window.py` | **改** | watch 与 play **分布局构建**；无操作条；EXT 上 **AI 日志** 非对手 HUD |
| 协议 / hub | **可选轻改** | 日志优先 **observation 差分**（零协议变更）；仅当不足时再增展示字段 |
| `tests/` | **增** | watch 无 hit 出牌；有日志区 |

### 3.5 共享 / 文档回写

| 文件 | 动作 |
|------|------|
| `docs/features/F0007_*.md` | 注：主桌内部分区 **由 F0015 取代**（布局） |
| `docs/features/README.md` | F0018 索引 |
| `docs/changelog.md` | 实现交付时追加 |
| `PLAN.md` | 实现后短更显示架构 |

---

## 4. 建议新增模块（可选但推荐）

| 模块 | 职责 |
|------|------|
| `display/main_interior.py` | 主窗 TABLE/SIDE/DICE/扇区纯几何 |
| `display/play_event_log.py` | 主进程出牌日志环形缓冲 |
| `players/seat_layout_play.py` | play 窗几何常量与分区计算 |
| `players/seat_layout_watch.py` | watch 窗几何（可与 play 共享 67/33 基类） |

避免继续把全部几何塞进 4k 行 `seat_window.py`。

---

## 5. 实现切片（推荐顺序）

| 切片 ID | 内容 | 设计 | 产出 | 验收要点 |
|---------|------|------|------|----------|
| **P0** | 几何库：画布 85% + sizes + plan A/B/C | D1 | `window_geometry` + 单测 | 三档 px、不重叠 |
| **P1** | Hub/App 应用新 plan | D1 | 启动落位正确 | 人工 1080p A/B/C |
| **P2** | 主窗 80/20 + SIDE 三区骨架 | D2 | layout + app 壳 | 比例单测 |
| **P3** | 主窗 DICE + 四扇区 + 弃/副露/手条带 | D2 | table_view | 从里到外顺序 |
| **P4** | 主窗出牌日志数据 + UI | D2 | play_log_panel | 有事件滚动 |
| **P5** | 人类窗 67/33 + 折叠 + 四段 OP | D3 | seat_window play | 折叠/比例 |
| **P6** | 人类迁入操作/推荐/进张/设置 | D3 | 同左 | 不丢 F0012 等 |
| **P7** | AI 窗骨架 + 无操作条 + 日志 | D4 | seat_window watch | 与 D3 分栏一致 |
| **P8** | 回归 + 文档 Done | 全部 | 测试绿 / changelog | F0015–18 状态 |

**建议触发语**：`实现 F0018-P0` … 或 `实现布局几何`（P0+P1）、`实现 F0015`（P2–P4）、`实现 F0016`（P5–P6）、`实现 F0017`（P7）。

---

## 6. 数据流修改点

```text
引擎状态变化
    │
    ├─► App / TableView          （主桌重绘 + 写 play_event_log）
    ├─► SeatUIHub.broadcast      （observation → 各座位窗）
    │         │
    │         ├─ play seat_window  （人类：手牌可点、操作条）
    │         └─ watch seat_window （AI：只读；append 本座日志）
    └─► （可选）专用 log NDJSON  type=seat_log
```

| 需求 | 建议数据源 |
|------|------------|
| 主窗 SIDE 日志 | 主进程在 `on_state` / action 提交处 append |
| AI 窗 EXT 日志 | 子进程根据 observation 差分（手牌/弃牌变化）生成行；或主进程下发 |

---

## 7. 测试计划

| 层级 | 内容 |
|------|------|
| 单测 | 画布 85%；A/B/C 矩形；主窗 80/20；DICE 同心；扇区条带 1+2 行；座位 67/33 |
| 组件 | play 折叠；watch 无 decision 按钮（就绪除外） |
| 手工 | 1080p 布局 A 开局；扩展折叠；主窗日志有出牌 |

---

## 8. 风险与缓解

| 风险 | 缓解 |
|------|------|
| `seat_window.py` 过大难改 | 先抽 layout 纯函数，再改 pack 树 |
| AI 外框 6.25% 过小装不下内部设计 | 实现时：完整模式 AI 可用最小可读下限放大，或仅 A 布局人类大窗优先；**若破 6.25% 须先改 UI_DESIGN_STANDARD** |
| 主窗四角射线难绘制 | 先用扇区 AABB + 条带，射线作可选装饰 |
| 日志性能 | 环形缓冲 + UI 节流 |

---

## 9. 验收总表（F0018 Done 条件）

- [x] D1：plan A/B/C 与 §8 三档表一致；示意图尺寸可对上  
- [x] D2：主窗 80/20、DICE、四区从里到外弃/副露/手、SIDE 三区含日志  
- [x] D3：人类 67/33 可折叠、OP 四段、EXT HUD+弃牌  
- [x] D4：AI 同构、EXT 日志+弃牌（watch 底栏仅就绪/决策条路径保留兼容）  
- [x] 相关单测通过；changelog 实现条目；F0015–17 实现状态更新  
- [ ] 可选：1080p 目视 A/B/C；macOS 抽检  

---

## 10. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 初稿：关联四设计 + 文件级修改 + P0–P8 切片 |
| 2026-07-21 | **§1.3 确认**：程序图形资源库 = 仓库 **`assets/`**（AssetManager 默认根） |
| 2026-07-21 | **§0 范围边界**：本次 = **布局与 UI**，**非**改玩法/规则/AI 决策功能 |
| 2026-07-21 | **用户确认 / 状态 → `Approved`**；实现前完整备份 `backup/2026-07-21/`（2520 文件）；**仍不写业务代码**直至用户明确「实现」 |
| 2026-07-21 | **实现 Done**：P0–P8 落地（外框 A/B/C、主窗 80/20+条带+日志、座位 67/33+折叠/AI 日志）；单测 `tests/test_f0018_layout_geometry.py` 等 |
