# MODEL-001 独立数据与校准轨道

状态：**EXTERNAL DATA GATED / rule fallback remains usable**

## 不影响确定性开发的结论

MODEL-001 保持 Task 17 的 INTEGRATED。当前规则 fallback、合法动作约束和隐藏字段拒绝链可继续用于 B1～B3；缺少外部数据不得阻塞确定性规则、算法、状态或启发式开发，也不得把 MODEL-001 降级为未实现。

## 数据门禁

关闭 `MODEL001-DATA-001` 至少需要：

1. 版本化冻结评估发布，≥10,000 个符合规则与schema的有效样本；
2. 物理隔离的 `policy_features` 与 `restricted_label_zone`；
3. 按玩家、比赛、牌局和 seed-family 分组的 train/validation/test manifest；
4. 来源、许可/同意、规则集、schema、生成器、时间范围和 canonical SHA-256；
5. 泄漏扫描、重复/近重复检查、缺失/范围/分布报告；
6. 若声称训练模型优于 fallback，提供冻结模型产物及训练配置；
7. 分任务 Brier、log loss、15-bin ECE、可靠性、top-2 recall 和 95% CI；
8. 与规则 fallback 的同样本比较、OOD/超时/版本不匹配回退验证；
9. 评估器与策略进程/对象/schema隔离，truth 不进入 Observation、势能、日志明文或解释字段。

## 禁止证据

- 不能用规则 fallback 生成标签后评价同一 fallback；
- 不能把历史普通游戏日志补字段后冒充冻结校准发布；
- 不能用训练集指标替代隔离测试集；
- 不能只报 accuracy；
- 不能因工程测试通过而把 MODEL-001 提升为 AUDITED。

## 可并行工程工作

可先完成数据 schema、manifest validator、泄漏扫描器、metric runner、fallback 对照接口和证据包模板；这些工作不改变 MODEL-001 状态。最终 AUDITED 仍要求数据发布和独立审计。
