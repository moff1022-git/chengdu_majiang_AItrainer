# RULE/STATE 单元可执行测试规格

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 覆盖 | RULE等，共28单元 |
| 单元规格 | Approved |
| 测试实现/验收 | Not Implemented / Not Evaluated |

本文件规定测试代码、向量、断言和证据合同；详细业务定义仍只来自已批准单元规格。本文件存在不表示测试文件、fixture或行为已实现。

## RULE-001 规则、参数、不变量与合法性裁决优先级

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-001](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_001.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_001.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | ruleset/config/state |
| 主要输出 | authoritative legal set or explicit rejection |
| 本卡焦点 | 规则、参数、不变量与合法性裁决优先级的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-001-N01 | `test_rule_001_normal_golden` | JSONL `case=normal` | 规则、参数、不变量与合法性裁决优先级的批准输入、输出和验收边界；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-001-B01 | `test_rule_001_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-001-I01 | `test_rule_001_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-001-P01 | `test_rule_001_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-001-R01 | `test_rule_001_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-001-X01 | `test_rule_001_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_001.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-001-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-002 换三张同花色、方向与提交合法性

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-002](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_002.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_002.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | concealed physical tiles + direction |
| 主要输出 | accepted exchange or error |
| 本卡焦点 | 同花色三张、交换方向与实体所有权 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-002-N01 | `test_rule_002_normal_golden` | JSONL `case=normal` | 同花色三张、交换方向与实体所有权；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-002-B01 | `test_rule_002_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-002-I01 | `test_rule_002_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-002-P01 | `test_rule_002_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-002-R01 | `test_rule_002_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-002-X01 | `test_rule_002_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_002.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-002-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-003 定缺未清时的强制出牌约束

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-003](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_003.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_003.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | hand + dingque |
| 主要输出 | legal discards |
| 本卡焦点 | 定缺未清时合法弃牌全集 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-003-N01 | `test_rule_003_normal_golden` | JSONL `case=normal` | 定缺未清时合法弃牌全集；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-003-B01 | `test_rule_003_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-003-I01 | `test_rule_003_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-003-P01 | `test_rule_003_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-003-R01 | `test_rule_003_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-003-X01 | `test_rule_003_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_003.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-003-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-004 定缺、死叫与胡牌资格约束

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-004](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_004.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_004.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | hand + dingque + waits |
| 主要输出 | hu eligibility |
| 本卡焦点 | 定缺、死叫与胡牌资格约束的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-004-N01 | `test_rule_004_normal_golden` | JSONL `case=normal` | 定缺、死叫与胡牌资格约束的批准输入、输出和验收边界；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-004-B01 | `test_rule_004_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-004-I01 | `test_rule_004_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-004-P01 | `test_rule_004_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-004-R01 | `test_rule_004_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-004-X01 | `test_rule_004_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_004.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-004-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-005 座位、庄家与活动顺序

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-005](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_005.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_005.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | seats + dealer + active set + actor |
| 主要输出 | next actor |
| 本卡焦点 | 座位、庄家与活动顺序的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-005-N01 | `test_rule_005_normal_golden` | JSONL `case=normal` | 座位、庄家与活动顺序的批准输入、输出和验收边界；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-005-B01 | `test_rule_005_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-005-I01 | `test_rule_005_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-005-P01 | `test_rule_005_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-005-R01 | `test_rule_005_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-005-X01 | `test_rule_005_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_005.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-005-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-006 摸牌、可选响应与出牌标准顺序

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-006](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_006.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_006.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | phase + actor + wall |
| 主要输出 | next phase/action request |
| 本卡焦点 | 摸牌→自摸/杠→出牌的唯一阶段顺序 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-006-N01 | `test_rule_006_normal_golden` | JSONL `case=normal` | 摸牌→自摸/杠→出牌的唯一阶段顺序；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-006-B01 | `test_rule_006_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-006-I01 | `test_rule_006_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-006-P01 | `test_rule_006_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-006-R01 | `test_rule_006_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-006-X01 | `test_rule_006_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_006.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-006-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-007 碰牌资格、执行与后续出牌

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-007](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_007.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_007.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | discard + responders + hands |
| 主要输出 | meld/turn |
| 本卡焦点 | 碰牌资格、执行与后续出牌的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-007-N01 | `test_rule_007_normal_golden` | JSONL `case=normal` | 碰牌资格、执行与后续出牌的批准输入、输出和验收边界；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-007-B01 | `test_rule_007_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-007-I01 | `test_rule_007_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-007-P01 | `test_rule_007_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-007-R01 | `test_rule_007_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-007-X01 | `test_rule_007_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_007.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-007-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-008 明杠、暗杠与补杠资格及执行

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-008](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_008.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_008.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | hand/meld/discard |
| 主要输出 | gang transition |
| 本卡焦点 | 明杠、暗杠与补杠资格及执行的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-008-N01 | `test_rule_008_normal_golden` | JSONL `case=normal` | 明杠、暗杠与补杠资格及执行的批准输入、输出和验收边界；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-008-B01 | `test_rule_008_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-008-I01 | `test_rule_008_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-008-P01 | `test_rule_008_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-008-R01 | `test_rule_008_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-008-X01 | `test_rule_008_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_008.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-008-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-009 补杠抢杠胡窗口与解析

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-009](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_009.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_009.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | bugang intent + responders |
| 主要输出 | hu or gang |
| 本卡焦点 | 补杠暂存、抢杠胡响应窗与取消提交 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-009-N01 | `test_rule_009_normal_golden` | JSONL `case=normal` | 补杠暂存、抢杠胡响应窗与取消提交；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-009-B01 | `test_rule_009_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-009-I01 | `test_rule_009_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-009-P01 | `test_rule_009_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-009-R01 | `test_rule_009_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-009-X01 | `test_rule_009_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_009.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-009-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-010 自摸、点炮与抢杠胡资格

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-010](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_010.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_010.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | state + winning tile + source |
| 主要输出 | legal hu set |
| 本卡焦点 | 自摸、点炮与抢杠胡资格的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-010-N01 | `test_rule_010_normal_golden` | JSONL `case=normal` | 自摸、点炮与抢杠胡资格的批准输入、输出和验收边界；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-010-B01 | `test_rule_010_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-010-I01 | `test_rule_010_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-010-P01 | `test_rule_010_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-010-R01 | `test_rule_010_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-010-X01 | `test_rule_010_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_010.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-010-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-011 过胡设置、持续与恢复

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-011](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_011.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_011.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | declined hu + phase/events |
| 主要输出 | pass-hu state |
| 本卡焦点 | 过胡设置、持续及恢复触发点 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-011-N01 | `test_rule_011_normal_golden` | JSONL `case=normal` | 过胡设置、持续及恢复触发点；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-011-B01 | `test_rule_011_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-011-I01 | `test_rule_011_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-011-P01 | `test_rule_011_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-011-R01 | `test_rule_011_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-011-X01 | `test_rule_011_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_011.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-011-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-012 强制胡与最后阶段必胡

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-012](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_012.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_012.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | legal hu + GP rule + wall state |
| 主要输出 | forced action |
| 本卡焦点 | 强制胡与最后阶段必胡的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-012-N01 | `test_rule_012_normal_golden` | JSONL `case=normal` | 强制胡与最后阶段必胡的批准输入、输出和验收边界；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-012-B01 | `test_rule_012_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-012-I01 | `test_rule_012_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-012-P01 | `test_rule_012_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-012-R01 | `test_rule_012_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-012-X01 | `test_rule_012_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_012.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-012-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-013 多人响应确定性优先级

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-013](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_013.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_013.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | response set + GP-008 |
| 主要输出 | resolved actions |
| 本卡焦点 | 多人响应优先级及座次稳定裁决 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-013-N01 | `test_rule_013_normal_golden` | JSONL `case=normal` | 多人响应优先级及座次稳定裁决；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-013-B01 | `test_rule_013_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-013-I01 | `test_rule_013_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-013-P01 | `test_rule_013_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-013-R01 | `test_rule_013_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-013-X01 | `test_rule_013_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_013.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-013-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-014 血战胡后退出、继续与终止

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-014](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_014.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_014.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | hu result + active seats + wall |
| 主要输出 | active set/end |
| 本卡焦点 | 胡牌玩家退出、继续血战及墙空终止 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-014-N01 | `test_rule_014_normal_golden` | JSONL `case=normal` | 胡牌玩家退出、继续血战及墙空终止；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-014-B01 | `test_rule_014_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-014-I01 | `test_rule_014_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-014-P01 | `test_rule_014_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-014-R01 | `test_rule_014_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-014-X01 | `test_rule_014_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_014.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-014-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-015 启用番型、互斥/叠加与封顶规则

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-015](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_015.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_015.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | ruleset + hand facts |
| 主要输出 | applicable fan policy |
| 本卡焦点 | 启用番型、互斥/叠加与封顶规则的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-015-N01 | `test_rule_015_normal_golden` | JSONL `case=normal` | 启用番型、互斥/叠加与封顶规则的批准输入、输出和验收边界；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-015-B01 | `test_rule_015_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-015-I01 | `test_rule_015_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-015-P01 | `test_rule_015_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-015-R01 | `test_rule_015_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-015-X01 | `test_rule_015_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_015.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-015-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## RULE-016 局中与终局公开信息范围

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [RULE-016](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_rule_016.py` |
| 向量文件 | `tests/spec_v3/vectors/rule_016.jsonl` |
| pytest标记 | `deterministic,rule,hard_gate,rule` |
| 主要输入 | phase + seat + event |
| 主要输出 | visible field set |
| 本卡焦点 | 逐座PlayerView字段白名单和隐藏信息投毒 |
| oracle | 逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-RULE-016-N01 | `test_rule_016_normal_golden` | JSONL `case=normal` | 逐座PlayerView字段白名单和隐藏信息投毒；逐字段精确比较权威状态、合法集、稳定错误码及事件顺序 |
| T-RULE-016-B01 | `test_rule_016_boundary_table` | JSONL `case=boundary` 参数化 | 最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界；不越过批准输出范围 |
| T-RULE-016-I01 | `test_rule_016_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变；断言稳定错误码和失败原子性 |
| T-RULE-016-P01 | `test_rule_016_properties` | 固定seed生成器；seed写入报告 | 同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立 |
| T-RULE-016-R01 | `test_rule_016_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-RULE-016-X01 | `test_rule_016_integration_contract` | 生产入口fixture | 经生产Engine公开入口提交事件，不得直接伪造后置状态；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_rule_016.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`RULE-016-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## STATE-001 Match 配置冻结、玩家装配与整场控制

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [STATE-001](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_state_001.py` |
| 向量文件 | `tests/spec_v3/vectors/state_001.jsonl` |
| pytest标记 | `deterministic,state,hard_gate,state` |
| 主要输入 | match request |
| 主要输出 | immutable match context |
| 本卡焦点 | Match 配置冻结、玩家装配与整场控制的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-STATE-001-N01 | `test_state_001_normal_golden` | JSONL `case=normal` | Match 配置冻结、玩家装配与整场控制的批准输入、输出和验收边界；逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| T-STATE-001-B01 | `test_state_001_boundary_table` | JSONL `case=boundary` 参数化 | 初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界；不越过批准输出范围 |
| T-STATE-001-I01 | `test_state_001_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败；断言稳定错误码和失败原子性 |
| T-STATE-001-P01 | `test_state_001_properties` | 固定seed生成器；seed写入报告 | 合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现 |
| T-STATE-001-R01 | `test_state_001_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-STATE-001-X01 | `test_state_001_integration_contract` | 生产入口fixture | 通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_state_001.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`STATE-001-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## STATE-002 权威 RoundState 存储与授权访问

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [STATE-002](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_state_002.py` |
| 向量文件 | `tests/spec_v3/vectors/state_002.jsonl` |
| pytest标记 | `deterministic,state,hard_gate,state` |
| 主要输入 | atomic events |
| 主要输出 | authoritative state |
| 本卡焦点 | 权威 RoundState 存储与授权访问的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-STATE-002-N01 | `test_state_002_normal_golden` | JSONL `case=normal` | 权威 RoundState 存储与授权访问的批准输入、输出和验收边界；逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| T-STATE-002-B01 | `test_state_002_boundary_table` | JSONL `case=boundary` 参数化 | 初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界；不越过批准输出范围 |
| T-STATE-002-I01 | `test_state_002_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败；断言稳定错误码和失败原子性 |
| T-STATE-002-P01 | `test_state_002_properties` | 固定seed生成器；seed写入报告 | 合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现 |
| T-STATE-002-R01 | `test_state_002_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-STATE-002-X01 | `test_state_002_integration_contract` | 生产入口fixture | 通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_state_002.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`STATE-002-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## STATE-003 PlayerRoundState 手牌、副露、定缺与过胡状态

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [STATE-003](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_state_003.py` |
| 向量文件 | `tests/spec_v3/vectors/state_003.jsonl` |
| pytest标记 | `deterministic,state,hard_gate,state` |
| 主要输入 | rule transitions |
| 主要输出 | player state |
| 本卡焦点 | PlayerRoundState 手牌、副露、定缺与过胡状态的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-STATE-003-N01 | `test_state_003_normal_golden` | JSONL `case=normal` | PlayerRoundState 手牌、副露、定缺与过胡状态的批准输入、输出和验收边界；逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| T-STATE-003-B01 | `test_state_003_boundary_table` | JSONL `case=boundary` 参数化 | 初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界；不越过批准输出范围 |
| T-STATE-003-I01 | `test_state_003_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败；断言稳定错误码和失败原子性 |
| T-STATE-003-P01 | `test_state_003_properties` | 固定seed生成器；seed写入报告 | 合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现 |
| T-STATE-003-R01 | `test_state_003_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-STATE-003-X01 | `test_state_003_integration_contract` | 生产入口fixture | 通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_state_003.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`STATE-003-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## STATE-004 CONFIGURED→SETTLED 状态机

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [STATE-004](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_state_004.py` |
| 向量文件 | `tests/spec_v3/vectors/state_004.jsonl` |
| pytest标记 | `deterministic,state,hard_gate,state` |
| 主要输入 | current phase + event |
| 主要输出 | next phase or error |
| 本卡焦点 | CONFIGURED→SETTLED 状态机的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-STATE-004-N01 | `test_state_004_normal_golden` | JSONL `case=normal` | CONFIGURED→SETTLED 状态机的批准输入、输出和验收边界；逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| T-STATE-004-B01 | `test_state_004_boundary_table` | JSONL `case=boundary` 参数化 | 初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界；不越过批准输出范围 |
| T-STATE-004-I01 | `test_state_004_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败；断言稳定错误码和失败原子性 |
| T-STATE-004-P01 | `test_state_004_properties` | 固定seed生成器；seed写入报告 | 合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现 |
| T-STATE-004-R01 | `test_state_004_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-STATE-004-X01 | `test_state_004_integration_contract` | 生产入口fixture | 通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_state_004.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`STATE-004-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## STATE-005 不可变 PlayerView 状态载体

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [STATE-005](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_state_005.py` |
| 向量文件 | `tests/spec_v3/vectors/state_005.jsonl` |
| pytest标记 | `deterministic,state,hard_gate,state` |
| 主要输入 | builder output |
| 主要输出 | frozen seat view |
| 本卡焦点 | 不可变 PlayerView 状态载体的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-STATE-005-N01 | `test_state_005_normal_golden` | JSONL `case=normal` | 不可变 PlayerView 状态载体的批准输入、输出和验收边界；逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| T-STATE-005-B01 | `test_state_005_boundary_table` | JSONL `case=boundary` 参数化 | 初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界；不越过批准输出范围 |
| T-STATE-005-I01 | `test_state_005_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败；断言稳定错误码和失败原子性 |
| T-STATE-005-P01 | `test_state_005_properties` | 固定seed生成器；seed写入报告 | 合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现 |
| T-STATE-005-R01 | `test_state_005_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-STATE-005-X01 | `test_state_005_integration_contract` | 生产入口fixture | 通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_state_005.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`STATE-005-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## STATE-006 策略侧认知运行态初始化与归档

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [STATE-006](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_state_006.py` |
| 向量文件 | `tests/spec_v3/vectors/state_006.jsonl` |
| pytest标记 | `deterministic,state,hard_gate,state` |
| 主要输入 | round start/end |
| 主要输出 | cognition state/snapshot |
| 本卡焦点 | 策略侧认知运行态初始化与归档的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-STATE-006-N01 | `test_state_006_normal_golden` | JSONL `case=normal` | 策略侧认知运行态初始化与归档的批准输入、输出和验收边界；逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| T-STATE-006-B01 | `test_state_006_boundary_table` | JSONL `case=boundary` 参数化 | 初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界；不越过批准输出范围 |
| T-STATE-006-I01 | `test_state_006_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败；断言稳定错误码和失败原子性 |
| T-STATE-006-P01 | `test_state_006_properties` | 固定seed生成器；seed写入报告 | 合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现 |
| T-STATE-006-R01 | `test_state_006_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-STATE-006-X01 | `test_state_006_integration_contract` | 生产入口fixture | 通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_state_006.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`STATE-006-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## STATE-007 存档 schema 持久化与迁移

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [STATE-007](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_state_007.py` |
| 向量文件 | `tests/spec_v3/vectors/state_007.jsonl` |
| pytest标记 | `deterministic,state,hard_gate,state` |
| 主要输入 | state v1–v5 |
| 主要输出 | current state or error |
| 本卡焦点 | 存档 schema 持久化与迁移的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-STATE-007-N01 | `test_state_007_normal_golden` | JSONL `case=normal` | 存档 schema 持久化与迁移的批准输入、输出和验收边界；逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| T-STATE-007-B01 | `test_state_007_boundary_table` | JSONL `case=boundary` 参数化 | 初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界；不越过批准输出范围 |
| T-STATE-007-I01 | `test_state_007_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败；断言稳定错误码和失败原子性 |
| T-STATE-007-P01 | `test_state_007_properties` | 固定seed生成器；seed写入报告 | 合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现 |
| T-STATE-007-R01 | `test_state_007_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-STATE-007-X01 | `test_state_007_integration_contract` | 生产入口fixture | 通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_state_007.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`STATE-007-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## STATE-008 跨局比分、认知和 episode 状态继承

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [STATE-008](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_state_008.py` |
| 向量文件 | `tests/spec_v3/vectors/state_008.jsonl` |
| pytest标记 | `deterministic,state,hard_gate,state` |
| 主要输入 | round result |
| 主要输出 | next-round context |
| 本卡焦点 | 跨局比分、认知和 episode 状态继承的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-STATE-008-N01 | `test_state_008_normal_golden` | JSONL `case=normal` | 跨局比分、认知和 episode 状态继承的批准输入、输出和验收边界；逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| T-STATE-008-B01 | `test_state_008_boundary_table` | JSONL `case=boundary` 参数化 | 初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界；不越过批准输出范围 |
| T-STATE-008-I01 | `test_state_008_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败；断言稳定错误码和失败原子性 |
| T-STATE-008-P01 | `test_state_008_properties` | 固定seed生成器；seed写入报告 | 合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现 |
| T-STATE-008-R01 | `test_state_008_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-STATE-008-X01 | `test_state_008_integration_contract` | 生产入口fixture | 通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_state_008.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`STATE-008-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## STATE-009 决策请求上下文与生命周期

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [STATE-009](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_state_009.py` |
| 向量文件 | `tests/spec_v3/vectors/state_009.jsonl` |
| pytest标记 | `deterministic,state,hard_gate,state` |
| 主要输入 | phase + PlayerView + legal set |
| 主要输出 | request/result |
| 本卡焦点 | 决策请求上下文与生命周期的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-STATE-009-N01 | `test_state_009_normal_golden` | JSONL `case=normal` | 决策请求上下文与生命周期的批准输入、输出和验收边界；逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| T-STATE-009-B01 | `test_state_009_boundary_table` | JSONL `case=boundary` 参数化 | 初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界；不越过批准输出范围 |
| T-STATE-009-I01 | `test_state_009_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败；断言稳定错误码和失败原子性 |
| T-STATE-009-P01 | `test_state_009_properties` | 固定seed生成器；seed写入报告 | 合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现 |
| T-STATE-009-R01 | `test_state_009_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-STATE-009-X01 | `test_state_009_integration_contract` | 生产入口fixture | 通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_state_009.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`STATE-009-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## STATE-010 GP/RP/Profile 注册与生命周期

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [STATE-010](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_state_010.py` |
| 向量文件 | `tests/spec_v3/vectors/state_010.jsonl` |
| pytest标记 | `deterministic,state,hard_gate,state` |
| 主要输入 | source config + phase |
| 主要输出 | owned parameter state |
| 本卡焦点 | GP/RP/Profile 注册与生命周期的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-STATE-010-N01 | `test_state_010_normal_golden` | JSONL `case=normal` | GP/RP/Profile 注册与生命周期的批准输入、输出和验收边界；逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| T-STATE-010-B01 | `test_state_010_boundary_table` | JSONL `case=boundary` 参数化 | 初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界；不越过批准输出范围 |
| T-STATE-010-I01 | `test_state_010_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败；断言稳定错误码和失败原子性 |
| T-STATE-010-P01 | `test_state_010_properties` | 固定seed生成器；seed写入报告 | 合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现 |
| T-STATE-010-R01 | `test_state_010_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-STATE-010-X01 | `test_state_010_integration_contract` | 生产入口fixture | 通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_state_010.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`STATE-010-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## STATE-011 牌墙构建、洗牌与初始发牌

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [STATE-011](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_state_011.py` |
| 向量文件 | `tests/spec_v3/vectors/state_011.jsonl` |
| pytest标记 | `deterministic,state,hard_gate,state` |
| 主要输入 | named RNG + player count |
| 主要输出 | wall/hands |
| 本卡焦点 | 牌墙构建、洗牌与初始发牌的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-STATE-011-N01 | `test_state_011_normal_golden` | JSONL `case=normal` | 牌墙构建、洗牌与初始发牌的批准输入、输出和验收边界；逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| T-STATE-011-B01 | `test_state_011_boundary_table` | JSONL `case=boundary` 参数化 | 初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界；不越过批准输出范围 |
| T-STATE-011-I01 | `test_state_011_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败；断言稳定错误码和失败原子性 |
| T-STATE-011-P01 | `test_state_011_properties` | 固定seed生成器；seed写入报告 | 合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现 |
| T-STATE-011-R01 | `test_state_011_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-STATE-011-X01 | `test_state_011_integration_contract` | 生产入口fixture | 通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_state_011.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`STATE-011-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## STATE-012 策略超时、崩溃与合法默认动作回退

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [STATE-012](../03-unit-specs/deterministic_rule_state_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_state_012.py` |
| 向量文件 | `tests/spec_v3/vectors/state_012.jsonl` |
| pytest标记 | `deterministic,state,hard_gate,state` |
| 主要输入 | request + deadline/failure + legal set |
| 主要输出 | fallback result |
| 本卡焦点 | 策略超时、崩溃与合法默认动作回退的批准输入、输出和验收边界 |
| oracle | 逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-STATE-012-N01 | `test_state_012_normal_golden` | JSONL `case=normal` | 策略超时、崩溃与合法默认动作回退的批准输入、输出和验收边界；逐字段精确比较状态、版本、所有权、生命周期与序列化结果 |
| T-STATE-012-B01 | `test_state_012_boundary_table` | JSONL `case=boundary` 参数化 | 初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界；不越过批准输出范围 |
| T-STATE-012-I01 | `test_state_012_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败；断言稳定错误码和失败原子性 |
| T-STATE-012-P01 | `test_state_012_properties` | 固定seed生成器；seed写入报告 | 合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现 |
| T-STATE-012-R01 | `test_state_012_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-STATE-012-X01 | `test_state_012_integration_contract` | 生产入口fixture | 通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_state_012.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`STATE-012-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

