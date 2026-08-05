# F0046 big_hand_preference=0.60 固定牌局 A/B

Status: Approved

使用 `fairness-20260802-fair-004` 同一 1000 局。s0 使用 F0043 已验证权重 speed=0.35、hand_value=0.25、defense=0.25、flexibility=0.15，并仅将 `big_hand_preference` 设为 0.60；其余 Nonhuman 参数保持不变。s1–s3 为 novice_balanced。保存完整 games、steps、audit 和参数快照，不覆盖既有结果。验收比较总分、胡牌、自摸、花猪、点炮及与 expert 的差异。
