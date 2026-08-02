# 架构决策记录（ADR）

重大、跨模块、难以轻易回退的决策写入本目录。

命名：`NNNN-<slug>.md`（如 `0001-human-subprocess.md`）。

## 已有决策（自 PLAN Review 迁入）

以下决议已在 `PLAN.md` 确认；需要时可补写正式 ADR 文件便于检索。

| 编号 | 决策 | 状态 |
|------|------|------|
| （基线） | 骰子定庄 + 独立 game_id 复现 | Accepted |
| （基线） | 默认一炮多响 | Accepted |
| （基线） | 首版含换三张 | Accepted |
| （基线） | 成都血战番型 + 可配置 fan_cap | Accepted |
| （基线） | Human 子进程隔离 | Accepted |
| （基线） | 2/3/4 人规则路径一致 | Accepted |
| （基线） | 允许 numpy | Accepted |
| （基线） | **Docs-First 开发流程** | Accepted（见 DEVELOPMENT.md） |
| ADR-0001 | [Agent 编排的无人值守开发流程](0001-agent-orchestrated-unattended-development.md) | Accepted |

新决策：先写 `NNNN-*.md`（Proposed）→ 确认 Accepted → 再改代码。
