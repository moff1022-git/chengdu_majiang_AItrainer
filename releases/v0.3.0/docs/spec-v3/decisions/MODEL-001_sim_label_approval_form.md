# MODEL-001模拟标签审批表

- SIM-LABEL-001 APPROVED_OPTION：`A (cleared/dominant current snapshot only)`
- SIM-LABEL-002 APPROVED_OPTION：`A (concealed + public meld; strict max; tie/zero=mixed)`
- SIM-LABEL-003 APPROVED_OPTION：`C (terminal outcome backfill)`
- APPROVAL_STATUS：`APPROVED`
- APPROVED_BY：`project_owner_user`
- APPROVED_AT：`2026-07-30（用户指令时间；无精确时分秒）`
- DECISION_VERSION：`MODEL001-SIM-LABELS 1.0.0`
- LABEL_SCHEMA_VERSION：`MODEL001-LABEL-SCHEMA 1.0.0`
- COMMENT：`shape允许终局truth回填但只能进入restricted labels；不得因shape=other跳过样本；同game不得跨split。`
