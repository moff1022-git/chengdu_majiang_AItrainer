#!/usr/bin/env python3
"""Generate spec-v3 detailed test catalog, golden registry and coverage matrix."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/spec-v3"
OUT = SPEC / "05-test-spec"
CATALOG = SPEC / "02-unit-catalog/locked_unit_catalog.csv"

KINDS = [
    ("unit", "UT", "单元测试"),
    ("boundary", "BD", "边界测试"),
    ("parameterized", "PT", "参数化测试"),
    ("property", "PB", "属性测试"),
    ("state_machine", "SM", "状态机测试"),
    ("integration", "IT", "集成测试"),
    ("random_replay", "RR", "随机回放测试"),
    ("statistical", "SD", "统计分布测试"),
    ("calibration", "MC", "模型校准测试"),
    ("performance", "PF", "性能测试"),
    ("hidden_leakage", "HL", "隐藏信息泄漏测试"),
]

PARENT = {
    "unit": "N01", "boundary": "B01", "parameterized": "N01/B01/I01",
    "property": "P01", "state_machine": "X01", "integration": "X01",
    "random_replay": "R01", "statistical": "P01", "calibration": "P01",
    "performance": "X01", "hidden_leakage": "X01",
}

STATEFUL = {"RULE", "STATE", "SCORE", "HEUR", "TRAIN", "AUDIT"}
STAT_UNITS = {
    "ALGO-008", "ALGO-011", "TRAIN-005", "TRAIN-007", "TRAIN-009",
    "AUDIT-007", "AUDIT-009", "AUDIT-012",
}


def applicable(uid: str, kind: str) -> tuple[bool, str]:
    prefix = uid.split("-")[0]
    if kind == "state_machine":
        ok = prefix in STATEFUL or uid == "MODEL-005"
        return ok, "拥有权威/认知/生命周期状态" if ok else "纯函数/无生命周期状态"
    if kind == "statistical":
        ok = prefix in {"HEUR", "MODEL"} or uid in STAT_UNITS
        return ok, "输出分布、随机过程或统计指标" if ok else "规范输出为精确值，不以分布验收"
    if kind == "calibration":
        ok = prefix == "MODEL"
        return ok, "概率模型或模型生命周期必须验证校准证据" if ok else "非概率模型"
    return True, "所有单元强制检查"


def seed(uid: str, code: str) -> str:
    return "0x" + hashlib.sha256(f"spec-v3/{uid}/{code}/001".encode()).hexdigest()[:16]


def tolerance(prefix: str, kind: str) -> str:
    if kind in {"statistical", "calibration"}:
        return "采用Approved单元规格的样本量、95% CI、ECE/Brier/log-loss或分布阈值；无阈值不得通过"
    if prefix in {"HEUR", "MODEL"}:
        return "schema/合法性/泄漏误差0；软评分或概率采用Approved卡明示误差"
    return "整数、枚举、集合、状态/hash为0误差；浮点仅采用Approved卡明示误差"


def expected(prefix: str, kind: str, output: str, uid: str) -> str:
    common = {
        "unit": f"返回批准schema的`{output}`；正常向量与Approved oracle一致",
        "boundary": f"边界仍返回范围内`{output}`或稳定错误码，不截断、不猜默认值",
        "parameterized": "所有参数行分别得到登记expected/error；case_id不得串扰",
        "property": "批准不变量在全部生成样本成立；失败输出固定seed与最小反例",
        "state_machine": "仅允许批准迁移；非法迁移提交前失败；版本单调且actor/phase正确",
        "integration": f"通过生产入口得到`{output}`，上下游schema/version/hash一致",
        "random_replay": "同输入、配置、版本和seed的action/state/score/log逐字段相同",
        "statistical": "允许行为域100%满足；分布、方向效应、regret或CI达到Approved阈值，不要求唯一动作",
        "calibration": "冻结切分上输出Brier/log loss/ECE/可靠性；达到Approved阈值并报告不确定性",
        "performance": "结果与功能oracle相同且P50/P95/P99、吞吐、内存满足Approved预算",
        "hidden_leakage": "投毒字段被拒绝/忽略；基准与投毒运行的策略可见输出相同，公开日志无隐藏值",
    }
    if uid.startswith("ALGO-") and kind == "unit":
        return f"匹配`GV-{uid}-N01`金标准；{common[kind]}"
    return common[kind]


def operation(uid: str, kind: str) -> str:
    slug = uid.lower().replace("-", "_")
    suffix = dict((k, c.lower()) for k, c, _ in KINDS)[kind]
    special = {
        "property": "用固定命名seed生成≥100个合法样本并缩减失败例",
        "random_replay": "隔离进程执行两次完整路径并比较canonical产物",
        "statistical": "按冻结样本量执行多seed批跑，计算分布与95% CI",
        "calibration": "在冻结牌局级测试切分推理，计算Brier/log loss/ECE和可靠性桶",
        "performance": "warm-up后在冻结环境运行基准批次并同时校验功能输出",
        "hidden_leakage": "构造只改变对手隐藏牌/墙序/future truth的成对投毒输入并差分",
    }
    return special.get(kind, f"调用生产门面执行`test_{slug}_{suffix}`对应路径")


def pre_state(prefix: str, kind: str) -> str:
    if kind == "state_machine":
        return "由Approved fixture构造迁移前合法状态及相邻非法phase，冻结state_version/hash"
    if kind == "integration":
        return "生产runtime已用冻结VersionBundle/config/seed初始化，上游Approved合同通过"
    if kind == "hidden_leakage":
        return "一对公开信息完全相同、仅restricted truth不同的隔离状态"
    if prefix in {"MODEL", "HEUR"}:
        return "冻结PlayerView、legal mask、profile/模型版本；不得持有RoundState引用"
    return "按Approved单元规格构造最小合法初态，冻结版本、配置hash和输入hash"


def state_change(kind: str) -> str:
    if kind in {"state_machine", "integration"}:
        return "仅发生Approved事件对应的原子迁移；失败时before_hash==after_hash"
    if kind == "random_replay":
        return "两次运行的完整状态序列逐event_index一致"
    return "测试对象若为纯函数则无权威状态变化；有状态单元仅改变卡内声明字段"


def logs(uid: str, kind: str) -> str:
    extra = "；记录sample_size/alpha/CI/metric/threshold" if kind in {"statistical", "calibration"} else ""
    return f"至少含unit_id={uid}、test_id、case_id、seed_ref、version/config/input/output hash、accepted/error、latency、evidence freshness{extra}；私有值仅受控引用"


def case_block(row: dict[str, str], kind: str, code: str, label: str) -> str:
    uid = row["新单元ID"]
    prefix = uid.split("-")[0]
    slug = uid.lower().replace("-", "_")
    test_id = f"TC-{uid}-{code}-01"
    vector = f"tests/spec_v3/vectors/{slug}.jsonl#case={code.lower()}01"
    parents = "、".join(f"`T-{uid}-{part}`" for part in PARENT[kind].split("/"))
    failure = {
        "statistical": "样本不足、CI/阈值缺失、非法/泄漏非0、分布超出Approved允许域或同seed不复现",
        "calibration": "只报准确率、ECE/Brier/log loss缺失、切分泄漏、阈值未达或回退不可用",
        "hidden_leakage": "投毒改变策略可见输出/动作，公开日志出现隐藏值，或restricted loader可被policy调用",
        "performance": "功能结果漂移、预算超限、环境/样本未冻结或只报告最好一次",
    }.get(kind, "任一expected字段/状态/hash/错误码不符，出现未声明副作用、隐藏泄漏或不可复现")
    return f"""## {test_id} — {label}

| 字段 | 内容 |
|---|---|
| 测试ID | `{test_id}` |
| 对应单元ID | `{uid}` — {row['名称']} |
| 父测试合同 | {parents}；本卡是Approved N/B/I/P/R/X合同的细化，不另立业务要求 |
| 前置状态 | {pre_state(prefix, kind)} |
| 输入 | `{row['主要输入']}`；向量引用`{vector}`；字段/范围以Approved单元规格为准 |
| 随机种子 | `{seed(uid, code)}`；通过ALGO-011 `property_test/{uid}/{code}`命名域派生；无随机单元也记录seed_ref以证明不消费随机流 |
| 操作 | {operation(uid, kind)} |
| 预期输出 | {expected(prefix, kind, row['主要输出'], uid)} |
| 允许误差 | {tolerance(prefix, kind)} |
| 预期状态变化 | {state_change(kind)} |
| 预期日志 | {logs(uid, kind)} |
| 失败条件 | {failure} |
| 自动化位置 | `tests/spec_v3/test_{slug}.py::test_{slug}_{code.lower()}` |

"""


def extract_goldens() -> list[tuple[str, str, str]]:
    path = SPEC / "03-unit-specs/deterministic_algorithm_scoring_specs.md"
    text = path.read_text()
    heads = list(re.finditer(r'^## ((?:ALGO|SCORE)-\d{3})\b', text, re.M))
    result = []
    for i, match in enumerate(heads):
        uid = match.group(1)
        block = text[match.start():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        m = re.search(r'^### 11\. 金标准示例[^\n]*\n\n(.+?)(?=\n### 12\.)', block, re.M | re.S)
        if not m:
            raise ValueError(f"missing golden section: {uid}")
        line = " ".join(m.group(1).strip().split())
        markers = list(re.finditer(r'(?:^|；)(正常|边界|非法)[：:]?', line))
        parts: dict[str, str] = {}
        for j, marker in enumerate(markers):
            end = markers[j + 1].start() if j + 1 < len(markers) else line.find("。三类示例", marker.end())
            if end < 0:
                end = len(line)
            parts[marker.group(1)] = line[marker.end():end].strip("；。 ")
        for label, code in (("正常", "N01"), ("边界", "B01"), ("非法", "I01")):
            if not parts.get(label):
                raise ValueError(f"missing {label} golden: {uid}: {line}")
            result.append((uid, code, parts[label]))
    return result


STRATEGY = """# Spec v3 测试策略

| 字段 | 内容 |
|---|---|
| 文档状态 | Draft |
| 日期 | 2026-07-29 |
| 功能单元 | 96/96 |
| 用例状态 | Specified / Not Implemented / Not Evaluated |
| 上游 | Approved单元规格、Approved基础测试规格 |

## 1. 测试层级

每单元逐项检查单元、边界、参数化、属性、状态机、集成、随机回放、统计分布、模型校准、性能和隐藏信息泄漏11类。覆盖矩阵的`Y`必须在用例目录中有唯一测试卡；`N`必须给出方法学理由，不能因为尚未实现而标N。

单元测试隔离单一职责；集成测试只能走生产门面；系统/回放测试保存完整事件与环境。测试fixture不得复制生产规则、计分或状态机，expected来自Approved规范公式、人工冻结golden或独立不变量。

## 2. 方法边界

- RULE/STATE/ALGO/SCORE：规范字段、状态、集合、整数和hash精确比较；浮点只用规格明示误差。
- HEUR：验证合法允许域、候选上限、方向效应、regret、统计分布和95% CI，不强制每手唯一动作。
- MODEL：冻结牌局级切分，必须报告Brier、log loss、ECE、可靠性和不确定性；准确率不能单独通过。
- TRAIN：与生产Engine逐事件等价；reward追踪ScoreTransfer或显式势能差；策略观测不得读truth。
- AUDIT：证据缺失、过期、篡改、泄漏或hard失败不得输出Passed。

## 3. 确定性与随机回放

所有用例记录命名seed，即使目标不消费随机数也记录`seed_ref`。相同输入、初态、规则/config/code/model/schema版本和seed必须完整复现action、状态序列、分数、日志与hash；跨进程至少复算两次。新增随机调用必须使用新命名子域，禁止全局RNG、系统时间、Python`hash()`或线程到达顺序。

## 4. 金标准向量

ALGO-001～011每个至少有正常、边界、非法三类冻结向量；SCORE同样登记三类。向量实现于`tests/spec_v3/vectors/<unit>.jsonl`，必须包含canonical input、expected/expected_error、中间量、公式版本、允许误差和SHA-256。基线公式输出可另存`baseline_expected`，不得替代规范expected。

## 5. 隐藏信息隔离

全部96单元均有HL用例。成对状态保持PlayerView/公开事件/合法集相同，只改变对手手牌、墙序、future truth或离线标签；策略侧输出必须不变。评估器可读取restricted truth，但模块/进程/文件权限、loader和日志通道与policy隔离。任何公开日志、异常文本或解释字段泄漏实体牌/隐藏牌即hard失败。

## 6. 统计与校准

统计用例预先冻结样本量、seed集合、指标、阈值和alpha=0.05，报告效应量及95% CI；不得观察结果后调阈值。启发式硬约束逐样本100%满足，软行为按Approved区间验收。概率模型使用牌局/玩家/时间防泄漏切分并比较规则基线；ECE分桶规则也必须冻结。

## 7. 性能

性能用例同时执行功能oracle；冻结硬件、OS、Python/依赖、数据、warm-up、并发和采样次数，报告P50/P95/P99、吞吐、峰值内存。超预算或功能漂移均失败；不得只选最好一次或用缓存结果冒充全路径。

## 8. 失败、skip和证据

hard gate不得N/A、skip或宽松xfail。其他N/A需owner和批准理由；临时skip需issue和到期日。Passed至少需要EV3直接测试证据；跨模块/回放/性能需要EV4；真人相似、强度和学习效果需要EV5。当前目录只定义用例，测试代码、向量与运行证据仍Not Implemented/Not Evaluated。

## 9. 执行批次

按锁定DAG执行：配置/RNG/状态/牌墙→RULE→ALGO/SCORE/View→HEUR/MODEL→TRAIN→AUDIT。每批先落向量和fixture，再实现用例；通过后回填JUnit、环境manifest、commit、版本、seed、输入/输出hash和证据新鲜度。
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with CATALOG.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    catalog = """# Spec v3 测试用例目录

| 字段 | 内容 |
|---|---|
| 文档状态 | Draft |
| 日期 | 2026-07-29 |
| 单元覆盖 | 96/96 |
| 用例实现/证据 | Not Implemented / Not Evaluated |

本目录只收录覆盖矩阵中适用的测试卡。业务expected以Approved单元规格为唯一来源；本目录细化前置、输入、seed、操作、输出、状态、日志、失败和自动化位置。

"""
    matrix_rows = []
    for row in rows:
        uid = row["新单元ID"]
        item = {"unit_id": uid, "unit_name": row["名称"], "unit_type": row["类型"]}
        for kind, code, label in KINDS:
            ok, reason = applicable(uid, kind)
            item[kind] = "Y" if ok else "N"
            item[kind + "_reason"] = reason
            item[kind + "_test_id"] = f"TC-{uid}-{code}-01" if ok else ""
            if ok:
                catalog += case_block(row, kind, code, label)
        matrix_rows.append(item)
    (OUT / "test_case_catalog.md").write_text(catalog, encoding="utf-8")

    fields = ["unit_id", "unit_name", "unit_type"]
    for kind, _, _ in KINDS:
        fields += [kind, kind + "_test_id", kind + "_reason"]
    with (OUT / "coverage_matrix.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader(); writer.writerows(matrix_rows)

    goldens = extract_goldens()
    golden_doc = """# Spec v3 金标准向量目录

| 字段 | 内容 |
|---|---|
| 文档状态 | Draft |
| 日期 | 2026-07-29 |
| 覆盖 | ALGO-001～011与SCORE-001～006；每单元正常/边界/非法 |
| 向量实现/证据 | Not Implemented / Not Evaluated |

以下描述逐字义来源于Approved ALGO/SCORE规格的“金标准示例”。实现时必须将描述展开为canonical JSONL的完整字段和中间量，计算并冻结SHA-256；没有实际JSONL和hash前不得标Passed。规范expected与baseline_expected必须分栏。

| 向量ID | 单元 | 类别 | Approved示例 | 计划JSONL定位 | 误差/判定 |
|---|---|---|---|---|---|
"""
    for uid, code, desc in goldens:
        slug = uid.lower().replace("-", "_")
        category = {"N01": "正常", "B01": "边界", "I01": "非法"}[code]
        err = "稳定错误码精确匹配" if code == "I01" else "采用Approved卡允许误差；整数/集合默认0"
        golden_doc += f"| `GV-{uid}-{code}` | `{uid}` | {category} | {desc.replace('|', '&#124;')} | `tests/spec_v3/vectors/{slug}.jsonl#golden={code}` | {err} |\n"
    golden_doc += """

## 向量必填字段

`vector_id,unit_id,case_kind,ruleset_version,formula_version,baseline_version,config_hash,seed_ref,input,normalized_input,intermediates,expected,baseline_expected,expected_error,tolerance,source_clause_refs,canonical_sha256`。非法向量的`expected=null`；正常/边界向量不得用当前实现输出来自动冻结expected，必须经规范复算和独立复核。

## 复现门禁

同一向量在同进程重复100次、隔离进程至少2次，并在支持平台上比较canonical输出；规范字段、状态、集合、错误码和hash逐字段一致。任何seed、版本、输入或expected变化必须产生新向量版本和hash，不得覆盖已引用向量。
"""
    (OUT / "golden_vectors.md").write_text(golden_doc, encoding="utf-8")
    (OUT / "test_strategy.md").write_text(STRATEGY, encoding="utf-8")


if __name__ == "__main__":
    main()
