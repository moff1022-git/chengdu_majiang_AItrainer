#!/usr/bin/env python3
"""Generate 96 spec-v3 development task cards from the locked catalog."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/spec-v3"
CATALOG = SPEC / "02-unit-catalog/locked_unit_catalog.csv"
OUT = SPEC / "04-development-guide/development_task_cards.md"

ROOTS = {
    "RULE": "engine/rules",
    "ALGO": "engine/analysis",
    "HEUR": "players/humanlike/heuristics",
    "MODEL": "players/humanlike/models",
    "STATE": "engine/state",
    "SCORE": "engine/scoring",
    "TRAIN": "training",
    "AUDIT": "engine/audit",
}

LEGACY = {
    "RULE": "engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py",
    "ALGO": "engine/physical_tile.py, engine/shanten.py, engine/hand_utils.py, players/analysis/, players/humanlike/hand_analyzer.py",
    "HEUR": "players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py",
    "MODEL": "players/analysis/opponent_model.py, hand_predict.py, players/humanlike/belief.py",
    "STATE": "engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py",
    "SCORE": "engine/fan.py, engine/score.py, engine/reward.py",
    "TRAIN": "training/env.py, action_codec_v2.py, observations_v2.py, reward_v2.py, runner.py",
    "AUDIT": "engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py",
}

STEPS = {
    "RULE": [
        "从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。",
        "接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。",
        "接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。",
    ],
    "STATE": [
        "定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。",
        "实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。",
        "通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。",
    ],
    "ALGO": [
        "把Approved规范公式实现为纯函数，固定输入规范化、计算顺序、误差和错误码。",
        "建立golden向量和性质断言；确定算法禁止加载模型或读取超出可见域的数据。",
        "接入上游PlayerView/权威事实和下游候选/规则/计分接口，记录公式版本和输入输出hash。",
    ],
    "SCORE": [
        "实现番/事件事实到不可变`ScoreTransfer`的纯转换，逐条验证支付方与接收方。",
        "实现幂等账本写入、分层结算和累计排名；每事件、每层和本局断言`sum(deltas)==0`。",
        "接入规则提交后事件，完成重放、重复投递、封顶和终局结算证据。",
    ],
    "HEUR": [
        "只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。",
        "实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。",
        "输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。",
    ],
    "MODEL": [
        "冻结线上白名单特征和独立label schema；实现确定规则基线与不可用/OOD/超时回退。",
        "实现训练切分、泄漏扫描、损失、校准、版本/artifact加载和不确定性输出。",
        "在legal mask或策略边界内接入推理；报告Brier/log loss/ECE及卡内最低阈值。",
    ],
    "TRAIN": [
        "通过adapter调用同一生产Engine/Rule/State/Score，不复制环境转换或计分。",
        "实现观测/action mask/reward/seed/回放/快照/数据或评估职责，并隔离restricted truth。",
        "建立生产等价golden、确定回放、并行和性能测试，保存版本与artifact manifest。",
    ],
    "AUDIT": [
        "定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。",
        "实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。",
        "接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。",
    ],
}


def paths(unit_id: str) -> tuple[str, str, str]:
    prefix = unit_id.split("-")[0]
    slug = unit_id.lower().replace("-", "_")
    code = f"{ROOTS[prefix]}/{slug}.py"
    test = f"tests/spec_v3/test_{slug}.py"
    vector = f"tests/spec_v3/vectors/{slug}.jsonl"
    return code, test, vector


def card(row: dict[str, str]) -> str:
    uid = row["新单元ID"]
    prefix = uid.split("-")[0]
    code, test, vector = paths(uid)
    deps = row["上游依赖"] or "无"
    consumers = row["下游消费者"] or "无"
    tests = "、".join(f"T-{uid}-{x}01" for x in "NBIPRX")
    steps = "\n".join(f"{i}. {step}" for i, step in enumerate(STEPS[prefix], 1))
    return f"""## {uid} {row['名称']}

| 字段 | 内容 |
|---|---|
| 单元ID | `{uid}` |
| 类型 | {row['类型']} |
| 目标 | {row['一句话目标']} |
| 建议主文件 | `{code}` |
| 建议测试 | `{test}` |
| 测试向量 | `{vector}` |
| 现有代码候选 | `{LEGACY[prefix]}`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `{deps}` |
| 下游消费者 | `{consumers}` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

{steps}
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：{tests}。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q {test}`。
- 直接行为证据至少EV3；P0/跨模块路径至少EV4；外部效果声明按适用项EV5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

"""


def main() -> None:
    with CATALOG.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    body = """# Spec v3 96单元开发任务卡

| 字段 | 内容 |
|---|---|
| 文档状态 | Draft |
| 日期 | 2026-07-29 |
| 覆盖 | 96/96锁定单元 |
| 单元规格 | Approved |
| 测试规格 | Approved |
| 实现/验收 | 待逐单元差距审计 |

## 使用规则

每卡是实施导航，不复制业务公式。建议主文件表示目标位置；现有代码候选必须经行为审计后才能复用。实施必须按锁定DAG，在上游契约通过后开始下游；可并行的仅是不共享未冻结接口的同层单元。所有任务状态初始保守记为Not Implemented/Not Evaluated，后续由代码、测试和运行证据逐项提升。

""" + "".join(card(row) for row in rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
