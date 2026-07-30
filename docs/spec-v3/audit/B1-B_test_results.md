# B1-B remediation and re-audit test results

Date: 2026-07-30. Environment: macOS, Python 3.12.13.

## Remediation smoke

`pytest -q tests/spec_v3/test_b1b_remediation.py tests/spec_v3/test_state_001.py tests/spec_v3/test_state_011.py tests/spec_v3/test_state_004.py --maxfail=1`

Result: **16 passed, 0 failed, 0 skipped in 0.40s**.

## Independent focused rerun

The command included B1-B direct/remediation, contracts, game-id/RNG, tile/deal, audit replay, blood battle, PlayerView, session scores and subprocess compatibility tests.

Result: **69 passed, 0 failed, 0 skipped in 4.25s**.

## Full repository

`.venv-macos/bin/python -m pytest -q --durations=10`

Collected: 453. Result: **452 passed, 0 failed, 1 skipped in 37.66s**.

The green suite confirms compatibility and the new production adapters. It does not substitute for the remaining objective Locked oracles listed in `B1-B_defects.csv`.

## Approved authority adapter implementation rerun

Focused B1-B/contracts/RNG/replay/blood-battle/visibility/session/subprocess suite: **85 passed in 4.90s**.

Full repository: **454 passed, 0 failed, 1 skipped in 40.33s** (455 collected).

## Approved full legacy golden and evidence refresh

Focused suite: **86 passed in 4.89s**. Full repository: **455 passed, 0 failed, 1 skipped in 40.01s** (456 collected).

The approved full legacy fixture passes exact seeds/dice/dealer/ordered-hands/ordered-wall comparison and replay version selection.

## Final independent audit rerun

Focused suite: **86 passed, 0 failed, 0 skipped in 4.87s**.

Full repository: **455 passed, 0 failed, 1 skipped in 39.60s** (456 collected).

These results are current evidence, but the missing objective Oracles listed in the final audit report remain uncollected.

## Final remediation closure and independent acceptance

The final remediation added the objective Locked oracles that were missing from the preceding rerun: 100 fresh-process Match reproduction, four-seat paired hidden-information perturbation, the complete STATE-004 phase/event Cartesian oracle, and ordered hu/pong/gang transactional postconditions.

Focused command scope: B1-B direct, branch/exception, atomicity, determinism, contracts, game-id/RNG, legacy replay, blood-battle state machine, hidden-information, session score, subprocess compatibility, and final remediation tests.

Result: **94 passed, 0 failed, 0 skipped in 9.91s**.

Full repository command: `.venv-macos/bin/python -m pytest -q --durations=10`.

Collected: 464. Result: **463 passed, 0 failed, 1 skipped in 44.84s**.

Environment: macOS, Python 3.12.13. These are the final current test results used by the independent acceptance report; the earlier sections remain only as chronological remediation history.
