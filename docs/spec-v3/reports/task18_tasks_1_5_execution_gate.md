# Tasks 1–5 execution gate

Status: **BLOCKED at MODEL-001 calibration evidence / deterministic batches remain authorized**

Date: 2026-07-30

## Requested scope

This gate records the attempt to execute the five follow-up items from Task 17:
MODEL-001 calibration, B1 deterministic kernel, B2 deterministic completion,
B3 heuristics, and B4–B6 model/training/audit completion.

## MODEL-001 result

The production rule fallback, direct tests, integration trace, and hidden-field
rejection remain present. The locked acceptance contract additionally requires a
frozen evaluation release with at least 10,000 samples, grouped leakage-safe
train/validation/test manifests, restricted labels, and per-task Brier, log loss,
15-bin ECE, reliability, top-2 recall, and 95% confidence intervals.

No repository artifact satisfies that contract. Existing `logs/` prediction and
game records do not contain the locked MODEL-001 label-zone/schema/split manifest
and must not be relabelled or treated as calibration truth. Generating labels from
the rule fallback and evaluating the same fallback would be circular evidence.

Therefore MODEL-001 remains **INTEGRATED**, not AUDITED. Blocker:
`MODEL001-DATA-001 — compliant frozen calibration release is unavailable`.

## Consequences for items 2–5

Task 15 explicitly classified this as a model-stage caveat rather than a blocker
for deterministic development. B1–B3 remain authorized, but they cover 61
non-pilot units and cannot be truthfully collapsed into one unreviewed bulk patch.
Each unit must retain the approved dependency order and independently acquire code,
test, runtime, and traceability evidence. B4 and the external-evaluation portions
of B6 depend on compliant data releases; B5 also depends on the completed B1/B2
production engine contract.

No business code or test assertion was changed in this gate. This prevents a
missing external dataset from being hidden by synthetic evidence or weakened
acceptance criteria.

## Required unblock inputs

1. A versioned MODEL-001 evaluation release with at least 10,000 eligible rows.
2. Feature and label schemas with physically separate `policy_features` and
   `restricted_label_zone`.
3. Player/match/game/seed-family grouped split manifest and leakage scan result.
4. Source release, ruleset hash, consent/provenance, and canonical file hashes.
5. A trained artifact if the claim is model improvement over the rule fallback;
   otherwise MODEL-001 intentionally remains the integrated deterministic fallback.

## Safe continuation order

While the data blocker is open, implementation may continue in this order:
ALGO-009/ALGO-011/STATE-010 → STATE-001/STATE-011/STATE-004 → RULE and SCORE P0
units → B2 algorithms/state → B3 heuristics → B5 production-equivalent training.
B4 calibration and B6 external-effect claims remain gated by their data releases.
