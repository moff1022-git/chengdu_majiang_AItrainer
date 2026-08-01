# Spec v3 10单元可实施性试点报告

| 字段 | 结果 |
|---|---|
| 基线 | `SPEC-V3-3.0.0`，锁定集hash `6df28948e37dd95c57c9060c6e7e7d28a8243b86e8844a133ab33b6641c1e4ec` |
| 范围 | RULE-003、RULE-016、ALGO-001、ALGO-010、HEUR-019、MODEL-001、STATE-005、SCORE-001、TRAIN-003、AUDIT-003 |
| 试点测试 | 10 passed in 0.05s |
| 全仓回归 | 367 passed、1 skipped in 30.26s |
| 总结论 | 规格可指导E2/E3实现和行为测试，但尚不足以无解释地形成10个E4/AUDITED结论 |

## 1. 实现与测试结果

| 单元 | 实现/补全入口 | 自动化位置 | 覆盖结果 | 审计结论 |
|---|---|---|---|---|
| RULE-003 | `engine.legal.legal_discards`（既有入口按锁定规则复核） | `tests/spec_v3/test_rule_003.py` | 清缺、清完释放、胡后退出、复算 | E3；非测试生产调用存在，但本次未形成完整局trace，NOT AUDITED |
| RULE-016 | `protocols.player_view_builder.PlayerViewBuilder` | `test_rule_016.py` | 四座交叉、sentinel、墙序/暗手隔离 | E3；NOT AUDITED |
| ALGO-001 | `engine.physical_tile.validate_physical_ownership` | `test_algo_001.py` | 108守恒、边界、重复、缺失、置换 | E3；新增入口尚无生产调用，NOT AUDITED |
| ALGO-010 | `PlayerViewBuilder.build` | `test_algo_010.py` | self/other投影、hidden墙、非法viewer | E3；NOT AUDITED |
| HEUR-019 | `players.humanlike.attention.rank_attention_cues` | `test_heur_019.py` | 规范基线公式、mandatory、Top-K、范围、置换 | E3；无冻结统计样本，NOT AUDITED |
| MODEL-001 | `players.humanlike.belief.model_001_rule_baseline` | `test_model_001.py` | 规则回退、概率归一、低证据、隐藏字段拒绝 | E3规则基线；未训练/校准，NOT AUDITED |
| STATE-005 | `PlayerViewV2.stable_hash`及既有深冻结 | `test_state_005.py` | 深层写拒绝、hash复算 | E3；新hash尚无生产调用，NOT AUDITED |
| SCORE-001 | `engine.score.apply_conserved_transfers` | `test_score_001.py` | 正常/空事件/自转/零金额/ΣΔ=0 | E3；event幂等与完整结算调用未接入，NOT AUDITED |
| TRAIN-003 | `training.action_codec_v2`既有生产共用入口 | `test_train_003.py` | 双射、mask、上下界非法 | E3；本次未生成训练episode trace，NOT AUDITED |
| AUDIT-003 | `engine.audit.DecisionAuditWriter/verify_audit` | `test_audit_003.py` | canonical、原链、篡改、截断 | E3；性能及完整运行trace未在本次冻结scope内，NOT AUDITED |

任务卡建议的目录与既有 `engine/rules.py`、`engine/state.py`、`engine/audit.py` 等模块重名。为避免Python导入遮蔽，本试点在现有生产模块补稳定入口；这属于兼容适配，不是绕过规格。

## 2. 测试合同执行说明

每个自动化模块把父合同的正常、边界、非法、确定/统计或隐藏隔离要求合并为可执行测试；没有为制造数量而复制同一断言。确定单元使用显式golden值，HEUR只断言允许域和稳定排序，MODEL只验规则基线的概率契约而未虚构校准成绩。

未执行并因此未判Passed的项目：真实训练模型校准、HEUR大样本统计置信区间、10个单元各自P50/P95/P99、完整游戏生产trace、外部效果和E5。它们不能由本次10个定向测试替代。

## 3. 运行证据

| 证据 | 路径 | SHA-256 |
|---|---|---|
| 试点JUnit | `docs/spec-v3/08-review/pilot-evidence/pilot_tests.xml` | `583673a163027c24964bcea77606b1e9837e9587f4031940a35b3a9358ae6b6a` |
| 全仓JUnit | `docs/spec-v3/08-review/pilot-evidence/full_regression.xml` | `766bb52e8769e1c66fdd74123efef43ab0a5bea70686c38e8b52226a834ad632` |

命令：

```text
PYTHONPYCACHEPREFIX=/tmp/spec_v3_pilot_pycache .venv-macos/bin/python -m pytest -q tests/spec_v3 --junitxml=docs/spec-v3/08-review/pilot-evidence/pilot_tests.xml
PYTHONPYCACHEPREFIX=/tmp/spec_v3_pilot_full_pycache .venv-macos/bin/python -m pytest -q --junitxml=docs/spec-v3/08-review/pilot-evidence/full_regression.xml
```

## 4. 审计验收

按每单元AC-01～14审阅：AC-01～03、07～08及适用的13/14已有E1～E3证据；AC-04、05、09～12未在同一current-run scope对全部10单元满足。因AUDITED要求14项同时Passed且至少E4，10个单元均保持`NOT AUDITED`，没有以聚合通过率抵消hard gate。

## 5. 试点终止条件

本轮只完成10单元，不开始其余86单元。下一动作必须由用户决定先修订规格，还是批准以反馈中的解释作为实施约定后再开展下一批。

## 6. 3.0.2复验更新

4项Medium已解决，10单元按3.0.2重新验收并全部达到E3试点可实施性Passed。详见`pilot_revalidation_report_3_0_2.md`。没有单元被越级标记为生产AUDITED。
