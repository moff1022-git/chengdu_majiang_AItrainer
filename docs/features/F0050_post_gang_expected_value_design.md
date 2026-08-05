# F0050 杠后期望收益模型设计

Status: Rejected after validation

F0049 的10000局验证未通过正式晋级门槛：一个独立seed数据集候选 `.55` 为负，合并95% bootstrap CI下界为 `-0.0011`。因此不修改正式人格预设，也不继续盲调固定 `gang_preference`。

## 方案

杠候选采用公开信息代理的有限期望收益，不读取未来牌墙、对手暗手或复盘真值：

`gang_ev = 0.30 * immediate_income + 0.35 * post_gang_speed * wall_pressure + 0.20 * defense - 0.15 * terminal_risk`

- `immediate_income`：按 `gang_an/gang_jia/gang_ming` 的规则即时收益归一化；
- `post_gang_speed`：候选分析得到的当前手牌 speed；
- `wall_pressure`：由公开 `wall_remaining` 映射，墙越短越强调确定收益；
- `defense`：公开弃牌危险聚合的候选防守值；
- `terminal_risk`：墙短且候选不具备速度优势时的风险；
- 原 `0.12 * gang_preference` 保留为弱风格项，系数降为 `0.03`，避免完全抹除人格差异。

所有输入必须来自 `DecisionContext.view.payload` 与 `PublicBelief` 白名单；若 `wall_remaining` 不可见，使用中性压力 `0.5`。trace 增加 `gang_ev_breakdown`。

## 范围

In Scope：evaluator 杠候选评分、trace 分解、规则/场景测试、固定小样本A/B。

Out of Scope：引擎结算规则、牌墙生成、正式人格默认值、读取未来牌墙或对手隐牌。

## 验收

- 缺失/非法 `wall_remaining` 不崩溃并回退0.5；
- 所有杠EV输入均来自公开视图；禁止字段测试通过；
- 杠后EV分解可复现、同一输入同一分数；
- 小样本至少100局 `.50`、`.55` 与 `gang_ev` 对照，成功率100%；
- 只有小样本不劣于两基线后才运行1000局完整trace。

## 验证结果与回滚

公开信息边界与确定性测试通过（12项相关测试通过），但固定同100局小样本失败：旧模型 `.50/.55` 均为91分、34胡、4花猪；本公式为-45分、30胡、8花猪。模型把即时杠收入作为正向项，但当前 `post_gang_speed` 并未真正模拟杠后补牌和牌型，造成过度杠并破坏成胡路径。未进入1000局门禁，业务实现与专项测试已回滚，正式预设未修改。
