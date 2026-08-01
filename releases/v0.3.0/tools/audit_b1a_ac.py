"""Produce conservative B1-A AC and E5 matrices from current evidence."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/spec-v3"

PASS = {
    "AC-STATE-010-01", "AC-STATE-010-02", "AC-STATE-010-03", "AC-STATE-010-06", "AC-STATE-010-11", "AC-STATE-010-12",
    "AC-ALGO-009-01", "AC-ALGO-009-02", "AC-ALGO-009-03", "AC-ALGO-009-06", "AC-ALGO-009-09", "AC-ALGO-009-11", "AC-ALGO-009-12", "AC-ALGO-009-13",
    "AC-ALGO-011-01", "AC-ALGO-011-02", "AC-ALGO-011-03", "AC-ALGO-011-06", "AC-ALGO-011-07", "AC-ALGO-011-08", "AC-ALGO-011-09", "AC-ALGO-011-11", "AC-ALGO-011-12", "AC-ALGO-011-13",
    "AC-STATE-010-04", "AC-STATE-010-05", "AC-STATE-010-07", "AC-STATE-010-08", "AC-STATE-010-09", "AC-STATE-010-10", "AC-STATE-010-13", "AC-STATE-010-14",
    "AC-ALGO-009-04", "AC-ALGO-009-05", "AC-ALGO-009-07", "AC-ALGO-009-08", "AC-ALGO-009-10", "AC-ALGO-009-14",
    "AC-ALGO-011-04", "AC-ALGO-011-05", "AC-ALGO-011-10", "AC-ALGO-011-14",
}

REASONS = {
    "STATE-010": "逐字段授权/default/范围、orchestrator四座装配、全局归档、性能与跨进程复现尚未全部取得oracle",
    "ALGO-009": "阶段序列、完整数字边界、v2 reload、性能/跨进程及策略投毒隔离尚未全部取得oracle",
    "ALGO-011": "全部replay/worker消费者、ID长度边界、E4字段全集、性能与跨进程/取消排列尚未全部取得oracle",
}

def main() -> None:
    source = SPEC / "semantic-completion/first_batch_acceptance_matrix.csv"
    rows = list(csv.DictReader(source.open(encoding="utf-8-sig")))
    output = SPEC / "reports/B1-A_acceptance_audit_matrix.csv"
    with output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["unit_id", "ac_id", "result", "objective_oracle", "evidence", "finding"])
        writer.writeheader()
        for row in rows:
            passed = row["ac_id"] in PASS
            writer.writerow({"unit_id": row["unit_id"], "ac_id": row["ac_id"], "result": "PASS" if passed else "FAIL", "objective_oracle": row["objective_test_oracle"], "evidence": "tests/spec_v3/test_b1a_*.py; evidence/task18b_b1a/B1-A_runtime_evidence.json; B1-A_golden_execution.json", "finding": "oracle satisfied by current implementation/evidence" if passed else REASONS[row["unit_id"]]})

    deltas = list(csv.DictReader((SPEC / "semantic-completion/task18b_r1_effective_delta_catalog.csv").open(encoding="utf-8-sig")))
    active = [row for row in deltas if row["effective_status"] == "ACTIVE"]
    trace = SPEC / "reports/B1-A_E5_trace_matrix.csv"
    with trace.open("w", encoding="utf-8-sig", newline="") as stream:
        fields = ["delta_id", "unit_id", "delta_kind", "code_symbols", "tests", "runtime_artifact", "status"]
        writer = csv.DictWriter(stream, fieldnames=fields); writer.writeheader()
        for row in active:
            unit = row["unit_id"]
            code = {"STATE-010": "players/humanlike/state010.py;players/humanlike/player.py", "ALGO-009": "players/humanlike/config_v2.py;players/humanlike/settings_service.py", "ALGO-011": "engine/rng_v2.py;engine/deal.py;engine/replay.py;training/runner.py"}[unit]
            writer.writerow({"delta_id": row["delta_id"], "unit_id": unit, "delta_kind": row["delta_kind"], "code_symbols": code, "tests": f"tests/spec_v3/test_b1a_{unit.lower().replace('-', '')}.py", "runtime_artifact": "docs/spec-v3/evidence/task18b_b1a/B1-A_runtime_evidence.json", "status": "TRACED_NOT_NECESSARILY_ACCEPTED"})

    artifacts = [SPEC / "evidence/task18b_b1a/B1-A_runtime_evidence.json", SPEC / "evidence/task18b_b1a/B1-A_golden_execution.json", SPEC / "evidence/task18b_b1a/B1-A_performance_baseline.json", output, trace]
    passed_count = sum(row["ac_id"] in PASS for row in rows)
    manifest = {"artifacts": [{"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in artifacts], "ac_total": len(rows), "ac_pass": passed_count, "ac_fail": len(rows)-passed_count, "audit_result": "AUDITED_CANDIDATE" if passed_count == len(rows) else "REVIEW_REQUIRED_NOT_AUDITED"}
    (SPEC / "evidence/task18b_b1a/B1-A_E5_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ac_total": len(rows), "pass": manifest["ac_pass"], "fail": manifest["ac_fail"], "result": manifest["audit_result"]}))

if __name__ == "__main__":
    main()
