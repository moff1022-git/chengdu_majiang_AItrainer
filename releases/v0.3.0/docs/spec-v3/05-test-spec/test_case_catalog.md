# Spec v3 测试用例目录

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 单元覆盖 | 96/96 |
| 用例实现/证据 | Not Implemented / Not Evaluated |

本目录只收录覆盖矩阵中适用的测试卡。业务expected以Approved单元规格为唯一来源；本目录细化前置、输入、seed、操作、输出、状态、日志、失败和自动化位置。

## TC-RULE-001-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-001-UT-01` |
| 对应单元ID | `RULE-001` — 规则、参数、不变量与合法性裁决优先级 |
| 父测试合同 | `T-RULE-001-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ruleset/config/state`；向量引用`tests/spec_v3/vectors/rule_001.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x50b427593ed37416`；通过ALGO-011 `property_test/RULE-001/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_001_ut`对应路径 |
| 预期输出 | 返回批准schema的`authoritative legal set or explicit rejection`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_001.py::test_rule_001_ut` |

## TC-RULE-001-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-001-BD-01` |
| 对应单元ID | `RULE-001` — 规则、参数、不变量与合法性裁决优先级 |
| 父测试合同 | `T-RULE-001-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ruleset/config/state`；向量引用`tests/spec_v3/vectors/rule_001.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5e1f8275523432bf`；通过ALGO-011 `property_test/RULE-001/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_001_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`authoritative legal set or explicit rejection`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_001.py::test_rule_001_bd` |

## TC-RULE-001-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-001-PT-01` |
| 对应单元ID | `RULE-001` — 规则、参数、不变量与合法性裁决优先级 |
| 父测试合同 | `T-RULE-001-N01`、`T-RULE-001-B01`、`T-RULE-001-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ruleset/config/state`；向量引用`tests/spec_v3/vectors/rule_001.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf367d24f3688d6d2`；通过ALGO-011 `property_test/RULE-001/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_001_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_001.py::test_rule_001_pt` |

## TC-RULE-001-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-001-PB-01` |
| 对应单元ID | `RULE-001` — 规则、参数、不变量与合法性裁决优先级 |
| 父测试合同 | `T-RULE-001-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ruleset/config/state`；向量引用`tests/spec_v3/vectors/rule_001.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbcad2311bbfcb3f5`；通过ALGO-011 `property_test/RULE-001/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_001.py::test_rule_001_pb` |

## TC-RULE-001-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-001-SM-01` |
| 对应单元ID | `RULE-001` — 规则、参数、不变量与合法性裁决优先级 |
| 父测试合同 | `T-RULE-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `ruleset/config/state`；向量引用`tests/spec_v3/vectors/rule_001.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1c38a4377e317046`；通过ALGO-011 `property_test/RULE-001/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_001_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_001.py::test_rule_001_sm` |

## TC-RULE-001-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-001-IT-01` |
| 对应单元ID | `RULE-001` — 规则、参数、不变量与合法性裁决优先级 |
| 父测试合同 | `T-RULE-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `ruleset/config/state`；向量引用`tests/spec_v3/vectors/rule_001.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xad1c2f3f3315e451`；通过ALGO-011 `property_test/RULE-001/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_001_it`对应路径 |
| 预期输出 | 通过生产入口得到`authoritative legal set or explicit rejection`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_001.py::test_rule_001_it` |

## TC-RULE-001-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-001-RR-01` |
| 对应单元ID | `RULE-001` — 规则、参数、不变量与合法性裁决优先级 |
| 父测试合同 | `T-RULE-001-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ruleset/config/state`；向量引用`tests/spec_v3/vectors/rule_001.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2eb6712f4d16e1bf`；通过ALGO-011 `property_test/RULE-001/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_001.py::test_rule_001_rr` |

## TC-RULE-001-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-001-PF-01` |
| 对应单元ID | `RULE-001` — 规则、参数、不变量与合法性裁决优先级 |
| 父测试合同 | `T-RULE-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ruleset/config/state`；向量引用`tests/spec_v3/vectors/rule_001.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x028cd30171f9b6fb`；通过ALGO-011 `property_test/RULE-001/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_001.py::test_rule_001_pf` |

## TC-RULE-001-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-001-HL-01` |
| 对应单元ID | `RULE-001` — 规则、参数、不变量与合法性裁决优先级 |
| 父测试合同 | `T-RULE-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `ruleset/config/state`；向量引用`tests/spec_v3/vectors/rule_001.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xea111b31ebb88782`；通过ALGO-011 `property_test/RULE-001/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_001.py::test_rule_001_hl` |

## TC-RULE-002-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-002-UT-01` |
| 对应单元ID | `RULE-002` — 换三张同花色、方向与提交合法性 |
| 父测试合同 | `T-RULE-002-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `concealed physical tiles + direction`；向量引用`tests/spec_v3/vectors/rule_002.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xaca8d6ddbf355b92`；通过ALGO-011 `property_test/RULE-002/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_002_ut`对应路径 |
| 预期输出 | 返回批准schema的`accepted exchange or error`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_002.py::test_rule_002_ut` |

## TC-RULE-002-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-002-BD-01` |
| 对应单元ID | `RULE-002` — 换三张同花色、方向与提交合法性 |
| 父测试合同 | `T-RULE-002-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `concealed physical tiles + direction`；向量引用`tests/spec_v3/vectors/rule_002.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2f65744a821bf22a`；通过ALGO-011 `property_test/RULE-002/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_002_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`accepted exchange or error`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_002.py::test_rule_002_bd` |

## TC-RULE-002-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-002-PT-01` |
| 对应单元ID | `RULE-002` — 换三张同花色、方向与提交合法性 |
| 父测试合同 | `T-RULE-002-N01`、`T-RULE-002-B01`、`T-RULE-002-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `concealed physical tiles + direction`；向量引用`tests/spec_v3/vectors/rule_002.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x23ec789c6c335ce8`；通过ALGO-011 `property_test/RULE-002/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_002_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_002.py::test_rule_002_pt` |

## TC-RULE-002-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-002-PB-01` |
| 对应单元ID | `RULE-002` — 换三张同花色、方向与提交合法性 |
| 父测试合同 | `T-RULE-002-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `concealed physical tiles + direction`；向量引用`tests/spec_v3/vectors/rule_002.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7b9b526766afb48c`；通过ALGO-011 `property_test/RULE-002/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_002.py::test_rule_002_pb` |

## TC-RULE-002-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-002-SM-01` |
| 对应单元ID | `RULE-002` — 换三张同花色、方向与提交合法性 |
| 父测试合同 | `T-RULE-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `concealed physical tiles + direction`；向量引用`tests/spec_v3/vectors/rule_002.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc9505c3cb136a09a`；通过ALGO-011 `property_test/RULE-002/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_002_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_002.py::test_rule_002_sm` |

## TC-RULE-002-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-002-IT-01` |
| 对应单元ID | `RULE-002` — 换三张同花色、方向与提交合法性 |
| 父测试合同 | `T-RULE-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `concealed physical tiles + direction`；向量引用`tests/spec_v3/vectors/rule_002.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe28c90b111c3d1ab`；通过ALGO-011 `property_test/RULE-002/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_002_it`对应路径 |
| 预期输出 | 通过生产入口得到`accepted exchange or error`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_002.py::test_rule_002_it` |

## TC-RULE-002-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-002-RR-01` |
| 对应单元ID | `RULE-002` — 换三张同花色、方向与提交合法性 |
| 父测试合同 | `T-RULE-002-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `concealed physical tiles + direction`；向量引用`tests/spec_v3/vectors/rule_002.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf31837495e1dcf89`；通过ALGO-011 `property_test/RULE-002/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_002.py::test_rule_002_rr` |

## TC-RULE-002-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-002-PF-01` |
| 对应单元ID | `RULE-002` — 换三张同花色、方向与提交合法性 |
| 父测试合同 | `T-RULE-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `concealed physical tiles + direction`；向量引用`tests/spec_v3/vectors/rule_002.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x97cb4a7d7633a5ea`；通过ALGO-011 `property_test/RULE-002/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_002.py::test_rule_002_pf` |

## TC-RULE-002-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-002-HL-01` |
| 对应单元ID | `RULE-002` — 换三张同花色、方向与提交合法性 |
| 父测试合同 | `T-RULE-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `concealed physical tiles + direction`；向量引用`tests/spec_v3/vectors/rule_002.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xeca794741492df57`；通过ALGO-011 `property_test/RULE-002/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_002.py::test_rule_002_hl` |

## TC-RULE-003-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-003-UT-01` |
| 对应单元ID | `RULE-003` — 定缺未清时的强制出牌约束 |
| 父测试合同 | `T-RULE-003-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand + dingque`；向量引用`tests/spec_v3/vectors/rule_003.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0d601c6134800066`；通过ALGO-011 `property_test/RULE-003/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_003_ut`对应路径 |
| 预期输出 | 返回批准schema的`legal discards`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_003.py::test_rule_003_ut` |

## TC-RULE-003-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-003-BD-01` |
| 对应单元ID | `RULE-003` — 定缺未清时的强制出牌约束 |
| 父测试合同 | `T-RULE-003-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand + dingque`；向量引用`tests/spec_v3/vectors/rule_003.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x94e5a6c07ce0f2a2`；通过ALGO-011 `property_test/RULE-003/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_003_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`legal discards`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_003.py::test_rule_003_bd` |

## TC-RULE-003-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-003-PT-01` |
| 对应单元ID | `RULE-003` — 定缺未清时的强制出牌约束 |
| 父测试合同 | `T-RULE-003-N01`、`T-RULE-003-B01`、`T-RULE-003-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand + dingque`；向量引用`tests/spec_v3/vectors/rule_003.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x856b0345a4654373`；通过ALGO-011 `property_test/RULE-003/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_003_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_003.py::test_rule_003_pt` |

## TC-RULE-003-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-003-PB-01` |
| 对应单元ID | `RULE-003` — 定缺未清时的强制出牌约束 |
| 父测试合同 | `T-RULE-003-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand + dingque`；向量引用`tests/spec_v3/vectors/rule_003.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xaef8553f4657d2dd`；通过ALGO-011 `property_test/RULE-003/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_003.py::test_rule_003_pb` |

## TC-RULE-003-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-003-SM-01` |
| 对应单元ID | `RULE-003` — 定缺未清时的强制出牌约束 |
| 父测试合同 | `T-RULE-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `hand + dingque`；向量引用`tests/spec_v3/vectors/rule_003.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd7373363d52f3a25`；通过ALGO-011 `property_test/RULE-003/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_003_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_003.py::test_rule_003_sm` |

## TC-RULE-003-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-003-IT-01` |
| 对应单元ID | `RULE-003` — 定缺未清时的强制出牌约束 |
| 父测试合同 | `T-RULE-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `hand + dingque`；向量引用`tests/spec_v3/vectors/rule_003.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6305beb06c091156`；通过ALGO-011 `property_test/RULE-003/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_003_it`对应路径 |
| 预期输出 | 通过生产入口得到`legal discards`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_003.py::test_rule_003_it` |

## TC-RULE-003-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-003-RR-01` |
| 对应单元ID | `RULE-003` — 定缺未清时的强制出牌约束 |
| 父测试合同 | `T-RULE-003-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand + dingque`；向量引用`tests/spec_v3/vectors/rule_003.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8394fe76723bbd08`；通过ALGO-011 `property_test/RULE-003/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_003.py::test_rule_003_rr` |

## TC-RULE-003-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-003-PF-01` |
| 对应单元ID | `RULE-003` — 定缺未清时的强制出牌约束 |
| 父测试合同 | `T-RULE-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand + dingque`；向量引用`tests/spec_v3/vectors/rule_003.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9a65d258e56eec2b`；通过ALGO-011 `property_test/RULE-003/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_003.py::test_rule_003_pf` |

## TC-RULE-003-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-003-HL-01` |
| 对应单元ID | `RULE-003` — 定缺未清时的强制出牌约束 |
| 父测试合同 | `T-RULE-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `hand + dingque`；向量引用`tests/spec_v3/vectors/rule_003.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x42078c8ed4830bac`；通过ALGO-011 `property_test/RULE-003/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_003.py::test_rule_003_hl` |

## TC-RULE-004-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-004-UT-01` |
| 对应单元ID | `RULE-004` — 定缺、死叫与胡牌资格约束 |
| 父测试合同 | `T-RULE-004-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand + dingque + waits`；向量引用`tests/spec_v3/vectors/rule_004.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xccc07c7e41b56c4e`；通过ALGO-011 `property_test/RULE-004/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_004_ut`对应路径 |
| 预期输出 | 返回批准schema的`hu eligibility`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_004.py::test_rule_004_ut` |

## TC-RULE-004-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-004-BD-01` |
| 对应单元ID | `RULE-004` — 定缺、死叫与胡牌资格约束 |
| 父测试合同 | `T-RULE-004-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand + dingque + waits`；向量引用`tests/spec_v3/vectors/rule_004.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x68378acd798dd04d`；通过ALGO-011 `property_test/RULE-004/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_004_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`hu eligibility`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_004.py::test_rule_004_bd` |

## TC-RULE-004-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-004-PT-01` |
| 对应单元ID | `RULE-004` — 定缺、死叫与胡牌资格约束 |
| 父测试合同 | `T-RULE-004-N01`、`T-RULE-004-B01`、`T-RULE-004-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand + dingque + waits`；向量引用`tests/spec_v3/vectors/rule_004.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7261989cf3db4f39`；通过ALGO-011 `property_test/RULE-004/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_004_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_004.py::test_rule_004_pt` |

## TC-RULE-004-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-004-PB-01` |
| 对应单元ID | `RULE-004` — 定缺、死叫与胡牌资格约束 |
| 父测试合同 | `T-RULE-004-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand + dingque + waits`；向量引用`tests/spec_v3/vectors/rule_004.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x97dac7ec854fb05e`；通过ALGO-011 `property_test/RULE-004/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_004.py::test_rule_004_pb` |

## TC-RULE-004-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-004-SM-01` |
| 对应单元ID | `RULE-004` — 定缺、死叫与胡牌资格约束 |
| 父测试合同 | `T-RULE-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `hand + dingque + waits`；向量引用`tests/spec_v3/vectors/rule_004.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4236ca0a2b527350`；通过ALGO-011 `property_test/RULE-004/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_004_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_004.py::test_rule_004_sm` |

## TC-RULE-004-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-004-IT-01` |
| 对应单元ID | `RULE-004` — 定缺、死叫与胡牌资格约束 |
| 父测试合同 | `T-RULE-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `hand + dingque + waits`；向量引用`tests/spec_v3/vectors/rule_004.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5baa6cefa0162da1`；通过ALGO-011 `property_test/RULE-004/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_004_it`对应路径 |
| 预期输出 | 通过生产入口得到`hu eligibility`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_004.py::test_rule_004_it` |

## TC-RULE-004-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-004-RR-01` |
| 对应单元ID | `RULE-004` — 定缺、死叫与胡牌资格约束 |
| 父测试合同 | `T-RULE-004-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand + dingque + waits`；向量引用`tests/spec_v3/vectors/rule_004.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xefbaacdbcb8bcec2`；通过ALGO-011 `property_test/RULE-004/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_004.py::test_rule_004_rr` |

## TC-RULE-004-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-004-PF-01` |
| 对应单元ID | `RULE-004` — 定缺、死叫与胡牌资格约束 |
| 父测试合同 | `T-RULE-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand + dingque + waits`；向量引用`tests/spec_v3/vectors/rule_004.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xba7f34d2dfd6b21c`；通过ALGO-011 `property_test/RULE-004/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_004.py::test_rule_004_pf` |

## TC-RULE-004-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-004-HL-01` |
| 对应单元ID | `RULE-004` — 定缺、死叫与胡牌资格约束 |
| 父测试合同 | `T-RULE-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `hand + dingque + waits`；向量引用`tests/spec_v3/vectors/rule_004.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x16981aea85c0d505`；通过ALGO-011 `property_test/RULE-004/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_004.py::test_rule_004_hl` |

## TC-RULE-005-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-005-UT-01` |
| 对应单元ID | `RULE-005` — 座位、庄家与活动顺序 |
| 父测试合同 | `T-RULE-005-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `seats + dealer + active set + actor`；向量引用`tests/spec_v3/vectors/rule_005.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9d7de55ffe8ce2cd`；通过ALGO-011 `property_test/RULE-005/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_005_ut`对应路径 |
| 预期输出 | 返回批准schema的`next actor`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_005.py::test_rule_005_ut` |

## TC-RULE-005-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-005-BD-01` |
| 对应单元ID | `RULE-005` — 座位、庄家与活动顺序 |
| 父测试合同 | `T-RULE-005-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `seats + dealer + active set + actor`；向量引用`tests/spec_v3/vectors/rule_005.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x12b8a66d1b419810`；通过ALGO-011 `property_test/RULE-005/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_005_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`next actor`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_005.py::test_rule_005_bd` |

## TC-RULE-005-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-005-PT-01` |
| 对应单元ID | `RULE-005` — 座位、庄家与活动顺序 |
| 父测试合同 | `T-RULE-005-N01`、`T-RULE-005-B01`、`T-RULE-005-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `seats + dealer + active set + actor`；向量引用`tests/spec_v3/vectors/rule_005.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9720ff2111750bef`；通过ALGO-011 `property_test/RULE-005/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_005_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_005.py::test_rule_005_pt` |

## TC-RULE-005-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-005-PB-01` |
| 对应单元ID | `RULE-005` — 座位、庄家与活动顺序 |
| 父测试合同 | `T-RULE-005-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `seats + dealer + active set + actor`；向量引用`tests/spec_v3/vectors/rule_005.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x247c90278495887c`；通过ALGO-011 `property_test/RULE-005/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_005.py::test_rule_005_pb` |

## TC-RULE-005-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-005-SM-01` |
| 对应单元ID | `RULE-005` — 座位、庄家与活动顺序 |
| 父测试合同 | `T-RULE-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `seats + dealer + active set + actor`；向量引用`tests/spec_v3/vectors/rule_005.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x50bb13d7ae18a95c`；通过ALGO-011 `property_test/RULE-005/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_005_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_005.py::test_rule_005_sm` |

## TC-RULE-005-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-005-IT-01` |
| 对应单元ID | `RULE-005` — 座位、庄家与活动顺序 |
| 父测试合同 | `T-RULE-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `seats + dealer + active set + actor`；向量引用`tests/spec_v3/vectors/rule_005.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbff24ffe13baa99c`；通过ALGO-011 `property_test/RULE-005/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_005_it`对应路径 |
| 预期输出 | 通过生产入口得到`next actor`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_005.py::test_rule_005_it` |

## TC-RULE-005-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-005-RR-01` |
| 对应单元ID | `RULE-005` — 座位、庄家与活动顺序 |
| 父测试合同 | `T-RULE-005-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `seats + dealer + active set + actor`；向量引用`tests/spec_v3/vectors/rule_005.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdc8502cc720783b0`；通过ALGO-011 `property_test/RULE-005/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_005.py::test_rule_005_rr` |

## TC-RULE-005-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-005-PF-01` |
| 对应单元ID | `RULE-005` — 座位、庄家与活动顺序 |
| 父测试合同 | `T-RULE-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `seats + dealer + active set + actor`；向量引用`tests/spec_v3/vectors/rule_005.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xfa4b5ede9ba278c2`；通过ALGO-011 `property_test/RULE-005/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_005.py::test_rule_005_pf` |

## TC-RULE-005-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-005-HL-01` |
| 对应单元ID | `RULE-005` — 座位、庄家与活动顺序 |
| 父测试合同 | `T-RULE-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `seats + dealer + active set + actor`；向量引用`tests/spec_v3/vectors/rule_005.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x27a85d8ff5c8df48`；通过ALGO-011 `property_test/RULE-005/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_005.py::test_rule_005_hl` |

## TC-RULE-006-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-006-UT-01` |
| 对应单元ID | `RULE-006` — 摸牌、可选响应与出牌标准顺序 |
| 父测试合同 | `T-RULE-006-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + actor + wall`；向量引用`tests/spec_v3/vectors/rule_006.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xfe33de16b1c9f616`；通过ALGO-011 `property_test/RULE-006/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_006_ut`对应路径 |
| 预期输出 | 返回批准schema的`next phase/action request`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_006.py::test_rule_006_ut` |

## TC-RULE-006-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-006-BD-01` |
| 对应单元ID | `RULE-006` — 摸牌、可选响应与出牌标准顺序 |
| 父测试合同 | `T-RULE-006-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + actor + wall`；向量引用`tests/spec_v3/vectors/rule_006.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3817be76cc90bfee`；通过ALGO-011 `property_test/RULE-006/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_006_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`next phase/action request`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_006.py::test_rule_006_bd` |

## TC-RULE-006-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-006-PT-01` |
| 对应单元ID | `RULE-006` — 摸牌、可选响应与出牌标准顺序 |
| 父测试合同 | `T-RULE-006-N01`、`T-RULE-006-B01`、`T-RULE-006-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + actor + wall`；向量引用`tests/spec_v3/vectors/rule_006.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7ccc30cafa335e6a`；通过ALGO-011 `property_test/RULE-006/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_006_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_006.py::test_rule_006_pt` |

## TC-RULE-006-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-006-PB-01` |
| 对应单元ID | `RULE-006` — 摸牌、可选响应与出牌标准顺序 |
| 父测试合同 | `T-RULE-006-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + actor + wall`；向量引用`tests/spec_v3/vectors/rule_006.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf970715db985e542`；通过ALGO-011 `property_test/RULE-006/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_006.py::test_rule_006_pb` |

## TC-RULE-006-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-006-SM-01` |
| 对应单元ID | `RULE-006` — 摸牌、可选响应与出牌标准顺序 |
| 父测试合同 | `T-RULE-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `phase + actor + wall`；向量引用`tests/spec_v3/vectors/rule_006.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x226c3bba02dcd1b0`；通过ALGO-011 `property_test/RULE-006/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_006_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_006.py::test_rule_006_sm` |

## TC-RULE-006-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-006-IT-01` |
| 对应单元ID | `RULE-006` — 摸牌、可选响应与出牌标准顺序 |
| 父测试合同 | `T-RULE-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `phase + actor + wall`；向量引用`tests/spec_v3/vectors/rule_006.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe7550846e5fadc5b`；通过ALGO-011 `property_test/RULE-006/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_006_it`对应路径 |
| 预期输出 | 通过生产入口得到`next phase/action request`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_006.py::test_rule_006_it` |

## TC-RULE-006-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-006-RR-01` |
| 对应单元ID | `RULE-006` — 摸牌、可选响应与出牌标准顺序 |
| 父测试合同 | `T-RULE-006-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + actor + wall`；向量引用`tests/spec_v3/vectors/rule_006.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4b0f37e6254bb903`；通过ALGO-011 `property_test/RULE-006/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_006.py::test_rule_006_rr` |

## TC-RULE-006-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-006-PF-01` |
| 对应单元ID | `RULE-006` — 摸牌、可选响应与出牌标准顺序 |
| 父测试合同 | `T-RULE-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + actor + wall`；向量引用`tests/spec_v3/vectors/rule_006.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe2ae1928f60b9013`；通过ALGO-011 `property_test/RULE-006/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_006.py::test_rule_006_pf` |

## TC-RULE-006-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-006-HL-01` |
| 对应单元ID | `RULE-006` — 摸牌、可选响应与出牌标准顺序 |
| 父测试合同 | `T-RULE-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `phase + actor + wall`；向量引用`tests/spec_v3/vectors/rule_006.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd4d113fdef01ad24`；通过ALGO-011 `property_test/RULE-006/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_006.py::test_rule_006_hl` |

## TC-RULE-007-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-007-UT-01` |
| 对应单元ID | `RULE-007` — 碰牌资格、执行与后续出牌 |
| 父测试合同 | `T-RULE-007-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `discard + responders + hands`；向量引用`tests/spec_v3/vectors/rule_007.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x08dd4290068e1171`；通过ALGO-011 `property_test/RULE-007/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_007_ut`对应路径 |
| 预期输出 | 返回批准schema的`meld/turn`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_007.py::test_rule_007_ut` |

## TC-RULE-007-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-007-BD-01` |
| 对应单元ID | `RULE-007` — 碰牌资格、执行与后续出牌 |
| 父测试合同 | `T-RULE-007-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `discard + responders + hands`；向量引用`tests/spec_v3/vectors/rule_007.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x21416084c562353f`；通过ALGO-011 `property_test/RULE-007/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_007_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`meld/turn`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_007.py::test_rule_007_bd` |

## TC-RULE-007-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-007-PT-01` |
| 对应单元ID | `RULE-007` — 碰牌资格、执行与后续出牌 |
| 父测试合同 | `T-RULE-007-N01`、`T-RULE-007-B01`、`T-RULE-007-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `discard + responders + hands`；向量引用`tests/spec_v3/vectors/rule_007.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8e3369df4f1eb740`；通过ALGO-011 `property_test/RULE-007/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_007_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_007.py::test_rule_007_pt` |

## TC-RULE-007-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-007-PB-01` |
| 对应单元ID | `RULE-007` — 碰牌资格、执行与后续出牌 |
| 父测试合同 | `T-RULE-007-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `discard + responders + hands`；向量引用`tests/spec_v3/vectors/rule_007.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd303597831f1ccf3`；通过ALGO-011 `property_test/RULE-007/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_007.py::test_rule_007_pb` |

## TC-RULE-007-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-007-SM-01` |
| 对应单元ID | `RULE-007` — 碰牌资格、执行与后续出牌 |
| 父测试合同 | `T-RULE-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `discard + responders + hands`；向量引用`tests/spec_v3/vectors/rule_007.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x019763d0a430510b`；通过ALGO-011 `property_test/RULE-007/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_007_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_007.py::test_rule_007_sm` |

## TC-RULE-007-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-007-IT-01` |
| 对应单元ID | `RULE-007` — 碰牌资格、执行与后续出牌 |
| 父测试合同 | `T-RULE-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `discard + responders + hands`；向量引用`tests/spec_v3/vectors/rule_007.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0c5d949fc6c195e9`；通过ALGO-011 `property_test/RULE-007/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_007_it`对应路径 |
| 预期输出 | 通过生产入口得到`meld/turn`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_007.py::test_rule_007_it` |

## TC-RULE-007-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-007-RR-01` |
| 对应单元ID | `RULE-007` — 碰牌资格、执行与后续出牌 |
| 父测试合同 | `T-RULE-007-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `discard + responders + hands`；向量引用`tests/spec_v3/vectors/rule_007.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2422e7428ac9da6d`；通过ALGO-011 `property_test/RULE-007/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_007.py::test_rule_007_rr` |

## TC-RULE-007-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-007-PF-01` |
| 对应单元ID | `RULE-007` — 碰牌资格、执行与后续出牌 |
| 父测试合同 | `T-RULE-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `discard + responders + hands`；向量引用`tests/spec_v3/vectors/rule_007.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd4cae3ffc8ca7113`；通过ALGO-011 `property_test/RULE-007/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_007.py::test_rule_007_pf` |

## TC-RULE-007-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-007-HL-01` |
| 对应单元ID | `RULE-007` — 碰牌资格、执行与后续出牌 |
| 父测试合同 | `T-RULE-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `discard + responders + hands`；向量引用`tests/spec_v3/vectors/rule_007.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xfc914b933bf8f28e`；通过ALGO-011 `property_test/RULE-007/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_007.py::test_rule_007_hl` |

## TC-RULE-008-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-008-UT-01` |
| 对应单元ID | `RULE-008` — 明杠、暗杠与补杠资格及执行 |
| 父测试合同 | `T-RULE-008-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand/meld/discard`；向量引用`tests/spec_v3/vectors/rule_008.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6fdb8fad31ed8d9f`；通过ALGO-011 `property_test/RULE-008/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_008_ut`对应路径 |
| 预期输出 | 返回批准schema的`gang transition`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_008.py::test_rule_008_ut` |

## TC-RULE-008-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-008-BD-01` |
| 对应单元ID | `RULE-008` — 明杠、暗杠与补杠资格及执行 |
| 父测试合同 | `T-RULE-008-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand/meld/discard`；向量引用`tests/spec_v3/vectors/rule_008.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x71f1eabc75baccb0`；通过ALGO-011 `property_test/RULE-008/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_008_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`gang transition`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_008.py::test_rule_008_bd` |

## TC-RULE-008-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-008-PT-01` |
| 对应单元ID | `RULE-008` — 明杠、暗杠与补杠资格及执行 |
| 父测试合同 | `T-RULE-008-N01`、`T-RULE-008-B01`、`T-RULE-008-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand/meld/discard`；向量引用`tests/spec_v3/vectors/rule_008.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x04d314138f23ff66`；通过ALGO-011 `property_test/RULE-008/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_008_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_008.py::test_rule_008_pt` |

## TC-RULE-008-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-008-PB-01` |
| 对应单元ID | `RULE-008` — 明杠、暗杠与补杠资格及执行 |
| 父测试合同 | `T-RULE-008-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand/meld/discard`；向量引用`tests/spec_v3/vectors/rule_008.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4d9c668466e7198a`；通过ALGO-011 `property_test/RULE-008/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_008.py::test_rule_008_pb` |

## TC-RULE-008-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-008-SM-01` |
| 对应单元ID | `RULE-008` — 明杠、暗杠与补杠资格及执行 |
| 父测试合同 | `T-RULE-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `hand/meld/discard`；向量引用`tests/spec_v3/vectors/rule_008.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7b539cdc3f4dfd6e`；通过ALGO-011 `property_test/RULE-008/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_008_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_008.py::test_rule_008_sm` |

## TC-RULE-008-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-008-IT-01` |
| 对应单元ID | `RULE-008` — 明杠、暗杠与补杠资格及执行 |
| 父测试合同 | `T-RULE-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `hand/meld/discard`；向量引用`tests/spec_v3/vectors/rule_008.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xce34985cbf81b59b`；通过ALGO-011 `property_test/RULE-008/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_008_it`对应路径 |
| 预期输出 | 通过生产入口得到`gang transition`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_008.py::test_rule_008_it` |

## TC-RULE-008-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-008-RR-01` |
| 对应单元ID | `RULE-008` — 明杠、暗杠与补杠资格及执行 |
| 父测试合同 | `T-RULE-008-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand/meld/discard`；向量引用`tests/spec_v3/vectors/rule_008.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1b8fc73daf9a6ea2`；通过ALGO-011 `property_test/RULE-008/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_008.py::test_rule_008_rr` |

## TC-RULE-008-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-008-PF-01` |
| 对应单元ID | `RULE-008` — 明杠、暗杠与补杠资格及执行 |
| 父测试合同 | `T-RULE-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hand/meld/discard`；向量引用`tests/spec_v3/vectors/rule_008.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xee4fa750e54401d4`；通过ALGO-011 `property_test/RULE-008/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_008.py::test_rule_008_pf` |

## TC-RULE-008-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-008-HL-01` |
| 对应单元ID | `RULE-008` — 明杠、暗杠与补杠资格及执行 |
| 父测试合同 | `T-RULE-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `hand/meld/discard`；向量引用`tests/spec_v3/vectors/rule_008.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x15a30e0c54434b27`；通过ALGO-011 `property_test/RULE-008/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_008.py::test_rule_008_hl` |

## TC-RULE-009-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-009-UT-01` |
| 对应单元ID | `RULE-009` — 补杠抢杠胡窗口与解析 |
| 父测试合同 | `T-RULE-009-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `bugang intent + responders`；向量引用`tests/spec_v3/vectors/rule_009.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xae54b8f198388a64`；通过ALGO-011 `property_test/RULE-009/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_009_ut`对应路径 |
| 预期输出 | 返回批准schema的`hu or gang`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_009.py::test_rule_009_ut` |

## TC-RULE-009-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-009-BD-01` |
| 对应单元ID | `RULE-009` — 补杠抢杠胡窗口与解析 |
| 父测试合同 | `T-RULE-009-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `bugang intent + responders`；向量引用`tests/spec_v3/vectors/rule_009.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd51a9074b6cc8af6`；通过ALGO-011 `property_test/RULE-009/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_009_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`hu or gang`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_009.py::test_rule_009_bd` |

## TC-RULE-009-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-009-PT-01` |
| 对应单元ID | `RULE-009` — 补杠抢杠胡窗口与解析 |
| 父测试合同 | `T-RULE-009-N01`、`T-RULE-009-B01`、`T-RULE-009-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `bugang intent + responders`；向量引用`tests/spec_v3/vectors/rule_009.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6f99cb29bfb79b7f`；通过ALGO-011 `property_test/RULE-009/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_009_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_009.py::test_rule_009_pt` |

## TC-RULE-009-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-009-PB-01` |
| 对应单元ID | `RULE-009` — 补杠抢杠胡窗口与解析 |
| 父测试合同 | `T-RULE-009-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `bugang intent + responders`；向量引用`tests/spec_v3/vectors/rule_009.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x77efe4554877356f`；通过ALGO-011 `property_test/RULE-009/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_009.py::test_rule_009_pb` |

## TC-RULE-009-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-009-SM-01` |
| 对应单元ID | `RULE-009` — 补杠抢杠胡窗口与解析 |
| 父测试合同 | `T-RULE-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `bugang intent + responders`；向量引用`tests/spec_v3/vectors/rule_009.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf231e61dca11b013`；通过ALGO-011 `property_test/RULE-009/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_009_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_009.py::test_rule_009_sm` |

## TC-RULE-009-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-009-IT-01` |
| 对应单元ID | `RULE-009` — 补杠抢杠胡窗口与解析 |
| 父测试合同 | `T-RULE-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `bugang intent + responders`；向量引用`tests/spec_v3/vectors/rule_009.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc5d76558a178e1bb`；通过ALGO-011 `property_test/RULE-009/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_009_it`对应路径 |
| 预期输出 | 通过生产入口得到`hu or gang`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_009.py::test_rule_009_it` |

## TC-RULE-009-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-009-RR-01` |
| 对应单元ID | `RULE-009` — 补杠抢杠胡窗口与解析 |
| 父测试合同 | `T-RULE-009-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `bugang intent + responders`；向量引用`tests/spec_v3/vectors/rule_009.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe690fab1c2ed183e`；通过ALGO-011 `property_test/RULE-009/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_009.py::test_rule_009_rr` |

## TC-RULE-009-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-009-PF-01` |
| 对应单元ID | `RULE-009` — 补杠抢杠胡窗口与解析 |
| 父测试合同 | `T-RULE-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `bugang intent + responders`；向量引用`tests/spec_v3/vectors/rule_009.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdd648485bcc4b276`；通过ALGO-011 `property_test/RULE-009/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_009.py::test_rule_009_pf` |

## TC-RULE-009-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-009-HL-01` |
| 对应单元ID | `RULE-009` — 补杠抢杠胡窗口与解析 |
| 父测试合同 | `T-RULE-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `bugang intent + responders`；向量引用`tests/spec_v3/vectors/rule_009.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9b5137d133a360fc`；通过ALGO-011 `property_test/RULE-009/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_009.py::test_rule_009_hl` |

## TC-RULE-010-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-010-UT-01` |
| 对应单元ID | `RULE-010` — 自摸、点炮与抢杠胡资格 |
| 父测试合同 | `T-RULE-010-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state + winning tile + source`；向量引用`tests/spec_v3/vectors/rule_010.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xed6fda55b45341ee`；通过ALGO-011 `property_test/RULE-010/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_010_ut`对应路径 |
| 预期输出 | 返回批准schema的`legal hu set`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_010.py::test_rule_010_ut` |

## TC-RULE-010-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-010-BD-01` |
| 对应单元ID | `RULE-010` — 自摸、点炮与抢杠胡资格 |
| 父测试合同 | `T-RULE-010-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state + winning tile + source`；向量引用`tests/spec_v3/vectors/rule_010.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2878f0346e499832`；通过ALGO-011 `property_test/RULE-010/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_010_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`legal hu set`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_010.py::test_rule_010_bd` |

## TC-RULE-010-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-010-PT-01` |
| 对应单元ID | `RULE-010` — 自摸、点炮与抢杠胡资格 |
| 父测试合同 | `T-RULE-010-N01`、`T-RULE-010-B01`、`T-RULE-010-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state + winning tile + source`；向量引用`tests/spec_v3/vectors/rule_010.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3ed80556bed74115`；通过ALGO-011 `property_test/RULE-010/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_010_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_010.py::test_rule_010_pt` |

## TC-RULE-010-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-010-PB-01` |
| 对应单元ID | `RULE-010` — 自摸、点炮与抢杠胡资格 |
| 父测试合同 | `T-RULE-010-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state + winning tile + source`；向量引用`tests/spec_v3/vectors/rule_010.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0bdf33dc8d5674ae`；通过ALGO-011 `property_test/RULE-010/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_010.py::test_rule_010_pb` |

## TC-RULE-010-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-010-SM-01` |
| 对应单元ID | `RULE-010` — 自摸、点炮与抢杠胡资格 |
| 父测试合同 | `T-RULE-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `state + winning tile + source`；向量引用`tests/spec_v3/vectors/rule_010.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7becf8f0d5cdc7fb`；通过ALGO-011 `property_test/RULE-010/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_010_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_010.py::test_rule_010_sm` |

## TC-RULE-010-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-010-IT-01` |
| 对应单元ID | `RULE-010` — 自摸、点炮与抢杠胡资格 |
| 父测试合同 | `T-RULE-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `state + winning tile + source`；向量引用`tests/spec_v3/vectors/rule_010.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xef897fadeb62a575`；通过ALGO-011 `property_test/RULE-010/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_010_it`对应路径 |
| 预期输出 | 通过生产入口得到`legal hu set`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_010.py::test_rule_010_it` |

## TC-RULE-010-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-010-RR-01` |
| 对应单元ID | `RULE-010` — 自摸、点炮与抢杠胡资格 |
| 父测试合同 | `T-RULE-010-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state + winning tile + source`；向量引用`tests/spec_v3/vectors/rule_010.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x01b470d28acd8692`；通过ALGO-011 `property_test/RULE-010/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_010.py::test_rule_010_rr` |

## TC-RULE-010-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-010-PF-01` |
| 对应单元ID | `RULE-010` — 自摸、点炮与抢杠胡资格 |
| 父测试合同 | `T-RULE-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state + winning tile + source`；向量引用`tests/spec_v3/vectors/rule_010.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x806bbf99a0543e22`；通过ALGO-011 `property_test/RULE-010/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_010.py::test_rule_010_pf` |

## TC-RULE-010-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-010-HL-01` |
| 对应单元ID | `RULE-010` — 自摸、点炮与抢杠胡资格 |
| 父测试合同 | `T-RULE-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `state + winning tile + source`；向量引用`tests/spec_v3/vectors/rule_010.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2d3561d40d818ac6`；通过ALGO-011 `property_test/RULE-010/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_010.py::test_rule_010_hl` |

## TC-RULE-011-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-011-UT-01` |
| 对应单元ID | `RULE-011` — 过胡设置、持续与恢复 |
| 父测试合同 | `T-RULE-011-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `declined hu + phase/events`；向量引用`tests/spec_v3/vectors/rule_011.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf3ee56c921d9a6ad`；通过ALGO-011 `property_test/RULE-011/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_011_ut`对应路径 |
| 预期输出 | 返回批准schema的`pass-hu state`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_011.py::test_rule_011_ut` |

## TC-RULE-011-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-011-BD-01` |
| 对应单元ID | `RULE-011` — 过胡设置、持续与恢复 |
| 父测试合同 | `T-RULE-011-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `declined hu + phase/events`；向量引用`tests/spec_v3/vectors/rule_011.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0e4b6c5f00f5b00e`；通过ALGO-011 `property_test/RULE-011/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_011_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`pass-hu state`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_011.py::test_rule_011_bd` |

## TC-RULE-011-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-011-PT-01` |
| 对应单元ID | `RULE-011` — 过胡设置、持续与恢复 |
| 父测试合同 | `T-RULE-011-N01`、`T-RULE-011-B01`、`T-RULE-011-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `declined hu + phase/events`；向量引用`tests/spec_v3/vectors/rule_011.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x254d99423b15120b`；通过ALGO-011 `property_test/RULE-011/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_011_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_011.py::test_rule_011_pt` |

## TC-RULE-011-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-011-PB-01` |
| 对应单元ID | `RULE-011` — 过胡设置、持续与恢复 |
| 父测试合同 | `T-RULE-011-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `declined hu + phase/events`；向量引用`tests/spec_v3/vectors/rule_011.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x437f7ecfa3b6ff16`；通过ALGO-011 `property_test/RULE-011/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_011.py::test_rule_011_pb` |

## TC-RULE-011-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-011-SM-01` |
| 对应单元ID | `RULE-011` — 过胡设置、持续与恢复 |
| 父测试合同 | `T-RULE-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `declined hu + phase/events`；向量引用`tests/spec_v3/vectors/rule_011.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xfe57769a7a115159`；通过ALGO-011 `property_test/RULE-011/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_011_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_011.py::test_rule_011_sm` |

## TC-RULE-011-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-011-IT-01` |
| 对应单元ID | `RULE-011` — 过胡设置、持续与恢复 |
| 父测试合同 | `T-RULE-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `declined hu + phase/events`；向量引用`tests/spec_v3/vectors/rule_011.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf907bf3e2ec4d549`；通过ALGO-011 `property_test/RULE-011/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_011_it`对应路径 |
| 预期输出 | 通过生产入口得到`pass-hu state`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_011.py::test_rule_011_it` |

## TC-RULE-011-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-011-RR-01` |
| 对应单元ID | `RULE-011` — 过胡设置、持续与恢复 |
| 父测试合同 | `T-RULE-011-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `declined hu + phase/events`；向量引用`tests/spec_v3/vectors/rule_011.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2ca67212f9880956`；通过ALGO-011 `property_test/RULE-011/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_011.py::test_rule_011_rr` |

## TC-RULE-011-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-011-PF-01` |
| 对应单元ID | `RULE-011` — 过胡设置、持续与恢复 |
| 父测试合同 | `T-RULE-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `declined hu + phase/events`；向量引用`tests/spec_v3/vectors/rule_011.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd545db7020054925`；通过ALGO-011 `property_test/RULE-011/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_011.py::test_rule_011_pf` |

## TC-RULE-011-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-011-HL-01` |
| 对应单元ID | `RULE-011` — 过胡设置、持续与恢复 |
| 父测试合同 | `T-RULE-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `declined hu + phase/events`；向量引用`tests/spec_v3/vectors/rule_011.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc436c4ba6ae94d38`；通过ALGO-011 `property_test/RULE-011/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_011.py::test_rule_011_hl` |

## TC-RULE-012-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-012-UT-01` |
| 对应单元ID | `RULE-012` — 强制胡与最后阶段必胡 |
| 父测试合同 | `T-RULE-012-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal hu + GP rule + wall state`；向量引用`tests/spec_v3/vectors/rule_012.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x82697cfdca96dbae`；通过ALGO-011 `property_test/RULE-012/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_012_ut`对应路径 |
| 预期输出 | 返回批准schema的`forced action`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_012.py::test_rule_012_ut` |

## TC-RULE-012-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-012-BD-01` |
| 对应单元ID | `RULE-012` — 强制胡与最后阶段必胡 |
| 父测试合同 | `T-RULE-012-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal hu + GP rule + wall state`；向量引用`tests/spec_v3/vectors/rule_012.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe43d4ef1c30d19e5`；通过ALGO-011 `property_test/RULE-012/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_012_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`forced action`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_012.py::test_rule_012_bd` |

## TC-RULE-012-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-012-PT-01` |
| 对应单元ID | `RULE-012` — 强制胡与最后阶段必胡 |
| 父测试合同 | `T-RULE-012-N01`、`T-RULE-012-B01`、`T-RULE-012-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal hu + GP rule + wall state`；向量引用`tests/spec_v3/vectors/rule_012.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x42908d85066e62f2`；通过ALGO-011 `property_test/RULE-012/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_012_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_012.py::test_rule_012_pt` |

## TC-RULE-012-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-012-PB-01` |
| 对应单元ID | `RULE-012` — 强制胡与最后阶段必胡 |
| 父测试合同 | `T-RULE-012-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal hu + GP rule + wall state`；向量引用`tests/spec_v3/vectors/rule_012.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcce9a0bc4cc53a93`；通过ALGO-011 `property_test/RULE-012/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_012.py::test_rule_012_pb` |

## TC-RULE-012-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-012-SM-01` |
| 对应单元ID | `RULE-012` — 强制胡与最后阶段必胡 |
| 父测试合同 | `T-RULE-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `legal hu + GP rule + wall state`；向量引用`tests/spec_v3/vectors/rule_012.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x154a0aacab34b68f`；通过ALGO-011 `property_test/RULE-012/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_012_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_012.py::test_rule_012_sm` |

## TC-RULE-012-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-012-IT-01` |
| 对应单元ID | `RULE-012` — 强制胡与最后阶段必胡 |
| 父测试合同 | `T-RULE-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `legal hu + GP rule + wall state`；向量引用`tests/spec_v3/vectors/rule_012.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xecf3443eb0c6ed79`；通过ALGO-011 `property_test/RULE-012/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_012_it`对应路径 |
| 预期输出 | 通过生产入口得到`forced action`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_012.py::test_rule_012_it` |

## TC-RULE-012-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-012-RR-01` |
| 对应单元ID | `RULE-012` — 强制胡与最后阶段必胡 |
| 父测试合同 | `T-RULE-012-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal hu + GP rule + wall state`；向量引用`tests/spec_v3/vectors/rule_012.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x733912af94ec9a36`；通过ALGO-011 `property_test/RULE-012/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_012.py::test_rule_012_rr` |

## TC-RULE-012-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-012-PF-01` |
| 对应单元ID | `RULE-012` — 强制胡与最后阶段必胡 |
| 父测试合同 | `T-RULE-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal hu + GP rule + wall state`；向量引用`tests/spec_v3/vectors/rule_012.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x76fca2bfab29a91f`；通过ALGO-011 `property_test/RULE-012/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_012.py::test_rule_012_pf` |

## TC-RULE-012-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-012-HL-01` |
| 对应单元ID | `RULE-012` — 强制胡与最后阶段必胡 |
| 父测试合同 | `T-RULE-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `legal hu + GP rule + wall state`；向量引用`tests/spec_v3/vectors/rule_012.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc1c75cc9a5bddc38`；通过ALGO-011 `property_test/RULE-012/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_012.py::test_rule_012_hl` |

## TC-RULE-013-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-013-UT-01` |
| 对应单元ID | `RULE-013` — 多人响应确定性优先级 |
| 父测试合同 | `T-RULE-013-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `response set + GP-008`；向量引用`tests/spec_v3/vectors/rule_013.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa36f615fe5dfa78b`；通过ALGO-011 `property_test/RULE-013/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_013_ut`对应路径 |
| 预期输出 | 返回批准schema的`resolved actions`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_013.py::test_rule_013_ut` |

## TC-RULE-013-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-013-BD-01` |
| 对应单元ID | `RULE-013` — 多人响应确定性优先级 |
| 父测试合同 | `T-RULE-013-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `response set + GP-008`；向量引用`tests/spec_v3/vectors/rule_013.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd2f74feb0dd25930`；通过ALGO-011 `property_test/RULE-013/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_013_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`resolved actions`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_013.py::test_rule_013_bd` |

## TC-RULE-013-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-013-PT-01` |
| 对应单元ID | `RULE-013` — 多人响应确定性优先级 |
| 父测试合同 | `T-RULE-013-N01`、`T-RULE-013-B01`、`T-RULE-013-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `response set + GP-008`；向量引用`tests/spec_v3/vectors/rule_013.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdc759315a690c17e`；通过ALGO-011 `property_test/RULE-013/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_013_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_013.py::test_rule_013_pt` |

## TC-RULE-013-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-013-PB-01` |
| 对应单元ID | `RULE-013` — 多人响应确定性优先级 |
| 父测试合同 | `T-RULE-013-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `response set + GP-008`；向量引用`tests/spec_v3/vectors/rule_013.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x230b7d4fe512dfa5`；通过ALGO-011 `property_test/RULE-013/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_013.py::test_rule_013_pb` |

## TC-RULE-013-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-013-SM-01` |
| 对应单元ID | `RULE-013` — 多人响应确定性优先级 |
| 父测试合同 | `T-RULE-013-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `response set + GP-008`；向量引用`tests/spec_v3/vectors/rule_013.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2318d3f5538d4a65`；通过ALGO-011 `property_test/RULE-013/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_013_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_013.py::test_rule_013_sm` |

## TC-RULE-013-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-013-IT-01` |
| 对应单元ID | `RULE-013` — 多人响应确定性优先级 |
| 父测试合同 | `T-RULE-013-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `response set + GP-008`；向量引用`tests/spec_v3/vectors/rule_013.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x43352aba91c3359b`；通过ALGO-011 `property_test/RULE-013/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_013_it`对应路径 |
| 预期输出 | 通过生产入口得到`resolved actions`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_013.py::test_rule_013_it` |

## TC-RULE-013-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-013-RR-01` |
| 对应单元ID | `RULE-013` — 多人响应确定性优先级 |
| 父测试合同 | `T-RULE-013-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `response set + GP-008`；向量引用`tests/spec_v3/vectors/rule_013.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf6fae46ba0c80f6e`；通过ALGO-011 `property_test/RULE-013/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_013.py::test_rule_013_rr` |

## TC-RULE-013-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-013-PF-01` |
| 对应单元ID | `RULE-013` — 多人响应确定性优先级 |
| 父测试合同 | `T-RULE-013-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `response set + GP-008`；向量引用`tests/spec_v3/vectors/rule_013.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x09f15763774aab92`；通过ALGO-011 `property_test/RULE-013/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_013.py::test_rule_013_pf` |

## TC-RULE-013-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-013-HL-01` |
| 对应单元ID | `RULE-013` — 多人响应确定性优先级 |
| 父测试合同 | `T-RULE-013-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `response set + GP-008`；向量引用`tests/spec_v3/vectors/rule_013.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5897efcf76bd867e`；通过ALGO-011 `property_test/RULE-013/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_013.py::test_rule_013_hl` |

## TC-RULE-014-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-014-UT-01` |
| 对应单元ID | `RULE-014` — 血战胡后退出、继续与终止 |
| 父测试合同 | `T-RULE-014-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hu result + active seats + wall`；向量引用`tests/spec_v3/vectors/rule_014.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x843e94a5f87cff80`；通过ALGO-011 `property_test/RULE-014/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_014_ut`对应路径 |
| 预期输出 | 返回批准schema的`active set/end`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_014.py::test_rule_014_ut` |

## TC-RULE-014-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-014-BD-01` |
| 对应单元ID | `RULE-014` — 血战胡后退出、继续与终止 |
| 父测试合同 | `T-RULE-014-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hu result + active seats + wall`；向量引用`tests/spec_v3/vectors/rule_014.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x637098c75cead7c5`；通过ALGO-011 `property_test/RULE-014/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_014_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`active set/end`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_014.py::test_rule_014_bd` |

## TC-RULE-014-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-014-PT-01` |
| 对应单元ID | `RULE-014` — 血战胡后退出、继续与终止 |
| 父测试合同 | `T-RULE-014-N01`、`T-RULE-014-B01`、`T-RULE-014-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hu result + active seats + wall`；向量引用`tests/spec_v3/vectors/rule_014.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbf08551dd5cd85a8`；通过ALGO-011 `property_test/RULE-014/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_014_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_014.py::test_rule_014_pt` |

## TC-RULE-014-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-014-PB-01` |
| 对应单元ID | `RULE-014` — 血战胡后退出、继续与终止 |
| 父测试合同 | `T-RULE-014-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hu result + active seats + wall`；向量引用`tests/spec_v3/vectors/rule_014.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa0ff3f50aab74e8b`；通过ALGO-011 `property_test/RULE-014/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_014.py::test_rule_014_pb` |

## TC-RULE-014-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-014-SM-01` |
| 对应单元ID | `RULE-014` — 血战胡后退出、继续与终止 |
| 父测试合同 | `T-RULE-014-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `hu result + active seats + wall`；向量引用`tests/spec_v3/vectors/rule_014.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x665b561a46b2695a`；通过ALGO-011 `property_test/RULE-014/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_014_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_014.py::test_rule_014_sm` |

## TC-RULE-014-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-014-IT-01` |
| 对应单元ID | `RULE-014` — 血战胡后退出、继续与终止 |
| 父测试合同 | `T-RULE-014-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `hu result + active seats + wall`；向量引用`tests/spec_v3/vectors/rule_014.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x581833717e981ea5`；通过ALGO-011 `property_test/RULE-014/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_014_it`对应路径 |
| 预期输出 | 通过生产入口得到`active set/end`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_014.py::test_rule_014_it` |

## TC-RULE-014-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-014-RR-01` |
| 对应单元ID | `RULE-014` — 血战胡后退出、继续与终止 |
| 父测试合同 | `T-RULE-014-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hu result + active seats + wall`；向量引用`tests/spec_v3/vectors/rule_014.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcaeb9d289919b5d4`；通过ALGO-011 `property_test/RULE-014/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_014.py::test_rule_014_rr` |

## TC-RULE-014-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-014-PF-01` |
| 对应单元ID | `RULE-014` — 血战胡后退出、继续与终止 |
| 父测试合同 | `T-RULE-014-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hu result + active seats + wall`；向量引用`tests/spec_v3/vectors/rule_014.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe29bca094aaeb912`；通过ALGO-011 `property_test/RULE-014/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_014.py::test_rule_014_pf` |

## TC-RULE-014-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-014-HL-01` |
| 对应单元ID | `RULE-014` — 血战胡后退出、继续与终止 |
| 父测试合同 | `T-RULE-014-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `hu result + active seats + wall`；向量引用`tests/spec_v3/vectors/rule_014.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8a3b8992122f7a41`；通过ALGO-011 `property_test/RULE-014/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_014.py::test_rule_014_hl` |

## TC-RULE-015-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-015-UT-01` |
| 对应单元ID | `RULE-015` — 启用番型、互斥/叠加与封顶规则 |
| 父测试合同 | `T-RULE-015-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ruleset + hand facts`；向量引用`tests/spec_v3/vectors/rule_015.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3d5537e655f41342`；通过ALGO-011 `property_test/RULE-015/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_015_ut`对应路径 |
| 预期输出 | 返回批准schema的`applicable fan policy`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_015.py::test_rule_015_ut` |

## TC-RULE-015-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-015-BD-01` |
| 对应单元ID | `RULE-015` — 启用番型、互斥/叠加与封顶规则 |
| 父测试合同 | `T-RULE-015-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ruleset + hand facts`；向量引用`tests/spec_v3/vectors/rule_015.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd1f3d887ab3faafd`；通过ALGO-011 `property_test/RULE-015/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_015_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`applicable fan policy`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_015.py::test_rule_015_bd` |

## TC-RULE-015-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-015-PT-01` |
| 对应单元ID | `RULE-015` — 启用番型、互斥/叠加与封顶规则 |
| 父测试合同 | `T-RULE-015-N01`、`T-RULE-015-B01`、`T-RULE-015-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ruleset + hand facts`；向量引用`tests/spec_v3/vectors/rule_015.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x70b552424d664b15`；通过ALGO-011 `property_test/RULE-015/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_015_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_015.py::test_rule_015_pt` |

## TC-RULE-015-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-015-PB-01` |
| 对应单元ID | `RULE-015` — 启用番型、互斥/叠加与封顶规则 |
| 父测试合同 | `T-RULE-015-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ruleset + hand facts`；向量引用`tests/spec_v3/vectors/rule_015.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe6fc2d94e801ce29`；通过ALGO-011 `property_test/RULE-015/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_015.py::test_rule_015_pb` |

## TC-RULE-015-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-015-SM-01` |
| 对应单元ID | `RULE-015` — 启用番型、互斥/叠加与封顶规则 |
| 父测试合同 | `T-RULE-015-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `ruleset + hand facts`；向量引用`tests/spec_v3/vectors/rule_015.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x317be60b07d9fc96`；通过ALGO-011 `property_test/RULE-015/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_015_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_015.py::test_rule_015_sm` |

## TC-RULE-015-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-015-IT-01` |
| 对应单元ID | `RULE-015` — 启用番型、互斥/叠加与封顶规则 |
| 父测试合同 | `T-RULE-015-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `ruleset + hand facts`；向量引用`tests/spec_v3/vectors/rule_015.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8a7f680330e2eb43`；通过ALGO-011 `property_test/RULE-015/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_015_it`对应路径 |
| 预期输出 | 通过生产入口得到`applicable fan policy`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_015.py::test_rule_015_it` |

## TC-RULE-015-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-015-RR-01` |
| 对应单元ID | `RULE-015` — 启用番型、互斥/叠加与封顶规则 |
| 父测试合同 | `T-RULE-015-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ruleset + hand facts`；向量引用`tests/spec_v3/vectors/rule_015.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb1268b21dc96a32e`；通过ALGO-011 `property_test/RULE-015/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_015.py::test_rule_015_rr` |

## TC-RULE-015-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-015-PF-01` |
| 对应单元ID | `RULE-015` — 启用番型、互斥/叠加与封顶规则 |
| 父测试合同 | `T-RULE-015-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ruleset + hand facts`；向量引用`tests/spec_v3/vectors/rule_015.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcdcdf69cf9381bab`；通过ALGO-011 `property_test/RULE-015/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_015.py::test_rule_015_pf` |

## TC-RULE-015-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-015-HL-01` |
| 对应单元ID | `RULE-015` — 启用番型、互斥/叠加与封顶规则 |
| 父测试合同 | `T-RULE-015-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `ruleset + hand facts`；向量引用`tests/spec_v3/vectors/rule_015.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x51dbc266cc3f5927`；通过ALGO-011 `property_test/RULE-015/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_015.py::test_rule_015_hl` |

## TC-RULE-016-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-016-UT-01` |
| 对应单元ID | `RULE-016` — 局中与终局公开信息范围 |
| 父测试合同 | `T-RULE-016-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + seat + event`；向量引用`tests/spec_v3/vectors/rule_016.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4c0912b142721f32`；通过ALGO-011 `property_test/RULE-016/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_016_ut`对应路径 |
| 预期输出 | 返回批准schema的`visible field set`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_016.py::test_rule_016_ut` |

## TC-RULE-016-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-016-BD-01` |
| 对应单元ID | `RULE-016` — 局中与终局公开信息范围 |
| 父测试合同 | `T-RULE-016-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + seat + event`；向量引用`tests/spec_v3/vectors/rule_016.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1a23f17dd17451f7`；通过ALGO-011 `property_test/RULE-016/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_016_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`visible field set`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_016.py::test_rule_016_bd` |

## TC-RULE-016-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-016-PT-01` |
| 对应单元ID | `RULE-016` — 局中与终局公开信息范围 |
| 父测试合同 | `T-RULE-016-N01`、`T-RULE-016-B01`、`T-RULE-016-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + seat + event`；向量引用`tests/spec_v3/vectors/rule_016.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdcc0adea54b1b5da`；通过ALGO-011 `property_test/RULE-016/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_016_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_016.py::test_rule_016_pt` |

## TC-RULE-016-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-016-PB-01` |
| 对应单元ID | `RULE-016` — 局中与终局公开信息范围 |
| 父测试合同 | `T-RULE-016-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + seat + event`；向量引用`tests/spec_v3/vectors/rule_016.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf088d00d3af6ff99`；通过ALGO-011 `property_test/RULE-016/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_016.py::test_rule_016_pb` |

## TC-RULE-016-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-016-SM-01` |
| 对应单元ID | `RULE-016` — 局中与终局公开信息范围 |
| 父测试合同 | `T-RULE-016-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `phase + seat + event`；向量引用`tests/spec_v3/vectors/rule_016.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd42524beed85e0b1`；通过ALGO-011 `property_test/RULE-016/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_016_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_016.py::test_rule_016_sm` |

## TC-RULE-016-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-016-IT-01` |
| 对应单元ID | `RULE-016` — 局中与终局公开信息范围 |
| 父测试合同 | `T-RULE-016-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `phase + seat + event`；向量引用`tests/spec_v3/vectors/rule_016.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbeff2252d5a79b55`；通过ALGO-011 `property_test/RULE-016/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_rule_016_it`对应路径 |
| 预期输出 | 通过生产入口得到`visible field set`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=RULE-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_016.py::test_rule_016_it` |

## TC-RULE-016-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-016-RR-01` |
| 对应单元ID | `RULE-016` — 局中与终局公开信息范围 |
| 父测试合同 | `T-RULE-016-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + seat + event`；向量引用`tests/spec_v3/vectors/rule_016.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x610964811ea4e0e6`；通过ALGO-011 `property_test/RULE-016/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=RULE-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_rule_016.py::test_rule_016_rr` |

## TC-RULE-016-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-016-PF-01` |
| 对应单元ID | `RULE-016` — 局中与终局公开信息范围 |
| 父测试合同 | `T-RULE-016-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + seat + event`；向量引用`tests/spec_v3/vectors/rule_016.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcddd270cf7487731`；通过ALGO-011 `property_test/RULE-016/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_rule_016.py::test_rule_016_pf` |

## TC-RULE-016-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-RULE-016-HL-01` |
| 对应单元ID | `RULE-016` — 局中与终局公开信息范围 |
| 父测试合同 | `T-RULE-016-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `phase + seat + event`；向量引用`tests/spec_v3/vectors/rule_016.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x638a43d274bb61ce`；通过ALGO-011 `property_test/RULE-016/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=RULE-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_rule_016.py::test_rule_016_hl` |

## TC-ALGO-001-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-001-UT-01` |
| 对应单元ID | `ALGO-001` — face/physical tile 编码、投影与所有权守恒 |
| 父测试合同 | `T-ALGO-001-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `physical regions`；向量引用`tests/spec_v3/vectors/algo_001.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x73169e5c8db22996`；通过ALGO-011 `property_test/ALGO-001/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_001_ut`对应路径 |
| 预期输出 | 匹配`GV-ALGO-001-N01`金标准；返回批准schema的`face views + conservation result`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_001.py::test_algo_001_ut` |

## TC-ALGO-001-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-001-BD-01` |
| 对应单元ID | `ALGO-001` — face/physical tile 编码、投影与所有权守恒 |
| 父测试合同 | `T-ALGO-001-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `physical regions`；向量引用`tests/spec_v3/vectors/algo_001.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa369a974c1f38bbe`；通过ALGO-011 `property_test/ALGO-001/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_001_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`face views + conservation result`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_001.py::test_algo_001_bd` |

## TC-ALGO-001-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-001-PT-01` |
| 对应单元ID | `ALGO-001` — face/physical tile 编码、投影与所有权守恒 |
| 父测试合同 | `T-ALGO-001-N01`、`T-ALGO-001-B01`、`T-ALGO-001-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `physical regions`；向量引用`tests/spec_v3/vectors/algo_001.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x44c4ce8d176e8162`；通过ALGO-011 `property_test/ALGO-001/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_001_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_001.py::test_algo_001_pt` |

## TC-ALGO-001-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-001-PB-01` |
| 对应单元ID | `ALGO-001` — face/physical tile 编码、投影与所有权守恒 |
| 父测试合同 | `T-ALGO-001-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `physical regions`；向量引用`tests/spec_v3/vectors/algo_001.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe7bee161dce0882e`；通过ALGO-011 `property_test/ALGO-001/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_001.py::test_algo_001_pb` |

## TC-ALGO-001-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-001-IT-01` |
| 对应单元ID | `ALGO-001` — face/physical tile 编码、投影与所有权守恒 |
| 父测试合同 | `T-ALGO-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `physical regions`；向量引用`tests/spec_v3/vectors/algo_001.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1a81ccb7f2c83b80`；通过ALGO-011 `property_test/ALGO-001/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_001_it`对应路径 |
| 预期输出 | 通过生产入口得到`face views + conservation result`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=ALGO-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_001.py::test_algo_001_it` |

## TC-ALGO-001-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-001-RR-01` |
| 对应单元ID | `ALGO-001` — face/physical tile 编码、投影与所有权守恒 |
| 父测试合同 | `T-ALGO-001-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `physical regions`；向量引用`tests/spec_v3/vectors/algo_001.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x11369798e8d01bf5`；通过ALGO-011 `property_test/ALGO-001/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=ALGO-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_001.py::test_algo_001_rr` |

## TC-ALGO-001-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-001-PF-01` |
| 对应单元ID | `ALGO-001` — face/physical tile 编码、投影与所有权守恒 |
| 父测试合同 | `T-ALGO-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `physical regions`；向量引用`tests/spec_v3/vectors/algo_001.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2985db06f9d6a37c`；通过ALGO-011 `property_test/ALGO-001/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_algo_001.py::test_algo_001_pf` |

## TC-ALGO-001-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-001-HL-01` |
| 对应单元ID | `ALGO-001` — face/physical tile 编码、投影与所有权守恒 |
| 父测试合同 | `T-ALGO-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `physical regions`；向量引用`tests/spec_v3/vectors/algo_001.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1ceb9572b627486b`；通过ALGO-011 `property_test/ALGO-001/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_algo_001.py::test_algo_001_hl` |

## TC-ALGO-002-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-002-UT-01` |
| 对应单元ID | `ALGO-002` — 手牌分解、向听、弃牌向听与等待形状 |
| 父测试合同 | `T-ALGO-002-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `concealed faces + melds`；向量引用`tests/spec_v3/vectors/algo_002.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc639f9d151b4a413`；通过ALGO-011 `property_test/ALGO-002/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_002_ut`对应路径 |
| 预期输出 | 匹配`GV-ALGO-002-N01`金标准；返回批准schema的`analyses`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_002.py::test_algo_002_ut` |

## TC-ALGO-002-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-002-BD-01` |
| 对应单元ID | `ALGO-002` — 手牌分解、向听、弃牌向听与等待形状 |
| 父测试合同 | `T-ALGO-002-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `concealed faces + melds`；向量引用`tests/spec_v3/vectors/algo_002.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x44eaaec2c85db2e1`；通过ALGO-011 `property_test/ALGO-002/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_002_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`analyses`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_002.py::test_algo_002_bd` |

## TC-ALGO-002-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-002-PT-01` |
| 对应单元ID | `ALGO-002` — 手牌分解、向听、弃牌向听与等待形状 |
| 父测试合同 | `T-ALGO-002-N01`、`T-ALGO-002-B01`、`T-ALGO-002-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `concealed faces + melds`；向量引用`tests/spec_v3/vectors/algo_002.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4a6d85a7221cf133`；通过ALGO-011 `property_test/ALGO-002/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_002_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_002.py::test_algo_002_pt` |

## TC-ALGO-002-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-002-PB-01` |
| 对应单元ID | `ALGO-002` — 手牌分解、向听、弃牌向听与等待形状 |
| 父测试合同 | `T-ALGO-002-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `concealed faces + melds`；向量引用`tests/spec_v3/vectors/algo_002.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5323a3deef7c5088`；通过ALGO-011 `property_test/ALGO-002/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_002.py::test_algo_002_pb` |

## TC-ALGO-002-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-002-IT-01` |
| 对应单元ID | `ALGO-002` — 手牌分解、向听、弃牌向听与等待形状 |
| 父测试合同 | `T-ALGO-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `concealed faces + melds`；向量引用`tests/spec_v3/vectors/algo_002.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1e5e1ef088f7a522`；通过ALGO-011 `property_test/ALGO-002/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_002_it`对应路径 |
| 预期输出 | 通过生产入口得到`analyses`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=ALGO-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_002.py::test_algo_002_it` |

## TC-ALGO-002-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-002-RR-01` |
| 对应单元ID | `ALGO-002` — 手牌分解、向听、弃牌向听与等待形状 |
| 父测试合同 | `T-ALGO-002-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `concealed faces + melds`；向量引用`tests/spec_v3/vectors/algo_002.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0206c0dd026a107a`；通过ALGO-011 `property_test/ALGO-002/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=ALGO-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_002.py::test_algo_002_rr` |

## TC-ALGO-002-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-002-PF-01` |
| 对应单元ID | `ALGO-002` — 手牌分解、向听、弃牌向听与等待形状 |
| 父测试合同 | `T-ALGO-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `concealed faces + melds`；向量引用`tests/spec_v3/vectors/algo_002.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe35ac12852dab839`；通过ALGO-011 `property_test/ALGO-002/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_algo_002.py::test_algo_002_pf` |

## TC-ALGO-002-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-002-HL-01` |
| 对应单元ID | `ALGO-002` — 手牌分解、向听、弃牌向听与等待形状 |
| 父测试合同 | `T-ALGO-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `concealed faces + melds`；向量引用`tests/spec_v3/vectors/algo_002.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7cc04a1a236ba3eb`；通过ALGO-011 `property_test/ALGO-002/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_algo_002.py::test_algo_002_hl` |

## TC-ALGO-003-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-003-UT-01` |
| 对应单元ID | `ALGO-003` — 去重可见牌与未见牌聚合 |
| 父测试合同 | `T-ALGO-003-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `PlayerView`；向量引用`tests/spec_v3/vectors/algo_003.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc57b8e4889f5ba13`；通过ALGO-011 `property_test/ALGO-003/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_003_ut`对应路径 |
| 预期输出 | 匹配`GV-ALGO-003-N01`金标准；返回批准schema的`visible/unseen counts`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_003.py::test_algo_003_ut` |

## TC-ALGO-003-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-003-BD-01` |
| 对应单元ID | `ALGO-003` — 去重可见牌与未见牌聚合 |
| 父测试合同 | `T-ALGO-003-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `PlayerView`；向量引用`tests/spec_v3/vectors/algo_003.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x45e59a7d64ef055e`；通过ALGO-011 `property_test/ALGO-003/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_003_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`visible/unseen counts`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_003.py::test_algo_003_bd` |

## TC-ALGO-003-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-003-PT-01` |
| 对应单元ID | `ALGO-003` — 去重可见牌与未见牌聚合 |
| 父测试合同 | `T-ALGO-003-N01`、`T-ALGO-003-B01`、`T-ALGO-003-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `PlayerView`；向量引用`tests/spec_v3/vectors/algo_003.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc86876c8ea74cb4f`；通过ALGO-011 `property_test/ALGO-003/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_003_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_003.py::test_algo_003_pt` |

## TC-ALGO-003-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-003-PB-01` |
| 对应单元ID | `ALGO-003` — 去重可见牌与未见牌聚合 |
| 父测试合同 | `T-ALGO-003-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `PlayerView`；向量引用`tests/spec_v3/vectors/algo_003.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x504743e0e72d4b23`；通过ALGO-011 `property_test/ALGO-003/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_003.py::test_algo_003_pb` |

## TC-ALGO-003-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-003-IT-01` |
| 对应单元ID | `ALGO-003` — 去重可见牌与未见牌聚合 |
| 父测试合同 | `T-ALGO-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `PlayerView`；向量引用`tests/spec_v3/vectors/algo_003.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x346ad69647fe702e`；通过ALGO-011 `property_test/ALGO-003/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_003_it`对应路径 |
| 预期输出 | 通过生产入口得到`visible/unseen counts`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=ALGO-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_003.py::test_algo_003_it` |

## TC-ALGO-003-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-003-RR-01` |
| 对应单元ID | `ALGO-003` — 去重可见牌与未见牌聚合 |
| 父测试合同 | `T-ALGO-003-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `PlayerView`；向量引用`tests/spec_v3/vectors/algo_003.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xca6760423ebaebd7`；通过ALGO-011 `property_test/ALGO-003/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=ALGO-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_003.py::test_algo_003_rr` |

## TC-ALGO-003-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-003-PF-01` |
| 对应单元ID | `ALGO-003` — 去重可见牌与未见牌聚合 |
| 父测试合同 | `T-ALGO-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `PlayerView`；向量引用`tests/spec_v3/vectors/algo_003.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe76da47b8882f26e`；通过ALGO-011 `property_test/ALGO-003/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_algo_003.py::test_algo_003_pf` |

## TC-ALGO-003-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-003-HL-01` |
| 对应单元ID | `ALGO-003` — 去重可见牌与未见牌聚合 |
| 父测试合同 | `T-ALGO-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `PlayerView`；向量引用`tests/spec_v3/vectors/algo_003.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x66aa41928b83a4ba`；通过ALGO-011 `property_test/ALGO-003/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_algo_003.py::test_algo_003_hl` |

## TC-ALGO-004-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-004-UT-01` |
| 对应单元ID | `ALGO-004` — 墙内活牌区间或估计 |
| 父测试合同 | `T-ALGO-004-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `unseen + public allocations`；向量引用`tests/spec_v3/vectors/algo_004.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf9912d2149049bd4`；通过ALGO-011 `property_test/ALGO-004/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_004_ut`对应路径 |
| 预期输出 | 匹配`GV-ALGO-004-N01`金标准；返回批准schema的`live estimate`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_004.py::test_algo_004_ut` |

## TC-ALGO-004-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-004-BD-01` |
| 对应单元ID | `ALGO-004` — 墙内活牌区间或估计 |
| 父测试合同 | `T-ALGO-004-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `unseen + public allocations`；向量引用`tests/spec_v3/vectors/algo_004.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x47cc8faff4417e74`；通过ALGO-011 `property_test/ALGO-004/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_004_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`live estimate`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_004.py::test_algo_004_bd` |

## TC-ALGO-004-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-004-PT-01` |
| 对应单元ID | `ALGO-004` — 墙内活牌区间或估计 |
| 父测试合同 | `T-ALGO-004-N01`、`T-ALGO-004-B01`、`T-ALGO-004-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `unseen + public allocations`；向量引用`tests/spec_v3/vectors/algo_004.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0cc95da6b28a0eed`；通过ALGO-011 `property_test/ALGO-004/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_004_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_004.py::test_algo_004_pt` |

## TC-ALGO-004-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-004-PB-01` |
| 对应单元ID | `ALGO-004` — 墙内活牌区间或估计 |
| 父测试合同 | `T-ALGO-004-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `unseen + public allocations`；向量引用`tests/spec_v3/vectors/algo_004.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcc5465a290034d65`；通过ALGO-011 `property_test/ALGO-004/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_004.py::test_algo_004_pb` |

## TC-ALGO-004-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-004-IT-01` |
| 对应单元ID | `ALGO-004` — 墙内活牌区间或估计 |
| 父测试合同 | `T-ALGO-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `unseen + public allocations`；向量引用`tests/spec_v3/vectors/algo_004.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa412713606073d36`；通过ALGO-011 `property_test/ALGO-004/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_004_it`对应路径 |
| 预期输出 | 通过生产入口得到`live estimate`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=ALGO-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_004.py::test_algo_004_it` |

## TC-ALGO-004-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-004-RR-01` |
| 对应单元ID | `ALGO-004` — 墙内活牌区间或估计 |
| 父测试合同 | `T-ALGO-004-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `unseen + public allocations`；向量引用`tests/spec_v3/vectors/algo_004.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa62e8213eef49fc3`；通过ALGO-011 `property_test/ALGO-004/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=ALGO-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_004.py::test_algo_004_rr` |

## TC-ALGO-004-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-004-PF-01` |
| 对应单元ID | `ALGO-004` — 墙内活牌区间或估计 |
| 父测试合同 | `T-ALGO-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `unseen + public allocations`；向量引用`tests/spec_v3/vectors/algo_004.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1d79fff459765a7c`；通过ALGO-011 `property_test/ALGO-004/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_algo_004.py::test_algo_004_pf` |

## TC-ALGO-004-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-004-HL-01` |
| 对应单元ID | `ALGO-004` — 墙内活牌区间或估计 |
| 父测试合同 | `T-ALGO-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `unseen + public allocations`；向量引用`tests/spec_v3/vectors/algo_004.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xebf6dbd351992270`；通过ALGO-011 `property_test/ALGO-004/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_algo_004.py::test_algo_004_hl` |

## TC-ALGO-005-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-005-UT-01` |
| 对应单元ID | `ALGO-005` — 逐座剩余摸牌机会估计 |
| 父测试合同 | `T-ALGO-005-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `active order + wall + response assumptions`；向量引用`tests/spec_v3/vectors/algo_005.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x22f1a0298cc565a4`；通过ALGO-011 `property_test/ALGO-005/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_005_ut`对应路径 |
| 预期输出 | 匹配`GV-ALGO-005-N01`金标准；返回批准schema的`draw interval`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_005.py::test_algo_005_ut` |

## TC-ALGO-005-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-005-BD-01` |
| 对应单元ID | `ALGO-005` — 逐座剩余摸牌机会估计 |
| 父测试合同 | `T-ALGO-005-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `active order + wall + response assumptions`；向量引用`tests/spec_v3/vectors/algo_005.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0fd1540873fed802`；通过ALGO-011 `property_test/ALGO-005/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_005_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`draw interval`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_005.py::test_algo_005_bd` |

## TC-ALGO-005-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-005-PT-01` |
| 对应单元ID | `ALGO-005` — 逐座剩余摸牌机会估计 |
| 父测试合同 | `T-ALGO-005-N01`、`T-ALGO-005-B01`、`T-ALGO-005-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `active order + wall + response assumptions`；向量引用`tests/spec_v3/vectors/algo_005.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xfb81280141999018`；通过ALGO-011 `property_test/ALGO-005/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_005_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_005.py::test_algo_005_pt` |

## TC-ALGO-005-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-005-PB-01` |
| 对应单元ID | `ALGO-005` — 逐座剩余摸牌机会估计 |
| 父测试合同 | `T-ALGO-005-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `active order + wall + response assumptions`；向量引用`tests/spec_v3/vectors/algo_005.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x439598afb400889b`；通过ALGO-011 `property_test/ALGO-005/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_005.py::test_algo_005_pb` |

## TC-ALGO-005-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-005-IT-01` |
| 对应单元ID | `ALGO-005` — 逐座剩余摸牌机会估计 |
| 父测试合同 | `T-ALGO-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `active order + wall + response assumptions`；向量引用`tests/spec_v3/vectors/algo_005.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9638f1bbf5e736d3`；通过ALGO-011 `property_test/ALGO-005/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_005_it`对应路径 |
| 预期输出 | 通过生产入口得到`draw interval`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=ALGO-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_005.py::test_algo_005_it` |

## TC-ALGO-005-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-005-RR-01` |
| 对应单元ID | `ALGO-005` — 逐座剩余摸牌机会估计 |
| 父测试合同 | `T-ALGO-005-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `active order + wall + response assumptions`；向量引用`tests/spec_v3/vectors/algo_005.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x739dd637bb6560f1`；通过ALGO-011 `property_test/ALGO-005/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=ALGO-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_005.py::test_algo_005_rr` |

## TC-ALGO-005-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-005-PF-01` |
| 对应单元ID | `ALGO-005` — 逐座剩余摸牌机会估计 |
| 父测试合同 | `T-ALGO-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `active order + wall + response assumptions`；向量引用`tests/spec_v3/vectors/algo_005.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe4a170ecd4e63a2a`；通过ALGO-011 `property_test/ALGO-005/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_algo_005.py::test_algo_005_pf` |

## TC-ALGO-005-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-005-HL-01` |
| 对应单元ID | `ALGO-005` — 逐座剩余摸牌机会估计 |
| 父测试合同 | `T-ALGO-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `active order + wall + response assumptions`；向量引用`tests/spec_v3/vectors/algo_005.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa5a3809f1f98d8d8`；通过ALGO-011 `property_test/ALGO-005/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_algo_005.py::test_algo_005_hl` |

## TC-ALGO-006-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-006-UT-01` |
| 对应单元ID | `ALGO-006` — mandatory 分类、候选上限与稳定排序 |
| 父测试合同 | `T-ALGO-006-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal actions + context`；向量引用`tests/spec_v3/vectors/algo_006.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe7cf9fdec6782071`；通过ALGO-011 `property_test/ALGO-006/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_006_ut`对应路径 |
| 预期输出 | 匹配`GV-ALGO-006-N01`金标准；返回批准schema的`mandatory/candidate set`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_006.py::test_algo_006_ut` |

## TC-ALGO-006-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-006-BD-01` |
| 对应单元ID | `ALGO-006` — mandatory 分类、候选上限与稳定排序 |
| 父测试合同 | `T-ALGO-006-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal actions + context`；向量引用`tests/spec_v3/vectors/algo_006.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x36ccfad6ecd3993e`；通过ALGO-011 `property_test/ALGO-006/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_006_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`mandatory/candidate set`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_006.py::test_algo_006_bd` |

## TC-ALGO-006-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-006-PT-01` |
| 对应单元ID | `ALGO-006` — mandatory 分类、候选上限与稳定排序 |
| 父测试合同 | `T-ALGO-006-N01`、`T-ALGO-006-B01`、`T-ALGO-006-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal actions + context`；向量引用`tests/spec_v3/vectors/algo_006.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbc59a56c9cbfb332`；通过ALGO-011 `property_test/ALGO-006/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_006_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_006.py::test_algo_006_pt` |

## TC-ALGO-006-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-006-PB-01` |
| 对应单元ID | `ALGO-006` — mandatory 分类、候选上限与稳定排序 |
| 父测试合同 | `T-ALGO-006-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal actions + context`；向量引用`tests/spec_v3/vectors/algo_006.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x463ab8f4b903cff2`；通过ALGO-011 `property_test/ALGO-006/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_006.py::test_algo_006_pb` |

## TC-ALGO-006-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-006-IT-01` |
| 对应单元ID | `ALGO-006` — mandatory 分类、候选上限与稳定排序 |
| 父测试合同 | `T-ALGO-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `legal actions + context`；向量引用`tests/spec_v3/vectors/algo_006.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe460bd50d3b2af17`；通过ALGO-011 `property_test/ALGO-006/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_006_it`对应路径 |
| 预期输出 | 通过生产入口得到`mandatory/candidate set`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=ALGO-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_006.py::test_algo_006_it` |

## TC-ALGO-006-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-006-RR-01` |
| 对应单元ID | `ALGO-006` — mandatory 分类、候选上限与稳定排序 |
| 父测试合同 | `T-ALGO-006-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal actions + context`；向量引用`tests/spec_v3/vectors/algo_006.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xfe4a14533e02ee46`；通过ALGO-011 `property_test/ALGO-006/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=ALGO-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_006.py::test_algo_006_rr` |

## TC-ALGO-006-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-006-PF-01` |
| 对应单元ID | `ALGO-006` — mandatory 分类、候选上限与稳定排序 |
| 父测试合同 | `T-ALGO-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal actions + context`；向量引用`tests/spec_v3/vectors/algo_006.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x52791b96bd11fb34`；通过ALGO-011 `property_test/ALGO-006/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_algo_006.py::test_algo_006_pf` |

## TC-ALGO-006-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-006-HL-01` |
| 对应单元ID | `ALGO-006` — mandatory 分类、候选上限与稳定排序 |
| 父测试合同 | `T-ALGO-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `legal actions + context`；向量引用`tests/spec_v3/vectors/algo_006.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xedaa5e3268e3d643`；通过ALGO-011 `property_test/ALGO-006/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_algo_006.py::test_algo_006_hl` |

## TC-ALGO-007-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-007-UT-01` |
| 对应单元ID | `ALGO-007` — 六分量候选 Q 评价 |
| 父测试合同 | `T-ALGO-007-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `normalized features + weights`；向量引用`tests/spec_v3/vectors/algo_007.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x12dbfbc28c8c7115`；通过ALGO-011 `property_test/ALGO-007/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_007_ut`对应路径 |
| 预期输出 | 匹配`GV-ALGO-007-N01`金标准；返回批准schema的`Q components/total`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_007.py::test_algo_007_ut` |

## TC-ALGO-007-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-007-BD-01` |
| 对应单元ID | `ALGO-007` — 六分量候选 Q 评价 |
| 父测试合同 | `T-ALGO-007-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `normalized features + weights`；向量引用`tests/spec_v3/vectors/algo_007.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd91ebab2a0ea5921`；通过ALGO-011 `property_test/ALGO-007/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_007_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`Q components/total`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_007.py::test_algo_007_bd` |

## TC-ALGO-007-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-007-PT-01` |
| 对应单元ID | `ALGO-007` — 六分量候选 Q 评价 |
| 父测试合同 | `T-ALGO-007-N01`、`T-ALGO-007-B01`、`T-ALGO-007-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `normalized features + weights`；向量引用`tests/spec_v3/vectors/algo_007.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2db89b05146c7dd8`；通过ALGO-011 `property_test/ALGO-007/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_007_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_007.py::test_algo_007_pt` |

## TC-ALGO-007-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-007-PB-01` |
| 对应单元ID | `ALGO-007` — 六分量候选 Q 评价 |
| 父测试合同 | `T-ALGO-007-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `normalized features + weights`；向量引用`tests/spec_v3/vectors/algo_007.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8497442c7f2b4bbf`；通过ALGO-011 `property_test/ALGO-007/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_007.py::test_algo_007_pb` |

## TC-ALGO-007-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-007-IT-01` |
| 对应单元ID | `ALGO-007` — 六分量候选 Q 评价 |
| 父测试合同 | `T-ALGO-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `normalized features + weights`；向量引用`tests/spec_v3/vectors/algo_007.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa2948c52db1d2494`；通过ALGO-011 `property_test/ALGO-007/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_007_it`对应路径 |
| 预期输出 | 通过生产入口得到`Q components/total`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=ALGO-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_007.py::test_algo_007_it` |

## TC-ALGO-007-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-007-RR-01` |
| 对应单元ID | `ALGO-007` — 六分量候选 Q 评价 |
| 父测试合同 | `T-ALGO-007-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `normalized features + weights`；向量引用`tests/spec_v3/vectors/algo_007.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x711c883bcd2f7c06`；通过ALGO-011 `property_test/ALGO-007/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=ALGO-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_007.py::test_algo_007_rr` |

## TC-ALGO-007-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-007-PF-01` |
| 对应单元ID | `ALGO-007` — 六分量候选 Q 评价 |
| 父测试合同 | `T-ALGO-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `normalized features + weights`；向量引用`tests/spec_v3/vectors/algo_007.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa5064d61897a0a85`；通过ALGO-011 `property_test/ALGO-007/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_algo_007.py::test_algo_007_pf` |

## TC-ALGO-007-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-007-HL-01` |
| 对应单元ID | `ALGO-007` — 六分量候选 Q 评价 |
| 父测试合同 | `T-ALGO-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `normalized features + weights`；向量引用`tests/spec_v3/vectors/algo_007.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa5a9534beb98041c`；通过ALGO-011 `property_test/ALGO-007/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_algo_007.py::test_algo_007_hl` |

## TC-ALGO-008-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-008-UT-01` |
| 对应单元ID | `ALGO-008` — seed、噪声、思考时间与随机流确定派生 |
| 父测试合同 | `T-ALGO-008-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id/seat/decision/config`；向量引用`tests/spec_v3/vectors/algo_008.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa07af58bf5b7d389`；通过ALGO-011 `property_test/ALGO-008/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_008_ut`对应路径 |
| 预期输出 | 匹配`GV-ALGO-008-N01`金标准；返回批准schema的`reproducible samples`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_008.py::test_algo_008_ut` |

## TC-ALGO-008-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-008-BD-01` |
| 对应单元ID | `ALGO-008` — seed、噪声、思考时间与随机流确定派生 |
| 父测试合同 | `T-ALGO-008-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id/seat/decision/config`；向量引用`tests/spec_v3/vectors/algo_008.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x45d9a71bed176fca`；通过ALGO-011 `property_test/ALGO-008/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_008_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`reproducible samples`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_008.py::test_algo_008_bd` |

## TC-ALGO-008-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-008-PT-01` |
| 对应单元ID | `ALGO-008` — seed、噪声、思考时间与随机流确定派生 |
| 父测试合同 | `T-ALGO-008-N01`、`T-ALGO-008-B01`、`T-ALGO-008-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id/seat/decision/config`；向量引用`tests/spec_v3/vectors/algo_008.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xddd3978869f2569c`；通过ALGO-011 `property_test/ALGO-008/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_008_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_008.py::test_algo_008_pt` |

## TC-ALGO-008-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-008-PB-01` |
| 对应单元ID | `ALGO-008` — seed、噪声、思考时间与随机流确定派生 |
| 父测试合同 | `T-ALGO-008-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id/seat/decision/config`；向量引用`tests/spec_v3/vectors/algo_008.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x66bfde363b771cd0`；通过ALGO-011 `property_test/ALGO-008/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_008.py::test_algo_008_pb` |

## TC-ALGO-008-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-008-IT-01` |
| 对应单元ID | `ALGO-008` — seed、噪声、思考时间与随机流确定派生 |
| 父测试合同 | `T-ALGO-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `game_id/seat/decision/config`；向量引用`tests/spec_v3/vectors/algo_008.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7d02cdb4ee7314c2`；通过ALGO-011 `property_test/ALGO-008/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_008_it`对应路径 |
| 预期输出 | 通过生产入口得到`reproducible samples`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=ALGO-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_008.py::test_algo_008_it` |

## TC-ALGO-008-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-008-RR-01` |
| 对应单元ID | `ALGO-008` — seed、噪声、思考时间与随机流确定派生 |
| 父测试合同 | `T-ALGO-008-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id/seat/decision/config`；向量引用`tests/spec_v3/vectors/algo_008.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xce7025abe91466d3`；通过ALGO-011 `property_test/ALGO-008/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=ALGO-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_008.py::test_algo_008_rr` |

## TC-ALGO-008-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-008-SD-01` |
| 对应单元ID | `ALGO-008` — seed、噪声、思考时间与随机流确定派生 |
| 父测试合同 | `T-ALGO-008-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id/seat/decision/config`；向量引用`tests/spec_v3/vectors/algo_008.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x813463b5b5112459`；通过ALGO-011 `property_test/ALGO-008/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_algo_008.py::test_algo_008_sd` |

## TC-ALGO-008-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-008-PF-01` |
| 对应单元ID | `ALGO-008` — seed、噪声、思考时间与随机流确定派生 |
| 父测试合同 | `T-ALGO-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id/seat/decision/config`；向量引用`tests/spec_v3/vectors/algo_008.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x35d2978e5b655155`；通过ALGO-011 `property_test/ALGO-008/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_algo_008.py::test_algo_008_pf` |

## TC-ALGO-008-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-008-HL-01` |
| 对应单元ID | `ALGO-008` — seed、噪声、思考时间与随机流确定派生 |
| 父测试合同 | `T-ALGO-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `game_id/seat/decision/config`；向量引用`tests/spec_v3/vectors/algo_008.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe6ea4345e83b5d10`；通过ALGO-011 `property_test/ALGO-008/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_algo_008.py::test_algo_008_hl` |

## TC-ALGO-009-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-009-UT-01` |
| 对应单元ID | `ALGO-009` — 配置类型/范围/版本校验、迁移与 canonical hash |
| 父测试合同 | `T-ALGO-009-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `raw config`；向量引用`tests/spec_v3/vectors/algo_009.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5baffa2a51a5ed7d`；通过ALGO-011 `property_test/ALGO-009/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_009_ut`对应路径 |
| 预期输出 | 匹配`GV-ALGO-009-N01`金标准；返回批准schema的`frozen config/hash or explicit error`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_009.py::test_algo_009_ut` |

## TC-ALGO-009-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-009-BD-01` |
| 对应单元ID | `ALGO-009` — 配置类型/范围/版本校验、迁移与 canonical hash |
| 父测试合同 | `T-ALGO-009-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `raw config`；向量引用`tests/spec_v3/vectors/algo_009.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x76dc3deaa6a9291c`；通过ALGO-011 `property_test/ALGO-009/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_009_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`frozen config/hash or explicit error`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_009.py::test_algo_009_bd` |

## TC-ALGO-009-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-009-PT-01` |
| 对应单元ID | `ALGO-009` — 配置类型/范围/版本校验、迁移与 canonical hash |
| 父测试合同 | `T-ALGO-009-N01`、`T-ALGO-009-B01`、`T-ALGO-009-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `raw config`；向量引用`tests/spec_v3/vectors/algo_009.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2ef85f8d61b697a7`；通过ALGO-011 `property_test/ALGO-009/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_009_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_009.py::test_algo_009_pt` |

## TC-ALGO-009-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-009-PB-01` |
| 对应单元ID | `ALGO-009` — 配置类型/范围/版本校验、迁移与 canonical hash |
| 父测试合同 | `T-ALGO-009-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `raw config`；向量引用`tests/spec_v3/vectors/algo_009.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3647aebf0e14b005`；通过ALGO-011 `property_test/ALGO-009/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_009.py::test_algo_009_pb` |

## TC-ALGO-009-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-009-IT-01` |
| 对应单元ID | `ALGO-009` — 配置类型/范围/版本校验、迁移与 canonical hash |
| 父测试合同 | `T-ALGO-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `raw config`；向量引用`tests/spec_v3/vectors/algo_009.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0767234d2cfa5f65`；通过ALGO-011 `property_test/ALGO-009/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_009_it`对应路径 |
| 预期输出 | 通过生产入口得到`frozen config/hash or explicit error`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=ALGO-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_009.py::test_algo_009_it` |

## TC-ALGO-009-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-009-RR-01` |
| 对应单元ID | `ALGO-009` — 配置类型/范围/版本校验、迁移与 canonical hash |
| 父测试合同 | `T-ALGO-009-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `raw config`；向量引用`tests/spec_v3/vectors/algo_009.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x14be7c3d1d0dda9b`；通过ALGO-011 `property_test/ALGO-009/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=ALGO-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_009.py::test_algo_009_rr` |

## TC-ALGO-009-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-009-PF-01` |
| 对应单元ID | `ALGO-009` — 配置类型/范围/版本校验、迁移与 canonical hash |
| 父测试合同 | `T-ALGO-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `raw config`；向量引用`tests/spec_v3/vectors/algo_009.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x578abbb6bb76e8a8`；通过ALGO-011 `property_test/ALGO-009/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_algo_009.py::test_algo_009_pf` |

## TC-ALGO-009-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-009-HL-01` |
| 对应单元ID | `ALGO-009` — 配置类型/范围/版本校验、迁移与 canonical hash |
| 父测试合同 | `T-ALGO-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `raw config`；向量引用`tests/spec_v3/vectors/algo_009.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x38b8bafeb8af10d1`；通过ALGO-011 `property_test/ALGO-009/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_algo_009.py::test_algo_009_hl` |

## TC-ALGO-010-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-010-UT-01` |
| 对应单元ID | `ALGO-010` — PlayerView 白名单构建 |
| 父测试合同 | `T-ALGO-010-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `authoritative state + seat + phase`；向量引用`tests/spec_v3/vectors/algo_010.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7cb3fd8d1dc52e22`；通过ALGO-011 `property_test/ALGO-010/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_010_ut`对应路径 |
| 预期输出 | 匹配`GV-ALGO-010-N01`金标准；返回批准schema的`PlayerView`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_010.py::test_algo_010_ut` |

## TC-ALGO-010-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-010-BD-01` |
| 对应单元ID | `ALGO-010` — PlayerView 白名单构建 |
| 父测试合同 | `T-ALGO-010-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `authoritative state + seat + phase`；向量引用`tests/spec_v3/vectors/algo_010.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7bf7043bcdf30d1f`；通过ALGO-011 `property_test/ALGO-010/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_010_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`PlayerView`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_010.py::test_algo_010_bd` |

## TC-ALGO-010-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-010-PT-01` |
| 对应单元ID | `ALGO-010` — PlayerView 白名单构建 |
| 父测试合同 | `T-ALGO-010-N01`、`T-ALGO-010-B01`、`T-ALGO-010-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `authoritative state + seat + phase`；向量引用`tests/spec_v3/vectors/algo_010.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0cd96ed851ff536b`；通过ALGO-011 `property_test/ALGO-010/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_010_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_010.py::test_algo_010_pt` |

## TC-ALGO-010-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-010-PB-01` |
| 对应单元ID | `ALGO-010` — PlayerView 白名单构建 |
| 父测试合同 | `T-ALGO-010-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `authoritative state + seat + phase`；向量引用`tests/spec_v3/vectors/algo_010.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x18deeacb2475c247`；通过ALGO-011 `property_test/ALGO-010/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_010.py::test_algo_010_pb` |

## TC-ALGO-010-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-010-IT-01` |
| 对应单元ID | `ALGO-010` — PlayerView 白名单构建 |
| 父测试合同 | `T-ALGO-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `authoritative state + seat + phase`；向量引用`tests/spec_v3/vectors/algo_010.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0de38692d7fe6280`；通过ALGO-011 `property_test/ALGO-010/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_010_it`对应路径 |
| 预期输出 | 通过生产入口得到`PlayerView`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=ALGO-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_010.py::test_algo_010_it` |

## TC-ALGO-010-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-010-RR-01` |
| 对应单元ID | `ALGO-010` — PlayerView 白名单构建 |
| 父测试合同 | `T-ALGO-010-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `authoritative state + seat + phase`；向量引用`tests/spec_v3/vectors/algo_010.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7ea68ea6938a53cf`；通过ALGO-011 `property_test/ALGO-010/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=ALGO-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_010.py::test_algo_010_rr` |

## TC-ALGO-010-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-010-PF-01` |
| 对应单元ID | `ALGO-010` — PlayerView 白名单构建 |
| 父测试合同 | `T-ALGO-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `authoritative state + seat + phase`；向量引用`tests/spec_v3/vectors/algo_010.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x314f5ddbd470de5c`；通过ALGO-011 `property_test/ALGO-010/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_algo_010.py::test_algo_010_pf` |

## TC-ALGO-010-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-010-HL-01` |
| 对应单元ID | `ALGO-010` — PlayerView 白名单构建 |
| 父测试合同 | `T-ALGO-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `authoritative state + seat + phase`；向量引用`tests/spec_v3/vectors/algo_010.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbea65a1803e2b81c`；通过ALGO-011 `property_test/ALGO-010/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_algo_010.py::test_algo_010_hl` |

## TC-ALGO-011-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-011-UT-01` |
| 对应单元ID | `ALGO-011` — game_id 到牌墙、骰子及子随机流的确定映射 |
| 父测试合同 | `T-ALGO-011-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id + versions`；向量引用`tests/spec_v3/vectors/algo_011.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6109b719eb5dc781`；通过ALGO-011 `property_test/ALGO-011/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_011_ut`对应路径 |
| 预期输出 | 匹配`GV-ALGO-011-N01`金标准；返回批准schema的`named RNG streams`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_011.py::test_algo_011_ut` |

## TC-ALGO-011-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-011-BD-01` |
| 对应单元ID | `ALGO-011` — game_id 到牌墙、骰子及子随机流的确定映射 |
| 父测试合同 | `T-ALGO-011-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id + versions`；向量引用`tests/spec_v3/vectors/algo_011.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf0057d6eafff1086`；通过ALGO-011 `property_test/ALGO-011/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_011_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`named RNG streams`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_011.py::test_algo_011_bd` |

## TC-ALGO-011-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-011-PT-01` |
| 对应单元ID | `ALGO-011` — game_id 到牌墙、骰子及子随机流的确定映射 |
| 父测试合同 | `T-ALGO-011-N01`、`T-ALGO-011-B01`、`T-ALGO-011-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id + versions`；向量引用`tests/spec_v3/vectors/algo_011.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb8414011c654fda5`；通过ALGO-011 `property_test/ALGO-011/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_011_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_011.py::test_algo_011_pt` |

## TC-ALGO-011-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-011-PB-01` |
| 对应单元ID | `ALGO-011` — game_id 到牌墙、骰子及子随机流的确定映射 |
| 父测试合同 | `T-ALGO-011-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id + versions`；向量引用`tests/spec_v3/vectors/algo_011.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf1368b369202fbdd`；通过ALGO-011 `property_test/ALGO-011/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_011.py::test_algo_011_pb` |

## TC-ALGO-011-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-011-IT-01` |
| 对应单元ID | `ALGO-011` — game_id 到牌墙、骰子及子随机流的确定映射 |
| 父测试合同 | `T-ALGO-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `game_id + versions`；向量引用`tests/spec_v3/vectors/algo_011.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf63008da83915f2e`；通过ALGO-011 `property_test/ALGO-011/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_algo_011_it`对应路径 |
| 预期输出 | 通过生产入口得到`named RNG streams`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=ALGO-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_011.py::test_algo_011_it` |

## TC-ALGO-011-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-011-RR-01` |
| 对应单元ID | `ALGO-011` — game_id 到牌墙、骰子及子随机流的确定映射 |
| 父测试合同 | `T-ALGO-011-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id + versions`；向量引用`tests/spec_v3/vectors/algo_011.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5d6ee115ee48a2b1`；通过ALGO-011 `property_test/ALGO-011/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=ALGO-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_algo_011.py::test_algo_011_rr` |

## TC-ALGO-011-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-011-SD-01` |
| 对应单元ID | `ALGO-011` — game_id 到牌墙、骰子及子随机流的确定映射 |
| 父测试合同 | `T-ALGO-011-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id + versions`；向量引用`tests/spec_v3/vectors/algo_011.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x38d09c7529d5f061`；通过ALGO-011 `property_test/ALGO-011/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_algo_011.py::test_algo_011_sd` |

## TC-ALGO-011-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-011-PF-01` |
| 对应单元ID | `ALGO-011` — game_id 到牌墙、骰子及子随机流的确定映射 |
| 父测试合同 | `T-ALGO-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `game_id + versions`；向量引用`tests/spec_v3/vectors/algo_011.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x50efb8501a0bb0c5`；通过ALGO-011 `property_test/ALGO-011/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_algo_011.py::test_algo_011_pf` |

## TC-ALGO-011-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-ALGO-011-HL-01` |
| 对应单元ID | `ALGO-011` — game_id 到牌墙、骰子及子随机流的确定映射 |
| 父测试合同 | `T-ALGO-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `game_id + versions`；向量引用`tests/spec_v3/vectors/algo_011.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd499b1064f7348b0`；通过ALGO-011 `property_test/ALGO-011/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=ALGO-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_algo_011.py::test_algo_011_hl` |

## TC-HEUR-001-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-001-UT-01` |
| 对应单元ID | `HEUR-001` — 换三张候选评价 |
| 父测试合同 | `T-HEUR-001-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal triples + hand/public features`；向量引用`tests/spec_v3/vectors/heur_001.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1de355d63361c890`；通过ALGO-011 `property_test/HEUR-001/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_001_ut`对应路径 |
| 预期输出 | 返回批准schema的`ranked triples`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_001.py::test_heur_001_ut` |

## TC-HEUR-001-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-001-BD-01` |
| 对应单元ID | `HEUR-001` — 换三张候选评价 |
| 父测试合同 | `T-HEUR-001-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal triples + hand/public features`；向量引用`tests/spec_v3/vectors/heur_001.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb6768fb5029f8a74`；通过ALGO-011 `property_test/HEUR-001/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_001_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`ranked triples`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_001.py::test_heur_001_bd` |

## TC-HEUR-001-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-001-PT-01` |
| 对应单元ID | `HEUR-001` — 换三张候选评价 |
| 父测试合同 | `T-HEUR-001-N01`、`T-HEUR-001-B01`、`T-HEUR-001-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal triples + hand/public features`；向量引用`tests/spec_v3/vectors/heur_001.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb01d409a73ec2cdb`；通过ALGO-011 `property_test/HEUR-001/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_001_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_001.py::test_heur_001_pt` |

## TC-HEUR-001-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-001-PB-01` |
| 对应单元ID | `HEUR-001` — 换三张候选评价 |
| 父测试合同 | `T-HEUR-001-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal triples + hand/public features`；向量引用`tests/spec_v3/vectors/heur_001.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8812c7aea5b4a5df`；通过ALGO-011 `property_test/HEUR-001/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_001.py::test_heur_001_pb` |

## TC-HEUR-001-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-001-SM-01` |
| 对应单元ID | `HEUR-001` — 换三张候选评价 |
| 父测试合同 | `T-HEUR-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `legal triples + hand/public features`；向量引用`tests/spec_v3/vectors/heur_001.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x232622047965ba50`；通过ALGO-011 `property_test/HEUR-001/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_001_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_001.py::test_heur_001_sm` |

## TC-HEUR-001-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-001-IT-01` |
| 对应单元ID | `HEUR-001` — 换三张候选评价 |
| 父测试合同 | `T-HEUR-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `legal triples + hand/public features`；向量引用`tests/spec_v3/vectors/heur_001.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x32dc9e97949ff02c`；通过ALGO-011 `property_test/HEUR-001/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_001_it`对应路径 |
| 预期输出 | 通过生产入口得到`ranked triples`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_001.py::test_heur_001_it` |

## TC-HEUR-001-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-001-RR-01` |
| 对应单元ID | `HEUR-001` — 换三张候选评价 |
| 父测试合同 | `T-HEUR-001-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal triples + hand/public features`；向量引用`tests/spec_v3/vectors/heur_001.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0861a901068e8482`；通过ALGO-011 `property_test/HEUR-001/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_001.py::test_heur_001_rr` |

## TC-HEUR-001-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-001-SD-01` |
| 对应单元ID | `HEUR-001` — 换三张候选评价 |
| 父测试合同 | `T-HEUR-001-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal triples + hand/public features`；向量引用`tests/spec_v3/vectors/heur_001.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x140cbff45a417145`；通过ALGO-011 `property_test/HEUR-001/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_001.py::test_heur_001_sd` |

## TC-HEUR-001-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-001-PF-01` |
| 对应单元ID | `HEUR-001` — 换三张候选评价 |
| 父测试合同 | `T-HEUR-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal triples + hand/public features`；向量引用`tests/spec_v3/vectors/heur_001.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x74a2aa85c64ab0eb`；通过ALGO-011 `property_test/HEUR-001/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_001.py::test_heur_001_pf` |

## TC-HEUR-001-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-001-HL-01` |
| 对应单元ID | `HEUR-001` — 换三张候选评价 |
| 父测试合同 | `T-HEUR-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `legal triples + hand/public features`；向量引用`tests/spec_v3/vectors/heur_001.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3a1da38485149bfe`；通过ALGO-011 `property_test/HEUR-001/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_001.py::test_heur_001_hl` |

## TC-HEUR-002-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-002-UT-01` |
| 对应单元ID | `HEUR-002` — 定缺花色评价 |
| 父测试合同 | `T-HEUR-002-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand structure + public context`；向量引用`tests/spec_v3/vectors/heur_002.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbea051f0d9309a36`；通过ALGO-011 `property_test/HEUR-002/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_002_ut`对应路径 |
| 预期输出 | 返回批准schema的`ranked suits`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_002.py::test_heur_002_ut` |

## TC-HEUR-002-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-002-BD-01` |
| 对应单元ID | `HEUR-002` — 定缺花色评价 |
| 父测试合同 | `T-HEUR-002-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand structure + public context`；向量引用`tests/spec_v3/vectors/heur_002.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc865e8bd5d853610`；通过ALGO-011 `property_test/HEUR-002/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_002_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`ranked suits`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_002.py::test_heur_002_bd` |

## TC-HEUR-002-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-002-PT-01` |
| 对应单元ID | `HEUR-002` — 定缺花色评价 |
| 父测试合同 | `T-HEUR-002-N01`、`T-HEUR-002-B01`、`T-HEUR-002-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand structure + public context`；向量引用`tests/spec_v3/vectors/heur_002.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x77f83480291dd63b`；通过ALGO-011 `property_test/HEUR-002/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_002_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_002.py::test_heur_002_pt` |

## TC-HEUR-002-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-002-PB-01` |
| 对应单元ID | `HEUR-002` — 定缺花色评价 |
| 父测试合同 | `T-HEUR-002-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand structure + public context`；向量引用`tests/spec_v3/vectors/heur_002.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x17fa5bdabf2b66eb`；通过ALGO-011 `property_test/HEUR-002/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_002.py::test_heur_002_pb` |

## TC-HEUR-002-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-002-SM-01` |
| 对应单元ID | `HEUR-002` — 定缺花色评价 |
| 父测试合同 | `T-HEUR-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `hand structure + public context`；向量引用`tests/spec_v3/vectors/heur_002.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x72a0f41b48da4d0d`；通过ALGO-011 `property_test/HEUR-002/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_002_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_002.py::test_heur_002_sm` |

## TC-HEUR-002-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-002-IT-01` |
| 对应单元ID | `HEUR-002` — 定缺花色评价 |
| 父测试合同 | `T-HEUR-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `hand structure + public context`；向量引用`tests/spec_v3/vectors/heur_002.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x55fd752f2dd3372e`；通过ALGO-011 `property_test/HEUR-002/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_002_it`对应路径 |
| 预期输出 | 通过生产入口得到`ranked suits`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_002.py::test_heur_002_it` |

## TC-HEUR-002-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-002-RR-01` |
| 对应单元ID | `HEUR-002` — 定缺花色评价 |
| 父测试合同 | `T-HEUR-002-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand structure + public context`；向量引用`tests/spec_v3/vectors/heur_002.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x434fe60b9d682fb7`；通过ALGO-011 `property_test/HEUR-002/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_002.py::test_heur_002_rr` |

## TC-HEUR-002-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-002-SD-01` |
| 对应单元ID | `HEUR-002` — 定缺花色评价 |
| 父测试合同 | `T-HEUR-002-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand structure + public context`；向量引用`tests/spec_v3/vectors/heur_002.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xafc6105ccc8434ef`；通过ALGO-011 `property_test/HEUR-002/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_002.py::test_heur_002_sd` |

## TC-HEUR-002-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-002-PF-01` |
| 对应单元ID | `HEUR-002` — 定缺花色评价 |
| 父测试合同 | `T-HEUR-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand structure + public context`；向量引用`tests/spec_v3/vectors/heur_002.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0914d6aa2fe429b1`；通过ALGO-011 `property_test/HEUR-002/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_002.py::test_heur_002_pf` |

## TC-HEUR-002-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-002-HL-01` |
| 对应单元ID | `HEUR-002` — 定缺花色评价 |
| 父测试合同 | `T-HEUR-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `hand structure + public context`；向量引用`tests/spec_v3/vectors/heur_002.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3b4a909526d93fac`；通过ALGO-011 `property_test/HEUR-002/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_002.py::test_heur_002_hl` |

## TC-HEUR-003-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-003-UT-01` |
| 对应单元ID | `HEUR-003` — 动态风格调节 |
| 父测试合同 | `T-HEUR-003-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + score/stage/hand`；向量引用`tests/spec_v3/vectors/heur_003.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xeb9c83f94263b71d`；通过ALGO-011 `property_test/HEUR-003/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_003_ut`对应路径 |
| 预期输出 | 返回批准schema的`effective style knobs`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_003.py::test_heur_003_ut` |

## TC-HEUR-003-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-003-BD-01` |
| 对应单元ID | `HEUR-003` — 动态风格调节 |
| 父测试合同 | `T-HEUR-003-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + score/stage/hand`；向量引用`tests/spec_v3/vectors/heur_003.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb14bc01f03925cbb`；通过ALGO-011 `property_test/HEUR-003/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_003_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`effective style knobs`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_003.py::test_heur_003_bd` |

## TC-HEUR-003-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-003-PT-01` |
| 对应单元ID | `HEUR-003` — 动态风格调节 |
| 父测试合同 | `T-HEUR-003-N01`、`T-HEUR-003-B01`、`T-HEUR-003-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + score/stage/hand`；向量引用`tests/spec_v3/vectors/heur_003.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5b53383e6898002f`；通过ALGO-011 `property_test/HEUR-003/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_003_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_003.py::test_heur_003_pt` |

## TC-HEUR-003-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-003-PB-01` |
| 对应单元ID | `HEUR-003` — 动态风格调节 |
| 父测试合同 | `T-HEUR-003-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + score/stage/hand`；向量引用`tests/spec_v3/vectors/heur_003.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x97d52dc0a7e1c5a3`；通过ALGO-011 `property_test/HEUR-003/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_003.py::test_heur_003_pb` |

## TC-HEUR-003-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-003-SM-01` |
| 对应单元ID | `HEUR-003` — 动态风格调节 |
| 父测试合同 | `T-HEUR-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `profile + score/stage/hand`；向量引用`tests/spec_v3/vectors/heur_003.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4e31d8d1fd1392c6`；通过ALGO-011 `property_test/HEUR-003/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_003_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_003.py::test_heur_003_sm` |

## TC-HEUR-003-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-003-IT-01` |
| 对应单元ID | `HEUR-003` — 动态风格调节 |
| 父测试合同 | `T-HEUR-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `profile + score/stage/hand`；向量引用`tests/spec_v3/vectors/heur_003.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x968e07bb6d449488`；通过ALGO-011 `property_test/HEUR-003/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_003_it`对应路径 |
| 预期输出 | 通过生产入口得到`effective style knobs`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_003.py::test_heur_003_it` |

## TC-HEUR-003-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-003-RR-01` |
| 对应单元ID | `HEUR-003` — 动态风格调节 |
| 父测试合同 | `T-HEUR-003-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + score/stage/hand`；向量引用`tests/spec_v3/vectors/heur_003.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa8b3f9a47a15dd68`；通过ALGO-011 `property_test/HEUR-003/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_003.py::test_heur_003_rr` |

## TC-HEUR-003-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-003-SD-01` |
| 对应单元ID | `HEUR-003` — 动态风格调节 |
| 父测试合同 | `T-HEUR-003-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + score/stage/hand`；向量引用`tests/spec_v3/vectors/heur_003.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x63c3dece014b9604`；通过ALGO-011 `property_test/HEUR-003/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_003.py::test_heur_003_sd` |

## TC-HEUR-003-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-003-PF-01` |
| 对应单元ID | `HEUR-003` — 动态风格调节 |
| 父测试合同 | `T-HEUR-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + score/stage/hand`；向量引用`tests/spec_v3/vectors/heur_003.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0c6360003447e26c`；通过ALGO-011 `property_test/HEUR-003/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_003.py::test_heur_003_pf` |

## TC-HEUR-003-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-003-HL-01` |
| 对应单元ID | `HEUR-003` — 动态风格调节 |
| 父测试合同 | `T-HEUR-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `profile + score/stage/hand`；向量引用`tests/spec_v3/vectors/heur_003.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x087dab6f3c1062c7`；通过ALGO-011 `property_test/HEUR-003/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_003.py::test_heur_003_hl` |

## TC-HEUR-004-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-004-UT-01` |
| 对应单元ID | `HEUR-004` — 初始做牌方向形成 |
| 父测试合同 | `T-HEUR-004-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `initial analysis + profile`；向量引用`tests/spec_v3/vectors/heur_004.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbba8341578e70a9a`；通过ALGO-011 `property_test/HEUR-004/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_004_ut`对应路径 |
| 预期输出 | 返回批准schema的`primary/backup direction`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_004.py::test_heur_004_ut` |

## TC-HEUR-004-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-004-BD-01` |
| 对应单元ID | `HEUR-004` — 初始做牌方向形成 |
| 父测试合同 | `T-HEUR-004-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `initial analysis + profile`；向量引用`tests/spec_v3/vectors/heur_004.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf7276ad0f5a91f4e`；通过ALGO-011 `property_test/HEUR-004/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_004_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`primary/backup direction`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_004.py::test_heur_004_bd` |

## TC-HEUR-004-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-004-PT-01` |
| 对应单元ID | `HEUR-004` — 初始做牌方向形成 |
| 父测试合同 | `T-HEUR-004-N01`、`T-HEUR-004-B01`、`T-HEUR-004-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `initial analysis + profile`；向量引用`tests/spec_v3/vectors/heur_004.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6a23305c95954eda`；通过ALGO-011 `property_test/HEUR-004/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_004_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_004.py::test_heur_004_pt` |

## TC-HEUR-004-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-004-PB-01` |
| 对应单元ID | `HEUR-004` — 初始做牌方向形成 |
| 父测试合同 | `T-HEUR-004-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `initial analysis + profile`；向量引用`tests/spec_v3/vectors/heur_004.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3c0eba801e99bede`；通过ALGO-011 `property_test/HEUR-004/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_004.py::test_heur_004_pb` |

## TC-HEUR-004-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-004-SM-01` |
| 对应单元ID | `HEUR-004` — 初始做牌方向形成 |
| 父测试合同 | `T-HEUR-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `initial analysis + profile`；向量引用`tests/spec_v3/vectors/heur_004.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3f604f36a26fbdc3`；通过ALGO-011 `property_test/HEUR-004/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_004_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_004.py::test_heur_004_sm` |

## TC-HEUR-004-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-004-IT-01` |
| 对应单元ID | `HEUR-004` — 初始做牌方向形成 |
| 父测试合同 | `T-HEUR-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `initial analysis + profile`；向量引用`tests/spec_v3/vectors/heur_004.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1fa6670269bcf199`；通过ALGO-011 `property_test/HEUR-004/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_004_it`对应路径 |
| 预期输出 | 通过生产入口得到`primary/backup direction`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_004.py::test_heur_004_it` |

## TC-HEUR-004-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-004-RR-01` |
| 对应单元ID | `HEUR-004` — 初始做牌方向形成 |
| 父测试合同 | `T-HEUR-004-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `initial analysis + profile`；向量引用`tests/spec_v3/vectors/heur_004.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x87824cbaed0ad04e`；通过ALGO-011 `property_test/HEUR-004/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_004.py::test_heur_004_rr` |

## TC-HEUR-004-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-004-SD-01` |
| 对应单元ID | `HEUR-004` — 初始做牌方向形成 |
| 父测试合同 | `T-HEUR-004-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `initial analysis + profile`；向量引用`tests/spec_v3/vectors/heur_004.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8088effe539660e6`；通过ALGO-011 `property_test/HEUR-004/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_004.py::test_heur_004_sd` |

## TC-HEUR-004-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-004-PF-01` |
| 对应单元ID | `HEUR-004` — 初始做牌方向形成 |
| 父测试合同 | `T-HEUR-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `initial analysis + profile`；向量引用`tests/spec_v3/vectors/heur_004.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc261d597e9548bac`；通过ALGO-011 `property_test/HEUR-004/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_004.py::test_heur_004_pf` |

## TC-HEUR-004-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-004-HL-01` |
| 对应单元ID | `HEUR-004` — 初始做牌方向形成 |
| 父测试合同 | `T-HEUR-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `initial analysis + profile`；向量引用`tests/spec_v3/vectors/heur_004.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf27eeae7c73927f8`；通过ALGO-011 `property_test/HEUR-004/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_004.py::test_heur_004_hl` |

## TC-HEUR-005-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-005-UT-01` |
| 对应单元ID | `HEUR-005` — 主备计划生命周期 |
| 父测试合同 | `T-HEUR-005-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observations + current plan`；向量引用`tests/spec_v3/vectors/heur_005.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1b73461e35516033`；通过ALGO-011 `property_test/HEUR-005/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_005_ut`对应路径 |
| 预期输出 | 返回批准schema的`retain/switch/restart`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_005.py::test_heur_005_ut` |

## TC-HEUR-005-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-005-BD-01` |
| 对应单元ID | `HEUR-005` — 主备计划生命周期 |
| 父测试合同 | `T-HEUR-005-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observations + current plan`；向量引用`tests/spec_v3/vectors/heur_005.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb4356413829e22c0`；通过ALGO-011 `property_test/HEUR-005/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_005_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`retain/switch/restart`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_005.py::test_heur_005_bd` |

## TC-HEUR-005-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-005-PT-01` |
| 对应单元ID | `HEUR-005` — 主备计划生命周期 |
| 父测试合同 | `T-HEUR-005-N01`、`T-HEUR-005-B01`、`T-HEUR-005-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observations + current plan`；向量引用`tests/spec_v3/vectors/heur_005.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8b1d028b7694e3cc`；通过ALGO-011 `property_test/HEUR-005/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_005_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_005.py::test_heur_005_pt` |

## TC-HEUR-005-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-005-PB-01` |
| 对应单元ID | `HEUR-005` — 主备计划生命周期 |
| 父测试合同 | `T-HEUR-005-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observations + current plan`；向量引用`tests/spec_v3/vectors/heur_005.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe445c231e4d515b8`；通过ALGO-011 `property_test/HEUR-005/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_005.py::test_heur_005_pb` |

## TC-HEUR-005-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-005-SM-01` |
| 对应单元ID | `HEUR-005` — 主备计划生命周期 |
| 父测试合同 | `T-HEUR-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `observations + current plan`；向量引用`tests/spec_v3/vectors/heur_005.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe12773a8a27373a5`；通过ALGO-011 `property_test/HEUR-005/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_005_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_005.py::test_heur_005_sm` |

## TC-HEUR-005-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-005-IT-01` |
| 对应单元ID | `HEUR-005` — 主备计划生命周期 |
| 父测试合同 | `T-HEUR-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `observations + current plan`；向量引用`tests/spec_v3/vectors/heur_005.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1ad1f640f8aff1f2`；通过ALGO-011 `property_test/HEUR-005/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_005_it`对应路径 |
| 预期输出 | 通过生产入口得到`retain/switch/restart`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_005.py::test_heur_005_it` |

## TC-HEUR-005-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-005-RR-01` |
| 对应单元ID | `HEUR-005` — 主备计划生命周期 |
| 父测试合同 | `T-HEUR-005-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observations + current plan`；向量引用`tests/spec_v3/vectors/heur_005.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5e03686ff7e998c1`；通过ALGO-011 `property_test/HEUR-005/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_005.py::test_heur_005_rr` |

## TC-HEUR-005-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-005-SD-01` |
| 对应单元ID | `HEUR-005` — 主备计划生命周期 |
| 父测试合同 | `T-HEUR-005-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observations + current plan`；向量引用`tests/spec_v3/vectors/heur_005.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd71262c38178b031`；通过ALGO-011 `property_test/HEUR-005/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_005.py::test_heur_005_sd` |

## TC-HEUR-005-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-005-PF-01` |
| 对应单元ID | `HEUR-005` — 主备计划生命周期 |
| 父测试合同 | `T-HEUR-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observations + current plan`；向量引用`tests/spec_v3/vectors/heur_005.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x53c9016236339f0b`；通过ALGO-011 `property_test/HEUR-005/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_005.py::test_heur_005_pf` |

## TC-HEUR-005-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-005-HL-01` |
| 对应单元ID | `HEUR-005` — 主备计划生命周期 |
| 父测试合同 | `T-HEUR-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `observations + current plan`；向量引用`tests/spec_v3/vectors/heur_005.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd598dbb61a4b9fd3`；通过ALGO-011 `property_test/HEUR-005/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_005.py::test_heur_005_hl` |

## TC-HEUR-006-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-006-UT-01` |
| 对应单元ID | `HEUR-006` — 定缺花色环境评估 |
| 父测试合同 | `T-HEUR-006-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `all public dingque/melds`；向量引用`tests/spec_v3/vectors/heur_006.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf79537b73606d25b`；通过ALGO-011 `property_test/HEUR-006/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_006_ut`对应路径 |
| 预期输出 | 返回批准schema的`suit environment`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_006.py::test_heur_006_ut` |

## TC-HEUR-006-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-006-BD-01` |
| 对应单元ID | `HEUR-006` — 定缺花色环境评估 |
| 父测试合同 | `T-HEUR-006-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `all public dingque/melds`；向量引用`tests/spec_v3/vectors/heur_006.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x985bb305fa3c0032`；通过ALGO-011 `property_test/HEUR-006/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_006_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`suit environment`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_006.py::test_heur_006_bd` |

## TC-HEUR-006-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-006-PT-01` |
| 对应单元ID | `HEUR-006` — 定缺花色环境评估 |
| 父测试合同 | `T-HEUR-006-N01`、`T-HEUR-006-B01`、`T-HEUR-006-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `all public dingque/melds`；向量引用`tests/spec_v3/vectors/heur_006.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x69aec098c18ca41d`；通过ALGO-011 `property_test/HEUR-006/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_006_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_006.py::test_heur_006_pt` |

## TC-HEUR-006-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-006-PB-01` |
| 对应单元ID | `HEUR-006` — 定缺花色环境评估 |
| 父测试合同 | `T-HEUR-006-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `all public dingque/melds`；向量引用`tests/spec_v3/vectors/heur_006.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2b59d63a96795d81`；通过ALGO-011 `property_test/HEUR-006/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_006.py::test_heur_006_pb` |

## TC-HEUR-006-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-006-SM-01` |
| 对应单元ID | `HEUR-006` — 定缺花色环境评估 |
| 父测试合同 | `T-HEUR-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `all public dingque/melds`；向量引用`tests/spec_v3/vectors/heur_006.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8174ea646562e925`；通过ALGO-011 `property_test/HEUR-006/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_006_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_006.py::test_heur_006_sm` |

## TC-HEUR-006-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-006-IT-01` |
| 对应单元ID | `HEUR-006` — 定缺花色环境评估 |
| 父测试合同 | `T-HEUR-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `all public dingque/melds`；向量引用`tests/spec_v3/vectors/heur_006.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x579bc27ae97674b3`；通过ALGO-011 `property_test/HEUR-006/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_006_it`对应路径 |
| 预期输出 | 通过生产入口得到`suit environment`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_006.py::test_heur_006_it` |

## TC-HEUR-006-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-006-RR-01` |
| 对应单元ID | `HEUR-006` — 定缺花色环境评估 |
| 父测试合同 | `T-HEUR-006-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `all public dingque/melds`；向量引用`tests/spec_v3/vectors/heur_006.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x61d7326c1f0652bc`；通过ALGO-011 `property_test/HEUR-006/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_006.py::test_heur_006_rr` |

## TC-HEUR-006-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-006-SD-01` |
| 对应单元ID | `HEUR-006` — 定缺花色环境评估 |
| 父测试合同 | `T-HEUR-006-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `all public dingque/melds`；向量引用`tests/spec_v3/vectors/heur_006.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xabf91ccd49c53ab2`；通过ALGO-011 `property_test/HEUR-006/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_006.py::test_heur_006_sd` |

## TC-HEUR-006-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-006-PF-01` |
| 对应单元ID | `HEUR-006` — 定缺花色环境评估 |
| 父测试合同 | `T-HEUR-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `all public dingque/melds`；向量引用`tests/spec_v3/vectors/heur_006.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7d99a686dda32dcf`；通过ALGO-011 `property_test/HEUR-006/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_006.py::test_heur_006_pf` |

## TC-HEUR-006-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-006-HL-01` |
| 对应单元ID | `HEUR-006` — 定缺花色环境评估 |
| 父测试合同 | `T-HEUR-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `all public dingque/melds`；向量引用`tests/spec_v3/vectors/heur_006.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xadf34ab7571f62ea`；通过ALGO-011 `property_test/HEUR-006/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_006.py::test_heur_006_hl` |

## TC-HEUR-007-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-007-UT-01` |
| 对应单元ID | `HEUR-007` — 公开事件驱动的逐家方向更新 |
| 父测试合同 | `T-HEUR-007-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `prior hypotheses + events`；向量引用`tests/spec_v3/vectors/heur_007.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8a6c3b89231e8548`；通过ALGO-011 `property_test/HEUR-007/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_007_ut`对应路径 |
| 预期输出 | 返回批准schema的`heuristic direction evidence`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_007.py::test_heur_007_ut` |

## TC-HEUR-007-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-007-BD-01` |
| 对应单元ID | `HEUR-007` — 公开事件驱动的逐家方向更新 |
| 父测试合同 | `T-HEUR-007-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `prior hypotheses + events`；向量引用`tests/spec_v3/vectors/heur_007.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7bfe608b65ac206d`；通过ALGO-011 `property_test/HEUR-007/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_007_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`heuristic direction evidence`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_007.py::test_heur_007_bd` |

## TC-HEUR-007-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-007-PT-01` |
| 对应单元ID | `HEUR-007` — 公开事件驱动的逐家方向更新 |
| 父测试合同 | `T-HEUR-007-N01`、`T-HEUR-007-B01`、`T-HEUR-007-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `prior hypotheses + events`；向量引用`tests/spec_v3/vectors/heur_007.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xded4782afb88c29c`；通过ALGO-011 `property_test/HEUR-007/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_007_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_007.py::test_heur_007_pt` |

## TC-HEUR-007-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-007-PB-01` |
| 对应单元ID | `HEUR-007` — 公开事件驱动的逐家方向更新 |
| 父测试合同 | `T-HEUR-007-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `prior hypotheses + events`；向量引用`tests/spec_v3/vectors/heur_007.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x36fec015e9fdedf6`；通过ALGO-011 `property_test/HEUR-007/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_007.py::test_heur_007_pb` |

## TC-HEUR-007-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-007-SM-01` |
| 对应单元ID | `HEUR-007` — 公开事件驱动的逐家方向更新 |
| 父测试合同 | `T-HEUR-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `prior hypotheses + events`；向量引用`tests/spec_v3/vectors/heur_007.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x56852a5aa7882dfd`；通过ALGO-011 `property_test/HEUR-007/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_007_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_007.py::test_heur_007_sm` |

## TC-HEUR-007-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-007-IT-01` |
| 对应单元ID | `HEUR-007` — 公开事件驱动的逐家方向更新 |
| 父测试合同 | `T-HEUR-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `prior hypotheses + events`；向量引用`tests/spec_v3/vectors/heur_007.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x84fdbf7cb972768d`；通过ALGO-011 `property_test/HEUR-007/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_007_it`对应路径 |
| 预期输出 | 通过生产入口得到`heuristic direction evidence`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_007.py::test_heur_007_it` |

## TC-HEUR-007-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-007-RR-01` |
| 对应单元ID | `HEUR-007` — 公开事件驱动的逐家方向更新 |
| 父测试合同 | `T-HEUR-007-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `prior hypotheses + events`；向量引用`tests/spec_v3/vectors/heur_007.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc4bf13fb2bebac90`；通过ALGO-011 `property_test/HEUR-007/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_007.py::test_heur_007_rr` |

## TC-HEUR-007-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-007-SD-01` |
| 对应单元ID | `HEUR-007` — 公开事件驱动的逐家方向更新 |
| 父测试合同 | `T-HEUR-007-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `prior hypotheses + events`；向量引用`tests/spec_v3/vectors/heur_007.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe03fc53212e9b630`；通过ALGO-011 `property_test/HEUR-007/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_007.py::test_heur_007_sd` |

## TC-HEUR-007-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-007-PF-01` |
| 对应单元ID | `HEUR-007` — 公开事件驱动的逐家方向更新 |
| 父测试合同 | `T-HEUR-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `prior hypotheses + events`；向量引用`tests/spec_v3/vectors/heur_007.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x07bc52b0d97dfd7d`；通过ALGO-011 `property_test/HEUR-007/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_007.py::test_heur_007_pf` |

## TC-HEUR-007-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-007-HL-01` |
| 对应单元ID | `HEUR-007` — 公开事件驱动的逐家方向更新 |
| 父测试合同 | `T-HEUR-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `prior hypotheses + events`；向量引用`tests/spec_v3/vectors/heur_007.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2689e82687f8ab95`；通过ALGO-011 `property_test/HEUR-007/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_007.py::test_heur_007_hl` |

## TC-HEUR-008-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-008-UT-01` |
| 对应单元ID | `HEUR-008` — 整场比分与剩余局效用调节 |
| 父测试合同 | `T-HEUR-008-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `standings + rounds left`；向量引用`tests/spec_v3/vectors/heur_008.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5f3da977bad8774c`；通过ALGO-011 `property_test/HEUR-008/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_008_ut`对应路径 |
| 预期输出 | 返回批准schema的`match utility modifiers`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_008.py::test_heur_008_ut` |

## TC-HEUR-008-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-008-BD-01` |
| 对应单元ID | `HEUR-008` — 整场比分与剩余局效用调节 |
| 父测试合同 | `T-HEUR-008-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `standings + rounds left`；向量引用`tests/spec_v3/vectors/heur_008.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5256b5dfa8d508b0`；通过ALGO-011 `property_test/HEUR-008/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_008_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`match utility modifiers`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_008.py::test_heur_008_bd` |

## TC-HEUR-008-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-008-PT-01` |
| 对应单元ID | `HEUR-008` — 整场比分与剩余局效用调节 |
| 父测试合同 | `T-HEUR-008-N01`、`T-HEUR-008-B01`、`T-HEUR-008-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `standings + rounds left`；向量引用`tests/spec_v3/vectors/heur_008.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4126e7965e7316f0`；通过ALGO-011 `property_test/HEUR-008/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_008_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_008.py::test_heur_008_pt` |

## TC-HEUR-008-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-008-PB-01` |
| 对应单元ID | `HEUR-008` — 整场比分与剩余局效用调节 |
| 父测试合同 | `T-HEUR-008-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `standings + rounds left`；向量引用`tests/spec_v3/vectors/heur_008.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x114a0fee8946a4fe`；通过ALGO-011 `property_test/HEUR-008/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_008.py::test_heur_008_pb` |

## TC-HEUR-008-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-008-SM-01` |
| 对应单元ID | `HEUR-008` — 整场比分与剩余局效用调节 |
| 父测试合同 | `T-HEUR-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `standings + rounds left`；向量引用`tests/spec_v3/vectors/heur_008.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xef7f040a680b5b44`；通过ALGO-011 `property_test/HEUR-008/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_008_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_008.py::test_heur_008_sm` |

## TC-HEUR-008-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-008-IT-01` |
| 对应单元ID | `HEUR-008` — 整场比分与剩余局效用调节 |
| 父测试合同 | `T-HEUR-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `standings + rounds left`；向量引用`tests/spec_v3/vectors/heur_008.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x886bc55c91574a23`；通过ALGO-011 `property_test/HEUR-008/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_008_it`对应路径 |
| 预期输出 | 通过生产入口得到`match utility modifiers`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_008.py::test_heur_008_it` |

## TC-HEUR-008-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-008-RR-01` |
| 对应单元ID | `HEUR-008` — 整场比分与剩余局效用调节 |
| 父测试合同 | `T-HEUR-008-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `standings + rounds left`；向量引用`tests/spec_v3/vectors/heur_008.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x90cac0b3ea5a70af`；通过ALGO-011 `property_test/HEUR-008/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_008.py::test_heur_008_rr` |

## TC-HEUR-008-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-008-SD-01` |
| 对应单元ID | `HEUR-008` — 整场比分与剩余局效用调节 |
| 父测试合同 | `T-HEUR-008-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `standings + rounds left`；向量引用`tests/spec_v3/vectors/heur_008.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x865c8de4c7e0643f`；通过ALGO-011 `property_test/HEUR-008/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_008.py::test_heur_008_sd` |

## TC-HEUR-008-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-008-PF-01` |
| 对应单元ID | `HEUR-008` — 整场比分与剩余局效用调节 |
| 父测试合同 | `T-HEUR-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `standings + rounds left`；向量引用`tests/spec_v3/vectors/heur_008.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6c8198799759603f`；通过ALGO-011 `property_test/HEUR-008/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_008.py::test_heur_008_pf` |

## TC-HEUR-008-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-008-HL-01` |
| 对应单元ID | `HEUR-008` — 整场比分与剩余局效用调节 |
| 父测试合同 | `T-HEUR-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `standings + rounds left`；向量引用`tests/spec_v3/vectors/heur_008.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7ec427d97d4d8c56`；通过ALGO-011 `property_test/HEUR-008/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_008.py::test_heur_008_hl` |

## TC-HEUR-009-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-009-UT-01` |
| 对应单元ID | `HEUR-009` — 先胡、做大和血战顺序效用 |
| 父测试合同 | `T-HEUR-009-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hu order + hand value + risk`；向量引用`tests/spec_v3/vectors/heur_009.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x29fb1e7b638608f3`；通过ALGO-011 `property_test/HEUR-009/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_009_ut`对应路径 |
| 预期输出 | 返回批准schema的`speed/value preference`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_009.py::test_heur_009_ut` |

## TC-HEUR-009-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-009-BD-01` |
| 对应单元ID | `HEUR-009` — 先胡、做大和血战顺序效用 |
| 父测试合同 | `T-HEUR-009-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hu order + hand value + risk`；向量引用`tests/spec_v3/vectors/heur_009.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa3d8ee89063c2855`；通过ALGO-011 `property_test/HEUR-009/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_009_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`speed/value preference`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_009.py::test_heur_009_bd` |

## TC-HEUR-009-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-009-PT-01` |
| 对应单元ID | `HEUR-009` — 先胡、做大和血战顺序效用 |
| 父测试合同 | `T-HEUR-009-N01`、`T-HEUR-009-B01`、`T-HEUR-009-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hu order + hand value + risk`；向量引用`tests/spec_v3/vectors/heur_009.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x467c051c5f634c6e`；通过ALGO-011 `property_test/HEUR-009/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_009_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_009.py::test_heur_009_pt` |

## TC-HEUR-009-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-009-PB-01` |
| 对应单元ID | `HEUR-009` — 先胡、做大和血战顺序效用 |
| 父测试合同 | `T-HEUR-009-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hu order + hand value + risk`；向量引用`tests/spec_v3/vectors/heur_009.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3ee688b7635fdfa0`；通过ALGO-011 `property_test/HEUR-009/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_009.py::test_heur_009_pb` |

## TC-HEUR-009-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-009-SM-01` |
| 对应单元ID | `HEUR-009` — 先胡、做大和血战顺序效用 |
| 父测试合同 | `T-HEUR-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `hu order + hand value + risk`；向量引用`tests/spec_v3/vectors/heur_009.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x85426d2333de6435`；通过ALGO-011 `property_test/HEUR-009/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_009_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_009.py::test_heur_009_sm` |

## TC-HEUR-009-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-009-IT-01` |
| 对应单元ID | `HEUR-009` — 先胡、做大和血战顺序效用 |
| 父测试合同 | `T-HEUR-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `hu order + hand value + risk`；向量引用`tests/spec_v3/vectors/heur_009.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x238f209a3c0259f8`；通过ALGO-011 `property_test/HEUR-009/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_009_it`对应路径 |
| 预期输出 | 通过生产入口得到`speed/value preference`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_009.py::test_heur_009_it` |

## TC-HEUR-009-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-009-RR-01` |
| 对应单元ID | `HEUR-009` — 先胡、做大和血战顺序效用 |
| 父测试合同 | `T-HEUR-009-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hu order + hand value + risk`；向量引用`tests/spec_v3/vectors/heur_009.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x336deb117d185273`；通过ALGO-011 `property_test/HEUR-009/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_009.py::test_heur_009_rr` |

## TC-HEUR-009-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-009-SD-01` |
| 对应单元ID | `HEUR-009` — 先胡、做大和血战顺序效用 |
| 父测试合同 | `T-HEUR-009-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hu order + hand value + risk`；向量引用`tests/spec_v3/vectors/heur_009.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb17ceccf1671bb1b`；通过ALGO-011 `property_test/HEUR-009/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_009.py::test_heur_009_sd` |

## TC-HEUR-009-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-009-PF-01` |
| 对应单元ID | `HEUR-009` — 先胡、做大和血战顺序效用 |
| 父测试合同 | `T-HEUR-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hu order + hand value + risk`；向量引用`tests/spec_v3/vectors/heur_009.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6c85afd9e242d700`；通过ALGO-011 `property_test/HEUR-009/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_009.py::test_heur_009_pf` |

## TC-HEUR-009-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-009-HL-01` |
| 对应单元ID | `HEUR-009` — 先胡、做大和血战顺序效用 |
| 父测试合同 | `T-HEUR-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `hu order + hand value + risk`；向量引用`tests/spec_v3/vectors/heur_009.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4a7ead02f1d2dac6`；通过ALGO-011 `property_test/HEUR-009/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_009.py::test_heur_009_hl` |

## TC-HEUR-010-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-010-UT-01` |
| 对应单元ID | `HEUR-010` — 多目标冲突复核 |
| 父测试合同 | `T-HEUR-010-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `speed/fan/risk/plan/match signals`；向量引用`tests/spec_v3/vectors/heur_010.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x30fab07968a0ad0c`；通过ALGO-011 `property_test/HEUR-010/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_010_ut`对应路径 |
| 预期输出 | 返回批准schema的`resolved preference`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_010.py::test_heur_010_ut` |

## TC-HEUR-010-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-010-BD-01` |
| 对应单元ID | `HEUR-010` — 多目标冲突复核 |
| 父测试合同 | `T-HEUR-010-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `speed/fan/risk/plan/match signals`；向量引用`tests/spec_v3/vectors/heur_010.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd0e56c7cde539367`；通过ALGO-011 `property_test/HEUR-010/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_010_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`resolved preference`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_010.py::test_heur_010_bd` |

## TC-HEUR-010-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-010-PT-01` |
| 对应单元ID | `HEUR-010` — 多目标冲突复核 |
| 父测试合同 | `T-HEUR-010-N01`、`T-HEUR-010-B01`、`T-HEUR-010-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `speed/fan/risk/plan/match signals`；向量引用`tests/spec_v3/vectors/heur_010.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1eb1640077f11f22`；通过ALGO-011 `property_test/HEUR-010/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_010_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_010.py::test_heur_010_pt` |

## TC-HEUR-010-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-010-PB-01` |
| 对应单元ID | `HEUR-010` — 多目标冲突复核 |
| 父测试合同 | `T-HEUR-010-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `speed/fan/risk/plan/match signals`；向量引用`tests/spec_v3/vectors/heur_010.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xaeef6567a25494cf`；通过ALGO-011 `property_test/HEUR-010/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_010.py::test_heur_010_pb` |

## TC-HEUR-010-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-010-SM-01` |
| 对应单元ID | `HEUR-010` — 多目标冲突复核 |
| 父测试合同 | `T-HEUR-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `speed/fan/risk/plan/match signals`；向量引用`tests/spec_v3/vectors/heur_010.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0bc4e36e0c519584`；通过ALGO-011 `property_test/HEUR-010/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_010_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_010.py::test_heur_010_sm` |

## TC-HEUR-010-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-010-IT-01` |
| 对应单元ID | `HEUR-010` — 多目标冲突复核 |
| 父测试合同 | `T-HEUR-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `speed/fan/risk/plan/match signals`；向量引用`tests/spec_v3/vectors/heur_010.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa11d4a7644f74a2e`；通过ALGO-011 `property_test/HEUR-010/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_010_it`对应路径 |
| 预期输出 | 通过生产入口得到`resolved preference`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_010.py::test_heur_010_it` |

## TC-HEUR-010-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-010-RR-01` |
| 对应单元ID | `HEUR-010` — 多目标冲突复核 |
| 父测试合同 | `T-HEUR-010-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `speed/fan/risk/plan/match signals`；向量引用`tests/spec_v3/vectors/heur_010.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xde123df6cc024b85`；通过ALGO-011 `property_test/HEUR-010/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_010.py::test_heur_010_rr` |

## TC-HEUR-010-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-010-SD-01` |
| 对应单元ID | `HEUR-010` — 多目标冲突复核 |
| 父测试合同 | `T-HEUR-010-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `speed/fan/risk/plan/match signals`；向量引用`tests/spec_v3/vectors/heur_010.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7ed8b8647ab3cdbb`；通过ALGO-011 `property_test/HEUR-010/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_010.py::test_heur_010_sd` |

## TC-HEUR-010-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-010-PF-01` |
| 对应单元ID | `HEUR-010` — 多目标冲突复核 |
| 父测试合同 | `T-HEUR-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `speed/fan/risk/plan/match signals`；向量引用`tests/spec_v3/vectors/heur_010.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xecf64233b5c23d08`；通过ALGO-011 `property_test/HEUR-010/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_010.py::test_heur_010_pf` |

## TC-HEUR-010-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-010-HL-01` |
| 对应单元ID | `HEUR-010` — 多目标冲突复核 |
| 父测试合同 | `T-HEUR-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `speed/fan/risk/plan/match signals`；向量引用`tests/spec_v3/vectors/heur_010.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x129f98d3cea279db`；通过ALGO-011 `property_test/HEUR-010/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_010.py::test_heur_010_hl` |

## TC-HEUR-011-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-011-UT-01` |
| 对应单元ID | `HEUR-011` — 番型边际做牌价值 |
| 父测试合同 | `T-HEUR-011-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `enabled fan policy + hand path`；向量引用`tests/spec_v3/vectors/heur_011.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf7fac74f6261c611`；通过ALGO-011 `property_test/HEUR-011/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_011_ut`对应路径 |
| 预期输出 | 返回批准schema的`marginal value`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_011.py::test_heur_011_ut` |

## TC-HEUR-011-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-011-BD-01` |
| 对应单元ID | `HEUR-011` — 番型边际做牌价值 |
| 父测试合同 | `T-HEUR-011-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `enabled fan policy + hand path`；向量引用`tests/spec_v3/vectors/heur_011.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc3257c7811eb8e43`；通过ALGO-011 `property_test/HEUR-011/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_011_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`marginal value`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_011.py::test_heur_011_bd` |

## TC-HEUR-011-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-011-PT-01` |
| 对应单元ID | `HEUR-011` — 番型边际做牌价值 |
| 父测试合同 | `T-HEUR-011-N01`、`T-HEUR-011-B01`、`T-HEUR-011-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `enabled fan policy + hand path`；向量引用`tests/spec_v3/vectors/heur_011.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb0a2ea35cdda0f10`；通过ALGO-011 `property_test/HEUR-011/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_011_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_011.py::test_heur_011_pt` |

## TC-HEUR-011-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-011-PB-01` |
| 对应单元ID | `HEUR-011` — 番型边际做牌价值 |
| 父测试合同 | `T-HEUR-011-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `enabled fan policy + hand path`；向量引用`tests/spec_v3/vectors/heur_011.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4d406bc649bfa54d`；通过ALGO-011 `property_test/HEUR-011/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_011.py::test_heur_011_pb` |

## TC-HEUR-011-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-011-SM-01` |
| 对应单元ID | `HEUR-011` — 番型边际做牌价值 |
| 父测试合同 | `T-HEUR-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `enabled fan policy + hand path`；向量引用`tests/spec_v3/vectors/heur_011.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2ac751beef81333e`；通过ALGO-011 `property_test/HEUR-011/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_011_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_011.py::test_heur_011_sm` |

## TC-HEUR-011-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-011-IT-01` |
| 对应单元ID | `HEUR-011` — 番型边际做牌价值 |
| 父测试合同 | `T-HEUR-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `enabled fan policy + hand path`；向量引用`tests/spec_v3/vectors/heur_011.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb26d73eadede9a0b`；通过ALGO-011 `property_test/HEUR-011/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_011_it`对应路径 |
| 预期输出 | 通过生产入口得到`marginal value`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_011.py::test_heur_011_it` |

## TC-HEUR-011-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-011-RR-01` |
| 对应单元ID | `HEUR-011` — 番型边际做牌价值 |
| 父测试合同 | `T-HEUR-011-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `enabled fan policy + hand path`；向量引用`tests/spec_v3/vectors/heur_011.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa03799b37aa7b0f7`；通过ALGO-011 `property_test/HEUR-011/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_011.py::test_heur_011_rr` |

## TC-HEUR-011-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-011-SD-01` |
| 对应单元ID | `HEUR-011` — 番型边际做牌价值 |
| 父测试合同 | `T-HEUR-011-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `enabled fan policy + hand path`；向量引用`tests/spec_v3/vectors/heur_011.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa5d27cf81d15e937`；通过ALGO-011 `property_test/HEUR-011/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_011.py::test_heur_011_sd` |

## TC-HEUR-011-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-011-PF-01` |
| 对应单元ID | `HEUR-011` — 番型边际做牌价值 |
| 父测试合同 | `T-HEUR-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `enabled fan policy + hand path`；向量引用`tests/spec_v3/vectors/heur_011.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x27094e83db08b5f8`；通过ALGO-011 `property_test/HEUR-011/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_011.py::test_heur_011_pf` |

## TC-HEUR-011-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-011-HL-01` |
| 对应单元ID | `HEUR-011` — 番型边际做牌价值 |
| 父测试合同 | `T-HEUR-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `enabled fan policy + hand path`；向量引用`tests/spec_v3/vectors/heur_011.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd20fc0b113338ebc`；通过ALGO-011 `property_test/HEUR-011/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_011.py::test_heur_011_hl` |

## TC-HEUR-012-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-012-UT-01` |
| 对应单元ID | `HEUR-012` — 碰牌策略评价 |
| 父测试合同 | `T-HEUR-012-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal peng + structure/exposure/turn`；向量引用`tests/spec_v3/vectors/heur_012.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x96ed2f6cfbbdea67`；通过ALGO-011 `property_test/HEUR-012/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_012_ut`对应路径 |
| 预期输出 | 返回批准schema的`accept/pass score`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_012.py::test_heur_012_ut` |

## TC-HEUR-012-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-012-BD-01` |
| 对应单元ID | `HEUR-012` — 碰牌策略评价 |
| 父测试合同 | `T-HEUR-012-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal peng + structure/exposure/turn`；向量引用`tests/spec_v3/vectors/heur_012.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcad2cfe56bd5be63`；通过ALGO-011 `property_test/HEUR-012/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_012_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`accept/pass score`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_012.py::test_heur_012_bd` |

## TC-HEUR-012-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-012-PT-01` |
| 对应单元ID | `HEUR-012` — 碰牌策略评价 |
| 父测试合同 | `T-HEUR-012-N01`、`T-HEUR-012-B01`、`T-HEUR-012-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal peng + structure/exposure/turn`；向量引用`tests/spec_v3/vectors/heur_012.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4cdfebfa21930859`；通过ALGO-011 `property_test/HEUR-012/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_012_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_012.py::test_heur_012_pt` |

## TC-HEUR-012-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-012-PB-01` |
| 对应单元ID | `HEUR-012` — 碰牌策略评价 |
| 父测试合同 | `T-HEUR-012-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal peng + structure/exposure/turn`；向量引用`tests/spec_v3/vectors/heur_012.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4935db661c5a3546`；通过ALGO-011 `property_test/HEUR-012/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_012.py::test_heur_012_pb` |

## TC-HEUR-012-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-012-SM-01` |
| 对应单元ID | `HEUR-012` — 碰牌策略评价 |
| 父测试合同 | `T-HEUR-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `legal peng + structure/exposure/turn`；向量引用`tests/spec_v3/vectors/heur_012.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9c8a459e94a7a34d`；通过ALGO-011 `property_test/HEUR-012/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_012_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_012.py::test_heur_012_sm` |

## TC-HEUR-012-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-012-IT-01` |
| 对应单元ID | `HEUR-012` — 碰牌策略评价 |
| 父测试合同 | `T-HEUR-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `legal peng + structure/exposure/turn`；向量引用`tests/spec_v3/vectors/heur_012.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x413dce77388955af`；通过ALGO-011 `property_test/HEUR-012/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_012_it`对应路径 |
| 预期输出 | 通过生产入口得到`accept/pass score`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_012.py::test_heur_012_it` |

## TC-HEUR-012-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-012-RR-01` |
| 对应单元ID | `HEUR-012` — 碰牌策略评价 |
| 父测试合同 | `T-HEUR-012-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal peng + structure/exposure/turn`；向量引用`tests/spec_v3/vectors/heur_012.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5bdfd3c374f7d11f`；通过ALGO-011 `property_test/HEUR-012/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_012.py::test_heur_012_rr` |

## TC-HEUR-012-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-012-SD-01` |
| 对应单元ID | `HEUR-012` — 碰牌策略评价 |
| 父测试合同 | `T-HEUR-012-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal peng + structure/exposure/turn`；向量引用`tests/spec_v3/vectors/heur_012.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9aa48819275c26d8`；通过ALGO-011 `property_test/HEUR-012/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_012.py::test_heur_012_sd` |

## TC-HEUR-012-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-012-PF-01` |
| 对应单元ID | `HEUR-012` — 碰牌策略评价 |
| 父测试合同 | `T-HEUR-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal peng + structure/exposure/turn`；向量引用`tests/spec_v3/vectors/heur_012.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x416099e3d90abb0d`；通过ALGO-011 `property_test/HEUR-012/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_012.py::test_heur_012_pf` |

## TC-HEUR-012-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-012-HL-01` |
| 对应单元ID | `HEUR-012` — 碰牌策略评价 |
| 父测试合同 | `T-HEUR-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `legal peng + structure/exposure/turn`；向量引用`tests/spec_v3/vectors/heur_012.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd7f39c5e681d4be9`；通过ALGO-011 `property_test/HEUR-012/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_012.py::test_heur_012_hl` |

## TC-HEUR-013-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-013-UT-01` |
| 对应单元ID | `HEUR-013` — 杠牌策略评价 |
| 父测试合同 | `T-HEUR-013-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal gang + score/risk/rob context`；向量引用`tests/spec_v3/vectors/heur_013.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdd903ff2260acc5f`；通过ALGO-011 `property_test/HEUR-013/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_013_ut`对应路径 |
| 预期输出 | 返回批准schema的`accept/pass score`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_013.py::test_heur_013_ut` |

## TC-HEUR-013-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-013-BD-01` |
| 对应单元ID | `HEUR-013` — 杠牌策略评价 |
| 父测试合同 | `T-HEUR-013-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal gang + score/risk/rob context`；向量引用`tests/spec_v3/vectors/heur_013.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb61fa79d64f5aac1`；通过ALGO-011 `property_test/HEUR-013/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_013_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`accept/pass score`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_013.py::test_heur_013_bd` |

## TC-HEUR-013-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-013-PT-01` |
| 对应单元ID | `HEUR-013` — 杠牌策略评价 |
| 父测试合同 | `T-HEUR-013-N01`、`T-HEUR-013-B01`、`T-HEUR-013-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal gang + score/risk/rob context`；向量引用`tests/spec_v3/vectors/heur_013.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa66e0a80af22495a`；通过ALGO-011 `property_test/HEUR-013/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_013_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_013.py::test_heur_013_pt` |

## TC-HEUR-013-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-013-PB-01` |
| 对应单元ID | `HEUR-013` — 杠牌策略评价 |
| 父测试合同 | `T-HEUR-013-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal gang + score/risk/rob context`；向量引用`tests/spec_v3/vectors/heur_013.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5963ab511988e39b`；通过ALGO-011 `property_test/HEUR-013/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_013.py::test_heur_013_pb` |

## TC-HEUR-013-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-013-SM-01` |
| 对应单元ID | `HEUR-013` — 杠牌策略评价 |
| 父测试合同 | `T-HEUR-013-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `legal gang + score/risk/rob context`；向量引用`tests/spec_v3/vectors/heur_013.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x986a11c88ecb00a7`；通过ALGO-011 `property_test/HEUR-013/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_013_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_013.py::test_heur_013_sm` |

## TC-HEUR-013-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-013-IT-01` |
| 对应单元ID | `HEUR-013` — 杠牌策略评价 |
| 父测试合同 | `T-HEUR-013-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `legal gang + score/risk/rob context`；向量引用`tests/spec_v3/vectors/heur_013.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf7ccd38279f1e47b`；通过ALGO-011 `property_test/HEUR-013/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_013_it`对应路径 |
| 预期输出 | 通过生产入口得到`accept/pass score`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_013.py::test_heur_013_it` |

## TC-HEUR-013-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-013-RR-01` |
| 对应单元ID | `HEUR-013` — 杠牌策略评价 |
| 父测试合同 | `T-HEUR-013-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal gang + score/risk/rob context`；向量引用`tests/spec_v3/vectors/heur_013.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcb43d69e57a6534a`；通过ALGO-011 `property_test/HEUR-013/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_013.py::test_heur_013_rr` |

## TC-HEUR-013-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-013-SD-01` |
| 对应单元ID | `HEUR-013` — 杠牌策略评价 |
| 父测试合同 | `T-HEUR-013-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal gang + score/risk/rob context`；向量引用`tests/spec_v3/vectors/heur_013.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x488ee7f796d7beea`；通过ALGO-011 `property_test/HEUR-013/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_013.py::test_heur_013_sd` |

## TC-HEUR-013-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-013-PF-01` |
| 对应单元ID | `HEUR-013` — 杠牌策略评价 |
| 父测试合同 | `T-HEUR-013-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `legal gang + score/risk/rob context`；向量引用`tests/spec_v3/vectors/heur_013.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x023b991081677325`；通过ALGO-011 `property_test/HEUR-013/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_013.py::test_heur_013_pf` |

## TC-HEUR-013-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-013-HL-01` |
| 对应单元ID | `HEUR-013` — 杠牌策略评价 |
| 父测试合同 | `T-HEUR-013-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `legal gang + score/risk/rob context`；向量引用`tests/spec_v3/vectors/heur_013.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdf497dcc3be95bbe`；通过ALGO-011 `property_test/HEUR-013/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_013.py::test_heur_013_hl` |

## TC-HEUR-014-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-014-UT-01` |
| 对应单元ID | `HEUR-014` — 出牌牌效与结构保留策略 |
| 父测试合同 | `T-HEUR-014-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `analyzed hand + legal discards`；向量引用`tests/spec_v3/vectors/heur_014.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x70f22ef9959ce956`；通过ALGO-011 `property_test/HEUR-014/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_014_ut`对应路径 |
| 预期输出 | 返回批准schema的`strategic rank`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_014.py::test_heur_014_ut` |

## TC-HEUR-014-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-014-BD-01` |
| 对应单元ID | `HEUR-014` — 出牌牌效与结构保留策略 |
| 父测试合同 | `T-HEUR-014-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `analyzed hand + legal discards`；向量引用`tests/spec_v3/vectors/heur_014.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x65c219b936c4c4a4`；通过ALGO-011 `property_test/HEUR-014/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_014_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`strategic rank`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_014.py::test_heur_014_bd` |

## TC-HEUR-014-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-014-PT-01` |
| 对应单元ID | `HEUR-014` — 出牌牌效与结构保留策略 |
| 父测试合同 | `T-HEUR-014-N01`、`T-HEUR-014-B01`、`T-HEUR-014-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `analyzed hand + legal discards`；向量引用`tests/spec_v3/vectors/heur_014.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x213dcfa83807dc4a`；通过ALGO-011 `property_test/HEUR-014/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_014_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_014.py::test_heur_014_pt` |

## TC-HEUR-014-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-014-PB-01` |
| 对应单元ID | `HEUR-014` — 出牌牌效与结构保留策略 |
| 父测试合同 | `T-HEUR-014-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `analyzed hand + legal discards`；向量引用`tests/spec_v3/vectors/heur_014.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xefece0fc5115fe0e`；通过ALGO-011 `property_test/HEUR-014/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_014.py::test_heur_014_pb` |

## TC-HEUR-014-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-014-SM-01` |
| 对应单元ID | `HEUR-014` — 出牌牌效与结构保留策略 |
| 父测试合同 | `T-HEUR-014-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `analyzed hand + legal discards`；向量引用`tests/spec_v3/vectors/heur_014.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x63eb9f728801589d`；通过ALGO-011 `property_test/HEUR-014/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_014_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_014.py::test_heur_014_sm` |

## TC-HEUR-014-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-014-IT-01` |
| 对应单元ID | `HEUR-014` — 出牌牌效与结构保留策略 |
| 父测试合同 | `T-HEUR-014-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `analyzed hand + legal discards`；向量引用`tests/spec_v3/vectors/heur_014.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3c777f4fd30b6d96`；通过ALGO-011 `property_test/HEUR-014/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_014_it`对应路径 |
| 预期输出 | 通过生产入口得到`strategic rank`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_014.py::test_heur_014_it` |

## TC-HEUR-014-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-014-RR-01` |
| 对应单元ID | `HEUR-014` — 出牌牌效与结构保留策略 |
| 父测试合同 | `T-HEUR-014-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `analyzed hand + legal discards`；向量引用`tests/spec_v3/vectors/heur_014.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb982071c604f519b`；通过ALGO-011 `property_test/HEUR-014/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_014.py::test_heur_014_rr` |

## TC-HEUR-014-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-014-SD-01` |
| 对应单元ID | `HEUR-014` — 出牌牌效与结构保留策略 |
| 父测试合同 | `T-HEUR-014-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `analyzed hand + legal discards`；向量引用`tests/spec_v3/vectors/heur_014.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd29fdbc7d734fe04`；通过ALGO-011 `property_test/HEUR-014/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_014.py::test_heur_014_sd` |

## TC-HEUR-014-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-014-PF-01` |
| 对应单元ID | `HEUR-014` — 出牌牌效与结构保留策略 |
| 父测试合同 | `T-HEUR-014-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `analyzed hand + legal discards`；向量引用`tests/spec_v3/vectors/heur_014.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x001880fb9b5ad0e0`；通过ALGO-011 `property_test/HEUR-014/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_014.py::test_heur_014_pf` |

## TC-HEUR-014-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-014-HL-01` |
| 对应单元ID | `HEUR-014` — 出牌牌效与结构保留策略 |
| 父测试合同 | `T-HEUR-014-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `analyzed hand + legal discards`；向量引用`tests/spec_v3/vectors/heur_014.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbe1b0f8b5e938a92`；通过ALGO-011 `property_test/HEUR-014/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_014.py::test_heur_014_hl` |

## TC-HEUR-015-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-015-UT-01` |
| 对应单元ID | `HEUR-015` — 防守偏好与安全牌选择 |
| 父测试合同 | `T-HEUR-015-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `per-seat risk + loss + profile`；向量引用`tests/spec_v3/vectors/heur_015.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x74d5a1a9058d3e3c`；通过ALGO-011 `property_test/HEUR-015/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_015_ut`对应路径 |
| 预期输出 | 返回批准schema的`defensive rank`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_015.py::test_heur_015_ut` |

## TC-HEUR-015-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-015-BD-01` |
| 对应单元ID | `HEUR-015` — 防守偏好与安全牌选择 |
| 父测试合同 | `T-HEUR-015-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `per-seat risk + loss + profile`；向量引用`tests/spec_v3/vectors/heur_015.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3d13f70a502c4604`；通过ALGO-011 `property_test/HEUR-015/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_015_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`defensive rank`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_015.py::test_heur_015_bd` |

## TC-HEUR-015-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-015-PT-01` |
| 对应单元ID | `HEUR-015` — 防守偏好与安全牌选择 |
| 父测试合同 | `T-HEUR-015-N01`、`T-HEUR-015-B01`、`T-HEUR-015-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `per-seat risk + loss + profile`；向量引用`tests/spec_v3/vectors/heur_015.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x392f110d9c37057e`；通过ALGO-011 `property_test/HEUR-015/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_015_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_015.py::test_heur_015_pt` |

## TC-HEUR-015-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-015-PB-01` |
| 对应单元ID | `HEUR-015` — 防守偏好与安全牌选择 |
| 父测试合同 | `T-HEUR-015-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `per-seat risk + loss + profile`；向量引用`tests/spec_v3/vectors/heur_015.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf8d0fab967d5b0c2`；通过ALGO-011 `property_test/HEUR-015/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_015.py::test_heur_015_pb` |

## TC-HEUR-015-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-015-SM-01` |
| 对应单元ID | `HEUR-015` — 防守偏好与安全牌选择 |
| 父测试合同 | `T-HEUR-015-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `per-seat risk + loss + profile`；向量引用`tests/spec_v3/vectors/heur_015.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1460133e0e3cfc7f`；通过ALGO-011 `property_test/HEUR-015/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_015_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_015.py::test_heur_015_sm` |

## TC-HEUR-015-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-015-IT-01` |
| 对应单元ID | `HEUR-015` — 防守偏好与安全牌选择 |
| 父测试合同 | `T-HEUR-015-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `per-seat risk + loss + profile`；向量引用`tests/spec_v3/vectors/heur_015.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x24c3ee180d6b1589`；通过ALGO-011 `property_test/HEUR-015/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_015_it`对应路径 |
| 预期输出 | 通过生产入口得到`defensive rank`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_015.py::test_heur_015_it` |

## TC-HEUR-015-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-015-RR-01` |
| 对应单元ID | `HEUR-015` — 防守偏好与安全牌选择 |
| 父测试合同 | `T-HEUR-015-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `per-seat risk + loss + profile`；向量引用`tests/spec_v3/vectors/heur_015.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7eb29d02b3a42427`；通过ALGO-011 `property_test/HEUR-015/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_015.py::test_heur_015_rr` |

## TC-HEUR-015-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-015-SD-01` |
| 对应单元ID | `HEUR-015` — 防守偏好与安全牌选择 |
| 父测试合同 | `T-HEUR-015-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `per-seat risk + loss + profile`；向量引用`tests/spec_v3/vectors/heur_015.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x070b23a6eadafbec`；通过ALGO-011 `property_test/HEUR-015/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_015.py::test_heur_015_sd` |

## TC-HEUR-015-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-015-PF-01` |
| 对应单元ID | `HEUR-015` — 防守偏好与安全牌选择 |
| 父测试合同 | `T-HEUR-015-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `per-seat risk + loss + profile`；向量引用`tests/spec_v3/vectors/heur_015.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x46736c2155984e8c`；通过ALGO-011 `property_test/HEUR-015/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_015.py::test_heur_015_pf` |

## TC-HEUR-015-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-015-HL-01` |
| 对应单元ID | `HEUR-015` — 防守偏好与安全牌选择 |
| 父测试合同 | `T-HEUR-015-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `per-seat risk + loss + profile`；向量引用`tests/spec_v3/vectors/heur_015.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x97c9f47b9955c2b2`；通过ALGO-011 `property_test/HEUR-015/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-015、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_015.py::test_heur_015_hl` |

## TC-HEUR-016-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-016-UT-01` |
| 对应单元ID | `HEUR-016` — 行为序列推断 |
| 父测试合同 | `T-HEUR-016-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `ordered public actions`；向量引用`tests/spec_v3/vectors/heur_016.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf98888b6bc642468`；通过ALGO-011 `property_test/HEUR-016/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_016_ut`对应路径 |
| 预期输出 | 返回批准schema的`behavioral cues`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_016.py::test_heur_016_ut` |

## TC-HEUR-016-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-016-BD-01` |
| 对应单元ID | `HEUR-016` — 行为序列推断 |
| 父测试合同 | `T-HEUR-016-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `ordered public actions`；向量引用`tests/spec_v3/vectors/heur_016.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa96e5f8adefe7aaa`；通过ALGO-011 `property_test/HEUR-016/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_016_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`behavioral cues`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_016.py::test_heur_016_bd` |

## TC-HEUR-016-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-016-PT-01` |
| 对应单元ID | `HEUR-016` — 行为序列推断 |
| 父测试合同 | `T-HEUR-016-N01`、`T-HEUR-016-B01`、`T-HEUR-016-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `ordered public actions`；向量引用`tests/spec_v3/vectors/heur_016.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe972a70612231ac3`；通过ALGO-011 `property_test/HEUR-016/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_016_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_016.py::test_heur_016_pt` |

## TC-HEUR-016-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-016-PB-01` |
| 对应单元ID | `HEUR-016` — 行为序列推断 |
| 父测试合同 | `T-HEUR-016-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `ordered public actions`；向量引用`tests/spec_v3/vectors/heur_016.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc866e3c6fb1472ff`；通过ALGO-011 `property_test/HEUR-016/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_016.py::test_heur_016_pb` |

## TC-HEUR-016-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-016-SM-01` |
| 对应单元ID | `HEUR-016` — 行为序列推断 |
| 父测试合同 | `T-HEUR-016-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `ordered public actions`；向量引用`tests/spec_v3/vectors/heur_016.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xba5c90a743d70a24`；通过ALGO-011 `property_test/HEUR-016/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_016_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_016.py::test_heur_016_sm` |

## TC-HEUR-016-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-016-IT-01` |
| 对应单元ID | `HEUR-016` — 行为序列推断 |
| 父测试合同 | `T-HEUR-016-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `ordered public actions`；向量引用`tests/spec_v3/vectors/heur_016.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x14046d72a770a1d3`；通过ALGO-011 `property_test/HEUR-016/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_016_it`对应路径 |
| 预期输出 | 通过生产入口得到`behavioral cues`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_016.py::test_heur_016_it` |

## TC-HEUR-016-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-016-RR-01` |
| 对应单元ID | `HEUR-016` — 行为序列推断 |
| 父测试合同 | `T-HEUR-016-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `ordered public actions`；向量引用`tests/spec_v3/vectors/heur_016.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4236b9934b6d31b7`；通过ALGO-011 `property_test/HEUR-016/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_016.py::test_heur_016_rr` |

## TC-HEUR-016-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-016-SD-01` |
| 对应单元ID | `HEUR-016` — 行为序列推断 |
| 父测试合同 | `T-HEUR-016-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `ordered public actions`；向量引用`tests/spec_v3/vectors/heur_016.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x765cd81ced0b3d0b`；通过ALGO-011 `property_test/HEUR-016/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_016.py::test_heur_016_sd` |

## TC-HEUR-016-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-016-PF-01` |
| 对应单元ID | `HEUR-016` — 行为序列推断 |
| 父测试合同 | `T-HEUR-016-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `ordered public actions`；向量引用`tests/spec_v3/vectors/heur_016.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x34c40abe043e6ab3`；通过ALGO-011 `property_test/HEUR-016/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_016.py::test_heur_016_pf` |

## TC-HEUR-016-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-016-HL-01` |
| 对应单元ID | `HEUR-016` — 行为序列推断 |
| 父测试合同 | `T-HEUR-016-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `ordered public actions`；向量引用`tests/spec_v3/vectors/heur_016.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8551f3bb2b386375`；通过ALGO-011 `property_test/HEUR-016/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-016、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_016.py::test_heur_016_hl` |

## TC-HEUR-017-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-017-UT-01` |
| 对应单元ID | `HEUR-017` — 思考节奏生成 |
| 父测试合同 | `T-HEUR-017-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `complexity + profile + deadline`；向量引用`tests/spec_v3/vectors/heur_017.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc725de241ea87d80`；通过ALGO-011 `property_test/HEUR-017/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_017_ut`对应路径 |
| 预期输出 | 返回批准schema的`planned think time`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-017、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_017.py::test_heur_017_ut` |

## TC-HEUR-017-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-017-BD-01` |
| 对应单元ID | `HEUR-017` — 思考节奏生成 |
| 父测试合同 | `T-HEUR-017-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `complexity + profile + deadline`；向量引用`tests/spec_v3/vectors/heur_017.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcf360d9d5c7400fd`；通过ALGO-011 `property_test/HEUR-017/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_017_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`planned think time`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-017、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_017.py::test_heur_017_bd` |

## TC-HEUR-017-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-017-PT-01` |
| 对应单元ID | `HEUR-017` — 思考节奏生成 |
| 父测试合同 | `T-HEUR-017-N01`、`T-HEUR-017-B01`、`T-HEUR-017-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `complexity + profile + deadline`；向量引用`tests/spec_v3/vectors/heur_017.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xae25af467eb58998`；通过ALGO-011 `property_test/HEUR-017/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_017_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-017、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_017.py::test_heur_017_pt` |

## TC-HEUR-017-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-017-PB-01` |
| 对应单元ID | `HEUR-017` — 思考节奏生成 |
| 父测试合同 | `T-HEUR-017-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `complexity + profile + deadline`；向量引用`tests/spec_v3/vectors/heur_017.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x342f73032971fe69`；通过ALGO-011 `property_test/HEUR-017/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-017、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_017.py::test_heur_017_pb` |

## TC-HEUR-017-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-017-SM-01` |
| 对应单元ID | `HEUR-017` — 思考节奏生成 |
| 父测试合同 | `T-HEUR-017-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `complexity + profile + deadline`；向量引用`tests/spec_v3/vectors/heur_017.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8993ca65b8cd0adc`；通过ALGO-011 `property_test/HEUR-017/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_017_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-017、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_017.py::test_heur_017_sm` |

## TC-HEUR-017-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-017-IT-01` |
| 对应单元ID | `HEUR-017` — 思考节奏生成 |
| 父测试合同 | `T-HEUR-017-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `complexity + profile + deadline`；向量引用`tests/spec_v3/vectors/heur_017.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x08161ee4f6237375`；通过ALGO-011 `property_test/HEUR-017/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_017_it`对应路径 |
| 预期输出 | 通过生产入口得到`planned think time`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-017、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_017.py::test_heur_017_it` |

## TC-HEUR-017-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-017-RR-01` |
| 对应单元ID | `HEUR-017` — 思考节奏生成 |
| 父测试合同 | `T-HEUR-017-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `complexity + profile + deadline`；向量引用`tests/spec_v3/vectors/heur_017.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x473a3325a5da8e05`；通过ALGO-011 `property_test/HEUR-017/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-017、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_017.py::test_heur_017_rr` |

## TC-HEUR-017-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-017-SD-01` |
| 对应单元ID | `HEUR-017` — 思考节奏生成 |
| 父测试合同 | `T-HEUR-017-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `complexity + profile + deadline`；向量引用`tests/spec_v3/vectors/heur_017.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdac66bec85ab235e`；通过ALGO-011 `property_test/HEUR-017/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-017、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_017.py::test_heur_017_sd` |

## TC-HEUR-017-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-017-PF-01` |
| 对应单元ID | `HEUR-017` — 思考节奏生成 |
| 父测试合同 | `T-HEUR-017-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `complexity + profile + deadline`；向量引用`tests/spec_v3/vectors/heur_017.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcea7934344ff0a3d`；通过ALGO-011 `property_test/HEUR-017/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-017、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_017.py::test_heur_017_pf` |

## TC-HEUR-017-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-017-HL-01` |
| 对应单元ID | `HEUR-017` — 思考节奏生成 |
| 父测试合同 | `T-HEUR-017-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `complexity + profile + deadline`；向量引用`tests/spec_v3/vectors/heur_017.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x29fd6a95542966b0`；通过ALGO-011 `property_test/HEUR-017/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-017、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_017.py::test_heur_017_hl` |

## TC-HEUR-018-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-018-UT-01` |
| 对应单元ID | `HEUR-018` — 安全牌储备、扣牌与信息表达 |
| 父测试合同 | `T-HEUR-018-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand/public threats/self exposure`；向量引用`tests/spec_v3/vectors/heur_018.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xba1c427771392b51`；通过ALGO-011 `property_test/HEUR-018/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_018_ut`对应路径 |
| 预期输出 | 返回批准schema的`retention preference`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-018、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_018.py::test_heur_018_ut` |

## TC-HEUR-018-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-018-BD-01` |
| 对应单元ID | `HEUR-018` — 安全牌储备、扣牌与信息表达 |
| 父测试合同 | `T-HEUR-018-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand/public threats/self exposure`；向量引用`tests/spec_v3/vectors/heur_018.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0b877a6a43f8c00a`；通过ALGO-011 `property_test/HEUR-018/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_018_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`retention preference`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-018、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_018.py::test_heur_018_bd` |

## TC-HEUR-018-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-018-PT-01` |
| 对应单元ID | `HEUR-018` — 安全牌储备、扣牌与信息表达 |
| 父测试合同 | `T-HEUR-018-N01`、`T-HEUR-018-B01`、`T-HEUR-018-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand/public threats/self exposure`；向量引用`tests/spec_v3/vectors/heur_018.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa1844faa725c04da`；通过ALGO-011 `property_test/HEUR-018/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_018_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-018、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_018.py::test_heur_018_pt` |

## TC-HEUR-018-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-018-PB-01` |
| 对应单元ID | `HEUR-018` — 安全牌储备、扣牌与信息表达 |
| 父测试合同 | `T-HEUR-018-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand/public threats/self exposure`；向量引用`tests/spec_v3/vectors/heur_018.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe05173605031b0db`；通过ALGO-011 `property_test/HEUR-018/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-018、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_018.py::test_heur_018_pb` |

## TC-HEUR-018-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-018-SM-01` |
| 对应单元ID | `HEUR-018` — 安全牌储备、扣牌与信息表达 |
| 父测试合同 | `T-HEUR-018-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `hand/public threats/self exposure`；向量引用`tests/spec_v3/vectors/heur_018.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3ef84b4cf596f10b`；通过ALGO-011 `property_test/HEUR-018/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_018_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-018、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_018.py::test_heur_018_sm` |

## TC-HEUR-018-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-018-IT-01` |
| 对应单元ID | `HEUR-018` — 安全牌储备、扣牌与信息表达 |
| 父测试合同 | `T-HEUR-018-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `hand/public threats/self exposure`；向量引用`tests/spec_v3/vectors/heur_018.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6e4507c1fd958698`；通过ALGO-011 `property_test/HEUR-018/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_018_it`对应路径 |
| 预期输出 | 通过生产入口得到`retention preference`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-018、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_018.py::test_heur_018_it` |

## TC-HEUR-018-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-018-RR-01` |
| 对应单元ID | `HEUR-018` — 安全牌储备、扣牌与信息表达 |
| 父测试合同 | `T-HEUR-018-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand/public threats/self exposure`；向量引用`tests/spec_v3/vectors/heur_018.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3801405dd2491945`；通过ALGO-011 `property_test/HEUR-018/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-018、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_018.py::test_heur_018_rr` |

## TC-HEUR-018-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-018-SD-01` |
| 对应单元ID | `HEUR-018` — 安全牌储备、扣牌与信息表达 |
| 父测试合同 | `T-HEUR-018-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand/public threats/self exposure`；向量引用`tests/spec_v3/vectors/heur_018.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0fa05287ceeee126`；通过ALGO-011 `property_test/HEUR-018/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-018、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_018.py::test_heur_018_sd` |

## TC-HEUR-018-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-018-PF-01` |
| 对应单元ID | `HEUR-018` — 安全牌储备、扣牌与信息表达 |
| 父测试合同 | `T-HEUR-018-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `hand/public threats/self exposure`；向量引用`tests/spec_v3/vectors/heur_018.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7ed629f0bb5c1a33`；通过ALGO-011 `property_test/HEUR-018/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-018、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_018.py::test_heur_018_pf` |

## TC-HEUR-018-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-018-HL-01` |
| 对应单元ID | `HEUR-018` — 安全牌储备、扣牌与信息表达 |
| 父测试合同 | `T-HEUR-018-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `hand/public threats/self exposure`；向量引用`tests/spec_v3/vectors/heur_018.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x893839884b0ce8bd`；通过ALGO-011 `property_test/HEUR-018/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-018、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_018.py::test_heur_018_hl` |

## TC-HEUR-019-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-019-UT-01` |
| 对应单元ID | `HEUR-019` — Top-K 有限注意分配 |
| 父测试合同 | `T-HEUR-019-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible cues + capacity`；向量引用`tests/spec_v3/vectors/heur_019.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9e99eef663da056c`；通过ALGO-011 `property_test/HEUR-019/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_019_ut`对应路径 |
| 预期输出 | 返回批准schema的`attended items`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-019、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_019.py::test_heur_019_ut` |

## TC-HEUR-019-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-019-BD-01` |
| 对应单元ID | `HEUR-019` — Top-K 有限注意分配 |
| 父测试合同 | `T-HEUR-019-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible cues + capacity`；向量引用`tests/spec_v3/vectors/heur_019.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5ae4b9d2aee3eceb`；通过ALGO-011 `property_test/HEUR-019/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_019_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`attended items`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-019、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_019.py::test_heur_019_bd` |

## TC-HEUR-019-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-019-PT-01` |
| 对应单元ID | `HEUR-019` — Top-K 有限注意分配 |
| 父测试合同 | `T-HEUR-019-N01`、`T-HEUR-019-B01`、`T-HEUR-019-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible cues + capacity`；向量引用`tests/spec_v3/vectors/heur_019.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x24586f8f17f448ee`；通过ALGO-011 `property_test/HEUR-019/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_019_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-019、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_019.py::test_heur_019_pt` |

## TC-HEUR-019-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-019-PB-01` |
| 对应单元ID | `HEUR-019` — Top-K 有限注意分配 |
| 父测试合同 | `T-HEUR-019-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible cues + capacity`；向量引用`tests/spec_v3/vectors/heur_019.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x54296f1d8df807a4`；通过ALGO-011 `property_test/HEUR-019/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-019、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_019.py::test_heur_019_pb` |

## TC-HEUR-019-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-019-SM-01` |
| 对应单元ID | `HEUR-019` — Top-K 有限注意分配 |
| 父测试合同 | `T-HEUR-019-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `visible cues + capacity`；向量引用`tests/spec_v3/vectors/heur_019.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x865b7475d61ff75f`；通过ALGO-011 `property_test/HEUR-019/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_019_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-019、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_019.py::test_heur_019_sm` |

## TC-HEUR-019-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-019-IT-01` |
| 对应单元ID | `HEUR-019` — Top-K 有限注意分配 |
| 父测试合同 | `T-HEUR-019-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `visible cues + capacity`；向量引用`tests/spec_v3/vectors/heur_019.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6ccf365ba8abb9ff`；通过ALGO-011 `property_test/HEUR-019/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_019_it`对应路径 |
| 预期输出 | 通过生产入口得到`attended items`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-019、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_019.py::test_heur_019_it` |

## TC-HEUR-019-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-019-RR-01` |
| 对应单元ID | `HEUR-019` — Top-K 有限注意分配 |
| 父测试合同 | `T-HEUR-019-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible cues + capacity`；向量引用`tests/spec_v3/vectors/heur_019.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd7abfceb7150d0e6`；通过ALGO-011 `property_test/HEUR-019/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-019、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_019.py::test_heur_019_rr` |

## TC-HEUR-019-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-019-SD-01` |
| 对应单元ID | `HEUR-019` — Top-K 有限注意分配 |
| 父测试合同 | `T-HEUR-019-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible cues + capacity`；向量引用`tests/spec_v3/vectors/heur_019.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd1fd17b8c6b4561c`；通过ALGO-011 `property_test/HEUR-019/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-019、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_019.py::test_heur_019_sd` |

## TC-HEUR-019-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-019-PF-01` |
| 对应单元ID | `HEUR-019` — Top-K 有限注意分配 |
| 父测试合同 | `T-HEUR-019-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible cues + capacity`；向量引用`tests/spec_v3/vectors/heur_019.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5e4ed5ab2f8994fa`；通过ALGO-011 `property_test/HEUR-019/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-019、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_019.py::test_heur_019_pf` |

## TC-HEUR-019-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-019-HL-01` |
| 对应单元ID | `HEUR-019` — Top-K 有限注意分配 |
| 父测试合同 | `T-HEUR-019-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `visible cues + capacity`；向量引用`tests/spec_v3/vectors/heur_019.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb1be0583dd7c95d4`；通过ALGO-011 `property_test/HEUR-019/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-019、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_019.py::test_heur_019_hl` |

## TC-HEUR-020-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-020-UT-01` |
| 对应单元ID | `HEUR-020` — 有界记忆衰减与强化 |
| 父测试合同 | `T-HEUR-020-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible events + memory config`；向量引用`tests/spec_v3/vectors/heur_020.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x78c7818299182f06`；通过ALGO-011 `property_test/HEUR-020/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_020_ut`对应路径 |
| 预期输出 | 返回批准schema的`memory snapshot`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-020、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_020.py::test_heur_020_ut` |

## TC-HEUR-020-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-020-BD-01` |
| 对应单元ID | `HEUR-020` — 有界记忆衰减与强化 |
| 父测试合同 | `T-HEUR-020-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible events + memory config`；向量引用`tests/spec_v3/vectors/heur_020.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x035e411b0ec7c068`；通过ALGO-011 `property_test/HEUR-020/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_020_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`memory snapshot`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-020、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_020.py::test_heur_020_bd` |

## TC-HEUR-020-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-020-PT-01` |
| 对应单元ID | `HEUR-020` — 有界记忆衰减与强化 |
| 父测试合同 | `T-HEUR-020-N01`、`T-HEUR-020-B01`、`T-HEUR-020-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible events + memory config`；向量引用`tests/spec_v3/vectors/heur_020.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf662f34a4d074cd6`；通过ALGO-011 `property_test/HEUR-020/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_020_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-020、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_020.py::test_heur_020_pt` |

## TC-HEUR-020-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-020-PB-01` |
| 对应单元ID | `HEUR-020` — 有界记忆衰减与强化 |
| 父测试合同 | `T-HEUR-020-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible events + memory config`；向量引用`tests/spec_v3/vectors/heur_020.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa93500437418ffcd`；通过ALGO-011 `property_test/HEUR-020/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-020、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_020.py::test_heur_020_pb` |

## TC-HEUR-020-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-020-SM-01` |
| 对应单元ID | `HEUR-020` — 有界记忆衰减与强化 |
| 父测试合同 | `T-HEUR-020-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `visible events + memory config`；向量引用`tests/spec_v3/vectors/heur_020.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe8245a21bdbf284e`；通过ALGO-011 `property_test/HEUR-020/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_020_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-020、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_020.py::test_heur_020_sm` |

## TC-HEUR-020-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-020-IT-01` |
| 对应单元ID | `HEUR-020` — 有界记忆衰减与强化 |
| 父测试合同 | `T-HEUR-020-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `visible events + memory config`；向量引用`tests/spec_v3/vectors/heur_020.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4ec4a0bbaa4f4322`；通过ALGO-011 `property_test/HEUR-020/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_020_it`对应路径 |
| 预期输出 | 通过生产入口得到`memory snapshot`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-020、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_020.py::test_heur_020_it` |

## TC-HEUR-020-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-020-RR-01` |
| 对应单元ID | `HEUR-020` — 有界记忆衰减与强化 |
| 父测试合同 | `T-HEUR-020-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible events + memory config`；向量引用`tests/spec_v3/vectors/heur_020.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcdb4c014570ebcd7`；通过ALGO-011 `property_test/HEUR-020/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-020、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_020.py::test_heur_020_rr` |

## TC-HEUR-020-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-020-SD-01` |
| 对应单元ID | `HEUR-020` — 有界记忆衰减与强化 |
| 父测试合同 | `T-HEUR-020-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible events + memory config`；向量引用`tests/spec_v3/vectors/heur_020.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb5da5f9e559b2c16`；通过ALGO-011 `property_test/HEUR-020/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-020、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_020.py::test_heur_020_sd` |

## TC-HEUR-020-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-020-PF-01` |
| 对应单元ID | `HEUR-020` — 有界记忆衰减与强化 |
| 父测试合同 | `T-HEUR-020-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `visible events + memory config`；向量引用`tests/spec_v3/vectors/heur_020.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x256c9b91e8131c8f`；通过ALGO-011 `property_test/HEUR-020/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-020、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_020.py::test_heur_020_pf` |

## TC-HEUR-020-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-020-HL-01` |
| 对应单元ID | `HEUR-020` — 有界记忆衰减与强化 |
| 父测试合同 | `T-HEUR-020-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `visible events + memory config`；向量引用`tests/spec_v3/vectors/heur_020.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa18692d2dc1d5a32`；通过ALGO-011 `property_test/HEUR-020/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-020、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_020.py::test_heur_020_hl` |

## TC-HEUR-021-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-021-UT-01` |
| 对应单元ID | `HEUR-021` — 有限推演与满意停止 |
| 父测试合同 | `T-HEUR-021-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `candidates + budget/threshold`；向量引用`tests/spec_v3/vectors/heur_021.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x779862f0de53c0e8`；通过ALGO-011 `property_test/HEUR-021/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_021_ut`对应路径 |
| 预期输出 | 返回批准schema的`checked set/stop reason`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-021、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_021.py::test_heur_021_ut` |

## TC-HEUR-021-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-021-BD-01` |
| 对应单元ID | `HEUR-021` — 有限推演与满意停止 |
| 父测试合同 | `T-HEUR-021-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `candidates + budget/threshold`；向量引用`tests/spec_v3/vectors/heur_021.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4a1be32fe1333f15`；通过ALGO-011 `property_test/HEUR-021/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_021_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`checked set/stop reason`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-021、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_021.py::test_heur_021_bd` |

## TC-HEUR-021-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-021-PT-01` |
| 对应单元ID | `HEUR-021` — 有限推演与满意停止 |
| 父测试合同 | `T-HEUR-021-N01`、`T-HEUR-021-B01`、`T-HEUR-021-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `candidates + budget/threshold`；向量引用`tests/spec_v3/vectors/heur_021.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x23477ad4ebd827d4`；通过ALGO-011 `property_test/HEUR-021/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_021_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-021、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_021.py::test_heur_021_pt` |

## TC-HEUR-021-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-021-PB-01` |
| 对应单元ID | `HEUR-021` — 有限推演与满意停止 |
| 父测试合同 | `T-HEUR-021-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `candidates + budget/threshold`；向量引用`tests/spec_v3/vectors/heur_021.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x64186b7a6f47637e`；通过ALGO-011 `property_test/HEUR-021/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-021、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_021.py::test_heur_021_pb` |

## TC-HEUR-021-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-021-SM-01` |
| 对应单元ID | `HEUR-021` — 有限推演与满意停止 |
| 父测试合同 | `T-HEUR-021-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `candidates + budget/threshold`；向量引用`tests/spec_v3/vectors/heur_021.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbf850e821c388e18`；通过ALGO-011 `property_test/HEUR-021/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_021_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-021、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_021.py::test_heur_021_sm` |

## TC-HEUR-021-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-021-IT-01` |
| 对应单元ID | `HEUR-021` — 有限推演与满意停止 |
| 父测试合同 | `T-HEUR-021-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `candidates + budget/threshold`；向量引用`tests/spec_v3/vectors/heur_021.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc51d70f5dd3207ca`；通过ALGO-011 `property_test/HEUR-021/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_021_it`对应路径 |
| 预期输出 | 通过生产入口得到`checked set/stop reason`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-021、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_021.py::test_heur_021_it` |

## TC-HEUR-021-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-021-RR-01` |
| 对应单元ID | `HEUR-021` — 有限推演与满意停止 |
| 父测试合同 | `T-HEUR-021-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `candidates + budget/threshold`；向量引用`tests/spec_v3/vectors/heur_021.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4584a1d094708708`；通过ALGO-011 `property_test/HEUR-021/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-021、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_021.py::test_heur_021_rr` |

## TC-HEUR-021-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-021-SD-01` |
| 对应单元ID | `HEUR-021` — 有限推演与满意停止 |
| 父测试合同 | `T-HEUR-021-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `candidates + budget/threshold`；向量引用`tests/spec_v3/vectors/heur_021.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x186a4b5aa4fa9e8e`；通过ALGO-011 `property_test/HEUR-021/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-021、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_021.py::test_heur_021_sd` |

## TC-HEUR-021-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-021-PF-01` |
| 对应单元ID | `HEUR-021` — 有限推演与满意停止 |
| 父测试合同 | `T-HEUR-021-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `candidates + budget/threshold`；向量引用`tests/spec_v3/vectors/heur_021.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8dca66dbafe93ed2`；通过ALGO-011 `property_test/HEUR-021/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-021、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_021.py::test_heur_021_pf` |

## TC-HEUR-021-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-021-HL-01` |
| 对应单元ID | `HEUR-021` — 有限推演与满意停止 |
| 父测试合同 | `T-HEUR-021-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `candidates + budget/threshold`；向量引用`tests/spec_v3/vectors/heur_021.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x73fe323de260345a`；通过ALGO-011 `property_test/HEUR-021/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-021、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_021.py::test_heur_021_hl` |

## TC-HEUR-022-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-022-UT-01` |
| 对应单元ID | `HEUR-022` — 人格、水平与情绪状态消费 |
| 父测试合同 | `T-HEUR-022-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + short state`；向量引用`tests/spec_v3/vectors/heur_022.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x11c5bf7450986769`；通过ALGO-011 `property_test/HEUR-022/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_022_ut`对应路径 |
| 预期输出 | 返回批准schema的`decision modifiers`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-022、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_022.py::test_heur_022_ut` |

## TC-HEUR-022-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-022-BD-01` |
| 对应单元ID | `HEUR-022` — 人格、水平与情绪状态消费 |
| 父测试合同 | `T-HEUR-022-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + short state`；向量引用`tests/spec_v3/vectors/heur_022.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc82f0e52d2330bda`；通过ALGO-011 `property_test/HEUR-022/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_022_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`decision modifiers`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-022、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_022.py::test_heur_022_bd` |

## TC-HEUR-022-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-022-PT-01` |
| 对应单元ID | `HEUR-022` — 人格、水平与情绪状态消费 |
| 父测试合同 | `T-HEUR-022-N01`、`T-HEUR-022-B01`、`T-HEUR-022-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + short state`；向量引用`tests/spec_v3/vectors/heur_022.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x49d3181b9beefe7d`；通过ALGO-011 `property_test/HEUR-022/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_022_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-022、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_022.py::test_heur_022_pt` |

## TC-HEUR-022-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-022-PB-01` |
| 对应单元ID | `HEUR-022` — 人格、水平与情绪状态消费 |
| 父测试合同 | `T-HEUR-022-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + short state`；向量引用`tests/spec_v3/vectors/heur_022.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3d44f96107a918a4`；通过ALGO-011 `property_test/HEUR-022/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-022、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_022.py::test_heur_022_pb` |

## TC-HEUR-022-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-022-SM-01` |
| 对应单元ID | `HEUR-022` — 人格、水平与情绪状态消费 |
| 父测试合同 | `T-HEUR-022-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `profile + short state`；向量引用`tests/spec_v3/vectors/heur_022.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x79fbb0535afd1bf5`；通过ALGO-011 `property_test/HEUR-022/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_022_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-022、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_022.py::test_heur_022_sm` |

## TC-HEUR-022-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-022-IT-01` |
| 对应单元ID | `HEUR-022` — 人格、水平与情绪状态消费 |
| 父测试合同 | `T-HEUR-022-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `profile + short state`；向量引用`tests/spec_v3/vectors/heur_022.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4ca42d7ccdbee83e`；通过ALGO-011 `property_test/HEUR-022/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_022_it`对应路径 |
| 预期输出 | 通过生产入口得到`decision modifiers`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-022、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_022.py::test_heur_022_it` |

## TC-HEUR-022-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-022-RR-01` |
| 对应单元ID | `HEUR-022` — 人格、水平与情绪状态消费 |
| 父测试合同 | `T-HEUR-022-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + short state`；向量引用`tests/spec_v3/vectors/heur_022.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5c5816014279329b`；通过ALGO-011 `property_test/HEUR-022/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-022、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_022.py::test_heur_022_rr` |

## TC-HEUR-022-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-022-SD-01` |
| 对应单元ID | `HEUR-022` — 人格、水平与情绪状态消费 |
| 父测试合同 | `T-HEUR-022-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + short state`；向量引用`tests/spec_v3/vectors/heur_022.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3f75acd3d56e0e4b`；通过ALGO-011 `property_test/HEUR-022/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-022、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_022.py::test_heur_022_sd` |

## TC-HEUR-022-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-022-PF-01` |
| 对应单元ID | `HEUR-022` — 人格、水平与情绪状态消费 |
| 父测试合同 | `T-HEUR-022-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `profile + short state`；向量引用`tests/spec_v3/vectors/heur_022.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2f3c71ee0285292b`；通过ALGO-011 `property_test/HEUR-022/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-022、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_022.py::test_heur_022_pf` |

## TC-HEUR-022-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-022-HL-01` |
| 对应单元ID | `HEUR-022` — 人格、水平与情绪状态消费 |
| 父测试合同 | `T-HEUR-022-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `profile + short state`；向量引用`tests/spec_v3/vectors/heur_022.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x418010cb07686ff6`；通过ALGO-011 `property_test/HEUR-022/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-022、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_022.py::test_heur_022_hl` |

## TC-HEUR-023-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-023-UT-01` |
| 对应单元ID | `HEUR-023` — 有界近似选择与人类失误 |
| 父测试合同 | `T-HEUR-023-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `checked candidates + bounded noise`；向量引用`tests/spec_v3/vectors/heur_023.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8fa7dc7b376d6a8d`；通过ALGO-011 `property_test/HEUR-023/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_023_ut`对应路径 |
| 预期输出 | 返回批准schema的`chosen legal action`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-023、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_023.py::test_heur_023_ut` |

## TC-HEUR-023-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-023-BD-01` |
| 对应单元ID | `HEUR-023` — 有界近似选择与人类失误 |
| 父测试合同 | `T-HEUR-023-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `checked candidates + bounded noise`；向量引用`tests/spec_v3/vectors/heur_023.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xacaaab23e5323ca1`；通过ALGO-011 `property_test/HEUR-023/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_023_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`chosen legal action`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-023、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_023.py::test_heur_023_bd` |

## TC-HEUR-023-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-023-PT-01` |
| 对应单元ID | `HEUR-023` — 有界近似选择与人类失误 |
| 父测试合同 | `T-HEUR-023-N01`、`T-HEUR-023-B01`、`T-HEUR-023-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `checked candidates + bounded noise`；向量引用`tests/spec_v3/vectors/heur_023.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7713eb4829d45283`；通过ALGO-011 `property_test/HEUR-023/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_023_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-023、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_023.py::test_heur_023_pt` |

## TC-HEUR-023-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-023-PB-01` |
| 对应单元ID | `HEUR-023` — 有界近似选择与人类失误 |
| 父测试合同 | `T-HEUR-023-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `checked candidates + bounded noise`；向量引用`tests/spec_v3/vectors/heur_023.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x46489a9ecd8b77db`；通过ALGO-011 `property_test/HEUR-023/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-023、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_023.py::test_heur_023_pb` |

## TC-HEUR-023-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-023-SM-01` |
| 对应单元ID | `HEUR-023` — 有界近似选择与人类失误 |
| 父测试合同 | `T-HEUR-023-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `checked candidates + bounded noise`；向量引用`tests/spec_v3/vectors/heur_023.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb0ff12c03202d927`；通过ALGO-011 `property_test/HEUR-023/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_023_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-023、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_023.py::test_heur_023_sm` |

## TC-HEUR-023-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-023-IT-01` |
| 对应单元ID | `HEUR-023` — 有界近似选择与人类失误 |
| 父测试合同 | `T-HEUR-023-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `checked candidates + bounded noise`；向量引用`tests/spec_v3/vectors/heur_023.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe40a3a274d30f131`；通过ALGO-011 `property_test/HEUR-023/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_heur_023_it`对应路径 |
| 预期输出 | 通过生产入口得到`chosen legal action`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=HEUR-023、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_023.py::test_heur_023_it` |

## TC-HEUR-023-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-023-RR-01` |
| 对应单元ID | `HEUR-023` — 有界近似选择与人类失误 |
| 父测试合同 | `T-HEUR-023-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `checked candidates + bounded noise`；向量引用`tests/spec_v3/vectors/heur_023.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x162cf2757d7ea00b`；通过ALGO-011 `property_test/HEUR-023/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=HEUR-023、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_heur_023.py::test_heur_023_rr` |

## TC-HEUR-023-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-023-SD-01` |
| 对应单元ID | `HEUR-023` — 有界近似选择与人类失误 |
| 父测试合同 | `T-HEUR-023-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `checked candidates + bounded noise`；向量引用`tests/spec_v3/vectors/heur_023.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdfd9a42312a8ddaf`；通过ALGO-011 `property_test/HEUR-023/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-023、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_heur_023.py::test_heur_023_sd` |

## TC-HEUR-023-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-023-PF-01` |
| 对应单元ID | `HEUR-023` — 有界近似选择与人类失误 |
| 父测试合同 | `T-HEUR-023-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `checked candidates + bounded noise`；向量引用`tests/spec_v3/vectors/heur_023.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xda596e0d3e55d6be`；通过ALGO-011 `property_test/HEUR-023/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-023、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_heur_023.py::test_heur_023_pf` |

## TC-HEUR-023-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-HEUR-023-HL-01` |
| 对应单元ID | `HEUR-023` — 有界近似选择与人类失误 |
| 父测试合同 | `T-HEUR-023-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `checked candidates + bounded noise`；向量引用`tests/spec_v3/vectors/heur_023.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd1d08b24be456b18`；通过ALGO-011 `property_test/HEUR-023/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=HEUR-023、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_heur_023.py::test_heur_023_hl` |

## TC-MODEL-001-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-001-UT-01` |
| 对应单元ID | `MODEL-001` — 逐对手归一化方向/牌型假设 |
| 父测试合同 | `T-MODEL-001-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + prior`；向量引用`tests/spec_v3/vectors/model_001.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x94b28a56746df5f8`；通过ALGO-011 `property_test/MODEL-001/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_001_ut`对应路径 |
| 预期输出 | 返回批准schema的`posterior hypotheses`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_001.py::test_model_001_ut` |

## TC-MODEL-001-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-001-BD-01` |
| 对应单元ID | `MODEL-001` — 逐对手归一化方向/牌型假设 |
| 父测试合同 | `T-MODEL-001-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + prior`；向量引用`tests/spec_v3/vectors/model_001.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x14a22033f464dd94`；通过ALGO-011 `property_test/MODEL-001/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_001_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`posterior hypotheses`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_001.py::test_model_001_bd` |

## TC-MODEL-001-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-001-PT-01` |
| 对应单元ID | `MODEL-001` — 逐对手归一化方向/牌型假设 |
| 父测试合同 | `T-MODEL-001-N01`、`T-MODEL-001-B01`、`T-MODEL-001-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + prior`；向量引用`tests/spec_v3/vectors/model_001.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc88e25ce06c6651a`；通过ALGO-011 `property_test/MODEL-001/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_001_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_001.py::test_model_001_pt` |

## TC-MODEL-001-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-001-PB-01` |
| 对应单元ID | `MODEL-001` — 逐对手归一化方向/牌型假设 |
| 父测试合同 | `T-MODEL-001-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + prior`；向量引用`tests/spec_v3/vectors/model_001.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x95b9bd9408b5246b`；通过ALGO-011 `property_test/MODEL-001/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_001.py::test_model_001_pb` |

## TC-MODEL-001-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-001-IT-01` |
| 对应单元ID | `MODEL-001` — 逐对手归一化方向/牌型假设 |
| 父测试合同 | `T-MODEL-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `public evidence + prior`；向量引用`tests/spec_v3/vectors/model_001.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x86eee612ca0877fd`；通过ALGO-011 `property_test/MODEL-001/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_001_it`对应路径 |
| 预期输出 | 通过生产入口得到`posterior hypotheses`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=MODEL-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_001.py::test_model_001_it` |

## TC-MODEL-001-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-001-RR-01` |
| 对应单元ID | `MODEL-001` — 逐对手归一化方向/牌型假设 |
| 父测试合同 | `T-MODEL-001-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + prior`；向量引用`tests/spec_v3/vectors/model_001.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb15c1ddbf14ab236`；通过ALGO-011 `property_test/MODEL-001/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=MODEL-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_001.py::test_model_001_rr` |

## TC-MODEL-001-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-001-SD-01` |
| 对应单元ID | `MODEL-001` — 逐对手归一化方向/牌型假设 |
| 父测试合同 | `T-MODEL-001-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + prior`；向量引用`tests/spec_v3/vectors/model_001.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6cfb79e4a2f183b1`；通过ALGO-011 `property_test/MODEL-001/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_model_001.py::test_model_001_sd` |

## TC-MODEL-001-MC-01 — 模型校准测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-001-MC-01` |
| 对应单元ID | `MODEL-001` — 逐对手归一化方向/牌型假设 |
| 父测试合同 | `T-MODEL-001-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + prior`；向量引用`tests/spec_v3/vectors/model_001.jsonl#case=mc01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xde3dee5a366d54e1`；通过ALGO-011 `property_test/MODEL-001/MC`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 在冻结牌局级测试切分推理，计算Brier/log loss/ECE和可靠性桶 |
| 预期输出 | 冻结切分上输出Brier/log loss/ECE/可靠性；达到Approved阈值并报告不确定性 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 只报准确率、ECE/Brier/log loss缺失、切分泄漏、阈值未达或回退不可用 |
| 自动化位置 | `tests/spec_v3/test_model_001.py::test_model_001_mc` |

## TC-MODEL-001-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-001-PF-01` |
| 对应单元ID | `MODEL-001` — 逐对手归一化方向/牌型假设 |
| 父测试合同 | `T-MODEL-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + prior`；向量引用`tests/spec_v3/vectors/model_001.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcd632a635285337e`；通过ALGO-011 `property_test/MODEL-001/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_model_001.py::test_model_001_pf` |

## TC-MODEL-001-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-001-HL-01` |
| 对应单元ID | `MODEL-001` — 逐对手归一化方向/牌型假设 |
| 父测试合同 | `T-MODEL-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `public evidence + prior`；向量引用`tests/spec_v3/vectors/model_001.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3ff1d944f86638aa`；通过ALGO-011 `property_test/MODEL-001/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_model_001.py::test_model_001_hl` |

## TC-MODEL-002-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-002-UT-01` |
| 对应单元ID | `MODEL-002` — 逐对手听牌/等待/损失风险模型 |
| 父测试合同 | `T-MODEL-002-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + hypotheses`；向量引用`tests/spec_v3/vectors/model_002.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xfb03a7aa67f6c4af`；通过ALGO-011 `property_test/MODEL-002/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_002_ut`对应路径 |
| 预期输出 | 返回批准schema的`risk distribution`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_002.py::test_model_002_ut` |

## TC-MODEL-002-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-002-BD-01` |
| 对应单元ID | `MODEL-002` — 逐对手听牌/等待/损失风险模型 |
| 父测试合同 | `T-MODEL-002-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + hypotheses`；向量引用`tests/spec_v3/vectors/model_002.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf3c60fc438d23afe`；通过ALGO-011 `property_test/MODEL-002/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_002_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`risk distribution`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_002.py::test_model_002_bd` |

## TC-MODEL-002-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-002-PT-01` |
| 对应单元ID | `MODEL-002` — 逐对手听牌/等待/损失风险模型 |
| 父测试合同 | `T-MODEL-002-N01`、`T-MODEL-002-B01`、`T-MODEL-002-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + hypotheses`；向量引用`tests/spec_v3/vectors/model_002.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xea9ab16ccbad417d`；通过ALGO-011 `property_test/MODEL-002/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_002_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_002.py::test_model_002_pt` |

## TC-MODEL-002-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-002-PB-01` |
| 对应单元ID | `MODEL-002` — 逐对手听牌/等待/损失风险模型 |
| 父测试合同 | `T-MODEL-002-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + hypotheses`；向量引用`tests/spec_v3/vectors/model_002.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x668e565338667553`；通过ALGO-011 `property_test/MODEL-002/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_002.py::test_model_002_pb` |

## TC-MODEL-002-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-002-IT-01` |
| 对应单元ID | `MODEL-002` — 逐对手听牌/等待/损失风险模型 |
| 父测试合同 | `T-MODEL-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `public evidence + hypotheses`；向量引用`tests/spec_v3/vectors/model_002.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf6ef9712a7aaf408`；通过ALGO-011 `property_test/MODEL-002/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_002_it`对应路径 |
| 预期输出 | 通过生产入口得到`risk distribution`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=MODEL-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_002.py::test_model_002_it` |

## TC-MODEL-002-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-002-RR-01` |
| 对应单元ID | `MODEL-002` — 逐对手听牌/等待/损失风险模型 |
| 父测试合同 | `T-MODEL-002-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + hypotheses`；向量引用`tests/spec_v3/vectors/model_002.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2f9e44fd9f193a4c`；通过ALGO-011 `property_test/MODEL-002/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=MODEL-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_002.py::test_model_002_rr` |

## TC-MODEL-002-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-002-SD-01` |
| 对应单元ID | `MODEL-002` — 逐对手听牌/等待/损失风险模型 |
| 父测试合同 | `T-MODEL-002-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + hypotheses`；向量引用`tests/spec_v3/vectors/model_002.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb71abdbc4ec6d6b3`；通过ALGO-011 `property_test/MODEL-002/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_model_002.py::test_model_002_sd` |

## TC-MODEL-002-MC-01 — 模型校准测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-002-MC-01` |
| 对应单元ID | `MODEL-002` — 逐对手听牌/等待/损失风险模型 |
| 父测试合同 | `T-MODEL-002-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + hypotheses`；向量引用`tests/spec_v3/vectors/model_002.jsonl#case=mc01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4fce89b2be8da2a7`；通过ALGO-011 `property_test/MODEL-002/MC`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 在冻结牌局级测试切分推理，计算Brier/log loss/ECE和可靠性桶 |
| 预期输出 | 冻结切分上输出Brier/log loss/ECE/可靠性；达到Approved阈值并报告不确定性 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 只报准确率、ECE/Brier/log loss缺失、切分泄漏、阈值未达或回退不可用 |
| 自动化位置 | `tests/spec_v3/test_model_002.py::test_model_002_mc` |

## TC-MODEL-002-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-002-PF-01` |
| 对应单元ID | `MODEL-002` — 逐对手听牌/等待/损失风险模型 |
| 父测试合同 | `T-MODEL-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `public evidence + hypotheses`；向量引用`tests/spec_v3/vectors/model_002.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x93978b4fec01692f`；通过ALGO-011 `property_test/MODEL-002/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_model_002.py::test_model_002_pf` |

## TC-MODEL-002-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-002-HL-01` |
| 对应单元ID | `MODEL-002` — 逐对手听牌/等待/损失风险模型 |
| 父测试合同 | `T-MODEL-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `public evidence + hypotheses`；向量引用`tests/spec_v3/vectors/model_002.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xecb76cd65175001b`；通过ALGO-011 `property_test/MODEL-002/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_model_002.py::test_model_002_hl` |

## TC-MODEL-003-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-003-UT-01` |
| 对应单元ID | `MODEL-003` — 仅公开信息的跨局对手画像学习 |
| 父测试合同 | `T-MODEL-003-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `match history + bounded state`；向量引用`tests/spec_v3/vectors/model_003.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x666b8e129b4d5342`；通过ALGO-011 `property_test/MODEL-003/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_003_ut`对应路径 |
| 预期输出 | 返回批准schema的`next profile`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_003.py::test_model_003_ut` |

## TC-MODEL-003-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-003-BD-01` |
| 对应单元ID | `MODEL-003` — 仅公开信息的跨局对手画像学习 |
| 父测试合同 | `T-MODEL-003-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `match history + bounded state`；向量引用`tests/spec_v3/vectors/model_003.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xec3897e8934caf85`；通过ALGO-011 `property_test/MODEL-003/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_003_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`next profile`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_003.py::test_model_003_bd` |

## TC-MODEL-003-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-003-PT-01` |
| 对应单元ID | `MODEL-003` — 仅公开信息的跨局对手画像学习 |
| 父测试合同 | `T-MODEL-003-N01`、`T-MODEL-003-B01`、`T-MODEL-003-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `match history + bounded state`；向量引用`tests/spec_v3/vectors/model_003.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xea5c647a90e379c2`；通过ALGO-011 `property_test/MODEL-003/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_003_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_003.py::test_model_003_pt` |

## TC-MODEL-003-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-003-PB-01` |
| 对应单元ID | `MODEL-003` — 仅公开信息的跨局对手画像学习 |
| 父测试合同 | `T-MODEL-003-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `match history + bounded state`；向量引用`tests/spec_v3/vectors/model_003.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x85c581ff42e460be`；通过ALGO-011 `property_test/MODEL-003/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_003.py::test_model_003_pb` |

## TC-MODEL-003-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-003-IT-01` |
| 对应单元ID | `MODEL-003` — 仅公开信息的跨局对手画像学习 |
| 父测试合同 | `T-MODEL-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `match history + bounded state`；向量引用`tests/spec_v3/vectors/model_003.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x40bd25c7eae31385`；通过ALGO-011 `property_test/MODEL-003/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_003_it`对应路径 |
| 预期输出 | 通过生产入口得到`next profile`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=MODEL-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_003.py::test_model_003_it` |

## TC-MODEL-003-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-003-RR-01` |
| 对应单元ID | `MODEL-003` — 仅公开信息的跨局对手画像学习 |
| 父测试合同 | `T-MODEL-003-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `match history + bounded state`；向量引用`tests/spec_v3/vectors/model_003.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa5ea154468a5cd45`；通过ALGO-011 `property_test/MODEL-003/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=MODEL-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_003.py::test_model_003_rr` |

## TC-MODEL-003-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-003-SD-01` |
| 对应单元ID | `MODEL-003` — 仅公开信息的跨局对手画像学习 |
| 父测试合同 | `T-MODEL-003-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `match history + bounded state`；向量引用`tests/spec_v3/vectors/model_003.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xac55cec25d422c7c`；通过ALGO-011 `property_test/MODEL-003/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_model_003.py::test_model_003_sd` |

## TC-MODEL-003-MC-01 — 模型校准测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-003-MC-01` |
| 对应单元ID | `MODEL-003` — 仅公开信息的跨局对手画像学习 |
| 父测试合同 | `T-MODEL-003-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `match history + bounded state`；向量引用`tests/spec_v3/vectors/model_003.jsonl#case=mc01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc2d7721f315a220b`；通过ALGO-011 `property_test/MODEL-003/MC`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 在冻结牌局级测试切分推理，计算Brier/log loss/ECE和可靠性桶 |
| 预期输出 | 冻结切分上输出Brier/log loss/ECE/可靠性；达到Approved阈值并报告不确定性 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 只报准确率、ECE/Brier/log loss缺失、切分泄漏、阈值未达或回退不可用 |
| 自动化位置 | `tests/spec_v3/test_model_003.py::test_model_003_mc` |

## TC-MODEL-003-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-003-PF-01` |
| 对应单元ID | `MODEL-003` — 仅公开信息的跨局对手画像学习 |
| 父测试合同 | `T-MODEL-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `match history + bounded state`；向量引用`tests/spec_v3/vectors/model_003.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe4206ef712e22a6e`；通过ALGO-011 `property_test/MODEL-003/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_model_003.py::test_model_003_pf` |

## TC-MODEL-003-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-003-HL-01` |
| 对应单元ID | `MODEL-003` — 仅公开信息的跨局对手画像学习 |
| 父测试合同 | `T-MODEL-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `match history + bounded state`；向量引用`tests/spec_v3/vectors/model_003.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbf6baf0a6a3ad556`；通过ALGO-011 `property_test/MODEL-003/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_model_003.py::test_model_003_hl` |

## TC-MODEL-004-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-004-UT-01` |
| 对应单元ID | `MODEL-004` — 可训练策略输入输出契约 |
| 父测试合同 | `T-MODEL-004-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observation + mask + parameters`；向量引用`tests/spec_v3/vectors/model_004.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8a49651ed0068ffb`；通过ALGO-011 `property_test/MODEL-004/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_004_ut`对应路径 |
| 预期输出 | 返回批准schema的`action distribution/value`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_004.py::test_model_004_ut` |

## TC-MODEL-004-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-004-BD-01` |
| 对应单元ID | `MODEL-004` — 可训练策略输入输出契约 |
| 父测试合同 | `T-MODEL-004-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observation + mask + parameters`；向量引用`tests/spec_v3/vectors/model_004.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x463390c0d8d32998`；通过ALGO-011 `property_test/MODEL-004/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_004_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`action distribution/value`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_004.py::test_model_004_bd` |

## TC-MODEL-004-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-004-PT-01` |
| 对应单元ID | `MODEL-004` — 可训练策略输入输出契约 |
| 父测试合同 | `T-MODEL-004-N01`、`T-MODEL-004-B01`、`T-MODEL-004-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observation + mask + parameters`；向量引用`tests/spec_v3/vectors/model_004.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x58b2ed74bb90c298`；通过ALGO-011 `property_test/MODEL-004/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_004_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_004.py::test_model_004_pt` |

## TC-MODEL-004-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-004-PB-01` |
| 对应单元ID | `MODEL-004` — 可训练策略输入输出契约 |
| 父测试合同 | `T-MODEL-004-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observation + mask + parameters`；向量引用`tests/spec_v3/vectors/model_004.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x120ae9fe0244735c`；通过ALGO-011 `property_test/MODEL-004/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_004.py::test_model_004_pb` |

## TC-MODEL-004-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-004-IT-01` |
| 对应单元ID | `MODEL-004` — 可训练策略输入输出契约 |
| 父测试合同 | `T-MODEL-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `observation + mask + parameters`；向量引用`tests/spec_v3/vectors/model_004.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa9b314ee2c84ae1a`；通过ALGO-011 `property_test/MODEL-004/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_004_it`对应路径 |
| 预期输出 | 通过生产入口得到`action distribution/value`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=MODEL-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_004.py::test_model_004_it` |

## TC-MODEL-004-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-004-RR-01` |
| 对应单元ID | `MODEL-004` — 可训练策略输入输出契约 |
| 父测试合同 | `T-MODEL-004-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observation + mask + parameters`；向量引用`tests/spec_v3/vectors/model_004.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa7f5d856d2896ac9`；通过ALGO-011 `property_test/MODEL-004/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=MODEL-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_004.py::test_model_004_rr` |

## TC-MODEL-004-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-004-SD-01` |
| 对应单元ID | `MODEL-004` — 可训练策略输入输出契约 |
| 父测试合同 | `T-MODEL-004-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observation + mask + parameters`；向量引用`tests/spec_v3/vectors/model_004.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x96d60f0c3869dc6c`；通过ALGO-011 `property_test/MODEL-004/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_model_004.py::test_model_004_sd` |

## TC-MODEL-004-MC-01 — 模型校准测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-004-MC-01` |
| 对应单元ID | `MODEL-004` — 可训练策略输入输出契约 |
| 父测试合同 | `T-MODEL-004-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observation + mask + parameters`；向量引用`tests/spec_v3/vectors/model_004.jsonl#case=mc01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0c63d32bb48c5517`；通过ALGO-011 `property_test/MODEL-004/MC`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 在冻结牌局级测试切分推理，计算Brier/log loss/ECE和可靠性桶 |
| 预期输出 | 冻结切分上输出Brier/log loss/ECE/可靠性；达到Approved阈值并报告不确定性 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 只报准确率、ECE/Brier/log loss缺失、切分泄漏、阈值未达或回退不可用 |
| 自动化位置 | `tests/spec_v3/test_model_004.py::test_model_004_mc` |

## TC-MODEL-004-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-004-PF-01` |
| 对应单元ID | `MODEL-004` — 可训练策略输入输出契约 |
| 父测试合同 | `T-MODEL-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `observation + mask + parameters`；向量引用`tests/spec_v3/vectors/model_004.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x05febb99cdb922a8`；通过ALGO-011 `property_test/MODEL-004/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_model_004.py::test_model_004_pf` |

## TC-MODEL-004-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-004-HL-01` |
| 对应单元ID | `MODEL-004` — 可训练策略输入输出契约 |
| 父测试合同 | `T-MODEL-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `observation + mask + parameters`；向量引用`tests/spec_v3/vectors/model_004.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x27803414f69dc3d6`；通过ALGO-011 `property_test/MODEL-004/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_model_004.py::test_model_004_hl` |

## TC-MODEL-005-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-005-UT-01` |
| 对应单元ID | `MODEL-005` — 训练模型产物版本、冻结和评估生命周期 |
| 父测试合同 | `T-MODEL-005-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `training run + data/config hashes`；向量引用`tests/spec_v3/vectors/model_005.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x54a4dc571b3fbd6d`；通过ALGO-011 `property_test/MODEL-005/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_005_ut`对应路径 |
| 预期输出 | 返回批准schema的`frozen model card/artifact`；正常向量与Approved oracle一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_005.py::test_model_005_ut` |

## TC-MODEL-005-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-005-BD-01` |
| 对应单元ID | `MODEL-005` — 训练模型产物版本、冻结和评估生命周期 |
| 父测试合同 | `T-MODEL-005-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `training run + data/config hashes`；向量引用`tests/spec_v3/vectors/model_005.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x62a69ae7d1a9ac50`；通过ALGO-011 `property_test/MODEL-005/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_005_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`frozen model card/artifact`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_005.py::test_model_005_bd` |

## TC-MODEL-005-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-005-PT-01` |
| 对应单元ID | `MODEL-005` — 训练模型产物版本、冻结和评估生命周期 |
| 父测试合同 | `T-MODEL-005-N01`、`T-MODEL-005-B01`、`T-MODEL-005-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `training run + data/config hashes`；向量引用`tests/spec_v3/vectors/model_005.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf6173fd7f4c05c1c`；通过ALGO-011 `property_test/MODEL-005/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_005_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_005.py::test_model_005_pt` |

## TC-MODEL-005-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-005-PB-01` |
| 对应单元ID | `MODEL-005` — 训练模型产物版本、冻结和评估生命周期 |
| 父测试合同 | `T-MODEL-005-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `training run + data/config hashes`；向量引用`tests/spec_v3/vectors/model_005.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8656ddd619bd3f1a`；通过ALGO-011 `property_test/MODEL-005/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_005.py::test_model_005_pb` |

## TC-MODEL-005-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-005-SM-01` |
| 对应单元ID | `MODEL-005` — 训练模型产物版本、冻结和评估生命周期 |
| 父测试合同 | `T-MODEL-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `training run + data/config hashes`；向量引用`tests/spec_v3/vectors/model_005.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x09c349628a987dea`；通过ALGO-011 `property_test/MODEL-005/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_005_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=MODEL-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_005.py::test_model_005_sm` |

## TC-MODEL-005-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-005-IT-01` |
| 对应单元ID | `MODEL-005` — 训练模型产物版本、冻结和评估生命周期 |
| 父测试合同 | `T-MODEL-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `training run + data/config hashes`；向量引用`tests/spec_v3/vectors/model_005.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x55f6cf2c7d4a1394`；通过ALGO-011 `property_test/MODEL-005/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_model_005_it`对应路径 |
| 预期输出 | 通过生产入口得到`frozen model card/artifact`，上下游schema/version/hash一致 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=MODEL-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_005.py::test_model_005_it` |

## TC-MODEL-005-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-005-RR-01` |
| 对应单元ID | `MODEL-005` — 训练模型产物版本、冻结和评估生命周期 |
| 父测试合同 | `T-MODEL-005-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `training run + data/config hashes`；向量引用`tests/spec_v3/vectors/model_005.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x24301bf70c129712`；通过ALGO-011 `property_test/MODEL-005/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=MODEL-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_model_005.py::test_model_005_rr` |

## TC-MODEL-005-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-005-SD-01` |
| 对应单元ID | `MODEL-005` — 训练模型产物版本、冻结和评估生命周期 |
| 父测试合同 | `T-MODEL-005-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `training run + data/config hashes`；向量引用`tests/spec_v3/vectors/model_005.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x325a893dccee9b91`；通过ALGO-011 `property_test/MODEL-005/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_model_005.py::test_model_005_sd` |

## TC-MODEL-005-MC-01 — 模型校准测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-005-MC-01` |
| 对应单元ID | `MODEL-005` — 训练模型产物版本、冻结和评估生命周期 |
| 父测试合同 | `T-MODEL-005-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `training run + data/config hashes`；向量引用`tests/spec_v3/vectors/model_005.jsonl#case=mc01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcb4f058fce6e95c1`；通过ALGO-011 `property_test/MODEL-005/MC`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 在冻结牌局级测试切分推理，计算Brier/log loss/ECE和可靠性桶 |
| 预期输出 | 冻结切分上输出Brier/log loss/ECE/可靠性；达到Approved阈值并报告不确定性 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 只报准确率、ECE/Brier/log loss缺失、切分泄漏、阈值未达或回退不可用 |
| 自动化位置 | `tests/spec_v3/test_model_005.py::test_model_005_mc` |

## TC-MODEL-005-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-005-PF-01` |
| 对应单元ID | `MODEL-005` — 训练模型产物版本、冻结和评估生命周期 |
| 父测试合同 | `T-MODEL-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用 |
| 输入 | `training run + data/config hashes`；向量引用`tests/spec_v3/vectors/model_005.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdfdaf151f2eb4ec3`；通过ALGO-011 `property_test/MODEL-005/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_model_005.py::test_model_005_pf` |

## TC-MODEL-005-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-MODEL-005-HL-01` |
| 对应单元ID | `MODEL-005` — 训练模型产物版本、冻结和评估生命周期 |
| 父测试合同 | `T-MODEL-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `training run + data/config hashes`；向量引用`tests/spec_v3/vectors/model_005.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd486bb2b5a5261cf`；通过ALGO-011 `property_test/MODEL-005/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=MODEL-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_model_005.py::test_model_005_hl` |

## TC-STATE-001-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-001-UT-01` |
| 对应单元ID | `STATE-001` — Match 配置冻结、玩家装配与整场控制 |
| 父测试合同 | `T-STATE-001-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `match request`；向量引用`tests/spec_v3/vectors/state_001.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6d2a573206484625`；通过ALGO-011 `property_test/STATE-001/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_001_ut`对应路径 |
| 预期输出 | 返回批准schema的`immutable match context`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_001.py::test_state_001_ut` |

## TC-STATE-001-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-001-BD-01` |
| 对应单元ID | `STATE-001` — Match 配置冻结、玩家装配与整场控制 |
| 父测试合同 | `T-STATE-001-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `match request`；向量引用`tests/spec_v3/vectors/state_001.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd5c9582c96920a9c`；通过ALGO-011 `property_test/STATE-001/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_001_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`immutable match context`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_001.py::test_state_001_bd` |

## TC-STATE-001-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-001-PT-01` |
| 对应单元ID | `STATE-001` — Match 配置冻结、玩家装配与整场控制 |
| 父测试合同 | `T-STATE-001-N01`、`T-STATE-001-B01`、`T-STATE-001-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `match request`；向量引用`tests/spec_v3/vectors/state_001.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9f1d82c843d3dadf`；通过ALGO-011 `property_test/STATE-001/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_001_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_001.py::test_state_001_pt` |

## TC-STATE-001-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-001-PB-01` |
| 对应单元ID | `STATE-001` — Match 配置冻结、玩家装配与整场控制 |
| 父测试合同 | `T-STATE-001-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `match request`；向量引用`tests/spec_v3/vectors/state_001.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe1ef8c3a1d97eec2`；通过ALGO-011 `property_test/STATE-001/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_001.py::test_state_001_pb` |

## TC-STATE-001-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-001-SM-01` |
| 对应单元ID | `STATE-001` — Match 配置冻结、玩家装配与整场控制 |
| 父测试合同 | `T-STATE-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `match request`；向量引用`tests/spec_v3/vectors/state_001.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3a66d25360a46e39`；通过ALGO-011 `property_test/STATE-001/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_001_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_001.py::test_state_001_sm` |

## TC-STATE-001-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-001-IT-01` |
| 对应单元ID | `STATE-001` — Match 配置冻结、玩家装配与整场控制 |
| 父测试合同 | `T-STATE-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `match request`；向量引用`tests/spec_v3/vectors/state_001.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x97ae5281c60e3848`；通过ALGO-011 `property_test/STATE-001/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_001_it`对应路径 |
| 预期输出 | 通过生产入口得到`immutable match context`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_001.py::test_state_001_it` |

## TC-STATE-001-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-001-RR-01` |
| 对应单元ID | `STATE-001` — Match 配置冻结、玩家装配与整场控制 |
| 父测试合同 | `T-STATE-001-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `match request`；向量引用`tests/spec_v3/vectors/state_001.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x85b96e50d3dc3ef3`；通过ALGO-011 `property_test/STATE-001/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=STATE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_001.py::test_state_001_rr` |

## TC-STATE-001-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-001-PF-01` |
| 对应单元ID | `STATE-001` — Match 配置冻结、玩家装配与整场控制 |
| 父测试合同 | `T-STATE-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `match request`；向量引用`tests/spec_v3/vectors/state_001.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6f6b30317ba94974`；通过ALGO-011 `property_test/STATE-001/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_state_001.py::test_state_001_pf` |

## TC-STATE-001-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-001-HL-01` |
| 对应单元ID | `STATE-001` — Match 配置冻结、玩家装配与整场控制 |
| 父测试合同 | `T-STATE-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `match request`；向量引用`tests/spec_v3/vectors/state_001.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9a28b8a55fc1ce8e`；通过ALGO-011 `property_test/STATE-001/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_state_001.py::test_state_001_hl` |

## TC-STATE-002-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-002-UT-01` |
| 对应单元ID | `STATE-002` — 权威 RoundState 存储与授权访问 |
| 父测试合同 | `T-STATE-002-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `atomic events`；向量引用`tests/spec_v3/vectors/state_002.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa67a409dc94ddfa9`；通过ALGO-011 `property_test/STATE-002/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_002_ut`对应路径 |
| 预期输出 | 返回批准schema的`authoritative state`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_002.py::test_state_002_ut` |

## TC-STATE-002-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-002-BD-01` |
| 对应单元ID | `STATE-002` — 权威 RoundState 存储与授权访问 |
| 父测试合同 | `T-STATE-002-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `atomic events`；向量引用`tests/spec_v3/vectors/state_002.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf61f7df0867ec716`；通过ALGO-011 `property_test/STATE-002/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_002_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`authoritative state`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_002.py::test_state_002_bd` |

## TC-STATE-002-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-002-PT-01` |
| 对应单元ID | `STATE-002` — 权威 RoundState 存储与授权访问 |
| 父测试合同 | `T-STATE-002-N01`、`T-STATE-002-B01`、`T-STATE-002-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `atomic events`；向量引用`tests/spec_v3/vectors/state_002.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x07ad6abdcbffbf9a`；通过ALGO-011 `property_test/STATE-002/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_002_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_002.py::test_state_002_pt` |

## TC-STATE-002-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-002-PB-01` |
| 对应单元ID | `STATE-002` — 权威 RoundState 存储与授权访问 |
| 父测试合同 | `T-STATE-002-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `atomic events`；向量引用`tests/spec_v3/vectors/state_002.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd84c2f0b2915157e`；通过ALGO-011 `property_test/STATE-002/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_002.py::test_state_002_pb` |

## TC-STATE-002-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-002-SM-01` |
| 对应单元ID | `STATE-002` — 权威 RoundState 存储与授权访问 |
| 父测试合同 | `T-STATE-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `atomic events`；向量引用`tests/spec_v3/vectors/state_002.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0294b5f1add39ecb`；通过ALGO-011 `property_test/STATE-002/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_002_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_002.py::test_state_002_sm` |

## TC-STATE-002-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-002-IT-01` |
| 对应单元ID | `STATE-002` — 权威 RoundState 存储与授权访问 |
| 父测试合同 | `T-STATE-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `atomic events`；向量引用`tests/spec_v3/vectors/state_002.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x24a88aa58166fd27`；通过ALGO-011 `property_test/STATE-002/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_002_it`对应路径 |
| 预期输出 | 通过生产入口得到`authoritative state`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_002.py::test_state_002_it` |

## TC-STATE-002-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-002-RR-01` |
| 对应单元ID | `STATE-002` — 权威 RoundState 存储与授权访问 |
| 父测试合同 | `T-STATE-002-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `atomic events`；向量引用`tests/spec_v3/vectors/state_002.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe1ff0ea5905d0857`；通过ALGO-011 `property_test/STATE-002/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=STATE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_002.py::test_state_002_rr` |

## TC-STATE-002-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-002-PF-01` |
| 对应单元ID | `STATE-002` — 权威 RoundState 存储与授权访问 |
| 父测试合同 | `T-STATE-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `atomic events`；向量引用`tests/spec_v3/vectors/state_002.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0dd35819324e98fb`；通过ALGO-011 `property_test/STATE-002/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_state_002.py::test_state_002_pf` |

## TC-STATE-002-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-002-HL-01` |
| 对应单元ID | `STATE-002` — 权威 RoundState 存储与授权访问 |
| 父测试合同 | `T-STATE-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `atomic events`；向量引用`tests/spec_v3/vectors/state_002.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x71b7b8a1b3bfbebd`；通过ALGO-011 `property_test/STATE-002/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_state_002.py::test_state_002_hl` |

## TC-STATE-003-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-003-UT-01` |
| 对应单元ID | `STATE-003` — PlayerRoundState 手牌、副露、定缺与过胡状态 |
| 父测试合同 | `T-STATE-003-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `rule transitions`；向量引用`tests/spec_v3/vectors/state_003.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5e1f75520fd2397d`；通过ALGO-011 `property_test/STATE-003/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_003_ut`对应路径 |
| 预期输出 | 返回批准schema的`player state`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_003.py::test_state_003_ut` |

## TC-STATE-003-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-003-BD-01` |
| 对应单元ID | `STATE-003` — PlayerRoundState 手牌、副露、定缺与过胡状态 |
| 父测试合同 | `T-STATE-003-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `rule transitions`；向量引用`tests/spec_v3/vectors/state_003.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x72dbf6c5a2630a4d`；通过ALGO-011 `property_test/STATE-003/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_003_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`player state`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_003.py::test_state_003_bd` |

## TC-STATE-003-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-003-PT-01` |
| 对应单元ID | `STATE-003` — PlayerRoundState 手牌、副露、定缺与过胡状态 |
| 父测试合同 | `T-STATE-003-N01`、`T-STATE-003-B01`、`T-STATE-003-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `rule transitions`；向量引用`tests/spec_v3/vectors/state_003.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2469561779f3cff7`；通过ALGO-011 `property_test/STATE-003/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_003_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_003.py::test_state_003_pt` |

## TC-STATE-003-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-003-PB-01` |
| 对应单元ID | `STATE-003` — PlayerRoundState 手牌、副露、定缺与过胡状态 |
| 父测试合同 | `T-STATE-003-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `rule transitions`；向量引用`tests/spec_v3/vectors/state_003.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe9d976fd9363d6d9`；通过ALGO-011 `property_test/STATE-003/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_003.py::test_state_003_pb` |

## TC-STATE-003-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-003-SM-01` |
| 对应单元ID | `STATE-003` — PlayerRoundState 手牌、副露、定缺与过胡状态 |
| 父测试合同 | `T-STATE-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `rule transitions`；向量引用`tests/spec_v3/vectors/state_003.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6edda6463df1e5e9`；通过ALGO-011 `property_test/STATE-003/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_003_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_003.py::test_state_003_sm` |

## TC-STATE-003-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-003-IT-01` |
| 对应单元ID | `STATE-003` — PlayerRoundState 手牌、副露、定缺与过胡状态 |
| 父测试合同 | `T-STATE-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `rule transitions`；向量引用`tests/spec_v3/vectors/state_003.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x265a87e81965ebe6`；通过ALGO-011 `property_test/STATE-003/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_003_it`对应路径 |
| 预期输出 | 通过生产入口得到`player state`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_003.py::test_state_003_it` |

## TC-STATE-003-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-003-RR-01` |
| 对应单元ID | `STATE-003` — PlayerRoundState 手牌、副露、定缺与过胡状态 |
| 父测试合同 | `T-STATE-003-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `rule transitions`；向量引用`tests/spec_v3/vectors/state_003.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x63044dd59e57425a`；通过ALGO-011 `property_test/STATE-003/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=STATE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_003.py::test_state_003_rr` |

## TC-STATE-003-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-003-PF-01` |
| 对应单元ID | `STATE-003` — PlayerRoundState 手牌、副露、定缺与过胡状态 |
| 父测试合同 | `T-STATE-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `rule transitions`；向量引用`tests/spec_v3/vectors/state_003.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9a8c8145805ace44`；通过ALGO-011 `property_test/STATE-003/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_state_003.py::test_state_003_pf` |

## TC-STATE-003-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-003-HL-01` |
| 对应单元ID | `STATE-003` — PlayerRoundState 手牌、副露、定缺与过胡状态 |
| 父测试合同 | `T-STATE-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `rule transitions`；向量引用`tests/spec_v3/vectors/state_003.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xea7b963988c3294b`；通过ALGO-011 `property_test/STATE-003/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_state_003.py::test_state_003_hl` |

## TC-STATE-004-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-004-UT-01` |
| 对应单元ID | `STATE-004` — CONFIGURED→SETTLED 状态机 |
| 父测试合同 | `T-STATE-004-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `current phase + event`；向量引用`tests/spec_v3/vectors/state_004.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa90aa9d4f73054af`；通过ALGO-011 `property_test/STATE-004/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_004_ut`对应路径 |
| 预期输出 | 返回批准schema的`next phase or error`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_004.py::test_state_004_ut` |

## TC-STATE-004-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-004-BD-01` |
| 对应单元ID | `STATE-004` — CONFIGURED→SETTLED 状态机 |
| 父测试合同 | `T-STATE-004-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `current phase + event`；向量引用`tests/spec_v3/vectors/state_004.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x48130c5aa714a4e5`；通过ALGO-011 `property_test/STATE-004/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_004_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`next phase or error`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_004.py::test_state_004_bd` |

## TC-STATE-004-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-004-PT-01` |
| 对应单元ID | `STATE-004` — CONFIGURED→SETTLED 状态机 |
| 父测试合同 | `T-STATE-004-N01`、`T-STATE-004-B01`、`T-STATE-004-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `current phase + event`；向量引用`tests/spec_v3/vectors/state_004.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x86b8c72c367a4802`；通过ALGO-011 `property_test/STATE-004/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_004_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_004.py::test_state_004_pt` |

## TC-STATE-004-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-004-PB-01` |
| 对应单元ID | `STATE-004` — CONFIGURED→SETTLED 状态机 |
| 父测试合同 | `T-STATE-004-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `current phase + event`；向量引用`tests/spec_v3/vectors/state_004.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x16dc282733c59950`；通过ALGO-011 `property_test/STATE-004/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_004.py::test_state_004_pb` |

## TC-STATE-004-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-004-SM-01` |
| 对应单元ID | `STATE-004` — CONFIGURED→SETTLED 状态机 |
| 父测试合同 | `T-STATE-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `current phase + event`；向量引用`tests/spec_v3/vectors/state_004.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa4b554b43123d099`；通过ALGO-011 `property_test/STATE-004/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_004_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_004.py::test_state_004_sm` |

## TC-STATE-004-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-004-IT-01` |
| 对应单元ID | `STATE-004` — CONFIGURED→SETTLED 状态机 |
| 父测试合同 | `T-STATE-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `current phase + event`；向量引用`tests/spec_v3/vectors/state_004.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4619e70656bc863a`；通过ALGO-011 `property_test/STATE-004/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_004_it`对应路径 |
| 预期输出 | 通过生产入口得到`next phase or error`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_004.py::test_state_004_it` |

## TC-STATE-004-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-004-RR-01` |
| 对应单元ID | `STATE-004` — CONFIGURED→SETTLED 状态机 |
| 父测试合同 | `T-STATE-004-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `current phase + event`；向量引用`tests/spec_v3/vectors/state_004.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x889c2a58e4187760`；通过ALGO-011 `property_test/STATE-004/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=STATE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_004.py::test_state_004_rr` |

## TC-STATE-004-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-004-PF-01` |
| 对应单元ID | `STATE-004` — CONFIGURED→SETTLED 状态机 |
| 父测试合同 | `T-STATE-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `current phase + event`；向量引用`tests/spec_v3/vectors/state_004.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcab00cf94c8cfa39`；通过ALGO-011 `property_test/STATE-004/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_state_004.py::test_state_004_pf` |

## TC-STATE-004-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-004-HL-01` |
| 对应单元ID | `STATE-004` — CONFIGURED→SETTLED 状态机 |
| 父测试合同 | `T-STATE-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `current phase + event`；向量引用`tests/spec_v3/vectors/state_004.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x55f1e05e2bc8b221`；通过ALGO-011 `property_test/STATE-004/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_state_004.py::test_state_004_hl` |

## TC-STATE-005-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-005-UT-01` |
| 对应单元ID | `STATE-005` — 不可变 PlayerView 状态载体 |
| 父测试合同 | `T-STATE-005-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `builder output`；向量引用`tests/spec_v3/vectors/state_005.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x031dd2a5063a82a5`；通过ALGO-011 `property_test/STATE-005/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_005_ut`对应路径 |
| 预期输出 | 返回批准schema的`frozen seat view`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_005.py::test_state_005_ut` |

## TC-STATE-005-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-005-BD-01` |
| 对应单元ID | `STATE-005` — 不可变 PlayerView 状态载体 |
| 父测试合同 | `T-STATE-005-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `builder output`；向量引用`tests/spec_v3/vectors/state_005.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5c08c924f81f98ff`；通过ALGO-011 `property_test/STATE-005/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_005_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`frozen seat view`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_005.py::test_state_005_bd` |

## TC-STATE-005-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-005-PT-01` |
| 对应单元ID | `STATE-005` — 不可变 PlayerView 状态载体 |
| 父测试合同 | `T-STATE-005-N01`、`T-STATE-005-B01`、`T-STATE-005-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `builder output`；向量引用`tests/spec_v3/vectors/state_005.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf707a7c3ee80eb65`；通过ALGO-011 `property_test/STATE-005/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_005_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_005.py::test_state_005_pt` |

## TC-STATE-005-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-005-PB-01` |
| 对应单元ID | `STATE-005` — 不可变 PlayerView 状态载体 |
| 父测试合同 | `T-STATE-005-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `builder output`；向量引用`tests/spec_v3/vectors/state_005.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0d13ed1b11a2b4ec`；通过ALGO-011 `property_test/STATE-005/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_005.py::test_state_005_pb` |

## TC-STATE-005-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-005-SM-01` |
| 对应单元ID | `STATE-005` — 不可变 PlayerView 状态载体 |
| 父测试合同 | `T-STATE-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `builder output`；向量引用`tests/spec_v3/vectors/state_005.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x157ce661584d091f`；通过ALGO-011 `property_test/STATE-005/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_005_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_005.py::test_state_005_sm` |

## TC-STATE-005-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-005-IT-01` |
| 对应单元ID | `STATE-005` — 不可变 PlayerView 状态载体 |
| 父测试合同 | `T-STATE-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `builder output`；向量引用`tests/spec_v3/vectors/state_005.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3633e7e2764dfcfc`；通过ALGO-011 `property_test/STATE-005/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_005_it`对应路径 |
| 预期输出 | 通过生产入口得到`frozen seat view`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_005.py::test_state_005_it` |

## TC-STATE-005-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-005-RR-01` |
| 对应单元ID | `STATE-005` — 不可变 PlayerView 状态载体 |
| 父测试合同 | `T-STATE-005-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `builder output`；向量引用`tests/spec_v3/vectors/state_005.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8b5842c067f5380e`；通过ALGO-011 `property_test/STATE-005/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=STATE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_005.py::test_state_005_rr` |

## TC-STATE-005-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-005-PF-01` |
| 对应单元ID | `STATE-005` — 不可变 PlayerView 状态载体 |
| 父测试合同 | `T-STATE-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `builder output`；向量引用`tests/spec_v3/vectors/state_005.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0fbab8b151ac94be`；通过ALGO-011 `property_test/STATE-005/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_state_005.py::test_state_005_pf` |

## TC-STATE-005-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-005-HL-01` |
| 对应单元ID | `STATE-005` — 不可变 PlayerView 状态载体 |
| 父测试合同 | `T-STATE-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `builder output`；向量引用`tests/spec_v3/vectors/state_005.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdc50ada8e1070275`；通过ALGO-011 `property_test/STATE-005/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_state_005.py::test_state_005_hl` |

## TC-STATE-006-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-006-UT-01` |
| 对应单元ID | `STATE-006` — 策略侧认知运行态初始化与归档 |
| 父测试合同 | `T-STATE-006-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `round start/end`；向量引用`tests/spec_v3/vectors/state_006.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x635b88558116d6a3`；通过ALGO-011 `property_test/STATE-006/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_006_ut`对应路径 |
| 预期输出 | 返回批准schema的`cognition state/snapshot`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_006.py::test_state_006_ut` |

## TC-STATE-006-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-006-BD-01` |
| 对应单元ID | `STATE-006` — 策略侧认知运行态初始化与归档 |
| 父测试合同 | `T-STATE-006-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `round start/end`；向量引用`tests/spec_v3/vectors/state_006.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3f282430d53ad09f`；通过ALGO-011 `property_test/STATE-006/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_006_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`cognition state/snapshot`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_006.py::test_state_006_bd` |

## TC-STATE-006-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-006-PT-01` |
| 对应单元ID | `STATE-006` — 策略侧认知运行态初始化与归档 |
| 父测试合同 | `T-STATE-006-N01`、`T-STATE-006-B01`、`T-STATE-006-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `round start/end`；向量引用`tests/spec_v3/vectors/state_006.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa0ea4bfd042766e1`；通过ALGO-011 `property_test/STATE-006/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_006_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_006.py::test_state_006_pt` |

## TC-STATE-006-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-006-PB-01` |
| 对应单元ID | `STATE-006` — 策略侧认知运行态初始化与归档 |
| 父测试合同 | `T-STATE-006-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `round start/end`；向量引用`tests/spec_v3/vectors/state_006.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6b609f54ba89689e`；通过ALGO-011 `property_test/STATE-006/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_006.py::test_state_006_pb` |

## TC-STATE-006-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-006-SM-01` |
| 对应单元ID | `STATE-006` — 策略侧认知运行态初始化与归档 |
| 父测试合同 | `T-STATE-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `round start/end`；向量引用`tests/spec_v3/vectors/state_006.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x89b2814d5915e004`；通过ALGO-011 `property_test/STATE-006/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_006_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_006.py::test_state_006_sm` |

## TC-STATE-006-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-006-IT-01` |
| 对应单元ID | `STATE-006` — 策略侧认知运行态初始化与归档 |
| 父测试合同 | `T-STATE-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `round start/end`；向量引用`tests/spec_v3/vectors/state_006.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb978420b28eebfcb`；通过ALGO-011 `property_test/STATE-006/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_006_it`对应路径 |
| 预期输出 | 通过生产入口得到`cognition state/snapshot`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_006.py::test_state_006_it` |

## TC-STATE-006-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-006-RR-01` |
| 对应单元ID | `STATE-006` — 策略侧认知运行态初始化与归档 |
| 父测试合同 | `T-STATE-006-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `round start/end`；向量引用`tests/spec_v3/vectors/state_006.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xac9ec74375b6f4f4`；通过ALGO-011 `property_test/STATE-006/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=STATE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_006.py::test_state_006_rr` |

## TC-STATE-006-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-006-PF-01` |
| 对应单元ID | `STATE-006` — 策略侧认知运行态初始化与归档 |
| 父测试合同 | `T-STATE-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `round start/end`；向量引用`tests/spec_v3/vectors/state_006.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7d97135a9736633f`；通过ALGO-011 `property_test/STATE-006/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_state_006.py::test_state_006_pf` |

## TC-STATE-006-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-006-HL-01` |
| 对应单元ID | `STATE-006` — 策略侧认知运行态初始化与归档 |
| 父测试合同 | `T-STATE-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `round start/end`；向量引用`tests/spec_v3/vectors/state_006.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc862fae825929aaf`；通过ALGO-011 `property_test/STATE-006/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_state_006.py::test_state_006_hl` |

## TC-STATE-007-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-007-UT-01` |
| 对应单元ID | `STATE-007` — 存档 schema 持久化与迁移 |
| 父测试合同 | `T-STATE-007-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state v1–v5`；向量引用`tests/spec_v3/vectors/state_007.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0a7a0fd43a0ac498`；通过ALGO-011 `property_test/STATE-007/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_007_ut`对应路径 |
| 预期输出 | 返回批准schema的`current state or error`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_007.py::test_state_007_ut` |

## TC-STATE-007-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-007-BD-01` |
| 对应单元ID | `STATE-007` — 存档 schema 持久化与迁移 |
| 父测试合同 | `T-STATE-007-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state v1–v5`；向量引用`tests/spec_v3/vectors/state_007.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0791a19c087f0cad`；通过ALGO-011 `property_test/STATE-007/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_007_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`current state or error`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_007.py::test_state_007_bd` |

## TC-STATE-007-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-007-PT-01` |
| 对应单元ID | `STATE-007` — 存档 schema 持久化与迁移 |
| 父测试合同 | `T-STATE-007-N01`、`T-STATE-007-B01`、`T-STATE-007-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state v1–v5`；向量引用`tests/spec_v3/vectors/state_007.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x69412331e955eb40`；通过ALGO-011 `property_test/STATE-007/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_007_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_007.py::test_state_007_pt` |

## TC-STATE-007-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-007-PB-01` |
| 对应单元ID | `STATE-007` — 存档 schema 持久化与迁移 |
| 父测试合同 | `T-STATE-007-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state v1–v5`；向量引用`tests/spec_v3/vectors/state_007.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa8a6519a306534e0`；通过ALGO-011 `property_test/STATE-007/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_007.py::test_state_007_pb` |

## TC-STATE-007-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-007-SM-01` |
| 对应单元ID | `STATE-007` — 存档 schema 持久化与迁移 |
| 父测试合同 | `T-STATE-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `state v1–v5`；向量引用`tests/spec_v3/vectors/state_007.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x88b02be6b7165ef1`；通过ALGO-011 `property_test/STATE-007/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_007_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_007.py::test_state_007_sm` |

## TC-STATE-007-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-007-IT-01` |
| 对应单元ID | `STATE-007` — 存档 schema 持久化与迁移 |
| 父测试合同 | `T-STATE-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `state v1–v5`；向量引用`tests/spec_v3/vectors/state_007.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf878c390c1f04981`；通过ALGO-011 `property_test/STATE-007/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_007_it`对应路径 |
| 预期输出 | 通过生产入口得到`current state or error`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_007.py::test_state_007_it` |

## TC-STATE-007-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-007-RR-01` |
| 对应单元ID | `STATE-007` — 存档 schema 持久化与迁移 |
| 父测试合同 | `T-STATE-007-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state v1–v5`；向量引用`tests/spec_v3/vectors/state_007.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xea1e654e2ac42feb`；通过ALGO-011 `property_test/STATE-007/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=STATE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_007.py::test_state_007_rr` |

## TC-STATE-007-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-007-PF-01` |
| 对应单元ID | `STATE-007` — 存档 schema 持久化与迁移 |
| 父测试合同 | `T-STATE-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state v1–v5`；向量引用`tests/spec_v3/vectors/state_007.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb8f415d29b3dbed8`；通过ALGO-011 `property_test/STATE-007/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_state_007.py::test_state_007_pf` |

## TC-STATE-007-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-007-HL-01` |
| 对应单元ID | `STATE-007` — 存档 schema 持久化与迁移 |
| 父测试合同 | `T-STATE-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `state v1–v5`；向量引用`tests/spec_v3/vectors/state_007.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd6abee486ffcbef4`；通过ALGO-011 `property_test/STATE-007/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_state_007.py::test_state_007_hl` |

## TC-STATE-008-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-008-UT-01` |
| 对应单元ID | `STATE-008` — 跨局比分、认知和 episode 状态继承 |
| 父测试合同 | `T-STATE-008-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `round result`；向量引用`tests/spec_v3/vectors/state_008.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x86a12dfab0b37359`；通过ALGO-011 `property_test/STATE-008/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_008_ut`对应路径 |
| 预期输出 | 返回批准schema的`next-round context`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_008.py::test_state_008_ut` |

## TC-STATE-008-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-008-BD-01` |
| 对应单元ID | `STATE-008` — 跨局比分、认知和 episode 状态继承 |
| 父测试合同 | `T-STATE-008-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `round result`；向量引用`tests/spec_v3/vectors/state_008.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x93d7c8f67918c717`；通过ALGO-011 `property_test/STATE-008/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_008_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`next-round context`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_008.py::test_state_008_bd` |

## TC-STATE-008-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-008-PT-01` |
| 对应单元ID | `STATE-008` — 跨局比分、认知和 episode 状态继承 |
| 父测试合同 | `T-STATE-008-N01`、`T-STATE-008-B01`、`T-STATE-008-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `round result`；向量引用`tests/spec_v3/vectors/state_008.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7a39bad701869539`；通过ALGO-011 `property_test/STATE-008/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_008_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_008.py::test_state_008_pt` |

## TC-STATE-008-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-008-PB-01` |
| 对应单元ID | `STATE-008` — 跨局比分、认知和 episode 状态继承 |
| 父测试合同 | `T-STATE-008-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `round result`；向量引用`tests/spec_v3/vectors/state_008.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8b05d2ef925c5cb1`；通过ALGO-011 `property_test/STATE-008/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_008.py::test_state_008_pb` |

## TC-STATE-008-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-008-SM-01` |
| 对应单元ID | `STATE-008` — 跨局比分、认知和 episode 状态继承 |
| 父测试合同 | `T-STATE-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `round result`；向量引用`tests/spec_v3/vectors/state_008.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb033d2cda1af4d73`；通过ALGO-011 `property_test/STATE-008/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_008_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_008.py::test_state_008_sm` |

## TC-STATE-008-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-008-IT-01` |
| 对应单元ID | `STATE-008` — 跨局比分、认知和 episode 状态继承 |
| 父测试合同 | `T-STATE-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `round result`；向量引用`tests/spec_v3/vectors/state_008.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb720f75e0baf57fc`；通过ALGO-011 `property_test/STATE-008/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_008_it`对应路径 |
| 预期输出 | 通过生产入口得到`next-round context`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_008.py::test_state_008_it` |

## TC-STATE-008-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-008-RR-01` |
| 对应单元ID | `STATE-008` — 跨局比分、认知和 episode 状态继承 |
| 父测试合同 | `T-STATE-008-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `round result`；向量引用`tests/spec_v3/vectors/state_008.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd3341299da4da3de`；通过ALGO-011 `property_test/STATE-008/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=STATE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_008.py::test_state_008_rr` |

## TC-STATE-008-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-008-PF-01` |
| 对应单元ID | `STATE-008` — 跨局比分、认知和 episode 状态继承 |
| 父测试合同 | `T-STATE-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `round result`；向量引用`tests/spec_v3/vectors/state_008.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbce584fe50f9007a`；通过ALGO-011 `property_test/STATE-008/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_state_008.py::test_state_008_pf` |

## TC-STATE-008-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-008-HL-01` |
| 对应单元ID | `STATE-008` — 跨局比分、认知和 episode 状态继承 |
| 父测试合同 | `T-STATE-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `round result`；向量引用`tests/spec_v3/vectors/state_008.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x102d03433d589624`；通过ALGO-011 `property_test/STATE-008/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_state_008.py::test_state_008_hl` |

## TC-STATE-009-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-009-UT-01` |
| 对应单元ID | `STATE-009` — 决策请求上下文与生命周期 |
| 父测试合同 | `T-STATE-009-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + PlayerView + legal set`；向量引用`tests/spec_v3/vectors/state_009.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1f11b55206597a17`；通过ALGO-011 `property_test/STATE-009/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_009_ut`对应路径 |
| 预期输出 | 返回批准schema的`request/result`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_009.py::test_state_009_ut` |

## TC-STATE-009-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-009-BD-01` |
| 对应单元ID | `STATE-009` — 决策请求上下文与生命周期 |
| 父测试合同 | `T-STATE-009-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + PlayerView + legal set`；向量引用`tests/spec_v3/vectors/state_009.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x08899f4a83780c38`；通过ALGO-011 `property_test/STATE-009/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_009_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`request/result`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_009.py::test_state_009_bd` |

## TC-STATE-009-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-009-PT-01` |
| 对应单元ID | `STATE-009` — 决策请求上下文与生命周期 |
| 父测试合同 | `T-STATE-009-N01`、`T-STATE-009-B01`、`T-STATE-009-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + PlayerView + legal set`；向量引用`tests/spec_v3/vectors/state_009.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x083f2b6fefc96b4a`；通过ALGO-011 `property_test/STATE-009/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_009_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_009.py::test_state_009_pt` |

## TC-STATE-009-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-009-PB-01` |
| 对应单元ID | `STATE-009` — 决策请求上下文与生命周期 |
| 父测试合同 | `T-STATE-009-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + PlayerView + legal set`；向量引用`tests/spec_v3/vectors/state_009.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x50f6d84728f41b7f`；通过ALGO-011 `property_test/STATE-009/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_009.py::test_state_009_pb` |

## TC-STATE-009-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-009-SM-01` |
| 对应单元ID | `STATE-009` — 决策请求上下文与生命周期 |
| 父测试合同 | `T-STATE-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `phase + PlayerView + legal set`；向量引用`tests/spec_v3/vectors/state_009.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9ba337210a51cf1a`；通过ALGO-011 `property_test/STATE-009/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_009_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_009.py::test_state_009_sm` |

## TC-STATE-009-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-009-IT-01` |
| 对应单元ID | `STATE-009` — 决策请求上下文与生命周期 |
| 父测试合同 | `T-STATE-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `phase + PlayerView + legal set`；向量引用`tests/spec_v3/vectors/state_009.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdc06fa77521169ee`；通过ALGO-011 `property_test/STATE-009/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_009_it`对应路径 |
| 预期输出 | 通过生产入口得到`request/result`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_009.py::test_state_009_it` |

## TC-STATE-009-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-009-RR-01` |
| 对应单元ID | `STATE-009` — 决策请求上下文与生命周期 |
| 父测试合同 | `T-STATE-009-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + PlayerView + legal set`；向量引用`tests/spec_v3/vectors/state_009.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x883208a5e64179e1`；通过ALGO-011 `property_test/STATE-009/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=STATE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_009.py::test_state_009_rr` |

## TC-STATE-009-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-009-PF-01` |
| 对应单元ID | `STATE-009` — 决策请求上下文与生命周期 |
| 父测试合同 | `T-STATE-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `phase + PlayerView + legal set`；向量引用`tests/spec_v3/vectors/state_009.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8ad8d30d4d5c19a4`；通过ALGO-011 `property_test/STATE-009/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_state_009.py::test_state_009_pf` |

## TC-STATE-009-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-009-HL-01` |
| 对应单元ID | `STATE-009` — 决策请求上下文与生命周期 |
| 父测试合同 | `T-STATE-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `phase + PlayerView + legal set`；向量引用`tests/spec_v3/vectors/state_009.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x625d7b09f496c247`；通过ALGO-011 `property_test/STATE-009/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_state_009.py::test_state_009_hl` |

## TC-STATE-010-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-010-UT-01` |
| 对应单元ID | `STATE-010` — GP/RP/Profile 注册与生命周期 |
| 父测试合同 | `T-STATE-010-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source config + phase`；向量引用`tests/spec_v3/vectors/state_010.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb736abe975295302`；通过ALGO-011 `property_test/STATE-010/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_010_ut`对应路径 |
| 预期输出 | 返回批准schema的`owned parameter state`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_010.py::test_state_010_ut` |

## TC-STATE-010-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-010-BD-01` |
| 对应单元ID | `STATE-010` — GP/RP/Profile 注册与生命周期 |
| 父测试合同 | `T-STATE-010-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source config + phase`；向量引用`tests/spec_v3/vectors/state_010.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4ab3807a2b3d0548`；通过ALGO-011 `property_test/STATE-010/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_010_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`owned parameter state`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_010.py::test_state_010_bd` |

## TC-STATE-010-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-010-PT-01` |
| 对应单元ID | `STATE-010` — GP/RP/Profile 注册与生命周期 |
| 父测试合同 | `T-STATE-010-N01`、`T-STATE-010-B01`、`T-STATE-010-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source config + phase`；向量引用`tests/spec_v3/vectors/state_010.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9d7a80df8ee062c2`；通过ALGO-011 `property_test/STATE-010/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_010_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_010.py::test_state_010_pt` |

## TC-STATE-010-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-010-PB-01` |
| 对应单元ID | `STATE-010` — GP/RP/Profile 注册与生命周期 |
| 父测试合同 | `T-STATE-010-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source config + phase`；向量引用`tests/spec_v3/vectors/state_010.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc43406e4fc75a36b`；通过ALGO-011 `property_test/STATE-010/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_010.py::test_state_010_pb` |

## TC-STATE-010-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-010-SM-01` |
| 对应单元ID | `STATE-010` — GP/RP/Profile 注册与生命周期 |
| 父测试合同 | `T-STATE-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `source config + phase`；向量引用`tests/spec_v3/vectors/state_010.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd4526245cecb062e`；通过ALGO-011 `property_test/STATE-010/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_010_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_010.py::test_state_010_sm` |

## TC-STATE-010-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-010-IT-01` |
| 对应单元ID | `STATE-010` — GP/RP/Profile 注册与生命周期 |
| 父测试合同 | `T-STATE-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `source config + phase`；向量引用`tests/spec_v3/vectors/state_010.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa0bfa447e75d9f76`；通过ALGO-011 `property_test/STATE-010/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_010_it`对应路径 |
| 预期输出 | 通过生产入口得到`owned parameter state`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_010.py::test_state_010_it` |

## TC-STATE-010-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-010-RR-01` |
| 对应单元ID | `STATE-010` — GP/RP/Profile 注册与生命周期 |
| 父测试合同 | `T-STATE-010-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source config + phase`；向量引用`tests/spec_v3/vectors/state_010.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8c247282f2299fc1`；通过ALGO-011 `property_test/STATE-010/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=STATE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_010.py::test_state_010_rr` |

## TC-STATE-010-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-010-PF-01` |
| 对应单元ID | `STATE-010` — GP/RP/Profile 注册与生命周期 |
| 父测试合同 | `T-STATE-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source config + phase`；向量引用`tests/spec_v3/vectors/state_010.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x859bd0680319e06a`；通过ALGO-011 `property_test/STATE-010/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_state_010.py::test_state_010_pf` |

## TC-STATE-010-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-010-HL-01` |
| 对应单元ID | `STATE-010` — GP/RP/Profile 注册与生命周期 |
| 父测试合同 | `T-STATE-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `source config + phase`；向量引用`tests/spec_v3/vectors/state_010.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5f329f15e73b55aa`；通过ALGO-011 `property_test/STATE-010/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_state_010.py::test_state_010_hl` |

## TC-STATE-011-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-011-UT-01` |
| 对应单元ID | `STATE-011` — 牌墙构建、洗牌与初始发牌 |
| 父测试合同 | `T-STATE-011-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `named RNG + player count`；向量引用`tests/spec_v3/vectors/state_011.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbbd389880e87075f`；通过ALGO-011 `property_test/STATE-011/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_011_ut`对应路径 |
| 预期输出 | 返回批准schema的`wall/hands`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_011.py::test_state_011_ut` |

## TC-STATE-011-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-011-BD-01` |
| 对应单元ID | `STATE-011` — 牌墙构建、洗牌与初始发牌 |
| 父测试合同 | `T-STATE-011-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `named RNG + player count`；向量引用`tests/spec_v3/vectors/state_011.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x22ed5200822d3b0a`；通过ALGO-011 `property_test/STATE-011/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_011_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`wall/hands`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_011.py::test_state_011_bd` |

## TC-STATE-011-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-011-PT-01` |
| 对应单元ID | `STATE-011` — 牌墙构建、洗牌与初始发牌 |
| 父测试合同 | `T-STATE-011-N01`、`T-STATE-011-B01`、`T-STATE-011-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `named RNG + player count`；向量引用`tests/spec_v3/vectors/state_011.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2219879c250c86ee`；通过ALGO-011 `property_test/STATE-011/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_011_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_011.py::test_state_011_pt` |

## TC-STATE-011-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-011-PB-01` |
| 对应单元ID | `STATE-011` — 牌墙构建、洗牌与初始发牌 |
| 父测试合同 | `T-STATE-011-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `named RNG + player count`；向量引用`tests/spec_v3/vectors/state_011.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2100180ca7b536aa`；通过ALGO-011 `property_test/STATE-011/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_011.py::test_state_011_pb` |

## TC-STATE-011-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-011-SM-01` |
| 对应单元ID | `STATE-011` — 牌墙构建、洗牌与初始发牌 |
| 父测试合同 | `T-STATE-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `named RNG + player count`；向量引用`tests/spec_v3/vectors/state_011.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd5093ae6123a4a64`；通过ALGO-011 `property_test/STATE-011/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_011_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_011.py::test_state_011_sm` |

## TC-STATE-011-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-011-IT-01` |
| 对应单元ID | `STATE-011` — 牌墙构建、洗牌与初始发牌 |
| 父测试合同 | `T-STATE-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `named RNG + player count`；向量引用`tests/spec_v3/vectors/state_011.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xefce3604b641c8f6`；通过ALGO-011 `property_test/STATE-011/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_011_it`对应路径 |
| 预期输出 | 通过生产入口得到`wall/hands`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_011.py::test_state_011_it` |

## TC-STATE-011-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-011-RR-01` |
| 对应单元ID | `STATE-011` — 牌墙构建、洗牌与初始发牌 |
| 父测试合同 | `T-STATE-011-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `named RNG + player count`；向量引用`tests/spec_v3/vectors/state_011.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd154ccccfa7cca7c`；通过ALGO-011 `property_test/STATE-011/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=STATE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_011.py::test_state_011_rr` |

## TC-STATE-011-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-011-PF-01` |
| 对应单元ID | `STATE-011` — 牌墙构建、洗牌与初始发牌 |
| 父测试合同 | `T-STATE-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `named RNG + player count`；向量引用`tests/spec_v3/vectors/state_011.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf313d3c050e5be3b`；通过ALGO-011 `property_test/STATE-011/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_state_011.py::test_state_011_pf` |

## TC-STATE-011-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-011-HL-01` |
| 对应单元ID | `STATE-011` — 牌墙构建、洗牌与初始发牌 |
| 父测试合同 | `T-STATE-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `named RNG + player count`；向量引用`tests/spec_v3/vectors/state_011.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4e675403dc43da79`；通过ALGO-011 `property_test/STATE-011/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_state_011.py::test_state_011_hl` |

## TC-STATE-012-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-012-UT-01` |
| 对应单元ID | `STATE-012` — 策略超时、崩溃与合法默认动作回退 |
| 父测试合同 | `T-STATE-012-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `request + deadline/failure + legal set`；向量引用`tests/spec_v3/vectors/state_012.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x989105f830373ba3`；通过ALGO-011 `property_test/STATE-012/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_012_ut`对应路径 |
| 预期输出 | 返回批准schema的`fallback result`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_012.py::test_state_012_ut` |

## TC-STATE-012-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-012-BD-01` |
| 对应单元ID | `STATE-012` — 策略超时、崩溃与合法默认动作回退 |
| 父测试合同 | `T-STATE-012-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `request + deadline/failure + legal set`；向量引用`tests/spec_v3/vectors/state_012.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa028ca49a7cefb6a`；通过ALGO-011 `property_test/STATE-012/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_012_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`fallback result`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_012.py::test_state_012_bd` |

## TC-STATE-012-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-012-PT-01` |
| 对应单元ID | `STATE-012` — 策略超时、崩溃与合法默认动作回退 |
| 父测试合同 | `T-STATE-012-N01`、`T-STATE-012-B01`、`T-STATE-012-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `request + deadline/failure + legal set`；向量引用`tests/spec_v3/vectors/state_012.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xad8803a344cdd414`；通过ALGO-011 `property_test/STATE-012/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_012_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_012.py::test_state_012_pt` |

## TC-STATE-012-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-012-PB-01` |
| 对应单元ID | `STATE-012` — 策略超时、崩溃与合法默认动作回退 |
| 父测试合同 | `T-STATE-012-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `request + deadline/failure + legal set`；向量引用`tests/spec_v3/vectors/state_012.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe17d7cadf7e83ce9`；通过ALGO-011 `property_test/STATE-012/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_012.py::test_state_012_pb` |

## TC-STATE-012-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-012-SM-01` |
| 对应单元ID | `STATE-012` — 策略超时、崩溃与合法默认动作回退 |
| 父测试合同 | `T-STATE-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `request + deadline/failure + legal set`；向量引用`tests/spec_v3/vectors/state_012.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6c2b6d4038a8a865`；通过ALGO-011 `property_test/STATE-012/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_012_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_012.py::test_state_012_sm` |

## TC-STATE-012-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-012-IT-01` |
| 对应单元ID | `STATE-012` — 策略超时、崩溃与合法默认动作回退 |
| 父测试合同 | `T-STATE-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `request + deadline/failure + legal set`；向量引用`tests/spec_v3/vectors/state_012.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1b02d2665062830a`；通过ALGO-011 `property_test/STATE-012/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_state_012_it`对应路径 |
| 预期输出 | 通过生产入口得到`fallback result`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=STATE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_012.py::test_state_012_it` |

## TC-STATE-012-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-012-RR-01` |
| 对应单元ID | `STATE-012` — 策略超时、崩溃与合法默认动作回退 |
| 父测试合同 | `T-STATE-012-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `request + deadline/failure + legal set`；向量引用`tests/spec_v3/vectors/state_012.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6507c51ed1e94fac`；通过ALGO-011 `property_test/STATE-012/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=STATE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_state_012.py::test_state_012_rr` |

## TC-STATE-012-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-012-PF-01` |
| 对应单元ID | `STATE-012` — 策略超时、崩溃与合法默认动作回退 |
| 父测试合同 | `T-STATE-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `request + deadline/failure + legal set`；向量引用`tests/spec_v3/vectors/state_012.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6f914a236a637306`；通过ALGO-011 `property_test/STATE-012/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_state_012.py::test_state_012_pf` |

## TC-STATE-012-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-STATE-012-HL-01` |
| 对应单元ID | `STATE-012` — 策略超时、崩溃与合法默认动作回退 |
| 父测试合同 | `T-STATE-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `request + deadline/failure + legal set`；向量引用`tests/spec_v3/vectors/state_012.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1d18096c444af072`；通过ALGO-011 `property_test/STATE-012/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=STATE-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_state_012.py::test_state_012_hl` |

## TC-SCORE-001-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-001-UT-01` |
| 对应单元ID | `SCORE-001` — 分数账本分层与守恒 |
| 父测试合同 | `T-SCORE-001-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `score events`；向量引用`tests/spec_v3/vectors/score_001.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x193ded4191603d92`；通过ALGO-011 `property_test/SCORE-001/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_001_ut`对应路径 |
| 预期输出 | 返回批准schema的`ledger/before/after`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_001.py::test_score_001_ut` |

## TC-SCORE-001-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-001-BD-01` |
| 对应单元ID | `SCORE-001` — 分数账本分层与守恒 |
| 父测试合同 | `T-SCORE-001-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `score events`；向量引用`tests/spec_v3/vectors/score_001.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1205321e868b6b0d`；通过ALGO-011 `property_test/SCORE-001/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_001_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`ledger/before/after`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_001.py::test_score_001_bd` |

## TC-SCORE-001-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-001-PT-01` |
| 对应单元ID | `SCORE-001` — 分数账本分层与守恒 |
| 父测试合同 | `T-SCORE-001-N01`、`T-SCORE-001-B01`、`T-SCORE-001-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `score events`；向量引用`tests/spec_v3/vectors/score_001.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe5f2686207c56a4b`；通过ALGO-011 `property_test/SCORE-001/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_001_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_001.py::test_score_001_pt` |

## TC-SCORE-001-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-001-PB-01` |
| 对应单元ID | `SCORE-001` — 分数账本分层与守恒 |
| 父测试合同 | `T-SCORE-001-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `score events`；向量引用`tests/spec_v3/vectors/score_001.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x38d19ecf0d3dab43`；通过ALGO-011 `property_test/SCORE-001/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_001.py::test_score_001_pb` |

## TC-SCORE-001-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-001-SM-01` |
| 对应单元ID | `SCORE-001` — 分数账本分层与守恒 |
| 父测试合同 | `T-SCORE-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `score events`；向量引用`tests/spec_v3/vectors/score_001.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3f4d8991995d729e`；通过ALGO-011 `property_test/SCORE-001/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_001_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=SCORE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_001.py::test_score_001_sm` |

## TC-SCORE-001-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-001-IT-01` |
| 对应单元ID | `SCORE-001` — 分数账本分层与守恒 |
| 父测试合同 | `T-SCORE-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `score events`；向量引用`tests/spec_v3/vectors/score_001.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3602b2164ce0d946`；通过ALGO-011 `property_test/SCORE-001/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_001_it`对应路径 |
| 预期输出 | 通过生产入口得到`ledger/before/after`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=SCORE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_001.py::test_score_001_it` |

## TC-SCORE-001-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-001-RR-01` |
| 对应单元ID | `SCORE-001` — 分数账本分层与守恒 |
| 父测试合同 | `T-SCORE-001-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `score events`；向量引用`tests/spec_v3/vectors/score_001.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x104e172d1db182dd`；通过ALGO-011 `property_test/SCORE-001/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=SCORE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_001.py::test_score_001_rr` |

## TC-SCORE-001-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-001-PF-01` |
| 对应单元ID | `SCORE-001` — 分数账本分层与守恒 |
| 父测试合同 | `T-SCORE-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `score events`；向量引用`tests/spec_v3/vectors/score_001.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x16c8cb9a3089d7fe`；通过ALGO-011 `property_test/SCORE-001/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_score_001.py::test_score_001_pf` |

## TC-SCORE-001-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-001-HL-01` |
| 对应单元ID | `SCORE-001` — 分数账本分层与守恒 |
| 父测试合同 | `T-SCORE-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `score events`；向量引用`tests/spec_v3/vectors/score_001.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe0f1e62614423b32`；通过ALGO-011 `property_test/SCORE-001/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_score_001.py::test_score_001_hl` |

## TC-SCORE-002-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-002-UT-01` |
| 对应单元ID | `SCORE-002` — 自摸、点炮与抢杠胡计分 |
| 父测试合同 | `T-SCORE-002-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hu facts + fan policy`；向量引用`tests/spec_v3/vectors/score_002.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x38171b064b57213a`；通过ALGO-011 `property_test/SCORE-002/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_002_ut`对应路径 |
| 预期输出 | 返回批准schema的`hu transfers`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_002.py::test_score_002_ut` |

## TC-SCORE-002-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-002-BD-01` |
| 对应单元ID | `SCORE-002` — 自摸、点炮与抢杠胡计分 |
| 父测试合同 | `T-SCORE-002-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hu facts + fan policy`；向量引用`tests/spec_v3/vectors/score_002.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf103d317dd36bb59`；通过ALGO-011 `property_test/SCORE-002/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_002_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`hu transfers`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_002.py::test_score_002_bd` |

## TC-SCORE-002-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-002-PT-01` |
| 对应单元ID | `SCORE-002` — 自摸、点炮与抢杠胡计分 |
| 父测试合同 | `T-SCORE-002-N01`、`T-SCORE-002-B01`、`T-SCORE-002-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hu facts + fan policy`；向量引用`tests/spec_v3/vectors/score_002.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf3b924d5c0d6933e`；通过ALGO-011 `property_test/SCORE-002/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_002_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_002.py::test_score_002_pt` |

## TC-SCORE-002-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-002-PB-01` |
| 对应单元ID | `SCORE-002` — 自摸、点炮与抢杠胡计分 |
| 父测试合同 | `T-SCORE-002-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hu facts + fan policy`；向量引用`tests/spec_v3/vectors/score_002.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xeb809325cb20d995`；通过ALGO-011 `property_test/SCORE-002/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_002.py::test_score_002_pb` |

## TC-SCORE-002-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-002-SM-01` |
| 对应单元ID | `SCORE-002` — 自摸、点炮与抢杠胡计分 |
| 父测试合同 | `T-SCORE-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `hu facts + fan policy`；向量引用`tests/spec_v3/vectors/score_002.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdb806a3b464020fe`；通过ALGO-011 `property_test/SCORE-002/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_002_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=SCORE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_002.py::test_score_002_sm` |

## TC-SCORE-002-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-002-IT-01` |
| 对应单元ID | `SCORE-002` — 自摸、点炮与抢杠胡计分 |
| 父测试合同 | `T-SCORE-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `hu facts + fan policy`；向量引用`tests/spec_v3/vectors/score_002.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8d52dfc3bc83ba56`；通过ALGO-011 `property_test/SCORE-002/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_002_it`对应路径 |
| 预期输出 | 通过生产入口得到`hu transfers`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=SCORE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_002.py::test_score_002_it` |

## TC-SCORE-002-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-002-RR-01` |
| 对应单元ID | `SCORE-002` — 自摸、点炮与抢杠胡计分 |
| 父测试合同 | `T-SCORE-002-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hu facts + fan policy`；向量引用`tests/spec_v3/vectors/score_002.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9212ec3467a77142`；通过ALGO-011 `property_test/SCORE-002/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=SCORE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_002.py::test_score_002_rr` |

## TC-SCORE-002-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-002-PF-01` |
| 对应单元ID | `SCORE-002` — 自摸、点炮与抢杠胡计分 |
| 父测试合同 | `T-SCORE-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `hu facts + fan policy`；向量引用`tests/spec_v3/vectors/score_002.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6cb358f9478cd4ed`；通过ALGO-011 `property_test/SCORE-002/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_score_002.py::test_score_002_pf` |

## TC-SCORE-002-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-002-HL-01` |
| 对应单元ID | `SCORE-002` — 自摸、点炮与抢杠胡计分 |
| 父测试合同 | `T-SCORE-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `hu facts + fan policy`；向量引用`tests/spec_v3/vectors/score_002.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf96de34296620031`；通过ALGO-011 `property_test/SCORE-002/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_score_002.py::test_score_002_hl` |

## TC-SCORE-003-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-003-UT-01` |
| 对应单元ID | `SCORE-003` — 明/暗/补杠与呼叫转移计分 |
| 父测试合同 | `T-SCORE-003-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `gang events + rules`；向量引用`tests/spec_v3/vectors/score_003.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7c529a5c9baef312`；通过ALGO-011 `property_test/SCORE-003/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_003_ut`对应路径 |
| 预期输出 | 返回批准schema的`gang transfers`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_003.py::test_score_003_ut` |

## TC-SCORE-003-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-003-BD-01` |
| 对应单元ID | `SCORE-003` — 明/暗/补杠与呼叫转移计分 |
| 父测试合同 | `T-SCORE-003-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `gang events + rules`；向量引用`tests/spec_v3/vectors/score_003.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6536b0ea92ae57df`；通过ALGO-011 `property_test/SCORE-003/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_003_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`gang transfers`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_003.py::test_score_003_bd` |

## TC-SCORE-003-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-003-PT-01` |
| 对应单元ID | `SCORE-003` — 明/暗/补杠与呼叫转移计分 |
| 父测试合同 | `T-SCORE-003-N01`、`T-SCORE-003-B01`、`T-SCORE-003-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `gang events + rules`；向量引用`tests/spec_v3/vectors/score_003.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x00ee6c6db58339f9`；通过ALGO-011 `property_test/SCORE-003/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_003_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_003.py::test_score_003_pt` |

## TC-SCORE-003-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-003-PB-01` |
| 对应单元ID | `SCORE-003` — 明/暗/补杠与呼叫转移计分 |
| 父测试合同 | `T-SCORE-003-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `gang events + rules`；向量引用`tests/spec_v3/vectors/score_003.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x03d694669c6cd3d9`；通过ALGO-011 `property_test/SCORE-003/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_003.py::test_score_003_pb` |

## TC-SCORE-003-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-003-SM-01` |
| 对应单元ID | `SCORE-003` — 明/暗/补杠与呼叫转移计分 |
| 父测试合同 | `T-SCORE-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `gang events + rules`；向量引用`tests/spec_v3/vectors/score_003.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4e1bb9ce13ba7164`；通过ALGO-011 `property_test/SCORE-003/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_003_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=SCORE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_003.py::test_score_003_sm` |

## TC-SCORE-003-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-003-IT-01` |
| 对应单元ID | `SCORE-003` — 明/暗/补杠与呼叫转移计分 |
| 父测试合同 | `T-SCORE-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `gang events + rules`；向量引用`tests/spec_v3/vectors/score_003.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9b5f84feb711f5cd`；通过ALGO-011 `property_test/SCORE-003/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_003_it`对应路径 |
| 预期输出 | 通过生产入口得到`gang transfers`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=SCORE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_003.py::test_score_003_it` |

## TC-SCORE-003-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-003-RR-01` |
| 对应单元ID | `SCORE-003` — 明/暗/补杠与呼叫转移计分 |
| 父测试合同 | `T-SCORE-003-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `gang events + rules`；向量引用`tests/spec_v3/vectors/score_003.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6d1fd04626079289`；通过ALGO-011 `property_test/SCORE-003/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=SCORE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_003.py::test_score_003_rr` |

## TC-SCORE-003-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-003-PF-01` |
| 对应单元ID | `SCORE-003` — 明/暗/补杠与呼叫转移计分 |
| 父测试合同 | `T-SCORE-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `gang events + rules`；向量引用`tests/spec_v3/vectors/score_003.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6977d112d9e47807`；通过ALGO-011 `property_test/SCORE-003/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_score_003.py::test_score_003_pf` |

## TC-SCORE-003-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-003-HL-01` |
| 对应单元ID | `SCORE-003` — 明/暗/补杠与呼叫转移计分 |
| 父测试合同 | `T-SCORE-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `gang events + rules`；向量引用`tests/spec_v3/vectors/score_003.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x34a93ad8b876d116`；通过ALGO-011 `property_test/SCORE-003/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_score_003.py::test_score_003_hl` |

## TC-SCORE-004-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-004-UT-01` |
| 对应单元ID | `SCORE-004` — 花猪、查大叫与退税终局调整 |
| 父测试合同 | `T-SCORE-004-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `end state + rules`；向量引用`tests/spec_v3/vectors/score_004.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0834af49440d394b`；通过ALGO-011 `property_test/SCORE-004/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_004_ut`对应路径 |
| 预期输出 | 返回批准schema的`adjustments`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_004.py::test_score_004_ut` |

## TC-SCORE-004-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-004-BD-01` |
| 对应单元ID | `SCORE-004` — 花猪、查大叫与退税终局调整 |
| 父测试合同 | `T-SCORE-004-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `end state + rules`；向量引用`tests/spec_v3/vectors/score_004.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2fa6f03fb9d73518`；通过ALGO-011 `property_test/SCORE-004/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_004_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`adjustments`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_004.py::test_score_004_bd` |

## TC-SCORE-004-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-004-PT-01` |
| 对应单元ID | `SCORE-004` — 花猪、查大叫与退税终局调整 |
| 父测试合同 | `T-SCORE-004-N01`、`T-SCORE-004-B01`、`T-SCORE-004-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `end state + rules`；向量引用`tests/spec_v3/vectors/score_004.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x34819810a7f9d816`；通过ALGO-011 `property_test/SCORE-004/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_004_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_004.py::test_score_004_pt` |

## TC-SCORE-004-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-004-PB-01` |
| 对应单元ID | `SCORE-004` — 花猪、查大叫与退税终局调整 |
| 父测试合同 | `T-SCORE-004-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `end state + rules`；向量引用`tests/spec_v3/vectors/score_004.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6cb4ea95d0aeb8c6`；通过ALGO-011 `property_test/SCORE-004/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_004.py::test_score_004_pb` |

## TC-SCORE-004-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-004-SM-01` |
| 对应单元ID | `SCORE-004` — 花猪、查大叫与退税终局调整 |
| 父测试合同 | `T-SCORE-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `end state + rules`；向量引用`tests/spec_v3/vectors/score_004.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc5fad0e6d6c3a806`；通过ALGO-011 `property_test/SCORE-004/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_004_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=SCORE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_004.py::test_score_004_sm` |

## TC-SCORE-004-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-004-IT-01` |
| 对应单元ID | `SCORE-004` — 花猪、查大叫与退税终局调整 |
| 父测试合同 | `T-SCORE-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `end state + rules`；向量引用`tests/spec_v3/vectors/score_004.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x27ae2cc441bb04fd`；通过ALGO-011 `property_test/SCORE-004/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_004_it`对应路径 |
| 预期输出 | 通过生产入口得到`adjustments`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=SCORE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_004.py::test_score_004_it` |

## TC-SCORE-004-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-004-RR-01` |
| 对应单元ID | `SCORE-004` — 花猪、查大叫与退税终局调整 |
| 父测试合同 | `T-SCORE-004-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `end state + rules`；向量引用`tests/spec_v3/vectors/score_004.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe5415b2f0ac5e12c`；通过ALGO-011 `property_test/SCORE-004/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=SCORE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_004.py::test_score_004_rr` |

## TC-SCORE-004-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-004-PF-01` |
| 对应单元ID | `SCORE-004` — 花猪、查大叫与退税终局调整 |
| 父测试合同 | `T-SCORE-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `end state + rules`；向量引用`tests/spec_v3/vectors/score_004.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8d878156223224b1`；通过ALGO-011 `property_test/SCORE-004/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_score_004.py::test_score_004_pf` |

## TC-SCORE-004-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-004-HL-01` |
| 对应单元ID | `SCORE-004` — 花猪、查大叫与退税终局调整 |
| 父测试合同 | `T-SCORE-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `end state + rules`；向量引用`tests/spec_v3/vectors/score_004.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0163f71364fe3281`；通过ALGO-011 `property_test/SCORE-004/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_score_004.py::test_score_004_hl` |

## TC-SCORE-005-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-005-UT-01` |
| 对应单元ID | `SCORE-005` — 封顶、互斥和转移结算顺序 |
| 父测试合同 | `T-SCORE-005-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `raw components + cap policy`；向量引用`tests/spec_v3/vectors/score_005.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf870823ec0f60776`；通过ALGO-011 `property_test/SCORE-005/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_005_ut`对应路径 |
| 预期输出 | 返回批准schema的`final transfers`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_005.py::test_score_005_ut` |

## TC-SCORE-005-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-005-BD-01` |
| 对应单元ID | `SCORE-005` — 封顶、互斥和转移结算顺序 |
| 父测试合同 | `T-SCORE-005-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `raw components + cap policy`；向量引用`tests/spec_v3/vectors/score_005.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8a2aa8a3f08b4525`；通过ALGO-011 `property_test/SCORE-005/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_005_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`final transfers`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_005.py::test_score_005_bd` |

## TC-SCORE-005-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-005-PT-01` |
| 对应单元ID | `SCORE-005` — 封顶、互斥和转移结算顺序 |
| 父测试合同 | `T-SCORE-005-N01`、`T-SCORE-005-B01`、`T-SCORE-005-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `raw components + cap policy`；向量引用`tests/spec_v3/vectors/score_005.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x231d832b4d593743`；通过ALGO-011 `property_test/SCORE-005/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_005_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_005.py::test_score_005_pt` |

## TC-SCORE-005-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-005-PB-01` |
| 对应单元ID | `SCORE-005` — 封顶、互斥和转移结算顺序 |
| 父测试合同 | `T-SCORE-005-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `raw components + cap policy`；向量引用`tests/spec_v3/vectors/score_005.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1f0c4d0a1e2705cc`；通过ALGO-011 `property_test/SCORE-005/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_005.py::test_score_005_pb` |

## TC-SCORE-005-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-005-SM-01` |
| 对应单元ID | `SCORE-005` — 封顶、互斥和转移结算顺序 |
| 父测试合同 | `T-SCORE-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `raw components + cap policy`；向量引用`tests/spec_v3/vectors/score_005.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe4d64986deddcf15`；通过ALGO-011 `property_test/SCORE-005/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_005_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=SCORE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_005.py::test_score_005_sm` |

## TC-SCORE-005-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-005-IT-01` |
| 对应单元ID | `SCORE-005` — 封顶、互斥和转移结算顺序 |
| 父测试合同 | `T-SCORE-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `raw components + cap policy`；向量引用`tests/spec_v3/vectors/score_005.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x22b981d1de4a6a42`；通过ALGO-011 `property_test/SCORE-005/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_005_it`对应路径 |
| 预期输出 | 通过生产入口得到`final transfers`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=SCORE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_005.py::test_score_005_it` |

## TC-SCORE-005-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-005-RR-01` |
| 对应单元ID | `SCORE-005` — 封顶、互斥和转移结算顺序 |
| 父测试合同 | `T-SCORE-005-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `raw components + cap policy`；向量引用`tests/spec_v3/vectors/score_005.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x22575dbc22fa48f5`；通过ALGO-011 `property_test/SCORE-005/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=SCORE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_005.py::test_score_005_rr` |

## TC-SCORE-005-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-005-PF-01` |
| 对应单元ID | `SCORE-005` — 封顶、互斥和转移结算顺序 |
| 父测试合同 | `T-SCORE-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `raw components + cap policy`；向量引用`tests/spec_v3/vectors/score_005.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x345d8a2afa01eead`；通过ALGO-011 `property_test/SCORE-005/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_score_005.py::test_score_005_pf` |

## TC-SCORE-005-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-005-HL-01` |
| 对应单元ID | `SCORE-005` — 封顶、互斥和转移结算顺序 |
| 父测试合同 | `T-SCORE-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `raw components + cap policy`；向量引用`tests/spec_v3/vectors/score_005.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x44b0405d5efacc8e`；通过ALGO-011 `property_test/SCORE-005/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_score_005.py::test_score_005_hl` |

## TC-SCORE-006-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-006-UT-01` |
| 对应单元ID | `SCORE-006` — 单局总分、整场累计与排名 |
| 父测试合同 | `T-SCORE-006-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ledgers + prior standings`；向量引用`tests/spec_v3/vectors/score_006.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6175340edfaf7acc`；通过ALGO-011 `property_test/SCORE-006/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_006_ut`对应路径 |
| 预期输出 | 返回批准schema的`result/rank`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_006.py::test_score_006_ut` |

## TC-SCORE-006-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-006-BD-01` |
| 对应单元ID | `SCORE-006` — 单局总分、整场累计与排名 |
| 父测试合同 | `T-SCORE-006-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ledgers + prior standings`；向量引用`tests/spec_v3/vectors/score_006.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x67ca6a97f80056a2`；通过ALGO-011 `property_test/SCORE-006/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_006_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`result/rank`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_006.py::test_score_006_bd` |

## TC-SCORE-006-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-006-PT-01` |
| 对应单元ID | `SCORE-006` — 单局总分、整场累计与排名 |
| 父测试合同 | `T-SCORE-006-N01`、`T-SCORE-006-B01`、`T-SCORE-006-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ledgers + prior standings`；向量引用`tests/spec_v3/vectors/score_006.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe85a67f70e327290`；通过ALGO-011 `property_test/SCORE-006/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_006_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_006.py::test_score_006_pt` |

## TC-SCORE-006-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-006-PB-01` |
| 对应单元ID | `SCORE-006` — 单局总分、整场累计与排名 |
| 父测试合同 | `T-SCORE-006-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ledgers + prior standings`；向量引用`tests/spec_v3/vectors/score_006.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x94de2eebcec16738`；通过ALGO-011 `property_test/SCORE-006/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_006.py::test_score_006_pb` |

## TC-SCORE-006-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-006-SM-01` |
| 对应单元ID | `SCORE-006` — 单局总分、整场累计与排名 |
| 父测试合同 | `T-SCORE-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `ledgers + prior standings`；向量引用`tests/spec_v3/vectors/score_006.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x40fe932acd644aa5`；通过ALGO-011 `property_test/SCORE-006/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_006_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=SCORE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_006.py::test_score_006_sm` |

## TC-SCORE-006-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-006-IT-01` |
| 对应单元ID | `SCORE-006` — 单局总分、整场累计与排名 |
| 父测试合同 | `T-SCORE-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `ledgers + prior standings`；向量引用`tests/spec_v3/vectors/score_006.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc4d1353fc16ebf00`；通过ALGO-011 `property_test/SCORE-006/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_score_006_it`对应路径 |
| 预期输出 | 通过生产入口得到`result/rank`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=SCORE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_006.py::test_score_006_it` |

## TC-SCORE-006-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-006-RR-01` |
| 对应单元ID | `SCORE-006` — 单局总分、整场累计与排名 |
| 父测试合同 | `T-SCORE-006-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ledgers + prior standings`；向量引用`tests/spec_v3/vectors/score_006.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x01e34a9dcefb0a00`；通过ALGO-011 `property_test/SCORE-006/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=SCORE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_score_006.py::test_score_006_rr` |

## TC-SCORE-006-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-006-PF-01` |
| 对应单元ID | `SCORE-006` — 单局总分、整场累计与排名 |
| 父测试合同 | `T-SCORE-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ledgers + prior standings`；向量引用`tests/spec_v3/vectors/score_006.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0df06e0ca6b86fe8`；通过ALGO-011 `property_test/SCORE-006/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_score_006.py::test_score_006_pf` |

## TC-SCORE-006-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-SCORE-006-HL-01` |
| 对应单元ID | `SCORE-006` — 单局总分、整场累计与排名 |
| 父测试合同 | `T-SCORE-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `ledgers + prior standings`；向量引用`tests/spec_v3/vectors/score_006.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7d0528ce9aa7f652`；通过ALGO-011 `property_test/SCORE-006/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=SCORE-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_score_006.py::test_score_006_hl` |

## TC-TRAIN-001-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-001-UT-01` |
| 对应单元ID | `TRAIN-001` — 复用生产规则的训练包装 |
| 父测试合同 | `T-TRAIN-001-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `engine config + agents`；向量引用`tests/spec_v3/vectors/train_001.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x090db1ef3d43e127`；通过ALGO-011 `property_test/TRAIN-001/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_001_ut`对应路径 |
| 预期输出 | 返回批准schema的`training transition`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_001.py::test_train_001_ut` |

## TC-TRAIN-001-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-001-BD-01` |
| 对应单元ID | `TRAIN-001` — 复用生产规则的训练包装 |
| 父测试合同 | `T-TRAIN-001-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `engine config + agents`；向量引用`tests/spec_v3/vectors/train_001.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x16e3450cdc0ccf6d`；通过ALGO-011 `property_test/TRAIN-001/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_001_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`training transition`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_001.py::test_train_001_bd` |

## TC-TRAIN-001-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-001-PT-01` |
| 对应单元ID | `TRAIN-001` — 复用生产规则的训练包装 |
| 父测试合同 | `T-TRAIN-001-N01`、`T-TRAIN-001-B01`、`T-TRAIN-001-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `engine config + agents`；向量引用`tests/spec_v3/vectors/train_001.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x74827798983c1de4`；通过ALGO-011 `property_test/TRAIN-001/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_001_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_001.py::test_train_001_pt` |

## TC-TRAIN-001-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-001-PB-01` |
| 对应单元ID | `TRAIN-001` — 复用生产规则的训练包装 |
| 父测试合同 | `T-TRAIN-001-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `engine config + agents`；向量引用`tests/spec_v3/vectors/train_001.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0554150bbe6bb61d`；通过ALGO-011 `property_test/TRAIN-001/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_001.py::test_train_001_pb` |

## TC-TRAIN-001-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-001-SM-01` |
| 对应单元ID | `TRAIN-001` — 复用生产规则的训练包装 |
| 父测试合同 | `T-TRAIN-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `engine config + agents`；向量引用`tests/spec_v3/vectors/train_001.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x37393e8319f1c4ae`；通过ALGO-011 `property_test/TRAIN-001/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_001_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_001.py::test_train_001_sm` |

## TC-TRAIN-001-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-001-IT-01` |
| 对应单元ID | `TRAIN-001` — 复用生产规则的训练包装 |
| 父测试合同 | `T-TRAIN-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `engine config + agents`；向量引用`tests/spec_v3/vectors/train_001.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5199ea9cad9b3693`；通过ALGO-011 `property_test/TRAIN-001/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_001_it`对应路径 |
| 预期输出 | 通过生产入口得到`training transition`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_001.py::test_train_001_it` |

## TC-TRAIN-001-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-001-RR-01` |
| 对应单元ID | `TRAIN-001` — 复用生产规则的训练包装 |
| 父测试合同 | `T-TRAIN-001-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `engine config + agents`；向量引用`tests/spec_v3/vectors/train_001.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8bbfcfe3ee092aa6`；通过ALGO-011 `property_test/TRAIN-001/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=TRAIN-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_001.py::test_train_001_rr` |

## TC-TRAIN-001-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-001-PF-01` |
| 对应单元ID | `TRAIN-001` — 复用生产规则的训练包装 |
| 父测试合同 | `T-TRAIN-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `engine config + agents`；向量引用`tests/spec_v3/vectors/train_001.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xfc552e5b5c5493e3`；通过ALGO-011 `property_test/TRAIN-001/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_train_001.py::test_train_001_pf` |

## TC-TRAIN-001-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-001-HL-01` |
| 对应单元ID | `TRAIN-001` — 复用生产规则的训练包装 |
| 父测试合同 | `T-TRAIN-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `engine config + agents`；向量引用`tests/spec_v3/vectors/train_001.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc73a4ab9e1a526a2`；通过ALGO-011 `property_test/TRAIN-001/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_train_001.py::test_train_001_hl` |

## TC-TRAIN-002-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-002-UT-01` |
| 对应单元ID | `TRAIN-002` — Observation v2 编码 |
| 父测试合同 | `T-TRAIN-002-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `PlayerView + optional cognition`；向量引用`tests/spec_v3/vectors/train_002.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9d5433075b9885b3`；通过ALGO-011 `property_test/TRAIN-002/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_002_ut`对应路径 |
| 预期输出 | 返回批准schema的`fixed observation`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_002.py::test_train_002_ut` |

## TC-TRAIN-002-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-002-BD-01` |
| 对应单元ID | `TRAIN-002` — Observation v2 编码 |
| 父测试合同 | `T-TRAIN-002-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `PlayerView + optional cognition`；向量引用`tests/spec_v3/vectors/train_002.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbb09e4e2bb69381a`；通过ALGO-011 `property_test/TRAIN-002/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_002_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`fixed observation`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_002.py::test_train_002_bd` |

## TC-TRAIN-002-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-002-PT-01` |
| 对应单元ID | `TRAIN-002` — Observation v2 编码 |
| 父测试合同 | `T-TRAIN-002-N01`、`T-TRAIN-002-B01`、`T-TRAIN-002-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `PlayerView + optional cognition`；向量引用`tests/spec_v3/vectors/train_002.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xee1721c06cdff440`；通过ALGO-011 `property_test/TRAIN-002/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_002_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_002.py::test_train_002_pt` |

## TC-TRAIN-002-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-002-PB-01` |
| 对应单元ID | `TRAIN-002` — Observation v2 编码 |
| 父测试合同 | `T-TRAIN-002-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `PlayerView + optional cognition`；向量引用`tests/spec_v3/vectors/train_002.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf21914963d24ad32`；通过ALGO-011 `property_test/TRAIN-002/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_002.py::test_train_002_pb` |

## TC-TRAIN-002-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-002-SM-01` |
| 对应单元ID | `TRAIN-002` — Observation v2 编码 |
| 父测试合同 | `T-TRAIN-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `PlayerView + optional cognition`；向量引用`tests/spec_v3/vectors/train_002.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xeb86dff5be3447d8`；通过ALGO-011 `property_test/TRAIN-002/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_002_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_002.py::test_train_002_sm` |

## TC-TRAIN-002-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-002-IT-01` |
| 对应单元ID | `TRAIN-002` — Observation v2 编码 |
| 父测试合同 | `T-TRAIN-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `PlayerView + optional cognition`；向量引用`tests/spec_v3/vectors/train_002.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x98583bc2207beddc`；通过ALGO-011 `property_test/TRAIN-002/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_002_it`对应路径 |
| 预期输出 | 通过生产入口得到`fixed observation`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_002.py::test_train_002_it` |

## TC-TRAIN-002-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-002-RR-01` |
| 对应单元ID | `TRAIN-002` — Observation v2 编码 |
| 父测试合同 | `T-TRAIN-002-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `PlayerView + optional cognition`；向量引用`tests/spec_v3/vectors/train_002.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe035cb92485e9526`；通过ALGO-011 `property_test/TRAIN-002/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=TRAIN-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_002.py::test_train_002_rr` |

## TC-TRAIN-002-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-002-PF-01` |
| 对应单元ID | `TRAIN-002` — Observation v2 编码 |
| 父测试合同 | `T-TRAIN-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `PlayerView + optional cognition`；向量引用`tests/spec_v3/vectors/train_002.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6122f9b975918d8d`；通过ALGO-011 `property_test/TRAIN-002/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_train_002.py::test_train_002_pf` |

## TC-TRAIN-002-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-002-HL-01` |
| 对应单元ID | `TRAIN-002` — Observation v2 编码 |
| 父测试合同 | `T-TRAIN-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `PlayerView + optional cognition`；向量引用`tests/spec_v3/vectors/train_002.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe58e8b4fab6ad88b`；通过ALGO-011 `property_test/TRAIN-002/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_train_002.py::test_train_002_hl` |

## TC-TRAIN-003-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-003-UT-01` |
| 对应单元ID | `TRAIN-003` — 固定动作 codec 与 legal mask |
| 父测试合同 | `T-TRAIN-003-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal actions`；向量引用`tests/spec_v3/vectors/train_003.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcf541edd72922142`；通过ALGO-011 `property_test/TRAIN-003/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_003_ut`对应路径 |
| 预期输出 | 返回批准schema的`action ids/mask`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_003.py::test_train_003_ut` |

## TC-TRAIN-003-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-003-BD-01` |
| 对应单元ID | `TRAIN-003` — 固定动作 codec 与 legal mask |
| 父测试合同 | `T-TRAIN-003-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal actions`；向量引用`tests/spec_v3/vectors/train_003.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb9937c96f46366d3`；通过ALGO-011 `property_test/TRAIN-003/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_003_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`action ids/mask`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_003.py::test_train_003_bd` |

## TC-TRAIN-003-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-003-PT-01` |
| 对应单元ID | `TRAIN-003` — 固定动作 codec 与 legal mask |
| 父测试合同 | `T-TRAIN-003-N01`、`T-TRAIN-003-B01`、`T-TRAIN-003-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal actions`；向量引用`tests/spec_v3/vectors/train_003.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x94972d101c0bedc8`；通过ALGO-011 `property_test/TRAIN-003/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_003_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_003.py::test_train_003_pt` |

## TC-TRAIN-003-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-003-PB-01` |
| 对应单元ID | `TRAIN-003` — 固定动作 codec 与 legal mask |
| 父测试合同 | `T-TRAIN-003-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal actions`；向量引用`tests/spec_v3/vectors/train_003.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4781ae41ffbcd7a2`；通过ALGO-011 `property_test/TRAIN-003/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_003.py::test_train_003_pb` |

## TC-TRAIN-003-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-003-SM-01` |
| 对应单元ID | `TRAIN-003` — 固定动作 codec 与 legal mask |
| 父测试合同 | `T-TRAIN-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `legal actions`；向量引用`tests/spec_v3/vectors/train_003.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbaedda02fee9df85`；通过ALGO-011 `property_test/TRAIN-003/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_003_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_003.py::test_train_003_sm` |

## TC-TRAIN-003-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-003-IT-01` |
| 对应单元ID | `TRAIN-003` — 固定动作 codec 与 legal mask |
| 父测试合同 | `T-TRAIN-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `legal actions`；向量引用`tests/spec_v3/vectors/train_003.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xae9928d4a56c144c`；通过ALGO-011 `property_test/TRAIN-003/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_003_it`对应路径 |
| 预期输出 | 通过生产入口得到`action ids/mask`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_003.py::test_train_003_it` |

## TC-TRAIN-003-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-003-RR-01` |
| 对应单元ID | `TRAIN-003` — 固定动作 codec 与 legal mask |
| 父测试合同 | `T-TRAIN-003-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal actions`；向量引用`tests/spec_v3/vectors/train_003.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4987ad85f58263f1`；通过ALGO-011 `property_test/TRAIN-003/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=TRAIN-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_003.py::test_train_003_rr` |

## TC-TRAIN-003-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-003-PF-01` |
| 对应单元ID | `TRAIN-003` — 固定动作 codec 与 legal mask |
| 父测试合同 | `T-TRAIN-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `legal actions`；向量引用`tests/spec_v3/vectors/train_003.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc8a75d415a594d55`；通过ALGO-011 `property_test/TRAIN-003/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_train_003.py::test_train_003_pf` |

## TC-TRAIN-003-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-003-HL-01` |
| 对应单元ID | `TRAIN-003` — 固定动作 codec 与 legal mask |
| 父测试合同 | `T-TRAIN-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `legal actions`；向量引用`tests/spec_v3/vectors/train_003.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x50cd912bacb62f63`；通过ALGO-011 `property_test/TRAIN-003/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_train_003.py::test_train_003_hl` |

## TC-TRAIN-004-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-004-UT-01` |
| 对应单元ID | `TRAIN-004` — 非法训练动作处理契约 |
| 父测试合同 | `T-TRAIN-004-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `action id + mask + mode`；向量引用`tests/spec_v3/vectors/train_004.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf9ed8a4b52bb7b79`；通过ALGO-011 `property_test/TRAIN-004/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_004_ut`对应路径 |
| 预期输出 | 返回批准schema的`raise/terminate/penalty`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_004.py::test_train_004_ut` |

## TC-TRAIN-004-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-004-BD-01` |
| 对应单元ID | `TRAIN-004` — 非法训练动作处理契约 |
| 父测试合同 | `T-TRAIN-004-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `action id + mask + mode`；向量引用`tests/spec_v3/vectors/train_004.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdf63e115d0fd8cd9`；通过ALGO-011 `property_test/TRAIN-004/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_004_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`raise/terminate/penalty`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_004.py::test_train_004_bd` |

## TC-TRAIN-004-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-004-PT-01` |
| 对应单元ID | `TRAIN-004` — 非法训练动作处理契约 |
| 父测试合同 | `T-TRAIN-004-N01`、`T-TRAIN-004-B01`、`T-TRAIN-004-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `action id + mask + mode`；向量引用`tests/spec_v3/vectors/train_004.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x96d61ece111f9487`；通过ALGO-011 `property_test/TRAIN-004/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_004_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_004.py::test_train_004_pt` |

## TC-TRAIN-004-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-004-PB-01` |
| 对应单元ID | `TRAIN-004` — 非法训练动作处理契约 |
| 父测试合同 | `T-TRAIN-004-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `action id + mask + mode`；向量引用`tests/spec_v3/vectors/train_004.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x84818ea0aaa3497b`；通过ALGO-011 `property_test/TRAIN-004/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_004.py::test_train_004_pb` |

## TC-TRAIN-004-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-004-SM-01` |
| 对应单元ID | `TRAIN-004` — 非法训练动作处理契约 |
| 父测试合同 | `T-TRAIN-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `action id + mask + mode`；向量引用`tests/spec_v3/vectors/train_004.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x987c7305eaffddcb`；通过ALGO-011 `property_test/TRAIN-004/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_004_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_004.py::test_train_004_sm` |

## TC-TRAIN-004-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-004-IT-01` |
| 对应单元ID | `TRAIN-004` — 非法训练动作处理契约 |
| 父测试合同 | `T-TRAIN-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `action id + mask + mode`；向量引用`tests/spec_v3/vectors/train_004.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x04446ada78568c56`；通过ALGO-011 `property_test/TRAIN-004/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_004_it`对应路径 |
| 预期输出 | 通过生产入口得到`raise/terminate/penalty`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_004.py::test_train_004_it` |

## TC-TRAIN-004-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-004-RR-01` |
| 对应单元ID | `TRAIN-004` — 非法训练动作处理契约 |
| 父测试合同 | `T-TRAIN-004-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `action id + mask + mode`；向量引用`tests/spec_v3/vectors/train_004.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc254425da78bd52e`；通过ALGO-011 `property_test/TRAIN-004/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=TRAIN-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_004.py::test_train_004_rr` |

## TC-TRAIN-004-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-004-PF-01` |
| 对应单元ID | `TRAIN-004` — 非法训练动作处理契约 |
| 父测试合同 | `T-TRAIN-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `action id + mask + mode`；向量引用`tests/spec_v3/vectors/train_004.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3dc5c128fbd53514`；通过ALGO-011 `property_test/TRAIN-004/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_train_004.py::test_train_004_pf` |

## TC-TRAIN-004-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-004-HL-01` |
| 对应单元ID | `TRAIN-004` — 非法训练动作处理契约 |
| 父测试合同 | `T-TRAIN-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `action id + mask + mode`；向量引用`tests/spec_v3/vectors/train_004.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa839b879bc7a87a7`；通过ALGO-011 `property_test/TRAIN-004/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_train_004.py::test_train_004_hl` |

## TC-TRAIN-005-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-005-UT-01` |
| 对应单元ID | `TRAIN-005` — 真实得分与可见势能奖励契约 |
| 父测试合同 | `T-TRAIN-005-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `transition + visible potential`；向量引用`tests/spec_v3/vectors/train_005.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xaae77ca414f37ab1`；通过ALGO-011 `property_test/TRAIN-005/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_005_ut`对应路径 |
| 预期输出 | 返回批准schema的`reward components`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_005.py::test_train_005_ut` |

## TC-TRAIN-005-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-005-BD-01` |
| 对应单元ID | `TRAIN-005` — 真实得分与可见势能奖励契约 |
| 父测试合同 | `T-TRAIN-005-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `transition + visible potential`；向量引用`tests/spec_v3/vectors/train_005.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x51480d06555bbd34`；通过ALGO-011 `property_test/TRAIN-005/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_005_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`reward components`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_005.py::test_train_005_bd` |

## TC-TRAIN-005-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-005-PT-01` |
| 对应单元ID | `TRAIN-005` — 真实得分与可见势能奖励契约 |
| 父测试合同 | `T-TRAIN-005-N01`、`T-TRAIN-005-B01`、`T-TRAIN-005-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `transition + visible potential`；向量引用`tests/spec_v3/vectors/train_005.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1ae47574758167f5`；通过ALGO-011 `property_test/TRAIN-005/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_005_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_005.py::test_train_005_pt` |

## TC-TRAIN-005-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-005-PB-01` |
| 对应单元ID | `TRAIN-005` — 真实得分与可见势能奖励契约 |
| 父测试合同 | `T-TRAIN-005-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `transition + visible potential`；向量引用`tests/spec_v3/vectors/train_005.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x944c878a49a47045`；通过ALGO-011 `property_test/TRAIN-005/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_005.py::test_train_005_pb` |

## TC-TRAIN-005-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-005-SM-01` |
| 对应单元ID | `TRAIN-005` — 真实得分与可见势能奖励契约 |
| 父测试合同 | `T-TRAIN-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `transition + visible potential`；向量引用`tests/spec_v3/vectors/train_005.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8a0339d9863d058a`；通过ALGO-011 `property_test/TRAIN-005/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_005_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_005.py::test_train_005_sm` |

## TC-TRAIN-005-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-005-IT-01` |
| 对应单元ID | `TRAIN-005` — 真实得分与可见势能奖励契约 |
| 父测试合同 | `T-TRAIN-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `transition + visible potential`；向量引用`tests/spec_v3/vectors/train_005.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa10aaf90bcc91357`；通过ALGO-011 `property_test/TRAIN-005/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_005_it`对应路径 |
| 预期输出 | 通过生产入口得到`reward components`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_005.py::test_train_005_it` |

## TC-TRAIN-005-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-005-RR-01` |
| 对应单元ID | `TRAIN-005` — 真实得分与可见势能奖励契约 |
| 父测试合同 | `T-TRAIN-005-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `transition + visible potential`；向量引用`tests/spec_v3/vectors/train_005.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf7b88e93a2b24d1d`；通过ALGO-011 `property_test/TRAIN-005/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=TRAIN-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_005.py::test_train_005_rr` |

## TC-TRAIN-005-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-005-SD-01` |
| 对应单元ID | `TRAIN-005` — 真实得分与可见势能奖励契约 |
| 父测试合同 | `T-TRAIN-005-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `transition + visible potential`；向量引用`tests/spec_v3/vectors/train_005.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcbc290ff0237173a`；通过ALGO-011 `property_test/TRAIN-005/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_train_005.py::test_train_005_sd` |

## TC-TRAIN-005-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-005-PF-01` |
| 对应单元ID | `TRAIN-005` — 真实得分与可见势能奖励契约 |
| 父测试合同 | `T-TRAIN-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `transition + visible potential`；向量引用`tests/spec_v3/vectors/train_005.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcbaba66d05317bb1`；通过ALGO-011 `property_test/TRAIN-005/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_train_005.py::test_train_005_pf` |

## TC-TRAIN-005-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-005-HL-01` |
| 对应单元ID | `TRAIN-005` — 真实得分与可见势能奖励契约 |
| 父测试合同 | `T-TRAIN-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `transition + visible potential`；向量引用`tests/spec_v3/vectors/train_005.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb1fbaee80fb429dc`；通过ALGO-011 `property_test/TRAIN-005/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_train_005.py::test_train_005_hl` |

## TC-TRAIN-006-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-006-UT-01` |
| 对应单元ID | `TRAIN-006` — 单 learner reset/step/mask/clone/restore |
| 父测试合同 | `T-TRAIN-006-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `env state + learner action`；向量引用`tests/spec_v3/vectors/train_006.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x971ba4f436ca3182`；通过ALGO-011 `property_test/TRAIN-006/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_006_ut`对应路径 |
| 预期输出 | 返回批准schema的`transition/snapshot`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_006.py::test_train_006_ut` |

## TC-TRAIN-006-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-006-BD-01` |
| 对应单元ID | `TRAIN-006` — 单 learner reset/step/mask/clone/restore |
| 父测试合同 | `T-TRAIN-006-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `env state + learner action`；向量引用`tests/spec_v3/vectors/train_006.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa80b3b59c2ff9199`；通过ALGO-011 `property_test/TRAIN-006/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_006_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`transition/snapshot`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_006.py::test_train_006_bd` |

## TC-TRAIN-006-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-006-PT-01` |
| 对应单元ID | `TRAIN-006` — 单 learner reset/step/mask/clone/restore |
| 父测试合同 | `T-TRAIN-006-N01`、`T-TRAIN-006-B01`、`T-TRAIN-006-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `env state + learner action`；向量引用`tests/spec_v3/vectors/train_006.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x391d6c849e807fb5`；通过ALGO-011 `property_test/TRAIN-006/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_006_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_006.py::test_train_006_pt` |

## TC-TRAIN-006-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-006-PB-01` |
| 对应单元ID | `TRAIN-006` — 单 learner reset/step/mask/clone/restore |
| 父测试合同 | `T-TRAIN-006-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `env state + learner action`；向量引用`tests/spec_v3/vectors/train_006.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3cceb2ef2f19fc10`；通过ALGO-011 `property_test/TRAIN-006/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_006.py::test_train_006_pb` |

## TC-TRAIN-006-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-006-SM-01` |
| 对应单元ID | `TRAIN-006` — 单 learner reset/step/mask/clone/restore |
| 父测试合同 | `T-TRAIN-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `env state + learner action`；向量引用`tests/spec_v3/vectors/train_006.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x920330be85bda69d`；通过ALGO-011 `property_test/TRAIN-006/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_006_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_006.py::test_train_006_sm` |

## TC-TRAIN-006-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-006-IT-01` |
| 对应单元ID | `TRAIN-006` — 单 learner reset/step/mask/clone/restore |
| 父测试合同 | `T-TRAIN-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `env state + learner action`；向量引用`tests/spec_v3/vectors/train_006.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x95f8b8058d49e856`；通过ALGO-011 `property_test/TRAIN-006/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_006_it`对应路径 |
| 预期输出 | 通过生产入口得到`transition/snapshot`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_006.py::test_train_006_it` |

## TC-TRAIN-006-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-006-RR-01` |
| 对应单元ID | `TRAIN-006` — 单 learner reset/step/mask/clone/restore |
| 父测试合同 | `T-TRAIN-006-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `env state + learner action`；向量引用`tests/spec_v3/vectors/train_006.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x51f4d04fbed7cdd2`；通过ALGO-011 `property_test/TRAIN-006/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=TRAIN-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_006.py::test_train_006_rr` |

## TC-TRAIN-006-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-006-PF-01` |
| 对应单元ID | `TRAIN-006` — 单 learner reset/step/mask/clone/restore |
| 父测试合同 | `T-TRAIN-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `env state + learner action`；向量引用`tests/spec_v3/vectors/train_006.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x93309ccdaac16f90`；通过ALGO-011 `property_test/TRAIN-006/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_train_006.py::test_train_006_pf` |

## TC-TRAIN-006-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-006-HL-01` |
| 对应单元ID | `TRAIN-006` — 单 learner reset/step/mask/clone/restore |
| 父测试合同 | `T-TRAIN-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `env state + learner action`；向量引用`tests/spec_v3/vectors/train_006.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3f85995103178454`；通过ALGO-011 `property_test/TRAIN-006/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_train_006.py::test_train_006_hl` |

## TC-TRAIN-007-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-007-UT-01` |
| 对应单元ID | `TRAIN-007` — 多玩家 ActionMap 与自博弈调度 |
| 父测试合同 | `T-TRAIN-007-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `joint observations/actions`；向量引用`tests/spec_v3/vectors/train_007.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x79469ed283593c0e`；通过ALGO-011 `property_test/TRAIN-007/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_007_ut`对应路径 |
| 预期输出 | 返回批准schema的`joint transition`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_007.py::test_train_007_ut` |

## TC-TRAIN-007-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-007-BD-01` |
| 对应单元ID | `TRAIN-007` — 多玩家 ActionMap 与自博弈调度 |
| 父测试合同 | `T-TRAIN-007-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `joint observations/actions`；向量引用`tests/spec_v3/vectors/train_007.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x01802ff835e19a1c`；通过ALGO-011 `property_test/TRAIN-007/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_007_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`joint transition`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_007.py::test_train_007_bd` |

## TC-TRAIN-007-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-007-PT-01` |
| 对应单元ID | `TRAIN-007` — 多玩家 ActionMap 与自博弈调度 |
| 父测试合同 | `T-TRAIN-007-N01`、`T-TRAIN-007-B01`、`T-TRAIN-007-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `joint observations/actions`；向量引用`tests/spec_v3/vectors/train_007.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf641cc4885c9b67f`；通过ALGO-011 `property_test/TRAIN-007/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_007_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_007.py::test_train_007_pt` |

## TC-TRAIN-007-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-007-PB-01` |
| 对应单元ID | `TRAIN-007` — 多玩家 ActionMap 与自博弈调度 |
| 父测试合同 | `T-TRAIN-007-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `joint observations/actions`；向量引用`tests/spec_v3/vectors/train_007.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8842c67174055450`；通过ALGO-011 `property_test/TRAIN-007/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_007.py::test_train_007_pb` |

## TC-TRAIN-007-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-007-SM-01` |
| 对应单元ID | `TRAIN-007` — 多玩家 ActionMap 与自博弈调度 |
| 父测试合同 | `T-TRAIN-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `joint observations/actions`；向量引用`tests/spec_v3/vectors/train_007.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2a6588447f9ccd41`；通过ALGO-011 `property_test/TRAIN-007/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_007_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_007.py::test_train_007_sm` |

## TC-TRAIN-007-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-007-IT-01` |
| 对应单元ID | `TRAIN-007` — 多玩家 ActionMap 与自博弈调度 |
| 父测试合同 | `T-TRAIN-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `joint observations/actions`；向量引用`tests/spec_v3/vectors/train_007.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9a87e6f77527055e`；通过ALGO-011 `property_test/TRAIN-007/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_007_it`对应路径 |
| 预期输出 | 通过生产入口得到`joint transition`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_007.py::test_train_007_it` |

## TC-TRAIN-007-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-007-RR-01` |
| 对应单元ID | `TRAIN-007` — 多玩家 ActionMap 与自博弈调度 |
| 父测试合同 | `T-TRAIN-007-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `joint observations/actions`；向量引用`tests/spec_v3/vectors/train_007.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x131c977cc8583969`；通过ALGO-011 `property_test/TRAIN-007/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=TRAIN-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_007.py::test_train_007_rr` |

## TC-TRAIN-007-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-007-SD-01` |
| 对应单元ID | `TRAIN-007` — 多玩家 ActionMap 与自博弈调度 |
| 父测试合同 | `T-TRAIN-007-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `joint observations/actions`；向量引用`tests/spec_v3/vectors/train_007.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x54f9fdbcfcc8af20`；通过ALGO-011 `property_test/TRAIN-007/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_train_007.py::test_train_007_sd` |

## TC-TRAIN-007-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-007-PF-01` |
| 对应单元ID | `TRAIN-007` — 多玩家 ActionMap 与自博弈调度 |
| 父测试合同 | `T-TRAIN-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `joint observations/actions`；向量引用`tests/spec_v3/vectors/train_007.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xee4809f5d5efbe1c`；通过ALGO-011 `property_test/TRAIN-007/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_train_007.py::test_train_007_pf` |

## TC-TRAIN-007-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-007-HL-01` |
| 对应单元ID | `TRAIN-007` — 多玩家 ActionMap 与自博弈调度 |
| 父测试合同 | `T-TRAIN-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `joint observations/actions`；向量引用`tests/spec_v3/vectors/train_007.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x550fb6865cb8c313`；通过ALGO-011 `property_test/TRAIN-007/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_train_007.py::test_train_007_hl` |

## TC-TRAIN-008-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-008-UT-01` |
| 对应单元ID | `TRAIN-008` — 离线 BC 与回放 RL 数据消费 |
| 父测试合同 | `T-TRAIN-008-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `versioned trajectories`；向量引用`tests/spec_v3/vectors/train_008.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x45befb7a345990c7`；通过ALGO-011 `property_test/TRAIN-008/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_008_ut`对应路径 |
| 预期输出 | 返回批准schema的`batches/updates`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_008.py::test_train_008_ut` |

## TC-TRAIN-008-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-008-BD-01` |
| 对应单元ID | `TRAIN-008` — 离线 BC 与回放 RL 数据消费 |
| 父测试合同 | `T-TRAIN-008-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `versioned trajectories`；向量引用`tests/spec_v3/vectors/train_008.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1b07c8e91c7f3f9c`；通过ALGO-011 `property_test/TRAIN-008/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_008_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`batches/updates`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_008.py::test_train_008_bd` |

## TC-TRAIN-008-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-008-PT-01` |
| 对应单元ID | `TRAIN-008` — 离线 BC 与回放 RL 数据消费 |
| 父测试合同 | `T-TRAIN-008-N01`、`T-TRAIN-008-B01`、`T-TRAIN-008-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `versioned trajectories`；向量引用`tests/spec_v3/vectors/train_008.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x32ba646a66203e1f`；通过ALGO-011 `property_test/TRAIN-008/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_008_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_008.py::test_train_008_pt` |

## TC-TRAIN-008-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-008-PB-01` |
| 对应单元ID | `TRAIN-008` — 离线 BC 与回放 RL 数据消费 |
| 父测试合同 | `T-TRAIN-008-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `versioned trajectories`；向量引用`tests/spec_v3/vectors/train_008.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc1f17a8d6c90588c`；通过ALGO-011 `property_test/TRAIN-008/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_008.py::test_train_008_pb` |

## TC-TRAIN-008-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-008-SM-01` |
| 对应单元ID | `TRAIN-008` — 离线 BC 与回放 RL 数据消费 |
| 父测试合同 | `T-TRAIN-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `versioned trajectories`；向量引用`tests/spec_v3/vectors/train_008.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdf02620bb8db8184`；通过ALGO-011 `property_test/TRAIN-008/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_008_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_008.py::test_train_008_sm` |

## TC-TRAIN-008-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-008-IT-01` |
| 对应单元ID | `TRAIN-008` — 离线 BC 与回放 RL 数据消费 |
| 父测试合同 | `T-TRAIN-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `versioned trajectories`；向量引用`tests/spec_v3/vectors/train_008.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x84af3867d4c892c9`；通过ALGO-011 `property_test/TRAIN-008/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_008_it`对应路径 |
| 预期输出 | 通过生产入口得到`batches/updates`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_008.py::test_train_008_it` |

## TC-TRAIN-008-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-008-RR-01` |
| 对应单元ID | `TRAIN-008` — 离线 BC 与回放 RL 数据消费 |
| 父测试合同 | `T-TRAIN-008-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `versioned trajectories`；向量引用`tests/spec_v3/vectors/train_008.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x934ae58cdf71249d`；通过ALGO-011 `property_test/TRAIN-008/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=TRAIN-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_008.py::test_train_008_rr` |

## TC-TRAIN-008-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-008-PF-01` |
| 对应单元ID | `TRAIN-008` — 离线 BC 与回放 RL 数据消费 |
| 父测试合同 | `T-TRAIN-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `versioned trajectories`；向量引用`tests/spec_v3/vectors/train_008.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7595fa653bbf15a1`；通过ALGO-011 `property_test/TRAIN-008/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_train_008.py::test_train_008_pf` |

## TC-TRAIN-008-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-008-HL-01` |
| 对应单元ID | `TRAIN-008` — 离线 BC 与回放 RL 数据消费 |
| 父测试合同 | `T-TRAIN-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `versioned trajectories`；向量引用`tests/spec_v3/vectors/train_008.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe86896fb11cab8d4`；通过ALGO-011 `property_test/TRAIN-008/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_train_008.py::test_train_008_hl` |

## TC-TRAIN-009-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-009-UT-01` |
| 对应单元ID | `TRAIN-009` — 房规、profile 与行为域随机化 |
| 父测试合同 | `T-TRAIN-009-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `domain seed + allowed ranges`；向量引用`tests/spec_v3/vectors/train_009.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe65a97447d668d75`；通过ALGO-011 `property_test/TRAIN-009/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_009_ut`对应路径 |
| 预期输出 | 返回批准schema的`sampled domain`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_009.py::test_train_009_ut` |

## TC-TRAIN-009-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-009-BD-01` |
| 对应单元ID | `TRAIN-009` — 房规、profile 与行为域随机化 |
| 父测试合同 | `T-TRAIN-009-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `domain seed + allowed ranges`；向量引用`tests/spec_v3/vectors/train_009.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5beabf152fb405f8`；通过ALGO-011 `property_test/TRAIN-009/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_009_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`sampled domain`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_009.py::test_train_009_bd` |

## TC-TRAIN-009-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-009-PT-01` |
| 对应单元ID | `TRAIN-009` — 房规、profile 与行为域随机化 |
| 父测试合同 | `T-TRAIN-009-N01`、`T-TRAIN-009-B01`、`T-TRAIN-009-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `domain seed + allowed ranges`；向量引用`tests/spec_v3/vectors/train_009.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2114c30a647f2d79`；通过ALGO-011 `property_test/TRAIN-009/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_009_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_009.py::test_train_009_pt` |

## TC-TRAIN-009-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-009-PB-01` |
| 对应单元ID | `TRAIN-009` — 房规、profile 与行为域随机化 |
| 父测试合同 | `T-TRAIN-009-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `domain seed + allowed ranges`；向量引用`tests/spec_v3/vectors/train_009.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf6df3ebe2ef34d11`；通过ALGO-011 `property_test/TRAIN-009/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_009.py::test_train_009_pb` |

## TC-TRAIN-009-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-009-SM-01` |
| 对应单元ID | `TRAIN-009` — 房规、profile 与行为域随机化 |
| 父测试合同 | `T-TRAIN-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `domain seed + allowed ranges`；向量引用`tests/spec_v3/vectors/train_009.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x861e0b3e119e3062`；通过ALGO-011 `property_test/TRAIN-009/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_009_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_009.py::test_train_009_sm` |

## TC-TRAIN-009-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-009-IT-01` |
| 对应单元ID | `TRAIN-009` — 房规、profile 与行为域随机化 |
| 父测试合同 | `T-TRAIN-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `domain seed + allowed ranges`；向量引用`tests/spec_v3/vectors/train_009.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5710dffef12ed1b8`；通过ALGO-011 `property_test/TRAIN-009/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_train_009_it`对应路径 |
| 预期输出 | 通过生产入口得到`sampled domain`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=TRAIN-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_009.py::test_train_009_it` |

## TC-TRAIN-009-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-009-RR-01` |
| 对应单元ID | `TRAIN-009` — 房规、profile 与行为域随机化 |
| 父测试合同 | `T-TRAIN-009-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `domain seed + allowed ranges`；向量引用`tests/spec_v3/vectors/train_009.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x76be0365dc2322a3`；通过ALGO-011 `property_test/TRAIN-009/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=TRAIN-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_train_009.py::test_train_009_rr` |

## TC-TRAIN-009-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-009-SD-01` |
| 对应单元ID | `TRAIN-009` — 房规、profile 与行为域随机化 |
| 父测试合同 | `T-TRAIN-009-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `domain seed + allowed ranges`；向量引用`tests/spec_v3/vectors/train_009.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf9b6d978c93a0089`；通过ALGO-011 `property_test/TRAIN-009/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_train_009.py::test_train_009_sd` |

## TC-TRAIN-009-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-009-PF-01` |
| 对应单元ID | `TRAIN-009` — 房规、profile 与行为域随机化 |
| 父测试合同 | `T-TRAIN-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `domain seed + allowed ranges`；向量引用`tests/spec_v3/vectors/train_009.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdb6a68bf4afe0820`；通过ALGO-011 `property_test/TRAIN-009/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_train_009.py::test_train_009_pf` |

## TC-TRAIN-009-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-TRAIN-009-HL-01` |
| 对应单元ID | `TRAIN-009` — 房规、profile 与行为域随机化 |
| 父测试合同 | `T-TRAIN-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `domain seed + allowed ranges`；向量引用`tests/spec_v3/vectors/train_009.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6fa95454b1f6d3a1`；通过ALGO-011 `property_test/TRAIN-009/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=TRAIN-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_train_009.py::test_train_009_hl` |

## TC-AUDIT-001-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-001-UT-01` |
| 对应单元ID | `AUDIT-001` — 全原子规则事件日志 |
| 父测试合同 | `T-AUDIT-001-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state transition`；向量引用`tests/spec_v3/vectors/audit_001.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7aaec379c3b4f2db`；通过ALGO-011 `property_test/AUDIT-001/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_001_ut`对应路径 |
| 预期输出 | 返回批准schema的`public payload/private refs`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_001.py::test_audit_001_ut` |

## TC-AUDIT-001-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-001-BD-01` |
| 对应单元ID | `AUDIT-001` — 全原子规则事件日志 |
| 父测试合同 | `T-AUDIT-001-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state transition`；向量引用`tests/spec_v3/vectors/audit_001.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x249fc6f8976b9c7e`；通过ALGO-011 `property_test/AUDIT-001/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_001_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`public payload/private refs`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_001.py::test_audit_001_bd` |

## TC-AUDIT-001-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-001-PT-01` |
| 对应单元ID | `AUDIT-001` — 全原子规则事件日志 |
| 父测试合同 | `T-AUDIT-001-N01`、`T-AUDIT-001-B01`、`T-AUDIT-001-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state transition`；向量引用`tests/spec_v3/vectors/audit_001.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xae904159a044460e`；通过ALGO-011 `property_test/AUDIT-001/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_001_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_001.py::test_audit_001_pt` |

## TC-AUDIT-001-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-001-PB-01` |
| 对应单元ID | `AUDIT-001` — 全原子规则事件日志 |
| 父测试合同 | `T-AUDIT-001-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state transition`；向量引用`tests/spec_v3/vectors/audit_001.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x406d902fa69abb1d`；通过ALGO-011 `property_test/AUDIT-001/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_001.py::test_audit_001_pb` |

## TC-AUDIT-001-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-001-SM-01` |
| 对应单元ID | `AUDIT-001` — 全原子规则事件日志 |
| 父测试合同 | `T-AUDIT-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `state transition`；向量引用`tests/spec_v3/vectors/audit_001.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2d071f77d3b6bb07`；通过ALGO-011 `property_test/AUDIT-001/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_001_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_001.py::test_audit_001_sm` |

## TC-AUDIT-001-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-001-IT-01` |
| 对应单元ID | `AUDIT-001` — 全原子规则事件日志 |
| 父测试合同 | `T-AUDIT-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `state transition`；向量引用`tests/spec_v3/vectors/audit_001.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6143731c2178cec7`；通过ALGO-011 `property_test/AUDIT-001/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_001_it`对应路径 |
| 预期输出 | 通过生产入口得到`public payload/private refs`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_001.py::test_audit_001_it` |

## TC-AUDIT-001-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-001-RR-01` |
| 对应单元ID | `AUDIT-001` — 全原子规则事件日志 |
| 父测试合同 | `T-AUDIT-001-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state transition`；向量引用`tests/spec_v3/vectors/audit_001.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x05cbd21cffc26178`；通过ALGO-011 `property_test/AUDIT-001/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_001.py::test_audit_001_rr` |

## TC-AUDIT-001-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-001-PF-01` |
| 对应单元ID | `AUDIT-001` — 全原子规则事件日志 |
| 父测试合同 | `T-AUDIT-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `state transition`；向量引用`tests/spec_v3/vectors/audit_001.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x15bc4487495da2b9`；通过ALGO-011 `property_test/AUDIT-001/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_001.py::test_audit_001_pf` |

## TC-AUDIT-001-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-001-HL-01` |
| 对应单元ID | `AUDIT-001` — 全原子规则事件日志 |
| 父测试合同 | `T-AUDIT-001-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `state transition`；向量引用`tests/spec_v3/vectors/audit_001.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb0aab11b1f577eb8`；通过ALGO-011 `property_test/AUDIT-001/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-001、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_001.py::test_audit_001_hl` |

## TC-AUDIT-002-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-002-UT-01` |
| 对应单元ID | `AUDIT-002` — AI 决策解释日志 |
| 父测试合同 | `T-AUDIT-002-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `decision pipeline`；向量引用`tests/spec_v3/vectors/audit_002.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0c71a5bfa7db000f`；通过ALGO-011 `property_test/AUDIT-002/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_002_ut`对应路径 |
| 预期输出 | 返回批准schema的`view/memory/plan/scores/action trace`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_002.py::test_audit_002_ut` |

## TC-AUDIT-002-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-002-BD-01` |
| 对应单元ID | `AUDIT-002` — AI 决策解释日志 |
| 父测试合同 | `T-AUDIT-002-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `decision pipeline`；向量引用`tests/spec_v3/vectors/audit_002.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x160a72442e1daf7e`；通过ALGO-011 `property_test/AUDIT-002/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_002_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`view/memory/plan/scores/action trace`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_002.py::test_audit_002_bd` |

## TC-AUDIT-002-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-002-PT-01` |
| 对应单元ID | `AUDIT-002` — AI 决策解释日志 |
| 父测试合同 | `T-AUDIT-002-N01`、`T-AUDIT-002-B01`、`T-AUDIT-002-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `decision pipeline`；向量引用`tests/spec_v3/vectors/audit_002.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd69cc18fdb7626a6`；通过ALGO-011 `property_test/AUDIT-002/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_002_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_002.py::test_audit_002_pt` |

## TC-AUDIT-002-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-002-PB-01` |
| 对应单元ID | `AUDIT-002` — AI 决策解释日志 |
| 父测试合同 | `T-AUDIT-002-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `decision pipeline`；向量引用`tests/spec_v3/vectors/audit_002.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe04abe7abf89bc82`；通过ALGO-011 `property_test/AUDIT-002/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_002.py::test_audit_002_pb` |

## TC-AUDIT-002-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-002-SM-01` |
| 对应单元ID | `AUDIT-002` — AI 决策解释日志 |
| 父测试合同 | `T-AUDIT-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `decision pipeline`；向量引用`tests/spec_v3/vectors/audit_002.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcedbcac96939727d`；通过ALGO-011 `property_test/AUDIT-002/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_002_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_002.py::test_audit_002_sm` |

## TC-AUDIT-002-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-002-IT-01` |
| 对应单元ID | `AUDIT-002` — AI 决策解释日志 |
| 父测试合同 | `T-AUDIT-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `decision pipeline`；向量引用`tests/spec_v3/vectors/audit_002.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1c9e2950b1111df9`；通过ALGO-011 `property_test/AUDIT-002/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_002_it`对应路径 |
| 预期输出 | 通过生产入口得到`view/memory/plan/scores/action trace`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_002.py::test_audit_002_it` |

## TC-AUDIT-002-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-002-RR-01` |
| 对应单元ID | `AUDIT-002` — AI 决策解释日志 |
| 父测试合同 | `T-AUDIT-002-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `decision pipeline`；向量引用`tests/spec_v3/vectors/audit_002.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7e7255ae9b2e820d`；通过ALGO-011 `property_test/AUDIT-002/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_002.py::test_audit_002_rr` |

## TC-AUDIT-002-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-002-PF-01` |
| 对应单元ID | `AUDIT-002` — AI 决策解释日志 |
| 父测试合同 | `T-AUDIT-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `decision pipeline`；向量引用`tests/spec_v3/vectors/audit_002.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4d4fea20aaf0a040`；通过ALGO-011 `property_test/AUDIT-002/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_002.py::test_audit_002_pf` |

## TC-AUDIT-002-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-002-HL-01` |
| 对应单元ID | `AUDIT-002` — AI 决策解释日志 |
| 父测试合同 | `T-AUDIT-002-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `decision pipeline`；向量引用`tests/spec_v3/vectors/audit_002.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2e0e529032a3a1fa`；通过ALGO-011 `property_test/AUDIT-002/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-002、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_002.py::test_audit_002_hl` |

## TC-AUDIT-003-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-003-UT-01` |
| 对应单元ID | `AUDIT-003` — canonical hash 链与篡改检测 |
| 父测试合同 | `T-AUDIT-003-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ordered records + hashes`；向量引用`tests/spec_v3/vectors/audit_003.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2947e7a0ec040e53`；通过ALGO-011 `property_test/AUDIT-003/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_003_ut`对应路径 |
| 预期输出 | 返回批准schema的`verified/rejected`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_003.py::test_audit_003_ut` |

## TC-AUDIT-003-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-003-BD-01` |
| 对应单元ID | `AUDIT-003` — canonical hash 链与篡改检测 |
| 父测试合同 | `T-AUDIT-003-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ordered records + hashes`；向量引用`tests/spec_v3/vectors/audit_003.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0882b9edaf41f7ff`；通过ALGO-011 `property_test/AUDIT-003/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_003_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`verified/rejected`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_003.py::test_audit_003_bd` |

## TC-AUDIT-003-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-003-PT-01` |
| 对应单元ID | `AUDIT-003` — canonical hash 链与篡改检测 |
| 父测试合同 | `T-AUDIT-003-N01`、`T-AUDIT-003-B01`、`T-AUDIT-003-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ordered records + hashes`；向量引用`tests/spec_v3/vectors/audit_003.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf2a361dd3e5faa14`；通过ALGO-011 `property_test/AUDIT-003/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_003_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_003.py::test_audit_003_pt` |

## TC-AUDIT-003-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-003-PB-01` |
| 对应单元ID | `AUDIT-003` — canonical hash 链与篡改检测 |
| 父测试合同 | `T-AUDIT-003-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ordered records + hashes`；向量引用`tests/spec_v3/vectors/audit_003.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6ddd371298db5b08`；通过ALGO-011 `property_test/AUDIT-003/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_003.py::test_audit_003_pb` |

## TC-AUDIT-003-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-003-SM-01` |
| 对应单元ID | `AUDIT-003` — canonical hash 链与篡改检测 |
| 父测试合同 | `T-AUDIT-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `ordered records + hashes`；向量引用`tests/spec_v3/vectors/audit_003.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5876227295d4ef81`；通过ALGO-011 `property_test/AUDIT-003/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_003_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_003.py::test_audit_003_sm` |

## TC-AUDIT-003-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-003-IT-01` |
| 对应单元ID | `AUDIT-003` — canonical hash 链与篡改检测 |
| 父测试合同 | `T-AUDIT-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `ordered records + hashes`；向量引用`tests/spec_v3/vectors/audit_003.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x025be4ab1eda39da`；通过ALGO-011 `property_test/AUDIT-003/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_003_it`对应路径 |
| 预期输出 | 通过生产入口得到`verified/rejected`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_003.py::test_audit_003_it` |

## TC-AUDIT-003-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-003-RR-01` |
| 对应单元ID | `AUDIT-003` — canonical hash 链与篡改检测 |
| 父测试合同 | `T-AUDIT-003-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ordered records + hashes`；向量引用`tests/spec_v3/vectors/audit_003.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x615ea94aa52d2593`；通过ALGO-011 `property_test/AUDIT-003/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_003.py::test_audit_003_rr` |

## TC-AUDIT-003-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-003-PF-01` |
| 对应单元ID | `AUDIT-003` — canonical hash 链与篡改检测 |
| 父测试合同 | `T-AUDIT-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `ordered records + hashes`；向量引用`tests/spec_v3/vectors/audit_003.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x2c26aefb182db81e`；通过ALGO-011 `property_test/AUDIT-003/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_003.py::test_audit_003_pf` |

## TC-AUDIT-003-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-003-HL-01` |
| 对应单元ID | `AUDIT-003` — canonical hash 链与篡改检测 |
| 父测试合同 | `T-AUDIT-003-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `ordered records + hashes`；向量引用`tests/spec_v3/vectors/audit_003.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x91e01cfedb3b1562`；通过ALGO-011 `property_test/AUDIT-003/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-003、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_003.py::test_audit_003_hl` |

## TC-AUDIT-004-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-004-UT-01` |
| 对应单元ID | `AUDIT-004` — 同配置/seed/事件的确定性回放 |
| 父测试合同 | `T-AUDIT-004-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained artifact`；向量引用`tests/spec_v3/vectors/audit_004.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x693f849c2bea0de6`；通过ALGO-011 `property_test/AUDIT-004/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_004_ut`对应路径 |
| 预期输出 | 返回批准schema的`replay comparison`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_004.py::test_audit_004_ut` |

## TC-AUDIT-004-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-004-BD-01` |
| 对应单元ID | `AUDIT-004` — 同配置/seed/事件的确定性回放 |
| 父测试合同 | `T-AUDIT-004-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained artifact`；向量引用`tests/spec_v3/vectors/audit_004.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x52ca58c4212dd65c`；通过ALGO-011 `property_test/AUDIT-004/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_004_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`replay comparison`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_004.py::test_audit_004_bd` |

## TC-AUDIT-004-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-004-PT-01` |
| 对应单元ID | `AUDIT-004` — 同配置/seed/事件的确定性回放 |
| 父测试合同 | `T-AUDIT-004-N01`、`T-AUDIT-004-B01`、`T-AUDIT-004-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained artifact`；向量引用`tests/spec_v3/vectors/audit_004.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x183fcc8e847d61d7`；通过ALGO-011 `property_test/AUDIT-004/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_004_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_004.py::test_audit_004_pt` |

## TC-AUDIT-004-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-004-PB-01` |
| 对应单元ID | `AUDIT-004` — 同配置/seed/事件的确定性回放 |
| 父测试合同 | `T-AUDIT-004-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained artifact`；向量引用`tests/spec_v3/vectors/audit_004.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xfda3b24014c0ec45`；通过ALGO-011 `property_test/AUDIT-004/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_004.py::test_audit_004_pb` |

## TC-AUDIT-004-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-004-SM-01` |
| 对应单元ID | `AUDIT-004` — 同配置/seed/事件的确定性回放 |
| 父测试合同 | `T-AUDIT-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `retained artifact`；向量引用`tests/spec_v3/vectors/audit_004.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5694b487ac12f512`；通过ALGO-011 `property_test/AUDIT-004/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_004_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_004.py::test_audit_004_sm` |

## TC-AUDIT-004-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-004-IT-01` |
| 对应单元ID | `AUDIT-004` — 同配置/seed/事件的确定性回放 |
| 父测试合同 | `T-AUDIT-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `retained artifact`；向量引用`tests/spec_v3/vectors/audit_004.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x318a7fa9a30adf0d`；通过ALGO-011 `property_test/AUDIT-004/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_004_it`对应路径 |
| 预期输出 | 通过生产入口得到`replay comparison`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_004.py::test_audit_004_it` |

## TC-AUDIT-004-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-004-RR-01` |
| 对应单元ID | `AUDIT-004` — 同配置/seed/事件的确定性回放 |
| 父测试合同 | `T-AUDIT-004-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained artifact`；向量引用`tests/spec_v3/vectors/audit_004.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xeb6ae83ee00a430d`；通过ALGO-011 `property_test/AUDIT-004/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_004.py::test_audit_004_rr` |

## TC-AUDIT-004-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-004-PF-01` |
| 对应单元ID | `AUDIT-004` — 同配置/seed/事件的确定性回放 |
| 父测试合同 | `T-AUDIT-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained artifact`；向量引用`tests/spec_v3/vectors/audit_004.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x52bb7eb7326b25a3`；通过ALGO-011 `property_test/AUDIT-004/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_004.py::test_audit_004_pf` |

## TC-AUDIT-004-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-004-HL-01` |
| 对应单元ID | `AUDIT-004` — 同配置/seed/事件的确定性回放 |
| 父测试合同 | `T-AUDIT-004-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `retained artifact`；向量引用`tests/spec_v3/vectors/audit_004.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3e4a6c5aa219a1a4`；通过ALGO-011 `property_test/AUDIT-004/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-004、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_004.py::test_audit_004_hl` |

## TC-AUDIT-005-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-005-UT-01` |
| 对应单元ID | `AUDIT-005` — 每事件强制不变量执行 |
| 父测试合同 | `T-AUDIT-005-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `post-event state`；向量引用`tests/spec_v3/vectors/audit_005.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbb5be54e088d1094`；通过ALGO-011 `property_test/AUDIT-005/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_005_ut`对应路径 |
| 预期输出 | 返回批准schema的`pass or explicit failure`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_005.py::test_audit_005_ut` |

## TC-AUDIT-005-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-005-BD-01` |
| 对应单元ID | `AUDIT-005` — 每事件强制不变量执行 |
| 父测试合同 | `T-AUDIT-005-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `post-event state`；向量引用`tests/spec_v3/vectors/audit_005.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x28cdaf676f629a3c`；通过ALGO-011 `property_test/AUDIT-005/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_005_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`pass or explicit failure`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_005.py::test_audit_005_bd` |

## TC-AUDIT-005-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-005-PT-01` |
| 对应单元ID | `AUDIT-005` — 每事件强制不变量执行 |
| 父测试合同 | `T-AUDIT-005-N01`、`T-AUDIT-005-B01`、`T-AUDIT-005-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `post-event state`；向量引用`tests/spec_v3/vectors/audit_005.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x391256c0995d0d6d`；通过ALGO-011 `property_test/AUDIT-005/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_005_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_005.py::test_audit_005_pt` |

## TC-AUDIT-005-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-005-PB-01` |
| 对应单元ID | `AUDIT-005` — 每事件强制不变量执行 |
| 父测试合同 | `T-AUDIT-005-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `post-event state`；向量引用`tests/spec_v3/vectors/audit_005.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8aadb50043dde5ea`；通过ALGO-011 `property_test/AUDIT-005/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_005.py::test_audit_005_pb` |

## TC-AUDIT-005-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-005-SM-01` |
| 对应单元ID | `AUDIT-005` — 每事件强制不变量执行 |
| 父测试合同 | `T-AUDIT-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `post-event state`；向量引用`tests/spec_v3/vectors/audit_005.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x41c86495d9d283d4`；通过ALGO-011 `property_test/AUDIT-005/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_005_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_005.py::test_audit_005_sm` |

## TC-AUDIT-005-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-005-IT-01` |
| 对应单元ID | `AUDIT-005` — 每事件强制不变量执行 |
| 父测试合同 | `T-AUDIT-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `post-event state`；向量引用`tests/spec_v3/vectors/audit_005.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb24d1a1cfac1c38a`；通过ALGO-011 `property_test/AUDIT-005/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_005_it`对应路径 |
| 预期输出 | 通过生产入口得到`pass or explicit failure`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_005.py::test_audit_005_it` |

## TC-AUDIT-005-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-005-RR-01` |
| 对应单元ID | `AUDIT-005` — 每事件强制不变量执行 |
| 父测试合同 | `T-AUDIT-005-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `post-event state`；向量引用`tests/spec_v3/vectors/audit_005.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x980c65466b221bdd`；通过ALGO-011 `property_test/AUDIT-005/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_005.py::test_audit_005_rr` |

## TC-AUDIT-005-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-005-PF-01` |
| 对应单元ID | `AUDIT-005` — 每事件强制不变量执行 |
| 父测试合同 | `T-AUDIT-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `post-event state`；向量引用`tests/spec_v3/vectors/audit_005.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb1478cd3241f3c5a`；通过ALGO-011 `property_test/AUDIT-005/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_005.py::test_audit_005_pf` |

## TC-AUDIT-005-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-005-HL-01` |
| 对应单元ID | `AUDIT-005` — 每事件强制不变量执行 |
| 父测试合同 | `T-AUDIT-005-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `post-event state`；向量引用`tests/spec_v3/vectors/audit_005.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4a58bcdd8491d397`；通过ALGO-011 `property_test/AUDIT-005/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-005、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_005.py::test_audit_005_hl` |

## TC-AUDIT-006-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-006-UT-01` |
| 对应单元ID | `AUDIT-006` — 直接规则与接口测试证据门禁 |
| 父测试合同 | `T-AUDIT-006-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `assertion catalog + test results`；向量引用`tests/spec_v3/vectors/audit_006.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xfdeb945ee479565f`；通过ALGO-011 `property_test/AUDIT-006/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_006_ut`对应路径 |
| 预期输出 | 返回批准schema的`coverage status`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_006.py::test_audit_006_ut` |

## TC-AUDIT-006-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-006-BD-01` |
| 对应单元ID | `AUDIT-006` — 直接规则与接口测试证据门禁 |
| 父测试合同 | `T-AUDIT-006-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `assertion catalog + test results`；向量引用`tests/spec_v3/vectors/audit_006.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9026fa8201bf1541`；通过ALGO-011 `property_test/AUDIT-006/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_006_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`coverage status`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_006.py::test_audit_006_bd` |

## TC-AUDIT-006-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-006-PT-01` |
| 对应单元ID | `AUDIT-006` — 直接规则与接口测试证据门禁 |
| 父测试合同 | `T-AUDIT-006-N01`、`T-AUDIT-006-B01`、`T-AUDIT-006-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `assertion catalog + test results`；向量引用`tests/spec_v3/vectors/audit_006.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3ba6414cae543e1d`；通过ALGO-011 `property_test/AUDIT-006/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_006_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_006.py::test_audit_006_pt` |

## TC-AUDIT-006-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-006-PB-01` |
| 对应单元ID | `AUDIT-006` — 直接规则与接口测试证据门禁 |
| 父测试合同 | `T-AUDIT-006-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `assertion catalog + test results`；向量引用`tests/spec_v3/vectors/audit_006.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x95c4325ea0f1ac2b`；通过ALGO-011 `property_test/AUDIT-006/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_006.py::test_audit_006_pb` |

## TC-AUDIT-006-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-006-SM-01` |
| 对应单元ID | `AUDIT-006` — 直接规则与接口测试证据门禁 |
| 父测试合同 | `T-AUDIT-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `assertion catalog + test results`；向量引用`tests/spec_v3/vectors/audit_006.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf38d4c38b3c9f5b3`；通过ALGO-011 `property_test/AUDIT-006/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_006_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_006.py::test_audit_006_sm` |

## TC-AUDIT-006-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-006-IT-01` |
| 对应单元ID | `AUDIT-006` — 直接规则与接口测试证据门禁 |
| 父测试合同 | `T-AUDIT-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `assertion catalog + test results`；向量引用`tests/spec_v3/vectors/audit_006.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x020483b53a627b7b`；通过ALGO-011 `property_test/AUDIT-006/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_006_it`对应路径 |
| 预期输出 | 通过生产入口得到`coverage status`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_006.py::test_audit_006_it` |

## TC-AUDIT-006-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-006-RR-01` |
| 对应单元ID | `AUDIT-006` — 直接规则与接口测试证据门禁 |
| 父测试合同 | `T-AUDIT-006-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `assertion catalog + test results`；向量引用`tests/spec_v3/vectors/audit_006.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5c48adeb21148178`；通过ALGO-011 `property_test/AUDIT-006/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_006.py::test_audit_006_rr` |

## TC-AUDIT-006-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-006-PF-01` |
| 对应单元ID | `AUDIT-006` — 直接规则与接口测试证据门禁 |
| 父测试合同 | `T-AUDIT-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `assertion catalog + test results`；向量引用`tests/spec_v3/vectors/audit_006.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdd7c0b6b1c6741cd`；通过ALGO-011 `property_test/AUDIT-006/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_006.py::test_audit_006_pf` |

## TC-AUDIT-006-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-006-HL-01` |
| 对应单元ID | `AUDIT-006` — 直接规则与接口测试证据门禁 |
| 父测试合同 | `T-AUDIT-006-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `assertion catalog + test results`；向量引用`tests/spec_v3/vectors/audit_006.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc171ec8b13f4d919`；通过ALGO-011 `property_test/AUDIT-006/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-006、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_006.py::test_audit_006_hl` |

## TC-AUDIT-007-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-007-UT-01` |
| 对应单元ID | `AUDIT-007` — 属性式生成、缩减与不变量证据 |
| 父测试合同 | `T-AUDIT-007-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `generators + seeds`；向量引用`tests/spec_v3/vectors/audit_007.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1e0a920fa0a22129`；通过ALGO-011 `property_test/AUDIT-007/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_007_ut`对应路径 |
| 预期输出 | 返回批准schema的`minimized failures/report`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_007.py::test_audit_007_ut` |

## TC-AUDIT-007-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-007-BD-01` |
| 对应单元ID | `AUDIT-007` — 属性式生成、缩减与不变量证据 |
| 父测试合同 | `T-AUDIT-007-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `generators + seeds`；向量引用`tests/spec_v3/vectors/audit_007.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8d95fafa4e003cc9`；通过ALGO-011 `property_test/AUDIT-007/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_007_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`minimized failures/report`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_007.py::test_audit_007_bd` |

## TC-AUDIT-007-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-007-PT-01` |
| 对应单元ID | `AUDIT-007` — 属性式生成、缩减与不变量证据 |
| 父测试合同 | `T-AUDIT-007-N01`、`T-AUDIT-007-B01`、`T-AUDIT-007-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `generators + seeds`；向量引用`tests/spec_v3/vectors/audit_007.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x31cc63df9059c828`；通过ALGO-011 `property_test/AUDIT-007/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_007_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_007.py::test_audit_007_pt` |

## TC-AUDIT-007-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-007-PB-01` |
| 对应单元ID | `AUDIT-007` — 属性式生成、缩减与不变量证据 |
| 父测试合同 | `T-AUDIT-007-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `generators + seeds`；向量引用`tests/spec_v3/vectors/audit_007.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7ccea5fdf589a3f7`；通过ALGO-011 `property_test/AUDIT-007/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_007.py::test_audit_007_pb` |

## TC-AUDIT-007-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-007-SM-01` |
| 对应单元ID | `AUDIT-007` — 属性式生成、缩减与不变量证据 |
| 父测试合同 | `T-AUDIT-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `generators + seeds`；向量引用`tests/spec_v3/vectors/audit_007.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xef8df3e98bd77b16`；通过ALGO-011 `property_test/AUDIT-007/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_007_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_007.py::test_audit_007_sm` |

## TC-AUDIT-007-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-007-IT-01` |
| 对应单元ID | `AUDIT-007` — 属性式生成、缩减与不变量证据 |
| 父测试合同 | `T-AUDIT-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `generators + seeds`；向量引用`tests/spec_v3/vectors/audit_007.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf44d79e538e460de`；通过ALGO-011 `property_test/AUDIT-007/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_007_it`对应路径 |
| 预期输出 | 通过生产入口得到`minimized failures/report`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_007.py::test_audit_007_it` |

## TC-AUDIT-007-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-007-RR-01` |
| 对应单元ID | `AUDIT-007` — 属性式生成、缩减与不变量证据 |
| 父测试合同 | `T-AUDIT-007-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `generators + seeds`；向量引用`tests/spec_v3/vectors/audit_007.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf94304f6d31075ce`；通过ALGO-011 `property_test/AUDIT-007/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_007.py::test_audit_007_rr` |

## TC-AUDIT-007-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-007-SD-01` |
| 对应单元ID | `AUDIT-007` — 属性式生成、缩减与不变量证据 |
| 父测试合同 | `T-AUDIT-007-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `generators + seeds`；向量引用`tests/spec_v3/vectors/audit_007.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6aa2575bf27c3aec`；通过ALGO-011 `property_test/AUDIT-007/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_audit_007.py::test_audit_007_sd` |

## TC-AUDIT-007-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-007-PF-01` |
| 对应单元ID | `AUDIT-007` — 属性式生成、缩减与不变量证据 |
| 父测试合同 | `T-AUDIT-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `generators + seeds`；向量引用`tests/spec_v3/vectors/audit_007.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x851e43d19f2c1494`；通过ALGO-011 `property_test/AUDIT-007/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_007.py::test_audit_007_pf` |

## TC-AUDIT-007-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-007-HL-01` |
| 对应单元ID | `AUDIT-007` — 属性式生成、缩减与不变量证据 |
| 父测试合同 | `T-AUDIT-007-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `generators + seeds`；向量引用`tests/spec_v3/vectors/audit_007.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5d8086caa3666278`；通过ALGO-011 `property_test/AUDIT-007/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-007、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_007.py::test_audit_007_hl` |

## TC-AUDIT-008-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-008-UT-01` |
| 对应单元ID | `AUDIT-008` — 锁定来源逐章 golden-case 对照 |
| 父测试合同 | `T-AUDIT-008-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source clauses + cases`；向量引用`tests/spec_v3/vectors/audit_008.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1319b31bf8f07145`；通过ALGO-011 `property_test/AUDIT-008/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_008_ut`对应路径 |
| 预期输出 | 返回批准schema的`per-clause result`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_008.py::test_audit_008_ut` |

## TC-AUDIT-008-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-008-BD-01` |
| 对应单元ID | `AUDIT-008` — 锁定来源逐章 golden-case 对照 |
| 父测试合同 | `T-AUDIT-008-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source clauses + cases`；向量引用`tests/spec_v3/vectors/audit_008.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4a30e096335bb9ee`；通过ALGO-011 `property_test/AUDIT-008/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_008_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`per-clause result`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_008.py::test_audit_008_bd` |

## TC-AUDIT-008-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-008-PT-01` |
| 对应单元ID | `AUDIT-008` — 锁定来源逐章 golden-case 对照 |
| 父测试合同 | `T-AUDIT-008-N01`、`T-AUDIT-008-B01`、`T-AUDIT-008-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source clauses + cases`；向量引用`tests/spec_v3/vectors/audit_008.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdcac12d49b1678df`；通过ALGO-011 `property_test/AUDIT-008/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_008_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_008.py::test_audit_008_pt` |

## TC-AUDIT-008-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-008-PB-01` |
| 对应单元ID | `AUDIT-008` — 锁定来源逐章 golden-case 对照 |
| 父测试合同 | `T-AUDIT-008-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source clauses + cases`；向量引用`tests/spec_v3/vectors/audit_008.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x05507cf9ec4308ea`；通过ALGO-011 `property_test/AUDIT-008/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_008.py::test_audit_008_pb` |

## TC-AUDIT-008-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-008-SM-01` |
| 对应单元ID | `AUDIT-008` — 锁定来源逐章 golden-case 对照 |
| 父测试合同 | `T-AUDIT-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `source clauses + cases`；向量引用`tests/spec_v3/vectors/audit_008.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4be5f089f547e03e`；通过ALGO-011 `property_test/AUDIT-008/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_008_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_008.py::test_audit_008_sm` |

## TC-AUDIT-008-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-008-IT-01` |
| 对应单元ID | `AUDIT-008` — 锁定来源逐章 golden-case 对照 |
| 父测试合同 | `T-AUDIT-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `source clauses + cases`；向量引用`tests/spec_v3/vectors/audit_008.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xa4bf370c561ccd4d`；通过ALGO-011 `property_test/AUDIT-008/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_008_it`对应路径 |
| 预期输出 | 通过生产入口得到`per-clause result`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_008.py::test_audit_008_it` |

## TC-AUDIT-008-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-008-RR-01` |
| 对应单元ID | `AUDIT-008` — 锁定来源逐章 golden-case 对照 |
| 父测试合同 | `T-AUDIT-008-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source clauses + cases`；向量引用`tests/spec_v3/vectors/audit_008.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf24cfab2a15e30f4`；通过ALGO-011 `property_test/AUDIT-008/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_008.py::test_audit_008_rr` |

## TC-AUDIT-008-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-008-PF-01` |
| 对应单元ID | `AUDIT-008` — 锁定来源逐章 golden-case 对照 |
| 父测试合同 | `T-AUDIT-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source clauses + cases`；向量引用`tests/spec_v3/vectors/audit_008.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x299ac407cb13ee59`；通过ALGO-011 `property_test/AUDIT-008/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_008.py::test_audit_008_pf` |

## TC-AUDIT-008-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-008-HL-01` |
| 对应单元ID | `AUDIT-008` — 锁定来源逐章 golden-case 对照 |
| 父测试合同 | `T-AUDIT-008-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `source clauses + cases`；向量引用`tests/spec_v3/vectors/audit_008.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7403dad8f7f1f4c4`；通过ALGO-011 `property_test/AUDIT-008/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-008、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_008.py::test_audit_008_hl` |

## TC-AUDIT-009-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-009-UT-01` |
| 对应单元ID | `AUDIT-009` — 工程与行为回归指标 |
| 父测试合同 | `T-AUDIT-009-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained runs`；向量引用`tests/spec_v3/vectors/audit_009.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7cddb31217309328`；通过ALGO-011 `property_test/AUDIT-009/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_009_ut`对应路径 |
| 预期输出 | 返回批准schema的`metric report/CI`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_009.py::test_audit_009_ut` |

## TC-AUDIT-009-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-009-BD-01` |
| 对应单元ID | `AUDIT-009` — 工程与行为回归指标 |
| 父测试合同 | `T-AUDIT-009-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained runs`；向量引用`tests/spec_v3/vectors/audit_009.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb7970ad90715a8f8`；通过ALGO-011 `property_test/AUDIT-009/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_009_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`metric report/CI`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_009.py::test_audit_009_bd` |

## TC-AUDIT-009-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-009-PT-01` |
| 对应单元ID | `AUDIT-009` — 工程与行为回归指标 |
| 父测试合同 | `T-AUDIT-009-N01`、`T-AUDIT-009-B01`、`T-AUDIT-009-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained runs`；向量引用`tests/spec_v3/vectors/audit_009.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x17507e6cd68b537b`；通过ALGO-011 `property_test/AUDIT-009/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_009_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_009.py::test_audit_009_pt` |

## TC-AUDIT-009-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-009-PB-01` |
| 对应单元ID | `AUDIT-009` — 工程与行为回归指标 |
| 父测试合同 | `T-AUDIT-009-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained runs`；向量引用`tests/spec_v3/vectors/audit_009.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x550221e8f3439073`；通过ALGO-011 `property_test/AUDIT-009/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_009.py::test_audit_009_pb` |

## TC-AUDIT-009-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-009-SM-01` |
| 对应单元ID | `AUDIT-009` — 工程与行为回归指标 |
| 父测试合同 | `T-AUDIT-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `retained runs`；向量引用`tests/spec_v3/vectors/audit_009.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbcd0f55df1161502`；通过ALGO-011 `property_test/AUDIT-009/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_009_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_009.py::test_audit_009_sm` |

## TC-AUDIT-009-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-009-IT-01` |
| 对应单元ID | `AUDIT-009` — 工程与行为回归指标 |
| 父测试合同 | `T-AUDIT-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `retained runs`；向量引用`tests/spec_v3/vectors/audit_009.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3e7f63165dbc20d3`；通过ALGO-011 `property_test/AUDIT-009/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_009_it`对应路径 |
| 预期输出 | 通过生产入口得到`metric report/CI`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_009.py::test_audit_009_it` |

## TC-AUDIT-009-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-009-RR-01` |
| 对应单元ID | `AUDIT-009` — 工程与行为回归指标 |
| 父测试合同 | `T-AUDIT-009-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained runs`；向量引用`tests/spec_v3/vectors/audit_009.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x971c98645aca259a`；通过ALGO-011 `property_test/AUDIT-009/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_009.py::test_audit_009_rr` |

## TC-AUDIT-009-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-009-SD-01` |
| 对应单元ID | `AUDIT-009` — 工程与行为回归指标 |
| 父测试合同 | `T-AUDIT-009-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained runs`；向量引用`tests/spec_v3/vectors/audit_009.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x66c1cf3a14c0c37d`；通过ALGO-011 `property_test/AUDIT-009/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_audit_009.py::test_audit_009_sd` |

## TC-AUDIT-009-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-009-PF-01` |
| 对应单元ID | `AUDIT-009` — 工程与行为回归指标 |
| 父测试合同 | `T-AUDIT-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `retained runs`；向量引用`tests/spec_v3/vectors/audit_009.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x740ae127c305446f`；通过ALGO-011 `property_test/AUDIT-009/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_009.py::test_audit_009_pf` |

## TC-AUDIT-009-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-009-HL-01` |
| 对应单元ID | `AUDIT-009` — 工程与行为回归指标 |
| 父测试合同 | `T-AUDIT-009-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `retained runs`；向量引用`tests/spec_v3/vectors/audit_009.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5fa91b4888c5dbc3`；通过ALGO-011 `property_test/AUDIT-009/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-009、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_009.py::test_audit_009_hl` |

## TC-AUDIT-010-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-010-UT-01` |
| 对应单元ID | `AUDIT-010` — 来源→参数→实现→测试全链追踪 |
| 父测试合同 | `T-AUDIT-010-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `catalogs/manifests`；向量引用`tests/spec_v3/vectors/audit_010.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbf671bcc1f4a463a`；通过ALGO-011 `property_test/AUDIT-010/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_010_ut`对应路径 |
| 预期输出 | 返回批准schema的`trace matrix`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_010.py::test_audit_010_ut` |

## TC-AUDIT-010-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-010-BD-01` |
| 对应单元ID | `AUDIT-010` — 来源→参数→实现→测试全链追踪 |
| 父测试合同 | `T-AUDIT-010-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `catalogs/manifests`；向量引用`tests/spec_v3/vectors/audit_010.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6a1c5c62d54a9eb9`；通过ALGO-011 `property_test/AUDIT-010/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_010_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`trace matrix`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_010.py::test_audit_010_bd` |

## TC-AUDIT-010-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-010-PT-01` |
| 对应单元ID | `AUDIT-010` — 来源→参数→实现→测试全链追踪 |
| 父测试合同 | `T-AUDIT-010-N01`、`T-AUDIT-010-B01`、`T-AUDIT-010-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `catalogs/manifests`；向量引用`tests/spec_v3/vectors/audit_010.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x60203302704cf428`；通过ALGO-011 `property_test/AUDIT-010/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_010_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_010.py::test_audit_010_pt` |

## TC-AUDIT-010-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-010-PB-01` |
| 对应单元ID | `AUDIT-010` — 来源→参数→实现→测试全链追踪 |
| 父测试合同 | `T-AUDIT-010-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `catalogs/manifests`；向量引用`tests/spec_v3/vectors/audit_010.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x912800f2387e92c5`；通过ALGO-011 `property_test/AUDIT-010/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_010.py::test_audit_010_pb` |

## TC-AUDIT-010-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-010-SM-01` |
| 对应单元ID | `AUDIT-010` — 来源→参数→实现→测试全链追踪 |
| 父测试合同 | `T-AUDIT-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `catalogs/manifests`；向量引用`tests/spec_v3/vectors/audit_010.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x301e5b2b52f346d6`；通过ALGO-011 `property_test/AUDIT-010/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_010_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_010.py::test_audit_010_sm` |

## TC-AUDIT-010-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-010-IT-01` |
| 对应单元ID | `AUDIT-010` — 来源→参数→实现→测试全链追踪 |
| 父测试合同 | `T-AUDIT-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `catalogs/manifests`；向量引用`tests/spec_v3/vectors/audit_010.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x1fe9d7a4635ef2a6`；通过ALGO-011 `property_test/AUDIT-010/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_010_it`对应路径 |
| 预期输出 | 通过生产入口得到`trace matrix`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_010.py::test_audit_010_it` |

## TC-AUDIT-010-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-010-RR-01` |
| 对应单元ID | `AUDIT-010` — 来源→参数→实现→测试全链追踪 |
| 父测试合同 | `T-AUDIT-010-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `catalogs/manifests`；向量引用`tests/spec_v3/vectors/audit_010.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7306453462990455`；通过ALGO-011 `property_test/AUDIT-010/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_010.py::test_audit_010_rr` |

## TC-AUDIT-010-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-010-PF-01` |
| 对应单元ID | `AUDIT-010` — 来源→参数→实现→测试全链追踪 |
| 父测试合同 | `T-AUDIT-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `catalogs/manifests`；向量引用`tests/spec_v3/vectors/audit_010.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x8f624b8ba77ae65b`；通过ALGO-011 `property_test/AUDIT-010/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_010.py::test_audit_010_pf` |

## TC-AUDIT-010-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-010-HL-01` |
| 对应单元ID | `AUDIT-010` — 来源→参数→实现→测试全链追踪 |
| 父测试合同 | `T-AUDIT-010-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `catalogs/manifests`；向量引用`tests/spec_v3/vectors/audit_010.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xd0febe3b240e9f06`；通过ALGO-011 `property_test/AUDIT-010/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-010、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_010.py::test_audit_010_hl` |

## TC-AUDIT-011-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-011-UT-01` |
| 对应单元ID | `AUDIT-011` — 版本、迁移与发布物完整性 |
| 父测试合同 | `T-AUDIT-011-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `release candidate`；向量引用`tests/spec_v3/vectors/audit_011.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x665ff98ce16d4abb`；通过ALGO-011 `property_test/AUDIT-011/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_011_ut`对应路径 |
| 预期输出 | 返回批准schema的`manifest/gate result`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_011.py::test_audit_011_ut` |

## TC-AUDIT-011-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-011-BD-01` |
| 对应单元ID | `AUDIT-011` — 版本、迁移与发布物完整性 |
| 父测试合同 | `T-AUDIT-011-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `release candidate`；向量引用`tests/spec_v3/vectors/audit_011.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x27768d4630845a04`；通过ALGO-011 `property_test/AUDIT-011/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_011_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`manifest/gate result`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_011.py::test_audit_011_bd` |

## TC-AUDIT-011-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-011-PT-01` |
| 对应单元ID | `AUDIT-011` — 版本、迁移与发布物完整性 |
| 父测试合同 | `T-AUDIT-011-N01`、`T-AUDIT-011-B01`、`T-AUDIT-011-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `release candidate`；向量引用`tests/spec_v3/vectors/audit_011.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x67f9e2e40fac5751`；通过ALGO-011 `property_test/AUDIT-011/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_011_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_011.py::test_audit_011_pt` |

## TC-AUDIT-011-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-011-PB-01` |
| 对应单元ID | `AUDIT-011` — 版本、迁移与发布物完整性 |
| 父测试合同 | `T-AUDIT-011-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `release candidate`；向量引用`tests/spec_v3/vectors/audit_011.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x46d4b79038288025`；通过ALGO-011 `property_test/AUDIT-011/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_011.py::test_audit_011_pb` |

## TC-AUDIT-011-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-011-SM-01` |
| 对应单元ID | `AUDIT-011` — 版本、迁移与发布物完整性 |
| 父测试合同 | `T-AUDIT-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `release candidate`；向量引用`tests/spec_v3/vectors/audit_011.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x48e4ad90b7b44d17`；通过ALGO-011 `property_test/AUDIT-011/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_011_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_011.py::test_audit_011_sm` |

## TC-AUDIT-011-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-011-IT-01` |
| 对应单元ID | `AUDIT-011` — 版本、迁移与发布物完整性 |
| 父测试合同 | `T-AUDIT-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `release candidate`；向量引用`tests/spec_v3/vectors/audit_011.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x55471442949c5b77`；通过ALGO-011 `property_test/AUDIT-011/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_011_it`对应路径 |
| 预期输出 | 通过生产入口得到`manifest/gate result`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_011.py::test_audit_011_it` |

## TC-AUDIT-011-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-011-RR-01` |
| 对应单元ID | `AUDIT-011` — 版本、迁移与发布物完整性 |
| 父测试合同 | `T-AUDIT-011-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `release candidate`；向量引用`tests/spec_v3/vectors/audit_011.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xcb01e80aa3960da6`；通过ALGO-011 `property_test/AUDIT-011/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_011.py::test_audit_011_rr` |

## TC-AUDIT-011-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-011-PF-01` |
| 对应单元ID | `AUDIT-011` — 版本、迁移与发布物完整性 |
| 父测试合同 | `T-AUDIT-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `release candidate`；向量引用`tests/spec_v3/vectors/audit_011.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xef76348fc8c03233`；通过ALGO-011 `property_test/AUDIT-011/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_011.py::test_audit_011_pf` |

## TC-AUDIT-011-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-011-HL-01` |
| 对应单元ID | `AUDIT-011` — 版本、迁移与发布物完整性 |
| 父测试合同 | `T-AUDIT-011-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `release candidate`；向量引用`tests/spec_v3/vectors/audit_011.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x651f426e9a7dc547`；通过ALGO-011 `property_test/AUDIT-011/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-011、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_011.py::test_audit_011_hl` |

## TC-AUDIT-012-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-012-UT-01` |
| 对应单元ID | `AUDIT-012` — 强度、真人相似和学习效果外部评价 |
| 父测试合同 | `T-AUDIT-012-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `frozen datasets + policies`；向量引用`tests/spec_v3/vectors/audit_012.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3585f82fd2803524`；通过ALGO-011 `property_test/AUDIT-012/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_012_ut`对应路径 |
| 预期输出 | 返回批准schema的`statistics/CI`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_012.py::test_audit_012_ut` |

## TC-AUDIT-012-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-012-BD-01` |
| 对应单元ID | `AUDIT-012` — 强度、真人相似和学习效果外部评价 |
| 父测试合同 | `T-AUDIT-012-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `frozen datasets + policies`；向量引用`tests/spec_v3/vectors/audit_012.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x97efd9e40ea1fc6b`；通过ALGO-011 `property_test/AUDIT-012/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_012_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`statistics/CI`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_012.py::test_audit_012_bd` |

## TC-AUDIT-012-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-012-PT-01` |
| 对应单元ID | `AUDIT-012` — 强度、真人相似和学习效果外部评价 |
| 父测试合同 | `T-AUDIT-012-N01`、`T-AUDIT-012-B01`、`T-AUDIT-012-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `frozen datasets + policies`；向量引用`tests/spec_v3/vectors/audit_012.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x382486cee260a91c`；通过ALGO-011 `property_test/AUDIT-012/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_012_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_012.py::test_audit_012_pt` |

## TC-AUDIT-012-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-012-PB-01` |
| 对应单元ID | `AUDIT-012` — 强度、真人相似和学习效果外部评价 |
| 父测试合同 | `T-AUDIT-012-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `frozen datasets + policies`；向量引用`tests/spec_v3/vectors/audit_012.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x49080c7c34dbcd52`；通过ALGO-011 `property_test/AUDIT-012/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_012.py::test_audit_012_pb` |

## TC-AUDIT-012-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-012-SM-01` |
| 对应单元ID | `AUDIT-012` — 强度、真人相似和学习效果外部评价 |
| 父测试合同 | `T-AUDIT-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `frozen datasets + policies`；向量引用`tests/spec_v3/vectors/audit_012.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x929cbc2c32eb7a7b`；通过ALGO-011 `property_test/AUDIT-012/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_012_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_012.py::test_audit_012_sm` |

## TC-AUDIT-012-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-012-IT-01` |
| 对应单元ID | `AUDIT-012` — 强度、真人相似和学习效果外部评价 |
| 父测试合同 | `T-AUDIT-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `frozen datasets + policies`；向量引用`tests/spec_v3/vectors/audit_012.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc6e59e58fa1a5cfe`；通过ALGO-011 `property_test/AUDIT-012/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_012_it`对应路径 |
| 预期输出 | 通过生产入口得到`statistics/CI`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_012.py::test_audit_012_it` |

## TC-AUDIT-012-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-012-RR-01` |
| 对应单元ID | `AUDIT-012` — 强度、真人相似和学习效果外部评价 |
| 父测试合同 | `T-AUDIT-012-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `frozen datasets + policies`；向量引用`tests/spec_v3/vectors/audit_012.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xb1c25259f0b98227`；通过ALGO-011 `property_test/AUDIT-012/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_012.py::test_audit_012_rr` |

## TC-AUDIT-012-SD-01 — 统计分布测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-012-SD-01` |
| 对应单元ID | `AUDIT-012` — 强度、真人相似和学习效果外部评价 |
| 父测试合同 | `T-AUDIT-012-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `frozen datasets + policies`；向量引用`tests/spec_v3/vectors/audit_012.jsonl#case=sd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x00ab0ce7789f57ed`；通过ALGO-011 `property_test/AUDIT-012/SD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 按冻结样本量执行多seed批跑，计算分布与95% CI |
| 预期输出 | 允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作 |
| 允许误差 | 采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；记录sample_size/alpha/CI/metric/threshold；私有值仅受控引用 |
| 失败条件 | 样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现 |
| 自动化位置 | `tests/spec_v3/test_audit_012.py::test_audit_012_sd` |

## TC-AUDIT-012-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-012-PF-01` |
| 对应单元ID | `AUDIT-012` — 强度、真人相似和学习效果外部评价 |
| 父测试合同 | `T-AUDIT-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `frozen datasets + policies`；向量引用`tests/spec_v3/vectors/audit_012.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x58e2120bfed3ab3b`；通过ALGO-011 `property_test/AUDIT-012/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_012.py::test_audit_012_pf` |

## TC-AUDIT-012-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-012-HL-01` |
| 对应单元ID | `AUDIT-012` — 强度、真人相似和学习效果外部评价 |
| 父测试合同 | `T-AUDIT-012-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `frozen datasets + policies`；向量引用`tests/spec_v3/vectors/audit_012.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x7c6981ee3cde29a0`；通过ALGO-011 `property_test/AUDIT-012/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-012、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_012.py::test_audit_012_hl` |

## TC-AUDIT-013-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-013-UT-01` |
| 对应单元ID | `AUDIT-013` — 模块依赖、接口与信息流架构契约 |
| 父测试合同 | `T-AUDIT-013-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source graph + interfaces`；向量引用`tests/spec_v3/vectors/audit_013.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xbb975751da0a9807`；通过ALGO-011 `property_test/AUDIT-013/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_013_ut`对应路径 |
| 预期输出 | 返回批准schema的`violations/report`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_013.py::test_audit_013_ut` |

## TC-AUDIT-013-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-013-BD-01` |
| 对应单元ID | `AUDIT-013` — 模块依赖、接口与信息流架构契约 |
| 父测试合同 | `T-AUDIT-013-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source graph + interfaces`；向量引用`tests/spec_v3/vectors/audit_013.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xdf3eb3e54bb2f0e2`；通过ALGO-011 `property_test/AUDIT-013/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_013_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`violations/report`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_013.py::test_audit_013_bd` |

## TC-AUDIT-013-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-013-PT-01` |
| 对应单元ID | `AUDIT-013` — 模块依赖、接口与信息流架构契约 |
| 父测试合同 | `T-AUDIT-013-N01`、`T-AUDIT-013-B01`、`T-AUDIT-013-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source graph + interfaces`；向量引用`tests/spec_v3/vectors/audit_013.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xced595ed7771bc42`；通过ALGO-011 `property_test/AUDIT-013/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_013_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_013.py::test_audit_013_pt` |

## TC-AUDIT-013-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-013-PB-01` |
| 对应单元ID | `AUDIT-013` — 模块依赖、接口与信息流架构契约 |
| 父测试合同 | `T-AUDIT-013-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source graph + interfaces`；向量引用`tests/spec_v3/vectors/audit_013.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe389dd4a7253bc58`；通过ALGO-011 `property_test/AUDIT-013/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_013.py::test_audit_013_pb` |

## TC-AUDIT-013-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-013-SM-01` |
| 对应单元ID | `AUDIT-013` — 模块依赖、接口与信息流架构契约 |
| 父测试合同 | `T-AUDIT-013-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `source graph + interfaces`；向量引用`tests/spec_v3/vectors/audit_013.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe3694c4172649bbd`；通过ALGO-011 `property_test/AUDIT-013/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_013_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_013.py::test_audit_013_sm` |

## TC-AUDIT-013-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-013-IT-01` |
| 对应单元ID | `AUDIT-013` — 模块依赖、接口与信息流架构契约 |
| 父测试合同 | `T-AUDIT-013-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `source graph + interfaces`；向量引用`tests/spec_v3/vectors/audit_013.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x6c7fa6293209cbb4`；通过ALGO-011 `property_test/AUDIT-013/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_013_it`对应路径 |
| 预期输出 | 通过生产入口得到`violations/report`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_013.py::test_audit_013_it` |

## TC-AUDIT-013-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-013-RR-01` |
| 对应单元ID | `AUDIT-013` — 模块依赖、接口与信息流架构契约 |
| 父测试合同 | `T-AUDIT-013-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source graph + interfaces`；向量引用`tests/spec_v3/vectors/audit_013.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x0be534e6a7351a82`；通过ALGO-011 `property_test/AUDIT-013/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_013.py::test_audit_013_rr` |

## TC-AUDIT-013-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-013-PF-01` |
| 对应单元ID | `AUDIT-013` — 模块依赖、接口与信息流架构契约 |
| 父测试合同 | `T-AUDIT-013-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `source graph + interfaces`；向量引用`tests/spec_v3/vectors/audit_013.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xc3501e7ce8e6b972`；通过ALGO-011 `property_test/AUDIT-013/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_013.py::test_audit_013_pf` |

## TC-AUDIT-013-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-013-HL-01` |
| 对应单元ID | `AUDIT-013` — 模块依赖、接口与信息流架构契约 |
| 父测试合同 | `T-AUDIT-013-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `source graph + interfaces`；向量引用`tests/spec_v3/vectors/audit_013.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x3b4293d2c8cc33a0`；通过ALGO-011 `property_test/AUDIT-013/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-013、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_013.py::test_audit_013_hl` |

## TC-AUDIT-014-UT-01 — 单元测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-014-UT-01` |
| 对应单元ID | `AUDIT-014` — 证据数据保留、脱敏与新鲜度管理 |
| 父测试合同 | `T-AUDIT-014-N01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `run artifacts + policy`；向量引用`tests/spec_v3/vectors/audit_014.jsonl#case=ut01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x9054809af4b89e14`；通过ALGO-011 `property_test/AUDIT-014/UT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_014_ut`对应路径 |
| 预期输出 | 返回批准schema的`retained manifest`；正常向量与Approved oracle一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_014.py::test_audit_014_ut` |

## TC-AUDIT-014-BD-01 — 边界测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-014-BD-01` |
| 对应单元ID | `AUDIT-014` — 证据数据保留、脱敏与新鲜度管理 |
| 父测试合同 | `T-AUDIT-014-B01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `run artifacts + policy`；向量引用`tests/spec_v3/vectors/audit_014.jsonl#case=bd01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5b845aab0d96829c`；通过ALGO-011 `property_test/AUDIT-014/BD`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_014_bd`对应路径 |
| 预期输出 | 边界仍返回范围内`retained manifest`或稳定错误码，不截断、不猜默认值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_014.py::test_audit_014_bd` |

## TC-AUDIT-014-PT-01 — 参数化测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-014-PT-01` |
| 对应单元ID | `AUDIT-014` — 证据数据保留、脱敏与新鲜度管理 |
| 父测试合同 | `T-AUDIT-014-N01`、`T-AUDIT-014-B01`、`T-AUDIT-014-I01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `run artifacts + policy`；向量引用`tests/spec_v3/vectors/audit_014.jsonl#case=pt01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x106cc79267c7acdc`；通过ALGO-011 `property_test/AUDIT-014/PT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_014_pt`对应路径 |
| 预期输出 | 所有参数行分别得到登记expected/error；case_id不得串扰 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_014.py::test_audit_014_pt` |

## TC-AUDIT-014-PB-01 — 属性测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-014-PB-01` |
| 对应单元ID | `AUDIT-014` — 证据数据保留、脱敏与新鲜度管理 |
| 父测试合同 | `T-AUDIT-014-P01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `run artifacts + policy`；向量引用`tests/spec_v3/vectors/audit_014.jsonl#case=pb01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x5deb6dbecad438e4`；通过ALGO-011 `property_test/AUDIT-014/PB`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 用固定命名seed生成≥100个合法样本并缩减失败例 |
| 预期输出 | 批准不变量在全部生成样本成立；失败输出固定seed与最小反例 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_014.py::test_audit_014_pb` |

## TC-AUDIT-014-SM-01 — 状态机测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-014-SM-01` |
| 对应单元ID | `AUDIT-014` — 证据数据保留、脱敏与新鲜度管理 |
| 父测试合同 | `T-AUDIT-014-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash |
| 输入 | `run artifacts + policy`；向量引用`tests/spec_v3/vectors/audit_014.jsonl#case=sm01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x54aabe4e44d19103`；通过ALGO-011 `property_test/AUDIT-014/SM`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_014_sm`对应路径 |
| 预期输出 | 仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_014.py::test_audit_014_sm` |

## TC-AUDIT-014-IT-01 — 集成测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-014-IT-01` |
| 对应单元ID | `AUDIT-014` — 证据数据保留、脱敏与新鲜度管理 |
| 父测试合同 | `T-AUDIT-014-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过 |
| 输入 | `run artifacts + policy`；向量引用`tests/spec_v3/vectors/audit_014.jsonl#case=it01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xe3cac284a258133f`；通过ALGO-011 `property_test/AUDIT-014/IT`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 调用生产门面执行`test_audit_014_it`对应路径 |
| 预期输出 | 通过生产入口得到`retained manifest`，上下游schema/version/hash一致 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash |
| 预期日志 | 至少含unit_id=AUDIT-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_014.py::test_audit_014_it` |

## TC-AUDIT-014-RR-01 — 随机回放测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-014-RR-01` |
| 对应单元ID | `AUDIT-014` — 证据数据保留、脱敏与新鲜度管理 |
| 父测试合同 | `T-AUDIT-014-R01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `run artifacts + policy`；向量引用`tests/spec_v3/vectors/audit_014.jsonl#case=rr01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x4ecc58be12be13d7`；通过ALGO-011 `property_test/AUDIT-014/RR`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 隔离进程执行两次完整路径并比较canonical产物 |
| 预期输出 | 同输入、配置、版本和seed的action/state/score/log逐字段相同 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 两次运行的完整状态序列逐event_index一致 |
| 预期日志 | 至少含unit_id=AUDIT-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现 |
| 自动化位置 | `tests/spec_v3/test_audit_014.py::test_audit_014_rr` |

## TC-AUDIT-014-PF-01 — 性能测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-014-PF-01` |
| 对应单元ID | `AUDIT-014` — 证据数据保留、脱敏与新鲜度管理 |
| 父测试合同 | `T-AUDIT-014-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash |
| 输入 | `run artifacts + policy`；向量引用`tests/spec_v3/vectors/audit_014.jsonl#case=pf01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0xf3dcb556e476157b`；通过ALGO-011 `property_test/AUDIT-014/PF`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | warm-up后在冻结环境运行基准批次并同时校验功能输出 |
| 预期输出 | 结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次 |
| 自动化位置 | `tests/spec_v3/test_audit_014.py::test_audit_014_pf` |

## TC-AUDIT-014-HL-01 — 隐藏信息泄漏测试

| 字段 | 内容 |
|---|---|
| 测试ID | `TC-AUDIT-014-HL-01` |
| 对应单元ID | `AUDIT-014` — 证据数据保留、脱敏与新鲜度管理 |
| 父测试合同 | `T-AUDIT-014-X01`；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | 一对公开信息完全相同、仅restricted truth不同的隔离状态 |
| 输入 | `run artifacts + policy`；向量引用`tests/spec_v3/vectors/audit_014.jsonl#case=hl01`；字段/范围以Approved单元规格为准 |
| 随机种子 | `0x26ee79afee621e0b`；通过ALGO-011 `property_test/AUDIT-014/HL`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | 构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分 |
| 预期输出 | 投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值 |
| 允许误差 | 整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差 |
| 预期状态变化 | 测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段 |
| 预期日志 | 至少含unit_id=AUDIT-014、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness；私有值仅受控引用 |
| 失败条件 | 投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用 |
| 自动化位置 | `tests/spec_v3/test_audit_014.py::test_audit_014_hl` |
# 3.0.1 试点High问题具体化规则

RULE-016、STATE-005、HEUR-019、MODEL-001、SCORE-001、AUDIT-003的TC必须直接引用`golden_vectors.md` 3.0.1 fixture，填写实际前置状态、完整输入、seed=`NONE`或指定命名seed、逐字段expected、稳定错误码、expected log与自动化测试符号；仅复制UT/BD/PT模板不得判为“测试规格完整”。其他90单元在进入实现批次前同样须完成该具体化门禁。
