# F0028-3 快速人工验收记录 — 2026-07-29

## 结论

**自动修复已通过，MT-04 人工复测结果待用户确认**。

MT-01、MT-02、MT-03 牌局运行、MT-05 通过；MT-04 首次执行发现的实体牌类型混用已完成代码修复与自动回归。修复后 GUI 已启动并正常关闭，日志未复现类型比较异常；是否实际完成换三张、定缺和至少 10 次出牌仍待用户反馈，快速人工验收尚未最终放行。

## 环境

| 项 | 值 |
|----|----|
| 日期 | 2026-07-29 |
| 平台 | macOS arm64 |
| Python | 3.12.13（项目 `.venv`） |
| Git 基线 | `c80ee0a`（含 F0028-3 实现 `56ebc5c`） |
| 临时证据 | `/tmp/f0028_3_manual_quick_20260729/`（不入库、不可跨机依赖） |

## 快速集结果

| 用例 | 结果 | 证据与说明 |
|------|------|------------|
| MT-01 CLI 四 humanlike_v2 | Pass | `manual-f28-001` 自然 `wall_empty`；分数 `[-6,6,-2,2]`；存档与 1.94MB steps 生成；无异常关键字 |
| MT-02 固定 game_id 重复性 | Pass | 双跑各 209 个决策且完全一致；动作摘要 `529c9502f97082ca61bc359db624e498371b71d5799b5a2410fd2351fbd1b614`；终局及胡牌序列一致 |
| MT-03 GUI 观战 | Partial Pass | 四观察窗创建/定位 `errors=0`；用户反馈“牌局正常”；策略列表中“人类化AI·v2”是否可见未单独回报 |
| MT-04 Human 混合局 | **Retest Pending** | 原 Blocker 已修复；定向 23 passed、全量 322 passed / 1 skipped；修复后 GUI 日志未复现异常，窗口操作结果待用户确认 |
| MT-05 旧 AI 回归 | Pass | rule_ai 分数 `[-3,1,2,0]`；current_s2 分数 `[2,0,-2,0]`；均自然 `wall_empty` |

## 阻塞缺陷分析

### 现象

Human 窗口在 exchange 阶段选中三张同花色牌后，点击“确认换牌”或“自动换牌”，界面无法进入定缺。主进程记录：

```text
[live] game error: '<' not supported between instances of 'Tile' and 'PhysicalTile'
```

### 根因链

1. `players/seat_window.py::_build_exchange_action()` 从 Human 可见的 face ID 构建 `Action(EXCHANGE, tiles=tuple[Tile])`。
2. `engine/orchestrator.py::_decide_and_opening_exchange()` 接收后将 face-level `Tile` 直接交给 `submit_exchange()`。
3. `engine/opening.py::submit_exchange()` 仅做牌面 multiset 校验，没有把 Action face 解析为该玩家手中的具体 `PhysicalTile`。
4. AI 提交路径使用手牌对象生成合法动作，携带 `PhysicalTile`；Human 路径携带 `Tile`。
5. `_resolve_exchange()` 将两类对象加入目的手牌，`PlayerState.sort_hand_inplace()` 排序混合列表时发生反向比较失败。

### 归属与影响

- 归属：F0028-2 实体牌迁移的 opening/Human 边界遗漏。
- 影响：任何包含 Human 且启用换三张的正常对局均可能被阻塞。
- 不影响：纯 AI humanlike_v2、rule_ai、current_s2 headless 路径。
- 严重性：P0/Blocker（核心 Human 对局无法开始）。

### 建议修复

- 在引擎 opening 权威边界新增 face action → 本手具体 PhysicalTile 的确定性解析；按手牌稳定顺序/实体 ID 选择副本。
- `pending_exchange`、offers、目标手牌始终只保存 `PhysicalTile`，禁止混合类型进入 GameState。
- Human 手选和自动换牌共用同一解析器。
- 增加集成测试：Human wire 返回三个 face `Tile`，其余 AI 返回 `PhysicalTile`，换牌后四手仅含 PhysicalTile、108 张守恒、phase 进入 dingque。
- 修复后重跑全量测试、2/3/4 人守恒，并重新执行 MT-04。

## 测试方案修订

`--save-every-decision` 生成的 M10 steps JSONL 是显式 private 全状态快照，按设计包含墙顺序和各家暗牌，不能用它判定 PlayerView 泄漏。信息隔离人工检查应针对：

- Human/AI 窗口实际显示；
- PlayerView/Observation 输出；
- decision analysis / 策略 trace；
- 非 private 的运行日志。

steps private 快照只能用于确定性/状态回放证据，必须限制访问，不应作为对外玩家视图。

## 放行条件

1. 修复 opening face→PhysicalTile 解析并补回归测试。
2. 全量自动测试和牌守恒门禁通过。
3. 重新执行 MT-04：Human 可完成换三张、定缺及至少 10 次出牌。
4. 补充人工确认 MT-03 策略列表显示项。

## 修复记录

- `engine.exchange.resolve_exchange_tiles()` 在 opening 权威边界把 Human 牌面动作确定性解析为本手具体实体牌；牌面重复时选择剩余副本中最小 `tile_id`。
- 已携带实体牌的 AI 动作按精确 `tile_id` 校验归属，不重新映射副本。
- `pending_exchange`、结算 offers 与目标手牌均只保存 `PhysicalTile`。
- 新增 Human face + AI physical 混合路径回归，换牌后验证所有手牌实体类型及 108 张状态守恒。
- 自动验收：定向 **23 passed**；全量 **322 passed / 1 skipped**。
- GUI 复测进程 `manual-f28-human-retest-001` 已正常启动和关闭，未输出原类型比较异常；人工操作结论待用户确认。
