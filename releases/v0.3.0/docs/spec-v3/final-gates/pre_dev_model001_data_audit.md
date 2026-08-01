# PRE-DEV-FINAL-GATE-001 — MODEL-001数据审计

结论：`ACCEPTED_FOR_SIMULATION_DEVELOPMENT_WITH_LIMITATIONS`，不是最终校准发布或真实玩家验证。

- requested=10000；actual=10595；manifest未单列eligible_samples，结构验证后可配对eligible=10595；excluded=0；15个完整game。
- train=7685/11局、validation=1359/2局、test=1551/2局，同game无跨split。
- cleared：0=4345、1=6250；dominant：wan=2979、tong=3467、tiao=3177、mixed=972；shape：other=9776、standard=657、seven_pairs=162、pure_suit=0、all_pongs=0。
- feature/label各10595个唯一sample_id且集合相同；label_source全部为SIMULATOR_TRUTH；未发现禁用字段或未来/终局字段进入policy_features。
- ruleset hash=`f60c5720...dd5aba`；generator=`model001-sim-v1`；feature schema=`MODEL001-FEATURE-SCHEMA 1.0.0`；label schema=`MODEL001-LABEL-SCHEMA 1.0.0`。
- `validation_scope=SIMULATION`；`external_validity=NOT_EVALUATED`。
- 文件SHA-256：features=`8906f481...c6dc`；labels=`878f6c35...25bf`；manifest=`166f4d4e...1b6e`。
- 唯一ID不是复制扩充证据；但每个decision×active opponent天然共享同一可见事件。按game切分避免跨集合泄漏。
- 类别≥200门禁不满足：seven_pairs仅162，pure_suit/all_pongs为0。数据/代码release manifest亦未冻结文件hash、eligible_samples和generator code hash。因此不得宣称MODEL-001最终校准通过。

