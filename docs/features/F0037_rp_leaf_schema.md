# F0037 RP 叶级 Schema 设计

Status: Done

Approval: 用户于 2026-08-01 指令“执行任务1-5”，明确批准并要求实现本规格。

## 1. 目的与范围

本规格为 RP-001～RP-033 运行态槽位定义统一的叶级 envelope 和字段合同。它只约束跨模块共享的元数据、生命周期、可见性和不变量；各业务切片可以在 `payload.extensions` 中增加经过登记的扩展字段。本文不把 RP 变成用户可编辑参数，也不改变 engine 的权威状态。

In Scope：统一 envelope、33 个 RP 的核心字段、类型/范围、更新事件、权限和审计要求；旧快照迁移策略；schema 校验门禁。

Out of Scope：新增业务规则、改变计分、开放隐藏信息、把 GP 配置复制进 RP、冻结尚未有消费者的启发式字段。

## 2. 统一 Envelope

每个非空 RP 槽位均采用如下结构：

```json
{
  "schema_version": "F0037-RP-1.0",
  "parameter_id": "RP-023",
  "lifecycle": "round|event|decision|settlement|cross_round",
  "event_index": 12,
  "owner_seat": 0,
  "visibility": "private|public_exact|public_partial|audit_only",
  "status": "absent|active|final|invalidated",
  "payload": {},
  "extensions": {},
  "source": "engine|player_view|humanlike_policy|audit",
  "updated_at_event": 12,
  "payload_hash": "sha256:..."
}
```

必选约束：`parameter_id` 必须与槽位一致；`event_index` 单调递增且为 0—1,000,000；`owner_seat` 为 0—3 或 `null`（全局槽位）；`extensions` 只能使用已登记命名空间；`payload_hash` 对 canonical JSON 的 payload+extensions 计算。`audit_only` 只允许审计读取，不能进入 PlayerView。

空槽位仍保持 `null`，表示尚未产生，而不是伪造默认 payload。兼容读取器同时接受 Task 19 现有裸 payload；保存/新快照统一写 envelope。

## 3. 叶字段命名和数据规则

- 字段使用 `snake_case`；数组顺序必须稳定；集合使用排序后的 ID 数组。
- 金额/分数为有符号整数，范围 `-1_000_000_000..1_000_000_000`；概率、强度、风险和置信度为 `0..1`。
- 牌类型使用现有 `tile_id`/27 维计数约定，不引入第二套牌编码。
- 时间使用非负整数毫秒；事件序号使用非负整数；时间戳是否公开由 GP-021 决定。
- 未公开字段必须省略或置 `null`，不得用服务器真实值填充。
- 扩展字段不得覆盖核心字段；未知扩展只能被忽略并记录审计告警。

## 4. 33 个 RP 核心叶字段

| RP | 核心 payload 字段 | 生命周期/更新事件 | 可见性 | 状态 |
|---|---|---|---|---|
| RP-001 | `round_id:string`、`round_index:1..total_rounds`、`event_index:0..1e6`、`status` | 建局、每原子事件、终局 | `public_partial`（id 可脱敏） | `IMPLEMENTED` |
| RP-002 | `dealer_id:0..3`、`self_seat:0..3`、`active_seats:sorted[0..3]`、`turn_order` | 建局、庄家/胡牌退出 | `public_exact` | `IMPLEMENTED` |
| RP-003 | `match_score_before_round:int[4]`、`round_ledger:int[4]`、`objective_strength:0..1`、`score_gap` | 建局、结算事件 | `public_partial` | `IMPLEMENTED` |
| RP-004 | `hand_counts:int[27]`、`dealer_hand_size:13|14`、`structure_hash` | 发牌后一次 | `private` | `CONTRACT_ONLY` |
| RP-005 | `out_tiles:tile[3]`、`in_tiles:tile[3]`、`direction`、`same_suit:true` | 换三张执行 | `private/public_partial` | `CONTRACT_ONLY` |
| RP-006 | `self_missing_suit`、`cleared`、`remaining_missing:0..14`、`opponent_confidence[4]` | 定缺提交、弃牌后 | `private`；对手仅置信度 | `CONTRACT_ONLY` |
| RP-007 | `hand_counts:int[27]`、`meld_removals`、`last_draw`、`last_discard` | 摸牌、出牌、碰杠 | `private` | `CONTRACT_ONLY` |
| RP-008 | `melds_by_seat[4]`、`meld_type`、`tile_ids` | 碰/杠/补杠 | `public_exact`（暗杠按 GP-021） | `CONTRACT_ONLY` |
| RP-009 | `entries[]:{seat,tile,event_index,source,time}` | 每次弃牌 | `public_partial` | `CONTRACT_ONLY` |
| RP-010 | `visible_counts:int[27]`、`unseen_upper:int[27]` | 每公开事件 | `public_exact` | `CONTRACT_ONLY` |
| RP-011 | `wall_remaining:0..108`、`round_turn`、`estimate_min/max` | 摸牌/杠后补牌 | `public_exact/partial` | `CONTRACT_ONLY` |
| RP-012 | `active_seats`、`winner_order`、`finished_seats` | 胡牌、退出、终局 | `public_exact` | `CONTRACT_ONLY` |
| RP-013 | `type`、`actor`、`tile`、`source`、`public_payload` | 每原子事件 | 按事件和 GP-021 | `IMPLEMENTED` |
| RP-014 | `legal_actions[]`、`deadline_ms`、`response_kind` | 决策窗口开始/关闭 | `private` | `IMPLEMENTED` |
| RP-015 | `state`、`unlock_reason`、`changed_event_index` | 过胡/恢复事件 | `private` | `IMPLEMENTED_PARTIAL` |
| RP-016 | `shanten:-1..13`、`meld_count:0..4`、`pair_count:0..7`、`quality:0..1` | 手牌/副露变化 | `private` | `IMPLEMENTED_PARTIAL` |
| RP-017 | `primary`、`backup[]`、`confidence:0..1`、`evidence_event_index` | 计划形成/切换 | `private` | `IMPLEMENTED_PARTIAL` |
| RP-018 | `wait_tiles[]`、`live_counts:int[27]`、`live_total`、`probability:0..1`、`dead_wait` | 手牌/可见牌变化 | `private` | `CONTRACT_ONLY` |
| RP-019 | `hypotheses[]:{id,probability}`、`evidence_event_index` | 公开行为后更新 | `private` | `CONTRACT_ONLY` |
| RP-020 | `risk_by_seat_tile`、`aggregate_risk`、`loss_norm` | 每次公开证据/决策 | `private` | `CONTRACT_ONLY` |
| RP-021 | `remaining_draws`、`self_draws_estimate`、`time_pressure:0..1` | 牌墙/活动座位变化 | `private` | `CONTRACT_ONLY` |
| RP-022 | `phase`、`phase_strength:0..1`、`wall_ratio:0..1` | 牌墙变化 | `public_partial` | `CONTRACT_ONLY` |
| RP-023 | `count`、`actions[]`、`mandatory_count`、`prune_reason` | 决策候选生成 | `private` | `IMPLEMENTED_PARTIAL` |
| RP-024 | `items[]:{key,category,weight}`、`capacity`、`temperature` | 每次决策 | `private` | `IMPLEMENTED_PARTIAL` |
| RP-025 | `items[]:{key,strength,salience}`、`capacity`、`cross_round_impressions` | 公开事件/跨局 | `private` | `IMPLEMENTED_PARTIAL` |
| RP-026 | `configured_depth`、`effective_depth`、`checked_count`、`stop_reason`、`quality:0..1` | 候选搜索/停止 | `audit_only` | `IMPLEMENTED_PARTIAL` |
| RP-027 | `deadline_ms`、`time_left_ms`、`think_time_ms`、`time_pressure` | 决策开始/结束 | `private/public_partial` | `IMPLEMENTED_PARTIAL` |
| RP-028 | `level`、`style`、`emotion:-1..1`、`plan_restarted`、`restart_reasons[]` | 每次决策/结果 | `private` | `IMPLEMENTED_PARTIAL` |
| RP-029 | `records[]`，每条含 `event_index,input_hash,candidates,selected,reason,stop_reason,rng_index` | 每次决策追加 | `audit_only` | `IMPLEMENTED_PARTIAL` |
| RP-030 | `deltas:int[4]`、`ledger:int[4]`、`zero_sum`、`event_kind` | 胡/杠/转移结算 | `audit_only` | `CONTRACT_ONLY` |
| RP-031 | `revealed_tiles`、`public_events`、`correction_versions` | 公开事件/更正 | `public_exact/partial` | `CONTRACT_ONLY` |
| RP-032 | `round_result:int[4]`、`huazhu_delta`、`dajiao_delta`、`tax_refund_delta` | 终局一次 | `public_exact` | `IMPLEMENTED` |
| RP-033 | `features:{key:0..1}`、`observation_count`、`eta:0..1`、`source_tags[]` | 终局后跨局 | `private/audit_only` | `IMPLEMENTED` |

`CONTRACT_ONLY` 表示本规格冻结了字段合同，但当前代码尚未统一写入；`IMPLEMENTED_PARTIAL` 表示已有同名或等价字段但尚未满足 envelope 全量要求；`IMPLEMENTED` 表示当前槽位已有稳定写入路径。

## 5. 写入、读取和合并规则

1. engine 只能写 RP-001～003、013、030～032 等权威状态；player policy 只能写自己的 RP-015～029 派生认知槽位；audit 只能追加 RP-029/030/031 证据。
2. `owner_seat` 不等于可见性；任何 PlayerView 读取必须再次通过 GP-021 白名单过滤。
3. 同一 `parameter_id + event_index` 只能有一个核心版本；冲突写入拒绝并保持上一快照。
4. 更新采用 copy-on-write；单次失败不得留下半个 payload。终局后所有 RP 只读。
5. RP 核心字段与扩展字段分开 hash；扩展缺失不影响核心回放，核心缺失则快照无效。

## 6. 迁移和版本

- `F0037-RP-0.x`：兼容 Task 19 裸 payload，读取时包装为 envelope，`status=active`，缺失字段标记 `absent`。
- `F0037-RP-1.0`：新写入版本；只允许新增可选字段或 extensions，不允许重解释现有字段。
- 破坏性字段变化升级 major，并提供纯函数迁移和双 hash 证据；不得静默覆盖旧审计记录。

## 7. 验收门禁

- 33 个 RP 均有唯一核心字段合同和生命周期。
- 非空 payload 的 `parameter_id`、`event_index`、visibility、hash 均可校验。
- 隐藏信息不会进入 public/public_partial；PlayerView 不泄露服务器真值。
- 同一事件重复写入幂等；冲突写入拒绝；失败事务回滚。
- 旧 Task 19 快照可读，新快照可 round-trip；终局快照不可变。
- 现有 Task 19 全量回归保持通过，RP schema 失败不得改变 engine 计分或合法动作。

## 8. 后续实现拆分

1. `runtime.py` 已增加 envelope、核心字段校验和版本迁移读取。
2. engine/player/audit 分权写入适配器已实现，Humanlike 已迁移到 envelope 写入。
3. 事件驱动的 RP 公共镜像、隐藏字段拦截和剩余槽位占位写入已实现。
4. schema round-trip、visibility、幂等和旧快照迁移测试已通过。

说明：部分 RP 的当前写入是事件镜像或稳定占位，不等于完整规则计算器；若需要完整业务派生，应另立实现规格，不改变本 schema 合同。
