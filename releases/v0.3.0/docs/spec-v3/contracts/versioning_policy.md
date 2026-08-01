# 公共契约版本与兼容策略

当前版本：`CDMJ-CONTRACTS 1.0.0`，Frozen。

采用`MAJOR.MINOR.PATCH`：PATCH仅澄清且不改变合法实例；MINOR只增加可选字段/新枚举能力且旧消费者可忽略；MAJOR用于删除/重命名字段、改变类型/单位/默认/null、枚举语义、canonical bytes、可见性、动作codec或状态迁移。

| 子契约 | 当前版本 | 兼容规则 |
|---|---:|---|
| GameState schema | 5 | 1—4只经显式迁移到5；写出只用5 |
| PlayerView | 2 | 策略必须精确声明支持版本；未知拒绝 |
| Action codec | 2 / 635 | 任一槽位改义必须MAJOR；旧回放保留codec版本 |
| Audit format | 1 | canonical/hash字段变化必须MAJOR |
| Fixture | 1 | expected语义变化必须MAJOR |
| 参数 | CDMJ-AI-PARAMS 1.1.0 | 参数ID不复用；单位/范围/default变化至少MINOR并迁移 |

变更流程：先提出docs/features或ADR→更新schema和兼容矩阵→提供迁移器与正反fixture→契约/回放/隐藏信息测试通过→跨文档审计→用户批准→提升版本和锁定manifest→才允许代码消费者切换。禁止原地修改Frozen schema、静默接受未知字段、按猜测填默认值或以模型兼容替代接口兼容。

消费者必须在边界校验`contract_version,schema_version,ruleset_hash,config_hash`。PATCH可原样读取；MINOR只能在声明forward-compatible且新增字段可选时读取；MAJOR不匹配返回`VERSION_CONFLICT`。回放永远使用记录时版本，不热迁移进行中的局。

弃用至少跨一个MINOR周期：先标deprecated并记录调用者→提供替代字段和双写只读期→验证无调用→下一MAJOR删除。安全/隐藏信息字段不得经历宽松双写，必须立即拒绝并走安全修订。
