# B1-B STATE-004 authority adapter decision

Status: **APPROVED**  
Decision version: `B1-B-STATE004-AUTHORITY-1.0.0`  
Approved by: project owner through the instruction `执行任务1-2` on 2026-07-30.

## Context

The first B1-B remediation connected `RoundStateMachine.observe_legacy_commit` to `PlayerGameRunner`, but observation occurs after legacy code mutates `GameState`. That is useful audit evidence but does not satisfy STATE-004's atomic authority boundary for gang ownership, replacement draw, pending claims and phase effects.

Replacing the mature blood-battle engine is out of scope and would duplicate rule authority. The approved design already requires a compatible adapter that preserves GameState v5 and legacy callers.

## Decision

Adopt `OPTION-A / TRANSACTIONAL_LEGACY_ADAPTER`:

1. `RoundStateMachine.apply_legacy_transaction` is the STATE-004 authority boundary.
2. It snapshots canonical GameState v5 before mutation, executes exactly one supplied legacy authority mutation on the working authority object, validates `GameState.validate`, derives the Locked phase/active/wall/claims/current-seat projection, and commits one STATE-004 version/audit/outbox result.
3. Any mutation or validation failure restores the exact pre-call GameState and returns a stable rejection with no version advance and no outbox delivery.
4. Notification happens only after commit. Notification failure does not roll back the committed authority state; retry/delivery policy is downstream and the audit record remains authoritative.
5. Existing `observe_legacy_commit` remains a compatibility/read-only audit bridge for callers not yet migrated, but it cannot be used as E4 proof for atomic effects.
6. `PlayerGameRunner` must route opening/play authority mutations through the transactional adapter at its mutation call sites. Rules remain in existing opening/blood-battle functions; STATE-004 owns atomic application and transition audit.

## Compatibility

- No GameState v5 schema or persisted phase value changes.
- No Locked/Frozen field changes.
- Existing public opening/blood-battle functions and legacy callers remain valid.
- The adapter is a compatible internal extension; rollback uses existing `GameState.to_dict/from_dict` serialization.

## Acceptance

- At least opening, draw, discard/response, hu continuation, gang/replacement draw, wall exhaustion and settlement call sites use the adapter or an equivalent single transaction wrapper.
- Failure restores byte-equivalent `GameState.to_dict`, version and outbox count.
- Success increments STATE-004 version once and records before/after authority hashes.
- Pending claims and tile ownership effects are proven from the committed GameState, not a phase-only snapshot.
- Full phase-event table, terminal absorption, 100 deterministic repeats and hidden-field-safe audit projection pass.

## Rejected option

`OPTION-B / POST_COMMIT_OBSERVER_ONLY` is rejected because it cannot roll back a failed legacy mutation and therefore cannot meet Locked atomicity.
