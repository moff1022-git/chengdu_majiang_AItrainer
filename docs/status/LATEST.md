# 进度快照

> 2026-07-26 — **版本管理规则落地 · 应用 v0.2.0**

## 本轮

| 项 | 说明 |
|----|------|
| 目标 | 建立版本管理规则，并更新文档与程序 |
| 规则 | [`docs/VERSIONING.md`](../VERSIONING.md)（SemVer · 多版本线分离 · 发版清单） |
| 单一源 | [`version.py`](../../version.py) → **`APP_VERSION = 0.2.0`** |
| 程序 | CLI `--version`；主窗/大厅/座位窗展示 `v0.2.0`；打包读版本写 plist |
| 流程 | `docs/DEVELOPMENT.md` 已链到 VERSIONING |
| 测试 | `tests/test_version.py` |

## 当前版本基线

| 线 | 值 |
|----|-----|
| **应用** | **0.2.0** |
| 存档 schema | 4 |
| 存档 format | 1 |
| 座位协议 | 1 |

## 发版口令（摘要）

1. 改 `version.py`  
2. `docs/changelog.md` 增加 `## X.Y.Z`  
3. 更新本文件  
4. `git tag vX.Y.Z`  
5. 打包脚本  

## 下一步

| 序 | 动作 | 建议触发语 |
|----|------|------------|
| 1 | 可选：`git tag v0.2.0` 并 push | `打 tag v0.2.0` |
| 2 | 用当前版本重建 mac 包 | `重新打包` |
| 3 | 双击 .app 完整验收 | 目视打包版 |
