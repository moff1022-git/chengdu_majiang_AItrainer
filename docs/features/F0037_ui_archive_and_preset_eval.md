# F0037 UI、存档与预设评估补充

Status: Done

- UI/审计同时提供 envelope 元数据视图和 payload 兼容视图；`audit_only` payload 不进入 PlayerView。
- 存档写入 `F0037-RP-1.0` envelope；读取兼容旧裸 payload，并通过 migration 后 round-trip。
- 12 预设使用固定 game_id 清单和相同公开输入，报告参数、胜率、得分和响应时间；不使用隐藏真值标签。

实现说明：envelope/payload 双视图与存档迁移已完成。12 局 smoke 已生成，但当前 player registry 仍加载默认配置，尚不能把 preset_id 动态注入每局，因此该结果只证明 runner 可运行，不作为预设能力差异结论；正式能力评估需新增 per-player config override 规格。
