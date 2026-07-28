# F0028-2 — 实体牌、事件断言与 PlayerView v2

| 字段 | 值 |
|------|----|
| 编号 | F0028-2 |
| 状态 | `Approved`（2026-07-28 用户确认；尚未实现） |
| 父规格 | [F0028_humanlike_ai_v2_implementation_plan.md](F0028_humanlike_ai_v2_implementation_plan.md) |
| 依赖 | F0028-1 `Done`；CDMJ-AI-RULES 1.0.0 / PARAMS 1.0.0 / IMPL 2.0.0 |
| 当前应用基线 | APP 0.2.1 / state schema 4 / persistence format 1 / wire protocol 1 |
| 规格日期 | 2026-07-28 |

## 1. 结论与已批准决议

F0028-2 在不重写规则引擎的前提下，引入 0–107 的实体牌身份、原子事件边界断言和显式白名单 PlayerView v2。`Tile(suit, rank)` 继续作为牌面值对象和算法输入；引擎状态中的实际牌张改由 `PhysicalTile(tile_id, face)` 表示，旧 UI、Action 和分析模块仍可通过牌面投影工作。

用户已于 2026-07-28 确认并锁定以下版本决议：

1. `GameState` 写出格式升级为 **schema 5**，读取继续支持 schema 1–5；schema 1–4 在内存中确定性迁移为实体牌。
2. 存档外壳字段未改变，`FORMAT_VERSION` 保持 **1**；外壳中的 `schema_version` 和 `state.schema_version` 写 5。
3. Human 子进程 NDJSON 消息外壳不变，`PROTOCOL_VERSION` 保持 **1**；`Observation.view` 增加 `view_version=2`，同时保留人类座位 UI 需要的兼容投影键。
4. `filter_state_for_seat()` 和 `build_observation()` 继续存在，但内部必须委托白名单 builder，不再先序列化全量状态再删除字段。
5. 训练 oracle 真值不再允许写入 `Observation.view`；改由 `training/oracle.py` 的独立类型返回，仅评估器可调用。

上述任一决议改变都需先修订本文，不能在实现中静默选择。

## 2. 背景与现状证据

当前实现有以下事实：

- `engine.tile.Tile` 只有牌面，四张同牌相等且无实体身份。
- `engine.deck.build_full_wall()` 重复放入同一个牌面对象；状态中的 wall/hand/discard 仅保存 `wan_1` 等牌面字符串。
- `PlayerState.melds` 是弱类型字典，只保存 `kind + tile_id(face)`，无法指出碰/杠具体占用哪几张实体牌。
- `discard_pile` 同时承担公开历史展示；被碰杠的弃牌仍留在历史中，因此它只能成为“事件引用”，不能与副露同时被当作两个所有权位置。
- `pending_exchange` 是手牌选择引用，不是从手牌移出的独立所有权位置。
- `last_discard`、`last_draw_tile`、`exchange_log`、`score_events` 和 `hu_sequence` 都是状态/事件引用，不应重复计入 108 张守恒。
- `protocols.view_filter` 当前从 `state.to_dict()` 开始再删除 wall 和他家手牌；未来一旦状态新增私有字段，存在默认泄漏风险。
- `build_observation(include_oracle_hands=True)` 可把他家真手牌放进普通 `view`，与生产 PlayerView 的零泄漏目标冲突。

## 3. 目标与非目标

### 3.1 In Scope

- 108 张实体牌稳定编码、牌面投影、唯一性与守恒。
- schema 1–4 的确定性实体 ID 补全和 schema 5 round-trip。
- 强类型副露与弃牌记录，使“所有权”和“历史引用”可区分。
- 在引擎原子事件完成后运行结构、所有权、牌面数量、状态机、账本和合法动作断言。
- 显式白名单 `PlayerViewV2` / `PlayerViewBuilder`，实现 GP-021 的可见性边界。
- 保持现有 2/3/4 人、Human 子进程、UI、RuleAI、训练入口可运行。
- 自动化泄漏审计和兼容测试。

### 3.2 Out of Scope

- 不实现 `humanlike_v2` 候选生成、评价或玩家注册（F0028-3）。
- 不实现记忆、注意力、人格和满意停止（F0028-4）。
- 不实现完整决策 trace / RNG 回放格式（F0028-5）。
- 不改变麻将合法行动、番型、计分和当前默认 AI 行为。
- 不修改 APP SemVer，不升级 persistence format 或 wire protocol。
- 不删除 schema 1–4 读取能力，不移除旧 `filter_state_for_seat` API。
- 不把 AI 认知状态写进 `GameState`。

## 4. 实体牌领域模型

### 4.1 编码与类型

```python
@dataclass(frozen=True, slots=True)
class PhysicalTile:
    tile_id: int       # 0..107，实体身份
    face: Tile         # 牌面值

    @property
    def face_id(self) -> str: ...  # wan_1
```

唯一换算：

```text
tile_type = suit_index * 9 + (rank - 1)       # 0..26
tile_id = tile_type * 4 + copy_index          # 0..107
copy_index = tile_id % 4                      # 0..3
```

约束：

- `physical_tile(tile_id)` 必须由 ID 反推出唯一 face，不接受 ID 与 face 不一致。
- `Tile.id` 保持 `wan_1` 风格，不改 UI/资源契约。
- 新规则代码优先传 `PhysicalTile`；只需要花色点数的既有算法通过 `.face` 或只读 `suit/rank` 投影使用。
- Action v1 仍按 face 表达玩家意图；Action Resolver 必须从该玩家合法所有权区域中确定性选择实体牌：同 face 按最小 `tile_id`。实体选择不得由 AI 或 UI 越权指定。

### 4.2 所有权区域与引用字段

守恒断言只扫描“所有权区域”，每个实体 ID 必须恰好出现一次：

1. `wall_tile_ids`；
2. 各座位 `concealed_tile_ids`；
3. 各座位副露 `meld.tile_ids`；
4. 未被认领的弃牌记录；
5. 抢杠/换牌原子转换期间的 `transit_tile_ids`。

以下字段是引用或历史，**不得**再次计入所有权：

- 已被认领的弃牌历史；
- `last_discard_tile_id` / `last_draw_tile_id`；
- `pending_exchange` 选择；
- `exchange_log`、事件流、计分事件和胡牌顺序；
- PlayerView、审计日志和训练真值中的实体 ID。

### 4.3 强类型副露和弃牌记录

```python
@dataclass(frozen=True, slots=True)
class Meld:
    kind: Literal["pong", "ming_gang", "an_gang", "jia_gang"]
    tile_ids: tuple[int, ...]      # pong=3，gang=4；同一 face
    source_seat: int | None
    claimed_discard_event: int | None

@dataclass(frozen=True, slots=True)
class DiscardRecord:
    event_index: int
    seat: int
    tile_id: int
    claimed_by: int | None
    claim_kind: str | None
```

- 碰/明杠时，弃牌历史保留，但该记录标记 `claimed_by`；同一实体 ID 的所有权转入副露。
- 暗杠从手牌转入四 ID 副露。
- 补杠在响应窗口内先进入 `transit_tile_ids`；无人抢杠后并入原碰，抢杠成功后转入胡牌事件定义的终态位置。
- `pending_exchange` 始终引用手牌中的 ID；交换统一 resolve 时才原子转移，禁止同时计为额外位置。
- 兼容投影仍输出旧 `melds=[{"kind", "tile_id": face_id}]` 和 `discard_pile=[face_id...]`，但这两个投影不是 schema 5 权威存储。

## 5. schema 5 与旧档迁移

### 5.1 schema 5 权威字段

schema 5 的权威实体字段使用明确后缀：

- `wall_tile_ids: list[int]`
- `players[*].concealed_tile_ids: list[int]`
- `players[*].melds[*].tile_ids: list[int]`
- `players[*].discards[*].tile_id/claimed_by/claim_kind/event_index`
- `pending_exchange_tile_ids: dict[str, list[int]]`
- `transit_tile_ids: list[int]`
- `last_discard_tile_id` / `last_draw_tile_id` 为非所有权引用

新 writer 不再把牌面字符串字段作为权威状态写出。`to_legacy_view_dict()` 负责生成 UI/wire 所需牌面键。

### 5.2 schema 1–4 确定性补全

迁移函数必须纯函数化：

```python
migrate_state_to_v5(raw_state: dict) -> dict
```

迁移顺序固定为：

1. 按旧 wall 列表原顺序；
2. 按 seat 升序、旧 hand 列表顺序；
3. 按 seat 升序、弃牌历史顺序；
4. 按 seat 升序、副露顺序补全副露所需牌。

对每个 face 建立 `copy_index=0..3` 池。迁移先识别被碰/明杠引用的最近同 face 弃牌，将该弃牌实体复用于副露而非重复分配；其余副露从对应玩家手牌概念移出后的剩余池补足。若旧快照无法在每 face 四张内形成唯一所有权，抛出 `StateMigrationError`，不得猜测或截断。

迁移必须满足：

- 同一旧 JSON 重复迁移得到字节级一致的 schema 5 实体字段；
- schema 1–4 读取后在内存中 `schema_version=5`；
- 不原地覆盖用户旧存档；只有显式再次保存时写 schema 5；
- schema 5 → JSON → schema 5 保持实体 ID、wall 顺序、弃牌/副露引用和语义一致；
- schema 1–4 兼容夹具覆盖 dealt、exchange、dingque、play、碰、三类杠、胡和 finished 状态。

### 5.3 版本决议

| 版本线 | 当前 | F0028-2 提议 | 原因 |
|--------|------|--------------|------|
| GameState schema | 4 | **5** | 权威牌字段从 face 字符串变为实体 ID，属于不兼容状态结构变化 |
| persistence format | 1 | **保持 1** | 外壳、元数据和加载入口不变，内部 schema 已独立版本化 |
| wire protocol | 1 | **保持 1** | NDJSON 消息类型不变；view 内版本化并保留兼容投影 |
| PlayerView | 无独立版本 | **2** | 新增强类型白名单和 GP-021 可见性契约 |

## 6. 原子事件与断言门禁

### 6.1 事件边界

断言只在完整原子转换后执行，不在临时移牌中间态执行。必须覆盖：

- 发牌完成；
- 四家换牌统一 resolve；
- 定缺提交/阶段结束；
- 摸牌；
- 出牌并开启响应窗；
- 全部 pass；
- 碰、明杠、暗杠、补杠成功；
- 抢杠响应完成；
- 自摸/点炮/一炮多响；
- 流局及终局结算。

实现采用现有入口的小步插桩，不新建第二套事件引擎。推荐统一调用：

```python
assert_event_boundary(state, *, event_type: str, legal_actions_by_seat=None)
```

### 6.2 必须断言

| 类别 | 断言 |
|------|------|
| ID | 全部 ID 为整数 0–107；所有权区域并集恰为 `set(range(108))`；交集为空 |
| 牌面 | 每个 tile_type 恰有 4 个实体；ID 反推 face 与对象 face 一致 |
| 引用 | last draw/discard、pending exchange、claim、事件引用都指向已存在实体；引用不另占所有权 |
| 副露 | pong 三张、gang 四张且同 face；补杠替换原碰，不并存重复组 |
| 手牌 | 张数与阶段/副露数/当前行动一致；定缺、胡牌基础结构仍由既有规则检查 |
| 状态机 | phase/current seat/active seats/response window/赢家状态组合合法 |
| 账本 | 每个零和计分事件增量和为 0；累计账本与 score_events 一致；非零和平台项必须显式标记 |
| 合法动作 | 每个 Action 引用的 face 在行动座位可用实体中；候选不得超出 legal actions |

生产模式断言失败抛出结构化 `InvariantViolation(code, event_type, event_index, details)`；测试和日志可读取 details，但 PlayerView 不得包含内部所有权快照。

## 7. PlayerView v2 白名单

### 7.1 类型与构建边界

新增：

- `protocols/player_view_v2.py`：冻结的 `PlayerViewV2`、`PublicPlayerView`、`PublicMeldView`、`WallView`。
- `protocols/player_view_builder.py`：唯一生产 builder；仅逐字段读取 `GameState`，禁止调用 `state.to_dict()`。
- `protocols/view_filter.py`：保留兼容函数，委托 builder 后输出 legacy-compatible dict。

所有生产策略只接收冻结 PlayerView，不接收 `GameState`。F0028-2 只建立边界，不注册新策略。

### 7.2 顶层允许字段

`PlayerViewV2` 只允许以下字段；schema 5 新增字段不会自动进入视图：

```text
view_version (=2)
game_id
self_seat
phase
event_index
dealer_seat
current_seat
turn_index
exchange_direction_public
wall
self_player
other_players
discard_history
last_public_event
legal_actions
deadline_ms
```

其中：

- 自己手牌可以含 `tile_id + face_id`，因为实体副本对本人可见且不泄漏他家位置。
- 他家只含 seat、score、dealer、dingque、status、hand_count、可公开副露和胡牌公开信息。
- 他家暗手、wall tile IDs、transit、pending claims 细节、全局真实状态、AI 认知状态永不进入视图。
- legal actions 仍按 face 表达，避免暴露实体选择细节。

### 7.3 GP-021 可见性矩阵

| GP-021 项 | hidden | public_partial | public_exact |
|-----------|--------|----------------|--------------|
| `wall_remaining` | `wall=None` | 只给稳定区间/档位，不给精确值 | 给 `remaining_exact` |
| `draw_source` | 弃牌记录不含摸切/手切 | 只给 unknown/direct/hand_change 分类 | 给可证明的来源字段 |
| `exchange_source` | 不给方向或来源座位 | 给方向，不给来源座位 | 给方向和来源座位 |
| `concealed_gang_tiles` | 只公开发生暗杠及数量 | 公开花色或平台粒度 | 公开 face；永不公开不必要的实体副本 ID |
| `hu_hand` | 只公开胡牌状态/牌张数 | 按平台公开摘要 | 公开完整 face 列表 |
| `draw_round_hand` | 不公开 | 按平台摘要 | 终局后公开 face 列表 |
| `thinking_time` | 不提供 | 桶化为 fast/normal/slow | 提供界面已显示毫秒值 |
| `cancel_action` | 不提供 | 只提供发生标志 | 提供界面可见的动作类型/时刻 |

`public_partial` 必须在配置或 builder 常量中有确定粒度；底层状态没有可靠公开证据时输出 `None/unknown`，禁止用真实隐藏值补齐。

### 7.4 legacy 兼容投影

Human UI、现有 RuleAI 和训练旧入口在 F0028-2 期间继续获得当前键形状：

- `wall_remaining`；
- `players[*].hand`（仅自己）、`hand_count`、`melds`、`discard_pile`；
- 当前公共 phase/config/last_discard 等必要键。

该投影从 `PlayerViewV2` 构造，而不是从 `GameState.to_dict()` 删除字段。兼容投影必须有字段快照测试；任何新增字段默认拒绝，需经规格批准后显式加入。

## 8. oracle 分离与泄漏审计

### 8.1 oracle API

- 删除生产 builder 的 `include_oracle_hands` 能力。
- 新增 `training/oracle.py::build_training_truth(state) -> TrainingTruth`。
- `TrainingTruth` 不属于 Observation、PlayerView 或 wire message；调用点仅允许 `training/` 评估和离线指标模块。
- 通过模块依赖测试禁止 `players/humanlike/`、`players/rule_ai_player.py`、`protocols/` 导入 `training.oracle`。

### 8.2 自动泄漏测试

对每个 seat、每个关键 phase 构建视图并递归扫描：

- 不出现他家 `concealed_tile_ids` 或 face 手牌列表；
- 不出现 wall 实体 ID 或真实顺序；
- 不出现隐藏暗杠 face；
- 不出现未公开换牌来源、胡牌手牌或终局手牌；
- 不出现 `oracle_hands`、`training_truth`、`transit_tile_ids`、`pending_claims`、完整 state/config 私有字段；
- 视图中的所有实体 ID 均属于观察者自己或明确公开事件，且不能据此反推出未知牌位置。

测试必须采用“向 `GameState` 注入哨兵私有字段后仍不出现在 view”的方式证明白名单，而不只检查当前已知黑名单。

## 9. EngineConfig 与 GP 的单一权威适配

F0028-2 只接入与实体牌/视图有关的 GP：GP-004、GP-005、GP-007、GP-009、GP-010、GP-021、GP-022。新增只读 `HumanlikeEngineAdapter` 将已验证的 `HumanlikeConfig` 投影为现有 `EngineConfig` 和 view policy；不允许反向修改 GP。

若现有 `EngineConfig` 与 GP 值冲突：

1. humanlike_v2 session 创建失败并列出冲突字段；
2. 旧 profile 继续只使用原 `EngineConfig`；
3. 不在运行中择一覆盖，也不维护两份可变权威。

完整 GP-011–GP-020 计分适配不属于本切片；需要接入时另立子规格或归入后续规则适配切片。

## 10. 文件清单

### 10.1 计划新增

- `engine/physical_tile.py`
- `engine/invariants.py`
- `engine/state_migrations.py`
- `protocols/player_view_v2.py`
- `protocols/player_view_builder.py`
- `training/oracle.py`
- `tests/humanlike_v2/test_physical_tiles.py`
- `tests/humanlike_v2/test_state_v5_migration.py`
- `tests/humanlike_v2/test_invariants.py`
- `tests/humanlike_v2/test_player_view_v2.py`
- `tests/humanlike_v2/fixtures/schema_1_4/`（小型、去隐私的固定夹具）

### 10.2 计划修改

- `engine/tile.py`、`engine/deck.py`、`engine/deal.py`、`engine/state.py`
- `engine/exchange.py`、`engine/dingque.py`、`engine/blood_battle.py`、`engine/legal.py`
- `engine/score.py`、`engine/persistence.py`、`engine/replay.py`
- `protocols/view_filter.py`、`protocols/messages.py`、`protocols/__init__.py`
- `training/env.py`、`players/seat_ui_hub.py`
- 相关 state/persistence/view/exchange/play 回归测试
- `docs/status/DOC_CODE_BASELINE.md`、`docs/status/LATEST.md`、`docs/changelog.md`

实现不得一次性修改 F0028-3–6 的候选、认知、trace 或训练动作空间文件。

## 11. 测试计划

### 11.1 单元与属性测试

1. 0/107 边界、非法 ID、ID↔face↔copy index 双向转换。
2. 108 张 wall ID 唯一；每 face 恰四张；固定 seed 洗牌顺序可复现。
3. 摸、打、换、碰、三类杠、抢杠胡和胡牌后的所有权分区互斥且并集为 108。
4. 引用字段不重复计数；悬空引用和重复所有权明确失败。
5. schema 1–4 固定夹具迁移 hash 稳定；坏档明确失败；schema 5 round-trip 保持 ID。
6. PlayerView v2 每个 GP-021 模式的字段矩阵。
7. 哨兵字段注入、每 seat/phase 泄漏扫描为 0。
8. oracle 只能通过训练真值 API 获取，生产模块依赖扫描为 0。

### 11.2 回归与兼容

- 现有全量 pytest 无新增失败；macOS Tk 继续仅保留既有预期 skip。
- 2/3/4 人从 deal 到 finished 均通过守恒断言。
- Human 子进程 observation/action_request 继续使用 wire v1 并可完成操作。
- RuleAI、Random、F0010/F0011、训练 env 的既有测试继续通过。
- schema 1–4 保存样本可加载并继续完成牌局；显式重存后为 schema 5。
- `game_id + seed` 对应的 **牌面序列与既有基线一致**；实体 copy index 不得改变牌面级洗牌/发牌结果。

### 11.3 性能门禁

- 默认关闭深度 debug 细节时，事件断言不得使 4AI 批量对局吞吐下降超过 20%。
- PlayerView v2 单次构建相对当前 filter 的中位耗时不得恶化超过 25%，并报告样本数和机器环境。
- 断言不可通过全量 JSON 序列化实现；直接扫描强类型区域。

## 12. 验收标准

- [x] schema 5 / persistence 1 / wire 1 / PlayerView 2 版本决议经用户确认（2026-07-28）。
- [ ] 108 个实体 ID 唯一，每个 face 四张；全部原子事件后所有权守恒。
- [ ] schema 1–4 迁移确定、可重复、坏档失败且不覆盖原文件。
- [ ] schema 5 保存/读取保持实体 ID 和事件引用。
- [ ] 碰杠后的弃牌历史可见，但同一 ID 只在一个所有权区域。
- [ ] PlayerView 从显式白名单构建，不调用 `GameState.to_dict()`。
- [ ] GP-021 八项在 hidden/partial/exact 下均有测试。
- [ ] 生产 PlayerView 泄漏率 0，oracle 与 Observation 完全分离。
- [ ] Human wire v1、旧 UI、RuleAI、训练旧入口兼容。
- [ ] 2/3/4 人及现有全量回归通过；性能门禁有报告。
- [ ] 实现后回写父规格、DOC_CODE_BASELINE、LATEST 和 changelog。

## 13. 风险与回滚

| 风险 | 控制 |
|------|------|
| 实体迁移范围大 | 先实现 ID 类型和迁移夹具，再改状态所有权；每个原子动作独立验收 |
| 旧 meld/discard 无实体信息 | 固定遍历和最近弃牌匹配；无法唯一守恒则失败，不猜测 |
| Action 仍是 face 可能选错副本 | resolver 固定选择该所有权区最小 tile_id，并记录选择 |
| 白名单破坏 UI | 保留 legacy 投影和字段快照测试；wire 版本不变 |
| 断言影响吞吐 | production 使用轻量必检；昂贵诊断只在失败或 debug 开启 |
| 双配置权威 | 只读 adapter + 冲突即失败，不双向同步 |

回滚方式：F0028-2 在合入前保持独立提交；若实体状态迁移未通过全部门禁，回退该切片并继续使用 schema 4、旧 `Tile` 状态和既有 view filter。已生成的 schema 5 测试档仅用于开发，不作为正式发布存档。中间状态不得发布。

## 14. 审批后实施顺序

1. PhysicalTile / wall / ID 属性测试。
2. schema 5 数据模型和 schema 1–4 迁移夹具。
3. 强类型 discard/meld 与各原子动作所有权迁移。
4. 事件边界断言与 2/3/4 人批量回归。
5. PlayerView v2 白名单、GP-021 和 legacy 投影。
6. oracle 分离、泄漏审计、Human/RuleAI/training 兼容。
7. 性能测试、全量验收、文档回写。

本文已达到 `Approved`，允许用户后续明确要求“实现 F0028-2”时按上述七步修改业务代码；本次确认动作本身不授权编码。
