# MODEL-001 smoke数据质量复核

日期：2026-07-30  
结论：**ACCEPTED_FOR_FORMAL_SIMULATION_GENERATION**

## 输入与结构

- 请求1000，实际1317，来自2个完整牌局。
- feature与label各1317条，ID集合相同且各自唯一。
- 四种风格样本数：conservative 291、balanced 342、aggressive 342、legal-random 342。
- 非法动作0；未发现禁用feature字段；同game无split交叉；manifest有效。

## 标签分布

- cleared：0=564，1=753。
- dominant：wan=338、tong=411、tiao=412、mixed=156。
- shape：standard=111、other=1206；未观察到seven_pairs、pure_suit、all_pongs。

## 判断

smoke证明生成、隔离、配对、复现和完整结束链路可用，允许正式生成。shape稀有类别覆盖不足不是生成器错误，但正式数据必须继续报告，并限制校准结论。

