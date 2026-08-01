# Task 19 重规划规则

触发：BREAKING_CHANGE、Locked/Frozen 冲突、接口/文件所有权冲突、新依赖、信息边界/确定性/性能失败、回归下降、E4/E5 不可归属、MODEL-001 门禁传播、进度与证据不一致或非法状态跳转。

暂停后生成记录：`replan_trigger_id, affected_batches, affected_units, current_evidence, required_decision, safe_resume_point, progress_tracker_impact`。Terminal 0 冻结相关 wave，未受影响批次只有在写路径和接口仍完全隔离时才可继续。
