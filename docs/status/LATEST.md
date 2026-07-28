# 进度快照

> 2026-07-29 — **F0028-6 训练契约 v2 子规格 Approved，进入自动实现**

## 当前状态

| 项 | 状态 |
|----|------|
| 应用版本 | 0.2.1（本轮未变） |
| 规格主线 | F0028 `In Progress`；F0028-1–5 `Done`；F0028-6 `Approved` |
| 版本线 | state schema 5（reader 1–5）/ persistence 1 / wire 1 / PlayerView 2 |
| 测试门禁 | 338 passed / 1 skipped in 29.55s；F0028-5 定向 19 passed；compileall 通过 |
| 批跑门禁 | F0028-4：2/3/4 人各 50 局，共 150 局，零策略崩溃/非法动作 |
| 性能门禁 | F0028-4：单决策 p95 1.1968 ms；相对 RuleAI 2.50×，均通过 |
| 人工测试 | 快速集通过；MT-04 确认进入定缺并正常出牌；MT-03 策略列表显示待非阻塞补验 |
| Git | F0028-5 Docs-First 规格、实现与验收已纳入本地 `main` 基线；远端未推送 |

## 本轮已完成

- 新增并批准 F0028-6：635 项固定动作 codec/mask、Observation v2、非法动作契约、奖励分解与训练指标。
- 用户授权本切片文档、实现、测试和本地 Git 全自动执行；Docs-First 门禁开放。

- F0028-5 子规格按用户自动授权完成 `Approved → Done`。
- 新增 private Audit v1 writer/reader/verifier、canonical SHA-256 链、state/view/config hash、认知/RNG 快照。
- orchestrator 覆盖换三张、定缺、出牌和响应决策；旧 steps/ReplaySession 保持兼容。
- 新增 humanlike 多 seat 策略输入序列复演；2/3/4 人共 60 局、9294 决策全部匹配。
- 篡改、截断、泄漏、非法动作、RNG 回退和同局双跑门禁通过。
- audit+steps 写入开销 1.375×；verifier 6288.3 records/s。

- F0028-4 子规格按用户预授权完成 `Approved → Done`。
- 新增公开信息 MemoryStore、Top-K AttentionSelector、持续 CognitiveState 和 CognitivePolicy。
- 落地 level/style 人格差异、计划惯性/重启、轻度情绪、满意停止、SHA-256 有界噪声和不 sleep 的思考时间。
- DecisionTrace v2 与 RP-024–029 接入；PlayerView-only / legal-only / mandatory 不变量保持。
- 2/3/4 人各 50 局共 150 局零策略崩溃/非法动作；双跑和跨 hash seed 复现通过。
- 单决策 p95 1.1968 ms；20 局相对 RuleAI 2.50×，均通过性能门禁。

- 新增纯 PlayerView 的 DecisionContext、PublicBelief、HandFeatures、PlanSnapshot、CandidateSet 和 EvaluationResult。
- 新增选配 HumanlikeV2Player，并通过 registry 与策略 presets 接入 CLI/大厅装配链。
- mandatory 不受 GP-026 上限裁剪；ordinary 按预评分和稳定动作键裁剪。
- 四分量 Q(action) 量化至 8 位；DecisionTrace v1 标记 `rng_used=false`。
- RoundRuntime 写入 RP-014/015/016/017/018/023/026/029，不进入 GameState。
- orchestrator 不再向 humanlike_v2 注入 `_engine_state`；Oracle/GameState 全知入口隔离测试通过。
- 跨 PYTHONHASHSEED 1/777 的动作摘要一致。
- F0028-3 `Approved → Done`，验收报告已落盘。

## 实现差异与风险

- Observation 仍是 wire 1 legacy mapping；策略按 PlayerView v2 白名单重建冻结对象，没有升级协议。
- 被认领弃牌须在公开计数中与副露去重；现已覆盖自动测试和批跑。
- 当前 belief 是确定性公开启发式，不输出精确他手；F0010/F0011 全知入口未复用。
- 认知/RNG 已进入 private audit 并可策略复演；尚未进入普通 GameState/persistence save。
- 默认四座仍均为 normal/balanced；多 profile 产品配置尚未启用。
- 远端未推送；OneDrive 可能拖慢 Git 扫描。

## 快速人工验收结果

- MT-01 四 humanlike_v2 完整局通过，自然 wall_empty，无异常关键字。
- MT-02 固定 game_id 双跑 209 个决策完全一致，动作摘要 `529c9502…b614`。
- MT-03 四观察窗创建 errors=0，用户反馈牌局正常；策略列表显示项尚未单独回报。
- MT-05 rule_ai/current_s2 均自然完成，旧 AI 回归通过。
- MT-04 原阻塞已修复：Human face Tile 在 opening 提交边界确定性解析为本手 PhysicalTile；pending/offers/目标手牌不再混用类型。
- 修复自动验收为定向 23 passed、全量 322 passed / 1 skipped；GUI 复测日志未复现异常。
- 用户确认 MT-04 已进入定缺并正常出牌；原 Blocker 清零，快速人工验收判定 **Pass**。
- MT-03 策略列表显示项尚未单独确认，保留为完整人工测试非阻塞补验。
- 已纠正测试口径：private steps 快照包含全状态是预期行为，不作为 PlayerView 泄漏判据。

## 下一步完整队列

| 序 | 动作 | 产出 / 依赖 | 建议触发语 |
|----|------|-------------|------------|
| 1 | 实现并验收 F0028-6（立即执行） | codec/mask、obs v2、reward/metrics、批跑报告 | 已自动执行 |
| 2 | 补验 F0028-3–5 完整人工场景 | 策略显示、MT-06～17、2/3 人、认知与审计体感 | `继续执行 F0028 完整人工测试` |
| 3 | 实现并验收 F0028-6 | 训练契约闭环 | `实现 F0028-6` |
| 4 | 验证真实历史存档 | schema 1–4 真实夹具和迁移报告；发布前建议完成 | `导入并验证真实历史存档夹具` |
| 5 | 推送本地 main | 外部状态变更，需显式授权 | `将恢复后的 main 推送到 origin` |
| 6 | 整理 OneDrive 冲突副本 | 先只读列清单；删除另行授权 | `整理 OneDrive 冲突副本，先出清单` |
