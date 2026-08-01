# 下一步任务计划

更新时间：2026-08-01
依据：Task 19 tracker/runtime/orchestrator、F0035、PLAN.md、Docs-First 约定

## 当前基线

- Task 19 工程证据：96/96 units `AUDITED`，14/14 waves 完成，40/40 batches 完成。
- MODEL-001：工程审计已通过；外部校准是程序完成后的独立功能，不阻塞 `AUDITED`。模拟数据标记 `SIMULATION`，运行期人类数据标记 `HUMAN`。
- 没有未完成的 Task 19 orchestrator work item；后续工作进入项目后续里程碑，不得重新打开已审计单元，除非出现回归或新规格。
- F0031、F0032、F0033、F0025 仍为 Draft；按仓库规则，未批准前只可评审/补规格，不写对应业务代码。

## 有序队列

| 优先级 | 任务 | 产出 | 依赖 | 触发语/门禁 |
|---:|---|---|---|---|
| 1 | Task 19 收尾归档 | 校验 tracker 96/96、runtime、orchestrator、LATEST/changelog 一致；形成最终 checkpoint | 当前 96/96 证据 | `完成 Task 19 收尾归档` |
| 2 | MODEL-001 独立校准工具 | SIMULATION/HUMAN 数据选择、指标报告、分组泄漏报告、fallback 对照；不改变 AUDITED | F0035 Approved；现有 validator | `实现 MODEL-001 独立校准功能` |
| 3 | 运行期 HUMAN 数据采集准备 | 脱敏、同意/provenance、保留/删除策略、导出 manifest；不影响实时决策 | F0035；隐私与数据来源决策 | `设计 MODEL-001 人类数据采集` |
| 4 | F0031 量化验收规格 | 完成 Draft→Approved，锁定条款、阈值、golden cases 和外部数据边界 | AU crosswalk、F0032 数据契约 | `批准 F0031` |
| 5 | F0032 评估数据集规格 | 完成 Draft→Approved，锁定 schema、动作映射、切分、隐私和版本契约 | F0031 口径对齐 | `批准 F0032` |
| 6 | F0033 总体软件设计 | 完成 Draft→Approved，解决与已实现代码的 baseline 差异 | F0031/F0032 crosswalk、DOC_CODE_BASELINE | `批准 F0033` |
| 7 | F0031/F0032/F0033 实现 | 按批准规格分批实现、测试、复审、审计 | 各规格 Approved | `实现 F003x` |
| 8 | F0025 Windows 打包 | Windows 主机构建、安装/升级/卸载验收和发布文档 | F0025 Approved、Windows 环境 | `批准并实现 F0025` |

## 自动化规则

- 已批准且语义明确的任务自动执行：实现→测试→修复→复审→独立审计→文档同步。
- 校准工具可对 `SIMULATION` 立即运行；`HUMAN` 数据必须通过授权、脱敏、provenance 和泄漏门禁。
- 外部有效性、真人相似性或产品新语义不能由模拟数据推断；遇到真正人工门禁才暂停。
- 每轮结束必须更新 `docs/status/LATEST.md` 和有实质交付时更新 `docs/changelog.md`。

## 风险

- `LATEST.md` 前部包含历史快照；以文件末尾最新记录、tracker 行级重算和 monitor 当前输出为准。
- F0033/F0031/F0032 尚未批准，不能因 Task 19 完成而自动进入业务编码。
- HUMAN 数据采集涉及隐私、同意和保留策略，必须保留独立数据门禁。
