# 进度快照

> 2026-07-28 — **F0028-1 配置与参数追踪基座 Done；下一步 F0028-2 子规格**

## 当前状态

| 项 | 状态 |
|----|------|
| 应用版本 | 0.2.1（`version.py`，本轮未变） |
| 规格主线 | M01–M11 Done；F0001–F0027 已实现；F0028 `In Progress` |
| F0028-1 | **Done**：27 GP、33 RP、60 条追踪映射、版本兼容矩阵；默认配置 hash `6c4f54ca…b06ee37` |
| F0028-2 | 待先补充并批准实体牌 / 事件断言 / PlayerView v2 子规格 |
| Git | 本地 `main` 恢复基线可用；本轮实现尚待提交；远端零 refs/非法 HEAD，未推送 |
| 测试门禁 | F0028-1 定向 12 passed；最终提交全量 **291 passed / 1 skipped**（27.29s） |
| 冲突副本 | 52 个 `*Moff的Mac Studio*` 文件仍保留；未删除 |

## 本轮已完成

- 在 F0028 主规格追加字段级 GP/RP 映射、失败契约和规范化 hash 契约，再进入编码。
- 新增 `configs/humanlike_v2/default.json`，完整声明 GP-001–GP-027 和四个中性普通水平 profile。
- 新增 `compatibility.json`，未知 RULES/PARAMS/IMPL 组合明确失败。
- 新增不可变 `GlobalParameters`、`PlayerProfile`、`HumanlikeConfig`；实现枚举、范围、固定值和权重归一校验。
- 新增 `RoundRuntime`，注册 RP-001–RP-033 并提供建局、事件、决策、终局受控入口。
- 新增 60 条无缺失、无重号的参数追踪记录。
- 新增 12 个定向测试；全量回归无新增失败。
- 未注册 `humanlike_v2` 玩家，未修改 engine/state/persistence/wire，未跨入 F0028-2。

## 下一步完整队列

| 序 | 动作 | 产出 / 依赖 | 建议触发语 |
|----|------|-------------|------------|
| 1 | 编写 F0028-2 子规格（立即下一步） | 实体牌兼容迁移、事件断言、PlayerView v2 白名单与验收；依赖 F0028-1 Done | `编写 F0028-2 实体牌与 PlayerView v2 子规格` |
| 2 | 确认 F0028-2 | 子规格 `Review → Approved`；确认 schema/format 是否升级 | `确认 F0028-2 方案` |
| 3 | 实现并验收 F0028-2 | 108 张实体 ID 守恒、视图泄漏为 0、老存档确定迁移 | `实现 F0028-2` |
| 4 | 依次实施 F0028-3–6 | 基础策略 → 有限认知 → 回放审计 → 训练契约；每切片先子规格 | `编写 F0028-3 子规格` |
| 5 | 推送本地恢复基线 | 外部状态变更；需确认远端零 refs 后显式授权 | `将恢复后的 main 推送到 origin` |
| 6 | 整理 OneDrive 冲突副本 | 先出保留/删除清单；删除前需授权 | `整理 OneDrive 冲突副本，先出清单` |

## 风险与边界

- 当前配置基座尚未适配既有 `EngineConfig`，该适配属于后续引擎接入切片；不能形成两个相互冲突的规则权威。
- `RoundRuntime` 当前承载 RP 生命周期和不透明 payload；各 RP 的领域计算将在 F0028-2–4 分属模块实现。
- 本地 Git 位于 OneDrive，普通 `git status/commit` 可能因云端资产水合而变慢；远端仍未推送。
