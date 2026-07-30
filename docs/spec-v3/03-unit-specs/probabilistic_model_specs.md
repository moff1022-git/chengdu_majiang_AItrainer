# MODEL-* 模型接口与基线模型完整规格

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 版本 | 0.1 |
| 日期 | 2026-07-29 |
| 覆盖 | MODEL-001～MODEL-005 |
| 单元数 | 5 |
| 验收 | Not Evaluated |

## 全局隔离与概率契约

线上模型只能读取PlayerView、公开历史和获准的本座认知/参数。对手隐藏手牌、精确牌墙、oracle和未来信息严禁作为推理输入。训练标签可由终局公开信息或离线模拟真值生成，但必须位于独立restricted label zone，不能进入特征构建、归一、校准或线上schema。

每个概率输出必须同时报告proper scoring rule和校准误差，不得只报告准确率。所有模型均配确定性规则基线；加载失败、超时、版本不兼容、概率非法或OOD策略触发时自动回退。

重点能力映射：MODEL-001覆盖对手清缺概率、主体花色和牌型；MODEL-002覆盖听牌概率、某牌为等待牌概率和综合点炮风险；MODEL-003覆盖对手风格学习；MODEL-004覆盖真人行为拟合与候选动作概率分布；MODEL-005覆盖训练、冻结、校准、评估和发布生命周期。

## MODEL-001 逐对手归一化方向/牌型假设

### 1. 预测目标

分别预测每个活动对手的清缺进度、主体花色和牌型假设概率。

### 2. 预测单位

单个决策事件 × 单个对手；同一时点三个对手分别推理，不合并。

### 3. 输入特征

PlayerView中的对手定缺、按时间排序的弃牌、公开碰/杠、副露花色、各花色公开计数、阶段、墙余量、响应记录，以及只由公开事件形成的有界记忆。

### 4. 禁止输入

对手当前/历史隐藏手牌、墙序、未来事件、oracle_hands、终局truth字段、其他座私有认知、标签派生特征。。线上入口必须执行字段白名单与递归泄漏扫描；发现即拒绝，不允许仅忽略。

### 5. 标签定义

离线可用终局公开手牌或模拟器truth生成：cleared_dingque∈{0,1}；dominant_suit∈{wan,tong,tiao,mixed}；shape∈{standard,seven_pairs,all_pongs,pure_suit,other}。标签区与policy_features物理分栏。 标签可以使用终局公开或离线真值，但必须位于restricted label zone，与策略输入schema、文件和加载权限隔离。

### 6. 输出格式

per_seat对象：p_cleared；dominant_suit_probs[4]；shape_probs[5]；evidence_count；uncertainty；model/fallback版本。

### 7. 输出范围

每概率[0,1]；各互斥分布和为1，绝对误差≤1e-9；熵[0,lnK]；无证据不得输出1。 所有概率必须有限；互斥分布归一误差≤1e-9。

### 8. 规则基线与基线公式

规则基线：定缺公开后，随公开缺门弃牌减少单调提高p_cleared；主体花色按公开副露+保留倾向做Laplace(α=1)计数；牌型按启用规则先验乘公开事件似然表后归一。 模型不可用、超时、版本不兼容或输出无效时必须回退此基线。

### 9. 损失函数

多任务加权：binary log loss(cleared)+categorical cross-entropy(suit)+categorical cross-entropy(shape)+0.1×Brier；权重默认1/1/1，可调[0.25,4]。

### 10. 训练数据格式

Parquet/JSONL每行含decision_id,game_id,match_id,player_id_hash,seat,policy_features,label_zone,visibility_manifest,ruleset_hash；label_zone不得被训练特征加载器读取。 每条记录必须带source_release、feature_schema、label_schema、ruleset、split和canonical hash。

### 11. 数据切分方式

按player_id_hash优先、其次match_id/game_id分组切分70/15/15；同玩家不可跨train/test；时间外推测试另保留。

### 12. 防止牌局泄漏规则

同一player、match、game、近重复局和seed家族不得跨切分；拟合器、归一器、词表、校准器只可用train/val。隐藏手牌/墙序只能在restricted_truth生成标签，永不进入online features。自动扫描后泄漏率必须为0。

### 13. 校准方法

验证集temperature/vector scaling；分任务、阶段、对手座报告ECE(15等频桶)、MCE、Brier及可靠性图。 概率模型必须报告校准误差，准确率/AUC不能替代ECE、Brier和可靠性图。

### 14. 评估指标

macro log loss、Brier、ECE、macro-AUC/F1、top-2 recall、概率和误差；不只报准确率。 所有指标按阶段、对手座、规则版本、数据来源和证据量分层，并报告95% CI。

### 15. 最低验收阈值

相对Laplace规则基线：三个任务中至少2个Brier改善≥5%，其余不劣>1%；ECE≤0.05；top-2 recall≥0.90；泄漏0。 阈值未达标时保持Not Evaluated/Failed，不得用其他指标平均抵消。

### 16. 不确定性表达

输出预测熵、最大概率、evidence_count；证据不足时与先验混合且设置low_evidence=true。

### 17. 模型版本

model_version、artifact_sha256、feature/label schema、ruleset、codec、data_release、training_code_commit、config_hash、seed、calibrator_version必须齐全；未知或不兼容版本拒绝。

### 18. 回退模型

上述公开事件Laplace/似然表基线；若连公开字段也缺失，输出按规则版本冻结的先验。

### 19. 在线推理时限

单对手P95≤2ms、三对手合计P99≤10ms，CPU单线程；超时走回退。 计时含特征编码、模型、校准和输出校验；超时结果不得迟到覆盖回退。

### 20. 可解释字段

每任务top公开证据、先验/后验、似然贡献、校准前后概率、缺失mask、禁止字段扫描结果。 通用另含request_id、seat、phase、input/output hash、latency、fallback_reason和禁止字段扫描摘要。

### 21. 测试与证据占位

必须测试正常/边界/非法schema、隐藏字段投毒、分布归一、校准、切分泄漏、超时回退、版本拒绝和同artifact冻结推理复现。MODEL-004还须测试legal mask全路径；MODEL-005须验证训练/评估隔离。

代码证据：TODO(MODEL-001-CODE)；测试证据：TODO(MODEL-001-TEST)；数据证据：TODO(MODEL-001-DATA)；校准证据：TODO(MODEL-001-CALIBRATION)；运行证据：TODO(MODEL-001-RUN)。

## MODEL-002 逐对手听牌、等待与综合点炮风险模型

### 1. 预测目标

预测每个对手听牌概率、每个可弃牌面成为其等待牌的条件概率、条件损失及综合点炮风险。

### 2. 预测单位

单个决策事件 × 对手 × 候选弃牌面；听牌概率按对手级，等待/风险按牌面级。

### 3. 输入特征

MODEL-001后验、公开弃牌/副露/响应、ALGO-003可见与未见计数、ALGO-004墙内区间、阶段、对手状态、候选牌公开安全证据。

### 4. 禁止输入

对手隐藏手牌、精确墙序、实际等待牌、未来胡牌结果、oracle损失、标签列或由其直接计算的特征。。线上入口必须执行字段白名单与递归泄漏扫描；发现即拒绝，不允许仅忽略。

### 5. 标签定义

离线truth：tenpai_now；wait_face[f]（当前听牌且f可和）；loss_if_hit[f]（冻结计分规则下离线计算）；deal_in[f]。终局公开仅在确能重建决策时点时可作标签。 标签可以使用终局公开或离线真值，但必须位于restricted label zone，与策略输入schema、文件和加载权限隔离。

### 6. 输出格式

per_seat: p_tenpai；per_face: p_wait_given_tenpai、expected_loss、deal_in_risk；risk_total；区间/熵；版本。

### 7. 输出范围

概率[0,1]；expected_loss[0,score_cap]；risk=p_tenpai×p_wait_given_tenpai×normalized_expected_loss∈[0,1]。 所有概率必须有限；互斥分布归一误差≤1e-9。

### 8. 规则基线与基线公式

规则基线：p_tenpai由阶段/副露数/弃牌数分桶先验；p_wait按未见张数×公开舍牌安全表归一；loss按启用番型先验；综合风险使用上述乘积，不把未见牌当墙内事实。 模型不可用、超时、版本不兼容或输出无效时必须回退此基线。

### 9. 损失函数

tenpai BCE+Brier；wait按多标签BCE或proper log loss；loss用Huber；risk用Brier+排序pairwise loss。默认权重1/1/0.5/1。

### 10. 训练数据格式

决策级Parquet，policy_features与restricted_truth分离；每行含27面mask、规则/计分版本、样本权重和label_availability。 每条记录必须带source_release、feature_schema、label_schema、ruleset、split和canonical hash。

### 11. 数据切分方式

按player→match→game分组；同一局所有牌面行必须同split；正式真人test永不训练/调参。

### 12. 防止牌局泄漏规则

同一player、match、game、近重复局和seed家族不得跨切分；拟合器、归一器、词表、校准器只可用train/val。隐藏手牌/墙序只能在restricted_truth生成标签，永不进入online features。自动扫描后泄漏率必须为0。

### 13. 校准方法

tenpai与risk用isotonic或temperature；wait分阶段/对手分层校准；报告ECE、adaptive ECE、Brier和calibration slope/intercept。 概率模型必须报告校准误差，准确率/AUC不能替代ECE、Brier和可靠性图。

### 14. 评估指标

tenpai/wait/risk Brier、log loss、ECE；危险排序AUC/NDCG；loss MAE；高风险召回；规则反例。 所有指标按阶段、对手座、规则版本、数据来源和证据量分层，并报告95% CI。

### 15. 最低验收阈值

综合危险排序AUC≥0.75；risk ECE≤0.05；tenpai与wait Brier相对规则基线改善≥5%；loss MAE优于常数基线；泄漏0。 阈值未达标时保持Not Evaluated/Failed，不得用其他指标平均抵消。

### 16. 不确定性表达

输出bootstrap/ensemble区间或conformal风险区间、熵、evidence_count、OOD标记；区间覆盖目标90%±3pp。

### 17. 模型版本

model_version、artifact_sha256、feature/label schema、ruleset、codec、data_release、training_code_commit、config_hash、seed、calibrator_version必须齐全；未知或不兼容版本拒绝。

### 18. 回退模型

阶段×副露规则先验+公开安全表+固定损失表；字段缺失时降级为更宽先验并标fallback_level。

### 19. 在线推理时限

三对手×27面合计P95≤12ms、P99≤25ms；超时回退且不阻塞合法动作。 计时含特征编码、模型、校准和输出校验；超时结果不得迟到覆盖回退。

### 20. 可解释字段

逐对手p_tenpai依据、逐牌top风险贡献、公开安全/危险证据、未见/墙内区间、校准前后值、risk乘积分解。 通用另含request_id、seat、phase、input/output hash、latency、fallback_reason和禁止字段扫描摘要。

### 21. 测试与证据占位

必须测试正常/边界/非法schema、隐藏字段投毒、分布归一、校准、切分泄漏、超时回退、版本拒绝和同artifact冻结推理复现。MODEL-004还须测试legal mask全路径；MODEL-005须验证训练/评估隔离。

代码证据：TODO(MODEL-002-CODE)；测试证据：TODO(MODEL-002-TEST)；数据证据：TODO(MODEL-002-DATA)；校准证据：TODO(MODEL-002-CALIBRATION)；运行证据：TODO(MODEL-002-RUN)。

## MODEL-003 仅公开信息的跨局对手风格学习

### 1. 预测目标

学习对手公开可观察风格以及下一局动作类别分布改善；不重建隐藏手牌。

### 2. 预测单位

对手 × 已完成局/整场；输出下一局profile。

### 3. 输入特征

历史公开弃碰杠胡过类别、响应频率、公开副露、决策时机桶、分数/阶段上下文、规则版本；历史长度有上限。

### 4. 禁止输入

任何局的隐藏手牌/墙序、训练标签回填到历史特征、跨玩家身份明文、正式测试集统计、未来局事件。。线上入口必须执行字段白名单与递归泄漏扫描；发现即拒绝，不允许仅忽略。

### 5. 标签定义

下一局公开动作类别分布与可观测风格维度（aggression,defense,peng,gang,pass_hu,speed）；真人标签只来自合规公开牌谱并保留来源许可。 标签可以使用终局公开或离线真值，但必须位于restricted label zone，与策略输入schema、文件和加载权限隔离。

### 6. 输出格式

profile维度均值[0,1]、方差/有效样本数、next_action_class_probs、history_window、版本与隐私元数据。

### 7. 输出范围

profile/probability[0,1]；分布和1；history_window[0,configured_max]；冷启动返回先验。 所有概率必须有限；互斥分布归一误差≤1e-9。

### 8. 规则基线与基线公式

Beta-Binomial/Dirichlet公开计数更新：posterior=(prior_count+observed_count)/total；时间衰减只作用公开事件，默认半衰期20局。 模型不可用、超时、版本不兼容或输出无效时必须回退此基线。

### 9. 损失函数

下一动作categorical log loss+Brier；profile维度Beta NLL或MSE；跨局平滑正则λ||profile_t-profile_t-1||²，λ默认0.05。

### 10. 训练数据格式

按player_hash和round聚合的Parquet；public_summary与future_label分栏；含consent/license、ruleset、source_release、history_cutoff。 每条记录必须带source_release、feature_schema、label_schema、ruleset、split和canonical hash。

### 11. 数据切分方式

严格按player_id_hash切分；同一玩家不得跨train/val/test；时间上先历史后标签；匿名无法稳定分组的数据不得进正式测试。

### 12. 防止牌局泄漏规则

同一player、match、game、近重复局和seed家族不得跨切分；拟合器、归一器、词表、校准器只可用train/val。隐藏手牌/墙序只能在restricted_truth生成标签，永不进入online features。自动扫描后泄漏率必须为0。

### 13. 校准方法

Dirichlet/temperature scaling；按冷启动、历史长度、规则版本报告ECE/Brier及置信区间覆盖。 概率模型必须报告校准误差，准确率/AUC不能替代ECE、Brier和可靠性图。

### 14. 评估指标

下一动作Brier/log loss/ECE；相对关闭学习改善；profile稳定性、冷启动、遗忘曲线、收益非劣仅作外部指标。 所有指标按阶段、对手座、规则版本、数据来源和证据量分层，并报告95% CI。

### 15. 最低验收阈值

下一动作Brier相对无学习基线改善≥5%，95% CI下界>0；ECE≤0.05；状态hash复现100%；跨玩家/隐藏泄漏0。 阈值未达标时保持Not Evaluated/Failed，不得用其他指标平均抵消。

### 16. 不确定性表达

Beta/Dirichlet后验方差、有效样本量、credible interval；样本不足保持宽区间，不伪装确定风格。

### 17. 模型版本

model_version、artifact_sha256、feature/label schema、ruleset、codec、data_release、training_code_commit、config_hash、seed、calibrator_version必须齐全；未知或不兼容版本拒绝。

### 18. 回退模型

冻结全局规则先验或仅当前match公开计数；加载失败时清空学习态，不影响权威行牌。

### 19. 在线推理时限

每公开事件更新P95≤1ms；局末归档≤10ms；开局加载≤20ms。 计时含特征编码、模型、校准和输出校验；超时结果不得迟到覆盖回退。

### 20. 可解释字段

各风格维度先验、公开计数、衰减权重、后验、区间、历史窗口、被丢弃旧事件及数据来源。 通用另含request_id、seat、phase、input/output hash、latency、fallback_reason和禁止字段扫描摘要。

### 21. 测试与证据占位

必须测试正常/边界/非法schema、隐藏字段投毒、分布归一、校准、切分泄漏、超时回退、版本拒绝和同artifact冻结推理复现。MODEL-004还须测试legal mask全路径；MODEL-005须验证训练/评估隔离。

代码证据：TODO(MODEL-003-CODE)；测试证据：TODO(MODEL-003-TEST)；数据证据：TODO(MODEL-003-DATA)；校准证据：TODO(MODEL-003-CALIBRATION)；运行证据：TODO(MODEL-003-RUN)。

## MODEL-004 可训练策略输入输出与真人行为拟合契约

### 1. 预测目标

在legal mask内预测候选动作概率分布和状态价值；可用合规真人动作做行为克隆。

### 2. 预测单位

一次玩家决策请求；动作概率按固定action codec槽位。

### 3. 输入特征

TRAIN-002 Observation v2（仅PlayerView及允许的本座认知）+TRAIN-003 legal mask+冻结profile/规则上下文。

### 4. 禁止输入

对手隐藏手牌、墙序、oracle、未来奖励、未掩码非法动作、训练标签拼入observation、评估集身份或统计。。线上入口必须执行字段白名单与递归泄漏扫描；发现即拒绝，不允许仅忽略。

### 5. 标签定义

BC标签为当时legal set内真人/基线策略动作ID；RL标签为版本化回报/优势；非法或响应窗口不完整记录排除。离线truth只能在label/reward侧。 标签可以使用终局公开或离线真值，但必须位于restricted label zone，与策略输入schema、文件和加载权限隔离。

### 6. 输出格式

policy_logits[N]、masked_action_probs[N]、value、entropy、legal_mass_before_mask、版本；非法槽概率强制0，合法和1。

### 7. 输出范围

概率[0,1]且合法和1±1e-9；非法为0；value在训练配置规定闭区间；logit有限。 所有概率必须有限；互斥分布归一误差≤1e-9。

### 8. 规则基线与基线公式

规则基线对ALGO-006合法候选按HEUR/ALGO-007分数softmax：p(a)=exp(Q/T)/Σlegal exp(Q/T)，T默认0.5；mandatory唯一时概率1。 模型不可用、超时、版本不兼容或输出无效时必须回退此基线。

### 9. 损失函数

BC为masked cross-entropy，可加Brier/label smoothing≤0.05；RL为policy loss+c_v value MSE-c_e entropy；所有系数版本化。

### 10. 训练数据格式

trajectory Parquet/Arrow：observation,legal_mask,action_id,reward/return,profile,game/player/split IDs,schema hashes；restricted_truth独立文件且训练loader默认不可见。 每条记录必须带source_release、feature_schema、label_schema、ruleset、split和canonical hash。

### 11. 数据切分方式

按player→match→game分组；真人正式test永不训练、调参、提示设计；模拟seed族不得跨split。

### 12. 防止牌局泄漏规则

同一player、match、game、近重复局和seed家族不得跨切分；拟合器、归一器、词表、校准器只可用train/val。隐藏手牌/墙序只能在restricted_truth生成标签，永不进入online features。自动扫描后泄漏率必须为0。

### 13. 校准方法

验证集temperature scaling或Dirichlet calibration；按动作类别/阶段/风格报告multiclass ECE、classwise ECE、Brier、NLL。 概率模型必须报告校准误差，准确率/AUC不能替代ECE、Brier和可靠性图。

### 14. 评估指标

masked NLL、Brier、ECE、top1/top3、碰杠胡过类别Brier、非法概率质量、价值MAE、真人分布JS divergence。 所有指标按阶段、对手座、规则版本、数据来源和证据量分层，并报告95% CI。

### 15. 最低验收阈值

非法选择/非法概率质量=0；概率和误差≤1e-9；ECE≤0.05；NLL/Brier不劣规则基线，至少3个关键类别中2个Brier显著改善；无真人数据则真人拟合Not Evaluated。 阈值未达标时保持Not Evaluated/Failed，不得用其他指标平均抵消。

### 16. 不确定性表达

entropy、top1-top2 margin、deep ensemble/MC-free ensemble方差或conformal set；低置信不解除任何规则。

### 17. 模型版本

model_version、artifact_sha256、feature/label schema、ruleset、codec、data_release、training_code_commit、config_hash、seed、calibrator_version必须齐全；未知或不兼容版本拒绝。

### 18. 回退模型

上述规则Q-softmax；若Q不可用则ALGO-006稳定合法首项one-hot；超时走STATE-012。

### 19. 在线推理时限

单决策CPU P95≤20ms/P99≤50ms，目标硬件可另列GPU≤10ms；不得超过请求deadline的80%。 计时含特征编码、模型、校准和输出校验；超时结果不得迟到覆盖回退。

### 20. 可解释字段

top-k动作、概率、mask理由、主要特征贡献、校准前后概率、entropy/margin、模型/数据/config hashes；不暴露隐藏标签。 通用另含request_id、seat、phase、input/output hash、latency、fallback_reason和禁止字段扫描摘要。

### 21. 测试与证据占位

必须测试正常/边界/非法schema、隐藏字段投毒、分布归一、校准、切分泄漏、超时回退、版本拒绝和同artifact冻结推理复现。MODEL-004还须测试legal mask全路径；MODEL-005须验证训练/评估隔离。

代码证据：TODO(MODEL-004-CODE)；测试证据：TODO(MODEL-004-TEST)；数据证据：TODO(MODEL-004-DATA)；校准证据：TODO(MODEL-004-CALIBRATION)；运行证据：TODO(MODEL-004-RUN)。

## MODEL-005 训练模型产物版本、冻结和评估生命周期

### 1. 预测目标

产出可复现、可验证、不可静默替换的冻结模型卡和artifact；本单元不直接预测牌局目标。

### 2. 预测单位

一次训练run/候选模型发布物。

### 3. 输入特征

训练代码commit、数据release/split hashes、feature/label schema、规则/codec版本、配置、seed、依赖与评估报告。

### 4. 禁止输入

未声明数据、正式test反馈进入训练、缺失许可证、隐藏truth作为线上feature、未固定seed/代码、人工替换指标。。线上入口必须执行字段白名单与递归泄漏扫描；发现即拒绝，不允许仅忽略。

### 5. 标签定义

不适用牌局标签；生命周期标签为candidate/rejected/frozen/approved/deprecated及拒绝原因。 标签可以使用终局公开或离线真值，但必须位于restricted label zone，与策略输入schema、文件和加载权限隔离。

### 6. 输出格式

manifest、model bytes hash、model_card、calibrator、thresholds、compatibility matrix、evaluation refs、signature。

### 7. 输出范围

所有hash为SHA-256；版本遵循model semver+schema版本；状态有限枚举；缺字段不能frozen。 所有概率必须有限；互斥分布归一误差≤1e-9。

### 8. 规则基线与基线公式

无训练时的发布基线是显式rule-baseline artifact，记录规则公式/版本/hash，接口与MODEL-004相同；不得伪装为训练模型。 模型不可用、超时、版本不兼容或输出无效时必须回退此基线。

### 9. 损失函数

不适用模型优化；选择准则为预注册指标向量和硬门禁，禁止用单一加权总分抵消泄漏/非法/校准失败。

### 10. 训练数据格式

model/、manifest.json、model_card.md、calibrator、metrics.json、split_manifest、licenses、repro command；内容寻址。 每条记录必须带source_release、feature_schema、label_schema、ruleset、split和canonical hash。

### 11. 数据切分方式

manifest必须绑定不可变train/val/test；test只用于最终门禁；新一轮调参后原test降级为开发证据并需新冻结test。

### 12. 防止牌局泄漏规则

同一player、match、game、近重复局和seed家族不得跨切分；拟合器、归一器、词表、校准器只可用train/val。隐藏手牌/墙序只能在restricted_truth生成标签，永不进入online features。自动扫描后泄漏率必须为0。

### 13. 校准方法

校准器与模型分别版本/hash；仅val拟合，test只验收；部署必须原子加载匹配对。 概率模型必须报告校准误差，准确率/AUC不能替代ECE、Brier和可靠性图。

### 14. 评估指标

汇总各目标NLL/Brier/ECE/AUC/延迟/非法率/泄漏、分层CI、相对规则基线、漂移/OOD。 所有指标按阶段、对手座、规则版本、数据来源和证据量分层，并报告95% CI。

### 15. 最低验收阈值

所有目标模型达到本卡相应阈值；非法/泄漏0；复现实验指标在容差内；artifact/hash/兼容性100%；否则不得Approved。 阈值未达标时保持Not Evaluated/Failed，不得用其他指标平均抵消。

### 16. 不确定性表达

模型卡声明适用域、置信区间、失败分层、样本量、OOD规则和Not Evaluated项；禁止删除不利结果。

### 17. 模型版本

model_version、artifact_sha256、feature/label schema、ruleset、codec、data_release、training_code_commit、config_hash、seed、calibrator_version必须齐全；未知或不兼容版本拒绝。

### 18. 回退模型

与artifact绑定的规则基线版本；不兼容、hash错、校准器缺失或超时立即回退并审计。

### 19. 在线推理时限

生命周期加载校验≤500ms；推理时限继承所属模型；加载不得阻塞已运行牌局，切换仅在安全边界。 计时含特征编码、模型、校准和输出校验；超时结果不得迟到覆盖回退。

### 20. 可解释字段

训练数据谱系、特征/标签隔离证明、超参/seed、指标/CI、校准图、失败案例、审批、兼容矩阵、回退版本。 通用另含request_id、seat、phase、input/output hash、latency、fallback_reason和禁止字段扫描摘要。

### 21. 测试与证据占位

必须测试正常/边界/非法schema、隐藏字段投毒、分布归一、校准、切分泄漏、超时回退、版本拒绝和同artifact冻结推理复现。MODEL-004还须测试legal mask全路径；MODEL-005须验证训练/评估隔离。

代码证据：TODO(MODEL-005-CODE)；测试证据：TODO(MODEL-005-TEST)；数据证据：TODO(MODEL-005-DATA)；校准证据：TODO(MODEL-005-CALIBRATION)；运行证据：TODO(MODEL-005-RUN)。
# 3.0.1 MODEL-001校准验收数据合同

规则回退可在无训练artifact时达到E3，但不得宣称模型校准通过。E4模型验收必须冻结`model_001_calibration_manifest.json`，至少含10000个decision×opponent样本、每任务正例/类别不少于200、15个等频桶边界、data_release、split hashes、规则版本和Laplace基线预测文件hash。ECE/Brier/top-2均从该manifest唯一计算；bootstrap 1000次、命名seed=`MODEL-001-CALIBRATION-V1`并报告95% CI。manifest缺失、样本下限不足或任一切分泄漏时返回`EVALUATION_MANIFEST_INVALID`并保持Not Evaluated。
