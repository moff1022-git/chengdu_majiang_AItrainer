# F0035 MODEL-001 分阶段校准方案

Status: Approved
Owner: Terminal 0
Scope: Task 19 / MODEL-001

## 目标

允许使用现有模拟数据完成 MODEL-001 的工程开发与确定性验证；开发和测试完成前不要求正式牌局数据。程序进入试运行/生产后，在合规前提下采集独立的人类玩家数据，用于后续训练、校准和外部有效性评估。外部数据未就绪不得阻塞工程开发，也不得把模拟结果宣传为外部有效性结论。

## 阶段状态

| 阶段 | 允许结论 | 禁止结论 |
|---|---|---|
| 工程开发 | 使用模拟数据完成 schema、训练/推理、artifact、fallback、回退链和 E4/E5 验证 | 真人相似、外部泛化、最终 AUDITED |
| 运行采集 | 运行中经授权采集脱敏人类玩家特征、独立真实结果标签、版本和来源 provenance | 开发前强制等待正式数据；未经同意采集；把 fallback 自生成标签当独立真值 |
| 独立校准功能（程序完成后单独运行） | 对明确标记的模拟/人类数据执行指标、对照和报告 | 不得成为开发/测试或 Task 19 `AUDITED` 的前置门禁 |
| 独立审计 | 工程证据达到要求即可完成 Task 19 `AUDITED`；外部校准结果另行记录 | 绕过数据/许可/人工门禁 |

## 模拟数据准入

`data/model001/model001-sim-v1` 可用于工程验证、确定性重训、接口/异常/回退测试和证据生成，manifest 必须标记 `data_origin=SIMULATION`。其 `external_validity` 必须保持 `NOT_EVALUATED`；类别覆盖不足的指标不得外推。

## 运行期人类数据采集

正式数据采集发生在工程开发与测试完成、程序进入试运行或生产之后，manifest 必须标记 `data_origin=HUMAN`。采集必须具备用户告知/同意、脱敏、访问隔离、保留期限和删除机制；不得影响牌局实时决策，也不得把受限真实标签暴露给策略进程。

## 正式数据最低要求

- 至少 10,000 条有效样本；特征与受限标签物理隔离。
- 按 player/match/game/seed-family 分组的 train/validation/test manifest。
- 来源、许可/同意、规则集/schema/生成器版本与 canonical SHA-256。
- 重复、近重复、泄漏、缺失和范围检查。
- Brier、log loss、15-bin ECE、reliability、top-2 recall、95% CI。
- 与规则 fallback 同测试集对照，以及 OOD/超时/版本不匹配安全回退。

## 状态映射

工程阶段完成后：`engineering_status=COMPLETE`、`simulation_validation=PASS_WITH_LIMITATIONS`、`production_fallback=ENABLED`、`external_calibration=PENDING_DATA`、`external_validity=NOT_EVALUATED`、`final_audit=DEFERRED`。只有独立审计通过后才可将 Task 19 unit 升级为 `AUDITED`。

## 门禁与下一步

本规格批准后按“模拟数据工程 validator → 模拟训练/推理与 fallback 对照 → E4/E5 工程审计 → Task 19 `AUDITED` → 独立校准功能（按需对 SIMULATION/HUMAN 运行）→ 运行期人类数据采集与后续外部评估”顺序实施。校准功能不参与开发/测试门禁，也不改变已通过单元的 `AUDITED` 状态；`T19-RISK-004` 仅记录外部评估状态。
