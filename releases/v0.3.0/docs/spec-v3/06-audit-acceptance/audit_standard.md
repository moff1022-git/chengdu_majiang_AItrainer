# Spec v3 审计与验收标准

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 适用范围 | 锁定目录全部96个功能单元 |
| 单元规格 | Approved |
| 测试父合同 | Approved |
| 当前实现验收 | Not Evaluated |

## 1. 目的与权威边界

本标准定义证据成熟度、逐单元验收检查和`AUDITED`最终判定，不复制业务公式或测试expected。业务行为服从Approved单元规格；测试方法服从Approved测试父合同及后续批准的细化目录；本标准只判断证据是否足以支持结论。

文件、类名、接口、TODO、mock返回、跳过测试、历史报告或未经保留的口头结果均不能单独证明实现通过。未知、缺失、过期和不适用必须显式记录，禁止默认为Passed。

## 2. 证据基本对象

最小证据记录必须包含：`evidence_id, unit_id, check_id, evidence_level, status, freshness, source_type, path_or_uri, symbol_or_nodeid, command, environment_manifest, code_commit, rule_version, parameter_version, config_hash, model_version, schema_version, seed_ref, input_hash, output_hash, artifact_hash, produced_at_utc, producer, reviewer, finding_ids`。

状态枚举：`Passed / Failed / Not Evaluated / N/A-approved`。新鲜度枚举：`current-run / retained-artifact / report-only / stale-cache`。`report-only`最高只能支持E2；`stale-cache`不能支持当前AUDITED。

## 3. E0—E5累计证据等级

| 等级 | 名称 | 必须具备 | 能支持的结论 | 明确不能证明 |
|---|---|---|---|---|
| E0 | 无证据 | 无可核查产物，或只有声明/TODO | 仅记录待办 | 规格、实现、测试、运行均不能通过 |
| E1 | 规格证据 | 锁定目录条目；Approved单元规格；Approved测试父合同；稳定ID/版本/hash | 需求与验收目标已冻结 | 不证明存在实现或测试 |
| E2 | 静态实现证据 | E1；非占位代码符号；稳定入口；实际调用方静态链；参数/状态/追踪绑定；静态架构与泄漏扫描 | 代码结构与绑定可审查 | 不证明代码被运行或行为正确 |
| E3 | 直接自动测试证据 | E2；当前受控环境中单元、边界、参数化、属性等必需直接测试通过；保存JUnit、命令、输入输出与hash | 单元行为在测试范围内通过 | 不证明生产完整流程实际调用、性能或系统回放 |
| E4 | 集成运行证据 | E3；生产入口完整流程实际调用；状态写回/账本/日志/追踪可核；同seed回放；性能；隐藏隔离；适用统计/校准达标 | 可支持该单元`AUDITED`候选结论 | 不自动支持真人相似、强度、学习效果或独立发布声明 |
| E5 | 独立/外部与发布证据 | E4；冻结数据/场景；盲测或独立复核；发布物manifest与签名；适用外部效果、跨平台、长期稳定性证据 | 可支持限定范围的发布、强度、真人相似或学习效果声明 | 不支持超出数据、版本、平台和时间范围的泛化声明 |

等级是累计的：缺少任一前级必要证据不得跃级。等级按单元和版本分别计算；新代码、规则、参数、模型、schema或关键依赖变更会使相关E3+证据过期，必须按影响图重跑。

## 4. 每单元14项强制检查

| 检查ID | 检查项 | Passed条件 | 最低等级 | hard |
|---|---|---|---:|---|
| AC-01 | 规格完整 | ID在Locked目录；单元与测试规格Approved；输入输出/状态/错误/不变量/指标定义无未决占位；代码/测试/运行证据占位允许保留 | E1 | 是 |
| AC-02 | 非占位实现 | 主要路径含真实算法/状态/效果；无`pass`、固定成功、空壳、仅协议、TODO替代行为或测试专用分支 | E2 | 是 |
| AC-03 | 代码入口 | 稳定公开/内部门面可从登记路径导入；schema/version/error契约一致 | E2 | 是 |
| AC-04 | 实际调用方 | 至少一个非测试生产调用方沿完整流程调用；调用边可由静态与运行trace共同证明 | E4 | 是 |
| AC-05 | 参数绑定 | GP/RP/配置键通过冻结loader进入单元；类型/范围/版本/hash可追踪，无未登记常量覆盖 | E2；运行确认E4 | 是 |
| AC-06 | 状态写回 | 纯函数明确无写回；有状态单元只经唯一权威入口原子提交，失败不变，版本/事件/账本一致 | E4 | 是 |
| AC-07 | 单元测试 | Approved N/UT及适用参数化/性质用例当前运行通过，直接断言正文行为 | E3 | 是 |
| AC-08 | 边界测试 | Approved B/BD、最小/最大/null/非法相邻边界通过，稳定错误且无部分提交 | E3 | 是 |
| AC-09 | 集成测试 | Approved X/IT通过生产门面，上下游schema/version/hash与依赖一致 | E4 | 是 |
| AC-10 | 运行日志 | 实际运行有输入/输出、seed、版本、hash、状态/错误、耗时和证据引用；私有字段受控 | E4 | 是 |
| AC-11 | 追踪关系 | 来源规则→GP/RP→单元→代码符号→测试ID→运行证据无断链 | E4 | 是 |
| AC-12 | 性能 | 冻结环境/样本下功能oracle不漂移，P50/P95/P99/吞吐/内存达到Approved预算 | E4 | 是 |
| AC-13 | 隐藏信息隔离 | 白名单、权限、静态扫描及成对truth投毒均通过；公开日志/错误/解释零泄漏 | E4 | 是 |
| AC-14 | 确定性或统计指标 | 确定单元同输入/状态/版本/seed完整复现；HEUR统计允许域；MODEL校准；TRAIN/AUDIT按卡指标 | E4；外部声明E5 | 是 |

“纯函数无状态写回”可以在AC-06中Passed，但必须用静态和运行证据证明无副作用，不能标N/A。所有14项均为hard，不允许用总分、覆盖率或其他强项抵消。

## 5. AUDITED通过条件

单元只有在同一`audit_scope=(unit_id, code_commit, rule_version, parameter_version, config_hash, model_version, schema_version, platform_scope)`下同时满足以下条件，才能标记`AUDITED`：

1. 规格已锁定：目录Locked，单元规格和必需测试规格Approved。
2. 实现不是框架、空壳、mock、固定返回或占位。
3. 全部必需测试当前运行通过；hard测试无skip、N/A或宽松xfail。
4. 在完整生产流程中被实际调用，调用前后trace连续。
5. 有可复核运行输入、输出、状态、日志、seed和hash证据。
6. 能追踪到来源规则、GP/RP或明确“无直接参数”，并继续到代码、测试、运行产物。
7. 当前范围无未关闭High/Critical缺陷；Medium必须有批准处置且不影响指标。
8. 功能、边界、状态、守恒、性能、隐藏隔离、确定性/统计/校准等全部适用指标达标。

此外：AC-01～AC-14全部Passed；证据至少E4；证据新鲜度为`current-run`或仍在批准有效期内的`retained-artifact`；AUDIT-003 hash链、AUDIT-004回放、AUDIT-010追踪和AUDIT-014保留检查通过。涉及强度、真人相似、学习效果、发布物或独立评价的声明必须达到E5。

`AUDITED`不是永久属性。任何scope键变化、证据过期、依赖单元降级或新High/Critical缺陷会自动变为`STALE`或`REVOKED`，等待重审。

## 6. 判定状态

| 状态 | 含义 |
|---|---|
| NOT_EVALUATED | 尚未执行或证据不足 |
| IN_REVIEW | 证据包完整性审查中，不能对外宣称通过 |
| FAILED | 至少一个hard检查失败或指标未达 |
| BLOCKED | 外部依赖/权限/冻结数据阻断，仍不是Passed |
| AUDITED | 同一scope下全部硬条件通过且至少E4 |
| AUDITED_E5 | AUDITED且适用外部/独立/发布证据达到E5 |
| STALE | 曾通过但版本、依赖或有效期变化 |
| REVOKED | 发现重大缺陷、伪证、泄漏或篡改后撤销 |

## 7. 方法类别的AC-14判定

| 类别 | AC-14最低判定 |
|---|---|
| RULE/STATE/SCORE | 同输入、初态、规则/config/code/schema和seed，事件、状态、分数、日志/hash逐字段相同；守恒适用项0误差 |
| ALGO | 规范golden、顺序置换、跨进程复算通过；确定算法未调用训练模型 |
| HEUR | 每seed可复现；非法/mandatory/泄漏为0；允许行为范围、方向效应、regret、分布及95% CI达Approved阈值，不强制唯一动作 |
| MODEL | 线上输入无truth；概率范围/归一化；冻结切分上的Brier、log loss、ECE、可靠性、不确定性和规则回退达标 |
| TRAIN | 生产转换等价；同seed回放/快照一致；reward全部追踪真实计分或显式势能；并行指标达标 |
| AUDIT | canonical结果确定；hard失败不误报；抽样/属性测试记录总体、seed和CI；证据链完整 |

## 8. 缺陷严重度与门禁

| 严重度 | 示例 | AUDITED处理 |
|---|---|---|
| Critical | 隐藏信息回流、计分不守恒、篡改未检出、规则绕过、不可恢复数据损坏 | 立即REVOKED，停止发布/训练数据流入 |
| High | 主要路径未调用、同seed不复现、错误状态提交、模型无回退、核心指标失败 | FAILED，不得AUDITED |
| Medium | 非核心边界偏差、性能接近预算、非敏感日志字段缺失 | 默认FAILED；仅经owner批准且证明不影响全部指标后限期处理 |
| Low | 文案、非功能元数据或不影响复现的改进项 | 可AUDITED但必须登记期限和owner |

## 9. 审计执行顺序

1. 冻结scope和依赖版本，验证来源hash。
2. AC-01规格/目录检查。
3. AC-02～06静态代码、入口、调用、参数和状态检查。
4. AC-07～09执行Approved直接/边界/集成测试。
5. AC-10～11核验运行日志与全链追踪。
6. AC-12～14执行性能、泄漏和确定/统计/校准验收。
7. 扫描缺陷与例外，验证证据新鲜度和hash链。
8. 两人规则：producer不得兼任final reviewer；生成签名报告。
9. AUDIT-014保留证据，更新追踪矩阵和单元状态。

## 10. 禁止的审计方式

- 用文件、类、函数、测试名称或导入成功证明行为实现。
- 用mock/self-test替代生产入口实际调用，或用生产实现复制测试oracle。
- 把历史报告、终端截图或未保留原产物升级为current-run E3/E4。
- 用总体覆盖率、平均分或低严重度多数抵消任一hard失败。
- 把Not Evaluated、Blocked、无数据或N/A当Passed。
- 隐藏失败样本、调低阈值、删除测试、永久skip或只报告最好运行。
- 让审计truth回流策略、模型线上特征、训练势能或权威状态。
- 覆盖、删除或重写已签失败记录；更正必须append superseding记录。

## 11. 关联文档

- [逐单元验收清单](acceptance_checklist.md)
- [证据包模板](evidence_template.md)
- [审计报告模板](audit_report_template.md)
- [测试策略](../05-test-spec/test_strategy.md)
- [96单元测试覆盖矩阵](../05-test-spec/coverage_matrix.csv)
- [AUDIT单元规格](../03-unit-specs/audit_specs.md)
# 3.0.1 可实施性试点与生产AUDITED两阶段门禁

## 3.0.2 统一日志与性能证据口径

单元运行证据必须为JSONL，每行至少含`timestamp_utc,run_id,event_id,unit_id,implementation_version,ruleset_hash,config_hash,input_hash,output_hash,accepted,error_code,latency_us,evidence_scope`；隐藏牌只记hash/受控引用。性能证据必须记录OS、Python、CPU、commit/worktree、冷启动次数、warmup、sample count和计时边界；使用`perf_counter_ns`，报告P50/P95/P99/max，至少1000个warm samples（明确更高成本单元可由卡内预算改写）。功能oracle在性能运行前后必须逐字段一致。未提供硬件manifest、样本不足或只报平均值时AC-性能保持Not Evaluated。

“试点可实施性通过”最高为E3：规格完整、非占位入口、单元/边界/属性或统计合同与current-run输入输出证据通过。它不等于AUDITED。生产AUDITED仍要求E4：同一scope内存在非测试生产调用边、完整流程trace、参数绑定、状态写回、集成、性能、隐藏隔离和追踪证据。报告必须分别给出`pilot_e3_status`与`production_audited_status`，禁止以试点E3豁免AC-04/05/09～14。
