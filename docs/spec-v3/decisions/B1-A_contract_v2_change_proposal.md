# B1-A CONTRACTS 2.0 / PARAMS 2.0正式版本变更提案

状态：**APPROVED / OPTION-J2**  
提案版本：`B1-A-CONTRACT-V2 2.0.0-rc1`

## 推荐版本组合

不发布PARAMS 1.2。历史读取固定为`PARAMS 1.1.0 + CONTRACTS 1.0.0 + legacy-json-v1`且现有config hash不变；新writer只写`PARAMS 2.0.0 + CONTRACTS 2.0.0 + canonical-jcs-nfc-v2 profile + rng_version=2`。v2 reader双读，v1 reader不读v2。

## JCS/int64选择

标准RFC 8785建立在IEEE-754/ECMAScript Number语义上，无法无损覆盖项目Locked int64全范围。推荐`OPTION-J2`：正式名称`CDMJ canonical-jcs-nfc-v2 profile`。整数token按int64精确十进制、无前导零、整数负零归一为0；非整数采用ECMAScript NumberToString；Decimal按注册scale量化。该profile是JCS的项目扩展，不得宣称为未经修改的RFC 8785。`OPTION-J1`会把整数限制到±(2^53-1)，与ScorePoint/int64契约冲突。

OPTION-J2已由项目负责人通过“执行任务1-5”批准；canonical profile门禁已解除。

## Decimal结论

扫描parameter_registry.csv全部60项，没有字段声明Decimal或scale，结论为`NO_DECIMAL_FIELDS_IN_CANONICAL_CONFIG`。若未来加入Decimal，必须先更新scale registry和版本，不能沿用本次空结论。

## 接口与兼容

v2 DecisionResult以`seed_trace_ref={rng_used,algorithm_version,rng_version,trace_ref}`替代完整seed_trace；完整随机材料只进入受限审计存储。普通策略、PlayerView和DecisionContext禁止master_seed、原始流名、原始index、seed_hash。旧reader/新reader、writer、回放和调用方矩阵见B1-A_version_matrix.csv及effective overlay。

## 破坏性变化与回滚

破坏性变化包括canonical bytes、contract/parameter版本、DecisionResult seed字段和新record必填rng版本。回滚停止v2新写但保留v2 reader；旧文件不重写；已生成v2文件不得用v1 hash覆盖。受影响单元STATE-010/ALGO-009/ALGO-011；调用方包括config/settings/STATE-001、persistence/replay/deal、DecisionResult serializer、audit writer和trainer controller。

## 审批条件

负责人必须在B1-A_contract_v2_approval_form.md明确选择J1或J2并批准版本包与迁移边。只有J选择、合同和MIG-CONFIG-110-200均Approved后，才可重新审查编码门禁。
