# B2-A1 design review

Status: **APPROVED** as `B2-A1-DESIGN-1.0.0`. Implementation remains a separate task.

## Authority and ordering

The batch order is `STATE-002 -> STATE-003 -> ALGO-002`. Sources are the Locked STATE-002/003 and ALGO-002 cards, Task 16 common/visibility/version contracts, effective B1-A canonical/version/RNG contracts, audited B1-B Match/deal/transaction/PlayerView/state-machine boundaries, the parameter registry, error catalog and E4/E5 standard. No Locked/Frozen content is changed.

## STATE-002 proposed contract

The sole authority owner is one per-round `RoundStateStore`, created by the B1-B round controller and initialized only from a committed STATE-011 result. STATE-004 and approved rule/state/score adapters receive opaque write capabilities; audit/replay and view projection receive read capabilities. Policy, `RoundRuntime`, TrainingTruth and training oracle receive neither.

Proposed additive request DTO: `RoundStateRequestV1(schema_version, migration_version, game_id, round_id, event_id, expected_state_version, ruleset_hash, config_hash, actor_seat, phase, operation, payload, capability_ref)`. All fields except actor where operation is system-owned are required; no implicit defaults. IDs follow Frozen 1..256 UTF-8 bytes, versions are uint64, hashes are lowercase SHA-256. Proposed result contains accepted, error_code, next_state_version, immutable snapshot or null, audit_ref and deterministic_fingerprint.

The committed snapshot deep-freezes phase/status, current/active seats, wall controlled reference/count, players, discards/claims, score/event ledgers and lifecycle metadata. It never contains a policy-reachable mutable object. `schema_version` and `migration_version`, and whether V1 names are selected, remain subject to DEC-001.

Write algorithm: authorize -> detect event ledger duplicate/conflict -> compare CAS -> prepare private copy -> validate schema, phase, actor, ownership and invariants -> canonicalize -> atomically commit state plus audit -> increment version once -> enqueue commit-only notifications. A pre-commit failure restores exact bytes/version and emits no outbox item. Notification failure records retry state but does not roll authority back, subject to DEC-004. Exact duplicate/same payload returns its original result; same ID/different payload is `INVALID_EVENT`; stale version is `VERSION_CONFLICT`, subject to DEC-003.

Reads return immutable committed snapshots or a PlayerView projection. Terminal/phase-incompatible writes reject; terminal reads require an approved reader capability. Legacy v5 `GameState` remains unchanged and enters/leaves only through a validating compatible adapter; raw `master_seed`, wall sequence and opponent hands cannot cross policy projection.

## STATE-003 proposed contract

`PlayerRoundMutationV1` carries the common Frozen envelope plus event kind, actor/target/source seats, physical tile IDs, meld/claim reference, dingque, hu/pass-hu payload and expected phase. It resolves against an immutable STATE-002 snapshot and returns a proposed `PlayerRoundStateV1`, ownership delta and public projection delta; STATE-002 is the only committer.

Player fields are seat, concealed physical IDs, canonical melds, discard records, dingque, pass-hu state/value/source, status, hu_order and last-win public reference. Missing optional domain fields are distinct from null. Default status is only set during explicit initialization, never during migration or mutation.

| Event | Phase / actor | Input | State and count mutation | Ownership / conservation | Failure / projection |
|---|---|---|---|---|---|
| draw | DRAW; current active seat | one wall tile ID | hand +1 | wall -> actor; total 108 unchanged | illegal phase/actor rejects; owner sees tile, others count |
| discard | DISCARD; current active seat | one owned hand tile ID | hand -1; discard +1 | actor hand -> public discard | absent tile rejects; public face/physical ID per GP-021 |
| pong | RESPONSE; winning claimant | claimed discard + two matching hand IDs | hand -2; meld +3; mark discard claimed | discard + hand -> claimant meld | invalid face/count/source rejects; meld public |
| ming gang | RESPONSE; claimant | discard + three matching hand IDs | hand -3; meld +4 | discard + hand -> meld | rollback all on invariant failure; meld public |
| an gang | DISCARD after draw; actor | four matching owned IDs | hand -4; concealed-gang meld +4 | hand -> owned meld | reveal controlled by GP-021/RULE-016 |
| jia gang | DISCARD after draw; actor | existing pong + matching owned ID | hand -1; pong provisionally upgrades to four | hand -> provisional meld | visibility and commit await response resolution |
| qiang gang | RESPONSE; eligible opponent(s) | provisional upgrade ref + winner order | cancel/commit provisional upgrade; winning tile routed per approved model | no duplicate/lost tile; 108 unchanged | DEC-005 blocks exact model |
| dingque | DINGQUE; owner | wan/tong/tiao | dingque null -> value | no tile movement | invalid/repeated policy exact behavior in approved event table |
| pass hu | RESPONSE; eligible owner | source/value/window | pass_hu free -> locked/value_limited | no tile movement | state owner sees permission; public only approved status |
| clear pass hu | approved reset event | reset cause/new value | pass_hu -> free/update | no tile movement | DEC-006 blocks trigger details |
| first hu | RESPONSE/DISCARD resolution; winner | win source/tile/ref | status active -> finished; hu_order set | winning tile into controlled winning region | public winner/order; concealed reveal by GP-021 |
| multi hu | one resolved response event | canonical winner set | each winner gets unique/order semantics | one source event; no physical duplication | DEC-007 blocks ordinal rule |
| active exit | hu resolution | winner seat | remove from active set through STATE-002 | no tile movement | public active set; no hidden hand |
| terminal | FINISHED/SETTLED | terminal reason | all player state immutable | conservation must still hold | later mutation `INVALID_STATUS`; terminal projection per RULE-016 |

Every accepted row invokes exactly one STATE-002 commit and increments authority version once. Any validation or commit failure leaves all players, wall/regions, ledgers, active set, version and hash byte-identical.

## ALGO-002 proposed contract

The additive pure facade accepts `HandAnalysisRequestV1(formula_version, baseline_version, counts:int8[27], open_melds:tuple, dingque:enum|null, requested_outputs:set)`. It does not accept GameState, player identity, wall, opponent data, seed, RNG, cache handle or label. Counts are 0..4; melds 0..4 and valid; concealed size must match the Locked 13/14 minus meld structure. Null is allowed only for dingque.

The result includes accepted/error, formula versions, normalized counts/melds/dingque, standard/seven-pairs result, minimum shanten -1..8, canonical decompositions, per-distinct-discard map, improving faces/ukeire, wait shapes and input/output hashes. Processing is validate -> normalize -> standard decomposition -> seven pairs -> minimum -> all distinct discards -> all 27 additions -> wait classification -> canonical sort. No partial output on failure.

Standard formula is the Locked `2(n-m)-min(t,n-m)-p`, `n=4-open_melds`; seven pairs is `6-pairs+max(0,7-distinct)` and is N/A for open hands; winning is -1. Improving faces strictly reduce shanten. Integer/set error tolerance is zero. Canonical tie/decomposition order, dingque burden and ukeire count meaning remain DEC-009/010/011 and block implementation. Legacy scalar `shanten`, `win_check` and `hand_analyzer` remain compatible wrappers/consumers rather than modified shared contracts.

## Performance, evidence and approval

ALGO-002 Locked threshold is cached O(27xS), P95 <= 5ms. STATE-002/003 cards do not give a unique numeric latency threshold; approval must bind one or explicitly mark performance AC blocked rather than invent a value. All units require 100 repeats, fresh-process and input/schedule permutation equality; state units also require CAS concurrency and rollback.

The CSV package binds 8 semantic, 4 direct-test, 2 evidence deltas and AC-01..14 per unit. E4 requires NORMAL, BOUNDARY, HARD_FAILURE and DETERMINISM production scenarios. E5 is per delta with complete E4 foreign keys and artifact SHA-256. The project owner approved Option A for B2A1-DEC-001 through 012 via the instruction `执行任务1和2`; coding is authorized only in a later explicit implementation task.
