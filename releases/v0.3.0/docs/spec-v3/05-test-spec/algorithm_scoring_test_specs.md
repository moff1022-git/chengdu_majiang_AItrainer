# ALGO/SCORE 单元可执行测试规格

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 覆盖 | ALGO等，共17单元 |
| 单元规格 | Approved |
| 测试实现/验收 | Not Implemented / Not Evaluated |

本文件规定测试代码、向量、断言和证据合同；详细业务定义仍只来自已批准单元规格。本文件存在不表示测试文件、fixture或行为已实现。

## ALGO-001 face/physical tile 编码、投影与所有权守恒

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [ALGO-001](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_algo_001.py` |
| 向量文件 | `tests/spec_v3/vectors/algo_001.jsonl` |
| pytest标记 | `deterministic,algorithm,formula,algo` |
| 主要输入 | physical regions |
| 主要输出 | face views + conservation result |
| 本卡焦点 | 108张physical_id唯一归属及face投影计数≤4 |
| oracle | 对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-ALGO-001-N01 | `test_algo_001_normal_golden` | JSONL `case=normal` | 108张physical_id唯一归属及face投影计数≤4；对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| T-ALGO-001-B01 | `test_algo_001_boundary_table` | JSONL `case=boundary` 参数化 | 空/最小/最大向量、计数0/4、上下界、候选上限及数值溢出边界；不越过批准输出范围 |
| T-ALGO-001-I01 | `test_algo_001_invalid_rejected` | JSONL `case=invalid` 参数化 | null、越界、重复实体、非有限数、版本冲突或隐藏字段投毒必须稳定失败；断言稳定错误码和失败原子性 |
| T-ALGO-001-P01 | `test_algo_001_properties` | 固定seed生成器；seed写入报告 | 排列不变性/单调性/守恒按卡适用；确定算法不得调用训练模型；同seed复现 |
| T-ALGO-001-R01 | `test_algo_001_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-ALGO-001-X01 | `test_algo_001_integration_contract` | 生产入口fixture | 从白名单PlayerView或权威引擎接口取输入，验证输出可被下游消费；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_algo_001.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`ALGO-001-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## ALGO-002 手牌分解、向听、弃牌向听与等待形状

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [ALGO-002](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_algo_002.py` |
| 向量文件 | `tests/spec_v3/vectors/algo_002.jsonl` |
| pytest标记 | `deterministic,algorithm,formula,algo` |
| 主要输入 | concealed faces + melds |
| 主要输出 | analyses |
| 本卡焦点 | 普通牌/七对向听、有效进张、死叫和等待形状golden |
| oracle | 对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-ALGO-002-N01 | `test_algo_002_normal_golden` | JSONL `case=normal` | 普通牌/七对向听、有效进张、死叫和等待形状golden；对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| T-ALGO-002-B01 | `test_algo_002_boundary_table` | JSONL `case=boundary` 参数化 | 空/最小/最大向量、计数0/4、上下界、候选上限及数值溢出边界；不越过批准输出范围 |
| T-ALGO-002-I01 | `test_algo_002_invalid_rejected` | JSONL `case=invalid` 参数化 | null、越界、重复实体、非有限数、版本冲突或隐藏字段投毒必须稳定失败；断言稳定错误码和失败原子性 |
| T-ALGO-002-P01 | `test_algo_002_properties` | 固定seed生成器；seed写入报告 | 排列不变性/单调性/守恒按卡适用；确定算法不得调用训练模型；同seed复现 |
| T-ALGO-002-R01 | `test_algo_002_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-ALGO-002-X01 | `test_algo_002_integration_contract` | 生产入口fixture | 从白名单PlayerView或权威引擎接口取输入，验证输出可被下游消费；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_algo_002.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`ALGO-002-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## ALGO-003 去重可见牌与未见牌聚合

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [ALGO-003](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_algo_003.py` |
| 向量文件 | `tests/spec_v3/vectors/algo_003.jsonl` |
| pytest标记 | `deterministic,algorithm,formula,algo` |
| 主要输入 | PlayerView |
| 主要输出 | visible/unseen counts |
| 本卡焦点 | 同一事件牌去重、可见数与未见数 |
| oracle | 对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-ALGO-003-N01 | `test_algo_003_normal_golden` | JSONL `case=normal` | 同一事件牌去重、可见数与未见数；对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| T-ALGO-003-B01 | `test_algo_003_boundary_table` | JSONL `case=boundary` 参数化 | 空/最小/最大向量、计数0/4、上下界、候选上限及数值溢出边界；不越过批准输出范围 |
| T-ALGO-003-I01 | `test_algo_003_invalid_rejected` | JSONL `case=invalid` 参数化 | null、越界、重复实体、非有限数、版本冲突或隐藏字段投毒必须稳定失败；断言稳定错误码和失败原子性 |
| T-ALGO-003-P01 | `test_algo_003_properties` | 固定seed生成器；seed写入报告 | 排列不变性/单调性/守恒按卡适用；确定算法不得调用训练模型；同seed复现 |
| T-ALGO-003-R01 | `test_algo_003_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-ALGO-003-X01 | `test_algo_003_integration_contract` | 生产入口fixture | 从白名单PlayerView或权威引擎接口取输入，验证输出可被下游消费；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_algo_003.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`ALGO-003-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## ALGO-004 墙内活牌区间或估计

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [ALGO-004](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_algo_004.py` |
| 向量文件 | `tests/spec_v3/vectors/algo_004.jsonl` |
| pytest标记 | `deterministic,algorithm,formula,algo` |
| 主要输入 | unseen + public allocations |
| 主要输出 | live estimate |
| 本卡焦点 | 未见牌与墙内活牌区间不得混同 |
| oracle | 对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-ALGO-004-N01 | `test_algo_004_normal_golden` | JSONL `case=normal` | 未见牌与墙内活牌区间不得混同；对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| T-ALGO-004-B01 | `test_algo_004_boundary_table` | JSONL `case=boundary` 参数化 | 空/最小/最大向量、计数0/4、上下界、候选上限及数值溢出边界；不越过批准输出范围 |
| T-ALGO-004-I01 | `test_algo_004_invalid_rejected` | JSONL `case=invalid` 参数化 | null、越界、重复实体、非有限数、版本冲突或隐藏字段投毒必须稳定失败；断言稳定错误码和失败原子性 |
| T-ALGO-004-P01 | `test_algo_004_properties` | 固定seed生成器；seed写入报告 | 排列不变性/单调性/守恒按卡适用；确定算法不得调用训练模型；同seed复现 |
| T-ALGO-004-R01 | `test_algo_004_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-ALGO-004-X01 | `test_algo_004_integration_contract` | 生产入口fixture | 从白名单PlayerView或权威引擎接口取输入，验证输出可被下游消费；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_algo_004.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`ALGO-004-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## ALGO-005 逐座剩余摸牌机会估计

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [ALGO-005](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_algo_005.py` |
| 向量文件 | `tests/spec_v3/vectors/algo_005.jsonl` |
| pytest标记 | `deterministic,algorithm,formula,algo` |
| 主要输入 | active order + wall + response assumptions |
| 主要输出 | draw interval |
| 本卡焦点 | 活动座次、墙长和胡后退出下的摸牌机会区间 |
| oracle | 对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-ALGO-005-N01 | `test_algo_005_normal_golden` | JSONL `case=normal` | 活动座次、墙长和胡后退出下的摸牌机会区间；对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| T-ALGO-005-B01 | `test_algo_005_boundary_table` | JSONL `case=boundary` 参数化 | 空/最小/最大向量、计数0/4、上下界、候选上限及数值溢出边界；不越过批准输出范围 |
| T-ALGO-005-I01 | `test_algo_005_invalid_rejected` | JSONL `case=invalid` 参数化 | null、越界、重复实体、非有限数、版本冲突或隐藏字段投毒必须稳定失败；断言稳定错误码和失败原子性 |
| T-ALGO-005-P01 | `test_algo_005_properties` | 固定seed生成器；seed写入报告 | 排列不变性/单调性/守恒按卡适用；确定算法不得调用训练模型；同seed复现 |
| T-ALGO-005-R01 | `test_algo_005_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-ALGO-005-X01 | `test_algo_005_integration_contract` | 生产入口fixture | 从白名单PlayerView或权威引擎接口取输入，验证输出可被下游消费；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_algo_005.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`ALGO-005-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## ALGO-006 mandatory 分类、候选上限与稳定排序

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [ALGO-006](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_algo_006.py` |
| 向量文件 | `tests/spec_v3/vectors/algo_006.jsonl` |
| pytest标记 | `deterministic,algorithm,formula,algo` |
| 主要输入 | legal actions + context |
| 主要输出 | mandatory/candidate set |
| 本卡焦点 | mandatory 分类、候选上限与稳定排序的批准输入、输出和验收边界 |
| oracle | 对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-ALGO-006-N01 | `test_algo_006_normal_golden` | JSONL `case=normal` | mandatory 分类、候选上限与稳定排序的批准输入、输出和验收边界；对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| T-ALGO-006-B01 | `test_algo_006_boundary_table` | JSONL `case=boundary` 参数化 | 空/最小/最大向量、计数0/4、上下界、候选上限及数值溢出边界；不越过批准输出范围 |
| T-ALGO-006-I01 | `test_algo_006_invalid_rejected` | JSONL `case=invalid` 参数化 | null、越界、重复实体、非有限数、版本冲突或隐藏字段投毒必须稳定失败；断言稳定错误码和失败原子性 |
| T-ALGO-006-P01 | `test_algo_006_properties` | 固定seed生成器；seed写入报告 | 排列不变性/单调性/守恒按卡适用；确定算法不得调用训练模型；同seed复现 |
| T-ALGO-006-R01 | `test_algo_006_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-ALGO-006-X01 | `test_algo_006_integration_contract` | 生产入口fixture | 从白名单PlayerView或权威引擎接口取输入，验证输出可被下游消费；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_algo_006.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`ALGO-006-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## ALGO-007 六分量候选 Q 评价

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [ALGO-007](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_algo_007.py` |
| 向量文件 | `tests/spec_v3/vectors/algo_007.jsonl` |
| pytest标记 | `deterministic,algorithm,formula,algo` |
| 主要输入 | normalized features + weights |
| 主要输出 | Q components/total |
| 本卡焦点 | 六分量候选 Q 评价的批准输入、输出和验收边界 |
| oracle | 对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-ALGO-007-N01 | `test_algo_007_normal_golden` | JSONL `case=normal` | 六分量候选 Q 评价的批准输入、输出和验收边界；对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| T-ALGO-007-B01 | `test_algo_007_boundary_table` | JSONL `case=boundary` 参数化 | 空/最小/最大向量、计数0/4、上下界、候选上限及数值溢出边界；不越过批准输出范围 |
| T-ALGO-007-I01 | `test_algo_007_invalid_rejected` | JSONL `case=invalid` 参数化 | null、越界、重复实体、非有限数、版本冲突或隐藏字段投毒必须稳定失败；断言稳定错误码和失败原子性 |
| T-ALGO-007-P01 | `test_algo_007_properties` | 固定seed生成器；seed写入报告 | 排列不变性/单调性/守恒按卡适用；确定算法不得调用训练模型；同seed复现 |
| T-ALGO-007-R01 | `test_algo_007_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-ALGO-007-X01 | `test_algo_007_integration_contract` | 生产入口fixture | 从白名单PlayerView或权威引擎接口取输入，验证输出可被下游消费；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_algo_007.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`ALGO-007-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## ALGO-008 seed、噪声、思考时间与随机流确定派生

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [ALGO-008](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_algo_008.py` |
| 向量文件 | `tests/spec_v3/vectors/algo_008.jsonl` |
| pytest标记 | `deterministic,algorithm,formula,algo` |
| 主要输入 | game_id/seat/decision/config |
| 主要输出 | reproducible samples |
| 本卡焦点 | seed、噪声、思考时间与随机流确定派生的批准输入、输出和验收边界 |
| oracle | 对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-ALGO-008-N01 | `test_algo_008_normal_golden` | JSONL `case=normal` | seed、噪声、思考时间与随机流确定派生的批准输入、输出和验收边界；对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| T-ALGO-008-B01 | `test_algo_008_boundary_table` | JSONL `case=boundary` 参数化 | 空/最小/最大向量、计数0/4、上下界、候选上限及数值溢出边界；不越过批准输出范围 |
| T-ALGO-008-I01 | `test_algo_008_invalid_rejected` | JSONL `case=invalid` 参数化 | null、越界、重复实体、非有限数、版本冲突或隐藏字段投毒必须稳定失败；断言稳定错误码和失败原子性 |
| T-ALGO-008-P01 | `test_algo_008_properties` | 固定seed生成器；seed写入报告 | 排列不变性/单调性/守恒按卡适用；确定算法不得调用训练模型；同seed复现 |
| T-ALGO-008-R01 | `test_algo_008_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-ALGO-008-X01 | `test_algo_008_integration_contract` | 生产入口fixture | 从白名单PlayerView或权威引擎接口取输入，验证输出可被下游消费；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_algo_008.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`ALGO-008-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## ALGO-009 配置类型/范围/版本校验、迁移与 canonical hash

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [ALGO-009](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_algo_009.py` |
| 向量文件 | `tests/spec_v3/vectors/algo_009.jsonl` |
| pytest标记 | `deterministic,algorithm,formula,algo` |
| 主要输入 | raw config |
| 主要输出 | frozen config/hash or explicit error |
| 本卡焦点 | 配置类型/范围/版本校验、迁移与 canonical hash的批准输入、输出和验收边界 |
| oracle | 对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-ALGO-009-N01 | `test_algo_009_normal_golden` | JSONL `case=normal` | 配置类型/范围/版本校验、迁移与 canonical hash的批准输入、输出和验收边界；对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| T-ALGO-009-B01 | `test_algo_009_boundary_table` | JSONL `case=boundary` 参数化 | 空/最小/最大向量、计数0/4、上下界、候选上限及数值溢出边界；不越过批准输出范围 |
| T-ALGO-009-I01 | `test_algo_009_invalid_rejected` | JSONL `case=invalid` 参数化 | null、越界、重复实体、非有限数、版本冲突或隐藏字段投毒必须稳定失败；断言稳定错误码和失败原子性 |
| T-ALGO-009-P01 | `test_algo_009_properties` | 固定seed生成器；seed写入报告 | 排列不变性/单调性/守恒按卡适用；确定算法不得调用训练模型；同seed复现 |
| T-ALGO-009-R01 | `test_algo_009_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-ALGO-009-X01 | `test_algo_009_integration_contract` | 生产入口fixture | 从白名单PlayerView或权威引擎接口取输入，验证输出可被下游消费；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_algo_009.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`ALGO-009-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## ALGO-010 PlayerView 白名单构建

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [ALGO-010](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_algo_010.py` |
| 向量文件 | `tests/spec_v3/vectors/algo_010.jsonl` |
| pytest标记 | `deterministic,algorithm,formula,algo` |
| 主要输入 | authoritative state + seat + phase |
| 主要输出 | PlayerView |
| 本卡焦点 | PlayerView 白名单构建的批准输入、输出和验收边界 |
| oracle | 对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-ALGO-010-N01 | `test_algo_010_normal_golden` | JSONL `case=normal` | PlayerView 白名单构建的批准输入、输出和验收边界；对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| T-ALGO-010-B01 | `test_algo_010_boundary_table` | JSONL `case=boundary` 参数化 | 空/最小/最大向量、计数0/4、上下界、候选上限及数值溢出边界；不越过批准输出范围 |
| T-ALGO-010-I01 | `test_algo_010_invalid_rejected` | JSONL `case=invalid` 参数化 | null、越界、重复实体、非有限数、版本冲突或隐藏字段投毒必须稳定失败；断言稳定错误码和失败原子性 |
| T-ALGO-010-P01 | `test_algo_010_properties` | 固定seed生成器；seed写入报告 | 排列不变性/单调性/守恒按卡适用；确定算法不得调用训练模型；同seed复现 |
| T-ALGO-010-R01 | `test_algo_010_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-ALGO-010-X01 | `test_algo_010_integration_contract` | 生产入口fixture | 从白名单PlayerView或权威引擎接口取输入，验证输出可被下游消费；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_algo_010.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`ALGO-010-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## ALGO-011 game_id 到牌墙、骰子及子随机流的确定映射

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [ALGO-011](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_algo_011.py` |
| 向量文件 | `tests/spec_v3/vectors/algo_011.jsonl` |
| pytest标记 | `deterministic,algorithm,formula,algo` |
| 主要输入 | game_id + versions |
| 主要输出 | named RNG streams |
| 本卡焦点 | game_id命名随机流域隔离与调用顺序无关 |
| oracle | 对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-ALGO-011-N01 | `test_algo_011_normal_golden` | JSONL `case=normal` | game_id命名随机流域隔离与调用顺序无关；对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差 |
| T-ALGO-011-B01 | `test_algo_011_boundary_table` | JSONL `case=boundary` 参数化 | 空/最小/最大向量、计数0/4、上下界、候选上限及数值溢出边界；不越过批准输出范围 |
| T-ALGO-011-I01 | `test_algo_011_invalid_rejected` | JSONL `case=invalid` 参数化 | null、越界、重复实体、非有限数、版本冲突或隐藏字段投毒必须稳定失败；断言稳定错误码和失败原子性 |
| T-ALGO-011-P01 | `test_algo_011_properties` | 固定seed生成器；seed写入报告 | 排列不变性/单调性/守恒按卡适用；确定算法不得调用训练模型；同seed复现 |
| T-ALGO-011-R01 | `test_algo_011_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-ALGO-011-X01 | `test_algo_011_integration_contract` | 生产入口fixture | 从白名单PlayerView或权威引擎接口取输入，验证输出可被下游消费；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_algo_011.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`ALGO-011-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## SCORE-001 分数账本分层与守恒

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [SCORE-001](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_score_001.py` |
| 向量文件 | `tests/spec_v3/vectors/score_001.jsonl` |
| pytest标记 | `deterministic,score,zero_sum,hard_gate,score` |
| 主要输入 | score events |
| 主要输出 | ledger/before/after |
| 本卡焦点 | 番型识别、互斥/叠加、封顶和确定排序 |
| oracle | 逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-SCORE-001-N01 | `test_score_001_normal_golden` | JSONL `case=normal` | 番型识别、互斥/叠加、封顶和确定排序；逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名 |
| T-SCORE-001-B01 | `test_score_001_boundary_table` | JSONL `case=boundary` 参数化 | 0番/封顶、单/多接收方、最小/最大玩家数、空杠链与终局边界；不越过批准输出范围 |
| T-SCORE-001-I01 | `test_score_001_invalid_rejected` | JSONL `case=invalid` 参数化 | 未知番、非法支付方、重复转移、负溢出或来源事件缺失必须稳定失败；断言稳定错误码和失败原子性 |
| T-SCORE-001-P01 | `test_score_001_properties` | 固定seed生成器；seed写入报告 | 每个原子事件、结算层和本局总账均满足ΣΔ=0；重放不重复入账 |
| T-SCORE-001-R01 | `test_score_001_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-SCORE-001-X01 | `test_score_001_integration_contract` | 生产入口fixture | 由生产规则事实驱动ScoreTransfer并写唯一账本，不直接改累计分；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_score_001.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`SCORE-001-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## SCORE-002 自摸、点炮与抢杠胡计分

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [SCORE-002](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_score_002.py` |
| 向量文件 | `tests/spec_v3/vectors/score_002.jsonl` |
| pytest标记 | `deterministic,score,zero_sum,hard_gate,score` |
| 主要输入 | hu facts + fan policy |
| 主要输出 | hu transfers |
| 本卡焦点 | 自摸/点炮/抢杠胡支付方向及逐事件零和 |
| oracle | 逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-SCORE-002-N01 | `test_score_002_normal_golden` | JSONL `case=normal` | 自摸/点炮/抢杠胡支付方向及逐事件零和；逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名 |
| T-SCORE-002-B01 | `test_score_002_boundary_table` | JSONL `case=boundary` 参数化 | 0番/封顶、单/多接收方、最小/最大玩家数、空杠链与终局边界；不越过批准输出范围 |
| T-SCORE-002-I01 | `test_score_002_invalid_rejected` | JSONL `case=invalid` 参数化 | 未知番、非法支付方、重复转移、负溢出或来源事件缺失必须稳定失败；断言稳定错误码和失败原子性 |
| T-SCORE-002-P01 | `test_score_002_properties` | 固定seed生成器；seed写入报告 | 每个原子事件、结算层和本局总账均满足ΣΔ=0；重放不重复入账 |
| T-SCORE-002-R01 | `test_score_002_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-SCORE-002-X01 | `test_score_002_integration_contract` | 生产入口fixture | 由生产规则事实驱动ScoreTransfer并写唯一账本，不直接改累计分；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_score_002.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`SCORE-002-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## SCORE-003 明/暗/补杠与呼叫转移计分

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [SCORE-003](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_score_003.py` |
| 向量文件 | `tests/spec_v3/vectors/score_003.jsonl` |
| pytest标记 | `deterministic,score,zero_sum,hard_gate,score` |
| 主要输入 | gang events + rules |
| 主要输出 | gang transfers |
| 本卡焦点 | 明杠/暗杠/补杠、取消与呼叫转移链接 |
| oracle | 逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-SCORE-003-N01 | `test_score_003_normal_golden` | JSONL `case=normal` | 明杠/暗杠/补杠、取消与呼叫转移链接；逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名 |
| T-SCORE-003-B01 | `test_score_003_boundary_table` | JSONL `case=boundary` 参数化 | 0番/封顶、单/多接收方、最小/最大玩家数、空杠链与终局边界；不越过批准输出范围 |
| T-SCORE-003-I01 | `test_score_003_invalid_rejected` | JSONL `case=invalid` 参数化 | 未知番、非法支付方、重复转移、负溢出或来源事件缺失必须稳定失败；断言稳定错误码和失败原子性 |
| T-SCORE-003-P01 | `test_score_003_properties` | 固定seed生成器；seed写入报告 | 每个原子事件、结算层和本局总账均满足ΣΔ=0；重放不重复入账 |
| T-SCORE-003-R01 | `test_score_003_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-SCORE-003-X01 | `test_score_003_integration_contract` | 生产入口fixture | 由生产规则事实驱动ScoreTransfer并写唯一账本，不直接改累计分；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_score_003.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`SCORE-003-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## SCORE-004 花猪、查大叫与退税终局调整

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [SCORE-004](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_score_004.py` |
| 向量文件 | `tests/spec_v3/vectors/score_004.jsonl` |
| pytest标记 | `deterministic,score,zero_sum,hard_gate,score` |
| 主要输入 | end state + rules |
| 主要输出 | adjustments |
| 本卡焦点 | 花猪、查大叫、死叫口径和退税来源链 |
| oracle | 逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-SCORE-004-N01 | `test_score_004_normal_golden` | JSONL `case=normal` | 花猪、查大叫、死叫口径和退税来源链；逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名 |
| T-SCORE-004-B01 | `test_score_004_boundary_table` | JSONL `case=boundary` 参数化 | 0番/封顶、单/多接收方、最小/最大玩家数、空杠链与终局边界；不越过批准输出范围 |
| T-SCORE-004-I01 | `test_score_004_invalid_rejected` | JSONL `case=invalid` 参数化 | 未知番、非法支付方、重复转移、负溢出或来源事件缺失必须稳定失败；断言稳定错误码和失败原子性 |
| T-SCORE-004-P01 | `test_score_004_properties` | 固定seed生成器；seed写入报告 | 每个原子事件、结算层和本局总账均满足ΣΔ=0；重放不重复入账 |
| T-SCORE-004-R01 | `test_score_004_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-SCORE-004-X01 | `test_score_004_integration_contract` | 生产入口fixture | 由生产规则事实驱动ScoreTransfer并写唯一账本，不直接改累计分；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_score_004.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`SCORE-004-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## SCORE-005 封顶、互斥和转移结算顺序

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [SCORE-005](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_score_005.py` |
| 向量文件 | `tests/spec_v3/vectors/score_005.jsonl` |
| pytest标记 | `deterministic,score,zero_sum,hard_gate,score` |
| 主要输入 | raw components + cap policy |
| 主要输出 | final transfers |
| 本卡焦点 | 原子转移幂等、分层账本与ΣΔ=0 |
| oracle | 逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-SCORE-005-N01 | `test_score_005_normal_golden` | JSONL `case=normal` | 原子转移幂等、分层账本与ΣΔ=0；逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名 |
| T-SCORE-005-B01 | `test_score_005_boundary_table` | JSONL `case=boundary` 参数化 | 0番/封顶、单/多接收方、最小/最大玩家数、空杠链与终局边界；不越过批准输出范围 |
| T-SCORE-005-I01 | `test_score_005_invalid_rejected` | JSONL `case=invalid` 参数化 | 未知番、非法支付方、重复转移、负溢出或来源事件缺失必须稳定失败；断言稳定错误码和失败原子性 |
| T-SCORE-005-P01 | `test_score_005_properties` | 固定seed生成器；seed写入报告 | 每个原子事件、结算层和本局总账均满足ΣΔ=0；重放不重复入账 |
| T-SCORE-005-R01 | `test_score_005_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-SCORE-005-X01 | `test_score_005_integration_contract` | 生产入口fixture | 由生产规则事实驱动ScoreTransfer并写唯一账本，不直接改累计分；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_score_005.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`SCORE-005-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## SCORE-006 单局总分、整场累计与排名

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [SCORE-006](../03-unit-specs/deterministic_algorithm_scoring_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_score_006.py` |
| 向量文件 | `tests/spec_v3/vectors/score_006.jsonl` |
| pytest标记 | `deterministic,score,zero_sum,hard_gate,score` |
| 主要输入 | ledgers + prior standings |
| 主要输出 | result/rank |
| 本卡焦点 | 本局累计、跨局累计、并列排名与稳定次序 |
| oracle | 逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-SCORE-006-N01 | `test_score_006_normal_golden` | JSONL `case=normal` | 本局累计、跨局累计、并列排名与稳定次序；逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名 |
| T-SCORE-006-B01 | `test_score_006_boundary_table` | JSONL `case=boundary` 参数化 | 0番/封顶、单/多接收方、最小/最大玩家数、空杠链与终局边界；不越过批准输出范围 |
| T-SCORE-006-I01 | `test_score_006_invalid_rejected` | JSONL `case=invalid` 参数化 | 未知番、非法支付方、重复转移、负溢出或来源事件缺失必须稳定失败；断言稳定错误码和失败原子性 |
| T-SCORE-006-P01 | `test_score_006_properties` | 固定seed生成器；seed写入报告 | 每个原子事件、结算层和本局总账均满足ΣΔ=0；重放不重复入账 |
| T-SCORE-006-R01 | `test_score_006_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-SCORE-006-X01 | `test_score_006_integration_contract` | 生产入口fixture | 由生产规则事实驱动ScoreTransfer并写唯一账本，不直接改累计分；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_score_006.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`SCORE-006-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

