# Spec v3 单元证据包模板

| 字段 | 填写值 |
|---|---|
| 文档状态 | Locked Template |
| evidence_package_id | `TODO(EVP-<UNIT>-<VERSION>)` |
| unit_id | `TODO` |
| audit_scope_hash | `TODO` |
| package_status | Not Evaluated |
| highest_evidence_level | E0 |
| producer / reviewer | `TODO / TODO` |
| created / expires UTC | `TODO / TODO` |

## 1. 审计scope

| scope字段 | 值 | 证据/hash |
|---|---|---|
| code_commit / dirty status | TODO | TODO |
| rule / parameter / implementation version | TODO | TODO |
| config / schema version | TODO | TODO |
| model / feature / label version | TODO或N/A | TODO |
| OS / arch / Python / dependency lock | TODO | TODO |
| platform / dataset / scenario范围 | TODO | TODO |
| game_id / seed manifest | TODO | TODO |

scope任一字段未知时不得AUDITED。dirty worktree必须记录diff hash和文件清单，不能只写commit。

## 2. E0—E5累计证据索引

| 等级 | 状态 | evidence_ids | 累计前置是否满足 | reviewer结论 |
|---|---|---|---|---|
| E0 | Not Evaluated | — | — | TODO |
| E1 | Not Evaluated | TODO | TODO | TODO |
| E2 | Not Evaluated | TODO | TODO | TODO |
| E3 | Not Evaluated | TODO | TODO | TODO |
| E4 | Not Evaluated | TODO | TODO | TODO |
| E5 | N/A或Not Evaluated | TODO | TODO | TODO |

## 3. AC-01～AC-14证据表

| check_id | 检查项 | status | evidence_level | freshness | 路径/符号/nodeid | 命令/运行ID | artifact_sha256 | finding_ids |
|---|---|---|---:|---|---|---|---|---|
| AC-01 | 规格完整 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-02 | 非占位实现 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-03 | 代码入口 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-04 | 实际调用方 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-05 | 参数绑定 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-06 | 状态写回 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-07 | 单元测试 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-08 | 边界测试 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-09 | 集成测试 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-10 | 运行日志 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-11 | 追踪关系 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-12 | 性能 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-13 | 隐藏信息隔离 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |
| AC-14 | 确定性或统计指标 | Not Evaluated | E0 | — | TODO | TODO | TODO | TODO |

## 4. 规格与追踪证据

- Locked目录行及hash：TODO
- Approved单元规格标题/版本/hash：TODO
- Approved父测试合同及细化TC测试ID：TODO
- 来源规则/章节：TODO
- GP/RP绑定或批准的“无直接参数”：TODO
- 代码入口→调用方→测试→运行追踪路径：TODO

## 5. 非占位实现与代码入口

| 项目 | 路径:行/符号 | 检查方法 | 结论 |
|---|---|---|---|
| 主要实现 | TODO | 阅读正文及复杂度/分支 | TODO |
| 稳定入口 | TODO | import/API契约 | TODO |
| 生产调用方 | TODO | 静态调用图+运行trace | TODO |
| 禁止依赖扫描 | TODO | 命令与规则 | TODO |
| placeholder扫描 | TODO | pass/TODO/fixed return/mock/test branch | TODO |

## 6. 参数与状态证据

| 参数/状态字段 | 来源 | loader/binder符号 | 运行值hash | 写回事件/无副作用证明 | 结论 |
|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO |

## 7. 测试结果

| test_id/nodeid | 类型 | seed | cases | passed/failed/skipped | duration | JUnit/artifact | sha256 |
|---|---|---|---:|---|---:|---|---|
| TODO | unit/boundary/integration/... | TODO | TODO | TODO | TODO | TODO | TODO |

任何hard测试skipped/N/A/xfail均令AUDITED失败。失败反例、缩减结果和全部不利统计必须保留。

## 8. 完整流程运行证据

| run_id | 生产入口 | 输入hash | output hash | before/after state hash | event范围 | score/ledger hash | log/hash-chain | result |
|---|---|---|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

附实际调用trace，必须显示该单元代码入口被执行；仅构造对象或import不算调用。

## 9. 性能、泄漏与指标

| 项目 | 环境/数据/样本 | 指标和阈值 | 实测/95% CI | 功能oracle | 结论 | artifact |
|---|---|---|---|---|---|---|
| 性能P50/P95/P99/吞吐/内存 | TODO | TODO | TODO | TODO | TODO | TODO |
| 隐藏truth成对投毒 | TODO | 泄漏0 | TODO | TODO | TODO | TODO |
| 同seed完整回放 | TODO | 逐字段一致 | TODO | TODO | TODO | TODO |
| HEUR统计或MODEL校准等 | TODO/N/A | Approved阈值 | TODO | TODO | TODO | TODO |

## 10. 缺陷、例外和风险

| finding_id | severity | 描述 | 影响检查 | 状态 | owner/期限 | 处置证据 |
|---|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO | TODO |

High/Critical未关闭时不得AUDITED。N/A/例外必须列批准人、理由、范围和到期日；AC-01～14不得N/A。

## 11. AUDITED判定

- [ ] E1～E4累计前置全部满足；适用外部声明E5满足。
- [ ] AC-01～AC-14全部Passed。
- [ ] 八项AUDITED条件全部满足。
- [ ] 无开放High/Critical；Medium处置符合标准。
- [ ] 证据新鲜、hash有效、隐私分类与保留策略已执行。
- [ ] producer与final reviewer不是同一人。

最终状态：`NOT_EVALUATED`。最终等级：`E0`。理由/签名：TODO。

## 12. 证据manifest JSON骨架

```json
{
  "evidence_package_id": "TODO",
  "unit_id": "TODO",
  "audit_scope": {},
  "audit_scope_hash": "TODO",
  "highest_evidence_level": "E0",
  "checks": [],
  "tests": [],
  "runs": [],
  "metrics": [],
  "findings": [],
  "artifact_hashes": {},
  "final_status": "NOT_EVALUATED",
  "producer": "TODO",
  "reviewer": "TODO",
  "signed_at_utc": null,
  "record_hash": "TODO"
}
```
