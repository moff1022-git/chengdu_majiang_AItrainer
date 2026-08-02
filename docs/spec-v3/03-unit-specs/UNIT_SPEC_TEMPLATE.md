# SV3-Uxxxx 功能单元规格：<单元名称>

| 字段 | 内容 |
|---|---|
| 单元 ID | SV3-Uxxxx |
| 状态 | Draft |
| 版本 | 0.1 |
| Owner | 未指定 |
| method_class | `deterministic_rule` / `deterministic_algorithm` / `humanlike_heuristic` / `trainable_model` |
| criticality | hard / high / normal |
| 首次分配日期 | YYYY-MM-DD |
| 取代/废弃关系 | 无 |

## 1. 单一职责

用一句可验证的话描述本单元唯一主要职责。若包含跨 method class 或可独立判定的多个职责，必须拆分单元或原子断言。

## 2. 来源与版本

| 来源 ID | 锁定文件路径 | 条款/行锚点 | 来源版本 | SHA-256 | 解释 |
|---|---|---|---|---|---|
| SRC-LOCK-xxx | `<path>` | `<section>` | `<version>` | `<hash>` | `<原文语义的释义，不大段复制>` |

不得修改锁定来源。歧义必须建立 `SV3-DEC-xxxx`，不得静默推断。

## 3. Legacy 审计映射

| legacy row | 映射关系 | 保留内容 | 需拆分/纠正内容 |
|---|---|---|---|
| `<audit row>` | full / partial / overlaps | `<内容>` | `<内容或“未找到”>` |

legacy 96 行不是本单元边界的权威来源。

## 4. 范围

### 4.1 In Scope

- <使用稳定断言 ID 描述>

### 4.2 Out of Scope

- <明确排除项及其目标单元 ID；未知时写“未找到”>

## 5. 输入、状态与输出

| 类型 | 名称 | Schema/范围 | 权威来源 | 错误行为 |
|---|---|---|---|---|
| 输入 | `<name>` | `<type/range>` | `<path::symbol>` | `<explicit failure>` |
| 状态 | `<name>` | `<lifecycle>` | `<path::symbol>` | `<explicit failure>` |
| 输出 | `<name>` | `<contract>` | `<path::symbol>` | `<explicit failure>` |

## 6. 原子断言

| 断言 ID | 要求 | method_class | 前置条件 | 可观测结果 | criticality |
|---|---|---|---|---|---|
| SV3-Uxxxx-A01 | `<单一可判定要求>` | `<one class>` | `<条件>` | `<结果>` | hard/high/normal |

每个断言只能得到 Passed、Failed、Not Evaluated 或 N/A-with-approval。hard 断言不得平均抵消。

## 7. 算法或规则流程

按 method class 单独描述，不得把以下类别混合成同一实现声明：

### 7.1 确定性规则

<若不适用，写“不适用”；若未找到，写“未找到”。>

### 7.2 确定性算法

<若不适用，写“不适用”；若未找到，写“未找到”。>

### 7.3 人类化启发式

<若不适用，写“不适用”；若未找到，写“未找到”。>

### 7.4 可训练模型

<若不适用，写“不适用”；若未找到，写“未找到”。>

## 8. 配置与版本兼容

| 配置/版本 | 允许值 | 默认值 | 迁移规则 | 未知值行为 | 证据 |
|---|---|---|---|---|---|
| `<id>` | `<range>` | `<value>` | `<rule>` | reject / explicit fallback | `<path::symbol>` |

## 9. 证据计划与当前证据

| 证据 ID | 断言 ID | 等级 | 文件路径 | 符号/测试/命令 | 结果 | 新鲜度 | 限制 |
|---|---|---|---|---|---|---|---|
| SV3-EV-xxxxxx | SV3-Uxxxx-A01 | E0～E5 | `<path 或“未找到”>` | `<symbol/test/command 或“未找到”>` | Passed/Failed/Not Evaluated | current-run/retained-artifact/report-only/stale-cache | `<限制>` |

类、接口、占位函数、测试名称或配置键单独只能作为E0；E1必须同时具备Locked目录、Approved单元规格和Approved父测试合同。完整等级语义只引用审计标准。

## 10. 测试规格

| 测试 ID | 断言 ID | 层级 | 输入/夹具 | 预期 | 保留产物 |
|---|---|---|---|---|---|
| SV3-Uxxxx-T01 | SV3-Uxxxx-A01 | unit/contract/integration/system/effect | `<fixture>` | `<exact assertion>` | `<artifact path>` |

必须定义反例、边界、版本冲突和失败路径；效果类断言还必须定义样本、分母、阈值和不确定性。

## 11. 审计与验收

- 验收状态：Not Evaluated。
- 最低证据等级：<Ex>。
- 必须保留的运行环境：<OS/Python/commit/config hashes>。
- 必须保留的结果：<命令、原始输出、摘要、哈希>。
- 未找到的证据：<逐项列出，不得推测>。

## 12. 追踪关系

| 方向 | ID/路径 | 关系 |
|---|---|---|
| 上游来源 | `<SRC/条款>` | derives-from |
| 相邻单元 | `<SV3-Uxxxx>` | depends-on / conflicts-with / supersedes |
| 实现候选 | `<path::symbol>` | implemented-by-candidate |
| 测试候选 | `<path::test>` | verified-by-candidate |
| 缺口 | `<SV3-GAP-xxxx>` | blocked-by |
| 决策 | `<SV3-DEC-xxxx>` | clarified-by |

## 13. 风险、缺失与开放问题

| 项 | 状态 | 证据 | 所需决策/输入 |
|---|---|---|---|
| `<问题>` | Open/Blocked | `<路径或“未找到”>` | `<内容>` |

## 14. 变更记录

| 日期 | 版本 | 变更 | 授权/证据 |
|---|---|---|---|
| YYYY-MM-DD | 0.1 | 初稿 | `<task/user decision>` |
