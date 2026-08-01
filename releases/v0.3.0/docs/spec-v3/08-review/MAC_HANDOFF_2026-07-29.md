# Spec v3 Mac 接续交接

| 字段 | 内容 |
|---|---|
| 文档 ID | SV3-HANDOFF-20260729-001 |
| 状态 | Mac continuation verified |
| 日期 | 2026-07-29 |
| 当前阶段 | 只分析和生成文档；未经明确授权不修改程序代码 |

## 1. 已完成

- 已按用户要求冻结 `UNIT-CATALOG 1.0.0`，产出正式 Markdown/CSV 目录及无环依赖图；Locked 仅冻结单元边界，不表示详细单元规格已 Approved 或代码已验收。
- 已完成 96 个 legacy rows 的边界审查、old→new 迁移图和 96 个建议新单元目录；交付见 `docs/spec-v3/02-unit-catalog/`。
- Mac 只读环境与哈希复核已通过，记录见 `docs/spec-v3/08-review/MAC_CONTINUATION_CHECK_2026-07-29.md`。
- 建立 `docs/spec-v3/` 九个目录及统一规则 `WORKING_RULES.md`。
- 完成来源清单、版本关系、逐文件 SHA-256、日志 tree SHA-256、缺失项和单元模板。
- 将当前 96 个 legacy audit rows 转换为证据差距矩阵。
- 矩阵逐项包含 AU ID、名称、目标、规则章节、GP/RP、声称文件、实际符号、调用方、测试、运行证据、状态、缺口、阻塞和优先级。
- 对所有引用符号和测试名称做存在性校验，并排除静态识别出的占位实现。

## 2. 当前权威交付物

- `docs/spec-v3/00-source-inventory/source_inventory.md`
- `docs/spec-v3/00-source-inventory/authoritative_file_manifest.md`
- `docs/spec-v3/00-source-inventory/log_file_manifest.md`
- `docs/spec-v3/03-unit-specs/UNIT_SPEC_TEMPLATE.md`
- `docs/spec-v3/01-audit-gap/audit_evidence_matrix.md`
- `docs/spec-v3/01-audit-gap/audit_evidence_matrix.csv`
- `docs/spec-v3/01-audit-gap/evidence_summary.md`

`docs/spec-v3/00-source-inventory/source_file_manifest.md` 是首次生成时受输出截断影响的废弃清单，不得引用；权威清单为 `authoritative_file_manifest.md`。

## 3. 当前证据结论

| 维度 | 结果 |
|---|---|
| legacy rows | 96 |
| 状态 | 21 INTEGRATED / 12 TESTED / 60 PARTIAL / 2 SCAFFOLDED / 1 SPECIFIED |
| 证据 | E4 21 / E3 71 / E2 1 / E1 2 / E0 1 / E5 0 |
| 原33/61/2 | 未直接沿用；已按严格证据门槛重判 |
| current-run | 未执行；Mac `.venv-macos` 已确认可用，但测试运行尚未授权 |
| report-only | F0028-2～6、F0030 与总审计中的历史运行声明 |
| 输入保护 | 来源清单中 225 个权威输入哈希复核全部一致 |

## 4. 锁定文档保护

- `成都麻将AI人类化决策规则_v1.md`  
  SHA-256：`6cbb4d4465abfd947b6cf7f1783db99408089d4e1646849a3afe674114267992`
- `成都麻将AI训练模拟器程序实现规范_v2.0.0.md`  
  SHA-256：`9bc4d4ea5278e09ae34a1efb5edfb3cbc295752ecf6b3ebe89b348210d670135`

两份文档禁止修改。

## 5. Mac 开工读序

1. `docs/status/LATEST.md`
2. 本文件
3. `docs/spec-v3/WORKING_RULES.md`
4. `docs/spec-v3/00-source-inventory/source_inventory.md`
5. `docs/spec-v3/01-audit-gap/evidence_summary.md`
6. 需要逐项核对时读取 Markdown 矩阵或 CSV

## 6. Mac 环境核验

在仓库根目录执行只读检查：

```bash
pwd
git status --short --branch
shasum -a 256 成都麻将AI人类化决策规则_v1.md 成都麻将AI训练模拟器程序实现规范_v2.0.0.md
find docs/spec-v3 -maxdepth 3 -type f | sort
```

随后检查可用 Python，不要假定 `.venv-macos/` 一定完整：

```bash
test -x .venv-macos/bin/python && .venv-macos/bin/python --version
test -x .venv/bin/python && .venv/bin/python --version
```

未经用户明确要求，不要自动安装依赖、修改代码、清理 Git 工作区或运行全量测试。

## 7. 未完成与风险

- 当前矩阵是 legacy row 粒度，不承认 96 行已经原子化或边界正确。
- E5 为 0：历史 `/tmp/f0028_*` 原始批跑、性能和 audit corpus 未入库。
- coverage、独立机器可读 Schema、真人评估数据均未找到。
- 静态调用扫描可能漏掉动态分派；“未找到”不得改写为推测实现。
- 工作区有大量既有脏文件；不要 reset、checkout、clean 或批量格式化。

## 8. 立即下一步与完整队列

| 序 | 动作 | 产出 | 依赖 | 建议触发语 |
|---|---|---|---|---|
| 1 | Mac 只读环境与哈希复核（已完成） | `MAC_CONTINUATION_CHECK_2026-07-29.md` | OneDrive 同步完成 | 无 |
| 2 | 人工复核 P0 单元（立即下一步） | P0 证据修订清单 | 当前矩阵 | `人工复核P0审计单元` |
| 3 | 恢复 current-run 证据 | pytest/coverage/命令/环境/哈希 | 可用 Mac Python 环境；运行授权 | `在Mac上重跑并保存审计证据` |
| 4 | 复合 legacy rows 边界审查（已完成 Draft） | `02-unit-catalog/` 三份交付 | 用户明确授权 | 无 |
| 5 | 冻结 v3 正式单元目录（已完成） | `UNIT-CATALOG 1.0.0` Markdown/CSV/依赖图 | 边界审查 | 无 |
| 6 | 按 P0 依赖序编写详细单元规格与测试规格（立即下一步） | `03-unit-specs/`、`05-test-spec/` | UNIT-CATALOG 1.0.0 | `编写首批v3单元规格` |
