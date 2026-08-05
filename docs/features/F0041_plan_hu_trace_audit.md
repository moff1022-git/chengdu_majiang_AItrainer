# F0041 计划坚持度与胡牌状态审计

Status: Approved

运行时 trace 必须记录 `primary_plan`、`inertial_plan`、`plan_age`、`plan_restarted` 及 GP-009 过胡语义摘要。计划坚持度仅可在同一计划且未重启时参与候选排序；HU mandatory 状态必须可由候选 trace 与 GP-009 复核，不能由满意阈值改变。
