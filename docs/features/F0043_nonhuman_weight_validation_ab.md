# F0043 Nonhuman 权重验证 A/B

Status: Approved

使用 `fairness-20260802-fair-004` 同一 1000 局，s0 保留 nonhuman 的候选容量、认知参数、碰杠偏好和其余配置，仅将 GP-026 决策权重设为 speed=0.35、hand_value=0.25、defense=0.25、flexibility=0.15。s1–s3 保持 novice_balanced。生成 games、steps、audit 和 F0042 完整参数快照，不覆盖 baseline。验收比较总分、胡牌、自摸、花猪、Top1，以及 104 个关键首分叉的实际恢复数量。
