# Task 18 post-B1-B next batch selection

Status: **READY_FOR_IMPLEMENTATION**. Design `B2-A1-DESIGN-1.0.0` is approved; implementation has not started.

## Selected batch

- Batch ID: `B2-A1`
- Name: deterministic prerequisites / 确定性前置基础
- Units: `STATE-002`, `STATE-003`, `ALGO-002`
- Current status: all three are `PARTIAL`
- Completion path: all three are `PATH-SEMANTIC-COMPLETION`
- In-batch order: `STATE-002 -> STATE-003 -> ALGO-002`

This is the unique next batch because B1-B is now independently AUDITED, all external prerequisites are AUDITED, and this small shared state/hand-analysis context unlocks the P0 rule foundation and many later deterministic consumers. `STATE-002` directly unlocks STATE-003, RULE-001, RULE-005, STATE-007 and other consumers; STATE-003 then unlocks ALGO-002 and most opening/claim rules; ALGO-002 unlocks win qualification and heuristic analysis. MODEL-001 calibration is not on this dependency path.

## Dependencies

| Unit | Satisfied external dependencies | In-batch dependency | Unmet external dependency |
|---|---|---|---|
| STATE-002 | STATE-004, STATE-011 | none | none |
| STATE-003 | ALGO-001 | STATE-002 | none |
| ALGO-002 | none | STATE-003 | none |

The batch is dependency-ready and design-approved. Implementation is authorized as a separate task in the fixed order `STATE-002 -> STATE-003 -> ALGO-002`.

## Authority and missing closure

- STATE-002: `docs/spec-v3/03-unit-specs/deterministic_rule_state_specs.md` at `STATE-002`; candidate production symbols exist, but the Locked schema, authorization model, event/CAS behavior, rollback, audit binding and production trace have not been isolated and approved as a v3 unit.
- STATE-003: the same Locked specification at `STATE-003`; candidate state/invariant code exists, but authoritative hand/meld/dingque/pass-hu/status mutations, ownership conservation, error mapping and atomic STATE-002 commit need a concrete delta package.
- ALGO-002: `docs/spec-v3/03-unit-specs/deterministic_algorithm_scoring_specs.md` at `ALGO-002`; decomposition, standard/seven-pairs shanten, discard map, ukeire and wait shapes need one approved facade with separable pure-function evidence.

No Locked/Frozen change is proposed. Any ambiguity discovered during design must be resolved in a decision record instead of inferred in code.

## Selection constraints

- Task 17 historical 9/1/85/1 remains unchanged.
- Task 18 current 15/1/79/1 remains the status authority.
- The remaining queue contains exactly 81 unique units and excludes all 15 current AUDITED units.
- HEUR-016 remains SCAFFOLDED in its original later batch; no current dependency requires advancing it.
- MODEL-001 remains INTEGRATED and externally gated only on its own calibration track.
