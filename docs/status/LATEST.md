# 进度快照

> 2026-07-28 — **F0028-2 子规格已编写至 Review；等待确认后才能实现**

## 当前状态

| 项 | 状态 |
|----|------|
| 应用版本 | 0.2.1（本轮未变） |
| 规格主线 | F0028 `In Progress`；F0028-1 `Done`；F0028-2 `Review` |
| F0028-1 | 27 GP、33 RP、60 条追踪映射、兼容矩阵和稳定配置 hash 已实现 |
| F0028-2 | 子规格完成；本轮无业务代码、无 schema/protocol 实际变更 |
| 测试门禁 | 沿用最终提交基线：291 passed / 1 skipped；本轮文档-only 未重跑 |
| Git | 本地 `main` 基线可用；本轮文档待提交；远端仍为空且未推送 |

## 本轮已完成

- 逐项核对现有 `Tile`、Deck、GameState schema 4、persistence format 1、event、view filter 和 wire protocol 1。
- 新增 `docs/features/F0028_2_physical_tiles_player_view_v2.md`，状态 `Review`。
- 区分实体牌所有权区域与 discard/event/last tile 等历史引用，避免碰杠后重复计数。
- 提议 `state schema 5 / persistence format 1 / wire protocol 1 / PlayerView 2` 版本组合。
- 设计 schema 1–4 确定性迁移、坏档失败和不覆盖旧文件的契约。
- 定义原子事件边界断言、108 张守恒、账本/状态机/合法动作检查。
- 定义 GP-021 八项 hidden/partial/exact 可见性矩阵和 legacy UI/wire 投影。
- 将训练 oracle 真值从普通 PlayerView/Observation 中分离为 training-only API。
- 未修改 engine、protocols、players、training 或 tests，符合 docs-first 门禁。

## 待确认决议

1. GameState 新 writer 升 schema 5，reader 保持支持 schema 1–5。
2. persistence 外壳保持 format 1；Human NDJSON 保持 wire 1；PlayerView 独立标记 version 2。
3. Action v1 继续表达 face，resolver 按最小 tile_id 选择合法实体副本。
4. 旧 `filter_state_for_seat` 保留 API，但改为白名单 builder 的兼容投影。
5. oracle 真值完全移出 Observation.view。

## 下一步完整队列

| 序 | 动作 | 产出 / 依赖 | 建议触发语 |
|----|------|-------------|------------|
| 1 | 确认 F0028-2（立即下一步） | 子规格 `Review → Approved`，锁定五项版本/兼容决议 | `确认 F0028-2 方案` |
| 2 | 实现 F0028-2 | PhysicalTile、schema 5 迁移、强类型所有权、事件断言、PlayerView v2、oracle 分离 | `实现 F0028-2` |
| 3 | 验收并回写 F0028-2 | 108 张守恒、泄漏 0、旧档迁移、2/3/4 人和全量回归、性能报告 | 实现任务内自动完成 |
| 4 | 编写 F0028-3 子规格 | 只读 PlayerView 的确定性基础策略 | `编写 F0028-3 子规格` |
| 5 | 推送本地恢复基线 | 外部状态变更；需显式授权 | `将恢复后的 main 推送到 origin` |
| 6 | 整理 OneDrive 冲突副本 | 先出清单；删除需授权 | `整理 OneDrive 冲突副本，先出清单` |

## 风险与边界

- 实体牌会触及 state、play、存档、UI 和训练，是 F0028 风险最高的切片；必须按子规格七步实施，不可一次性重写。
- 旧 schema 的 meld/discard 没有实体信息；迁移必须固定顺序并在无法守恒时失败，不能猜测。
- F0028-2 尚未 Approved，当前禁止修改业务代码。
- 远端 Git 仍未推送；OneDrive 云端资产可能拖慢普通 Git 工作树扫描。
