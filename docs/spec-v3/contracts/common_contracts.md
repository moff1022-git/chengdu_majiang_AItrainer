# 成都麻将AI训练模拟器公共接口与数据契约

| 字段 | 内容 |
|---|---|
| 契约版本 | `CDMJ-CONTRACTS 1.0.0` |
| 状态 | Frozen |
| 规范基线 | `SPEC-V3-3.0.3`、Task15 PASS |
| Schema | `schemas/common_contracts.schema.json`、`fixture.schema.json`、`decision.schema.json` |
| 序列化 | canonical JSON UTF-8；键排序；禁止NaN/Inf；时间UTC RFC3339 |

## 1. 唯一类型来源

引擎内部复用`engine.tile.Tile`、`PhysicalTile`、`Meld`、`DiscardRecord`、`PlayerState`、`GameState`、`Action`；策略边界复用`PlayerViewV2`、`DecisionContext`、`Candidate/CandidateSet`、`EvaluationResult`、`Decision`；审计复用`DecisionAuditWriter`格式。策略不得定义另一套牌、动作、座位或分数语义。跨进程/持久化只使用本契约JSON投影，不传Python对象引用。

## 2. 基础标量和单位

| 类型 | JSON/范围 | 必填/默认/null | 单位与精度 | 语义 |
|---|---|---|---|---|
| `SeatId` | integer 0..3 | 必填；无默认；禁null | seat；整数 | 固定座位，不能用相对方位替代 |
| `PhysicalTileId` | integer 0..107 | 必填；禁null | tile entity；整数 | 唯一实体牌 |
| `FaceId` | `wan|tong|tiao`+`_1..9` | 必填 | tile face | 可互换牌面 |
| `EventIndex` | uint64 | 必填；默认仅新局0 | event | 权威事件顺序 |
| `ScorePoint` | int64 | 必填；初始默认配置值 | point；整数0误差 | 可为负 |
| `Probability` | number 0..1 | 必填；禁null | ratio；误差≤1e-9 | 禁NaN/Inf |
| `NormalizedValue` | number -1..1 | 必填；禁null | normalized ratio；1e-8 | ROUND_HALF_EVEN |
| `ScoreValue` | number -4..4 | 必填 | utility；1e-8 | 启发式比较值，非真实分 |
| `DurationMs` | integer 0..600000 | 可选；默认null | millisecond | deadline/think time |
| `LatencyUs` | number ≥0 | 运行证据必填 | microsecond | P50/P95/P99同单位 |
| `Sha256Hex` | 64位小写hex | 必填；无默认 | hex chars | 对canonical bytes求SHA-256 |

## 3. 牌、手牌、牌墙、弃牌和副露

| 结构/字段 | 类型 | 必填 | 范围/默认/null | 语义与可见性 |
|---|---|---:|---|---|
| `FaceTile.face_id` | FaceId | 是 | 无默认/禁null | 公开牌面 |
| `FaceTile.suit/rank` | enum/integer | 是 | 3花色/1..9 | 必须与face_id一致 |
| `PhysicalTile.tile_id` | PhysicalTileId | 是 | 0..107 | 权威/本座私有；对手暗手不得公开 |
| `PhysicalTile.face_id/copy_index` | FaceId/integer | 是 | copy 0..3 | `face=floor(id/4)` |
| `Hand.owner_seat` | SeatId | 是 | 无默认 | 手牌所有者 |
| `Hand.tile_ids` | unique PhysicalTileId[] | 是 | 0..14；默认[] | 权威精确；策略仅本座可见 |
| `Wall.tile_ids` | unique PhysicalTileId[] | 是 | 0..108；默认[] | 仅模拟器全知；策略禁止 |
| `Wall.remaining` | integer | 是 | 0..108 | 可按GP-021公开精确值或区间 |
| `Discard.event_index/seat/tile_id` | uint64/SeatId/PhysicalTileId | 是 | 禁null | 已发生公开事件 |
| `Discard.claimed_by/claim_kind` | SeatId/null、enum/null | 否 | 默认null | 认领关系 |
| `Meld.kind` | `pong|ming_gang|an_gang|jia_gang` | 是 | 禁null | 副露种类 |
| `Meld.tile_ids` | unique PhysicalTileId[] | 是 | pong=3，其余=4 | 权威实体；公开投影受GP-021控制 |
| `Meld.source_seat/claimed_discard_event` | SeatId/null、uint64/null | 否 | 默认null | 来源追踪 |

实体牌在wall、四手牌、四弃牌、四副露、换牌池和过渡区中必须恰好出现一次，总数108。

## 4. 玩家和状态

`PlayerState`字段：`seat:SeatId`必填；`concealed_tile_ids:PhysicalTileId[]`必填默认[]；`score:int64`必填默认0；`is_dealer:bool`默认false；`dingque:Suit|null`默认null（定缺后不得null）；`melds:Meld[]`和`discards:Discard[]`默认[]；`status:active|finished`默认active；`hu_order:uint8|null`默认null；`last_win:object|null`默认null。已胡玩家`status=finished`，不再摸打或响应，但分数和公开信息保留。

`GameState`冻结schema版本5。必填：`game_id,master_seed,phase,num_players,dice,dealer_seat,wall_tile_ids,players,turn_index,config`。phase唯一枚举：`dealt,exchange,dingque,ready,draw,discard,response,finished`。可选流程字段沿用`GameState.to_dict()`，缺省集合为空、布尔为false、未知上下文为null。任何未知phase、重复seat、错误actor或非法状态组合必须显式错误，不能转为“无动作”。

## 5. 动作和合法集

`Action.type`唯一枚举：`exchange,dingque,discard,pass,pong,gang_ming,gang_an,gang_jia,hu`。`tiles`默认[]；`suit`默认null。exchange恰3张同花色；dingque只含suit；牌面动作按既有codec要求含一牌面；pass无牌；HU允许0或1上下文牌。`LegalActionSet`包含`request_id,seat,phase,actions,codec_version=2,mask[635],state_version,input_hash`；actions规范排序且非终止决策时非空。策略只能在该集合内选择。

## 6. 候选、评分和决策

`Candidate`：`candidate_key`必填稳定字符串；`action`必填；`mandatory:bool`默认false；`generated_by:unit_id`必填；`legal:bool`必须true；`filtered_reason:null|string`默认null。

`ScoreBreakdown`：`raw_features:map<string,number>`、`weights:map<string,number>`、`components:map<string,number>`、`corrections:{style,level,phase,noise}`、`final_score:ScoreValue`、`rank:uint16`。全部必填，缺失特征使用显式`missing_mask`，不得用0伪装未知。确定基线ROUND_HALF_EVEN至1e-8。

`DecisionResult`：`request_id,seat,event_index,selected_action,reason_code,explanation,model_or_policy_version,config_hash,ruleset_hash,seed_trace,state_version_before,state_version_after`必填；`think_time_ms`默认0；`error_code`成功为null。不可决策时`selected_action=null`并返回稳定状态码。

## 7. 解释和审计

`DecisionExplanation`必须包含：`generated_candidates`、`scored_candidates`、`filtered_candidates`、`selected_candidate_key`、`selection_reason`、`abandoned_reasons`、`stop_reason`、`plan`、`attention`、`belief_summary`、`rng_used/index_before/index_after`。不适用字段用空集合或null，不得删除必填键。审计记录绑定PlayerView hash、合法集、所选动作、状态前后hash、规则/config/code/model版本、前序record hash和UTC；隐藏牌只留受控hash。

## 8. 参数、随机数和错误

参数定义为`parameter_id,parameter_version,type,unit,min,max,default,nullable,visibility,source,value`；GP/RP ID不得别名化。配置冻结后由canonical hash标识，局中禁止热替换。

`SeedTrace`包含`game_id,algorithm_version,master_seed:uint64,stream_name,index_before,index_after,seed_hash`。禁止系统时间、全局random或worker调度决定策略结果。无随机单元`stream_name=null,index_before=index_after=0`。

稳定错误族：schema/版本/权限`SCHEMA_INVALID,VERSION_CONFLICT,UNAUTHORIZED`；状态`WRONG_PHASE,NOT_ACTOR,INVALID_STATE,NOT_DECIDABLE`；牌`PHYSICAL_ID_RANGE,OWNERSHIP_DUPLICATE,OWNERSHIP_MISSING`；动作`ACTION_CODEC_INVALID,ILLEGAL_ACTION,EMPTY_LEGAL_SET`；信息`VISIBILITY_LEAK,FORBIDDEN_INPUT`；数值/计分`NON_FINITE,SCORE_OVERFLOW,SCORE_NOT_ZERO_SUM,DUPLICATE_SCORE_EVENT`；审计`HASH_MISMATCH,CHAIN_TRUNCATED,CHAIN_REORDERED`。未知错误不得映射成功。

## 9. Fixture

测试场景使用`fixture.schema.json`：必填`fixture_version=1,fixture_id,title,ruleset_hash,config,game_id,seed,initial_state,steps,expected`。每step含`event_id,actor,phase,input,expected_output,expected_state_hash,expected_error`；无随机写`seed_stream=null`。隐藏truth只能置于`restricted_truth`，策略输入必须来自独立`player_views`。

## 10. 冻结声明

本契约不改变业务规则，只冻结跨模块语义。新增策略必须复用Action、Candidate、ScoreBreakdown、DecisionResult和PlayerView契约；禁止另建同义DTO。兼容与变更规则见`versioning_policy.md`。
