# Task 18B-R2：B1-A九项阻断规格决策包

状态：**APPROVED / OPTION A × 9**  
范围：STATE-010、ALGO-009、ALGO-011。本文是决策提案，不修改Locked规格、Frozen契约、业务代码、测试断言或Task 17/18A状态。

## 技术摘要

项目负责人已于`2026-07-30T04:39:21Z`明确批准九项选项A，决策版本为`B1-A-DECISIONS 1.0.0`。批准优先保护PARAMS 1.1配置、legacy-v1回放及shuffle/dice/exchange结果。canonical新字节规范采用版本双轨：历史使用legacy-json-v1，新写配置使用NFC+RFC8785 JCS的v2；该选择改变canonical bytes，后续仍必须按versioning_policy完成`CDMJ-CONTRACTS 2.0.0`和参数迁移审批，规格决策批准本身不等于Frozen接口已变更。

Golden文件共19条向量。所有hash术语统一解释为：**SHA-256，32字节，序列化为64个小写十六进制字符。**

## SPEC-DECISION-STATE-DEFAULTS — 参数缺失、默认值与null

- approval_status：`APPROVED`（选项A；2026-07-30T04:39:21Z）
- 当前未决问题：60项定义有范围和生命周期，但嵌套字段required/default/nullable未结构化冻结。
- Locked来源：STATE-010 §§6,11,15；ALGO-009 §§5,7；common_contracts §§2,8；parameter_registry.csv
- 当前代码行为：Humanlike配置根/GP/profile多采用exact-key；EngineConfig.from_dict用get+强转默认；RP未初始化项用None。
- 兼容要求：默认配置PARAMS 1.1必须原样有效；不得把false、0或空集合当作缺失。

### 选项 A — 当前schema所有配置字段必填，仅GP-003.early_end_score可null；不对raw current配置补默认。RP用内部UNINITIALIZED而非序列化null。
- 优点：匹配现有Humanlike exact-key并消除歧义
- 缺点：旧EngineConfig宽松输入需适配层
- 版本影响：PARAMS 1.2 minor for structured registry metadata
### 选项 B — 对所有缺失字段从default.json补值。
- 优点：宽松
- 缺点：掩盖拼写/版本错误且无法区分缺失
- 版本影响：default语义变化至少MINOR

### 影响分析

- 向后兼容：默认PARAMS 1.1文件无变化；EngineConfig旧宽松入口保留legacy adapter但不得进入ALGO-009权威门禁。
- 跨语言：结构化字段表跨语言直接实现。
- 持久化：registry元数据新增可选default_present/nullable；现有配置JSON不变。
- 安全/隐藏信息：不改变PlayerView；私有配置不写入策略。
- 测试：五类输入分别断言accepted/error/result；60 ID闭集。
- 迁移：把parameter_registry生成结构化schema；不改现有值。
- 回滚：撤回新registry schema，继续现有loader；无数据回写。
- Frozen契约：COMPATIBLE_EXTENSION
- 版本：PARAMS 1.2.0（元数据）；CONTRACTS不变

### 推荐

推荐选项：**A**。最接近现有权威humanlike loader，并满足缺省与null不同。

### 需要批准的准确规范文字

> 对PARAMS 1.1 raw config：根字段、GP-001..023、四座profile及各座GP-024..027和其声明子字段全部必填；唯一允许显式null为GP-003.early_end_score。缺失必填=SCHEMA_INVALID，未知字段=PARAM_UNKNOWN，显式null不可空=PARAM_NULL，类型错误=PARAM_TYPE，闭区间外=PARAM_RANGE。false、0、空字符串和空集合按实际值校验。RP未到创建时点使用内部UNINITIALIZED，不序列化为null；到时点后必须有领域值。

### Golden

- 正向：GV-001
- 反向：GV-002
## SPEC-DECISION-RP-ARCHIVE — RP归档、重置与跨局继承

- approval_status：`APPROVED`（选项A；2026-07-30T04:39:21Z）
- 当前未决问题：33项RP何时归档、下一局是否继承未完全冻结。
- Locked来源：STATE-010 §§11-15；parameter_registry RP lifecycle；common_contracts §4
- 当前代码行为：RoundRuntime创建33槽、finalize写RP-032/033并变为不可写；没有持久化归档信封。
- 兼容要求：现有一局Runtime行为不变；认知状态不得进入权威GameState。

### 选项 A — 局末不可变全量快照；新局重建全部RP，仅RP-033经显式学习适配器产生下一局profile输入，不直接复制任何RP。
- 优点：可审计、无串局、符合生命周期
- 缺点：归档体积较大
- 版本影响：可选归档记录MINOR
### 选项 B — 只归档RP-029/030/032/033并复制部分RP到下局。
- 优点：体积小
- 缺点：证据不全且复制边界易泄漏
- 版本影响：需定义新语义

### 影响分析

- 向后兼容：现有Runtime内存行为保持；新增归档消费者可忽略。
- 跨语言：固定字段JSON跨语言。
- 持久化：新增受限audit archive，可选记录；不进入GameState。
- 安全/隐藏信息：四座分开；RP-033不得含隐藏truth。
- 测试：完整生命周期、归档不可写、新局零串值、RP-033公开信息投毒。
- 迁移：历史局无归档不回填，标report-only。
- 回滚：停止写新archive；运行仍可用现有Runtime。
- Frozen契约：COMPATIBLE_EXTENSION
- 版本：AUDIT format MINOR；CONTRACTS不变

### 推荐

推荐选项：**A**。满足逐座归档和失败隔离，保留明确学习出口。

### 需要批准的准确规范文字

> round_end成功后归档{round_id,seat,state_version,event_index,RP-001..RP-033,created_event,updated_event,result_hash}的不可变逐座快照；归档后写=LIFECYCLE_VIOLATION。新round创建新RP实例，RP-001..RP-033均不直接复制；仅RP-033可由独立、公开信息受限的学习适配器转换为下一局profile输入。归档失败不改变已提交round结果，并报告审计失败。

### Golden

- 正向：GV-003
- 反向：GV-004
## SPEC-DECISION-MIGRATION-GRAPH — 显式唯一逐边迁移图

- approval_status：`APPROVED`（选项A；2026-07-30T04:39:21Z）
- 当前未决问题：compatibility.json只有节点，代码只有一个特例，没有通用唯一图。
- Locked来源：ALGO-009 §§3,5,10,13；versioning_policy.md
- 当前代码行为：支持RULES1.0/PARAMS1.0/IMPL2.0和RULES1.0/PARAMS1.1/IMPL2.1；唯一代码边把全局GP-024..027复制到四座并提升版本。
- 兼容要求：该真实边的输出和四座独立对象必须不变。

### 选项 A — 版本节点为完整三元组；只允许登记的单步有向边；当前唯一边1.0/2.0→1.1/2.1；路径必须唯一、无环、逐边执行。
- 优点：可审计且拒绝猜测
- 缺点：每个版本必须维护edge fixture
- 版本影响：图元数据MINOR
### 选项 B — 直接从任意旧版本迁移到current。
- 优点：代码少
- 缺点：无法证明中间语义和幂等
- 版本影响：风险高

### 影响分析

- 向后兼容：现有两版本和迁移结果保持。
- 跨语言：三元组与JSON patch/golden可移植。
- 持久化：manifest新增edges；原config不原地覆盖，成功后原子替换。
- 安全/隐藏信息：迁移不得放宽隐藏学习字段。
- 测试：节点唯一、边golden、无路径、多路径、环、输入不变、幂等。
- 迁移：把现有特例注册为edge，不改输出。
- 回滚：禁用graph门面，回退现有特例loader。
- Frozen契约：COMPATIBLE_EXTENSION
- 版本：PARAMS/IMPL下一MINOR用于图元数据；当前数据版本不变

### 推荐

推荐选项：**A**。与现有兼容表和版本策略完全一致。

### 需要批准的准确规范文字

> 迁移节点键为(rule_version,parameter_version,implementation_version)。仅可执行compatibility manifest登记的有向边；图必须无环，任一source到target最多一条路径。当前批准候选边仅(CDMJ-AI-RULES 1.0.0,PARAMS 1.0.0,IMPL 2.0.0)→(RULES 1.0.0,PARAMS 1.1.0,IMPL 2.1.0)，变换为从global_parameters移出GP-024..027并深复制到四座players[i].cognitive_parameters，再更新顶层及GP-001 parameter_version。无路径=MIGRATION_FAILED，多路径/环=VERSION_CONFLICT；每边纯函数、输入不变、重复执行target为字节幂等。

### Golden

- 正向：GV-005
- 反向：GV-006
## SPEC-DECISION-EXTENSIONS — extensions容器策略

- approval_status：`APPROVED`（选项A；2026-07-30T04:39:21Z）
- 当前未决问题：GP-002/004有extensions但元素schema、hash和迁移未定义。
- Locked来源：ALGO-009 §§5,7,11；versioning_policy unknown-field rule
- 当前代码行为：当前只校验GP-002.extensions为长度≤64 list；GP-004要求[]；元素未校验，且会进入config hash。
- 兼容要求：默认配置两个extensions均为空；普通未知字段继续拒绝。

### 选项 A — PARAMS1.1仅允许GP-002.extensions=[]和GP-004.extensions=[]；非空=PARAM_UNKNOWN。未来非空必须新PARAMS版本和注册schema。
- 优点：零新功能、最安全、完全兼容现有默认
- 缺点：暂不支持平台扩展
- 版本影响：无；未来至少MINOR
### 选项 B — 立即定义任意extension对象并保留。
- 优点：灵活
- 缺点：无业务来源、hash/安全不可控
- 版本影响：至少MINOR

### 影响分析

- 向后兼容：现有默认及空数组hash不变。
- 跨语言：空数组语义无差异。
- 持久化：格式不变。
- 安全/隐藏信息：阻止未经审查payload进入策略/日志。
- 测试：容器位置、null、对象、非空数组、未知根键。
- 迁移：无数据迁移。
- 回滚：撤销新拒绝门禁，恢复旧list校验。
- Frozen契约：NO_INTERFACE_CHANGE
- 版本：无（未来非空扩展至少PARAMS MINOR）

### 推荐

推荐选项：**A**。遵守不发明新功能及未知字段拒绝倾向。

### 需要批准的准确规范文字

> PARAMS 1.1只允许extensions字段出现在GP-002和GP-004，值必须是空JSON数组。其他位置出现extensions或任一非空元素返回PARAM_UNKNOWN，result=null。extensions字段参与canonical hash。未来支持非空元素必须提升parameter_version、登记extension_id/version/payload schema、迁移边和可见性测试。

### Golden

- 正向：GV-007
- 反向：GV-008
## SPEC-DECISION-CANONICAL-NUMBER — canonical JSON数字字节

- approval_status：`APPROVED`（选项A；2026-07-30T04:39:21Z）
- 当前未决问题：固定数字、Decimal scale、负零和指数未定义。
- Locked来源：ALGO-009 §§2,3,6；common_contracts序列化；versioning_policy canonical bytes=MAJOR
- 当前代码行为：Python json.dumps：int十进制，float采用CPython表示，-0.0输出-0.0；allow_nan=False。
- 兼容要求：PARAMS1.1现有config_hash必须保留为canonical_version=legacy-json-v1。

### 选项 A — 双轨：旧版本保留legacy-json-v1；新canonical-jcs-nfc-v2数字遵循RFC8785 JCS/ECMAScript NumberToString，-0为0，拒绝非有限；领域Decimal先按scale半偶量化再作为JSON number。
- 优点：跨语言且保legacy hash
- 缺点：新版本hash不同，需MAJOR契约版本
- 版本影响：CONTRACTS2/PARAMS2
### 选项 B — 永久使用Python json.dumps数字。
- 优点：当前hash不变
- 缺点：非跨语言规范且负零不统一
- 版本影响：无

### 影响分析

- 向后兼容：旧配置/回放保留legacy hash；新写入显式v2。
- 跨语言：RFC8785有多语言实现。
- 持久化：新增canonical_version；新配置hash改变。
- 安全/隐藏信息：无隐藏信息变化。
- 测试：-0,1.0,1.5,1e30,int64边界,NaN/Inf,Decimal半偶的固定bytes/hash。
- 迁移：旧缺字段映射legacy-v1；新格式必须显式v2。
- 回滚：停止新v2写入；旧reader继续读取legacy；已写v2需保留reader。
- Frozen契约：BREAKING_CHANGE_REQUIRED
- 版本：CDMJ-CONTRACTS 2.0.0 + CDMJ-AI-PARAMS 2.0.0 + migration edge

### 推荐

推荐选项：**A**。同时满足字节级、跨语言和旧hash兼容。

### 需要批准的准确规范文字

> canonical_version=legacy-json-v1的历史配置继续使用现有Python兼容字节且仅用于回放。新写配置必须canonical_version=canonical-jcs-nfc-v2：整数在int64范围内用无前导零十进制；非整数按RFC 8785引用的ECMAScript NumberToString最短round-trip格式；-0序列化为字节0；NaN和±Infinity返回NON_FINITE；Decimal先按字段scale以ROUND_HALF_EVEN量化，再移除无意义尾零并按同一number grammar输出。hash为SHA-256，32字节，序列化为64个小写十六进制字符。

### Golden

- 正向：GV-009, GV-010
- 反向：GV-011
## SPEC-DECISION-CANONICAL-UNICODE — canonical JSON Unicode字节与键序

- approval_status：`APPROVED`（选项A；2026-07-30T04:39:21Z）
- 当前未决问题：正规化、转义和键排序基准未定义。
- Locked来源：ALGO-009 §3；common_contracts序列化；versioning_policy
- 当前代码行为：ensure_ascii=False、Python Unicode码点键序、无NFC归一化。
- 兼容要求：PARAMS1.1现有hash继续legacy-json-v1。

### 选项 A — 新v2先对所有键和值做Unicode NFC，再按RFC8785 JCS UTF-16 code-unit键序和转义，输出UTF-8无BOM。
- 优点：跨语言、组合/分解字符串等价
- 缺点：与legacy字节不同；NFC步骤超出原JCS需明确
- 版本影响：CONTRACTS2/PARAMS2
### 选项 B — 不归一化，保持Python码点排序。
- 优点：旧hash不变
- 缺点：跨语言键序和等价文本不稳定
- 版本影响：无

### 影响分析

- 向后兼容：旧配置继续legacy；新配置hash版本显式。
- 跨语言：明确NFC+JCS，跨语言可复现。
- 持久化：同canonical version内字节唯一。
- 安全/隐藏信息：正规化前检查键碰撞，避免字段覆盖。
- 测试：NFC/NFD、非BMP、控制字符、键碰撞、UTF-16排序golden。
- 迁移：旧缺字段映射legacy；新写v2。
- 回滚：同数字决策。
- Frozen契约：BREAKING_CHANGE_REQUIRED
- 版本：CDMJ-CONTRACTS 2.0.0 + CDMJ-AI-PARAMS 2.0.0

### 推荐

推荐选项：**A**。为配置标识提供跨语言、用户输入稳定性，同时以版本双轨保护旧hash。

### 需要批准的准确规范文字

> canonical-jcs-nfc-v2先递归将所有JSON对象键和字符串值正规化为Unicode NFC；正规化后键冲突返回SCHEMA_INVALID。随后按RFC8785 JCS以UTF-16 code units升序排序键，使用JCS字符串转义，输出UTF-8、无BOM、无额外空白。U+0000..001F使用JSON转义，小写十六进制；其他Unicode直接UTF-8，必要的引号和反斜杠转义。hash为SHA-256，32字节，序列化为64个小写十六进制字符。

### Golden

- 正向：GV-012
- 反向：GV-013
## SPEC-DECISION-CONFIG-FALLBACK — 首次启动与热重载失败

- approval_status：`APPROVED`（选项A；2026-07-30T04:39:21Z）
- 当前未决问题：是否继续上一有效配置未定义。
- Locked来源：ALGO-009 §§5,9,13；STATE-010原子性；versioning_policy
- 当前代码行为：validate_raw失败不保存；save_raw先备份再os.replace；进程启动load_config失败抛异常。
- 兼容要求：已验证active config不能因失败更新而损坏。

### 选项 A — 首次启动无有效配置则hard fail；热重载失败保留当前已验证对象但本次accepted=false并报告错误，不自动读.bak替代。
- 优点：安全且符合倾向
- 缺点：首次启动不可降级
- 版本影响：无
### 选项 B — 任何失败自动回退.bak并继续。
- 优点：可用性高
- 缺点：可能静默运行旧规则
- 版本影响：需新状态语义

### 影响分析

- 向后兼容：现有失败异常和原子保存方向保持。
- 跨语言：纯状态机。
- 持久化：失败不改目标文件；.bak只供人工恢复。
- 安全/隐藏信息：防止旧规则静默启动。
- 测试：首次无配置、首次非法、热更非法、写入故障、并发热更。
- 迁移：无需数据迁移。
- 回滚：关闭热重载；继续只支持启动加载。
- Frozen契约：COMPATIBLE_EXTENSION
- 版本：IMPL MINOR用于结果信封；CONTRACTS不变

### 推荐

推荐选项：**A**。区分无安全基线与已有安全基线。

### 需要批准的准确规范文字

> 首次启动或match创建时配置验证失败：不得创建match/策略，返回accepted=false、result=null及准确error_code。热重载失败：active FrozenConfig对象、config_hash和持久化目标文件保持不变；本次返回accepted=false、result=null、attempted_source_hash、active_config_hash和error_code。不得把继续使用旧active配置报告为本次更新成功，不得自动以.bak替代输入。

### Golden

- 正向：GV-014
- 反向：GV-015
## SPEC-DECISION-RNG-VERSION — RNG版本选择与legacy回放

- approval_status：`APPROVED`（选项A；2026-07-30T04:39:21Z）
- 当前未决问题：algorithm/rng version缺失时和旧/新回放选择未定义。
- Locked来源：ALGO-011 §§1,3,4,10；common_contracts §8；versioning_policy回放规则
- 当前代码行为：derive_seeds无版本参数；生产deal使用legacy BLAKE2b(id)+XOR三流。
- 兼容要求：legacy shuffle/dice/exchange及deal结果必须零变化。

### 选项 A — 缺version的旧回放显式映射legacy-v1；新录制必须写rng_version=2和algorithm_version=2；未知版本拒绝。
- 优点：兼容旧回放且新行为明确
- 缺点：需要双reader
- 版本影响：replay schema MINOR/可能contract MAJOR取决于必填变化
### 选项 B — 缺version使用当前最新。
- 优点：简单
- 缺点：历史结果随升级漂移
- 版本影响：不可接受

### 影响分析

- 向后兼容：旧缺字段回放可继续；新记录自描述。
- 跨语言：版本整数无差异。
- 持久化：回放header新增必填字段；旧reader需兼容适配。
- 安全/隐藏信息：完整seed只在引擎/受限审计。
- 测试：旧缺字段、legacy golden、新必填、null、未知、版本冲突。
- 迁移：读取时适配旧header；不重写历史。
- 回滚：停止写v2并继续legacy；已写v2必须保留reader。
- Frozen契约：COMPATIBLE_EXTENSION for reader; new writer schema may require approval
- 版本：Replay/Audit MINOR；若Frozen schema必填集合改变则CONTRACTS 2.0.0

### 推荐

推荐选项：**A**。直接遵循用户倾向和回放永远使用记录时版本。

### 需要批准的准确规范文字

> 读取回放时：字段rng_version缺失且记录格式早于本决策版本，选择legacy-v1；字段存在则必须为注册版本，未知返回RNG_VERSION_UNKNOWN。legacy-v1严格调用现有derive_seeds，三旧流结果不变。批准后创建的任何新录制必须显式持久化rng_version=2、algorithm_version=2，不得省略或null；新v2不得覆盖legacy入口。策略不得接收master_seed、原始流名、原始index或seed_hash。

### Golden

- 正向：GV-016
- 反向：GV-017
## SPEC-DECISION-RNG-COORDINATE — 无状态RNG逻辑坐标

- approval_status：`APPROVED`（选项A；2026-07-30T04:39:21Z）
- 当前未决问题：并发consumer/index schema和重试语义未定义。
- Locked来源：ALGO-011 §§1,3,5,10；common_contracts §§7,8
- 当前代码行为：只有每game三个seed；其他Random入口分散，无统一坐标。
- 兼容要求：legacy三个旧流保持原值；策略不可见原始坐标/seed。

### 选项 A — v2坐标为{stream_name,consumer_kind,consumer_id,event_id,sample_index}，canonical后无状态派生；重试复用坐标。
- 优点：调度无关、可回放
- 缺点：调用方必须提供稳定ID
- 版本影响：rng v2
### 选项 B — 每stream维护原子递增index。
- 优点：API简单
- 缺点：结果依赖调度/取消/重试
- 版本影响：不满足约束

### 影响分析

- 向后兼容：legacy流不使用坐标；新v2独立。
- 跨语言：定长整数/长度前缀跨语言。
- 持久化：受限审计保存坐标hash，不在策略记录原值。
- 安全/隐藏信息：防止推导未来噪声/牌墙。
- 测试：调度100排列、取消、重试、worker增减、坐标维度域隔离。
- 迁移：消费者逐个迁移到v2；未迁移保持legacy/显式旧路径。
- 回滚：将新consumer切回明确legacy适配；不改变旧三流。
- Frozen契约：COMPATIBLE_EXTENSION；把原始坐标加入Frozen SeedTrace则BREAKING
- 版本：RNG version 2；审计可选字段MINOR

### 推荐

推荐选项：**A**。唯一满足并发确定性和禁止共享index。

### 需要批准的准确规范文字

> rng-v2每次抽样调用必须显式提供逻辑坐标{stream_name,consumer_kind,consumer_id,event_id,sample_index:uint64}。consumer_kind和stream_name来自版本化注册枚举；consumer_id/event_id为UTF-8稳定业务ID；sample_index从同一逻辑事件内0开始。坐标canonical bytes使用长度前缀UTF-8和uint64大端；派生函数纯函数，不读取或写入共享index。线程号、进程号、worker完成顺序、系统时间、容器位置和重试次数禁止进入坐标；重试必须复用原坐标。策略只接收rng_used和opaque trace_ref。

### Golden

- 正向：GV-018
- 反向：GV-019


## 审批门禁

九项规格决策均已关闭，`BLOCKED_BY_SPEC_DECISION`解除。因已批准的canonical v2选项要求Frozen canonical bytes MAJOR变更，在对应接口提案获批、版本提升和迁移规范落盘前，B1-A转为`BLOCKED_BY_INTERFACE_APPROVAL`，仍不得编码。
