# F0045 big_hand_preference 验证

Status: Approved

保持 F0043 已验证的决策权重（speed=0.35、hand_value=0.25、defense=0.25、flexibility=0.15）及其他 Nonhuman 参数不变，仅对 `big_hand_preference` 做离线反事实值 `0.80/0.60/0.40`。使用现有完整 audit 的候选特征，统计弃牌首选翻转、计划状态、花猪/胡牌局关联，不直接修改正式预设。只有离线结果显示稳定改善时，才启动固定牌局 A/B。
