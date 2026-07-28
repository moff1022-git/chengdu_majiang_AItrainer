# 进度快照

> 2026-07-29 — **F0028-4 有限认知子规格 Approved，进入自动实现**

## 当前状态

| 项 | 状态 |
|----|------|
| 应用版本 | 0.2.1（本轮未变） |
| 规格主线 | F0028 `In Progress`；F0028-1–3 `Done`；F0028-4 `Approved` |
| 版本线 | state schema 5（reader 1–5）/ persistence 1 / wire 1 / PlayerView 2 |
| 测试门禁 | 322 passed / 1 skipped in 30.76s；Human 混合换牌定向 23 passed |
| 批跑门禁 | 2/3/4 人各 50 局，共 150 局、23392 次决策，零策略崩溃/非法动作 |
| 性能门禁 | 单决策 p95 2.87 ms；相对 RuleAI 2.222×，均通过 |
| 人工测试 | 快速集通过；MT-04 确认进入定缺并正常出牌；MT-03 策略列表显示待非阻塞补验 |
| Git | Human 换三张修复已纳入本地 `main` 基线；远端未推送 |

## 本轮已完成

- 新增并批准 F0028-4 字段级子规格，锁定认知状态、人格、注意力、记忆、满意停止、有界噪声和思考时间契约。
- 用户授权本切片全程自动实现；Docs-First 实现门禁已开放。

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
- 人类差异、记忆、注意力、满意停止和噪声仍属 F0028-4，不能提前加入本基线。
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
| 1 | 实现并验收 F0028-4（立即执行） | 四个认知模块、玩家接线、测试与验收报告；依赖规格 Approved | 已自动执行 |
| 2 | 补验 F0028-3 MT-03 与完整人工场景 | 策略显示、MT-06～17、2/3 人与性能体感 | `继续执行 F0028-3 完整人工测试` |
| 3 | 编写、确认并实现 F0028-5–6 | 审计回放 → 训练契约；依赖 F0028-4 Done | 按对应 F 编号触发 |
| 4 | 验证真实历史存档 | schema 1–4 真实夹具和迁移报告；发布前建议完成 | `导入并验证真实历史存档夹具` |
| 5 | 推送本地 main | 外部状态变更，需显式授权 | `将恢复后的 main 推送到 origin` |
| 6 | 整理 OneDrive 冲突副本 | 先只读列清单；删除另行授权 | `整理 OneDrive 冲突副本，先出清单` |
