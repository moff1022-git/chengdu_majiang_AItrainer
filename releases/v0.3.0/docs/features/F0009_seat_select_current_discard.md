# F0009 — 座位窗：选中牌高亮 + 当前打出牌面板

| 字段 | 值 |
|------|-----|
| **编号** | F0009 |
| **标题** | Seat window: tile selection highlight + current discard focus |
| **状态** | `Done` |
| **类型** | UI 增强 |
| **依赖** | F0002 座位窗、F0006 响应式手牌、公共 `last_discard` / `last_discard_seat` |
| **关联** | `players/seat_window.py`、`engine/state` 序列化字段 |
| **授权** | 用户需求：① 选中牌效果更明显；② 当前打出牌面板 |
| **实装偏差（以代码为准）** | **不放大牌面**（`selected_tile_tw` 保持 base 宽，防回流闪烁）；用 **金框 + 暖底 + 未选压暗** 表现选中（2026-07 加固） |

---

## 1. 需求

| # | 说明 |
|---|------|
| R1 | 手牌（及换三张多选）**选中**态：明显 **高亮边框**（原案曾含放大；见 R2 / 实装偏差） |
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

### 2.1 选中特效（实装）

- 基准宽 `base_tw`；**`selected_tile_tw(base) == base`（偶数对齐）— 不放大**  
- 固定 chrome：`ht=2` 牌面环 + `face_hold` 外环；选中金黄 `#ffeb3b`，未选与桌面同色  
- 有选中时其余手牌略压暗  
- `_apply_hand_selection_styles`：仅改边框/底色，避免 destroy / 回流  

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
| `players/seat_window.py` | 选中金框/高亮 + 当前打出面板 |
| `tests/test_seat_ui.py` | helpers 单测 |
| `docs/changelog.md` / README 索引 | 回写 |

---

## 4. 验收

- [x] 点选手牌：**金黄边框/高亮**（不放大）；再点取消恢复  
- [x] 换三张多选：已选最多 3 张均高亮  
- [x] 有人出牌后，各座位窗「当前打出」显示该牌 + 打出者座位  
- [x] 本家出牌显示「本座 … 打出」  
- [x] pytest 相关通过  

---

## 5. 实现记录

| 日期 | 内容 |
|------|------|
| 2026-07-10 | `selected_tile_tw` / `format_discard_actor`；选中样式；`play_panel` 当前打出；测试 |
| 2026-07-10 | 当前打出增加 `remain_of_tile_from_view` / `剩余 r 张 (可见 s/4)` |
| 2026-07-10 | 当前打出增加 `format_wall_remaining_line`（牌墙总剩余）；此牌剩余文案区分 |
| 2026-07-26 | **冻结不放大**；金双环 + 未选压暗；文档与代码对齐（一致性审计） |

