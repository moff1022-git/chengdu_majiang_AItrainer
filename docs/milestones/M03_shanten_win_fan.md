# M03 — 向听、胡形判定、成都血战番型与封顶

| 字段 | 值 |
|------|-----|
| **编号** | M03 |
| **标题** | Shanten / Win-check / Chengdu Fan + fan_cap |
| **状态** | `Done` |
| **依赖** | **M01 Done**、**M02 Done**（`Tile`/`Suit`/`PlayerState.dingque`/`melds` 字段） |
| **下一里程碑** | M04（血战行牌状态机 + 合法动作 + 一炮多响） |
| **对应 PLAN** | §2.6 番型/封顶、§11 M3、`engine/shanten.py` · `win_check.py` · `fan.py` |

---

## 1. 目标

提供**与状态机解耦**的纯规则计算层，供 M04 合法胡判定、M05 计分、M08 策略分析复用：

1. **向听数（shanten）**：在定缺约束下，计算标准型与七对型的向听，并给出有效进张集合（可选但建议做）。  
2. **胡形判定（win check）**：判断「手牌 + 副露 + 和牌张」是否构成可胡牌形（标准 4 面子 1 将 / 七对），并满足定缺约束。  
3. **番型与番数（fan）**：按**成都血战**默认番表累加（可数据驱动），应用 **`fan_cap` 封顶**（`0` = 不封顶）。  
4. **上下文番**：杠上花、杠上炮、抢杠胡、海底/河底等依赖 `WinContext` 的标志位；本步定义接口与可测用例，不实现完整行牌触发。

本步**不**实现：摸打流程、点炮结算金额、碰杠操作、UI、玩家模块。

---

## 2. 范围

### 2.1 In Scope

| 项 | 说明 |
|----|------|
| `engine/hand_utils.py` | 手牌计数（34 码或 suit×rank）、副露规范化、定缺过滤辅助 |
| `engine/shanten.py` | `shanten(...)`、可选 `ukeire` / 有效进张 |
| `engine/win_check.py` | `is_winning_hand(...)`、`WinForm` 枚举 |
| `engine/fan.py` | `FanTable`、`compute_fan(...)`、`apply_fan_cap` |
| `engine/config.py` | 增加 `fan_cap: int = 0`（0=不封顶）；可选 `fan_table_path` |
| `configs/fan_table.json` | 默认成都血战番型表（数据驱动） |
| 单元测试 | 见 §7；固定手牌夹具，不依赖随机发牌 |

### 2.2 Out of Scope

- `blood_battle` 状态机、合法动作列表（M04）  
- 实际输赢分、底分倍率结算（M05 用本步 `fan` 结果）  
- 查花猪/查大叫金额（仅可预留「是否花猪/是否有叫」查询钩子，M05 计分）  
- numpy 加速（允许后续优化；本步可用纯 Python，接口不绑 numpy）  
- 龙七对/将七对等扩展番：见 §3.5 默认表，**首版包含七对/清七对/带幺相关**；更冷门组合按表配置  

---

## 3. 设计

### 3.1 牌面编码（内部）

为高效向听/胡判，内部使用 **27 种牌面**（无字牌）计数：

```text
index = suit_order * 9 + (rank - 1)   # 0..26
suit_order: wan=0, tong=1, tiao=2
counts: list[int] length 27, each 0..4
```

公开 API 仍接受 `list[Tile]` + `list[MeldView]`。

### 3.2 副露视图（M03 最小）

M01/M02 的 `melds: list` 尚未结构化。M03 定义：

```python
@dataclass(frozen=True)
class MeldView:
    kind: Literal["pong", "chow", "ming_gang", "an_gang", "jia_gang"]
    tile: Tile          # 面子代表牌（刻/杠为该牌；成都无吃，chow 仅占位禁用）
    # 可选 from_seat
```

- **成都无吃**：`kind=chow` 在 `is_winning_hand` 中 **直接非法**（或忽略并报错）。  
- 碰 = 刻子；明/补/暗杠 = 杠子（计「根」时用）。  
- 胡判时：副露已占面子数 `m`，手牌需凑 `4-m` 个面子 + 1 将（标准型）。

辅助：`melds_from_raw(raw: list) -> list[MeldView]`，兼容 dict/`MeldView`。

### 3.3 定缺约束

| 场景 | 规则 |
|------|------|
| 胡牌合法性 | 和牌瞬间：手牌（含所胡之张）与副露中 **不得残留 `dingque` 花色** 的牌 |
| `dingque is None` | 未定缺：本步可计算向听，但 **`is_winning_hand` 返回 False**（或 `WinReject.NO_DINGQUE`），与 M02「须定缺后 ready」一致 |
| 向听 | 缺门牌视为必须打出的废牌：计算时采用「缺门张不参与面子/将/对」，并增加「需先打出缺门」的代价——**推荐算法见 §3.4** |

### 3.4 向听（shanten）

#### 3.4.1 定义

- 输入：`hand: list[Tile]`（通常 13 张听牌形或 14 张），`melds`，`dingque: Suit | None`。  
- 输出：

```python
@dataclass(frozen=True)
class ShantenResult:
    shanten: int              # -1 = 已胡（仅当 14 张且 is_win）；0 = 听牌；1+ = 向听
    standard: int             # 标准型向听
    seven_pairs: int          # 七对向听（有副露时视为 +∞ / 大数，不参与 min）
    ukeire: frozenset[Tile] | None  # 进张牌面集合；shanten>0 时可算；首版允许 None 若性能不足
```

- **总向听** = `min(standard, seven_pairs)`（有副露时仅 standard）。  
- 约定：`shanten == -1` 表示当前 14 张（或手+胡张）已可胡。

#### 3.4.2 标准型算法（规格要求）

采用业界常用的 **完整枚举 / 递归拆分**（或等价查表）计算标准型向听，牌种仅 万筒条。

伪要求：

1. 将 `hand` 转为 27 维计数。  
2. 副露占用面子数 `meld_count`。  
3. 搜索使「面子数 + 将」最接近目标的拆分，向听公式与日本/国标通用标准型一致（目标：`meld_count + 手拆面子 = 4` 且 1 将）。  

**定缺处理（锁定方案 A）**：

- 将手牌中所有 `dingque` 花色牌计为 **isolated 强制弃张**：在标准向听上 **加上** `num_dingque_tiles` 的修正是否过严？  

更准确、与实战一致的方案：

**方案 A（推荐，本规格采用）**：

1. 从计数中 **暂时移除** 所有缺门牌（不参与拆牌）。  
2. 对剩余牌算标准向听 `s0`（注意手牌张数变少，按「目标面子数仍为 4-meld_count」但总张数不齐——应使用「向听定义：还需几步变成胡形」，缺门每张至少要打出 1 次）。  
3. 最终：`standard = s0 + dingque_count` 在「缺门不参与成型」下：  
   - 正确做法：缺门牌每张贡献「必须打出」，等价于在正常 13/14 张向听算法中把缺门当 **永远无法组成面子的孤张**（类似字牌孤张）。实现上：缺门 rank 槽位可参与「打出」但不参与顺子/刻子组合。  

**实现指令（可测试）**：

- 缺门花色的 9 个 index：**禁止**形成顺子/刻子/作为将？将也不允许缺门（因胡时不能有缺门）。故缺门张 **只能作为需要打出的废张**，向听至少 ≥ 缺门张数相关。  
- 标准库实现可参考：对非缺门牌做拆牌，目标仍为 4 面子 1 将；当前「有效张」= 总张 - 缺门张；缺门张全部视为「多余需要换成有效张」。  
- **验收夹具**优先于算法论文：用 §7 固定用例钉死结果。

#### 3.4.3 七对向听

- 仅当 `melds` 为空。  
- 七对：7 个对子；向听 = `6 - pair_count + max(0, need_adjust for quads)` 等标准七对向听（4 张同一牌面算 1 对 + 需处理）。  
- 缺门：七对胡时同样不能含缺门 → 缺门张破坏七对，计入向听惩罚（与夹具一致）。

#### 3.4.4 有效进张（建议 In Scope）

对 `shanten == 0` 的 13 张，枚举 27 种加 1 张后 `is_winning_hand` 为真的牌面；张数受剩余 4 枚上限约束（计算「理论进张」可不查牌山）。

### 3.5 胡形判定

```python
class WinForm(str, Enum):
    STANDARD = "standard"      # 4 melds + pair
    SEVEN_PAIRS = "seven_pairs"

@dataclass(frozen=True)
class WinCheckResult:
    ok: bool
    form: WinForm | None
    reason: str | None         # 失败原因码
```

```python
def is_winning_hand(
    hand: list[Tile],          # 含和进之张的完整手牌（未含副露）
    melds: list[MeldView],
    dingque: Suit | None,
    *,
    allow_seven_pairs: bool = True,
) -> WinCheckResult:
```

**成功条件**：

1. `dingque is not None`  
2. 手牌+副露无缺门花色  
3. 标准型可拆 **或**（无副露且）七对  

**张数**：标准型 `len(hand) + 3*len(melds) + gang_extra` 应符合麻将常识：

- 碰/吃占 3 张面子；杠占 4 张但算 1 面子；手牌张数 = `14 - 3*普通副露 - 3*杠?`  

统一约定（血战常见）：

| 副露 | 手牌张数（含胡牌张） |
|------|----------------------|
| 0 | 14 |
| 1 碰 | 11 |
| 2 碰 | 8 |
| 1 杠 | 11（杠 4 张已露出，手牌 11 含胡张） |
| … | `14 - 3 * num_melds`（**杠也按 1 面子减 3 的手牌计数习惯**：因第 4 张来自杠，手牌侧少 1） |

更清晰的 **实现约定**：

- `meld_slots = len(melds)`（每个副露 1 面子）。  
- 标准型需要手牌部分组成 `(4 - meld_slots)` 个面子 + 1 将。  
- 手牌张数必须等于 `3 * (4 - meld_slots) + 2`。  
- 杠的第 4 张不在 `hand` 里，已在 meld 中体现；`MeldView` 的杠不改变「面子槽」数量（仍为 1）。

### 3.6 番型与封顶

#### 3.6.1 WinContext

```python
@dataclass(frozen=True)
class WinContext:
    is_zimo: bool = False          # 自摸
    is_gang_shang_hua: bool = False  # 杠上花
    is_gang_shang_pao: bool = False  # 杠上炮
    is_qiang_gang: bool = False      # 抢杠胡
    is_hai_di: bool = False          # 海底捞月 / 河底捞鱼（合并标志，细分可后续）
    root_extra: int = 0              # 额外根（若算法未从牌面统计全）
    # 预留
```

#### 3.6.2 默认番表（`configs/fan_table.json`）

> 成都血战常见数字版约定：**平胡 0 番**，计分时 `score ∝ 2^fan`（M05）；本步只产出 `fan` 整数。  
> 下列为 **默认初值**，可用 JSON 覆盖，无需改代码。

| id | 名称 | 番 | 判定要点 |
|----|------|-----|----------|
| `ping_hu` | 平胡 | 0 | 标准型且无更高牌型时保底列出 |
| `dui_dui_hu` | 对对胡 | 1 | 全部刻子/杠 + 将（无顺子） |
| `qi_dui` | 七对 | 2 | 七对型（非龙七） |
| `qing_yi_se` | 清一色 | 2 | 手+副露同一花色 |
| `dai_yao_jiu` | 带幺九 | 1 | 每面子与将都含 1/9 |
| `duan_yao_jiu` | 断幺九 | 1 | 无 1/9 |
| `jin_gou_diao` | 金钩钓 | 1 | 胡时手牌仅 2 张（1 对）+ 全副露 |
| `gen` | 根 | 1/根 | 每组 4 张相同（含杠、暗 4）计 1 根；可叠加 |
| `gang_shang_hua` | 杠上花 | 1 | context |
| `gang_shang_pao` | 杠上炮 | 1 | context |
| `qiang_gang` | 抢杠胡 | 1 | context |
| `hai_di` | 海底 | 1 | context |

**叠加规则（默认）**：

- 牌型番 **可叠加**（如清一色 + 对对胡 = 清对，表中可不再单列，用叠加：2+1=3）。  
- `ping_hu` 仅当「标准型且其余牌型番均为 0 且无七对」时计入 0（标记用，总和仍 0）。  
- 七对与对对胡互斥（走七对分支不加对对）。  
- 清一色 + 七对 = 清七对：2+2=4（叠加）。  
- **根** 与牌型叠加。  
- 自摸 **不额外加番**（成都常自摸各家付，番数本身不因自摸+1；M05 处理付分对象）。  

若 JSON 中存在组合键 `qing_dui: 3` 等，可作为 **覆盖项**（检测到清+对时用固定 3 而非 2+1）——首版 **仅用叠加**，不做组合覆盖，除非表中显式 `"composite_rules"`。

#### 3.6.3 计算 API

```python
@dataclass(frozen=True)
class FanResult:
    fan: int                 # 封顶后
    fan_raw: int             # 封顶前
    yaku: list[str]          # 命中的 id 列表
    details: dict            # id -> fan 贡献

def compute_fan(
    hand: list[Tile],
    melds: list[MeldView],
    dingque: Suit,
    win_tile: Tile | None,   # 可冗余；hand 已含
    context: WinContext | None = None,
    *,
    fan_table: FanTable | None = None,
    fan_cap: int | None = None,  # None 则读 config 默认
) -> FanResult:
```

`apply_fan_cap(raw, cap)`：`cap <= 0` → 不封顶；否则 `min(raw, cap)`。

#### 3.6.4 根的统计

- 每一组 count==4 的牌面（手牌+副露杠）计 1 根。  
- 已杠出的 `ming_gang/an_gang/jia_gang` 各计 1 根。  
- 手牌中 4 张未杠也计 1 根（胡牌时）。

### 3.7 配置扩展

```python
@dataclass(frozen=True)
class EngineConfig:
    num_players: int = 4
    initial_score: int = 0
    exchange_dir: str = "auto_dice"
    fan_cap: int = 0              # 0 = 不封顶；常见 4 或 5
    # fan_table_path: 可选 str，默认 configs/fan_table.json
```

### 3.8 模块依赖

```text
tile / hand_utils
    ├── shanten
    ├── win_check  ──► fan（先确认 ok 再算番；fan 也可在调用方保证 ok）
    └── fan
config / configs/fan_table.json
```

`compute_fan` 在 `not is_winning_hand` 时：抛 `ValueError` 或返回 `fan=0, yaku=[]`——**规格采用抛 `FanError`**，避免静默错分。

### 3.9 与后续里程碑

| 里程碑 | 使用方式 |
|--------|----------|
| M04 | 弃牌后检查他人 `is_winning_hand`；自摸检查 |
| M05 | `FanResult.fan` × 底分 × 付分规则 |
| M08 | `shanten` + `ukeire` 展示策略 HUD |

---

## 4. 接口与数据摘要

### 4.1 `configs/fan_table.json` 形状

```json
{
  "version": 1,
  "yaku": {
    "ping_hu": 0,
    "dui_dui_hu": 1,
    "qi_dui": 2,
    "qing_yi_se": 2,
    "dai_yao_jiu": 1,
    "duan_yao_jiu": 1,
    "jin_gou_diao": 1,
    "gen": 1,
    "gang_shang_hua": 1,
    "gang_shang_pao": 1,
    "qiang_gang": 1,
    "hai_di": 1
  },
  "notes": "Chengdu xuezhan defaults; score uses 2^fan in M05"
}
```

### 4.2 错误类型

```python
class HandError(ValueError): ...
class FanError(ValueError): ...
```

---

## 5. 文件清单

| 路径 | 动作 |
|------|------|
| `engine/hand_utils.py` | 新增 |
| `engine/shanten.py` | 新增 |
| `engine/win_check.py` | 新增 |
| `engine/fan.py` | 新增 |
| `engine/config.py` | 修改 `fan_cap` |
| `engine/__init__.py` | 导出 |
| `configs/fan_table.json` | 新增 |
| `tests/test_shanten.py` | 新增 |
| `tests/test_win_fan.py` | 新增 |
| `docs/milestones/README.md` | M03 状态 |
| `docs/changelog.md` | 记录 |

---

## 6. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| S01 | 已听标准型 13 张 | `shanten == 0` |
| S02 | 已胡 14 张标准型 | `shanten == -1` 或 win 与 shanten 一致 |
| S03 | 七对听 | `seven_pairs == 0` |
| S04 | 含缺门废张 | 向听 > 无缺门同型 |
| W01 | 标准胡 | `ok` + `STANDARD` |
| W02 | 七对胡 | `ok` + `SEVEN_PAIRS` |
| W03 | 含缺门不能胡 | `ok is False` |
| W04 | 未定缺不能胡 | `ok is False` |
| W05 | 烂牌不能胡 | `ok is False` |
| F01 | 平胡 | `fan_raw == 0`，yaku 含 ping_hu |
| F02 | 对对胡 | `fan_raw >= 1` |
| F03 | 清一色 | `+2` |
| F04 | 清一色+对对 | 叠加 3 |
| F05 | 七对 | 2 |
| F06 | 带根 | +1/根 |
| F07 | `fan_cap=2` 截断 | `fan == 2`, `fan_raw > 2` |
| F08 | 杠上花 context | +1 |
| F09 | 非法非胡手算番 | `FanError` |
| R01 | 全量回归 M01+M02 | 仍通过 |

夹具用手写 `Tile` 列表，不依赖 `game_id` 发牌。

```bash
pytest tests/ -q
```

---

## 7. 验收标准

- [x] `shanten` / `is_winning_hand` / `compute_fan` API 可用且有单测  
- [x] 定缺约束在胡判中生效  
- [x] 默认番表与 JSON 加载一致；`fan_cap` 生效  
- [x] 七对与标准型分支正确互斥/可选  
- [x] M01+M02 回归通过  
- [x] 无行牌状态机、无 UI  

---

## 8. 风险与开放问题

| 项 | 默认决议 |
|----|----------|
| 平胡番数 | **0 番**（2^0 倍底，M05） |
| 自摸是否加番 | **否** |
| 清对 | **叠加** 清一色+对对，不单列 |
| 向听缺门 | **缺门不参与组合，废张推高向听**；以夹具为准 |
| numpy | 本步不强制 |

**开放问题 — 已关闭（用户确认 M03，2026-07-10）：**

| # | 决议 |
|---|------|
| 1 | 平胡 **0 番**（M05 用 `2^fan` 计分） |
| 2 | `fan_cap` 默认 **0（不封顶）**；对局可配 4/5 等 |
| 3 | **听牌（shanten==0）必须计算 ukeire**；`shanten>0` 允许 `ukeire=None` |

---

## 9. 实现备注（编码后填写）

- 新增：`hand_utils.py`、`win_check.py`、`shanten.py`、`fan.py`、`configs/fan_table.json`
- 向听：听牌用「+1 成胡」精确判定；一般情形 DFS + 封顶公式；缺门张 mask 后加惩罚
- 测试：`test_shanten.py`、`test_win_fan.py`；全量回归通过
- 偏差：无功能性偏差

---

## 10. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | `Review` | 首版规格提交，待用户确认 |
| 2026-07-10 | `Approved` | 用户确认 M03；开放问题按默认方案关闭 |
| 2026-07-10 | `Done` | 实现完成 |
