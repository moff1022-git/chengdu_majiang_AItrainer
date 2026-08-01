#!/usr/bin/env python3
"""Generate the approved spec-v3 test contracts from the locked unit catalog.

This generator only writes documentation and planned fixture/test paths.  It does
not create tests, fixtures, evidence, or claim that any implementation passes.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC_ROOT = ROOT / "docs/spec-v3"
CATALOG = SPEC_ROOT / "02-unit-catalog/locked_unit_catalog.csv"
OUT = SPEC_ROOT / "05-test-spec"

GROUPS = {
    "rule_state_test_specs.md": {"RULE", "STATE"},
    "algorithm_scoring_test_specs.md": {"ALGO", "SCORE"},
    "heuristic_test_specs.md": {"HEUR"},
    "model_test_specs.md": {"MODEL"},
    "training_test_specs.md": {"TRAIN"},
    "audit_test_specs.md": {"AUDIT"},
}

SPEC_LINK = {
    "RULE": "../03-unit-specs/deterministic_rule_state_specs.md",
    "STATE": "../03-unit-specs/deterministic_rule_state_specs.md",
    "ALGO": "../03-unit-specs/deterministic_algorithm_scoring_specs.md",
    "SCORE": "../03-unit-specs/deterministic_algorithm_scoring_specs.md",
    "HEUR": "../03-unit-specs/human_heuristic_specs.md",
    "MODEL": "../03-unit-specs/probabilistic_model_specs.md",
    "TRAIN": "../03-unit-specs/training_environment_specs.md",
    "AUDIT": "../03-unit-specs/audit_specs.md",
}

CLASS_RULES = {
    "RULE": {
        "oracle": "逐字段精确比较权威状态、合法集、稳定错误码及事件顺序",
        "boundary": "最小/最大合法牌数、首末座位、空响应窗、墙尾与阶段边界",
        "invalid": "非法actor、阶段、牌实体、动作或配置必须拒绝，且提交前状态hash不变",
        "property": "同输入/状态/规则/seed逐字段相同；牌张守恒、合法actor和隐藏隔离始终成立",
        "integration": "经生产Engine公开入口提交事件，不得直接伪造后置状态",
        "marker": "deterministic,rule,hard_gate",
    },
    "STATE": {
        "oracle": "逐字段精确比较状态、版本、所有权、生命周期与序列化结果",
        "boundary": "初始/终止状态、空集合、最大历史、超时临界点及迁移版本边界",
        "invalid": "非法迁移、旧版本写入、重复ID、跨座访问或损坏快照必须稳定失败",
        "property": "合法转移保持不变量；serialize→deserialize及snapshot→restore等价；同seed复现",
        "integration": "通过唯一状态所有者和生产事件入口验证，禁止测试直接绕过状态机",
        "marker": "deterministic,state,hard_gate",
    },
    "ALGO": {
        "oracle": "对批准规格的规范公式、golden与输出向量做精确比较，浮点仅用卡内允许误差",
        "boundary": "空/最小/最大向量、计数0/4、上下界、候选上限及数值溢出边界",
        "invalid": "null、越界、重复实体、非有限数、版本冲突或隐藏字段投毒必须稳定失败",
        "property": "排列不变性/单调性/守恒按卡适用；确定算法不得调用训练模型；同seed复现",
        "integration": "从白名单PlayerView或权威引擎接口取输入，验证输出可被下游消费",
        "marker": "deterministic,algorithm,formula",
    },
    "SCORE": {
        "oracle": "逐事件精确比较支付方、接收方、分项、封顶、账本及累计排名",
        "boundary": "0番/封顶、单/多接收方、最小/最大玩家数、空杠链与终局边界",
        "invalid": "未知番、非法支付方、重复转移、负溢出或来源事件缺失必须稳定失败",
        "property": "每个原子事件、结算层和本局总账均满足ΣΔ=0；重放不重复入账",
        "integration": "由生产规则事实驱动ScoreTransfer并写唯一账本，不直接改累计分",
        "marker": "deterministic,score,zero_sum,hard_gate",
    },
    "HEUR": {
        "oracle": "断言合法候选、允许行为域、排序/区间、解释字段和固定参数/seed复现，不断言唯一真人动作",
        "boundary": "单候选、候选上限、满意阈值两侧、扰动上下界及早中晚阶段",
        "invalid": "隐藏字段、非法候选、权重越界、缺mandatory或非有限评分必须拒绝/安全回退",
        "property": "非法动作、强制违例、隐藏泄漏均为0；方向效应/regret/分布指标按卡报告95% CI",
        "integration": "仅使用PlayerView+合法集，经ALGO候选后输出可执行动作和解释",
        "marker": "heuristic,statistical,visibility",
    },
    "MODEL": {
        "oracle": "断言输出schema、概率范围/归一化、校准指标、不确定性、版本和规则基线回退",
        "boundary": "无历史、最少样本、全mask、OOD、概率0/1、批大小1及在线时限边界",
        "invalid": "隐藏手牌/墙序/future truth投毒、模型hash错、NaN或非法概率必须拒绝并回退",
        "property": "Brier/log loss/ECE及卡内阈值使用冻结切分和95% CI；不能只报告准确率",
        "integration": "线上加载器只接收白名单特征；restricted label truth与policy输入物理隔离",
        "marker": "model,calibration,leakage",
    },
    "TRAIN": {
        "oracle": "逐事件比较生产Engine的状态、合法mask、真实计分、reward分解、终止与快照",
        "boundary": "单/多局、首末步、空合法集、并行1/N、截断、超时与恢复边界",
        "invalid": "非法动作、隐藏truth观测、第二规则引擎、错误版本或损坏快照必须稳定处理",
        "property": "同seed确定回放；策略观测无truth；每项reward追踪真实计分或显式势能差",
        "integration": "训练环境必须导入并调用生产Rule/State/Score实现，执行生产等价golden",
        "marker": "training,production_parity,replay",
    },
    "AUDIT": {
        "oracle": "逐字段比较canonical记录、hash、finding、状态、严重级别、证据引用与门禁结果",
        "boundary": "空批次、首末事件、乱序/重复、过期临界点、并行归并及保留期限边界",
        "invalid": "缺证据、篡改、schema/version错、权限越界或私有字段泄漏不得报告Passed",
        "property": "相同输入/version/seed逐字段一致；append-only；hard失败不被平均抵消；truth不回流",
        "integration": "消费真实运行产物并输出签名证据，失败证据也必须保留",
        "marker": "audit,evidence,hard_gate",
    },
}

FOCUS = {
    "RULE-002": "同花色三张、交换方向与实体所有权",
    "RULE-003": "定缺未清时合法弃牌全集",
    "RULE-006": "摸牌→自摸/杠→出牌的唯一阶段顺序",
    "RULE-009": "补杠暂存、抢杠胡响应窗与取消提交",
    "RULE-011": "过胡设置、持续及恢复触发点",
    "RULE-013": "多人响应优先级及座次稳定裁决",
    "RULE-014": "胡牌玩家退出、继续血战及墙空终止",
    "RULE-016": "逐座PlayerView字段白名单和隐藏信息投毒",
    "ALGO-001": "108张physical_id唯一归属及face投影计数≤4",
    "ALGO-002": "普通牌/七对向听、有效进张、死叫和等待形状golden",
    "ALGO-003": "同一事件牌去重、可见数与未见数",
    "ALGO-004": "未见牌与墙内活牌区间不得混同",
    "ALGO-005": "活动座次、墙长和胡后退出下的摸牌机会区间",
    "ALGO-011": "game_id命名随机流域隔离与调用顺序无关",
    "SCORE-001": "番型识别、互斥/叠加、封顶和确定排序",
    "SCORE-002": "自摸/点炮/抢杠胡支付方向及逐事件零和",
    "SCORE-003": "明杠/暗杠/补杠、取消与呼叫转移链接",
    "SCORE-004": "花猪、查大叫、死叫口径和退税来源链",
    "SCORE-005": "原子转移幂等、分层账本与ΣΔ=0",
    "SCORE-006": "本局累计、跨局累计、并列排名与稳定次序",
    "HEUR-001": "换三张同花色合法候选与选择分布",
    "HEUR-002": "定缺候选评分、风格/水平/阶段方向效应",
    "HEUR-010": "过胡允许域、机会成本及强制胡旁路",
    "HEUR-017": "危险牌风险排序与无oracle回退",
    "HEUR-021": "mandatory保留、有限候选上限和注意预算",
    "HEUR-023": "人类失误率、regret上界与思考时间分布",
    "MODEL-001": "清缺概率、主体花色和牌型三任务校准",
    "MODEL-002": "听牌、逐牌等待及综合点炮风险校准",
    "MODEL-003": "跨局风格更新、最少样本与跨玩家隔离",
    "MODEL-004": "legal-mask后候选动作概率分布与真人拟合",
    "MODEL-005": "模型版本、artifact hash、兼容门禁和回退",
    "TRAIN-001": "Episode单/多局边界及生产状态转换等价",
    "TRAIN-002": "Observation字段白名单和restricted truth投毒",
    "TRAIN-003": "固定动作codec、合法mask和非法动作处理",
    "TRAIN-004": "真实计分reward与γΦ(o')-Φ(o)逐项溯源",
    "TRAIN-006": "game_id/seed、确定回放、快照恢复逐字段等价",
    "AUDIT-001": "每个权威原子事件恰一条且私有牌仅受控引用",
    "AUDIT-003": "canonical序列化、genesis/prev/record hash链",
    "AUDIT-004": "同配置/seed/事件逐事件state/action/score一致",
    "AUDIT-005": "牌张、阶段、actor、视图泄漏和计分零和不变量",
    "AUDIT-007": "命名生成流、失败缩减及最小反例可复现",
    "AUDIT-010": "来源→参数→单元→实现→测试→证据无断链",
    "AUDIT-013": "禁止依赖、第二规则引擎与oracle信息流检测",
    "AUDIT-014": "脱敏、权限、保留期限、新鲜度和删除/归档manifest",
}


def slug(unit_id: str) -> str:
    return unit_id.lower().replace("-", "_")


def render_card(row: dict[str, str]) -> str:
    uid = row["新单元ID"]
    prefix = uid.split("-")[0]
    rules = CLASS_RULES[prefix]
    sid = slug(uid)
    focus = FOCUS.get(uid, f"{row['名称']}的批准输入、输出和验收边界")
    spec = SPEC_LINK[prefix]
    return f"""## {uid} {row['名称']}

### 测试契约

| 字段 | 值 |
|---|---|
| 规格来源 | [{uid}]({spec})对应二级标题；目录来源与参数以锁定目录对应行为准 |
| 测试状态 | Specified / Not Implemented / Not Evaluated |
| 测试模块 | `tests/spec_v3/test_{sid}.py` |
| 向量文件 | `tests/spec_v3/vectors/{sid}.jsonl` |
| pytest标记 | `{rules['marker']},{prefix.lower()}` |
| 主要输入 | {row['主要输入']} |
| 主要输出 | {row['主要输出']} |
| 本卡焦点 | {focus} |
| oracle | {rules['oracle']} |
| 允许误差 | 确定字段0；浮点/统计量仅采用批准单元规格明示误差，未明示则0 |
| 最低证据 | 直接断言EV3；P0/跨模块路径EV4；外部效果声明按适用项EV5 |

### 可执行用例

| 测试ID | pytest函数 | 向量/生成器 | 必须断言 |
|---|---|---|---|
| T-{uid}-N01 | `test_{sid}_normal_golden` | JSONL `case=normal` | {focus}；{rules['oracle']} |
| T-{uid}-B01 | `test_{sid}_boundary_table` | JSONL `case=boundary` 参数化 | {rules['boundary']}；不越过批准输出范围 |
| T-{uid}-I01 | `test_{sid}_invalid_rejected` | JSONL `case=invalid` 参数化 | {rules['invalid']}；断言稳定错误码和失败原子性 |
| T-{uid}-P01 | `test_{sid}_properties` | 固定seed生成器；seed写入报告 | {rules['property']} |
| T-{uid}-R01 | `test_{sid}_repeatability` | normal/boundary逐例重复2次 | 冻结输入、版本、参数和seed后规范输出逐字段相同；非确定训练过程仅比较规定可复现边界 |
| T-{uid}-X01 | `test_{sid}_integration_contract` | 生产入口fixture | {rules['integration']}；上下游schema/hash/version兼容 |

### Fixture与执行

JSONL每行必须含`case_id`、`case_kind`、`ruleset_version`、`config_hash`、`seed_ref`、`input`、`expected`、`expected_error`、`tolerance`、`source_clause_refs`。统计测试另含`sample_size`、`alpha`、`metric`、`threshold`；禁止以空阈值通过。

执行命令：`python -m pytest -q tests/spec_v3/test_{sid}.py`。实现测试文件前命令预期因文件不存在而不可执行成功；不得记录为Passed。完成后保存JUnit、环境manifest、commit、输入向量hash和输出hash，回填`{uid}-TEST/RUN`证据占位。

### 完成门禁

- 六个测试ID全部存在且直接断言正文行为，禁止只断言类/函数/文件存在。
- N/B/I/P/R/X全部Passed；不适用项必须给出批准的N/A理由，hard gate不可N/A。
- 无`xfail(strict=False)`、无无期限skip、无网络/时钟/无名随机源依赖。
- 当前结论：`Not Implemented / Not Evaluated`，本文不提供伪造运行结果。

"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with CATALOG.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    by_file: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        prefix = row["新单元ID"].split("-")[0]
        for filename, prefixes in GROUPS.items():
            if prefix in prefixes:
                by_file[filename].append(row)
                break
        else:
            raise ValueError(f"unrouted unit: {row['新单元ID']}")
    for filename, prefixes in GROUPS.items():
        selected = by_file[filename]
        title = "/".join(sorted(prefixes))
        body = f"""# {title} 单元可执行测试规格

| 字段 | 内容 |
|---|---|
| 文档状态 | Approved |
| 日期 | 2026-07-29 |
| 覆盖 | {selected[0]['新单元ID'].split('-')[0]}等，共{len(selected)}单元 |
| 单元规格 | Approved |
| 测试实现/验收 | Not Implemented / Not Evaluated |

本文件规定测试代码、向量、断言和证据合同；详细业务定义仍只来自已批准单元规格。本文件存在不表示测试文件、fixture或行为已实现。

""" + "".join(render_card(row) for row in selected)
        (OUT / filename).write_text(body, encoding="utf-8")

    manifest = OUT / "unit_test_manifest.csv"
    with manifest.open("w", encoding="utf-8", newline="") as fh:
        fields = ["unit_id", "unit_name", "unit_type", "test_spec", "test_module", "vector_file", "test_ids", "spec_status", "implementation_status", "evidence_status"]
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            uid = row["新单元ID"]
            prefix = uid.split("-")[0]
            filename = next(name for name, prefixes in GROUPS.items() if prefix in prefixes)
            sid = slug(uid)
            writer.writerow({
                "unit_id": uid,
                "unit_name": row["名称"],
                "unit_type": row["类型"],
                "test_spec": filename,
                "test_module": f"tests/spec_v3/test_{sid}.py",
                "vector_file": f"tests/spec_v3/vectors/{sid}.jsonl",
                "test_ids": "|".join(f"T-{uid}-{x}01" for x in "NBIPRX"),
                "spec_status": "Approved",
                "implementation_status": "Not Implemented",
                "evidence_status": "Not Evaluated",
            })

    readme = """# Spec v3 可执行测试规格索引

| 字段 | 内容 |
|---|---|
| 文档状态 | Approved |
| 日期 | 2026-07-29 |
| 覆盖 | 96/96锁定单元 |
| 测试契约 | 576个：每单元N/B/I/P/R/X各1个 |
| 实现状态 | Not Implemented |
| 证据状态 | Not Evaluated |

## 文件导航

- [RULE/STATE](rule_state_test_specs.md)
- [ALGO/SCORE](algorithm_scoring_test_specs.md)
- [HEUR](heuristic_test_specs.md)
- [MODEL](model_test_specs.md)
- [TRAIN](training_test_specs.md)
- [AUDIT](audit_test_specs.md)
- [96单元执行清单](unit_test_manifest.csv)
- [11类测试策略](test_strategy.md)
- [逐用例完整目录](test_case_catalog.md)
- [ALGO/SCORE金标准向量目录](golden_vectors.md)
- [96单元×11类覆盖矩阵](coverage_matrix.csv)

## 统一执行合同

每单元固定六类测试：N正常golden、B边界表、I非法与失败原子性、P性质/统计、R重复性、X生产入口集成。测试模块和JSONL向量路径均由执行清单冻结。确定性单元精确复算；HEUR验证合法允许域、方向效应、regret和统计区间；MODEL验证泄漏隔离、校准和规则回退；TRAIN验证与生产引擎同源；AUDIT验证证据链和hard门禁。

逐用例目录进一步把上述Approved合同细化为11种方法检查。覆盖矩阵登记890个适用TC测试卡；它们是576个N/B/I/P/R/X父合同的展开，不是第二套业务规范，也不能与父合同分别重复计算通过率。

## pytest与证据规则

计划统一命令为`python -m pytest -q tests/spec_v3`。在相应测试文件与向量落盘前，状态必须保持Not Implemented/Not Evaluated，禁止把本规格生成过程算作EV3。运行后每个测试ID记录JUnit nodeid、结果、耗时、环境manifest、commit、规则/config/model/schema hash、seed、向量hash及产物路径。skip/xfail必须有owner、原因和到期日；hard gate不得skip或N/A。

## 实现顺序

按锁定DAG和P0优先级：确定规则/状态/牌墙/随机流→确定算法/计分→视图/启发式/模型→训练→审计。每批先落实JSONL schema和共享fixture，再实现单元测试；不得为让测试通过而复制第二套规则oracle，golden expected必须来源于批准公式或人工冻结向量。
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
