# 进度快照

> 2026-07-29 — **F0028-3 已批准；下一步按规格实现并验收**

## 当前状态

| 项 | 状态 |
|----|------|
| 应用版本 | 0.2.1（本轮未变） |
| 规格主线 | F0028 `In Progress`；F0028-1–2 `Done`；F0028-3 `Approved` |
| 版本线 | state schema 5（reader 1–5）/ persistence 1 / wire 1 / PlayerView 2 |
| 最近测试门禁 | F0028-2：308 passed / 1 skipped；本轮仅批准文档，未重跑测试 |
| Git | 上一基线 `89af3de`；本轮批准文档待提交；远端未推送 |

## 本轮已完成

- 用户确认 `docs/features/F0028_3_deterministic_player_view_policy.md`，状态 `Review → Approved`。
- 六项决议正式锁定：
  1. 仅不可过胡为 mandatory，可过胡进入效用比较；
  2. GP-026 只裁剪 ordinary，不裁剪 mandatory；
  3. 确定性基础策略不消费 RNG，trace 为 `rng_used=false`；
  4. belief 不输出精确他手，只输出公开计数、花色压力和危险度；
  5. DecisionTrace v1 本切片只定义内存契约，持久化归 F0028-5；
  6. 版本保持 state 5 / PlayerView 2 / persistence 1 / wire 1。
- 实现门禁已开放；本轮没有修改业务代码、配置或测试。

## 实现边界与风险

- `humanlike_v2` 只能读取 PlayerView v2、ActionRequest、批准配置和自身 RoundRuntime。
- 禁止 `_engine_state`、GameState 全知分析和 TrainingTruth/Oracle；F0010/F0011 只能拆出纯可见输入函数复用。
- 不得修改 `engine/blood_battle.py` 规则行为；若发现必须改变引擎或 PlayerView 字段，须先回到规格修订和重新确认。
- 实现验收需覆盖 2/3/4 人各至少 50 局、跨 PYTHONHASHSEED 复现、隐藏真值不变性及性能门禁。
- OneDrive 可能拖慢 Git；远端仍未推送。

## 下一步完整队列

| 序 | 动作 | 产出 / 依赖 | 建议触发语 |
|----|------|-------------|------------|
| 1 | 实现并验收 F0028-3（立即下一步） | humanlike_v2、纯 PlayerView 特征/候选/评价、测试、批跑和验收报告；依赖已满足 | `实现 F0028-3` |
| 2 | 编写并确认 F0028-4 子规格 | 有限认知、人格、注意力、记忆、满意停止与有界噪声；依赖 F0028-3 Done | `编写 F0028-4 子规格` |
| 3 | 实现并验收 F0028-4 | 可复现人类化差异层；依赖 F0028-4 Approved | `实现 F0028-4` |
| 4 | 依次推进 F0028-5–6 | 审计回放 → 训练契约；每个切片先规格、确认、实现、验收 | 按对应 F 编号触发 |
| 5 | 验证真实历史存档 | schema 1–4 真实夹具和迁移报告；发布前建议完成 | `导入并验证真实历史存档夹具` |
| 6 | 推送本地 main | 外部状态变更，需显式授权 | `将恢复后的 main 推送到 origin` |
| 7 | 整理 OneDrive 冲突副本 | 先只读列清单；删除另行授权 | `整理 OneDrive 冲突副本，先出清单` |
