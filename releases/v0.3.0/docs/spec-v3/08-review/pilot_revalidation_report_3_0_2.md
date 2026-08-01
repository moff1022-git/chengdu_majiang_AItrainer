# SPEC-V3-3.0.2 十单元重新验收报告

| 项目 | 结果 |
|---|---|
| 复验基线 | SPEC-V3-3.0.2 |
| lock set | `2d8bc9d39cf4777f3ba40f10217075331e8afdae07abb06ad6382aee29f78cc4` |
| 反馈状态 | Critical 0 / High 0 / Medium 0 |
| 定向测试 | 10 passed in 0.10s |
| 全仓回归 | 367 passed, 1 skipped in 30.28s |
| 性能 | 10单元×1000 warm samples；oracle零漂移；全部预算内 |

## 逐单元结论

| 单元 | 新增复验重点 | P95 µs | E级 | 生产AUDITED |
|---|---|---:|---|---|
| RULE-003 | 查询前后state hash/version不变 | 4.000 | E3 Passed | 否：本scope无完整局调用trace |
| RULE-016 | 四座白名单和隐藏隔离 | 48.917 | E3 Passed | 否：缺同scope完整局trace/参数证据 |
| ALGO-001 | 完整region、unknown/missing、108守恒 | 19.375 | E3 Passed | 否：新增入口尚无生产调用方 |
| ALGO-010 | self/other投影、非法viewer | 48.250 | E3 Passed | 否：缺同scope完整局trace |
| HEUR-019 | 明确计算图、mandatory不占K | 2.542 | E3 Passed | 否：新增规范入口尚未接主策略，且无统计样本 |
| MODEL-001 | 规则回退、归一、隐藏输入拒绝 | 1.792 | E3 Passed | 否：无冻结校准manifest；规则回退不能替代模型校准 |
| STATE-005 | 深冻结、稳定hash | 47.375 | E3 Passed | 否：stable_hash尚无生产调用方 |
| SCORE-001 | 支付守恒、错误码 | 1.417 | E3 Passed | 否：尚未接权威ledger幂等存储 |
| TRAIN-003 | 635映射、双射、稳定错误码 | 1.875 | E3 Passed | 否：本scope无episode完整trace |
| AUDIT-003 | canonical、篡改、截断 | 1.750 | E3 Passed | 否：本scope未证明完整游戏链与保留流程 |

## AC复验摘要

十单元的AC-01～03、07、08、12及适用的13/14已由current-run证据支持；纯函数的AC-06以零副作用/零写入通过。AC-04、05、09～11未对全部单元在同一scope满足，因此没有任何单元被标记AUDITED。该结论符合3.0.2“两阶段门禁”，不是试点失败。

## 证据

- `pilot_tests_3_0_2.xml` SHA-256 `ebf930c2d879c65795f9f1242f0cce713bf076a1bd4033d54c01eb02445fce13`
- `full_regression_3_0_2.xml` SHA-256 `ea7cc4e91042106574e58135829e0db0c62f0afb76da08bf13537941c6b5c7ee`
- `pilot_runtime_3_0_2.jsonl` SHA-256 `b3206739e72deb98f44061a40b7db62576ed33ebdd5fd1235c69fc39491613ee`

## 最终判断

原10单元在E3“规格可实施性”层面全部通过。规格反馈严重度已清零，证明3.0.2足以指导这些单元的独立实现、边界测试和性能复验；生产E4仍需要后续正式接线任务，不得在本轮顺带实施。
