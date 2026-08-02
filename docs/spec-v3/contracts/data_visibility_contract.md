# 数据可见性契约

| 等级 | 定义 | 允许消费者 |
|---|---|---|
| PUBLIC | 已公开规则、弃牌、副露、状态、允许的墙余量 | 所有座、UI、策略、日志脱敏视图 |
| PLAYER_PRIVATE | 本座暗手、收到的换牌、本座认知状态和参数 | 该座策略及权威引擎 |
| SIMULATOR_TRUTH | 对手暗手、墙序、未来事件、oracle标签、restricted truth | 权威规则、离线评估器、标签生成器 |
| RESTRICTED_AUDIT | 完整状态、身份映射、原始训练truth | 最小权限审计器 |

## 字段矩阵

| 数据 | 引擎 | 本座PlayerView | 对手视图 | 策略 | 训练评估器 | 公共日志 |
|---|---:|---:|---:|---:|---:|---:|
| 本座暗手牌面/实体 | 是 | 是 | 否 | 是 | 是 | hash |
| 对手暗手/实体 | 是 | 否 | 仅其本人 | 否 | restricted truth | hash |
| 完整墙序 | 是 | 否 | 否 | 否 | restricted truth | hash |
| 墙余量 | 是 | GP-021 | GP-021 | 同PlayerView | 是 | 公开值 |
| 弃牌/公开副露 | 是 | 是 | 是 | 是 | 是 | 是 |
| 暗杠精确牌面 | 是 | GP-021 | GP-021 | 同PlayerView | 是 | 按策略 |
| 策略私有记忆/情绪 | 否 | 本座策略私有 | 否 | 本座 | 否 | private audit/hash |
| 终局/离线标签 | 是 | 仅规则允许公开 | 同左 | 禁止 | restricted | 聚合/hash |

PlayerView采用默认拒绝白名单。任何`hand,physical_hand,wall_order,oracle_hands,label_zone,truth`在非本座或策略输入的嵌套位置出现均为`VISIBILITY_LEAK/FORBIDDEN_INPUT`。训练策略、势能奖励和在线模型只能读取PlayerView；评估器读取truth必须通过独立对象、文件、schema和权限，不得把字段附加到Observation后“依赖模型忽略”。

强制表述：**策略禁止**读取或推导`SIMULATOR_TRUTH`与`RESTRICTED_AUDIT`字段；即使调用方声称不使用，只要该字段进入策略schema即为契约违反。

日志必须在序列化前脱敏；禁止先写明文再清洗。hidden/private对象不得出现在异常文本、repr、性能样本或解释字段。契约测试执行四座交叉、递归sentinel、序列化往返和静态禁止import检查。
