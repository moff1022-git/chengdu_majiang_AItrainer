# 成都麻将 AI 训练模拟器 Spec v3 来源清单

| 字段 | 内容 |
|---|---|
| 文档 ID | SV3-DOC-SOURCE-INVENTORY-001 |
| 状态 | Baseline |
| 日期 | 2026-07-29 |
| 适用规则 | `docs/spec-v3/WORKING_RULES.md` RULE-001～RULE-008 |
| 范围 | 来源登记、版本关系、证据分级、术语与后续依赖；不重新判定 96 个单元边界 |

## 1. 技术摘要

本轮要求的七类输入均已检查。两份锁定源文档、96 项审计 Markdown、canonical JSON、HTML 报告、F0028-2～F0030 验收记录、生产源码、测试、配置和仓库内日志均存在。全部权威输入文件见 `authoritative_file_manifest.md`，日志 corpus 见 `log_file_manifest.md`。

当前存在四项关键证据限制：未找到独立 JSON Schema；未找到 coverage/htmlcov 覆盖率产物；历史验收引用的 `/tmp/f0028_*` 临时证据不在当前仓库；Windows `.venv` 指向不存在的 Python 3.12，当前无法复跑 pytest。因此历史 `358 passed` 只能登记为验收报告中的既有运行声明，不能当作本轮复验结果。

原审计的 96 行仅作为 legacy audit rows 登记，不预设它们已经原子化、边界正确或应永久保持 96 个。后续必须从锁定条款重新建立稳定单元和原子断言，再把 legacy rows 映射进去。

## 2. 输入清单

### 2.1 锁定源文档

| 输入 ID | 路径 | 内含版本 | 字节数 | SHA-256 | 状态 |
|---|---|---|---:|---|---|
| SRC-LOCK-001 | `成都麻将AI人类化决策规则_v1.md` | RULES 1.0.0 / PARAMS 1.0.0；已锁定 | 123638 | `6cbb4d4465abfd947b6cf7f1783db99408089d4e1646849a3afe674114267992` | 可读；禁止修改 |
| SRC-LOCK-002 | `成都麻将AI训练模拟器程序实现规范_v2.0.0.md` | IMPL 2.0.0；依赖 RULES 1.0.0 / PARAMS 1.0.0 | 35292 | `9bc4d4ea5278e09ae34a1efb5edfb3cbc295752ecf6b3ebe89b348210d670135` | 可读；禁止修改 |

`SRC-LOCK-002` 正文记录的 `SRC-LOCK-001` SHA-256 与本轮实测一致。两份文档已完整读取用于目录、版本、参数注册表和冲突裁决登记；本轮未改写。

### 2.2 96 项审计与验收证据

| 输入 ID | 路径 | 版本/日期 | SHA-256 | 证据用途与限制 |
|---|---|---|---|---|
| SRC-AUD-001 | `docs/status/SPEC_IMPLEMENTATION_AUDIT_2026-07-29.md` | 2026-07-29；APP 0.2.1 / state 5 / PlayerView 2 / PARAMS 1.1 / IMPL 2.1 | `fe6cb6851b8ef69572f87fe86ab446e1f37167a8ccbDD81f6493b13d8224cd6b` | 96 legacy rows、33/61/2 审计结论；边界不视为权威 |
| SRC-AUD-002 | `docs/status/spec_audit_artifact.json` | canonical audit artifact，2026-07-29 | `811a75b1d91bbbd5cb82e9ad12eb3ee0284d09fbe76363c69bbcb7d3c6713505` | 机器可读审计载荷；仍继承 legacy row 边界 |
| SRC-AUD-003 | `docs/status/SPEC_IMPLEMENTATION_AUDIT_2026-07-29.html` | 自包含 HTML，2026-07-29 | 见 `authoritative_file_manifest.md` | 展示产物；结构验证不等于代码实现验证 |
| SRC-AUD-004 | `docs/status/F0031_F0032_QUANTIFICATION_REVIEW_2026-07-29.md` | Needs revision | 见 `authoritative_file_manifest.md` | 明确 96 行无稳定 ID、未完全原子化、无逐项 crosswalk |
| SRC-ACC-001 | `docs/status/F0028_2_ACCEPTANCE_2026-07-28.md` | F0028-2 Done | 见 `authoritative_file_manifest.md` | 实体牌 / PlayerView v2 验收声明 |
| SRC-ACC-002 | `docs/status/F0028_3_ACCEPTANCE_2026-07-29.md` | F0028-3 Done | 见 `authoritative_file_manifest.md` | 确定性 PlayerView 策略验收声明 |
| SRC-ACC-003 | `docs/status/F0028_3_MANUAL_QUICK_ACCEPTANCE_2026-07-29.md` | 快速人工验收 | 见 `authoritative_file_manifest.md` | GUI 快速证据；不能替代策略效果评估 |
| SRC-ACC-004 | `docs/status/F0028_4_ACCEPTANCE_2026-07-29.md` | F0028-4 Done | 见 `authoritative_file_manifest.md` | 有限认知验收声明；临时批跑不在仓库 |
| SRC-ACC-005 | `docs/status/F0028_5_ACCEPTANCE_2026-07-29.md` | F0028-5 Done | 见 `authoritative_file_manifest.md` | Audit v1 / replay 验收；临时原始证据不在仓库 |
| SRC-ACC-006 | `docs/status/F0028_6_ACCEPTANCE_2026-07-29.md` | F0028-6 Done | 见 `authoritative_file_manifest.md` | 训练契约 v2 验收声明 |
| SRC-ACC-007 | `docs/status/F0029_ACCEPTANCE_2026-07-29.md` | F0029 Done | 见 `authoritative_file_manifest.md` | GUI / 配置编辑验收声明 |
| SRC-ACC-008 | `docs/status/F0030_ACCEPTANCE_2026-07-29.md` | F0030 Done | 见 `authoritative_file_manifest.md` | PARAMS 1.1 / IMPL 2.1 迁移验收声明 |

注：`SRC-AUD-001` 的哈希统一以小写读取；表内任何大小写差异不改变 SHA-256 值。完整逐文件哈希以附件清单为准。

### 2.3 源码、测试、配置与 Schema

| 输入 ID | 范围 | 本轮发现 | 登记方式 |
|---|---|---|---|
| SRC-CODE-ENGINE | `engine/**/*.py` | 30 个 Python 文件；规则、状态、计分、审计与会话 | 逐文件见 `authoritative_file_manifest.md` |
| SRC-CODE-PLAYERS | `players/**/*.py` | 46 个 Python 文件；含 `players/humanlike/` | 逐文件见附件 |
| SRC-CODE-PROTOCOLS | `protocols/**/*.py` | 8 个 Python 文件；wire / PlayerView | 逐文件见附件 |
| SRC-CODE-TRAINING | `training/**/*.py` | 10 个 Python 文件；env / codec / observation / reward / oracle | 逐文件见附件 |
| SRC-CODE-DISPLAY | `display/**/*.py` | 21 个 Python 文件；仅作为产品接口和 GUI 证据候选 | 逐文件见附件 |
| SRC-CODE-TOOLS | `tools/**`、`packaging/**` | 工具及打包脚本存在 | 逐文件见附件 |
| SRC-TEST | `tests/**/*.py` | 61 个 Python 文件；静态发现 344 个 `test_*` 定义 | 逐文件见附件；名称本身不构成实现证据 |
| SRC-CONFIG | `configs/**` | 9 个配置文件 | 逐文件见附件；关键哈希见 2.4 |
| SRC-SCHEMA | 独立 JSON Schema | 未找到 | Schema 目前由代码常量、dataclass、validator 和迁移函数表达 |

生产能力的后续证据必须精确到符号。例如版本/Schema 候选锚点包括：

- `version.py::APP_VERSION`；
- `engine/state.py::SCHEMA_VERSION`、`GameState.from_dict`；
- `engine/persistence.py::FORMAT_VERSION`；
- `protocols/wire.py::PROTOCOL_VERSION`；
- `protocols/player_view_v2.py::PLAYER_VIEW_VERSION`；
- `players/humanlike/config.py::RULE_VERSION`、`PARAMETER_VERSION`、`IMPLEMENTATION_VERSION`、配置 validator；
- `training/action_codec_v2.py::ACTION_SPACE_SIZE`。

这些符号只证明版本声明或候选实现位置。是否满足某一功能，必须继续检查函数逻辑、直接测试断言和运行结果。

### 2.4 配置文件

| 路径 | SHA-256 |
|---|---|
| `configs/crash_policy.json` | `409f9be36c65225858e321174f9ad5e4774bce1ef85404852282a862a28c7dbb` |
| `configs/f0010_eval_sets.json` | `a31d87b0d6a41500485caa95c286b968cadc1494c312db8adecf74057868108d` |
| `configs/fan_table.json` | `f11d07119d5cd4801af86a5e30f8ec86453ee0331664bd5472fd2dbddc9a02b6` |
| `configs/humanlike_v2/compatibility.json` | `bd484e38bbfde715fe32dd49d0e2571bf35d524a72be56a092e70385811ddee7` |
| `configs/humanlike_v2/default.json` | `b7d5dde49ea260185f89ef786da8c8761942e68f88539fc2bac84909c1068546` |
| `configs/reward_default.json` | `fdace014d9999cb8ef664e9a815024ef23e3f142fad5c618eba7e852a9c2c2eb` |
| `configs/score_default.json` | `1c1374b299dd27e4338dbc72a932f1c97df9f05daa6294a615b1bb7e94b0b855` |
| `configs/strategies/current_s2.json` | `1976d6275c0aa2a2cf83994eaf7b385517b11cc22dc6e911bf4b4ecf9dd2fc3b` |
| `configs/strategies/presets.json` | `78eb902cf582695c07bd578d5b9c43176bf7acD610abf2e465ddb16ef61371f6` |

### 2.5 运行、覆盖率与审计证据

| 输入 ID | 路径/范围 | 发现 | 证据限制 |
|---|---|---|---|
| SRC-RUN-LOGS | `logs/` | 1,827 文件，327,357,125 字节；完整 tree hash 见 `log_file_manifest.md` | 大部分为 F0010 predict 与 GUI stderr；尚未逐条映射到新单元 |
| SRC-RUN-PYTEST-CACHE | `.pytest_cache/v/cache/nodeids` | 存在；SHA-256 `c33d66b863dccb2e536af2aa1a49f0f10b0138aab684292155bbe323b560a299` | cache 不是通过证明；`lastfailed` 仍含两个历史条目 |
| SRC-RUN-COVERAGE | `coverage/`、`htmlcov/`、`.coverage` | 未找到 | 不能给出当前行/分支覆盖率 |
| SRC-RUN-TMP | 验收引用的 `/tmp/f0028_*` | 当前仓库未找到 | 不能跨机复核原始批跑与性能文件 |
| SRC-RUN-AUDIT | Audit v1 生产代码与验收报告 | 文件存在；见 `engine/audit.py`、`tests/humanlike_v2/test_audit_replay.py`、SRC-ACC-005 | 当前未发现仓库内 F0028-5 原始 audit 批跑 corpus |
| SRC-RUN-CURRENT | 本轮 pytest | 未运行 | Windows `.venv` 解释器路径失效，不能把 358 passed 视为本轮复验 |

## 3. 版本关系

| 层 | 锁定/规范版本 | 当前代码声明 | 关系与限制 |
|---|---|---|---|
| 决策规则 | CDMJ-AI-RULES 1.0.0 | `players/humanlike/config.py::RULE_VERSION = 1.0.0` | 一致 |
| 参数规范 | CDMJ-AI-PARAMS 1.0.0 | `PARAMETER_VERSION = 1.1.0` | 代码已因 F0030 演进；锁定源文档不回写 |
| 实现规范 | CDMJ-AI-IMPL 2.0.0 | `IMPLEMENTATION_VERSION = 2.1.0` | 代码已因 F0030 演进；后续须显式记录差异 |
| 应用 | 未在锁定源文档定义 SemVer | `version.py::APP_VERSION = 0.2.1` | 独立版本线 |
| GameState | 规范描述领域模型 | `engine/state.py::SCHEMA_VERSION = 5` | reader 1～5；代码内 Schema |
| persistence | 未与应用 SemVer 合并 | `engine/persistence.py::FORMAT_VERSION = 1` | 独立版本线 |
| wire | 接口规范概念 | `protocols/wire.py::PROTOCOL_VERSION = 1` | legacy wire 线 |
| PlayerView | 规范要求信息隔离 | `protocols/player_view_v2.py::PLAYER_VIEW_VERSION = 2` | 强类型 v2；wire 仍为 v1 |
| action codec | 规范要求固定训练动作 | `training/action_codec_v2.py::ACTION_SPACE_SIZE = 635` | codec v2，635 项 |

版本冲突不能静默消解。新单元必须同时记录 `source_version` 和 `observed_implementation_version`，并把版本迁移作为独立断言，而不是改写锁定来源。

## 4. 缺失输入和阻塞项

| 阻塞 ID | 状态 | 缺失/问题 | 影响 | 后续解除条件 |
|---|---|---|---|---|
| BLK-001 | Blocked | 独立机器可读 Schema 未找到 | 不能仅靠 schema 文件验证 state/config/view/action 契约 | 从代码符号提取并评审 Schema，或后续经授权新增 schema 文档/文件 |
| BLK-002 | Blocked | coverage、htmlcov、`.coverage` 未找到 | 无法声明行/分支覆盖率 | 在可用环境执行覆盖率并保存产物 |
| BLK-003 | Blocked | F0028 验收引用的 `/tmp` 原始证据未入库 | 性能、批跑和 replay 原始记录不可跨机复核 | 重跑并把脱敏 manifest/摘要写入仓库证据目录 |
| BLK-004 | Blocked | Windows `.venv` 无可用解释器 | 本轮不能执行 pytest 或验证运行时版本 | 恢复 Python 3.12 环境后复跑 |
| BLK-005 | Open | 96 legacy rows 没有稳定、完全原子化边界 | 不能直接沿用为 v3 单元 | 从源条款重切单元并做 many-to-many crosswalk |
| BLK-006 | Open | 真人数据 release、授权和 Data Card 未找到 | 真人相似度只能 Not Evaluated | 合规数据来源、去标识、冻结 split 和验证报告 |
| BLK-007 | Open | F0032 schema/validator/golden release 未找到 | 无法执行逐单位量化 | 后续文档批准并明确授权实现后建立 |
| BLK-008 | Open | HTML 审计缺少 Chromium 浏览器 QA | 交互/窄屏呈现未验证 | 有浏览器环境时重新验证；不影响 Markdown 内容登记 |

## 5. 统一术语

| 术语 | 统一定义 |
|---|---|
| 锁定来源 | RULE-001 指定的两份根目录 Markdown；只读，不随实现演进回写 |
| legacy audit row | 2026-07-29 审计报告中的一行评价；不是默认原子单元 |
| 功能单元 | v3 中具有单一主要职责、稳定 ID、明确输入/输出和独立判定边界的规格对象 |
| 原子断言 | 功能单元内可单独 Passed / Failed / Not Evaluated / N/A-with-approval 的最小要求 |
| 实现锚点 | 生产文件路径加符号名称；只说明候选代码位置 |
| 直接测试 | 已检查断言内容、能直接触发原子断言行为的测试；名称本身不是证据 |
| 运行证据 | 保存命令、环境、输入版本、结果和产物哈希的可复核执行记录 |
| 确定性规则 | 成都房规或产品规则规定的权威状态转移与合法性 |
| 确定性算法 | 相同输入和版本下输出相同的工程计算；不自动等同房规 |
| 人类化启发式 | 人工设计的有限认知、风格、风险或近似决策机制 |
| 可训练模型 | 参数由数据/优化过程学习，并具有训练、冻结、评估和版本契约的模型 |
| Not Evaluated | 已定义要求，但证据或数据不足，不能判定通过/失败 |
| 未找到 | 在声明的搜索范围内没有发现所需证据；不得改写为“可能已实现” |

## 6. 单元 ID 规范

96 不是 v3 单元数量约束。v3 使用与章节、文件位置和实现模块解耦的单调稳定 ID：

- 功能单元：`SV3-U0001`、`SV3-U0002`……；分配后不复用、不重排。
- 原子断言：`SV3-U0001-A01`、`SV3-U0001-A02`……。
- 证据：`SV3-EV-000001`……。
- 决策/歧义：`SV3-DEC-0001`……。
- 缺口：`SV3-GAP-0001`……。

领域、阶段和方法类型作为字段记录，不编码进稳定 ID，避免分类变化导致改号。每个单元必须提供到锁定条款、legacy audit rows、实现锚点、测试/运行证据的 many-to-many 映射。废弃单元保留 ID 并标记 `Deprecated`，不得删除后复用。

每个原子断言必须选择一种 `method_class`：`deterministic_rule`、`deterministic_algorithm`、`humanlike_heuristic`、`trainable_model`。跨类复合要求必须拆分。

## 7. 证据等级

spec-v3正式验收只使用`E0—E5`，语义与[审计与验收标准](../06-audit-acceptance/audit_standard.md)完全相同：

| 等级 | 名称 | 最低要求 | 可支持的结论 |
|---|---|---|---|
| E0 | 无证据 | 无可核查产物，或只有声明/TODO/占位 | 仅记录待办 |
| E1 | 规格证据 | Locked目录、Approved单元规格和Approved父测试合同均存在 | 需求与验收目标已冻结 |
| E2 | 静态实现证据 | E1 + 非占位生产符号、实际调用链和参数/状态/追踪绑定 | 代码结构与绑定可审查 |
| E3 | 直接自动测试证据 | E2 + 当前受控环境直接测试通过并保留输入输出/hash | 单元行为在直接测试范围内通过 |
| E4 | 集成运行证据 | E3 + 生产完整流程调用、写回、日志、回放、性能和隐藏隔离证据 | 可支持AUDITED候选结论 |
| E5 | 独立/外部与发布证据 | E4 + 冻结数据、独立复核和适用发布/外部效果证据 | 可支持限定范围的发布或外部效果声明 |

证据还必须标记新鲜度：`current-run`、`retained-artifact`、`report-only`、`stale-cache`。历史验收报告中的通过数字若原始产物未保留，最高标为 `report-only`，不能冒充本轮 E3/E4。

旧实现审计矩阵中的`EV0—EV5`仅保留在显式命名的`legacy_evidence_level`字段，不是正式验收等级，也不能直接比较。一次性保守迁移规则为：`EV0→E0`；`EV1→E0`；`EV2→E2`仅在当前E1前置和静态证据重新核验后成立，否则最高E1；`EV3/EV4/EV5`必须按E1→目标等级的累计条件重验，只有`report-only`时最高E2。不得仅去掉字母`V`完成升级。

单元状态采用 `Passed`、`Failed`、`Not Evaluated`、`N/A-with-approval`。hard 断言不允许用平均分抵消，也不得未经批准标记 N/A。

## 8. 后续任务依赖关系

| 顺序 | 任务 | 输入依赖 | 产出 | 解锁对象 |
|---:|---|---|---|---|
| 1 | 来源条款原子化 | SRC-LOCK-001/002、本清单 | 锁定条款 catalog；不沿用 96 边界假设 | 单元划分 |
| 2 | legacy 审计拆解 | SRC-AUD-001/002、条款 catalog | legacy row → 原子条款 many-to-many crosswalk | gap 重评 |
| 3 | 建立 v3 单元目录 | 前两步、单元 ID 规范 | `SV3-Uxxxx` catalog、owner、method class | 单元规格编写 |
| 4 | 编写单元规格 | 单元 catalog、统一模板 | `03-unit-specs/` 单元文档 | 开发与测试指导 |
| 5 | 代码/测试证据审计 | 权威文件清单、单元断言 | 路径 + 符号 + 断言 + 运行证据矩阵 | 当前实现判定 |
| 6 | 缺口与开发指导 | 单元判定、版本差异 | `01-audit-gap/`、`04-development-guide/` | 后续经授权实现 |
| 7 | 测试与验收规格 | 单元断言、证据等级 | `05-test-spec/`、`06-audit-acceptance/` | 可执行验收 |
| 8 | 全链追踪与复核 | 上述全部产物 | `07-traceability/`、`08-review/` | v3 Approved 候选 |

当前阶段不解锁程序实现。任何代码修改必须由具体任务明确授权，并继续遵守 Docs-First。

## 9. 方法与完整性检查

- 读取：两份锁定源文档、96 项审计、canonical artifact、验收与量化审查。
- 枚举：生产源码、测试、配置、工具/打包定义及日志 corpus。
- 身份：逐文件 SHA-256 或明确记录的目录 tree SHA-256。
- 限制：不把文件名、类、接口、占位函数或测试名当实现证据。
- 变更保护：本轮结束时重新计算两份锁定文档哈希，并与 2.1 比较。

## 10. 后续问题

1. legacy 96 rows 拆分后实际会形成多少个原子断言？当前未确定，不应预设为 96。
2. PARAMS 1.1 / IMPL 2.1 与锁定 1.0 / 2.0 的每项兼容差异如何映射到 v3 单元？
3. 哪些历史验收需要重跑以达到 E3/E4，而不是仅保留 report-only？
4. 独立 Schema 应以 Markdown 字段表、JSON Schema 还是代码生成形式交付？当前阶段只记录问题，不新增程序 Schema。
