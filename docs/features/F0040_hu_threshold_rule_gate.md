# F0040 胡牌候选与满意阈值规则门禁

Status: Approved

`satisfaction_threshold` 只适用于普通候选的 satisficing 停止，不得延迟、过滤或放弃合法胡牌。胡牌候选是否 mandatory 仅由 GP-009 当前响应类型的过胡许可决定：不允许过胡时强制胡；允许过胡时才可进入普通候选排序。新增测试覆盖候选容量为 1、低阈值和 response/discard 两类语义。
