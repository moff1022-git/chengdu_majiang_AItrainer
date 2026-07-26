# F0013 — 座位窗脏更新 / 控件复用（减闪 · 减负）

| 字段 | 值 |
|------|-----|
| **编号** | F0013 |
| **标题** | Seat window dirty update + widget reuse (anti-flicker) |
| **状态** | `Done` |
| **类型** | 性能 / UI 渲染增强 |
| **依赖** | F0002 座位窗、F0006 响应式、F0012 推荐标记 |
| **平台** | **Windows + macOS 同源逻辑**；禁止 Win-only 破坏负坐标/Tk 语义 |

---

## 1. 背景与动机

轻薄本（如 i5 核显）上完整 UI 为「主进程 pygame + 4× Tk 子进程 + 逐步 NDJSON 广播」。  
座位窗在手牌/弃牌变化时 **destroy + pack 重建**，导致：

- 明显闪烁 / 「整行刷新」感  
- CPU 被控件重建与 4 路 observation 放大  

方案 **B**（见会话分析）：**脏更新 + 控件复用 + 广播节流**，不改引擎规则、不改 mac 几何协议。

---

## 2. 目标

| ID | 目标 |
|----|------|
| G1 | 手牌条在 **张数与布局参数不变** 时，仅 `config` 牌面/选中样式，不 destroy 整行 |
| G2 | 弃牌条在 **布局参数不变** 时同上（仅更新 tid 列表） |
| G3 | 副露 `meld_key` 不变时不重建副露区 |
| G4 | observation 高频到达时 debounce ≥ 80ms（已有）且 **全量重建路径显著减少** |
| G5 | Hub `broadcast`：**内容签名相同则跳过**；另设最小间隔（默认 60ms），**不阻塞** `action_request` / ready 协议 |
| G6 | Win/Mac 共用代码路径；mac 负坐标 / set_geometry / 字体 families 扫描等 **不回退** |

---

## 3. 范围

### 3.1 In Scope

- `players/seat_window.py`：手牌 / 弃牌 / 副露 脏更新与控件池  
- `players/seat_ui_hub.py`：`broadcast` 节流与签名  
- 单元测试：指纹、控件池更新逻辑（dummy Tk 或无 GUI 纯函数）  
- 文档：本规格、features README、changelog  

### 3.2 Out of Scope

- 取消多进程座位窗 / 改 Canvas 整帧（方案 C/D）  
- 引擎规则、计分、F0010 算法  
- 主桌 pygame 渲染重构  

---

## 4. 设计

### 4.1 手牌控件池

- 首次（或 `layout_key` 变化时）走现有 `_pack_tiles_wrapped` 建池。  
- `layout_key = (n, tw, per_row, recommend_on, reserve_uke)`  
- 若 `layout_key` 与池一致且 `len(hand)==n`：  
  - 对每个 index：`_update_tile_face(label, tid, selected, tw)`  
  - 更新 `_hand_tile_widgets` / `_hand_cell_by_tid` 元数据  
  - 调用既有 `_update_ukeire_overlays` / `_apply_hand_selection_styles`  
- `layout_key` 变化（含张数变、列数变、tw 变）：**一次** clear + rebuild（与今相同）。

### 4.2 弃牌 / 副露

- 弃牌：`disc_layout_key = (len(discs), disc_tw, disc_per)`；一致则只更新 face。  
- 副露：`meld_key` 与上次相同则 **不** `_clear(meld_fr)`；变化才重建。

### 4.3 `_render_state` 分层

```
refresh chrome / score / current discard panel (in-place labels)
maybe_refresh_predict
compute grids + fingerprints
if not force:
  try hand inplace
  try disc inplace  
  try skip melds if meld_key same
  opp hud inplace / rebuild as today
  rebuild action bar if fingerprint changed
  return early when all strips handled
else full rebuild path (legacy)
```

### 4.4 Broadcast 节流（Hub）

```python
# per broadcast call
sig = (phase, turn_index, wall_len, last_discard_id, last_discard_seat,
       scores_tuple, hands_len_tuple, melds_lens, discard_seq)
if sig == last_sig and (now - last_t) < min_interval_s:
    return  # skip all seats
last_sig, last_t = sig, now
# then existing per-seat send_observation
```

- `min_interval_s` 默认 **0.06**（约 16Hz 上限）。  
- **不得**节流：`request_ready` / `request_decision` / `send_game_end`。  
- 签名变化（如有人出牌）**立即**广播，不受间隔阻塞。

### 4.5 平台兼容

| 项 | 策略 |
|----|------|
| macOS | 不改负坐标、不改 stdin/Tk 顺序、不改字体 families 扫描 |
| Windows | 沿用现有 unlock chrome / 仅主 HWND 置位；脏更新为共享逻辑 |
| Tk 8.6 | 仅用 `Label.configure(image=..., text=..., bg=...)` 等通用 API |

---

## 5. 文件清单

| 路径 | 变更 |
|------|------|
| `docs/features/F0013_seat_dirty_update.md` | 本规格 |
| `docs/features/README.md` | 索引 |
| `docs/changelog.md` | 实现摘要 |
| `players/seat_window.py` | 脏更新 / 控件池 |
| `players/seat_ui_hub.py` | broadcast 签名 + 节流 |
| `tests/test_f0013_dirty_update.py` | 指纹与节流单测 |

---

## 6. 测试计划

- `test_tiles_fingerprint_excludes_opp_scores`（若已有则扩展）  
- `test_hand_inplace_updates_tid_without_new_widget`（dummy Tk：同一 Label 实例）  
- `test_broadcast_skips_identical_sig` / `test_broadcast_sends_on_sig_change`  
- 现有 `test_seat_ui` / `test_f0004` 不回归  

---

## 7. 验收

- [x] 布局参数不变时手牌/弃牌走 `_try_inplace_*`（控件实例保留）  
- [x] 副露 `meld_key` 不变时跳过副露 rebuild  
- [x] Hub broadcast：相同签名 + 最小间隔跳过  
- [x] 换三张选牌 / 双击出牌路径保留（selection in-place + bind）  
- [x] 平台：逻辑共享；Win clamp/sanitize 与 mac 路径隔离未回退  
- [x] `tests/test_f0013_dirty_update.py` 通过

---

## 8. 回滚

- 恢复 `_render_state` 全量 clear 路径；去掉 hub 节流字段即可。  
- 规格状态回 `Cancelled` 或保留文档作历史。  

---

## 9. 风险

| 风险 | 缓解 |
|------|------|
| 控件池与 ukeire overlay 不同步 | inplace 后强制 `_update_ukeire_overlays` |
| 节流导致 UI 略延迟 | 仅相同签名节流；签名变立即发 |
| 池与 layout 不一致 | layout_key 变化必 rebuild |
