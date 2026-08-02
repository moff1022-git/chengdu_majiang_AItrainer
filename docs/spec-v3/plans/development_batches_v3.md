# Task 18A：Spec v3 可执行开发批次

状态：**Ready for execution planning / no audit status change**  
基线：Task 17（9 AUDITED / 1 INTEGRATED / 85 PARTIAL / 1 SCAFFOLDED）  
当前测试：Windows Python 3.12.10，387 passed，0 failed，0 skipped，234.46s

## 规划结论

87 个非 AUDITED 单元已全部分配到 23 个可执行小批次，每批 1～10 个单元；小于 5 个的批次均由强依赖或外部数据门禁造成。没有把 MODEL-001 数据问题传播为 B1～B3 阻塞。

`B1-A` 是唯一立即可启动批次。依赖矩阵显示 `STATE-010` 无单元依赖，`ALGO-009` 和 `ALGO-011` 均依赖 `STATE-010`，所以批内拓扑顺序为 `STATE-010 → ALGO-009 / ALGO-011`。

## 批次总表

| 批次 | 顺序 | 目标 | 数量 | 单元 | 前置批次 | 门禁 |
|---|---|---|---|---|---|---|
| B1-A | 1 | deterministic-root | 3 | STATE-010/ALGO-009/ALGO-011 | — | immediate |
| B4-DATA-MODEL001 | 2 | model001-calibration-data | 1 | MODEL-001 | — | external |
| B1-B | 3 | state-bootstrap | 3 | STATE-001/STATE-011/STATE-004 | B1-A | dependency |
| B2-A1 | 4 | deterministic-prerequisites | 3 | STATE-002/STATE-003/ALGO-002 | B1-B | dependency |
| B1-C1 | 5 | p0-rule-foundation | 5 | RULE-001/RULE-002/RULE-005/RULE-006/RULE-015 | B2-A1 | dependency |
| B2-A2 | 6 | decision-prerequisites | 2 | ALGO-006/STATE-009 | B1-C1 | dependency |
| B1-C2 | 7 | p0-rule-claims | 6 | RULE-004/RULE-007/RULE-008/RULE-010/RULE-011/RULE-012 | B1-C1 | dependency |
| B1-C3 | 8 | p0-response-score | 5 | RULE-009/RULE-013/RULE-014/SCORE-002/SCORE-003 | B1-C2 | dependency |
| B1-C4 | 9 | p0-terminal-score | 3 | SCORE-004/SCORE-005/SCORE-006 | B1-C3 | dependency |
| B2-B | 10 | deterministic-completion | 9 | ALGO-003/ALGO-004/ALGO-005/ALGO-007/ALGO-008/STATE-006/STATE-007/STATE-008/STATE-012 | B1-C4/B2-A2 | dependency |
| B3-A | 11 | heuristic-foundation | 8 | HEUR-001/HEUR-002/HEUR-004/HEUR-006/HEUR-008/HEUR-011/HEUR-020/HEUR-022 | B2-B | dependency |
| B3-B | 12 | heuristic-decision | 10 | HEUR-003/HEUR-005/HEUR-014/HEUR-007/HEUR-009/HEUR-010/HEUR-012/HEUR-017/HEUR-021/HEUR-023 | B3-A | dependency |
| B4-A | 13 | model-inference-engineering | 2 | MODEL-002/MODEL-003 | B2-B/B3-A | dependency |
| B3-C | 14 | heuristic-risk-sequence | 4 | HEUR-013/HEUR-015/HEUR-016/HEUR-018 | B3-B/B4-A | dependency |
| B5-A | 15 | training-contracts | 4 | TRAIN-001/TRAIN-002/TRAIN-004/TRAIN-005 | B2-B | dependency |
| B4-A2 | 16 | trainable-policy-contract | 1 | MODEL-004 | B5-A | dependency |
| B5-B | 17 | training-environment | 2 | TRAIN-006/TRAIN-009 | B5-A | dependency |
| B5-C | 18 | training-self-play | 1 | TRAIN-007 | B5-B | dependency |
| B6-A | 19 | audit-runtime | 6 | AUDIT-001/AUDIT-002/AUDIT-004/AUDIT-005/AUDIT-006/AUDIT-007 | B2-B | dependency |
| B6-B | 20 | audit-trace-release | 6 | AUDIT-010/AUDIT-008/AUDIT-009/AUDIT-011/AUDIT-013/AUDIT-014 | B6-A/B5-B | dependency |
| B5-DATA | 21 | offline-training-data | 1 | TRAIN-008 | B6-B/B5-A | dependency |
| B4-B | 22 | model-lifecycle | 1 | MODEL-005 | B4-A2/B5-DATA/B6-B | external |
| B6-C | 23 | external-effect-evaluation | 1 | AUDIT-012 | B4-B/B5-C/B6-B | external |

## 统一入口条件

1. Task 17 状态与 Frozen 公共契约保持不变；Locked 规格无待决歧义。
2. 上游批次中的每个依赖单元均已独立审计通过，而非只有批次总测试通过。
3. 开始前记录 Git/版本/测试基线；保护用户已有工作树。
4. 开发步骤与独立审计步骤分开；不得由实现完成自动写成 AUDITED。

## 统一退出条件

1. 每单元分别取得规格、非占位生产代码、直接与分支测试、生产接线、可归属运行和全链追踪证据。
2. 运行记录含 unit_id、scenario/game_id、输入摘要、参数版本、seed、候选/中间结果、最终输出、调用位置和测试/回放引用。
3. 所有适用 AC-01～AC-14 为 Passed，无开放 High/Critical；性能满足 Locked 规格。
4. 批次定向、公共契约、固定 seed 回放、信息边界专项和全仓 pytest 均通过。

## 信息边界回归

Task 17 的全部 86 个 `REQUIRES_BOUNDARY_TEST` 单元均进入专项测试总体范围：8 个已 AUDITED 单元继续作为回归基线，78 个位于本计划矩阵并按所属批次执行。该标记表示必须测试，不表示已发现泄漏。

专项测试统一验证 PlayerView 默认拒绝白名单、对手暗手/墙序递归 sentinel、对象引用/缓存/日志/派生字段隔离，以及同一可见状态下隐藏字段删除或扰动不改变策略决策。规则裁判和模拟器依法可读全知状态，但必须验证与策略模块隔离。

## 并行规则

- P1 为确定性主链，只能按依赖顺序推进。
- P2 中 B3、B4 工程、B5 和 B6 可在共同上游 B2-B 完成后按各自依赖并行。
- P3/P4 涉及模型发布、离线数据或最终外部评价；没有冻结数据时可继续工程准备，但不得宣称外部效果通过。
- MODEL-001 数据轨与 B1/B2/B3 独立并行。
