# 进度快照

> 2026-07-28 — **Git 与测试门禁已恢复；下一步可进入 F0028-1**

## 当前状态

| 项 | 状态 |
|----|------|
| 应用版本 | 0.2.1（`version.py`） |
| 规格主线 | M01–M11 已 Done；F0001–F0027 已实现；F0028 人类化 AI v2 已 Approved |
| F0028 输入 | 两份根目录新规范已校验 hash 并完成代码差距分析 |
| 接管审计 | 已完成并二次复核，见 `docs/status/PROJECT_TAKEOVER_AUDIT_2026-07-28.md` |
| Git | **本地基线已重建**：`main` 根提交 `90e7174`；损坏 `.git` 已备份；远端零 refs/非法 HEAD，未推送 |
| 编译 / CLI | `compileall` 通过；`main.py --version` = 0.2.1 |
| 测试门禁 | **全量 279 passed / 1 skipped（27.83s）**；无失败、无解释器 Abort |
| 冲突副本 | 排除 `.venv` / `backup` 后仍扫到 52 个 `*Moff的Mac Studio*` 文件 |
| 大目录 | `.venv` 415 MB、backup 350 MB、logs 316 MB、releases 309 MB、dist 274 MB、build 18 MB |

## 已确认问题

1. 远端 GitHub 当前无可恢复 refs，尚未将新本地基线推送至远端，历史 `v0.2.1` tag 也无法验证。
2. OneDrive 冲突副本仍保留在本地，但新 `.gitignore` 已将其与 venv/logs/build/dist/backup 排除出 Git 基线。

## 本轮已完成

- 用户确认 F0028；状态 `Review` → `Approved`，本轮未写业务代码。
- 锁定六切片渐进实施、`humanlike_v2` 选配 profile、实体牌 ID 必做和中性中等水平首个 profile。
- 新增并已批准 `docs/features/F0028_humanlike_ai_v2_implementation_plan.md`，将新规范映射为 6 个渐进切片。
- 完成 Docs-First 一致性补齐：`PLAN.md`、`DOC_CODE_BASELINE.md`、F0026/F0027 正文状态、status 文档链接已同步。
- 读取 GitHub 远端并临时 clone；确认远端零 refs/非法 HEAD，不可作为恢复源。
- 盘点本地冲突 index：728 个条目中 675 个 blob 缺失；原历史无法完整恢复。
- 将损坏 `.git` 移至 `backup/git-metadata-corrupt-2026-07-28/`，以当前工作树重建本地 `main`/index。
- 恢复正常 `.gitignore`，新基线收录 744 个源文件/文档/资源，排除本地产物与冲突副本。
- 创建本地 `main` 恢复根提交 `90e7174`；`git fsck --full` 无损坏 ref/对象错误（仅有未引用 blob）。
- 恢复后 `compileall` 通过；安全测试主体 278 passed / 1 failed / 1 deselected，唯一失败仍是 F0020 旧断言。
- 更新 M09 历史测试为 F0020 当前行为：允许 2H/3H，拒绝 4H。
- 为 F0013 Tk GUI 用例增加 macOS 收集期 skip 门禁，避免 `tk.Tk()` 在当前环境直接 Abort 整个 pytest 进程。
- 验收：`compileall` 通过；不带排除条件的全量 `pytest -q` = 279 passed / 1 skipped（27.83s）。
- 确认规则文件 SHA-256 与实现规范绑定值一致；记录实现规范 hash。
- 对照现有 `engine/`、`protocols/`、`players/analysis/`、`training/` 和 replay，明确复用边界与缺口。
- 锁定“不重建 `src/`、不复制引擎、新 profile 先选配、保留 2/3/4 人”的兼容方向。
- 按强制读序恢复了跨机基线，复阅接管审计、流程规范和系统设计。
- 以只读命令复核 Git refs / fsck / remote，确认 P0 损坏仍在。
- 复跑安全测试主体，结果与上轮一致：278 passed / 1 failed / 1 deselected。
- 复核冲突副本和大目录数量；未删除文件，未修改业务代码、测试或 Git 元数据。

## 下一步完整队列

| 序 | 动作 | 产出 / 依赖 | 建议触发语 |
|----|------|-------------|------------|
| 1 | 实施 F0028-1（立即下一步） | GP/RP 强类型、验证、hash 和追踪矩阵 | `实现 F0028-1 配置与参数追踪基座` |
| 2 | 确认并推送新远端基线 | 将本地 `main` 推送到当前零 refs 远端；是外部状态变更，需单独确认 | `将恢复后的 main 推送到 origin` |
| 4 | 依次实施 F0028-2–6 | 实体牌/视图 → 基础策略 → 有限认知 → 回放 → 训练 | 见 F0028 每切片触发语 |
| 5 | 处理冲突副本与瘦身 | 恢复 `.gitignore`，diff/删除清单；删除前需授权 | `整理 OneDrive 冲突副本，先出保留删除清单再执行` |

## 风险与边界

- 本地 Git 基线已可提交；远端推送和 `v0.2.1` tag 重建尚未授权。
- F0028 已 Approved，Git 与测试前置门禁均已满足，可开始 F0028-1。
