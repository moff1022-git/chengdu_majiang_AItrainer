# 进度快照

> 2026-07-29 — **F0028-3 Done；人工测试方案已就绪，建议先执行快速验收**

## 当前状态

| 项 | 状态 |
|----|------|
| 应用版本 | 0.2.1（本轮未变） |
| 规格主线 | F0028 `In Progress`；F0028-1–3 `Done`；F0028-4 待子规格 |
| 版本线 | state schema 5（reader 1–5）/ persistence 1 / wire 1 / PlayerView 2 |
| 测试门禁 | 321 passed / 1 skipped in 29.24s；compileall 通过 |
| 批跑门禁 | 2/3/4 人各 50 局，共 150 局、23392 次决策，零策略崩溃/非法动作 |
| 性能门禁 | 单决策 p95 2.87 ms；相对 RuleAI 2.222×，均通过 |
| 人工测试 | `docs/testing/F0028_3_MANUAL_TEST_PLAN_2026-07-29.md` Ready，尚待人工执行 |
| Git | F0028-3 实现基线 `56ebc5c`；本轮测试方案待提交；远端未推送 |

## 本轮已完成

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

## 本轮补充：人工测试方案

- 新增 F0028-3 人工测试计划，快速集 MT-01～05 预计 20–30 分钟。
- 覆盖 CLI 四 AI、固定 game_id 重复、GUI 策略选择、Human 混合局和旧 AI 回归。
- 完整集补充碰杠胡/一炮多响/墙空场景、2/3 人、信息泄漏扫描和性能体感。
- 人工执行尚未发生；实际结果必须另建验收记录，不把方案编写等同于通过。

## 下一步完整队列

| 序 | 动作 | 产出 / 依赖 | 建议触发语 |
|----|------|-------------|------------|
| 1 | 执行 F0028-3 快速人工验收（立即下一步） | MT-01～05、截图/日志和人工验收记录；依赖可用 GUI 环境 | `按方案执行 F0028-3 快速人工测试` |
| 2 | 执行完整人工场景与隔离检查 | MT-06～17、2/3 人和性能体感；依赖快速集通过 | `继续执行 F0028-3 完整人工测试` |
| 3 | 编写 F0028-4 子规格 | CognitiveState、记忆/注意力、人格、满意停止、有界噪声、思考时间；依赖 F0028-3 Done | `编写 F0028-4 子规格` |
| 4 | 确认并实现 F0028-4 | 可复现人类化差异层及 profile 对比 | 按 F0028-4 触发 |
| 5 | 编写、确认并实现 F0028-5–6 | 审计回放 → 训练契约 | 按对应 F 编号触发 |
| 6 | 验证真实历史存档 | schema 1–4 真实夹具和迁移报告；发布前建议完成 | `导入并验证真实历史存档夹具` |
| 7 | 推送本地 main | 外部状态变更，需显式授权 | `将恢复后的 main 推送到 origin` |
| 8 | 整理 OneDrive 冲突副本 | 先只读列清单；删除另行授权 | `整理 OneDrive 冲突副本，先出清单` |
