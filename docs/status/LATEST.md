# 进度快照

> 2026-07-29 — **F0030 逐玩家认知与目标参数 Done**

## 当前状态

| 项 | 状态 |
|----|------|
| 应用版本 | 0.2.1（本轮未变） |
| 规格主线 | F0028–F0030 均 `Done` |
| 版本线 | state 5 / persistence 1 / wire 1 / PlayerView 2 / PARAMS 1.1 / IMPL 2.1 |
| 测试门禁 | 356 passed / 1 skipped in 29.73s；F0030 定向 37 passed |
| 批跑门禁 | F0028-6：2/3/4 人各 50 局，共 150 局、10,950 决策样本，零非法动作 |
| 性能门禁 | F0028-6：obs+mask p95 0.4917ms；v2/v1 环境 1.0847×，均通过 |
| 人工测试 | 快速集通过；MT-04 确认进入定缺并正常出牌；MT-03 策略列表显示待非阻塞补验 |
| Git | F0029 Draft/Approved 已提交；实现与验收待本轮收尾提交；远端未推送 |

## 本轮已完成

- F0030 `Approved → Done`：GP-024–027 已从全局迁移为 S0–S3 独立认知与目标参数。
- Humanlike 玩家只读取本座参数，trace/audit 写入逐座 `player_config_hash`。
- 旧 PARAMS 1.0 / IMPL 2.0 配置可确定性深拷贝迁移；新权威版本为 PARAMS 1.1 / IMPL 2.1。
- 设置窗口无全局认知页；244 总控件中 112 个为逐座认知/目标字段。
- 全量 356 passed / 1 skipped；2/3/4 人各 10 局批跑通过。

- 审计确认 GP-024–027 当前位于 `global_parameters`，四个玩家运行时共同读取，用户指出的问题属实。
- 新增 F0030 Draft：GP-001–023 保持全局；GP-024–027 迁移到 S0–S3 各自 `cognitive_parameters`。
- 明确 PARAMS/IMPL 版本升级、旧配置深拷贝迁移、canonical hash、审计复演和设置窗口改造边界。
- 本轮未越过 Approved 门禁修改配置结构或策略代码。

- 修复参数窗口底部按钮白底白字：统一浅色背景与深色文字。
- 遍历 validator：全部可调数值展示明确范围/关联约束，自由文本展示长度或非空规则。
- 所有枚举型文本改为只读下拉框；真实 GUI 共 34 个下拉框，输出 `controls-ok`。
- 全量 353 passed / 1 skipped。

- 修正 F0029 偏差：移除整份 JSON 文档编辑模式，改为 5 个中文分组、156 个逐项参数控件。
- 每项显示中文名称、作用和范围；布尔开关、枚举下拉、数值输入、锁定禁用均已接入。
- 真实 GUI 输出 `chinese-form-ok`；全量 352 passed / 1 skipped。

- F0029 `Approved → Done`：大厅、主桌控制面板、AI 座位窗均有 Humanlike v2 开关和参数入口。
- 新增独立 Tk 全参数编辑器与配置服务，覆盖 GP-001–027、S0–S3、顶层版本/ruleset/seed。
- 保存复用严格 validator，并使用备份、fsync 与原子替换；当前局不热更新，下一局生效。
- 定向 6 passed；全量 352 passed / 1 skipped；真实 Tk 启动与大厅多尺寸布局通过。

- 检查大厅、主程序、AI 座位窗、策略预设和 Humanlike 配置加载链。
- 确认 `humanlike_v2` 已在动态策略列表中，但大厅无显式全局开关，AI 窗口无独立开关和参数入口。
- 新增 F0029 Draft：大厅/主桌/AI 座位开关，以及覆盖 GP-001–027、四座 profile、顶层字段的独立参数窗口。
- 规定锁定项只读、合法项可编辑、原子保存/备份/并发保护和下局生效；本轮未越过 Approved 门禁修改代码。

- F0028-6 `Approved → Done`：固定 635 动作 codec/mask、Observation v2、非法动作契约、奖励分解和训练指标全部实现。
- v1 保持默认和 legal-list index 语义；v2 显式 opt-in，响应 HU 的上下文牌在 env 边界恢复。
- 定向 18 passed；全量 347 passed / 1 skipped；2/3/4 人各 50 局零非法动作。
- obs+mask p95 0.4917ms；30 局 v2/v1=1.0847×，通过性能门禁。
- F0028-1–6 全部完成，父功能 F0028 更新为 `Done`。

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
| 1 | 执行 F0030 GUI 人工验收（立即下一步） | 四座独立修改、保存及下局生效 | `执行 F0030 人工测试` |
| 2 | 补验 F0028 完整人工场景 | MT-06～17、2/3 人、认知/审计/训练体感 | `继续执行 F0028 完整人工测试` |
| 3 | 验证真实历史存档 | schema 1–4 真实夹具和迁移报告 | `导入并验证真实历史存档夹具` |
| 4 | 规划发版或下一功能 | 依赖人工验收 | `准备发布` 或 `规划下一功能` |
