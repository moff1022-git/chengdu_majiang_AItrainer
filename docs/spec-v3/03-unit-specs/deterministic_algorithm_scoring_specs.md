# ALGO-* 与 SCORE-* 确定算法和计分完整规格

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 版本 | 0.1 |
| 日期 | 2026-07-29 |
| 覆盖 | ALGO-001～ALGO-011、SCORE-001～SCORE-006 |
| 单元数 | 17 |
| 验收 | Not Evaluated |

## 统一契约

规范公式与基线公式严格分离。确定算法不得由训练模型替代。相同输入、状态、规则、公式、代码版本和命名种子必须输出唯一结果。全部计分采用不可变转移，每个原子事件、结算层和本局汇总必须满足支付方与接收方守恒，即所有座位分差之和为0。所有单元必须保留正常、边界、非法输入golden及审计证据。

番型识别的权威事实由相邻确定规则 `RULE-015` 产生，`SCORE-005` 不重新猜测牌型；它必须验证已识别番型的启用状态、互斥关系和来源证据，再按规范顺序完成番型叠加与封顶。这样保持单元目录边界，同时完整覆盖“番型识别 → 番型叠加 → 封顶 → 胡牌计分”。

## ALGO-001 face/physical tile 编码、投影与所有权守恒

### 1. 输入向量和字段含义

physical_regions: Map<region,uint8[]>；physical_id 0..107；face_index 0..26。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 ALGO-001 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

face=floor(id/4), copy=id mod 4；所有owner区域并集必须恰为{0..107}且每id计数1

### 4. 基线公式及与规范差异

基线已有PhysicalTile及迁移池检查；规范额外覆盖弃牌、副露和全部过渡区 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

区域名规范序→扫ID→owner表→face计数→重复/缺失检查。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 整数0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(108)，≤100µs

### 9. 输出范围

face_count 0..4；conserved bool；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。

### 10. 数值不变量

108实体唯一；投影总数108；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 确定算法不得调用训练模型替代。

### 11. 金标准示例（正常、边界、非法）

正常：0..107各一次通过；边界：全在wall通过；非法：id7位于hand和meld→OWNERSHIP_DUPLICATE。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：整数0误差

### 13. 错误码

`PHYSICAL_ID_RANGE,OWNERSHIP_DUPLICATE,OWNERSHIP_MISSING,FACE_COUNT_EXCEEDED`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=ALGO-001,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：region_counts,duplicate_ids,missing_ids,face_counts_hash,owner_hash。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 权威路径不调用训练模型。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(ALGO-001-CODE)；测试证据：TODO(ALGO-001-TEST)；运行证据：TODO(ALGO-001-RUN)。

## ALGO-002 手牌分解、向听、弃牌向听与等待形状

### 1. 输入向量和字段含义

counts:int8[27]各0..4；melds 0..4；dingque enum/null；hand_size符合13/14-3m。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 ALGO-002 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

普通：对全部合法分解取min s=2(n-m)-min(t,n-m)-p，n=4-open_melds；七对：s7=6-pairs+max(0,7-distinct)；和牌=-1；有效进张u满足sh(H+u)<sh(H)；等待分类两面/嵌张/边张/单钓/双碰/复合

### 4. 基线公式及与规范差异

基线DFS普通向听；七对仅6-pairs且仅听牌返回ukeire；规范补distinct项、一般有效进张和完整等待形状 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

校验→定缺负担→普通分解→七对→逐弃牌→27面进张→完成分解分类。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 整数/集合0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

缓存后O(27×S)，P95≤5ms

### 9. 输出范围

shanten -1..8；ukeire 0..27面；等待标签集合；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。

### 10. 数值不变量

取全局最小；和牌=-1；有效进张不增向听；开放手七对N/A；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 确定算法不得调用训练模型替代。

### 11. 金标准示例（正常、边界、非法）

正常：123W456W123T123B+W9为单钓0向听；边界：七对子=-1；非法：某面5张→FACE_COUNT_EXCEEDED。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：整数/集合0误差

### 13. 错误码

`HAND_SIZE_INVALID,FACE_COUNT_EXCEEDED,MELD_INVALID,DINGQUE_CONFLICT,DECOMPOSITION_FAILED`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=ALGO-002,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：counts_hash,melds,dingque,standard,seven_pairs,best_decomposition,discard_map,ukeire,wait_shapes。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 权威路径不调用训练模型。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(ALGO-002-CODE)；测试证据：TODO(ALGO-002-TEST)；运行证据：TODO(ALGO-002-RUN)。

## ALGO-003 去重可见牌与未见牌聚合

### 1. 输入向量和字段含义

PlayerView；physical_id 0..107可选；event_id uint64；face 0..26；meld_count 3..4。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 ALGO-003 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

按physical_id或稳定(source,event_id,seat,slot)去重；Vf=unique visible；Uf=4-Vf；被认领弃牌转移到meld只计一次；等待W死叫可证 iff W非空且ΣUf=0

### 4. 基线公式及与规范差异

基线按牌面Counter跳过被认领弃牌，多个同面事件可能歧义；规范要求事件/实体级去重 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

白名单校验→手牌→弃牌→claimed转移→副露→去重→V/U→死叫。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 整数0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(N+27)，N≤108

### 9. 输出范围

Vf,Uf 0..4；dead_wait bool/unknown；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。

### 10. 数值不变量

Vf+Uf=4；同实体只计一次；未见牌不等于墙内牌；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 确定算法不得调用训练模型替代。

### 11. 金标准示例（正常、边界、非法）

正常：自有W1×2+公开W1×1→V3/U1；边界：V4/U0；非法：同physical重复→VISIBLE_DUPLICATE。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：整数0误差

### 13. 错误码

`VIEW_SCHEMA_INVALID,VISIBLE_DUPLICATE,VISIBLE_COUNT_EXCEEDED,SOURCE_KEY_MISSING`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=ALGO-003,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：view_hash,source_count,dedup_hash,claimed_count,visible,unseen,dead_wait。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 权威路径不调用训练模型。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(ALGO-003-CODE)；测试证据：TODO(ALGO-003-TEST)；运行证据：TODO(ALGO-003-RUN)。

## ALGO-004 墙内活牌区间或估计

### 1. 输入向量和字段含义

unseen Uf 0..4×27；wall W 0..108；opponent_hidden H 0..52。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 ALGO-004 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

U=ΣUf,H=U-W；Lf=max(0,Uf-H),Rf=min(Uf,W),Ef=0若U=0否则W×Uf/U

### 4. 基线公式及与规范差异

当前无独立完整实现；模型估计不得替代组合上下界 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

校验U≥W→H→L/R→Decimal E→残差校正→不变量。任一步失败不提交部分输出或分数。

### 6. 舍入规则

Decimal内部精度≥28，最终ROUND_HALF_EVEN至小数点后8位；残差按稳定索引分配。 E半偶8位，绝对/总和≤1e-8；界0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(27)，≤100µs

### 9. 输出范围

0≤L≤E≤R≤4；ΣE=W；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。

### 10. 数值不变量

ΣL≤W≤ΣR；W=0全0；未见不宣称在墙；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 确定算法不得调用训练模型替代。

### 11. 金标准示例（正常、边界、非法）

正常：U=[2,2],W2→E=[1,1]；边界W0全0；非法U3/W4→WALL_UNSEEN_CONFLICT。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：E半偶8位，绝对/总和≤1e-8；界0误差

### 13. 错误码

`UNSEEN_RANGE,WALL_RANGE,WALL_UNSEEN_CONFLICT,NUMERIC_INVARIANT`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=ALGO-004,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：unseen_hash,W,H,lower,upper,estimate,rounding,residual。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 权威路径不调用训练模型。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(ALGO-004-CODE)；测试证据：TODO(ALGO-004-TEST)；运行证据：TODO(ALGO-004-RUN)。

## ALGO-005 逐座剩余摸牌机会估计

### 1. 输入向量和字段含义

active_order 2..4唯一seat；actor；phase；wall W；known_extra_draws；unknown_gang_budget。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 ALGO-005 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

从下一实际draw起按RULE-005环序将W张逐张分配；Ds=计数；已承诺补摸先占用；未知未来杠只输出区间

### 4. 基线公式及与规范差异

ceil(W/A)只是粗基线，不能处理当前phase、碰、杠、胡后退出 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

校验→确定next draw→承诺补摸→模拟基线→未知杠上下界。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 整数0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(W+A)且W≤108，目标≤100µs

### 9. 输出范围

每座draw interval 0..W；确定分配和=W；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。

### 10. 数值不变量

非活动座0；每墙牌最多分配一次；活动集变化重算；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 确定算法不得调用训练模型替代。

### 11. 金标准示例（正常、边界、非法）

正常order0123,next1,W5→[1,2,1,1]；边界W0全0；非法actor不活动→ACTOR_NOT_ACTIVE。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：整数0误差

### 13. 错误码

`ACTIVE_ORDER_INVALID,ACTOR_NOT_ACTIVE,PHASE_INVALID,WALL_RANGE,EXTRA_DRAW_CONFLICT`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=ALGO-005,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：active_order,next_draw,W,extra_draws,assumption_version,intervals。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 权威路径不调用训练模型。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(ALGO-005-CODE)；测试证据：TODO(ALGO-005-TEST)；运行证据：TODO(ALGO-005-RUN)。

## ALGO-006 mandatory 分类、候选上限与稳定排序

### 1. 输入向量和字段含义

legal_actions 1..N；context；force_flags；max_candidates 1..14；stable_action_key。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 ALGO-006 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

M={mandatory}; O=sort(L-M,key); C=sort(M,key)+first_cap(O)；强制项不受cap；唯一动作强制

### 4. 基线公式及与规范差异

基线同样保留mandatory；规范明确cap只约束普通项并要求分类理由 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

验证/去重→分类→稳定排序→裁普通项→非空。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 集合/顺序0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(NlogN)，N为固定动作空间

### 9. 输出范围

1≤|C|≤|M|+cap且C⊆L；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。

### 10. 数值不变量

mandatory不丢；输入顺序无关；不调用训练模型；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 确定算法不得调用训练模型替代。

### 11. 金标准示例（正常、边界、非法）

正常HU强制+两弃牌,cap1→HU+键最小弃牌；边界两强制均保留；非法cap0。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：集合/顺序0误差

### 13. 错误码

`LEGAL_SET_EMPTY,ACTION_DUPLICATE,ACTION_SCHEMA_INVALID,CANDIDATE_CAP_RANGE`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=ALGO-006,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：legal_hash,mandatory,ordinary_sorted,cap,trimmed,classification_version。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 权威路径不调用训练模型。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(ALGO-006-CODE)；测试证据：TODO(ALGO-006-TEST)；运行证据：TODO(ALGO-006-RUN)。

## ALGO-007 六分量候选 Q 评价

### 1. 输入向量和字段含义

x=(S,L,F,R,P,M) Decimal各0..1；权重w各0..1且Σw=1；action_key。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 ALGO-007 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

Q=wS*S+wL*L+wF*F-wR*R+wP*P+wM*M；排序(-Q,action_key)；本单元不含噪声

### 4. 基线公式及与规范差异

基线为speed/hand_value/defense/flexibility四项+动作调整；不是六分量规范；模型不得替代分量/Q 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

校验→固定S,L,F,R,P,M顺序乘→风险取负→求和→量化→tie-break。任一步失败不提交部分输出或分数。

### 6. 舍入规则

Decimal内部精度≥28，最终ROUND_HALF_EVEN至小数点后8位；残差按稳定索引分配。 ROUND_HALF_EVEN到1e-8，规范字面值0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(NlogN)，N≤14，≤1ms

### 9. 输出范围

Q -1..1；分量0..1；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。

### 10. 数值不变量

风险仅负号；顺序固定；Decimal确定；不调用训练模型；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 确定算法不得调用训练模型替代。

### 11. 金标准示例（正常、边界、非法）

正常仅S权重1且S=.75→Q=.75；边界仅R=1→-1；非法S=1.1。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：ROUND_HALF_EVEN到1e-8，规范字面值0误差

### 13. 错误码

`FEATURE_RANGE,WEIGHT_RANGE,WEIGHT_SUM,NON_FINITE,FEATURE_NULL`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=ALGO-007,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：features,weights,products,q_raw,q8,rounding,formula_version,action_key。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 权威路径不调用训练模型。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(ALGO-007-CODE)；测试证据：TODO(ALGO-007-TEST)；运行证据：TODO(ALGO-007-RUN)。

## ALGO-008 seed、噪声、思考时间与随机流确定派生

### 1. 输入向量和字段含义

stream_key uint64；seat0..3；decision/sample_index uint64；purpose枚举；distribution params。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 ALGO-008 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

subseed=U64(BLAKE2b(canonical(game,version,seat,decision,purpose),8))；样本=versioned_PRNG(subseed,index)

### 4. 基线公式及与规范差异

基线少数流用XOR；规范采用purpose/version哈希域隔离；旧流必须按旧版本回放 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

canonical→purpose→hash→PRNG→index样本→分布变换→量化。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 整数0；浮点半偶8位且0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

派生O(bytes)，样本O(1)

### 9. 输出范围

seed 0..2^64-1；U01 [0,1)；时间在配置区间；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。

### 10. 数值不变量

跨进程一致；新增purpose不改旧流；墙钟不参与决策；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 确定算法不得调用训练模型替代。

### 11. 金标准示例（正常、边界、非法）

正常同tuple百次一致；边界seed0/index0；非法unknown purpose。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：整数0；浮点半偶8位且0误差

### 13. 错误码

`RNG_INPUT_INVALID,RNG_PURPOSE_UNKNOWN,RNG_VERSION_UNKNOWN,SAMPLE_INDEX_RANGE`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=ALGO-008,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：canonical_hash,purpose,subseed_hash,prng_version,index,distribution,sample_hash。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 权威路径不调用训练模型。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(ALGO-008-CODE)；测试证据：TODO(ALGO-008-TEST)；运行证据：TODO(ALGO-008-RUN)。

## ALGO-009 配置类型/范围/版本校验、迁移与 canonical hash

### 1. 输入向量和字段含义

raw JSON；schema uint16；GP/RP registry范围；migration path。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 ALGO-009 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

逐版本纯迁移→registry类型/范围/交叉约束；canonical UTF-8 JSON键序、固定数字、无NaN/Inf；hash=SHA256(bytes)

### 4. 基线公式及与规范差异

基线已有sort_keys紧凑JSON/SHA256；规范补数字canonical及逐步迁移hash 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

解析→版本→逐迁移→默认→类型/范围→交叉约束→拒未知→canonical/hash→冻结。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 canonical/hash 0误差；Decimal按字段scale半偶

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(B+P)，1MB≤50ms

### 9. 输出范围

hash为64小写hex；参数均在闭区间；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。

### 10. 数值不变量

语义等价配置hash相同；迁移幂等；模型不能放宽参数；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 确定算法不得调用训练模型替代。

### 11. 金标准示例（正常、边界、非法）

正常键序不同hash同；边界=max通过；非法NaN/未知GP。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：canonical/hash 0误差；Decimal按字段scale半偶

### 13. 错误码

`CONFIG_PARSE,SCHEMA_VERSION_UNSUPPORTED,PARAM_UNKNOWN,PARAM_TYPE,PARAM_RANGE,PARAM_NULL,CROSS_CONSTRAINT,MIGRATION_FAILED`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=ALGO-009,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：source_hash,schema_before_after,migration_steps,defaults,errors,canonical_hash。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 权威路径不调用训练模型。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(ALGO-009-CODE)；测试证据：TODO(ALGO-009-TEST)；运行证据：TODO(ALGO-009-RUN)。

## ALGO-010 PlayerView 白名单构建

### 1. 输入向量和字段含义

authoritative state；viewer 0..N-1；phase；policy/state version。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 ALGO-010 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

View=project(State,Whitelist[phase,viewer])；未列字段默认删除；本人暗手与公共信息按白名单深复制

### 4. 基线公式及与规范差异

已有PlayerView v2候选；历史E3/report-only不等于本卡验收 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

验证→白名单→逐字段投影→self/other→递归泄漏扫描→canonical→深冻结。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 字段/字节0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(public+self_private)，≤1ms

### 9. 输出范围

字段严格为白名单子集；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。

### 10. 数值不变量

零对手暗手/墙序/oracle；无可变引用；模型/训练不扩权；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 确定算法不得调用训练模型替代。

### 11. 金标准示例（正常、边界、非法）

正常S0见自己手而S1仅张数；边界finished仍不自动公开墙序；非法viewer4。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：字段/字节0误差

### 13. 错误码

`VIEWER_RANGE,PHASE_INVALID,POLICY_VERSION_UNKNOWN,WHITELIST_VIOLATION,LEAK_DETECTED`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=ALGO-010,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：state_hash,version,viewer,phase,policy,included_paths_hash,redacted_count,view_hash。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 权威路径不调用训练模型。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(ALGO-010-CODE)；测试证据：TODO(ALGO-010-TEST)；运行证据：TODO(ALGO-010-RUN)。

## ALGO-011 game_id 到牌墙、骰子及子随机流的确定映射

### 1. 输入向量和字段含义

game_id UTF-8 1..256字节；版本uint16；注册stream_name；index uint64。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 ALGO-011 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

master=U64(BLAKE2b(domain||len(id)||id||versions,8)); seed(name)=U64(BLAKE2b(master||len(name)||name||rng_version,8))

### 4. 基线公式及与规范差异

基线master=BLAKE2b(id)且dice/exchange固定XOR；规范为版本化域隔离，旧版保留回放 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

规范化ID→编码版本/domain→master→逐注册流seed→冻结映射。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 uint64/字节0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(bytes(id)+Σnames)

### 9. 输出范围

seed 0..2^64-1；流名唯一；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。

### 10. 数值不变量

同ID/版本同流；新增流不改旧流；禁用内置hash；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 确定算法不得调用训练模型替代。

### 11. 金标准示例（正常、边界、非法）

正常同ID映射同；边界1字节ID；非法空ID。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：uint64/字节0误差

### 13. 错误码

`GAME_ID_TYPE,GAME_ID_EMPTY,GAME_ID_TOO_LONG,RNG_VERSION_UNKNOWN,STREAM_UNKNOWN`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=ALGO-011,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：game_id_hash,versions,algorithm,master_hash,stream_names,seed_hashes。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 权威路径不调用训练模型。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(ALGO-011-CODE)；测试证据：TODO(ALGO-011-TEST)；运行证据：TODO(ALGO-011-RUN)。

## SCORE-001 分数账本分层与守恒

### 1. 输入向量和字段含义

events；transfer(from,to,amount int64>0)；balances_before int64[N]；layer枚举。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 SCORE-001 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

每t: Δfrom-=amount,Δto+=amount；每事件ΣΔ=0；after=before+ΣΔ；hash-chain不可变

### 4. 基线公式及与规范差异

基线逐条减加并记after；规范新增提交前零和、自转移、重复与溢出硬门禁 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

schema→seat/amount→禁自转→聚合Δ→零和/溢出→版本→原子after→hash。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 整数0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(T+N)，≤100µs

### 9. 输出范围

amount正int64；sum_delta=0；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。 transfers/delta_by_seat为int64且sum_delta=0。

### 10. 数值不变量

每事件支付接收守恒；ledger净额=余额差；event只一次；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 每个原子计分、结算层和汇总均须验证支付方—接收方守恒。

### 11. 金标准示例（正常、边界、非法）

正常S1→S0 4=[+4,-4]；边界允许负余额；非法仅S0+4无payer。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：整数0误差

### 13. 错误码

`TRANSFER_SCHEMA,SEAT_RANGE,SELF_TRANSFER,AMOUNT_RANGE,SCORE_OVERFLOW,SCORE_NOT_ZERO_SUM,DUPLICATE_SCORE_EVENT`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=SCORE-001,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：event_id,layer,reason,transfers,delta,sum,before,after,prev_hash,event_hash。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 每个支付方—接收方事件、结算层及本局汇总ΣΔ=0。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(SCORE-001-CODE)；测试证据：TODO(SCORE-001-TEST)；运行证据：TODO(SCORE-001-RUN)。

## SCORE-002 自摸、点炮与抢杠胡计分

### 1. 输入向量和字段含义

win_type；winners1..3；payer(s)；fan0..64；base1..1e6；active_set。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 SCORE-002 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

P=base×2^fan_effective；自摸由规则指定活动非赢家各付P；点炮/抢杠责任座向每赢家分别付P；多响为独立转移

### 4. 基线公式及与规范差异

基线同P公式、自摸active支付、点炮多赢家；未独立标抢杠reason，封顶顺序待SCORE-005 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

胡事实→fan/cap→P/溢出→payer集合→规范转移→逐赢家及总守恒。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 整数0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(winners×payers)，≤9转移

### 9. 输出范围

P正int64；事件ΣΔ=0；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。 transfers/delta_by_seat为int64且sum_delta=0。

### 10. 数值不变量

赢家非自身payer；非法胡零分；reward不入账本；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 每个原子计分、结算层和汇总均须验证支付方—接收方守恒。

### 11. 金标准示例（正常、边界、非法）

正常base1 fan2点炮→±4；边界fan0自摸三家各付1；非法winner=loser。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：整数0误差

### 13. 错误码

`WIN_TYPE_INVALID,WINNER_INVALID,PAYER_INVALID,HU_SELF_PAYMENT,FAN_MISSING,FAN_RANGE,POINT_OVERFLOW,SCORE_NOT_ZERO_SUM`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=SCORE-002,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：win_event,type,winners,payer_policy,fan_raw_effective,base,points,transfers,sum。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 每个支付方—接收方事件、结算层及本局汇总ΣΔ=0。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(SCORE-002-CODE)；测试证据：TODO(SCORE-002-TEST)；运行证据：TODO(SCORE-002-RUN)。

## SCORE-003 明/暗/补杠与呼叫转移计分

### 1. 输入向量和字段含义

kind明/暗/补；gang/source seat；active_set；base/multipliers；related_hu_event。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 SCORE-003 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

明杠来源付base×m_ming；暗/补杠规则支付集逐座付base×m；呼叫转移按关联原杠金额反向/重定向；抢杠成功不产补杠分

### 4. 基线公式及与规范差异

基线明2base单付、暗2base多付、补1base多付；未实现呼叫转移；未知kind不得静默空 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

确认杠成立→kind/payers→基础分→抢杠取消→转移关联→规范转移→逐子事件守恒。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 整数0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(N)，N≤4

### 9. 输出范围

每笔正int64；各子事件ΣΔ=0；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。 transfers/delta_by_seat为int64且sum_delta=0。

### 10. 数值不变量

未成立杠零分；抢杠取消；关联唯一；支付接收守恒；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 每个原子计分、结算层和汇总均须验证支付方—接收方守恒。

### 11. 金标准示例（正常、边界、非法）

正常暗杠S0获三家各2；边界仅一对手付2；非法明杠缺source。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：整数0误差

### 13. 错误码

`GANG_KIND_INVALID,GANG_NOT_COMMITTED,GANG_SOURCE_MISSING,QIANG_GANG_CANCELLED,TRANSFER_LINK_INVALID,TRANSFER_DUPLICATE`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=SCORE-003,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：gang_event,kind,seats,payer_policy,base,multiplier,related_hu,mode,transfers,sum。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 每个支付方—接收方事件、结算层及本局汇总ΣΔ=0。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(SCORE-003-CODE)；测试证据：TODO(SCORE-003-TEST)；运行证据：TODO(SCORE-003-RUN)。

## SCORE-004 花猪、查大叫与退税终局调整

### 1. 输入向量和字段含义

end_state；花猪/听口/max_fan集合；gang_ledger；rules；base。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 SCORE-004 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

花猪P_h=base×2^hua_fan逐合格对支付；查大叫无叫向有叫支付base×2^min(max_wait_fan,cap)；退税按原杠账本逐笔反向；各层ΣΔ=0

### 4. 基线公式及与规范差异

基线花猪同式；查叫仅base×mult简化且不搜最大番；未实现退税。三者分开审计 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

终局冻结→花猪→资格→ALGO-002听口/RULE-015番→最大番→花猪→查叫→原杠退税→层守恒。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 整数0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(players×27×analysis+gang events)，≤100ms

### 9. 输出范围

每笔正int64；每层/总ΣΔ=0；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。 transfers/delta_by_seat为int64且sum_delta=0。

### 10. 数值不变量

顺序固定；死叫不冒充有叫；退税可追溯且不超原收益；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 每个原子计分、结算层和汇总均须验证支付方—接收方守恒。

### 11. 金标准示例（正常、边界、非法）

正常base1花猪fan3向三家各付8；边界无人听则查叫no-op；非法ting缺maxfan。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：整数0误差

### 13. 错误码

`END_STATE_INVALID,HUA_ZHU_CLASSIFICATION,CHA_JIAO_FAN_MISSING,DEAD_WAIT_POLICY_UNKNOWN,TAX_SOURCE_MISSING,TAX_EXCEEDS_SOURCE`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=SCORE-004,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：version,hua_zhu_ting_dead_sets,wait_fans,maxfan,layer_order,source_gangs,adjustments,sum_by_layer。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 每个支付方—接收方事件、结算层及本局汇总ΣΔ=0。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(SCORE-004-CODE)；测试证据：TODO(SCORE-004-TEST)；运行证据：TODO(SCORE-004-RUN)。

## SCORE-005 封顶、互斥和转移结算顺序

### 1. 输入向量和字段含义

raw fan/components/transfers；cap0..64；互斥策略；settlement_order；links。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 SCORE-005 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

输入番型必须来自 `RULE-015` 的确定性识别结果；先验证每个番型ID、启用状态与证据，再按互斥表删除被替代项。`fan_raw=Σ retained_fan_component`；`fan_eff=fan_raw` 若 `cap=0`，否则 `min(fan_raw,cap)`；胡分使用 `fan_eff`。杠分不重复受胡番cap；最终按版本化结算层序汇总Δ。

### 4. 基线公式及与规范差异

基线apply_fan_cap已做cap≤0不限；即时入账，未统一全层、转移和退税编排 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

互斥→叠加→cap→胡→杠→花猪→查叫→退税/转移（具体层序按批准版本）→各层/总守恒。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 整数0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(F+TlogT)，≤10ms不含分析

### 9. 输出范围

0≤eff≤raw≤64；final int64；ΣΔ=0；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。 transfers/delta_by_seat为int64且sum_delta=0。

### 10. 数值不变量

cap一次且位置固定；互斥不共存；相反转移保留审计明细；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 每个原子计分、结算层和汇总均须验证支付方—接收方守恒。

### 11. 金标准示例（正常、边界、非法）

正常raw5 cap3→eff3/P8；边界cap0→5；非法互斥项并存。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：整数0误差

### 13. 错误码

`FAN_RANGE,FAN_CAP_RANGE,FAN_EXCLUSION_CONFLICT,SETTLEMENT_ORDER_UNKNOWN,TRANSFER_LINK_INVALID,SCORE_NOT_ZERO_SUM`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=SCORE-005,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：components_before_after,raw,eff,cap,layers,raw_final_hash,sum_each_total,policy_versions。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 每个支付方—接收方事件、结算层及本局汇总ΣΔ=0。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(SCORE-005-CODE)；测试证据：TODO(SCORE-005-TEST)；运行证据：TODO(SCORE-005-RUN)。

## SCORE-006 单局总分、整场累计与排名

### 1. 输入向量和字段含义

round_ledger；starting/prior scores int64[N]；round_index；tie/early_end policy。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../02-unit-catalog/locked_unit_catalog.md) 的 SCORE-006 行。

### 2. 数据类型、最小值和最大值

必须使用上述固定宽度整数、Decimal、稳定枚举和canonical集合；未另注的计数最小0，最大受108实体牌、27牌面、4玩家和int64约束。禁止NaN、±Inf、隐式截断和int64溢出。

### 3. 规范公式

round_delta=ΣledgerΔ；round_end=start+delta；match=prior+delta（版本须防双加）；rank按(-match_score,tiebreak_key)

### 4. 基线公式及与规范差异

基线session有累计与UI；需审计起分重复累计、并列及提前终止；UI ledger非权威证据 规范公式是目标契约；基线只用于兼容和差距审计，必须分别记录formula_version与baseline_version。

### 5. 计算顺序

验证事件/hash→round delta→余额对账→合prior→总分/溢出→early end→稳定排名→冻结。任一步失败不提交部分输出或分数。

### 6. 舍入规则

纯整数/集合步骤不舍入。 整数/排名0误差

### 7. 边界处理与空值处理

边界必须显式覆盖零、最小、最大、空集合和终止状态。仅明确可选字段允许null；缺省与null不同；其他null返回SCHEMA_INVALID，不得静默转0/空集合/默认房规。

### 8. 复杂度目标

O(E+NlogN)，≤5ms

### 9. 输出范围

score int64；rank1..N；Σround_delta=0；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。 transfers/delta_by_seat为int64且sum_delta=0。

### 10. 数值不变量

账本净额=余额差；累计只加一次；总分守恒；相同输入唯一排名；相同输入、状态、规则/公式/代码版本和命名种子必须产生唯一结果。 每个原子计分、结算层和汇总均须验证支付方—接收方守恒。

### 11. 金标准示例（正常、边界、非法）

正常prior00+delta[4,-4]→rank S0>S1；边界全0并列；非法delta和1。三类示例均须固定canonical输入、全部中间量、输出或错误码及hash。

### 12. 测试向量与允许误差

至少覆盖：正常向量、最小/最大边界、非法类型/范围/null、输入顺序置换、100次复算、跨进程；领域向量按本节golden扩展。允许误差：整数/排名0误差

### 13. 错误码

`LEDGER_INVALID,ROUND_ALREADY_COUNTED,BALANCE_MISMATCH,MATCH_SCORE_NOT_CONSERVED,RANK_POLICY_UNKNOWN,SCORE_OVERFLOW`；通用：SCHEMA_INVALID、VERSION_CONFLICT、NON_FINITE、NUMERIC_INVARIANT、DETERMINISM_VIOLATION。

### 14. 审计字段

通用：timestamp_utc,game_id,round_id,event_id,unit_id=SCORE-006,state_version,ruleset_hash,config_hash,formula_version,baseline_version,input_hash,output_hash,accepted,error_code,latency_us。领域：match_round_id,ledger_hash,start,prior,delta,end,match,sum,rank_policy,rank,early_end,result_hash。隐藏牌只记录受控引用/hash。

### 15. 验收与证据占位

- [ ] 规范公式golden、边界与非法向量全部通过。
- [ ] 基线差异可观测，未用基线近似证明规范完成。
- [ ] 复算、顺序置换和跨进程逐字段一致。
- [ ] 每个支付方—接收方事件、结算层及本局汇总ΣΔ=0。
- [ ] E3单元/契约证据；P0集成E4；当前Not Evaluated。

代码证据：TODO(SCORE-006-CODE)；测试证据：TODO(SCORE-006-TEST)；运行证据：TODO(SCORE-006-RUN)。
# 3.0.1 SCORE-001事件与幂等契约

## 3.0.2 ALGO-001 region枚举

规范region为`wall,hand:S0..S3,discard:S0..S3,meld:S0..S3,exchange_pool:S0..S3,pending_discard,pending_gang,removed`；phase未使用的region仍必须以空集出现，以保持schema/hash稳定。未知region返回`REGION_UNKNOWN`，缺少必需region返回`REGION_MISSING`。所有region中physical ID并集必须恰为0..107且每ID一次。`removed`只用于规则明确移出但仍需守恒跟踪的实体，不得作为丢失牌的默认容器。

`layer∈{atomic,round_settlement,match_total}`。输入event必须含非空`event_id`、layer、reason、transfers；transfer为`{from_seat:uint8,to_seat:uint8,amount:int64}`且amount>0。幂等边界是同一权威ledger：首次event_id原子提交；同ID且canonical payload相同返回原结果且不重复写；同ID不同payload返回`DUPLICATE_SCORE_EVENT`。event hash为SHA-256(canonical JSON UTF-8 of `{event_id,layer,reason,transfers,delta,before,after,prev_hash}`)，不得使用浮点。golden：before `[0,0,0,0]`、S1→S0 4，after `[4,-4,0,0]`、delta同值、sum=0。
