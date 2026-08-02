# F0011 历史合同迁移说明

当前 `tests/test_f0011_integrated.py` 验证的是旧的 `strategy.rank_discards/F0011` 入口，与已确认的 0.3.1 人类推荐架构冲突。当前架构允许的推荐算法为：

- `humanlike_v2`；
- `rule_ai`；
- `rule_ai_plus`。

本轮不恢复旧 F0011 业务路径，也不篡改历史测试；将该测试标记为迁移候选。后续应新增当前算法合同测试，覆盖：算法选择持久化、下一次 discard 请求生效、合法弃牌集合约束、humanlike 人格预设传递和 hints 字段。
