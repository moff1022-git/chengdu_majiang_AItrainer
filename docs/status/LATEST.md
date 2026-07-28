# 进度快照

> 2026-07-28 — **F0028-2 已 Approved；等待明确实现指令**

## 当前状态

| 项 | 状态 |
|----|------|
| 应用版本 | 0.2.1（本轮未变） |
| 规格主线 | F0028 `In Progress`；F0028-1 `Done`；F0028-2 `Approved`、待实现 |
| F0028-1 | 27 GP、33 RP、60 条追踪映射、兼容矩阵和稳定配置 hash 已实现 |
| F0028-2 | 五项版本/兼容决议已锁定；尚无实体牌、schema 5 或 PlayerView v2 代码 |
| 测试门禁 | 沿用最终提交基线：291 passed / 1 skipped；本轮文档-only 未重跑 |
| Git | 本地 `main` 基线可用；本轮审批文档待提交；远端仍为空且未推送 |

## 本轮已完成

- 用户确认 `docs/features/F0028_2_physical_tiles_player_view_v2.md`，状态 `Review → Approved`。
- 锁定 GameState 新 writer 使用 schema 5，reader 支持 schema 1–5。
- 锁定 persistence format 保持 1、Human NDJSON wire protocol 保持 1、PlayerView 独立标记 version 2。
- 锁定 Action v1 继续表达 face，由 resolver 按合法所有权区域最小 tile_id 选择实体副本。
- 锁定旧 `filter_state_for_seat` API 保留，但实现改为白名单 builder 的兼容投影。
- 锁定 oracle 真值完全移出普通 `Observation.view`，仅通过 training-only API 获取。
- 本轮只更新规格、索引、changelog 和状态基线；未修改业务代码或测试。

## 下一步完整队列

| 序 | 动作 | 产出 / 依赖 | 建议触发语 |
|----|------|-------------|------------|
| 1 | 实现 F0028-2（立即下一步） | PhysicalTile、schema 5 迁移、所有权区域、原子事件断言、PlayerView v2、oracle 分离；依赖已满足 | `实现 F0028-2` |
| 2 | 验收并回写 F0028-2 | 108 张守恒、泄漏 0、schema 1–4 迁移、2/3/4 人、全量兼容与性能报告 | 实现任务内自动完成 |
| 3 | 编写 F0028-3 子规格 | 只读 PlayerView 的确定性基础策略；依赖 F0028-2 Done | `编写 F0028-3 子规格` |
| 4 | 确认并实现 F0028-3 | 子规格 Approved 后接入 `humanlike_v2` 选配 profile | 后续按文档触发 |
| 5 | 依次实施 F0028-4–6 | 有限认知 → 审计回放 → 训练契约 | 每切片先子规格 |
| 6 | 推送本地恢复基线 | 外部状态变更；需显式授权 | `将恢复后的 main 推送到 origin` |
| 7 | 整理 OneDrive 冲突副本 | 先出清单；删除需授权 | `整理 OneDrive 冲突副本，先出清单` |

## 风险与边界

- F0028-2 是高风险跨模块切片，实施必须按已批准的七步顺序推进并在每步跑定向门禁。
- 旧 schema meld/discard 没有实体身份；迁移无法守恒时必须失败，不能猜测或覆盖原文件。
- 规格已 Approved，但本轮“确认文档”不包含编码授权；当前代码仍是 schema 4 / persistence 1 / wire 1。
- 远端 Git 仍未推送；OneDrive 云端资产可能拖慢普通 Git 工作树扫描。
