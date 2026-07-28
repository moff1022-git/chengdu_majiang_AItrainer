# 文档 ↔ 程序一致性基线

> **日期**：2026-07-29  
> **应用版本**：`0.2.1`（`version.py`）  
> **Git**：本地 `main` 已推进至 F0028-2 提交 `0c82c78`；损坏元数据保留于 `backup/git-metadata-corrupt-2026-07-28/`；远端尚未推送  

本文件是 **权威对照表**：文档状态须与下表一致。换机 / 新 session 除读 `LATEST.md` 外，冲突时以 **代码 + 本表** 为准。

---

## 1. 版本与协议线

| 线 | 权威位置 | 当前值 |
|----|----------|--------|
| 应用 SemVer | `version.py` → `APP_VERSION` | **0.2.1** |
| 存档 GameState schema | `engine/state.py` → `SCHEMA_VERSION` | **5**（reader 1–5） |
| 存档外壳 format | `engine/persistence.py` → `FORMAT_VERSION` | **1** |
| 座位 NDJSON 协议 | `protocols/wire.py` → `PROTOCOL_VERSION` | **1** |
| Git 本地基线 | `main` / `0c82c78` | F0028-2 已提交；原历史因对象缺失无法完整恢复 |
| Git 远端 | `origin` | GitHub 当前返回零 refs 与非法 `refs/heads/.invalid`；未推送、未恢复 tag |
| 历史发布记录 | `v0.2.1` | changelog 记录 Release 已发布；当前无可验证 Git tag ref |

---

## 2. 里程碑 M01–M11

全部 **Done**（见 `docs/milestones/README.md`）。  
**M09 补充**：首版规格写「最多 1 human」；**已被 F0020 取代**（代码允许 ≤3 human）。M09 文档须标注「见 F0020」。

---

## 3. 功能规格状态（与代码一致）

| 编号 | 状态 | 代码锚点（摘要） |
|------|------|------------------|
| F0001–F0008 | Done | 几何 / 座位窗 / 大厅 / ready / 兼容 / 响应式 / 主桌 / 结算 |
| F0009 | Done | **实装：选中金框+底色，不放大牌面**（防闪）；当前打出面板 |
| F0010 系列 | Done / 子计划见各文 | `players/analysis/*` 对手预测与向听 |
| F0011 | Done | 综合出牌顾问 |
| F0012 | Done | 推荐序号 + 进张条 |
| F0013 | Done | 脏更新 / broadcast 节流 |
| F0014 | **Done（几何移交）** | 内容/视觉决议仍有效；外框权威 = UI_DESIGN_STANDARD + F0018/F0020 |
| F0015–F0019 | Done | 主/人/AI 内区 + 实现计划 + 缩放 |
| F0020 | Done | 布局 A/B/C/D；`human_seats`；registry ≤3 |
| F0021 | Done | 打包脚本 + `app_paths` + `--seat-window` |
| F0022 | Done | `ui_chrome` + lobby/result |
| F0023 | Done | `dice_fx` + 确认后播骰再开局 |
| F0024 | Done | `play_log_format` 细化日志 |
| F0025 | **Done** | `packaging/windows/*` + `tools/packaging/build_*_windows.ps1`；见 WINDOWS_BUILD |
| F0026 | **Done** | README 五图 `docs/media/readme/` + `tools/capture_readme_screenshots.py` |
| F0027 | **Done** | MSI：`build_msi_windows.ps1` + `packaging/windows/msi/Product.wxs`（WiX 3.14） |
| F0028 | **In Progress（F0028-1–3 Done）** | 配置追踪 + 实体牌/视图隔离 + 确定性 humanlike_v2 已实现；有限认知待 F0028-4 |
| F0028-2 | **Done** | `engine/physical_tile.py`、schema migration/invariants、`protocols/player_view_*`、`training/oracle.py` |
| F0028-3 | **Done** | `players/humanlike/{view,belief,hand_analyzer,plan,candidates,evaluator,player}.py` + registry/preset |
| F0010-规则表 | Review | 清单文档，非阻塞实现 |

---

## 4. 关键行为（文档易错点）

> **已知阻塞缺陷（2026-07-29）**：Human 换三张返回 face `Tile`，opening 未解析为具体 `PhysicalTile`；与 AI offer 混合后排序报类型比较异常。纯 AI 不受影响，Human+AI 启用换三张暂不可放行。详见 `F0028_3_MANUAL_QUICK_ACCEPTANCE_2026-07-29.md`。

| 主题 | 程序事实 |
|------|----------|
| 选中手牌 | 金黄双环 + 压暗未选；**`selected_tile_tw` 不放大** |
| 弃牌区 | 多行 compact；**无可见滚动条**；滚轮可滚 |
| 人类数 | 1–3 + 对应 AI；4 human 拒绝 |
| 布局 | A(1H3AI) B(2H2AI) C(0H4AI) D(3H1AI) |
| 主窗掷骰 | 每轮 ready 后动画 ~2s，骰点=game_id 派生 |
| 出牌日志 | 摸/打/碰/杠/胡/分 + 中文牌名 |
| 打包产物 | **仅 Releases / 本机 dist·releases**；不在 git tree |

---

## 5. 文档目录角色

| 路径 | 角色 |
|------|------|
| `docs/DEVELOPMENT.md` | 流程权威 |
| `docs/VERSIONING.md` | 版本规则 |
| `docs/status/LATEST.md` | 每轮进度（覆盖写） |
| `docs/changelog.md` | 人读变更 |
| `docs/features/*` | 功能规格 |
| `docs/milestones/*` | 里程碑（历史权威） |
| `docs/design/*` | UI 几何/内区设计 |
| `docs/packaging/*` | 打包 |
| `PLAN.md` | 系统总设计（M 路线图）；后续功能以 F 为准 |
| `AGENTS.md` | 助手强制规则 |

---

## 6. 审计修订记录

| 日期 | 说明 |
|------|------|
| 2026-07-26 | 全面对照 v0.2.1 代码；修正 F0009/F0014/M09/LATEST/README/状态索引 |
| 2026-07-28 | 登记 F0028 Approved/未实现；修正 Git 状态为本地 P0 损坏待远端核验 |
| 2026-07-28 | 远端与本地历史均无法完整恢复；以当前工作树重建本地 main/index，保留损坏 `.git` 备份 |
| 2026-07-28 | F0028-1 完成：27 GP / 33 RP / 60 条追踪映射、版本兼容矩阵和稳定配置 hash；全量 291 passed / 1 skipped |
| 2026-07-28 | 新增 F0028-2 子规格至 Review；仅文档，等待确认版本与迁移决议 |
| 2026-07-28 | 用户确认 F0028-2：Review → Approved；五项版本/兼容决议锁定，本轮未编码 |
| 2026-07-28 | F0028-2 Done：state schema 5、PlayerView 2、108 张守恒与 oracle 分离；308 passed / 1 skipped |
| 2026-07-29 | 新增 F0028-3 确定性 PlayerView 策略子规格至 Review；本轮未修改业务代码 |
| 2026-07-29 | 用户确认 F0028-3：Review → Approved；六项确定性策略决议锁定，本轮未编码 |
| 2026-07-29 | F0028-3 Done：纯 PlayerView 确定性策略与选配玩家；321 passed / 1 skipped，150 局零策略崩溃 |
| 2026-07-29 | 快速人工验收 MT-04 发现 Human 换三张 face/PhysicalTile 混用阻塞缺陷；待修复复测 |
