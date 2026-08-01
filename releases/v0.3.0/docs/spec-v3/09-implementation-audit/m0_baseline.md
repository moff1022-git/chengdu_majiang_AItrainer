# Spec v3 M0 基线记录

| 字段 | 内容 |
|---|---|
| 日期 | 2026-07-29 |
| 规范版本 | SPEC-V3-3.0.0 |
| lock_set_sha256 | `6df28948e37dd95c57c9060c6e7e7d28a8243b86e8844a133ab33b6641c1e4ec` |
| Git HEAD | `423326ecf6e602f9c1c3392dd2a844b1e61ce9b3` |
| Python | `.venv-macos/bin/python`；Python 3.12.13 |
| pytest | 9.1.1 |
| 工作树 | Dirty；保留用户既有修改，不能仅用HEAD复原本轮代码状态 |
| 代码快照 | `m0_code_file_manifest.csv`逐文件SHA-256 |

## 测试基线

命令：

```bash
PYTHONPYCACHEPREFIX=/tmp/spec_v3_m0_pycache .venv-macos/bin/python -m pytest -q -rs
```

结果：`357 passed, 1 skipped in 29.34s`。

Skip：`tests/test_f0013_dirty_update.py:122`，原因为macOS Tk在`Tk()`构造时可能终止进程；测试自身声明由纯helper及人工/子进程GUI验收覆盖。

本结果只用于迁移回归比较。`tests/spec_v3/`不存在，故不能给任何v3单元E3。

## 代表性冻结样本

| 样本 | SHA-256 |
|---|---|
| `docs/spec-v3/09-implementation-audit/baseline_fixtures/dealt_state.json` | `f8905d8bdc9931f222b3278dc06048d72bb0283e26b92738637f8605d258a541` |
| `docs/spec-v3/09-implementation-audit/baseline_fixtures/player_view_seat0.json` | `73dee6bfefbce3b09dffe4e976f78ee824ca7751872a1e0ee80e258cade40f68` |
| `docs/spec-v3/09-implementation-audit/baseline_fixtures/domain_event.json` | `3f6e45d7fc641006a1c77f4db95961d8f48c214f058cab041202197037dea7e4` |
| `docs/spec-v3/09-implementation-audit/baseline_fixtures/score_transfer.json` | `0c9887cfeb8f31723e4ebb4894b940b2e0f5fb18bf8308f3eaa89a5b4dbcf0ee` |


样本由当前生产模块生成，用于影子比较，不作为锁定规范oracle。若M1改变命名随机域或schema，应保留本baseline并以版本化差异报告解释，不得覆盖原文件。

## 工作树限制

审计开始时已存在与本任务无关的修改和未跟踪文件，包括`protocols/subprocess_transport.py`、`tests/test_subprocess_compat.py`及其他文档/环境目录。本轮未回滚或覆盖它们。候选代码的可复核状态以`m0_code_file_manifest.csv`为准，而非仅以Git HEAD为准。
