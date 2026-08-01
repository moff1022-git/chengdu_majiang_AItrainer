# B1-B正式开发授权提示词

只实现B1-B：STATE-001、STATE-011、STATE-004。只读取`pre_dev_execution_authorization.json`列出的effective spec/delta文件；禁止把SUPERSEDED Delta作为要求。

按`B1-B_semantic_deltas.csv`的24条semantic Delta逐条实施，保留PlayerGameRunner、create_dealt_game、GameState v5、legacy replay/RNG的兼容行为。随后独立完成12条test Delta与6条E4/E5 evidence Delta。运行B1-A、合同、牌墙、PlayerView、回放及全仓回归。不得修改Locked/Frozen/Task17历史状态，不得自行标记AUDITED；完成后提交独立审计。
