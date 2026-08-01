# B1-B final evidence-package test results

- Evidence time: 2026-07-30
- Source commit: `423326ecf6e602f9c1c3392dd2a844b1e61ce9b3`
- Worktree: dirty; pre-existing tracked modifications and untracked files were present and are disclosed in the final audit report.
- Platform: macOS
- Python: 3.12.13
- Command: `.venv-macos/bin/python -m pytest -q -rs --durations=10`
- Collected: 464
- Passed: 463
- Failed: 0
- Skipped: 1
- Duration: 44.78 seconds

## Skipped test assessment

| Node ID | Reason | B1-B scope | Acceptance impact |
|---|---|---|---|
| `tests/test_f0013_dirty_update.py::test_f0013_tk_inplace_paths_single_root` | On macOS, constructing `Tk()` may abort the Python process; the test is covered by pure helper tests and manual/subprocess GUI acceptance. | No. This is an F0013 Tk GUI dirty-update test, not STATE-001, STATE-011, or STATE-004. | None. It does not exercise Match configuration/control, wall/deal, or the Locked round state machine. |

The skip is explicit, explained, unrelated to B1-B, and therefore does not block promotion. No B1-B test failed or was skipped.
