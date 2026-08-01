# Spec v3 Mac 接续核验记录

| 字段 | 内容 |
|---|---|
| 文档 ID | SV3-REVIEW-20260729-001 |
| 状态 | Passed |
| 日期 | 2026-07-29 |
| 范围 | 只读环境、输入保护与接续基线核验 |
| 适用规则 | `docs/spec-v3/WORKING_RULES.md` |

## 1. 结论

Mac 接续门禁通过。OneDrive 中 `docs/spec-v3/` 的交接、来源清单、证据矩阵和模板均可读；两份锁定来源的 SHA-256 与交接基线完全一致。Mac Python 环境可用，但本次未运行测试，因此不改变任何证据等级或 `current-run` 状态。

## 2. 环境与 Git

| 项 | 结果 |
|---|---|
| 仓库 | `/Users/moff/onedrive/chatgpt/chengdu_majiang_AItrainer` |
| OS | macOS 26.5.2 (25F84), arm64 |
| Git branch | `main` |
| Git HEAD | `423326ecf6e602f9c1c3392dd2a844b1e61ce9b3` |
| Python | `.venv-macos/bin/python` → Python 3.12.13 |
| pytest | 9.1.1（仅查询版本，未运行测试） |
| 工作树 | 已有未提交改动；本次未 reset/checkout/clean |

## 3. 锁定来源保护

| 路径 | 实测 SHA-256 | 结果 |
|---|---|---|
| `成都麻将AI人类化决策规则_v1.md` | `6cbb4d4465abfd947b6cf7f1783db99408089d4e1646849a3afe674114267992` | 与 SRC-LOCK-001 一致 |
| `成都麻将AI训练模拟器程序实现规范_v2.0.0.md` | `9bc4d4ea5278e09ae34a1efb5edfb3cbc295752ecf6b3ebe89b348210d670135` | 与 SRC-LOCK-002 一致 |

本次未修改两份锁定来源。

## 4. Spec v3 关键输入身份

| 路径 | SHA-256 |
|---|---|
| `docs/spec-v3/WORKING_RULES.md` | `57dfd4385e40ef6acdc3ed7a34a3cc24b24b169368fb75fddedac922bf74fb9f` |
| `docs/spec-v3/01-audit-gap/audit_evidence_matrix.csv` | `0dd4d358b61b2be57c7505c4488e03220d1e56f114a2ebcd96a9d7ec63535048` |
| `docs/spec-v3/01-audit-gap/audit_evidence_matrix.md` | `4de487bee722a1f018a5014b32b3518ac76c7e8d0798123c5d63a82c2dc6a8c8` |
| `docs/spec-v3/01-audit-gap/evidence_summary.md` | `7faa45ccb4ba2973bd39328efa4d562aa5286d3d7dc93e5bbf27949e6dcf04b0` |

CSV 可解析为 96 行 legacy audit rows，其中 P0 为 33 行，与交接摘要一致。

## 5. 证据边界

- 未运行 pytest、coverage、批跑、回放或性能测试。
- 不将 Python/pytest 可用性当作 E3/E4 证据。
- 矩阵中的历史运行结论继续保持 `report-only`。
- 未修改程序代码、测试、配置或证据矩阵。

## 6. 下一步

交接队列第 1 项已完成。立即下一步为人工复核 33 个 P0 legacy rows，输出 P0 证据修订清单；运行测试仍需明确授权。
