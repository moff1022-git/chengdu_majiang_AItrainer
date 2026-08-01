# HEUR 单元可执行测试规格

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 覆盖 | HEUR等，共23单元 |
| 单元规格 | Approved |
| 测试实现/验收 | Not Implemented / Not Evaluated |

本文件规定测试代码、向量、断言和证据合同；详细业务定义仍只来自已批准单元规格。本文件存在不表示测试文件、fixture或行为已实现。

## HEUR-001 换三张候选评价

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-001](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_001.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_001.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | legal triples + hand/public features |
| 主要输出 | ranked triples |
| 本卡焦点 | 换三张同花色合法候选与选择分布 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-001-N01 | `test_heur_001_normal_golden` | JSONL `case=normal` | 换三张同花色合法候选与选择分布；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-001-B01 | `test_heur_001_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-001-I01 | `test_heur_001_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-001-P01 | `test_heur_001_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-001-R01 | `test_heur_001_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-001-X01 | `test_heur_001_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_001.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-001-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-002 定缺花色评价

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-002](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_002.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_002.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | hand structure + public context |
| 主要输出 | ranked suits |
| 本卡焦点 | 定缺候选评分、风格/水平/阶段方向效应 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-002-N01 | `test_heur_002_normal_golden` | JSONL `case=normal` | 定缺候选评分、风格/水平/阶段方向效应；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-002-B01 | `test_heur_002_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-002-I01 | `test_heur_002_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-002-P01 | `test_heur_002_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-002-R01 | `test_heur_002_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-002-X01 | `test_heur_002_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_002.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-002-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-003 动态风格调节

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-003](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_003.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_003.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | profile + score/stage/hand |
| 主要输出 | effective style knobs |
| 本卡焦点 | 动态风格调节的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-003-N01 | `test_heur_003_normal_golden` | JSONL `case=normal` | 动态风格调节的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-003-B01 | `test_heur_003_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-003-I01 | `test_heur_003_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-003-P01 | `test_heur_003_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-003-R01 | `test_heur_003_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-003-X01 | `test_heur_003_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_003.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-003-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-004 初始做牌方向形成

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-004](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_004.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_004.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | initial analysis + profile |
| 主要输出 | primary/backup direction |
| 本卡焦点 | 初始做牌方向形成的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-004-N01 | `test_heur_004_normal_golden` | JSONL `case=normal` | 初始做牌方向形成的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-004-B01 | `test_heur_004_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-004-I01 | `test_heur_004_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-004-P01 | `test_heur_004_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-004-R01 | `test_heur_004_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-004-X01 | `test_heur_004_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_004.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-004-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-005 主备计划生命周期

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-005](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_005.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_005.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | observations + current plan |
| 主要输出 | retain/switch/restart |
| 本卡焦点 | 主备计划生命周期的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-005-N01 | `test_heur_005_normal_golden` | JSONL `case=normal` | 主备计划生命周期的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-005-B01 | `test_heur_005_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-005-I01 | `test_heur_005_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-005-P01 | `test_heur_005_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-005-R01 | `test_heur_005_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-005-X01 | `test_heur_005_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_005.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-005-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-006 定缺花色环境评估

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-006](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_006.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_006.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | all public dingque/melds |
| 主要输出 | suit environment |
| 本卡焦点 | 定缺花色环境评估的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-006-N01 | `test_heur_006_normal_golden` | JSONL `case=normal` | 定缺花色环境评估的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-006-B01 | `test_heur_006_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-006-I01 | `test_heur_006_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-006-P01 | `test_heur_006_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-006-R01 | `test_heur_006_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-006-X01 | `test_heur_006_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_006.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-006-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-007 公开事件驱动的逐家方向更新

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-007](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_007.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_007.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | prior hypotheses + events |
| 主要输出 | heuristic direction evidence |
| 本卡焦点 | 公开事件驱动的逐家方向更新的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-007-N01 | `test_heur_007_normal_golden` | JSONL `case=normal` | 公开事件驱动的逐家方向更新的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-007-B01 | `test_heur_007_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-007-I01 | `test_heur_007_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-007-P01 | `test_heur_007_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-007-R01 | `test_heur_007_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-007-X01 | `test_heur_007_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_007.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-007-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-008 整场比分与剩余局效用调节

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-008](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_008.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_008.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | standings + rounds left |
| 主要输出 | match utility modifiers |
| 本卡焦点 | 整场比分与剩余局效用调节的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-008-N01 | `test_heur_008_normal_golden` | JSONL `case=normal` | 整场比分与剩余局效用调节的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-008-B01 | `test_heur_008_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-008-I01 | `test_heur_008_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-008-P01 | `test_heur_008_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-008-R01 | `test_heur_008_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-008-X01 | `test_heur_008_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_008.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-008-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-009 先胡、做大和血战顺序效用

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-009](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_009.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_009.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | hu order + hand value + risk |
| 主要输出 | speed/value preference |
| 本卡焦点 | 先胡、做大和血战顺序效用的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-009-N01 | `test_heur_009_normal_golden` | JSONL `case=normal` | 先胡、做大和血战顺序效用的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-009-B01 | `test_heur_009_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-009-I01 | `test_heur_009_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-009-P01 | `test_heur_009_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-009-R01 | `test_heur_009_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-009-X01 | `test_heur_009_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_009.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-009-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-010 多目标冲突复核

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-010](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_010.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_010.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | speed/fan/risk/plan/match signals |
| 主要输出 | resolved preference |
| 本卡焦点 | 过胡允许域、机会成本及强制胡旁路 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-010-N01 | `test_heur_010_normal_golden` | JSONL `case=normal` | 过胡允许域、机会成本及强制胡旁路；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-010-B01 | `test_heur_010_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-010-I01 | `test_heur_010_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-010-P01 | `test_heur_010_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-010-R01 | `test_heur_010_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-010-X01 | `test_heur_010_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_010.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-010-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-011 番型边际做牌价值

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-011](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_011.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_011.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | enabled fan policy + hand path |
| 主要输出 | marginal value |
| 本卡焦点 | 番型边际做牌价值的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-011-N01 | `test_heur_011_normal_golden` | JSONL `case=normal` | 番型边际做牌价值的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-011-B01 | `test_heur_011_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-011-I01 | `test_heur_011_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-011-P01 | `test_heur_011_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-011-R01 | `test_heur_011_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-011-X01 | `test_heur_011_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_011.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-011-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-012 碰牌策略评价

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-012](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_012.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_012.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | legal peng + structure/exposure/turn |
| 主要输出 | accept/pass score |
| 本卡焦点 | 碰牌策略评价的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-012-N01 | `test_heur_012_normal_golden` | JSONL `case=normal` | 碰牌策略评价的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-012-B01 | `test_heur_012_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-012-I01 | `test_heur_012_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-012-P01 | `test_heur_012_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-012-R01 | `test_heur_012_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-012-X01 | `test_heur_012_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_012.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-012-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-013 杠牌策略评价

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-013](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_013.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_013.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | legal gang + score/risk/rob context |
| 主要输出 | accept/pass score |
| 本卡焦点 | 杠牌策略评价的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-013-N01 | `test_heur_013_normal_golden` | JSONL `case=normal` | 杠牌策略评价的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-013-B01 | `test_heur_013_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-013-I01 | `test_heur_013_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-013-P01 | `test_heur_013_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-013-R01 | `test_heur_013_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-013-X01 | `test_heur_013_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_013.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-013-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-014 出牌牌效与结构保留策略

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-014](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_014.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_014.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | analyzed hand + legal discards |
| 主要输出 | strategic rank |
| 本卡焦点 | 出牌牌效与结构保留策略的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-014-N01 | `test_heur_014_normal_golden` | JSONL `case=normal` | 出牌牌效与结构保留策略的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-014-B01 | `test_heur_014_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-014-I01 | `test_heur_014_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-014-P01 | `test_heur_014_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-014-R01 | `test_heur_014_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-014-X01 | `test_heur_014_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_014.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-014-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-015 防守偏好与安全牌选择

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-015](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_015.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_015.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | per-seat risk + loss + profile |
| 主要输出 | defensive rank |
| 本卡焦点 | 防守偏好与安全牌选择的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-015-N01 | `test_heur_015_normal_golden` | JSONL `case=normal` | 防守偏好与安全牌选择的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-015-B01 | `test_heur_015_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-015-I01 | `test_heur_015_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-015-P01 | `test_heur_015_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-015-R01 | `test_heur_015_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-015-X01 | `test_heur_015_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_015.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-015-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-016 行为序列推断

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-016](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_016.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_016.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | ordered public actions |
| 主要输出 | behavioral cues |
| 本卡焦点 | 行为序列推断的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-016-N01 | `test_heur_016_normal_golden` | JSONL `case=normal` | 行为序列推断的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-016-B01 | `test_heur_016_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-016-I01 | `test_heur_016_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-016-P01 | `test_heur_016_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-016-R01 | `test_heur_016_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-016-X01 | `test_heur_016_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_016.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-016-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-017 思考节奏生成

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-017](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_017.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_017.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | complexity + profile + deadline |
| 主要输出 | planned think time |
| 本卡焦点 | 危险牌风险排序与无oracle回退 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-017-N01 | `test_heur_017_normal_golden` | JSONL `case=normal` | 危险牌风险排序与无oracle回退；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-017-B01 | `test_heur_017_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-017-I01 | `test_heur_017_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-017-P01 | `test_heur_017_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-017-R01 | `test_heur_017_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-017-X01 | `test_heur_017_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_017.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-017-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-018 安全牌储备、扣牌与信息表达

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-018](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_018.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_018.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | hand/public threats/self exposure |
| 主要输出 | retention preference |
| 本卡焦点 | 安全牌储备、扣牌与信息表达的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-018-N01 | `test_heur_018_normal_golden` | JSONL `case=normal` | 安全牌储备、扣牌与信息表达的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-018-B01 | `test_heur_018_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-018-I01 | `test_heur_018_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-018-P01 | `test_heur_018_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-018-R01 | `test_heur_018_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-018-X01 | `test_heur_018_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_018.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-018-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-019 Top-K 有限注意分配

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-019](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_019.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_019.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | visible cues + capacity |
| 主要输出 | attended items |
| 本卡焦点 | Top-K 有限注意分配的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-019-N01 | `test_heur_019_normal_golden` | JSONL `case=normal` | Top-K 有限注意分配的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-019-B01 | `test_heur_019_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-019-I01 | `test_heur_019_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-019-P01 | `test_heur_019_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-019-R01 | `test_heur_019_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-019-X01 | `test_heur_019_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_019.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-019-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-020 有界记忆衰减与强化

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-020](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_020.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_020.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | visible events + memory config |
| 主要输出 | memory snapshot |
| 本卡焦点 | 有界记忆衰减与强化的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-020-N01 | `test_heur_020_normal_golden` | JSONL `case=normal` | 有界记忆衰减与强化的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-020-B01 | `test_heur_020_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-020-I01 | `test_heur_020_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-020-P01 | `test_heur_020_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-020-R01 | `test_heur_020_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-020-X01 | `test_heur_020_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_020.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-020-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-021 有限推演与满意停止

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-021](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_021.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_021.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | candidates + budget/threshold |
| 主要输出 | checked set/stop reason |
| 本卡焦点 | mandatory保留、有限候选上限和注意预算 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-021-N01 | `test_heur_021_normal_golden` | JSONL `case=normal` | mandatory保留、有限候选上限和注意预算；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-021-B01 | `test_heur_021_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-021-I01 | `test_heur_021_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-021-P01 | `test_heur_021_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-021-R01 | `test_heur_021_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-021-X01 | `test_heur_021_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_021.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-021-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-022 人格、水平与情绪状态消费

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-022](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_022.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_022.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | profile + short state |
| 主要输出 | decision modifiers |
| 本卡焦点 | 人格、水平与情绪状态消费的批准输入、输出和验收边界 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-022-N01 | `test_heur_022_normal_golden` | JSONL `case=normal` | 人格、水平与情绪状态消费的批准输入、输出和验收边界；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-022-B01 | `test_heur_022_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-022-I01 | `test_heur_022_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-022-P01 | `test_heur_022_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-022-R01 | `test_heur_022_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-022-X01 | `test_heur_022_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_022.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-022-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## HEUR-023 有界近似选择与人类失误

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [HEUR-023](../03-unit-specs/human_heuristic_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_heur_023.py` |
| 向量文件 | `tests/spec_v3/vectors/heur_023.jsonl` |
| pytest标记 | `heuristic,statistical,visibility,heur` |
| 主要输入 | checked candidates + bounded noise |
| 主要输出 | chosen legal action |
| 本卡焦点 | 人类失误率、regret上界与思考时间分布 |
| oracle | 断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-HEUR-023-N01 | `test_heur_023_normal_golden` | JSONL `case=normal` | 人类失误率、regret上界与思考时间分布；断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作 |
| T-HEUR-023-B01 | `test_heur_023_boundary_table` | JSONL `case=boundary` 参数化 | 单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段；不越过批准输出范围 |
| T-HEUR-023-I01 | `test_heur_023_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退；断言稳定错误码和失败原子性 |
| T-HEUR-023-P01 | `test_heur_023_properties` | 固定seed生成器；seed写入报告 | 非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI |
| T-HEUR-023-R01 | `test_heur_023_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-HEUR-023-X01 | `test_heur_023_integration_contract` | 生产入口fixture | 仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_heur_023.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`HEUR-023-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

