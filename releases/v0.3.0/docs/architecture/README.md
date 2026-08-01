# 架构文档索引

系统级总设计见仓库根目录 **[`PLAN.md`](../../PLAN.md)**。

本目录用于：

- 跨模块补充说明（通信时序、状态机图、部署形态）
- 对 `PLAN.md` 的细化，避免总文档无限膨胀

| 文档 | 说明 |
|------|------|
| [`../../PLAN.md`](../../PLAN.md) | 产品目标、目录结构、规则模型、接口草图、Reward、里程碑 |
| [`../DEVELOPMENT.md`](../DEVELOPMENT.md) | 开发流程（文档先行） |
| [`../milestones/`](../milestones/) | 分步实现规格 |
| [`../features/`](../features/) | 里程碑外功能变更（如 [F0001 窗口几何](../features/F0001_window_geometry.md)） |
| [`../adr/`](../adr/) | 架构决策记录 |

新增架构说明时：先建 md，再在实现里程碑中引用。
