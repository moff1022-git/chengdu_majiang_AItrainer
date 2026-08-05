# F0060 Humanlike受控多进程批跑设计

- 状态：Approved
- 日期：2026-08-05
- 前置：`docs/status/humanlike_concurrency_memory_audit.md`

## 目标

将Humanlike批量测试从无吞吐收益的线程并发迁移为可选、受内存约束的多进程执行；保持固定牌局、人格配置、报告、checkpoint和复盘语义不变。

## 设计

1. 新增执行后端`serial/thread/process`，Humanlike默认`serial`；非Humanlike保持现有兼容默认。
2. `process`使用spawn上下文，worker只接收可序列化的game index、fixed deal、玩家类型和preset ID；在子进程内部创建并关闭玩家。
3. 主进程唯一负责结果排序、checkpoint、报告和Ctrl-C；子进程不得并发写同一报告或trace文件。
4. worker上限按以下最小值计算：用户请求、CPU核数、待运行局数、内存预算上限。内存预算采用保守估算并允许CLI显式下调，禁止自动越过用户上限。
5. 完整trace模式每局使用独立目录，主进程以game_id合并索引；原始记录不可覆盖。
6. 每局保留现有确定性种子和fixed deal；不同后端的终局结果、校验码及人格快照必须一致。

## CLI建议

- `--executor serial|thread|process`
- `--workers N`
- `--memory-budget-mib N`
- 启动确认显示实际worker、估计峰值内存及回退原因。

## 验收

- 同一固定12/100局在serial/process下逐局终局结果一致；
- process workers 2相对serial有可测吞吐提升，否则自动建议serial；
- 峰值RSS不超过预算加单worker容差；
- Ctrl-C后checkpoint可恢复，无重复game_id；
- 完整trace 100%且人格快照一致；
- 全仓回归通过。

## Out of Scope

- 本轮不实现runner代码；
- 不修改Humanlike策略、参数或评分；
- 不自动选择超过用户指定值的worker；
- 不引入外部分布式队列。

## 批准记录

用户执行LATEST任务2，授权形成Humanlike多进程批跑设计；本轮仅规格落盘，据此Approved。
