# Spec v3 开发实施指南

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 依据 | UNIT-CATALOG 1.0.0 Locked；96份单元规格Approved；96份测试规格Approved |
| 实现/验收 | Not Evaluated |

## 1. 文档角色与权威边界

本文只规定代码组织、公共接口、调用顺序、实施门禁与迁移方法，不复制单元内部公式、房规或验收阈值。发生差异时依次服从锁定目录、已批准单元规格、已批准测试规格；本文中的类型和接口是推荐实现骨架，若实施时需要改变公开字段，必须先更新相应单元规格。

## 2. 推荐模块结构

```text
engine/
  domain/                 # 纯数据：tile/action/event/state/score_transfer/error
  config/                 # schema、loader、validator、frozen snapshot、version/hash
  rng/                    # game_id派生、NamedRandomStreams；禁止散落random
  state/                  # match/round/wall/player/response/ledger存储与迁移
  rules/                  # RULE-*纯裁决与RuleEngine门面
  analysis/               # ALGO-*确定算法；不得依赖players/models
  scoring/                # SCORE-*识别、转移、账本、排名
  view/                   # PlayerView白名单投影与脱敏
  runtime/                # command handler、状态机、响应窗、事件总线、orchestrator
  audit/                  # 事件/决策日志、hash、回放、不变量与证据接口
players/
  base_player.py          # PlayerPort
  humanlike/
    cognition/            # STATE-006/007/008
    heuristics/           # HEUR-*
    models/               # MODEL-*推理门面、基线与artifact加载
    decision/             # STATE-009决策管线与解释
training/
  env/                    # TRAIN-001～004；只包装生产runtime
  selfplay/               # TRAIN-005
  replay/                 # TRAIN-006
  vector/                 # TRAIN-007
  data/                   # TRAIN-008
  evaluation/             # TRAIN-009；restricted truth仅在此
protocols/
  schemas/                # 对外消息schema/version
tests/spec_v3/
  vectors/                # Approved JSONL golden/边界/非法向量
  fixtures/               # 生产入口fixture；禁止第二规则oracle
  test_<unit_id>.py       # 96个计划测试模块
```

迁移期间允许旧文件继续存在，但新代码只能通过稳定门面调用；旧路径不得新增第二份规则、计分、随机或状态真值。模块具体落点以[开发任务卡](development_task_cards.md)逐单元“文件建议”为准。

## 3. 公共数据结构

公共结构优先使用`@dataclass(frozen=True, slots=True)`或等价不可变值对象；跨进程/落盘必须有`schema_version`和canonical序列化。

```python
PhysicalTileId = int          # 0..107；唯一实体身份
FaceTile = int                # 0..26；万/筒/条×1..9
Seat = int                    # 0..num_players-1
EventIndex = int              # uint64单调递增

@dataclass(frozen=True, slots=True)
class VersionBundle:
    rule_version: str
    parameter_version: str
    implementation_version: str
    schema_version: str

@dataclass(frozen=True, slots=True)
class MatchContext:
    match_id: str
    game_id: str
    versions: VersionBundle
    config_hash: str
    code_hash: str
    seed_manifest_hash: str

@dataclass(frozen=True, slots=True)
class Command:
    command_id: str
    actor: Seat | None
    kind: str
    payload: Mapping[str, JsonValue]
    expected_state_version: int

@dataclass(frozen=True, slots=True)
class DomainEvent:
    event_id: str
    event_index: EventIndex
    kind: str
    actor: Seat | None
    public_payload: Mapping[str, JsonValue]
    private_refs: tuple[str, ...]
    before_hash: str
    after_hash: str

@dataclass(frozen=True, slots=True)
class PlayerView:
    viewer: Seat
    state_version: int
    phase: str
    public_events: tuple[DomainEvent, ...]
    self_private: Mapping[str, JsonValue]
    legal_actions: tuple["Action", ...]

@dataclass(frozen=True, slots=True)
class ActionRequest:
    request_id: str
    actor: Seat
    phase: str
    deadline_ms: int
    view: PlayerView

@dataclass(frozen=True, slots=True)
class Decision:
    request_id: str
    action: "Action"
    explanation: Mapping[str, JsonValue]
    policy_version: str

@dataclass(frozen=True, slots=True)
class ScoreTransfer:
    transfer_id: str
    event_id: str
    reason: str
    deltas: Mapping[Seat, int]  # 每条必须sum==0

@dataclass(frozen=True, slots=True)
class UnitError:
    code: str
    unit_id: str
    message: str
    retryable: bool
    public_context: Mapping[str, JsonValue]
    private_ref: str | None
```

状态对象、事件和日志不得存活的可变引用；`PlayerView`不得包含对手手牌、墙序、未来事件、审计truth或离线标签。

## 4. 核心接口定义

```python
class RuleEngine(Protocol):
    def legal_actions(self, state: RoundState, request: ActionRequest) -> tuple[Action, ...]: ...
    def validate(self, state: RoundState, command: Command) -> None: ...
    def decide_effects(self, state: RoundState, command: Command) -> tuple[DomainEvent, ...]: ...

class StateStore(Protocol):
    def snapshot(self) -> RoundState: ...
    def commit(self, expected_version: int, events: Sequence[DomainEvent]) -> RoundState: ...

class ScoreEngine(Protocol):
    def transfers(self, state: RoundState, events: Sequence[DomainEvent]) -> tuple[ScoreTransfer, ...]: ...

class ViewProjector(Protocol):
    def project(self, state: RoundState, viewer: Seat, legal: Sequence[Action]) -> PlayerView: ...

class PlayerPort(Protocol):
    def decide(self, request: ActionRequest) -> Decision: ...

class EventSubscriber(Protocol):
    def handle(self, envelope: EventEnvelope) -> None: ...

class NamedRandomStreams(Protocol):
    def derive_seed(self, domain: str, *stable_keys: object) -> int: ...
    def stream(self, domain: str, *stable_keys: object) -> RandomLike: ...

class AuditSink(Protocol):
    def append(self, envelope: EventEnvelope) -> AuditReceipt: ...
```

所有门面返回稳定值或抛稳定`UnitError`映射；禁止跨层返回内部可变对象、裸异常或包含隐藏字段的字典。

## 5. 权威状态机

权威运行枚举只采用Approved `STATE-004`的`RoundPhase`。Match创建、局创建、提交/解析、计分累积等名称是命令或领域事件，不是第二套phase枚举。

```text
CONFIGURED → DEALT → EXCHANGE（GP-005关闭时可跳过）→ DINGQUE → READY
READY → DRAW → DISCARD → RESPONSE
                 ↑         ├─ HU事件后：仍有至少2名active → DRAW
                 │         ├─ GANG事件后：补摸 → DRAW
                 └─────────┴─ PENG/ALL_PASS后：DISCARD或下一家DRAW
DRAW/DISCARD/RESPONSE → FINISHED → SETTLED
```

事件到phase的唯一映射如下；事件名称不得进入`RoundPhase`字段：

| 领域事件/命令 | phase_before | phase_after |
|---|---|---|
| `ROUND_CONFIGURED` | 无 | `CONFIGURED` |
| `DEAL_COMMITTED` | `CONFIGURED` | `DEALT` |
| `EXCHANGE_OPENED/RESOLVED` | `DEALT/EXCHANGE` | `EXCHANGE/DINGQUE` |
| `DINGQUE_OPENED/RESOLVED` | `DEALT或EXCHANGE/DINGQUE` | `DINGQUE/READY` |
| `DRAW_COMMITTED` | `READY或RESPONSE或DRAW` | `DRAW` |
| `DISCARD_COMMITTED` | `DRAW或RESPONSE` | `DISCARD` |
| `RESPONSE_OPENED/RESOLVED` | `DISCARD/RESPONSE` | `RESPONSE`或转换表允许的下一phase |
| `ROUND_TERMINATED` | `READY/DRAW/DISCARD/RESPONSE` | `FINISHED` |
| `SETTLEMENT_COMMITTED` | `FINISHED` | `SETTLED` |

整场生命周期由STATE-001持有，使用`match_status=CREATED/ACTIVE/COMPLETED`；它与STATE-004的`RoundPhase`是不同字段，不得互相赋值。只有`runtime/command_handler`可请求STATE-004转换，只有`StateStore.commit`可落权威phase。响应窗口持有`request_id`、候选响应者、deadline、已收响应和稳定座次；解析顺序固定为资格过滤→胡优先→多人胡规则→杠/碰→座次tie-break→PASS。非法命令、重复命令和旧版本命令在commit前失败。

## 6. 事件总线

事件总线是提交后分发，不是共享状态容器。同步关键订阅者按固定顺序运行：

1. `InvariantSubscriber`：提交后强不变量；失败令当前事务失败或进入隔离故障状态。
2. `ScoreSubscriber`：只消费已提交规则事实，生成零和`ScoreTransfer`。
3. `LedgerSubscriber`：幂等写账本。
4. `ViewCacheInvalidator`：仅清缓存，不产生权威事实。
5. `AuditSubscriber`：append-only canonical日志与hash链。
6. `TrainingRecorder`：从公开/受限分区分别写数据，不回流策略。
7. UI/遥测异步订阅者：可丢帧或重试，不得阻塞或改变规则结果。

事件键为`(game_id,event_index,event_id)`；订阅者使用幂等键，重复投递不得重复计分。异步顺序按event_index重排，无法补齐缺口时标记不完整，不得伪造连续日志。

## 7. 规则引擎调用顺序

```text
接收Command
→ schema/version/权限验证
→ expected_state_version并发检查
→ RULE-001总优先级
→ 阶段专属RULE资格与强制约束
→ RULE-016可见性/信息边界检查
→ 生成DomainEvent草案
→ 纯函数reduce得到候选后置状态
→ RULE/STATE/SCORE强不变量预检
→ 原子commit
→ ScoreTransfer与Ledger
→ 事件总线分发、日志和新ActionRequest
```

计分不得参与胡牌合法性；HEUR/MODEL不得改变legal set；日志失败不得静默丢失权威事件，按配置执行fail-closed或受控降级并记录错误。

## 8. AI决策调用顺序

```text
ActionRequest
→ RULE-016/STATE-005构建不可变PlayerView
→ ALGO-010再次校验字段白名单
→ STATE-006更新仅公开认知
→ ALGO-002～005确定分析
→ ALGO-006生成mandatory与有限候选
→ HEUR主计划/备选计划及候选软评分
→ MODEL可选概率/风险/动作分布（超时/OOD则规则基线）
→ ALGO-007组合规范Q分量
→ HEUR风格/水平/阶段/注意/满意停止/允许扰动
→ STATE-009选择一个legal action
→ AUDIT-002写特征版本、候选、分量、模型不确定性、回退和选择理由
→ 返回Decision；Engine重新验证后提交
```

策略端永远不接收`RoundState`。强制动作、合法mask、信息白名单和超时回退不能被模型替换。

## 9. 配置加载

加载顺序固定：内建schema默认值→版本化规则集→部署配置→比赛配置→逐座Profile允许覆盖→命令行允许覆盖→一次性校验/冻结→canonical JSON→SHA-256。未知键默认拒绝；范围、互斥、跨字段和版本兼容在STATE-010/ALGO-009完成。运行中不得原地修改配置；变更必须创建新`config_version/config_hash`并在允许的局界生效。

敏感项、训练标签路径和审计密钥不进入PlayerView。旧配置通过显式migration函数升级，保留输入hash、迁移版本、输出hash和告警。

## 10. 随机数管理

所有随机性经ALGO-011命名域派生：`shuffle`、`dice`、`exchange_direction`、`policy/<seat>`、`human_error/<seat>`、`think_time/<seat>`、`training/opponent`、`property_test`。派生输入至少包含`game_id`、版本、稳定座次/事件/decision index；禁止Python进程`hash()`、模块全局RNG、系统时间和调用顺序作为规范种子。

同域同键只表示同一随机对象；新增随机调用必须使用新子域，不能插入旧流改变历史序列。seed manifest进入回放和审计，不公开足以反推出隐藏墙序的信息。

## 11. 日志和回放

每个权威事件写公共载荷与受控私有引用，canonical JSON使用UTF-8、固定字段、稳定数字表示和排序；记录`prev_hash/record_hash`。AI决策日志保存可见特征hash、参数/模型版本、legal/mask、候选分量、选择、回退和耗时，不保存未授权truth。

回放输入为冻结配置、版本、seed manifest、初始快照及有序命令/事件。验证按event_index比较state/action/score/log hash并定位首个差异。日志、回放和证据保留由AUDIT-001～004/014定义；缺失或过期证据是Not Evaluated/Failed，不得推断Passed。

## 12. 错误处理

错误分四类：`VALIDATION_*`调用方输入错误；`CONFLICT_*`版本/重复/并发冲突；`RULE_*`稳定业务拒绝；`INTERNAL_*`不变量、持久化或未知故障。错误必须带`unit_id/code/request_id/state_version`，公开消息脱敏，私有诊断用引用关联。

重试只允许显式`retryable=True`且幂等的基础设施错误。玩家超时/崩溃由STATE-012按冻结策略选择PASS、稳定合法弃牌、替换或终止；不得让异常路径绕过规则。`except Exception: pass`、返回空合法集掩盖错误、静默修复守恒均禁止。

## 13. 性能要求

性能验收阈值只从对应Approved单元规格的性能/复杂度/在线时限字段读取；本指南不另设规则、分析、视图、回退或模型延迟数字。跨单元容量规划可以汇总`steps/s`、P50/P95/P99 step latency、内存/环境和确定回放成功率，但汇总值不得替代、放宽或覆盖任一单元阈值。若单元规格未给出可测阈值，AC-12保持`Not Evaluated`并先走规格变更，不得在实现或测试中临时发明门槛。

所有性能测试冻结硬件、Python/依赖、样本、warm-up、进程数和统计口径；不得用缓存命中结果替代冷/热两组报告。性能优化不得改变canonical结果、随机流或隐藏边界。

## 14. 分阶段开发顺序与完成条件

| 阶段 | 单元/主题 | 主要产出 | 完成条件 |
|---|---|---|---|
| D0 | 基线与脚手架 | 差距矩阵、包骨架、公共schema、适配器 | 96单元均有现状分类；旧测试基线保存；无行为变化 |
| D1 | STATE-010、ALGO-009/011、STATE-001/002/011 | 冻结配置、版本/hash、命名RNG、牌墙和权威状态 | 同game_id重放一致；108牌守恒；配置错误稳定拒绝 |
| D2 | RULE-001～016、STATE-003/004/009/012 | 规则门面、完整状态机、响应窗、回退 | 换三张/定缺/摸打/碰杠胡/多人响应/胡后退出/墙终止P0合同通过 |
| D3 | ALGO-001～008/010、SCORE-001～006 | 确定分析、PlayerView、计分和账本 | 规范golden通过；逐事件/层/本局ΣΔ=0；无模型替代 |
| D4 | STATE-005～008、HEUR-001～023 | 视图、认知、主备计划和人类化策略 | 非法/泄漏0；同seed复现；统计方向效应和regret按卡通过 |
| D5 | MODEL-001～005 | 特征/标签隔离、规则基线、校准模型和生命周期 | ECE/Brier等阈值、OOD/超时回退、artifact门禁通过 |
| D6 | TRAIN-001～009 | 生产同源环境、自博弈、回放、数据与评估 | 生产等价golden、reward溯源、truth隔离、快照恢复通过 |
| D7 | AUDIT-001～014 | 日志/hash/回放/证据/发布门禁 | 96单元追踪无断链；hard gate全通过；证据新鲜且脱敏 |
| D8 | 兼容收口 | 删除旧写路径、迁移存档/配置、性能与发布 | 无双写/双规则；全量回归与发布审计通过；回滚包可用 |

阶段不可只因文件或类存在而完成。每阶段必须回填任务卡代码、测试和运行证据；未实现项保持Not Evaluated。

## 15. 依赖原则

依赖顺序由锁定DAG唯一决定。允许方向为domain/config/rng→state/rules/analysis/scoring→view→players→training/audit；`engine`不得导入具体玩家、模型或训练包，`analysis`不得导入HEUR/MODEL，`training`不得拥有规则实现，UI不得产生业务事实。循环需求通过不可变事件、Protocol或依赖注入拆解。

## 16. 禁止的实现方式

- 在训练、玩家、UI或测试fixture复制规则、计分或状态机。
- 用HEUR/MODEL替代合法性、向听/计数、计分、守恒、mask、hash或状态转移。
- 将对手隐藏手牌、墙序、未来事件、离线标签或审计truth传入线上策略。
- 依赖字典/集合迭代、线程到达、系统时间、Python`hash()`或全局RNG决定规范结果。
- 原地修改权威状态、配置、PlayerView或已发布事件；跨层共享可变引用。
- 在事件总线中先发事件后提交状态，或让异步订阅者修改权威结果。
- 用浮点累计真实分数，忽略每个支付方—接收方守恒，或回放重复入账。
- 吞异常、使用不稳定错误文本当协议、失败后伪造空结果或Passed。
- 为通过测试而把生产实现复制进测试oracle，或只断言函数/文件存在。
- 一次性“大爆炸”替换现有引擎、无适配器双写、无回放比较即删除旧路径。
- 未更新Approved规格就静默改变公式、字段、房规、随机域、事件顺序或兼容格式。

## 17. 关联文档

- [总实现规范](../AI_implementation_spec_v3.md)
- [锁定单元目录](../02-unit-catalog/locked_unit_catalog.md)
- [96单元测试规格](../05-test-spec/README.md)
- [开发任务卡](development_task_cards.md)
- [迁移计划](migration_plan.md)
# 3.0.1 Python兼容路径规则（规范补丁）

任务卡中的代码位置是逻辑模块建议，不得覆盖语言导入规则。若仓库已存在`engine/rules.py`、`engine/state.py`、`engine/audit.py`、`engine/score.py`等同名模块，禁止同时创建会遮蔽它的同名package。实施者必须优先在现有模块增加稳定单元入口，或先通过Approved ADR完成一次性package迁移；代码证据记录逻辑建议路径到实际符号的映射。未获ADR批准不得以满足建议路径为由破坏既有import。
