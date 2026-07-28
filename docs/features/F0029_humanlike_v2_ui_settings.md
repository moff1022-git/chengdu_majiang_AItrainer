# F0029 — Humanlike AI v2 界面开关与全参数设置

| 字段 | 值 |
|---|---|
| 编号 | F0029 |
| 状态 | `Approved`（2026-07-29，用户确认并要求实现） |
| 依赖 | F0028 `Done`；F0014/F0022 座位窗与大厅 UI |
| 应用版本 | 0.2.1（本规格阶段不变） |

## 1. 背景与目标

当前 `humanlike_v2` 已注册到策略预设，但大厅只有固定玩家组合轮换，无法直接全局启停；AI 座位窗虽能从策略列表选择“人类化AI·v2”，入口不够明确，也没有参数编辑界面。

本功能提供：

1. 大厅的 Humanlike AI v2 全局开启/关闭开关；
2. 主程序桌面可见当前启用状态，并可设置下局启停；
3. 每个 AI 玩家窗口的 Humanlike AI v2 座位开关；
4. 大厅和 AI 玩家窗口均可打开同一个“Humanlike AI v2 参数设置”窗口；
5. 完整查看与编辑 Humanlike 配置，校验后原子保存，下局生效。

## 2. 现状确认

- `configs/strategies/presets.json` 已包含 `humanlike_v2`。
- AI 座位窗的通用策略按钮会动态显示该预设，但没有独立的 Humanlike 开关或参数入口。
- 大厅 `_PLAYER_PRESETS` 仅包含 `rule_ai/random/human` 固定组合。
- `HumanlikeV2Player` 当前统一读取 `configs/humanlike_v2/default.json`。
- `players/humanlike/config.py` 已能严格校验 GP-001–027、四座 profile、seed 和配置哈希，可作为设置窗口保存门禁。

## 3. 开关语义

### 3.1 大厅全局开关

- 新增一行 `Humanlike AI v2：开启/关闭`，另有 `参数…` 按钮/点击区域。
- 开启：把当前玩家配置中的所有非 `human` 座位设置为 `humanlike_v2`；人类座位不变。
- 关闭：仅把当前为 `humanlike_v2` 的座位恢复为 `rule_ai`；已有 `random/current_s2` 不被覆盖。
- 切换玩家预设后，开关值由实际 `players_spec` 重新计算：全部 AI 座均为 humanlike 时显示“开启”，否则显示“关闭/混合”。
- 变更在下一局开始时生效；若桌面已有运行中牌局，不热替换玩家实例。

### 3.2 主程序桌面

- 主桌控制面板显示 `人类化 AI：关/开/混合`。
- 点击只修改下一局 AI 座配置；当前局保持原实例和配置哈希。
- 提示“下局生效”；不能影响 Human 座位。

### 3.3 AI 玩家窗口

- AI 窗口常显设置条新增独立 `人类化 v2` 开关，开启等价于该座 `ai_type=humanlike_v2`。
- 关闭时该座恢复为 `rule_ai`；通用“AI 策略”选择仍保留。
- 选择其他策略后 Humanlike 开关自动显示关闭；选择 humanlike_v2 后显示开启。
- 新增 `参数…` 入口；Human 操作窗口不显示或禁用这些 AI 专用控件。
- 座位设置仍通过 `seat_settings` 传回主程序，且只在下局合并到 `players_spec`。

## 4. 全参数设置窗口

### 4.1 形态

- 新增独立 Tk 窗口/进程 `players/humanlike/settings_window.py`，大厅和座位窗使用同一启动器打开，避免 Pygame/Tk 事件循环互相阻塞。
- 单实例：已有窗口时聚焦；并发打开或文件已变化时，保存前提示重新载入，不静默覆盖。
- 页面分组：`基础/规则 GP-001–010`、`番型与结算 GP-011–020`、`可见性与行为 GP-021–027`、`玩家画像 S0–S3`、`版本与哈希`。
- 支持滚动、搜索 GP 编号/字段、显示字段路径、当前值、合法范围/枚举和说明。

### 4.2 参数覆盖范围

必须展示 `default.json` 的全部叶子字段：

- 顶层：rule_version、parameter_version、implementation_version、ruleset、seed；
- `global_parameters`：GP-001 至 GP-027 的全部字段及嵌套 weights/patterns/relations/extensions；
- `players[0..3].profile`：name、level、style、peng/gang/big_hand preference、defense awareness、plan persistence、thinking speed；
- 当前规范锁定字段仍展示但只读，例如版本锁、固定牌组、禁止吃牌及其他 validator 锁定值。

“所有参数可设置”定义为：所有规范允许变化的字段可编辑；规范锁定字段完整可见、明确标注“锁定”，不得绕过 F0028 配置校验。

### 4.3 编辑与保存

- bool 使用开关，enum 使用下拉框，数值使用带范围校验输入，权重组显示合计值，数组/对象使用受控表格或 JSON 子编辑器。
- 按钮：`校验`、`保存`、`恢复默认`、`重新载入`、`导入…`、`导出…`、`取消`。
- 保存前调用 `load_config` 等价的完整校验并重新计算 config hash；失败时定位到具体字段，不修改磁盘文件。
- 保存采用同目录临时文件 + 原子替换，并保留一个 `default.json.bak`；不得写半截 JSON。
- 保存成功广播/提示“下局生效”；运行中 Humanlike 玩家继续使用开局时已加载的 immutable config。
- 导入只接受通过相同 validator 的 JSON；导出不包含隐藏状态、记忆或 RNG 运行时数据。

## 5. 配置路径与生命周期

- 权威配置保持 `configs/humanlike_v2/default.json`；不复制出另一套 UI 配置模型。
- 大厅、主桌和各 AI 窗口显示配置摘要：参数版本、短 config hash、文件更新时间。
- 创建 `HumanlikeV2Player` 时继续读取该路径；每局开始产生的 config hash 进入现有审计链。
- 若保存后下一局加载失败，阻止使用 Humanlike 开局并显示校验错误，不静默回退到其他 AI。

## 6. 协议与文件

新增：

- `players/humanlike/settings_window.py`：参数编辑 UI；
- `players/humanlike/settings_service.py`：加载、schema 元数据、校验、原子保存、备份和单实例启动；
- `tests/humanlike_v2/test_settings_service.py`；
- `tests/test_humanlike_ui_controls.py`。

修改：

- `display/lobby_view.py`：全局开关和参数入口；
- `display/app.py`：开关状态、点击处理、主桌状态与下一局语义；
- `display/control_panel.py`（以实际控制面板文件为准）：主桌开关；
- `players/seat_window.py`：座位开关和参数入口；
- `players/seat_ui_hub.py`、`protocols/wire.py`：必要的座位设置字段；
- `players/humanlike/config.py`：仅补公开校验/保存接口，不削弱现有约束；
- UI/状态/测试文档。

不升级 GameState、PlayerView、persistence 或 wire 版本；新增 wire 字段必须保持旧读取方忽略兼容。

## 7. 验收标准

1. 大厅可明确看到关/开/混合状态，可一键切换所有 AI 座且不修改 Human 座。
2. 主桌和每个 AI 窗口显示实际/下局状态；座位开关只修改对应座。
3. 大厅和 AI 窗口均能打开参数窗口，重复打开不会产生相互覆盖的多个编辑实例。
4. GP-001–027、四座 profile、顶层字段无遗漏；锁定项只读，可变项能编辑。
5. 非法数值、非法 enum、权重不等于 1、缺字段和额外字段均禁止保存并显示路径。
6. 合法保存后重新加载 hash 改变；下一局玩家使用新 hash，当前局 hash 不变。
7. 恢复默认、备份、导入、导出和并发修改保护通过。
8. 800×600 大厅和现有座位窗最小尺寸无控件遮挡；green/blue 主题可读。
9. 原有 rule_ai/random/current_s2、CLI 和 Human 窗口行为不回归。
10. 全量 pytest、compileall 通过，并完成人工点击验收。

## 8. Out of Scope

- 运行中热更新 Humanlike 玩家认知状态；
- 修改 GP/RP 语义、范围或成都麻将规则；
- 云端配置同步、账号级配置和远程参数服务；
- 为每局保存多套命名 profile 库（本期只编辑权威 default.json）；
- 自动推送远端或发布新版本。

## 9. 实现顺序

1. 参数 schema 元数据、校验与原子保存服务；
2. 独立参数窗口及单实例启动；
3. 大厅开关、参数入口及主程序状态；
4. AI 座位窗开关、参数入口与消息合并；
5. 自动测试、800×600/座位窗人工验收、状态文档。

## 10. 确认记录

用户于 2026-07-29 明确“确认并实现 F0029”，本规格据此更新为 `Approved` 并开放实现门禁。
