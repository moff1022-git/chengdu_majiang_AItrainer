# F0030 — Humanlike v2 逐玩家认知与目标参数

| 字段 | 值 |
|---|---|
| 编号 | F0030 |
| 状态 | `Done`（2026-07-29，自动验收通过） |
| 依赖 | F0028、F0029 `Done` |
| 影响版本 | CDMJ-AI-PARAMS 1.1.0 / CDMJ-AI-IMPL 2.1.0（拟） |

## 1. 问题

现有 `GP-024` 记忆、`GP-025` 情绪/误差、`GP-026` 搜索/决策和 `GP-027` 全局目标位于 `global_parameters`。四个 `HumanlikeV2Player` 均从同一位置读取，因此设置窗口即使按座位显示人格，认知容量、遗忘率、随机误差、满意停止、决策权重和目标仍然共享。

用户明确要求：认知与目标不是所有玩家的整体参数，必须按每个玩家独立设置。

## 2. 目标模型

- `GP-001–023` 继续作为全局规则与对局参数。
- `GP-024–027` 改为每个玩家的 `cognitive_parameters`，每座必须各有完整四组参数。
- `PlayerProfile` 与该座认知参数共同构成 `HumanlikePlayerConfig`。
- 玩家实例只能读取 `players[self.seat]` 下的 profile 和 GP-024–027，禁止回读全局副本。

目标结构：

```json
{
  "global_parameters": {"GP-001": {}, "...": {}, "GP-023": {}},
  "players": [
    {
      "player_id": 0,
      "profile": {},
      "cognitive_parameters": {
        "GP-024": {}, "GP-025": {}, "GP-026": {}, "GP-027": {}
      }
    }
  ]
}
```

## 3. 版本和迁移

- `parameter_version` 升为 `CDMJ-AI-PARAMS 1.1.0`，`implementation_version` 升为 `CDMJ-AI-IMPL 2.1.0`；规则版本不变。
- loader 继续接受 1.0.0/2.0.0 旧配置：把旧全局 GP-024–027 深拷贝到四座，随后按新结构计算 config hash。
- 默认配置直接迁移到新结构，不同时保留两份权威值。
- compatibility 表同时登记旧读入组合和新权威组合；保存永远输出新结构。
- Audit 的 config hash 自然变化；Audit 版本不升级，记录中新增 `player_config_hash` 或等价逐座摘要以确认实际生效参数。

## 4. 代码调整

- `players/humanlike/config.py`
  - `GlobalParameters` 改为严格 GP-001–023；
  - 新增 `CognitiveParameters`，严格 GP-024–027；
  - `PlayerProfile`/新玩家配置绑定逐座认知参数；
  - 实现旧配置迁移和新结构 canonical hash。
- `players/humanlike/player.py`
  - observe/decide 全部改读当前座的 GP-024/025/026；
  - GP-027 作为该座局间目标输入，不再共享。
- `players/humanlike/traceability.py`：GP-024–027 路径改为 `players[i].cognitive_parameters`。
- `players/humanlike/settings_window.py`
  - 删除全局“认知与目标”页；
  - 在“玩家画像”中为 S0–S3 各建立“人格 / 记忆 / 情绪与误差 / 搜索与决策 / 目标”分组；
  - 每座可独立修改、校验和保存。
- 默认配置、兼容表、审计复演及相关测试同步迁移。

## 5. 不变量

- 四座认知参数对象不可共享引用；修改 S0 不得改变 S1–S3。
- 每座 decision weights 与 objective weights 分别必须合计为 1。
- `learn_hidden_information=false` 仍为逐座锁定值。
- 不改变 GP-024–027 的字段语义和取值范围。
- 相同新配置、game_id、seat 和 seed 仍须确定性复现。
- 旧配置迁移后四座行为与迁移前一致；只有用户主动制造座位差异后行为才允许分化。

## 6. 验收

1. 设置窗口不再出现全局“认知与目标”；S0–S3 均显示独立完整 GP-024–027。
2. 修改 S0 某参数并保存，S1–S3 原值和逐座 hash 不变。
3. 四个玩家实例的 trace/audit 能证明读取各自 seat 参数。
4. 旧 1.0.0 配置自动迁移，四座初值完全相同且行为摘要不变。
5. 新配置缺少任一座/任一 GP、权重非法或出现全局 GP-024–027 均拒绝保存。
6. config、cognition、policy、audit replay、settings 定向测试和全量 pytest 通过。
7. 2/3/4 人 Humanlike 批跑无非法动作，并验证不同座位参数确实产生可解释差异。

## 7. Out of Scope

- 运行中热更新；
- 每座使用独立配置文件；
- 修改成都麻将规则或认知算法含义；
- 自动生成最优参数。

## 8. 确认记录

用户于 2026-07-29 明确“确认并实现 F0030”，本规格据此更新为 `Approved` 并开放实现门禁。

实现与验收见 [`F0030_ACCEPTANCE_2026-07-29.md`](../status/F0030_ACCEPTANCE_2026-07-29.md)。
