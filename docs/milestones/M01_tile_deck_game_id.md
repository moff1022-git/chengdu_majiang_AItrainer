# M01 — 牌、牌墙、game_id、掷骰定庄、状态序列化

| 字段 | 值 |
|------|-----|
| **编号** | M01 |
| **标题** | Tile / Deck / GameId / Dice Dealer / State (deal snapshot) |
| **状态** | `Done` |
| **依赖** | 无（首个里程碑）；基线：`PLAN.md`、`docs/DEVELOPMENT.md` |
| **下一里程碑** | M02（换三张 + 定缺阶段状态机） |
| **对应 PLAN** | §2.1–2.3 开局前半、§3.1–3.2、§6.4、§11 M1 |

---

## 1. 目标

建立引擎最底层的**可复现发牌底座**，使后续血战状态机、玩家模块、训练环境都能依赖统一约定：

1. 用标准类型表示成都麻将 108 张牌（万/筒/条，无字牌）。  
2. 由 **独立 `game_id`** 确定性派生全部引擎随机源（洗牌、掷骰），保证同 ID 可复盘。  
3. 实现 **双骰定庄**（逻辑层；本步不做 Pygame 渲染，但输出可对接 `assets/dice` 的点数）。  
4. 实现洗牌与按座位发牌（各 13 张，庄家再摸 1 成 14）。  
5. 提供 **可 JSON 序列化/反序列化** 的开局快照（至少覆盖：game_id、种子、骰点、庄家、各家手牌、牌墙剩余），供存档与测试断言。

本步**不**实现行牌、碰杠胡、换三张、定缺决策流程、UI、玩家接口。

---

## 2. 范围

### 2.1 In Scope

| 项 | 说明 |
|----|------|
| `engine/tile.py` | `Suit`、`Tile`、全量牌表、字符串 ID（`wan_3`） |
| `engine/game_id.py` | 生成/规范化 `game_id`；`master_seed`；`shuffle_seed` / `dice_seed`（及预留 `exchange_seed`） |
| `engine/deck.py` | 108 张构建、Fisher–Yates 洗牌、发牌、摸牌指针 |
| `engine/dice.py` | 双骰点数（1–6×2）、点数和、由 `dice_seed` 派生、庄家座位计算 |
| `engine/state.py` | M01 所需最小状态结构 + `to_dict` / `from_dict` |
| `engine/config.py` | 最小配置：`num_players ∈ {2,3,4}`、`initial_score`（可选默认 0） |
| `engine/deal.py` 或函数集合 | 「给定 game_id + config → DealResult / GameState」一站式开局 |
| 包初始化 | `engine/__init__.py` 导出公开 API |
| 依赖声明 | `requirements.txt`：至少 `pytest`（本步可不强依赖 pygame/numpy，但可写入预留） |
| 单元测试 | 见 §7 |

### 2.2 Out of Scope（明确不做）

- 换三张、定缺、行牌、合法动作、血战、计分、番型、向听  
- Pygame / AssetManager / 骰子动画 UI  
- `players/`、`protocols/`、`training/`、`main.py` CLI 完整入口  
- 完整 `GameSession` 状态机（M02+）  
- 持久化到 `saves/` 的高层 API（本步只需内存序列化往返；文件 IO 可测但非必须）  
- 玩家 RNG、AI 决策  

---

## 3. 设计

### 3.1 模块关系

```
game_id (str)
    │
    ▼
game_id.derive_seeds() ──► master_seed
    │                         ├── shuffle_seed ──► Deck.shuffle + deal
    │                         ├── dice_seed    ──► DiceResult + dealer_seat
    │                         └── exchange_seed （仅预留常量派生，M01 不使用）
    ▼
build_initial_state(game_id, config) ──► GameState (phase=dealt)
    │
    ▼
to_dict / from_dict  （JSON 兼容）
```

### 3.2 座位与人数

- 座位索引：`0 .. num_players-1`，逻辑顺序为 **逆时针**（与后续东→南→西→北映射：`seat i` 在 4 人时对应 `DIRS[i]`，M07 UI 再用）。  
- **庄家**：见 §3.4。  
- 发牌顺序：自庄家起按座位递增（模 `num_players`）依次各得 13 张，最后庄家再摸 1 张。  
- 2/3 人：仍用 **108 张** 全墙；仅减少座位数；规则与 4 人一致（已决议）。

### 3.3 Tile 约定

```text
Suit: wan | tong | tiao
Tile: (suit, rank)  rank ∈ 1..9
id 字符串: "{suit}_{rank}"   例: wan_1, tong_9, tiao_5
asset 路径键: suit + rank + theme（本步只提供 to_asset_parts()，不读盘）
```

- `Tile` 必须 **不可变**、可哈希、可排序（先 suit 再 rank；suit 序：`wan < tong < tiao`）。  
- 一副牌：每 `(suit, rank)` 有 **4** 张；构建时用 **4 个相同 Tile 值**（或可选 `instance_id` 0–3 仅用于调试去重；**默认相等语义按牌面**，发牌列表允许重复值）。  
  - **决议**：`Tile` 仅表示牌面；`Deck` 内部用 `list[Tile]`，相同牌面多实例可区分靠列表位置，序列化时手牌为 id 字符串列表即可。

### 3.4 game_id 与种子

| 项目 | 规格 |
|------|------|
| 用户指定 | 任意非空字符串（strip 后）；禁止空串 |
| 自动生成 | `cmj-{utc_yyyymmdd_hhmmss}-{8位hex}`（hex 来自 `secrets` 或 `os.urandom`，**仅用于新 ID 生成**，不参与同 ID 复现） |
| master_seed | `int.from_bytes(blake2b(game_id.encode('utf-8'), digest_size=8).digest(), 'big')` |
| shuffle_seed | `master_seed`（64-bit 截断后供 `random.Random`） |
| dice_seed | `master_seed ^ 0xA5A5A5A5A5A5A5A5`（再 `& 0xFFFFFFFFFFFFFFFF`） |
| exchange_seed | `master_seed ^ 0x5A5A5A5A5A5A5A5A`（M01 **只导出**，不消费） |

说明：

- 使用标准库 `hashlib.blake2b` + `random.Random(seed)`，**本步不强制 numpy**。  
- 同 `game_id` → 同 `master_seed` → 同骰点、同庄、同洗牌序列、同各家手牌与牌墙。

### 3.5 掷骰定庄

- 两枚独立骰子：`d1, d2 ∈ {1,2,3,4,5,6}`。  
- 派生方式（确定性）：

```text
rng = Random(dice_seed)
d1 = rng.randint(1, 6)
d2 = rng.randint(1, 6)
total = d1 + d2   # 2..12
```

- **庄家座位**（与人数无关的统一定义）：

```text
# 从座位 0 起，按骰子点数和「数」total 步（含起点为第 1 步的常见麻将数法）
# 采用：dealer_seat = (total - 1) % num_players
# 例：4 人，total=5 → seat 4%4=0；total=2 → seat 1
dealer_seat = (total - 1) % num_players
```

- 输出结构 `DiceResult`：`d1, d2, total, dealer_seat`。  
- UI 后续用 `assets/dice/dice_{n}_{theme}.png`；M01 只保证 `d1/d2` 可序列化。

### 3.6 牌墙与发牌

1. `build_full_wall() -> list[Tile]`：固定顺序生成 108 张（suit 序 × rank × 4 张），便于测试「未洗前」内容。  
2. `shuffle(wall, shuffle_seed)`：`Random(shuffle_seed).shuffle` 原地或返回新列表。  
3. 发牌：  
   - 墙用队列：从列表 **左侧 pop(0)** 或使用 index 指针 `wall_index`（推荐 **index 指针**，避免 O(n) 搬移；序列化保存剩余切片）。  
   - 对 `i in 0..12`：对 `k in 0..num_players-1`：`seat = (dealer_seat + k) % num_players` 发 1 张（共 13 轮）。  
   - 最后：庄家再摸 1 张。  
4. 发完后：`wall_remaining = 108 - (13 * num_players + 1)`。  
   - 4 人：`108 - 53 = 55`  
   - 3 人：`108 - 40 = 68`  
   - 2 人：`108 - 27 = 81`

### 3.7 状态模型（M01 最小集）

```text
GameState
  game_id: str
  master_seed: int
  phase: "dealt"          # M01 固定；后续扩展 dingque/playing/...
  num_players: int
  dice: {d1, d2, total}
  dealer_seat: int
  wall: list[Tile]        # 剩余牌墙（未发出）
  players: list[PlayerState]
  turn_index: int         # M01 置 0
  config: dict            # 快照

PlayerState
  seat: int
  hand: list[Tile]        # 庄 14，闲 13；可未排序，但提供 sorted_hand 辅助
  score: int              # 默认 0
  is_dealer: bool
  # 以下字段 M01 可空/默认，为序列化稳定预留：
  dingque: null
  melds: []
  discard_pile: []
  status: "active"
```

序列化：`Tile` → `"wan_3"`；`from_dict` 严格校验非法 id。

### 3.8 公开编排函数

```python
def create_dealt_game(
    game_id: str | None = None,
    *,
    num_players: int = 4,
    initial_score: int = 0,
) -> GameState:
    """
    - game_id is None → 自动生成新 ID
    - 返回 phase=='dealt' 的 GameState
    """
```

辅助：

- `generate_game_id() -> str`  
- `parse_tile(id: str) -> Tile`  
- `tiles_to_ids` / `ids_to_tiles`  
- `state_to_json(state) -> str` / `state_from_json(s) -> GameState`  

### 3.9 与 PLAN 对齐 / 偏差

| PLAN | M01 |
|------|-----|
| 骰子定庄 + 独立 game_id | ✅ |
| 庄家 13+1 | ✅ |
| exchange_seed 派生 | ✅ 仅预留 |
| 换三张 / 定缺 | ❌ M02 |
| UI 骰子 | ❌ M07 |

---

## 4. 接口与数据（实现契约）

### 4.1 JSON 示例（4 人，字段示意）

```json
{
  "schema_version": 1,
  "game_id": "demo-001",
  "master_seed": 1234567890123456789,
  "phase": "dealt",
  "num_players": 4,
  "dice": {"d1": 3, "d2": 5, "total": 8},
  "dealer_seat": 3,
  "wall": ["wan_1", "tong_2"],
  "players": [
    {
      "seat": 0,
      "hand": ["tiao_1", "..."],
      "score": 0,
      "is_dealer": false,
      "dingque": null,
      "melds": [],
      "discard_pile": [],
      "status": "active"
    }
  ],
  "turn_index": 0,
  "config": {"num_players": 4, "initial_score": 0}
}
```

### 4.2 配置

```python
@dataclass(frozen=True)
class EngineConfig:
    num_players: int = 4          # 2..4
    initial_score: int = 0
```

非法 `num_players` → `ValueError`。

### 4.3 错误行为

| 情况 | 行为 |
|------|------|
| 空 game_id | `ValueError` |
| 非法 tile id | `ValueError` |
| JSON 缺字段 / schema_version 不支持 | `ValueError` |
| from_dict 后手牌张数不对 | 校验失败 `ValueError`（可选 strict 模式，默认开） |

---

## 5. 文件清单

| 路径 | 动作 | 说明 |
|------|------|------|
| `engine/__init__.py` | 新增 | 导出公开 API |
| `engine/tile.py` | 新增 | Suit, Tile, 全集、解析 |
| `engine/game_id.py` | 新增 | 生成 ID、种子派生 |
| `engine/dice.py` | 新增 | 掷骰与庄家 |
| `engine/deck.py` | 新增 | 建墙、洗牌、发牌 |
| `engine/config.py` | 新增 | EngineConfig |
| `engine/state.py` | 新增 | PlayerState, GameState, 序列化 |
| `engine/deal.py` | 新增 | `create_dealt_game` 编排 |
| `requirements.txt` | 新增 | `pytest>=7.0`；（可选注释 pygame/numpy 待后续） |
| `tests/test_tile_deck.py` | 新增 | 牌与墙 |
| `tests/test_game_id_repro.py` | 新增 | 复现性 |
| `tests/test_state_serde.py` | 新增 | 序列化往返 |
| `docs/milestones/README.md` | 修改 | M01 状态 → Review |
| `docs/changelog.md` | 修改 | 记录规格 |
| **业务代码** | **本规格阶段不写** | 待 `Approved` 后实现 |

---

## 6. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| T01 | 全集牌 | `len(build_full_wall())==108`；每种牌面恰 4 张 |
| T02 | Tile id 往返 | `parse_tile(t.id)==t`；非法 id 抛错 |
| T03 | 同 game_id 种子 | 两次 `derive_seeds("demo")` 全等 |
| T04 | 不同 game_id | 高概率不同 master_seed（至少不等） |
| T05 | 骰子范围 | d1,d2 ∈ 1..6；dealer_seat ∈ 0..n-1 |
| T06 | 复现发牌 | 同 id 两次 `create_dealt_game`：dice、dealer、hands、wall 全等 |
| T07 | 手牌张数 | 庄 14、闲 13；墙剩余公式成立（2/3/4 人各测） |
| T08 | 序列化往返 | `from_dict(to_dict(s))` 语义相等 |
| T09 | JSON 字符串 | `state_from_json(state_to_json(s))` 相等 |
| T10 | 自动 game_id | `None` 生成非空且可再次复现该局（用返回的 id 再开一局应一致） |
| T11 | exchange_seed | 已派生且与 shuffle/dice 不同（稳定断言固定 game_id 的期望值可选） |

运行（实现后）：

```bash
pytest tests/test_tile_deck.py tests/test_game_id_repro.py tests/test_state_serde.py -q
```

---

## 7. 验收标准

- [x] 存在 §5 所列引擎模块与测试，且 `pytest` 上述用例通过  
- [x] 相同 `game_id` 两次运行：`d1,d2,dealer_seat`、各座位 `hand`、剩余 `wall` **完全一致**  
- [x] 4/3/2 人发牌张数与墙剩余正确  
- [x] `GameState` JSON 往返不丢字段、不改语义  
- [x] `exchange_seed` API 可调用（供 M02），本步不改变墙与手牌  
- [x] 无 Pygame 窗口依赖即可跑测试  
- [x] 未实现 Out of Scope 中的玩法逻辑  

---

## 8. 风险与开放问题

| 项 | 说明 | 状态 |
|----|------|------|
| 数庄算法 | 采用 `(total - 1) % num_players` | **本规格定为默认**；若用户要求「从某固定方位起数」可在 Review 改 |
| Tile 多实例 | 仅牌面、无 instance_id | 已定 |
| blake2b 跨平台 | 标准库，确定性 | 低风险 |
| 自动 game_id 含时间 | 仅新局唯一性；复现靠返回的 id | 已定 |

**开放问题 — 已关闭（用户确认 M01，2026-07-10）：**

| # | 决议 |
|---|------|
| 1 | 庄家公式采用 **`(dice_total - 1) % num_players`** |
| 2 | `requirements.txt` 本步 **仅 `pytest`**；pygame/numpy 在文件中注释预留，用到再启用 |

---

## 9. 实现备注（编码后填写）

- 实现路径：`engine/{tile,game_id,dice,deck,config,state,deal}.py` + `engine/__init__.py`
- 测试：`tests/test_tile_deck.py`、`test_game_id_repro.py`、`test_state_serde.py` — **19 passed**
- `Tile` 排序使用 `suit.sort_key`（wan&lt;tong&lt;tiao），未使用 `dataclass(order=True)`（避免 str Enum 字母序错误）
- JSON 中 `dice` 仅含 d1/d2/total；`dealer_seat` 在顶层；`from_dict` 会合并后校验
- 偏差：无功能性偏差

---

## 10. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | `Review` | 首版规格提交，待用户确认 |
| 2026-07-10 | `Approved` | 用户确认 M01；开放问题按默认方案关闭 |
| 2026-07-10 | `In Progress` / `Done` | 实现完成；pytest 19 passed |
