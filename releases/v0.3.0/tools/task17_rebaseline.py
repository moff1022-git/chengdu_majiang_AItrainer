#!/usr/bin/env python3
"""Generate Task 17's reproducible 96-unit evidence baseline.

The M0 matrix is used only as a search index. Every referenced path and Python
symbol is checked against the current tree before it can appear as evidence.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/spec-v3"
OUT = SPEC / "audit"
CATALOG = SPEC / "02-unit-catalog/locked_unit_catalog.csv"
TRACE = SPEC / "07-traceability/rule_parameter_unit_matrix.csv"
M0 = SPEC / "09-implementation-audit/m0_implementation_gap_matrix.csv"
PILOT = SPEC / "reports/task15_pilot_findings.csv"
LOCK = SPEC / "SPEC_V3_LOCK_MANIFEST.md"
MIGRATION = SPEC / "02-unit-catalog/unit_migration_map.csv"

ALLOWED_STATUS = {
    "NOT_SPECIFIED", "SPECIFIED", "SCAFFOLDED", "PARTIAL", "IMPLEMENTED",
    "TESTED", "INTEGRATED", "AUDITED", "BLOCKED",
}
PILOT_IDS = {
    "RULE-003", "RULE-016", "ALGO-001", "ALGO-010", "HEUR-019",
    "MODEL-001", "STATE-005", "SCORE-001", "TRAIN-003", "AUDIT-003",
}
SPLIT_REVIEW = {
    "RULE-001": "规则裁决、参数解析和不变量执行具有不同变化轴；进入实现批次前确认是否保留门面并拆为内部组件",
    "ALGO-002": "牌型拆解、普通/七对向听、弃牌向听和等待形状应以同一门面下的独立纯函数实现",
    "ALGO-008": "随机流派生、噪声与思考时间应共享种子契约但分离算法职责",
    "SCORE-004": "花猪、查大叫、退税是同一终局事务内三类独立调整，需分别留守恒证据",
    "AUDIT-009": "工程回归与行为回归指标的数据源、阈值和执行频率不同，建议拆为两个内部检查器",
}
# Current-tree discoveries that were absent from the historical M0 search index.
# These are audit-reference corrections only; they do not change production code.
CURRENT_EVIDENCE_OVERLAY = {
    "ALGO-011": {
        "symbols": [
            "engine/game_id.py::master_seed_from_game_id",
            "engine/game_id.py::derive_seeds",
        ],
        "callers": [
            "engine/deal.py::derive_seeds",
            "engine/orchestrator.py::create_dealt_game",
        ],
        "tests": [
            "tests/test_game_id_repro.py::test_t03_same_game_id_same_seeds",
            "tests/test_game_id_repro.py::test_t04_different_game_id_different_master",
            "tests/test_game_id_repro.py::test_t06_deal_reproducible",
            "tests/test_game_id_repro.py::test_t11_exchange_seed_derived_and_distinct",
        ],
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def split_refs(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PythonIndex:
    def __init__(self) -> None:
        self._cache: dict[str, tuple[set[str], set[str], set[str]]] = {}

    def symbols(self, relative: str) -> tuple[set[str], set[str], set[str]]:
        if relative in self._cache:
            return self._cache[relative]
        path = ROOT / relative
        names: set[str] = set()
        mentions: set[str] = set()
        placeholders: set[str] = set()
        if not path.is_file() or path.suffix != ".py":
            self._cache[relative] = (names, mentions, placeholders)
            return names, mentions, placeholders
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            self._cache[relative] = (names, mentions, placeholders)
            return names, mentions, placeholders
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                mentions.add(node.id)
            elif isinstance(node, ast.Attribute):
                mentions.add(node.attr)
            elif isinstance(node, ast.alias):
                mentions.add(node.asname or node.name.rsplit(".", 1)[-1])
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.add(node.name)
                mentions.add(node.name)
                body = getattr(node, "body", [])
                if len(body) == 1 and isinstance(body[0], ast.Pass):
                    placeholders.add(node.name)
                if any(
                    isinstance(child, ast.Raise)
                    and isinstance(child.exc, ast.Call)
                    and isinstance(child.exc.func, ast.Name)
                    and child.exc.func.id == "NotImplementedError"
                    for child in ast.walk(node)
                ):
                    placeholders.add(node.name)
        self._cache[relative] = (names, mentions, placeholders)
        return names, mentions, placeholders

    def verify(self, ref: str, *, allow_reference: bool = False) -> bool:
        if "::" not in ref:
            return (ROOT / ref).is_file()
        relative, symbol = ref.split("::", 1)
        symbol_set = self.symbols(relative)[1 if allow_reference else 0]
        return (ROOT / relative).is_file() and symbol in symbol_set

    def placeholder(self, ref: str) -> bool:
        if "::" not in ref:
            return False
        relative, symbol = ref.split("::", 1)
        return symbol in self.symbols(relative)[2]


def batch_for(unit_id: str, priority: str) -> str:
    category = unit_id.split("-", 1)[0]
    if unit_id in PILOT_IDS:
        return "B0-PILOT-ACCEPTANCE"
    if category in {"RULE", "STATE", "ALGO", "SCORE"} and priority == "P0":
        return "B1-DETERMINISTIC-KERNEL"
    if category in {"RULE", "STATE", "ALGO", "SCORE"}:
        return "B2-DETERMINISTIC-COMPLETION"
    if category == "HEUR":
        return "B3-HEURISTICS"
    if category == "MODEL":
        return "B4-MODELS-CALIBRATION"
    if category == "TRAIN":
        return "B5-TRAINING"
    return "B6-AUDIT-RELEASE"


def complexity(row: dict[str, str]) -> str:
    category = row["unit_id"].split("-", 1)[0]
    if category in {"MODEL", "TRAIN"} or row["m0_classification"] in {"ADD", "REWRITE"}:
        return "HIGH"
    if len(split_refs(row["existing_files"])) >= 7 or row["priority"] == "P0":
        return "MEDIUM"
    return "LOW"


def severity(unit_id: str, status: str, priority: str, hidden_risk: str) -> str:
    if status == "BLOCKED":
        return "BLOCKER"
    if status in {"SPECIFIED", "SCAFFOLDED", "PARTIAL"} and priority == "P0":
        return "HIGH"
    if hidden_risk != "NONE" or status in {"SPECIFIED", "SCAFFOLDED", "PARTIAL"}:
        return "MEDIUM"
    return "LOW"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    catalog = read_csv(CATALOG)
    trace = {row["unit_id"]: row for row in read_csv(TRACE)}
    m0 = {row["unit_id"]: row for row in read_csv(M0)}
    pilot = {row["unit_id"]: row for row in read_csv(PILOT)}
    assert len(catalog) == len(trace) == len(m0) == 96
    unit_ids = {row["新单元ID"] for row in catalog}
    assert len(unit_ids) == 96
    migration = read_csv(MIGRATION)
    legacy_ids = {row["legacy_id"] for row in migration if row["legacy_id"].startswith("AU-")}
    assert legacy_ids == {f"AU-{number:03d}" for number in range(1, 97)}
    assert all(target in unit_ids for row in migration for target in split_refs(row["new_unit_ids"]))

    py = PythonIndex()
    audited_rows: list[dict[str, object]] = []
    invalid_refs: list[str] = []
    placeholder_refs: list[str] = []
    for source in catalog:
        uid = source["新单元ID"]
        candidate = m0[uid]
        tr = trace[uid]
        existing = [ref for ref in split_refs(candidate["existing_files"]) if (ROOT / ref).is_file()]
        symbols = [ref for ref in split_refs(candidate["verified_symbols"]) if py.verify(ref)]
        callers = [ref for ref in split_refs(candidate["verified_production_callers"]) if py.verify(ref, allow_reference=True)]
        tests = [ref for ref in split_refs(candidate["legacy_test_cases"]) if py.verify(ref)]
        overlay = CURRENT_EVIDENCE_OVERLAY.get(uid, {})
        symbols.extend(ref for ref in overlay.get("symbols", []) if py.verify(ref) and ref not in symbols)
        callers.extend(ref for ref in overlay.get("callers", []) if py.verify(ref, allow_reference=True) and ref not in callers)
        tests.extend(ref for ref in overlay.get("tests", []) if py.verify(ref) and ref not in tests)
        planned_test = candidate["planned_v3_test"]
        if planned_test and (ROOT / planned_test).is_file():
            tests.insert(0, planned_test)
        for field in ("verified_symbols", "verified_production_callers", "legacy_test_cases"):
            for ref in split_refs(candidate[field]):
                if not py.verify(ref, allow_reference=field == "verified_production_callers"):
                    invalid_refs.append(f"{uid}:{field}:{ref}")
        unit_placeholders = [ref for ref in symbols if py.placeholder(ref)]
        placeholder_refs.extend(f"{uid}:{ref}" for ref in unit_placeholders)

        if uid in pilot:
            p = pilot[uid]
            status = p["new_status"]
            code_evidence = p["code_evidence"]
            test_evidence = p["test_evidence"]
            runtime_evidence = p["runtime_evidence"]
            trace_evidence = p["traceability_evidence"]
        else:
            # Legacy symbols are evidence of related semantics, not proof that the
            # locked v3 unit boundary and full contract have been implemented.
            status = "PARTIAL" if symbols else ("SCAFFOLDED" if existing else "SPECIFIED")
            code_evidence = "|".join(symbols)
            test_evidence = "|".join(tests)
            runtime_evidence = ""
            caller_chain = "|".join(callers) if callers else "NO_VERIFIED_PRODUCTION_CALLER"
            trace_evidence = f"{tr['source_rule_refs']}→{tr['detailed_spec']}→{tr['target_module']}→{caller_chain}"
        assert status in ALLOWED_STATUS
        four_evidence = all((code_evidence, test_evidence, runtime_evidence, trace_evidence))
        if status == "AUDITED" and not four_evidence:
            raise AssertionError(f"{uid}: AUDITED without all evidence classes")

        hidden = "NONE"
        visibility = source["信息可见性等级"]
        risk_tags = candidate["risk_tags"]
        if "VISIBILITY" in risk_tags or any(k in visibility for k in ("隐藏", "私有", "全知")):
            hidden = "REQUIRES_BOUNDARY_TEST"
        if uid in pilot and pilot[uid]["hidden_information_violation"].strip().lower() not in {"", "false", "0", "none", "否"}:
            hidden = "VIOLATION"

        atomicity = "ATOMIC"
        split_merge = "NONE"
        if uid in SPLIT_REVIEW:
            atomicity = "ATOMIC_FACADE_INTERNAL_SPLIT_REVIEW"
            split_merge = SPLIT_REVIEW[uid]
        impl_gap = "NONE" if status in {"AUDITED", "INTEGRATED"} else candidate["key_gap"]
        if unit_placeholders:
            impl_gap += "; referenced placeholder: " + "|".join(unit_placeholders)
        test_gap = "NONE" if status == "AUDITED" else (
            "缺少锁定单元的直接测试及四类验收证据" if tests else "未找到当前可验证测试；需新增单元、边界、集成与回放测试"
        )
        spec_gap = "NONE" if uid not in SPLIT_REVIEW else "实现前需落实门面内职责分离，不改变已锁定外部语义"
        sev = severity(uid, status, source["开发优先级"], hidden)
        audited_rows.append({
            "unit_id": uid,
            "unit_name": source["名称"],
            "category": uid.split("-", 1)[0],
            "atomicity": atomicity,
            "current_status": status,
            "target_status": "AUDITED",
            "rule_refs": tr["source_rule_refs"],
            "spec_refs": tr["detailed_spec"],
            "code_refs": code_evidence,
            "test_refs": test_evidence,
            "runtime_refs": runtime_evidence,
            "traceability_evidence": trace_evidence,
            "production_callers": "|".join(callers),
            "dependencies": source["上游依赖"],
            "downstream_consumers": source["下游消费者"],
            "hidden_information_risk": hidden,
            "implementation_gap": impl_gap,
            "test_gap": test_gap,
            "spec_gap": spec_gap,
            "severity": sev,
            "estimated_complexity": complexity(candidate),
            "recommended_batch": batch_for(uid, source["开发优先级"]),
            "code_evidence": bool(code_evidence),
            "test_evidence": bool(test_evidence),
            "runtime_evidence": bool(runtime_evidence),
            "traceability_evidence_present": bool(trace_evidence),
            "placeholder_detected": bool(unit_placeholders),
            "split_merge_recommendation": split_merge,
            "primary_inputs": source["主要输入"],
            "primary_outputs": source["主要输出"],
            "deterministic": source["是否确定性"],
            "trainable": source["是否可训练"],
            "rng_required": source["是否需要随机数"],
            "visibility": visibility,
            "priority": source["开发优先级"],
            "parameter_refs": tr["parameter_refs"],
        })

    statuses = Counter(str(row["current_status"]) for row in audited_rows)
    categories = Counter(str(row["category"]) for row in audited_rows)
    batches: dict[str, list[str]] = defaultdict(list)
    for row in audited_rows:
        batches[str(row["recommended_batch"])].append(str(row["unit_id"]))

    matrix_fields = [
        "unit_id", "unit_name", "category", "atomicity", "current_status", "target_status",
        "rule_refs", "spec_refs", "code_refs", "test_refs", "runtime_refs", "dependencies",
        "hidden_information_risk", "implementation_gap", "test_gap", "spec_gap", "severity",
        "estimated_complexity", "recommended_batch", "downstream_consumers", "production_callers", "traceability_evidence",
        "code_evidence", "test_evidence", "runtime_evidence", "traceability_evidence_present",
        "placeholder_detected", "split_merge_recommendation",
    ]
    with (OUT / "unit_gap_matrix_v3.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=matrix_fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(audited_rows)

    catalog_fields = [
        "unit_id", "unit_name", "category", "current_status", "target_status", "primary_inputs",
        "primary_outputs", "deterministic", "trainable", "rng_required", "visibility", "priority",
        "parameter_refs", "rule_refs", "spec_refs", "dependencies", "downstream_consumers",
        "recommended_batch",
    ]
    with (OUT / "unit_catalog_v3.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=catalog_fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(audited_rows)

    graph_lines = [
        "# 96 单元依赖图（Task 17）", "", f"> 生成日期：{date.today().isoformat()}。边 `A --> B` 表示 B 依赖 A。",
        "> 本图来自锁定目录的上游依赖字段；不把候选代码引用误当作架构依赖。", "", "## 分批视图", "",
    ]
    for batch in sorted(batches):
        graph_lines += [f"### {batch}", "", ", ".join(f"`{uid}`" for uid in batches[batch]), ""]
    graph_lines += ["## 完整邻接表", "", "| 单元 | 上游依赖 | 下游消费者 |", "|---|---|---|"]
    for row in audited_rows:
        graph_lines.append(f"| {row['unit_id']} | {row['dependencies'] or '—'} | {row['downstream_consumers'] or '—'} |")
    graph_lines += ["", "## 拆分/合并复核", ""]
    for uid, note in SPLIT_REVIEW.items():
        graph_lines.append(f"- `{uid}`：{note}。外部单元 ID 与契约保持不变。")
    graph_lines += ["", "未发现需要合并的锁定单元；相邻单元共享数据结构时应复用 Task 16 契约，而非合并职责。", ""]
    (OUT / "unit_dependency_graph.md").write_text("\n".join(graph_lines), encoding="utf-8")

    audited = [str(r["unit_id"]) for r in audited_rows if r["current_status"] == "AUDITED"]
    blocked = [str(r["unit_id"]) for r in audited_rows if r["current_status"] == "BLOCKED"]
    continue_impl = [str(r["unit_id"]) for r in audited_rows if r["current_status"] not in {"AUDITED", "BLOCKED"}]
    junit_path = OUT / "task17_full_junit.xml"
    test_run: dict[str, object] = {"status": "NOT_RUN", "path": str(junit_path.relative_to(ROOT))}
    if junit_path.is_file():
        suite = ET.parse(junit_path).getroot()
        if suite.tag == "testsuites" and len(suite):
            suite = suite[0]
        tests_count = int(suite.attrib.get("tests", 0))
        failures = int(suite.attrib.get("failures", 0))
        errors = int(suite.attrib.get("errors", 0))
        skipped = int(suite.attrib.get("skipped", 0))
        test_run.update({
            "status": "PASS" if failures == errors == 0 else "FAIL",
            "python": "3.12",
            "tests": tests_count,
            "passed": tests_count - failures - errors - skipped,
            "skipped": skipped,
            "failures": failures,
            "errors": errors,
            "time_seconds": float(suite.attrib.get("time", 0.0)),
        })
    summary = {
        "task": "Task 17 - 96-unit evidence rebaseline",
        "generated_on": date.today().isoformat(),
        "catalog_version": "SPEC-V3-3.1.0",
        "unit_count": len(audited_rows),
        "status_distribution": dict(sorted(statuses.items())),
        "category_distribution": dict(sorted(categories.items())),
        "legacy_migration_coverage": {"covered": len(legacy_ids), "expected": 96, "complete": True},
        "evidence_counts": {
            key: sum(bool(row[key]) for row in audited_rows)
            for key in ("code_evidence", "test_evidence", "runtime_evidence", "traceability_evidence_present")
        },
        "audited_units": audited,
        "blocked_units": blocked,
        "units_requiring_implementation_or_acceptance": continue_impl,
        "split_review_units": list(SPLIT_REVIEW),
        "merge_review_units": [],
        "recommended_batches": dict(sorted(batches.items())),
        "invalid_candidate_reference_count": len(invalid_refs),
        "placeholder_reference_count": len(placeholder_refs),
        "audit_constraints": {
            "audited_requires_all_four_evidence_classes": True,
            "old_status_reused": False,
            "candidate_references_revalidated": True,
            "bulk_implementation_performed": False,
        },
        "test_run": test_run,
        "source_hashes": {
            str(path.relative_to(ROOT)): file_hash(path)
            for path in (CATALOG, TRACE, M0, PILOT, LOCK, MIGRATION) if path.is_file()
        },
    }
    (OUT / "unit_rebaseline_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    report = [
        "# Task 17：96 单元真实基线复审报告", "", "状态：**Completed / Evidence Rebaseline**", "",
        "## 结论", "",
        f"本次从锁定的 96 单元目录重新取证，状态分布为：{json.dumps(dict(sorted(statuses.items())), ensure_ascii=False)}。",
        "旧的“33/61/2”统计未作为状态输入。M0 矩阵仅作为候选路径索引；脚本逐项验证当前文件、Python AST 符号、生产调用线索和测试函数。",
        "除任务14/15已经形成四类证据闭环的单元外，旧代码即使含相关语义也只记为 PARTIAL，直到锁定边界、直接测试、完整流程运行和追溯证据全部补齐。", "",
        "## 审计方法", "",
        "- 规格：核对目录、详细规格、规则参数追踪矩阵，确认 96 个 ID 唯一且均有正式定义。",
        "- 代码：逐个验证候选文件与 AST 符号；失效引用不进入 `code_refs`。",
        "- 测试：逐个验证测试文件/测试函数；计划中的文件若当前不存在，不计证据。",
        "- 运行：仅接受单元可归属的真实运行产物；普通测试文件存在不等于运行证据。",
        "- 追溯：逐项建立规则→详细规格→目标模块链；AUDITED 仍要求四类证据同时存在。",
        "- 安全：带 VISIBILITY 或私有/隐藏/全知语义的单元标为 `REQUIRES_BOUNDARY_TEST`，不等同于已发现泄漏。",
        "- 占位：对候选符号检查空 `pass` 与 `NotImplementedError`；固定返回值不自动判占位，以免误判合法常量函数。", "",
        "## 可直接验收与阻塞", "",
        "可直接维持 AUDITED：" + ", ".join(f"`{uid}`" for uid in audited) + "。",
        ("BLOCKED：" + ", ".join(f"`{uid}`" for uid in blocked) + "。") if blocked else "BLOCKED：无。当前差距均可通过既定实施/测试/证据流程关闭，未发现必须发明业务规则的矛盾。",
        "`MODEL-001` 保持 INTEGRATED：代码、测试、运行与追溯存在，但任务15确认其模型校准验收尚未满足，不能提升为 AUDITED。", "",
        "## 原子性、拆分与合并", "",
    ]
    for uid, note in SPLIT_REVIEW.items():
        report.append(f"- `{uid}`：{note}。建议只拆内部组件，保留锁定单元门面和 ID。")
    report += ["", "未发现必须合并的单元。", "", "## 主要差距", "",
        f"- 需继续实施或补证的单元：{len(continue_impl)} 个。",
        f"- 当前具备代码证据：{summary['evidence_counts']['code_evidence']} 个；测试证据：{summary['evidence_counts']['test_evidence']} 个；运行证据：{summary['evidence_counts']['runtime_evidence']} 个；追溯证据：{summary['evidence_counts']['traceability_evidence_present']} 个。",
        f"- 候选索引中已失效、未被继承的路径/符号/测试引用：{len(invalid_refs)} 条。",
        f"- 被明确识别为 `pass`/`NotImplementedError` 的候选符号引用：{len(placeholder_refs)} 条。",
        "- 最大系统性缺口是非试点单元缺少锁定边界的直接测试和单元归属明确的运行证据，而不是规格目录缺失。", "",
        "## 推荐开发批次", "",
    ]
    for batch in sorted(batches):
        report.append(f"- **{batch}**（{len(batches[batch])}）：" + ", ".join(f"`{uid}`" for uid in batches[batch]))
    report += ["", "批次内仍应按依赖图拓扑排序；每个单元在升级 AUDITED 前必须重新收集四类证据。", "",
        "## 审计边界", "",
        "本任务未修改业务代码、业务测试断言或规则文档；只生成新审计基线。失效候选引用保留为生成过程统计，不回写旧 M0 文件，以避免把历史线索改写成当前事实。", "",
        "## 可复现命令", "", "```bash", "python3 tools/task17_rebaseline.py", "pytest -q", "```", "",
    ]
    if test_run["status"] == "PASS":
        report[report.index("## 可复现命令"):report.index("## 可复现命令")] = [
            "## 当前测试执行", "",
            f"Python 3.12 全量测试：{test_run['passed']} passed、{test_run['skipped']} skipped、0 failed；JUnit：`{test_run['path']}`。", "",
        ]
        report[-3] = "PYTHONPYCACHEPREFIX=/tmp/task17_pycache .venv-macos/bin/python -m pytest -q --junitxml=docs/spec-v3/audit/task17_full_junit.xml"
    (OUT / "unit_rebaseline_report.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"statuses": dict(statuses), "invalid_refs": len(invalid_refs), "placeholders": len(placeholder_refs)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
