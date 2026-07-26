# 里程碑规格目录

每个里程碑 **一份** 规格文档，命名：`Mxx_<英文短名>.md`（如 `M01_tile_deck_game_id.md`）。

## 状态

`Draft` → `Review` → `Approved` → `In Progress` → `Done`

仅 **`Approved` 及之后** 允许编写该里程碑业务代码（见 [`../DEVELOPMENT.md`](../DEVELOPMENT.md)）。

## 路线图（与 PLAN.md §11 对齐）

| 编号 | 文档 | 摘要 | 状态 |
|------|------|------|------|
| M01 | [M01_tile_deck_game_id.md](M01_tile_deck_game_id.md) | tile / deck / game_id / 掷骰定庄 / state 序列化 | **Done** |
| M02 | [M02_exchange_dingque.md](M02_exchange_dingque.md) | 换三张 + 定缺阶段 | **Done** |
| M03 | [M03_shanten_win_fan.md](M03_shanten_win_fan.md) | 向听 / 胡形 / 成都番型 + fan_cap | **Done** |
| M04 | [M04_blood_battle.md](M04_blood_battle.md) | 血战状态机 + 一炮多响 + 合法动作 | **Done** |
| M05 | [M05_score_reward_jsonl.md](M05_score_reward_jsonl.md) | 计分 + Reward + JSONL | **Done** |
| M06 | [M06_base_player_ai.md](M06_base_player_ai.md) | BasePlayer + random/rule_ai + Session | **Done** |
| M07 | [M07_display_assets.md](M07_display_assets.md) | AssetManager + 主程序显示 | **Done** |
| M08 | [M08_analysis_hud.md](M08_analysis_hud.md) | analysis + strategy HUD | **Done** |
| M09 | [M09_human_subprocess.md](M09_human_subprocess.md) | human 子进程 + transport | **Done** |
| M10 | [M10_persistence_crash.md](M10_persistence_crash.md) | 存档 / 回放 / 崩溃策略 | **Done** |
| M11 | [M11_training_env_readme.md](M11_training_env_readme.md) | 类 Gym `ChengduMahjongEnv` + 项目 README | **Done** |

## 新建步骤

1. 复制下方模板标题结构，创建 `Mxx_*.md`  
2. 状态设为 `Draft`，写完后改 `Review`  
3. 用户确认后改 `Approved`，再编码  
4. 每轮相关工作结束后：对话内输出收尾报告（已完成 + 下一步清单），见 [`../DEVELOPMENT.md`](../DEVELOPMENT.md) §2.1  

模板字段见 [`../DEVELOPMENT.md`](../DEVELOPMENT.md) §4.1。
