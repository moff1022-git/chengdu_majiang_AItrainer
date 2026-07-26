# F0003 — 游戏封面 / 局后保窗 / 副露显示

| 字段 | 值 |
|------|-----|
| **编号** | F0003 |
| **标题** | Lobby cover + keep seat windows + meld display |
| **状态** | `Done` |
| **类型** | 功能增强 + 缺陷修复（UI / 引擎配置） |
| **依赖** | F0001、F0002、M02（换三张）、M07（Lobby） |
| **关联** | `display/app.py`、`lobby_view.py`、`player_view.py`、`engine/config.py`、`SeatUIHub` |

---

## 1. 背景与问题（用户反馈）

| # | 现象 | 期望 |
|---|------|------|
| P1 | 一轮结束后人类 + AI **玩家窗口全部消失** | 局结束仅结算；座位窗保持，可再开一局 |
| P2 | 玩家窗 **碰/杠副露不显示** | 本家与可见副露在座位窗绘制 |
| P3 | 主程序缺封面与局前设置 | 封面可设模式、是否换三张、轮数；**点击开始**才开局 |
| P4 | 窗口加载仍不稳定 | 保活/复用 Hub；缺座时再补启 |

---

## 2. 目标

| ID | 目标 |
|----|------|
| G1 | 对局结束 **不** 关闭座位子进程；仅 `game_end` + 主窗 Result |
| G2 | 再来一局 / 多轮：复用存活的 `SeatUIHub` 传输，避免整批杀进程 |
| G3 | `PlayerView` 绘制 `me.melds`（碰/明杠/暗杠/加杠） |
| G4 | Lobby 封面：游戏模式、换三张开关、轮数、主题；**Start 才 `_start_game`** |
| G5 | `EngineConfig.enable_exchange`；为 false 时跳过换三张 → 直接定缺 |
| G6 | `main.py human` / `play` 含 human 时默认 **不 auto_start**（进封面） |

---

## 3. 设计

### 3.1 生命周期

```
Lobby（封面，座位窗可已存在或尚未启动）
   │ 点击「开始」
   ▼
SeatUIHub.ensure_all()  — 缺则 spawn，活则复用
   │
   ▼
PlayerGameRunner(shutdown_players_on_end=False)
   │ 结束 → on_game_end + hub.send_game_end
   │        **不** pl.shutdown() 杀附着传输
   ▼
Result（座位窗仍在）
   │ 再来一局 → 复用 Hub
   │ 回大厅 → 可选保留 Hub；退出应用才 hub.shutdown
```

- `HumanPlayerProxy`：`attach_transport` 时 `_owns_transport=False`；`shutdown()` **仅**在 owns 时终止子进程。
- `PlayerGameRunner.shutdown_players_on_end`：live GUI 为 `False`。
- 应用退出 / 明确「关闭座位窗」时才 `hub.shutdown()`。

### 3.2 副露绘制

- 数据：`PlayerState.melds` / observation 中 `{"kind","tile_id"}`。
- 座位：`PlayerView` 手牌上方或弃牌旁画一组牌面；杠画 4 张同 id，碰画 3 张；标签 kind 简写。
- 主桌 `TableView` 已有 melds 绘制，保持。

### 3.3 封面 / AppConfig

| 字段 | 说明 | 默认 |
|------|------|------|
| `game_mode` | 展示用；当前仅 `blood_battle`（血战到底） | blood_battle |
| `players_spec` | 人类+3AI / 4AI 等预设可点切换 | 入参 |
| `enable_exchange` | 是否换三张 | True |
| `num_rounds` | 本会话目标轮数（1/2/4/8…） | 1 |
| `theme` | green/blue | green |

- 仅点击 **开始** 或 Lobby 上 Start 按钮开局（键盘 Enter 可保留为快捷开始）。
- 多轮：`round_index` 递增；Result 显示「第 r/N 局」；未满可再来一局；满则回大厅提示。

#### 3.3.1 「开始」按钮外观（2026-07-11）

| 项 | 规定 |
|----|------|
| 资源 | **不使用** `assets/buttons/btn_confirm_*.png` |
| 绘制 | 绿底圆角矩形 `(40,120,80)` + 描边 `(80,180,120)` + 白字「开  始」 |
| 实现 | `display/lobby_view.py` 实心 `pygame.draw.rect`，无 `assets.button("confirm")` |

### 3.4 引擎

```python
@dataclass(frozen=True)
class EngineConfig:
    ...
    enable_exchange: bool = True
```

- `opening.begin_dingque_skip_exchange` 或 orchestrator 分支：`dealt` → `dingque`（不写 exchange 日志）。
- InteractiveRunner / PlayerGameRunner / env 尊重该开关。

---

## 4. 验收

- [x] 一局结束后座位窗仍在（不发 shutdown）
- [x] 再来一局不强制杀掉再全启（复用存活 transport）
- [x] 有 melds 时座位窗可见碰杠牌
- [x] 封面可改模式/换三张/轮数；点开始才进 table
- [x] `enable_exchange=False` 测例跳过 exchange 相位
- [x] 单元测试通过

---

## 5. 实现文件

| 路径 | 变更 |
|------|------|
| `engine/config.py` | `enable_exchange` |
| `engine/opening.py` | skip exchange → dingque |
| `engine/orchestrator.py` | 开关 + `shutdown_players_on_end` |
| `display/lobby_view.py` | 封面控件 |
| `display/app.py` | 保窗、复用 Hub、局配置、rounds |
| `display/result_view.py` | 轮次文案 |
| `players/view/player_view.py` | melds |
| `players/human_proxy.py` | owns transport |
| `players/seat_ui_hub.py` | ensure_all / alive |
| `main.py` | human 默认 auto_start=False |
| `tests/` | config / meld draw / hub 语义 |

---

## 6. 修订记录

| 日期 | 内容 |
|------|------|
| 2026-07-10 | 初版 Done：封面 / 保窗 / 副露 |
| 2026-07-11 | §3.3.1：封面「开始」改为同色普通按钮，取消 `btn_confirm` 图资源 |
