# Task 18B-R3：B1-A IMPLEMENTATION_READY复审

结论：**SUPERSEDED — BLOCKED_BY_CANONICAL_PROFILE_DECISION**  
复审时间：`2026-07-30T04:43:40Z`  
范围：STATE-010、ALGO-009、ALGO-011。

> 本复审的ready结论已被正式R3版本包复核取代：先前Frozen v2审批未独立解决RFC 8785与Locked int64的canonical profile选择。当前权威门禁见`../../decisions/B1-A_contract_v2_change_proposal.md`和`../../decisions/B1-A_contract_v2_approval_form.md`。

## 门禁结论

- 九项业务规格决策：9/9 APPROVED，版本`B1-A-DECISIONS 1.0.0`。
- Frozen接口变更：APPROVED，版本`B1-A-FROZEN-V2 1.0.0`。
- semantic delta：24条均有具体当前/目标行为、代码位置和oracle。
- test delta：12条，与生产语义delta分离。
- evidence delta：6条，E4明确要求真实生产链。
- AC-01：三个单元均已通过规格/接口来源门禁；AC-02..14为实施验收项，不是开始编码前必须已有的实现证据。
- 上游：STATE-010无上游；批内顺序固定为STATE-010先完成注册/生命周期门面，再实施ALGO-009和ALGO-011。
- 输入、输出、错误、canonical bytes、旧回放、迁移、边界、可见性、固定种子、测试和运行证据格式均已有Approved来源。

## 单元ready判定

### STATE-010 — READY

60 ID闭集、strict required/null、GP冻结、RP归档/重置、四座owner隔离、原子提交和失败零写入已经批准。实现不得把RP的UNINITIALIZED序列化为null，也不得直接跨局复制任何RP。

### ALGO-009 — READY AFTER STATE-010 REGISTRY API

流水线、唯一迁移图、empty-only extensions、canonical legacy/v2字节、首次启动/热更语义和FrozenConfig边界已经批准。依赖STATE-010注册表API是批内顺序，不是外部阻断。

### ALGO-011 — READY AFTER STATE-010 VERSION REGISTRY

legacy-v1零变化、新录制显式v2、无状态逻辑坐标、策略安全seed_trace_ref和受限完整trace已经批准。依赖STATE-010版本注册是批内顺序。

## 实施边界

编码只能覆盖三个单元及Approved契约/schema/迁移适配；不得扩展其他随机consumer的业务迁移，未迁移consumer保留明确legacy路径。不得修改Task17/18A状态。开发完成后状态仍为PARTIAL，需独立审计才能升级。

## 第一实施顺序

1. 建立CONTRACTS/PARAMS v2 schema与只读v1 adapter及golden tests。
2. STATE-010注册/生命周期/事务门面。
3. ALGO-009迁移、canonical和配置原子门禁。
4. ALGO-011 legacy/v2 RNG、坐标与SeedTrace隔离。
5. 直接/边界/集成测试，随后采集真实E4和E5证据。
