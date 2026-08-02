# Task 19 进度更新政策

设计、审批、实现、测试、证据、缺陷、审计、合并、依赖/接口/计划变化均触发刷新。Terminal 0 校验 delta、状态转换、证据引用、commit、Task17 字段和幂等键后，原子重写完整 Markdown，增加 revision，重算摘要与 evidence snapshot hash；失败保持原文件。

Delta 必填：unit_id, previous_status, proposed_status, completed_gate, evidence_reference, test_run_id, commit_sha, blocking_change, next_required_action, generated_at, generated_by。
