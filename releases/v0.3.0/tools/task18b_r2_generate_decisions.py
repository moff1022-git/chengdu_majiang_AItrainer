from __future__ import annotations

import csv, hashlib, json, re, struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"docs/spec-v3/decisions"; OUT.mkdir(parents=True,exist_ok=True)

def sha(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def b2(b:bytes)->int: return int.from_bytes(hashlib.blake2b(b,digest_size=8).digest(),"big")
def write_csv(path,rows):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

ids=[
"SPEC-DECISION-STATE-DEFAULTS","SPEC-DECISION-RP-ARCHIVE","SPEC-DECISION-MIGRATION-GRAPH",
"SPEC-DECISION-EXTENSIONS","SPEC-DECISION-CANONICAL-NUMBER","SPEC-DECISION-CANONICAL-UNICODE",
"SPEC-DECISION-CONFIG-FALLBACK","SPEC-DECISION-RNG-VERSION","SPEC-DECISION-RNG-COORDINATE"]

common={"approval_status":"APPROVED","decision_version":"B1-A-DECISIONS 1.0.0"}
D=[]
def add(id,title,issue,source,current,compat,opts,reco,why,text,back,cross,persist,security,tests,migration,rollback,contract,version):
    D.append(dict(decision_id=id,title=title,unresolved_issue=issue,locked_source=source,current_code_behavior=current,
      compatibility_requirement=compat,options=json.dumps(opts,ensure_ascii=False,separators=(",",":")),recommended_option=reco,
      recommendation_reason=why,proposed_normative_text=text,backward_compatibility=back,cross_language_impact=cross,
      persistence_impact=persist,security_visibility_impact=security,test_impact=tests,migration_requirement=migration,
      rollback=rollback,frozen_contract_impact=contract,required_version_change=version,**common))

add(ids[0],"参数缺失、默认值与null",
"60项定义有范围和生命周期，但嵌套字段required/default/nullable未结构化冻结。",
"STATE-010 §§6,11,15；ALGO-009 §§5,7；common_contracts §§2,8；parameter_registry.csv",
"Humanlike配置根/GP/profile多采用exact-key；EngineConfig.from_dict用get+强转默认；RP未初始化项用None。",
"默认配置PARAMS 1.1必须原样有效；不得把false、0或空集合当作缺失。",
[{"option":"A","summary":"当前schema所有配置字段必填，仅GP-003.early_end_score可null；不对raw current配置补默认。RP用内部UNINITIALIZED而非序列化null。","pros":"匹配现有Humanlike exact-key并消除歧义","cons":"旧EngineConfig宽松输入需适配层","version":"PARAMS 1.2 minor for structured registry metadata"},{"option":"B","summary":"对所有缺失字段从default.json补值。","pros":"宽松","cons":"掩盖拼写/版本错误且无法区分缺失","version":"default语义变化至少MINOR"}],"A",
"最接近现有权威humanlike loader，并满足缺省与null不同。",
"对PARAMS 1.1 raw config：根字段、GP-001..023、四座profile及各座GP-024..027和其声明子字段全部必填；唯一允许显式null为GP-003.early_end_score。缺失必填=SCHEMA_INVALID，未知字段=PARAM_UNKNOWN，显式null不可空=PARAM_NULL，类型错误=PARAM_TYPE，闭区间外=PARAM_RANGE。false、0、空字符串和空集合按实际值校验。RP未到创建时点使用内部UNINITIALIZED，不序列化为null；到时点后必须有领域值。",
"默认PARAMS 1.1文件无变化；EngineConfig旧宽松入口保留legacy adapter但不得进入ALGO-009权威门禁。","结构化字段表跨语言直接实现。","registry元数据新增可选default_present/nullable；现有配置JSON不变。","不改变PlayerView；私有配置不写入策略。","五类输入分别断言accepted/error/result；60 ID闭集。","把parameter_registry生成结构化schema；不改现有值。","撤回新registry schema，继续现有loader；无数据回写。","COMPATIBLE_EXTENSION","PARAMS 1.2.0（元数据）；CONTRACTS不变")

add(ids[1],"RP归档、重置与跨局继承",
"33项RP何时归档、下一局是否继承未完全冻结。","STATE-010 §§11-15；parameter_registry RP lifecycle；common_contracts §4",
"RoundRuntime创建33槽、finalize写RP-032/033并变为不可写；没有持久化归档信封。","现有一局Runtime行为不变；认知状态不得进入权威GameState。",
[{"option":"A","summary":"局末不可变全量快照；新局重建全部RP，仅RP-033经显式学习适配器产生下一局profile输入，不直接复制任何RP。","pros":"可审计、无串局、符合生命周期","cons":"归档体积较大","version":"可选归档记录MINOR"},{"option":"B","summary":"只归档RP-029/030/032/033并复制部分RP到下局。","pros":"体积小","cons":"证据不全且复制边界易泄漏","version":"需定义新语义"}],"A","满足逐座归档和失败隔离，保留明确学习出口。",
"round_end成功后归档{round_id,seat,state_version,event_index,RP-001..RP-033,created_event,updated_event,result_hash}的不可变逐座快照；归档后写=LIFECYCLE_VIOLATION。新round创建新RP实例，RP-001..RP-033均不直接复制；仅RP-033可由独立、公开信息受限的学习适配器转换为下一局profile输入。归档失败不改变已提交round结果，并报告审计失败。",
"现有Runtime内存行为保持；新增归档消费者可忽略。","固定字段JSON跨语言。","新增受限audit archive，可选记录；不进入GameState。","四座分开；RP-033不得含隐藏truth。","完整生命周期、归档不可写、新局零串值、RP-033公开信息投毒。","历史局无归档不回填，标report-only。","停止写新archive；运行仍可用现有Runtime。","COMPATIBLE_EXTENSION","AUDIT format MINOR；CONTRACTS不变")

add(ids[2],"显式唯一逐边迁移图",
"compatibility.json只有节点，代码只有一个特例，没有通用唯一图。","ALGO-009 §§3,5,10,13；versioning_policy.md",
"支持RULES1.0/PARAMS1.0/IMPL2.0和RULES1.0/PARAMS1.1/IMPL2.1；唯一代码边把全局GP-024..027复制到四座并提升版本。","该真实边的输出和四座独立对象必须不变。",
[{"option":"A","summary":"版本节点为完整三元组；只允许登记的单步有向边；当前唯一边1.0/2.0→1.1/2.1；路径必须唯一、无环、逐边执行。","pros":"可审计且拒绝猜测","cons":"每个版本必须维护edge fixture","version":"图元数据MINOR"},{"option":"B","summary":"直接从任意旧版本迁移到current。","pros":"代码少","cons":"无法证明中间语义和幂等","version":"风险高"}],"A","与现有兼容表和版本策略完全一致。",
"迁移节点键为(rule_version,parameter_version,implementation_version)。仅可执行compatibility manifest登记的有向边；图必须无环，任一source到target最多一条路径。当前批准候选边仅(CDMJ-AI-RULES 1.0.0,PARAMS 1.0.0,IMPL 2.0.0)→(RULES 1.0.0,PARAMS 1.1.0,IMPL 2.1.0)，变换为从global_parameters移出GP-024..027并深复制到四座players[i].cognitive_parameters，再更新顶层及GP-001 parameter_version。无路径=MIGRATION_FAILED，多路径/环=VERSION_CONFLICT；每边纯函数、输入不变、重复执行target为字节幂等。",
"现有两版本和迁移结果保持。","三元组与JSON patch/golden可移植。","manifest新增edges；原config不原地覆盖，成功后原子替换。","迁移不得放宽隐藏学习字段。","节点唯一、边golden、无路径、多路径、环、输入不变、幂等。","把现有特例注册为edge，不改输出。","禁用graph门面，回退现有特例loader。","COMPATIBLE_EXTENSION","PARAMS/IMPL下一MINOR用于图元数据；当前数据版本不变")

add(ids[3],"extensions容器策略","GP-002/004有extensions但元素schema、hash和迁移未定义。","ALGO-009 §§5,7,11；versioning_policy unknown-field rule",
"当前只校验GP-002.extensions为长度≤64 list；GP-004要求[]；元素未校验，且会进入config hash。","默认配置两个extensions均为空；普通未知字段继续拒绝。",
[{"option":"A","summary":"PARAMS1.1仅允许GP-002.extensions=[]和GP-004.extensions=[]；非空=PARAM_UNKNOWN。未来非空必须新PARAMS版本和注册schema。","pros":"零新功能、最安全、完全兼容现有默认","cons":"暂不支持平台扩展","version":"无；未来至少MINOR"},{"option":"B","summary":"立即定义任意extension对象并保留。","pros":"灵活","cons":"无业务来源、hash/安全不可控","version":"至少MINOR"}],"A","遵守不发明新功能及未知字段拒绝倾向。",
"PARAMS 1.1只允许extensions字段出现在GP-002和GP-004，值必须是空JSON数组。其他位置出现extensions或任一非空元素返回PARAM_UNKNOWN，result=null。extensions字段参与canonical hash。未来支持非空元素必须提升parameter_version、登记extension_id/version/payload schema、迁移边和可见性测试。",
"现有默认及空数组hash不变。","空数组语义无差异。","格式不变。","阻止未经审查payload进入策略/日志。","容器位置、null、对象、非空数组、未知根键。","无数据迁移。","撤销新拒绝门禁，恢复旧list校验。","NO_INTERFACE_CHANGE","无（未来非空扩展至少PARAMS MINOR）")

add(ids[4],"canonical JSON数字字节","固定数字、Decimal scale、负零和指数未定义。","ALGO-009 §§2,3,6；common_contracts序列化；versioning_policy canonical bytes=MAJOR",
"Python json.dumps：int十进制，float采用CPython表示，-0.0输出-0.0；allow_nan=False。","PARAMS1.1现有config_hash必须保留为canonical_version=legacy-json-v1。",
[{"option":"A","summary":"双轨：旧版本保留legacy-json-v1；新canonical-jcs-nfc-v2数字遵循RFC8785 JCS/ECMAScript NumberToString，-0为0，拒绝非有限；领域Decimal先按scale半偶量化再作为JSON number。","pros":"跨语言且保legacy hash","cons":"新版本hash不同，需MAJOR契约版本","version":"CONTRACTS2/PARAMS2"},{"option":"B","summary":"永久使用Python json.dumps数字。","pros":"当前hash不变","cons":"非跨语言规范且负零不统一","version":"无"}],"A","同时满足字节级、跨语言和旧hash兼容。",
"canonical_version=legacy-json-v1的历史配置继续使用现有Python兼容字节且仅用于回放。新写配置必须canonical_version=canonical-jcs-nfc-v2：整数在int64范围内用无前导零十进制；非整数按RFC 8785引用的ECMAScript NumberToString最短round-trip格式；-0序列化为字节0；NaN和±Infinity返回NON_FINITE；Decimal先按字段scale以ROUND_HALF_EVEN量化，再移除无意义尾零并按同一number grammar输出。hash为SHA-256，32字节，序列化为64个小写十六进制字符。",
"旧配置/回放保留legacy hash；新写入显式v2。","RFC8785有多语言实现。","新增canonical_version；新配置hash改变。","无隐藏信息变化。","-0,1.0,1.5,1e30,int64边界,NaN/Inf,Decimal半偶的固定bytes/hash。","旧缺字段映射legacy-v1；新格式必须显式v2。","停止新v2写入；旧reader继续读取legacy；已写v2需保留reader。","BREAKING_CHANGE_REQUIRED","CDMJ-CONTRACTS 2.0.0 + CDMJ-AI-PARAMS 2.0.0 + migration edge")

add(ids[5],"canonical JSON Unicode字节与键序","正规化、转义和键排序基准未定义。","ALGO-009 §3；common_contracts序列化；versioning_policy",
"ensure_ascii=False、Python Unicode码点键序、无NFC归一化。","PARAMS1.1现有hash继续legacy-json-v1。",
[{"option":"A","summary":"新v2先对所有键和值做Unicode NFC，再按RFC8785 JCS UTF-16 code-unit键序和转义，输出UTF-8无BOM。","pros":"跨语言、组合/分解字符串等价","cons":"与legacy字节不同；NFC步骤超出原JCS需明确","version":"CONTRACTS2/PARAMS2"},{"option":"B","summary":"不归一化，保持Python码点排序。","pros":"旧hash不变","cons":"跨语言键序和等价文本不稳定","version":"无"}],"A","为配置标识提供跨语言、用户输入稳定性，同时以版本双轨保护旧hash。",
"canonical-jcs-nfc-v2先递归将所有JSON对象键和字符串值正规化为Unicode NFC；正规化后键冲突返回SCHEMA_INVALID。随后按RFC8785 JCS以UTF-16 code units升序排序键，使用JCS字符串转义，输出UTF-8、无BOM、无额外空白。U+0000..001F使用JSON转义，小写十六进制；其他Unicode直接UTF-8，必要的引号和反斜杠转义。hash为SHA-256，32字节，序列化为64个小写十六进制字符。",
"旧配置继续legacy；新配置hash版本显式。","明确NFC+JCS，跨语言可复现。","同canonical version内字节唯一。","正规化前检查键碰撞，避免字段覆盖。","NFC/NFD、非BMP、控制字符、键碰撞、UTF-16排序golden。","旧缺字段映射legacy；新写v2。","同数字决策。","BREAKING_CHANGE_REQUIRED","CDMJ-CONTRACTS 2.0.0 + CDMJ-AI-PARAMS 2.0.0")

add(ids[6],"首次启动与热重载失败","是否继续上一有效配置未定义。","ALGO-009 §§5,9,13；STATE-010原子性；versioning_policy",
"validate_raw失败不保存；save_raw先备份再os.replace；进程启动load_config失败抛异常。","已验证active config不能因失败更新而损坏。",
[{"option":"A","summary":"首次启动无有效配置则hard fail；热重载失败保留当前已验证对象但本次accepted=false并报告错误，不自动读.bak替代。","pros":"安全且符合倾向","cons":"首次启动不可降级","version":"无"},{"option":"B","summary":"任何失败自动回退.bak并继续。","pros":"可用性高","cons":"可能静默运行旧规则","version":"需新状态语义"}],"A","区分无安全基线与已有安全基线。",
"首次启动或match创建时配置验证失败：不得创建match/策略，返回accepted=false、result=null及准确error_code。热重载失败：active FrozenConfig对象、config_hash和持久化目标文件保持不变；本次返回accepted=false、result=null、attempted_source_hash、active_config_hash和error_code。不得把继续使用旧active配置报告为本次更新成功，不得自动以.bak替代输入。",
"现有失败异常和原子保存方向保持。","纯状态机。","失败不改目标文件；.bak只供人工恢复。","防止旧规则静默启动。","首次无配置、首次非法、热更非法、写入故障、并发热更。","无需数据迁移。","关闭热重载；继续只支持启动加载。","COMPATIBLE_EXTENSION","IMPL MINOR用于结果信封；CONTRACTS不变")

add(ids[7],"RNG版本选择与legacy回放","algorithm/rng version缺失时和旧/新回放选择未定义。","ALGO-011 §§1,3,4,10；common_contracts §8；versioning_policy回放规则",
"derive_seeds无版本参数；生产deal使用legacy BLAKE2b(id)+XOR三流。","legacy shuffle/dice/exchange及deal结果必须零变化。",
[{"option":"A","summary":"缺version的旧回放显式映射legacy-v1；新录制必须写rng_version=2和algorithm_version=2；未知版本拒绝。","pros":"兼容旧回放且新行为明确","cons":"需要双reader","version":"replay schema MINOR/可能contract MAJOR取决于必填变化"},{"option":"B","summary":"缺version使用当前最新。","pros":"简单","cons":"历史结果随升级漂移","version":"不可接受"}],"A","直接遵循用户倾向和回放永远使用记录时版本。",
"读取回放时：字段rng_version缺失且记录格式早于本决策版本，选择legacy-v1；字段存在则必须为注册版本，未知返回RNG_VERSION_UNKNOWN。legacy-v1严格调用现有derive_seeds，三旧流结果不变。批准后创建的任何新录制必须显式持久化rng_version=2、algorithm_version=2，不得省略或null；新v2不得覆盖legacy入口。策略不得接收master_seed、原始流名、原始index或seed_hash。",
"旧缺字段回放可继续；新记录自描述。","版本整数无差异。","回放header新增必填字段；旧reader需兼容适配。","完整seed只在引擎/受限审计。","旧缺字段、legacy golden、新必填、null、未知、版本冲突。","读取时适配旧header；不重写历史。","停止写v2并继续legacy；已写v2必须保留reader。","COMPATIBLE_EXTENSION for reader; new writer schema may require approval","Replay/Audit MINOR；若Frozen schema必填集合改变则CONTRACTS 2.0.0")

add(ids[8],"无状态RNG逻辑坐标","并发consumer/index schema和重试语义未定义。","ALGO-011 §§1,3,5,10；common_contracts §§7,8",
"只有每game三个seed；其他Random入口分散，无统一坐标。","legacy三个旧流保持原值；策略不可见原始坐标/seed。",
[{"option":"A","summary":"v2坐标为{stream_name,consumer_kind,consumer_id,event_id,sample_index}，canonical后无状态派生；重试复用坐标。","pros":"调度无关、可回放","cons":"调用方必须提供稳定ID","version":"rng v2"},{"option":"B","summary":"每stream维护原子递增index。","pros":"API简单","cons":"结果依赖调度/取消/重试","version":"不满足约束"}],"A","唯一满足并发确定性和禁止共享index。",
"rng-v2每次抽样调用必须显式提供逻辑坐标{stream_name,consumer_kind,consumer_id,event_id,sample_index:uint64}。consumer_kind和stream_name来自版本化注册枚举；consumer_id/event_id为UTF-8稳定业务ID；sample_index从同一逻辑事件内0开始。坐标canonical bytes使用长度前缀UTF-8和uint64大端；派生函数纯函数，不读取或写入共享index。线程号、进程号、worker完成顺序、系统时间、容器位置和重试次数禁止进入坐标；重试必须复用原坐标。策略只接收rng_used和opaque trace_ref。",
"legacy流不使用坐标；新v2独立。","定长整数/长度前缀跨语言。","受限审计保存坐标hash，不在策略记录原值。","防止推导未来噪声/牌墙。","调度100排列、取消、重试、worker增减、坐标维度域隔离。","消费者逐个迁移到v2；未迁移保持legacy/显式旧路径。","将新consumer切回明确legacy适配；不改变旧三流。","COMPATIBLE_EXTENSION；把原始坐标加入Frozen SeedTrace则BREAKING","RNG version 2；审计可选字段MINOR")

# Golden vectors: every decision has at least one positive and one negative.
gold=[]
def gv(id,kind,name,input,expected): gold.append({"vector_id":f"GV-{len(gold)+1:03d}","decision_id":id,"kind":kind,"name":name,"input":input,"expected":expected})
gv(ids[0],"positive","explicit-null-only-allowed",{"GP-003":{"early_end_score":None}}, {"accepted":True})
gv(ids[0],"negative","missing-required",{"GP-003":{"starting_score":0}}, {"accepted":False,"error_code":"SCHEMA_INVALID","result":None})
gv(ids[1],"positive","new-round-no-copy",{"archived_RP_028":{"emotion":0.8},"next_round":True},{"next_RP_028":"created_from_round_default_or_profile","direct_copy":False})
gv(ids[1],"negative","write-after-archive",{"lifecycle":"FINALIZED","write":"RP-010"},{"accepted":False,"error_code":"LIFECYCLE_VIOLATION"})
gv(ids[2],"positive","only-current-edge",{"from":["CDMJ-AI-RULES 1.0.0","CDMJ-AI-PARAMS 1.0.0","CDMJ-AI-IMPL 2.0.0"],"to":["CDMJ-AI-RULES 1.0.0","CDMJ-AI-PARAMS 1.1.0","CDMJ-AI-IMPL 2.1.0"]},{"steps":["move GP-024..027 to each players[i].cognitive_parameters","update parameter versions"],"unique":True})
gv(ids[2],"negative","no-path",{"from":"PARAMS 0.9","to":"PARAMS 1.1"},{"accepted":False,"error_code":"MIGRATION_FAILED"})
gv(ids[3],"positive","declared-empty-containers",{"GP-002.extensions":[],"GP-004.extensions":[]},{"accepted":True,"included_in_hash":True})
gv(ids[3],"negative","non-empty-current-extension",{"GP-002.extensions":[{"x":1}]},{"accepted":False,"error_code":"PARAM_UNKNOWN"})

# Recommended canonical v2 byte examples (NFC + JCS). Simple numbers have unambiguous JCS bytes.
for name,obj,canon in [
    ("negative-zero",{"n":-0.0},b'{"n":0}'),
    ("integer-and-fraction",{"i":1,"n":1.5},b'{"i":1,"n":1.5}'),
]: gv(ids[4],"positive",name,obj,{"canonical_utf8_hex":canon.hex(),"canonical_utf8_text":canon.decode(),"sha256_hex":sha(canon)})
gv(ids[4],"negative","non-finite",{"n":"NaN token"},{"accepted":False,"error_code":"NON_FINITE","canonical_bytes":None})
nfc='é'; canon=json.dumps({"é":nfc},ensure_ascii=False,separators=(",",":"),sort_keys=True).encode()
gv(ids[5],"positive","nfd-normalizes-to-nfc",{"key":"e+U+0301","value":"e+U+0301"},{"canonical_utf8_hex":canon.hex(),"canonical_utf8_text":canon.decode(),"sha256_hex":sha(canon)})
gv(ids[5],"negative","normalization-key-collision",{"keys":["é","e\u0301"]},{"accepted":False,"error_code":"SCHEMA_INVALID","canonical_bytes":None})
gv(ids[6],"positive","hot-reload-failure-keeps-active",{"active_hash":"a"*64,"candidate":"invalid"},{"accepted":False,"active_hash_after":"a"*64,"error_code":"SCHEMA_INVALID"})
gv(ids[6],"negative","cold-start-invalid",{"active_config":None,"candidate":"invalid"},{"started":False,"accepted":False,"result":None,"error_code":"SCHEMA_INVALID"})

# Legacy concrete values.
gid="fixed-for-exchange"; master=b2(gid.encode()); mask=(1<<64)-1
gv(ids[7],"positive","legacy-v1-fixed-for-exchange",{"game_id":gid,"rng_version_missing_in_legacy_replay":True},{"selected_version":"legacy-v1","master_seed":master,"shuffle_seed":master,"dice_seed":(master^0xA5A5A5A5A5A5A5A5)&mask,"exchange_seed":(master^0x5A5A5A5A5A5A5A5A)&mask})
gv(ids[7],"negative","new-record-missing-version",{"record_format":"post-decision","rng_version":None},{"accepted":False,"error_code":"SCHEMA_INVALID"})

# Proposed v2 master and coordinate byte layout.
gidb=b"demo"; master_input=b"CDMJ-RNG\0master\0"+struct.pack(">H",len(gidb))+gidb+struct.pack(">HH",2,2); m2=b2(master_input)
name=b"policy_noise"; stream_input=b"CDMJ-RNG\0stream\0"+struct.pack(">QH",m2,len(name))+name+struct.pack(">H",2); ss=b2(stream_input)
coord=b"CDMJ-RNG\0coord\0"+struct.pack(">Q",ss)
for part in (b"policy_noise",b"policy",b"seat-0",b"event-42"): coord+=struct.pack(">H",len(part))+part
coord+=struct.pack(">Q",0); sample=b2(coord)
gv(ids[8],"positive","stateless-coordinate",{"game_id":"demo","algorithm_version":2,"rng_version":2,"stream_name":"policy_noise","consumer_kind":"policy","consumer_id":"seat-0","event_id":"event-42","sample_index":0},{"master_input_hex":master_input.hex(),"master_seed":m2,"stream_input_hex":stream_input.hex(),"stream_seed":ss,"coordinate_input_hex":coord.hex(),"sample_seed":sample})
gv(ids[8],"negative","forbidden-scheduler-coordinate",{"coordinate":{"worker_completion_order":3,"system_time":123}}, {"accepted":False,"error_code":"SCHEMA_INVALID"})

gold_doc={"schema_version":1,"status":"APPROVED_OPTION_A","decision_version":"B1-A-DECISIONS 1.0.0","approved_by":"project_owner_user","approved_at":"2026-07-30T04:39:21Z","hash_definition":"SHA-256，32字节，序列化为64个小写十六进制字符。","vector_count":len(gold),"vectors":gold}
(OUT/"B1-A_golden_vectors.json").write_text(json.dumps(gold_doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

write_csv(OUT/"B1-A_decision_matrix.csv",D)

def options_md(raw):
    opts=json.loads(raw); lines=[]
    for o in opts:
        lines += [f"### 选项 {o['option']} — {o['summary']}",f"- 优点：{o['pros']}",f"- 缺点：{o['cons']}",f"- 版本影响：{o['version']}"]
    return "\n".join(lines)

sections=[]
for d in D:
    pos=[g["vector_id"] for g in gold if g["decision_id"]==d["decision_id"] and g["kind"]=="positive"]
    neg=[g["vector_id"] for g in gold if g["decision_id"]==d["decision_id"] and g["kind"]=="negative"]
    sections.append(f"""## {d['decision_id']} — {d['title']}

- approval_status：`APPROVED`（选项A；2026-07-30T04:39:21Z）
- 当前未决问题：{d['unresolved_issue']}
- Locked来源：{d['locked_source']}
- 当前代码行为：{d['current_code_behavior']}
- 兼容要求：{d['compatibility_requirement']}

{options_md(d['options'])}

### 影响分析

- 向后兼容：{d['backward_compatibility']}
- 跨语言：{d['cross_language_impact']}
- 持久化：{d['persistence_impact']}
- 安全/隐藏信息：{d['security_visibility_impact']}
- 测试：{d['test_impact']}
- 迁移：{d['migration_requirement']}
- 回滚：{d['rollback']}
- Frozen契约：{d['frozen_contract_impact']}
- 版本：{d['required_version_change']}

### 推荐

推荐选项：**{d['recommended_option']}**。{d['recommendation_reason']}

### 需要批准的准确规范文字

> {d['proposed_normative_text']}

### Golden

- 正向：{', '.join(pos)}
- 反向：{', '.join(neg)}
""")

pack=f"""# Task 18B-R2：B1-A九项阻断规格决策包

状态：**APPROVED / OPTION A × 9**  
范围：STATE-010、ALGO-009、ALGO-011。本文是决策提案，不修改Locked规格、Frozen契约、业务代码、测试断言或Task 17/18A状态。

## 技术摘要

项目负责人已于`2026-07-30T04:39:21Z`明确批准九项选项A，决策版本为`B1-A-DECISIONS 1.0.0`。批准优先保护PARAMS 1.1配置、legacy-v1回放及shuffle/dice/exchange结果。canonical新字节规范采用版本双轨：历史使用legacy-json-v1，新写配置使用NFC+RFC8785 JCS的v2；该选择改变canonical bytes，后续仍必须按versioning_policy完成`CDMJ-CONTRACTS 2.0.0`和参数迁移审批，规格决策批准本身不等于Frozen接口已变更。

Golden文件共{len(gold)}条向量。所有hash术语统一解释为：**SHA-256，32字节，序列化为64个小写十六进制字符。**

{''.join(sections)}

## 审批门禁

九项规格决策均已关闭，`BLOCKED_BY_SPEC_DECISION`解除。因已批准的canonical v2选项要求Frozen canonical bytes MAJOR变更，在对应接口提案获批、版本提升和迁移规范落盘前，B1-A转为`BLOCKED_BY_INTERFACE_APPROVAL`，仍不得编码。
"""
(OUT/"B1-A_decision_pack.md").write_text(pack,encoding="utf-8")

form=["# B1-A规格决策审批表","","说明：每项只能选择APPROVED_OPTION、REJECTED或NEEDS_REVISION之一；推荐不等于批准。","","| DECISION_ID | APPROVED_OPTION | REJECTED | NEEDS_REVISION | COMMENT | APPROVED_BY | APPROVED_AT | DECISION_VERSION |","|---|---|---|---|---|---|---|---|"]
for d in D: form.append(f"| {d['decision_id']} | A |  |  | 项目负责人明确批准9项均选择A | project_owner_user | 2026-07-30T04:39:21Z | {d['decision_version']} |")
form += ["","## 生效条件","","- APPROVED_OPTION必须填写A/B或经修订后的明确选项编号。","- APPROVED_AT使用UTC RFC3339。","- canonical bytes、可见性或Frozen必填字段变化必须另有接口/版本批准。","- 九项未全部形成明确结论前，不得将B1-A标为IMPLEMENTATION_READY。"]
(OUT/"B1-A_approval_form.md").write_text("\n".join(form)+"\n",encoding="utf-8")

# Hash wording findings: report only, never edit source Locked/Frozen files here.
patterns=re.compile(r"(?:64\s*位[^\n]{0,20}(?:hash|SHA-?256|小写|hex)|hash[^\n]{0,20}64\s*位|hash为64|64位小写hex)",re.I)
scan=[ROOT/"docs/spec-v3/03-unit-specs/deterministic_algorithm_scoring_specs.md",ROOT/"docs/spec-v3/contracts/common_contracts.md",ROOT/"docs/spec-v3/semantic-completion/reviews/B1-A_design_review.md",ROOT/"docs/spec-v3/semantic-completion/first_batch_acceptance_matrix.csv",ROOT/"docs/spec-v3/semantic-completion/semantic_completion_matrix.csv"]
find=[]
for p in scan:
    for n,line in enumerate(p.read_text(encoding="utf-8-sig").splitlines(),1):
        if patterns.search(line): find.append((p.relative_to(ROOT).as_posix(),n,line.strip()[:500]))
finding_lines="\n".join(f"| `{p}:{n}` | `{line.replace('|','\\|')}` |" for p,n,line in find) or "| 无 | 无 |"
find_doc=f"""# B1-A SHA-256术语复核

## 规范表述

统一使用：**SHA-256，32字节，序列化为64个小写十六进制字符。** “64位SHA-256”会被理解为64 bit，错误缩短摘要；“64位小写hex”也没有说明64是字符数。

## 发现

| 位置 | 原文字 |
|---|---|
{finding_lines}

本任务只列出发现，没有修改Locked单元规格或Task16 Frozen契约。非Locked派生文档可在后续获批同步时修正。
"""
(OUT/"B1-A_hash_wording_findings.md").write_text(find_doc,encoding="utf-8")

assert len(D)==9 and set(d["approval_status"] for d in D)=={"APPROVED"}
assert all(any(g["decision_id"]==i and g["kind"]==k for g in gold) for i in ids for k in ("positive","negative"))
print(json.dumps({"decisions":len(D),"golden_vectors":len(gold),"positive":sum(g['kind']=='positive' for g in gold),"negative":sum(g['kind']=='negative' for g in gold),"hash_findings":len(find),"status":"APPROVED","approved_option":"A","decision_version":"B1-A-DECISIONS 1.0.0"},ensure_ascii=False))
