# F0059 人类推荐F0011退役测试合同

- 状态：Done
- 日期：2026-08-05

## 目标

对齐用户已确认的人类出牌推荐算法合同：设置窗口仅允许`humanlike_v2`、`rule_ai`、`rule_ai_plus`；历史`strategy.rank_discards / F0011`开关不得重新接入人类推荐pipeline。

## 范围

- `analyze_for_seat(..., use_f0011=True)`作为遗留兼容参数保留，但结果必须仍为`use_f0011=False`。
- 三种当前推荐算法均不得启用F0011标志。
- 不删除F0011历史实现、文档或`rule_ai_plus`玩家自己的旧策略配置；本功能只修正人类推荐测试合同。
- 不改变引擎规则、Humanlike决策或AI玩家对局行为。

## 验收

- 旧显式F0011 pipeline测试改为退役断言；
- 当前三种推荐算法合同测试通过；
- 全仓回归通过。

## 批准记录

用户此前明确要求取消人类推荐`strategy.rank_discards / F0011`并改为三种已有AI算法，本轮“执行任务1-4”明确授权修正过期测试，据此Approved。

## 验收记录

- 遗留`use_f0011=True`调用确认不能重新启用人类推荐F0011。
- 全仓按四片执行：`512 passed, 1 skipped`。
