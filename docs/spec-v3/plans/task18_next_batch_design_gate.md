# B2-A1 design and evidence gate

Status: **APPROVED / READY_FOR_IMPLEMENTATION**  
Coding authorization: **AUTHORIZED for a later explicit implementation task; not started in this approval task**.

## Decisions requiring approval

1. STATE-002 authority boundary: approved Option A uses one canonical RoundState owner, opaque reader/writer capabilities, immutable snapshots, state-version/CAS, idempotency and atomic audit plus post-commit retry outbox.
2. STATE-003 mutation contract: approved Option A uses the event-to-field table, provisional jia-gang resolution, GP-009-bound pass-hu reset, deterministic unique hu order and GP-021/RULE-016 projection.
3. ALGO-002 facade: approved Option A adds `analyze_hand_v1`, lexicographic normalized decompositions, explicit dingque burden and improving-face count semantics while retaining legacy wrappers.
4. Shared interface impact: whether existing GameState/PlayerState and shanten/win-check functions are adapted behind compatible production facades; no Locked/Frozen signature may change without a separately approved interface decision.

## Required design package

For each unit create eight concrete semantic deltas, direct/test/evidence deltas, AC-01 through AC-14 binding, source symbols, consumers, error codes, atomicity boundary, visibility policy and compatibility classification. Approval must identify the exact production call chain and reject test-only facades.

## Direct tests

- STATE-002: schema/version, authorized read/write, snapshot immutability, duplicate/late event, concurrent CAS, commit-once, rollback, terminal/phase access and legacy v5 adapter.
- STATE-003: all legal field mutations, illegal actor/phase, physical ownership and 108-tile conservation, hand/meld/count boundaries, dingque/pass-hu lifecycle, duplicate/CAS and exact rollback.
- ALGO-002: standard and seven-pairs decomposition/shanten, 13/14-tile and meld-count boundaries, dingque, discard map, ukeire and wait shapes, malformed counts, canonical tie/order and known goldens.

Each direct suite must also include branch, exception, property, integration, contract and full-regression coverage. A passing legacy test is only a candidate reference, not direct Locked acceptance.

## E4 and E5

Each unit requires at least four production-path E4 scenarios: NORMAL, BOUNDARY, HARD_FAILURE and DETERMINISM. STATE-002 and STATE-003 additionally require concurrent CAS/idempotency and rollback evidence; ALGO-002 requires representative standard/seven-pairs/tie decomposition and invalid-count evidence. E4 must carry complete hashes, versions, call site, before/intermediate/after state, error code, numeric latency and artifact SHA-256.

E5 must contain one row per approved semantic, test and evidence delta; every AC must be covered, every code symbol locatable, every runtime evidence ID resolvable, and every artifact hash a full SHA-256. No summary row may replace per-delta traceability.

## Information boundary

- STATE-002 authority state must never be passed to policy code; policy receives only approved PlayerView projection.
- Each seat sees only its own concealed hand. Wall order, opponent concealed tiles, raw seed and restricted audit payloads remain inaccessible.
- STATE-003 hidden-field and opponent-hand perturbations must not alter another seat's same-visible-state projection or ALGO-002 result for that seat.
- ALGO-002 may consume only the caller's explicit counts/melds/dingque; it must not read GameState, wall, opponent hands, RNG, cache state or training oracle.

## Performance and determinism

Use the exact Locked per-unit latency thresholds; the design review must quote them before approval rather than inventing replacements. Verify 100 repeated runs, fresh-process reproduction, input mapping/order permutations and concurrent scheduling where applicable. Outputs, error codes, state/version and canonical hashes must be byte-stable for identical versioned input.

## Independent audit gate

Each unit is decided separately. AUDITED requires approved deltas, real production integration, direct/branch/integration tests, four-class E4, per-delta E5, all applicable AC PASS, information-boundary proof, deterministic/performance proof, no unapproved interface change and no open P0/P1 defect. Development self-report cannot sign the audit. Task 17 history is immutable.
