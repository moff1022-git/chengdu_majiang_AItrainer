# Task 18B-R1：B1-A详细实现设计（修订）

状态：**IMPLEMENTATION_IN_PROGRESS / R4合同门禁已通过**  
批次：`B1-A`；范围：`STATE-010 → ALGO-009 / ALGO-011`

> 2026-07-30 R3更正：九项规格决策均以选项A批准（`B1-A-DECISIONS 1.0.0`），但先前Frozen v2审批没有独立裁决RFC 8785与Locked int64的冲突，不能作为canonical profile获批证据。当前推荐`OPTION-J2 / CDMJ canonical-jcs-nfc-v2 profile`，等待负责人批准。

## 结论

R4已批准OPTION-J2、CONTRACTS/PARAMS 2.0及`MIG-CONFIG-110-200`，编码门禁解除。当前首个实现切片与正常路径E4已完成，但独立审计仍为`REVIEW_REQUIRED / NOT_AUDITED`；测试或证据delta不能替代生产语义实现。

## 实施包分离

- 生产语义：`reviews/B1-A_semantic_deltas.csv`（24条）。
- 测试补全：`reviews/B1-A_test_deltas.csv`（12条），每条指向生产语义delta并有业务oracle。
- 证据补全：`reviews/B1-A_evidence_deltas.csv`（6条），E4必须从真实生产入口采集。
- SeedTrace可见性和接口影响分别见对应review CSV。

## 决策批准后的实施顺序

1. 批准required/default/nullable、RP归档、迁移图、extensions、canonical数字/Unicode、fallback、RNG版本和逻辑坐标决策。
2. STATE-010：注册表→GP冻结→RP状态机/归档→四座owner隔离→事务/结果信封→可见性适配。
3. ALGO-009：固定流水线→逐边迁移→schema/default/null→canonical/hash→原子commit/fallback。
4. ALGO-011：冻结legacy golden→实现版本化v2公式/流registry→无状态逻辑坐标→SeedTrace受控投影。
5. 执行test delta；随后由真实settings/orchestrator/deal/replay/worker链采集E4，再建立E5追踪。

## 不可变设计约束

- 旧`derive_seeds`及shuffle/dice/exchange/deal结果零变化；新公式只能在显式新版本入口。
- 无共享可变stream index；worker调度、重试、取消和数量不得进入随机坐标。
- 策略不见master seed、流名、index或seed hash；完整SeedTrace不进入策略对象图。
- canonical hash在规格决策前不得声称跨语言权威；迁移/校验失败无部分内存或文件写入。
- 不新增Frozen必填字段；确需改变必须停止并走接口批准。

## 完成判定

编码已经开始且首个切片完成。最终完成仍要求24条semantic delta、12条test delta、6条evidence delta和42条AC逐项取得客观结果；当前缺口以`reports/B1-A_implementation_audit.md`为准，实现完成不等于AUDITED。
