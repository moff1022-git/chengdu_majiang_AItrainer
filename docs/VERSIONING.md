# 版本管理规则（权威）

| 字段 | 值 |
|------|-----|
| **状态** | **Approved** |
| **生效** | 2026-07-26 |
| **程序单一源** | 仓库根目录 [`version.py`](../version.py) |
| **人类可读版本线** | 本文件 + [`docs/changelog.md`](changelog.md) |
| **关联** | [`docs/DEVELOPMENT.md`](DEVELOPMENT.md) · [`docs/packaging/MACOS_BUILD.md`](packaging/MACOS_BUILD.md) · [`docs/packaging/WINDOWS_BUILD.md`](packaging/WINDOWS_BUILD.md) |

---

## 1. 版本种类（必须区分）

本项目存在**多条版本线**，不得混用：

| 种类 | 常量 / 字段 | 含义 | 何时升 |
|------|-------------|------|--------|
| **应用版本** | `version.APP_VERSION` | 产品/分发包版本（SemVer） | 见 §2 |
| **存档 schema** | `engine.state.SCHEMA_VERSION` | `GameState` JSON 结构 | 状态字段不兼容时 +1 |
| **存档文件格式** | `engine.persistence.FORMAT_VERSION` | 外层 save 文档壳 | 存档外壳变时 +1 |
| **座位协议** | `protocols.wire.PROTOCOL_VERSION` | 主进程↔座位窗 NDJSON | 线协议不兼容时 +1 |
| **配置表** | 各 `configs/*.json` 的 `version` | 计分/番表/策略等 | 表语义变时 +1 |

**规则**：应用版本**不**因仅改文档而强制 +1；schema/协议变时**必须**在 changelog 写明，并视兼容性决定是否升 **MINOR/MAJOR**（见 §2.3）。

---

## 2. 应用版本：语义化版本（SemVer）

格式：

```text
MAJOR.MINOR.PATCH[-prerelease][+build]
```

例：`0.2.0`、`1.0.0-rc.1`、`1.0.0+pyinstaller`。

### 2.1 递增规则

| 变更类型 | 升哪一段 | 例 |
|----------|----------|-----|
| 不兼容的 API/规则/默认行为（老存档或老操作方式失效） | **MAJOR** | 0.x → 1.0.0 首次稳定；之后 1→2 |
| 向后兼容的功能（新布局模式、新 CLI、新 UI） | **MINOR** | 0.2.0 → 0.3.0 |
| 向后兼容的缺陷修复、性能、文案 | **PATCH** | 0.2.0 → 0.2.1 |
| 内部重构、纯文档、测试（行为不变） | 可不升版；若已打 tag 再修文档则 **不升** | — |

**0.x 阶段**（当前）：允许较大改动仍只升 MINOR；**1.0.0** 起严格执行上表。  
**预发布**：`-alpha.N` / `-beta.N` / `-rc.N` 仅用于发版前试玩包，不替代正式 PATCH/MINOR。

### 2.2 何时必须 bump

发版或合并到 `main` 且满足任一条件时，**同一 PR/提交**内：

1. 改 `version.py` 中 `APP_VERSION`（及 `APP_VERSION_INFO`）  
2. 在 `docs/changelog.md` **顶部**追加该版本节（见 §4）  
3. 刷新 `docs/status/LATEST.md`（写明当前应用版本）  
4. 若改 schema/协议：同步改对应常量 + changelog 交叉引用  

### 2.3 与 schema / 协议的联动

| 情况 | 应用版本建议 |
|------|----------------|
| 仅 PATCH 修 bug，schema 不变 | PATCH |
| 新功能，老存档仍可读 | MINOR |
| `SCHEMA_VERSION` 升高且不兼容旧存档 | **至少 MINOR**；1.0 后倾向 **MAJOR** |
| `PROTOCOL_VERSION` 不兼容 | 同上；并保证主程序与座位窗同包发布 |

---

## 3. 单一源与展示

### 3.1 源文件

```text
version.py          # APP_VERSION, APP_VERSION_INFO, APP_NAME, …
```

禁止在 UI/打包脚本中手写第二个版本号（打包从 `version.py` 读取）。

### 3.2 程序展示

| 位置 | 行为 |
|------|------|
| CLI | `main.py --version` / `-V` 打印应用版本 |
| CLI help | argparse 使用同一版本 |
| 主窗 / 大厅 | 标题或状态区可见 `vX.Y.Z` |
| 座位窗标题 | 可选后缀 `vX.Y.Z`（不遮挡座位号） |
| 打包 Info.plist | `CFBundleShortVersionString` = `APP_VERSION` |

### 3.3 Git 标签（推荐）

```bash
git tag -a "v$(.venv/bin/python -c 'from version import APP_VERSION; print(APP_VERSION)')" -m "release"
git push origin "v$(...)"
```

标签名：`v` + `APP_VERSION`（如 `v0.2.0`）。  
**先**改 `version.py` 与 changelog，**再**打 tag。

---

## 4. Changelog 约定

`docs/changelog.md` 倒序；每个**已发布**应用版本一节：

```markdown
## X.Y.Z — YYYY-MM-DD

### 新增
- …

### 修复
- …

### 破坏性变更（若有）
- schema / 协议 / 操作方式 …

### 内部
- 文档、测试、打包 …
```

日常开发过程条目可继续按日期写在「未版本化」日更下；**打 tag 前**把该周期整理进 `## X.Y.Z`。

---

## 5. 分支与发布流程（简）

| 步骤 | 动作 |
|------|------|
| 1 | 功能/修复按 Docs-First 合入 `main` |
| 2 | 决定 SemVer 段；改 `version.py` |
| 3 | 更新 `changelog.md` + `LATEST.md` |
| 4 | 测试：`pytest`；可选打包脚本 |
| 4b | **刷新 README 功能截图**（F0026）：`.venv/bin/python tools/capture_readme_screenshots.py`，提交 `docs/media/readme/*`（UI 无改动的纯内部 PATCH 可跳过，见 F0026） |
| 5 | commit：`chore(release): vX.Y.Z` |
| 6 | `git tag vX.Y.Z` 并 push |
| 7 | 构建 macOS `.app` / Windows onedir（产物名可带版本，见打包脚本） |

热修：从 tag 拉 hotfix 分支 → 只升 PATCH → 合并回 main。

---

## 6. 当前基线

| 项 | 值 |
|----|-----|
| 应用版本 | 见 `version.py`（当前发布线 **0.2.1**；规则落地首版 0.2.0） |
| 存档 schema | 4 |
| 存档 format | 1 |
| 座位协议 | 1 |

---

## 7. 禁止事项

- 只改展示字符串、不改 `version.py`  
- 同一 commit 混升 MAJOR 又塞大量无关重构且不写 changelog  
- 用日期串（`2026.07.26`）代替 SemVer 作为应用版本  
- 把 `PROTOCOL_VERSION` 与 `APP_VERSION` 绑死为同一数字  

---

## 8. 变更历史

| 日期 | 说明 |
|------|------|
| 2026-07-26 | 初版 Approved；落地 `version.py` + CLI/UI/打包读取 |
