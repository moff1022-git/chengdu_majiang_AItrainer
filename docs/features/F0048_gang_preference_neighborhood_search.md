# F0048 gang_preference 邻域搜索与跨数据集验证

Status: Done

## 背景

F0047 将 `gang_preference` 从 .85 调至 .50 后，在固定数据集上从 171 分恢复到 Expert 的 282 分。目标仍是让 Nonhuman 稳定超过 Expert，而不是复制 Expert；单一数据集和少数高影响牌局不足以证明泛化。

## 范围与方法

1. 基于 F0047 完整 audit 中保存的全部候选与分数，对 `.35/.40/.45/.55/.60` 进行离线重排；杠候选分数按实现公式增加 `0.12*(candidate-.50)`，非杠候选不变。
2. 以“相对 .50 产生可测但不过度的杠/弃牌排序变化”为筛选依据；离线重排只用于选唯一候选，不声称牌局收益。
3. 唯一候选在 `fairness-20260802-fair-004` 运行固定 1000 局完整 games/steps/audit。
4. 独立生成新的公平模式 1000 局数据集；分别运行 `.50` 和唯一候选，至少保存终局记录。若工具成本允许，保留完整 trace。
5. 比较总分、均分、95% bootstrap CI、最差 5% 均分、标准差、胡牌、自摸、花猪、点炮以及配对 game_id 差值。

## 固定条件

- s0 权重 speed/hand_value/defense/flexibility=.35/.25/.25/.15；peng=.70、big_hand=.80、defense=.45、plan persistence=.05；
- s1-s3=`novice_balanced`；
- 除 `gang_preference` 外不得改变其他参数；
- 不覆盖旧结果，不修改正式人格预设。

## 晋级门槛

正式预设只有在两个数据集均满足候选总分高于 `.50`，且合并配对均分差的 95% bootstrap CI 下界大于 0 时才允许另立规格修改。否则保留正式预设不变并记录否决。

## Out of Scope

- 不修改 evaluator 或引擎规则；
- 不并行调多个参数；
- 不以离线候选重排替代真实 replay。

## 验收

- 离线五候选覆盖率与翻转统计完整；
- 选出且只选出一个真实 replay 候选；
- 主数据集候选 1000/1000；新独立数据集 `.50` 与候选均 1000/1000；
- 输出稳定性、置信区间和是否满足晋级门槛的明确结论；
- 更新 LATEST、changelog、DOC_CODE_BASELINE。

## 验收结果

五档离线筛选、`.55` 主数据集完整1000局、held-out `.50/.55` 各1000局和稳定性统计均完成。两个数据集点估计分别 +5/+12，但合并95%配对bootstrap CI `[-.0035,.0235]`，未达到晋级门槛；正式预设保持不变。详见 `docs/status/nonhuman_gang_neighborhood_f0048_result.md`。
