# Spec v3 可执行测试规格索引

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 覆盖 | 96/96锁定单元 |
| 测试契约 | 576个：每单元N/B/I/P/R/X各1个 |
| 实现状态 | Not Implemented |
| 证据状态 | Not Evaluated |

## 文件导航

- [RULE/STATE](rule_state_test_specs.md)
- [ALGO/SCORE](algorithm_scoring_test_specs.md)
- [HEUR](heuristic_test_specs.md)
- [MODEL](model_test_specs.md)
- [TRAIN](training_test_specs.md)
- [AUDIT](audit_test_specs.md)
- [96单元执行清单](unit_test_manifest.csv)
- [11类测试策略](test_strategy.md)
- [逐用例完整目录](test_case_catalog.md)
- [ALGO/SCORE金标准向量目录](golden_vectors.md)
- [96单元×11类覆盖矩阵](coverage_matrix.csv)

## 统一执行合同

每单元固定六类测试：N正常golden、B边界表、I非法与失败原子性、P性质/统计、R重复性、X生产入口集成。测试模块和JSONL向量路径均由执行清单冻结。确定性单元精确复算；HEUR验证合法允许域、方向效应、regret和统计区间；MODEL验证泄漏隔离、校准和规则回退；TRAIN验证与生产引擎同源；AUDIT验证证据链和hard门禁。

逐用例目录进一步把上述Approved合同细化为11种方法检查。覆盖矩阵登记890个适用TC测试卡；它们是576个N/B/I/P/R/X父合同的展开，不是第二套业务规范，也不能与父合同分别重复计算通过率。

## pytest与证据规则

计划统一命令为`python -m pytest -q tests/spec_v3`。在相应测试文件与向量落盘前，状态必须保持Not Implemented/Not Evaluated，禁止把本规格生成过程算作E3。运行后每个测试ID记录JUnit nodeid、结果、耗时、环境manifest、commit、规则/config/model/schema hash、seed、向量hash及产物路径。skip/xfail必须有owner、原因和到期日；hard gate不得skip或N/A。

## 实现顺序

按锁定DAG和P0优先级：确定规则/状态/牌墙/随机流→确定算法/计分→视图/启发式/模型→训练→审计。每批先落实JSONL schema和共享fixture，再实现单元测试；不得为让测试通过而复制第二套规则oracle，golden expected必须来源于批准公式或人工冻结向量。
