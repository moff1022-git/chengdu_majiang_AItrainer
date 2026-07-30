# Spec v3 审计报告模板

| 字段 | 填写值 |
|---|---|
| 文档状态 | Locked Template |
| report_id | `TODO(AUDIT-REPORT-...)` |
| 审计范围 | 单元/批次/发布候选 |
| scope_hash | TODO |
| 审计日期 | TODO UTC |
| producer / lead reviewer | TODO / TODO |
| 总结论 | NOT_EVALUATED |

## 1. 结论先行

结论：`NOT_EVALUATED / IN_REVIEW / FAILED / BLOCKED / AUDITED / AUDITED_E5 / STALE / REVOKED`。

适用版本、平台、数据和期限：TODO。不得写超出scope的“全部通过”。

主要通过依据：TODO。主要失败/限制：TODO。

## 2. 范围与排除

| 项目 | 内容 |
|---|---|
| unit_ids | TODO |
| code_commit / dirty diff hash | TODO |
| rule/parameter/config/schema/model版本 | TODO |
| 平台/数据/场景 | TODO |
| 明确排除项 | TODO；排除不能包含AC-01～14 hard项 |

## 3. 单元结论摘要

| unit_id | evidence package | highest E | AC passed/14 | Critical/High open | final status | expires |
|---|---|---:|---:|---:|---|---|
| TODO | TODO | E0 | 0/14 | TODO | NOT_EVALUATED | TODO |

## 4. E0—E5分布

| 等级 | 单元数 | unit_ids | 备注 |
|---|---:|---|---|
| E0 | TODO | TODO | TODO |
| E1 | TODO | TODO | TODO |
| E2 | TODO | TODO | TODO |
| E3 | TODO | TODO | TODO |
| E4 | TODO | TODO | TODO |
| E5 | TODO | TODO | TODO |

等级按最高累计证据统计；不得把E3测试数量加到E4重复计数。

## 5. AC-01～AC-14汇总

| check_id | Passed | Failed | Not Evaluated | 主要finding/evidence |
|---|---:|---:|---:|---|
| AC-01 规格完整 | TODO | TODO | TODO | TODO |
| AC-02 非占位实现 | TODO | TODO | TODO | TODO |
| AC-03 代码入口 | TODO | TODO | TODO | TODO |
| AC-04 实际调用方 | TODO | TODO | TODO | TODO |
| AC-05 参数绑定 | TODO | TODO | TODO | TODO |
| AC-06 状态写回 | TODO | TODO | TODO | TODO |
| AC-07 单元测试 | TODO | TODO | TODO | TODO |
| AC-08 边界测试 | TODO | TODO | TODO | TODO |
| AC-09 集成测试 | TODO | TODO | TODO | TODO |
| AC-10 运行日志 | TODO | TODO | TODO | TODO |
| AC-11 追踪关系 | TODO | TODO | TODO | TODO |
| AC-12 性能 | TODO | TODO | TODO | TODO |
| AC-13 隐藏信息隔离 | TODO | TODO | TODO | TODO |
| AC-14 确定性或统计指标 | TODO | TODO | TODO | TODO |

任一单元任一AC失败，该单元不得AUDITED；报告总通过率不能抵消。

## 6. 八项AUDITED条件复核

| # | 条件 | status | 证据/说明 |
|---:|---|---|---|
| 1 | 规格已锁定 | Not Evaluated | TODO |
| 2 | 非框架/非占位实现 | Not Evaluated | TODO |
| 3 | 必需测试通过 | Not Evaluated | TODO |
| 4 | 完整流程实际调用 | Not Evaluated | TODO |
| 5 | 运行输入输出证据 | Not Evaluated | TODO |
| 6 | 规则和参数可追踪 | Not Evaluated | TODO |
| 7 | 无高严重度缺陷 | Not Evaluated | TODO |
| 8 | 所有指标达标 | Not Evaluated | TODO |

## 7. 测试与运行证据

| run/test suite | command | env manifest | passed/failed/skipped | artifact/hash | freshness |
|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO |

## 8. 性能、确定性、统计、校准与泄漏

| 领域 | 适用单元 | 阈值 | 实测/CI | 失败单元 | 结论 |
|---|---|---|---|---|---|
| 性能 | TODO | TODO | TODO | TODO | TODO |
| 同seed回放 | TODO | 逐字段一致 | TODO | TODO | TODO |
| HEUR统计 | TODO | Approved允许域/CI | TODO | TODO | TODO |
| MODEL校准 | TODO | Brier/log loss/ECE等 | TODO | TODO | TODO |
| 隐藏信息隔离 | 96 | 泄漏0 | TODO | TODO | TODO |

## 9. 追踪与架构

来源→参数→单元→代码→测试→运行完整率：TODO。断链：TODO。

禁止依赖、第二规则引擎、oracle回流、全局RNG、直接状态写入扫描结果：TODO。

## 10. 缺陷清单

| finding_id | unit_id | severity | 描述 | status | owner/期限 | 证据 |
|---|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO | TODO |

## 11. 决议、限制与下一步

- AUDITED单元：TODO
- FAILED/BLOCKED/NOT_EVALUATED单元：TODO
- E5声明范围：TODO或无
- 必须修复：TODO
- 建议改进：TODO
- 重审触发和到期日：TODO

## 12. 签名与hash链

| 角色 | 身份 | 决议 | 时间UTC | 签名/record hash |
|---|---|---|---|---|
| producer | TODO | TODO | TODO | TODO |
| technical reviewer | TODO | TODO | TODO | TODO |
| final reviewer | TODO | TODO | TODO | TODO |

`prev_report_hash=TODO`；`report_hash=TODO`；保留manifest=TODO。更正必须生成新revision并supersede，禁止覆盖本报告。
