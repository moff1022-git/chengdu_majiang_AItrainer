# MODEL-001模拟标签合同

状态：**Approved**  
版本：`MODEL001-LABEL-SCHEMA 1.0.0`  
来源：`MODEL001-SIM-LABELS 1.0.0`及Locked MODEL-001 §2、§4、§5、§10—12。

## 样本与时点

一行表示`decision event × active opponent`，主键为`game_id:decision_id:observer_seat:opponent_seat`。features在动作执行前从observer的生产PlayerView提取；cleared/dominant从同一时点restricted truth生成；shape在完整牌局结束后按同一opponent回填。

## Restricted label schema

| 字段 | 类型/枚举 | 来源 |
|---|---|---|
| sample_id | 非空稳定字符串 | event关联键 |
| cleared_dingque | `0|1` | CURRENT_HIDDEN_STATE |
| dominant_suit | `wan|tong|tiao|mixed` | CURRENT_HIDDEN_STATE |
| shape | `seven_pairs|pure_suit|all_pongs|standard|other` | EVENTUAL_TERMINAL_OUTCOME |
| label_source | 常量`SIMULATOR_TRUTH` | 生成器 |

manifest必须包含三个target元数据及`label_schema_version=MODEL001-LABEL-SCHEMA 1.0.0`。

## Shape唯一分类

终局先判断玩家是否形成可确认胡牌；否则`other`。已胡时复用生产胡牌/番型函数，按seven_pairs、pure_suit、all_pongs、standard、other顺序首个命中。暗手、胡牌上下文牌和副露必须来自同一终局truth；缺字段或无法重建为`other`，不得猜测。

## 物理隔离

features.jsonl禁止递归出现：`opponent_hidden_hand,wall_order,oracle,truth,label,future_event,other_seat_private_memory,raw_seed`。终局shape缓存和当前truth只存在生成器restricted内存/labels writer，不进入PlayerView或policy feature对象。

## Split

对UTF-8 `game_id`求SHA-256，以摘要转无符号整数后模100：0—69 train、70—84 validation、85—99 test。同一game_id只计算一次并复用于全部样本。
