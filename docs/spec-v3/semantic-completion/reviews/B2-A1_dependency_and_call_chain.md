# B2-A1 dependency and production call chain

## Dependency order

`STATE-004 AUDITED + STATE-011 AUDITED -> STATE-002 -> STATE-003 -> ALGO-002`, with `ALGO-001 AUDITED -> STATE-003`.

## Proposed production chains

- STATE-002 write: `PlayerGameRunner / RoundStateMachine committed event -> RoundStateStore.apply -> capability/CAS/event validation -> private snapshot validation -> atomic state+audit commit -> outbox -> consumers`.
- STATE-002 read: `rule/score/audit adapter -> authorized immutable snapshot`; policy path is `RoundStateStore -> PlayerViewBuilder -> PlayerViewV2 -> player` only.
- STATE-003: `opening/blood-battle resolved rule event -> PlayerRoundMutationV1.resolve(snapshot) -> ownership/conservation validation -> RoundStateStore.apply -> committed PlayerView delta`.
- ALGO-002: `RULE-004/RULE-010 or humanlike hand analyzer -> explicit own-hand counts/melds/dingque -> analyze_hand_v1 pure facade -> versioned result`; no authority object is accepted.

## Consumers

- STATE-002: ALGO-010, AUDIT-001, RULE-001/005, SCORE-001, STATE-003/007.
- STATE-003: ALGO-002, RULE-002/003/004/007/008/010/011.
- ALGO-002: ALGO-007, HEUR-001/002/004/009/011/012/014, RULE-004/010.

Existing `GameState`, `PlayerState`, `RoundRuntime`, `PlayerViewV2`, `shanten`, `win_check`, `hand_analyzer` and `legal_actions` are candidates only under the classifications in `B2-A1_interface_impact.csv`. Test-only facades cannot satisfy production integration.
