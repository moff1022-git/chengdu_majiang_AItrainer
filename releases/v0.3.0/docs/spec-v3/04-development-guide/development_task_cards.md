# Spec v3 96单元开发任务卡

| 字段 | 内容 |
|---|---|
| 文档状态 | Locked |
| 日期 | 2026-07-29 |
| 覆盖 | 96/96锁定单元 |
| 单元规格 | Approved |
| 测试规格 | Approved |
| 实现/验收 | 待逐单元差距审计 |

## 使用规则

每卡是实施导航，不复制业务公式。建议主文件表示目标位置；现有代码候选必须经行为审计后才能复用。实施必须按锁定DAG，在上游契约通过后开始下游；可并行的仅是不共享未冻结接口的同层单元。所有任务状态初始保守记为Not Implemented/Not Evaluated，后续由代码、测试和运行证据逐项提升。

## RULE-001 规则、参数、不变量与合法性裁决优先级

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-001` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「authoritative legal set or explicit rejection」并通过「冲突配置及非法动作表驱动测试」验收。 |
| 建议主文件 | `engine/rules/rule_001.py` |
| 建议测试 | `tests/spec_v3/test_rule_001.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_001.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-002|STATE-010|ALGO-009` |
| 下游消费者 | `ALGO-006|AUDIT-005|RULE-007|RULE-008|RULE-010|RULE-013|STATE-009|TRAIN-001|TRAIN-003` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-001-N01、T-RULE-001-B01、T-RULE-001-I01、T-RULE-001-P01、T-RULE-001-R01、T-RULE-001-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_001.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-002 换三张同花色、方向与提交合法性

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-002` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「accepted exchange or error」并通过「方向×花色×实体牌用例」验收。 |
| 建议主文件 | `engine/rules/rule_002.py` |
| 建议测试 | `tests/spec_v3/test_rule_002.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_002.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-003|STATE-011|ALGO-001` |
| 下游消费者 | `HEUR-001` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-002-N01、T-RULE-002-B01、T-RULE-002-I01、T-RULE-002-P01、T-RULE-002-R01、T-RULE-002-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_002.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-003 定缺未清时的强制出牌约束

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-003` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「legal discards」并通过「缺门存在/清空边界」验收。 |
| 建议主文件 | `engine/rules/rule_003.py` |
| 建议测试 | `tests/spec_v3/test_rule_003.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_003.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-003` |
| 下游消费者 | `HEUR-002|HEUR-014` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-003-N01、T-RULE-003-B01、T-RULE-003-I01、T-RULE-003-P01、T-RULE-003-R01、T-RULE-003-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_003.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-004 定缺、死叫与胡牌资格约束

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-004` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「hu eligibility」并通过「清缺/未清/死叫用例」验收。 |
| 建议主文件 | `engine/rules/rule_004.py` |
| 建议测试 | `tests/spec_v3/test_rule_004.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_004.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-003|ALGO-002` |
| 下游消费者 | `SCORE-004` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-004-N01、T-RULE-004-B01、T-RULE-004-I01、T-RULE-004-P01、T-RULE-004-R01、T-RULE-004-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_004.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-005 座位、庄家与活动顺序

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-005` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「next actor」并通过「2/3/4 人及退出轮转」验收。 |
| 建议主文件 | `engine/rules/rule_005.py` |
| 建议测试 | `tests/spec_v3/test_rule_005.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_005.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-002` |
| 下游消费者 | `ALGO-005|RULE-014` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-005-N01、T-RULE-005-B01、T-RULE-005-I01、T-RULE-005-P01、T-RULE-005-R01、T-RULE-005-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_005.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-006 摸牌、可选响应与出牌标准顺序

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-006` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「next phase/action request」并通过「每阶段状态转换表」验收。 |
| 建议主文件 | `engine/rules/rule_006.py` |
| 建议测试 | `tests/spec_v3/test_rule_006.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_006.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-004|STATE-011` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-006-N01、T-RULE-006-B01、T-RULE-006-I01、T-RULE-006-P01、T-RULE-006-R01、T-RULE-006-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_006.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-007 碰牌资格、执行与后续出牌

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-007` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「meld/turn」并通过「合法/非法碰及让序」验收。 |
| 建议主文件 | `engine/rules/rule_007.py` |
| 建议测试 | `tests/spec_v3/test_rule_007.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_007.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-001|STATE-003` |
| 下游消费者 | `HEUR-012|RULE-013` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-007-N01、T-RULE-007-B01、T-RULE-007-I01、T-RULE-007-P01、T-RULE-007-R01、T-RULE-007-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_007.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-008 明杠、暗杠与补杠资格及执行

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-008` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「gang transition」并通过「三类杠与补牌守恒」验收。 |
| 建议主文件 | `engine/rules/rule_008.py` |
| 建议测试 | `tests/spec_v3/test_rule_008.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_008.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-001|STATE-003|STATE-011` |
| 下游消费者 | `HEUR-013|RULE-009|SCORE-003` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-008-N01、T-RULE-008-B01、T-RULE-008-I01、T-RULE-008-P01、T-RULE-008-R01、T-RULE-008-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_008.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-009 补杠抢杠胡窗口与解析

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-009` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「hu or gang」并通过「抢杠/无人抢/多人抢」验收。 |
| 建议主文件 | `engine/rules/rule_009.py` |
| 建议测试 | `tests/spec_v3/test_rule_009.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_009.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-008|RULE-010` |
| 下游消费者 | `HEUR-013|RULE-013|SCORE-003` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-009-N01、T-RULE-009-B01、T-RULE-009-I01、T-RULE-009-P01、T-RULE-009-R01、T-RULE-009-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_009.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-010 自摸、点炮与抢杠胡资格

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-010` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「legal hu set」并通过「三类胡及反例」验收。 |
| 建议主文件 | `engine/rules/rule_010.py` |
| 建议测试 | `tests/spec_v3/test_rule_010.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_010.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-001|STATE-003|ALGO-002` |
| 下游消费者 | `RULE-009|RULE-011|RULE-012|RULE-013|RULE-014|SCORE-002` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-010-N01、T-RULE-010-B01、T-RULE-010-I01、T-RULE-010-P01、T-RULE-010-R01、T-RULE-010-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_010.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-011 过胡设置、持续与恢复

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-011` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「pass-hu state」并通过「恢复模式矩阵」验收。 |
| 建议主文件 | `engine/rules/rule_011.py` |
| 建议测试 | `tests/spec_v3/test_rule_011.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_011.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-010|STATE-003` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-011-N01、T-RULE-011-B01、T-RULE-011-I01、T-RULE-011-P01、T-RULE-011-R01、T-RULE-011-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_011.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-012 强制胡与最后阶段必胡

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-012` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「forced action」并通过「开关及尾牌边界」验收。 |
| 建议主文件 | `engine/rules/rule_012.py` |
| 建议测试 | `tests/spec_v3/test_rule_012.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_012.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-010|STATE-011` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-012-N01、T-RULE-012-B01、T-RULE-012-I01、T-RULE-012-P01、T-RULE-012-R01、T-RULE-012-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_012.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-013 多人响应确定性优先级

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-013` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「resolved actions」并通过「返回时序置换不变」验收。 |
| 建议主文件 | `engine/rules/rule_013.py` |
| 建议测试 | `tests/spec_v3/test_rule_013.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_013.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-001|RULE-007|RULE-009|RULE-010` |
| 下游消费者 | `TRAIN-007` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-013-N01、T-RULE-013-B01、T-RULE-013-I01、T-RULE-013-P01、T-RULE-013-R01、T-RULE-013-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_013.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-014 血战胡后退出、继续与终止

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-014` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「active set/end」并通过「第1/2/3胡与荒牌」验收。 |
| 建议主文件 | `engine/rules/rule_014.py` |
| 建议测试 | `tests/spec_v3/test_rule_014.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_014.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-005|RULE-010|STATE-004` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-014-N01、T-RULE-014-B01、T-RULE-014-I01、T-RULE-014-P01、T-RULE-014-R01、T-RULE-014-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_014.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-015 启用番型、互斥/叠加与封顶规则

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-015` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「applicable fan policy」并通过「配置组合 golden cases」验收。 |
| 建议主文件 | `engine/rules/rule_015.py` |
| 建议测试 | `tests/spec_v3/test_rule_015.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_015.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-010` |
| 下游消费者 | `HEUR-011|SCORE-002|SCORE-004|SCORE-005` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-015-N01、T-RULE-015-B01、T-RULE-015-I01、T-RULE-015-P01、T-RULE-015-R01、T-RULE-015-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_015.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## RULE-016 局中与终局公开信息范围

| 字段 | 内容 |
|---|---|
| 单元ID | `RULE-016` |
| 类型 | 确定规则 |
| 目标 | 在冻结输入和版本下，独立产生「visible field set」并通过「白名单/禁止字段矩阵」验收。 |
| 建议主文件 | `engine/rules/rule_016.py` |
| 建议测试 | `tests/spec_v3/test_rule_016.py` |
| 测试向量 | `tests/spec_v3/vectors/rule_016.jsonl` |
| 现有代码候选 | `engine/rules.py, engine/legal.py, engine/blood_battle.py, engine/exchange.py, engine/opening.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-004|STATE-010` |
| 下游消费者 | `ALGO-010|AUDIT-013|MODEL-003` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 从Approved卡提取输入、稳定错误码、状态转移与不变量，先实现无I/O纯裁决函数。
2. 接入`RuleEngine`门面和权威command handler；所有effects先生成事件草案，再原子commit。
3. 接入RULE-016视图边界、AUDIT事件字段和适用的SCORE事实，禁止策略修改结果。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-RULE-016-N01、T-RULE-016-B01、T-RULE-016-I01、T-RULE-016-P01、T-RULE-016-R01、T-RULE-016-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_rule_016.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## ALGO-001 face/physical tile 编码、投影与所有权守恒

| 字段 | 内容 |
|---|---|
| 单元ID | `ALGO-001` |
| 类型 | 确定算法 |
| 目标 | 在冻结输入和版本下，独立产生「face views + conservation result」并通过「108 张唯一性和迁移用例」验收。 |
| 建议主文件 | `engine/analysis/algo_001.py` |
| 建议测试 | `tests/spec_v3/test_algo_001.py` |
| 测试向量 | `tests/spec_v3/vectors/algo_001.jsonl` |
| 现有代码候选 | `engine/physical_tile.py, engine/shanten.py, engine/hand_utils.py, players/analysis/, players/humanlike/hand_analyzer.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-011` |
| 下游消费者 | `ALGO-003|AUDIT-005|RULE-002|STATE-003` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 把Approved规范公式实现为纯函数，固定输入规范化、计算顺序、误差和错误码。
2. 建立golden向量和性质断言；确定算法禁止加载模型或读取超出可见域的数据。
3. 接入上游PlayerView/权威事实和下游候选/规则/计分接口，记录公式版本和输入输出hash。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-ALGO-001-N01、T-ALGO-001-B01、T-ALGO-001-I01、T-ALGO-001-P01、T-ALGO-001-R01、T-ALGO-001-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_algo_001.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## ALGO-002 手牌分解、向听、弃牌向听与等待形状

| 字段 | 内容 |
|---|---|
| 单元ID | `ALGO-002` |
| 类型 | 确定算法 |
| 目标 | 在冻结输入和版本下，独立产生「analyses」并通过「标准/七对/特殊边界」验收。 |
| 建议主文件 | `engine/analysis/algo_002.py` |
| 建议测试 | `tests/spec_v3/test_algo_002.py` |
| 测试向量 | `tests/spec_v3/vectors/algo_002.jsonl` |
| 现有代码候选 | `engine/physical_tile.py, engine/shanten.py, engine/hand_utils.py, players/analysis/, players/humanlike/hand_analyzer.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-003` |
| 下游消费者 | `ALGO-007|HEUR-001|HEUR-002|HEUR-004|HEUR-009|HEUR-011|HEUR-012|HEUR-014|RULE-004|RULE-010` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 把Approved规范公式实现为纯函数，固定输入规范化、计算顺序、误差和错误码。
2. 建立golden向量和性质断言；确定算法禁止加载模型或读取超出可见域的数据。
3. 接入上游PlayerView/权威事实和下游候选/规则/计分接口，记录公式版本和输入输出hash。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-ALGO-002-N01、T-ALGO-002-B01、T-ALGO-002-I01、T-ALGO-002-P01、T-ALGO-002-R01、T-ALGO-002-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_algo_002.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## ALGO-003 去重可见牌与未见牌聚合

| 字段 | 内容 |
|---|---|
| 单元ID | `ALGO-003` |
| 类型 | 确定算法 |
| 目标 | 在冻结输入和版本下，独立产生「visible/unseen counts」并通过「被认领弃牌去重用例」验收。 |
| 建议主文件 | `engine/analysis/algo_003.py` |
| 建议测试 | `tests/spec_v3/test_algo_003.py` |
| 测试向量 | `tests/spec_v3/vectors/algo_003.jsonl` |
| 现有代码候选 | `engine/physical_tile.py, engine/shanten.py, engine/hand_utils.py, players/analysis/, players/humanlike/hand_analyzer.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-005|ALGO-001` |
| 下游消费者 | `ALGO-004|ALGO-007|HEUR-001|MODEL-001|MODEL-002` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 把Approved规范公式实现为纯函数，固定输入规范化、计算顺序、误差和错误码。
2. 建立golden向量和性质断言；确定算法禁止加载模型或读取超出可见域的数据。
3. 接入上游PlayerView/权威事实和下游候选/规则/计分接口，记录公式版本和输入输出hash。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-ALGO-003-N01、T-ALGO-003-B01、T-ALGO-003-I01、T-ALGO-003-P01、T-ALGO-003-R01、T-ALGO-003-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_algo_003.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## ALGO-004 墙内活牌区间或估计

| 字段 | 内容 |
|---|---|
| 单元ID | `ALGO-004` |
| 类型 | 确定算法 |
| 目标 | 在冻结输入和版本下，独立产生「live estimate」并通过「上下界、归一与极端状态」验收。 |
| 建议主文件 | `engine/analysis/algo_004.py` |
| 建议测试 | `tests/spec_v3/test_algo_004.py` |
| 测试向量 | `tests/spec_v3/vectors/algo_004.jsonl` |
| 现有代码候选 | `engine/physical_tile.py, engine/shanten.py, engine/hand_utils.py, players/analysis/, players/humanlike/hand_analyzer.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-003|STATE-011` |
| 下游消费者 | `MODEL-002` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 把Approved规范公式实现为纯函数，固定输入规范化、计算顺序、误差和错误码。
2. 建立golden向量和性质断言；确定算法禁止加载模型或读取超出可见域的数据。
3. 接入上游PlayerView/权威事实和下游候选/规则/计分接口，记录公式版本和输入输出hash。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-ALGO-004-N01、T-ALGO-004-B01、T-ALGO-004-I01、T-ALGO-004-P01、T-ALGO-004-R01、T-ALGO-004-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_algo_004.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## ALGO-005 逐座剩余摸牌机会估计

| 字段 | 内容 |
|---|---|
| 单元ID | `ALGO-005` |
| 类型 | 确定算法 |
| 目标 | 在冻结输入和版本下，独立产生「draw interval」并通过「碰杠胡后重算」验收。 |
| 建议主文件 | `engine/analysis/algo_005.py` |
| 建议测试 | `tests/spec_v3/test_algo_005.py` |
| 测试向量 | `tests/spec_v3/vectors/algo_005.jsonl` |
| 现有代码候选 | `engine/physical_tile.py, engine/shanten.py, engine/hand_utils.py, players/analysis/, players/humanlike/hand_analyzer.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-005|STATE-011` |
| 下游消费者 | `ALGO-007|HEUR-009` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 把Approved规范公式实现为纯函数，固定输入规范化、计算顺序、误差和错误码。
2. 建立golden向量和性质断言；确定算法禁止加载模型或读取超出可见域的数据。
3. 接入上游PlayerView/权威事实和下游候选/规则/计分接口，记录公式版本和输入输出hash。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-ALGO-005-N01、T-ALGO-005-B01、T-ALGO-005-I01、T-ALGO-005-P01、T-ALGO-005-R01、T-ALGO-005-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_algo_005.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## ALGO-006 mandatory 分类、候选上限与稳定排序

| 字段 | 内容 |
|---|---|
| 单元ID | `ALGO-006` |
| 类型 | 确定算法 |
| 目标 | 在冻结输入和版本下，独立产生「mandatory/candidate set」并通过「唯一动作、强制项不裁剪」验收。 |
| 建议主文件 | `engine/analysis/algo_006.py` |
| 建议测试 | `tests/spec_v3/test_algo_006.py` |
| 测试向量 | `tests/spec_v3/vectors/algo_006.jsonl` |
| 现有代码候选 | `engine/physical_tile.py, engine/shanten.py, engine/hand_utils.py, players/analysis/, players/humanlike/hand_analyzer.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-001|STATE-009` |
| 下游消费者 | `HEUR-021|HEUR-023|STATE-012` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 把Approved规范公式实现为纯函数，固定输入规范化、计算顺序、误差和错误码。
2. 建立golden向量和性质断言；确定算法禁止加载模型或读取超出可见域的数据。
3. 接入上游PlayerView/权威事实和下游候选/规则/计分接口，记录公式版本和输入输出hash。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-ALGO-006-N01、T-ALGO-006-B01、T-ALGO-006-I01、T-ALGO-006-P01、T-ALGO-006-R01、T-ALGO-006-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_algo_006.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## ALGO-007 六分量候选 Q 评价

| 字段 | 内容 |
|---|---|
| 单元ID | `ALGO-007` |
| 类型 | 确定算法 |
| 目标 | 在冻结输入和版本下，独立产生「Q components/total」并通过「分量、范围、权重与 tie-break」验收。 |
| 建议主文件 | `engine/analysis/algo_007.py` |
| 建议测试 | `tests/spec_v3/test_algo_007.py` |
| 测试向量 | `tests/spec_v3/vectors/algo_007.jsonl` |
| 现有代码候选 | `engine/physical_tile.py, engine/shanten.py, engine/hand_utils.py, players/analysis/, players/humanlike/hand_analyzer.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-002|ALGO-003|ALGO-005|STATE-010` |
| 下游消费者 | `AUDIT-002|HEUR-010|HEUR-021|HEUR-023` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 把Approved规范公式实现为纯函数，固定输入规范化、计算顺序、误差和错误码。
2. 建立golden向量和性质断言；确定算法禁止加载模型或读取超出可见域的数据。
3. 接入上游PlayerView/权威事实和下游候选/规则/计分接口，记录公式版本和输入输出hash。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-ALGO-007-N01、T-ALGO-007-B01、T-ALGO-007-I01、T-ALGO-007-P01、T-ALGO-007-R01、T-ALGO-007-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_algo_007.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## ALGO-008 seed、噪声、思考时间与随机流确定派生

| 字段 | 内容 |
|---|---|
| 单元ID | `ALGO-008` |
| 类型 | 确定算法 |
| 目标 | 在冻结输入和版本下，独立产生「reproducible samples」并通过「跨进程/hash-seed 重现」验收。 |
| 建议主文件 | `engine/analysis/algo_008.py` |
| 建议测试 | `tests/spec_v3/test_algo_008.py` |
| 测试向量 | `tests/spec_v3/vectors/algo_008.jsonl` |
| 现有代码候选 | `engine/physical_tile.py, engine/shanten.py, engine/hand_utils.py, players/analysis/, players/humanlike/hand_analyzer.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-011|STATE-009` |
| 下游消费者 | `AUDIT-004|HEUR-017|HEUR-023` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 把Approved规范公式实现为纯函数，固定输入规范化、计算顺序、误差和错误码。
2. 建立golden向量和性质断言；确定算法禁止加载模型或读取超出可见域的数据。
3. 接入上游PlayerView/权威事实和下游候选/规则/计分接口，记录公式版本和输入输出hash。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-ALGO-008-N01、T-ALGO-008-B01、T-ALGO-008-I01、T-ALGO-008-P01、T-ALGO-008-R01、T-ALGO-008-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_algo_008.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## ALGO-009 配置类型/范围/版本校验、迁移与 canonical hash

| 字段 | 内容 |
|---|---|
| 单元ID | `ALGO-009` |
| 类型 | 确定算法 |
| 目标 | 在冻结输入和版本下，独立产生「frozen config/hash or explicit error」并通过「旧版迁移与未知组合拒绝」验收。 |
| 建议主文件 | `engine/analysis/algo_009.py` |
| 建议测试 | `tests/spec_v3/test_algo_009.py` |
| 测试向量 | `tests/spec_v3/vectors/algo_009.jsonl` |
| 现有代码候选 | `engine/physical_tile.py, engine/shanten.py, engine/hand_utils.py, players/analysis/, players/humanlike/hand_analyzer.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-010` |
| 下游消费者 | `AUDIT-011|RULE-001|STATE-001|STATE-007` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 把Approved规范公式实现为纯函数，固定输入规范化、计算顺序、误差和错误码。
2. 建立golden向量和性质断言；确定算法禁止加载模型或读取超出可见域的数据。
3. 接入上游PlayerView/权威事实和下游候选/规则/计分接口，记录公式版本和输入输出hash。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-ALGO-009-N01、T-ALGO-009-B01、T-ALGO-009-I01、T-ALGO-009-P01、T-ALGO-009-R01、T-ALGO-009-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_algo_009.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## ALGO-010 PlayerView 白名单构建

| 字段 | 内容 |
|---|---|
| 单元ID | `ALGO-010` |
| 类型 | 确定算法 |
| 目标 | 在冻结输入和版本下，独立产生「PlayerView」并通过「隐藏字段不存在及冻结」验收。 |
| 建议主文件 | `engine/analysis/algo_010.py` |
| 建议测试 | `tests/spec_v3/test_algo_010.py` |
| 测试向量 | `tests/spec_v3/vectors/algo_010.jsonl` |
| 现有代码候选 | `engine/physical_tile.py, engine/shanten.py, engine/hand_utils.py, players/analysis/, players/humanlike/hand_analyzer.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-016|STATE-002` |
| 下游消费者 | `AUDIT-013|STATE-005|TRAIN-002` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 把Approved规范公式实现为纯函数，固定输入规范化、计算顺序、误差和错误码。
2. 建立golden向量和性质断言；确定算法禁止加载模型或读取超出可见域的数据。
3. 接入上游PlayerView/权威事实和下游候选/规则/计分接口，记录公式版本和输入输出hash。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-ALGO-010-N01、T-ALGO-010-B01、T-ALGO-010-I01、T-ALGO-010-P01、T-ALGO-010-R01、T-ALGO-010-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_algo_010.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## ALGO-011 game_id 到牌墙、骰子及子随机流的确定映射

| 字段 | 内容 |
|---|---|
| 单元ID | `ALGO-011` |
| 类型 | 确定算法 |
| 目标 | 在冻结输入和版本下，独立产生「named RNG streams」并通过「同 ID 同流、域隔离（新增）」验收。 |
| 建议主文件 | `engine/analysis/algo_011.py` |
| 建议测试 | `tests/spec_v3/test_algo_011.py` |
| 测试向量 | `tests/spec_v3/vectors/algo_011.jsonl` |
| 现有代码候选 | `engine/physical_tile.py, engine/shanten.py, engine/hand_utils.py, players/analysis/, players/humanlike/hand_analyzer.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-010` |
| 下游消费者 | `ALGO-008|AUDIT-007|STATE-001|STATE-011|TRAIN-009` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 把Approved规范公式实现为纯函数，固定输入规范化、计算顺序、误差和错误码。
2. 建立golden向量和性质断言；确定算法禁止加载模型或读取超出可见域的数据。
3. 接入上游PlayerView/权威事实和下游候选/规则/计分接口，记录公式版本和输入输出hash。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-ALGO-011-N01、T-ALGO-011-B01、T-ALGO-011-I01、T-ALGO-011-P01、T-ALGO-011-R01、T-ALGO-011-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_algo_011.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-001 换三张候选评价

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-001` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「ranked triples」并通过「强结构保护与送牌敏感场景」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_001.py` |
| 建议测试 | `tests/spec_v3/test_heur_001.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_001.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-002|ALGO-002|ALGO-003` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-001-N01、T-HEUR-001-B01、T-HEUR-001-I01、T-HEUR-001-P01、T-HEUR-001-R01、T-HEUR-001-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_001.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-002 定缺花色评价

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-002` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「ranked suits」并通过「0张、少而散、清一色反例」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_002.py` |
| 建议测试 | `tests/spec_v3/test_heur_002.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_002.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-003|ALGO-002` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-002-N01、T-HEUR-002-B01、T-HEUR-002-I01、T-HEUR-002-P01、T-HEUR-002-R01、T-HEUR-002-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_002.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-003 动态风格调节

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-003` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「effective style knobs」并通过「保守/激进方向效应」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_003.py` |
| 建议测试 | `tests/spec_v3/test_heur_003.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_003.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-001|STATE-010|HEUR-022` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-003-N01、T-HEUR-003-B01、T-HEUR-003-I01、T-HEUR-003-P01、T-HEUR-003-R01、T-HEUR-003-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_003.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-004 初始做牌方向形成

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-004` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「primary/backup direction」并通过「不同牌型初始场景」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_004.py` |
| 建议测试 | `tests/spec_v3/test_heur_004.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_004.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-002|HEUR-022` |
| 下游消费者 | `HEUR-005` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-004-N01、T-HEUR-004-B01、T-HEUR-004-I01、T-HEUR-004-P01、T-HEUR-004-R01、T-HEUR-004-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_004.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-005 主备计划生命周期

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-005` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「retain/switch/restart」并通过「惯性、阈值与可推翻性」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_005.py` |
| 建议测试 | `tests/spec_v3/test_heur_005.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_005.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `HEUR-004|STATE-006` |
| 下游消费者 | `HEUR-010|HEUR-014` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-005-N01、T-HEUR-005-B01、T-HEUR-005-I01、T-HEUR-005-P01、T-HEUR-005-R01、T-HEUR-005-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_005.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-006 定缺花色环境评估

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-006` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「suit environment」并通过「四家组合表」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_006.py` |
| 建议测试 | `tests/spec_v3/test_heur_006.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_006.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-005` |
| 下游消费者 | `HEUR-007` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-006-N01、T-HEUR-006-B01、T-HEUR-006-I01、T-HEUR-006-P01、T-HEUR-006-R01、T-HEUR-006-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_006.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-007 公开事件驱动的逐家方向更新

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-007` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「heuristic direction evidence」并通过「事件序列差分」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_007.py` |
| 建议测试 | `tests/spec_v3/test_heur_007.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_007.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `HEUR-006|STATE-005|MODEL-001` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-007-N01、T-HEUR-007-B01、T-HEUR-007-I01、T-HEUR-007-P01、T-HEUR-007-R01、T-HEUR-007-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_007.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-008 整场比分与剩余局效用调节

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-008` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「match utility modifiers」并通过「领先/落后/末局」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_008.py` |
| 建议测试 | `tests/spec_v3/test_heur_008.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_008.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-001|SCORE-006` |
| 下游消费者 | `HEUR-009|HEUR-010` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-008-N01、T-HEUR-008-B01、T-HEUR-008-I01、T-HEUR-008-P01、T-HEUR-008-R01、T-HEUR-008-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_008.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-009 先胡、做大和血战顺序效用

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-009` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「speed/value preference」并通过「第几胡收益场景」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_009.py` |
| 建议测试 | `tests/spec_v3/test_heur_009.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_009.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-002|ALGO-005|HEUR-008` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-009-N01、T-HEUR-009-B01、T-HEUR-009-I01、T-HEUR-009-P01、T-HEUR-009-R01、T-HEUR-009-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_009.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-010 多目标冲突复核

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-010` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「resolved preference」并通过「冲突权重与持续复核」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_010.py` |
| 建议测试 | `tests/spec_v3/test_heur_010.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_010.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-007|HEUR-005|HEUR-008` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-010-N01、T-HEUR-010-B01、T-HEUR-010-I01、T-HEUR-010-P01、T-HEUR-010-R01、T-HEUR-010-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_010.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-011 番型边际做牌价值

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-011` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「marginal value」并通过「封顶前后与互斥」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_011.py` |
| 建议测试 | `tests/spec_v3/test_heur_011.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_011.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-015|ALGO-002` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-011-N01、T-HEUR-011-B01、T-HEUR-011-I01、T-HEUR-011-P01、T-HEUR-011-R01、T-HEUR-011-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_011.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-012 碰牌策略评价

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-012` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「accept/pass score」并通过「速度、暴露、后续弃牌」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_012.py` |
| 建议测试 | `tests/spec_v3/test_heur_012.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_012.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-007|ALGO-002` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-012-N01、T-HEUR-012-B01、T-HEUR-012-I01、T-HEUR-012-P01、T-HEUR-012-R01、T-HEUR-012-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_012.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-013 杠牌策略评价

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-013` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「accept/pass score」并通过「明暗补杠风险」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_013.py` |
| 建议测试 | `tests/spec_v3/test_heur_013.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_013.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-008|RULE-009|SCORE-003|MODEL-002` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-013-N01、T-HEUR-013-B01、T-HEUR-013-I01、T-HEUR-013-P01、T-HEUR-013-R01、T-HEUR-013-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_013.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-014 出牌牌效与结构保留策略

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-014` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「strategic rank」并通过「清缺、听前/听后、拆搭」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_014.py` |
| 建议测试 | `tests/spec_v3/test_heur_014.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_014.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-003|ALGO-002|HEUR-005` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-014-N01、T-HEUR-014-B01、T-HEUR-014-I01、T-HEUR-014-P01、T-HEUR-014-R01、T-HEUR-014-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_014.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-015 防守偏好与安全牌选择

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-015` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「defensive rank」并通过「多家风险与安全牌」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_015.py` |
| 建议测试 | `tests/spec_v3/test_heur_015.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_015.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `MODEL-002|HEUR-022` |
| 下游消费者 | `HEUR-018` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-015-N01、T-HEUR-015-B01、T-HEUR-015-I01、T-HEUR-015-P01、T-HEUR-015-R01、T-HEUR-015-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_015.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-016 行为序列推断

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-016` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「behavioral cues」并通过「顺序变化与阶段对照」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_016.py` |
| 建议测试 | `tests/spec_v3/test_heur_016.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_016.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-005|HEUR-020` |
| 下游消费者 | `HEUR-018` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-016-N01、T-HEUR-016-B01、T-HEUR-016-I01、T-HEUR-016-P01、T-HEUR-016-R01、T-HEUR-016-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_016.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-017 思考节奏生成

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-017` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「planned think time」并通过「范围、复现、无真实 sleep 契约」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_017.py` |
| 建议测试 | `tests/spec_v3/test_heur_017.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_017.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-009|ALGO-008|HEUR-022` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-017-N01、T-HEUR-017-B01、T-HEUR-017-I01、T-HEUR-017-P01、T-HEUR-017-R01、T-HEUR-017-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_017.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-018 安全牌储备、扣牌与信息表达

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-018` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「retention preference」并通过「一阶与二阶行为场景」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_018.py` |
| 建议测试 | `tests/spec_v3/test_heur_018.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_018.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `HEUR-015|HEUR-016` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-018-N01、T-HEUR-018-B01、T-HEUR-018-I01、T-HEUR-018-P01、T-HEUR-018-R01、T-HEUR-018-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_018.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-019 Top-K 有限注意分配

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-019` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「attended items」并通过「mandatory 进入、容量与稳定性」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_019.py` |
| 建议测试 | `tests/spec_v3/test_heur_019.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_019.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-006|STATE-009` |
| 下游消费者 | `HEUR-021` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-019-N01、T-HEUR-019-B01、T-HEUR-019-I01、T-HEUR-019-P01、T-HEUR-019-R01、T-HEUR-019-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_019.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-020 有界记忆衰减与强化

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-020` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「memory snapshot」并通过「衰减、显著强化、不精确恢复」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_020.py` |
| 建议测试 | `tests/spec_v3/test_heur_020.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_020.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-006|STATE-005` |
| 下游消费者 | `HEUR-016|MODEL-001|MODEL-003` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-020-N01、T-HEUR-020-B01、T-HEUR-020-I01、T-HEUR-020-P01、T-HEUR-020-R01、T-HEUR-020-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_020.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-021 有限推演与满意停止

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-021` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「checked set/stop reason」并通过「深度、预算、停止条件」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_021.py` |
| 建议测试 | `tests/spec_v3/test_heur_021.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_021.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-006|ALGO-007|HEUR-019` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-021-N01、T-HEUR-021-B01、T-HEUR-021-I01、T-HEUR-021-P01、T-HEUR-021-R01、T-HEUR-021-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_021.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-022 人格、水平与情绪状态消费

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-022` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「decision modifiers」并通过「座位独立及方向效应」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_022.py` |
| 建议测试 | `tests/spec_v3/test_heur_022.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_022.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-006|STATE-010` |
| 下游消费者 | `HEUR-003|HEUR-004|HEUR-015|HEUR-017|HEUR-023` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-022-N01、T-HEUR-022-B01、T-HEUR-022-I01、T-HEUR-022-P01、T-HEUR-022-R01、T-HEUR-022-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_022.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## HEUR-023 有界近似选择与人类失误

| 字段 | 内容 |
|---|---|
| 单元ID | `HEUR-023` |
| 类型 | 启发式策略 |
| 目标 | 在冻结输入和版本下，独立产生「chosen legal action」并通过「合法性、误差上限、复现」验收。 |
| 建议主文件 | `players/humanlike/heuristics/heur_023.py` |
| 建议测试 | `tests/spec_v3/test_heur_023.py` |
| 测试向量 | `tests/spec_v3/vectors/heur_023.jsonl` |
| 现有代码候选 | `players/humanlike/policy.py, plan.py, candidates.py, evaluator.py, attention.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-006|ALGO-007|ALGO-008|HEUR-022` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 只从PlayerView、合法集和认知状态构建特征；落实规范约束、默认基线和参数范围。
2. 实现有限候选、软评分、风格/水平/阶段修正、满意停止与命名随机扰动。
3. 输出legal action、排序/区间和解释；用允许域、regret、方向效应及95% CI验收。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-HEUR-023-N01、T-HEUR-023-B01、T-HEUR-023-I01、T-HEUR-023-P01、T-HEUR-023-R01、T-HEUR-023-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_heur_023.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## MODEL-001 逐对手归一化方向/牌型假设

| 字段 | 内容 |
|---|---|
| 单元ID | `MODEL-001` |
| 类型 | 概率模型 |
| 目标 | 在冻结输入和版本下，独立产生「posterior hypotheses」并通过「每座独立、和为1、不确定性下限」验收。 |
| 建议主文件 | `players/humanlike/models/model_001.py` |
| 建议测试 | `tests/spec_v3/test_model_001.py` |
| 测试向量 | `tests/spec_v3/vectors/model_001.jsonl` |
| 现有代码候选 | `players/analysis/opponent_model.py, hand_predict.py, players/humanlike/belief.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-003|HEUR-020|STATE-005` |
| 下游消费者 | `HEUR-007|MODEL-002` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 冻结线上白名单特征和独立label schema；实现确定规则基线与不可用/OOD/超时回退。
2. 实现训练切分、泄漏扫描、损失、校准、版本/artifact加载和不确定性输出。
3. 在legal mask或策略边界内接入推理；报告Brier/log loss/ECE及卡内最低阈值。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-MODEL-001-N01、T-MODEL-001-B01、T-MODEL-001-I01、T-MODEL-001-P01、T-MODEL-001-R01、T-MODEL-001-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_model_001.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## MODEL-002 逐对手听牌/等待/损失风险模型

| 字段 | 内容 |
|---|---|
| 单元ID | `MODEL-002` |
| 类型 | 概率模型 |
| 目标 | 在冻结输入和版本下，独立产生「risk distribution」并通过「校准、分层与反例」验收。 |
| 建议主文件 | `players/humanlike/models/model_002.py` |
| 建议测试 | `tests/spec_v3/test_model_002.py` |
| 测试向量 | `tests/spec_v3/vectors/model_002.jsonl` |
| 现有代码候选 | `players/analysis/opponent_model.py, hand_predict.py, players/humanlike/belief.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `MODEL-001|ALGO-003|ALGO-004` |
| 下游消费者 | `HEUR-013|HEUR-015` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 冻结线上白名单特征和独立label schema；实现确定规则基线与不可用/OOD/超时回退。
2. 实现训练切分、泄漏扫描、损失、校准、版本/artifact加载和不确定性输出。
3. 在legal mask或策略边界内接入推理；报告Brier/log loss/ECE及卡内最低阈值。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-MODEL-002-N01、T-MODEL-002-B01、T-MODEL-002-I01、T-MODEL-002-P01、T-MODEL-002-R01、T-MODEL-002-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_model_002.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## MODEL-003 仅公开信息的跨局对手画像学习

| 字段 | 内容 |
|---|---|
| 单元ID | `MODEL-003` |
| 类型 | 概率模型 |
| 目标 | 在冻结输入和版本下，独立产生「next profile」并通过「冷启动、历史上限、复现」验收。 |
| 建议主文件 | `players/humanlike/models/model_003.py` |
| 建议测试 | `tests/spec_v3/test_model_003.py` |
| 测试向量 | `tests/spec_v3/vectors/model_003.jsonl` |
| 现有代码候选 | `players/analysis/opponent_model.py, hand_predict.py, players/humanlike/belief.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `HEUR-020|STATE-008|RULE-016` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 冻结线上白名单特征和独立label schema；实现确定规则基线与不可用/OOD/超时回退。
2. 实现训练切分、泄漏扫描、损失、校准、版本/artifact加载和不确定性输出。
3. 在legal mask或策略边界内接入推理；报告Brier/log loss/ECE及卡内最低阈值。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-MODEL-003-N01、T-MODEL-003-B01、T-MODEL-003-I01、T-MODEL-003-P01、T-MODEL-003-R01、T-MODEL-003-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_model_003.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## MODEL-004 可训练策略输入输出契约

| 字段 | 内容 |
|---|---|
| 单元ID | `MODEL-004` |
| 类型 | 可训练模型 |
| 目标 | 在冻结输入和版本下，独立产生「action distribution/value」并通过「mask 合法性和冻结推理」验收。 |
| 建议主文件 | `players/humanlike/models/model_004.py` |
| 建议测试 | `tests/spec_v3/test_model_004.py` |
| 测试向量 | `tests/spec_v3/vectors/model_004.jsonl` |
| 现有代码候选 | `players/analysis/opponent_model.py, hand_predict.py, players/humanlike/belief.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `TRAIN-002|TRAIN-003` |
| 下游消费者 | `MODEL-005` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 冻结线上白名单特征和独立label schema；实现确定规则基线与不可用/OOD/超时回退。
2. 实现训练切分、泄漏扫描、损失、校准、版本/artifact加载和不确定性输出。
3. 在legal mask或策略边界内接入推理；报告Brier/log loss/ECE及卡内最低阈值。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-MODEL-004-N01、T-MODEL-004-B01、T-MODEL-004-I01、T-MODEL-004-P01、T-MODEL-004-R01、T-MODEL-004-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_model_004.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## MODEL-005 训练模型产物版本、冻结和评估生命周期

| 字段 | 内容 |
|---|---|
| 单元ID | `MODEL-005` |
| 类型 | 可训练模型 |
| 目标 | 在冻结输入和版本下，独立产生「frozen model card/artifact」并通过「训练/评估隔离与版本拒绝（新增）」验收。 |
| 建议主文件 | `players/humanlike/models/model_005.py` |
| 建议测试 | `tests/spec_v3/test_model_005.py` |
| 测试向量 | `tests/spec_v3/vectors/model_005.jsonl` |
| 现有代码候选 | `players/analysis/opponent_model.py, hand_predict.py, players/humanlike/belief.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `MODEL-004|TRAIN-008|AUDIT-011` |
| 下游消费者 | `AUDIT-012` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 冻结线上白名单特征和独立label schema；实现确定规则基线与不可用/OOD/超时回退。
2. 实现训练切分、泄漏扫描、损失、校准、版本/artifact加载和不确定性输出。
3. 在legal mask或策略边界内接入推理；报告Brier/log loss/ECE及卡内最低阈值。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-MODEL-005-N01、T-MODEL-005-B01、T-MODEL-005-I01、T-MODEL-005-P01、T-MODEL-005-R01、T-MODEL-005-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_model_005.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## STATE-001 Match 配置冻结、玩家装配与整场控制

| 字段 | 内容 |
|---|---|
| 单元ID | `STATE-001` |
| 类型 | 状态管理 |
| 目标 | 在冻结输入和版本下，独立产生「immutable match context」并通过「seat/profile/round/seed 冻结」验收。 |
| 建议主文件 | `engine/state/state_001.py` |
| 建议测试 | `tests/spec_v3/test_state_001.py` |
| 测试向量 | `tests/spec_v3/vectors/state_001.jsonl` |
| 现有代码候选 | `engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-009|ALGO-011|STATE-010` |
| 下游消费者 | `HEUR-003|HEUR-008|SCORE-006|STATE-004|STATE-006|STATE-008|TRAIN-001` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。
2. 实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。
3. 通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-STATE-001-N01、T-STATE-001-B01、T-STATE-001-I01、T-STATE-001-P01、T-STATE-001-R01、T-STATE-001-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_state_001.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## STATE-002 权威 RoundState 存储与授权访问

| 字段 | 内容 |
|---|---|
| 单元ID | `STATE-002` |
| 类型 | 状态管理 |
| 目标 | 在冻结输入和版本下，独立产生「authoritative state」并通过「save/read ownership contract」验收。 |
| 建议主文件 | `engine/state/state_002.py` |
| 建议测试 | `tests/spec_v3/test_state_002.py` |
| 测试向量 | `tests/spec_v3/vectors/state_002.jsonl` |
| 现有代码候选 | `engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-004|STATE-011` |
| 下游消费者 | `ALGO-010|AUDIT-001|RULE-001|RULE-005|SCORE-001|STATE-003|STATE-007` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。
2. 实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。
3. 通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-STATE-002-N01、T-STATE-002-B01、T-STATE-002-I01、T-STATE-002-P01、T-STATE-002-R01、T-STATE-002-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_state_002.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## STATE-003 PlayerRoundState 手牌、副露、定缺与过胡状态

| 字段 | 内容 |
|---|---|
| 单元ID | `STATE-003` |
| 类型 | 状态管理 |
| 目标 | 在冻结输入和版本下，独立产生「player state」并通过「字段一致性与生命周期」验收。 |
| 建议主文件 | `engine/state/state_003.py` |
| 建议测试 | `tests/spec_v3/test_state_003.py` |
| 测试向量 | `tests/spec_v3/vectors/state_003.jsonl` |
| 现有代码候选 | `engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-002|ALGO-001` |
| 下游消费者 | `ALGO-002|RULE-002|RULE-003|RULE-004|RULE-007|RULE-008|RULE-010|RULE-011` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。
2. 实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。
3. 通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-STATE-003-N01、T-STATE-003-B01、T-STATE-003-I01、T-STATE-003-P01、T-STATE-003-R01、T-STATE-003-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_state_003.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## STATE-004 CONFIGURED→SETTLED 状态机

| 字段 | 内容 |
|---|---|
| 单元ID | `STATE-004` |
| 类型 | 状态管理 |
| 目标 | 在冻结输入和版本下，独立产生「next phase or error」并通过「全转换表及非法跳转」验收。 |
| 建议主文件 | `engine/state/state_004.py` |
| 建议测试 | `tests/spec_v3/test_state_004.py` |
| 测试向量 | `tests/spec_v3/vectors/state_004.jsonl` |
| 现有代码候选 | `engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-001` |
| 下游消费者 | `AUDIT-001|AUDIT-005|RULE-006|RULE-014|RULE-016|STATE-002|STATE-009|TRAIN-001` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。
2. 实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。
3. 通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-STATE-004-N01、T-STATE-004-B01、T-STATE-004-I01、T-STATE-004-P01、T-STATE-004-R01、T-STATE-004-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_state_004.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## STATE-005 不可变 PlayerView 状态载体

| 字段 | 内容 |
|---|---|
| 单元ID | `STATE-005` |
| 类型 | 状态管理 |
| 目标 | 在冻结输入和版本下，独立产生「frozen seat view」并通过「mutation rejection与schema」验收。 |
| 建议主文件 | `engine/state/state_005.py` |
| 建议测试 | `tests/spec_v3/test_state_005.py` |
| 测试向量 | `tests/spec_v3/vectors/state_005.jsonl` |
| 现有代码候选 | `engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-010` |
| 下游消费者 | `ALGO-003|HEUR-006|HEUR-007|HEUR-016|HEUR-020|MODEL-001|STATE-006|STATE-009|TRAIN-002` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。
2. 实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。
3. 通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-STATE-005-N01、T-STATE-005-B01、T-STATE-005-I01、T-STATE-005-P01、T-STATE-005-R01、T-STATE-005-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_state_005.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## STATE-006 策略侧认知运行态初始化与归档

| 字段 | 内容 |
|---|---|
| 单元ID | `STATE-006` |
| 类型 | 状态管理 |
| 目标 | 在冻结输入和版本下，独立产生「cognition state/snapshot」并通过「不进入权威 GameState」验收。 |
| 建议主文件 | `engine/state/state_006.py` |
| 建议测试 | `tests/spec_v3/test_state_006.py` |
| 测试向量 | `tests/spec_v3/vectors/state_006.jsonl` |
| 现有代码候选 | `engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-001|STATE-005|STATE-010` |
| 下游消费者 | `AUDIT-002|HEUR-005|HEUR-019|HEUR-020|HEUR-022|STATE-008` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。
2. 实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。
3. 通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-STATE-006-N01、T-STATE-006-B01、T-STATE-006-I01、T-STATE-006-P01、T-STATE-006-R01、T-STATE-006-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_state_006.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## STATE-007 存档 schema 持久化与迁移

| 字段 | 内容 |
|---|---|
| 单元ID | `STATE-007` |
| 类型 | 状态管理 |
| 目标 | 在冻结输入和版本下，独立产生「current state or error」并通过「真实/合成迁移夹具」验收。 |
| 建议主文件 | `engine/state/state_007.py` |
| 建议测试 | `tests/spec_v3/test_state_007.py` |
| 测试向量 | `tests/spec_v3/vectors/state_007.jsonl` |
| 现有代码候选 | `engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-002|ALGO-009` |
| 下游消费者 | `AUDIT-004|AUDIT-011` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。
2. 实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。
3. 通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-STATE-007-N01、T-STATE-007-B01、T-STATE-007-I01、T-STATE-007-P01、T-STATE-007-R01、T-STATE-007-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_state_007.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## STATE-008 跨局比分、认知和 episode 状态继承

| 字段 | 内容 |
|---|---|
| 单元ID | `STATE-008` |
| 类型 | 状态管理 |
| 目标 | 在冻结输入和版本下，独立产生「next-round context」并通过「允许/禁止继承字段」验收。 |
| 建议主文件 | `engine/state/state_008.py` |
| 建议测试 | `tests/spec_v3/test_state_008.py` |
| 测试向量 | `tests/spec_v3/vectors/state_008.jsonl` |
| 现有代码候选 | `engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-001|SCORE-006|STATE-006` |
| 下游消费者 | `MODEL-003` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。
2. 实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。
3. 通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-STATE-008-N01、T-STATE-008-B01、T-STATE-008-I01、T-STATE-008-P01、T-STATE-008-R01、T-STATE-008-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_state_008.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## STATE-009 决策请求上下文与生命周期

| 字段 | 内容 |
|---|---|
| 单元ID | `STATE-009` |
| 类型 | 状态管理 |
| 目标 | 在冻结输入和版本下，独立产生「request/result」并通过「超期、重复、错误 seat」验收。 |
| 建议主文件 | `engine/state/state_009.py` |
| 建议测试 | `tests/spec_v3/test_state_009.py` |
| 测试向量 | `tests/spec_v3/vectors/state_009.jsonl` |
| 现有代码候选 | `engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-004|STATE-005|RULE-001` |
| 下游消费者 | `ALGO-006|ALGO-008|AUDIT-002|HEUR-017|HEUR-019|STATE-012|TRAIN-003` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。
2. 实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。
3. 通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-STATE-009-N01、T-STATE-009-B01、T-STATE-009-I01、T-STATE-009-P01、T-STATE-009-R01、T-STATE-009-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_state_009.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## STATE-010 GP/RP/Profile 注册与生命周期

| 字段 | 内容 |
|---|---|
| 单元ID | `STATE-010` |
| 类型 | 状态管理 |
| 目标 | 在冻结输入和版本下，独立产生「owned parameter state」并通过「唯一性、逐座化、归档」验收。 |
| 建议主文件 | `engine/state/state_010.py` |
| 建议测试 | `tests/spec_v3/test_state_010.py` |
| 测试向量 | `tests/spec_v3/vectors/state_010.jsonl` |
| 现有代码候选 | `engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `无` |
| 下游消费者 | `ALGO-007|ALGO-009|ALGO-011|HEUR-003|HEUR-022|RULE-001|RULE-015|RULE-016|STATE-001|STATE-006|TRAIN-009` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。
2. 实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。
3. 通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-STATE-010-N01、T-STATE-010-B01、T-STATE-010-I01、T-STATE-010-P01、T-STATE-010-R01、T-STATE-010-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_state_010.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## STATE-011 牌墙构建、洗牌与初始发牌

| 字段 | 内容 |
|---|---|
| 单元ID | `STATE-011` |
| 类型 | 状态管理 |
| 目标 | 在冻结输入和版本下，独立产生「wall/hands」并通过「108张守恒与发牌数量（新增）」验收。 |
| 建议主文件 | `engine/state/state_011.py` |
| 建议测试 | `tests/spec_v3/test_state_011.py` |
| 测试向量 | `tests/spec_v3/vectors/state_011.jsonl` |
| 现有代码候选 | `engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-011` |
| 下游消费者 | `ALGO-001|ALGO-004|ALGO-005|RULE-002|RULE-006|RULE-008|RULE-012|STATE-002` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。
2. 实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。
3. 通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-STATE-011-N01、T-STATE-011-B01、T-STATE-011-I01、T-STATE-011-P01、T-STATE-011-R01、T-STATE-011-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_state_011.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## STATE-012 策略超时、崩溃与合法默认动作回退

| 字段 | 内容 |
|---|---|
| 单元ID | `STATE-012` |
| 类型 | 状态管理 |
| 目标 | 在冻结输入和版本下，独立产生「fallback result」并通过「超时/异常/唯一动作（新增）」验收。 |
| 建议主文件 | `engine/state/state_012.py` |
| 建议测试 | `tests/spec_v3/test_state_012.py` |
| 测试向量 | `tests/spec_v3/vectors/state_012.jsonl` |
| 现有代码候选 | `engine/state.py, engine/session.py, engine/orchestrator.py, players/humanlike/runtime.py, cognition.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-009|ALGO-006` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义不可变schema、版本、所有权和合法生命周期；为旧schema提供显式迁移器。
2. 实现唯一写入口、乐观版本检查、canonical序列化/hash及失败原子性。
3. 通过事件reducer接入runtime；验证快照/恢复、并发/超时及隐藏域隔离。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-STATE-012-N01、T-STATE-012-B01、T-STATE-012-I01、T-STATE-012-P01、T-STATE-012-R01、T-STATE-012-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_state_012.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## SCORE-001 分数账本分层与守恒

| 字段 | 内容 |
|---|---|
| 单元ID | `SCORE-001` |
| 类型 | 计分 |
| 目标 | 在冻结输入和版本下，独立产生「ledger/before/after」并通过「每事件零和及层级一致」验收。 |
| 建议主文件 | `engine/scoring/score_001.py` |
| 建议测试 | `tests/spec_v3/test_score_001.py` |
| 测试向量 | `tests/spec_v3/vectors/score_001.jsonl` |
| 现有代码候选 | `engine/fan.py, engine/score.py, engine/reward.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-002` |
| 下游消费者 | `AUDIT-005|SCORE-002|SCORE-003|SCORE-004|SCORE-006|TRAIN-005` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 实现番/事件事实到不可变`ScoreTransfer`的纯转换，逐条验证支付方与接收方。
2. 实现幂等账本写入、分层结算和累计排名；每事件、每层和本局断言`sum(deltas)==0`。
3. 接入规则提交后事件，完成重放、重复投递、封顶和终局结算证据。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-SCORE-001-N01、T-SCORE-001-B01、T-SCORE-001-I01、T-SCORE-001-P01、T-SCORE-001-R01、T-SCORE-001-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_score_001.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## SCORE-002 自摸、点炮与抢杠胡计分

| 字段 | 内容 |
|---|---|
| 单元ID | `SCORE-002` |
| 类型 | 计分 |
| 目标 | 在冻结输入和版本下，独立产生「hu transfers」并通过「三类胡及多人支付」验收。 |
| 建议主文件 | `engine/scoring/score_002.py` |
| 建议测试 | `tests/spec_v3/test_score_002.py` |
| 测试向量 | `tests/spec_v3/vectors/score_002.jsonl` |
| 现有代码候选 | `engine/fan.py, engine/score.py, engine/reward.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-010|RULE-015|SCORE-001` |
| 下游消费者 | `SCORE-005` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 实现番/事件事实到不可变`ScoreTransfer`的纯转换，逐条验证支付方与接收方。
2. 实现幂等账本写入、分层结算和累计排名；每事件、每层和本局断言`sum(deltas)==0`。
3. 接入规则提交后事件，完成重放、重复投递、封顶和终局结算证据。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-SCORE-002-N01、T-SCORE-002-B01、T-SCORE-002-I01、T-SCORE-002-P01、T-SCORE-002-R01、T-SCORE-002-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_score_002.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## SCORE-003 明/暗/补杠与呼叫转移计分

| 字段 | 内容 |
|---|---|
| 单元ID | `SCORE-003` |
| 类型 | 计分 |
| 目标 | 在冻结输入和版本下，独立产生「gang transfers」并通过「杠类型、抢杠与转移」验收。 |
| 建议主文件 | `engine/scoring/score_003.py` |
| 建议测试 | `tests/spec_v3/test_score_003.py` |
| 测试向量 | `tests/spec_v3/vectors/score_003.jsonl` |
| 现有代码候选 | `engine/fan.py, engine/score.py, engine/reward.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-008|RULE-009|SCORE-001` |
| 下游消费者 | `HEUR-013|SCORE-005` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 实现番/事件事实到不可变`ScoreTransfer`的纯转换，逐条验证支付方与接收方。
2. 实现幂等账本写入、分层结算和累计排名；每事件、每层和本局断言`sum(deltas)==0`。
3. 接入规则提交后事件，完成重放、重复投递、封顶和终局结算证据。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-SCORE-003-N01、T-SCORE-003-B01、T-SCORE-003-I01、T-SCORE-003-P01、T-SCORE-003-R01、T-SCORE-003-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_score_003.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## SCORE-004 花猪、查大叫与退税终局调整

| 字段 | 内容 |
|---|---|
| 单元ID | `SCORE-004` |
| 类型 | 计分 |
| 目标 | 在冻结输入和版本下，独立产生「adjustments」并通过「顺序、资格与边界」验收。 |
| 建议主文件 | `engine/scoring/score_004.py` |
| 建议测试 | `tests/spec_v3/test_score_004.py` |
| 测试向量 | `tests/spec_v3/vectors/score_004.jsonl` |
| 现有代码候选 | `engine/fan.py, engine/score.py, engine/reward.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-004|RULE-015|SCORE-001` |
| 下游消费者 | `SCORE-005` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 实现番/事件事实到不可变`ScoreTransfer`的纯转换，逐条验证支付方与接收方。
2. 实现幂等账本写入、分层结算和累计排名；每事件、每层和本局断言`sum(deltas)==0`。
3. 接入规则提交后事件，完成重放、重复投递、封顶和终局结算证据。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-SCORE-004-N01、T-SCORE-004-B01、T-SCORE-004-I01、T-SCORE-004-P01、T-SCORE-004-R01、T-SCORE-004-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_score_004.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## SCORE-005 封顶、互斥和转移结算顺序

| 字段 | 内容 |
|---|---|
| 单元ID | `SCORE-005` |
| 类型 | 计分 |
| 目标 | 在冻结输入和版本下，独立产生「final transfers」并通过「封顶前后次序」验收。 |
| 建议主文件 | `engine/scoring/score_005.py` |
| 建议测试 | `tests/spec_v3/test_score_005.py` |
| 测试向量 | `tests/spec_v3/vectors/score_005.jsonl` |
| 现有代码候选 | `engine/fan.py, engine/score.py, engine/reward.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-015|SCORE-002|SCORE-003|SCORE-004` |
| 下游消费者 | `SCORE-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 实现番/事件事实到不可变`ScoreTransfer`的纯转换，逐条验证支付方与接收方。
2. 实现幂等账本写入、分层结算和累计排名；每事件、每层和本局断言`sum(deltas)==0`。
3. 接入规则提交后事件，完成重放、重复投递、封顶和终局结算证据。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-SCORE-005-N01、T-SCORE-005-B01、T-SCORE-005-I01、T-SCORE-005-P01、T-SCORE-005-R01、T-SCORE-005-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_score_005.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## SCORE-006 单局总分、整场累计与排名

| 字段 | 内容 |
|---|---|
| 单元ID | `SCORE-006` |
| 类型 | 计分 |
| 目标 | 在冻结输入和版本下，独立产生「result/rank」并通过「守恒、并列及提前终止」验收。 |
| 建议主文件 | `engine/scoring/score_006.py` |
| 建议测试 | `tests/spec_v3/test_score_006.py` |
| 测试向量 | `tests/spec_v3/vectors/score_006.jsonl` |
| 现有代码候选 | `engine/fan.py, engine/score.py, engine/reward.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `SCORE-001|SCORE-005|STATE-001` |
| 下游消费者 | `HEUR-008|STATE-008` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 实现番/事件事实到不可变`ScoreTransfer`的纯转换，逐条验证支付方与接收方。
2. 实现幂等账本写入、分层结算和累计排名；每事件、每层和本局断言`sum(deltas)==0`。
3. 接入规则提交后事件，完成重放、重复投递、封顶和终局结算证据。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-SCORE-006-N01、T-SCORE-006-B01、T-SCORE-006-I01、T-SCORE-006-P01、T-SCORE-006-R01、T-SCORE-006-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_score_006.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## TRAIN-001 复用生产规则的训练包装

| 字段 | 内容 |
|---|---|
| 单元ID | `TRAIN-001` |
| 类型 | 训练接口 |
| 目标 | 在冻结输入和版本下，独立产生「training transition」并通过「与生产边界等价」验收。 |
| 建议主文件 | `training/train_001.py` |
| 建议测试 | `tests/spec_v3/test_train_001.py` |
| 测试向量 | `tests/spec_v3/vectors/train_001.jsonl` |
| 现有代码候选 | `training/env.py, action_codec_v2.py, observations_v2.py, reward_v2.py, runner.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-001|STATE-004|RULE-001` |
| 下游消费者 | `AUDIT-013|TRAIN-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 通过adapter调用同一生产Engine/Rule/State/Score，不复制环境转换或计分。
2. 实现观测/action mask/reward/seed/回放/快照/数据或评估职责，并隔离restricted truth。
3. 建立生产等价golden、确定回放、并行和性能测试，保存版本与artifact manifest。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-TRAIN-001-N01、T-TRAIN-001-B01、T-TRAIN-001-I01、T-TRAIN-001-P01、T-TRAIN-001-R01、T-TRAIN-001-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_train_001.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## TRAIN-002 Observation v2 编码

| 字段 | 内容 |
|---|---|
| 单元ID | `TRAIN-002` |
| 类型 | 训练接口 |
| 目标 | 在冻结输入和版本下，独立产生「fixed observation」并通过「schema、范围、泄漏」验收。 |
| 建议主文件 | `training/train_002.py` |
| 建议测试 | `tests/spec_v3/test_train_002.py` |
| 测试向量 | `tests/spec_v3/vectors/train_002.jsonl` |
| 现有代码候选 | `training/env.py, action_codec_v2.py, observations_v2.py, reward_v2.py, runner.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-005|ALGO-010` |
| 下游消费者 | `MODEL-004|TRAIN-005|TRAIN-006|TRAIN-008` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 通过adapter调用同一生产Engine/Rule/State/Score，不复制环境转换或计分。
2. 实现观测/action mask/reward/seed/回放/快照/数据或评估职责，并隔离restricted truth。
3. 建立生产等价golden、确定回放、并行和性能测试，保存版本与artifact manifest。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-TRAIN-002-N01、T-TRAIN-002-B01、T-TRAIN-002-I01、T-TRAIN-002-P01、T-TRAIN-002-R01、T-TRAIN-002-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_train_002.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## TRAIN-003 固定动作 codec 与 legal mask

| 字段 | 内容 |
|---|---|
| 单元ID | `TRAIN-003` |
| 类型 | 训练接口 |
| 目标 | 在冻结输入和版本下，独立产生「action ids/mask」并通过「encode/decode 双射」验收。 |
| 建议主文件 | `training/train_003.py` |
| 建议测试 | `tests/spec_v3/test_train_003.py` |
| 测试向量 | `tests/spec_v3/vectors/train_003.jsonl` |
| 现有代码候选 | `training/env.py, action_codec_v2.py, observations_v2.py, reward_v2.py, runner.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-001|STATE-009` |
| 下游消费者 | `MODEL-004|TRAIN-004|TRAIN-006|TRAIN-008` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 通过adapter调用同一生产Engine/Rule/State/Score，不复制环境转换或计分。
2. 实现观测/action mask/reward/seed/回放/快照/数据或评估职责，并隔离restricted truth。
3. 建立生产等价golden、确定回放、并行和性能测试，保存版本与artifact manifest。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-TRAIN-003-N01、T-TRAIN-003-B01、T-TRAIN-003-I01、T-TRAIN-003-P01、T-TRAIN-003-R01、T-TRAIN-003-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_train_003.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## TRAIN-004 非法训练动作处理契约

| 字段 | 内容 |
|---|---|
| 单元ID | `TRAIN-004` |
| 类型 | 训练接口 |
| 目标 | 在冻结输入和版本下，独立产生「raise/terminate/penalty」并通过「各模式精确结果」验收。 |
| 建议主文件 | `training/train_004.py` |
| 建议测试 | `tests/spec_v3/test_train_004.py` |
| 测试向量 | `tests/spec_v3/vectors/train_004.jsonl` |
| 现有代码候选 | `training/env.py, action_codec_v2.py, observations_v2.py, reward_v2.py, runner.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `TRAIN-003` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 通过adapter调用同一生产Engine/Rule/State/Score，不复制环境转换或计分。
2. 实现观测/action mask/reward/seed/回放/快照/数据或评估职责，并隔离restricted truth。
3. 建立生产等价golden、确定回放、并行和性能测试，保存版本与artifact manifest。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-TRAIN-004-N01、T-TRAIN-004-B01、T-TRAIN-004-I01、T-TRAIN-004-P01、T-TRAIN-004-R01、T-TRAIN-004-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_train_004.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## TRAIN-005 真实得分与可见势能奖励契约

| 字段 | 内容 |
|---|---|
| 单元ID | `TRAIN-005` |
| 类型 | 训练接口 |
| 目标 | 在冻结输入和版本下，独立产生「reward components」并通过「shaping 分离与默认关闭」验收。 |
| 建议主文件 | `training/train_005.py` |
| 建议测试 | `tests/spec_v3/test_train_005.py` |
| 测试向量 | `tests/spec_v3/vectors/train_005.jsonl` |
| 现有代码候选 | `training/env.py, action_codec_v2.py, observations_v2.py, reward_v2.py, runner.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `SCORE-001|TRAIN-002` |
| 下游消费者 | `TRAIN-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 通过adapter调用同一生产Engine/Rule/State/Score，不复制环境转换或计分。
2. 实现观测/action mask/reward/seed/回放/快照/数据或评估职责，并隔离restricted truth。
3. 建立生产等价golden、确定回放、并行和性能测试，保存版本与artifact manifest。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-TRAIN-005-N01、T-TRAIN-005-B01、T-TRAIN-005-I01、T-TRAIN-005-P01、T-TRAIN-005-R01、T-TRAIN-005-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_train_005.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## TRAIN-006 单 learner reset/step/mask/clone/restore

| 字段 | 内容 |
|---|---|
| 单元ID | `TRAIN-006` |
| 类型 | 训练接口 |
| 目标 | 在冻结输入和版本下，独立产生「transition/snapshot」并通过「round-trip restore」验收。 |
| 建议主文件 | `training/train_006.py` |
| 建议测试 | `tests/spec_v3/test_train_006.py` |
| 测试向量 | `tests/spec_v3/vectors/train_006.jsonl` |
| 现有代码候选 | `training/env.py, action_codec_v2.py, observations_v2.py, reward_v2.py, runner.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `TRAIN-001|TRAIN-002|TRAIN-003|TRAIN-005` |
| 下游消费者 | `AUDIT-009|TRAIN-007` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 通过adapter调用同一生产Engine/Rule/State/Score，不复制环境转换或计分。
2. 实现观测/action mask/reward/seed/回放/快照/数据或评估职责，并隔离restricted truth。
3. 建立生产等价golden、确定回放、并行和性能测试，保存版本与artifact manifest。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-TRAIN-006-N01、T-TRAIN-006-B01、T-TRAIN-006-I01、T-TRAIN-006-P01、T-TRAIN-006-R01、T-TRAIN-006-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_train_006.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## TRAIN-007 多玩家 ActionMap 与自博弈调度

| 字段 | 内容 |
|---|---|
| 单元ID | `TRAIN-007` |
| 类型 | 训练接口 |
| 目标 | 在冻结输入和版本下，独立产生「joint transition」并通过「同步动作与座位轮换」验收。 |
| 建议主文件 | `training/train_007.py` |
| 建议测试 | `tests/spec_v3/test_train_007.py` |
| 测试向量 | `tests/spec_v3/vectors/train_007.jsonl` |
| 现有代码候选 | `training/env.py, action_codec_v2.py, observations_v2.py, reward_v2.py, runner.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `TRAIN-006|RULE-013` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 通过adapter调用同一生产Engine/Rule/State/Score，不复制环境转换或计分。
2. 实现观测/action mask/reward/seed/回放/快照/数据或评估职责，并隔离restricted truth。
3. 建立生产等价golden、确定回放、并行和性能测试，保存版本与artifact manifest。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-TRAIN-007-N01、T-TRAIN-007-B01、T-TRAIN-007-I01、T-TRAIN-007-P01、T-TRAIN-007-R01、T-TRAIN-007-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_train_007.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## TRAIN-008 离线 BC 与回放 RL 数据消费

| 字段 | 内容 |
|---|---|
| 单元ID | `TRAIN-008` |
| 类型 | 训练接口 |
| 目标 | 在冻结输入和版本下，独立产生「batches/updates」并通过「split、mask、版本契约」验收。 |
| 建议主文件 | `training/train_008.py` |
| 建议测试 | `tests/spec_v3/test_train_008.py` |
| 测试向量 | `tests/spec_v3/vectors/train_008.jsonl` |
| 现有代码候选 | `training/env.py, action_codec_v2.py, observations_v2.py, reward_v2.py, runner.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `TRAIN-002|TRAIN-003|AUDIT-014` |
| 下游消费者 | `MODEL-005` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 通过adapter调用同一生产Engine/Rule/State/Score，不复制环境转换或计分。
2. 实现观测/action mask/reward/seed/回放/快照/数据或评估职责，并隔离restricted truth。
3. 建立生产等价golden、确定回放、并行和性能测试，保存版本与artifact manifest。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-TRAIN-008-N01、T-TRAIN-008-B01、T-TRAIN-008-I01、T-TRAIN-008-P01、T-TRAIN-008-R01、T-TRAIN-008-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_train_008.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## TRAIN-009 房规、profile 与行为域随机化

| 字段 | 内容 |
|---|---|
| 单元ID | `TRAIN-009` |
| 类型 | 训练接口 |
| 目标 | 在冻结输入和版本下，独立产生「sampled domain」并通过「可复现及越界拒绝」验收。 |
| 建议主文件 | `training/train_009.py` |
| 建议测试 | `tests/spec_v3/test_train_009.py` |
| 测试向量 | `tests/spec_v3/vectors/train_009.jsonl` |
| 现有代码候选 | `training/env.py, action_codec_v2.py, observations_v2.py, reward_v2.py, runner.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-010|ALGO-011` |
| 下游消费者 | `AUDIT-006` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 通过adapter调用同一生产Engine/Rule/State/Score，不复制环境转换或计分。
2. 实现观测/action mask/reward/seed/回放/快照/数据或评估职责，并隔离restricted truth。
3. 建立生产等价golden、确定回放、并行和性能测试，保存版本与artifact manifest。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-TRAIN-009-N01、T-TRAIN-009-B01、T-TRAIN-009-I01、T-TRAIN-009-P01、T-TRAIN-009-R01、T-TRAIN-009-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_train_009.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-001 全原子规则事件日志

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-001` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「public payload/private refs」并通过「事件覆盖与历史不可变」验收。 |
| 建议主文件 | `engine/audit/audit_001.py` |
| 建议测试 | `tests/spec_v3/test_audit_001.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_001.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-004|STATE-002` |
| 下游消费者 | `AUDIT-003|AUDIT-014` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-001-N01、T-AUDIT-001-B01、T-AUDIT-001-I01、T-AUDIT-001-P01、T-AUDIT-001-R01、T-AUDIT-001-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_001.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-002 AI 决策解释日志

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-002` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「view/memory/plan/scores/action trace」并通过「字段完整与敏感边界」验收。 |
| 建议主文件 | `engine/audit/audit_002.py` |
| 建议测试 | `tests/spec_v3/test_audit_002.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_002.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-009|STATE-006|ALGO-007` |
| 下游消费者 | `AUDIT-003|AUDIT-014` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-002-N01、T-AUDIT-002-B01、T-AUDIT-002-I01、T-AUDIT-002-P01、T-AUDIT-002-R01、T-AUDIT-002-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_002.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-003 canonical hash 链与篡改检测

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-003` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「verified/rejected」并通过「篡改、截断、重排」验收。 |
| 建议主文件 | `engine/audit/audit_003.py` |
| 建议测试 | `tests/spec_v3/test_audit_003.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_003.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `AUDIT-001|AUDIT-002` |
| 下游消费者 | `AUDIT-004` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-003-N01、T-AUDIT-003-B01、T-AUDIT-003-I01、T-AUDIT-003-P01、T-AUDIT-003-R01、T-AUDIT-003-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_003.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-004 同配置/seed/事件的确定性回放

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-004` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「replay comparison」并通过「state/action/score 一致」验收。 |
| 建议主文件 | `engine/audit/audit_004.py` |
| 建议测试 | `tests/spec_v3/test_audit_004.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_004.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `AUDIT-003|ALGO-008|STATE-007` |
| 下游消费者 | `AUDIT-009` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-004-N01、T-AUDIT-004-B01、T-AUDIT-004-I01、T-AUDIT-004-P01、T-AUDIT-004-R01、T-AUDIT-004-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_004.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-005 每事件强制不变量执行

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-005` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「pass or explicit failure」并通过「守恒、actor、legal、view、账本」验收。 |
| 建议主文件 | `engine/audit/audit_005.py` |
| 建议测试 | `tests/spec_v3/test_audit_005.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_005.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `STATE-004|ALGO-001|RULE-001|SCORE-001` |
| 下游消费者 | `AUDIT-006|AUDIT-007` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-005-N01、T-AUDIT-005-B01、T-AUDIT-005-I01、T-AUDIT-005-P01、T-AUDIT-005-R01、T-AUDIT-005-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_005.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-006 直接规则与接口测试证据门禁

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-006` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「coverage status」并通过「测试正文与断言语义复核」验收。 |
| 建议主文件 | `engine/audit/audit_006.py` |
| 建议测试 | `tests/spec_v3/test_audit_006.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_006.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `AUDIT-005` |
| 下游消费者 | `AUDIT-008|AUDIT-011` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-006-N01、T-AUDIT-006-B01、T-AUDIT-006-I01、T-AUDIT-006-P01、T-AUDIT-006-R01、T-AUDIT-006-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_006.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-007 属性式生成、缩减与不变量证据

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-007` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「minimized failures/report」并通过「状态空间与缩减可复核」验收。 |
| 建议主文件 | `engine/audit/audit_007.py` |
| 建议测试 | `tests/spec_v3/test_audit_007.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_007.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `AUDIT-005|ALGO-011` |
| 下游消费者 | `发布门禁` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-007-N01、T-AUDIT-007-B01、T-AUDIT-007-I01、T-AUDIT-007-P01、T-AUDIT-007-R01、T-AUDIT-007-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_007.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-008 锁定来源逐章 golden-case 对照

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-008` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「per-clause result」并通过「0–18章及profile允许集」验收。 |
| 建议主文件 | `engine/audit/audit_008.py` |
| 建议测试 | `tests/spec_v3/test_audit_008.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_008.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `AUDIT-006|AUDIT-010` |
| 下游消费者 | `发布门禁` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-008-N01、T-AUDIT-008-B01、T-AUDIT-008-I01、T-AUDIT-008-P01、T-AUDIT-008-R01、T-AUDIT-008-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_008.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-009 工程与行为回归指标

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-009` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「metric report/CI」并通过「合法、复现、性能、风格」验收。 |
| 建议主文件 | `engine/audit/audit_009.py` |
| 建议测试 | `tests/spec_v3/test_audit_009.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_009.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `AUDIT-004|TRAIN-006` |
| 下游消费者 | `AUDIT-012` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-009-N01、T-AUDIT-009-B01、T-AUDIT-009-I01、T-AUDIT-009-P01、T-AUDIT-009-R01、T-AUDIT-009-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_009.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-010 来源→参数→实现→测试全链追踪

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-010` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「trace matrix」并通过「断链、版本和公式元数据」验收。 |
| 建议主文件 | `engine/audit/audit_010.py` |
| 建议测试 | `tests/spec_v3/test_audit_010.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_010.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `无` |
| 下游消费者 | `AUDIT-008|AUDIT-011` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-010-N01、T-AUDIT-010-B01、T-AUDIT-010-I01、T-AUDIT-010-P01、T-AUDIT-010-R01、T-AUDIT-010-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_010.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-011 版本、迁移与发布物完整性

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-011` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「manifest/gate result」并通过「schema/test/migration/hash/tag」验收。 |
| 建议主文件 | `engine/audit/audit_011.py` |
| 建议测试 | `tests/spec_v3/test_audit_011.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_011.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `ALGO-009|STATE-007|AUDIT-006|AUDIT-010` |
| 下游消费者 | `MODEL-005` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-011-N01、T-AUDIT-011-B01、T-AUDIT-011-I01、T-AUDIT-011-P01、T-AUDIT-011-R01、T-AUDIT-011-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_011.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-012 强度、真人相似和学习效果外部评价

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-012` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「statistics/CI」并通过「E5、盲测与 Not Evaluated」验收。 |
| 建议主文件 | `engine/audit/audit_012.py` |
| 建议测试 | `tests/spec_v3/test_audit_012.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_012.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `AUDIT-009|AUDIT-014|MODEL-005` |
| 下游消费者 | `发布门禁` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-012-N01、T-AUDIT-012-B01、T-AUDIT-012-I01、T-AUDIT-012-P01、T-AUDIT-012-R01、T-AUDIT-012-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_012.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-013 模块依赖、接口与信息流架构契约

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-013` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「violations/report」并通过「禁止反向依赖和 oracle 泄漏」验收。 |
| 建议主文件 | `engine/audit/audit_013.py` |
| 建议测试 | `tests/spec_v3/test_audit_013.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_013.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `RULE-016|ALGO-010|TRAIN-001` |
| 下游消费者 | `发布门禁` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-013-N01、T-AUDIT-013-B01、T-AUDIT-013-I01、T-AUDIT-013-P01、T-AUDIT-013-R01、T-AUDIT-013-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_013.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。

## AUDIT-014 证据数据保留、脱敏与新鲜度管理

| 字段 | 内容 |
|---|---|
| 单元ID | `AUDIT-014` |
| 类型 | 日志审计 |
| 目标 | 在冻结输入和版本下，独立产生「retained manifest」并通过「current-run/report-only/敏感数据」验收。 |
| 建议主文件 | `engine/audit/audit_014.py` |
| 建议测试 | `tests/spec_v3/test_audit_014.py` |
| 测试向量 | `tests/spec_v3/vectors/audit_014.jsonl` |
| 现有代码候选 | `engine/audit.py, engine/replay.py, engine/invariants.py, players/humanlike/audit_replay.py`；仅作迁移盘点，不代表符合规格 |
| 上游依赖 | `AUDIT-001|AUDIT-002` |
| 下游消费者 | `AUDIT-012|TRAIN-008` |
| 规格来源 | 对应Approved单元规格；目录来源/GP/RP以锁定目录本行为准 |
| 当前状态 | Not Implemented / Not Evaluated（须以差距审计更新） |

### 实现步骤

1. 定义canonical输入、检查ID、finding/error、证据引用、权限和保留schema。
2. 实现确定检查、首错定位、全部可继续finding、签名/hash和append-only生命周期。
3. 接入真实运行/测试/发布产物；验证hard失败不被抵消、truth不回流和证据新鲜度。
4. 对照现有候选代码决定`reuse/adapt/rewrite/retire`，禁止双权威；以适配器保持旧调用方并逐步切换。
5. 回填代码符号、commit、配置/公式/schema版本及迁移偏差；任何行为差异先更新Approved规格。

### 测试要求

- 必须实现Approved测试合同：T-AUDIT-014-N01、T-AUDIT-014-B01、T-AUDIT-014-I01、T-AUDIT-014-P01、T-AUDIT-014-R01、T-AUDIT-014-X01。
- 正常、边界、非法、性质/统计、重复性及生产入口集成全部适用；计划命令：`python -m pytest -q tests/spec_v3/test_audit_014.py`。
- 直接行为证据至少E3；P0/跨模块路径至少E4；外部效果声明按适用项E5。测试不得复制生产规则oracle。

### 完成定义

- 主文件通过稳定门面接入且无禁止依赖；上游契约已通过，下游schema/version兼容。
- 六类测试全部Passed或有经批准且非hard gate的N/A；无永久skip、宽松xfail或隐藏信息泄漏。
- 代码、测试、运行证据占位均有可核查路径/hash；性能达到单元规格；现有旧写路径已移除或明确deprecated截止版本。
- 未满足任一项时保持Partial/Not Evaluated，不得仅因文件、类或测试名存在标Done。
# 3.0.1 任务卡路径解释（适用于全部96卡）

所有“文件建议/代码入口候选”均为逻辑归属而非强制物理package。与既有`.py`模块同名时，实际入口必须落在既有模块，或落在不遮蔽导入的`spec_v3`子命名空间；报告必须给出`unit_id → importable symbol`映射。只有Approved迁移ADR才可把单文件模块迁为package。
