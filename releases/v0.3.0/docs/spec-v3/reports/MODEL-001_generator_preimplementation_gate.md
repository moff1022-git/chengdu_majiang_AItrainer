# MODEL-001模拟生成器编码前门禁复核

结论：**IMPLEMENTATION_READY**。

## 已关闭决策

- cleared/dominant时点：动作执行前同事件CURRENT_HIDDEN_STATE。
- dominant计数与并列：暗手+公开副露，唯一严格最大；并列/全0=mixed；不排除定缺门。
- shape：EVENTUAL_TERMINAL_OUTCOME，终局restricted truth回填；优先级seven_pairs>pure_suit>all_pongs>standard>other；未胡/不完整/不可确认=other且不跳样本。
- split：game_id稳定hash分组，同局不得跨集合。

## 实现可执行性

现有生产GameState、PlayerView、合法动作、胡牌/番型入口和完整牌局runner足以提供所需边界。生成器需在内存中暂存事件样本，到完整终局后回填shape并一次写出；失败牌局不得形成valid数据集。

CLI、三个输出文件、禁止字段、固定seed、四种程序化风格、自动验证和20—100条测试范围均已由用户任务冻结，无剩余接口或规则决策。

因此允许下一轮实现`training.model001.generate`、测试与1000样本smoke；本复核不授权训练模型，也不改变MODEL-001审计状态。
