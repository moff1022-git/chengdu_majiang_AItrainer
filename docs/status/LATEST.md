# 进度快照

> 2026-07-29 — **F0028-3 子规格已编写，状态 Review；下一步确认方案**

## 当前状态

| 项 | 状态 |
|----|------|
| 应用版本 | 0.2.1（本轮未变） |
| 规格主线 | F0028 `In Progress`；F0028-1–2 `Done`；F0028-3 `Review` |
| 版本线 | state schema 5（reader 1–5）/ persistence 1 / wire 1 / PlayerView 2 |
| 最近测试门禁 | F0028-2：308 passed / 1 skipped；本轮仅文档，未重跑测试 |
| Git | F0028-2 本地提交 `0c82c78`；本轮 F0028-3 文档变更待提交；远端未推送 |

## 本轮已完成

- 新增 `docs/features/F0028_3_deterministic_player_view_policy.md`，状态 `Review`。
- 明确 `humanlike_v2` 只能读取 PlayerView v2、ActionRequest、批准配置和自身 RoundRuntime。
- 锁定换牌、定缺、响应、出牌四阶段的确定性候选与评价框架。
- mandatory 不受 GP-026 候选上限裁剪；普通候选以显式稳定键决胜。
- Q(action) 使用 speed / hand_value / defense / flexibility 四分量，量化到 8 位，不消费 RNG。
- 定义内存 DecisionTrace v1 和 RP-014/015/016/017/018/023/026/029 映射。
- 明确禁止 `_engine_state`、GameState 全知分析和 TrainingTruth/Oracle；加入隐藏真值不变性与跨 PYTHONHASHSEED 门禁。
- 本轮仅更新规格、索引、基线、changelog 和 PLAN，未修改业务代码。

## 待确认的六项决议

1. 仅不可过胡为 mandatory；可过胡进入效用比较。
2. GP-026 只裁剪 ordinary，不裁剪 mandatory。
3. F0028-3 不消费 RNG，trace 记 `rng_used=false`。
4. belief 不输出精确他手，只输出公开计数、花色压力和危险度。
5. DecisionTrace v1 本轮只作内存契约；持久化归 F0028-5。
6. 版本保持 state 5 / PlayerView 2 / persistence 1 / wire 1。

## 风险与边界

- 现有 F0010/F0011 部分入口接受全知 GameState；实现时只能拆出纯可见输入函数，不能直接复用全知入口。
- `humanlike_v2` 注册涉及现有玩家工厂、CLI/大厅枚举，必须保持 rule_ai/current_s2 默认行为不变。
- 性能门禁要求 4 人单决策 p95 ≤20 ms，且批跑墙钟不超过同提交 rule_ai 的 3 倍。
- OneDrive 可能拖慢 Git 扫描；远端仍未推送。

## 下一步完整队列

| 序 | 动作 | 产出 / 依赖 | 建议触发语 |
|----|------|-------------|------------|
| 1 | 确认 F0028-3（立即下一步） | 六项决议锁定，子规格 Review → Approved；不写代码 | `确认 F0028-3 方案` |
| 2 | 实现并验收 F0028-3 | 选配 humanlike_v2、纯 PlayerView 特征/候选/评价、2/3/4 人批跑及验收报告；依赖 Approved | `实现 F0028-3` |
| 3 | 编写并确认 F0028-4 子规格 | 有限认知、人格、注意力、记忆、满意停止与有界噪声；依赖 F0028-3 Done | `编写 F0028-4 子规格` |
| 4 | 实现并验收 F0028-4 | 可复现的人类化差异层；依赖 F0028-4 Approved | `实现 F0028-4` |
| 5 | 依次推进 F0028-5–6 | 审计回放 → 训练契约；每切片先规格后实现 | 按对应 F 编号触发 |
| 6 | 验证真实历史存档 | schema 1–4 真实夹具和迁移报告；发布前建议完成 | `导入并验证真实历史存档夹具` |
| 7 | 推送本地 main | 外部状态变更，需显式授权 | `将恢复后的 main 推送到 origin` |
| 8 | 整理 OneDrive 冲突副本 | 先只读列清单；删除另行授权 | `整理 OneDrive 冲突副本，先出清单` |
