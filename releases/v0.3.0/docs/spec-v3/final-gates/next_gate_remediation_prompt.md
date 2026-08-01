# 下一条修复任务提示词

执行`PRE-DEV-FINAL-GATE-001-R1`，只为B1-B（STATE-001、STATE-011、STATE-004）建立并审批可编码设计，不修改业务代码或测试断言。

逐单元从Locked规格和当前代码提取具体current/required差异，分别生成原子semantic_delta、test_delta、evidence_delta；明确输入、输出、错误码、原子性、边界、可见性、接口影响、依赖、代码位置、客观test oracle、E4/E5要求和AC-01至AC-14绑定。不得读取SUPERSEDED泛化SEM-PARAMETER作为要求。

同时生成一个仅修正派生权威引用的supersession说明，明确OPTION-J2及CONTRACTS/PARAMS 2.0已批准，并将仍写PENDING的`B1-A_effective_spec_overlay.md`和`B1-A_version_matrix.csv`列为历史/被覆盖引用；不得修改Locked语义。

输出B1-B设计审查、三类Delta、接口影响、验收矩阵、审批表及更新后的authority map。审批前结论只能是REVIEW_REQUIRED；不得授权编码、不得标记AUDITED。完成并获用户批准后重新执行PRE-DEV-FINAL-GATE-001。
