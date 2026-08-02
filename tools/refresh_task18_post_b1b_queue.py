from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict, deque
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/spec-v3"
PLANS = SPEC / "plans"
AUDIT = SPEC / "audit"
GAPS = PLANS / "task18_gap_classification.csv"
BATCHES = PLANS / "development_batches_v3.csv"

TASK17_AUDITED = {
    "RULE-003", "RULE-016", "ALGO-001", "ALGO-010", "HEUR-019",
    "STATE-005", "SCORE-001", "TRAIN-003", "AUDIT-003",
}
PROMOTED = {"STATE-010", "ALGO-009", "ALGO-011", "STATE-001", "STATE-011", "STATE-004"}
CURRENT_AUDITED = TASK17_AUDITED | PROMOTED
NEXT = ("STATE-002", "STATE-003", "ALGO-002")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    gaps = read_csv(GAPS)
    batches = read_csv(BATCHES)
    by_unit = {row["unit_id"]: row for row in gaps}
    original = set(by_unit)
    remaining = original - PROMOTED
    assert len(original) == 87 and len(remaining) == 81
    assert not remaining & CURRENT_AUDITED
    assert len(by_unit) == len(gaps)

    dependencies = {
        unit: {value for value in row["dependencies"].split("|") if value and value != "无"}
        for unit, row in by_unit.items()
    }
    all_units = original | TASK17_AUDITED
    indegree = {unit: 0 for unit in all_units}
    consumers: dict[str, set[str]] = defaultdict(set)
    edges = []
    for unit, deps in dependencies.items():
        for dep in deps:
            assert dep in all_units, (unit, dep)
            indegree[unit] += 1
            consumers[dep].add(unit)
            edges.append({"from": dep, "to": unit})
    queue = deque(sorted(unit for unit, degree in indegree.items() if degree == 0))
    visited = []
    while queue:
        unit = queue.popleft()
        visited.append(unit)
        for child in sorted(consumers[unit]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    assert len(visited) == len(all_units), "dependency graph contains a cycle"

    batch_by_unit = {}
    for batch in batches:
        for unit in batch["unit_ids"].split("|"):
            batch_by_unit[unit] = batch
    rows = []
    for unit in sorted(remaining):
        row = by_unit[unit]
        deps = dependencies[unit]
        satisfied = sorted(deps & CURRENT_AUDITED)
        unmet = sorted(deps - CURRENT_AUDITED)
        current = "INTEGRATED" if unit == "MODEL-001" else "SCAFFOLDED" if unit == "HEUR-016" else "PARTIAL"
        batch = batch_by_unit[unit]
        rows.append({
            "unit_id": unit,
            "unit_name": row["unit_name"],
            "category": row["category"],
            "current_status": current,
            "completion_path": row["primary_completion_path"],
            "planned_batch": batch["batch_id"],
            "batch_order": batch["order"],
            "dependencies": "|".join(sorted(deps)),
            "satisfied_dependencies": "|".join(satisfied),
            "unmet_dependencies": "|".join(unmet),
            "queue_gate": "EXTERNAL_DATA_GATE" if unit == "MODEL-001" else "DEPENDENCY_BLOCKED" if unmet else "DESIGN_REVIEW_READY",
            "model001_external_gate_blocks_unit": "false" if unit != "MODEL-001" else "true",
            "spec_reference": row["spec_refs"],
        })
    write_csv(PLANS / "task18_post_b1b_queue.csv", rows, list(rows[0]))

    graph = {
        "authority": "Task 18A dependency graph refreshed after B1-A and B1-B audit closure",
        "effective_date": str(date.today()),
        "node_count": len(all_units),
        "remaining_queue_count": len(remaining),
        "edge_count": len(edges),
        "acyclic": True,
        "topological_order": visited,
        "current_audited_units": sorted(CURRENT_AUDITED),
        "removed_completed_units": sorted(PROMOTED),
        "remaining_units": sorted(remaining),
        "edges": sorted(edges, key=lambda x: (x["from"], x["to"])),
        "model001_external_calibration_isolated": True,
    }
    (PLANS / "task18_post_b1b_dependency_graph.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    next_rows = []
    for order, unit in enumerate(NEXT, 1):
        row = by_unit[unit]
        deps = dependencies[unit]
        external_met = sorted(deps & CURRENT_AUDITED)
        internal = sorted(deps & set(NEXT))
        next_rows.append({
            "batch_id": "B2-A1",
            "batch_name": "deterministic prerequisites / 确定性前置基础",
            "implementation_order": order,
            "unit_id": unit,
            "unit_name": row["unit_name"],
            "current_status": "PARTIAL",
            "completion_path": row["primary_completion_path"],
            "satisfied_external_dependencies": "|".join(external_met),
            "in_batch_dependencies": "|".join(internal),
            "unmet_external_dependencies": "",
            "authoritative_spec": row["spec_refs"],
            "existing_code_candidates": row["code_refs"],
            "existing_test_candidates": row["test_refs"],
            "missing_semantics": row["notes"],
        })
    write_csv(PLANS / "task18_next_batch_units.csv", next_rows, list(next_rows[0]))

    validation = {
        "original_non_audited_count": 87,
        "removed_completed_count": 6,
        "remaining_count": len(remaining),
        "duplicate_count": 0,
        "audited_unit_in_remaining_count": len(remaining & CURRENT_AUDITED),
        "missing_count": len(original - PROMOTED - remaining),
        "unexpected_count": len(remaining - (original - PROMOTED)),
        "dependency_graph_acyclic": True,
        "model001_external_gate_blocks_independent_units": False,
        "next_batch": "B2-A1",
    }
    print(json.dumps(validation, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
