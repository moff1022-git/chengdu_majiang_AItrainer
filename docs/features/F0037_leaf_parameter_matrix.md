# F0037 Humanlike v2 叶参数矩阵

Status: Draft

本矩阵由 `tools/generate_f0037_leaf_matrix.py` 从当前默认配置、严格校验器和 Task 19 参数注册表生成。完整机器可读内容见 `F0037_leaf_parameter_matrix.csv`。

## 边界

- GP 和四座 profile/cognitive 配置行是当前代码真实存在的叶字段。
- RP 当前只冻结了 `RP-001`～`RP-033` 槽位及组级语义，未冻结统一叶级 payload schema，因此使用 `runtime.RP-nnn.*` 表示语义字段集合。
- `CONTRACT_ONLY` 不等于功能缺失，而是表示该 RP 的 payload 由切片拥有；在 F0037 批准前不得把文档公式直接转成新代码字段。

## 统计

| 项 | 数量 |
|---|---:|
| 总矩阵行 | 277 |
| 已实现真实叶字段 | 244 |
| 已有部分统一 payload 的 RP 槽位 | 11 |
| 仅组级合同的 RP 槽位 | 22 |

## 字段说明

| 字段 | 含义 |
|---|---|
| `leaf_path` | 配置中的精确 JSON 路径；RP 的 `*` 为尚未冻结的语义 payload |
| `default_value` | 当前 `default.json` 值；运行态 RP 在事件产生前为 `null` |
| `range_enum_or_formula` | Task 19 的取值合同、联动约束或运行态公式 |
| `permission` | `EDITABLE` / `ADVANCED` / `READ_ONLY` / `HIDDEN_RUNTIME` |
| `implementation_status` | 文档字段与当前实现的对应程度 |
| `consumer_unit_ids` | 消费该参数组的 Task 19 单元 |

## 验收结论

- 所有当前 Humanlike v2 配置标量叶字段均有矩阵行。
- 四个座位分别展开，不把 S0 的默认值误用于其他座位。
- 33 个 RP 均有运行态合同覆盖，同时显式暴露叶级 schema 缺口。
