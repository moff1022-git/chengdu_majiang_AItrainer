from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/spec-v3/audit"
PLANS = ROOT / "docs/spec-v3/plans"
REPORTS = ROOT / "docs/spec-v3/reports"
GAP_SOURCE = AUDIT / "unit_gap_matrix_v3.csv"

AUDITED = {
    "RULE-003", "RULE-016", "ALGO-001", "ALGO-010", "HEUR-019",
    "STATE-005", "SCORE-001", "TRAIN-003", "AUDIT-003",
}

ATOMICITY_REVIEW = {"RULE-001", "ALGO-002", "ALGO-008", "SCORE-004", "AUDIT-009"}
MODEL_DATA = {"MODEL-001", "MODEL-002", "MODEL-003", "MODEL-004", "MODEL-005", "TRAIN-008", "AUDIT-012"}
EXTERNAL_PRIMARY = {"MODEL-001", "MODEL-005", "AUDIT-012"}

BATCHES = [
    ("B1-A", "deterministic-root", ["STATE-010", "ALGO-009", "ALGO-011"], [], "immediate", "P1"),
    ("B4-DATA-MODEL001", "model001-calibration-data", ["MODEL-001"], [], "external", "P3"),
    ("B1-B", "state-bootstrap", ["STATE-001", "STATE-011", "STATE-004"], ["B1-A"], "dependency", "P1"),
    ("B2-A1", "deterministic-prerequisites", ["STATE-002", "STATE-003", "ALGO-002"], ["B1-B"], "dependency", "P1"),
    ("B1-C1", "p0-rule-foundation", ["RULE-001", "RULE-002", "RULE-005", "RULE-006", "RULE-015"], ["B2-A1"], "dependency", "P1"),
    ("B2-A2", "decision-prerequisites", ["ALGO-006", "STATE-009"], ["B1-C1"], "dependency", "P1"),
    ("B1-C2", "p0-rule-claims", ["RULE-004", "RULE-007", "RULE-008", "RULE-010", "RULE-011", "RULE-012"], ["B1-C1"], "dependency", "P1"),
    ("B1-C3", "p0-response-score", ["RULE-009", "RULE-013", "RULE-014", "SCORE-002", "SCORE-003"], ["B1-C2"], "dependency", "P1"),
    ("B1-C4", "p0-terminal-score", ["SCORE-004", "SCORE-005", "SCORE-006"], ["B1-C3"], "dependency", "P1"),
    ("B2-B", "deterministic-completion", ["ALGO-003", "ALGO-004", "ALGO-005", "ALGO-007", "ALGO-008", "STATE-006", "STATE-007", "STATE-008", "STATE-012"], ["B1-C4", "B2-A2"], "dependency", "P1"),
    ("B3-A", "heuristic-foundation", ["HEUR-001", "HEUR-002", "HEUR-004", "HEUR-006", "HEUR-008", "HEUR-011", "HEUR-020", "HEUR-022"], ["B2-B"], "dependency", "P2"),
    ("B3-B", "heuristic-decision", ["HEUR-003", "HEUR-005", "HEUR-014", "HEUR-007", "HEUR-009", "HEUR-010", "HEUR-012", "HEUR-017", "HEUR-021", "HEUR-023"], ["B3-A"], "dependency", "P2"),
    ("B4-A", "model-inference-engineering", ["MODEL-002", "MODEL-003"], ["B2-B", "B3-A"], "dependency", "P2"),
    ("B3-C", "heuristic-risk-sequence", ["HEUR-013", "HEUR-015", "HEUR-016", "HEUR-018"], ["B3-B", "B4-A"], "dependency", "P2"),
    ("B5-A", "training-contracts", ["TRAIN-001", "TRAIN-002", "TRAIN-004", "TRAIN-005"], ["B2-B"], "dependency", "P2"),
    ("B4-A2", "trainable-policy-contract", ["MODEL-004"], ["B5-A"], "dependency", "P2"),
    ("B5-B", "training-environment", ["TRAIN-006", "TRAIN-009"], ["B5-A"], "dependency", "P2"),
    ("B5-C", "training-self-play", ["TRAIN-007"], ["B5-B"], "dependency", "P3"),
    ("B6-A", "audit-runtime", ["AUDIT-001", "AUDIT-002", "AUDIT-004", "AUDIT-005", "AUDIT-006", "AUDIT-007"], ["B2-B"], "dependency", "P2"),
    ("B6-B", "audit-trace-release", ["AUDIT-010", "AUDIT-008", "AUDIT-009", "AUDIT-011", "AUDIT-013", "AUDIT-014"], ["B6-A", "B5-B"], "dependency", "P3"),
    ("B5-DATA", "offline-training-data", ["TRAIN-008"], ["B6-B", "B5-A"], "dependency", "P3"),
    ("B4-B", "model-lifecycle", ["MODEL-005"], ["B4-A2", "B5-DATA", "B6-B"], "external", "P3"),
    ("B6-C", "external-effect-evaluation", ["AUDIT-012"], ["B4-B", "B5-C", "B6-B"], "external", "P4"),
]

GAP_FIELDS = [
    "gap_spec", "gap_code", "gap_direct_test", "gap_branch_test",
    "gap_integration", "gap_runtime", "gap_trace", "gap_boundary",
    "gap_reproducibility", "gap_model_data", "gap_performance", "gap_atomicity",
]

OUT_FIELDS = [
    "unit_id", "unit_name", "category", "task17_status", "primary_completion_path",
    *GAP_FIELDS, "code_refs", "test_refs", "runtime_refs", "rule_refs", "spec_refs",
    "dependencies", "estimated_complexity", "recommended_batch", "recommended_action",
    "audit_exit_criteria", "notes",
]


def truth(value: str) -> bool:
    return value.strip().lower() == "true"


def join_nonempty(*parts: str) -> str:
    return "；".join(p for p in parts if p and p != "NONE")


def batch_map() -> dict[str, str]:
    result: dict[str, str] = {}
    for batch_id, _, unit_ids, *_ in BATCHES:
        for unit_id in unit_ids:
            if unit_id in result:
                raise ValueError(f"duplicate batch assignment: {unit_id}")
            result[unit_id] = batch_id
    return result


def completion_path(row: dict[str, str]) -> str:
    unit_id = row["unit_id"]
    if unit_id == "HEUR-016":
        return "PATH-FULL-IMPLEMENTATION"
    if unit_id in EXTERNAL_PRIMARY:
        return "PATH-EXTERNAL-DATA"
    # Task 17 only validated candidate implementations for PARTIAL units.  It did
    # not prove their full locked semantics, so evidence-only/test-only paths would
    # overstate the evidence.  Keep the classification conservative.
    return "PATH-SEMANTIC-COMPLETION"


def classify(row: dict[str, str], batches: dict[str, str]) -> dict[str, str]:
    unit_id = row["unit_id"]
    runtime_missing = not truth(row["runtime_evidence"])
    boundary = row["hidden_information_risk"] == "REQUIRES_BOUNDARY_TEST"
    full_impl = unit_id == "HEUR-016"
    external = unit_id in EXTERNAL_PRIMARY
    semantic = not full_impl and not external
    gap_code = full_impl or row["implementation_gap"] != "NONE"
    gap_trace = runtime_missing or not truth(row["traceability_evidence_present"])

    if full_impl:
        action = "按Locked规格新增独立生产单元；补正常/边界/异常/集成/回放测试并接入生产调用链"
    elif external:
        action = "保持现有安全fallback/框架；建设隔离数据发布、训练/校准或外部评价证据，不阻断B1-B3"
    else:
        action = "对照Locked规格逐字段核验候选实现，补齐缺失语义并建立直接、分支、集成、回放与性能证据"

    exit_criteria = (
        "同一版本scope内：Locked规格无歧义；非占位生产实现覆盖主要语义并接入正确调用链；"
        "直接/分支/边界测试通过；运行证据含unit_id、scenario/game_id、输入摘要、参数版本、seed、"
        "中间结果、输出、调用位置和测试/回放引用；追踪闭环；性能达规格；AC-01～AC-14适用项全Passed且独立审计通过"
    )
    if unit_id == "MODEL-001":
        exit_criteria += "；另需≥10000有效样本冻结发布、隔离label zone、分组防泄漏切分及Brier/log loss/15-bin ECE/CI通过"

    notes = join_nonempty(
        row["implementation_gap"],
        row["test_gap"],
        row["split_merge_recommendation"],
        "Task17状态保持不变；本表是计划分型，不是新验收" if True else "",
    )
    return {
        "unit_id": unit_id,
        "unit_name": row["unit_name"],
        "category": row["category"],
        "task17_status": row["current_status"],
        "primary_completion_path": completion_path(row),
        "gap_spec": "false",
        "gap_code": str(gap_code).lower(),
        "gap_direct_test": str(unit_id != "MODEL-001").lower(),
        "gap_branch_test": "true",
        "gap_integration": str(runtime_missing).lower(),
        "gap_runtime": str(runtime_missing).lower(),
        "gap_trace": str(gap_trace).lower(),
        "gap_boundary": str(boundary).lower(),
        "gap_reproducibility": str(runtime_missing).lower(),
        "gap_model_data": str(unit_id in MODEL_DATA).lower(),
        "gap_performance": str(runtime_missing).lower(),
        "gap_atomicity": str(unit_id in ATOMICITY_REVIEW).lower(),
        "code_refs": row["code_refs"],
        "test_refs": row["test_refs"],
        "runtime_refs": row["runtime_refs"],
        "rule_refs": row["rule_refs"],
        "spec_refs": row["spec_refs"],
        "dependencies": row["dependencies"],
        "estimated_complexity": row["estimated_complexity"],
        "recommended_batch": batches[unit_id],
        "recommended_action": action,
        "audit_exit_criteria": exit_criteria,
        "notes": notes,
    }


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def regression_scope(batch_id: str, unit_ids: list[str]) -> str:
    categories = sorted({unit_id.split("-")[0] for unit_id in unit_ids})
    return (
        f"新增tests/spec_v3直接/分支/异常/性质测试；相关现有{'/'.join(categories)}定向测试；"
        "contracts与固定seed回放；全仓pytest；失败时只在实施任务修复"
    )


def boundary_scope(unit_ids: list[str], rows_by_id: dict[str, dict[str, str]]) -> str:
    risky = [u for u in unit_ids if rows_by_id[u]["gap_boundary"] == "true"]
    if not risky:
        return "本批无新增REQUIRES_BOUNDARY_TEST单元；仍回归公共visibility contract"
    return (
        "覆盖" + "|".join(risky) + "；PlayerView白名单、对手暗手/墙序递归sentinel、对象引用/缓存/日志隔离、"
        "隐藏字段删除或扰动不改变同可见状态决策；权威引擎全知权限与策略边界分离"
    )


def entry_criteria(batch_id: str, dependencies: list[str], gate: str) -> str:
    base = "Task17基线与Frozen公共契约未变；批次规格Locked；工作树已保护；前置批次独立审计通过"
    if batch_id == "B1-A":
        return "STATE-010无未满足单元依赖；先完成STATE-010，再并行ALGO-009/ALGO-011；MODEL001数据缺口不阻断"
    if gate == "external":
        return base + "；所需冻结数据/模型/评价发布已到位并通过schema、来源、许可和泄漏预检"
    return base + ("；前置=" + "|".join(dependencies) if dependencies else "")


def exit_criteria(batch_id: str, unit_ids: list[str]) -> str:
    return (
        "每个单元独立具备代码、直接测试、可归属运行、追踪四类证据；关键分支与信息边界门禁通过；"
        "固定seed/版本/状态复现；性能达Locked阈值；全量回归通过；开发人与独立审计结论分离；"
        f"批次{batch_id}内{len(unit_ids)}个单元不得以批量PASS替代逐单元AC验收"
    )


def create_batch_rows(rows_by_id: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    result = []
    for order, (batch_id, phase, unit_ids, dependencies, gate, parallel_group) in enumerate(BATCHES, 1):
        result.append({
            "batch_id": batch_id,
            "order": str(order),
            "phase": phase,
            "unit_count": str(len(unit_ids)),
            "unit_ids": "|".join(unit_ids),
            "dependency_batches": "|".join(dependencies),
            "gate_type": gate,
            "parallel_group": parallel_group,
            "entry_criteria": entry_criteria(batch_id, dependencies, gate),
            "exit_criteria": exit_criteria(batch_id, unit_ids),
            "regression_scope": regression_scope(batch_id, unit_ids),
            "boundary_test_scope": boundary_scope(unit_ids, rows_by_id),
        })
    return result


def build_queue(batch_rows: list[dict[str, str]]) -> dict:
    immediately = [r["batch_id"] for r in batch_rows if r["gate_type"] == "immediate"]
    dependency = [r["batch_id"] for r in batch_rows if r["gate_type"] == "dependency"]
    external = [r["batch_id"] for r in batch_rows if r["gate_type"] == "external"]
    return {
        "task": "Task 18A executable queue",
        "generated_on": "2026-07-30",
        "authoritative_status_unchanged": {"AUDITED": 9, "INTEGRATED": 1, "PARTIAL": 85, "SCAFFOLDED": 1, "BLOCKED": 0},
        "current_test_baseline": {"python": "3.12.10", "tests": 387, "passed": 387, "failed": 0, "skipped": 0, "time_seconds": 234.46},
        "immediately_executable_batches": immediately,
        "dependency_blocked_batches": dependency,
        "external_data_gated_batches": external,
        "batch_unit_ids": {r["batch_id"]: r["unit_ids"].split("|") for r in batch_rows},
        "entry_criteria": {r["batch_id"]: r["entry_criteria"] for r in batch_rows},
        "exit_criteria": {r["batch_id"]: r["exit_criteria"] for r in batch_rows},
        "regression_scope": {r["batch_id"]: r["regression_scope"] for r in batch_rows},
        "boundary_test_scope": {r["batch_id"]: r["boundary_test_scope"] for r in batch_rows},
        "recommended_order": [r["batch_id"] for r in batch_rows],
        "parallel_groups": {
            "P1": [r["batch_id"] for r in batch_rows if r["parallel_group"] == "P1"],
            "P2": [r["batch_id"] for r in batch_rows if r["parallel_group"] == "P2"],
            "P3": [r["batch_id"] for r in batch_rows if r["parallel_group"] == "P3"],
            "P4": [r["batch_id"] for r in batch_rows if r["parallel_group"] == "P4"],
            "notes": [
                "同组仅表示上游满足后可并行，不覆盖dependency_batches",
                "MODEL-001数据轨与B1/B2/B3工程轨并行，不能传播为确定性开发阻塞",
                "开发实现与独立审计必须由不同执行步骤完成",
            ],
        },
    }


def md_table(rows: list[list[str]], headers: list[str]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out.extend("| " + " | ".join(cell.replace("|", "/") for cell in row) + " |" for row in rows)
    return "\n".join(out)


def write_markdown_outputs(classified: list[dict[str, str]], batch_rows: list[dict[str, str]]) -> None:
    path_counts = Counter(row["primary_completion_path"] for row in classified)
    gap_counts = {gap: sum(row[gap] == "true" for row in classified) for gap in GAP_FIELDS}

    batch_table = md_table([
        [r["batch_id"], r["order"], r["phase"], r["unit_count"], r["unit_ids"], r["dependency_batches"] or "—", r["gate_type"]]
        for r in batch_rows
    ], ["批次", "顺序", "目标", "数量", "单元", "前置批次", "门禁"])
    plan = f"""# Task 18A：Spec v3 可执行开发批次

状态：**Ready for execution planning / no audit status change**  
基线：Task 17（9 AUDITED / 1 INTEGRATED / 85 PARTIAL / 1 SCAFFOLDED）  
当前测试：Windows Python 3.12.10，387 passed，0 failed，0 skipped，234.46s

## 规划结论

87 个非 AUDITED 单元已全部分配到 23 个可执行小批次，每批 1～10 个单元；小于 5 个的批次均由强依赖或外部数据门禁造成。没有把 MODEL-001 数据问题传播为 B1～B3 阻塞。

`B1-A` 是唯一立即可启动批次。依赖矩阵显示 `STATE-010` 无单元依赖，`ALGO-009` 和 `ALGO-011` 均依赖 `STATE-010`，所以批内拓扑顺序为 `STATE-010 → ALGO-009 / ALGO-011`。

## 批次总表

{batch_table}

## 统一入口条件

1. Task 17 状态与 Frozen 公共契约保持不变；Locked 规格无待决歧义。
2. 上游批次中的每个依赖单元均已独立审计通过，而非只有批次总测试通过。
3. 开始前记录 Git/版本/测试基线；保护用户已有工作树。
4. 开发步骤与独立审计步骤分开；不得由实现完成自动写成 AUDITED。

## 统一退出条件

1. 每单元分别取得规格、非占位生产代码、直接与分支测试、生产接线、可归属运行和全链追踪证据。
2. 运行记录含 unit_id、scenario/game_id、输入摘要、参数版本、seed、候选/中间结果、最终输出、调用位置和测试/回放引用。
3. 所有适用 AC-01～AC-14 为 Passed，无开放 High/Critical；性能满足 Locked 规格。
4. 批次定向、公共契约、固定 seed 回放、信息边界专项和全仓 pytest 均通过。

## 信息边界回归

Task 17 的全部 86 个 `REQUIRES_BOUNDARY_TEST` 单元均进入专项测试总体范围：8 个已 AUDITED 单元继续作为回归基线，78 个位于本计划矩阵并按所属批次执行。该标记表示必须测试，不表示已发现泄漏。

专项测试统一验证 PlayerView 默认拒绝白名单、对手暗手/墙序递归 sentinel、对象引用/缓存/日志/派生字段隔离，以及同一可见状态下隐藏字段删除或扰动不改变策略决策。规则裁判和模拟器依法可读全知状态，但必须验证与策略模块隔离。

## 并行规则

- P1 为确定性主链，只能按依赖顺序推进。
- P2 中 B3、B4 工程、B5 和 B6 可在共同上游 B2-B 完成后按各自依赖并行。
- P3/P4 涉及模型发布、离线数据或最终外部评价；没有冻结数据时可继续工程准备，但不得宣称外部效果通过。
- MODEL-001 数据轨与 B1/B2/B3 独立并行。
"""
    (PLANS / "development_batches_v3.md").write_text(plan, encoding="utf-8")

    model_track = """# MODEL-001 独立数据与校准轨道

状态：**EXTERNAL DATA GATED / rule fallback remains usable**

## 不影响确定性开发的结论

MODEL-001 保持 Task 17 的 INTEGRATED。当前规则 fallback、合法动作约束和隐藏字段拒绝链可继续用于 B1～B3；缺少外部数据不得阻塞确定性规则、算法、状态或启发式开发，也不得把 MODEL-001 降级为未实现。

## 数据门禁

关闭 `MODEL001-DATA-001` 至少需要：

1. 版本化冻结评估发布，≥10,000 个符合规则与schema的有效样本；
2. 物理隔离的 `policy_features` 与 `restricted_label_zone`；
3. 按玩家、比赛、牌局和 seed-family 分组的 train/validation/test manifest；
4. 来源、许可/同意、规则集、schema、生成器、时间范围和 canonical SHA-256；
5. 泄漏扫描、重复/近重复检查、缺失/范围/分布报告；
6. 若声称训练模型优于 fallback，提供冻结模型产物及训练配置；
7. 分任务 Brier、log loss、15-bin ECE、可靠性、top-2 recall 和 95% CI；
8. 与规则 fallback 的同样本比较、OOD/超时/版本不匹配回退验证；
9. 评估器与策略进程/对象/schema隔离，truth 不进入 Observation、势能、日志明文或解释字段。

## 禁止证据

- 不能用规则 fallback 生成标签后评价同一 fallback；
- 不能把历史普通游戏日志补字段后冒充冻结校准发布；
- 不能用训练集指标替代隔离测试集；
- 不能只报 accuracy；
- 不能因工程测试通过而把 MODEL-001 提升为 AUDITED。

## 可并行工程工作

可先完成数据 schema、manifest validator、泄漏扫描器、metric runner、fallback 对照接口和证据包模板；这些工作不改变 MODEL-001 状态。最终 AUDITED 仍要求数据发布和独立审计。
"""
    (PLANS / "model001_data_track.md").write_text(model_track, encoding="utf-8")

    path_table = md_table([[k, str(v)] for k, v in sorted(path_counts.items())], ["主要完成路径", "单元数"])
    gap_table = md_table([[k, str(v)] for k, v in gap_counts.items()], ["缺口类型", "单元数"])
    report = f"""# Task 18A：87 个非 AUDITED 单元缺口分型与批次规划报告

状态：**Completed / planning evidence only**  
权威来源：`docs/spec-v3/audit/task17_96_unit_audit_clarification.md`  
当前工作树测试：387 passed，0 failed，0 skipped，234.46s

## 技术摘要

Task 17 的 9/1/85/1 状态未改变。87 个非 AUDITED 单元已完成逐行分型、主要完成路径分配和无重复批次归属。由于 Task 17 对 85 个 PARTIAL 只确认了候选实现/测试线索，没有证明完整 Locked 语义，本计划保守地不把任何 PARTIAL 标成 `PATH-EVIDENCE-ONLY`、`PATH-TEST-CLOSURE` 或 `PATH-INTEGRATION-CLOSURE`。

{path_table}

`PATH-SEMANTIC-COMPLETION` 包含仍需逐字段验证并可能补齐语义的单元；这不表示必须重写全部候选实现。`HEUR-016` 是唯一完整实现路径。`MODEL-001`、`MODEL-005`、`AUDIT-012` 以外部数据/产物/效果证据为主要完成路径，其中只有 MODEL-001 的规则 fallback 已形成 INTEGRATED 工程链。

## 范围、数据与定义

分析总体是 SPEC-V3-3.1.0 的 96 个锁定单元；待规划总体是剔除 9 个 AUDITED 后的 87 个唯一 unit_id。输入以 Task 17 gap matrix 为行粒度，以 Task 15 试点证据、Task 16 Frozen 契约、96 单元规格卡及当前代码/测试目录为约束来源。布尔缺口表示“仍需闭合的验收条件”，不表示已确认缺陷；主要完成路径表示当前最主要的闭合方式，不排除同一单元具有多个缺口。

## 缺口分布

{gap_table}

`gap_spec=0`：96 个 Locked 单元规格和追踪端点齐全，当前未发现必须先做规则决策的单元。`gap_direct_test=86` 使用 Locked 单元直接验收口径；MODEL-001 已有直接工程测试，其缺口是校准分支与外部数据。其余单元即使 Task 17 找到旧测试候选，也不等于直接测试闭环。`gap_boundary` 只表示专项测试要求，不表示泄漏已发生。

## 关键分型

- 只补证据且不改业务代码：当前为 0。原因是 Task 17 没有证明任何 PARTIAL 的完整生产语义；未来批次复核若证明语义完整，可在新证据下改走 evidence-only，但不能在 Task 18A 预判。
- 需要语义补全：83。应优先复用候选实现，只补锁定语义缺口，禁止无关重构。
- 需要完整实现：1，即 `HEUR-016`。
- 主要外部数据路径：3，即 `MODEL-001`、`MODEL-005`、`AUDIT-012`。
- 含 `GAP-MODEL-DATA`：7，即 MODEL-001～005、TRAIN-008、AUDIT-012；其中工程准备和确定性 fallback 可继续。
- 原子性内部拆分复核：5，即 RULE-001、ALGO-002、ALGO-008、SCORE-004、AUDIT-009；只拆内部职责，不改变 Locked ID/门面。

## 第一批

立即执行 `B1-A = STATE-010, ALGO-009, ALGO-011`。真实依赖根是 STATE-010；完成并独立审计 STATE-010 后，ALGO-009 与 ALGO-011 可并行开发与取证。

## 方法与限制

分型直接继承 Task 17 的代码、测试、运行、追踪、依赖、风险和原子性字段，并对 Task 15 试点与 Task 16 Frozen 契约进行约束复核。Task 18A 没有重跑逐单元生产 trace，因此所有状态保持不变；本报告是执行计划，不是新的 AUDITED 判定。

稳健性检查包括：96/87集合差、状态透视、分类计数、批次并集/交集、逐单元依赖顺序、批次依赖顺序、MODEL-001与HEUR-016特例、86个边界测试标记覆盖及每批入口/出口字段完整性。主要限制是 Task 17 对多数单元只保留候选实现/测试线索，因此本计划宁可归入语义补全，也不无证据推断为 evidence-only。

## 建议下一步

启动 B1-A 的 Docs-First 实施与独立审计。实现阶段只能修改该批范围，测试阶段补直接/分支/边界/回放，审计阶段再决定三个单元是否逐个达到 AUDITED。

下一条可直接用于开发的 Codex 提示词：

```text
执行成都麻将AI训练模拟器 Task 18 B1-A：仅处理 STATE-010、ALGO-009、ALGO-011。以 docs/spec-v3/plans/development_batches_v3.md、task18_gap_classification.csv、Task 16 Frozen 公共契约和 Locked 单元规格为权威。先按 STATE-010 → ALGO-009/ALGO-011 的批内拓扑核实现有代码与测试；规格已 Approved/Locked 后再补齐最小业务语义，不做无关重构。为每个单元分别补直接、关键分支、异常、固定 seed、性能、生产接线、运行 trace、追踪及信息边界测试，运行定向/契约/全仓回归。开发交付与独立审计分开；没有四类证据和 AC-01～AC-14 闭环不得标 AUDITED。不得修改其他 Task 17 状态，不得让 MODEL-001 数据门禁阻塞本批。
```

## 进一步问题

- B1-A 实施取证后，哪些候选实现可被证明语义完整并转为 test/evidence closure，而无需继续改业务逻辑？
- MODEL-001 合规冻结数据由谁提供、采用何种来源许可与玩家/牌局分组键？
- 独立审计执行者与开发执行者如何在仓库证据包中记录分离签名？
"""
    (REPORTS / "task18_planning_report.md").write_text(report, encoding="utf-8")

    test_baseline = """# Task 18A 当前工作树测试基线

状态：**PASS**  
日期：2026-07-30  
命令：`.\\.venv\\Scripts\\python.exe -m pytest -q`

| 项 | 结果 |
|---|---:|
| Python | 3.12.10 |
| collected/executed | 387 |
| passed | 387 |
| failed | 0 |
| errors | 0 |
| skipped | 0 |
| duration | 234.46s（pytest报告；外层进程约251s） |

## 解释边界

该结果是 Task 18A 开始时当前工作树的全仓回归基线。它证明当前标准测试命令通过，但不自动形成 87 个单元各自的直接测试、运行归属或 AUDITED 证据，也不改变 Task 17 权威状态。

工作树在测试前已有 668 个 Git porcelain 条目；本任务将其视为用户既有修改并予以保护。测试无失败，因此没有失败到单元的关联记录。
"""
    (REPORTS / "task18_current_test_baseline.md").write_text(test_baseline, encoding="utf-8")


def validate(source_rows: list[dict[str, str]], classified: list[dict[str, str]], batch_rows: list[dict[str, str]]) -> None:
    source_ids = {row["unit_id"] for row in source_rows}
    classified_ids = [row["unit_id"] for row in classified]
    if len(source_rows) != 96 or len(source_ids) != 96:
        raise ValueError("Task17 source must contain 96 unique units")
    if len(classified) != 87 or len(set(classified_ids)) != 87:
        raise ValueError("classification must contain 87 unique units")
    if set(classified_ids) != source_ids - AUDITED:
        raise ValueError("classification set differs from Task17 non-AUDITED set")
    if any(unit_id in AUDITED for unit_id in classified_ids):
        raise ValueError("AUDITED unit leaked into classification")
    statuses = Counter(row["current_status"] for row in source_rows)
    if statuses != Counter({"AUDITED": 9, "INTEGRATED": 1, "PARTIAL": 85, "SCAFFOLDED": 1}):
        raise ValueError(f"unexpected Task17 status distribution: {statuses}")
    graph = {
        row["unit_id"]: [
            dep for dep in row["dependencies"].split("|")
            if dep and dep != "无"
        ]
        for row in source_rows
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(unit_id: str) -> None:
        if unit_id in visiting:
            raise ValueError(f"unit dependency cycle detected at {unit_id}")
        if unit_id in visited:
            return
        visiting.add(unit_id)
        for dep in graph[unit_id]:
            if dep not in graph:
                raise ValueError(f"unknown unit dependency: {unit_id} <- {dep}")
            visit(dep)
        visiting.remove(unit_id)
        visited.add(unit_id)

    for unit_id in graph:
        visit(unit_id)
    if sum(row["task17_status"] == "PARTIAL" for row in classified) != 85:
        raise ValueError("all 85 PARTIAL units must be classified")
    if next(row for row in classified if row["unit_id"] == "MODEL-001")["primary_completion_path"] != "PATH-EXTERNAL-DATA":
        raise ValueError("MODEL-001 must be on external data path")
    if next(row for row in classified if row["unit_id"] == "HEUR-016")["primary_completion_path"] != "PATH-FULL-IMPLEMENTATION":
        raise ValueError("HEUR-016 must have an independent full implementation path")
    batch_ids = [unit_id for row in batch_rows for unit_id in row["unit_ids"].split("|")]
    if len(batch_ids) != 87 or len(set(batch_ids)) != 87 or set(batch_ids) != set(classified_ids):
        raise ValueError("batch unit sets must cover all 87 units exactly once")
    known_batches = {row["batch_id"] for row in batch_rows}
    order = {row["batch_id"]: int(row["order"]) for row in batch_rows}
    unit_order = {
        unit_id: int(row["order"])
        for row in batch_rows
        for unit_id in row["unit_ids"].split("|")
    }
    for row in batch_rows:
        for dep in filter(None, row["dependency_batches"].split("|")):
            if dep not in known_batches or order[dep] >= order[row["batch_id"]]:
                raise ValueError(f"batch dependency is missing or cyclic: {dep}->{row['batch_id']}")
        if not row["entry_criteria"] or not row["exit_criteria"]:
            raise ValueError(f"missing entry/exit criteria: {row['batch_id']}")
    for row in classified:
        # MODEL-001 is already INTEGRATED; this batch closes only its independent
        # calibration publication and therefore does not rebuild its engineering deps.
        if row["unit_id"] == "MODEL-001":
            continue
        for dep in row["dependencies"].split("|"):
            if not dep or dep == "无" or dep in AUDITED:
                continue
            if dep not in unit_order:
                raise ValueError(f"missing planned dependency: {row['unit_id']} <- {dep}")
            if unit_order[dep] > unit_order[row["unit_id"]]:
                raise ValueError(
                    f"unit dependency scheduled too late: {row['unit_id']} <- {dep}"
                )


def main() -> None:
    PLANS.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    with GAP_SOURCE.open(encoding="utf-8-sig", newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    batches = batch_map()
    classified = [classify(row, batches) for row in source_rows if row["unit_id"] not in AUDITED]
    rows_by_id = {row["unit_id"]: row for row in classified}
    batch_rows = create_batch_rows(rows_by_id)
    validate(source_rows, classified, batch_rows)

    write_csv(PLANS / "task18_gap_classification.csv", OUT_FIELDS, classified)
    batch_fields = [
        "batch_id", "order", "phase", "unit_count", "unit_ids", "dependency_batches",
        "gate_type", "parallel_group", "entry_criteria", "exit_criteria",
        "regression_scope", "boundary_test_scope",
    ]
    write_csv(PLANS / "development_batches_v3.csv", batch_fields, batch_rows)
    (PLANS / "task18_execution_queue.json").write_text(
        json.dumps(build_queue(batch_rows), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_markdown_outputs(classified, batch_rows)
    print(json.dumps({
        "classified_units": len(classified),
        "path_distribution": Counter(row["primary_completion_path"] for row in classified),
        "gap_distribution": {gap: sum(row[gap] == "true" for row in classified) for gap in GAP_FIELDS},
        "batches": len(batch_rows),
        "batch_units": sum(int(row["unit_count"]) for row in batch_rows),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
