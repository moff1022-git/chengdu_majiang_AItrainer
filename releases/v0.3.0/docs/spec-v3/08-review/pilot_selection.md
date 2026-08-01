# Spec v3 规格可实施性试点选择

| 字段 | 内容 |
|---|---|
| 日期 | 2026-07-29 |
| 规范基线 | SPEC-V3-3.0.0 Locked |
| 目的 | 验证锁定规格能否直接指导实现、测试、运行证据与审计，不追求全项目完成 |
| 规模 | 10/96单元 |
| 授权 | 用户明确要求按规格实现试点并在完成后暂停 |

## 1. 选择结果

| 单元 | 类型 | 代表性 | 主要既有候选 | 试点价值 |
|---|---|---|---|---|
| RULE-003 | 确定规则 | 定缺强制出牌与合法性 | `engine/legal.py` | 验证规则规格能否形成稳定错误和纯裁决入口 |
| RULE-016 | 确定规则 | 隐藏信息公开白名单 | `protocols/player_view_builder.py` | 验证可见性规则和truth投毒门禁 |
| ALGO-001 | 确定算法 | 实体牌编码与守恒 | `engine/physical_tile.py`、`invariants.py` | 验证精确不变量、非法输入和属性测试 |
| ALGO-010 | 确定算法 | PlayerView投影 | `protocols/player_view_builder.py` | 验证算法与RULE-016的跨单元接口 |
| HEUR-019 | 启发式策略 | Top-K有限注意 | `players/humanlike/attention.py` | 验证非唯一动作、容量、方向效应与统计验收 |
| MODEL-001 | 概率模型 | 对手方向/牌型后验 | `players/humanlike/belief.py` | 验证概率归一化、校准接口、无truth输入与规则回退 |
| STATE-005 | 状态管理 | 不可变PlayerView载体 | `protocols/player_view_v2.py` | 验证不可变schema、序列化和越权拒绝 |
| SCORE-001 | 计分 | 分层账本与守恒 | `engine/score.py` | 验证每笔支付方—接收方守恒、幂等与原子性 |
| TRAIN-003 | 训练接口 | 固定动作codec与legal mask | `training/action_codec_v2.py` | 验证训练/生产合法动作一致、双射和隐藏隔离 |
| AUDIT-003 | 日志审计 | canonical hash链 | `engine/audit.py` | 验证篡改、乱序、截断、canonical和证据可复核性 |

## 2. 选择原则

- 覆盖RULE、ALGO、HEUR、MODEL、STATE、SCORE、TRAIN、AUDIT八类。
- 同时包含纯函数、有状态、概率、启发式、隐藏信息、零和账本和证据链。
- 选择已有迁移候选但尚无v3独立入口的单元，能检验规格是否足以指导“抽取/补全”，而不是只验证从零写简单函数。
- 不选择需要大规模模型训练或完整状态机重写的单元，避免把试点变成全项目实施。

## 3. 实施门禁

1. 实现前逐项读取对应Locked单元规格、父测试合同、细化TC、coverage和AC-01～14。
2. 目标代码必须位于开发任务卡建议位置，或在报告中给出经规格允许的适配理由。
3. 测试expected来自Locked规格/golden，不得从生产实现反向生成。
4. HEUR-019不强制唯一排序；MODEL-001必须测试概率与校准/回退边界。
5. RULE-016、ALGO-010、STATE-005、MODEL-001和TRAIN-003必须执行隐藏truth差分测试。
6. SCORE-001每个原子转移必须验证`ΣΔ=0`；AUDIT-003必须检出篡改/截断/乱序。
7. 只有实际入口、调用方、测试、运行输入输出、hash和指标齐备时才按审计标准赋E等级。
8. 试点结束后暂停；不扩展到其余86单元。

## 4. 明确不在本试点范围

- 不迁移完整STATE-004状态机、全部成都麻将房规或全部计分链。
- 不训练神经模型，不宣称真人相似、强度或E5。
- 不修改SPEC-V3-3.0.0 Locked定义；发现含糊时记录反馈，不静默补规则。
- 不批量生成其余86单元代码或测试。
