"""Generate F0037 leaf-level configuration and runtime contract matrices."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "configs/humanlike_v2/default.json"
REGISTRY = ROOT / "docs/spec-v3/07-traceability/parameter_registry.csv"
STEP_CATEGORIES = ROOT / "docs/features/F0037_parameter_step_categories.csv"
OUT_CSV = ROOT / "docs/features/F0037_leaf_parameter_matrix.csv"
OUT_MD = ROOT / "docs/features/F0037_leaf_parameter_matrix.md"

FIELDS = (
    "parameter_id", "leaf_path", "scope", "default_value", "data_type",
    "range_enum_or_formula", "effect_step_category", "permission",
    "implementation_status", "consumer_unit_ids", "authoritative_source", "notes",
)

EDITABLE_GROUPS = {"GP-024", "GP-025", "GP-027"}
ADVANCED_GROUPS = {"GP-022", "GP-026"}


def scalar_type(value: object) -> str:
    if value is None:
        return "null | integer"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    return type(value).__name__


def flatten(value: object, prefix: str):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from flatten(item, f"{prefix}.{key}" if prefix else key)
    elif isinstance(value, list):
        if not value:
            yield prefix + "[*]", value
        else:
            for index, item in enumerate(value):
                yield from flatten(item, f"{prefix}[{index}]")
    else:
        yield prefix, value


def permission(parameter_id: str, path: str) -> str:
    locked = {
        "GP-001", "GP-002", "GP-004", "GP-006", "GP-007", "GP-008",
        "GP-009", "GP-010", "GP-011", "GP-012", "GP-013", "GP-014",
        "GP-015", "GP-016", "GP-017", "GP-018", "GP-019", "GP-020",
        "GP-021", "GP-023",
    }
    if parameter_id in locked or path.endswith("learn_hidden_information"):
        return "READ_ONLY"
    if parameter_id in ADVANCED_GROUPS:
        return "ADVANCED"
    if parameter_id in EDITABLE_GROUPS or path.startswith("players["):
        return "EDITABLE"
    return "READ_ONLY"


def main() -> None:
    config = json.loads(DEFAULT.read_text(encoding="utf-8"))
    with REGISTRY.open(encoding="utf-8", newline="") as handle:
        registry = {row["parameter_id"]: row for row in csv.DictReader(handle)}
    with STEP_CATEGORIES.open(encoding="utf-8", newline="") as handle:
        steps = {row["parameter_id"]: row["effect_step_category"] for row in csv.DictReader(handle)}

    rows: list[dict[str, str]] = []
    for parameter_id, payload in config["global_parameters"].items():
        meta = registry[parameter_id]
        for path, value in flatten(payload, f"global_parameters.{parameter_id}"):
            rows.append({
                "parameter_id": parameter_id,
                "leaf_path": path,
                "scope": "match_global",
                "default_value": json.dumps(value, ensure_ascii=False),
                "data_type": scalar_type(value),
                "range_enum_or_formula": meta["data_type_and_range"],
                "effect_step_category": steps[parameter_id],
                "permission": permission(parameter_id, path),
                "implementation_status": "IMPLEMENTED",
                "consumer_unit_ids": meta["consumer_unit_ids"],
                "authoritative_source": "default.json + config.py + Task 19 parameter_registry.csv",
                "notes": "真实配置叶字段；具体字段校验以 config.py 为准。",
            })

    profile_ranges = {
        "name": "非空字符串",
        "level": "novice | normal | skilled | expert",
        "style": "conservative | balanced | aggressive",
        "peng_preference": "0..1", "gang_preference": "0..1",
        "big_hand_preference": "0..1", "defense_awareness": "0..1",
        "plan_persistence": "0..1", "thinking_speed": "0..1",
    }
    for seat, player in enumerate(config["players"]):
        for key, value in player["profile"].items():
            rows.append({
                "parameter_id": "GP-023", "leaf_path": f"players[{seat}].profile.{key}",
                "scope": f"seat_s{seat}", "default_value": json.dumps(value, ensure_ascii=False),
                "data_type": scalar_type(value), "range_enum_or_formula": profile_ranges[key],
                "effect_step_category": steps["GP-023"], "permission": "EDITABLE",
                "implementation_status": "IMPLEMENTED",
                "consumer_unit_ids": registry["GP-023"]["consumer_unit_ids"],
                "authoritative_source": "default.json + PlayerProfile.from_dict",
                "notes": "逐座 AI 基础档案字段。",
            })
        for parameter_id, payload in player["cognitive_parameters"].items():
            meta = registry[parameter_id]
            for path, value in flatten(payload, f"players[{seat}].cognitive_parameters.{parameter_id}"):
                rows.append({
                    "parameter_id": parameter_id, "leaf_path": path, "scope": f"seat_s{seat}",
                    "default_value": json.dumps(value, ensure_ascii=False), "data_type": scalar_type(value),
                    "range_enum_or_formula": meta["data_type_and_range"],
                    "effect_step_category": steps[parameter_id], "permission": permission(parameter_id, path),
                    "implementation_status": "IMPLEMENTED",
                    "consumer_unit_ids": meta["consumer_unit_ids"],
                    "authoritative_source": "default.json + config.py + Task 19 parameter_registry.csv",
                    "notes": "逐座认知配置真实叶字段；组内联动约束同样适用。",
                })

    for parameter_id in (f"RP-{index:03d}" for index in range(1, 34)):
        meta = registry[parameter_id]
        status = "IMPLEMENTED_PARTIAL" if parameter_id in {"RP-001", "RP-002", "RP-003", "RP-013", "RP-014", "RP-023", "RP-026", "RP-027", "RP-029", "RP-032", "RP-033"} else "CONTRACT_ONLY"
        rows.append({
            "parameter_id": parameter_id, "leaf_path": f"runtime.{parameter_id}.*",
            "scope": "round_runtime", "default_value": "null",
            "data_type": "runtime payload",
            "range_enum_or_formula": meta["data_type_and_range"],
            "effect_step_category": steps[parameter_id], "permission": "HIDDEN_RUNTIME",
            "implementation_status": status, "consumer_unit_ids": meta["consumer_unit_ids"],
            "authoritative_source": "Task 19 parameter_registry.csv + players/humanlike/runtime.py",
            "notes": "Task 19 未冻结统一叶级 payload schema；* 表示语义字段集合，批准前不得据此新增代码字段。",
        })

    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    counts = {status: sum(row["implementation_status"] == status for row in rows) for status in {row["implementation_status"] for row in rows}}
    md = [
        "# F0037 Humanlike v2 叶参数矩阵", "", "Status: Draft", "",
        "本矩阵由 `tools/generate_f0037_leaf_matrix.py` 从当前默认配置、严格校验器和 Task 19 参数注册表生成。完整机器可读内容见 `F0037_leaf_parameter_matrix.csv`。", "",
        "## 边界", "",
        "- GP 和四座 profile/cognitive 配置行是当前代码真实存在的叶字段。",
        "- RP 当前只冻结了 `RP-001`～`RP-033` 槽位及组级语义，未冻结统一叶级 payload schema，因此使用 `runtime.RP-nnn.*` 表示语义字段集合。",
        "- `CONTRACT_ONLY` 不等于功能缺失，而是表示该 RP 的 payload 由切片拥有；在 F0037 批准前不得把文档公式直接转成新代码字段。", "",
        "## 统计", "", "| 项 | 数量 |", "|---|---:|",
        f"| 总矩阵行 | {len(rows)} |",
        f"| 已实现真实叶字段 | {counts.get('IMPLEMENTED', 0)} |",
        f"| 已有部分统一 payload 的 RP 槽位 | {counts.get('IMPLEMENTED_PARTIAL', 0)} |",
        f"| 仅组级合同的 RP 槽位 | {counts.get('CONTRACT_ONLY', 0)} |", "",
        "## 字段说明", "",
        "| 字段 | 含义 |", "|---|---|",
        "| `leaf_path` | 配置中的精确 JSON 路径；RP 的 `*` 为尚未冻结的语义 payload |",
        "| `default_value` | 当前 `default.json` 值；运行态 RP 在事件产生前为 `null` |",
        "| `range_enum_or_formula` | Task 19 的取值合同、联动约束或运行态公式 |",
        "| `permission` | `EDITABLE` / `ADVANCED` / `READ_ONLY` / `HIDDEN_RUNTIME` |",
        "| `implementation_status` | 文档字段与当前实现的对应程度 |",
        "| `consumer_unit_ids` | 消费该参数组的 Task 19 单元 |", "",
        "## 验收结论", "",
        "- 所有当前 Humanlike v2 配置标量叶字段均有矩阵行。",
        "- 四个座位分别展开，不把 S0 的默认值误用于其他座位。",
        "- 33 个 RP 均有运行态合同覆盖，同时显式暴露叶级 schema 缺口。",
    ]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps({"rows": len(rows), "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
