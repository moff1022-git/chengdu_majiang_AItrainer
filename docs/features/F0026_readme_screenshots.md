# F0026 — README 功能截图与发版刷新

| 字段 | 值 |
|------|-----|
| **编号** | F0026 |
| **标题** | README feature screenshots + mandatory refresh on release |
| **状态** | **`Approved`**（用户明确要求：功能章增加五图 + 每次程序更新后重刷） |
| **类型** | 文档交付 / 工程流程 |
| **关联** | 根目录 `README.md` · `docs/media/readme/` · `tools/capture_readme_screenshots.py` · [`docs/VERSIONING.md`](../VERSIONING.md) |
| **依赖** | 既有 display / seat UI（F0002+、F0022–F0024） |

---

## 1. 目标

| ID | 目标 |
|----|------|
| G1 | 在 GitHub `README.md` **功能**章节展示五类界面图 |
| G2 | 图片路径固定、可链接、可随仓库 clone |
| G3 | **每次应用版本发版 / UI 变更后**必须重刷并提交截图 |
| G4 | 提供一键脚本，减少手工截图遗漏 |

### 五类画面（固定文件名）

| 场景 | 文件 | 内容要求 |
|------|------|----------|
| 大厅 | `docs/media/readme/01_lobby.png` | 主程序封面/设置/开始 |
| 主窗口（游戏中） | `docs/media/readme/02_main_play.png` | 牌桌观战 + 侧栏日志/HUD |
| 人类玩家（游戏中） | `docs/media/readme/03_human_play.png` | play 座位窗手牌/操作区 |
| AI 玩家（游戏中） | `docs/media/readme/04_ai_watch.png` | watch 座位窗只读 |
| 计分窗口 | `docs/media/readme/05_result.png` | 结算 / 本局分 / 回大厅 |

配套：`docs/media/readme/MANIFEST.json`（版本、生成时间、生成方式）。

---

## 2. 范围

### In Scope

- README 功能节插图与说明  
- 截图目录、生成脚本、发版清单勾项  
- 主窗 pygame 离屏真渲染；座位窗优先 OS 抓窗，失败则资源拼合 mockup  

### Out of Scope

- 动图 / 视频演示  
- 多语言 README 截图分叉  
- CI 强制跑截图（本机/发版机执行即可；有显示器权限更佳）  

---

## 3. 刷新策略（强制）

下列任一发生时，**发版或合入前**必须执行截图刷新并 commit：

1. `version.py` 的 **MINOR / MAJOR** 发版  
2. **PATCH** 发版且改动涉及：大厅 / 主桌 / 结算 / 座位窗 UI、主题资源、布局几何  
3. 用户明确要求更新 README 展示  

**可不刷新**（仍建议抽检）：纯引擎规则、训练 env、文档-only、无 UI 影响的 bugfix。

### 发版检查表（写入 VERSIONING）

- [ ] `python tools/capture_readme_screenshots.py`  
- [ ] 目视五图与当前 UI 一致  
- [ ] 提交 `docs/media/readme/*` + 如有需要的 README 文案  
- [ ] `MANIFEST.json` 中 `app_version` = 当前 `APP_VERSION`  

触发语：`更新 README 截图` / 发版步骤内自动执行。

---

## 4. 生成方式

```bash
cd /path/to/chengdu_majiang_AItrainer
.venv/bin/python tools/capture_readme_screenshots.py
# 可选：尝试真座位窗抓取（macOS 需「屏幕录制」权限）
.venv/bin/python tools/capture_readme_screenshots.py --prefer-seat-grab
```

| 画面 | 默认方法 |
|------|----------|
| 大厅 / 主桌 / 结算 | `pygame` Surface 离屏绘制（与程序同一 `LobbyView` / `TableView` / `ResultView`） |
| 人类 / AI 座位 | 有权限：Tk 窗 OS grab；否则：`tools/gen_window_mockups_from_assets.py` 资源拼合 → PNG |

> 无屏幕录制权限的 CI/沙箱环境：**座位图为资源实装拼合**，主窗三图仍为真渲染。有权限时应 `--prefer-seat-grab` 刷真窗。

固定 `game_id=readme-screenshot-fixed` 保证主桌/结算可复现布局基线（具体牌面随规则演进可能变化，属预期）。

---

## 5. README 版式

功能列表下增加 **「界面预览」** 小节：五图用表格或连续 `###` 小标题 + 相对路径图片。  
图片宽度由 GitHub 自动缩放；源图建议宽 ≥ 900px。

---

## 6. 验收

- [x] 五文件存在且 README 可预览  
- [x] 脚本可重复运行覆盖写  
- [x] VERSIONING / DEVELOPMENT 发版步骤含刷新项  
- [x] LATEST / changelog 记录  

---

## 7. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-26 | Approved → Done | 用户要求 README 功能章五图 + 程序更新后重刷 |
