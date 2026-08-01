# 十个试点单元可执行公共合同

| 字段 | 内容 |
|---|---|
| 状态 | Locked |
| 版本 | SPEC-V3-3.0.3 |
| 适用单元 | RULE-003、RULE-016、ALGO-001、ALGO-010、HEUR-019、MODEL-001、STATE-005、SCORE-001、TRAIN-003、AUDIT-003 |
| 优先级 | 对上述十单元的字段、分支、解释和证据结构作强制具体化；麻将规则仍以两份上游规则为准 |

## 1. 通用请求与结果

所有试点门面接受`UnitRequest`：`unit_id:str`、`game_id:str(1..256 UTF-8 bytes)`、`event_id:str(1..256)`、`state_version:uint64`、`ruleset_hash:sha256hex`、`config_hash:sha256hex`、`seed_ref:str|null`、`payload:object`。ID单位为N/A，版本单位为event revision，hash单位为hex字符；来源分别为Match Controller、权威State Store、冻结规则/配置loader和ALGO-011。无随机单元`seed_ref`默认`null`且不得消费随机数；其他必填字段无默认，null返回`SCHEMA_INVALID`。

统一`UnitResult`：`accepted:bool`、`result:object|null`、`error_code:str|null`、`state_version_before:uint64`、`state_version_after:uint64`、`input_hash/output_hash:sha256hex`、`explanation:object`。成功`error_code=null`；失败`result=null`。纯查询版本不变；命令仅经权威提交后+1。

## 2. 单元字段合同

| 单元 | payload字段：类型；单位；来源；范围；默认；null | result字段：类型/范围/精度 | 必测分支ID |
|---|---|---|---|
| RULE-003 | `phase:str;N/A;state;discard;无;拒绝`，`actor/seat:uint8;seat;state/request;0..3;无;拒绝`，`hand:PhysicalTile[];tile;state;0..14;[];拒绝`，`dingque:Suit;N/A;state;wan/tong/tiao;无;DINGQUE_UNSET`，`force:bool;N/A;GP-002;true/false;true;拒绝` | `legal_faces:str[]`规范序、`entity_map:face→physical_id[]`；0误差；explanation含forced/filtered/rejected | R003-B01 phase；B02 actor；B03 force；B04 missing dingque；B05 still-held；B06 cleared；B07 duplicate face；B08 inactive/version零写入 |
| RULE-016 | `phase:str;N/A;state;冻结phase枚举;无;拒绝`，`viewer:uint8;seat;request;0..3;无;拒绝`，`authoritative_state:object;N/A;state;schema;无;拒绝`，`policy_version:uint16;revision;config;2;2;拒绝` | `included_paths:str[]`、`redacted_count:uint32`、`view:object`；零隐藏字段；explanation含每条include/redact理由 | R016-B01 viewer；B02 phase；B03 self；B04 opponents；B05 wall；B06 finished；B07 unknown nested；B08 serialization/truth poison |
| ALGO-001 | `regions:map<Region,uint8[]>;tile;state;完整23 region且ID0..107;空region;拒绝` | `face_counts:uint8[27] 0..4`、`owner_by_id:Region[108]`、`conserved:bool`；整数0误差 | A001-B01 normal；B02 permutation；B03 id range；B04 duplicate；B05 missing tile；B06 unknown region；B07 missing region；B08 invalid container |
| ALGO-010 | 与RULE-016相同，来源为State Store+visibility policy | `PlayerViewV2`及formula/input/output hash；字段0误差 | A010-B01..B08与R016逐项对应并增加policy version |
| HEUR-019 | `cues:Cue[];cue;PlayerView/公开记忆;0..256;[];拒绝`；Cue含key、mandatory、salience/freshness/memory_strength `[0,1]`；`capacity:uint8;cue;GP-026;1..64;无;拒绝`；修正默认0且null拒绝 | 排序项含raw/components/corrections/final_score[-4,4]、rank、selected、filtered_reason；Decimal 1e-8 | H019-B01 golden；B02 mandatory；B03 capacity；B04 tie；B05 style；B06 level；B07 phase；B08 stop；B09 invalid；B10 permutation/statistics |
| MODEL-001 | `opponents:PublicOpponent[];opponent;PlayerView;0..3;[];拒绝`，只允许seat/dingque/discard_pile/melds/phase/wall_remaining/responses；缺省公开集合为空；禁用字段命中即拒绝 | 每seat概率、entropy/max_probability/evidence_count/low_evidence、prior/posterior/contributions、fallback/model版本；概率误差≤1e-9 | M001-B01 prior；B02 evidence；B03 normalization；B04 monotonic；B05 forbidden recursive；B06 schema；B07 timeout；B08 version；B09 calibration；B10 deterministic |
| STATE-005 | `builder_output:object;N/A;ALGO-010;白名单schema;无;拒绝`、`seat:uint8`、`phase:str`、`view/state_version:uint64` | 深冻结PlayerView、stable hash；字节0误差；explanation含schema/leak scan | S005-B01 freeze；B02 nested mutation；B03 hash；B04 roundtrip；B05 four-seat；B06 leak；B07 schema；B08 version |
| SCORE-001 | `event_id:str`、`layer:enum`、`reason:str`、`transfers:Transfer[]`、`balances_before:int64[];point;ledger;2..4 seats;无;拒绝`、`prev_hash:sha256hex|null`；空transfer默认[]，其他null拒绝 | `delta/after:int64[]`、sum_delta=0、event_hash、idempotent bool；整数0误差 | S001-B01 golden；B02 empty；B03 seat；B04 self；B05 amount；B06 overflow；B07 duplicate-same；B08 duplicate-conflict；B09 layer；B10 hash |
| TRAIN-003 | `actions:Action[];action;RULE-001;0..635;[]仅终止态;拒绝`、`action_id:uint16;slot;policy;0..634;无;拒绝`、`codec_version:uint16;revision;config;2;2;拒绝` | `mask:bool[635]`、encode/decode；零误差；解释含legal source与非法原因 | T003-B01 boundaries；B02 all635；B03 exchange；B04 invalid；B05 duplicate；B06 mask equality；B07 terminal；B08 env integration；B09 replay |
| AUDIT-003 | `records:AuditRecord[];record;AUDIT-001/002;1..N;无;拒绝`、`manifest:object;N/A;run;真实hash/time/versions;无;拒绝` | verified/status/error/first_failure/counts/final hash；字节0误差 | U003-B01 golden bytes；B02 valid chain；B03 byte tamper；B04 truncate；B05 reorder；B06 duplicate；B07 genesis；B08 privacy；B09 decision；B10 deterministic |

## 3. 解释与轨迹合同

决策类单元必须输出`candidate_key,generated_by,legal,raw_features,score_components,corrections,final_score,rank,selected,filtered_reason,abandon_reason,stop_reason`；不适用字段显式为null。完整轨迹按`game_id,event_index,unit_id`排序，绑定真实规则/config/code/model hash及命名seed，双跑逐事件比较输入、候选、选择、状态、分数、RNG位置和record hash。

## 4. 正式证据禁用值

`locked,pilot,unknown,TBD,TODO,placeholder`及固定伪时间不得出现在正式hash/time字段。证据生成器必须从真实文件字节、冻结配置和当前UTC时间计算；worktree dirty必须显式记录。命中禁用值时证据等级最高E2。
