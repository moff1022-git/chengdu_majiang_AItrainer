# B1-A SHA-256术语复核

## 规范表述

统一使用：**SHA-256，32字节，序列化为64个小写十六进制字符。** “64位SHA-256”会被理解为64 bit，错误缩短摘要；“64位小写hex”也没有说明64是字符数。

## 发现

| 位置 | 原文字 |
|---|---|
| `docs/spec-v3/03-unit-specs/deterministic_algorithm_scoring_specs.md:598` | `hash为64小写hex；参数均在闭区间；输出同时含accepted、formula_version、input_hash、output_hash；失败时result=null且error_code稳定。` |
| `docs/spec-v3/contracts/common_contracts.md:29` | `\| `Sha256Hex` \| 64位小写hex \| 必填；无默认 \| hex chars \| 对canonical bytes求SHA-256 \|` |
| `docs/spec-v3/semantic-completion/first_batch_acceptance_matrix.csv:17` | `ALGO-009,AC-ALGO-009-02,非占位生产实现,SEM-ALGO-009-01\|SEM-ALGO-009-02\|SEM-ALGO-009-03\|SEM-ALGO-009-04\|SEM-ALGO-009-05\|SEM-ALGO-009-06\|SEM-ALGO-009-07\|SEM-ALGO-009-08,TEST-ALGO-009-01\|TEST-ALGO-009-02\|TEST-ALGO-009-03\|TEST-ALGO-009-04,EVIDENCE-ALGO-009-01\|EVIDENCE-ALGO-009-02,"给定current配置输出FrozenConfig及64位小写hash；NaN输入result=null,error_code=NON_FINITE",planned current-run artifact,PLANNED,等待规格门禁后实现/执行` |
| `docs/spec-v3/semantic-completion/semantic_completion_matrix.csv:23` | `ALGO-009,配置类型/范围/版本校验、迁移与 canonical hash,ALGO,PARTIAL,PATH-SEMANTIC-COMPLETION,VALID,15,14,1,0.9333,0,0,0,0,0,1,0,0,0,0,true,true,true,true,true,COMPATIBLE_EXTENSION,SDELTA-ALGO-009-02\|SDELTA-ALGO-009-03\|SDELTA-ALGO-009-04\|SDELTA-ALGO-009-05\|SDELTA-ALGO-009-06\|SDELTA-ALGO-009-07,STATE-010,B1-A,false,Task18B-R1: BLOCKED_BY_SPEC_DECISION；见reviews/B1-A_design_review.md,"purpose:### 1. 输入向量和字段含义 raw JSON；schema uint16；GP/RP registry范围；migration path。区间均闭区间，枚举外值非法；来源锚点继承 [locked_unit_catalog.md](../0` |

Locked单元规格和Task16 Frozen契约没有直接修改，其措辞更正进入合同v2提案。非Locked的`first_batch_acceptance_matrix.csv`已更正为“SHA-256，32字节，序列化为64个小写十六进制字符”；`semantic_completion_matrix.csv`中的内容是Locked来源摘录，由`B1-A_effective_spec_overlay.md`覆盖解释，保留历史盘点文件不改。
