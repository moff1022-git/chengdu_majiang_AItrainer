# TRAIN-* 训练环境完整规格

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 版本 | 0.1 |
| 日期 | 2026-07-29 |
| 覆盖 | TRAIN-001～TRAIN-009 |
| 单元数 | 9 |
| 验收 | Not Evaluated |

## 全局硬门禁

训练和生产必须共用同一个规则引擎、状态机、合法动作解析和计分服务。训练评估器与离线标签生成器可以通过受限通道读取隐藏真值，但策略观测、模型输入、动作选择和势能函数不得读取。每项奖励必须追踪到真实ScoreTransfer/score event，或追踪到显式势能差 γΦ(s')-Φ(s)；无来源的奖励禁止进入总奖励。

## TRAIN-001 复用生产规则的训练包装

### 1. Episode边界

CONFIGURED开始；单局至SETTLED，多局至设定局数/提前终止。episode_id、match_id、game_id、round_index和终止原因必须稳定记录；规则终止为terminated，时间/资源预算为truncated，二者不可混淆。

### 2. 多局和单局模式

single_round：reset创建一局，SETTLED后结束。multi_round：共享冻结match配置与累计分，逐局派生game_id，直到round_limit、规则提前终止或外部truncation。本单元必须原生支持两种模式。

### 3. 观测空间

生产PlayerView。统一Observation v2，字段、shape、dtype、范围、缺失mask和schema hash固定；任何新增字段需版本升级。

### 4. 动作空间

生产legal Action。统一固定codec；策略提交action_id，不得提交绕过codec的引擎对象。

### 5. 合法动作掩码

生产合法集映射mask。mask是bool[N]，至少一个合法动作（非决策/终止状态除外）；模型非法槽概率必须为0，encode/decode与权威legal set一致。

### 6. 隐藏状态隔离

训练与生产同state/event/hash序列。训练评估器、标签生成器和调试器可以通过独立restricted_truth channel读取隐藏真值；策略观测、模型输入、势能奖励和动作选择不得读取。自动泄漏扫描命中即失败。

### 7. 奖励

真实奖励仅来自SCORE-001账本：r_score(s,t)=score_after-score_before，并携带score_event_ids。终局累计不得重复计算已发即时分。训练专用奖励不写回真实账本。

### 8. 势能型塑形奖励

仅允许 r_shape=γΦ(o_next)-Φ(o_current)，γ∈[0,1]且默认1。Φ必须是版本化、只用策略可见观测的确定函数；默认关闭(weight=0)。每个Φ分量记录公式、输入路径、上下界和hash。

### 9. 非法动作处理

模式固定为raise、terminate或penalty之一：raise抛稳定错误且零状态写入；terminate给配置惩罚并结束；penalty给惩罚后执行确定性合法回退。不得静默接受、夹取到最近action或让非法动作影响生产state。

### 10. 自博弈

允许同版本镜像、历史快照、混合规则基线；每座策略实例/RNG/认知态隔离。响应窗口由RULE-013统一解析；训练调度不得改变房规优先级。

### 11. 对手池

pool entry包含model/artifact hash、规则/profile兼容范围、冻结日期、评级与采样权重。必须含规则基线和最近稳定模型；淘汰/晋升版本化，正式评估对手池冻结。

### 12. 随机种子

master由game_id+版本经ALGO-011派生；shuffle、dice、domain、opponent_pool、policy_noise、worker各用命名子流。禁止全局RNG、系统时间和worker调度决定样本。

### 13. 确定性回放

相同代码/规则/config/model/seed/动作序列必须重现state、obs、mask、reward、done和日志hash。浮点训练本身可非确定，但冻结推理与环境转换必须确定。

### 14. 快照和恢复

快照包含权威state schema、全部命名RNG位置、episode/match counters、累计分、pending request/response、domain/model versions。restore后下一transition逐字段等于原运行；损坏/不兼容快照拒绝。

### 15. 并行环境

worker_id仅用于派生独立子流，不进入房规。环境无共享可变GameState；结果归并按episode_id排序。并行1与N在相同episode清单上逐episodehash一致，禁止seed碰撞。

### 16. 数据记录格式

Parquet/Arrow为训练主格式，JSONL可作审计：episode/decision IDs、obs、mask、action、reward components、next_obs、terminated/truncated、score refs、seed refs、版本/hash。restricted_truth单独文件、权限和manifest。

### 17. 模型版本

记录MODEL-005 artifact、feature/observation/action/reward schema、ruleset、config、calibrator、代码commit。未知或不兼容模型拒绝并回退规则基线，不允许热替换进行中的episode。

### 18. 评估环境

评估使用冻结seed、座位轮换、对手池、规则、模型和数据manifest；允许评估器读取隐藏truth计算准确率/风险，但policy channel与训练reward仍不可见。正式test不得用于训练或调参。

### 19. 生产环境一致性

包装生产Engine/State/Rule/Score，step只提交生产事件。训练和生产必须导入并调用同一Engine/Rule/State/Score实现；禁止复制规则、简化响应或另写计分。逐事件状态、合法集、分数和终止原因应与生产路径相同。

### 20. 性能指标

报告env steps/s、决策P50/P95/P99、reset/snapshot/restore延迟、内存/worker、并行扩展效率、超时率、回放吞吐。基线目标：单环境≥500非模型steps/s，P95 transition≤5ms，4 worker效率≥70%，seed冲突0；具体硬件需记录。

### 21. 验收测试

规则等价逐事件100%，零分叉实现。通用：单局/多局、全部phase、mask双射、隐藏投毒、奖励来源、势能telescoping、三种非法mode、自博弈响应乱序、对手池、seed/回放、快照round-trip、1/N并行、模型版本拒绝、评估/生产对照。非法动作率与隐藏泄漏率均0；生产等价golden 100%。

证据占位：TODO(TRAIN-001-CODE)、TODO(TRAIN-001-TEST)、TODO(TRAIN-001-RUN)、TODO(TRAIN-001-PERF)。

## TRAIN-002 Observation v2 编码

### 1. Episode边界

继承环境episode，不创建/终止episode。episode_id、match_id、game_id、round_index和终止原因必须稳定记录；规则终止为terminated，时间/资源预算为truncated，二者不可混淆。

### 2. 多局和单局模式

single_round：reset创建一局，SETTLED后结束。multi_round：共享冻结match配置与累计分，逐局派生game_id，直到round_limit、规则提前终止或外部truncation。本单元继承该边界并在记录中保留mode。

### 3. 观测空间

tile counts、self hand、公开河/副露/状态、phase、score、wall_remaining、允许认知。统一Observation v2，字段、shape、dtype、范围、缺失mask和schema hash固定；任何新增字段需版本升级。

### 4. 动作空间

不处理动作。统一固定codec；策略提交action_id，不得提交绕过codec的引擎对象。

### 5. 合法动作掩码

不处理mask但绑定mask schema版本。mask是bool[N]，至少一个合法动作（非决策/终止状态除外）；模型非法槽概率必须为0，encode/decode与权威legal set一致。

### 6. 隐藏状态隔离

编码器只接PlayerView，评估truth走旁路。训练评估器、标签生成器和调试器可以通过独立restricted_truth channel读取隐藏真值；策略观测、模型输入、势能奖励和动作选择不得读取。自动泄漏扫描命中即失败。

### 7. 奖励

真实奖励仅来自SCORE-001账本：r_score(s,t)=score_after-score_before，并携带score_event_ids。终局累计不得重复计算已发即时分。训练专用奖励不写回真实账本。

### 8. 势能型塑形奖励

仅允许 r_shape=γΦ(o_next)-Φ(o_current)，γ∈[0,1]且默认1。Φ必须是版本化、只用策略可见观测的确定函数；默认关闭(weight=0)。每个Φ分量记录公式、输入路径、上下界和hash。

### 9. 非法动作处理

模式固定为raise、terminate或penalty之一：raise抛稳定错误且零状态写入；terminate给配置惩罚并结束；penalty给惩罚后执行确定性合法回退。不得静默接受、夹取到最近action或让非法动作影响生产state。

### 10. 自博弈

允许同版本镜像、历史快照、混合规则基线；每座策略实例/RNG/认知态隔离。响应窗口由RULE-013统一解析；训练调度不得改变房规优先级。

### 11. 对手池

pool entry包含model/artifact hash、规则/profile兼容范围、冻结日期、评级与采样权重。必须含规则基线和最近稳定模型；淘汰/晋升版本化，正式评估对手池冻结。

### 12. 随机种子

master由game_id+版本经ALGO-011派生；shuffle、dice、domain、opponent_pool、policy_noise、worker各用命名子流。禁止全局RNG、系统时间和worker调度决定样本。

### 13. 确定性回放

相同代码/规则/config/model/seed/动作序列必须重现state、obs、mask、reward、done和日志hash。浮点训练本身可非确定，但冻结推理与环境转换必须确定。

### 14. 快照和恢复

快照包含权威state schema、全部命名RNG位置、episode/match counters、累计分、pending request/response、domain/model versions。restore后下一transition逐字段等于原运行；损坏/不兼容快照拒绝。

### 15. 并行环境

worker_id仅用于派生独立子流，不进入房规。环境无共享可变GameState；结果归并按episode_id排序。并行1与N在相同episode清单上逐episodehash一致，禁止seed碰撞。

### 16. 数据记录格式

Parquet/Arrow为训练主格式，JSONL可作审计：episode/decision IDs、obs、mask、action、reward components、next_obs、terminated/truncated、score refs、seed refs、版本/hash。restricted_truth单独文件、权限和manifest。

### 17. 模型版本

记录MODEL-005 artifact、feature/observation/action/reward schema、ruleset、config、calibrator、代码commit。未知或不兼容模型拒绝并回退规则基线，不允许热替换进行中的episode。

### 18. 评估环境

评估使用冻结seed、座位轮换、对手池、规则、模型和数据manifest；允许评估器读取隐藏truth计算准确率/风险，但policy channel与训练reward仍不可见。正式test不得用于训练或调参。

### 19. 生产环境一致性

PlayerView→固定张量/字典，缺失用mask。训练和生产必须导入并调用同一Engine/Rule/State/Score实现；禁止复制规则、简化响应或另写计分。逐事件状态、合法集、分数和终止原因应与生产路径相同。

### 20. 性能指标

报告env steps/s、决策P50/P95/P99、reset/snapshot/restore延迟、内存/worker、并行扩展效率、超时率、回放吞吐。基线目标：单环境≥500非模型steps/s，P95 transition≤5ms，4 worker效率≥70%，seed冲突0；具体硬件需记录。

### 21. 验收测试

schema/range100%，隐藏字段扫描0。通用：单局/多局、全部phase、mask双射、隐藏投毒、奖励来源、势能telescoping、三种非法mode、自博弈响应乱序、对手池、seed/回放、快照round-trip、1/N并行、模型版本拒绝、评估/生产对照。非法动作率与隐藏泄漏率均0；生产等价golden 100%。

证据占位：TODO(TRAIN-002-CODE)、TODO(TRAIN-002-TEST)、TODO(TRAIN-002-RUN)、TODO(TRAIN-002-PERF)。

## TRAIN-003 固定动作 codec 与 legal mask

### 3.0.2 固定codec表

`codec_version=2`，`N=635`：0 PASS；1 HU；2..28 PONG(27 faces)；29..55 GANG_MING；56..82 GANG_AN；83..109 GANG_JIA；110..136 DISCARD；137..631 EXCHANGE（三个同花色牌面、花色顺序wan/tong/tiao、每花色组合可重复字典序，每花65组）；632..634 DINGQUE(wan/tong/tiao)。face序为wan1..9,tong1..9,tiao1..9。encode/decode必须双射；非同花色exchange、越界id及非规范action返回`ACTION_CODEC_INVALID`。

### 1. Episode边界

继承episode；每决策请求生成一次codec/mask。episode_id、match_id、game_id、round_index和终止原因必须稳定记录；规则终止为terminated，时间/资源预算为truncated，二者不可混淆。

### 2. 多局和单局模式

single_round：reset创建一局，SETTLED后结束。multi_round：共享冻结match配置与累计分，逐局派生game_id，直到round_limit、规则提前终止或外部truncation。本单元继承该边界并在记录中保留mode。

### 3. 观测空间

不新增观测特征。统一Observation v2，字段、shape、dtype、范围、缺失mask和schema hash固定；任何新增字段需版本升级。

### 4. 动作空间

固定action_id空间，encode/decode双射。统一固定codec；策略提交action_id，不得提交绕过codec的引擎对象。

### 5. 合法动作掩码

mask[id]=1 iff decode(id)∈legal。mask是bool[N]，至少一个合法动作（非决策/终止状态除外）；模型非法槽概率必须为0，encode/decode与权威legal set一致。

### 6. 隐藏状态隔离

不读取权威隐藏状态生成额外动作。训练评估器、标签生成器和调试器可以通过独立restricted_truth channel读取隐藏真值；策略观测、模型输入、势能奖励和动作选择不得读取。自动泄漏扫描命中即失败。

### 7. 奖励

真实奖励仅来自SCORE-001账本：r_score(s,t)=score_after-score_before，并携带score_event_ids。终局累计不得重复计算已发即时分。训练专用奖励不写回真实账本。

### 8. 势能型塑形奖励

仅允许 r_shape=γΦ(o_next)-Φ(o_current)，γ∈[0,1]且默认1。Φ必须是版本化、只用策略可见观测的确定函数；默认关闭(weight=0)。每个Φ分量记录公式、输入路径、上下界和hash。

### 9. 非法动作处理

模式固定为raise、terminate或penalty之一：raise抛稳定错误且零状态写入；terminate给配置惩罚并结束；penalty给惩罚后执行确定性合法回退。不得静默接受、夹取到最近action或让非法动作影响生产state。

### 10. 自博弈

允许同版本镜像、历史快照、混合规则基线；每座策略实例/RNG/认知态隔离。响应窗口由RULE-013统一解析；训练调度不得改变房规优先级。

### 11. 对手池

pool entry包含model/artifact hash、规则/profile兼容范围、冻结日期、评级与采样权重。必须含规则基线和最近稳定模型；淘汰/晋升版本化，正式评估对手池冻结。

### 12. 随机种子

master由game_id+版本经ALGO-011派生；shuffle、dice、domain、opponent_pool、policy_noise、worker各用命名子流。禁止全局RNG、系统时间和worker调度决定样本。

### 13. 确定性回放

相同代码/规则/config/model/seed/动作序列必须重现state、obs、mask、reward、done和日志hash。浮点训练本身可非确定，但冻结推理与环境转换必须确定。

### 14. 快照和恢复

快照包含权威state schema、全部命名RNG位置、episode/match counters、累计分、pending request/response、domain/model versions。restore后下一transition逐字段等于原运行；损坏/不兼容快照拒绝。

### 15. 并行环境

worker_id仅用于派生独立子流，不进入房规。环境无共享可变GameState；结果归并按episode_id排序。并行1与N在相同episode清单上逐episodehash一致，禁止seed碰撞。

### 16. 数据记录格式

Parquet/Arrow为训练主格式，JSONL可作审计：episode/decision IDs、obs、mask、action、reward components、next_obs、terminated/truncated、score refs、seed refs、版本/hash。restricted_truth单独文件、权限和manifest。

### 17. 模型版本

记录MODEL-005 artifact、feature/observation/action/reward schema、ruleset、config、calibrator、代码commit。未知或不兼容模型拒绝并回退规则基线，不允许热替换进行中的episode。

### 18. 评估环境

评估使用冻结seed、座位轮换、对手池、规则、模型和数据manifest；允许评估器读取隐藏truth计算准确率/风险，但policy channel与训练reward仍不可见。正式test不得用于训练或调参。

### 19. 生产环境一致性

仅需request phase/seat和权威legal_actions。训练和生产必须导入并调用同一Engine/Rule/State/Score实现；禁止复制规则、简化响应或另写计分。逐事件状态、合法集、分数和终止原因应与生产路径相同。

### 20. 性能指标

报告env steps/s、决策P50/P95/P99、reset/snapshot/restore延迟、内存/worker、并行扩展效率、超时率、回放吞吐。基线目标：单环境≥500非模型steps/s，P95 transition≤5ms，4 worker效率≥70%，seed冲突0；具体硬件需记录。

### 21. 验收测试

双射/合法集一致100%，非法槽0。通用：单局/多局、全部phase、mask双射、隐藏投毒、奖励来源、势能telescoping、三种非法mode、自博弈响应乱序、对手池、seed/回放、快照round-trip、1/N并行、模型版本拒绝、评估/生产对照。非法动作率与隐藏泄漏率均0；生产等价golden 100%。

证据占位：TODO(TRAIN-003-CODE)、TODO(TRAIN-003-TEST)、TODO(TRAIN-003-RUN)、TODO(TRAIN-003-PERF)。

## TRAIN-004 非法训练动作处理契约

### 1. Episode边界

非法动作发生于step边界；按mode决定是否终止episode。episode_id、match_id、game_id、round_index和终止原因必须稳定记录；规则终止为terminated，时间/资源预算为truncated，二者不可混淆。

### 2. 多局和单局模式

single_round：reset创建一局，SETTLED后结束。multi_round：共享冻结match配置与累计分，逐局派生game_id，直到round_limit、规则提前终止或外部truncation。本单元继承该边界并在记录中保留mode。

### 3. 观测空间

可见observation hash和mask，不读取隐藏truth。统一Observation v2，字段、shape、dtype、范围、缺失mask和schema hash固定；任何新增字段需版本升级。

### 4. 动作空间

输入任意action_id；合法时透传，非法时raise/terminate/penalty。统一固定codec；策略提交action_id，不得提交绕过codec的引擎对象。

### 5. 合法动作掩码

以TRAIN-003 mask为唯一判据。mask是bool[N]，至少一个合法动作（非决策/终止状态除外）；模型非法槽概率必须为0，encode/decode与权威legal set一致。

### 6. 隐藏状态隔离

错误处理不暴露为什么某隐藏状态非法。训练评估器、标签生成器和调试器可以通过独立restricted_truth channel读取隐藏真值；策略观测、模型输入、势能奖励和动作选择不得读取。自动泄漏扫描命中即失败。

### 7. 奖励

真实奖励仅来自SCORE-001账本：r_score(s,t)=score_after-score_before，并携带score_event_ids。终局累计不得重复计算已发即时分。训练专用奖励不写回真实账本。

### 8. 势能型塑形奖励

仅允许 r_shape=γΦ(o_next)-Φ(o_current)，γ∈[0,1]且默认1。Φ必须是版本化、只用策略可见观测的确定函数；默认关闭(weight=0)。每个Φ分量记录公式、输入路径、上下界和hash。

### 9. 非法动作处理

模式固定为raise、terminate或penalty之一：raise抛稳定错误且零状态写入；terminate给配置惩罚并结束；penalty给惩罚后执行确定性合法回退。不得静默接受、夹取到最近action或让非法动作影响生产state。

### 10. 自博弈

允许同版本镜像、历史快照、混合规则基线；每座策略实例/RNG/认知态隔离。响应窗口由RULE-013统一解析；训练调度不得改变房规优先级。

### 11. 对手池

pool entry包含model/artifact hash、规则/profile兼容范围、冻结日期、评级与采样权重。必须含规则基线和最近稳定模型；淘汰/晋升版本化，正式评估对手池冻结。

### 12. 随机种子

master由game_id+版本经ALGO-011派生；shuffle、dice、domain、opponent_pool、policy_noise、worker各用命名子流。禁止全局RNG、系统时间和worker调度决定样本。

### 13. 确定性回放

相同代码/规则/config/model/seed/动作序列必须重现state、obs、mask、reward、done和日志hash。浮点训练本身可非确定，但冻结推理与环境转换必须确定。

### 14. 快照和恢复

快照包含权威state schema、全部命名RNG位置、episode/match counters、累计分、pending request/response、domain/model versions。restore后下一transition逐字段等于原运行；损坏/不兼容快照拒绝。

### 15. 并行环境

worker_id仅用于派生独立子流，不进入房规。环境无共享可变GameState；结果归并按episode_id排序。并行1与N在相同episode清单上逐episodehash一致，禁止seed碰撞。

### 16. 数据记录格式

Parquet/Arrow为训练主格式，JSONL可作审计：episode/decision IDs、obs、mask、action、reward components、next_obs、terminated/truncated、score refs、seed refs、版本/hash。restricted_truth单独文件、权限和manifest。

### 17. 模型版本

记录MODEL-005 artifact、feature/observation/action/reward schema、ruleset、config、calibrator、代码commit。未知或不兼容模型拒绝并回退规则基线，不允许热替换进行中的episode。

### 18. 评估环境

评估使用冻结seed、座位轮换、对手池、规则、模型和数据manifest；允许评估器读取隐藏truth计算准确率/风险，但policy channel与训练reward仍不可见。正式test不得用于训练或调参。

### 19. 生产环境一致性

记录action_id、mask、mode、request_id。训练和生产必须导入并调用同一Engine/Rule/State/Score实现；禁止复制规则、简化响应或另写计分。逐事件状态、合法集、分数和终止原因应与生产路径相同。

### 20. 性能指标

报告env steps/s、决策P50/P95/P99、reset/snapshot/restore延迟、内存/worker、并行扩展效率、超时率、回放吞吐。基线目标：单环境≥500非模型steps/s，P95 transition≤5ms，4 worker效率≥70%，seed冲突0；具体硬件需记录。

### 21. 验收测试

三种mode精确结果100%，非法不改权威状态。通用：单局/多局、全部phase、mask双射、隐藏投毒、奖励来源、势能telescoping、三种非法mode、自博弈响应乱序、对手池、seed/回放、快照round-trip、1/N并行、模型版本拒绝、评估/生产对照。非法动作率与隐藏泄漏率均0；生产等价golden 100%。

证据占位：TODO(TRAIN-004-CODE)、TODO(TRAIN-004-TEST)、TODO(TRAIN-004-RUN)、TODO(TRAIN-004-PERF)。

## TRAIN-005 真实得分与可见势能奖励契约

### 1. Episode边界

每生产transition产生分量；episode结束汇总但不重复入账。episode_id、match_id、game_id、round_index和终止原因必须稳定记录；规则终止为terminated，时间/资源预算为truncated，二者不可混淆。

### 2. 多局和单局模式

single_round：reset创建一局，SETTLED后结束。multi_round：共享冻结match配置与累计分，逐局派生game_id，直到round_limit、规则提前终止或外部truncation。本单元继承该边界并在记录中保留mode。

### 3. 观测空间

Φ只用策略可见的向听、进张、公开风险/计划特征。统一Observation v2，字段、shape、dtype、范围、缺失mask和schema hash固定；任何新增字段需版本升级。

### 4. 动作空间

奖励不改变动作空间。统一固定codec；策略提交action_id，不得提交绕过codec的引擎对象。

### 5. 合法动作掩码

奖励计算前后使用同legal/mask版本。mask是bool[N]，至少一个合法动作（非决策/终止状态除外）；模型非法槽概率必须为0，encode/decode与权威legal set一致。

### 6. 隐藏状态隔离

评估器可另读truth算指标，但reward Φ不得读truth。训练评估器、标签生成器和调试器可以通过独立restricted_truth channel读取隐藏真值；策略观测、模型输入、势能奖励和动作选择不得读取。自动泄漏扫描命中即失败。

### 7. 奖励

真实奖励仅来自SCORE-001账本：r_score(s,t)=score_after-score_before，并携带score_event_ids。终局累计不得重复计算已发即时分。训练专用奖励不写回真实账本。

### 8. 势能型塑形奖励

仅允许 r_shape=γΦ(o_next)-Φ(o_current)，γ∈[0,1]且默认1。Φ必须是版本化、只用策略可见观测的确定函数；默认关闭(weight=0)。每个Φ分量记录公式、输入路径、上下界和hash。

### 9. 非法动作处理

模式固定为raise、terminate或penalty之一：raise抛稳定错误且零状态写入；terminate给配置惩罚并结束；penalty给惩罚后执行确定性合法回退。不得静默接受、夹取到最近action或让非法动作影响生产state。

### 10. 自博弈

允许同版本镜像、历史快照、混合规则基线；每座策略实例/RNG/认知态隔离。响应窗口由RULE-013统一解析；训练调度不得改变房规优先级。

### 11. 对手池

pool entry包含model/artifact hash、规则/profile兼容范围、冻结日期、评级与采样权重。必须含规则基线和最近稳定模型；淘汰/晋升版本化，正式评估对手池冻结。

### 12. 随机种子

master由game_id+版本经ALGO-011派生；shuffle、dice、domain、opponent_pool、policy_noise、worker各用命名子流。禁止全局RNG、系统时间和worker调度决定样本。

### 13. 确定性回放

相同代码/规则/config/model/seed/动作序列必须重现state、obs、mask、reward、done和日志hash。浮点训练本身可非确定，但冻结推理与环境转换必须确定。

### 14. 快照和恢复

快照包含权威state schema、全部命名RNG位置、episode/match counters、累计分、pending request/response、domain/model versions。restore后下一transition逐字段等于原运行；损坏/不兼容快照拒绝。

### 15. 并行环境

worker_id仅用于派生独立子流，不进入房规。环境无共享可变GameState；结果归并按episode_id排序。并行1与N在相同episode清单上逐episodehash一致，禁止seed碰撞。

### 16. 数据记录格式

Parquet/Arrow为训练主格式，JSONL可作审计：episode/decision IDs、obs、mask、action、reward components、next_obs、terminated/truncated、score refs、seed refs、版本/hash。restricted_truth单独文件、权限和manifest。

### 17. 模型版本

记录MODEL-005 artifact、feature/observation/action/reward schema、ruleset、config、calibrator、代码commit。未知或不兼容模型拒绝并回退规则基线，不允许热替换进行中的episode。

### 18. 评估环境

评估使用冻结seed、座位轮换、对手池、规则、模型和数据manifest；允许评估器读取隐藏truth计算准确率/风险，但policy channel与训练reward仍不可见。正式test不得用于训练或调参。

### 19. 生产环境一致性

r_score=真实SCORE-001分差；r_shape=γΦ(o')-Φ(o)。训练和生产必须导入并调用同一Engine/Rule/State/Score实现；禁止复制规则、简化响应或另写计分。逐事件状态、合法集、分数和终止原因应与生产路径相同。

### 20. 性能指标

报告env steps/s、决策P50/P95/P99、reset/snapshot/restore延迟、内存/worker、并行扩展效率、超时率、回放吞吐。基线目标：单环境≥500非模型steps/s，P95 transition≤5ms，4 worker效率≥70%，seed冲突0；具体硬件需记录。

### 21. 验收测试

每分量来源覆盖100%，无来源奖励0项，回放误差0。通用：单局/多局、全部phase、mask双射、隐藏投毒、奖励来源、势能telescoping、三种非法mode、自博弈响应乱序、对手池、seed/回放、快照round-trip、1/N并行、模型版本拒绝、评估/生产对照。非法动作率与隐藏泄漏率均0；生产等价golden 100%。

证据占位：TODO(TRAIN-005-CODE)、TODO(TRAIN-005-TEST)、TODO(TRAIN-005-RUN)、TODO(TRAIN-005-PERF)。

## TRAIN-006 单 learner reset/step/mask/clone/restore

### 1. Episode边界

reset创建单局或多局episode；terminated规则终局，truncated仅外部预算。episode_id、match_id、game_id、round_index和终止原因必须稳定记录；规则终止为terminated，时间/资源预算为truncated，二者不可混淆。

### 2. 多局和单局模式

single_round：reset创建一局，SETTLED后结束。multi_round：共享冻结match配置与累计分，逐局派生game_id，直到round_limit、规则提前终止或外部truncation。本单元必须原生支持两种模式。

### 3. 观测空间

Observation v2。统一Observation v2，字段、shape、dtype、范围、缺失mask和schema hash固定；任何新增字段需版本升级。

### 4. 动作空间

learner action_id。统一固定codec；策略提交action_id，不得提交绕过codec的引擎对象。

### 5. 合法动作掩码

随每request返回。mask是bool[N]，至少一个合法动作（非决策/终止状态除外）；模型非法槽概率必须为0，encode/decode与权威legal set一致。

### 6. 隐藏状态隔离

snapshot含权威state+RNG+episode counters；策略仍只见obs。训练评估器、标签生成器和调试器可以通过独立restricted_truth channel读取隐藏真值；策略观测、模型输入、势能奖励和动作选择不得读取。自动泄漏扫描命中即失败。

### 7. 奖励

真实奖励仅来自SCORE-001账本：r_score(s,t)=score_after-score_before，并携带score_event_ids。终局累计不得重复计算已发即时分。训练专用奖励不写回真实账本。

### 8. 势能型塑形奖励

仅允许 r_shape=γΦ(o_next)-Φ(o_current)，γ∈[0,1]且默认1。Φ必须是版本化、只用策略可见观测的确定函数；默认关闭(weight=0)。每个Φ分量记录公式、输入路径、上下界和hash。

### 9. 非法动作处理

模式固定为raise、terminate或penalty之一：raise抛稳定错误且零状态写入；terminate给配置惩罚并结束；penalty给惩罚后执行确定性合法回退。不得静默接受、夹取到最近action或让非法动作影响生产state。

### 10. 自博弈

允许同版本镜像、历史快照、混合规则基线；每座策略实例/RNG/认知态隔离。响应窗口由RULE-013统一解析；训练调度不得改变房规优先级。

### 11. 对手池

pool entry包含model/artifact hash、规则/profile兼容范围、冻结日期、评级与采样权重。必须含规则基线和最近稳定模型；淘汰/晋升版本化，正式评估对手池冻结。

### 12. 随机种子

master由game_id+版本经ALGO-011派生；shuffle、dice、domain、opponent_pool、policy_noise、worker各用命名子流。禁止全局RNG、系统时间和worker调度决定样本。

### 13. 确定性回放

相同代码/规则/config/model/seed/动作序列必须重现state、obs、mask、reward、done和日志hash。浮点训练本身可非确定，但冻结推理与环境转换必须确定。

### 14. 快照和恢复

快照包含权威state schema、全部命名RNG位置、episode/match counters、累计分、pending request/response、domain/model versions。restore后下一transition逐字段等于原运行；损坏/不兼容快照拒绝。

### 15. 并行环境

worker_id仅用于派生独立子流，不进入房规。环境无共享可变GameState；结果归并按episode_id排序。并行1与N在相同episode清单上逐episodehash一致，禁止seed碰撞。

### 16. 数据记录格式

Parquet/Arrow为训练主格式，JSONL可作审计：episode/decision IDs、obs、mask、action、reward components、next_obs、terminated/truncated、score refs、seed refs、版本/hash。restricted_truth单独文件、权限和manifest。

### 17. 模型版本

记录MODEL-005 artifact、feature/observation/action/reward schema、ruleset、config、calibrator、代码commit。未知或不兼容模型拒绝并回退规则基线，不允许热替换进行中的episode。

### 18. 评估环境

评估使用冻结seed、座位轮换、对手池、规则、模型和数据manifest；允许评估器读取隐藏truth计算准确率/风险，但policy channel与训练reward仍不可见。正式test不得用于训练或调参。

### 19. 生产环境一致性

整合TRAIN-001/002/003/005，提供Gym式transition。训练和生产必须导入并调用同一Engine/Rule/State/Score实现；禁止复制规则、简化响应或另写计分。逐事件状态、合法集、分数和终止原因应与生产路径相同。

### 20. 性能指标

报告env steps/s、决策P50/P95/P99、reset/snapshot/restore延迟、内存/worker、并行扩展效率、超时率、回放吞吐。基线目标：单环境≥500非模型steps/s，P95 transition≤5ms，4 worker效率≥70%，seed冲突0；具体硬件需记录。

### 21. 验收测试

clone/restore逐字节回放100%。通用：单局/多局、全部phase、mask双射、隐藏投毒、奖励来源、势能telescoping、三种非法mode、自博弈响应乱序、对手池、seed/回放、快照round-trip、1/N并行、模型版本拒绝、评估/生产对照。非法动作率与隐藏泄漏率均0；生产等价golden 100%。

证据占位：TODO(TRAIN-006-CODE)、TODO(TRAIN-006-TEST)、TODO(TRAIN-006-RUN)、TODO(TRAIN-006-PERF)。

## TRAIN-007 多玩家 ActionMap 与自博弈调度

### 1. Episode边界

联合episode同规则局/整场边界；轮到/响应座才需动作。episode_id、match_id、game_id、round_index和终止原因必须稳定记录；规则终止为terminated，时间/资源预算为truncated，二者不可混淆。

### 2. 多局和单局模式

single_round：reset创建一局，SETTLED后结束。multi_round：共享冻结match配置与累计分，逐局派生game_id，直到round_limit、规则提前终止或外部truncation。本单元继承该边界并在记录中保留mode。

### 3. 观测空间

ActionMap<seat,action_id>；异步返回按规则窗口收齐。统一Observation v2，字段、shape、dtype、范围、缺失mask和schema hash固定；任何新增字段需版本升级。

### 4. 动作空间

每座独立mask。统一固定codec；策略提交action_id，不得提交绕过codec的引擎对象。

### 5. 合法动作掩码

RULE-013解析，不按返回先后。mask是bool[N]，至少一个合法动作（非决策/终止状态除外）；模型非法槽概率必须为0，encode/decode与权威legal set一致。

### 6. 隐藏状态隔离

每策略只收本座view；中央评估truth不入policy channel。训练评估器、标签生成器和调试器可以通过独立restricted_truth channel读取隐藏真值；策略观测、模型输入、势能奖励和动作选择不得读取。自动泄漏扫描命中即失败。

### 7. 奖励

真实奖励仅来自SCORE-001账本：r_score(s,t)=score_after-score_before，并携带score_event_ids。终局累计不得重复计算已发即时分。训练专用奖励不写回真实账本。

### 8. 势能型塑形奖励

仅允许 r_shape=γΦ(o_next)-Φ(o_current)，γ∈[0,1]且默认1。Φ必须是版本化、只用策略可见观测的确定函数；默认关闭(weight=0)。每个Φ分量记录公式、输入路径、上下界和hash。

### 9. 非法动作处理

模式固定为raise、terminate或penalty之一：raise抛稳定错误且零状态写入；terminate给配置惩罚并结束；penalty给惩罚后执行确定性合法回退。不得静默接受、夹取到最近action或让非法动作影响生产state。

### 10. 自博弈

允许同版本镜像、历史快照、混合规则基线；每座策略实例/RNG/认知态隔离。响应窗口由RULE-013统一解析；训练调度不得改变房规优先级。

### 11. 对手池

pool entry包含model/artifact hash、规则/profile兼容范围、冻结日期、评级与采样权重。必须含规则基线和最近稳定模型；淘汰/晋升版本化，正式评估对手池冻结。

### 12. 随机种子

master由game_id+版本经ALGO-011派生；shuffle、dice、domain、opponent_pool、policy_noise、worker各用命名子流。禁止全局RNG、系统时间和worker调度决定样本。

### 13. 确定性回放

相同代码/规则/config/model/seed/动作序列必须重现state、obs、mask、reward、done和日志hash。浮点训练本身可非确定，但冻结推理与环境转换必须确定。

### 14. 快照和恢复

快照包含权威state schema、全部命名RNG位置、episode/match counters、累计分、pending request/response、domain/model versions。restore后下一transition逐字段等于原运行；损坏/不兼容快照拒绝。

### 15. 并行环境

worker_id仅用于派生独立子流，不进入房规。环境无共享可变GameState；结果归并按episode_id排序。并行1与N在相同episode清单上逐episodehash一致，禁止seed碰撞。

### 16. 数据记录格式

Parquet/Arrow为训练主格式，JSONL可作审计：episode/decision IDs、obs、mask、action、reward components、next_obs、terminated/truncated、score refs、seed refs、版本/hash。restricted_truth单独文件、权限和manifest。

### 17. 模型版本

记录MODEL-005 artifact、feature/observation/action/reward schema、ruleset、config、calibrator、代码commit。未知或不兼容模型拒绝并回退规则基线，不允许热替换进行中的episode。

### 18. 评估环境

评估使用冻结seed、座位轮换、对手池、规则、模型和数据manifest；允许评估器读取隐藏truth计算准确率/风险，但policy channel与训练reward仍不可见。正式test不得用于训练或调参。

### 19. 生产环境一致性

每座独立PlayerView/obs；调度器只读request集合。训练和生产必须导入并调用同一Engine/Rule/State/Score实现；禁止复制规则、简化响应或另写计分。逐事件状态、合法集、分数和终止原因应与生产路径相同。

### 20. 性能指标

报告env steps/s、决策P50/P95/P99、reset/snapshot/restore延迟、内存/worker、并行扩展效率、超时率、回放吞吐。基线目标：单环境≥500非模型steps/s，P95 transition≤5ms，4 worker效率≥70%，seed冲突0；具体硬件需记录。

### 21. 验收测试

同步/异步排列等价100%，座位轮换均衡±1%。通用：单局/多局、全部phase、mask双射、隐藏投毒、奖励来源、势能telescoping、三种非法mode、自博弈响应乱序、对手池、seed/回放、快照round-trip、1/N并行、模型版本拒绝、评估/生产对照。非法动作率与隐藏泄漏率均0；生产等价golden 100%。

证据占位：TODO(TRAIN-007-CODE)、TODO(TRAIN-007-TEST)、TODO(TRAIN-007-RUN)、TODO(TRAIN-007-PERF)。

## TRAIN-008 离线 BC 与回放 RL 数据消费

### 1. Episode边界

trajectory按episode边界存；batch不得跨序列边界而丢done。episode_id、match_id、game_id、round_index和终止原因必须稳定记录；规则终止为terminated，时间/资源预算为truncated，二者不可混淆。

### 2. 多局和单局模式

single_round：reset创建一局，SETTLED后结束。multi_round：共享冻结match配置与累计分，逐局派生game_id，直到round_limit、规则提前终止或外部truncation。本单元继承该边界并在记录中保留mode。

### 3. 观测空间

存储的Observation v2；restricted_truth仅评估loader。统一Observation v2，字段、shape、dtype、范围、缺失mask和schema hash固定；任何新增字段需版本升级。

### 4. 动作空间

action_id必须mask=1；否则样本隔离。统一固定codec；策略提交action_id，不得提交绕过codec的引擎对象。

### 5. 合法动作掩码

读取并复验mask。mask是bool[N]，至少一个合法动作（非决策/终止状态除外）；模型非法槽概率必须为0，encode/decode与权威legal set一致。

### 6. 隐藏状态隔离

label/truth独立文件和权限；正式test不训练。训练评估器、标签生成器和调试器可以通过独立restricted_truth channel读取隐藏真值；策略观测、模型输入、势能奖励和动作选择不得读取。自动泄漏扫描命中即失败。

### 7. 奖励

真实奖励仅来自SCORE-001账本：r_score(s,t)=score_after-score_before，并携带score_event_ids。终局累计不得重复计算已发即时分。训练专用奖励不写回真实账本。

### 8. 势能型塑形奖励

仅允许 r_shape=γΦ(o_next)-Φ(o_current)，γ∈[0,1]且默认1。Φ必须是版本化、只用策略可见观测的确定函数；默认关闭(weight=0)。每个Φ分量记录公式、输入路径、上下界和hash。

### 9. 非法动作处理

模式固定为raise、terminate或penalty之一：raise抛稳定错误且零状态写入；terminate给配置惩罚并结束；penalty给惩罚后执行确定性合法回退。不得静默接受、夹取到最近action或让非法动作影响生产state。

### 10. 自博弈

允许同版本镜像、历史快照、混合规则基线；每座策略实例/RNG/认知态隔离。响应窗口由RULE-013统一解析；训练调度不得改变房规优先级。

### 11. 对手池

pool entry包含model/artifact hash、规则/profile兼容范围、冻结日期、评级与采样权重。必须含规则基线和最近稳定模型；淘汰/晋升版本化，正式评估对手池冻结。

### 12. 随机种子

master由game_id+版本经ALGO-011派生；shuffle、dice、domain、opponent_pool、policy_noise、worker各用命名子流。禁止全局RNG、系统时间和worker调度决定样本。

### 13. 确定性回放

相同代码/规则/config/model/seed/动作序列必须重现state、obs、mask、reward、done和日志hash。浮点训练本身可非确定，但冻结推理与环境转换必须确定。

### 14. 快照和恢复

快照包含权威state schema、全部命名RNG位置、episode/match counters、累计分、pending request/response、domain/model versions。restore后下一transition逐字段等于原运行；损坏/不兼容快照拒绝。

### 15. 并行环境

worker_id仅用于派生独立子流，不进入房规。环境无共享可变GameState；结果归并按episode_id排序。并行1与N在相同episode清单上逐episodehash一致，禁止seed碰撞。

### 16. 数据记录格式

Parquet/Arrow为训练主格式，JSONL可作审计：episode/decision IDs、obs、mask、action、reward components、next_obs、terminated/truncated、score refs、seed refs、版本/hash。restricted_truth单独文件、权限和manifest。

### 17. 模型版本

记录MODEL-005 artifact、feature/observation/action/reward schema、ruleset、config、calibrator、代码commit。未知或不兼容模型拒绝并回退规则基线，不允许热替换进行中的episode。

### 18. 评估环境

评估使用冻结seed、座位轮换、对手池、规则、模型和数据manifest；允许评估器读取隐藏truth计算准确率/风险，但policy channel与训练reward仍不可见。正式test不得用于训练或调参。

### 19. 生产环境一致性

消费版本化obs/mask/action/reward/next_obs/done。训练和生产必须导入并调用同一Engine/Rule/State/Score实现；禁止复制规则、简化响应或另写计分。逐事件状态、合法集、分数和终止原因应与生产路径相同。

### 20. 性能指标

报告env steps/s、决策P50/P95/P99、reset/snapshot/restore延迟、内存/worker、并行扩展效率、超时率、回放吞吐。基线目标：单环境≥500非模型steps/s，P95 transition≤5ms，4 worker效率≥70%，seed冲突0；具体硬件需记录。

### 21. 验收测试

split泄漏0，mask违例样本0进入训练。通用：单局/多局、全部phase、mask双射、隐藏投毒、奖励来源、势能telescoping、三种非法mode、自博弈响应乱序、对手池、seed/回放、快照round-trip、1/N并行、模型版本拒绝、评估/生产对照。非法动作率与隐藏泄漏率均0；生产等价golden 100%。

证据占位：TODO(TRAIN-008-CODE)、TODO(TRAIN-008-TEST)、TODO(TRAIN-008-RUN)、TODO(TRAIN-008-PERF)。

## TRAIN-009 房规、profile 与行为域随机化

### 1. Episode边界

仅reset安全边界采样；episode内冻结。episode_id、match_id、game_id、round_index和终止原因必须稳定记录；规则终止为terminated，时间/资源预算为truncated，二者不可混淆。

### 2. 多局和单局模式

single_round：reset创建一局，SETTLED后结束。multi_round：共享冻结match配置与累计分，逐局派生game_id，直到round_limit、规则提前终止或外部truncation。本单元继承该边界并在记录中保留mode。

### 3. 观测空间

采样后的公开规则/profile摘要进入obs允许字段。统一Observation v2，字段、shape、dtype、范围、缺失mask和schema hash固定；任何新增字段需版本升级。

### 4. 动作空间

动作空间随规则但codec固定。统一固定codec；策略提交action_id，不得提交绕过codec的引擎对象。

### 5. 合法动作掩码

mask由采样后生产规则生成。mask是bool[N]，至少一个合法动作（非决策/终止状态除外）；模型非法槽概率必须为0，encode/decode与权威legal set一致。

### 6. 隐藏状态隔离

采样器可知配置但策略不得获未公开配置真值。训练评估器、标签生成器和调试器可以通过独立restricted_truth channel读取隐藏真值；策略观测、模型输入、势能奖励和动作选择不得读取。自动泄漏扫描命中即失败。

### 7. 奖励

真实奖励仅来自SCORE-001账本：r_score(s,t)=score_after-score_before，并携带score_event_ids。终局累计不得重复计算已发即时分。训练专用奖励不写回真实账本。

### 8. 势能型塑形奖励

仅允许 r_shape=γΦ(o_next)-Φ(o_current)，γ∈[0,1]且默认1。Φ必须是版本化、只用策略可见观测的确定函数；默认关闭(weight=0)。每个Φ分量记录公式、输入路径、上下界和hash。

### 9. 非法动作处理

模式固定为raise、terminate或penalty之一：raise抛稳定错误且零状态写入；terminate给配置惩罚并结束；penalty给惩罚后执行确定性合法回退。不得静默接受、夹取到最近action或让非法动作影响生产state。

### 10. 自博弈

允许同版本镜像、历史快照、混合规则基线；每座策略实例/RNG/认知态隔离。响应窗口由RULE-013统一解析；训练调度不得改变房规优先级。

### 11. 对手池

pool entry包含model/artifact hash、规则/profile兼容范围、冻结日期、评级与采样权重。必须含规则基线和最近稳定模型；淘汰/晋升版本化，正式评估对手池冻结。

### 12. 随机种子

master由game_id+版本经ALGO-011派生；shuffle、dice、domain、opponent_pool、policy_noise、worker各用命名子流。禁止全局RNG、系统时间和worker调度决定样本。

### 13. 确定性回放

相同代码/规则/config/model/seed/动作序列必须重现state、obs、mask、reward、done和日志hash。浮点训练本身可非确定，但冻结推理与环境转换必须确定。

### 14. 快照和恢复

快照包含权威state schema、全部命名RNG位置、episode/match counters、累计分、pending request/response、domain/model versions。restore后下一transition逐字段等于原运行；损坏/不兼容快照拒绝。

### 15. 并行环境

worker_id仅用于派生独立子流，不进入房规。环境无共享可变GameState；结果归并按episode_id排序。并行1与N在相同episode清单上逐episodehash一致，禁止seed碰撞。

### 16. 数据记录格式

Parquet/Arrow为训练主格式，JSONL可作审计：episode/decision IDs、obs、mask、action、reward components、next_obs、terminated/truncated、score refs、seed refs、版本/hash。restricted_truth单独文件、权限和manifest。

### 17. 模型版本

记录MODEL-005 artifact、feature/observation/action/reward schema、ruleset、config、calibrator、代码commit。未知或不兼容模型拒绝并回退规则基线，不允许热替换进行中的episode。

### 18. 评估环境

评估使用冻结seed、座位轮换、对手池、规则、模型和数据manifest；允许评估器读取隐藏truth计算准确率/风险，但policy channel与训练reward仍不可见。正式test不得用于训练或调参。

### 19. 生产环境一致性

sampled_domain由命名seed和批准范围产生。训练和生产必须导入并调用同一Engine/Rule/State/Score实现；禁止复制规则、简化响应或另写计分。逐事件状态、合法集、分数和终止原因应与生产路径相同。

### 20. 性能指标

报告env steps/s、决策P50/P95/P99、reset/snapshot/restore延迟、内存/worker、并行扩展效率、超时率、回放吞吐。基线目标：单环境≥500非模型steps/s，P95 transition≤5ms，4 worker效率≥70%，seed冲突0；具体硬件需记录。

### 21. 验收测试

同seed复现100%，越界0，覆盖组合达到manifest。通用：单局/多局、全部phase、mask双射、隐藏投毒、奖励来源、势能telescoping、三种非法mode、自博弈响应乱序、对手池、seed/回放、快照round-trip、1/N并行、模型版本拒绝、评估/生产对照。非法动作率与隐藏泄漏率均0；生产等价golden 100%。

证据占位：TODO(TRAIN-009-CODE)、TODO(TRAIN-009-TEST)、TODO(TRAIN-009-RUN)、TODO(TRAIN-009-PERF)。
