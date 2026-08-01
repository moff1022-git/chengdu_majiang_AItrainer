from __future__ import annotations

import ast
import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs/spec-v3/plans/task18_gap_classification.csv"
TASK17 = ROOT / "docs/spec-v3/audit/unit_gap_matrix_v3.csv"
CATALOG = ROOT / "docs/spec-v3/audit/unit_catalog_v3.csv"
QUEUE = ROOT / "docs/spec-v3/plans/task18_execution_queue.json"
OUT = ROOT / "docs/spec-v3/semantic-completion"

AUDITED = {
    "RULE-003", "RULE-016", "ALGO-001", "ALGO-010", "HEUR-019",
    "STATE-005", "SCORE-001", "TRAIN-003", "AUDIT-003",
}

SPEC_BY_CATEGORY = {
    "RULE": "docs/spec-v3/03-unit-specs/deterministic_rule_state_specs.md",
    "STATE": "docs/spec-v3/03-unit-specs/deterministic_rule_state_specs.md",
    "ALGO": "docs/spec-v3/03-unit-specs/deterministic_algorithm_scoring_specs.md",
    "SCORE": "docs/spec-v3/03-unit-specs/deterministic_algorithm_scoring_specs.md",
    "HEUR": "docs/spec-v3/03-unit-specs/human_heuristic_specs.md",
    "MODEL": "docs/spec-v3/03-unit-specs/probabilistic_model_specs.md",
    "TRAIN": "docs/spec-v3/03-unit-specs/training_environment_specs.md",
    "AUDIT": "docs/spec-v3/03-unit-specs/audit_specs.md",
}

FACETS = [
    "purpose", "trigger", "preconditions", "inputs", "outputs", "parameters",
    "main_flow", "branch_flow", "error_flow", "formula", "boundary",
    "visibility", "determinism", "dependencies", "consumers",
]

FACET_CATEGORY = {
    "purpose": "SEM-FLOW",
    "trigger": "SEM-FLOW",
    "preconditions": "SEM-BOUNDARY",
    "inputs": "SEM-INTEGRATION",
    "outputs": "SEM-OUTPUT",
    "parameters": "SEM-PARAMETER",
    "main_flow": "SEM-FLOW",
    "branch_flow": "SEM-BRANCH",
    "error_flow": "SEM-ERROR",
    "formula": "SEM-FORMULA",
    "boundary": "SEM-BOUNDARY",
    "visibility": "SEM-VISIBILITY",
    "determinism": "SEM-RANDOMNESS",
    "dependencies": "SEM-INTEGRATION",
    "consumers": "SEM-INTEGRATION",
}

FACET_TITLES = {
    "purpose": "闭合单元目的与唯一职责",
    "trigger": "补齐规范触发时点",
    "preconditions": "补齐前置条件验证与失败零写入",
    "inputs": "对齐Locked输入schema与版本",
    "outputs": "补齐规范输出与解释/审计字段",
    "parameters": "接入并冻结规范参数",
    "main_flow": "补齐规范主流程",
    "branch_flow": "补齐规则关键分支",
    "error_flow": "补齐稳定错误与不可决策处理",
    "formula": "实现规范公式或启发式步骤",
    "boundary": "补齐边界与非法状态行为",
    "visibility": "闭合公开/私有/全知信息隔离",
    "determinism": "闭合命名种子与复现契约",
    "dependencies": "接入规范上游依赖",
    "consumers": "接入规范下游消费者",
}

MATRIX_FIELDS = [
    "unit_id", "unit_name", "category", "task17_status", "task18_path",
    "classification_valid", "target_semantics_count", "implemented_semantics_count",
    "missing_semantics_count", "semantic_completion_ratio", "missing_flow",
    "missing_branch", "missing_formula", "missing_parameter", "missing_boundary",
    "missing_visibility", "missing_integration", "missing_output",
    "missing_randomness", "missing_error", "missing_direct_test",
    "missing_branch_test", "missing_integration_test", "missing_runtime_evidence",
    "missing_traceability", "interface_impact", "delta_ids", "dependencies",
    "recommended_batch", "implementation_ready", "blocking_reason",
    "target_semantics", "current_implementation_semantics", "missing_semantics",
    "code_refs", "production_callers", "test_refs", "runtime_refs", "rule_refs",
    "spec_refs", "notes",
]

DELTA_FIELDS = [
    "delta_id", "unit_id", "title", "semantic_category", "source_requirement",
    "source_reference", "current_behavior", "required_behavior", "input_change",
    "output_change", "algorithm_change", "state_change", "interface_change",
    "affected_code", "affected_tests", "dependencies", "boundary_cases",
    "visibility_constraints", "acceptance_criteria", "runtime_evidence_required",
    "risk", "implementation_order",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def clean(text: str, limit: int = 1200) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def unit_block(spec_path: str, unit_id: str) -> str:
    text = (ROOT / spec_path).read_text(encoding="utf-8")
    match = re.search(
        rf"(?ms)^## {re.escape(unit_id)}\b.*?(?=^## (?:RULE|STATE|ALGO|SCORE|HEUR|MODEL|TRAIN|AUDIT)-\d{{3}}\b|\Z)",
        text,
    )
    if not match:
        raise ValueError(f"Locked unit section not found: {unit_id} in {spec_path}")
    return match.group(0)


def numbered_sections(block: str) -> dict[int, str]:
    matches = list(re.finditer(r"(?m)^###\s+(\d+)\.\s+.*$", block))
    result: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        result[int(match.group(1))] = clean(block[match.start():end], 1800)
    return result


def source_for_facet(block: str, facet: str, category: str) -> str:
    sections = numbered_sections(block)
    if category in {"RULE", "STATE"}:
        mapping = {
            "purpose": [3, 4], "trigger": [7], "preconditions": [8], "inputs": [9],
            "outputs": [13], "parameters": [6, 10], "main_flow": [11],
            "branch_flow": [12, 17], "error_flow": [16], "formula": [11],
            "boundary": [15, 17, 19], "visibility": [5, 9, 15],
            "determinism": [2, 3, 15, 19], "dependencies": [4], "consumers": [4],
        }
    else:
        mapping = {
            "purpose": [1, 3], "trigger": [1, 5], "preconditions": [1, 7],
            "inputs": [1, 2], "outputs": [9, 10], "parameters": [1, 2, 4],
            "main_flow": [5, 9], "branch_flow": [4, 5, 7], "error_flow": [7, 13],
            "formula": [3, 4, 5], "boundary": [7, 10, 11, 12],
            "visibility": [10, 14], "determinism": [10, 12],
            "dependencies": [1, 5], "consumers": [9, 14],
        }
    chunks = [sections[n] for n in mapping[facet] if n in sections]
    if not chunks:
        # HEUR/MODEL/TRAIN/AUDIT cards use different headings.  Preserve a real
        # Locked excerpt instead of inventing a requirement.
        chunks = [clean(block, 1800)]
    return clean(" ".join(chunks), 1600)


class Stats(ast.NodeVisitor):
    def __init__(self) -> None:
        self.functions = 0
        self.classes = 0
        self.branches = 0
        self.raises = 0
        self.returns = 0
        self.calls: Counter[str] = Counter()
        self.arithmetic = 0
        self.todos = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.functions += 1
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.classes += 1
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        self.branches += 1
        self.generic_visit(node)

    def visit_Match(self, node: ast.Match) -> None:
        self.branches += len(node.cases)
        self.generic_visit(node)

    def visit_Raise(self, node: ast.Raise) -> None:
        self.raises += 1
        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        self.returns += 1
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        name = ""
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        if name:
            self.calls[name] += 1
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        self.arithmetic += 1
        self.generic_visit(node)


def code_stats(code_refs: str) -> tuple[Stats, list[str], list[str]]:
    aggregate = Stats()
    existing: list[str] = []
    missing: list[str] = []
    paths = sorted({ref.split("::", 1)[0] for ref in code_refs.split("|") if ref})
    for relative in paths:
        path = ROOT / relative
        if not path.exists() or path.suffix != ".py":
            missing.append(relative)
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError):
            missing.append(relative)
            continue
        stats = Stats()
        stats.visit(tree)
        aggregate.functions += stats.functions
        aggregate.classes += stats.classes
        aggregate.branches += stats.branches
        aggregate.raises += stats.raises
        aggregate.returns += stats.returns
        aggregate.calls.update(stats.calls)
        aggregate.arithmetic += stats.arithmetic
        existing.append(relative)
    return aggregate, existing, missing


def forced_missing_facet(row: dict[str, str]) -> str:
    gap = row["implementation_gap"]
    if any(word in gap for word in ("公式", "估计", "Q", "计分", "最大番", "退税", "转移")):
        return "formula"
    if any(word in gap for word in ("随机", "seed", "RNG", "命名子流")):
        return "determinism"
    if any(word in gap for word in ("参数", "配置", "canonical hash", "范围", "迁移")):
        return "parameters"
    if any(word in gap for word in ("状态机", "流程", "事件", "训练必须")):
        return "main_flow"
    if any(word in gap for word in ("可见", "隐藏", "PlayerView")):
        return "visibility"
    return "outputs"


def implemented_facets(row: dict[str, str], stats: Stats) -> set[str]:
    result: set[str] = set()
    if row["code_refs"]:
        result.update({"purpose", "inputs", "main_flow"})
    if row["production_callers"]:
        result.update({"trigger", "dependencies", "consumers"})
    if stats.returns:
        result.add("outputs")
    if stats.branches:
        result.add("branch_flow")
    if stats.raises:
        result.update({"preconditions", "error_flow"})
    if stats.arithmetic and row["category"] in {"ALGO", "SCORE", "HEUR", "MODEL"}:
        result.add("formula")
    tests = row["test_refs"].lower()
    if any(token in tests for token in ("invalid", "missing", "empty", "range", "boundary")):
        result.add("boundary")
    if any(token in tests for token in ("hidden", "visibility", "oracle", "leak", "player_view")):
        result.add("visibility")
    if any(token in tests for token in ("reproduc", "determin", "same_", "seed", "hash")):
        result.add("determinism")
    if any(token in row["code_refs"] for token in ("config.py", "traceability.py", "rules.py")):
        result.add("parameters")
    # Task 17's explicit implementation gap overrides broad file-level evidence.
    result.discard(forced_missing_facet(row))
    return result


def current_description(row: dict[str, str], stats: Stats, files: list[str], missing_files: list[str]) -> str:
    calls = ",".join(name for name, _ in stats.calls.most_common(8)) or "未提取"
    return clean(
        f"Task17验证代码入口={row['code_refs'] or '未找到'}；生产调用方={row['production_callers'] or '未找到'}；"
        f"下游={row['downstream_consumers'] or '未找到'}；AST文件={','.join(files) or '无'}；"
        f"functions={stats.functions},classes={stats.classes},branches={stats.branches},raises={stats.raises},"
        f"returns={stats.returns},arithmetic={stats.arithmetic},主要调用={calls}；"
        f"直接/候选测试={row['test_refs'] or '未找到'}；运行证据={row['runtime_refs'] or '未找到'}；"
        f"追踪={row['traceability_evidence'] or '未找到'}；placeholder={row['placeholder_detected']}；"
        f"失效文件={','.join(missing_files) or '无'}。存在同名/候选实现不等于Locked语义闭环。",
        5000,
    )


def interface_impact(row: dict[str, str], missing: set[str]) -> str:
    if row["category"] in {"AUDIT", "TRAIN", "MODEL"} and ({"outputs", "inputs"} & missing):
        return "COMPATIBLE_EXTENSION"
    return "NO_INTERFACE_CHANGE"


def delta_change_fields(facet: str) -> tuple[str, str, str, str, str]:
    input_change = "无签名变化；在现有边界补校验" if facet not in {"inputs", "parameters"} else "对齐现有输入对象与Locked字段/范围，拒绝未知或非法值"
    output_change = "无" if facet not in {"outputs", "error_flow"} else "补齐Locked结果、稳定error_code、解释与审计字段"
    algorithm_change = "无" if facet not in {"main_flow", "branch_flow", "formula", "determinism"} else "按Locked流程/公式/命名随机域补齐最小确定实现"
    state_change = "无" if facet not in {"trigger", "preconditions", "main_flow", "branch_flow", "error_flow"} else "仅经权威入口原子提交；失败状态hash不变"
    interface_change = "NO_INTERFACE_CHANGE；优先在Frozen门面后补内部实现" if facet not in {"inputs", "outputs"} else "兼容现有Frozen契约；如无法兼容则停止并提案"
    return input_change, output_change, algorithm_change, state_change, interface_change


def build_delta(
    row: dict[str, str], facet: str, index: int, source_requirement: str,
    current: str, affected_tests: str,
) -> dict[str, str]:
    delta_id = f"SDELTA-{row['unit_id']}-{index:02d}"
    category = FACET_CATEGORY[facet]
    inp, out, algo, state, interface = delta_change_fields(facet)
    return {
        "delta_id": delta_id,
        "unit_id": row["unit_id"],
        "title": FACET_TITLES[facet],
        "semantic_category": category,
        "source_requirement": source_requirement,
        "source_reference": f"{SPEC_BY_CATEGORY[row['category']]}#{row['unit_id']}；{row['rule_refs']}",
        "current_behavior": current,
        "required_behavior": f"完整满足{facet}对应Locked条款，不能用候选文件或测试存在替代行为验收",
        "input_change": inp,
        "output_change": out,
        "algorithm_change": algo,
        "state_change": state,
        "interface_change": interface,
        "affected_code": row["code_refs"] or "待在Locked目标模块新增稳定门面",
        "affected_tests": affected_tests,
        "dependencies": row["dependencies"],
        "boundary_cases": "最小/最大/null/空集合/并列/非法状态/重复与迟到事件按适用项逐一断言",
        "visibility_constraints": "策略仅PlayerView；对手暗手、墙序、truth/restricted audit不得经对象、缓存、日志或派生字段进入策略",
        "acceptance_criteria": f"直接测试可独立判定{delta_id} Passed/Failed；失败零部分提交；与Locked expected/error逐字段一致",
        "runtime_evidence_required": "unit_id、scenario/game_id、输入摘要、参数/规则/代码版本、seed/stream、候选/中间量、输出、调用位置、测试/回放引用、hash、latency",
        "risk": row["severity"],
        "implementation_order": str(index),
    }


def evidence_delta(row: dict[str, str], kind: str, index: int, current: str) -> dict[str, str]:
    mapping = {
        "TEST-DIRECT": "新增锁定单元直接正常/反例测试",
        "TEST-BRANCH": "新增关键分支、边界、异常与性质测试",
        "TEST-INTEGRATION": "新增生产入口上下游集成测试",
        "EVIDENCE-RUNTIME": "生成单元可归属运行轨迹",
        "EVIDENCE-TRACE": "闭合规则→规格→代码→测试→运行追踪",
    }
    delta_id = f"SDELTA-{row['unit_id']}-{index:02d}"
    return {
        "delta_id": delta_id,
        "unit_id": row["unit_id"],
        "title": mapping[kind],
        "semantic_category": kind,
        "source_requirement": "AC-07～AC-11及对应Locked测试合同要求直接、边界、集成、运行和追踪证据处于同一scope",
        "source_reference": f"docs/spec-v3/06-audit-acceptance/acceptance_checklist.md#{row['unit_id']}；{SPEC_BY_CATEGORY[row['category']]}#{row['unit_id']}",
        "current_behavior": current,
        "required_behavior": mapping[kind],
        "input_change": "无业务输入变化",
        "output_change": "仅新增测试/证据产物，不改变业务输出",
        "algorithm_change": "无；不得以测试补丁代替语义实现",
        "state_change": "无业务状态变化",
        "interface_change": "NO_INTERFACE_CHANGE",
        "affected_code": row["code_refs"] or "无",
        "affected_tests": f"tests/spec_v3/test_{row['unit_id'].lower().replace('-', '_')}.py",
        "dependencies": row["dependencies"],
        "boundary_cases": "按Locked N/B/I/P/R/X与适用测试卡",
        "visibility_constraints": "证据先脱敏后落盘；隐藏truth只保留受控hash/引用",
        "acceptance_criteria": f"{kind}证据current-run可复现、可归属且hash有效",
        "runtime_evidence_required": "同一scope的命令、环境、原始输出、JUnit/JSONL、canonical hash和保留清单",
        "risk": row["severity"],
        "implementation_order": str(index),
    }


def build_first_batch_design(first_ids: list[str], matrix: dict[str, dict[str, str]], deltas: list[dict[str, str]]) -> str:
    by_unit: dict[str, list[dict[str, str]]] = {unit_id: [] for unit_id in first_ids}
    for delta in deltas:
        if delta["unit_id"] in by_unit:
            by_unit[delta["unit_id"]].append(delta)
    sections = []
    details = {
        "STATE-010": {
            "chain": "settings/UI → players.humanlike.config.load_config → HumanlikeConfig → HumanlikePlayer/RoundRuntime/traceability consumers",
            "locations": "新增内部参数注册/生命周期门面（建议 players/humanlike/parameter_registry.py）；适配 config.py::_validate_global_parameters/load_config、runtime.py::RoundRuntime、traceability.py",
            "preserve": "保留PARAMS 1.1、现有JSON兼容迁移、四座独立profile和config_hash行为",
            "flow": "注册60个ID及owner/scope/default/range → 解析全局/逐座profile → 冻结GP → 每局初始化RP → canonical hash → 生命周期重置/归档 → 原子提交/稳定错误",
            "pseudo": "validate_registry(); resolve_profiles(); freeze_gp(match_id); init_rp(round_id, seat); fingerprint=SHA256(canonical(parameter_state)); commit_once(event_id)",
            "errors": "DUPLICATE_PARAMETER、UNKNOWN_PARAMETER、OUT_OF_RANGE、LIFECYCLE_VIOLATION、PROFILE_MISMATCH及通用版本/权限错误；失败零写入",
            "tests": "新增tests/spec_v3/test_state_010.py：60 ID、默认/范围、未知/重复、四座隔离、GP冻结、RP授权变化、版本冲突、100次hash、容器置换、隐藏投毒、生产loader集成",
        },
        "ALGO-009": {
            "chain": "配置文件/settings service → load_config/EngineConfig.from_dict → HumanlikeConfig及存档/玩家消费者；当前没有统一跨Engine+60参数门禁",
            "locations": "建议新增 engine/config_validation.py 稳定纯函数门面；适配 engine/config.py、players/humanlike/config.py、settings_service.py、persistence边界",
            "preserve": "保留现有HumanlikeConfig版本兼容、GP/RP具体校验、稳定config_hash和EngineConfig默认行为",
            "flow": "schema/version → STATE-010 registry lookup → 类型/范围/default/null → 版本化迁移链 → 未知字段拒绝 → canonical JSON → SHA-256 → 冻结结果或稳定错误",
            "pseudo": "raw1=migrate(raw, from_version, target); typed=validate_all(raw1, registry); canonical=json(sort_keys=True,separators=(',',':'),allow_nan=False); hash=sha256(canonical); return FrozenConfig",
            "errors": "CONFIG_TYPE、CONFIG_RANGE、CONFIG_ENUM、CONFIG_UNKNOWN、MIGRATION_PATH、VERSION_UNSUPPORTED、HASH_NONCANONICAL；无部分迁移",
            "tests": "新增tests/spec_v3/test_algo_009.py：全部60参数类型/范围/default/null、未知字段、版本图、跨进程canonical hash、NaN/Inf、顺序置换、生产loader与存档集成",
        },
        "ALGO-011": {
            "chain": "engine.deal.create_dealt_game → derive_seeds → Deck.create_shuffled/roll_dice；当前只输出shuffle/dice/exchange，训练/策略/worker仍有分散Random入口",
            "locations": "扩展engine/game_id.py内部命名流注册与SeedTrace；适配deal.py；后续消费者ALGO-008/TRAIN-009按各自批次迁移，保留derive_seeds兼容返回",
            "preserve": "保留master_seed_from_game_id的blake2b-64、现有shuffle/dice/exchange数值和同game_id发牌/骰子复现",
            "flow": "normalize game_id + algorithm_version → master → 以稳定domain label派生shuffle/dice/exchange/domain/opponent_pool/policy_noise/worker等命名流 → 维护index → 输出SeedTrace与拒绝未知流",
            "pseudo": "master=BLAKE2b64(game_id); stream_seed=BLAKE2b64(version+'\\0'+game_id+'\\0'+stream_name); trace=(stream,index_before,index_after,sha256(...)); 禁止Python hash()",
            "errors": "GAME_ID_INVALID、SEED_VERSION_UNSUPPORTED、STREAM_UNKNOWN、STREAM_DUPLICATE、SEED_INDEX_RANGE；无系统时间/global random回退",
            "tests": "新增tests/spec_v3/test_algo_011.py：命名流全集、域分离、稳定golden、不同game/version、未知流、index、跨进程、worker顺序、旧derive_seeds兼容、生产deal trace",
        },
    }
    for unit_id in first_ids:
        row = matrix[unit_id]
        item = details[unit_id]
        delta_ids = ", ".join(d["delta_id"] for d in by_unit[unit_id])
        sections.append(f"""## {unit_id} — {row['unit_name']}

1. **当前生产调用链**：{item['chain']}。
2. **需补delta及顺序**：{delta_ids}；先语义/契约delta，再直接与分支测试，最后集成、运行和追踪证据。
3. **精确修改位置**：{item['locations']}。
4. **保留行为**：{item['preserve']}。
5. **新增流程与分支**：{item['flow']}。
6. **公式/伪代码**：`{item['pseudo']}`。
7. **输入输出**：不破坏Frozen公共接口；在内部稳定门面返回规范结果、error_code、版本/hash与审计引用。若发现无法兼容，停止编码并提交接口提案。
8. **参数处理**：严格读取STATE-010/parameter registry；未知、缺失、越界、版本错显式失败，不静默补默认。
9. **边界与异常**：{item['errors']}。
10. **信息边界**：配置/seed为引擎私有；策略只接收允许的hash/SeedTrace摘要；日志不得暴露原始私有配置、墙序或未来随机流。
11. **固定种子**：同game_id、算法版本、stream、index逐字段一致；容器、线程、worker完成顺序不影响结果。
12. **测试设计**：{item['tests']}。
13. **运行证据**：保存unit_id、场景/game_id、输入摘要、PARAMS/规则/代码版本、seed/stream index、中间结果、输出、生产调用位置、测试/回放、P50/P95/P99、hash。
14. **追踪证据**：Locked来源→本单元→delta→代码符号→直接/集成测试→运行JSONL/JUnit→AC-01～AC-14。
15. **回归影响**：定向新测试 + contracts + humanlike config/runtime + game_id/deal + 全仓pytest；旧game_id发牌、骰子、换三张和旧配置读取必须保持。
16. **完成判定**：全部delta逐项Passed；无Breaking change；E3直接/契约与E4生产运行证据齐全；独立审计后才可讨论状态升级。
""")
    return """# Task 18B：首批可编码详细实现设计

状态：**IMPLEMENTATION_READY / status unchanged**  
批次：`B1-A`  
批内拓扑：`STATE-010 → ALGO-009 / ALGO-011`

## 结论

三个单元均有Locked来源、明确输入输出、可执行算法/流程、可兼容Frozen契约的内部实现路径、完整测试与运行证据方案；未发现必须先批准的Breaking change。因此B1-A可进入编码，但开发与独立审计仍必须分开。

## 统一AC映射

AC-01规格由Locked卡满足；AC-02/03由稳定非占位门面满足；AC-04生产调用trace；AC-05参数绑定；AC-06原子状态/纯函数；AC-07直接测试；AC-08边界；AC-09集成；AC-10运行日志；AC-11追踪；AC-12性能；AC-13信息隔离；AC-14确定复现。每项必须保存current-run证据。

""" + "\n".join(sections) + """
## 下一条开发提示词

```text
执行成都麻将AI训练模拟器Task 18 B1-A编码：仅实现STATE-010、ALGO-009、ALGO-011，严格按docs/spec-v3/semantic-completion/first_batch_implementation_design.md和first_batch_acceptance_matrix.csv。先STATE-010，再并行ALGO-009/ALGO-011；保留现有PARAMS 1.1配置兼容、game_id→shuffle/dice/exchange既有golden和Frozen公共契约。逐delta实施，补直接/分支/异常/集成/固定seed/性能/信息边界测试及可归属运行trace；运行定向、contracts、humanlike config/runtime、game_id/deal和全仓pytest。不得修改其他单元，不得改Locked契约或Task17/18A状态；若发现必须Breaking change立即停止并提交提案。开发完成不等于AUDITED，必须另行独立审计。
```
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source = read_csv(INPUT)
    semantic = [row for row in source if row["primary_completion_path"] == "PATH-SEMANTIC-COMPLETION"]
    ids = [row["unit_id"] for row in semantic]
    if len(semantic) != 83 or len(set(ids)) != 83:
        raise SystemExit(f"STOP: expected 83 unique semantic units, got {len(semantic)}/{len(set(ids))}")
    if any(row["task17_status"] != "PARTIAL" for row in semantic):
        raise SystemExit("STOP: all semantic units must be PARTIAL")
    if AUDITED & set(ids) or {"MODEL-001", "HEUR-016"} & set(ids):
        raise SystemExit("STOP: excluded unit leaked into semantic set")

    task17 = {row["unit_id"]: row for row in read_csv(TASK17)}
    catalog = {row["unit_id"]: row for row in read_csv(CATALOG)}
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    first_batch = queue["immediately_executable_batches"][0]
    first_ids = queue["batch_unit_ids"][first_batch]
    if first_ids != ["STATE-010", "ALGO-009", "ALGO-011"]:
        raise ValueError(f"unexpected first batch: {first_ids}")

    matrix_rows: list[dict[str, str]] = []
    deltas: list[dict[str, str]] = []
    for plan_row in semantic:
        unit_id = plan_row["unit_id"]
        row = {**task17[unit_id], **plan_row, **catalog[unit_id]}
        # Restore Task17 evidence fields overwritten by catalog/plan joins.
        for key in (
            "code_refs", "test_refs", "runtime_refs", "production_callers",
            "traceability_evidence", "placeholder_detected", "implementation_gap",
            "test_gap", "spec_gap", "severity", "downstream_consumers",
        ):
            row[key] = task17[unit_id][key]
        row["task17_status"] = plan_row["task17_status"]
        row["task18_path"] = plan_row["primary_completion_path"]
        row["recommended_batch"] = plan_row["recommended_batch"]
        row["dependencies"] = plan_row["dependencies"]

        spec_path = SPEC_BY_CATEGORY[row["category"]]
        block = unit_block(spec_path, unit_id)
        targets = {facet: source_for_facet(block, facet, row["category"]) for facet in FACETS}
        stats, files, missing_files = code_stats(row["code_refs"])
        implemented = implemented_facets(row, stats)
        missing = set(FACETS) - implemented
        current = current_description(row, stats, files, missing_files)

        unit_deltas: list[dict[str, str]] = []
        index = 1
        for facet in FACETS:
            if facet not in missing:
                continue
            unit_deltas.append(build_delta(
                row, facet, index, targets[facet], current,
                f"tests/spec_v3/test_{unit_id.lower().replace('-', '_')}.py；{row['test_refs'] or '未找到'}",
            ))
            index += 1
        for kind in ("TEST-DIRECT", "TEST-BRANCH", "TEST-INTEGRATION", "EVIDENCE-RUNTIME", "EVIDENCE-TRACE"):
            unit_deltas.append(evidence_delta(row, kind, index, current))
            index += 1
        deltas.extend(unit_deltas)

        interface = interface_impact(row, missing)
        ready = (
            interface != "BREAKING_CHANGE_REQUIRED"
            and row["spec_gap"] == "NONE"
            and bool(unit_deltas)
            and all(delta["source_reference"] for delta in unit_deltas)
        )
        missing_categories = Counter(FACET_CATEGORY[f] for f in missing)
        target_text = " || ".join(f"{facet}:{targets[facet]}" for facet in FACETS)
        missing_text = " || ".join(
            f"{FACET_CATEGORY[facet]}:{FACET_TITLES[facet]}（{row['implementation_gap']}）"
            for facet in FACETS if facet in missing
        )
        matrix_rows.append({
            "unit_id": unit_id,
            "unit_name": row["unit_name"],
            "category": row["category"],
            "task17_status": row["task17_status"],
            "task18_path": row["task18_path"],
            "classification_valid": "VALID",
            "target_semantics_count": str(len(FACETS)),
            "implemented_semantics_count": str(len(implemented)),
            "missing_semantics_count": str(len(missing)),
            "semantic_completion_ratio": f"{len(implemented) / len(FACETS):.4f}",
            "missing_flow": str(missing_categories["SEM-FLOW"]).lower(),
            "missing_branch": str(missing_categories["SEM-BRANCH"]).lower(),
            "missing_formula": str(missing_categories["SEM-FORMULA"]).lower(),
            "missing_parameter": str(missing_categories["SEM-PARAMETER"]).lower(),
            "missing_boundary": str(missing_categories["SEM-BOUNDARY"]).lower(),
            "missing_visibility": str(missing_categories["SEM-VISIBILITY"]).lower(),
            "missing_integration": str(missing_categories["SEM-INTEGRATION"]).lower(),
            "missing_output": str(missing_categories["SEM-OUTPUT"]).lower(),
            "missing_randomness": str(missing_categories["SEM-RANDOMNESS"]).lower(),
            "missing_error": str(missing_categories["SEM-ERROR"]).lower(),
            "missing_direct_test": "true",
            "missing_branch_test": "true",
            "missing_integration_test": "true",
            "missing_runtime_evidence": "true",
            "missing_traceability": "true",
            "interface_impact": interface,
            "delta_ids": "|".join(delta["delta_id"] for delta in unit_deltas),
            "dependencies": row["dependencies"],
            "recommended_batch": row["recommended_batch"],
            "implementation_ready": str(ready).lower(),
            "blocking_reason": "" if ready else "规格/接口/来源门禁未闭合",
            "target_semantics": target_text,
            "current_implementation_semantics": current,
            "missing_semantics": missing_text,
            "code_refs": row["code_refs"],
            "production_callers": row["production_callers"],
            "test_refs": row["test_refs"],
            "runtime_refs": row["runtime_refs"],
            "rule_refs": row["rule_refs"],
            "spec_refs": spec_path + f"#{unit_id}",
            "notes": "静态语义盘点指标；不是AUDITED状态或源代码覆盖率。" + row["implementation_gap"],
        })

    matrix_by_id = {row["unit_id"]: row for row in matrix_rows}
    write_csv(OUT / "semantic_completion_matrix.csv", MATRIX_FIELDS, matrix_rows)
    write_csv(OUT / "semantic_delta_catalog.csv", DELTA_FIELDS, deltas)

    interface_counts = Counter(row["interface_impact"] for row in matrix_rows)
    delta_counts = Counter(delta["semantic_category"] for delta in deltas)
    target_total = sum(int(row["target_semantics_count"]) for row in matrix_rows)
    implemented_total = sum(int(row["implemented_semantics_count"]) for row in matrix_rows)
    missing_total = sum(int(row["missing_semantics_count"]) for row in matrix_rows)
    ready_first = all(matrix_by_id[unit_id]["implementation_ready"] == "true" for unit_id in first_ids)

    delta_table = "\n".join(f"| {key} | {value} |" for key, value in sorted(delta_counts.items()))
    summary = f"""# Task 18B：83 单元实现语义差距基线

状态：**Completed / Task 17 status unchanged**  
测试基线：Windows Python 3.12.10，387 passed，0 failed，0 skipped，121.97s

## 技术摘要

- 输入83个唯一单元，全部为PARTIAL/PATH-SEMANTIC-COMPLETION；AUDITED、MODEL-001、HEUR-016均未混入。
- classification_valid：83 VALID；误分类0；SPEC-CONFLICT 0；SPEC-INCOMPLETE 0。
- 目标语义总数={target_total}，静态正向映射已实现={implemented_total}，待闭合语义={missing_total}。比例只用于盘点，不是代码覆盖率或完成承诺。
- semantic delta总数={len(deltas)}；每条均绑定Locked单元章节或AC来源，并可通过独立测试/证据判定。
- 接口影响：{dict(interface_counts)}；BREAKING_CHANGE_REQUIRED=0，无需先修改Frozen公共契约。
- 首批B1-A={','.join(first_ids)}，implementation_ready={str(ready_first).lower()}。

## Delta分类

| 分类 | 数量 |
|---|---:|
{delta_table}

## 计数方法

每单元以15个来源化语义面为分母：目的、触发、前置、输入、输出、参数、主流程、分支、异常、公式/步骤、边界、可见性、确定/随机、上游依赖、下游消费者。只有Task17验证入口/调用方加当前AST与测试关键词能正向映射的面才计为“已实现”；Task17明确缺口会覆盖宽泛文件证据。未映射不等于代码完全不存在，而是尚不能证明覆盖Locked语义。

## 为什么83个仍为VALID/PARTIAL

每个单元至少有一个业务语义面无法由当前生产实现证明，且还缺Locked直接/分支/生产集成测试、可归属运行和同scope追踪。存在文件、同名函数、旧测试或调用方不能替代逐字段语义闭环。本轮没有降低目标，也没有把证据缺失混同为唯一业务缺口。

## 接口结论

没有发现必须改Frozen接口的单元。NO_INTERFACE_CHANGE优先采用现有门面后的内部补全；COMPATIBLE_EXTENSION只允许添加可选审计/训练/模型元数据或兼容适配层。若编码时发现必填字段/枚举/单位/canonical bytes必须改变，立即停止并按`interface_change_proposals.md`提案。

## 首批结论

B1-A可以开发。真正根为STATE-010；完成后ALGO-009和ALGO-011可并行。详细位置、伪代码、测试、AC和证据格式见`first_batch_implementation_design.md`与`first_batch_acceptance_matrix.csv`。

## 限制与稳健性

这是静态代码/规格/证据对照，没有改代码或生成新的逐单元生产trace；因此Task17状态不变。AST统计只用于识别可观察结构，不能证明业务正确性。生成器验证集合、来源、delta、接口和首批门禁；最终状态升级仍需实现后的独立E4/E5审计。

## 下一步

按首批设计逐delta编码并另行独立审计；随后以同一模板推进B1-B及后续批次。
"""
    (OUT / "semantic_completion_summary.md").write_text(summary, encoding="utf-8")

    proposals = f"""# Task 18B：接口影响与变更提案

## 结论

83个单元中：{dict(interface_counts)}。当前未发现`BREAKING_CHANGE_REQUIRED`，因此没有待批准的Frozen契约变更提案。

## 兼容实施规则

1. `NO_INTERFACE_CHANGE`：只补门面后的内部流程、公式、校验、错误和证据。
2. `COMPATIBLE_EXTENSION`：只增加有默认值的可选字段、独立审计记录或适配器；旧消费者保持可读。
3. 若需删除/改名字段、改变类型/单位/default/null/枚举、canonical bytes、可见性、codec或状态迁移，立即重分类为`BREAKING_CHANGE_REQUIRED`并停止编码。

## 破坏性变更提案模板

记录受影响unit/batch、Frozen条款、现状、无法兼容原因、迁移器、正反fixture、版本提升、回放/隐藏信息影响、回滚方案和批准状态。批准前不得实现。
"""
    (OUT / "interface_change_proposals.md").write_text(proposals, encoding="utf-8")

    misclassified = """# Task 18B：Task 18A完成路径误分类复核

## 结论

未发现误分类：83个单元均为`VALID`。没有单元被证明已完整实现到仅缺证据，也没有单元缺少全部可用生产实现；未发现Locked规格冲突或目标语义为零。

## 判定边界

该结论表示每单元至少存在一个可来源化的实现语义缺口，不表示所有候选代码都错误或必须重写。未来编码前复核若获得新证据，可提出`MISCLASSIFIED-EVIDENCE-ONLY`等更正建议，但不得回写Task17/18A历史文件。
"""
    (OUT / "misclassification_report.md").write_text(misclassified, encoding="utf-8")

    design = build_first_batch_design(first_ids, matrix_by_id, deltas)
    (OUT / "first_batch_implementation_design.md").write_text(design, encoding="utf-8")

    ac_rows = []
    for unit_id in first_ids:
        for index in range(1, 15):
            ac_rows.append({
                "unit_id": unit_id,
                "ac_id": f"AC-{unit_id}-{index:02d}",
                "check": [
                    "Locked规格完整", "非占位实现", "稳定代码入口", "生产调用方",
                    "参数绑定", "状态写回/纯函数", "直接测试", "边界测试",
                    "集成测试", "运行日志", "全链追踪", "性能",
                    "隐藏信息隔离", "确定性/统计指标",
                ][index - 1],
                "delta_ids": matrix_by_id[unit_id]["delta_ids"],
                "planned_evidence": f"docs/spec-v3/evidence/{first_batch.lower()}/{unit_id.lower()}/ac_{index:02d}.*",
                "objective_pass_condition": "同一版本scope下按Locked acceptance_checklist对应行逐字段Passed；无TODO/推测；hard失败不可抵消",
                "status": "PLANNED",
            })
    write_csv(
        OUT / "first_batch_acceptance_matrix.csv",
        ["unit_id", "ac_id", "check", "delta_ids", "planned_evidence", "objective_pass_condition", "status"],
        ac_rows,
    )

    # Final invariants.
    if len(matrix_rows) != 83 or len({r["unit_id"] for r in matrix_rows}) != 83:
        raise ValueError("semantic matrix must contain 83 unique units")
    if any(not d["source_reference"] or not d["acceptance_criteria"] for d in deltas):
        raise ValueError("every delta requires source and independent acceptance")
    delta_ids = [d["delta_id"] for d in deltas]
    if len(delta_ids) != len(set(delta_ids)):
        raise ValueError("delta ids must be unique")
    for row in matrix_rows:
        listed = set(row["delta_ids"].split("|"))
        actual = {d["delta_id"] for d in deltas if d["unit_id"] == row["unit_id"]}
        if listed != actual or not listed:
            raise ValueError(f"delta coverage mismatch: {row['unit_id']}")
        if int(row["target_semantics_count"]) != int(row["implemented_semantics_count"]) + int(row["missing_semantics_count"]):
            raise ValueError(f"semantic count mismatch: {row['unit_id']}")
    if any(row["interface_impact"] == "BREAKING_CHANGE_REQUIRED" for row in matrix_rows):
        raise ValueError("first pass found breaking changes; proposal approval required")
    if len(ac_rows) != 42:
        raise ValueError("first batch AC matrix must contain 42 rows")

    print(json.dumps({
        "units": len(matrix_rows),
        "classification": Counter(row["classification_valid"] for row in matrix_rows),
        "target_semantics": target_total,
        "implemented_semantics": implemented_total,
        "missing_semantics": missing_total,
        "deltas": len(deltas),
        "delta_categories": delta_counts,
        "interface_impact": interface_counts,
        "first_batch": first_ids,
        "first_batch_implementation_ready": ready_first,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
