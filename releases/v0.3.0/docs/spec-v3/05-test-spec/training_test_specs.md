# TRAIN 单元可执行测试规格

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 覆盖 | TRAIN等，共9单元 |
| 单元规格 | Approved |
| 测试实现/验收 | Not Implemented / Not Evaluated |

本文件规定测试代码、向量、断言和证据合同；详细业务定义仍只来自已批准单元规格。本文件存在不表示测试文件、fixture或行为已实现。

## TRAIN-001 复用生产规则的训练包装

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [TRAIN-001](../03-unit-specs/training_environment_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_train_001.py` |
| 向量文件 | `tests/spec_v3/vectors/train_001.jsonl` |
| pytest标记 | `training,production_parity,replay,train` |
| 主要输入 | engine config + agents |
| 主要输出 | training transition |
| 本卡焦点 | Episode单/多局边界及生产状态转换等价 |
| oracle | 逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-TRAIN-001-N01 | `test_train_001_normal_golden` | JSONL `case=normal` | Episode单/多局边界及生产状态转换等价；逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| T-TRAIN-001-B01 | `test_train_001_boundary_table` | JSONL `case=boundary` 参数化 | 单/多局、首末步、空合法集、并行1/N、截断、超时与恢复边界；不越过批准输出范围 |
| T-TRAIN-001-I01 | `test_train_001_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法动作、隐藏truth观测、第二规则引擎、错误版本或损坏快照必须稳定处理；断言稳定错误码和失败原子性 |
| T-TRAIN-001-P01 | `test_train_001_properties` | 固定seed生成器；seed写入报告 | 同seed确定回放；策略观测无truth；每项reward追踪真实计分或显式势能差 |
| T-TRAIN-001-R01 | `test_train_001_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-TRAIN-001-X01 | `test_train_001_integration_contract` | 生产入口fixture | 训练环境必须导入并调用生产Rule/State/Score实现，执行生产等价golden；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_train_001.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`TRAIN-001-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## TRAIN-002 Observation v2 编码

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [TRAIN-002](../03-unit-specs/training_environment_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_train_002.py` |
| 向量文件 | `tests/spec_v3/vectors/train_002.jsonl` |
| pytest标记 | `training,production_parity,replay,train` |
| 主要输入 | PlayerView + optional cognition |
| 主要输出 | fixed observation |
| 本卡焦点 | Observation字段白名单和restricted truth投毒 |
| oracle | 逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-TRAIN-002-N01 | `test_train_002_normal_golden` | JSONL `case=normal` | Observation字段白名单和restricted truth投毒；逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| T-TRAIN-002-B01 | `test_train_002_boundary_table` | JSONL `case=boundary` 参数化 | 单/多局、首末步、空合法集、并行1/N、截断、超时与恢复边界；不越过批准输出范围 |
| T-TRAIN-002-I01 | `test_train_002_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法动作、隐藏truth观测、第二规则引擎、错误版本或损坏快照必须稳定处理；断言稳定错误码和失败原子性 |
| T-TRAIN-002-P01 | `test_train_002_properties` | 固定seed生成器；seed写入报告 | 同seed确定回放；策略观测无truth；每项reward追踪真实计分或显式势能差 |
| T-TRAIN-002-R01 | `test_train_002_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-TRAIN-002-X01 | `test_train_002_integration_contract` | 生产入口fixture | 训练环境必须导入并调用生产Rule/State/Score实现，执行生产等价golden；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_train_002.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`TRAIN-002-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## TRAIN-003 固定动作 codec 与 legal mask

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [TRAIN-003](../03-unit-specs/training_environment_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_train_003.py` |
| 向量文件 | `tests/spec_v3/vectors/train_003.jsonl` |
| pytest标记 | `training,production_parity,replay,train` |
| 主要输入 | legal actions |
| 主要输出 | action ids/mask |
| 本卡焦点 | 固定动作codec、合法mask和非法动作处理 |
| oracle | 逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-TRAIN-003-N01 | `test_train_003_normal_golden` | JSONL `case=normal` | 固定动作codec、合法mask和非法动作处理；逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| T-TRAIN-003-B01 | `test_train_003_boundary_table` | JSONL `case=boundary` 参数化 | 单/多局、首末步、空合法集、并行1/N、截断、超时与恢复边界；不越过批准输出范围 |
| T-TRAIN-003-I01 | `test_train_003_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法动作、隐藏truth观测、第二规则引擎、错误版本或损坏快照必须稳定处理；断言稳定错误码和失败原子性 |
| T-TRAIN-003-P01 | `test_train_003_properties` | 固定seed生成器；seed写入报告 | 同seed确定回放；策略观测无truth；每项reward追踪真实计分或显式势能差 |
| T-TRAIN-003-R01 | `test_train_003_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-TRAIN-003-X01 | `test_train_003_integration_contract` | 生产入口fixture | 训练环境必须导入并调用生产Rule/State/Score实现，执行生产等价golden；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_train_003.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`TRAIN-003-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## TRAIN-004 非法训练动作处理契约

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [TRAIN-004](../03-unit-specs/training_environment_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_train_004.py` |
| 向量文件 | `tests/spec_v3/vectors/train_004.jsonl` |
| pytest标记 | `training,production_parity,replay,train` |
| 主要输入 | action id + mask + mode |
| 主要输出 | raise/terminate/penalty |
| 本卡焦点 | 真实计分reward与γΦ(o')-Φ(o)逐项溯源 |
| oracle | 逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-TRAIN-004-N01 | `test_train_004_normal_golden` | JSONL `case=normal` | 真实计分reward与γΦ(o')-Φ(o)逐项溯源；逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| T-TRAIN-004-B01 | `test_train_004_boundary_table` | JSONL `case=boundary` 参数化 | 单/多局、首末步、空合法集、并行1/N、截断、超时与恢复边界；不越过批准输出范围 |
| T-TRAIN-004-I01 | `test_train_004_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法动作、隐藏truth观测、第二规则引擎、错误版本或损坏快照必须稳定处理；断言稳定错误码和失败原子性 |
| T-TRAIN-004-P01 | `test_train_004_properties` | 固定seed生成器；seed写入报告 | 同seed确定回放；策略观测无truth；每项reward追踪真实计分或显式势能差 |
| T-TRAIN-004-R01 | `test_train_004_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-TRAIN-004-X01 | `test_train_004_integration_contract` | 生产入口fixture | 训练环境必须导入并调用生产Rule/State/Score实现，执行生产等价golden；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_train_004.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`TRAIN-004-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## TRAIN-005 真实得分与可见势能奖励契约

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [TRAIN-005](../03-unit-specs/training_environment_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_train_005.py` |
| 向量文件 | `tests/spec_v3/vectors/train_005.jsonl` |
| pytest标记 | `training,production_parity,replay,train` |
| 主要输入 | transition + visible potential |
| 主要输出 | reward components |
| 本卡焦点 | 真实得分与可见势能奖励契约的批准输入、输出和验收边界 |
| oracle | 逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-TRAIN-005-N01 | `test_train_005_normal_golden` | JSONL `case=normal` | 真实得分与可见势能奖励契约的批准输入、输出和验收边界；逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| T-TRAIN-005-B01 | `test_train_005_boundary_table` | JSONL `case=boundary` 参数化 | 单/多局、首末步、空合法集、并行1/N、截断、超时与恢复边界；不越过批准输出范围 |
| T-TRAIN-005-I01 | `test_train_005_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法动作、隐藏truth观测、第二规则引擎、错误版本或损坏快照必须稳定处理；断言稳定错误码和失败原子性 |
| T-TRAIN-005-P01 | `test_train_005_properties` | 固定seed生成器；seed写入报告 | 同seed确定回放；策略观测无truth；每项reward追踪真实计分或显式势能差 |
| T-TRAIN-005-R01 | `test_train_005_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-TRAIN-005-X01 | `test_train_005_integration_contract` | 生产入口fixture | 训练环境必须导入并调用生产Rule/State/Score实现，执行生产等价golden；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_train_005.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`TRAIN-005-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## TRAIN-006 单 learner reset/step/mask/clone/restore

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [TRAIN-006](../03-unit-specs/training_environment_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_train_006.py` |
| 向量文件 | `tests/spec_v3/vectors/train_006.jsonl` |
| pytest标记 | `training,production_parity,replay,train` |
| 主要输入 | env state + learner action |
| 主要输出 | transition/snapshot |
| 本卡焦点 | game_id/seed、确定回放、快照恢复逐字段等价 |
| oracle | 逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-TRAIN-006-N01 | `test_train_006_normal_golden` | JSONL `case=normal` | game_id/seed、确定回放、快照恢复逐字段等价；逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| T-TRAIN-006-B01 | `test_train_006_boundary_table` | JSONL `case=boundary` 参数化 | 单/多局、首末步、空合法集、并行1/N、截断、超时与恢复边界；不越过批准输出范围 |
| T-TRAIN-006-I01 | `test_train_006_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法动作、隐藏truth观测、第二规则引擎、错误版本或损坏快照必须稳定处理；断言稳定错误码和失败原子性 |
| T-TRAIN-006-P01 | `test_train_006_properties` | 固定seed生成器；seed写入报告 | 同seed确定回放；策略观测无truth；每项reward追踪真实计分或显式势能差 |
| T-TRAIN-006-R01 | `test_train_006_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-TRAIN-006-X01 | `test_train_006_integration_contract` | 生产入口fixture | 训练环境必须导入并调用生产Rule/State/Score实现，执行生产等价golden；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_train_006.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`TRAIN-006-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## TRAIN-007 多玩家 ActionMap 与自博弈调度

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [TRAIN-007](../03-unit-specs/training_environment_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_train_007.py` |
| 向量文件 | `tests/spec_v3/vectors/train_007.jsonl` |
| pytest标记 | `training,production_parity,replay,train` |
| 主要输入 | joint observations/actions |
| 主要输出 | joint transition |
| 本卡焦点 | 多玩家 ActionMap 与自博弈调度的批准输入、输出和验收边界 |
| oracle | 逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-TRAIN-007-N01 | `test_train_007_normal_golden` | JSONL `case=normal` | 多玩家 ActionMap 与自博弈调度的批准输入、输出和验收边界；逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| T-TRAIN-007-B01 | `test_train_007_boundary_table` | JSONL `case=boundary` 参数化 | 单/多局、首末步、空合法集、并行1/N、截断、超时与恢复边界；不越过批准输出范围 |
| T-TRAIN-007-I01 | `test_train_007_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法动作、隐藏truth观测、第二规则引擎、错误版本或损坏快照必须稳定处理；断言稳定错误码和失败原子性 |
| T-TRAIN-007-P01 | `test_train_007_properties` | 固定seed生成器；seed写入报告 | 同seed确定回放；策略观测无truth；每项reward追踪真实计分或显式势能差 |
| T-TRAIN-007-R01 | `test_train_007_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-TRAIN-007-X01 | `test_train_007_integration_contract` | 生产入口fixture | 训练环境必须导入并调用生产Rule/State/Score实现，执行生产等价golden；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_train_007.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`TRAIN-007-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## TRAIN-008 离线 BC 与回放 RL 数据消费

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [TRAIN-008](../03-unit-specs/training_environment_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_train_008.py` |
| 向量文件 | `tests/spec_v3/vectors/train_008.jsonl` |
| pytest标记 | `training,production_parity,replay,train` |
| 主要输入 | versioned trajectories |
| 主要输出 | batches/updates |
| 本卡焦点 | 离线 BC 与回放 RL 数据消费的批准输入、输出和验收边界 |
| oracle | 逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-TRAIN-008-N01 | `test_train_008_normal_golden` | JSONL `case=normal` | 离线 BC 与回放 RL 数据消费的批准输入、输出和验收边界；逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| T-TRAIN-008-B01 | `test_train_008_boundary_table` | JSONL `case=boundary` 参数化 | 单/多局、首末步、空合法集、并行1/N、截断、超时与恢复边界；不越过批准输出范围 |
| T-TRAIN-008-I01 | `test_train_008_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法动作、隐藏truth观测、第二规则引擎、错误版本或损坏快照必须稳定处理；断言稳定错误码和失败原子性 |
| T-TRAIN-008-P01 | `test_train_008_properties` | 固定seed生成器；seed写入报告 | 同seed确定回放；策略观测无truth；每项reward追踪真实计分或显式势能差 |
| T-TRAIN-008-R01 | `test_train_008_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-TRAIN-008-X01 | `test_train_008_integration_contract` | 生产入口fixture | 训练环境必须导入并调用生产Rule/State/Score实现，执行生产等价golden；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_train_008.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`TRAIN-008-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## TRAIN-009 房规、profile 与行为域随机化

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [TRAIN-009](../03-unit-specs/training_environment_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_train_009.py` |
| 向量文件 | `tests/spec_v3/vectors/train_009.jsonl` |
| pytest标记 | `training,production_parity,replay,train` |
| 主要输入 | domain seed + allowed ranges |
| 主要输出 | sampled domain |
| 本卡焦点 | 房规、profile 与行为域随机化的批准输入、输出和验收边界 |
| oracle | 逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-TRAIN-009-N01 | `test_train_009_normal_golden` | JSONL `case=normal` | 房规、profile 与行为域随机化的批准输入、输出和验收边界；逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照 |
| T-TRAIN-009-B01 | `test_train_009_boundary_table` | JSONL `case=boundary` 参数化 | 单/多局、首末步、空合法集、并行1/N、截断、超时与恢复边界；不越过批准输出范围 |
| T-TRAIN-009-I01 | `test_train_009_invalid_rejected` | JSONL `case=invalid` 参数化 | 非法动作、隐藏truth观测、第二规则引擎、错误版本或损坏快照必须稳定处理；断言稳定错误码和失败原子性 |
| T-TRAIN-009-P01 | `test_train_009_properties` | 固定seed生成器；seed写入报告 | 同seed确定回放；策略观测无truth；每项reward追踪真实计分或显式势能差 |
| T-TRAIN-009-R01 | `test_train_009_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-TRAIN-009-X01 | `test_train_009_integration_contract` | 生产入口fixture | 训练环境必须导入并调用生产Rule/State/Score实现，执行生产等价golden；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_train_009.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`TRAIN-009-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

