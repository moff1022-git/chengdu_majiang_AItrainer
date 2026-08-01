# Spec v3 测试策略

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 功能单元 | 96/96 |
| 用例状态 | Specified / Not Implemented / Not Evaluated |
| 上游 | Approved单元规格、Approved基础测试规格 |

## 1. 测试层级

每单元逐项检查单元、边界、参数化、属性、状态机、集成、随机回放、统计分布、模型校准、性能和隐藏信息泄漏11类。覆盖矩阵的`Y`必须在用例目录中有唯一测试卡；`N`必须给出方法学理由，不能因为尚未实现而标N。

单元测试隔离单一职责；集成测试只能走生产门面；系统/回放测试保存完整事件与环境。测试fixture不得复制生产规则、计分或状态机，expected来自Approved规范公式、人工冻结golden或独立不变量。

## 2. 方法边界

- RULE/STATE/ALGO/SCORE：规范字段、状态、集合、整数和hash精确比较；浮点只用规格明示误差。
- HEUR：验证合法允许域、候选上限、方向效应、regret、统计分布和95% CI，不强制每手唯一动作。
- MODEL：冻结牌局级切分，必须报告Brier、log loss、ECE、可靠性和不确定性；准确率不能单独通过。
- TRAIN：与生产Engine逐事件等价；reward追踪ScoreTransfer或显式势能差；策略观测不得读truth。
- AUDIT：证据缺失、过期、篡改、泄漏或hard失败不得输出Passed。

## 3. 确定性与随机回放

所有用例记录命名seed，即使目标不消费随机数也记录`seed_ref`。相同输入、初态、规则/config/code/model/schema版本和seed必须完整复现action、状态序列、分数、日志与hash；跨进程至少复算两次。新增随机调用必须使用新命名子域，禁止全局RNG、系统时间、Python`hash()`或线程到达顺序。

## 4. 金标准向量

ALGO-001～011每个至少有正常、边界、非法三类冻结向量；SCORE同样登记三类。向量实现于`tests/spec_v3/vectors/<unit>.jsonl`，必须包含canonical input、expected/expected_error、中间量、公式版本、允许误差和SHA-256。基线公式输出可另存`baseline_expected`，不得替代规范expected。

## 5. 隐藏信息隔离

全部96单元均有HL用例。成对状态保持PlayerView/公开事件/合法集相同，只改变对手手牌、墙序、future truth或离线标签；策略侧输出必须不变。评估器可读取restricted truth，但模块/进程/文件权限、loader和日志通道与policy隔离。任何公开日志、异常文本或解释字段泄漏实体牌/隐藏牌即hard失败。

## 6. 统计与校准

统计用例预先冻结样本量、seed集合、指标、阈值和alpha=0.05，报告效应量及95% CI；不得观察结果后调阈值。启发式硬约束逐样本100%满足，软行为按Approved区间验收。概率模型使用牌局/玩家/时间防泄漏切分并比较规则基线；ECE分桶规则也必须冻结。

## 7. 性能

性能用例同时执行功能oracle；冻结硬件、OS、Python/依赖、数据、warm-up、并发和采样次数，报告P50/P95/P99、吞吐、峰值内存。超预算或功能漂移均失败；不得只选最好一次或用缓存结果冒充全路径。

## 8. 失败、skip和证据

hard gate不得N/A、skip或宽松xfail。其他N/A需owner和批准理由；临时skip需issue和到期日。Passed至少需要E3直接测试证据；跨模块/回放/性能需要E4；真人相似、强度和学习效果需要E5。当前目录只定义用例，测试代码、向量与运行证据仍Not Implemented/Not Evaluated。

## 9. 执行批次

按锁定DAG执行：配置/RNG/状态/牌墙→RULE→ALGO/SCORE/View→HEUR/MODEL→TRAIN→AUDIT。每批先落向量和fixture，再实现用例；通过后回填JUnit、环境manifest、commit、版本、seed、输入/输出hash和证据新鲜度。
