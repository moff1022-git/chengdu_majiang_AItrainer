# Spec v3 未解决问题清单（最终锁定审计）

| 字段 | 内容 |
|---|---|
| 日期 | 2026-07-29 |
| Critical Open | 0 |
| High Open | 0 |
| Medium Open | 1 |
| Low Open | 1 |
| 锁定状态 | **Locked — SPEC-V3-3.0.0** |

## 1. 已关闭问题

| issue | 原严重度 | 状态 | 关闭证据 |
|---|---|---|---|
| CDI-001 状态枚举冲突 | High | Closed | STATE-004唯一RoundPhase；事件与STATE-001 Match状态分层 |
| CDI-002 证据等级冲突 | High | Closed | 正式E0—E5；legacy EV隔离并保守迁移 |
| CDI-003 核心文档未批准 | High | Closed | 总规范、开发三件套、细化测试三件套、审计标准/清单及模板均Approved |
| CDI-004 参数范围不可机检 | Medium | Closed | 60行参数注册表；source/consumer/test端点全部通过 |
| CDI-006 双重性能阈值 | Medium | Closed | 指南移除第二套数值；AC-12只读Approved单元规格 |

## 2. 当前开放问题

### CDI-005 — 计划证据当前无法支持AUDITED

| 字段 | 内容 |
|---|---|
| 严重度 | Medium / Implementation readiness |
| 状态 | Open |
| 缺口 | 96个建议入口、`tests/spec_v3/`、JSONL golden、current-run日志及E4/E5产物尚未建立 |
| 影响 | AC-02～14大部分保持Not Evaluated；任何单元均不能依据新模板标AUDITED |
| 对规范锁定 | 不阻断；锁定的是已批准契约，不是实现完成声明 |
| 处理 | 锁定后执行M0差距审计，再按DAG实现、测试和保留证据 |

### CDI-007 — 治理sink与单元消费者字段混用

| 字段 | 内容 |
|---|---|
| 严重度 | Low |
| 状态 | Open |
| 证据 | AUDIT-007/008/012/013下游消费者写`发布门禁`，不是稳定单元ID |
| 对规范锁定 | 不阻断；治理sink语义明确，单元端点检查不把它当单元 |
| 处理 | catalog下一小版本增加`governance_consumers`或稳定`GATE-RELEASE` ID，不改变96单元数量 |

## 3. 后续顺序

1. M0 inventory已完成；依据96行矩阵编写并批准M1首批实施规格/任务批次。
2. M1起逐单元关闭CDI-005，形成E2/E3/E4证据，不能用旧pytest基线替代。
3. CDI-007随catalog下一小版本处理；因规范已Locked，必须走版本化解锁/变更/复审/重锁。
