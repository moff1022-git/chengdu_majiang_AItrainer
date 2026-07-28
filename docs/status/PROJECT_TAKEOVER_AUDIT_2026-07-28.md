# 项目接管审计

> 日期：2026-07-28  
> 范围：仓库结构、Git 元数据、文档/代码基线、Python 环境、测试、构建与运行产物  
> 结论：**代码主体可读、可编译，核心测试大部分通过；但 Git 元数据已被 OneDrive 冲突副本破坏，当前目录不可视为可安全提交/发布的正常工作树。**

> **后续处置（2026-07-28）**：远端 clone 返回零 refs/非法 HEAD；本地冲突 index 的 728 个条目中 675 个 blob 已缺失，无法完整恢复原历史。已保留损坏 `.git` 备份，并以当前经编译/测试验证的工作树重建本地 `main` 基线。

## 1. 接管结论

| 等级 | 结论 | 证据 / 影响 |
|------|------|-------------|
| P0 | Git 工作树失去有效分支基线 | `main` 为 unborn；`origin/main [gone]`；全部文件显示未跟踪；正常 `index`、`refs/heads/main` 缺失 |
| P0 | `.git` 被 OneDrive 冲突副本污染且对象不完整 | 存在 `index-Moff的Mac Studio`、非法 ref；tag `v0.2.1` 指向缺失对象；`git fsck` 报 badRefName / invalid sha1 / dangling commit |
| P1 | 测试套件并非全绿 | 共收集 280 项；排除会 Abort 的 Tk 用例后：278 passed、1 failed、1 deselected |
| P1 | 测试与已批准规格冲突 | `tests/test_human_wire.py::test_h05_registry_human` 仍断言最多 1 human；F0020 与 `players/registry.py` 已允许最多 3 human |
| P1 | Tk GUI 测试可令解释器硬崩溃 | `test_f0013_tk_inplace_paths_single_root` 在当前 macOS/Python 3.12/Tk 环境创建 `tk.Tk()` 时触发 Fatal Python error: Aborted，无法由 pytest 正常报告/清理 |
| P1 | 大量同步冲突副本可能造成双版本事实源 | 根目录、`docs/`、`display/`、`tools/` 与 `.git/` 均有 `*-Moff的Mac Studio*`；部分内容不同，例如两个 `LATEST` 表示不同下一步 |
| P2 | 仓库目录膨胀严重 | `.venv` 415 MB、backup 350 MB、logs 316 MB、releases 309 MB、dist 274 MB；`logs/predict` 含约 1,700 个 JSONL |
| P2 | 正常 `.gitignore` 文件缺失 | 仅存在冲突命名 `-Moff的Mac Studio.gitignore`，因此虚拟环境、日志、构建产物、缓存全部显示未跟踪 |
| P2 | 文档状态曾有轻微不一致（**2026-07-28 已修复**） | F0026/F0027 正文已与索引及 `DOC_CODE_BASELINE` 统一为 Done |

## 2. 已验证的健康项

- 当前解释器：`.venv/bin/python` = Python 3.12.13。
- `python -m compileall` 对 `app_paths.py`、`main.py`、`engine/`、`players/`、`protocols/`、`display/`、`training/`、`tools/`、`tests/` 通过。
- CLI 可用：`main.py --version` 输出 `0.2.1`；`--help` 正常列出 gui/play/human/train/resume/spectate/save-info。
- 版本锚点与基线一致：APP 0.2.1、state schema 4、persistence format 1、wire protocol 1。
- 280 项测试可正常收集；排除两个已明确问题后其余 278 项通过。
- 业务架构仍遵循 `PLAN.md` 的主要边界：`engine/`、`players/`、`protocols/`、`display/`、`training/` 分层存在，Human 子进程与可复现 game_id 均有实现和测试。
- 未在源代码/文档扫描中发现明显明文 API key、token、password 或 secret 赋值。

## 3. 测试复现

```bash
# 收集
.venv/bin/python -m pytest --collect-only -q
# 结果：280 tests collected

# 当前可安全跑的主体
.venv/bin/python -m pytest -q -k 'not test_f0013_tk_inplace_paths_single_root'
# 结果：278 passed, 1 failed, 1 deselected

# 语法/字节码编译
.venv/bin/python -m compileall -q app_paths.py main.py engine players protocols display training tools tests
# 结果：通过
```

普通失败：`tests/test_human_wire.py::test_h05_registry_human`。这是测试滞后于 F0020，不是当前 registry 实现偏离已批准规格。

## 4. Git 恢复边界

本轮没有直接修复 `.git`，原因是恢复动作会改变版本历史/索引，必须先确定权威来源。当前可见信息：

- remote URL：`https://github.com/moff1022-git/chengdu_majiang_AItrainer.git`
- OneDrive 冲突 ref 指向 commit `ae56c020...`，该 commit 可局部读取，主题为 README 截图刷新。
- `v0.2.1` ref 指向的 `7c919058...` 对象在本机缺失。
- 对 `ae56c020...` 的 tree 遍历也遇到缺失对象，说明不能只靠本地 `.git` 完整恢复。

推荐先从远端只读 fetch/clone 到临时目录核对，再选择“重新 clone 后搬入本地未提交文件”或“就地重建 refs/index”。优先推荐前者，风险更低。任何清理冲突副本、日志、build/dist/releases/backup 的动作都应在恢复 Git 并生成清单后单独执行。

## 5. 接管后的有序任务队列

1. **P0：恢复 Git 基线（本地已完成）**  
   已以当前工作树重建健康 `main`/index；损坏元数据保留在 `backup/git-metadata-corrupt-2026-07-28/`。远端推送与 tag 重建需单独确认。
2. **P1：修复测试基线**  
   产出：更新 M09 旧测试以符合 F0020；为 Tk 用例增加安全 skip/环境门禁；全量测试不再硬崩溃。  
   依赖：Git 基线恢复；属于纯缺陷/测试修复，补 changelog。  
   建议触发语：`修复接管审计中的两项测试问题`。
3. **P1：处理 OneDrive 冲突副本**  
   产出：逐文件 diff 决议表；合并有效差异；移除确认冗余副本。  
   依赖：Git 基线和备份；删除前需明确授权。  
   建议触发语：`整理 OneDrive 冲突副本，先出保留删除清单再执行`。
4. **P2：恢复忽略规则并瘦身**  
   产出：正常 `.gitignore`；本地大目录保留/迁移/删除方案；Git 状态只展示真实源文件变更。  
   依赖：冲突副本决议；删除构建/日志/备份需授权。  
   建议触发语：`恢复 gitignore 并制定项目瘦身清单`。
5. **P2：统一文档状态（已完成）**  
   2026-07-28 已将 F0026/F0027 正文、索引和 baseline 统一为 Done；远端 Release 事实仍待 Git P0 恢复时重新核验。
6. **P3：建立接管后质量门禁**  
   产出：可重复的无头测试命令、GUI 测试分组、基础 lint/type 策略与发布检查表规格。  
   依赖：前述 P0/P1 完成；先写 feature/ADR 再实现自动化。  
   建议触发语：`起草接管后的质量门禁规格`。

## 6. 本轮边界

- 未修改业务代码、测试代码、Git refs/index 或发布产物。
- 未删除任何冲突副本、缓存、日志、备份或构建产物。
- 未进行 GUI 人工目视验收、Windows MSI 实机安装或远端 GitHub Release 复核。
