#!/usr/bin/env python3
"""Generate AC-01..AC-14 checklists for all 96 locked spec-v3 units."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/spec-v3"
CATALOG = SPEC / "02-unit-catalog/locked_unit_catalog.csv"
OUT = SPEC / "06-audit-acceptance/acceptance_checklist.md"

ROOTS = {
    "RULE": "engine/rules", "ALGO": "engine/analysis",
    "HEUR": "players/humanlike/heuristics", "MODEL": "players/humanlike/models",
    "STATE": "engine/state", "SCORE": "engine/scoring",
    "TRAIN": "training", "AUDIT": "engine/audit",
}

METRIC = {
    "RULE": "逐字段确定复现；合法性、阶段、守恒和稳定错误码0偏差",
    "STATE": "逐事件状态/hash确定复现；合法迁移、版本和所有权0偏差",
    "ALGO": "Approved规范golden、顺序置换、跨进程复算0偏差；浮点仅卡内误差",
    "SCORE": "逐事件/层/本局确定复现且ΣΔ=0；账本幂等",
    "HEUR": "每seed复现；允许域/方向效应/regret/分布/95% CI达标；不要求唯一动作",
    "MODEL": "冻结切分Brier/log loss/ECE/可靠性/不确定性及规则回退达标",
    "TRAIN": "生产等价、reward溯源、回放/快照/并行指标达标",
    "AUDIT": "canonical结果确定、hard失败不误报、证据完整/新鲜/脱敏；统计项含CI",
}

CHECKS = [
    ("01", "规格完整", "E1", "Locked目录+Approved单元/测试规格；规范定义无未决占位；证据占位可保留"),
    ("02", "非占位实现", "E2", "真实主要逻辑；无pass/固定成功/空返回/mock/TODO或仅schema框架"),
    ("03", "代码入口", "E2", "建议主文件存在稳定可导入门面；版本/schema/error契约一致"),
    ("04", "实际调用方", "E4", "非测试生产调用方静态边+完整运行trace均命中入口"),
    ("05", "参数绑定", "E4", "GP/RP或无直接参数声明可追；冻结loader、运行值和config hash一致"),
    ("06", "状态写回", "E4", "纯函数无副作用，或只经权威入口原子commit；失败hash不变"),
    ("07", "单元测试", "E3", "Approved N/UT及适用参数/属性测试current-run通过并直接断言行为"),
    ("08", "边界测试", "E3", "Approved B/BD、最小最大/null/非法相邻边界通过且无部分提交"),
    ("09", "集成测试", "E4", "Approved X/IT通过生产门面；上下游schema/version/hash兼容"),
    ("10", "运行日志", "E4", "实际输入输出、seed、版本、状态/错误、耗时、hash和私有引用完整"),
    ("11", "追踪关系", "E4", "来源→参数→单元→代码→测试→运行无断链"),
    ("12", "性能", "E4", "冻结环境功能oracle不漂移；P50/P95/P99/吞吐/内存达Approved预算"),
    ("13", "隐藏信息隔离", "E4", "白名单/权限/静态扫描/成对truth投毒/日志脱敏全通过，泄漏0"),
    ("14", "确定性或统计指标", "E4", "按单元方法类别执行确定、统计、校准或生产等价指标"),
]


def card(row: dict[str, str]) -> str:
    uid = row["新单元ID"]
    prefix = uid.split("-")[0]
    slug = uid.lower().replace("-", "_")
    code = f"{ROOTS[prefix]}/{slug}.py"
    test = f"tests/spec_v3/test_{slug}.py"
    parent = "、".join(f"T-{uid}-{x}01" for x in "NBIPRX")
    tc = f"TC-{uid}-UT/BD/PT/PB/SM/IT/RR/SD/MC/PF/HL-01（按覆盖矩阵Y项）"
    rows = []
    for num, label, level, condition in CHECKS:
        if num == "14":
            condition += "：" + METRIC[prefix]
        rows.append(f"| `AC-{uid}-{num}` | {label} | {level} | Not Evaluated | {condition} | TODO(evidence_id/path/hash) |")
    joined_rows = "\n".join(rows)
    return f"""## {uid} {row['名称']}

| 字段 | 内容 |
|---|---|
| 类型 | {row['类型']} |
| 代码入口候选 | `{code}`；存在不代表通过 |
| 上游依赖 | `{row['上游依赖'] or '无'}` |
| 参数绑定 | `{row['关联GP_RP'] or '无直接参数'}` |
| 来源规则 | {row['来源规则']} |
| 父测试合同 | {parent} |
| 细化测试卡 | `{tc}` |
| 自动化模块 | `{test}` |
| 最低AUDITED等级 | E4；适用外部/发布声明E5 |
| 当前状态 | NOT_EVALUATED / E0 |

| 验收ID | 检查项 | 最低E | 当前状态 | Passed条件 | 证据引用 |
|---|---|---:|---|---|---|
{joined_rows}

### 单元AUDITED判定

- [ ] `AC-{uid}-01`～`AC-{uid}-14`全部Passed。
- [ ] 八项AUDITED条件全部满足且证据处于同一scope。
- [ ] 无开放High/Critical；hash链、回放、追踪和保留检查通过。
- [ ] 最高累计证据≥E4；需要外部效果/发布声明时达到E5。

最终结论：`NOT_EVALUATED`。不得因目录状态、代码候选或测试名称存在改为AUDITED。

"""


def main() -> None:
    with CATALOG.open(encoding="utf-8", newline="") as fh:
        units = list(csv.DictReader(fh))
    header = """# Spec v3 96单元验收清单

| 字段 | 内容 |
|---|---|
| 文档状态 | Draft |
| 日期 | 2026-07-29 |
| 单元覆盖 | 96/96 |
| 验收检查 | 1344项：每单元AC-01～AC-14 |
| 当前总体状态 | NOT_EVALUATED |

本清单是[audit_standard.md](audit_standard.md)的逐单元展开。全部检查均为hard；纯函数的状态写回项必须证明无副作用，不能N/A。代码路径均为开发任务卡建议位置，需经差距审计改为实际路径后才形成E2证据。

"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(header + "".join(card(row) for row in units), encoding="utf-8")


if __name__ == "__main__":
    main()
