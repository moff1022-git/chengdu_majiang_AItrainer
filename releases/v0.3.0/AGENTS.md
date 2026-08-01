# Agent / 助手协作约定

本仓库对人与 AI 编程助手统一适用。细则见 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。

## 强制规则

1. **先文档，后代码**  
   任何里程碑步骤、功能变更、规则/接口调整：先写或更新 `docs/` 下规格，状态达到 `Approved`（或用户明确「按此文档实现」）后，才修改业务代码。

2. **范围以文档为准**  
   不实现当前里程碑/功能文档 Out of Scope 中的内容；不「顺便」大重构。

3. **冲突处理**  
   代码与已批准文档不一致时：先修正文档（若需求变了）或先修正代码（若实现偏了），并在交付说明中写明。

4. **用户指令映射**

   | 用户说法 | 助手行为 |
   |----------|----------|
   | 开始 Mx / 做 Mx | 若无 `Approved` 规格 → **只写** `docs/milestones/Mxx_*.md` |
   | 确认文档 / Approved | 更新文档状态；**仍不写代码**除非用户同时要求实现 |
   | 实现 / Build / 写代码 | 检查规格已批准 → 按文档编码 + 测试 |
   | 新功能 / 改规则 | 先 `docs/features/` 或 `docs/adr/` |
   | 修 bug | 行为变更则补短文或 changelog；纯缺陷可小补丁 + changelog |

5. **交付格式**  
   每次实现交付应包含：文档路径、代码路径、测试/验收结果。

6. **每轮任务收尾（强制）**  
   每轮任务的**最后一条回复**必须包含：
   - **本轮已完成情况**（目标、交付物、状态变更、未完成/偏差、风险）
   - **下一步完整任务清单**（立即下一步 + 有序全量队列：动作 / 产出 / 依赖 / 建议触发语）  
   细则见 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) §2.1。

7. **每步文档落盘 / 跨机同步基线（强制）**  
   对话 session **不可**当作跨电脑状态源。每一轮闭环工作结束时，助手**必须**把可恢复基线写入仓库文档（至少覆盖写 `docs/status/LATEST.md`），并在有实质交付时追加 `docs/changelog.md`。  
   - 目的：换 Mac/Win/另一台机打开同一仓库即可「读文档同步」，不依赖旧 chat。  
   - 新会话开场：优先读 `docs/status/LATEST.md` → `docs/changelog.md` → 相关 `docs/features/` / 里程碑状态。  
   - 细则见 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) §2.1–§2.2、[`docs/status/README.md`](docs/status/README.md)。

8. **技术基线**  
   遵守 `PLAN.md`：engine 权威、players 可插拔、Human 子进程、game_id 可复现、允许 numpy/pygame。

9. **版本与一致性**
   应用版本仅改 `version.py`（见 `docs/VERSIONING.md`）；发版写 changelog + LATEST + tag。  
   文档与代码冲突时先对齐文档或代码，并更新 `docs/status/DOC_CODE_BASELINE.md`。  
   新 session 读序：`LATEST.md` → `DOC_CODE_BASELINE.md`（可选）→ changelog → 相关 F/M。

10. **Task 19 CLI 重启自动续跑**
    新 session 进入本仓库并发现 Task 19 未完成时，在完成第 7/9 条读序后立即运行 `python tools/task19_agent_runtime.py reconcile-startup`（使用当前环境的 Python）。存在 `resume_queue` 且无 `human_gates` 时，必须自动恢复 Goal、核对 integration HEAD/证据 SHA、忽略上一 session 的过期 Agent 心跳，并按幂等键续派；不等待用户再说“继续”。仅 `human_gates` 命中 ADR-0001 真正人工门禁时停止。CLI 关闭期间任务暂停；不安装或运行外部自动唤醒程序。
