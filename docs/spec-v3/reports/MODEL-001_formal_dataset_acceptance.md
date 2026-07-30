# MODEL-001正式模拟数据验收

日期：2026-07-30  
数据：`data/model001/model001-sim-v1`  
结论：**ACCEPTED_FOR_SIMULATION_DEVELOPMENT_WITH_LIMITATIONS**

## 验收结果

- 请求10000，完整运行15局后实际10595；`manifest.valid=true`。
- train 7685条/11局，validation 1359条/2局，test 1551条/2局；game级无交叉。
- feature/label ID唯一且集合一致；非法动作0；禁用字段0；四风格均覆盖。
- cleared：0=4345、1=6250。
- dominant：wan=2979、tong=3467、tiao=3177、mixed=972。
- shape：other=9776、standard=657、seven_pairs=162、pure_suit=0、all_pongs=0。

## 限制

test的1551条shape全部为other；validation仅有standard/other。因此数据可用于本地模拟开发和流程校准，但不能证明五类shape的泛化或外部有效性。未观察类别不得以零误差或高总体准确率解释为通过。

