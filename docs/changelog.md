# Changelog

## 2026-08-03 — 清理本仓 C1 采集数据

- 会话产生的视频/标注图/难度报告已迁至 `chengdumajiang_vision_capturer`，**本仓不再保留**该数据集与 research 目录。
- 仅保留 F0038 方案文档（无媒体资产）。


## 2026-08-03 — C1 训练：Mac 可运行性检查

- 新增 `docs/research/c1_video_capture_difficulty/MAC_RUNTIME.md`：欢乐麻将/JJ/人人/微信小游戏/禅游渠道在 macOS 的运行路径与 C1 采集建议。


## 2026-08-03 — 补禅游/血战真实帧并修正难度结论

- 补全「微信小游戏/禅游血战」线索真实截图标注 ≥10 张（熊猫川麻竖屏 + 血战麻将横屏）。
- 明确撤回无图断言「微信小游戏最简单」；C1 首发以真机录屏或 C2 合成为准。


## 2026-08-03 — C1 真实视频截图标注

- 从公开 YouTube/B 站实玩视频抽帧，每类 ≥10 张并标注手牌/弃牌河/副露难易 ROI。
- 见 `docs/research/c1_video_capture_difficulty/frames/annotated/` 与 REPORT 附录 A。
- 原始 mp4 不入库（gitignore）。


## 2026-08-03 — C1 公开视频画面采集难度报告

- 新增独立调研 [`docs/research/c1_video_capture_difficulty/REPORT.md`](research/c1_video_capture_difficulty/REPORT.md)：分游戏检索公开实玩视频、C1 采集难度评分、难易标注图与视频清单。
- 结论摘要：微信川麻血战类相对适合作 C1 MVP；欢乐/JJ 3D 更难；客户端不明视频仅作噪声集。

## 2026-08-03 — F0038 方案 C1 主路径细化

- 用户判定 **C0 整副手录无实操性**；方案 C **初步主路径改为 C1**（区域截图+视觉识别）。
- [`F0038`](features/F0038_online_platform_ai_bridge.md) 新增 **§4.4.11**：Layout Profile、截帧/动画门控、检测+分类、手牌/河差分/副露解析、置信降级、模块目录、M0–M6 交付与 4–7 周工作量；C0 仅点状纠错。
- **无业务代码**。

## 2026-08-03 — F0038 方案 C 观测采集补充

- [`F0038`](features/F0038_online_platform_ai_bridge.md) §4.4 扩充：对手弃牌 / 副露 / 自家手牌的采集通道、`CoachObservation`、架构与实施步骤；仍禁止逆向/代打。
- **无业务代码**。

## 2026-08-03 — F0038 线上平台 AI 接入方案（Draft）

- 新增 [`docs/features/F0038_online_platform_ai_bridge.md`](features/F0038_online_platform_ai_bridge.md)：主流川麻/血战线上平台调研；方案 A 自建房 / B 官方合作 / C 教练 HUD；禁止逆向与 RPA 挂机；与 `BasePlayer`/Humanlike v2 映射及分阶段路线。
- **无业务代码**；待用户确认主路径后再开实现规格。

## 2026-08-03 — v0.3.1 首页与 macOS 打包修复

- GitHub 首页按 v0.3.1 当前功能整体重写，增加 macOS arm64 PyInstaller/Nuitka 包及 SHA-256 清单的直接下载入口。
- PyInstaller、Nuitka 构建脚本和可选 spec 永久补收 Humanlike 参数注册表。
- 构建脚本增加 App Bundle、assets、configs、参数注册表与 CLI 冒烟强制门禁；缺失时不再静默成功。
- 定向验证：`tests/test_app_paths.py` 7 passed；两个已发布 App 的版本、座位窗口和资源检查均通过。

## 0.3.1 — 2026-08-02

- 新增 M21 Humanlike 提升计划草案：基于 Task 19 96 单元状态与《成都麻将AI人类化决策规则_v1.md》建立偏差分类、验收门禁和优化任务队列；仅文档变更。
- M21 执行启动：保存执行约束，完成全量项目备份和 Task 19 主矩阵只读盘点；未修改业务代码。
- M21 自动执行继续：完成四维状态模型和代码/测试/证据缺口扫描；按保守门禁未将任何单元升级为 DONE，未修改业务代码。
- M21 自动执行：完成文档引用与规则测试映射扫描；全仓测试发现 500 passed、1 skipped、2 个已登记 finding，未绕过失败或修改业务代码。

- 修复人类推荐算法设置窗口：`humanlike_v2` 模式显示四座位 13 种人格预设，并支持应用、保存及下局生效。
- 保持 Humanlike 配置根字段兼容；推荐算法选择独立保存于配置旁车文件，避免破坏严格配置校验。
- 0.3.1 发布范围明确：包含 0.3.0 之后的引擎、UI、Humanlike v2、人格预设、推荐算法和相关规则修复；不包含牌局生成工具、性能测试工具、其专属测试脚本及生成数据。
- 生成 `releases/v0.3.1/` 本地完整源代码归档；排除虚拟环境、运行数据、日志、缓存和构建产物。

## 2026-08-02 — F0038 固定回放缺陷修复

- F0043: 新增人类推荐算法模式设计（Review）；目标是移除 strategy/F0011 入口，改由 humanlike_v2、humanlike_v2.ruleai、humanlike_v2.ruleai_plus 和 13 种人格预设驱动。当前仅更新规格，未修改业务代码。
- F0043: 需求修正为移除 `HumanPlayerProxy` 内置推荐算法，默认使用 `rule_ai`，由持久化设置值选择算法并在下一次 discard 请求生效；本轮仅更新规格。

- 修复固定牌局错误的四座各 13 张/剩余墙 56 张合同，改为庄家 14、闲家 13、剩余墙 55，并按权威发牌顺序生成。
- 固定回放将牌面数据稳定映射到唯一物理牌，满足 0–107 `tile_id` 所有权守恒；真实 humanlike_v2 单局回放正常结束且四座均产生决策。
- 能力测试报告区分尝试/成功/失败，新增 `FAILED`/`PARTIAL` 与失败原因，避免全失败数据被报告为已完成；移除重复校验码。
- 删除不兼容旧固定数据集 `data/fairness/fairness-20260802-independent-004`（约 67 MB）；未删除其他编号。
- 清理 `data/fairness` 下此前全部旧编号（independent-001/002/003），并重新生成 `fairness-20260802-random-001` 与 `fairness-20260802-fair-001` 两套完整 10000 局数据。
- 完成 random/fair 两套新数据集的 50–10000 局公平性复核：全部硬约束和统计状态 PASS；fair 模式座位初始牌总量严格平衡，random 模式差异符合庄家第 14 张的规则预期。
- 审查发现 fair 模式尚未实现 F0038 约定的窗口配额/候选选择和逐局审计字段；已记录为实现缺口，不能将当前 `fairness-20260802-fair-001` 宣称为完整公平模式证据。
- 修复 fair 模式：加入 100 局窗口四座 25 局庄家配额校验、候选/选择元数据、seed 坐标、wall SHA-256 和手牌统计；删除旧 fair/random 数据并重建 `fairness-20260802-random-002`、`fairness-20260802-fair-002`。两套数据 50–10000 局公平性复核全部 PASS。
- F0038 fair-v3: 真正实现每局 16 候选牌墙的确定性花色平衡评分选择，删除 -002 数据并重建 `fairness-20260802-random-003`、`fairness-20260802-fair-003`；全部规模公平性 PASS，fair 模式花色 effect size 显著下降。
- 按用户要求删除全部旧牌局集并最终重建 `fairness-20260802-random-004`、`fairness-20260802-fair-004`；两套 50–10000 局公平性复核全部 PASS，fair 窗口配额全部通过。
- 分析 1000 局 fair-004：nonhuman s0 胜率 31.70%、总分 -277，明显低于 novice s1/s3；s0 平均响应 189.9ms，其他座位约 62ms。公平性指标 PASS，问题定位为 nonhuman 策略参数/搜索实现未转化为更高牌局收益，非发牌偏差。

## 2026-08-02 — F0038 生成模式设计（待确认）

- 设计生成器交互式/CLI `fair` 公平模式与 `random` 随机模式；模式、约束版本和候选选择索引纳入 manifest、报告和校验码。
- 公平模式采用确定性庄家轮换与窗口配额约束，禁止按 AI 结果事后筛选；规格状态调整为 `Review`，尚未修改业务代码。
- F0038: 实现 `--mode fair|random` 及启动后交互选择；模式、约束版本写入每局记录和 manifest。公平模式固定按局号轮换庄家，随机模式按模式绑定 seed 洗牌；两种模式均完成 10000 局 CLI 验收。

## 2026-08-01 — MODEL-001 F0035 工程门禁

- 新增独立数据集 validator，覆盖模拟数据准入、feature/label 隔离、分组泄漏检查、正式 provenance 门禁和文件 SHA-256 记录。
- MODEL-001 模拟数据 10,595 条校验通过；外部有效性仍为 `NOT_EVALUATED`，不改变 `INTEGRATED` 状态。

## 2026-08-01 — Task 19 权威状态同步

- 将 integration worktree revision 14 tracker、orchestrator state 和 agent runtime 同步到主目录，两者现在均为 `41/96 AUDITED`。
- 保留 T02 人工门禁：性能 workload 语义未自动选择，未降低标准或改变权威语义。

## 2026-08-01 — Task 19 M02 独立审计收口

- MODEL-004 独立 clean-archive 审计 PASS：`0 P0/0 P1/0 P2`，定向 `70 passed`，全量 `776 passed, 1 skipped`，更新 Task 19 为 `41/96 AUDITED`。
- T02 保持 ADR-0001 人工门禁：不自动选择性能 workload 语义，不降低门禁，不改变权威 legal/view/hash 语义。

## 2026-08-01 — Task 19 W04 D05/D12/D14 审计收口

- D05 最终 clean-archive 审计 PASS：RULE-007/008/012 达成真实 PONG/MING_GANG transition exactly-once、legacy golden、E4/E5/AC 门禁，更新为 AUDITED。
- D12/D14 修复后 clean-archive 审计 PASS：ALGO-008/STATE-007/STATE-012 更新为 AUDITED。W04 累计 `40/96 AUDITED`。
- T02 实际环境性能标准与批准 contract-transition workload 存在语义冲突，已按 ADR-0001 进入唯一人工门禁，暂停修复，不降标或改变权威语义。

## 2026-08-01 — Task 19 CLI 重启后自动续跑设计

- 将 F0034 调整为会话内 Root Orchestrator + CLI 重启后 Startup Reconciler；CLI 关闭期间任务暂停，重启后无需再输入“继续 Task 19”。
- 增加仓库状态恢复顺序、幂等键和人工门禁跨 session 保留规则。
- 明确排除 `launchd`、Windows Task Scheduler、常驻守护进程和其他外臨自动唤醒程序；未修改 Task 19 业务代码或审计门禁。
- 新增 `reconcile-startup` 只读恢复入口，自动选择权威 integration worktree 并输出幂等续派队列；`AGENTS.md` 要求 Task 19 新 session 在读取基线后立即执行。调度/runtime 专项 `18 passed`。

## 2026-08-01（Task 19 监控器多工作区修复）

- 监控器自动发现 Git worktree 并选择最先进的有效 Task 19 tracker；同状态时优先 integration 分支，避免主工作区或 detached 审计副本覆盖实时进度。
- 新增 `--workspace`、source/branch/HEAD/tracker/runtime 元数据、候选源摘要和 runtime fallback/lag 标志。
- 过期 runtime 中的 RUNNING 现在投影为 STALE；14 项监控/runtime 测试通过，实际显示从主工作区 `15/96` 修正为 integration `27/96`。

## 2026-07-31（Codex CLI 无人值守配置与重启检查点）

- 新增项目级 `.codex/config.toml`：`on-request + auto_review + workspace-write`，仅对已信任的本仓库生效，允许工作区/`/private/tmp` 写入与 workspace-write 网络访问。
- 已将 B2-A1 commit `259b3e1` 独立 clean-archive 终审 PASS 和 CLI 重启后恢复顺序固化到 `LATEST.md`；重启后先集成 B2-A1，再完成 D10/W01，然后继续 W02–W14。

## 2026-07-31（Task 19 平台与不可逆操作扩展授权）

- 项目所有者授权 Task 19 必需的平台强制权限、Git/外部不可逆操作按自动同意处理，不再对话式二次询问。
- 平台强制弹窗不能被仓库授权绕过；Root 直接发起请求，并用 `confirm-open/confirm-close` 在监控器中标记挂起状态。
- 授权不扩大 Task 19 范围；push、发布、删除、tag 移动和历史重写仅在完成任务必需、目标精确且最小范围时执行。

## 2026-07-31（Task 19 动态进度监控）

- 用户明确授权实现长时间无人值守任务的动态状态程序，`task19_progress_tool_design.md` 的只读监控范围升为 Approved；可写 `apply-delta` 仍未授权。
- 新增 `tools/task19_monitor.py`：动态显示 14 wave / 40 batch / 96 unit 的已完成、进行中、未开始、累计时间和 tracker 新鲜度；支持 `--once`、`--json`、`--interval`和 `--started-at`。
- 新增 `tests/test_task19_monitor.py`；3 项测试通过，验证 14/40/96 覆盖、状态投影与时长格式。
- 监控器增加 Agent 面板，从 `docs/status/task19_agent_runtime.json` 显示运行/完成/中断/过期状态、当前工作、已运行时间和心跳年龄；`RUNNING` 心跳超过 60 秒自动投影为 `STALE`。
- Agent 面板增加 `requires_human_confirmation` 和原因；顶部汇总待人工确认数，当前为 0。只有 Orchestrator 明确登记的真实门禁才显示 YES，过期/中断不自动误报。
- 监控器增加总体、W01–W14 和 40 个 batch 的 evidence-gate 进度百分比，按所属单元 tracker `progress` 等权平均；当前权威快照显示总体 21.61%、W01 13.75%。
- 交互终端增加 ANSI 状态颜色：需要人工确认红色、运行中蓝色、已完成绿色、待运行白色；中断/过期红色。非 TTY、JSON 和 `NO_COLOR` 保持无颜色文本。
- 修正 Root 误显示 `STALE`：Agent 状态保留 Orchestrator 最后明确登记的 `RUNNING`，心跳超过 60 秒另行显示红色 `HEARTBEAT STALE` 警告，不再用快照新鲜度覆盖 Agent 状态。
- 修复 Agent 列表不完整：补入遗漏的嵌套 `stage5_review`，当前快照 4 个 Agent 与会话 API 一致；面板增加 `Registered agents` 和 `Agent snapshot age`。
- Agent 状态增加 `WAITING` 黄色，表示已创建但等待依赖/任务/资源/调度；与白色 `NOT_STARTED` 明确区分。
- 新增 `tools/task19_agent_runtime.py` Orchestrator 钩子：`sync` 原子替换完整 Agent 树，`upsert` 记录单 Agent 生命周期且不丢失其他条目，`heartbeat` 刷新 Root。新增 3 项专用测试，与监控器合计 `8 passed`。
- 修复平台授权弹窗不更新监控状态：增加 `confirm-open/confirm-close` 生命周期钩子，强制在发起权限请求前置红色 `confirm=YES`，请求结束后清除。端到端开/关模拟通过，Agent 同步+监控合计 `11 passed`。

## 2026-07-31（W01 无人值守闭环阶段结果）

- MODEL-001 R4、TRAIN-009、RULE-015 和 AUDIT-010 已分别完成独立复审 PASS；设计批准线仍不自动宣称业务实现/AUDITED。
- B2-A1 `0327f32` 在测试全绿下被独立审计判 FAIL：生产权威路由不完整、outbox/副露合同缺口、E4 占位/过期 hash 和 E5 AC 外键不全。修复检查点 `9fdd945` 已关闭 claimed-tile 与 outbox 两项 P1；剩余需以 STATE-004 最终提交事件重建完整权威路由和真实 E4/E5。

## 2026-07-31（Task 19 统一持续授权）

- 项目所有者指令“统一授权，后续授权均自动同意，不要再询问”；自此 Task 19 范围内的实现、修复、测试、复审、独立审计、推荐语义选择、共享路径接线、scoped commit、集成和状态回写默认自动同意。详见 `docs/status/TASK19_STANDING_AUTORIZATION_2026-07-31.md`。
- 统一授权不降低 Locked/Frozen、AC/E4/E5 或独立审计门禁，不替代系统强制的外部权限；外部 push/发布、删除、历史重写或凭据操作默认跳过而不阻塞其他工作。

## 2026-07-31（W01 合并所有者硬门禁批准）

- 项目所有者批准 RULE-015 向量 `A,A,A,A,A,A,A,A,A,A,A,B`、AUDIT-010 向量 `A,A,A,A,A`，并临时授权 Orchestrator 修改 B2-A1 已批验收所必需的共享生产路径和新增专用集成测试。详见 `docs/status/TASK19_W01_MERGED_OWNER_GATE_2026-07-31.md`。
- 授权不包含修改既有测试断言、Locked/Frozen、push、发布、删除或将设计批准直接升级为 AUDITED；W01 无人值守闭环已恢复。

## 2026-07-31（ADR-0001 批准与 W01 无人值守试运行）

- 项目所有者批准 ADR-0001，状态由 Proposed 更新为 Accepted；实际并行调度 MODEL-001 独立审计、B2-A1 闭环和 W01 设计复核/机械修订。
- MODEL-001 R3 虽全仓 490 passed / 1 skipped，独立审计仍因 `private memory` 边界绕过和 manifest 合同违反判 FAIL；B2-A1 63 项测试通过但因共享生产路径所有权与 42 AC 缺口停在硬门禁；TRAIN-009 `06fd0b1` 复审发现 4 处机械绑定遗漏。未降低验收、未集成 FAIL 提交。

## 2026-07-31（Task 19 多 Agent 自动化流程诊断）

- 确认现有 Terminal 0～3 方案将用户变成手动消息总线，且固定多窗口/分支没有按依赖图、写路径和任务成本调度，造成等待、交接和重复授权浪费。
- 新增 Proposed `docs/adr/0001-agent-orchestrated-unattended-development.md`：建议用单 Orchestrator 按需调度实现/修复/复审/独立审计 Agent，默认无人值守闭环，只在新语义、扩权、不可逆操作、用户改动冲突或连续失败时请示。本轮未改业务代码或现有授权状态。

## 2026-07-31（策略设计补充资料与 W01 进展核对）

- 读取根目录 `成都麻将ai策略设计补充资料md.md`，确认其为 ChatGPT 对话导出而非 Approved 规格；其完整策略流程、K-01～K-12 和 AU-001～AU-096 主体已落入 Draft `docs/features/F0033_humanlike_ai_complete_software_design.md`。
- 根据 Git/worktree 事实刷新 `docs/status/LATEST.md`：记录 B2-A1 未提交草案、RULE-015 `2064eaa` 待批决策、TRAIN-009 `21ea400` 待 Terminal 0 复核、AUDIT-010 待批，以及 MODEL-001 repair `badea8e` 待独立复审。本轮未改业务代码或测试。

## 2026-07-31（Mac 目录初始化 / Task 19 基线同步）

- 核对 `main` @ `65e8dcb`、`task19-w01-baseline` tag、`task19/w01-b2a1` 分支、checkpoint 最终授权与 B2-A1 Approved 设计授权；更新 `docs/status/LATEST.md`，纠正旧快照中“checkpoint 待批准 / B2-A1 不可编码”的过期描述。本轮未改业务代码或测试。

## 2026-07-30（Task 19 剩余开发并行执行总计划）

- 重验 96/81 单元、207 边无环图、Task18 当前状态及 B2-A1-DESIGN-1.0.0；将 81 单元重分为 40 个小批次、14 个 wave 和 6 条主轨道。
- 生成 Task19 批次/单元/依赖/并行/文件/接口/worktree/集成/审计/风险/重规划/状态/进度/工具设计及四终端提示词。
- `task19_progress_tracker.md` 含 96 个唯一单元，初始分布 15 AUDITED / 3 READY / 76 WAITING DESIGN / 1 INTEGRATED / 1 SCAFFOLDED；计划/进度验证错误计数全为0。
- 因当前主工作树 dirty 且无包含已审计成果的 clean checkpoint，结论 `TASK19_WAITING_FOR_APPROVAL`。本轮未实现业务代码/测试/进度工具，未执行 Git 写操作，未改单元或 Task17 状态。

## 2026-07-30（B2-A1 设计审批生效）

- 按用户“执行任务1和2”，逐项批准 B2A1-DEC-001～012 的推荐 Option A，并批准 24 semantic、12 test、6 evidence、42 AC、9 interface、43 parameter 及 6 visibility 定义。
- 生成 `B2-A1_approval_form.md`，设计版本为 `B2-A1-DESIGN-1.0.0`；执行授权切换为 `READY_FOR_IMPLEMENTATION`，实施尚未开始。
- 本轮仅更新设计/决策/授权文档，未改业务代码、既有测试断言、Locked/Frozen、STATE-002/003/ALGO-002 状态或 Task17 历史。

## 2026-07-30（Task 18 B2-A1 设计闭环）

- 以 Locked STATE-002/003、ALGO-002、Task16 Frozen、B1-A effective contracts 及 B1-B 已审计边界为权威，生成设计、决策、接口、参数、可见性、调用链和执行授权包。
- 结构化闭环为每单元 8 semantic / 4 direct-test / 2 evidence / 14 AC，共 24/12/6/42；另有 9 项接口分类、43 行准确 Locked 参数引用和 6 项信息边界。
- 识别 12 项非唯一语义/接口决策并全部保持 PENDING；状态 `WAITING_FOR_DESIGN_APPROVAL`，`business_code_authorized=false`。未改业务代码、既有测试断言、Locked/Frozen、单元状态或 Task17 历史。

## 2026-07-30（Task 18 B1-B 关闭后队列刷新）

- 重读 Task18A 87 单元矩阵、23 批次、单元依赖图、完成路径、Task18 当前视图及 B1-A/B1-B 审计；移除已完成 6 单元后生成 81 单元队列。
- 机器校验为 0 重复、0 遗漏、0 AUDITED 混入，96 节点/207 边依赖图无环；MODEL-001 外部校准门禁不传播到独立确定性单元。
- 选定唯一下一批 `B2-A1 = STATE-002 -> STATE-003 -> ALGO-002`；因逐单元语义/接口决策尚未 Approved，授权为 `WAITING_FOR_DESIGN_APPROVAL`，未修改业务代码、Locked/Frozen 或 Task17 历史状态。

## 2026-07-30（B1-B 最终证据包修复与审计签署）

- 不修改业务代码或既有测试断言，生成 final E4/E5/AC、证据 manifest、严格校验 JSON、最终测试报告和独立审计签署。
- E5 42 行与 42 个唯一 Delta 全部通过外键检查：缺失引用、重复 Delta、无法解析引用均为 0；E4 每单元四类证据齐全，哈希均为实际文件 SHA-256 或 null。
- 全仓复跑 463 passed / 0 failed / 1 skipped（44.78s）；唯一 macOS Tk GUI skip 与 B1-B 无关。签署结论 `READY_TO_PROMOTE`，Task18 当前视图三单元为 AUDITED，Task17 历史不变。

按时间倒序记录**已完成**的文档与实现摘要（非自动生成）。
配合 `docs/status/LATEST.md` 作**跨机/跨 session 同步基线**（见 `docs/DEVELOPMENT.md` §2.2）。

## 2026-07-30（B1-B 最终缺口关闭与 AUDITED）

- 补齐STATE-001 100次完整跨进程Match复现、STATE-011四座成对隐藏扰动、STATE-004全phase×event笛卡尔与胡/碰/三杠事务效果验收。
- 干净重建独立E4与42行E5（24 semantic + 12 test + 6 evidence），无历史/summary/superseded行。
- 定向94 passed；全仓463 passed / 1 skipped。最终独立审计为24/24 semantic、12/12 test、6/6 evidence、42/42 AC PASS。
- STATE-001、STATE-011、STATE-004在Task18当前视图中均升为AUDITED，B1-B关闭；Task17历史文件不变。B2-A1移为仅设计复核的立即可执行批次。

## 2026-07-30（B1-B 最终独立验收）

- 重新独立复核 Approved 权威链、24/12/6 Delta、42 AC、生产调用图、Frozen 兼容和两项补充决策。
- 定向 86 passed；全仓 455 passed / 1 skipped；未修改业务代码或测试断言。
- 有效 AC 结论为 34 PASS / 1 FAIL / 7 BLOCKED；STATE-001/011/004 均保持 TESTED，未达 AUDITED。
- 剩余缺口是 STATE-001 100次完整跨进程、STATE-011 事务绑定隐藏扰动、STATE-004 全笛卡尔/胡杠响应分支和干净最终 E5。B1-B 不关闭，B2-A1 保持阻断。

## 2026-07-30（STATE-011 legacy deal golden 批准与 B1-B 证据刷新）

- 按用户“执行任务1和2”批准 `STATE-011-LEGACY-DEAL-GOLDEN-1.0.0`，冻结 legacy-v1 四 seeds、骰子、庄家、逐座有序手牌和55张有序牌墙。
- 不可变夹具 canonical SHA-256 为 `e806f33e58780a1ccdbaf306a417cd8d181dedd1173053ec4a98d5eada0547c5`，生产 DealTransaction 逐字段匹配。
- 刷新 STATE-011 独立 E4/E5；定向 86 passed，全仓 455 passed / 1 skipped。
- 三单元均达到 TESTED；本任务为证据生成而非最终独立审计，因此未标 AUDITED、未关闭 B1-B。

## 2026-07-30（STATE-004 权威适配决策与 B1-B 剩余缺口实施）

- 按用户“执行任务1-2”授权批准 `B1-B-STATE004-AUTHORITY-1.0.0`，选择 transactional legacy adapter，否决 post-commit observer-only。
- PlayerGameRunner 的 opening、draw 和 seat action 已通过 STATE-004 事务适配器；失败恢复 GameState、不加版本、不通知。
- STATE-001 生产请求支持 Approved FrozenConfig canonical bytes；STATE-011 添加 shuffle/deal/conservation 三故障阶段精确错误与零提交验证。
- 定向 85 passed；全仓 454 passed / 1 skipped。STATE-001/004 升为 TESTED，STATE-011 保持 PARTIAL；未生成队列刷新。

## 2026-07-30（B1-B 返工切片与再独立验收）

- 将 MatchController、DealTransaction 与 RoundStateMachine 实际接入 PlayerGameRunner；新增同步提交、RNG 三域安全引用、可注入发牌故障和 authority hash 兼容转换记录。
- 新增 B1-B 返工验收测试；定向 69 passed，全仓 452 passed / 1 skipped。
- 再独立审计确认原孤立 facade 问题已关闭，但 FrozenConfig 生产冻结、批准前 legacy golden、STATE-004 权威效果事务与全量 Oracle 仍不完整；三单元仍为 PARTIAL。
- 当前为 16/24 semantic PASS、19 PASS / 11 FAIL / 12 BLOCKED AC；B1-B 不关闭，B2-A1 不刷新。

## 2026-07-30（B1-B 独立验收审计重执行）

- 独立重新验证 Approved 权威链、生产调用图、Locked/Frozen/B1-A 兼容性、当前测试与运行证据；未接受开发 E4/E5 声明为当然事实。
- 三单元独立结论均为 `PARTIAL`；24 条 semantic Delta 中 6 PASS，42 项 AC 为 7 PASS / 22 FAIL / 13 BLOCKED。
- 独立产出 13 条 E4、24 条 semantic E5 加 1 条 artifact manifest，记录 12 项缺陷；B1-B 不得关闭，B2-A1 保持依赖阻断。
- 定向 61 passed；全仓 448 passed / 1 skipped；子进程兼容 2 passed。本轮未修改业务代码、测试断言、Locked/Frozen 或 Task 17 历史状态。

## 2026-07-30（Codex CLI 多安装处置）

- 已将默认 `codex` 解析切换到 npm 版，`codex --version` 现在输出 `codex-cli 0.146.0`。
- `Get-Command codex -All` / `where.exe codex` 目前仅显示 npm 入口；WinGet 链接 `C:\Users\moff1\AppData\Local\Microsoft\WinGet\Links\codex.exe` 已删除。
- WinGet 包目录中的残留二进制仍未能完全清理，原因是 Windows ACL 拒绝访问；本轮保留该残留作为后续清理事项，不影响当前默认命令。

## 2026-07-30（开发环境：启动并核对 CC Switch 现有配置）

- CC Switch 已启动，`cc-switch` 进程正常运行，主窗口可用。
- 本地 `~/.cc-switch` 数据目录已存在，数据库中已有现成 provider；Codex 侧当前仍停留在默认 provider。
- 本轮未对 provider、代理、启动项或其他持久化设置做改动。

## 2026-07-30（开发环境：安装 CC Switch v3.19.0）

- 从官方 `farion1231/cc-switch` GitHub Release 下载 Windows x64 MSI；SHA-256 与发布资产记录一致。
- 静默安装成功（MSI 返回码 0），注册版本 3.19.0，位置为 `C:\Users\moff1\AppData\Local\Programs\CC Switch\`。
- 未启动首次配置，未修改麻将训练器业务代码、规格、测试或产品状态。

## 2026-07-30（B1-B独立审计）

- 独立复核42项AC：7 PASS、22 FAIL、13 UNPROVEN；结论REJECTED_REWORK_REQUIRED
- 发现STATE-001/STATE-004新门面未进入真实生产调用链，既有E4生产链声明不成立
- 记录12项整改发现，覆盖FrozenConfig冻结、玩家装配、并发CAS、Deal故障/RNG域/边界、Round GameState/outbox集成及逐Delta E5
- 定向68 passed、全仓449 passed；Task17状态不变，B1-B队列改为AUDIT_REJECTED_REWORK_REQUIRED

## 2026-07-30（B1-B批准、终审授权与实现）

- 批准B1-B-DESIGN-1.0.0；重跑终审得到READY_WITH_MODEL001_SIMULATION_LIMITATION，授权范围仅STATE-001/STATE-011/STATE-004
- 新增Match原子控制、Deal事务门面和Round Locked状态机，保持旧runner、GameState v5、legacy replay/RNG兼容
- 新增12项测试以及B1-B E4/E5证据；定向68 passed，全仓449 passed
- 队列更新为IMPLEMENTED_PENDING_INDEPENDENT_AUDIT；Task17状态未改变，未标记AUDITED

## 2026-07-30（PRE-DEV-FINAL-GATE-001-R1：B1-B设计审查包）

- 为STATE-001、STATE-011、STATE-004生成24条semantic、12条test、6条evidence Delta以及42条逐项验收Oracle；结论为REVIEW_REQUIRED，未授权编码
- 明确真实依赖拓扑、STATE-004 Locked phase枚举、三单元生产缺口、原子性/可见性/确定性及接口影响
- 新增B1-A ACTIVE authority correction及authority map R1，统一清理FG-002旧PENDING派生引用，分类为MUST_FIX_BEFORE_AUTHORIZATION
- CSV结构与引用自检通过；定向77 passed；全仓437 passed、0 failed、0 skipped

## 2026-07-30（MODEL-001模拟标签A/A/C批准与实现门禁）

- 批准current cleared/dominant标签、暗手+副露dominant并列规则及terminal shape回填方案C
- 新增MODEL001-LABEL-SCHEMA 1.0.0合同、示例、10条测试向量和审批表
- 生成器门禁由BLOCKED_BY_LABEL_SPEC_DECISION更新为IMPLEMENTATION_READY；未编码、未生成数据、未改变MODEL-001状态

## 2026-07-30（MODEL-001模拟生成器编码前标签门禁）

- 发现标签时点、dominant_suit计数/并列和shape重叠/未完成结构尚无唯一Approved定义
- 按任务约束停止编码，新增三项PENDING最小标签决策包和门禁报告
- 未生成数据、未访问网络/模型、未修改MODEL-001审计状态

## 2026-07-30（Task 18执行队列推进）

- 生成TASK18-QUEUE-2当前队列，将B1-A标为COMPLETED
- B1-B依赖满足，移动为IMMEDIATELY_EXECUTABLE FOR DESIGN REVIEW，单元STATE-001/STATE-011/STATE-004
- 当前批次分布为1完成、1立即设计、3外部数据门禁、18依赖阻断；Task18A原始队列保持历史不变

## 2026-07-30（Task 18 B1-A权威状态登记）

- 创建Task 18审计状态增量，将STATE-010、ALGO-009、ALGO-011由PARTIAL登记为AUDITED
- 生成当前96单元CSV、JSON与摘要；当前分布12 AUDITED、82 PARTIAL、1 INTEGRATED、1 SCAFFOLDED
- 保持Task17历史文件和9/1/85/1历史分布不变，明确历史状态与当前状态引用边界

## 2026-07-30（B1-A第三轮缺口关闭：42/42 AC）

- 完成orchestrator四座STATE-010装配与归档、信息隔离和跨进程复现
- 完成ALGO-009阶段/版本/边界/E4/幂等闭环及ALGO-011七字段审计投影、完整版本和调度闭环
- Golden 18/18、专项57 passed、全量423 passed
- 第三轮审计42 PASS/0 FAIL，结论AUDITED_CANDIDATE；未修改Task17历史文件

## 2026-07-30（B1-A第二轮缺口关闭与再审计）

- 新增STATE-010闭集/重复校验、owned resolve结果和性能基线
- 新增ALGO-009 v2 reload、fallback、迁移元数据、扩展边界与1MB性能验收，最大9.58ms
- 新增ALGO-011 1—256 UTF-8 ID边界、跨进程复现及orchestrator rng_version传播
- Golden 18/18、全量417 passed；第二轮42项AC由11/31提升为24 PASS/18 FAIL
- 独立审计仍NOT_AUDITED，Task17三个单元保持PARTIAL

## 2026-07-30（B1-A任务1-6继续：Golden/E4/E5与42项AC审计）

- 将60行权威参数元数据生成到生产注册表，并把Humanlike真实决策RP写链接入逐座STATE-010 CAS store
- 增加ALGO-009纯legacy迁移、严格v1.1前置验证及只写v2的原子writer
- 增加ALGO-011受限SeedTrace store和training runner显式rng v2路径
- 机器执行18/18 Executable Golden全部通过；E4扩展为12条正常/失败生产轨迹并生成E5 SHA-256 manifest
- 全量回归401 passed；独立审计42项AC为11 PASS、31 FAIL，保持Task17三单元PARTIAL

## 2026-07-30（B1-A清单1-5：合同批准、R4与首个实现切片）

- 批准OPTION-J2、CONTRACTS/PARAMS 2.0及1.1→2.0迁移边，R4编码门禁通过
- 实现STATE-010的60 ID注册、GP冻结、四座RP隔离/CAS/归档基础
- 实现ALGO-009显式迁移和CDMJ canonical-jcs-nfc-v2编码/hash基础
- 实现ALGO-011 legacy兼容、无状态逻辑坐标、受控trace_ref及显式v2发牌/回放记录入口
- 新增12个B1-A测试；专项与相关回归30 passed，全量399 passed
- 从三个真实生产入口采集E4正常路径及SHA-256 manifest
- 独立审计为REVIEW_REQUIRED/NOT_AUDITED；未降低Task17验收标准，三个单元仍保持PARTIAL

## 2026-07-30（Task 18B-R3：B1-A正式版本变更包与Golden合同）

- 生成CONTRACTS 2.0/PARAMS 2.0正式变更提案、版本矩阵、三条迁移边、有效规格覆盖层和待填写审批表；保持PARAMS 1.1 legacy读取与旧hash不变，新writer只写v2
- 识别RFC 8785与Locked int64冲突，推荐但未批准`OPTION-J2 / CDMJ canonical-jcs-nfc-v2 profile`；因此最终状态为BLOCKED_BY_CANONICAL_PROFILE_DECISION
- 扫描60项参数，无Decimal canonical字段，登记`NO_DECIMAL_FIELDS_IN_CANONICAL_CONFIG`
- 将19个向量分为18个可执行Golden和1个说明性示例，补齐执行目标、完整输入、版本、字节级canonical/SHA-256、错误码及BLAKE2b-64参数
- 生成R1有效覆盖层：83条泛化SEM-PARAMETER标为SUPERSEDED，24条semantic、12条test和6条evidence delta保持ACTIVE；42项AC绑定到新版本门禁
- 更正非Locked验收矩阵中的SHA-256措辞；Locked措辞仅进入合同v2提案，未直接修改
- Windows Python 3.12.10标准全量回归387 passed、0 failed、0 skipped，耗时217.34秒
- 撤回上一条过早的IMPLEMENTATION_READY结论；尚需批准canonical profile、合同版本包和1.1→2.0迁移边，未修改业务代码或测试断言

## 2026-07-30（清单1-3：Frozen v2提案、批准与B1-A R3复审）

> 已被后续Task 18B-R3正式版本包覆盖：该轮未独立裁决canonical profile，不构成编码授权。

- 创建并由项目负责人批准`B1-A-FROZEN-V2 1.0.0`，冻结CONTRACTS/PARAMS 2.0、NFC+JCS canonical、v1只读适配、显式迁移与回滚
- 将v2策略DecisionResult改为安全seed_trace_ref，完整SeedTraceV2Restricted隔离到受限引擎/trainer/audit存储，解决Frozen v1的隐藏随机材料暴露冲突
- 完成R3门禁复审，STATE-010、ALGO-009、ALGO-011均为IMPLEMENTATION_READY；STATE-010先行，ALGO-009/011随后并行
- Windows Python 3.12.10全量回归387 passed、0 failed、0 skipped，耗时218.65秒
- 同步首批实现设计和R1历史报告状态；未修改业务代码、测试断言、现有Frozen v1、Task17/18A状态或其他批次

## 2026-07-30（B1-A九项规格决策批准）

- 项目负责人明确批准Task 18B-R2九项决策全部选择A；以`project_owner_user`、UTC `2026-07-30T04:39:21Z`和`B1-A-DECISIONS 1.0.0`登记到审批表、决策矩阵及golden元数据
- 解除BLOCKED_BY_SPEC_DECISION；因canonical v2选项要求改变Frozen canonical bytes，门禁转为BLOCKED_BY_INTERFACE_APPROVAL，需先完成CONTRACTS 2.0.0、PARAMS 2.0.0和迁移边审批
- 批准本身未修改Locked/Frozen规格、业务代码、测试断言、Task 17/18A状态或其他批次，也不等同于允许编码

## 2026-07-30（Task 18B-R2：B1-A九项规格决策包）

- 为STATE defaults、RP archive、migration graph、extensions、canonical number/Unicode、config fallback、RNG version/coordinate九项阻断生成正式PENDING决策卡；每项含两个选项、兼容/跨语言/持久化/安全/测试/迁移/回滚分析和可复制规范文字
- 推荐保护现有PARAMS 1.1、legacy-v1回放及三条旧随机流；新录制显式rng v2，无状态逻辑坐标禁止调度和共享index材料
- canonical推荐采用legacy/v2双轨；NFC+RFC8785 JCS新字节规则明确要求CONTRACTS 2.0.0、PARAMS 2.0.0和迁移边，未修改Frozen契约
- 生成19条golden（10正向、9反向），独立验证legacy当前值及canonical bytes/SHA-256；统一SHA-256为32字节/64个小写十六进制字符
- 登记4处B1-A相关hash位数措辞问题，Locked算法规格与Task16 Frozen契约只报告未修改
- Windows Python 3.12.10全量回归387 passed、0 failed、0 skipped，耗时133.82秒
- 新增逐项审批表，九项均保持PENDING；未修改业务代码、测试断言、Task 17/18A状态或其他批次

## 2026-07-30（Task 18B-R1：B1-A实现设计复审与修正）

- 独立复审STATE-010、ALGO-009、ALGO-011，撤回原implementation-ready结论并改为BLOCKED_BY_SPEC_DECISION；明确9项需先批准的默认/null、归档、迁移、canonical和随机版本/坐标决策
- 将B1-A拆为24条具体semantic delta、12条test delta和6条evidence delta，建立SeedTrace字段级可见性与7项接口影响分析；42条AC改为42个不同的客观oracle
- 冻结旧随机兼容策略为legacy-v1结果零变化，新规范公式使用显式新版本；并发派生禁止共享可变index和调度序号
- 回溯83单元并删除全部83条无具体参数ID/行为差异的机械SEM-PARAMETER；同步修正矩阵、目录和汇总为目标1245、已实现映射1069、缺失176、总delta 591
- 接口统计由83 NO_INTERFACE_CHANGE修正为80 NO_INTERFACE_CHANGE + 3 COMPATIBLE_EXTENSION；新增Frozen SeedTrace必填坐标字段被识别为breaking并禁止
- Windows Python 3.12.10全量回归387 passed、0 failed、0 skipped，耗时154.91秒；未修改业务代码、测试断言、Locked/Frozen规格、Task 17/18A历史文件或其他批次

## 2026-07-30（Task 18B：83 单元实现语义差距基线）

- 对 Task 18A 的 83 个 semantic-completion 单元逐项建立 Locked 目标语义、当前生产语义和缺失语义对照；确认 83 个均为 VALID，未发现误分类、规格冲突或规格不完整
- 采用 15 个来源化语义面盘点出目标 1,245、静态正向映射已实现 986、缺失 259，并拆分为 674 个带 Locked 来源、独立验收标准和实施顺序的 semantic/test/evidence delta
- 完成 83 个单元的接口影响分析，均可在现有 Frozen 契约后内部补全，无待批准 Breaking change
- 为首批 B1-A（STATE-010、ALGO-009、ALGO-011）形成可直接编码设计、42 条 AC-01～AC-14 验收矩阵和完整开发提示词；结论为 implementation_ready
- Windows Python 3.12.10 全量回归 387 passed、0 failed、0 skipped，耗时 121.97 秒
- 新增 `docs/spec-v3/semantic-completion/` 七项交付及 `tools/task18b_semantic_baseline.py`；未修改业务代码、测试断言、Locked 规格、Task 17/18A 历史产物或版本号

## 2026-07-30（Task 18A：87 单元缺口分型与批次规划）

- 基于 Task 17 权威矩阵、Task 15 试点、Task 16 Frozen 公共契约、96 单元规格及当前实现/测试目录，对全部 87 个非 AUDITED 单元逐行完成 12 类缺口和主要完成路径分型
- 路径分布为 83 semantic completion、1 full implementation（HEUR-016）、3 external data（MODEL-001、MODEL-005、AUDIT-012）；没有在缺乏新证据时升级状态或推断 evidence-only
- 将 87 个唯一单元分配到 23 个 1～10 单元的依赖有序批次；修正 Task 17 阶段标签并非完整拓扑序的问题，确认首批内部顺序为 STATE-010 → ALGO-009/ALGO-011
- 单列 MODEL-001 合规10,000样本、隔离label zone、分组切分、校准指标与泄漏门禁；该轨与B1～B3并行
- Windows Python 3.12.10 全量回归 387 passed、0 failed、0 skipped，耗时234.46秒
- 新增七项 plans/reports 交付及 `tools/task18a_generate_plan.py` 可复现生成器；未修改业务代码、测试断言、Locked规格、Task 17原始产物或版本号

## 2026-07-30（Task 17：96 单元审计状态重新明确）

- 以 audit 目录 Task 17 的 summary、gap matrix、catalog、report、dependency graph 与 JUnit 为唯一依据，复核 96 行、分类计数、状态透视及证据计数
- 明确最终状态为 9 AUDITED、1 INTEGRATED、85 PARTIAL、1 SCAFFOLDED；MODEL-001 是唯一 INTEGRATED，HEUR-016 是唯一 SCAFFOLDED
- 说明代码/测试线索不等于 AUDITED：代码证据 95、测试证据 94，但可归属运行证据仅 10；96 个单元均有追踪证据
- 新增 `docs/spec-v3/audit/task17_96_unit_audit_clarification.md`，完整列示全部 96 个 ID、分类结果、证据口径、风险和批次含义
- 本轮未修改业务代码、测试断言、Locked 规格、Task 17 机器可读产物或版本号

## 2026-07-30（项目进度初始化与当前基线核验）

- 按规定读序恢复项目上下文，确认主线为 Spec v3 Task 18，`MODEL001-DATA-001` 继续阻断 MODEL-001 校准，但不阻断 B1–B3 确定性/启发式实施
- 核验本地 `main` / `423326e`、应用版本 `0.2.1`，并登记工作树 650 个 tracked changes、18 个 untracked entries；全部视为既有改动保留
- Windows Python 3.12.10 全量测试通过：387 passed、0 failed、0 skipped，耗时 117.21 秒
- 仅同步 `LATEST.md` 与 changelog，未修改业务代码、测试断言、Locked 规格或版本号

## 2026-07-30（Task 17 / Tasks 1–5人工保存检查点）

- 固化当前恢复基线：Task 17已完成；Tasks 1–5停在`MODEL001-DATA-001`，尚未启动B1–B6批量实现
- 在LATEST登记推荐恢复顺序及关键报告路径；未修改业务代码、测试断言或Locked规范
- 保留全部既有未提交修改，未执行Git提交或破坏性工作树操作

## 2026-07-30（Tasks 1–5执行门禁）

- 复核MODEL-001最终校准条件，确认仓库缺少Locked规格要求的10,000样本冻结发布、隔离标签、分组切分和模型产物
- 拒绝将历史日志或规则fallback自生成标签伪装为ECE/Brier验收数据；MODEL-001保持INTEGRATED并登记`MODEL001-DATA-001`
- 确认该缺口不阻断B1–B3，但B4模型校准、B6外部评价受数据门禁约束，B5受B1/B2生产引擎依赖约束
- 新增`docs/spec-v3/reports/task18_tasks_1_5_execution_gate.md`；未修改业务代码或测试断言

## 2026-07-30（Task 17：96 单元真实基线复审）

- 以 Task 14/15 四类证据标准逐项重审 96 个锁定单元，未直接沿用旧“33/61/2”结论
- 新基线为 9 AUDITED、1 INTEGRATED、85 PARTIAL、1 SCAFFOLDED、0 BLOCKED；AUDITED 均具备代码、测试、运行和追踪四类证据
- 重新验证候选文件、AST 符号、生产调用线索与测试函数，剔除 13 条当前失效候选引用并补正 ALGO-011 漏列证据；AU-001～AU-096 迁移及 96/96 规格追踪完整
- 记录 RULE-001、ALGO-002、ALGO-008、SCORE-004、AUDIT-009 的内部职责拆分复核建议，保持锁定外部门面和 ID 不变
- Python 3.12 全量测试 386 passed、1 skipped；新增 `docs/spec-v3/audit/` 五项基线交付、JUnit 与 `tools/task17_rebaseline.py`
- 本轮未修改业务代码、规则文档或测试断言

## 2026-07-29（Spec v3 Locked与M0实现差距审计）

- 正式锁定`SPEC-V3-3.0.0`，冻结36份规范文件和2份上游来源的逐文件SHA-256；集合hash为`6df28948e37dd95c57c9060c6e7e7d28a8243b86e8844a133ab33b6641c1e4ec`
- 新增`SPEC_V3_LOCK_MANIFEST.md/.csv`，明确证据层不进入规范hash以及版本化解锁/重锁规则
- 完成96行M0实现差距盘点：80 ADAPT、15 REWRITE、1 ADD；目标主文件、v3测试模块和JSONL均为0/96
- 保存50个候选代码文件hash及game_id/状态、PlayerView、事件、ScoreTransfer四类baseline fixture
- 运行全量旧基线：357 passed、1 skipped；结果不作为v3 E3，全部单元仍E1/Not Evaluated
- 交付`docs/spec-v3/09-implementation-audit/`；本轮未修改业务代码，保留既有dirty worktree

## 2026-07-29（CDI-003批准与Spec v3最终锁定审计）

- 根据用户明确批准，将总规范、开发指南/任务卡/迁移计划、测试策略/用例目录/golden、审计标准/清单及模板提升为Approved/Approved Template
- 保留实现、测试代码、JSONL、运行证据及AUDITED状态为Not Implemented/Not Evaluated，未把文档批准冒充工程证据
- 重跑96单元跨层集合、576父测试、890 TC、1344 AC、AU-001～096迁移、60参数及状态/证据/性能边界检查
- 最终Open为Critical 0 / High 0 / Medium 1 / Low 1，达到规范锁定建议门禁，结论更新为`READY FOR SPEC LOCK`
- 更新三份最终审计报告、总规范、旧冲突报告和LATEST；未修改业务代码或运行pytest/回放/训练

## 2026-07-29（Spec v3 一致性修复与复审）

- 统一STATE-004唯一RoundPhase；开发指南新增事件—phase映射及STATE-001 Match状态分层，关闭CDI-001
- 正式证据等级统一为E0—E5；旧EV隔离为legacy历史字段并增加保守迁移规则，关闭CDI-002
- 新增60行`parameter_registry.csv`，登记GP/RP名称、范围、生命周期、可见性、source hash、consumer和边界测试，关闭CDI-004
- 删除开发指南第二套5/20/5/50ms性能数字，规定AC-12只读Approved单元规格，关闭CDI-006
- 重跑96单元、576父测试、890 TC、1344 AC、96旧AU及60参数检查；当前Critical 0 / High 1 / Medium 1 / Low 1，仍不建议锁定
- 更新三份复审报告、旧冲突报告、总规范和LATEST；未修改业务代码或执行pytest/回放/训练

## 2026-07-29（Spec v3 全量跨文档一致性审计）

- 对`docs/spec-v3/`执行目录、规格、开发、测试、验收、追踪、迁移、参数、公式、I/O、状态、证据、隐藏信息和HEUR边界全量审计；未修改程序代码
- 验证96/96跨层覆盖、576个父测试、890个细化TC、1344个AC和AU-001～096迁移的集合完整性与唯一性
- 记录Critical 0 / High 3 / Medium 3 / Low 1；High为状态枚举未映射、EV/E证据等级未统一、核心候选文档仍为Draft
- 根据锁定门禁结论标记`NOT READY FOR LOCK`，未把结构完整误报为实现、运行或AUDITED通过
- 交付`docs/spec-v3/08-review/{cross_document_consistency_report.md,unresolved_issues.md,final_readiness_report.md}`，并同步旧冲突报告、总规范与LATEST结论

## 2026-07-29（Spec v3 审计与验收规范 Draft）

- 定义E0—E5累计证据等级、证据新鲜度、缺陷严重度和AUDITED/STALE/REVOKED状态
- 为96单元生成AC-01～AC-14共1344项hard验收清单，覆盖用户要求的全部实现、测试、运行、追踪、性能、泄漏与指标检查
- AUDITED要求八项条件、14项检查、至少E4及无开放High/Critical同时满足；外部/发布声明按适用项E5
- 新增单元证据包和审计报告模板，当前所有实现证据仍NOT_EVALUATED/E0
- 交付 `docs/spec-v3/06-audit-acceptance/`及`tools/generate_spec_v3_acceptance_checklist.py`；未运行pytest或审计业务实现

## 2026-07-29（Spec v3 测试策略与用例目录 Draft）

- 对96单元逐项判断11类测试适用性，生成96行覆盖矩阵和890个适用TC测试卡
- 每用例定义完整前置、输入、命名seed、操作、expected、误差、状态变化、日志、失败和自动化位置，并关联Approved父测试合同
- 为ALGO-001～011与SCORE-001～006登记51个正常/边界/非法golden来源
- 全部单元强制隐藏信息差分与同seed回放；HEUR按允许域/统计分布、MODEL按校准指标验收
- 新测试目录为Draft，代码/向量未实现且证据Not Evaluated；未运行pytest
- 交付 `docs/spec-v3/05-test-spec/{test_strategy.md,test_case_catalog.md,golden_vectors.md,coverage_matrix.csv}`及生成器

## 2026-07-29（Spec v3 开发实施指南 Draft）

- 新增总体开发指南，定义目标模块、公共结构/接口、状态机、事件总线、规则与AI调用、配置/RNG、日志回放、错误、性能、阶段和禁止方式
- 为96个锁定单元生成开发任务卡，逐卡关联建议文件、现有候选、依赖、实施步骤、Approved测试合同和完成定义
- 新增现有代码分阶段迁移计划，规定适配器、影子比较、单权威切换、兼容、回滚和旧路径退役门禁
- 指南为Draft，代码符合度仍Not Evaluated；未修改业务代码或运行pytest
- 交付 `docs/spec-v3/04-development-guide/` 与`tools/generate_spec_v3_development_cards.py`

## 2026-07-29（Spec v3 全部测试规格 Approved）

- 根据用户明确批准，将测试规格索引及六份分类测试规格由Draft提升为Approved
- 96行执行清单同步为规格Approved，576个测试合同成为后续测试实现和验收的权威依据
- 同步测试规格生成器，确保重复生成保持Approved状态
- 测试代码/向量仍Not Implemented，证据仍Not Evaluated；本轮未修改业务代码或运行pytest

## 2026-07-29（Spec v3 96单元可执行测试规格 Draft）

- 为96个Approved单元建立每单元N/B/I/P/R/X六类可执行测试合同，共576个唯一测试ID
- 生成六份分类测试规格、96行执行清单与统一索引，冻结计划pytest模块、JSONL向量、oracle、误差、执行命令和证据门禁
- 按方法边界分别定义确定精确断言、启发式统计允许域、模型校准/泄漏、训练生产等价和审计证据链测试
- 测试规格为Draft，计划测试代码与向量仍Not Implemented，未运行pytest或形成EV3证据
- 交付 `docs/spec-v3/05-test-spec/` 与可重复生成工具 `tools/generate_spec_v3_test_specs.py`

## 2026-07-29（Spec v3 全部单元规格 Approved）

- 根据用户明确批准，将六份spec-v3单元规格文档由Draft提升为Approved，覆盖全部96个单元
- 将96行追踪矩阵同步为 `Approved / Not Evaluated`，严格区分规范批准与实现验收
- 更新总实现规范和冲突报告并关闭CF-002；这是当时局部检查结论，后续已由全量一致性审计取代；实现、测试、运行及发布证据仍未验收
- 本轮未修改业务代码或执行pytest、回放、训练和发布审计

## 2026-07-29（AUDIT 14 单元完整规格 Draft）

- 为 `AUDIT-001～AUDIT-014` 编写统一23栏规格，覆盖日志、hash链、回放、不变量、测试证据、指标、追踪、发布、外部评价、架构和证据治理
- 规定审计truth隔离、append-only证据、canonical顺序、稳定错误码、脱敏/保留、新鲜度及hard门禁语义
- 将总规范和96行追踪矩阵的详细规格覆盖更新为96/96，并在冲突报告关闭AUDIT规格缺口CF-001
- 六份详细规格仍为Draft / Not Evaluated，未授权业务代码实现；本轮未修改业务代码或运行pytest
- 交付 `docs/spec-v3/03-unit-specs/audit_specs.md`，并同步总规范、追踪矩阵、冲突报告和状态基线

## 2026-07-29（AI Implementation Spec v3 集成 Draft）

- 生成只汇总和引用、不复制单元详细定义的 `docs/spec-v3/AI_implementation_spec_v3.md`
- 新增96行规则→参数→单元→模块追踪矩阵，覆盖目录全部输入/输出、方法类别、RNG、可见性与详细规格状态
- 在总规范记录AU-001～AU-096迁移，并区分确定规则/算法、启发式、概率/可训练模型、训练和审计truth边界及公式规范等级
- 完成跨文档结构检查；锁定来源hash、目录/迁移/端点/链接通过，发现AUDIT-001～014详细规格缺失和现有规格仍为Draft两项阻断
- 交付 `docs/spec-v3/07-traceability/rule_parameter_unit_matrix.csv` 与 `docs/spec-v3/08-review/spec_conflict_report.md`；未修改业务代码或运行pytest

## 2026-07-29（TRAIN 9 单元训练环境规格 Draft）

- 为 `TRAIN-001～TRAIN-009` 编写episode、观测/动作/mask、奖励、非法动作、自博弈、对手池、回放、快照、并行、数据、评估和性能规格
- 强制训练/生产复用同一规则、状态和计分引擎；禁止训练包装复制或简化房规
- 隐藏truth仅供隔离的评估器/标签区使用；策略观测、模型输入和势能函数不得读取
- 所有奖励追踪到真实计分事件或显式可见势能差，塑形默认关闭；状态Draft / Not Evaluated，未修改业务代码或运行训练
- 交付 `docs/spec-v3/03-unit-specs/training_environment_specs.md`

## 2026-07-29（MODEL 5 单元模型接口与基线规格 Draft）

- 为 `MODEL-001～MODEL-005` 编写模型接口、规则基线、训练数据、切分防泄漏、校准、阈值、回退、时限和解释规格
- 覆盖对手清缺/主体花色/牌型、听牌/等待/点炮风险、跨局风格学习、真人行为拟合、候选动作概率分布及模型产物生命周期
- 禁止隐藏手牌、墙序、oracle和未来信息进入线上特征；终局公开或离线truth只允许进入独立label zone
- 所有概率模型要求Brier/log loss/ECE及可靠性证据，并绑定确定性规则回退；状态Draft / Not Evaluated，未训练模型或修改业务代码
- 交付 `docs/spec-v3/03-unit-specs/probabilistic_model_specs.md`

## 2026-07-29（HEUR 23 单元启发式规格 Draft）

- 为 `HEUR-001～HEUR-023` 编写可实现、可量化且不假设唯一正确动作的统一23栏规格
- 每单元区分不可违反的规范约束、默认基线、可调参数和可训练软替换；模型替换仍受合法性、可见性、mandatory、回退和审计门禁约束
- 覆盖换三张、定缺、计划/转向、碰杠过胡、弃牌/换听、防守扣牌、注意/有限搜索、满意停止、人类失误和思考节奏
- 硬门禁以零非法、零规则违例、零泄漏和100% seed复现验收；软行为以方向效应、regret、分布及95% CI验收，无真人数据不虚构真人相似结论
- 交付 `docs/spec-v3/03-unit-specs/human_heuristic_specs.md`；状态Draft / Not Evaluated，未修改业务代码或运行pytest

## 2026-07-29（ALGO/SCORE 17 单元数值规格 Draft）

- 为 `ALGO-001～ALGO-011` 与 `SCORE-001～SCORE-006` 编写完整数值规格，覆盖输入向量、范围、公式、顺序、舍入、边界/null、复杂度、输出、不变量、golden、测试向量、误差、错误码和审计字段
- 严格区分规范公式与基线公式，禁止训练模型替代确定算法；覆盖向听/进张/等待、可见/未见/墙内估计、候选/Q、配置/视图/随机流及完整计分链
- 对胡、杠、花猪、查大叫、退税、呼叫转移和累计账本规定逐事件、逐层和总账零和；当前简化查叫与未实现退税显式保留为基线差距
- 交付 `docs/spec-v3/03-unit-specs/deterministic_algorithm_scoring_specs.md`；状态 Draft / Not Evaluated，未修改业务代码或运行pytest

## 2026-07-29（RULE/STATE 28 单元规格卡 Draft）

- 为 `RULE-001～RULE-016` 与 `STATE-001～STATE-012` 编写统一 23 栏完整规格卡，覆盖输入输出、处理流程、状态转移、不变量、错误码、并发、日志、测试和验收
- 建立同输入/状态/规则/种子唯一结果的确定性总契约，并细化牌张守恒、发牌、换三张、定缺、摸打、碰杠胡、多人响应、过胡、胡后退出、牌墙终止和隐藏信息隔离 hard gate
- 代码、测试和运行证据均保留显式占位，状态为 Draft / Not Evaluated；本轮未修改程序代码或运行 pytest
- 交付 `docs/spec-v3/03-unit-specs/deterministic_rule_state_specs.md`

## 2026-07-29（UNIT-CATALOG 1.0.0 Locked）

- 将原子性审查结果冻结为开发、测试和验收共用的 96 单元正式目录，按 9 种类型明确分层
- 为每个单元登记来源、GP/RP、依赖/消费者、输入/输出、确定性、可训练性、RNG、可见性、优先级和当前证据状态
- 产生具有 96 节点和 221 条直接边的依赖图，修正 game_id 随机流与 Match 初始化循环后通过 DAG 和反向消费者一致性校验
- 交付 `docs/spec-v3/02-unit-catalog/{locked_unit_catalog.md,locked_unit_catalog.csv,dependency_graph.md}`；未修改代码或运行测试

## 2026-07-29（Spec v3 96 单元边界审查）

- 对 AU-001～AU-096 逐项判定 KEEP/SPLIT/MERGE/RENAME/REMOVE，建立完整 old→new many-to-many CSV
- 建议 96 个新单元，分为 RULE/ALGO/HEUR/MODEL/STATE/SCORE/TRAIN/AUDIT 八类，各自有单一职责和独立验收边界
- 移除 3 个无独立运行价值的治理汇总项，新增牌墙/发牌、game_id 随机流、策略失败回退和模型生命周期 4 个缺失单元
- 交付 `docs/spec-v3/02-unit-catalog/{unit_boundary_review.md,unit_migration_map.csv,proposed_unit_catalog.md}`；未修改代码或运行测试

## 2026-07-29（Spec v3 Mac 接续核验）

- 按 spec-v3 交接读序恢复来源清单、96 行证据矩阵、证据分级和单元模板上下文
- 确认两份锁定来源哈希与基线一致，Mac Python 3.12.13 / pytest 9.1.1 环境可用
- 新增 `docs/spec-v3/08-review/MAC_CONTINUATION_CHECK_2026-07-29.md`，完成交接队列第 1 项
- 未运行测试或修改程序代码；下一步为 33 个 P0 legacy rows 的人工证据复核

## 2026-07-29（F0033 Humanlike AI 完整软件设计 Draft）

- 重新归一两份成都麻将 AI 源规格和实现审计，创建覆盖 96 个审计单元的完整软件设计
- AU-001～AU-096 逐项给出具体流程、量化目标和证据类型，并定义全局 K-01～K-12 门禁
- 补充九模块边界、Humanlike 决策管线、Q 公式、状态机、错误处理、训练评估和发布规则
- 本轮只落盘 Draft、索引和状态，不修改业务代码或宣称目标已实测达成

## 2026-07-29（F0031/F0032 量化能力审查）

- 验证 F0031 指标方法、阈值、分母和统计口径，以及 F0032 grain、切分、覆盖和质量门禁
- 结论为 Needs revision：框架可用，但尚无 96 单位原子化 ID 和逐项 metric/data/threshold/evidence crosswalk
- 指出 G3/G4 校准、G5 上下文与概率契约、真人来源和 F0032 实际数据 release 等阻断项
- 提出 AU-001～AU-096 机器可读矩阵及 Q0～Q5 分阶段量化路线
- 报告：`docs/status/F0031_F0032_QUANTIFICATION_REVIEW_2026-07-29.md`

## 2026-07-29（F0032 Humanlike 评估数据集规划 Draft）

- 新增 F0032 Draft，规划规则 golden、模拟对局、真人试点、冻结真人评估和挑战集五类数据
- 定义决策级 schema、PlayerView/标签/受限真值隔离、玩家级切分、覆盖规模、版本和质量门禁
- 明确真人原始数据不进入 Git，正式测试集永不参与训练，授权不明或规则不可识别的数据不得进入正式评估
- 本轮只落盘数据规格、索引和状态，未采集数据或修改代码

## 2026-07-29（F0031 人类化功能量化验收规格 Draft）

- 新增 F0031 Draft，将“人类化”拆为机制可信、行为可辨识、策略合格、真人相似和学习有效五级结论
- 定义安全/语义/风格/强度/真人相似/学习/性能七组门禁及样本量、配对 seed、座位轮换和置信区间口径
- 明确无合规真人牌谱时真人相似度只能为 Not Evaluated，不得以工程测试替代效果结论
- 本轮只落盘规格、索引和状态，不修改业务代码

## 2026-07-29（规格审计结论澄清）

- 确认“缺乏量化目标和效果指标”是人类化效果无法明确判定的重要原因，但不是唯一原因
- 进一步区分三类缺口：需求不可操作化、实现与规格缺少直接追踪证据、缺少外部基准与真人数据
- 指出规则正确性/确定性等工程指标已有量化门禁；模糊主要集中在人类化语义、策略强度和真人相似度

## 2026-07-29（两份 AI 规格实现审计）

- 逐章对照人类化决策规则 v1 与程序实现规范 v2.0.0，形成 96 个功能审计单元
- 结论：33 完成、61 部分完成、2 未实现；工程底座强，但人类化语义深度、训练模式和真人效果证据仍有缺口
- 交付 Markdown、canonical artifact JSON 和自包含 HTML；HTML validation/package/structural verification 通过
- 证据：当前全量 358 passed；沿用 F0028/F0030 批跑、审计、性能和人工快速验收记录
- 报告：`docs/status/SPEC_IMPLEMENTATION_AUDIT_2026-07-29.md`

## 2026-07-29（F0005 Windows creationflags 回归修复）

- `SubprocessTransport` 仅在 win32 显式传入中性的 `creationflags=0`
- macOS/Linux 不传 Windows 专用参数；不启用曾导致管道异常的 `CREATE_NEW_PROCESS_GROUP`
- 对齐 F0005 跨平台 Popen 契约并补回归测试验证
- 定向兼容测试 16 passed；全量 358 passed in 355.49s

## 2026-07-29（F0030 Done）

- PARAMS 1.1 / IMPL 2.1：GP-024–027 从全局迁移到 S0–S3 各自 cognitive_parameters
- 玩家运行时按 seat 读取并记录 player_config_hash；旧 1.0/2.0 配置自动深拷贝迁移
- 设置窗口生成 112 个逐座认知字段，无全局认知页
- 全量 356 passed / 1 skipped；2/3/4 人各 10 局批跑通过
- 验收：`docs/status/F0030_ACCEPTANCE_2026-07-29.md`

## 2026-07-29（F0030 Approved）

- 用户确认逐玩家认知与目标参数迁移规格并要求实现；Docs-First 门禁开放

## 2026-07-29（F0030 Draft）

- 确认 GP-024–027 当前由四个 Humanlike 玩家共享，不能仅通过 UI 调整实现逐座独立
- 新增逐玩家认知与目标参数迁移草案：GP-001–023 保持全局，GP-024–027 移入 S0–S3
- 拟升级 PARAMS 1.1.0 / IMPL 2.1.0，并提供旧配置深拷贝迁移与审计兼容

## 2026-07-29（F0029 表单可用性修复）

- 底部按钮改为浅色背景/深色文字，修复 macOS 白底白字
- 所有可调数值显示 validator 的明确范围；自由文本显示长度/非空规则
- 遍历全部枚举型文本，生成 34 个只读下拉框；全量 353 passed / 1 skipped

## 2026-07-29（F0029 中文参数表单纠偏）

- 用户拒绝 JSON 文档编辑模式；设置窗口改为逐项中文表单、用途说明和范围提示

## 2026-07-29（F0029 Done）

- 大厅、主桌控制面板和 AI 座位窗新增 Humanlike v2 开关与参数入口
- 新增独立 Tk 全参数 JSON 编辑器，覆盖 GP-001–027、S0–S3、版本与 seed
- 保存复用严格 validator，支持备份、临时文件、fsync 与原子替换；所有变更下局生效
- 全量 352 passed / 1 skipped；compileall、GUI 启动与多尺寸大厅布局通过
- 验收：`docs/status/F0029_ACCEPTANCE_2026-07-29.md`

## 2026-07-29（F0029 Approved）

- 用户确认 F0029 规格并要求实现；Docs-First 门禁开放

## 2026-07-29（F0029 Draft）

### 文档 — Humanlike v2 UI 与参数设置

- 盘点确认：策略预设已存在，但大厅无全局开关，AI 窗口无独立开关和参数入口
- 新增 F0029 草案：大厅/主桌/AI 座位开关、完整 GP-001–027 与四座画像编辑、原子保存和下局生效
- 锁定字段只读且完整可见；不削弱 F0028 validator，不热更新运行中玩家

## 2026-07-29（F0028-6 Done）

### 实现 — 训练契约 v2

- 新增 635 项固定 codec/legal mask、PlayerView-only Observation v2 与 921 维 flat encoder
- env v2 支持固定整数动作、非法 raise/terminate、base/shaping/true-score 分离和 episode metrics；v1 默认兼容
- 新增 PlayerView 势能塑形与稳定批次指标聚合器
- 全量 347 passed / 1 skipped；2/3/4 人各 50 局零非法动作；obs p95 0.4917ms；v2/v1 1.0847×
- 验收：`docs/status/F0028_6_ACCEPTANCE_2026-07-29.md`

## 2026-07-29（F0028-6 Approved）

### 文档 — 训练契约 v2

- 新增 `docs/features/F0028_6_training_contract.md`
- 锁定 635 项固定动作空间、等长 legal mask、结构化 Observation v2、非法动作模式、奖励分解和回归指标
- v2 显式 opt-in，M11 v1 默认兼容；不引入训练框架或修改规则/协议
- 用户授权文档确认、实现和本地 Git 全自动执行，规格落盘即 Approved

## 2026-07-29（F0028-5 Done）

### 实现 — private Audit v1 与策略复演

- 新增 canonical SHA-256 hash 链、state/view/config hash、认知/RNG 快照、strict verifier 与 humanlike 多座位策略复演
- orchestrator 在换三张、定缺、出牌和响应动作前后记录审计；旧 steps snapshot 校正为 after-state
- 定向 19 passed；全量 338 passed / 1 skipped；2/3/4 人共 60 局、9294 决策零 replay mismatch
- audit+steps 写入开销 1.375×；verifier 6288.3 records/s
- 验收：`docs/status/F0028_5_ACCEPTANCE_2026-07-29.md`

## 2026-07-29（F0028-5 Approved）

### 文档 — 决策审计与确定性策略回放

- 新增 `docs/features/F0028_5_decision_audit_replay.md`
- 锁定 private Audit v1、canonical SHA-256 链、state/view/config hash、认知/RNG 快照和 humanlike 策略复演
- 保留 M10 steps/ReplaySession；不升级 APP/state/PlayerView/persistence/wire
- 用户授权文档确认、实现与本地 Git 全自动执行，规格落盘即 Approved

## 2026-07-29（F0028-4 Done）

### 实现 — 人类化有限认知

- 新增公开信息有限记忆、稳定 Top-K 注意力、持续 CognitiveState、人格/水平修正、计划惯性/重启、满意停止、有界噪声和模型思考时间
- `HumanlikeV2Player` 输出 DecisionTrace v2 并写入 RP-024–029；不读取 GameState/Oracle，不真实 sleep，不升级协议
- humanlike 定向 52 passed；全量 332 passed / 1 skipped；2/3/4 人各 50 局零策略崩溃/非法动作
- 50 局双跑及跨 PYTHONHASHSEED 摘要一致；p95 1.1968 ms；20 局相对 RuleAI 2.50×
- 验收：`docs/status/F0028_4_ACCEPTANCE_2026-07-29.md`

## 2026-07-29（F0028-4 Approved）

### 文档 — 人类化有限认知子规格

- 新增 `docs/features/F0028_4_human_cognition.md`，锁定认知状态、人格/水平、记忆衰减、Top-K 注意力、满意停止、有界噪声和思考时间
- mandatory、PlayerView-only、稳定 SHA-256 RNG、无真实 sleep 与不升级协议等边界明确
- 用户已授权“编写、确认并实现”及中途授权，因此规格落盘即为 `Approved`，实现门禁开放

## 2026-07-29（Human 换三张实体牌混用修复）

### 修复 — opening 牌面动作解析为实体牌

- 新增 `resolve_exchange_tiles()`：Human face action 按剩余副本最小 `tile_id` 确定性解析，AI PhysicalTile action 按精确实体 ID 校验
- `pending_exchange`、exchange offers 和目标手牌统一只保存 `PhysicalTile`，消除混合排序异常
- 新增 Human face + AI physical 混合换牌回归，验证进入定缺、全手牌实体类型和 108 张守恒
- 定向测试 **23 passed**；全量 **322 passed / 1 skipped**
- 修复后 GUI 复测进程正常启动/关闭且未复现类型异常；用户确认 MT-04 已进入定缺并正常出牌，原 Blocker 闭环

## 2026-07-29（F0028-3 快速人工验收）

### 测试 — MT-04 阻塞失败

- MT-01/02/05 通过；MT-03 用户确认 GUI 牌局正常，策略列表显示项尚未单独回报
- MT-04 Human 换三张失败：face `Tile` 与 AI `PhysicalTile` 混入目标手牌，排序报类型比较异常
- 根因定位至 `engine/opening.py` 的 face action → PhysicalTile 解析遗漏；本轮只诊断和记录，未修改业务代码
- 修订人工测试方案：M10 steps 是 private 全状态快照，不作为 PlayerView 泄漏判据
- 记录：`docs/status/F0028_3_MANUAL_QUICK_ACCEPTANCE_2026-07-29.md`

## 2026-07-29（F0028-3 人工测试方案）

### 文档 — 可执行人工验收清单

- 新增 `docs/testing/F0028_3_MANUAL_TEST_PLAN_2026-07-29.md`
- 覆盖 CLI/GUI、Human 混合局、旧 AI 回归、固定 game_id 重复性、2/3 人兼容、规则场景和信息隔离
- 定义快速验收、完整场景、证据目录、记录模板和阻塞放行规则
- 本轮仅新增测试文档和状态基线，未修改业务代码

## 2026-07-29（F0028-3 Done）

### 实现 — 只读 PlayerView v2 的确定性 humanlike_v2

- 新增七个 `players/humanlike/` 策略模块：上下文、belief、牌效、计划、候选、评价和玩家生命周期
- 注册选配 `humanlike_v2` 与大厅策略 preset；rule_ai/rule_ai_plus 默认行为不变
- orchestrator 全知 `_engine_state` 注入缩窄为 legacy RuleAI，humanlike_v2 无该通道
- DecisionTrace v1、RP 写入、mandatory 候选和稳定 8 位评分落地，策略不消费 RNG
- 全量 321 passed / 1 skipped；2/3/4 人各 50 局共 150 局、23392 次决策零策略崩溃/非法动作
- p95 2.87 ms，相对 RuleAI 2.222×；验收报告：`docs/status/F0028_3_ACCEPTANCE_2026-07-29.md`

## 2026-07-29（F0028-3 Approved）

### 文档 — 确定性 PlayerView v2 基础策略方案确认

- 用户确认 `docs/features/F0028_3_deterministic_player_view_policy.md`：`Review → Approved`
- 锁定可过胡、mandatory 候选、零 RNG、非精确 belief、内存 trace 和版本保持六项决议
- 实现门禁已开放；本轮仅更新文档，未修改业务代码或运行测试

## 2026-07-29（F0028-3 子规格）

### 文档 — 确定性 PlayerView v2 基础策略进入 Review

- 新增 `docs/features/F0028_3_deterministic_player_view_policy.md`
- 锁定只读输入边界、mandatory 候选规则、四分量评价、稳定同分键和内存 DecisionTrace v1
- 明确本切片不消费 RNG，不实现记忆、注意力、满意停止、噪声或持久化审计
- 规定 `humanlike_v2` 禁止读取 `_engine_state` / Oracle，并增加隐藏真值不变性与跨 `PYTHONHASHSEED` 门禁
- 状态为 `Review`；本轮仅修改文档，未修改业务代码

## 2026-07-28（F0028-2 Done）

### 实现 — 实体牌、schema 5、事件断言与 PlayerView v2

- 新增 `PhysicalTile(tile_id=0..107, face)`；固定 seed 的牌面级洗牌/发牌序列保持兼容
- GameState schema 4→5，reader 支持 1–5；persistence format 保持 1，wire protocol 保持 1
- 新增 schema 1–4 确定迁移、强类型 Meld/DiscardRecord、transit/winning 所有权区域和事件断言
- 新增 PlayerView version 2 白名单 builder；旧 UI/wire API 改由显式兼容投影生成，不再全状态删字段
- 新增 training-only `TrainingTruth`；普通 Observation 和座位窗口移除 oracle 手牌
- F0028-2 定向/全量与批量验收通过：**308 passed / 1 skipped**，2/3/4 人共 60 局守恒通过
- 性能：PlayerView v2 -23.8%；四 RuleAI 断言抽样 -2.2%（均通过门禁）
- 规格状态：F0028-2 `Approved → Done`；验收报告见 `docs/status/F0028_2_ACCEPTANCE_2026-07-28.md`

## 2026-07-28（F0028-2 Approved）

### 文档 — 实体牌与 PlayerView v2 方案确认

- 用户确认 `docs/features/F0028_2_physical_tiles_player_view_v2.md`：`Review → Approved`
- 锁定 GameState schema 5、persistence format 1、wire protocol 1、PlayerView version 2
- 锁定 Action 保持 face 表达并由 resolver 确定实体副本、legacy builder 兼容投影、oracle 移出 Observation
- 本轮只更新规格状态和跨机基线，未修改业务代码或测试

## 2026-07-28（F0028-2 实体牌与 PlayerView v2 子规格）

### 文档 — schema 5、所有权守恒、白名单视图与 oracle 分离

- 新增 `docs/features/F0028_2_physical_tiles_player_view_v2.md`，状态 `Review`
- 提议版本线：GameState schema 4→5；persistence format 保持 1；wire protocol 保持 1；PlayerView 新增版本 2
- 锁定实体 ID 编码、所有权区域/历史引用区分、强类型副露与弃牌记录、schema 1–4 确定迁移
- 定义原子事件边界断言、GP-021 八项可见性矩阵、legacy view 兼容投影和自动泄漏审计
- 明确训练 oracle 真值移出普通 Observation；本轮仅文档，未修改业务代码或测试

## 2026-07-28（F0028-1 配置与参数追踪基座）

### 实现 — GP/RP 强类型、兼容门禁、稳定 hash 与生命周期

- `configs/humanlike_v2/default.json`：完整 GP-001–GP-027 与四个中性 `normal/balanced` profile
- `configs/humanlike_v2/compatibility.json`：锁定 RULES 1.0.0 / PARAMS 1.0.0 / IMPL 2.0.0 组合
- `players/humanlike/config.py`：不可变配置、枚举/范围/权重验证、规范化 SHA-256
- `players/humanlike/runtime.py`：RP-001–RP-033 唯一注册及建局、事件、决策、终局生命周期
- `players/humanlike/traceability.py`：60 条参数到 schema、consumer、测试锚点的机械映射
- 文档状态：F0028 `Approved` → `In Progress`，F0028-1 `Done`
- 验收：F0028-1 定向 **12 passed**；最终提交全量 **291 passed / 1 skipped**（27.29s）；`compileall` 通过

## 2026-07-28（接管测试门禁修复）

### 测试 — F0020 旧断言与 macOS Tk 硬崩溃隔离

- `tests/test_human_wire.py`：将 M09 “最多 1 human”旧断言更新为 F0020 当前规格（2H/3H 允许，4H 拒绝）
- `tests/test_f0013_dirty_update.py`：对 macOS 显式 skip 会在 `tk.Tk()` 构造期 Abort 解释器的 GUI 用例；Windows/Linux 继续执行
- F0013/F0020 规格回写测试环境门禁和历史断言更新
- 验收：`compileall` 通过；全量 `pytest -q` = **279 passed / 1 skipped**（27.83s），无失败、无 Abort

## 2026-07-28（Git 本地基线恢复）

### 工程 — 以当前工作树重建 main/index

- GitHub 远端只读核对与临时 clone 均返回零 refs，默认 HEAD 为非法 `refs/heads/.invalid`
- 本地冲突 index 有 728 个条目，其中 675 个 blob 已缺失；dangling commit 父链/树也不完整，原历史不可恢复
- 损坏 `.git` 已可恢复地移至 `backup/git-metadata-corrupt-2026-07-28/`
- 恢复 `.gitignore`，排除 `.venv` / logs / backup / build / dist / releases 产物与 OneDrive 冲突副本
- 以当前经编译/测试审计的工作树重建本地 `main` 和 index；744 个文件进入恢复基线
- 创建恢复根提交 `90e7174`；`git fsck --full` 无损坏 ref/对象错误
- 恢复后验收：`compileall` 通过；278 passed / 1 failed / 1 deselected，失败仍为 F0020 旧 human 断言
- 未推送远端，未重建历史 `v0.2.1` tag

## 2026-07-28（Docs-First 一致性补齐）

### 文档 — F0028 审批后全局状态对齐

- `PLAN.md` 登记 F0028 Approved 主线和 Git/测试/F0028-1 执行顺序
- `docs/status/DOC_CODE_BASELINE.md` 登记 F0028 **Approved（未实现）**，并将 Git 措辞修正为本地 P0 损坏待远端核验
- F0026/F0027 正文状态与索引/代码基线统一为 `Done`
- 修正 `PLAN.md` 和 `docs/status/README.md` 的 `AGENTS.md` 链接大小写
- README 未将 F0028 列为已有功能：当前仅 Approved 而未实现，符合文档/代码事实

## 2026-07-28（F0028 Approved）

### 文档 — 人类化 AI v2 实现方案确认

- 用户确认 `docs/features/F0028_humanlike_ai_v2_implementation_plan.md`：`Review` → `Approved`
- 锁定：6 切片渐进实施；`humanlike_v2` 先作为选配 profile；实体牌 ID 为必做；首个 profile 为中性中等水平
- 本轮只更新规格状态、索引、changelog 和 LATEST，未修改业务代码
- 实施前阻塞仍是 Git P0 基线损坏和两项已知测试问题

## 2026-07-28（F0028 人类化 AI v2 实现方案）

### 文档 — 新规则/实现规范差距分析与分阶段方案

- 校验 `成都麻将AI人类化决策规则_v1.md` SHA-256，与 CDMJ-AI-IMPL 2.0.0 绑定值一致
- 新增 `docs/features/F0028_humanlike_ai_v2_implementation_plan.md`，状态 `Review`
- 对照现有 engine / PlayerView / F0010/F0011 / replay / training，拆分为 6 个可独立验收切片
- 决议方向：复用现有引擎，不新建平行 `src/`；`humanlike_v2` 先作为选配 profile；保留 2/3/4 人与现有 AI
- 本轮仅修改规格/索引/状态文档，未修改业务代码

## 2026-07-28（接管审计复核）

### 复核 — 异常与测试结论稳定

- Git 只读复核再次确认：`main` unborn、冲突 ref 非法、`v0.2.1` 对象缺失；未修改 `.git`
- `compileall` 与 `main.py --version` 通过
- 安全测试主体复跑：278 passed / 1 failed / 1 deselected（26.63s）；失败仍是 M09 旧 human 上限断言与 F0020 冲突
- 排除 `.venv` / `backup` 后盘点到 52 个 `*Moff的Mac Studio*` 冲突文件；未删除或合并
- 刷新 `docs/status/LATEST.md`；当前优先级仍是先恢复 Git 基线

## 2026-07-28（项目接管审计）

### 评估 — 仓库与测试基线

- 完成全目录接管审计：`docs/status/PROJECT_TAKEOVER_AUDIT_2026-07-28.md`
- 确认 P0：Git `main` / index / refs 被 OneDrive 冲突副本破坏，且部分 Git object 缺失；本轮未冒险修改 `.git`
- 确认测试基线：280 collected；排除 Tk 硬崩溃用例后 278 passed / 1 failed / 1 deselected
- 普通失败为 M09 旧测试与 F0020 多 human 规格冲突；Tk 用例在当前 macOS/Python 3.12 环境令解释器 Abort
- `compileall` 、CLI `--version` / `--help` 通过；未修改业务代码或删除任何文件

## 2026-07-26（F0027 · 安装程序修复）

### 修复 — MSI 安装失败 / 体验问题

| 问题 | 处理 |
|------|------|
| 中文乱码 | `Codepage=936` + GBK 源（`gen_msi_product_wxs.py`） |
| **错误 1925** 权限不足 | 去掉公共桌面快捷方式；`InstallPrivileges=elevated`；安装需 UAC |
| 无安装向导 | 增加 **WixUI_InstallDir** + **zh-CN** 界面 |
| ARP 无路径 | `ARPINSTALLLOCATION` 写入安装目录 |
| 版本显示 0.2.1.0 | ProductVersion 改为 **0.2.1** 三段 |

- 重打 MSI 后请 **以管理员身份** 安装验证
- 文档 WINDOWS_BUILD §8 补充错误码表

## 2026-07-26（F0027 · MSI 中文乱码修复）

### 修复 — 安装程序中文乱码

- 根因：MSI 字符串表为 **ANSI 代码页**；曾用 `Codepage=65001`/UTF-8 → 控制面板/开始菜单乱码
- 修正：`Codepage=936`（GBK）+ `Language=2052`；`gen_msi_product_wxs.py` 生成 **GBK** 编码 `Product.wxs`
- 请重新 `build_msi_windows.ps1` 后安装验证「成都麻将AI训练器」

## 2026-07-26（F0027 · Windows MSI）

### 实现 — WiX MSI 安装程序

- 规格 [`F0027_windows_msi.md`](features/F0027_windows_msi.md)：**Done**
- 脚本 `tools/packaging/build_msi_windows.ps1`：heat 采集 PyInstaller onedir → candle/light → `dist/msi/*-windows-x64.msi`
- WiX 3.14 binaries 首次自动下载至 `%LOCALAPPDATA%\wix314`
- 开始菜单快捷方式、per-machine Program Files、MajorUpgrade
- 本机产物约 **31.4 MB**；已上传 GitHub **Release v0.2.1**：`ChengduMahjongAITrainer-0.2.1-windows-x64.msi`
- 手册 WINDOWS_BUILD §8 · README 构建命令 · 索引 / DOC_CODE_BASELINE

## 2026-07-26（README · 分发说明）

### 文档 — 根 README 对齐 Windows 发布

- 功能「分发」改为 **Win x64 + macOS arm64** 双平台预构建
- 删除「Windows 打包（规划中）/ F0025 Draft」；改为 **预构建下载** + **本机构建**（Win/Mac 分节）
- 含 Release 附件表、Windows 解压示例、构建命令与日志路径

## 2026-07-26（F0025 · Release 发布）

### 工程 — Windows 包上传 GitHub Release v0.2.1

- 附件：
  - `ChengduMahjongAITrainer-0.2.1-windows-x64-PyInstaller.zip`（约 40 MB）
  - `ChengduMahjongAITrainer-0.2.1-windows-x64-Nuitka.zip`（约 42 MB）
- 页面：https://github.com/moff1022-git/chengdu_majiang_AItrainer/releases/tag/v0.2.1
- Release 说明已改为 **Windows x64 + macOS arm64** 双平台

## 2026-07-26（F0025 · 本机构建）

### 工程 — Windows 双包本机构建成功

- **PyInstaller**：`dist/pyinstaller/…/ChengduMahjongAITrainer.exe` · `--version` 0.2.1
- **Nuitka**：`dist/nuitka/pyinstaller_entry.dist/ChengduMahjongAITrainer.exe` · 冒烟通过
  （首次 MinGW 下载曾失败，重试后 gcc 15.2 缓存成功；脚本加 `--lto=no` 加速链接）
- 副本：`releases/windows/*-PyInstaller`、`*-Nuitka`（gitignore）

## 2026-07-26（F0025 Done · 实现）

### 实现 — Windows 打包（PyInstaller + Nuitka）

- **入口** `packaging/windows/pyinstaller_entry.py`（`freeze_support` + `main.main`）
- **spec** `packaging/windows/ChengduMahjongAITrainer.spec`（可选）
- **脚本** `tools/packaging/build_pyinstaller_windows.ps1` / `build_nuitka_windows.ps1` / `.bat`
- **本机副本** `releases/windows/README.md`（产物 gitignore）
- **单测** `tests/test_app_paths.py`：frozen 再入、`_MEIPASS`、Win 可写路径
- 规格 **Approved → Done**；手册/索引/基线同步

## 2026-07-26（F0025 Approved）

### 文档 — 确认 Windows 打包规格

- [`F0025_windows_packaging.md`](features/F0025_windows_packaging.md)：**Draft → Approved**
- 锁定：双脚本（PyInstaller + Nuitka）；Release 默认只挂 PyInstaller onedir x64；须在 Windows 构建
- 同步：`WINDOWS_BUILD.md`、features 索引、`DOC_CODE_BASELINE`、`LATEST`

## 2026-07-26（README 截图重刷）

- 重跑 `tools/capture_readme_screenshots.py`，刷新 `docs/media/readme/01–05` 与 `MANIFEST.json`
- 脚本：`--prefer-seat-grab` 改为 **子进程** 抓座位窗，避免 macOS 上 pygame/Tk 同进程 abort

## 2026-07-26（F0026 README 截图）

### 文档 / 工程 — README 功能界面五图

- 根 `README.md` **功能 → 界面预览**：大厅、主窗口（游戏中）、人类/AI 座位（游戏中）、计分窗口
- 图片：`docs/media/readme/01_lobby.png` … `05_result.png` + `MANIFEST.json`
- 脚本：`tools/capture_readme_screenshots.py`（主窗 pygame 真渲染；座位无屏幕权限时用资源拼合）
- 发版强制刷新：[`F0026`](features/F0026_readme_screenshots.md) · `VERSIONING` 步骤 4b · `DEVELOPMENT`

## 2026-07-26（仓库公开）

### 工程 — GitHub visibility

- 仓库由 **private → public**：https://github.com/moff1022-git/chengdu_majiang_AItrainer
- 历史 changelog 中「private」表述仅描述导入当时状态，以当前 **public** 为准

## 2026-07-26（F0025 Windows 打包 · 文档）

### 文档 — Windows 打包规格（Draft）

- 新增 [`docs/features/F0025_windows_packaging.md`](features/F0025_windows_packaging.md)：PyInstaller + Nuitka、onedir、`--seat-window`、须在 Windows 构建
- 新增 [`docs/packaging/WINDOWS_BUILD.md`](packaging/WINDOWS_BUILD.md)：前置条件、手动命令、验收 W1–W11、与 macOS 差异
- 交叉链接：`MACOS_BUILD.md` §7、`VERSIONING.md`、功能索引、`DOC_CODE_BASELINE`
- `.gitignore`：忽略 `releases/windows/**` 与本地 windows zip / `*.exe`
- **未实现**：`packaging/windows/*` 脚本（待 `确认 F0025` 后编码；验收须在 Windows 主机）

## 2026-07-26（文档审计）

### 文档 — 全面一致性修正

- 新增 [`docs/status/DOC_CODE_BASELINE.md`](status/DOC_CODE_BASELINE.md)
- 对齐 F0009 实装（选中不放大）、F0014 Done、M09 多 human 演进、状态索引与 README/PLAN/LATEST
- 远程：Release v0.2.1 已挂 zip；tag/下一步文档去陈旧项

## 0.2.1 — 2026-07-26

文档完善后的功能补丁发布（相对 **0.2.0**）。单一源：`version.py`。

### 新增
- **F0023** 主窗每轮开局掷骰定庄动画（与 `game_id` 可复现骰点一致）
- **F0024** 主窗出牌日志细化：摸/打/碰/杠/胡/计分、中文牌名、阶段与终局摘要、着色
- **F0022** 大厅/结算 UI 对齐人类窗（顶栏/底栏/卡片）
- **F0020** 2H+2AI / 3H+1AI 布局 B/D（若 0.2.0 文档日已含实现，本版一并纳入发布说明）

### 修复 / 体验
- 弃牌区**多行**显示 + **隐藏**右侧滚动条（滚轮仍可用）
- 座位窗胡牌横幅、副露中文类型、手牌选中金框
- 打包：`app_paths`、`--seat-window`、Nuitka 同步 `releases/macos/`

### 文档
- `docs/VERSIONING.md` 版本规则
- `docs/packaging/MACOS_BUILD.md` 打包
- 功能索引 F0020–F0024

### 打包
- 用 **0.2.1** 重打 PyInstaller + Nuitka macOS `.app`（产物本地 `dist/` / `releases/macos/`，不进 git）
- **GitHub Release** 已发布：https://github.com/moff1022-git/chengdu_majiang_AItrainer/releases/tag/v0.2.1
  - PyInstaller / Nuitka 各一 zip（arm64）

---

## 2026-07-26（续）

### 功能 — 主窗出牌日志细化（F0024）

- 解析完整 `score_events`：摸/打/碰/杠/胡/计分/行牌开始/流局
- 中文牌名（3万/9筒）；回合号 `T12`；终局胡序与得分摘要
- 侧栏按事件类型着色；容量 400
- 代码：`play_log_format.py`、`app._ingest_play_log`、`play_log_panel.py`

### 功能 — 主窗每轮掷骰定庄展示（F0023）

- 全员确认后、发牌前：主窗中心播放双骰动画（~2s）
- 骰点与引擎 `game_id` 派生结果一致；定格后显示庄家
- 日志：`掷骰 d1+d2=total → 庄家 Sx`
- 代码：`display/dice_fx.py`、`table_view`、`app` 时序；测：`test_dice_fx.py`

### 修复 — 座位窗弃牌多行显示

- **现象**：AI/人类「本家弃牌」像单行排，右侧裁切显示不全
- **修复**：按真实扩展区宽度多行换行（compact 牌面 + chrome）；多行时纵向可滚；标题显示行×列与张数
- 代码：`players/seat_window.py`；测：`test_discard_grid_multi_row_narrow_ext`
- **续**：去掉弃牌区右侧滚动条（仍可用滚轮滚动）

### UI — 大厅/结算对齐人类窗风格（F0022）

- 共享色板与分区：`display/ui_chrome.py`（顶栏 / 底栏 / 面板 / 主次按钮）
- `lobby_view`：设置卡片 + 固定底栏「开始」，小窗不遮挡
- `result_view`：摘要条 + 座位卡片网格 + 固定底栏「回大厅/再来一局」
- 测：`tests/test_lobby_view.py`、`test_result_view` 小窗

## 0.2.0 — 2026-07-26

首个按 [`docs/VERSIONING.md`](VERSIONING.md) 管理的应用版本（SemVer 单一源 `version.py`）。

### 新增
- **版本管理规则** `docs/VERSIONING.md`；`version.py`（`APP_VERSION=0.2.0`）
- CLI：`main.py --version` / `-V`
- UI：主窗标题、大厅副标题、座位窗标题栏显示 `v0.2.0`
- 打包脚本从 `version.py` 读取版本并写入 Info.plist

### 累计能力（相对项目早期）
- F0020 2H/3H 布局 B/D；F0021 macOS PyInstaller/Nuitka 打包
- 座位窗胡牌横幅、副露中文/手牌同尺寸、选中金框等

### 内部版本线（非 APP）
- 存档 schema：4 · format：1 · 座位协议：1

---

## 2026-07-26

### 工程 — 版本管理规则（v0.2.0）

- 权威：`docs/VERSIONING.md`；源：`version.py`
- 接入：`main.py`、`display/app.py`、`lobby_view`、`seat_window`、打包脚本
- 测：`tests/test_version.py`

### 工程 — macOS 打包（F0021 · PyInstaller + Nuitka）

- **文档**：`docs/packaging/MACOS_BUILD.md`、`docs/features/F0021_macos_packaging.md`
- **路径**：`app_paths.py`（资源根 / 可写 logs / 冻结子进程命令）
- **入口**：`packaging/macos/pyinstaller_entry.py`；`main --seat-window` 再入座位窗
- **脚本**：`tools/packaging/build_pyinstaller_macos.sh`、`build_nuitka_macos.sh`
- **实测产物**（arm64）：
  - PyInstaller ≈199MB：`dist/pyinstaller/ChengduMahjongAITrainer.app`
  - Nuitka ≈97MB：`dist/nuitka/ChengduMahjongAITrainer.app`
- 测：`tests/test_app_paths.py`

### 修复 — 座位窗胡牌提示 / 副露尺寸 / 中文类型

1. **胡牌无提示**：`hu_banner` 曾 `pack(before=meta_row)`，但横幅在 `mid`、meta 在 `op_status_fr`，跨父级 pack 静默失败 → 改挂 `op_info_fr`（状态栏下），始终可见；AI 窗同步显示
2. **AI 副露过大裁切**：固定 `tw=28` 在小 AI 窗溢出 → 副露牌面改与**手牌同宽**
3. **副露类型英文**：`pong`/`ming_gang`… → **碰/明杠/暗杠/加杠/吃**（`meld_kind_label`）
- 代码：`players/seat_window.py`；测：`test_meld_kind_label_zh`

### 修复 — 人类手牌选中无加框/高亮

- **现象**：点选手牌后几乎无选中提示（PhotoImage 铺满 Label，1px 边框不可见）
- **修复**：
  - 手牌固定外框预算（`ht=2` 面环 + `face_hold` 外环），选中/取消不回流
  - 选中：金黄双框 `#ffeb3b` + 暖金底；未选中边框与桌面同色
  - 有选中时其余牌略压暗，对比更强
- 代码：`players/seat_window.py`；测：`tests/test_seat_ui.py`

### 实现 — F0020 多人人类模式（2H/3H · Done）

- **规格** `docs/features/F0020_multi_human_modes.md` → **Done**
- **几何**：`plan_mode_D`（AI 顶带 + body 2×2）；`resolve_layout_mode(3,1)==D`；B 沿用
- **Hub**：`human_seats: list[int]`；play/watch 按列表；`start_all`/`ensure_all` 返回 `dict[seat, transport]`
- **App**：`_human_seats` 全链路；为每位 human 的 `HumanPlayerProxy.attach_transport`
- **Registry**：允许多 human（最多 3）；4H 拒绝
- **大厅**：预设「2人类+2AI」「3人类+1AI」
- **测试**：`tests/test_f0020_multi_human.py`；更新 `test_f0018_layout_geometry` / `test_players`

### 文档 — 2/3 人类模式（F0020 · 规格先行）

- **F0020** 初稿 Review → Approved → Done（同日）
- **UI 规范 v1.4.0**：布局 D；B 的 AI 顶对齐；`(3,1)→D`
- 索引：`docs/features/README.md`

### 工程 — 导入 GitHub

- 本地 `git init -b main`；初始提交 `b4020a4` + 进度文档 `b1fbb99`
- `.gitignore`：排除 `.venv/`、`logs/`、`backup/` 等
- **远程**：https://github.com/moff1022-git/chengdu_majiang_AItrainer （导入时 **private**；**2026-07-26 已改为 public**）
- `main` 已 push 至 `origin/main`（HTTP/1.1 重试成功）

## 2026-07-21

### 修复 — 初始布局 AI 遮挡（位置上移，不改 AI 高度）

- **现象**：AI 在上半区垂直居中 → 位置偏低，易压住 MAIN/人类
- **正确修复**：AI **保持原尺寸**（1080p 442×249）；**仅顶对齐 / 必要时上移**；禁止拔高 AI
- **MAIN↔人类**：完整模式同高（`_equalize_main_human_heights`）
- 代码：`display/window_geometry.py`；测：`test_window_geometry.py`
- 说明：曾误把 AI 拉高填满上半带，已按用户澄清回退尺寸

### 修复 — MAIN 比人类窗高出约数个标题栏

- **实测根因（macOS Quartz）**：client 同为 plan 高时 outer 同高；但 **SDL_VIDEO_WINDOW_POS 是内容顶**，且 **Dock 会把 pygame 主窗上推**（例：plan y=554 → 实际 outer y=444，差 ≈110px≈数个标题栏），Tk 人类窗仍在 plan y
- **修复**：
  1. 工作区扣除 **菜单栏+Dock**（AppKit `visibleFrame`）
  2. `set_sdl_window_pos` 在 darwin 将 Y **+ title chrome**，与 Tk outer 顶对齐
  3. 人类 client 锁定 + MAIN pin 对齐人类实际高度
- 代码：`window_geometry.py`、`seat_window.py`、`seat_ui_hub.py`、`app.py`

### 修复 — 主桌左右手牌大小/排列与上下一致

- 根因：左右扇区仅骰子高度，14 张竖排被迫缩小
- **画框手牌**：左右 `ZONE_HAND` 占满 TABLE 高；上下手牌在左右厚度之间内缩（四角不重叠）
- 绘制：四家同一 `draw_tw` / 居中逻辑（左右仍 ±90°）
- 代码：`display/main_interior.py` `_frame_hand_strips`；`display/table_view.py` 手牌绘制
- 测试：`test_main_hand_bands_frame_and_equal_face_size`

### 调整 — 取消手牌区滚动条 + 放大手牌

- 实时手牌区 **去掉右侧 Scrollbar 占位**（保留滚轮滚动）
- 手牌再放大：14 张占满区宽，左右仅小边距（非半张）

### 修复 — 手牌只能显示约 11 张

- 根因：选中框 chrome（ht=3+bd=2）使每格实际宽 > face_tw
- 修正：手牌 **compact 描边**；宽度公式计入 chrome

### 调整 — 手牌宽按 14 张 + 半张边距

- 人类/AI：按区宽算 face 宽，保证 **14 张一行**，左右约 **½ 张** 余量；间距仍为 0

### 调整 — 进张贴手牌上方 50% 透明 + 手牌间距 0

- 可听进张：`Toplevel` **alpha=0.5**，几何贴在手牌条 **正上方**
- 人类/AI 手牌 **gap=0**（牌面贴紧）

### 调整 — 进张浮动层 + 手牌贴底

- 可听进张：改为叠在手牌区上的浮动面板（有进张才显示），**不占流式高度**
- 手牌：固定在实时手牌区 **底部**（人类/AI 共用贴底逻辑）

### 调整 — 操作条单行 50/50（文案 | 按钮）

- OP_PLAY 底栏 **一行高**；左 50% 中文提示居左；右 50% 按钮按数量均分宽与间隔

### 调整 — 状态区严格 50/50 + 当前牌框 95% 高

- STATUS_L/R **place 各 50% 宽**（人类/AI 共用）
- 当前牌显示框：**高 = 状态区 × 0.95**，**w = h/1.4** 固定比例；牌面随框缩放

### 调整 — 操作条半高 + 状态区当前牌缩放

- **操作区**：OP_PLAY 内碰杠胡条高度约为原预算 **一半**（约 play 的 19%）
- **当前打出牌**：随 OP_STATUS 可用高宽缩放（去掉固定 64px）

### 文档 + 实现 — 座位窗 STATUS 20% / PLAY 60%

- **规范**：`HUMAN_WINDOW_LAYOUT` / `AI_WINDOW_LAYOUT` v0.2；F0016/F0017 摘要同步 — 当前状态 **20%**、实时手牌 **60%**（原 25%/55%）
- **代码**：`players/seat_layout_play.py` `STATUS_RATIO=0.20` `PLAY_RATIO=0.60`；示意脚本同改

### 修复 — 主窗条带居中 + 座位操作条/字号

- **主窗**：手/副露/弃牌严格在 ZONE 矩形内绘制；放不下则缩小牌面；网格在矩形内**居中**；`set_clip` 防溢出
- **座位操作条**：操作区占 OP_PLAY 更高比例；按钮紧凑换行；就绪/碰杠胡控件适配条高
- **字号**：人类基准 9/11、上限 12/14，避免完整窗内文字过大

### 修复 — 窗口外框不放大（完整模式尺寸）

- **约定**：完整模式外框 = 规范尺寸；**1080p 表为上限**（MAIN/人类 ≤885×498，AI ≤442×249）；大于 1080p 屏也用 1080p 窗尺寸，**不随分辨率放大窗**
- `plan_layout_abc` size_basis 封顶 1770×996 画布；`clamp_outer_size`；主窗/座位 min=max 锁定完整尺寸

### 修复 — 座位窗顺序/比例/精简模式

- **核查** `docs/status/UI_LAYOUT_ISSUE_CHECK.md`：按钮/设置顺序 = **程序 bug**（设计正确）；分区比例 = **程序未强制 place**；精简模式 = **实现缺失**
- **修正**：`seat_layout_play.compute_seat_interior` + `seat_window._apply_interior_geometry` — OP 67/33、STATUS/PLAY 25:55、EXT 30/70；**操作条在设置上方**
- **完整|精简**：标题栏切换；精简隐藏弃牌带 + 宽 50%/高 72%；完整恢复尺寸

### 实现 — F0019 窗内元素等比缩放

- **规格** `docs/features/F0019_interior_element_scale.md`：1080p 默认客户区为基准与 **minsize**（MAIN/人类 885×498、AI 442×249）；**布局比例不变**；`S=min(Cw/Cw0,Ch/Ch0)` 缩放牌/字/间距
- **模块** `display/interior_scale.py`；`layout.py` / 侧栏 / 控制面板 / `seat_window` 接入；手牌网格随 S 的 min/max_tw
- **测试** `tests/test_f0019_interior_scale.py`；F0013 脏更新保持控件复用

### 实现 — F0018 UI 布局改造（P0–P8）

- **多窗外框（D1）**：`layout_canvas` 85% 居中 + 2160p 封顶；`plan_mode_A/B/C`；`resolve_layout_mode`；Hub/App/`human_proxy` 应用 plan
- **主窗内部（D2/F0015）**：`main_interior` 80/20；DICE 同心；四扇区弃→副露→手条带；SIDE 积分/控制/出牌日志；`PlayEventLog` 环形缓冲
- **座位窗（D3/D4/F0016–17）**：play/watch **67/33**；扩展区折叠；人类 EXT=对手 HUD+弃牌；AI EXT=操作日志+弃牌；保留推荐/进张/就绪/脏更新
- **测试**：`tests/test_f0018_layout_geometry.py`；更新 `test_window_geometry` / `test_table_layout`；全量 **237 passed**（1 预存 subprocess 失败）
- **状态**：F0015/16/17/18 → **Done**；F0007 注布局由 F0015 取代；`PLAN.md` §10.3 短更；任务清单见 `UI_MODIFICATION_TASK_LIST.md`

### 备份 + 文档确认

- **完整项目备份（实现前）**：`backup/2026-07-21/` — 源码 + docs + assets 等 **2520** 文件（~333 MiB）；`BACKUP_MANIFEST.txt`；脚本 `tools/backup_project.py`（排除 git/venv/cache/嵌套 backup）
- **F0018 确认 / `Approved`**：用户确认后实现；见上节 Done

## 2026-07-20

### 文档 / 设计

- **UI 设计规范 v0.1（布局权威）**：`docs/design/UI_DESIGN_STANDARD.md` — 布局 A 横屏 / B 竖屏；配置 C1=1H3AI、C2=2H2AI；完整版占比与矩形算法；精简=完整宽 **50%**、高不变、**左锚向左收窄**；3H1AI 不做；本阶段不出图。F0014 几何移交本文
- **UI 设计规范 v0.2**：布局总面积 **85%** 居中画布；**720p/1080p/2160p** 横竖默认窗口像素表（C1/C2×完整/精简）；同角色尺寸一致；默认=最小可等比放大；**>2160p 默认封顶 2160p 表**
- **UI 设计规范 v0.3 布局示意图**：`docs/design/layout_schematics/` — A/B × 单人C1/双人C2 × 完整/精简 共 8 张（1080p 尺寸标注）
- **布局示意图 v0.3.1 重出**：删除旧版；`tools/gen_layout_schematics.py` 统一样式；**图片像素=实际设计画布**（A 1770×996 / B 996×1770），窗框=表列默认 px
- **布局规范 v0.4 / 示意图重出**：修正 A/B AI（及 MAIN/人类）尺寸不一致；**同档同配置跨布局窗像素必须相同**；1080p C1 AI=**586×349**、MAIN=**882×349**；删旧图后重生成 8 张
- **UI 布局规范 v1.0-draft 重设计**：`docs/design/UI_DESIGN_STANDARD.md` — **仅横屏**；布局 **A=3AI+1H / B=2AI+2H / C=0AI+3H / D=4AI+0H**；MAIN **25% 左下固定**；人类完整 **25%**（A 右下；B 右下+右上；C 右下+右上+左上）；AI 完整 **6.25%**（A/D 上半横均分，B 左上横均分）；旧竖屏与 85% 统一 h **废止**
- **UI 布局规范 v1.1-draft**：**取消布局 C**（0AI+3 人类）；In Scope 仅 **A / B / D**
- **UI 布局规范 v1.2-draft**：删除原 0AI+3H 布局 C 全部描述；原 **D（4AI+0H）更名为布局 C**；In Scope **A / B / C**
- **UI 布局规范 v1.3-draft**：**85% 布局画布**；**720p/1080p/2160p** 默认窗尺寸表（MAIN/人类 25%、AI 6.25% 相对画布）；A/B/C 共用外框；默认=最小可等比放大；>2160p 封顶
- **布局示意图 v1.3.1**：删除旧图；`tools/gen_layout_schematics.py` 生成 **9 张**（720/1080/2160 × A/B/C 完整）；图素=画布；统一样式；每窗标注尺寸
- **布局示意图已确认**（2026-07-21）：用户确认 `docs/design/layout_schematics/` 九图与 v1.3 尺寸表；实现须对齐
- **主窗口内部布局设计 v0.1**：`docs/design/MAIN_WINDOW_LAYOUT.md` + F0015 Draft — 左右 80%/20%；TABLE 中心方形掷骰区；四角连线分下/右/上/左四玩家区；SIDE 上积分状态 / 中开关 / 下出牌日志
- **人类窗口内部布局设计 v0.1**：`docs/design/HUMAN_WINDOW_LAYOUT.md` + F0016 Draft — 左操作 67%/右扩展 33%（可向左折叠）；状态 25%+手牌 55%+设置 2 行；扩展区上 HUD 30%/下本家弃牌 70%
- **人类窗口布局已确认**（2026-07-21）：F0016 设计 **Approved**；`HUMAN_WINDOW_LAYOUT.md` 标已确认；实现另令
- **AI 窗口内部布局设计 v0.1**：`docs/design/AI_WINDOW_LAYOUT.md` + F0017 Draft — 与人类窗同 67/33 与 OP 比例；无操作条；EXT 上 AI 日志 30%/下本家弃牌 70%
- **三窗内部设计确认 + 示意图**：F0015/F0016/F0017 设计 **Approved**；统一风格布局图 `docs/design/window_interiors/{MAIN,HUMAN,AI}_interior_1080p.jpg`（外框 885×498，区尺寸标注）
- **三窗 assets 完整示意**：`tools/gen_window_mockups_from_assets.py` 用 `assets/` 翠玉青云主题合成 `MAIN/HUMAN/AI_mockup_assets_green.jpg`（1770×996，真实牌面/按钮/头像/骰子/图标）
- **主窗设计 v0.2**：`MAIN_WINDOW_LAYOUT` 玩家区从里到外 **弃牌 → 副露(2 行牌高) → 手牌(1 行牌高)**；弃牌占扇区剩余厚度
- **F0018 UI→程序修改计划**：关联四设计（UI_DESIGN_STANDARD + MAIN/HUMAN/AI 内部）与代码文件/切片 P0–P8；`docs/features/F0018_ui_design_to_code_change_plan.md`
- **资源库约定确认**：运行时 UI 图形 **唯一根目录 = 项目 `assets/`**（`AssetManager` 默认；F0018 §1.3；契约 `assets/ASSETS.md`）
- **F0018 范围澄清**：本次改造 = **布局与 UI 呈现**（分区/搬迁/展示日志）；**不改** 规则、计分、AI 决策、合法动作；任务清单见 `docs/status/UI_MODIFICATION_TASK_LIST.md`
- **F0014 重写（Draft）**：assets 风格统一；保留设置；V1/V2 布局；制图硬规则 **平面 2D + 独立进程窗**
- **F0014 设计图套装 `flat_*`**：独立窗 5 张 + 布局 2 套于 `docs/design/f0014/`
- **F0014 元素全表**：对照 `seat_window.py` 列出 A1–A13 / B1–B18；完整模式全量；精简仅默藏本家弃牌(B16)+允许降密
- **F0014 T7/T8 同窗延展 + 图一体**：完整/精简不换窗只延展高度；组件包统一；有效图 `kit_style_strip` `win_human_modes` `win_ai_modes` `win_main` `layout_V1_unified` `layout_V2_unified`

### 流程规则

- **强制每步文档落盘 / 跨机基线**：每轮结束必须覆盖写 `docs/status/LATEST.md`；有实质交付追加 `changelog`；新 session 读序 LATEST → changelog → 相关规格。写入 `Agents.md` 规则 7、`docs/DEVELOPMENT.md` §2.2、`docs/status/README.md`

### 文档 + 实现

- **F0012 可听进张显示**：独立全宽「可听进张」条（32–40px 牌面、自动换行），修复原单元格内 mini≤22px 且按手牌宽裁切导致过小/不全；规格 `docs/features/F0012_seat_discard_recommend_marks.md`
- **F0013 座位窗脏更新 / 控件复用**：手牌·弃牌 layout 稳定时 `_update_tile_face` 原地改牌面；副露 meld_key 不变不重建；Hub `broadcast` 内容签名 + 60ms 节流；Win/Mac 共享逻辑。规格 `docs/features/F0013_seat_dirty_update.md`；测试 `tests/test_f0013_dirty_update.py`
- **F0013 实测修复**：对手 HUD `refs["seat"]` 被 Label 覆盖导致 `_update_opponent_hud_inplace` TypeError；改为 `seat_id` 存座位号；补 `_render_state` 手牌/弃牌/分数原地复用回归测

## 2026-07-13

### 实现

- **座位窗刷新防闪烁（加强）**：手牌指纹**剔除**对手分数/手牌数；对手 HUD 结构稳定时仅 in-place 改文字；选中高亮**不放大、不改 padding**；content width 缓存
- **F0012 座位窗推荐出牌标记**：`discard_recommend.py`；非听最多 3 张 / 听牌则全部可听张；角标序号；焦点显示进张（万筒条序）；**剩余张数在进张牌面上方**（不遮挡）；换三张按手牌索引；手牌 in-place 更新 + 进张条预留高度减闪烁
- **策略预设 + 座位窗「当前策略·S2」**：`configs/strategies/presets.json`、`rule_ai_plus.json`（导出 F0010-S 常量）；`players/strategy_presets.py`；`registry` 支持 `rule_ai_plus`（rule_ai + F0011）；观战座 AI 策略三选：规则 / 随机 / **当前S2**（下局生效）；CLI `--players rule_ai_plus,...`

## 2026-07-12

### 文档

- **set50 确认 S2 mid**：`set50-20260713_123456` mid **0.494**（与 set20 S2 0.493 齐）；set20「+1.7」含 S1 回弹，相对 S 前 set50 锚点约 **+0.5pt**，**不可按 +1.7 宣传**
- **F0010-S S2**：J4 连续 sh 恶化软罚×0.4；late S-TRUST（\|sh−target\|>1.5 衰减 sh 项）；S2 假近听×0.55；blend 保持 0.24。set20 overall **0.505** mid **0.493**（较 S1 +F1），MAE 2.20 **未达** ≤1.85
- **F0010-S S0+S1**：`Approved`；S0 诊断字段（MAE 相位/假近听/signed/best-hyp）；S1 late 假近听软杀+结构下限+采样/精炼/重生重试；set20 overall 0.501 late 0.512 MAE 2.16（MAE 门禁未达）；诊断 `docs/status/F0010_S_shanten_diagnostics.md`
- **F0010-S 向听质量计划**：`docs/features/F0010_S_shanten_quality_plan.md`

### 评估

- **Discard accuracy 指标**：`players/analysis/discard_accuracy.py`；`eval_hand_predict` 每决策写 `discard_acc.jsonl`；set20 top1 **0.438** / top3 **0.716** / expert 一致 **0.718**（随机弃牌标签，≈baseline 0.43，**非**文献人类 68–88%）；set50 top1 **0.440**；见 `docs/status/discard_accuracy_set20_set50.md`
- **F0010 set50（blend 0.76/0.24）**：`set50-20260713_100802` overall **0.511** / Top1 **0.435**；mid 0.489 / late **0.521** / deep 0.592；vs 0.70/0.30 set50 overall 持平、late +0.2pt；见 `docs/status/set50_comparison.md`
- **F0010-ML L3 blend 调参**：`LATE_BLEND` 0.70/0.30 → **0.76/0.24**；set20 overall **0.503** / late **0.506** / mid **0.491**
- **F0010 固定 set50 确认（0.70/0.30）**：`set50-20260712_154251` overall **0.512** / mid **0.495**；见历史对照
- **F0010 100 局评估**：seed=42；best F1=0.512，Top1=0.435，lift=+0.139；详见 docs/status/F0010_predict_accuracy_100games.md

### 实现

- **F0010-ML L3（排序）**：规格 `F0010_L3_ranking_plan.md`；late T=0.35 / mid T=0.50；MMR 0.55/0.40/0.15；late blend 0.70/0.30；`_dump_compliance_mult`。`--set 20`：overall 0.501 / Top1 0.422 / late best 0.504；rank1=best **45.4%**（L2 44.0%）；best/Top1 略低于 L2（噪声带），门禁 mid/early/deep 通过
- **F0010-ML L2（向听/结构）**：规格 `F0010_L2_shanten_structure_plan.md`；`_target_shanten` 经验表(C5b)、mid 终评关向听(G4)、late sh≥3/4 分档罚+听牌 bonus(G5)、late 结构 bonus×1.2(G1)。`--set 20`：overall **0.505**、mid **0.490**、late **0.513**（较 L2 前 +0.7/+1.1/+0.9pt）；向听 MAE≈2.16（未达 −0.2 目标，F1 优先不回滚）
- **F0010-ML M1（中期止血）**：`hand_predict.py` — mid 关闭配额(D6)、份额惩罚软化(C4c)、关高压色额外罚(C4d)、MC 均匀≥50%(H3)、prefer 强制双色且 attack 权重×0.5(B5/D3)；常量 `MID_*`。50 局对照：mid 0.454→0.456（微升，未达 0.48），late 0.539→0.542，overall 0.512→0.515，early 持平
- **F0010 固定评估集**：`configs/f0010_eval_sets.json` 嵌套 20⊂50⊂100 局，每条含 `game_id`+`play_seed`；`tools/eval_hand_predict.py --set 20|50|100`；`load_eval_set`
- **F0010-ML M2（斩色）**：`_dumped_suits` / `_streak_dumped_suits`；期望份额硬顶；采样降权；同 id 弃≥2 软罚×0.1；固定 `--set 50` mid best≈0.46、late≈0.52
- **F0010-ML L1（连续补摸）**：C1 失败→受限重生；补摸 prefer 保留色；late 连续权重 1.6/出牌 bonus 1.7；mut 10；J6；`--set 20` late≈0.515
- **F0010-DH 出牌–手牌关联**：排除定缺；前期 combo_assoc 高→降权；中后 tenpai_assoc（ukeire+向听差分，快分仅组合代理）；`--set 20` mid **0.488**、overall **0.506**
- **F0011 综合出牌顾问 A1–A6**：`integrated_discard.py`（S攻−S防+S废、remain_eff、F0010 听口危险、番 proxy）；`analyze_for_seat(use_f0011=)` / 环境变量 `F0011=1`；`tools/eval_f0011.py` 对照基线

## 2026-07-11

### 实现

- **F0010 对手牌形预测（Done）**：座位窗「对手牌预测」开关（默认关）；另三家各 **Top-5** 牌形+可信度%（由 10 改为 5 以减计算量）；全局出牌刷新；enabled 座 `oracle_hands` 算 tile F1；`hand_predict.py`
- **F0010 组数调整**：每家预测组数 10→**5**；采样 attempts 随 top_k 下调
- **F0010 算法 v2（Done）**：联合场景 `JointHandScene`（跨对手 remain 互斥）；出牌连续性 `prev_joints` + C1 打出必须在手；`StrategyBelief`（攻一门/打定缺/防守/快副露）；向听加权；座位窗缓存场景并展示场景#/策略/向听；`tests/test_hand_predict.py` 覆盖互斥与连续
- **F0010-L 预测日志与准确率分析**：座位窗每 tick 写 `logs/predict/{game_id}.jsonl`；`tools/eval_hand_predict.py` 无头评估；报告 `docs/status/F0010_predict_accuracy_analysis.md`（15 局：best F1≈0.53，Top1≈0.43，相对随机 lift≈0.16；主因排序差/早期信息少/向听误差）
- **F0010 v2.1 准确率修正**：去排序随机噪声；温度 softmax 校准 conf；弃牌时序/花色份额硬约束；结构+向听加权；连续性优先入 Top-K；开局粗粒度 UI；「牌张重合度」文案
- **F0010 v2.2 抬 F1**：相位自适应采样（早期均匀多样本 / 后期 beam+精炼+向听）；greedy MAP；花色 mode ensemble；MMR 多样 Top-K；15 局复评 early best F1 **0.41→0.48**，deep **0.60**，overall best≈**0.51**、Top1≈**0.44**

> **稳定性/多屏收尾权威摘要**（过程中曾试过 `_sdl2` 写坐标 / `display.quit` 重开等，**均因 macOS SEGV 回退**；以下为**最终保留行为**。）

### 稳定性与布局（最终状态）

#### 稳定性 / 崩溃修复

- **macOS 主程序 SEGV**：禁止使用 `pygame._sdl2.Window` 读/写位置尺寸；禁止中途 `display.quit()` 重开显示；主窗定位仅 `SDL_VIDEO_WINDOW_POS` + 主线程 `set_mode`
- **座位加载完主程序崩溃**：后台线程 `reassert_placements` 不得调用 `force_window_placement`/`set_mode`（`include_main=False`）；主窗 pin 只在 pygame 主线程
- **4AI 确认后 `UnboundLocalError`**：`work()` 内对 `players_spec` 赋值导致局部变量未绑定 → 使用 `effective_spec`
- **默认环境**：`main.py` 默认 `SDL_AUDIODRIVER=dummy`、`PYGAME_HIDE_SUPPORT_PROMPT=1`；启用 `faulthandler`；未捕获异常写 `logs/main_crash.log`

#### 窗口布局 / 多显示器

- **布局屏**：开局用 `detect_screen()`（光标/控制台当前屏）生成 `WindowPlan`；会话内锁定，ready 后不因点座位重测光标
- **主窗 pin**：仅主线程 `_pin_main_window`；座位 Tk 几何由 CLI + `set_geometry` 协议热迁移
- **玩家窗 Y 偏一整屏**：Tk 几何串禁止 `+x-y`（表示距底边）；`format_tk_geometry` 对负 Y 用 `+x+-y`；CLI `--y=-N`；映射后可做约一屏高度的漂移校正
- **座位 reassert**：macOS 只推 `set_geometry`，不碰主 pygame 窗

#### 开局 / Ready / 设置

- **4AI 开局**：先 `ready_request` 再组引擎；`_ready_wait_active` 期间禁止 poll 抢 ready；出错留在牌桌提示
- **座位设置条常显**：「自动开始」「AI 策略（规则/随机）」高对比色按钮（不依赖 Aqua Checkbutton 配色）
- **主窗封面「开始」**：取消 `btn_confirm` 背景图，改为绿底圆角实心按钮 + 白字

### 文档

- 当日复盘与终态：`docs/status/LATEST.md`、`docs/status/2026-07-11.md`
- **功能规格回写**：`F0001` §13、`F0002` §10、`F0003` §3.3.1、`F0004` 协议/流程/设置条、`F0005` §3.2/§10；`docs/features/README.md` 索引注解

### 主要代码路径

| 区域 | 路径 |
|------|------|
| 主 GUI / live | `display/app.py`、`display/lobby_view.py` |
| 几何 | `display/window_geometry.py` |
| 座位窗 / Hub | `players/seat_window.py`、`players/seat_ui_hub.py` |
| 协议 | `protocols/wire.py`、`protocols/subprocess_transport.py` |
| 入口 | `main.py` |

### 已知限制（未闭环）

- macOS 多显示器上 **SDL 对 `WINDOW_POS` 不一定总生效**，主窗可能仍留在系统默认位置；座位窗以 Tk 几何为准，二者偶发不完全重合
- 竖屏副屏负 Y / 复杂排列下仍可能需人工拖窗；漂移校正为 best-effort
- 未新增正式功能规格编号（本日以缺陷修复为主，changelog + status 为准）

## 2026-07-10

### 实现

- **4AI 开局白屏/回封面修复**：先发座位 `ready_request` 再组引擎；ready 等待期间禁止 poll 抢消息；出错留在牌桌提示而非静默回封面；竖屏工作区顶对齐减少窗口飞出
- **结算页累计得分**：顶部横幅展示各座累计分；玩家卡片标「累计 / 本局」分变（多轮会话）
- **座位窗设置面板**：标题栏「设置」可开关自动开始、选择 AI 策略（规则/随机，下局生效）；`seat_settings` 协议 + Hub 合并 players_spec
- **结算自动下一局**：四方座位均「自动开始」确认时，主窗可开「结算自动下一局」；结算页显示 3 秒后自动再来一局（多轮且未满轮数）；否则开关置灰无效
- **多局得分累计**：会话内 `_session_scores` 跨局结转；`PlayerGameRunner.starting_scores` 开局注入；座位窗局数/得分移到「当前打出」右侧以省竖向空间
- **主窗出牌区防重叠**：四家弃牌改十字分区（`Layout.river_area`），上下/左右河互不交叠，弃牌换行推进方向朝桌心
- **座位窗局数与得分情况**：显示「当前局数 第 r/n 局」与全员得分条（本家★）；`ready_request` 携带 `num_rounds`
- **4AI 模式座位窗 + 确认开始**：GUI 选 4AI 时同样启动 4 个 watch 座位窗，各窗点「确认开始」后才发牌（不再无窗自动开局）
- **全套牌面资源重制**：以 `tile_clean_{green,blue}.png` 为模版、`sample.jpg` 抠取花色，按原命名重生成万/筒/条 1–9 共 54 张（270×378）；脚本 `tools/regen_tiles_from_sample.py`
- **当前打出布局精简**：此牌剩余仅数字角标叠在牌面右下角；打出者+牌名合并一行（如「S2 打出 5万」）；牌墙总剩余单独一行
- **当前打出牌墙总剩余**：座位窗「当前打出」增加本局 `wall_remaining`（牌墙总剩余 n 张）；此牌剩余文案改为「此牌剩余」以免混淆
- **当前打出剩余张数**：座位窗「当前打出」显示该牌剩余/可见（本家手牌+全员弃牌+副露，同 analysis remain 模型）
- **F0009 座位窗选中放大 + 当前打出**：手牌选中金黄高亮并放大约 1.32×；新增「当前打出」面板展示 `last_discard` 牌面与打出者（本座/Sn）
- **F0008 结算计分牌积分明细**：`GameResult.score_events` + `build_score_ledger`；结算页按座位展示总分与每笔分变（自摸/点炮/杠/花猪/查叫，含番与对手）；终局标签与胡序摘要
- **座位窗对手状态 HUD + 本座胡牌横幅**：其他玩家以紧凑 HUD 显示定缺花色（色标万/筒/条）与是否已胡（胡序/自摸/点炮）；本座胡牌后分数行 + 红色醒目横幅「本座已胡·血战继续」；公共 view 保留 dingque/status/hu_order
- **玩家窗牌面最小尺寸 + 换行**：手牌默认最小宽 36px，禁止再缩小，一排放不下则加行；中区可滚动
- **AI 座位也需确认开始**：watch 默认 `auto_start=False`，与人类一样点「确认开始」（可勾选自动开始）
- **向听/策略面板遮挡底家手牌**：策略窗上移至底家手牌带之上；先画 HUD 再画手牌，牌面优先显示
- **F0007 主窗 UI**：手牌/弃牌统一最小 36px；随窗放大不缩小；放不下换行/换列；右侧控制面板（各座明牌、推理/策略/弃牌开关）；分区防遮挡
- **人类胡后“立刻结算”观感**：live 在人类离桌后 AI 全速打完剩余牌；`step_delay_ms` 节流行牌；主窗显示「血战继续·已胡/仍在打」；仅 `phase=finished` 才进结算
- **血战人类胡后卡死**：响应阶段缺 claim 时强制补 PASS 并 resolve；子进程 observation 非阻塞写入防管道堵死引擎；胡牌后座位窗立即提示血战继续
- **血战到底一胡不停局**：胡牌仅本座 `status=finished` 离桌；活跃≥2 时继续摸打；编排器/环境跳过已胡座位；座位窗提示「已胡牌·血战继续」
- **玩家窗牌面刷新闪烁**：observation 合并 40ms；手牌/布局指纹相同则跳过销毁重建；点选仅改样式；宽度未变不二次 relayout
- **AI 窗确认按钮不显示**：`_rebuild_action_bar` 曾对 watch 提前 return，跳过 ready UI；改为先画确认再进只读提示
- **主窗左右家牌面朝向中心**：`TableView` 左侧手牌/副露/弃牌旋转 -90°、右侧 +90°，牌顶指向桌心；间距按旋转后尺寸推进
- **座位窗牌面显示不全**：源图 ~270px 缩放过松 + 未计控件边距导致单行溢出裁切；严格缩放到布局 `tw`、`cell_extra` 换行、中间区可滚动
- **座位窗按钮底色（macOS）**：Aqua 下 `tk.Button` 忽略 `bg`，确认开始/操作钮改为 Frame+Label 实心底色（绿底白字）
- **F0006 玩家视窗响应式布局**：共享 `players/view/responsive.py`；手牌/弃牌/副露/按钮随窗宽缩放并换行；Tk 座位窗 `<Configure>` 防抖重排；PlayerView 多行手牌与 hit-test 一致
- **F0005 Windows/macOS 兼容**：`detect_screen` 按平台分发（Win32 / CoreGraphics macOS / pygame）；HWND 布局 API 仅 win32；主窗非 Win 用 pygame Window 定位；子进程强制 `encoding=utf-8` 且 `creationflags` 仅 Windows；座位窗 Mac 以 Tk geometry 为准
- **macOS 中文显示**：`draw_text` 改为优先加载本机 CJK 字体文件（STHeiti / 冬青黑 / Arial Unicode 等）并用探针拒绝「假匹配」的 Windows 字体名；座位窗 Tk 字体按系统可用族回退（PingFang SC 等），不再写死微软雅黑
- **座位窗改 tkinter**：多进程 pygame 在 Windows 上常丢 S1/S3 → `seat_window` 改用原生 Tk 窗，实测 4 座均 `placed=True`
- **点击开始卡死**：座位启动改后台线程；hello 尽早发送；主界面保持可绘
- **座位启动加固**：清继承的 `SDL_VIDEO_WINDOW_POS`；按 PID 强制置位；`window_ready` 协议
- **F0004 座位确认开始**：每局发牌前人类+AI 座位窗需点「确认开始」；「自动开始」复选框会话内记忆；`ready_request`/`ready` 协议 + `SeatUIHub.wait_all_ready`
- **F0003 游戏封面 / 保窗 / 副露**：主程序 Lobby 可设模式、换三张、轮数，点击开始才开局；一局结束不杀座位窗，Hub 复用；`PlayerView` 绘制碰杠副露；`EngineConfig.enable_exchange`；`human`/`play` 默认进封面；全量 **135 passed**
- **多显示器**：启动时检测命令所在屏幕（控制台/前台窗/光标 → MonitorFrom*），用该屏 `rcWork` 分辨率与原点布局全部窗口
- **座位窗网格布局 + 统一启动**：网格保证全在当前屏工作区内；Hub 一次启动 S0–S3
- **DPI/坐标修复**：逻辑像素工作区，禁止 DPI 混用
- **窗口布局权威流程**：`detect_screen()` → `plan_for_screen()` 共用 `window_plan`
- **F0002 布局补丁**：分区不重叠窗口几何（修 1440×900 下 S0/S3 被主窗挡住）；Hub 单座失败不中止；人类窗优先于 AI 观战窗启动
- **F0002 座位完整 UI**：人类窗可操作渲染加固；AI 座位 `watch` 子窗 + `SeatUIHub` 广播；主程序观战；`seat_window` 统一入口
- **Human 完整 UI**：`human` / `play` 含 human 时同时开主程序观战 + 玩家子窗口（后台引擎线程）；`--headless` 才纯无界面
- **Human 握手**：子进程 stdout 被 pygame 横幅污染导致 `JSONDecodeError` — 隐藏 banner、hello 提前发送、父进程跳过非 JSON 行
- **pytest 路径**：新增 `pytest.ini`（`pythonpath = .`）与 `tests/conftest.py`，避免在非根目录收集测试时出现 `No module named 'display'`（2 errors）
- **F0001 UI 窗口几何**（规格见 `docs/features/F0001_window_geometry.md`）：主窗居中、玩家窗四向、可缩放、初始化 ≤2K 工作区；`window_geometry` + layout/app/human 联动。**补记**：实现一度早于正式规格，已回写 Docs-First 权威文档
- **M11 Done**：`ChengduMahjongEnv`（类 Gym 5-tuple）+ `training/spaces.py` + 根 `README.md` + `tests/test_env.py`；全量 **114 passed**；路线图 M01–M11 收尾
- **M10 Done**：存档/加载/回放 + crash policy + CLI resume/spectate
- **M09 Done**：Human 子进程 + NDJSON transport + HumanPlayerProxy + 本家 GUI
- **M08 Done**：analysis pipeline + inference/strategy HUD + RuleAI 接入
- **M07 Done**：AssetManager + Lobby/Table/Result + InteractiveRunner + `main.py`
- **M06 Done**：BasePlayer + random/rule_ai + PlayerGameRunner
- **M05 Done**：ScoreService + Reward + JSONL
- **M04 Done**：血战行牌状态机 + legal_actions + Session
- **M03 Done**：向听 / 胡形 / 成都番型 + `fan_cap`
- **M02 Done**：换三张 + 定缺开局状态机
- **M01 Done**：牌/牌墙/game_id/掷骰定庄/发牌/状态 JSON
- **Spec v3 可实施性试点**：选择10个代表单元，补齐守恒、账本、注意、概率回退和PlayerView hash入口；定向10 passed，全量367 passed/1 skipped；形成选择、实施、规格反馈及JUnit证据。严格保持NOT AUDITED，等待High反馈是否修订后再继续。
- **SPEC-V3-3.0.1**：经用户批准解决试点8项High规格问题，新增兼容路径、可执行fixture、HEUR-019计算图、MODEL-001校准manifest、SCORE-001幂等事件、AUDIT-003字节公式和E3/E4两阶段门禁；Critical/High均0，不涉及业务代码。
- **SPEC-V3-3.0.2**：解决试点剩4项Medium，明确RULE-003查询版本、ALGO-001 region、TRAIN-003 codec及统一性能证据；10单元E3复验全通过，定向10 passed，全仓367 passed/1 skipped。
- **任务15批量开发准入审计**：结论FAIL。定向10/10与全仓367/1通过，但实现完成70%、关键分支55.7%、严格I/O完整0%、公式可执行70%、完整决策trace证据0%，且有10项High；4 INTEGRATED/3 TESTED/3 PARTIAL/0 AUDITED。
- **任务15复修重审 / SPEC-V3-3.0.3**：补齐公共I/O与88分支合同、真实hash/UTC证据、10单元生产接线和固定seed双跑。定向13 passed，全量370 passed/1 skipped，分支98.9%，轨迹复现100%；新准入结论PASS，9 AUDITED/1 INTEGRATED。
- **任务16 / SPEC-V3-3.1.0**：冻结`CDMJ-CONTRACTS 1.0.0`公共接口、数据可见性和版本策略，新增3份JSON Schema与16项契约测试；全量386 passed/1 skipped，45项锁定集hash验证通过。

### 文档

- 里程碑 **M11**：`Approved` → 实现 → **`Done`**（路线图闭环）
- 里程碑 **M10**：`Approved` → 实现 → **`Done`**
- 里程碑 **M09**：`Approved` → 实现 → **`Done`**
- 里程碑 **M08**：`Approved` → 实现 → **`Done`**
- 里程碑 **M07**：`Approved` → 实现 → **`Done`**
- 里程碑 **M06**：`Approved` → 实现 → **`Done`**
- 里程碑 **M05**：`Approved` → 实现 → **`Done`**
- 里程碑 **M04**：`Approved` → 实现 → **`Done`**
- 里程碑 **M03**：`Approved` → 实现 → **`Done`**
- 里程碑 **M02**：`Approved` → 实现 → **`Done`**
- 里程碑 **M01**：`Approved` → 实现 → **`Done`**
- 确立 **Docs-First** 开发规范：`docs/DEVELOPMENT.md`、`AGENTS.md`、收尾报告 §2.1
- 系统总设计基线：`PLAN.md`
## 2026-07-30 — MODEL-001最小模拟数据生成器实现

- 新增`training/model001/generate.py`及CLI，使用生产牌局引擎、合法动作与PlayerView-only四风格玩家生成模拟训练样本。
- 实现当前时点`cleared_dingque`/`dominant_suit`truth标签、终局`shape`restricted回填、game级稳定split、输出自动验证和失败manifest。
- 新增`tests/model001/test_generate.py`的12项专项测试与`docs/spec-v3/guides/model001_sim_generator.md`使用说明。
- 1000请求smoke实际生成1317条、2个完整牌局、非法动作0、manifest有效；全仓回归435 passed。未训练模型或修改MODEL-001审计状态。
## 2026-07-30 — MODEL-001正式模拟数据、训练与校准指标

- 完成smoke独立质量复核并生成10595条正式模拟样本；15局完整结束，game级train/validation/test切分无交叉。
- 新增`training/model001/train.py`，以PlayerView公开证据训练三个独立categorical Naive Bayes概率头；新增确定性和信息隔离测试。
- 产出模型artifact与Brier/log-loss/ECE报告；因Approved阈值缺失，明确不宣称校准通过，外部有效性仍未评估。
- 新增smoke复核、正式数据验收、模拟训练校准三份报告；全仓437 passed。MODEL-001审计状态未变。
## 2026-07-30 — PRE-DEV-FINAL-GATE-001独立终审

- 直接复核Task15—18、Locked/Frozen/批准决策、代码、测试、生成器和正式模拟数据，输出九项终审文件及修复提示词。
- 结论`NOT_READY_SPEC`：当前第一批B1-B缺少Approved具体三类Delta、接口影响和验收绑定，未授权任何编码范围。
- Task17 9/1/85/1历史基线保持；83条泛化SEM-PARAMETER全部SUPERSEDED；当前ACTIVE 24 semantic/12 test/6 evidence且仅覆盖B1-A。
- 同seed小生成逐文件hash一致；正式数据仅限SIMULATION；全仓437 passed、定向69 passed。
## 2026-07-30 — Codex CLI 多安装诊断

- 确认 WinGet 0.144.6 与 npm 0.146.0 并存，默认命令因 `PATH` 顺序解析到 WinGet 入口。
- 确认此前升级写入 npm 安装，未改变默认命令实际版本；本轮未执行升级、卸载或 `PATH` 修改。
## 2026-08-01

- 调整 Task 19 方案一：对已批准、口径明确的 T02 TRAIN-005 workload 门禁自动放行并恢复派发；保留真正新语义和安全冲突的人工门禁。
- W09 T19-D13 和 T19-H02 分别通过 clean-archive 独立审计（各 `P0/P1/P2=0/0/0`）；已自动进入 W10 T19-A01/H03 设计派发。
- W10 T19-A01/H03 设计包已通过独立复审（各 `P0/P1/P2=0/0/0`），已自动派发实现。
- W10 T19-A01 `5e6621a` 和 T19-H03 `eb3dcb6` 实现与证据已提交，已并行进入独立审计。
- W10 A01/H03 在 `760ad15` clean archive 均审计 PASS（各 `P0/P1/P2=0/0/0`）；W11 A06/H01/H08/X01 已自动准备设计派发。
- W11 A06/H08 和 H01/X01 设计独立复审均 PASS，已自动派发实现。
- W11 A06/H08 `bb53305` clean-archive 审计 PASS；H01/X01 实现与定向验证通过，但全量回归因执行环境禁止后台进程而保持验证阻断，未关闭 W11。
- W11 H01/X01 最终以前台纯归档全量 `831 passed, 1 skipped` 闭环，`9015b58` 审计 PASS；W12 H04/M01/X02 已自动派发。
- W12-W14 所有已派发批次均完成 clean-archive 独立审计，各 `P0/P1/P2=0/0/0`；已同步 orchestrator/runtime，待回写 tracker 96 单元汇总状态。
- T03 `a05dc684` 和 A02 `c69ba0e` 专属 clean-archive 审计 PASS；Task 19 tracker 现已汇总为 `96/96 AUDITED`。
- 消费 W09 H02/D13 独立设计复审 PASS 事件，将两项自动推进到 `IMPLEMENT/RUNNING` 并派发实现 Agent；同步 Root/Agent runtime 和 orchestrator 监控镜像。
## 0.3.0 — 2026-08-01

### 新增
- 完成 Task 19 全部 96 个单元的工程审计闭环。
- 增加 MODEL-001 分阶段开发方案：模拟数据用于工程开发，运行期 HUMAN 数据用于后续独立校准。
- 增加 MODEL-001 数据来源标记与数据集 validator。
- 增加 Task 19 状态监控、tracker reconciliation 和跨会话 runtime 状态同步。

### 内部
- Task 19 达到 14/14 waves、40/40 batches、96/96 AUDITED。
- 生成 `releases/v0.3.0/` 完整源代码归档。
# 2026-08-01

- F0036: 检查 batch 多线程 resume 逻辑，发现乱序完成时按 `len(rows)` 推导 pending 会重复/遗漏局；暂停性能基准，待修复后重测。
- F0036: 修复 batch 多线程按 game_id/index 的 resume 去重与 checkpoint；新增乱序 pending 回归测试，定向 `15 passed`，20 线程 smoke 验证通过。100 局正式基准因运行时间过长中断，结果可续跑。
- F0036: 根据实测首批耗时修正 batch ETA 基线：`SECONDS_PER_GAME=30s`；新增估算测试，定向 `16 passed`。
- F0036: 按修正 ETA 续跑 100 局 batch 至 `42/100` 后中断，保留 checkpoint；观察到 `rule_ai_plus` 长尾 P95 约 6.4 秒，完整基准仍待续跑。
- F0036: 第二轮续跑将 batch 推进至 `62/100` 后中断，checkpoint 保持可恢复。
- F0036: 第三轮续跑完成混合 AI batch `100/100`，总耗时约 `203.5s`，校验码 `5075D67FD5635D16`。
- F0036: batch JSON/Markdown/CSV 报告增加起止时间、总耗时、校验码和 humanlike_v2 座位人格预设字段；定向 `16 passed`。
- Design: 生成 Humanlike 雷达图参考样本 v1/v2，并将 22 张图片资产复制到 `assets/humanlike_radar_samples/`。
- Design: 按项目 green/blue UI 色板重生成 v2 双层雷达图；两层 60% 透明，并在每个轴顶点标注参数名和原始值。
- Design: 修正 v2 标签，改为显示 `normal_balanced` 预设的实际原始参数值；几何归一化仅用于绘图。
- Design: 将双层雷达填充透明度从 60% 降至 35%，改善重叠区域可读性。
- F0037: Humanlike 设置窗口实现双层雷达图、顶点点击高亮与人格预设切换动画。
- F0037: 调整雷达图为 S0–S3 2×2 网格同屏布局并缩小单图尺寸。
- F0037: 修复多雷达动画回调和透明填充；四座位下拉菜单、应用按钮与对应雷达图同面板显示。
- F0037: 降低外层/内层 stipple 密度并重绘内层边框，确保下层雷达在重叠区域可见。
- F0037: 修复设置窗口初始化仅绘制 S0，启动时为四个座位全部生成雷达图。
- F0037: 修复雷达参考环标量参数导致的 Tkinter `TypeError`。
- F0037: 新增 `humanlike_v2` 第13预设 `nonhuman_optimized`，主程序/设置窗口/性能测试统一接入，定向 `22 passed`。
- F0037: 修复 `nonhuman_optimized` 使用非法 style 导致批量全失败；改为合法 aggressive style，单局实战通过，预设测试 `6 passed`。
- F0038: 新增 Approved 固定测试编号牌局生成器方案，定义完整 10000 局及前缀数据集、可复现/公平性/审计合同和性能测试 test_id 绑定。
- F0038: 新增固定 test_id 牌局生成器第一版，生成 10000 局及 50/100/500/1000/2000/5000/10000 前缀数据集；smoke 成功。
- F0038: 增加公平性汇总、生成器回归测试（18 passed）及性能测试 `--test-id/--dataset-games` 参数校验。
- F0038: 独立生成并验证 `fairness-20260802-independent-001`：10000 局、七个前缀 hash 全匹配、四座硬约束 PASS；固定 deal 注入性能运行仍待完成。
- F0038: 补齐公平参数基础统计并重新生成 `fairness-20260802-independent-003`；硬约束 PASS、统计 `PASS_WITH_OBSERVATION`，定向 `18 passed`。
- F0038: 增加公平性 effect size、95% CI 与卡方描述统计；重新生成 `fairness-20260802-independent-004`，1000/10000 局 PASS。
- F0038: 完成性能测试固定数据集接入：`--test-id/--dataset-games` 读取并校验 deals artifact，使用固定 game_id 运行并写入 config 元数据；定向 `18 passed`。
- F0038: 增加可选 `--replay-fixed-deal` 完整复现开关；默认保持 game_id 高性能路径，开启后注入固定 deal。
- F0038: batch 交互模式增加固定测试编号与数据集规模选择菜单，支持从 `data/fairness/*/manifest.json` 选择。
- F0038: 修复 test_id 菜单触发时机，数据规模改读 manifest，并增加交互式复现方式选择。
- F0036/F0038: 参数选择 Ctrl-C/EOF 改为无 traceback 退出；报告增加 test_id、dataset hash/规模/路径和复现方式并绑定 verification code。
- F0037: 新增雷达点位动态说明浮动区，展示参数名称、实际值、范围和说明。
- F0037: 将点位说明改为选中点位下方的 Canvas 浮动标签，带背景和边界约束。

- F0036: 执行 batch 并发性能基准（100 局、20 线程、四 AI）；因单局耗时较高在 3/100 局中断，保留 checkpoint 与可恢复结果，校验码 `5075D67FD5635D16`。

- F0036: 新增无 UI AI 能力测试 runner，支持固定 game_id、四座 AI、断点续跑和胜负/得分/响应时间报告。
- F0036: 增加启动前预计耗时确认；取消返回参数选择界面。
- F0036: 交互式参数改为编号菜单选择，避免手工输入 AI 类型。
- F0036: 增加普通模式和能力评估模式的实时 ASCII 进度条。
- F0036: capability 模式增加已完成总局数/总局数显示。
- F0036: capability 汇总报告文件名增加测试日期和时间。
- F0036: 测试进度和报告增加按局数/固定 game_id/配置派生的唯一校验码。
- F0036: capability 模式增加动态已运行时间和剩余时间 ETA。
- 修复 STATE-004 response recovery：fallback PASS 改为原子事务，避免恢复失败留下部分 pending claims 并终止长测。
# 2026-08-01

- M20: 新增 Task 19 全功能独立回归测试规格，批准无人值守自动运行方案。
- M20: 新增独立自动测试调度器、失败重试、校验码、证据和时间戳报告输出。
- M20: 完成独立全量回归：498 passed, 1 skipped；96 units、14 waves、40 batches 均有独立结果证据。
# 2026-08-01

- F0037: 新增按 96 单元分类的 Humanlike v2 参数设置方案 Draft。
- F0037: 新增 96 单元到 60 个正式 GP/RP 参数组的完整反向关联矩阵。
- F0037: 为全部正式参数增加其在牌局生命周期中的作用步骤类别。
- F0037: 将完整作用步骤类别表直接合并进主方案文档。
- F0037: 根据 Task 19 权威参数注册表，为全部 60 个 GP/RP 参数补充类型、取值范围或运行态计算公式。
- F0037: 新增可再生的 277 行叶参数矩阵，覆盖四座默认值、类型/范围、作用步骤、权限、实现状态、96 单元消费者及 RP schema 缺口。
- F0037: 设计 12 种 GP-023 人格预设及 GP-025/026 联动，补充 search-depth 水平映射、custom 继承规则、UI 方案和验收测试，规格进入 Review。
- F0037: 完成 GP-023 12 种人格预设实现、设置窗口联动、custom 检测和 search-depth 有效上限；定向 32 passed，全量 506 passed/1 skipped，规格完成。
- F0037: 新增 RP-001～RP-033 叶级 schema 设计草案，明确统一 envelope、核心字段合同、可见性、分权写入、迁移和回滚门禁。
- F0037: 按批准规格开始 RP schema 实现：增加统一 envelope、canonical payload hash、篡改校验、旧裸 payload migration，并接入 RoundRuntime 写入校验。
- F0037: 增加 engine/player_policy/audit RP 分权写入 adapter，并接入 Humanlike 写入；全量回归 511 passed/1 skipped。兼容裸 payload 的最终切换和 22 个 RP 写入点仍待完成。
- F0037: 完成 RoundRuntime envelope 持久化与透明读取分离，迁移建局/事件/决策/终局路径，移除 Humanlike 裸 payload 覆盖；全量回归 511 passed/1 skipped。
- F0037: 完成 RP schema 验收：增加公共事件镜像、隐藏字段校验、幂等 envelope 和剩余槽位占位写入；定向 21 passed，全量 514 passed/1 skipped。
- F0037/Task20: 完成 RP schema 后续 1–5 项并执行独立全量回归；Task20 run `task20-20260802_000300`，96/96 units、14/14 waves、40/40 batches，校验码 `47C2B4BDBA3569F7`，`514 passed, 1 skipped`。
- F0037/Task20: 新增 RP-010、RP-018～RP-022 的公开投影派生，加入无上帝视野字段硬拒绝和边界测试；Task20 run `task20-20260802_001439`，校验码 `D99B1482DFA2B868`，`521 passed, 1 skipped`。
- F0037/Task20: 增强 RP-018 ukeire、RP-019 MODEL-001 posterior、RP-020 公开风险聚合，完成多座位隔离和 12 预设固定输入对比；Task20 run `task20-20260802_001956`，校验码 `64A377458C3A4C87`，`525 passed, 1 skipped`。
- F0037: 新增 RP envelope/payload 双视图及存档 round-trip/legacy migration；生成 12 预设 smoke 并明确动态 preset 注入尚未实现。全量回归 `526 passed, 1 skipped`。
- F0037: 增加 per-player humanlike preset 注入，12 预设 smoke 改为真实加载对应配置；新增注入测试，全量回归 `527 passed, 1 skipped`。
- F0037: 完成 RP 双视图 UI（envelope/payload/audit_only）及独立归档范围；全量回归 `527 passed, 1 skipped`。
- F0036: 新增 humanlike_v2 人格预设选择及报告记录；新增可选并发线程数 1/5/10/20/50/100。
- F0036: 完成全量回归与 1/5/10/20 线程并发 smoke；各线程档位 4 局均通过。
- F0036: 为 summary/report 的 JSON、CSV、Markdown 文件增加时间戳归档，同时保留无时间戳兼容指针。
- F0036: batch 模式新增按座位选择 humanlike_v2 人格预设，并将预设传入运行与报告。
- F0036: 修复 capability 人格预设记录与目标座位注入，避免预设列表嵌套。
- F0036: 调整 batch 座位配置交互，humanlike_v2 人格预设与对应座位同步选择。
- F0036: batch 模式接入 ThreadPoolExecutor 并发执行，修复选择 10 线程仍串行的问题。
