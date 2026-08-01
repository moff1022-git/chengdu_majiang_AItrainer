from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/spec-v3/semantic-completion/reviews"
BASE = ROOT / "docs/spec-v3/semantic-completion"
OUT.mkdir(parents=True, exist_ok=True)

SPEC_STATE = "03-unit-specs/deterministic_rule_state_specs.md §STATE-010"
SPEC_ALGO = "03-unit-specs/deterministic_algorithm_scoring_specs.md"
CONTRACT = "contracts/common_contracts.md"
REGISTRY = "07-traceability/parameter_registry.csv"


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


semantic_fields = [
    "delta_id", "unit_id", "target_semantic", "current_behavior", "missing_behavior",
    "source_reference", "semantic_delta", "code_location", "test_oracle", "boundary_cases",
    "runtime_evidence", "acceptance_criteria", "interface_impact", "blocked_by",
]


def sd(i: int, unit: str, target: str, current: str, missing: str, source: str,
       change: str, code: str, oracle: str, boundary: str, runtime: str,
       ac: str, impact: str = "NO_INTERFACE_CHANGE", blocked: str = "") -> dict[str, str]:
    return dict(delta_id=f"SEM-{unit}-{i:02d}", unit_id=unit, target_semantic=target,
                current_behavior=current, missing_behavior=missing, source_reference=source,
                semantic_delta=change, code_location=code, test_oracle=oracle,
                boundary_cases=boundary, runtime_evidence=runtime,
                acceptance_criteria=ac, interface_impact=impact, blocked_by=blocked)


S: list[dict[str, str]] = []
S += [
sd(1,"STATE-010","注册GP-001..027与RP-001..033且ID唯一","GP/RP常量和60条trace存在","没有权威定义对象的type/unit/min/max/default/nullable/visibility/source完整注册",f"{SPEC_STATE} §§6,11,15; {CONTRACT} §8; {REGISTRY}","建立60项不可变ParameterDefinition注册表并启动时校验唯一性/完整性","players/humanlike/parameter_registry.py (new); config.py; runtime.py","逐ID等于GP-001..027∪RP-001..033；重复/漏项分别精确错误","首尾ID、重复、漏项、错误scope","真实load_config→registry→owned state trace","60项逐字段与来源表一致，重复/漏项零提交"),
sd(2,"STATE-010","字段缺失/null/越界/未知字段语义不同","现有GP字段多为exact-key，RP多为None占位","公共参数定义哪些字段可选及default/nullable没有逐字段冻结",f"{SPEC_STATE} §§11,15,16; {CONTRACT} §§2,8; {REGISTRY}","按定义区分MISSING_REQUIRED、PARAM_NULL、OUT_OF_RANGE、UNKNOWN_PARAMETER/FIELD","parameter_registry.py; config_validation.py (planned)","四类输入各返回不同稳定码且state hash不变","缺失可选、缺失必填、显式null、上下界外、未知键","生产配置加载拒绝trace，before_hash=after_hash","只有注册表声明default的缺省才补值；null仅nullable=true接受",blocked="SPEC-DECISION-STATE-DEFAULTS"),
sd(3,"STATE-010","GP在整场创建时校验冻结","HumanlikeConfig不可变，但与Match创建未形成统一门禁","准确冻结提交点、match identity绑定和热替换拒绝未接线",f"{SPEC_STATE} §§11,14,15; {REGISTRY} GP lifecycle","在STATE-001创建match context前完成GP commit；提交后任何写返回LIFECYCLE_VIOLATION","players/humanlike/config.py; engine/orchestrator.py; planned registry","冻结前可构造、冻结后任一GP写失败且版本/hash不变","创建失败、重复freeze、跨match复用、热替换","真实orchestrator创建match的STATE-010 accepted trace","GP仅在新match或新规则版本创建时变化"),
sd(4,"STATE-010","RP按局创建、授权事件更新、局末冻结归档、新局重建","RoundRuntime有create/apply/decision/finalize，无归档对象和完整授权表","33项准确创建/更新/reset/archive时点与按ID授权事件表不完整",f"{SPEC_STATE} §§11,12,15; {REGISTRY} RP lifecycle","以registry lifecycle生成RP授权矩阵；round_start创建，事件后按定义更新，round_end finalize+archive，新局新实例","players/humanlike/runtime.py; parameter_registry.py","每个RP至少一个允许事件和一个拒绝事件；archive不可变；新局无旧局瞬时值","未开始、active、deciding、finalized、重复归档、迟到事件","真实一局从deal到settlement的RP lifecycle trace","RP只在来源表授权时点更新，归档后不可写，新局仅显式跨局输入可继承",blocked="SPEC-DECISION-RP-ARCHIVE"),
sd(5,"STATE-010","四座profile独立且不得串座","4个PlayerProfile及GP-024..027深冻结对象独立","缺少owner字段、seat授权校验和全生命周期串座防护","STATE-010 §§10,11,15,17; common_contracts §2 SeatId","每项seat-owned状态绑定owner_seat；读写必须匹配actor/seat；四座独立快照","config.py; runtime.py; parameter_registry.py","只修改seat2授权RP，其他三座逐字段/hash不变；错误seat=PROFILE_MISMATCH","seat -1/4、重复seat、交换容器顺序、跨座引用","生产四座装配与一局更新trace含每座独立hash","任何单座事件不得改变其他座owned parameter state"),
sd(6,"STATE-010","RECEIVED→VALIDATED→RESOLVED→COMMITTED或REJECTED，提交仅一次","config校验和settings原子文件替换各自存在，无统一权威事务","缺少event_id幂等/迟到/冲突、版本CAS和失败零写入事务","STATE-010 §§12,14,17","实现单写者compare-and-swap事务；先在临时结果完成全校验再一次提交","parameter_registry.py; runtime.py; settings_service.py adapter","每个失败注入点before snapshot/hash/version=after；成功version+1；重复event拒绝","解析/迁移/resolve/commit前后故障、重复和乱序event","生产调用trace记录phase/version/hash前后","失败无部分输出，成功只提交一次，并发排列等价串行"),
sd(7,"STATE-010","输出owned state、accepted、next version、稳定错误、audit ref、fingerprint","当前HumanlikeConfig/RuntimeSnapshot没有统一结果信封","缺少规范结果信封及deterministic fingerprint输入集合","STATE-010 §13","新增模块内部State010Result，不改变Frozen跨模块DTO","parameter_registry.py","固定输入golden逐字段/指纹相等；失败result=null","纯查询、失败、成功、hash字段缺失","生产trace保存输入/输出hash和audit_ref","结果字段齐全且fingerprint对canonical输入0误差","COMPATIBLE_EXTENSION"),
sd(8,"STATE-010","逐座/阶段可见性，种子值私有","策略目前消费HumanlikeConfig及PlayerView；无统一owned-state投影","必须阻止原始registry/seed/private lifecycle进入策略","STATE-010 §§5,9,15,18; common_contracts §§1,8","策略仅消费现有PlayerView白名单及非敏感config_hash，不传registry对象或seed","parameter_registry.py; player.py/view.py adapters","隐藏字段删除/扰动后同visible state决策一致；对象图不可达私有字段","对象引用、缓存、日志、派生字段投毒","production decision trace的输入schema白名单","策略侧不可取得私有参数源、seed或未来生命周期信息"),
]
S += [
sd(1,"ALGO-009","解析→版本→逐迁移→默认→类型/范围→交叉约束→拒未知→canonical/hash→冻结","load_config先根字段exact校验及兼容组合，再仅执行1.0/2.0→1.1/2.1迁移","当前顺序与Locked不一致；无统一逐阶段结果",f"{SPEC_ALGO} §ALGO-009 §§3,5","严格按Locked顺序纯函数流水线；每阶段只产临时值","engine/config_validation.py (new); players/humanlike/config.py","阶段故障注入验证后续阶段不执行且无输出","解析失败、未知版本、每一步迁移失败","真实settings/load_config阶段trace","阶段顺序固定，任一步失败result=null"),
sd(2,"ALGO-009","每个支持版本存在唯一逐步迁移路径且幂等","compatibility.json列组合；代码仅一条特例迁移","没有冻结完整版本节点/边/废弃字段转换",f"{SPEC_ALGO} §ALGO-009 §§3,5,10,13; versioning_policy.md","建立显式migration graph和逐边纯迁移函数；不允许跳跃或猜测","config_validation.py; configs/humanlike_v2/compatibility.json","每个声明旧版本有唯一到current路径；二次迁移字节不变","无路径、多路径、循环、未来版本、重复迁移","生产旧配置加载trace列migration_steps","所有受支持版本路径由批准决策逐边列明",blocked="SPEC-DECISION-MIGRATION-GRAPH"),
sd(3,"ALGO-009","未知字段显式拒绝；extensions仅在声明容器内处理","根和多数GP exact-key拒绝；GP-002/004有extensions","Locked未定义extensions元素schema、是否参与hash及迁移；废弃字段策略不全",f"{SPEC_ALGO} §ALGO-009 §§5,7,11; common_contracts §10","普通未知键PARAM_UNKNOWN；废弃键仅由特定迁移消费；extensions按批准schema保留并参与canonical hash","config_validation.py; config.py","未知键拒绝；已废弃键只在对应source version迁移；extensions顺序/内容golden","未知根/GP/profile键、废弃键、新extension","生产loader accepted/error trace","不得静默丢字段；extension处理逐项可预测",blocked="SPEC-DECISION-EXTENSIONS"),
sd(4,"ALGO-009","缺省与null不同；仅明确可选字段允许null","EngineConfig大量get/default/int/bool强制转换；Humanlike exact字段但early_end_score可null","60参数逐字段required/default/nullable表未冻结",f"{SPEC_ALGO} §ALGO-009 §7; common_contracts §§2,8; {REGISTRY}","只在registry定义default时对缺失应用Locked默认；显式null仅nullable=true接受","config_validation.py; parameter_registry.py; engine/config.py adapter","缺失必填/缺失有默认/null可空/null不可空四向量","false/0/empty不得当缺失；嵌套字段","真实配置加载defaults审计字段","defaults列表只包含实际应用项，其他情况稳定错误",blocked="SPEC-DECISION-STATE-DEFAULTS"),
sd(5,"ALGO-009","禁止NaN/Inf，Decimal按字段scale半偶","Humanlike json dumps禁非有限输出但_number接受float后范围通常拒绝；EngineConfig会强转","输入parse、嵌套值、-0及Decimal scale未统一","ALGO-009 §§2,6,7,13","JSON解析后递归拒非有限；按批准numeric canonical策略标准化","config_validation.py","NaN,+Inf,-Inf各层均NON_FINITE；无提交","字符串NaN、1e309、Decimal边界、-0.0","生产拒绝trace不含非法原值","非有限在hash前拒绝且结果为空",blocked="SPEC-DECISION-CANONICAL-NUMBER"),
sd(6,"ALGO-009","canonical UTF-8 JSON键序、固定数字、无NaN/Inf","现有ensure_ascii=False/sort_keys/compact/allow_nan=False","Unicode规范化、键排序基准、整数/浮点编码、-0尚未精确冻结",f"{SPEC_ALGO} §ALGO-009 §§3,4,6,10; common_contracts header","选定并文档化唯一字节算法，固化跨语言golden；hash=SHA256(bytes)","config_validation.py; canonical_json utility","包含组合/分解Unicode、大整数、1.0、指数、-0的固定bytes+hash golden","NFC/NFD、非BMP、转义、2^53±1、-0、尾零、指数","生产trace记录canonical_hash和算法版本，不记录敏感原文","跨进程/语言逐字节一致",blocked="SPEC-DECISION-CANONICAL-NUMBER|SPEC-DECISION-CANONICAL-UNICODE"),
sd(7,"ALGO-009","迁移失败零提交","settings_service文件写有临时文件原子replace；内存迁移无统一事务结果","无法证明所有迁移失败均保留上一配置和文件","ALGO-009 §5; STATE-010 §§12,14","迁移/验证/hash全在临时对象；成功后一次替换/冻结","config_validation.py; settings_service.py","每阶段异常后目标文件bytes与active config hash不变","磁盘满模拟、invalid target、并发保存、崩溃点","真实settings save failure trace","失败无文件/内存部分状态"),
sd(8,"ALGO-009","失败返回显式错误，不以旧配置伪装成功","settings保存失败抛异常；运行中自然保留旧对象","Locked未说明加载/热重载失败是否可继续使用上一有效配置及如何标记",f"{SPEC_ALGO} §ALGO-009 §§5,9,13; common_contracts §8","禁止静默fallback；是否允许显式degraded继续由规格决策；若允许必须accepted=false且old hash明确","settings_service.py; config manager","失败场景不会返回新accepted配置；旧配置使用行为匹配批准决策","启动加载失败与热重载失败分别测试","生产trace标识attempted_hash/active_hash/error","未批准前不实现自动回退",blocked="SPEC-DECISION-CONFIG-FALLBACK"),
]
S += [
sd(1,"ALGO-011","版本化域隔离公式生成master和注册流seed","当前master=BLAKE2b(id,8)，dice/exchange XOR","规范公式未实现",f"{SPEC_ALGO} §ALGO-011 §§1,3,4","实现v2纯函数：domain+长度前缀+id+versions→master；master+流名+版本→seed","engine/game_id.py","规范字节拼接和seed golden 0误差","1/256字节ID、uint16边界、Unicode字节长度","create_dealt_game生产trace记录版本和seed hashes","同ID/版本/流逐字段一致，域间不同"),
sd(2,"ALGO-011","旧版保留回放且shuffle/dice/exchange golden不变","derive_seeds使用旧master/XOR并已进入deal","原设计用新公式覆盖旧流会破坏golden","ALGO-011 §4 ‘旧版保留回放’","保留legacy-v1 derive_seeds原字节/数值；新增规范版本走独立入口，绝不改变legacy函数结果","engine/game_id.py; engine/deal.py","现有全部deal/dice/shuffle golden逐字段不变；新v2独立golden","旧ID空白规范化、历史存档","旧回放生产链输出hash与变更前一致","legacy-v1结果零变化；v2不复用XOR"),
sd(3,"ALGO-011","algorithm/rng version明确选择","Frozen SeedTrace要求algorithm_version；当前API无版本参数","缺省版本、旧/新回放选择规则未冻结",f"{SPEC_ALGO} §ALGO-011 §§1,4,13; common_contracts §8","新录制必须显式写版本；回放从持久化元数据选择；缺失版本行为等待决策，不按当前代码猜测","engine/game_id.py; persistence/replay adapters","版本缺失/未知/legacy/new四向量返回批准结果","缺字段、null、0、未来版本、版本冲突","真实旧/新回放trace显示选择来源","不允许运行环境或当前默认悄然改变历史结果",blocked="SPEC-DECISION-RNG-VERSION"),
sd(4,"ALGO-011","注册流名唯一；新增流不改旧流；未知流拒绝","仅固定DerivedSeeds字段，无registry","注册流全集和命名语法未集中","ALGO-011 §§1,5,9,10,13","建立版本化不可变stream registry；派生按名称纯函数；未知=STREAM_UNKNOWN","engine/game_id.py","注册顺序置换不影响每流seed；重复名启动失败；未知拒绝","空名、长名、Unicode、大小写、重复","生产trace只列已消费流和hash","每版本注册表唯一且新增名字不改变已有seed"),
sd(5,"ALGO-011","worker并发不依赖调度顺序","训练/策略仍有分散Random；现有derive无worker坐标","若用共享可变index会使完成顺序改变结果",f"{SPEC_ALGO} §ALGO-011 §§3,5,10; common_contracts §8","派生为无状态函数(seed(stream, logical_consumer, logical_index))；禁止全局next()/共享计数器","engine/game_id.py; later consumer adapters","随机化提交/完成顺序100次，每个逻辑坐标结果相同","worker增减、重试、取消、分片、乱序","真实多worker运行trace按逻辑坐标重放一致","结果仅由冻结坐标决定，不含OS线程/进程号/调度序"),
sd(6,"ALGO-011","逻辑consumer/index坐标稳定","Frozen SeedTrace有index_before/after，但未定义坐标语义","不同消费类型的index分配规则未冻结",f"{SPEC_ALGO} §ALGO-011 §§1,3,10; common_contracts §§7,8","坐标至少含stream_name+consumer_id+logical_event_id+draw_index；每次调用显式传入，不内部递增","engine/game_id.py","同坐标同seed；任一维变化域隔离；重试同坐标不前移","同事件多样本、批次重排、回放重试、取消","生产trace记录安全的consumer hash与logical index","禁止共享可变stream index；坐标可从事件日志恢复",blocked="SPEC-DECISION-RNG-COORDINATE"),
sd(7,"ALGO-011","SeedTrace满足Frozen字段且不泄露未来信息","当前无SeedTrace；DecisionResult契约要求它","Frozen结构含master_seed和index，但策略可见会泄露；需要受控投影","common_contracts §§6,8; ALGO-011 §14","引擎/审计持有完整SeedTrace；策略边界仅给rng_used和不透明trace_ref，不给seed/master/index/未来流","engine/game_id.py; decision/audit adapters","策略对象图与序列化均无敏感字段；审计可复算；持久化加密/受限","日志、异常、repr、缓存、派生hash投毒","生产decision trace通过schema白名单检查","策略无法从任何字段推导牌墙、对手行为或后续噪声","COMPATIBLE_EXTENSION"),
sd(8,"ALGO-011","输入失败不产生部分流映射","当前单个derive全量返回，无版本/registry校验","新多流实现必须保证未知/重复/版本错零输出","ALGO-011 §§5,7,9,13","先验证ID/版本/registry/坐标，再构造不可变映射","engine/game_id.py","任一非法输入result=null且无缓存/索引变化","空/超长/null ID、未知version/stream、index溢出","生产拒绝trace仅含安全hash和error","失败无部分seed映射或可观察index变化"),
]

test_fields = ["delta_id","unit_id","test_type","target_semantic_delta_ids","test_oracle","fixtures","boundary_cases","production_code_path","acceptance_criteria"]
T: list[dict[str,str]]=[]
def td(i,u,typ,ids,oracle,fixtures,boundary,path,ac):
    T.append(dict(delta_id=f"TEST-{u}-{i:02d}",unit_id=u,test_type=typ,target_semantic_delta_ids=ids,test_oracle=oracle,fixtures=fixtures,boundary_cases=boundary,production_code_path=path,acceptance_criteria=ac))
td(1,"STATE-010","direct","SEM-STATE-010-01|02","registry逐ID/逐字段等于Locked来源；四类错误码及零写入","60-row registry fixtures","missing/null/range/unknown/duplicate","真实registry API","断言业务结果和state hash，不仅断言可调用")
td(2,"STATE-010","state-machine","SEM-STATE-010-03|04|06","每个合法转移得到准确phase/version；非法转移拒绝且snapshot不变","GP/RP event sequences","重复/迟到/并发/归档后写","真实STATE-010 transaction API","状态机与原子性逐转移判定")
td(3,"STATE-010","visibility","SEM-STATE-010-05|08","扰动私有字段不改变同可见状态决策且策略对象图无私有字段","4-seat poison fixtures","引用/cache/log/派生字段","orchestrator→player decision","四座隔离与无泄漏")
td(1,"ALGO-009","pipeline","SEM-ALGO-009-01|02|07","逐阶段spy/结果证明固定顺序；每个失败点active bytes/hash不变","每版本配置fixture","无路径/循环/中途故障","settings/load_config production entry","迁移顺序和原子性客观可判")
td(2,"ALGO-009","schema","SEM-ALGO-009-03|04|05","未知/废弃/extensions/missing/null/nonfinite逐项准确结果或错误码","cross-product fixtures","false/0/empty/-0/NaN/Inf","真实validation API","每一输入类别有唯一oracle")
td(3,"ALGO-009","canonical-golden","SEM-ALGO-009-06","canonical bytes与SHA-256固定向量逐字节相等并跨进程一致","Unicode/number golden","NFC/NFD/nonBMP/2^53/-0/exponent","真实hash API","不能只比较两次hash相等")
td(4,"ALGO-009","integration","SEM-ALGO-009-01|07|08","settings保存/加载后active config及文件符合批准fallback语义","startup/hot-reload fixtures","失败恢复/并发保存","settings_service production chain","E3与E4分离；E4必须真实入口")
td(1,"ALGO-011","legacy-golden","SEM-ALGO-011-02|03","旧derive、dice、shuffle、hands、wall逐字段等于现有golden","captured legacy vectors","旧回放缺版本","create_dealt_game","任何legacy变化失败")
td(2,"ALGO-011","v2-golden","SEM-ALGO-011-01|04","规范拼接bytes/master/stream seed固定向量0误差","v2 byte vectors","ID长度/版本/stream","真实named stream API","不能只断言同调用相等")
td(3,"ALGO-011","concurrency","SEM-ALGO-011-05|06","100种调度排列每个逻辑坐标输出相同；重试不推进其他坐标","worker schedule fixtures","增减/取消/重试/乱序","trainer worker production adapter","不得使用共享mutable index")
td(4,"ALGO-011","visibility","SEM-ALGO-011-07","策略序列化字段白名单且无法推导future；审计可复算","SeedTrace poison fixtures","repr/log/cache/hash","real decision chain","敏感字段策略侧不可达")
td(5,"ALGO-011","error-atomicity","SEM-ALGO-011-08","所有非法输入result=null，映射/cache/index前后相同","invalid vectors","null/empty/too-long/unknown/overflow","named stream production API","稳定错误码且零部分输出")

evidence_fields=["delta_id","unit_id","evidence_type","semantic_or_test_refs","required_fields","production_call_chain","collection_method","acceptance_criteria"]
E=[]
for u,chain in [("STATE-010","settings/orchestrator→load/registry→owned state"),("ALGO-009","settings_service→validation/migration→frozen config"),("ALGO-011","create_dealt_game/replay/worker→named stream derivation")]:
    E.append(dict(delta_id=f"EVIDENCE-{u}-01",unit_id=u,evidence_type="E4_RUNTIME",semantic_or_test_refs=f"SEM-{u}-*|TEST-{u}-*",required_fields="unit_id,scenario/game_id,input_hash,versions,seed_ref,intermediate_stage/output_hash,call_site,test_or_replay_ref,accepted,error_code,latency_us",production_call_chain=chain,collection_method="instrument real production entry; no test-only facade",acceptance_criteria="至少一条正常和全部hard failure来自真实生产调用链且可回放"))
    E.append(dict(delta_id=f"EVIDENCE-{u}-02",unit_id=u,evidence_type="E5_TRACE",semantic_or_test_refs=f"SEM-{u}-*|TEST-{u}-*|EVIDENCE-{u}-01",required_fields="Locked clause→delta→code symbol→test→runtime artifact→AC",production_call_chain=chain,collection_method="same-scope manifest with artifact SHA-256",acceptance_criteria="每条语义delta有代码、oracle、E4或明确不适用；无TODO/仅日志存在证明"))

visibility = [
dict(field="game_id",engine_visible="yes",strategy_visible="opaque request/game identity only",trainer_visible="yes",audit_visible="hash preferred",persisted="yes",sensitive="conditional",future_information_risk="low alone",rationale="Frozen字段；策略无需原始值进行随机派生"),
dict(field="algorithm_version",engine_visible="yes",strategy_visible="version label only",trainer_visible="yes",audit_visible="yes",persisted="yes",sensitive="no",future_information_risk="low",rationale="回放选择必需，不提供seed能力"),
dict(field="master_seed",engine_visible="yes",strategy_visible="NO",trainer_visible="restricted controller only",audit_visible="restricted",persisted="restricted/encrypted",sensitive="yes",future_information_risk="critical",rationale="可推导牌墙及全部子流"),
dict(field="stream_name",engine_visible="yes",strategy_visible="rng_used boolean or opaque trace_ref only",trainer_visible="own-domain names only",audit_visible="yes",persisted="audit restricted",sensitive="yes",future_information_risk="medium",rationale="暴露后续随机域和行为类型"),
dict(field="index_before",engine_visible="yes",strategy_visible="NO",trainer_visible="own logical coordinate only",audit_visible="yes",persisted="audit restricted",sensitive="yes",future_information_risk="high",rationale="与seed/流结合可定位未来抽样"),
dict(field="index_after",engine_visible="yes",strategy_visible="NO",trainer_visible="own logical coordinate only",audit_visible="yes",persisted="audit restricted",sensitive="yes",future_information_risk="high",rationale="泄露消费量和下一位置"),
dict(field="seed_hash",engine_visible="yes",strategy_visible="opaque trace_ref only; raw hash NO",trainer_visible="restricted",audit_visible="yes",persisted="yes restricted",sensitive="yes",future_information_risk="medium",rationale="即使单向也可作为跨局关联/字典验证材料"),
dict(field="consumer_id_hash (compatible audit extension)",engine_visible="yes",strategy_visible="NO",trainer_visible="own job ref",audit_visible="yes",persisted="audit only",sensitive="yes",future_information_risk="low",rationale="审计并发坐标，不进入Frozen SeedTrace/策略DTO"),
dict(field="logical_index_hash (compatible audit extension)",engine_visible="yes",strategy_visible="NO",trainer_visible="own job ref",audit_visible="yes",persisted="audit only",sensitive="yes",future_information_risk="low",rationale="证明调度无关，不暴露原始future index"),
]

interfaces = [
dict(item="ParameterDefinition/owned state internal DTO",unit_id="STATE-010",change="新增内部不可变注册与结果对象",classification="NO_INTERFACE_CHANGE",frozen_surface="none",rationale="不跨Task16公共边界；现有消费者通过适配器读取",approval_required="no"),
dict(item="State010Result error_code/version/hash/audit_ref",unit_id="STATE-010",change="内部结果信封",classification="COMPATIBLE_EXTENSION",frozen_surface="audit/internal adapter",rationale="稳定错误族可扩展领域码；不删除或改Frozen字段",approval_required="no; schema decision still required"),
dict(item="FrozenConfig",unit_id="ALGO-009",change="新增内部冻结配置对象",classification="NO_INTERFACE_CHANGE",frozen_surface="none",rationale="Task16只冻结参数语义和hash，未冻结名为FrozenConfig的DTO；不得替代现有公共对象",approval_required="no"),
dict(item="config hash/version/defaults/migration_steps audit fields",unit_id="ALGO-009",change="审计记录增加可选元数据",classification="COMPATIBLE_EXTENSION",frozen_surface="audit record",rationale="可选审计字段且旧消费者可忽略；hash本身已Frozen必填",approval_required="no; canonical decisions required"),
dict(item="SeedTrace existing seven fields",unit_id="ALGO-011",change="实现Task16已冻结结构",classification="NO_INTERFACE_CHANGE",frozen_surface="common_contracts §8",rationale="不是新增接口；字段已Frozen。实现不得改名、删除或改变类型",approval_required="no"),
dict(item="SeedTrace consumer/logical coordinate raw fields",unit_id="ALGO-011",change="若加入Frozen SeedTrace必填字段",classification="BREAKING_CHANGE_REQUIRED",frozen_surface="common_contracts §8",rationale="改变Frozen结构并可能泄漏；本设计禁止加入，改用独立受限审计扩展",approval_required="yes if ever proposed"),
dict(item="opaque seed_trace_ref/rng_used strategy projection",unit_id="ALGO-011",change="策略只见不透明引用",classification="COMPATIBLE_EXTENSION",frozen_surface="DecisionExplanation/DecisionResult",rationale="保留必填seed_trace但序列化投影需与Frozen schema协调；不得传完整敏感值",approval_required="contract test required; if schema mandates full object then interface proposal required"),
]
interface_details={
"ParameterDefinition/owned state internal DTO":("source_config,phase,event_id,game_id,state_version,ruleset_hash,seed_ref,actor,seat","owned state,accepted,next_state_version,error_code,audit_ref,fingerprint","DUPLICATE_PARAMETER,UNKNOWN_PARAMETER,OUT_OF_RANGE,LIFECYCLE_VIOLATION,PROFILE_MISMATCH,SCHEMA_INVALID,VERSION_CONFLICT,UNAUTHORIZED","不新增跨模块持久化；归档使用既有状态/审计适配器","config loader,RoundRuntime,STATE-001 orchestrator","旧调用方保持；仅内部适配"),
"State010Result error_code/version/hash/audit_ref":("同STATE-010输入","result/accepted/next_state_version/reason/audit_ref/fingerprint","STATE-010领域码加Task16通用码","审计JSON增加可选字段，旧reader忽略","orchestrator,trace writer","可选扩展；若变为必填则需schema审批"),
"FrozenConfig":("raw JSON,schema,registry,migration path","immutable normalized config,canonical bytes,config_hash或result=null","CONFIG_PARSE,SCHEMA_VERSION_UNSUPPORTED,PARAM_UNKNOWN,PARAM_TYPE,PARAM_RANGE,PARAM_NULL,CROSS_CONSTRAINT,MIGRATION_FAILED,NON_FINITE","沿用配置JSON；不持久化Python DTO","settings_service,load_config,STATE-001","旧HumanlikeConfig/EngineConfig由适配器继续消费"),
"config hash/version/defaults/migration_steps audit fields":("source_hash,schema before/after,stage outcomes","canonical_hash,defaults,migration_steps,errors","同ALGO-009稳定码","审计JSON可选字段；config文件格式不因审计字段改变","audit writer,AUDIT-011","旧审计reader忽略未知可选字段；schema须验证"),
"SeedTrace existing seven fields":("game_id,algorithm_version,registered stream,logical coordinate","game_id,algorithm_version,master_seed,stream_name,index_before,index_after,seed_hash","GAME_ID_TYPE,GAME_ID_EMPTY,GAME_ID_TOO_LONG,RNG_VERSION_UNKNOWN,STREAM_UNKNOWN","回放/审计受限JSON按Frozen七字段","deal,replay,trainer controller,audit","严格复用Frozen名称和类型；不得增加必填字段"),
"SeedTrace consumer/logical coordinate raw fields":("consumer_id,logical event/draw index","若直接加入将改变SeedTrace schema","VERSION_CONFLICT或schema错误需新增定义","会改变Frozen回放JSON","DecisionResult readers,replay,audit","不兼容；本设计不实施"),
"opaque seed_trace_ref/rng_used strategy projection":("完整SeedTrace在引擎边界内","策略仅rng_used与opaque trace_ref；无master/stream/index/seed_hash","FORBIDDEN_INPUT,VISIBILITY_LEAK","策略Decision投影；完整trace单独受限持久化","policy,DecisionResult serializer,audit","若Frozen DecisionResult强制完整对象则BLOCKED_BY_INTERFACE_APPROVAL"),
}
for row in interfaces:
    inp,out,err,persist,callers,compat=interface_details[row["item"]]
    row.update(input_fields=inp,output_fields=out,error_codes=err,persisted_format=persist,callers=callers,caller_compatibility=compat)

write_csv(OUT/"B1-A_semantic_deltas.csv",S,semantic_fields)
write_csv(OUT/"B1-A_test_deltas.csv",T,test_fields)
write_csv(OUT/"B1-A_evidence_deltas.csv",E,evidence_fields)
write_csv(OUT/"B1-A_seed_visibility_matrix.csv",visibility,list(visibility[0]))
write_csv(OUT/"B1-A_interface_impact.csv",interfaces,list(interfaces[0]))

registry=list(csv.DictReader((ROOT/"docs/spec-v3/07-traceability/parameter_registry.csv").open(encoding="utf-8-sig")))
param_rows="\n".join(f"| {r['parameter_id']} | {r['parameter_name']} | {r['scope']} | {r['lifecycle_or_update']} |" for r in registry)
blockers="""| 决策ID | 未冻结问题 | 影响单元 | 最小批准内容 |
|---|---|---|---|
| SPEC-DECISION-STATE-DEFAULTS | 60项逐字段 required/default/nullable 未完整冻结 | STATE-010, ALGO-009 | 逐字段三列和值；明确缺失与null |
| SPEC-DECISION-RP-ARCHIVE | RP归档载荷、保留期及跨局继承边界不完整 | STATE-010 | 33项archive/reset/carry规则 |
| SPEC-DECISION-MIGRATION-GRAPH | 支持版本的完整节点/逐边迁移/废弃字段图未冻结 | ALGO-009 | 每条from→to及字段变换golden |
| SPEC-DECISION-EXTENSIONS | extensions元素schema、排序、hash和迁移策略未冻结 | ALGO-009 | 容器schema及canonical参与规则 |
| SPEC-DECISION-CANONICAL-NUMBER | float/Decimal/整数/-0/指数准确字节规则未冻结 | ALGO-009 | 选定算法和跨语言golden |
| SPEC-DECISION-CANONICAL-UNICODE | Unicode正规化、转义及键序基准未冻结 | ALGO-009 | NFC与否、码点/UTF-16/UTF-8排序、转义golden |
| SPEC-DECISION-CONFIG-FALLBACK | 启动/热重载失败是否继续旧配置未冻结 | ALGO-009 | 两场景的accepted/active/error语义 |
| SPEC-DECISION-RNG-VERSION | 缺省版本、旧/新回放版本选择未冻结 | ALGO-011 | 新录制、旧缺字段、新回放各选择规则 |
| SPEC-DECISION-RNG-COORDINATE | consumer/logical index坐标schema未冻结 | ALGO-011 | 坐标字段、稳定ID与重试语义 |
"""

review=f"""# Task 18B-R1：B1-A 实现设计独立复审

状态：**BLOCKED_BY_SPEC_DECISION**  
范围：STATE-010、ALGO-009、ALGO-011；未修改业务代码、测试断言、Locked规格、Frozen契约或Task 17/18A状态。
当前回归基线：Windows Python 3.12.10，387 passed，0 failed，0 skipped，154.91s。

## 技术结论

原Task 18B的`IMPLEMENTATION_READY`不能成立。原delta把生产语义、测试和证据混在同一编号中，AC使用同一句泛化条件，且对canonical数字/Unicode、迁移版本图、默认值与null、旧/新随机版本选择、并发逻辑坐标作了无来源推断。R1已拆为{len(S)}条semantic delta、{len(T)}条test delta和{len(E)}条evidence delta；测试/证据不再计作生产语义完成。

STATE-010有可编码子集，但ALGO-009与ALGO-011的字节级/回放级选择会固化长期兼容行为。依据STATE-010规格§6“歧义必须新增决策记录，不静默推断”，B1-A整体在这些决策批准前不得开始编码。

## 三个单元的真实生产语义缺口

- **STATE-010**：缺完整60项ParameterDefinition、逐字段required/default/nullable、GP与match的冻结门禁、33项RP授权生命周期/归档、owner/seat隔离、统一事务/CAS/失败零写入、结果信封及策略投影。
- **ALGO-009**：现有loader不是Locked顺序；仅有单条兼容迁移；缺完整迁移图、废弃/extensions策略、逐字段缺省/null策略、数字与Unicode canonical bytes、统一错误/原子事务和明确fallback语义。
- **ALGO-011**：仅有legacy master+XOR三流；缺规范v2域隔离、版本选择、版本化流注册、纯逻辑坐标、无共享index的并发确定性、原子错误和SeedTrace安全投影。

## 必须先批准的规格决策

{blockers}

## STATE-010：60个准确参数ID与生命周期来源

ID闭集为`GP-001..GP-027`和`RP-001..RP-033`，准确展开如下。字段具体范围以parameter_registry.csv为准；该表有range/lifecycle，但没有把每个嵌套字段完整结构化为required/default/nullable，因此不能由实现者补猜。

| ID | 名称 | scope | Locked生命周期摘要 |
|---|---|---|---|
{param_rows}

### 字段与状态机

- ParameterDefinition字段：`parameter_id,parameter_version,type,unit,min,max,default,nullable,visibility,source,value`。在逐字段决策批准前，不得把缺失统一解释为默认。
- 缺失必填→`SCHEMA_INVALID/PARAM_*`；显式null且nullable=false→`PARAM_NULL`；类型正确但闭区间外→`OUT_OF_RANGE/PARAM_RANGE`；未注册ID/字段→`UNKNOWN_PARAMETER/PARAM_UNKNOWN`。四者失败均零写入。
- GP在STATE-001创建immutable match context前冻结；冻结后整个match只读，新match/新规则版本才可创建新GP快照。
- RP在round start创建；只在parameter_registry声明的事件更新；round settlement后finalize并归档；新局创建新实例，不隐式携带瞬时值。归档载荷/跨局继承仍需决策。
- 四座owned state必须含owner_seat并分别冻结；seat事件只能写本座授权项。
- 事务状态机：`RECEIVED→VALIDATED→RESOLVED→COMMITTED`；`RECEIVED|VALIDATED→REJECTED`。成功CAS一次且version+1，失败snapshot/hash/version逐字段不变。

## ALGO-009：准确流水线与canonical门禁

Locked顺序是：`parse → version identify → stepwise migrate → apply declared defaults → type/range → cross constraints → reject unknown → canonical bytes/hash → freeze/commit`。迁移在临时对象完成，任何失败`result=null`且active config/文件不变。

当前只能冻结的canonical共同部分是UTF-8、键排序、紧凑无空白、禁止NaN/Inf、SHA-256小写hex。Unicode正规化/转义/键比较、整数与float/Decimal编码、指数、尾零和`-0`未给唯一规范，所以不能把Python `json.dumps`行为升级成跨语言Locked规范。性能§8的`1MB≤50ms`可作为ALGO-009 Locked阈值；其他无阈值项只能记录P50/P95/P99基线。

未知普通字段必须拒绝；废弃字段只能由明确source-version迁移消费；extensions不得当普通未知字段，但其元素schema、排序、hash参与和迁移仍需决策。启动失败/热重载失败均不得伪装accepted；是否显式继续上一有效配置等待决策。

## ALGO-011：legacy兼容与并发确定性

- `legacy-v1`路径原样保留当前`master=BLAKE2b(id,8)`及dice/exchange XOR，现有shuffle/dice/exchange/deal golden必须零变化。
- 新规范版本使用Locked公式，走独立版本化入口；禁止让新公式覆盖legacy函数。
- 新录制应显式持久化algorithm/rng version；旧回放和缺失版本的选择未冻结，批准前不设置默认。
- 流注册表按版本不可变、名称唯一；未知流=`STREAM_UNKNOWN`；新增流不能改变已有流。
- 并发派生必须是无状态纯函数，坐标来自稳定`stream_name + logical consumer + logical event + draw index`，调用者显式传入；禁止共享mutable stream index、worker完成序号、线程/进程号或系统时间。坐标准确schema仍需决策。

## SeedTrace字段级可见性

完整矩阵见`B1-A_seed_visibility_matrix.csv`。策略不得取得`master_seed`、原始`stream_name`、`index_before/after`、原始`seed_hash`或consumer/logical index；只能取得`rng_used`及不可逆、不可关联未来流的opaque trace reference。完整Frozen SeedTrace只允许引擎、受限trainer controller和审计使用，持久化必须受限。若现有DecisionResult schema强制把完整SeedTrace传给策略，则属于接口冲突，必须另提Frozen变更，而不是放宽可见性。

## 接口影响复评

不再统一判为NO_INTERFACE_CHANGE。内部ParameterDefinition/FrozenConfig和实现既有Frozen SeedTrace属于NO_INTERFACE_CHANGE；新增可选audit字段和内部结果信封属于COMPATIBLE_EXTENSION；向Frozen SeedTrace增加必填坐标字段属于BREAKING_CHANGE_REQUIRED，已明确禁止，改用独立受限审计扩展。逐项见`B1-A_interface_impact.csv`。

## AC复核规则

更新后的42条AC每条都有具体oracle。函数存在、日志存在、测试可调用均不算业务正确性。AC-12：ALGO-009使用Locked `1MB≤50ms`阈值；STATE-010/ALGO-011没有Locked阈值，只记录硬件、样本、P50/P95/P99基线，不作pass/fail。AC-10的E4必须从上述真实生产调用链采集；test-only facade不合格。

## 最终门禁

**BLOCKED_BY_SPEC_DECISION**。不允许开始B1-A整体编码。可以准备决策提案和不改代码的golden向量草案；必须先批准上表9项决策，再复审接口投影和42条AC，才可改为IMPLEMENTATION_READY。
"""
(OUT/"B1-A_design_review.md").write_text(review,encoding="utf-8")

design=f"""# Task 18B-R1：B1-A详细实现设计（修订）

状态：**BLOCKED_BY_SPEC_DECISION / status unchanged**  
批次：`B1-A`；范围：`STATE-010 → ALGO-009 / ALGO-011`

## 结论

原`IMPLEMENTATION_READY`撤回。权威理由和9项阻断决策见`reviews/B1-A_design_review.md`。在决策批准前不得开始业务编码；测试或证据delta不能证明生产语义完成。

## 实施包分离

- 生产语义：`reviews/B1-A_semantic_deltas.csv`（{len(S)}条）。
- 测试补全：`reviews/B1-A_test_deltas.csv`（{len(T)}条），每条指向生产语义delta并有业务oracle。
- 证据补全：`reviews/B1-A_evidence_deltas.csv`（{len(E)}条），E4必须从真实生产入口采集。
- SeedTrace可见性和接口影响分别见对应review CSV。

## 决策批准后的实施顺序

1. 批准required/default/nullable、RP归档、迁移图、extensions、canonical数字/Unicode、fallback、RNG版本和逻辑坐标决策。
2. STATE-010：注册表→GP冻结→RP状态机/归档→四座owner隔离→事务/结果信封→可见性适配。
3. ALGO-009：固定流水线→逐边迁移→schema/default/null→canonical/hash→原子commit/fallback。
4. ALGO-011：冻结legacy golden→实现版本化v2公式/流registry→无状态逻辑坐标→SeedTrace受控投影。
5. 执行test delta；随后由真实settings/orchestrator/deal/replay/worker链采集E4，再建立E5追踪。

## 不可变设计约束

- 旧`derive_seeds`及shuffle/dice/exchange/deal结果零变化；新公式只能在显式新版本入口。
- 无共享可变stream index；worker调度、重试、取消和数量不得进入随机坐标。
- 策略不见master seed、流名、index或seed hash；完整SeedTrace不进入策略对象图。
- canonical hash在规格决策前不得声称跨语言权威；迁移/校验失败无部分内存或文件写入。
- 不新增Frozen必填字段；确需改变必须停止并走接口批准。

## 完成判定

只有9项规格决策Approved、所有semantic delta有唯一Locked语义、42条AC oracle可执行、无未批准breaking change后，才能重新评为`IMPLEMENTATION_READY`。实现完成仍不等于AUDITED。
"""
(BASE/"first_batch_implementation_design.md").write_text(design,encoding="utf-8")

ac_names={1:"Locked规格/决策完整",2:"非占位生产实现",3:"稳定代码入口",4:"生产调用方",5:"参数/版本绑定",6:"原子状态或纯函数",7:"直接测试",8:"边界/异常测试",9:"生产集成测试",10:"E4运行证据",11:"全链追溯",12:"性能",13:"信息隔离",14:"确定性/复现"}
unit_oracles={
"STATE-010":{
1:"决策表中STATE默认/null与RP归档两项为Approved，并给出60项字段表及33项归档规则",
2:"注册表返回恰好GP-001..027和RP-001..033；重复ID=DUPLICATE_PARAMETER，漏项=SCHEMA_INVALID",
3:"registry.resolve(source_config,phase)正常返回owned state；未知ID返回UNKNOWN_PARAMETER且result=null",
4:"orchestrator创建match的E4 call_site经过STATE-010，输出四座owner hash和committed version",
5:"owned state记录parameter_version/ruleset_hash/config_hash；VERSION_CONFLICT时next_state_version不变",
6:"VALIDATED/RESOLVED阶段故障时before_state_hash=after_state_hash；成功仅version+1一次",
7:"直接测试逐项断言60 ID、owner、phase、default来源、accepted、error_code和next_state_version",
8:"缺失必填、允许缺省、null不可空、闭区间外、未知键、重复/迟到event各有准确错误码",
9:"settings→load_config→orchestrator装配四座；修改seat2授权RP后seat0/1/3 hash不变",
10:"真实match创建与一局归档trace包含phase_before/after、version/hash前后及生产call_site",
11:"每个SEM-STATE-010行映射到registry/runtime符号、直接测试、生产trace SHA-256和对应AC",
12:"固定环境分别测60项resolve和33项snapshot的P50/P95/P99；只登记基线，不设通过阈值",
13:"策略对象图无registry、seed_ref和其他座private RP；隐藏字段扰动后DecisionResult相同",
14:"同source config/event序列100次及跨进程owned state/fingerprint逐字段相同；事件排列符合规范排序",
},
"ALGO-009":{
1:"迁移图、extensions、canonical数字/Unicode及fallback五项决策Approved并带字节golden",
2:"给定current配置输出FrozenConfig及64位小写hash；NaN输入result=null,error_code=NON_FINITE",
3:"validate_and_freeze(raw)依次产生migration_steps/defaults/canonical_hash；未知字段=PARAM_UNKNOWN",
4:"settings_service.validate_raw/save_raw的E4 call_site调用统一ALGO-009入口且active hash等于返回hash",
5:"输出formula_version/baseline_version/schema_before_after/config_hash；未知组合=SCHEMA_VERSION_UNSUPPORTED",
6:"解析、每条迁移、default、交叉约束和hash阶段逐点失败时文件bytes及active config hash均不变",
7:"直接测试断言解析→版本→迁移→默认→类型范围→交叉→未知→hash的阶段序列和最终bytes",
8:"missing/null/false/0/empty、NaN/Inf、NFC/NFD、非BMP、2^53±1、-0、指数及未知/废弃键均有golden",
9:"真实settings保存后重新load所得normalized config和hash相等；失败时按批准fallback语义保留或拒绝",
10:"真实settings链E4记录source_hash、schema_before_after、migration_steps、defaults、errors和canonical_hash",
11:"每个SEM-ALGO-009行映射到validation/migration/canonical符号、字节golden、E4 artifact及SHA-256",
12:"1MB输入从parse到freeze在规定环境单次≤50ms，并报告样本数、预热、P50/P95/P99及最大值",
13:"配置原文/私有参数不进入策略或普通日志；策略只取得批准字段与config_hash，投毒不改变公开投影",
14:"键序/空白不同但语义等价输入100次和跨进程canonical bytes/hash完全相同；迁移二次执行字节不变",
},
"ALGO-011":{
1:"RNG版本选择与逻辑坐标两项决策Approved，明确旧缺版本、新录制、新回放和重试规则",
2:"legacy-v1三个seed及deal golden零变化；v2按Locked拼接bytes产生固定master/stream seed",
3:"derive_named_seed(game_id,versions,stream,coordinate)正常返回注册流；未知流=STREAM_UNKNOWN且result=null",
4:"create_dealt_game旧链及新回放/worker链E4均记录所选algorithm_version来源和命名流调用点",
5:"SeedTrace七个Frozen字段类型准确；版本缺失/未知分别按批准规则或RNG_VERSION_UNKNOWN处理",
6:"派生函数不写全局/cache index；非法ID/version/stream/index前后可观察映射完全相同",
7:"直接测试断言domain、长度前缀、id bytes、versions、master bytes、name bytes、rng version和uint64结果",
8:"1/256字节ID、空/257字节/null、uint16/uint64边界、重复/未知流及Unicode名称均有准确输出/错误",
9:"真实deal保持旧wall/hands/dice；真实replay按持久化版本选择；worker乱序仍按逻辑坐标取得同值",
10:"真实deal/replay/worker E4含game_id_hash、versions、algorithm、master_hash、stream_names和seed_hashes",
11:"每个SEM-ALGO-011行映射到game_id符号、legacy/v2/concurrency/visibility测试和真实E4 artifact SHA-256",
12:"固定ID长度/流数量/worker数记录P50/P95/P99及环境；规格无阈值，因此只登记基线",
13:"策略序列化无master_seed、原始stream/index/seed_hash；完整SeedTrace仅引擎/受限trainer/audit可达",
14:"同逻辑坐标100次/跨进程相同；100种worker调度、重试、取消排列不改变各坐标输出",
}}
ac=[]
for u in ("STATE-010","ALGO-009","ALGO-011"):
    sem="|".join(r["delta_id"] for r in S if r["unit_id"]==u)
    tests="|".join(r["delta_id"] for r in T if r["unit_id"]==u)
    for n,name in ac_names.items():
        oracle=unit_oracles[u][n]
        ac.append(dict(unit_id=u,ac_id=f"AC-{u}-{n:02d}",check=name,semantic_delta_ids=sem,test_delta_ids=tests,evidence_delta_ids=f"EVIDENCE-{u}-01|EVIDENCE-{u}-02",objective_test_oracle=oracle,evidence_source=("Locked spec + approved decision record" if n==1 else "planned current-run artifact"),gate_status="BLOCKED" if n==1 else "PLANNED",blocking_reason="9项规格决策未批准" if n==1 else "等待规格门禁后实现/执行"))
write_csv(BASE/"first_batch_acceptance_matrix.csv",ac,list(ac[0]))

# R1补充复核：Task18B生成器曾机械地给83个单元各加一条SEM-PARAMETER，
# 但这些行没有指出具体parameter_id及生产行为差异。按用户门禁全部删除，不将其
# 伪装为测试或证据缺口；原始目标参数引用保留在单元规格/矩阵source字段中。
catalog_path=BASE/"semantic_delta_catalog.csv"
catalog=list(csv.DictReader(catalog_path.open(encoding="utf-8-sig")))
catalog_fields=list(catalog[0])
removed=[r for r in catalog if r["semantic_category"]=="SEM-PARAMETER"]
catalog=[r for r in catalog if r["semantic_category"]!="SEM-PARAMETER"]
write_csv(catalog_path,catalog,catalog_fields)

matrix_path=BASE/"semantic_completion_matrix.csv"
matrix=list(csv.DictReader(matrix_path.open(encoding="utf-8-sig")))
matrix_fields=list(matrix[0])
removed_by_unit={r["unit_id"]:r for r in removed}
for r in matrix:
    old=removed_by_unit.get(r["unit_id"])
    if not old:
        continue
    ids=[x for x in r["delta_ids"].split("|") if x and x!=old["delta_id"]]
    r["delta_ids"]="|".join(ids)
    r["missing_parameter"]="0"
    r["implemented_semantics_count"]=str(int(r["implemented_semantics_count"])+1)
    r["missing_semantics_count"]=str(int(r["missing_semantics_count"])-1)
    target=int(r["target_semantics_count"])
    r["semantic_completion_ratio"]=f"{int(r['implemented_semantics_count'])/target:.4f}"
    r["missing_semantics"]=r["missing_semantics"].replace("parameters: "+old["source_requirement"]+" || ","").replace(" || parameters: "+old["source_requirement"],"")
    r["notes"] += " R1删除机械SEM-PARAMETER：未能指出具体参数ID及当前/目标生产行为差异。"
    if r["unit_id"] in {"STATE-010","ALGO-009","ALGO-011"}:
        r["interface_impact"]="COMPATIBLE_EXTENSION"
        r["implementation_ready"]="false"
        r["blocking_reason"]="Task18B-R1: BLOCKED_BY_SPEC_DECISION；见reviews/B1-A_design_review.md"
write_csv(matrix_path,matrix,matrix_fields)

parameter_review=[]
for r in matrix:
    old=removed_by_unit[r["unit_id"]]
    parameter_review.append(dict(unit_id=r["unit_id"],unit_name=r["unit_name"],source_parameter_requirement=old["source_requirement"],specific_parameter_id_found="",concrete_current_behavior_difference="",r1_decision="DELETE_SEM_PARAMETER",reason="原行仅引用参数范围并泛称接入，未证明任一具体参数未生效、错误生效或未绑定生产入口；不构成SEM业务差异"))
write_csv(OUT/"task18b_83_parameter_recheck.csv",parameter_review,list(parameter_review[0]))

summary_path=BASE/"semantic_completion_summary.md"
summary=summary_path.read_text(encoding="utf-8")
summary=summary.replace("静态正向映射已实现=986，待闭合语义=259","R1复核后静态正向映射已实现=1069，待闭合语义=176")
summary=summary.replace("semantic delta总数=674","R1复核后semantic delta总数=591")
summary=summary.replace("| SEM-PARAMETER | 83 |\n","")
summary=summary.replace("接口影响：{'NO_INTERFACE_CHANGE': 83}","R1接口影响复核：80 NO_INTERFACE_CHANGE、3 COMPATIBLE_EXTENSION（B1-A）；0 BREAKING_CHANGE_REQUIRED")
summary=summary.replace("首批B1-A=STATE-010,ALGO-009,ALGO-011，implementation_ready=true","R1撤回首批ready结论：B1-A=STATE-010,ALGO-009,ALGO-011，BLOCKED_BY_SPEC_DECISION")
summary += "\n## Task 18B-R1补充更正\n\n原生成器机械分配的83条SEM-PARAMETER均未指出具体参数ID和生产行为差异，已全部删除；对应语义面不再计为缺失。更正后目标语义仍为1245，已实现/未证缺口为1069，缺失为176，delta总数591。逐单元复核见`reviews/task18b_83_parameter_recheck.csv`。\n"
summary_path.write_text(summary,encoding="utf-8")

(BASE/"interface_change_proposals.md").write_text("""# Task 18B接口影响（经Task 18B-R1修正）

## 结论

83个单元不再统一判为NO_INTERFACE_CHANGE。B1-A逐字段复核后：STATE-010、ALGO-009、ALGO-011均为`COMPATIBLE_EXTENSION`；其余80个暂保留`NO_INTERFACE_CHANGE`，但尚未做与B1-A同深度的逐字段复核，不得把该标签当作编码证据。当前没有批准实施的`BREAKING_CHANGE_REQUIRED`。

## B1-A边界

- 内部ParameterDefinition、owned state和FrozenConfig不跨Frozen边界，属于NO_INTERFACE_CHANGE组成项。
- 领域错误码、版本/hash、migration/default和审计字段仅可作为有默认或旧reader可忽略的可选扩展，属于COMPATIBLE_EXTENSION。
- Task16七字段SeedTrace已经Frozen，实现它不是变更；向其增加consumer/index必填字段会是BREAKING_CHANGE_REQUIRED，本设计禁止，改用独立受限审计记录。
- 若DecisionResult schema强制把完整敏感SeedTrace交给策略，需停止并提交接口提案；不得以可见性放宽解决。

输入、输出、错误码、持久化格式、调用方和兼容性逐项见`reviews/B1-A_interface_impact.csv`。
""",encoding="utf-8")

print({"semantic_deltas":len(S),"test_deltas":len(T),"evidence_deltas":len(E),"ac_rows":len(ac),"parameters":len(registry),"removed_generic_sem_parameter":len(removed),"catalog_after":len(catalog),"conclusion":"BLOCKED_BY_SPEC_DECISION"})
