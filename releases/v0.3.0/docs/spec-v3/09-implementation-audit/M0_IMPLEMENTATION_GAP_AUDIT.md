# Spec v3 M0 实现差距审计报告

| 字段 | 内容 |
|---|---|
| 日期 | 2026-07-29 |
| 阶段 | M0 现状盘点与冻结 |
| 规范基线 | SPEC-V3-3.0.0；lock set `6df28948e37dd95c57c9060c6e7e7d28a8243b86e8844a133ab33b6641c1e4ec` |
| 代码基线 | Git HEAD `423326ecf6e602f9c1c3392dd2a844b1e61ce9b3`；工作树非clean，逐文件hash见manifest |
| 审计范围 | 96/96锁定单元；现有生产候选、调用方、旧测试、目标路径与v3计划测试 |
| M0状态 | **Completed for inventory** |
| 实现验收 | **Not Evaluated；没有单元因本报告升级到E2/E3/AUDITED** |
| 程序修改 | 无 |

## 1. 结论先行

现有仓库具备大量可迁移行为，但结构仍是旧复合模块，不是96个v3独立单元。96个目标主文件、96个计划v3测试模块和96个计划向量文件当前全部不存在。M0保守分类为：ADAPT 80、REWRITE 15、ADD 1、REUSE 0、RETIRE 0。

全部单元的正式证据仍为E1；旧符号、旧测试和本轮全量pytest只证明迁移基线健康，不满足E2的独立入口/绑定/trace，也不能冒充v3 E3。

## 2. 数量摘要

| 指标 | 结果 |
|---|---:|
| 锁定单元 | 96 |
| 有可核查旧生产符号候选 | 94 |
| 有可核查旧调用方候选 | 93 |
| 有旧测试用例候选 | 93 |
| v3目标主文件存在 | 0 |
| v3计划测试模块存在 | 0 |
| v3计划JSONL存在 | 0 |
| 候选代码文件hash | 50 |
| 当前E2或更高 | 0 |

## 3. 分类分布

| 类别 | 总数 | ADAPT | REWRITE | ADD | REUSE | RETIRE |
|---|---:|---:|---:|---:|---:|---:|
| RULE | 16 | 16 | 0 | 0 | 0 | 0 |
| ALGO | 11 | 4 | 7 | 0 | 0 | 0 |
| HEUR | 23 | 22 | 0 | 1 | 0 | 0 |
| MODEL | 5 | 5 | 0 | 0 | 0 | 0 |
| STATE | 12 | 11 | 1 | 0 | 0 | 0 |
| SCORE | 6 | 2 | 4 | 0 | 0 | 0 |
| TRAIN | 9 | 8 | 1 | 0 | 0 | 0 |
| AUDIT | 14 | 12 | 2 | 0 | 0 | 0 |
| **合计** | **96** | **80** | **15** | **1** | **0** | **0** |

优先级：P0 54、P1 13、P2 20、P3 9。负责人按责任域登记在矩阵中，不虚构个人owner。

## 4. 必须重写或新增

### 4.1 REWRITE（15）

| 单元 | 原因 |
|---|---|
| ALGO-003 | 可见牌必须按实体事件去重，旧聚合路径可能重复展示计数 |
| ALGO-004 | 规范区分未见牌与墙内活牌区间，旧remain估计边界不足 |
| ALGO-005 | 规范要求逐座剩余摸牌机会与轮转重算，旧逻辑未形成独立算法 |
| ALGO-007 | 规范冻结六分量Q及公式等级，旧评价器权重/中间量不等价 |
| ALGO-008 | 规范要求命名随机域、噪声和思考时间统一派生，旧RNG入口分散 |
| ALGO-009 | 规范要求60参数类型/范围/迁移/canonical hash统一门禁，旧配置只覆盖子集 |
| ALGO-011 | 规范要求game_id派生全部命名子流，旧实现仅固定少量seed |
| STATE-004 | 规范RoundPhase与原有小写phase/编排耦合不等价，需单一权威状态机 |
| SCORE-001 | 规范要求原子ScoreTransfer、分层账本与幂等守恒，旧服务直接改分 |
| SCORE-003 | 呼叫转移与抢杠关联账本在旧实现中不完整 |
| SCORE-004 | 查大叫最大番、死叫与退税在旧实现中缺失或简化 |
| SCORE-005 | 规范封顶/互斥/转移顺序需独立结算层，旧路径耦合 |
| TRAIN-001 | 训练必须包装同一生产规则引擎，旧env仍含独立流程职责 |
| AUDIT-001 | 旧审计主要记录决策，未覆盖全部原子规则事件 |
| AUDIT-005 | 旧不变量未证明在每个原子事件边界统一执行 |

### 4.2 ADD（1）

| 单元 | 原因 |
|---|---|
| HEUR-016 | 未找到可核查的独立生产符号；需按锁定规格新增单元 |

## 5. ADAPT边界

ADAPT只表示旧代码中找到可迁移候选，不表示行为等价。每个ADAPT单元仍需：抽出稳定入口；绑定锁定参数注册；明确纯函数或唯一状态写回；接入生产调用方；实现对应N/B/I/P/R/X与细化测试；保存输入输出、日志、性能和隐藏信息证据。完成这些检查前保持E1 / Not Evaluated。

## 6. 风险分布

| 风险标签 | 单元数 |
|---|---:|
| RULE_DELTA | 31 |
| REPLAY_BREAK | 23 |
| VISIBILITY | 16 |
| DATA_MIGRATION | 12 |
| SCHEMA_BREAK | 12 |
| RNG_BREAK | 10 |
| SCORE | 6 |

## 7. 测试与冻结基线

- 当前全量命令：`PYTHONPYCACHEPREFIX=/tmp/spec_v3_m0_pycache .venv-macos/bin/python -m pytest -q -rs`。
- 结果：357 passed、1 skipped；skip为macOS Tk构造可能终止进程，已有纯helper和人工/子进程GUI验收覆盖。
- 该结果是旧代码回归基线，不是v3测试通过。
- 已冻结game_id发牌状态、PlayerView、领域事件和点炮ScoreTransfer四个代表性JSON，逐文件hash见fixture manifest；计分样本`delta_sum=0`。

## 8. M0完成条件核对

| 条件 | 状态 | 证据 |
|---|---|---|
| 96行分类/owner/风险/符号 | Passed | `m0_implementation_gap_matrix.csv` |
| 当前测试命令/结果/环境/commit | Passed | `m0_baseline.md` |
| 关键输入与SHA-256 | Passed | `baseline_fixtures/fixture_manifest.csv` |
| 已知歧义/blocker显式登记 | Passed | 矩阵`blocker`列；模型/外部评价资产写“当前未找到” |
| 不修改业务行为 | Passed | 本阶段仅新增/更新文档和审计产物 |

## 9. 后续实施入口

先处理P0且分类为REWRITE/ADD的架构根，再处理P0 ADAPT；不得直接按96个目标文件机械搬运旧函数。建议下一阶段先形成M1实施规格差异确认和首批任务：ALGO-009/011、STATE-010/011、STATE-001以及公共VersionBundle/UnitError/NamedRandomStreams。

## 10. 交付

- `m0_implementation_gap_matrix.csv`：96行主矩阵。
- `m0_code_file_manifest.csv`：本轮核查的候选代码文件hash。
- `m0_baseline.md`：环境、测试、工作树与证据限制。
- `baseline_fixtures/`：四类代表性输入输出及hash。
