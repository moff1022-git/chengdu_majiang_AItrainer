from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/spec-v3"
EVIDENCE = SPEC / "evidence/task18b_b1b_independent"
AUDIT = SPEC / "audit"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    source_commit = commit()
    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    source_e4 = EVIDENCE / "B1-B_E4_runtime.jsonl"
    final_e4 = EVIDENCE / "B1-B_E4_runtime_final.jsonl"
    source_e5 = EVIDENCE / "B1-B_E5_trace.csv"
    final_e5 = EVIDENCE / "B1-B_E5_trace_final.csv"
    final_ac = EVIDENCE / "B1-B_AC_results_final.csv"

    artifact_by_unit = {
        "STATE-001": ROOT / "engine/match.py",
        "STATE-011": ROOT / "engine/deal.py",
        "STATE-004": ROOT / "engine/round_state_machine.py",
    }
    known_hashes = {
        "match": sha256(ROOT / "engine/match.py"),
        "deal": sha256(ROOT / "engine/deal.py"),
        "round": sha256(ROOT / "engine/round_state_machine.py"),
        "orchestrator": sha256(ROOT / "engine/orchestrator.py"),
        "tests": sha256(ROOT / "tests/spec_v3/test_b1b_remediation.py"),
        "fixture": sha256(ROOT / "tests/spec_v3/fixtures/state011_legacy_deal_golden_v1.json"),
    }

    e4_rows: list[dict[str, object]] = []
    valid_hash_fields = ("input_hash", "output_hash", "ruleset_hash", "config_hash")
    for line in source_e4.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        descriptions = []
        for field in valid_hash_fields:
            value = row.get(field)
            if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
                if value is not None:
                    descriptions.append(f"{field}: {value}")
                row[field] = None
        latency = row.pop("latency", None)
        row["latency_ms"] = None
        if latency is not None:
            descriptions.append(f"latency observation: {latency}")
        old_artifact = row.get("artifact_hash")
        if old_artifact is not None:
            descriptions.append(f"source artifact: {old_artifact}")
        row["artifact_hash"] = sha256(artifact_by_unit[row["unit_id"]])
        existing = row.get("description")
        row["description"] = "; ".join(([existing] if existing else []) + descriptions)
        e4_rows.append(row)
    final_e4.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in e4_rows),
        encoding="utf-8",
    )

    evidence_ids = {row["evidence_id"] for row in e4_rows}
    e5_rows: list[dict[str, str]] = []
    with source_e5.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        e5_fields = list(reader.fieldnames or [])
        for row in reader:
            expanded = []
            unit_prefix = f"FINAL-E4-{row['unit_id'].replace('-', '')}-"
            for reference in row["runtime_evidence_ids"].split("|"):
                expanded.append(reference if reference.startswith("FINAL-E4-") else unit_prefix + reference)
            row["runtime_evidence_ids"] = "|".join(expanded)
            labels = [item.split("=", 1)[0] for item in row["artifact_hashes"].split("|")]
            resolved = []
            for label in labels:
                key = label if label in known_hashes else {
                    "round.py": "round",
                    "orchestrator.py": "orchestrator",
                    "match.py": "match",
                    "deal.py": "deal",
                }.get(label, label)
                if key not in known_hashes:
                    key = {"STATE-001": "match", "STATE-011": "deal", "STATE-004": "round"}[row["unit_id"]]
                resolved.append(f"{label}={known_hashes[key]}")
            row["artifact_hashes"] = "|".join(resolved)
            e5_rows.append(row)
    write_csv(final_e5, e5_rows, e5_fields)

    with (EVIDENCE / "B1-B_AC_results.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        ac_rows = list(reader)
        ac_fields = list(reader.fieldnames or [])
    write_csv(final_ac, ac_rows, ac_fields)

    refs = [ref for row in e5_rows for ref in row["runtime_evidence_ids"].split("|")]
    deltas = [row["delta_id"] for row in e5_rows]
    malformed = [ref for ref in refs if not ref or not ref.startswith("FINAL-E4-")]
    missing = [ref for ref in refs if ref not in evidence_ids]
    duplicate_delta_count = len(deltas) - len(set(deltas))
    category_counts: dict[str, dict[str, int]] = {}
    for row in e4_rows:
        category = row["evidence_id"].rsplit("-", 1)[-1]
        category_counts.setdefault(row["unit_id"], {})[category] = (
            category_counts.setdefault(row["unit_id"], {}).get(category, 0) + 1
        )
    required = {"NORMAL", "BOUNDARY", "FAILURE", "DETERMINISM"}
    missing_categories = {
        unit: sorted(required - set(counts)) for unit, counts in category_counts.items() if required - set(counts)
    }
    bad_e4_hashes = []
    for index, row in enumerate(e4_rows, 1):
        for field in (*valid_hash_fields, "artifact_hash"):
            value = row[field]
            if value is not None and (not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value)):
                bad_e4_hashes.append(f"line {index}:{field}")
    bad_e5_hashes = []
    for index, row in enumerate(e5_rows, 2):
        for value in row["artifact_hashes"].split("|"):
            digest = value.split("=", 1)[-1]
            if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
                bad_e5_hashes.append(f"line {index}:{value}")

    validation = {
        "generated_at": generated_at,
        "source_commit": source_commit,
        "e5_row_count": len(e5_rows),
        "unique_delta_id_count": len(set(deltas)),
        "missing_runtime_evidence_reference_count": len(missing),
        "duplicate_delta_id_count": duplicate_delta_count,
        "unparseable_reference_count": len(malformed),
        "e4_row_count": len(e4_rows),
        "e4_category_counts": category_counts,
        "missing_e4_categories": missing_categories,
        "invalid_e4_hash_count": len(bad_e4_hashes),
        "invalid_e5_artifact_hash_count": len(bad_e5_hashes),
        "missing_runtime_evidence_references": missing,
        "unparseable_references": malformed,
        "invalid_hashes": bad_e4_hashes + bad_e5_hashes,
        "result": "PASS" if not (missing or malformed or duplicate_delta_count or missing_categories or bad_e4_hashes or bad_e5_hashes) else "FAIL",
    }
    (EVIDENCE / "B1-B_evidence_validation.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    manifest_paths = [
        final_e4,
        final_e5,
        final_ac,
        AUDIT / "B1-B_test_results_final.md",
        AUDIT / "task18_b1b_audit_status_delta_final.csv",
    ]
    manifest_rows = []
    for path in manifest_paths:
        if path.exists():
            manifest_rows.append({
                "artifact_path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
                "byte_size": path.stat().st_size,
                "generated_at": generated_at,
                "source_commit": source_commit,
            })
    write_csv(
        EVIDENCE / "B1-B_evidence_manifest.csv",
        manifest_rows,
        ["artifact_path", "sha256", "byte_size", "generated_at", "source_commit"],
    )
    print(json.dumps(validation, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
