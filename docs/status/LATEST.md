# 进度快照

> 2026-07-29 — **F0028-3 Done；下一步编写 F0028-4 有限认知子规格**

## 当前状态

| 项 | 状态 |
|----|------|
| 应用版本 | 0.2.1（本轮未变） |
| 规格主线 | F0028 `In Progress`；F0028-1–3 `Done`；F0028-4 待子规格 |
| 版本线 | state schema 5（reader 1–5）/ persistence 1 / wire 1 / PlayerView 2 |
| 测试门禁 | 321 passed / 1 skipped in 29.24s；compileall 通过 |
| 批跑门禁 | 2/3/4 人各 50 局，共 150 局、23392 次决策，零策略崩溃/非法动作 |
| 性能门禁 | 单决策 p95 2.87 ms；相对 RuleAI 2.222×，均通过 |
| Git | 上一基线 `28ec844`；本轮实现待提交；远端未推送 |

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

## 下一步完整队列

| 序 | 动作 | 产出 / 依赖 | 建议触发语 |
|----|------|-------------|------------|
| 1 | 编写 F0028-4 子规格（立即下一步） | CognitiveState、记忆/注意力、人格、满意停止、有界噪声、思考时间；依赖 F0028-3 Done | `编写 F0028-4 子规格` |
| 2 | 确认 F0028-4 | 子规格 Review → Approved | `确认 F0028-4 方案` |
| 3 | 实现并验收 F0028-4 | 可复现人类化差异层及 profile 对比；依赖 Approved | `实现 F0028-4` |
| 4 | 编写、确认并实现 F0028-5 | 持久化审计日志与确定性回放；依赖 F0028-4 Done | 按 F0028-5 触发 |
| 5 | 编写、确认并实现 F0028-6 | 训练动作空间、mask、奖励和回归评估；依赖 F0028-5 Done | 按 F0028-6 触发 |
| 6 | 验证真实历史存档 | schema 1–4 真实夹具和迁移报告；发布前建议完成 | `导入并验证真实历史存档夹具` |
| 7 | 推送本地 main | 外部状态变更，需显式授权 | `将恢复后的 main 推送到 origin` |
| 8 | 整理 OneDrive 冲突副本 | 先只读列清单；删除另行授权 | `整理 OneDrive 冲突副本，先出清单` |
