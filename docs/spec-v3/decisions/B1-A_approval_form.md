# B1-A规格决策审批表

说明：每项只能选择APPROVED_OPTION、REJECTED或NEEDS_REVISION之一；推荐不等于批准。

| DECISION_ID | APPROVED_OPTION | REJECTED | NEEDS_REVISION | COMMENT | APPROVED_BY | APPROVED_AT | DECISION_VERSION |
|---|---|---|---|---|---|---|---|
| SPEC-DECISION-STATE-DEFAULTS | A |  |  | 项目负责人明确批准9项均选择A | project_owner_user | 2026-07-30T04:39:21Z | B1-A-DECISIONS 1.0.0 |
| SPEC-DECISION-RP-ARCHIVE | A |  |  | 项目负责人明确批准9项均选择A | project_owner_user | 2026-07-30T04:39:21Z | B1-A-DECISIONS 1.0.0 |
| SPEC-DECISION-MIGRATION-GRAPH | A |  |  | 项目负责人明确批准9项均选择A | project_owner_user | 2026-07-30T04:39:21Z | B1-A-DECISIONS 1.0.0 |
| SPEC-DECISION-EXTENSIONS | A |  |  | 项目负责人明确批准9项均选择A | project_owner_user | 2026-07-30T04:39:21Z | B1-A-DECISIONS 1.0.0 |
| SPEC-DECISION-CANONICAL-NUMBER | A |  |  | 项目负责人明确批准9项均选择A | project_owner_user | 2026-07-30T04:39:21Z | B1-A-DECISIONS 1.0.0 |
| SPEC-DECISION-CANONICAL-UNICODE | A |  |  | 项目负责人明确批准9项均选择A | project_owner_user | 2026-07-30T04:39:21Z | B1-A-DECISIONS 1.0.0 |
| SPEC-DECISION-CONFIG-FALLBACK | A |  |  | 项目负责人明确批准9项均选择A | project_owner_user | 2026-07-30T04:39:21Z | B1-A-DECISIONS 1.0.0 |
| SPEC-DECISION-RNG-VERSION | A |  |  | 项目负责人明确批准9项均选择A | project_owner_user | 2026-07-30T04:39:21Z | B1-A-DECISIONS 1.0.0 |
| SPEC-DECISION-RNG-COORDINATE | A |  |  | 项目负责人明确批准9项均选择A | project_owner_user | 2026-07-30T04:39:21Z | B1-A-DECISIONS 1.0.0 |

## 生效条件

- APPROVED_OPTION必须填写A/B或经修订后的明确选项编号。
- APPROVED_AT使用UTC RFC3339。
- canonical bytes、可见性或Frozen必填字段变化必须另有接口/版本批准。
- 九项未全部形成明确结论前，不得将B1-A标为IMPLEMENTATION_READY。
