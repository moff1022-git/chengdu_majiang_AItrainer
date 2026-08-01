# Spec v3 金标准向量目录

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 覆盖 | ALGO-001～011与SCORE-001～006；每单元正常/边界/非法 |
| 向量实现/证据 | Not Implemented / Not Evaluated |

以下描述逐字义来源于Approved ALGO/SCORE规格的“金标准示例”。实现时必须将描述展开为canonical JSONL的完整字段和中间量，计算并冻结SHA-256；没有实际JSONL和hash前不得标Passed。规范expected与baseline_expected必须分栏。

| 向量ID | 单元 | 类别 | Approved示例 | 计划JSONL定位 | 误差/判定 |
|---|---|---|---|---|---|
| `GV-ALGO-001-N01` | `ALGO-001` | 正常 | 0..107各一次通过 | `tests/spec_v3/vectors/algo_001.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-001-B01` | `ALGO-001` | 边界 | 全在wall通过 | `tests/spec_v3/vectors/algo_001.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-001-I01` | `ALGO-001` | 非法 | id7位于hand和meld→OWNERSHIP_DUPLICATE | `tests/spec_v3/vectors/algo_001.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-ALGO-002-N01` | `ALGO-002` | 正常 | 123W456W123T123B+W9为单钓0向听 | `tests/spec_v3/vectors/algo_002.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-002-B01` | `ALGO-002` | 边界 | 七对子=-1 | `tests/spec_v3/vectors/algo_002.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-002-I01` | `ALGO-002` | 非法 | 某面5张→FACE_COUNT_EXCEEDED | `tests/spec_v3/vectors/algo_002.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-ALGO-003-N01` | `ALGO-003` | 正常 | 自有W1×2+公开W1×1→V3/U1 | `tests/spec_v3/vectors/algo_003.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-003-B01` | `ALGO-003` | 边界 | V4/U0 | `tests/spec_v3/vectors/algo_003.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-003-I01` | `ALGO-003` | 非法 | 同physical重复→VISIBLE_DUPLICATE | `tests/spec_v3/vectors/algo_003.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-ALGO-004-N01` | `ALGO-004` | 正常 | U=[2,2],W2→E=[1,1] | `tests/spec_v3/vectors/algo_004.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-004-B01` | `ALGO-004` | 边界 | W0全0 | `tests/spec_v3/vectors/algo_004.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-004-I01` | `ALGO-004` | 非法 | U3/W4→WALL_UNSEEN_CONFLICT | `tests/spec_v3/vectors/algo_004.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-ALGO-005-N01` | `ALGO-005` | 正常 | order0123,next1,W5→[1,2,1,1] | `tests/spec_v3/vectors/algo_005.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-005-B01` | `ALGO-005` | 边界 | W0全0 | `tests/spec_v3/vectors/algo_005.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-005-I01` | `ALGO-005` | 非法 | actor不活动→ACTOR_NOT_ACTIVE | `tests/spec_v3/vectors/algo_005.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-ALGO-006-N01` | `ALGO-006` | 正常 | HU强制+两弃牌,cap1→HU+键最小弃牌 | `tests/spec_v3/vectors/algo_006.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-006-B01` | `ALGO-006` | 边界 | 两强制均保留 | `tests/spec_v3/vectors/algo_006.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-006-I01` | `ALGO-006` | 非法 | cap0 | `tests/spec_v3/vectors/algo_006.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-ALGO-007-N01` | `ALGO-007` | 正常 | 仅S权重1且S=.75→Q=.75 | `tests/spec_v3/vectors/algo_007.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-007-B01` | `ALGO-007` | 边界 | 仅R=1→-1 | `tests/spec_v3/vectors/algo_007.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-007-I01` | `ALGO-007` | 非法 | S=1.1 | `tests/spec_v3/vectors/algo_007.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-ALGO-008-N01` | `ALGO-008` | 正常 | 同tuple百次一致 | `tests/spec_v3/vectors/algo_008.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-008-B01` | `ALGO-008` | 边界 | seed0/index0 | `tests/spec_v3/vectors/algo_008.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-008-I01` | `ALGO-008` | 非法 | unknown purpose | `tests/spec_v3/vectors/algo_008.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-ALGO-009-N01` | `ALGO-009` | 正常 | 键序不同hash同 | `tests/spec_v3/vectors/algo_009.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-009-B01` | `ALGO-009` | 边界 | =max通过 | `tests/spec_v3/vectors/algo_009.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-009-I01` | `ALGO-009` | 非法 | NaN/未知GP | `tests/spec_v3/vectors/algo_009.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-ALGO-010-N01` | `ALGO-010` | 正常 | S0见自己手而S1仅张数 | `tests/spec_v3/vectors/algo_010.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-010-B01` | `ALGO-010` | 边界 | finished仍不自动公开墙序 | `tests/spec_v3/vectors/algo_010.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-010-I01` | `ALGO-010` | 非法 | viewer4 | `tests/spec_v3/vectors/algo_010.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-ALGO-011-N01` | `ALGO-011` | 正常 | 同ID映射同 | `tests/spec_v3/vectors/algo_011.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-011-B01` | `ALGO-011` | 边界 | 1字节ID | `tests/spec_v3/vectors/algo_011.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-ALGO-011-I01` | `ALGO-011` | 非法 | 空ID | `tests/spec_v3/vectors/algo_011.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-SCORE-001-N01` | `SCORE-001` | 正常 | S1→S0 4=[+4,-4] | `tests/spec_v3/vectors/score_001.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-SCORE-001-B01` | `SCORE-001` | 边界 | 允许负余额 | `tests/spec_v3/vectors/score_001.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-SCORE-001-I01` | `SCORE-001` | 非法 | 仅S0+4无payer | `tests/spec_v3/vectors/score_001.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-SCORE-002-N01` | `SCORE-002` | 正常 | base1 fan2点炮→±4 | `tests/spec_v3/vectors/score_002.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-SCORE-002-B01` | `SCORE-002` | 边界 | fan0自摸三家各付1 | `tests/spec_v3/vectors/score_002.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-SCORE-002-I01` | `SCORE-002` | 非法 | winner=loser | `tests/spec_v3/vectors/score_002.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-SCORE-003-N01` | `SCORE-003` | 正常 | 暗杠S0获三家各2 | `tests/spec_v3/vectors/score_003.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-SCORE-003-B01` | `SCORE-003` | 边界 | 仅一对手付2 | `tests/spec_v3/vectors/score_003.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-SCORE-003-I01` | `SCORE-003` | 非法 | 明杠缺source | `tests/spec_v3/vectors/score_003.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-SCORE-004-N01` | `SCORE-004` | 正常 | base1花猪fan3向三家各付8 | `tests/spec_v3/vectors/score_004.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-SCORE-004-B01` | `SCORE-004` | 边界 | 无人听则查叫no-op | `tests/spec_v3/vectors/score_004.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-SCORE-004-I01` | `SCORE-004` | 非法 | ting缺maxfan | `tests/spec_v3/vectors/score_004.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-SCORE-005-N01` | `SCORE-005` | 正常 | raw5 cap3→eff3/P8 | `tests/spec_v3/vectors/score_005.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-SCORE-005-B01` | `SCORE-005` | 边界 | cap0→5 | `tests/spec_v3/vectors/score_005.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-SCORE-005-I01` | `SCORE-005` | 非法 | 互斥项并存 | `tests/spec_v3/vectors/score_005.jsonl#golden=I01` | 稳定错误码精确匹配 |
| `GV-SCORE-006-N01` | `SCORE-006` | 正常 | prior00+delta[4,-4]→rank S0>S1 | `tests/spec_v3/vectors/score_006.jsonl#golden=N01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-SCORE-006-B01` | `SCORE-006` | 边界 | 全0并列 | `tests/spec_v3/vectors/score_006.jsonl#golden=B01` | 采用Approved卡允许误差；整数/集合默认0 |
| `GV-SCORE-006-I01` | `SCORE-006` | 非法 | delta和1 | `tests/spec_v3/vectors/score_006.jsonl#golden=I01` | 稳定错误码精确匹配 |


## 向量必填字段

`vector_id,unit_id,case_kind,ruleset_version,formula_version,baseline_version,config_hash,seed_ref,input,normalized_input,intermediates,expected,baseline_expected,expected_error,tolerance,source_clause_refs,canonical_sha256`。非法向量的`expected=null`；正常/边界向量不得用当前实现输出来自动冻结expected，必须经规范复算和独立复核。

## 复现门禁

同一向量在同进程重复100次、隔离进程至少2次，并在支持平台上比较canonical输出；规范字段、状态、集合、错误码和hash逐字段一致。任何seed、版本、输入或expected变化必须产生新向量版本和hash，不得覆盖已引用向量。
# 3.0.1 试点单元强制fixture补充

## 3.0.2 Medium问题向量

- RULE-003：查询前后state canonical hash和version必须相同；仍持缺门时输出只含缺门牌面。
- ALGO-001：完整region schema中只有wall含0..107通过；删除`removed`返回`REGION_MISSING`；增加`unknown` 返回`REGION_UNKNOWN`。
- TRAIN-003：`decode(0)=PASS,decode(1)=HU,decode(110)=DISCARD wan1,decode(632)=DINGQUE wan,decode(634)=DINGQUE tiao`；-1和635返回`ACTION_CODEC_INVALID`。
- 日志/性能：对每试点入口至少1000 warm samples，并验证性能前后oracle hash相同。

以下fixture不得从实现反向生成：`RULE-016`: 四人局viewer0只含self0暗手且viewer4=`INVALID_VIEWER`；`STATE-005`: 三层嵌套写入拒绝且canonical hash 100次一致；`HEUR-019`: A=1.00000000、B=.70000000、C=1.05000000，排序A/C/B；`MODEL-001`: 无证据输出冻结规则先验且各分布和1±1e-9，含`hand`键返回`FORBIDDEN_INPUT`；`SCORE-001`: `[0,0,0,0]+(1→0,4)=[4,-4,0,0]`；`AUDIT-003`: 使用本版逐字节B规则并覆盖单字节篡改、截断和重排。每个fixture记录seed（不消费随机数写`NONE`）、expected log字段及自动化位置。
