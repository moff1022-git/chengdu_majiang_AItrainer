# 进度快照

> 2026-07-28 — **F0028-2 Done；下一步编写 F0028-3 确定性基础策略子规格**

## 当前状态

| 项 | 状态 |
|----|------|
| 应用版本 | 0.2.1（本轮未变） |
| 规格主线 | F0028 `In Progress`；F0028-1–2 `Done`；F0028-3 待子规格 |
| 版本线 | state schema **5**（reader 1–5）/ persistence **1** / wire **1** / PlayerView **2** |
| 测试门禁 | **308 passed / 1 skipped in 28.26s**；compileall 通过 |
| 守恒门禁 | 2/3/4 人各 20 局，共 60 局，无断言失败 |
| 性能门禁 | PlayerView v2 -23.8%；四 RuleAI 断言抽样 -2.2%，均通过 |
| Git | 本轮实现待提交；远端仍为空且未推送 |

## 本轮已完成

- 新增 0–107 实体牌 ID，保持 `Tile` 牌面算法、Action、UI 和资源接口兼容。
- GameState writer 升 schema 5；schema 1–4 确定迁移，坏档明确失败且不覆盖原文件。
- 新增强类型 Meld、DiscardRecord，以及 wall/hand/meld/discard/transit/winning 所有权区域。
- 在发牌、换牌、摸打、碰杠胡和终局边界执行 108 张守恒及引用断言。
- 新增冻结 PlayerView v2 和显式白名单 builder；旧 view API 改为显式兼容投影。
- GP-021 八项 hidden/partial/exact 可见性有自动测试；哨兵私有字段泄漏为 0。
- 新增 training-only TrainingTruth；普通 Observation 和座位窗口不再携带 oracle 手牌。
- 新增只读 HumanlikeEngineAdapter，GP 与旧 EngineConfig 冲突时明确失败。
- F0028-2 `Approved → Done`，验收报告已落盘。

## 实现差异与风险

- 为多人点炮/抢杠胡增加 `winning_tile_ids` 终态所有权区域，是批准规格中“胡牌事件终态位置”的具体实现。
- F0010 局中预测仍工作，但座位窗口不再获得真实对手手牌，因此局中 oracle 准确率停止计算；离线评估保留。
- schema 5 属于新写出结构；发布前仍建议增加来自真实历史文件的 schema 1–4 固定夹具，而当前自动测试使用确定构造夹具。
- 远端 Git 仍未推送；OneDrive 可能拖慢 Git 扫描。

## 下一步完整队列

| 序 | 动作 | 产出 / 依赖 | 建议触发语 |
|----|------|-------------|------------|
| 1 | 编写 F0028-3 子规格（立即下一步） | 只读 PlayerView 的确定性基础策略、候选/评价/追踪接口；依赖 F0028-2 Done | `编写 F0028-3 子规格` |
| 2 | 确认 F0028-3 | 子规格 Review → Approved | `确认 F0028-3 方案` |
| 3 | 实现并验收 F0028-3 | humanlike_v2 选配 profile、合法动作率 100%、同 seed 同决策 | `实现 F0028-3` |
| 4 | 依次实施 F0028-4–6 | 有限认知 → 审计回放 → 训练契约；每切片先子规格 | 按对应 F 编号触发 |
| 5 | 推送本地恢复基线 | 外部状态变更；需显式授权 | `将恢复后的 main 推送到 origin` |
| 6 | 整理 OneDrive 冲突副本 | 先出清单；删除需授权 | `整理 OneDrive 冲突副本，先出清单` |
