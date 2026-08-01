# MODEL 单元可执行测试规格

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 覆盖 | MODEL等，共5单元 |
| 单元规格 | Approved |
| 测试实现/验收 | Not Implemented / Not Evaluated |

本文件规定测试代码、向量、断言和证据合同；详细业务定义仍只来自已批准单元规格。本文件存在不表示测试文件、fixture或行为已实现。

## MODEL-001 逐对手归一化方向/牌型假设

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [MODEL-001](../03-unit-specs/probabilistic_model_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_model_001.py` |
| 向量文件 | `tests/spec_v3/vectors/model_001.jsonl` |
| pytest标记 | `model,calibration,leakage,model` |
| 主要输入 | public evidence + prior |
| 主要输出 | posterior hypotheses |
| 本卡焦点 | 清缺概率、主体花色和牌型三任务校准 |
| oracle | 断言输出schema、概率范围/归一化、校准指标、不确定性、版本和规则基线回退 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-MODEL-001-N01 | `test_model_001_normal_golden` | JSONL `case=normal` | 清缺概率、主体花色和牌型三任务校准；断言输出schema、概率范围/归一化、校准指标、不确定性、版本和规则基线回退 |
| T-MODEL-001-B01 | `test_model_001_boundary_table` | JSONL `case=boundary` 参数化 | 无历史、最少样本、全mask、OOD、概率0/1、批大小1及在线时限边界；不越过批准输出范围 |
| T-MODEL-001-I01 | `test_model_001_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏手牌/墙序/future truth投毒、模型hash错、NaN或非法概率必须拒绝并回退；断言稳定错误码和失败原子性 |
| T-MODEL-001-P01 | `test_model_001_properties` | 固定seed生成器；seed写入报告 | Brier/log loss/ECE及卡内阈值使用冻结切分和95% CI；不能只报告准确率 |
| T-MODEL-001-R01 | `test_model_001_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-MODEL-001-X01 | `test_model_001_integration_contract` | 生产入口fixture | 线上加载器只接收白名单特征；restricted label truth与policy输入物理隔离；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_model_001.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`MODEL-001-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## MODEL-002 逐对手听牌/等待/损失风险模型

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [MODEL-002](../03-unit-specs/probabilistic_model_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_model_002.py` |
| 向量文件 | `tests/spec_v3/vectors/model_002.jsonl` |
| pytest标记 | `model,calibration,leakage,model` |
| 主要输入 | public evidence + hypotheses |
| 主要输出 | risk distribution |
| 本卡焦点 | 听牌、逐牌等待及综合点炮风险校准 |
| oracle | 断言输出schema、概率范围/归一化、校准指标、不确定性、版本和规则基线回退 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-MODEL-002-N01 | `test_model_002_normal_golden` | JSONL `case=normal` | 听牌、逐牌等待及综合点炮风险校准；断言输出schema、概率范围/归一化、校准指标、不确定性、版本和规则基线回退 |
| T-MODEL-002-B01 | `test_model_002_boundary_table` | JSONL `case=boundary` 参数化 | 无历史、最少样本、全mask、OOD、概率0/1、批大小1及在线时限边界；不越过批准输出范围 |
| T-MODEL-002-I01 | `test_model_002_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏手牌/墙序/future truth投毒、模型hash错、NaN或非法概率必须拒绝并回退；断言稳定错误码和失败原子性 |
| T-MODEL-002-P01 | `test_model_002_properties` | 固定seed生成器；seed写入报告 | Brier/log loss/ECE及卡内阈值使用冻结切分和95% CI；不能只报告准确率 |
| T-MODEL-002-R01 | `test_model_002_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-MODEL-002-X01 | `test_model_002_integration_contract` | 生产入口fixture | 线上加载器只接收白名单特征；restricted label truth与policy输入物理隔离；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_model_002.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`MODEL-002-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## MODEL-003 仅公开信息的跨局对手画像学习

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [MODEL-003](../03-unit-specs/probabilistic_model_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_model_003.py` |
| 向量文件 | `tests/spec_v3/vectors/model_003.jsonl` |
| pytest标记 | `model,calibration,leakage,model` |
| 主要输入 | match history + bounded state |
| 主要输出 | next profile |
| 本卡焦点 | 跨局风格更新、最少样本与跨玩家隔离 |
| oracle | 断言输出schema、概率范围/归一化、校准指标、不确定性、版本和规则基线回退 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-MODEL-003-N01 | `test_model_003_normal_golden` | JSONL `case=normal` | 跨局风格更新、最少样本与跨玩家隔离；断言输出schema、概率范围/归一化、校准指标、不确定性、版本和规则基线回退 |
| T-MODEL-003-B01 | `test_model_003_boundary_table` | JSONL `case=boundary` 参数化 | 无历史、最少样本、全mask、OOD、概率0/1、批大小1及在线时限边界；不越过批准输出范围 |
| T-MODEL-003-I01 | `test_model_003_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏手牌/墙序/future truth投毒、模型hash错、NaN或非法概率必须拒绝并回退；断言稳定错误码和失败原子性 |
| T-MODEL-003-P01 | `test_model_003_properties` | 固定seed生成器；seed写入报告 | Brier/log loss/ECE及卡内阈值使用冻结切分和95% CI；不能只报告准确率 |
| T-MODEL-003-R01 | `test_model_003_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-MODEL-003-X01 | `test_model_003_integration_contract` | 生产入口fixture | 线上加载器只接收白名单特征；restricted label truth与policy输入物理隔离；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_model_003.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`MODEL-003-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## MODEL-004 可训练策略输入输出契约

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [MODEL-004](../03-unit-specs/probabilistic_model_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_model_004.py` |
| 向量文件 | `tests/spec_v3/vectors/model_004.jsonl` |
| pytest标记 | `model,calibration,leakage,model` |
| 主要输入 | observation + mask + parameters |
| 主要输出 | action distribution/value |
| 本卡焦点 | legal-mask后候选动作概率分布与真人拟合 |
| oracle | 断言输出schema、概率范围/归一化、校准指标、不确定性、版本和规则基线回退 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-MODEL-004-N01 | `test_model_004_normal_golden` | JSONL `case=normal` | legal-mask后候选动作概率分布与真人拟合；断言输出schema、概率范围/归一化、校准指标、不确定性、版本和规则基线回退 |
| T-MODEL-004-B01 | `test_model_004_boundary_table` | JSONL `case=boundary` 参数化 | 无历史、最少样本、全mask、OOD、概率0/1、批大小1及在线时限边界；不越过批准输出范围 |
| T-MODEL-004-I01 | `test_model_004_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏手牌/墙序/future truth投毒、模型hash错、NaN或非法概率必须拒绝并回退；断言稳定错误码和失败原子性 |
| T-MODEL-004-P01 | `test_model_004_properties` | 固定seed生成器；seed写入报告 | Brier/log loss/ECE及卡内阈值使用冻结切分和95% CI；不能只报告准确率 |
| T-MODEL-004-R01 | `test_model_004_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-MODEL-004-X01 | `test_model_004_integration_contract` | 生产入口fixture | 线上加载器只接收白名单特征；restricted label truth与policy输入物理隔离；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_model_004.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`MODEL-004-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

## MODEL-005 训练模型产物版本、冻结和评估生命周期

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [MODEL-005](../03-unit-specs/probabilistic_model_specs.md)对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_model_005.py` |
| 向量文件 | `tests/spec_v3/vectors/model_005.jsonl` |
| pytest标记 | `model,calibration,leakage,model` |
| 主要输入 | training run + data/config hashes |
| 主要输出 | frozen model card/artifact |
| 本卡焦点 | 模型版本、artifact hash、兼容门禁和回退 |
| oracle | 断言输出schema、概率范围/归一化、校准指标、不确定性、版本和规则基线回退 |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言E3；P0/跨模块路径E4；外部效果声明按适用项E5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-MODEL-005-N01 | `test_model_005_normal_golden` | JSONL `case=normal` | 模型版本、artifact hash、兼容门禁和回退；断言输出schema、概率范围/归一化、校准指标、不确定性、版本和规则基线回退 |
| T-MODEL-005-B01 | `test_model_005_boundary_table` | JSONL `case=boundary` 参数化 | 无历史、最少样本、全mask、OOD、概率0/1、批大小1及在线时限边界；不越过批准输出范围 |
| T-MODEL-005-I01 | `test_model_005_invalid_rejected` | JSONL `case=invalid` 参数化 | 隐藏手牌/墙序/future truth投毒、模型hash错、NaN或非法概率必须拒绝并回退；断言稳定错误码和失败原子性 |
| T-MODEL-005-P01 | `test_model_005_properties` | 固定seed生成器；seed写入报告 | Brier/log loss/ECE及卡内阈值使用冻结切分和95% CI；不能只报告准确率 |
| T-MODEL-005-R01 | `test_model_005_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-MODEL-005-X01 | `test_model_005_integration_contract` | 生产入口fixture | 线上加载器只接收白名单特征；restricted label truth与policy输入物理隔离；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_model_005.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`MODEL-005-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

