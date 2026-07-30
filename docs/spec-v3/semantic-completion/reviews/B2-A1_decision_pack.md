# B2-A1 decision pack

Status: **APPROVED**. The project owner selected Option A for all twelve decisions via `执行任务1和2` on 2026-07-30.

The authoritative decision rows are in `B2-A1_decision_matrix.csv`. Twelve decisions are open. Recommended options consistently preserve audited B1-B and Task 16 interfaces through additive DTOs or compatible adapters:

1. DEC-001/002: additive immutable authority DTO with store-owned opaque capabilities; legacy GameState is adapted, not promoted to a policy-visible authority object.
2. DEC-003/004: exact duplicates are idempotent, payload conflicts/stale CAS reject; audit is atomic with authority and notification is a durable post-commit outbox.
3. DEC-005/006/007/012: provisional qiang-gang, pass-hu reset, multi-hu ordering and reveal behavior must be explicitly chosen before STATE-003 coding.
4. DEC-008/009/010/011: additive ALGO-002 facade, canonical decomposition order, dingque semantics and ukeire meaning must be selected before algorithm coding.

Compatibility consequence: no proposed shared interface is classified BREAKING_CHANGE, but additive authority entrypoints and all semantic-choice rows remain approval-gated. Rejecting a recommendation requires updating the design matrices and AC oracles before implementation authorization.

The approval is recorded in `B2-A1_approval_form.md` and `B2-A1_decision_matrix.csv`. It authorizes later implementation but does not itself implement code, execute AC, or upgrade unit status.
