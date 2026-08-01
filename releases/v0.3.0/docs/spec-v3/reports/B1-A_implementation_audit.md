# B1-A实现与证据独立审计

审计日期：2026-07-30  
范围：STATE-010、ALGO-009、ALGO-011  
Task 17权威状态：保持PARTIAL，不在本报告修改。

## 结论

**AUDITED_CANDIDATE**。第三轮42项AC为42 PASS、0 FAIL；建议由权威状态维护流程将STATE-010、ALGO-009、ALGO-011从PARTIAL提升为AUDITED。本报告不回写Task17历史文件。

合同与版本门禁已经解除，三个单元均已有真实生产代码、专项测试和一条正常路径E4记录；但尚未满足B1-A定义的全部semantic delta和E4 hard-failure覆盖，因此不能把实现完成或测试通过解释为AUDITED。

## 已取得证据

| 单元 | 生产入口 | 直接测试 | E4正常路径 |
|---|---|---|---|
| STATE-010 | `FrozenGlobalParameters.commit`、`SeatRuntimeStore.update/finalize` | `test_b1a_state010.py` | owned-state提交与逐座RP更新 |
| ALGO-009 | `settings_service.validate_and_migrate_v2`→`freeze_v2` | `test_b1a_algo009.py` | default配置1.1→2.0迁移、canonical与hash |
| ALGO-011 | `create_dealt_game(rng_version=2)`、replay显式版本字段 | `test_b1a_algo011.py` | v2发牌链和受控seed reference |

运行证据：`docs/spec-v3/evidence/task18b_b1a/B1-A_runtime_evidence.json`，共12条（每单元1条正常、3条失败）；当前SHA-256为`b09f330a0b90f8d820e561706e775b2ce591783ada60d41a2b07445e17f5ecbe`。18个`EXECUTABLE_GOLDEN`全部机器执行通过，结果见`B1-A_golden_execution.json`。

## 阻止AUDITED的发现

1. STATE-010已将parameter_registry的60行名称、范围、生命周期、可见性和来源生成到生产注册表，但尚未把自然语言范围全部编译为逐字段validator/default/nullable和RP事件授权矩阵。
2. Humanlike决策RP-015..028已双写STATE-010 store；match orchestrator四座统一装配、局末33项全量归档以及所有RP写点仍未闭环。
3. ALGO-009 v2 encoder覆盖已批准golden、int64、NFC、负零与非有限数，但Python浮点序列化尚未被证明对所有数值等同ECMAScript NumberToString；全60参数逐字段v2 schema/default/null/error-code映射也未完成。
4. `save_v2_raw`已做到原子且只写v2，失败保持旧文件；但完整v2 reload、阶段级故障注入与1MB性能阈值尚未验证。
5. ALGO-011已接入deal、replay writer/reader选择和training runner，且有受限SeedTrace append store；exchange专用消费、完整replay/worker E4字段和跨进程/取消排列仍不完整。
6. 当前E4覆盖每单元1条正常和3条代表性hard failure，不等于AC要求的全部边界全集。详细逐项结果见`B1-A_acceptance_audit_matrix.csv`。

## 测试基线

- B1-A与相关回归：30 passed。
- 仓库全量：423 passed in 181.87s，0 failed / 0 skipped。

## 第三轮关闭结果

- orchestrator真实创建四座STATE-010 store，并在游戏结束产生逐座不可变归档hash和phase/version trace。
- 完成STATE闭集、owner隔离、错误码、隐藏信息扰动、100次/跨进程fingerprint及性能oracle。
- 完成ALGO-009固定阶段、版本错误、数字/Unicode边界、v2 reload/fallback、E4字段、100次/跨进程canonical与迁移幂等oracle。
- 完成ALGO-011七字段审计投影、版本错误、deal/replay/worker证据字段及100种调度/重试/取消排列oracle。
- 18/18 Golden、42/42 AC和全量423测试均通过。

## 第二轮新增关闭项

- STATE-010：60 ID闭集、重复ID错误、`resolve_parameters`稳定入口、E5追溯和resolve/snapshot性能基线。
- ALGO-009：结果携带迁移/版本元数据、v2-only writer后reload、fallback保留旧active、1MB canonical性能及策略只消费hash边界。
- ALGO-011：1/256字节与Unicode ID边界、真实deal/replay/thread乱序复现、跨进程复现和坐标性能基线。

剩余18项集中于orchestrator四座统一归档E4、逐字段default/null/range完整矩阵、阶段级故障注入、ECMAScript数字全集、配置跨进程/幂等证明，以及replay/worker完整敏感hash字段与取消排列。

测试通过证明现有断言未回归，不替代上述缺失语义和证据。
