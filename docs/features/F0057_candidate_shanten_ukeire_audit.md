# F0057 候选向听与有效进张审计字段

- 状态：Done
- 日期：2026-08-05
- 前置：F0054发现审计缺口

## 目标

在Humanlike v2候选trace中补充已有计算结果的原始向听、定缺张数、听牌有效进张牌面及按PublicBelief计算的公开剩余张数，使后续分析不再从压缩后的speed反推。只增强审计，不改变候选、评分、排序、随机、计划或动作。

## 字段

每个`decision_trace.candidates[].features`由四项扩展为：

- `shanten`: 弃牌后的原始向听；
- `dingque_tiles`: 弃牌后剩余定缺张数；
- `ukeire_faces`: `shanten==0`时的有效进张牌面，稳定排序；否则空数组；
- `ukeire_public_count`: 上述牌面在`PublicBelief.unseen_counts`中的总数；
- 保留speed、hand_value、defense、flexibility原值。

`RP-017`已使用`HandFeatures.to_dict()`，同步获得同口径字段。不得新增未来牌墙或对手暗手字段。

## 兼容性

trace schema保持version 2，新增可选字段，旧reader忽略即可；audit hash自然包含新字段。策略复演只比较动作，不应受影响。

## 验收

- 同一context改动前后selected action和四项评分完全一致；
- ukeire牌面稳定排序、公开计数正确；非听牌为空/0；
- 无隐藏信息字段；
- Humanlike v2全量回归通过。

## 批准记录

用户“执行任务1-6”明确要求执行LATEST第1项审计增强，并授权继续实现；规格限制为不改变行为，据此Approved。

## 验收记录

- `HandFeatures`与候选trace已增加原始向听、定缺张数、稳定排序有效进张和公开剩余计数。
- 定向审计/策略测试：`26 passed`；Humanlike扩大回归包含本功能并通过。
