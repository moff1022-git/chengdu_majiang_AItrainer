# Spec v3 规格可实施性反馈

## 结论

Locked规格足以提供领域目标、主要不变量和测试方向，但目前仍需要实施者解释若干关键空白。若目标是“任何开发者只读规格即可实现并达到AUDITED”，建议先修订，再批量开发。

## 发现

| ID      | 严重度    | 涉及单元               | 缺失或含糊内容                                                                                               | 试点处理                          | 建议修订                                       |
| ------- | ------ | ------------------ | ----------------------------------------------------------------------------------------------------- | ----------------------------- | ------------------------------------------ |
| SPF-001 | High   | 全类任务卡              | 建议路径如`engine/rules/rule_003.py`会与既有`engine/rules.py`产生Python导入遮蔽                                      | 保留现有模块并补入口                    | 明确兼容目录策略或统一迁移ADR                           |
| SPF-002 | High   | RULE-016、STATE-005 | “异常和错误码”与“测试要求”内容错位，且测试要求写为`undefined`                                                                | 从不变量和父测试合同推导测试                | 修正章节并给出稳定错误码到触发条件映射                        |
| SPF-003 | High   | 全部                 | 细化TC大量为通用模板，没有每条可直接执行的具体输入、seed、expected log与fixture                                                  | 在试点测试内人工具体化                   | 为每单元补机器可读golden/fixture引用                  |
| SPF-004 | Medium | RULE-003           | 纯查询的`next_state_version`可不变，但通用流程又称提交成功加1；合法出牌查询究竟是否写版本不唯一                                            | 沿用既有纯查询零写入                    | 明确query/command分类和版本规则                     |
| SPF-005 | Medium | ALGO-001           | 合法region枚举、过渡区集合及空region是否必须出现未定义                                                                     | 接受任意稳定字符串region               | 列出规范region enum与各phase所需region             |
| SPF-006 | High   | HEUR-019           | 基线公式中的`mandatory`数值编码、mandatory是否占K、风格/水平/阶段修正的具体组合顺序不完全明确                                            | mandatory取0/1且不占普通K；未虚构修正     | 明确计算图、裁剪顺序和golden样例                        |
| SPF-007 | High   | MODEL-001          | 最低校准阈值要求冻结数据集，但没有data release、样本下限、桶边界fixture或基线预测文件                                                  | 只实现规则回退，不宣称校准通过               | 指定评估manifest与可复现calibration fixture        |
| SPF-008 | High   | SCORE-001          | layer枚举、event schema、event_id幂等存储边界、hash链canonical字节未完整定义                                             | 实现原子守恒纯函数，不声称幂等完成             | 补JSON Schema、layer enum、事件存储接口和golden hash |
| SPF-009 | Medium | TRAIN-003          | 本卡未直接写固定动作空间N及全部action_id映射，只能依赖上游目录/既有v2 codec                                                       | 沿用已批准635 codec                | 在单元卡直接引用唯一codec表和版本                        |
| SPF-010 | High   | AUDIT-003          | 公式文字可理解为`SHA256(canonical(record_without_hash)+prev_hash)`，而record本身又含`previous_record_hash`，存在重复拼接解释 | 沿用已批准现有canonical record字段hash | 给出逐字节golden和是否额外拼接prev的明确公式                |
| SPF-011 | High   | 验收全局               | AC-04要求完整生产trace，试点新增纯函数即使行为正确也无法在不扩大业务接线范围时达到E4                                                      | 如实停在E3                        | 为试点定义“E3可实施性通过”与“E4生产接入通过”两阶段门禁            |
| SPF-012 | Medium | 日志/性能              | 单元卡给出日志字段和部分时限，但缺统一日志API、计时边界、硬件manifest与冷/热运行口径                                                      | 本轮仅保留JUnit运行证据                | 增加性能与日志执行规范及证据生成工具                         |

## 对规范等级的反馈

- 规范约束总体清楚：守恒、合法域、隐藏隔离、确定复现可直接成为hard assertion。
- 基线策略可实现，但HEUR/MODEL缺少完整fixture，不能把一次实现选择反写成唯一规范。
- 可调参数在单元卡多以范围出现，参数加载键、缺省来源和运行绑定证据仍需跨文档人工拼接。
- 可训练替换边界清楚；本试点没有用训练模型替代确定算法，也没有把规则回退的测试结果包装成模型质量。

## 建议决策

建议先处理SPF-001/002/003/006/007/008/010/011这些High项，再决定是否批量实施。若不修正文档，至少应形成Approved解释记录，否则不同开发者可能产生都“看似符合规格”但互不兼容的实现。

## 2026-07-29处理结果

用户已批准修订。SPF-001/002/003/006/007/008/010/011均已在`SPEC-V3-3.0.1`规范补丁中解决；其状态改为Resolved。SPF-004/005/009/012仍为Medium开放项，不阻止本补丁锁定，但在涉及单元进入生产E4前必须处理。

## 2026-07-29 Medium问题处理

SPF-004/005/009/012已分别通过RULE-003纯查询版本语义、ALGO-001完region枚举、TRAIN-003的635项codec表及统一JSONL/性能manifest口径解决。试点反馈Open Critical/High/Medium均为0。
