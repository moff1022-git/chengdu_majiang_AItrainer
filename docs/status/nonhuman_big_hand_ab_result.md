# Nonhuman big_hand_preference=0.60 A/B

固定数据集 `fairness-20260802-fair-004`，1000 局，完整终局、steps、audit trace 均生成（1000/1000），无运行失败。仅 s0 临时设置 `big_hand_preference=0.60`；F0043 权重保持 speed .35 / hand_value .25 / defense .25 / flexibility .15，其他 Nonhuman 参数不变。

|座位|总分|胡牌|自摸|花猪|
|---|---:|---:|---:|---:|
|s0 Nonhuman big=.60|171|358|126|41|
|s1 novice|99|374|130|45|
|s2 novice|-215|335|114|49|
|s3 novice|-55|355|132|53|

对照磁盘中的权威 `games.jsonl` 后，F0043 权重 A/B 的 s0 同为 171 分、358 胡、41 花猪；Expert s0 为 282 分、358 胡、40 花猪。此前记录的 185 分属于过期统计，已纠正。big_hand 从 .80 降至 .60 后，1000 局终局指标完全相同，故“大牌偏好”不是剩余 111 分差距的主因；主要差异仍需从自摸/结算收益及动作时机继续定位。该实验不修改正式人格预设，旧数据保留。
