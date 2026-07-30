# B1-B详细实现设计审查

状态：**APPROVED_FOR_FINAL_GATE_REVIEW**  
批次：`B1-B`  
单元：`STATE-001 / STATE-011 / STATE-004`  
本文件不授权编码、不修改审计状态。

## 1. 依赖与上游复核

权威依赖图给出：`STATE-010→STATE-001`、`ALGO-009→STATE-001`、`ALGO-011→STATE-001/STATE-011`、`STATE-001→STATE-004`。STATE-011不是STATE-004的直接上游，但二者在生产runner中通过新局创建与phase流转相遇。

B1-A当前Task18状态为已完成，生产入口分别为`SeatRuntimeStore/FrozenGlobalParameters`、`validate_and_migrate_v2/freeze_v2`、`derive_coordinate_seed/create_dealt_game(rng_version=2)`；42/42 AC、18 executable Golden和E4/E5证据存在。Task17历史仍保持三单元PARTIAL，本设计仅据当前队列判断依赖满足，不改历史审计。

有效版本：legacy读取PARAMS 1.1/CONTRACTS 1/legacy-json-v1；新写PARAMS 2/CONTRACTS 2/CDMJ canonical-jcs-nfc-v2；legacy RNG缺版本走旧路径，新录制显式algorithm/rng v2；策略只可见安全`seed_trace_ref`。

## 2. STATE-001目标与当前实现

Locked来源：`deterministic_rule_state_specs.md#STATE-001` §1—20；目录行`locked_unit_catalog.csv#STATE-001`；规则AU-003、实现AU-055；参数GP-001..027/RP-001..033。

目标是由携带event/game/state version、ruleset/config hash和seed ref的创建请求，原子产生不可变MatchContext；冻结2/3/4座唯一seat/profile、局数、初分、庄家、版本和跨局白名单状态；错误码包括`INVALID_MATCH_REQUEST/DUPLICATE_SEAT/CONFIG_MUTATION/SEED_MISSING`及通用码；单写者CAS、失败零装配、审计字段完整、同输入逐字段复现。

当前`PlayerGameRunner.__init__/run`只控制单局；接收players、EngineConfig、game_id、starting_scores和rng_version。支持2/3/4座及单局比分继承，但没有MatchCreateRequest、MatchContext、total_rounds、event ledger、state_version CAS、profile冻结、两阶段装配或MatchResult。`on_join`逐座执行，后座失败可能留下前座外部效果。现有测试覆盖starting scores、连续两局调用者传分、runner完整结束；没有STATE-001直接错误码、原子性、版本或E4证据。

设计为新增内部`engine.match`门面和兼容adapter：不删除或改变现有runner签名。8项具体生产变化见semantic CSV；实施顺序为请求/schema→版本/hash/seed→seat/profile两阶段装配→round plan→CAS/event ledger→Frozen context投影→跨局完成。下游STATE-004/006/008/TRAIN-001只消费白名单投影；原始seed和对手profile不得进入策略对象图。

## 3. STATE-011目标与当前实现

Locked来源：`deterministic_rule_state_specs.md#STATE-011` §1—20；目录行；实现规范§4.1/§7.2；规则§1/§4；ALGO-011批准覆盖。

目标是以命名RNG和player count构建108个唯一physical_id，shuffle一次，按冻结seat/dealer顺序庄14闲13，4座余墙55，事务验证守恒后发布；legacy零变化、v2域隔离、未知版本准确错误；失败零提交；墙序和他手对策略不可见；worker顺序不影响结果。

当前`build_full_wall/shuffle_wall/deal_hands/create_dealt_game`已有108闭集、2/3/4发牌和legacy/v2派生，`create_dealt_game`直接返回GameState。未知版本抛普通ValueError；没有DealRequest/Result、event/state version、事务ledger、专用错误包络或STATE-011 audit。PlayerView边界已隐藏墙序/他手，基础守恒与复现测试存在。

设计为在现有函数外新增事务门面，保持`create_dealt_game`默认legacy兼容；严格复用ALGO-011公式，不重新定义stream/coordinate。8项变化依次为闭集验证→版本选择→域隔离→发牌门面→CAS/event→working-copy原子提交→PlayerView边界→legacy/v2 Golden与调度证明。

## 4. STATE-004目标与当前实现

Locked真实枚举/转换为：`CONFIGURED→DEALT→EXCHANGE(可跳过)→DINGQUE→READY→DRAW/DISCARD/RESPONSE循环→FINISHED→SETTLED`。候选`WALL_READY/PLAYING/SETTLEMENT`不在Locked枚举，不采用。

来源：`deterministic_rule_state_specs.md#STATE-004` §1—20；目录行；规则AU-043、实现AU-071。每事件需phase/actor/version guard、原子提交、稳定错误码、SETTLED吸收、审计和下游通知。

当前phase是GameState字符串，转换散布在opening、blood_battle、orchestrator和training env；第一胡后继续、多胡、杠补摸、墙尽、finished结算已有可运行分支，但没有统一RoundPhase门面、完整转换表、CAS/event幂等、稳定STATE-004错误包络或FINISHED→SETTLED显式phase（目前`end_settled`布尔附着于finished）。异常恢复可能在直接状态写入后发生，通知/审计不是统一事务outbox。

设计新增`engine.round_state_machine`兼容门面，第一切片不修改持久化v5 phase字段；legacy字符串通过一对一adapter。8项变化顺序：Locked enum→转换表→event/CAS→血战胡后active set→gang/response→FINISHED/SETTLED→事务outbox→fingerprint/audit。每条合法/非法边、第一/二/三胡、一炮多响、三类杠、墙尽、结算吸收均有客观oracle。

## 5. 接口、测试与证据

接口结论：`COMPATIBLE_EXTENSION`。新增Frozen内部DTO、稳定错误包络、RoundPhase/Deal/Match门面和版本化audit记录；保留GameState v5、PlayerGameRunner、create_dealt_game、legacy replay和既有异常行为的兼容adapter。没有删除Frozen字段或改变旧writer/hash/RNG结果，因此无`BREAKING_CHANGE_REQUIRED`，当前无需接口变更审批。

Delta：24 semantic、12 test、6 evidence。验收矩阵42行（每单元AC-01..14），42个objective oracle互不相同。性能在Locked无数值阈值处仅记录创建、deal和transition延迟分布基线，不作通过阈值。

E4必须来自真实`MatchController/PlayerGameRunner/create_dealt_game/opening/blood_battle`调用链；test-only facade不能充当E4。E5必须把Locked→ACTIVE delta→代码→测试→E4串联，且不得引用SUPERSEDED泛化SEM-PARAMETER。

## 6. 待审批与结论

未发现必须新增业务规格决策；未发现breaking接口变更。B1-A FG-002由`B1-A_authority_correction.md`形成ACTIVE纠正层，旧pending行被批准文件覆盖，分类统一为`MUST_FIX_BEFORE_AUTHORIZATION`并在本设计中闭合，待独立终审确认。

设计已由项目负责人于2026-07-30批准为`B1-B-DESIGN-1.0.0`。该批准只允许重新运行`PRE-DEV-FINAL-GATE-001`；在新终审明确授权前不得编码、不得标记AUDITED。
