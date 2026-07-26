# F0004 — 座位窗每局开始确认

| 字段 | 值 |
|------|-----|
| **编号** | F0004 |
| **标题** | Per-seat ready confirm + auto-start checkbox |
| **状态** | `Done` |
| **类型** | 功能增强（UI / 协议） |
| **依赖** | F0002 座位窗、F0003 保窗与多轮 |
| **关联** | `players/seat_window.py`、`SeatUIHub`、`protocols/wire.py`、`display/app.py` |

---

## 1. 需求

| # | 说明 |
|---|------|
| R1 | **每轮**对局真正开局前，**每个座位窗**（人类 play + **AI watch**）须手动点「确认开始」；AI 座**默认不**自动确认 |
| R2 | 各座位窗提供 **「自动开始」复选框**：勾选后本窗收到开始请求时自动确认（跨局保存在进程内；人类/AI 默认均为未勾选） |
| R3 | 主进程 **收齐全部存活座位** 的 ready 后，才启动引擎发牌/换三张 |
| R4 | **GUI 含 4AI**：同样开 4 个 AI watch 座位窗，各窗确认后才开局；仅 **headless** / 显式无座位路径跳过本流程 |

---

## 2. 协议（NDJSON）

### 主 → 子：`ready_request`

```json
{
  "type": "ready_request",
  "round": 1,
  "game_id": "human-…",
  "num_players": 4,
  "num_rounds": 4
}
```

- `num_rounds`：会话总局数（座位窗显示「第 r/n 局」）；缺省按 1。

### 子 → 主：`ready`

```json
{
  "type": "ready",
  "seat": 0,
  "auto": false
}
```

- `auto=true` 表示由「自动开始」勾选触发。  
- 超时：默认与 human 超时同量级（如 10 分钟）；超时则本局失败/回大厅并写日志。

### 主 → 子：`set_geometry`（2026-07-11）

```json
{
  "type": "set_geometry",
  "x": 8,
  "y": 36,
  "w": 629,
  "h": 514
}
```

- 父进程在布局 plan 确定/变更后推送；座位 Tk 应用 `format_tk_geometry`（负 Y 见 F0001 §13.3）。

### 子 → 主：`seat_settings`（设置条）

```json
{
  "type": "seat_settings",
  "seat": 1,
  "auto_start": true,
  "ai_type": "rule_ai"
}
```

- `ai_type`：仅 watch 座；`rule_ai` | `random`；**下局** `compose_players_spec` 生效。  
- ready 等待期间 transport 须 **保留** settings 行，不得丢弃（`request_ready` 结束后 requeue）。

---

## 3. 流程

```
主程序点击「开始」/「再来一局」
        │
        ▼
主线程: detect_screen → plan → pin 主窗
        │
        ▼
后台线程: SeatUIHub.ensure_all / start_all
        │  （reassert 座位 only，禁止 set_mode 主窗）
        ▼
hub.wait_all_ready(round)   # _ready_wait_active=True，禁止 poll 抢 ready
        │  并行: 每座 transport.request_ready()
        ▼  各座 UI 确认（或 auto ready）
        ▼  全部 ready
effective_spec = hub.compose_players_spec(...)  # 勿赋值局部 players_spec
PlayerGameRunner.run()
```

- 局间：`game_end` 后座位窗仍在；下一局再次 `ready_request`。  
- 「自动开始」状态 **按窗口进程记忆**，不写盘（本会话有效）。  
- **顺序**：先 ready，**再** `create_players` / 引擎（避免 4AI 白屏与消息竞态）。  
- 引擎线程内对局错误：主窗 **留在 table** 显示错误，不静默回封面。

---

## 4. UI（座位窗）

| 控件 | 行为 |
|------|------|
| 文案 | 「第 N 局 — 请确认开始」 |
| 按钮「确认开始」 | 发送 `ready`，关闭确认层 |
| **设置条（常显）** | 「自动开始：开/关」；AI 座「规则AI / 随机AI」高对比按钮 |
| 可选「更多…」 | 展开说明文案 |
| 适用范围 | play 与 watch 均可点（AI 窗也要人确认） |

主程序状态栏：`等待座位确认 S0,S1…` → `已确认，开局中…`

---

## 5. 验收

- [x] 每局开局前 human + AI 座位窗出现确认 UI  
- [x] 未全员确认前引擎不发牌（无无 observation 进入 exchange/dingque）  
- [x] 勾选自动开始后下一局同窗自动 ready  
- [x] 协议单元测试；全量 pytest 绿  
- [x] 2026-07-11：设置条常显；ready 等待不丢 `seat_settings`；`effective_spec` 无 UnboundLocalError  

---

## 6. 实现文件

| 路径 | 变更 |
|------|------|
| `protocols/wire.py` | `msg_ready_request` / `msg_ready` / `msg_set_geometry` / `msg_seat_settings` |
| `protocols/subprocess_transport.py` | `request_ready` / `send_set_geometry`；ready 中 requeue settings |
| `players/seat_ui_hub.py` | `wait_all_ready`、`_ready_wait_active`、`compose_players_spec`、`apply_window_plan` |
| `players/seat_window.py` | 确认层 + 设置条 + `set_geometry` |
| `display/app.py` | 引擎前 ready；`effective_spec`；主线程 pin |
| `tests/test_f0004_ready.py` | 协议与 UI 冒烟 |

---

## 7. 修订记录

| 日期 | 内容 |
|------|------|
| 2026-07-10 | 初版 Done：ready 协议 + 确认 UI |
| 2026-07-11 | 4AI 先 ready 后引擎；poll 禁抢；设置条/`seat_settings`；`set_geometry`；`effective_spec` |
