# Task 19 W01 合并所有者门禁批准记录

| 字段 | 值 |
|---|---|
| 日期 | 2026-07-31 |
| 批准者 | Project Owner |
| 批准指令 | `批准 W01 合并硬门禁推荐方案` |
| 执行模式 | ADR-0001 无人值守 Orchestrator |

## 1. RULE-015

- 批准向量：`A,A,A,A,A,A,A,A,A,A,A,B`。
- `RULE015-DEC-001～011` 选 A；`RULE015-DEC-012` 选 B。
- 性能门禁：冻结参考环境/夹具下 `P95 <= 5 ms`。
- 本记录批准设计语义；实现仍须先完成决策绑定和独立复核，不直接声称 AC PASS/AUDITED。

## 2. AUDIT-010

- 批准向量：`A,A,A,A,A`。
- typed node/edge rows。
- SHA-256 + external signature reference。
- offline budget：`P95 <= 250 ms / 10,000 edges`，peak `<= 256 MiB`。
- retention/backpressure：atomic reject + durable bounded spool。
- freshness：run start no earlier than audited commit time and same scope。
- 本记录批准设计语义；实现仍须先完成决策绑定和独立复核，不直接声称 AC PASS/AUDITED。

## 3. B2-A1 共享路径临时授权

为完成已 Approved `B2-A1-DESIGN-1.0.0` 的生产调用链和 AC-09/10，临时授权 Orchestrator 在 B2-A1 范围内修改：

- `engine/orchestrator.py`
- `engine/opening.py`
- `engine/blood_battle.py`
- `engine/legal.py`
- `protocols/player_view_builder.py`
- `players/humanlike/hand_analyzer.py`
- 新增 `tests/spec_v3/` 下 B2-A1 专用集成测试。

限制：

- 只可做 Approved semantic delta / AC / dependency call-chain 所必需的最小接线。
- 不得修改既有测试断言、Locked/Frozen、Task17 历史或其他单元语义。
- 共享路径改动必须独立列出，通过范围、回归、信息边界和独立审计。

## 4. 未授权

- push、发布、tag 移动、删除或历史重写。
- 降低 AC/E4/E5、性能、确定性或信息边界门禁。
- 将设计批准自动等同于实现通过或 `AUDITED`。
