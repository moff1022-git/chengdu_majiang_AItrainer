# F0028-5 — 决策审计、哈希链与确定性策略回放

| 字段 | 值 |
|------|----|
| **编号** | F0028-5 |
| **状态** | `Done`（2026-07-29） |
| **父功能** | [F0028 人类化 AI v2 实现方案](F0028_humanlike_ai_v2_implementation_plan.md) |
| **依赖** | F0028-1–4 `Done` |
| **输入版本** | CDMJ-AI-RULES 1.0.0 / PARAMS 1.0.0 / IMPL 2.0.0 |
| **版本基线** | APP 0.2.1 / state 5 / PlayerView 2 / persistence 1 / wire 1 |
| **实现授权** | 已执行并通过验收 |

## 1. 目标

建立独立、版本化、可防篡改验证的决策审计文件，使维护者能够回答：决策前后权威状态是否一致、AI 当时收到哪个 PlayerView、有哪些 legal actions、检查了哪些候选、为何停止、使用了哪个 RNG 位置、最终选择什么，以及相同审计输入序列能否复演得到相同 humanlike 动作与认知 trace。

F0028-5 不替换 M10 私有 steps 快照和 ReplaySession。旧 `.steps.jsonl` 继续负责帧浏览；新 `.audit.jsonl` 负责决策证据、哈希链和策略复演。

## 2. 范围

### 2.1 In Scope

- 规范 UTF-8 JSON 的稳定 canonical 编码和 SHA-256。
- `audit_format_version=1` 的 header/decision/footer 记录。
- 每次决策的 state before/after hash、PlayerView hash、engine config hash、humanlike config hash。
- 保存该座位实际收到的过滤后 Observation、legal actions、最终动作、DecisionTrace v2、认知/RNG 摘要。
- `previous_record_hash → record_hash` 链式验证；任意字段、顺序或截断异常明确失败。
- 在 `save_every_decision` 模式并行生成 `<game_id>.audit.jsonl` 和旧 `<game_id>.steps.jsonl`。
- humanlike v2 策略复演：按审计顺序重建各 seat 玩家私有认知状态，重新 observe/decide，比较动作和规范化 trace。
- 独立文件验证 CLI/API 基座；本切片以 Python API 和测试为权威，不增加 GUI。

### 2.2 Out of Scope

- 从审计文件单独重放完整规则引擎事件；规则帧仍由 M10 steps/ReplaySession 提供。
- F0028-6 训练动作 codec、mask、reward 或多智能体训练。
- 将认知状态写入 GameState、persistence save 或 PlayerView 协议。
- 公开发布包含本家暗手的审计文件；`.audit.jsonl` 是 private diagnostic artifact。
- 密钥签名、加密、远程日志服务或不可抵赖证明；SHA-256 链只用于完整性与确定性检查。
- 为 legacy RuleAI 伪造 humanlike trace；非 humanlike 决策可记录但不做策略复演。

## 3. 安全与兼容边界

1. audit writer 位于引擎编排边界，可计算完整 state hash，但不得把完整 GameState 放入 decision 输入字段。
2. `player_view` 必须是实际发送给该 seat 的 Observation；允许包含本家暗手，不允许包含他家暗手、墙顺序或 TrainingTruth。
3. state before/after 只保存 hash；完整真值仍只存在 private steps 文件。
4. 审计记录不使用随机 `request_id` 参与确定性 hash；使用审计文件内递增 `decision_index`。
5. canonical JSON：UTF-8、sort_keys、紧凑分隔符、`allow_nan=false`；禁止 datetime、对象 repr 和平台路径进入 hash。
6. reader 拒绝未知 audit format、缺字段、非连续 index、链断裂、view hash 不匹配和 footer 数量/hash 不匹配。
7. 旧 ReplaySession、StepRecorder 文件格式保持可读；APP/state/persistence/wire/PlayerView 均不升级。

## 4. Audit v1 文件契约

每行一个对象，换行本身不参与 record hash。记录 hash 的输入是删除 `record_hash` 后的完整行对象。

### 4.1 Header

```json
{
  "audit_format_version": 1,
  "kind": "header",
  "game_id": "...",
  "implementation_version": "CDMJ-AI-IMPL 2.0.0",
  "state_schema_version": 5,
  "player_view_version": 2,
  "engine_config_hash": "sha256",
  "initial_state_hash": "sha256",
  "previous_record_hash": null,
  "record_hash": "sha256"
}
```

### 4.2 Decision

```json
{
  "audit_format_version": 1,
  "kind": "decision",
  "game_id": "...",
  "decision_index": 0,
  "seat": 0,
  "phase": "discard",
  "state_hash_before": "sha256",
  "state_hash_after": "sha256",
  "player_view": {"game_id": "...", "self_seat": 0, "phase": "discard", "view": {}},
  "player_view_hash": "sha256",
  "legal_actions": [],
  "policy": "humanlike_v2_cognitive",
  "policy_config_hash": "sha256|null",
  "decision_trace": {},
  "rng": {"used": false, "index_before": 0, "index_after": 0},
  "cognitive_snapshot": {"memory": {}, "attention": [], "plan": {}},
  "selected_action": {},
  "reason": "...",
  "applied": true,
  "previous_record_hash": "sha256",
  "record_hash": "sha256"
}
```

`decision_trace` 对 humanlike 必须是 trace v2。`cognitive_snapshot` 是 trace 的只读投影，不额外读取策略内部对象。普通玩家允许 trace/policy config 为 null。

### 4.3 Footer

Footer 记录 `decision_count`、`final_state_hash`、`final_chain_hash` 和 `finished_reason`，自身也加入链。正常 runner 结束必须写 footer；异常/截断文件允许 reader 加载记录，但 strict verify 必须失败。

## 5. 模块与接口

### 5.1 `engine/audit.py`

- `canonical_json_bytes(value)`, `canonical_hash(value)`。
- `DecisionAuditWriter(path, header...)`：原子逐行追加、持有链头与 decision index。
- `record_decision(...)`：校验 view/seat/phase/legal/action/trace 并写链。
- `finish(...)`：写 footer，关闭后不可追加。
- `load_audit(path)`：解析为不可变记录序列。
- `verify_audit(path, strict=True)`：返回 `AuditVerification`；坏链/坏 view hash/坏 index 明确抛 `AuditError`。

### 5.2 `players/humanlike/audit_replay.py`

- `replay_humanlike_audit(path, config_path=None)`。
- 为每个 seat 懒创建 `HumanlikeV2Player`；按 decision index 喂入存档 Observation 和 ActionRequest。
- request_id 使用本地稳定占位，不参与策略结果；比较 `Action.to_dict()`、trace v2 的确定性字段和 RNG before/after。
- 非 humanlike 记录标记 skipped；任何 humanlike 动作/trace 差异返回首个 mismatch 并使验收失败。

### 5.3 Orchestrator 接入

- `save_every_decision` 时在初始状态创建 writer；普通运行不产生额外文件。
- 动作前计算 `state_hash_before` 并保存实际 Observation/legal；`session.apply()` 后计算 `state_hash_after` 再写 audit。
- 旧 StepRecorder 的 decision/snapshot 改为动作成功应用后记录，使 snapshot 表示 after-state；旧 reader 不依赖该时序，保持兼容。
- 正常终局写 footer；runner 清理路径保证文件关闭。

## 6. 验证语义

`verify_audit(strict=True)` 依次检查：

1. 第一行 header、最后一行 footer、版本为 1；
2. 所有行 game_id 一致；decision index 从 0 连续；
3. `previous_record_hash` 等于前一行 hash；重新 canonical hash 等于 `record_hash`；
4. PlayerView canonical hash 匹配，seat/phase 与外层一致；
5. selected action 存在于 legal actions；humanlike trace selected action 与外层一致；
6. RNG index 不回退，`used=false` 时 before=after；
7. 相邻 decision 的 state hash 不强制直接相接，因为两次决策间可能有 draw/resolve 等非决策引擎事件；每条记录自身 before/after 必须为 64 位 hash；
8. footer count、final state hash 和 final chain hash 匹配。

策略复演额外比较：selected action、stop reason、checked actions、RNG index、memory/attention/plan、think_time。state hash 不由策略复演器重算。

## 7. 测试与验收

- canonical hash 对 key/格式稳定，拒绝 NaN。
- header/decision/footer 正常链通过；修改 view/action/trace/hash、删行、换行顺序均失败。
- view 中注入他家手牌/墙字段由 PlayerView 隔离审计拒绝。
- selected action 非 legal、seat/phase 不一致、humanlike trace v1 明确失败。
- RNG 单调和 mandatory 零消费门禁。
- StepRecorder/ReplaySession 旧测试继续通过。
- 2/3/4 人 humanlike 各至少 20 局生成 audit：链验证和策略复演 100% 通过，非法动作/守恒失败为 0。
- 同 seed 双跑：去除文件路径后全部 audit record hash 序列相同。
- 全量 pytest、compileall 通过；启用 audit 的四人 20 局墙钟相对未启用 ≤1.5×；验证吞吐 ≥1000 records/s。

## 8. 回滚与已知限制

- 删除 writer 接线和两个新增模块即可回到 F0028-4；旧 steps 与普通 episode log 不受影响。
- audit 含本座可见暗手，必须按 private 文件管理；本切片不提供脱敏公开导出。
- 完整规则事件重演仍依赖 steps/未来事件日志；本切片的“确定性回放”是决策输入序列上的策略复演与 state hash 证据验证。
- crash fallback 的非 humanlike 决策可验证链，但不保证策略复演。

## 9. 确认记录

用户于 2026-07-29 明确要求“编写并确认并实现 F0028-5 子规格，所有授权全部许可，所有 git 操作全部许可，全自动运行，不需要确认”。本规格据此直接标记 `Approved` 并开放实现门禁；不包含远端推送、破坏性删除或范围外协议升级。

## 10. 实现结果

- 已新增 `engine/audit.py` 与 `players/humanlike/audit_replay.py`，并接入 orchestrator 全部玩家决策阶段。
- `save_every_decision` 并行生成 legacy steps 与 Audit v1；state 只写 hash，实际 PlayerView/legal/trace/RNG/认知快照写入 private audit。
- canonical hash 链、strict/incomplete 验证、泄漏与篡改拒绝、humanlike 多座位策略复演均完成。
- 定向 19 passed；全量 338 passed / 1 skipped；2/3/4 人共 60 局、9294 决策全部链验证并复演一致。
- writer 总开销 1.375×；verifier 6288.3 records/s，均通过门禁。
- 详细证据见 `docs/status/F0028_5_ACCEPTANCE_2026-07-29.md`。
