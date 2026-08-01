# B1-A派生权威纠正层

状态：**ACTIVE AUTHORITY CORRECTION**  
生效日期：2026-07-30  
范围：只纠正派生文件状态引用，不修改Locked语义、历史审批或生产代码。

## 被覆盖的旧文字

1. `B1-A_effective_spec_overlay.md`标题中的`PENDING CANONICAL PROFILE APPROVAL`，已被`B1-A_contract_v2_approval_form.md`的`CANONICAL_PROFILE_OPTION=OPTION-J2`与`CONTRACT_V2_STATUS=APPROVED`覆盖。
2. `B1-A_version_matrix.csv`新config/new replay行中的`OPTION-J2 pending`和`PENDING_PROFILE_APPROVAL`，已被同一审批表以及`B1-A_frozen_contract_v2_approval.md`覆盖。

## 当前唯一有效状态

- canonical profile：`CDMJ canonical-jcs-nfc-v2 profile / OPTION-J2 / APPROVED`。
- 新写版本：`CDMJ-AI-PARAMS 2.0.0 + CDMJ-CONTRACTS 2.0.0`。
- legacy读取：`PARAMS 1.1.0 + CONTRACTS 1.0.0 + legacy-json-v1`，旧hash和legacy RNG结果零变化。
- 迁移：`MIG-CONFIG-110-200 / APPROVED`；v2 reader双读，新writer只写v2。
- Decimal：`CLOSED_NO_DECIMAL_FIELDS`。
- Frozen v2：`B1-A-FROZEN-V2 1.0.0 / APPROVED`。

开发任务必须读取：本纠正层、`B1-A_contract_v2_change_proposal.md`、`B1-A_contract_v2_approval_form.md`、`B1-A_frozen_contract_v2_proposal.md`、`B1-A_frozen_contract_v2_approval.md`。不得再把上述两个派生文件中的pending行当作当前门禁。原文件保留历史，不就地改写。

FG-002统一分类为`MUST_FIX_BEFORE_AUTHORIZATION`；本纠正层生成后该引用冲突已闭合，仍须由下一次独立终审确认。

