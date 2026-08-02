# F0028-3 人工测试方案

| 字段 | 值 |
|------|----|
| 对象 | F0028-3 确定性 `humanlike_v2` 基础策略 |
| 状态 | `Ready` |
| 日期 | 2026-07-29 |
| 前置版本 | 本地 main `56ebc5c` 或更新版本 |
| 预计耗时 | 快速验收 20–30 分钟；完整验收 60–90 分钟 |
| 不在本轮检查 | 人格差异、记忆、注意力、满意停止、随机失误（属于 F0028-4） |

## 1. 测试目标

人工确认以下用户可见结果：

1. `humanlike_v2` 可从 CLI 和 AI 策略选择界面进入游戏。
2. 换三张、定缺、摸打、碰杠胡、血战终局可完整运行。
3. AI 不提交非法动作，不崩溃或被 crash policy 替换。
4. 固定 `game_id` 下策略动作可重复。
5. `rule_ai`、`rule_ai_plus` 和 human 模式未被 F0028-3 破坏。
6. UI、日志和存档中没有显示其他玩家暗牌、牌墙顺序或 Oracle 信息。

人工测试不是自动测试的替代。开始前应确认自动基线仍为 `321 passed / 1 skipped`。

## 2. 环境与证据准备

### 2.1 macOS / Linux 命令前缀

```bash
cd <项目目录>
.venv/bin/python main.py --version
```

### 2.2 Windows PowerShell 命令前缀

```powershell
cd <项目目录>
.\.venv\Scripts\python.exe main.py --version
```

预期版本显示 `0.2.1`。人工证据建议保存到不入库的临时目录：

```text
manual_evidence/F0028-3/<日期>/
├── screenshots/
├── run-a/
├── run-b/
└── notes.md
```

每个用例至少记录：平台、Python/安装包版本、命令或操作路径、game_id、实际结果、通过/失败、截图或日志位置。

## 3. 快速验收集（发布前最低执行）

### MT-01 — CLI 注册与完整四 AI 对局

macOS：

```bash
.venv/bin/python main.py play \
  --players humanlike_v2,humanlike_v2,humanlike_v2,humanlike_v2 \
  --game-id manual-f28-001 \
  --headless \
  --save-dir manual_evidence/F0028-3/run-a \
  --save-every-decision
```

Windows 将解释器替换为 `.\.venv\Scripts\python.exe`，其余参数不变。

检查：

- [ ] 命令接受 `humanlike_v2`，没有 `unknown player type`。
- [ ] 对局自然结束，终局原因不是玩家异常中止。
- [ ] 控制台没有 `PolicyInputError`、`illegal action`、`replace_player` 或 traceback。
- [ ] 生成终局 save；开启逐步保存时生成 steps JSONL。
- [ ] 对局包含正常换三张、定缺和行牌过程。

失败判定：任何 AI 异常替换、非法动作恢复或进程非零退出均为阻塞缺陷。

### MT-02 — 固定 game_id 重复性

清空或分别指定 `run-a/run-b` 后，用完全相同参数再次运行 `manual-f28-001`。

- [ ] 两次终局分数、胡牌顺序和结束原因一致。
- [ ] 两份 steps JSONL 中的 decision action 序列一致。
- [ ] decision 原因均以 `humanlike_v2:deterministic:` 开头。

允许差异：文件时间、进程耗时、绝对路径。F0028-3 不要求思考耗时一致，因为本切片不输出模拟 sleep。

### MT-03 — GUI 观战与策略显示

```bash
.venv/bin/python main.py play \
  --players humanlike_v2,humanlike_v2,humanlike_v2,humanlike_v2 \
  --game-id manual-f28-gui-001 \
  --theme green \
  --step-ms 80
```

- [ ] 主窗口正常打开，无白屏、卡死或布局破坏。
- [ ] 四个座位均能持续摸打并进入结算。
- [ ] 换三张、定缺、碰/杠/胡事件能在现有日志区域正常显示。
- [ ] AI 策略选择列表中出现“人类化AI·v2”或“人类v2”。
- [ ] 选择 `humanlike_v2` 后提示下局生效，下一局确实使用该策略。
- [ ] green 主题通过后，以 `--theme blue` 再做一次启动冒烟。

注：F0028-3 没有新增专属认知 HUD；界面不显示 Q 分量不是缺陷。

### MT-04 — Human 对局回归

```bash
.venv/bin/python main.py play \
  --players human,humanlike_v2,humanlike_v2,humanlike_v2 \
  --game-id manual-f28-human-001 \
  --theme green
```

- [ ] Human 子窗口正常打开并进入准备/开始流程。
- [ ] 人工能完成换三张、定缺和至少 10 次出牌。
- [ ] AI 响应期间窗口不死锁。
- [ ] 人工可见内容仍只有本人手牌及公开信息。
- [ ] 完成一局或主动关闭时无未处理 traceback。

### MT-05 — 旧 AI 回归

分别运行：

```bash
.venv/bin/python main.py play --players rule_ai,rule_ai,rule_ai,rule_ai --game-id manual-rule --headless
.venv/bin/python main.py play --players rule_ai_plus,rule_ai_plus,rule_ai_plus,rule_ai_plus --game-id manual-s2 --headless
```

- [ ] 两种旧策略仍可识别并完整结束。
- [ ] 默认大厅/CLI 没有自动改成 `humanlike_v2`。
- [ ] rule_ai_plus 的现有分析/推荐能力没有因 `_engine_state` 注入收窄而报错。

## 4. 完整规则场景集

自然对局不保证一次覆盖所有分支。建议连续运行 10–20 局 GUI 或 headless，并在日志中勾选：

| 编号 | 场景 | 预期 |
|------|------|------|
| MT-06 | 换三张 | 每家恰好交换同花色三张，无非法回退 |
| MT-07 | 定缺 | 三门之一；同数量时稳定采用 wan/tong/tiao 顺序 |
| MT-08 | 清缺 | 手牌仍有缺门牌时，AI 不优先打非缺门弃牌 |
| MT-09 | 碰 | 可碰时可按效用选择碰或过，动作必须合法 |
| MT-10 | 明杠/暗杠/加杠 | 有合法杠时可评分选择；杠后补摸和计分正常 |
| MT-11 | 自摸胡 | 不可过的自摸胡作为 mandatory，不被候选上限裁掉 |
| MT-12 | 点炮胡/可过胡 | 按合法动作与效用决定，不能制造非法胡 |
| MT-13 | 一炮多响 | 多名响应者可正常完成，之后血战继续 |
| MT-14 | 玩家胡后退出 | 已胡座位不再收到决策，其余玩家继续 |
| MT-15 | 墙空/末家终止 | 正常结算，无卡在 response/draw/discard |

若自然批次未出现某场景，记录为“未覆盖”，不能误标通过；可保留到专用固定夹具或后续自动场景测试。

## 5. 信息隔离人工检查

### MT-16 — 公共视角检查

以 human + 3 个 humanlike_v2 开局：

- [ ] Human 窗口看不到三个 AI 的暗牌。
- [ ] 暗杠按当前 GP-021 只显示允许的公开粒度。
- [ ] AI 胡牌后的亮牌符合 GP-021，不提前显示。
- [ ] 日志中没有 `physical_hand`、`winning_tile_ids`、墙内 tile ID 列表或 `TrainingTruth`。
- [ ] decision analysis 如可见，只含 plan、belief_summary、candidates、selected_action 等基础 trace。

### MT-17 — 崩溃/泄漏关键字扫描

> 注意：`--save-every-decision` 的 `*.steps.jsonl` 是 M10 明确定义的 **private 全状态快照**，按设计包含墙顺序与暗牌。它只用于回放证据，应限制访问；不得将其当作 PlayerView 泄漏判据。下列扫描目标应限于非 private 运行日志、Observation/decision 导出与人工可见 UI。

对人工证据目录执行：

```bash
rg -n -g '!*.steps.jsonl' "Traceback|PolicyInputError|illegal action|replace_player|_engine_state|TrainingTruth|oracle" manual_evidence/F0028-3
```

预期：无异常或私有信息命中。若 `oracle` 只出现在测试说明文件中，应人工排除；运行日志出现则失败。

## 6. 2/3 人兼容检查

```bash
.venv/bin/python main.py play --players humanlike_v2,humanlike_v2 --game-id manual-f28-2p --headless
.venv/bin/python main.py play --players humanlike_v2,humanlike_v2,humanlike_v2 --game-id manual-f28-3p --headless
```

- [ ] 2 人和 3 人均能完成换牌、定缺、行牌和结算。
- [ ] 不出现固定访问不存在第 3/4 座位的错误。
- [ ] 分数结果包含且仅包含实际参赛座位。

## 7. 性能体感检查

GUI 四 AI设置 `--step-ms 0` 或较小值观察：

- [ ] AI 决策无肉眼可见的长时间冻结。
- [ ] 主窗口仍能刷新和响应关闭操作。
- [ ] 与 rule_ai 对局相比没有数量级变慢。

人工只做体感确认；定量权威仍是自动验收 p95 2.87ms、相对 RuleAI 2.222×。

## 8. 验收记录模板

```markdown
# F0028-3 人工验收记录

- 日期：
- 平台/系统：
- Python 或安装包版本：
- Git commit：
- 测试人：

| 用例 | 结果 Pass/Fail/未覆盖 | 证据 | 备注/缺陷号 |
|------|----------------------|------|-------------|
| MT-01 | | | |
| MT-02 | | | |
| MT-03 | | | |
| MT-04 | | | |
| MT-05 | | | |
| MT-06–15 | | | |
| MT-16 | | | |
| MT-17 | | | |
| 2/3 人 | | | |
| 性能体感 | | | |

结论：通过 / 有条件通过 / 不通过
阻塞缺陷：
未覆盖项：
```

## 9. 放行规则

- 快速验收 MT-01～05、信息隔离 MT-16～17、2/3 人兼容必须全部通过。
- MT-06～15 中本轮自然对局未出现的场景可标“未覆盖”，但任何已出现场景不得失败。
- 任一非法动作、策略崩溃替换、暗牌/Oracle 泄漏或固定 game_id 动作不一致均阻塞放行。
- UI 文案或非阻塞视觉问题可记录为后续缺陷，但必须附截图并评估是否影响操作。
