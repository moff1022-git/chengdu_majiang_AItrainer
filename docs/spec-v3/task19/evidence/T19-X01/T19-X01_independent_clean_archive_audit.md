# T19-X01 Independent Clean-Archive Audit

- Evidence/archive commit: `9015b58`
- Implementation candidate: `2fc345911f7c470a2991ed6143a525d60f0a175e`
- The archive was extracted without `.git`; manifest hashes and evidence files were recomputed from that tree.

## Gates

- `T19-X01_E4_runtime.jsonl`: NORMAL, BOUNDARY, HARD_FAILURE, DETERMINISM.
- `MODEL-001_AC.csv`: 14 rows; `MODEL-001_E5.csv`: 14 rows.
- Manifest and validation hashes match the archived files.
- Targeted tests: `3 passed`.
- Fresh-process equality: `true`; P95: `0.01 ms`.
- Full regression: `831 passed, 1 skipped, 0 failed, 0 errors` in `118.79s` from source archive `795e13f`.

## Verdict

PASS — P0/P1/P2 = `0/0/0`. The external calibration status remains governed by the existing MODEL-001 external-data gate; this audit does not infer external validity.
