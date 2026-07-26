# F0009 — 座位窗：选中牌高亮放大 + 当前打出牌面板

| 字段 | 值 |
|------|-----|
| **编号** | F0009 |
| **标题** | Seat window: stronger tile selection + current discard focus |
| **状态** | `Done` |
| **类型** | UI 增强 |
| **依赖** | F0002 座位窗、F0006 响应式手牌、公共 `last_discard` / `last_discard_seat` |
| **关联** | `players/seat_window.py`、`engine/state` 序列化字段 |
| **授权** | 用户需求：① 选中牌效果不够明显，需高亮+放大；② 新增当前打出牌显示并标明谁打出 |

---

## 1. 需求

| # | 说明 |
|---|------|
| R1 | 手牌（及换三张多选）**选中**态：明显 **高亮边框** + **牌面放大**（相对未选中约 +30% 宽，且至少 +10px） |
| R2 | 点选切换不整页闪烁（in-place 边框/底色；**不放大**牌面以免回流闪烁） |
| R3 | 座位窗新增 **「当前打出」** 区域：大号展示 `last_discard` 牌面 |
| R4 | 同步显示打出者：`本座 Sx 打出` / `S{n} 打出`；无当前弃牌时显示「暂无出牌」 |
| R4b | 同步显示该牌 **剩余张数**（及可见 x/4）：本家手牌 + 全员弃牌 + 副露，与 M08 remain 一致 |
| R4c | 同步显示本局 **牌墙总剩余**（`wall_remaining`） |
| R5 | play / watch 模式均显示当前打出面板（观战同样需要） |
| R6 | 不改引擎规则；仅消费 observation 中已有公共字段 |

### Out of Scope

- 主窗同步改造（主桌已有弃牌区）  
- 动画帧序列 / 音效  
- 响应阶段高亮「可碰杠胡」目标牌（可后续功能）  

---

## 2. 方案

### 2.1 选中特效

- 基准宽 `base_tw`（布局 `compute_tile_grid` 结果）  
- 选中宽 `sel_tw = max(base_tw + 10, round(base_tw * 1.32))` 并偶数对齐（复用 photo cache）  
- 样式：金黄粗边框 `highlightthickness≥3`、`bg` 深金/亮绿、`relief=raised`、略增 `padx`  
- `_apply_hand_selection_styles`：对 `_hand_tile_widgets` 换 `image` 尺寸 + 样式，避免 destroy  

### 2.2 当前打出面板

位置：分数行 / 自胡横幅之下、对手 HUD 之上（滚动区顶部易见）。

| 元素 | 内容 |
|------|------|
| 标题 | 当前打出 |
| 牌面 | `last_discard`，约 56–72px 宽 |
| 文案 | 由 `format_discard_actor(seat, self_seat)` 生成 |

字段来源：`view["last_discard"]`、`view["last_discard_seat"]`（`to_dict` 已有，filter 保留）。

每次 `_render_state` **始终**刷新该面板（不依赖手牌 fingerprint 是否跳过重建）。

### 2.3 辅助纯函数（可测）

```python
def selected_tile_tw(base_tw: int) -> int: ...
def format_discard_actor(discard_seat, self_seat) -> str: ...
```

---

## 3. 文件清单

| 路径 | 变更 |
|------|------|
| `docs/features/F0009_seat_select_current_discard.md` | 本规格 |
| `players/seat_window.py` | 选中放大 + 当前打出面板 |
| `tests/test_seat_ui.py` | helpers 单测 |
| `docs/changelog.md` / README 索引 | 回写 |

---

## 4. 验收

- [x] 点选手牌：明显变大 + 金黄高亮；再点取消恢复  
- [x] 换三张多选：已选最多 3 张均放大高亮  
- [x] 有人出牌后，各座位窗「当前打出」显示该牌 + 打出者座位  
- [x] 本家出牌显示「本座 … 打出」  
- [x] pytest 相关通过  

---

## 5. 实现记录

| 日期 | 内容 |
|------|------|
| 2026-07-10 | `selected_tile_tw` / `format_discard_actor`；`_apply_hand_selection_styles` 换大图+金边；`play_panel` 当前打出；测试 |
| 2026-07-10 | 当前打出增加 `remain_of_tile_from_view` / `剩余 r 张 (可见 s/4)` |
| 2026-07-10 | 当前打出增加 `format_wall_remaining_line`（牌墙总剩余）；此牌剩余文案区分 |
