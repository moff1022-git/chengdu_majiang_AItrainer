# Changelog

按时间倒序记录**已完成**的文档与实现摘要（非自动生成）。  
配合 `docs/status/LATEST.md` 作**跨机/跨 session 同步基线**（见 `docs/DEVELOPMENT.md` §2.2）。

## 2026-07-26（续）

### 功能 — 主窗出牌日志细化（F0024）

- 解析完整 `score_events`：摸/打/碰/杠/胡/计分/行牌开始/流局  
- 中文牌名（3万/9筒）；回合号 `T12`；终局胡序与得分摘要  
- 侧栏按事件类型着色；容量 400  
- 代码：`play_log_format.py`、`app._ingest_play_log`、`play_log_panel.py`

### 功能 — 主窗每轮掷骰定庄展示（F0023）

- 全员确认后、发牌前：主窗中心播放双骰动画（~2s）
- 骰点与引擎 `game_id` 派生结果一致；定格后显示庄家
- 日志：`掷骰 d1+d2=total → 庄家 Sx`
- 代码：`display/dice_fx.py`、`table_view`、`app` 时序；测：`test_dice_fx.py`

### 修复 — 座位窗弃牌多行显示

- **现象**：AI/人类「本家弃牌」像单行排，右侧裁切显示不全  
- **修复**：按真实扩展区宽度多行换行（compact 牌面 + chrome）；多行时纵向可滚；标题显示行×列与张数  
- 代码：`players/seat_window.py`；测：`test_discard_grid_multi_row_narrow_ext`
- **续**：去掉弃牌区右侧滚动条（仍可用滚轮滚动）

### UI — 大厅/结算对齐人类窗风格（F0022）

- 共享色板与分区：`display/ui_chrome.py`（顶栏 / 底栏 / 面板 / 主次按钮）
- `lobby_view`：设置卡片 + 固定底栏「开始」，小窗不遮挡
- `result_view`：摘要条 + 座位卡片网格 + 固定底栏「回大厅/再来一局」
- 测：`tests/test_lobby_view.py`、`test_result_view` 小窗

## 0.2.0 — 2026-07-26

首个按 [`docs/VERSIONING.md`](VERSIONING.md) 管理的应用版本（SemVer 单一源 `version.py`）。

### 新增
- **版本管理规则** `docs/VERSIONING.md`；`version.py`（`APP_VERSION=0.2.0`）
- CLI：`main.py --version` / `-V`
- UI：主窗标题、大厅副标题、座位窗标题栏显示 `v0.2.0`
- 打包脚本从 `version.py` 读取版本并写入 Info.plist

### 累计能力（相对项目早期）
- F0020 2H/3H 布局 B/D；F0021 macOS PyInstaller/Nuitka 打包
- 座位窗胡牌横幅、副露中文/手牌同尺寸、选中金框等

### 内部版本线（非 APP）
- 存档 schema：4 · format：1 · 座位协议：1

---

## 2026-07-26

### 工程 — 版本管理规则（v0.2.0）

- 权威：`docs/VERSIONING.md`；源：`version.py`
- 接入：`main.py`、`display/app.py`、`lobby_view`、`seat_window`、打包脚本
- 测：`tests/test_version.py`

### 工程 — macOS 打包（F0021 · PyInstaller + Nuitka）

- **文档**：`docs/packaging/MACOS_BUILD.md`、`docs/features/F0021_macos_packaging.md`
- **路径**：`app_paths.py`（资源根 / 可写 logs / 冻结子进程命令）
- **入口**：`packaging/macos/pyinstaller_entry.py`；`main --seat-window` 再入座位窗
- **脚本**：`tools/packaging/build_pyinstaller_macos.sh`、`build_nuitka_macos.sh`
- **实测产物**（arm64）：
  - PyInstaller ≈199MB：`dist/pyinstaller/ChengduMahjongAITrainer.app`
  - Nuitka ≈97MB：`dist/nuitka/ChengduMahjongAITrainer.app`
- 测：`tests/test_app_paths.py`

### 修复 — 座位窗胡牌提示 / 副露尺寸 / 中文类型

1. **胡牌无提示**：`hu_banner` 曾 `pack(before=meta_row)`，但横幅在 `mid`、meta 在 `op_status_fr`，跨父级 pack 静默失败 → 改挂 `op_info_fr`（状态栏下），始终可见；AI 窗同步显示  
2. **AI 副露过大裁切**：固定 `tw=28` 在小 AI 窗溢出 → 副露牌面改与**手牌同宽**  
3. **副露类型英文**：`pong`/`ming_gang`… → **碰/明杠/暗杠/加杠/吃**（`meld_kind_label`）  
- 代码：`players/seat_window.py`；测：`test_meld_kind_label_zh`

### 修复 — 人类手牌选中无加框/高亮

- **现象**：点选手牌后几乎无选中提示（PhotoImage 铺满 Label，1px 边框不可见）
- **修复**：
  - 手牌固定外框预算（`ht=2` 面环 + `face_hold` 外环），选中/取消不回流
  - 选中：金黄双框 `#ffeb3b` + 暖金底；未选中边框与桌面同色
  - 有选中时其余牌略压暗，对比更强
- 代码：`players/seat_window.py`；测：`tests/test_seat_ui.py`

### 实现 — F0020 多人人类模式（2H/3H · Done）

- **规格** `docs/features/F0020_multi_human_modes.md` → **Done**
- **几何**：`plan_mode_D`（AI 顶带 + body 2×2）；`resolve_layout_mode(3,1)==D`；B 沿用
- **Hub**：`human_seats: list[int]`；play/watch 按列表；`start_all`/`ensure_all` 返回 `dict[seat, transport]`
- **App**：`_human_seats` 全链路；为每位 human 的 `HumanPlayerProxy.attach_transport`
- **Registry**：允许多 human（最多 3）；4H 拒绝
- **大厅**：预设「2人类+2AI」「3人类+1AI」
- **测试**：`tests/test_f0020_multi_human.py`；更新 `test_f0018_layout_geometry` / `test_players`

### 文档 — 2/3 人类模式（F0020 · 规格先行）

- **F0020** 初稿 Review → Approved → Done（同日）
- **UI 规范 v1.4.0**：布局 D；B 的 AI 顶对齐；`(3,1)→D`
- 索引：`docs/features/README.md`

### 工程 — 导入 GitHub

- 本地 `git init -b main`；初始提交 `b4020a4` + 进度文档 `b1fbb99`
- `.gitignore`：排除 `.venv/`、`logs/`、`backup/` 等
- **远程**：https://github.com/moff1022-git/chengdu_majiang_AItrainer （**private**）
- `main` 已 push 至 `origin/main`（HTTP/1.1 重试成功）

## 2026-07-21

### 修复 — 初始布局 AI 遮挡（位置上移，不改 AI 高度）

- **现象**：AI 在上半区垂直居中 → 位置偏低，易压住 MAIN/人类
- **正确修复**：AI **保持原尺寸**（1080p 442×249）；**仅顶对齐 / 必要时上移**；禁止拔高 AI
- **MAIN↔人类**：完整模式同高（`_equalize_main_human_heights`）
- 代码：`display/window_geometry.py`；测：`test_window_geometry.py`
- 说明：曾误把 AI 拉高填满上半带，已按用户澄清回退尺寸

### 修复 — MAIN 比人类窗高出约数个标题栏

- **实测根因（macOS Quartz）**：client 同为 plan 高时 outer 同高；但 **SDL_VIDEO_WINDOW_POS 是内容顶**，且 **Dock 会把 pygame 主窗上推**（例：plan y=554 → 实际 outer y=444，差 ≈110px≈数个标题栏），Tk 人类窗仍在 plan y
- **修复**：
  1. 工作区扣除 **菜单栏+Dock**（AppKit `visibleFrame`）
  2. `set_sdl_window_pos` 在 darwin 将 Y **+ title chrome**，与 Tk outer 顶对齐
  3. 人类 client 锁定 + MAIN pin 对齐人类实际高度
- 代码：`window_geometry.py`、`seat_window.py`、`seat_ui_hub.py`、`app.py`

### 修复 — 主桌左右手牌大小/排列与上下一致

- 根因：左右扇区仅骰子高度，14 张竖排被迫缩小
- **画框手牌**：左右 `ZONE_HAND` 占满 TABLE 高；上下手牌在左右厚度之间内缩（四角不重叠）
- 绘制：四家同一 `draw_tw` / 居中逻辑（左右仍 ±90°）
- 代码：`display/main_interior.py` `_frame_hand_strips`；`display/table_view.py` 手牌绘制
- 测试：`test_main_hand_bands_frame_and_equal_face_size`

### 调整 — 取消手牌区滚动条 + 放大手牌

- 实时手牌区 **去掉右侧 Scrollbar 占位**（保留滚轮滚动）
- 手牌再放大：14 张占满区宽，左右仅小边距（非半张）

### 修复 — 手牌只能显示约 11 张

- 根因：选中框 chrome（ht=3+bd=2）使每格实际宽 > face_tw
- 修正：手牌 **compact 描边**；宽度公式计入 chrome

### 调整 — 手牌宽按 14 张 + 半张边距

- 人类/AI：按区宽算 face 宽，保证 **14 张一行**，左右约 **½ 张** 余量；间距仍为 0

### 调整 — 进张贴手牌上方 50% 透明 + 手牌间距 0

- 可听进张：`Toplevel` **alpha=0.5**，几何贴在手牌条 **正上方**
- 人类/AI 手牌 **gap=0**（牌面贴紧）

### 调整 — 进张浮动层 + 手牌贴底

- 可听进张：改为叠在手牌区上的浮动面板（有进张才显示），**不占流式高度**
- 手牌：固定在实时手牌区 **底部**（人类/AI 共用贴底逻辑）

### 调整 — 操作条单行 50/50（文案 | 按钮）

- OP_PLAY 底栏 **一行高**；左 50% 中文提示居左；右 50% 按钮按数量均分宽与间隔

### 调整 — 状态区严格 50/50 + 当前牌框 95% 高

- STATUS_L/R **place 各 50% 宽**（人类/AI 共用）
- 当前牌显示框：**高 = 状态区 × 0.95**，**w = h/1.4** 固定比例；牌面随框缩放

### 调整 — 操作条半高 + 状态区当前牌缩放

- **操作区**：OP_PLAY 内碰杠胡条高度约为原预算 **一半**（约 play 的 19%）
- **当前打出牌**：随 OP_STATUS 可用高宽缩放（去掉固定 64px）

### 文档 + 实现 — 座位窗 STATUS 20% / PLAY 60%

- **规范**：`HUMAN_WINDOW_LAYOUT` / `AI_WINDOW_LAYOUT` v0.2；F0016/F0017 摘要同步 — 当前状态 **20%**、实时手牌 **60%**（原 25%/55%）
- **代码**：`players/seat_layout_play.py` `STATUS_RATIO=0.20` `PLAY_RATIO=0.60`；示意脚本同改

### 修复 — 主窗条带居中 + 座位操作条/字号

- **主窗**：手/副露/弃牌严格在 ZONE 矩形内绘制；放不下则缩小牌面；网格在矩形内**居中**；`set_clip` 防溢出
- **座位操作条**：操作区占 OP_PLAY 更高比例；按钮紧凑换行；就绪/碰杠胡控件适配条高
- **字号**：人类基准 9/11、上限 12/14，避免完整窗内文字过大

### 修复 — 窗口外框不放大（完整模式尺寸）

- **约定**：完整模式外框 = 规范尺寸；**1080p 表为上限**（MAIN/人类 ≤885×498，AI ≤442×249）；大于 1080p 屏也用 1080p 窗尺寸，**不随分辨率放大窗**
- `plan_layout_abc` size_basis 封顶 1770×996 画布；`clamp_outer_size`；主窗/座位 min=max 锁定完整尺寸

### 修复 — 座位窗顺序/比例/精简模式

- **核查** `docs/status/UI_LAYOUT_ISSUE_CHECK.md`：按钮/设置顺序 = **程序 bug**（设计正确）；分区比例 = **程序未强制 place**；精简模式 = **实现缺失**
- **修正**：`seat_layout_play.compute_seat_interior` + `seat_window._apply_interior_geometry` — OP 67/33、STATUS/PLAY 25:55、EXT 30/70；**操作条在设置上方**
- **完整|精简**：标题栏切换；精简隐藏弃牌带 + 宽 50%/高 72%；完整恢复尺寸

### 实现 — F0019 窗内元素等比缩放

- **规格** `docs/features/F0019_interior_element_scale.md`：1080p 默认客户区为基准与 **minsize**（MAIN/人类 885×498、AI 442×249）；**布局比例不变**；`S=min(Cw/Cw0,Ch/Ch0)` 缩放牌/字/间距
- **模块** `display/interior_scale.py`；`layout.py` / 侧栏 / 控制面板 / `seat_window` 接入；手牌网格随 S 的 min/max_tw
- **测试** `tests/test_f0019_interior_scale.py`；F0013 脏更新保持控件复用

### 实现 — F0018 UI 布局改造（P0–P8）

- **多窗外框（D1）**：`layout_canvas` 85% 居中 + 2160p 封顶；`plan_mode_A/B/C`；`resolve_layout_mode`；Hub/App/`human_proxy` 应用 plan
- **主窗内部（D2/F0015）**：`main_interior` 80/20；DICE 同心；四扇区弃→副露→手条带；SIDE 积分/控制/出牌日志；`PlayEventLog` 环形缓冲
- **座位窗（D3/D4/F0016–17）**：play/watch **67/33**；扩展区折叠；人类 EXT=对手 HUD+弃牌；AI EXT=操作日志+弃牌；保留推荐/进张/就绪/脏更新
- **测试**：`tests/test_f0018_layout_geometry.py`；更新 `test_window_geometry` / `test_table_layout`；全量 **237 passed**（1 预存 subprocess 失败）
- **状态**：F0015/16/17/18 → **Done**；F0007 注布局由 F0015 取代；`PLAN.md` §10.3 短更；任务清单见 `UI_MODIFICATION_TASK_LIST.md`

### 备份 + 文档确认

- **完整项目备份（实现前）**：`backup/2026-07-21/` — 源码 + docs + assets 等 **2520** 文件（~333 MiB）；`BACKUP_MANIFEST.txt`；脚本 `tools/backup_project.py`（排除 git/venv/cache/嵌套 backup）
- **F0018 确认 / `Approved`**：用户确认后实现；见上节 Done

## 2026-07-20

### 文档 / 设计

- **UI 设计规范 v0.1（布局权威）**：`docs/design/UI_DESIGN_STANDARD.md` — 布局 A 横屏 / B 竖屏；配置 C1=1H3AI、C2=2H2AI；完整版占比与矩形算法；精简=完整宽 **50%**、高不变、**左锚向左收窄**；3H1AI 不做；本阶段不出图。F0014 几何移交本文
- **UI 设计规范 v0.2**：布局总面积 **85%** 居中画布；**720p/1080p/2160p** 横竖默认窗口像素表（C1/C2×完整/精简）；同角色尺寸一致；默认=最小可等比放大；**>2160p 默认封顶 2160p 表**
- **UI 设计规范 v0.3 布局示意图**：`docs/design/layout_schematics/` — A/B × 单人C1/双人C2 × 完整/精简 共 8 张（1080p 尺寸标注）
- **布局示意图 v0.3.1 重出**：删除旧版；`tools/gen_layout_schematics.py` 统一样式；**图片像素=实际设计画布**（A 1770×996 / B 996×1770），窗框=表列默认 px
- **布局规范 v0.4 / 示意图重出**：修正 A/B AI（及 MAIN/人类）尺寸不一致；**同档同配置跨布局窗像素必须相同**；1080p C1 AI=**586×349**、MAIN=**882×349**；删旧图后重生成 8 张
- **UI 布局规范 v1.0-draft 重设计**：`docs/design/UI_DESIGN_STANDARD.md` — **仅横屏**；布局 **A=3AI+1H / B=2AI+2H / C=0AI+3H / D=4AI+0H**；MAIN **25% 左下固定**；人类完整 **25%**（A 右下；B 右下+右上；C 右下+右上+左上）；AI 完整 **6.25%**（A/D 上半横均分，B 左上横均分）；旧竖屏与 85% 统一 h **废止**
- **UI 布局规范 v1.1-draft**：**取消布局 C**（0AI+3 人类）；In Scope 仅 **A / B / D**
- **UI 布局规范 v1.2-draft**：删除原 0AI+3H 布局 C 全部描述；原 **D（4AI+0H）更名为布局 C**；In Scope **A / B / C**
- **UI 布局规范 v1.3-draft**：**85% 布局画布**；**720p/1080p/2160p** 默认窗尺寸表（MAIN/人类 25%、AI 6.25% 相对画布）；A/B/C 共用外框；默认=最小可等比放大；>2160p 封顶
- **布局示意图 v1.3.1**：删除旧图；`tools/gen_layout_schematics.py` 生成 **9 张**（720/1080/2160 × A/B/C 完整）；图素=画布；统一样式；每窗标注尺寸
- **布局示意图已确认**（2026-07-21）：用户确认 `docs/design/layout_schematics/` 九图与 v1.3 尺寸表；实现须对齐
- **主窗口内部布局设计 v0.1**：`docs/design/MAIN_WINDOW_LAYOUT.md` + F0015 Draft — 左右 80%/20%；TABLE 中心方形掷骰区；四角连线分下/右/上/左四玩家区；SIDE 上积分状态 / 中开关 / 下出牌日志
- **人类窗口内部布局设计 v0.1**：`docs/design/HUMAN_WINDOW_LAYOUT.md` + F0016 Draft — 左操作 67%/右扩展 33%（可向左折叠）；状态 25%+手牌 55%+设置 2 行；扩展区上 HUD 30%/下本家弃牌 70%
- **人类窗口布局已确认**（2026-07-21）：F0016 设计 **Approved**；`HUMAN_WINDOW_LAYOUT.md` 标已确认；实现另令
- **AI 窗口内部布局设计 v0.1**：`docs/design/AI_WINDOW_LAYOUT.md` + F0017 Draft — 与人类窗同 67/33 与 OP 比例；无操作条；EXT 上 AI 日志 30%/下本家弃牌 70%
- **三窗内部设计确认 + 示意图**：F0015/F0016/F0017 设计 **Approved**；统一风格布局图 `docs/design/window_interiors/{MAIN,HUMAN,AI}_interior_1080p.jpg`（外框 885×498，区尺寸标注）
- **三窗 assets 完整示意**：`tools/gen_window_mockups_from_assets.py` 用 `assets/` 翠玉青云主题合成 `MAIN/HUMAN/AI_mockup_assets_green.jpg`（1770×996，真实牌面/按钮/头像/骰子/图标）
- **主窗设计 v0.2**：`MAIN_WINDOW_LAYOUT` 玩家区从里到外 **弃牌 → 副露(2 行牌高) → 手牌(1 行牌高)**；弃牌占扇区剩余厚度
- **F0018 UI→程序修改计划**：关联四设计（UI_DESIGN_STANDARD + MAIN/HUMAN/AI 内部）与代码文件/切片 P0–P8；`docs/features/F0018_ui_design_to_code_change_plan.md`
- **资源库约定确认**：运行时 UI 图形 **唯一根目录 = 项目 `assets/`**（`AssetManager` 默认；F0018 §1.3；契约 `assets/ASSETS.md`）
- **F0018 范围澄清**：本次改造 = **布局与 UI 呈现**（分区/搬迁/展示日志）；**不改** 规则、计分、AI 决策、合法动作；任务清单见 `docs/status/UI_MODIFICATION_TASK_LIST.md`
- **F0014 重写（Draft）**：assets 风格统一；保留设置；V1/V2 布局；制图硬规则 **平面 2D + 独立进程窗**
- **F0014 设计图套装 `flat_*`**：独立窗 5 张 + 布局 2 套于 `docs/design/f0014/`
- **F0014 元素全表**：对照 `seat_window.py` 列出 A1–A13 / B1–B18；完整模式全量；精简仅默藏本家弃牌(B16)+允许降密
- **F0014 T7/T8 同窗延展 + 图一体**：完整/精简不换窗只延展高度；组件包统一；有效图 `kit_style_strip` `win_human_modes` `win_ai_modes` `win_main` `layout_V1_unified` `layout_V2_unified`

### 流程规则

- **强制每步文档落盘 / 跨机基线**：每轮结束必须覆盖写 `docs/status/LATEST.md`；有实质交付追加 `changelog`；新 session 读序 LATEST → changelog → 相关规格。写入 `Agents.md` 规则 7、`docs/DEVELOPMENT.md` §2.2、`docs/status/README.md`

### 文档 + 实现

- **F0012 可听进张显示**：独立全宽「可听进张」条（32–40px 牌面、自动换行），修复原单元格内 mini≤22px 且按手牌宽裁切导致过小/不全；规格 `docs/features/F0012_seat_discard_recommend_marks.md`
- **F0013 座位窗脏更新 / 控件复用**：手牌·弃牌 layout 稳定时 `_update_tile_face` 原地改牌面；副露 meld_key 不变不重建；Hub `broadcast` 内容签名 + 60ms 节流；Win/Mac 共享逻辑。规格 `docs/features/F0013_seat_dirty_update.md`；测试 `tests/test_f0013_dirty_update.py`
- **F0013 实测修复**：对手 HUD `refs["seat"]` 被 Label 覆盖导致 `_update_opponent_hud_inplace` TypeError；改为 `seat_id` 存座位号；补 `_render_state` 手牌/弃牌/分数原地复用回归测

## 2026-07-13

### 实现

- **座位窗刷新防闪烁（加强）**：手牌指纹**剔除**对手分数/手牌数；对手 HUD 结构稳定时仅 in-place 改文字；选中高亮**不放大、不改 padding**；content width 缓存
- **F0012 座位窗推荐出牌标记**：`discard_recommend.py`；非听最多 3 张 / 听牌则全部可听张；角标序号；焦点显示进张（万筒条序）；**剩余张数在进张牌面上方**（不遮挡）；换三张按手牌索引；手牌 in-place 更新 + 进张条预留高度减闪烁
- **策略预设 + 座位窗「当前策略·S2」**：`configs/strategies/presets.json`、`current_s2.json`（导出 F0010-S 常量）；`players/strategy_presets.py`；`registry` 支持 `current_s2`（rule_ai + F0011）；观战座 AI 策略三选：规则 / 随机 / **当前S2**（下局生效）；CLI `--players current_s2,...`

## 2026-07-12

### 文档

- **set50 确认 S2 mid**：`set50-20260713_123456` mid **0.494**（与 set20 S2 0.493 齐）；set20「+1.7」含 S1 回弹，相对 S 前 set50 锚点约 **+0.5pt**，**不可按 +1.7 宣传**
- **F0010-S S2**：J4 连续 sh 恶化软罚×0.4；late S-TRUST（\|sh−target\|>1.5 衰减 sh 项）；S2 假近听×0.55；blend 保持 0.24。set20 overall **0.505** mid **0.493**（较 S1 +F1），MAE 2.20 **未达** ≤1.85
- **F0010-S S0+S1**：`Approved`；S0 诊断字段（MAE 相位/假近听/signed/best-hyp）；S1 late 假近听软杀+结构下限+采样/精炼/重生重试；set20 overall 0.501 late 0.512 MAE 2.16（MAE 门禁未达）；诊断 `docs/status/F0010_S_shanten_diagnostics.md`
- **F0010-S 向听质量计划**：`docs/features/F0010_S_shanten_quality_plan.md`

### 评估

- **Discard accuracy 指标**：`players/analysis/discard_accuracy.py`；`eval_hand_predict` 每决策写 `discard_acc.jsonl`；set20 top1 **0.438** / top3 **0.716** / expert 一致 **0.718**（随机弃牌标签，≈baseline 0.43，**非**文献人类 68–88%）；set50 top1 **0.440**；见 `docs/status/discard_accuracy_set20_set50.md`
- **F0010 set50（blend 0.76/0.24）**：`set50-20260713_100802` overall **0.511** / Top1 **0.435**；mid 0.489 / late **0.521** / deep 0.592；vs 0.70/0.30 set50 overall 持平、late +0.2pt；见 `docs/status/set50_comparison.md`
- **F0010-ML L3 blend 调参**：`LATE_BLEND` 0.70/0.30 → **0.76/0.24**；set20 overall **0.503** / late **0.506** / mid **0.491**
- **F0010 固定 set50 确认（0.70/0.30）**：`set50-20260712_154251` overall **0.512** / mid **0.495**；见历史对照
- **F0010 100 局评估**：seed=42；best F1=0.512，Top1=0.435，lift=+0.139；详见 docs/status/F0010_predict_accuracy_100games.md

### 实现

- **F0010-ML L3（排序）**：规格 `F0010_L3_ranking_plan.md`；late T=0.35 / mid T=0.50；MMR 0.55/0.40/0.15；late blend 0.70/0.30；`_dump_compliance_mult`。`--set 20`：overall 0.501 / Top1 0.422 / late best 0.504；rank1=best **45.4%**（L2 44.0%）；best/Top1 略低于 L2（噪声带），门禁 mid/early/deep 通过
- **F0010-ML L2（向听/结构）**：规格 `F0010_L2_shanten_structure_plan.md`；`_target_shanten` 经验表(C5b)、mid 终评关向听(G4)、late sh≥3/4 分档罚+听牌 bonus(G5)、late 结构 bonus×1.2(G1)。`--set 20`：overall **0.505**、mid **0.490**、late **0.513**（较 L2 前 +0.7/+1.1/+0.9pt）；向听 MAE≈2.16（未达 −0.2 目标，F1 优先不回滚）
- **F0010-ML M1（中期止血）**：`hand_predict.py` — mid 关闭配额(D6)、份额惩罚软化(C4c)、关高压色额外罚(C4d)、MC 均匀≥50%(H3)、prefer 强制双色且 attack 权重×0.5(B5/D3)；常量 `MID_*`。50 局对照：mid 0.454→0.456（微升，未达 0.48），late 0.539→0.542，overall 0.512→0.515，early 持平
- **F0010 固定评估集**：`configs/f0010_eval_sets.json` 嵌套 20⊂50⊂100 局，每条含 `game_id`+`play_seed`；`tools/eval_hand_predict.py --set 20|50|100`；`load_eval_set`
- **F0010-ML M2（斩色）**：`_dumped_suits` / `_streak_dumped_suits`；期望份额硬顶；采样降权；同 id 弃≥2 软罚×0.1；固定 `--set 50` mid best≈0.46、late≈0.52
- **F0010-ML L1（连续补摸）**：C1 失败→受限重生；补摸 prefer 保留色；late 连续权重 1.6/出牌 bonus 1.7；mut 10；J6；`--set 20` late≈0.515
- **F0010-DH 出牌–手牌关联**：排除定缺；前期 combo_assoc 高→降权；中后 tenpai_assoc（ukeire+向听差分，快分仅组合代理）；`--set 20` mid **0.488**、overall **0.506**
- **F0011 综合出牌顾问 A1–A6**：`integrated_discard.py`（S攻−S防+S废、remain_eff、F0010 听口危险、番 proxy）；`analyze_for_seat(use_f0011=)` / 环境变量 `F0011=1`；`tools/eval_f0011.py` 对照基线

## 2026-07-11

### 实现

- **F0010 对手牌形预测（Done）**：座位窗「对手牌预测」开关（默认关）；另三家各 **Top-5** 牌形+可信度%（由 10 改为 5 以减计算量）；全局出牌刷新；enabled 座 `oracle_hands` 算 tile F1；`hand_predict.py`
- **F0010 组数调整**：每家预测组数 10→**5**；采样 attempts 随 top_k 下调
- **F0010 算法 v2（Done）**：联合场景 `JointHandScene`（跨对手 remain 互斥）；出牌连续性 `prev_joints` + C1 打出必须在手；`StrategyBelief`（攻一门/打定缺/防守/快副露）；向听加权；座位窗缓存场景并展示场景#/策略/向听；`tests/test_hand_predict.py` 覆盖互斥与连续
- **F0010-L 预测日志与准确率分析**：座位窗每 tick 写 `logs/predict/{game_id}.jsonl`；`tools/eval_hand_predict.py` 无头评估；报告 `docs/status/F0010_predict_accuracy_analysis.md`（15 局：best F1≈0.53，Top1≈0.43，相对随机 lift≈0.16；主因排序差/早期信息少/向听误差）
- **F0010 v2.1 准确率修正**：去排序随机噪声；温度 softmax 校准 conf；弃牌时序/花色份额硬约束；结构+向听加权；连续性优先入 Top-K；开局粗粒度 UI；「牌张重合度」文案
- **F0010 v2.2 抬 F1**：相位自适应采样（早期均匀多样本 / 后期 beam+精炼+向听）；greedy MAP；花色 mode ensemble；MMR 多样 Top-K；15 局复评 early best F1 **0.41→0.48**，deep **0.60**，overall best≈**0.51**、Top1≈**0.44**

> **稳定性/多屏收尾权威摘要**（过程中曾试过 `_sdl2` 写坐标 / `display.quit` 重开等，**均因 macOS SEGV 回退**；以下为**最终保留行为**。）

### 稳定性与布局（最终状态）

#### 稳定性 / 崩溃修复

- **macOS 主程序 SEGV**：禁止使用 `pygame._sdl2.Window` 读/写位置尺寸；禁止中途 `display.quit()` 重开显示；主窗定位仅 `SDL_VIDEO_WINDOW_POS` + 主线程 `set_mode`
- **座位加载完主程序崩溃**：后台线程 `reassert_placements` 不得调用 `force_window_placement`/`set_mode`（`include_main=False`）；主窗 pin 只在 pygame 主线程
- **4AI 确认后 `UnboundLocalError`**：`work()` 内对 `players_spec` 赋值导致局部变量未绑定 → 使用 `effective_spec`
- **默认环境**：`main.py` 默认 `SDL_AUDIODRIVER=dummy`、`PYGAME_HIDE_SUPPORT_PROMPT=1`；启用 `faulthandler`；未捕获异常写 `logs/main_crash.log`

#### 窗口布局 / 多显示器

- **布局屏**：开局用 `detect_screen()`（光标/控制台当前屏）生成 `WindowPlan`；会话内锁定，ready 后不因点座位重测光标
- **主窗 pin**：仅主线程 `_pin_main_window`；座位 Tk 几何由 CLI + `set_geometry` 协议热迁移
- **玩家窗 Y 偏一整屏**：Tk 几何串禁止 `+x-y`（表示距底边）；`format_tk_geometry` 对负 Y 用 `+x+-y`；CLI `--y=-N`；映射后可做约一屏高度的漂移校正
- **座位 reassert**：macOS 只推 `set_geometry`，不碰主 pygame 窗

#### 开局 / Ready / 设置

- **4AI 开局**：先 `ready_request` 再组引擎；`_ready_wait_active` 期间禁止 poll 抢 ready；出错留在牌桌提示
- **座位设置条常显**：「自动开始」「AI 策略（规则/随机）」高对比色按钮（不依赖 Aqua Checkbutton 配色）
- **主窗封面「开始」**：取消 `btn_confirm` 背景图，改为绿底圆角实心按钮 + 白字

### 文档

- 当日复盘与终态：`docs/status/LATEST.md`、`docs/status/2026-07-11.md`
- **功能规格回写**：`F0001` §13、`F0002` §10、`F0003` §3.3.1、`F0004` 协议/流程/设置条、`F0005` §3.2/§10；`docs/features/README.md` 索引注解

### 主要代码路径

| 区域 | 路径 |
|------|------|
| 主 GUI / live | `display/app.py`、`display/lobby_view.py` |
| 几何 | `display/window_geometry.py` |
| 座位窗 / Hub | `players/seat_window.py`、`players/seat_ui_hub.py` |
| 协议 | `protocols/wire.py`、`protocols/subprocess_transport.py` |
| 入口 | `main.py` |

### 已知限制（未闭环）

- macOS 多显示器上 **SDL 对 `WINDOW_POS` 不一定总生效**，主窗可能仍留在系统默认位置；座位窗以 Tk 几何为准，二者偶发不完全重合
- 竖屏副屏负 Y / 复杂排列下仍可能需人工拖窗；漂移校正为 best-effort
- 未新增正式功能规格编号（本日以缺陷修复为主，changelog + status 为准）

## 2026-07-10

### 实现

- **4AI 开局白屏/回封面修复**：先发座位 `ready_request` 再组引擎；ready 等待期间禁止 poll 抢消息；出错留在牌桌提示而非静默回封面；竖屏工作区顶对齐减少窗口飞出
- **结算页累计得分**：顶部横幅展示各座累计分；玩家卡片标「累计 / 本局」分变（多轮会话）
- **座位窗设置面板**：标题栏「设置」可开关自动开始、选择 AI 策略（规则/随机，下局生效）；`seat_settings` 协议 + Hub 合并 players_spec
- **结算自动下一局**：四方座位均「自动开始」确认时，主窗可开「结算自动下一局」；结算页显示 3 秒后自动再来一局（多轮且未满轮数）；否则开关置灰无效
- **多局得分累计**：会话内 `_session_scores` 跨局结转；`PlayerGameRunner.starting_scores` 开局注入；座位窗局数/得分移到「当前打出」右侧以省竖向空间
- **主窗出牌区防重叠**：四家弃牌改十字分区（`Layout.river_area`），上下/左右河互不交叠，弃牌换行推进方向朝桌心
- **座位窗局数与得分情况**：显示「当前局数 第 r/n 局」与全员得分条（本家★）；`ready_request` 携带 `num_rounds`
- **4AI 模式座位窗 + 确认开始**：GUI 选 4AI 时同样启动 4 个 watch 座位窗，各窗点「确认开始」后才发牌（不再无窗自动开局）
- **全套牌面资源重制**：以 `tile_clean_{green,blue}.png` 为模版、`sample.jpg` 抠取花色，按原命名重生成万/筒/条 1–9 共 54 张（270×378）；脚本 `tools/regen_tiles_from_sample.py`
- **当前打出布局精简**：此牌剩余仅数字角标叠在牌面右下角；打出者+牌名合并一行（如「S2 打出 5万」）；牌墙总剩余单独一行
- **当前打出牌墙总剩余**：座位窗「当前打出」增加本局 `wall_remaining`（牌墙总剩余 n 张）；此牌剩余文案改为「此牌剩余」以免混淆
- **当前打出剩余张数**：座位窗「当前打出」显示该牌剩余/可见（本家手牌+全员弃牌+副露，同 analysis remain 模型）
- **F0009 座位窗选中放大 + 当前打出**：手牌选中金黄高亮并放大约 1.32×；新增「当前打出」面板展示 `last_discard` 牌面与打出者（本座/Sn）
- **F0008 结算计分牌积分明细**：`GameResult.score_events` + `build_score_ledger`；结算页按座位展示总分与每笔分变（自摸/点炮/杠/花猪/查叫，含番与对手）；终局标签与胡序摘要
- **座位窗对手状态 HUD + 本座胡牌横幅**：其他玩家以紧凑 HUD 显示定缺花色（色标万/筒/条）与是否已胡（胡序/自摸/点炮）；本座胡牌后分数行 + 红色醒目横幅「本座已胡·血战继续」；公共 view 保留 dingque/status/hu_order
- **玩家窗牌面最小尺寸 + 换行**：手牌默认最小宽 36px，禁止再缩小，一排放不下则加行；中区可滚动
- **AI 座位也需确认开始**：watch 默认 `auto_start=False`，与人类一样点「确认开始」（可勾选自动开始）
- **向听/策略面板遮挡底家手牌**：策略窗上移至底家手牌带之上；先画 HUD 再画手牌，牌面优先显示
- **F0007 主窗 UI**：手牌/弃牌统一最小 36px；随窗放大不缩小；放不下换行/换列；右侧控制面板（各座明牌、推理/策略/弃牌开关）；分区防遮挡
- **人类胡后“立刻结算”观感**：live 在人类离桌后 AI 全速打完剩余牌；`step_delay_ms` 节流行牌；主窗显示「血战继续·已胡/仍在打」；仅 `phase=finished` 才进结算
- **血战人类胡后卡死**：响应阶段缺 claim 时强制补 PASS 并 resolve；子进程 observation 非阻塞写入防管道堵死引擎；胡牌后座位窗立即提示血战继续
- **血战到底一胡不停局**：胡牌仅本座 `status=finished` 离桌；活跃≥2 时继续摸打；编排器/环境跳过已胡座位；座位窗提示「已胡牌·血战继续」
- **玩家窗牌面刷新闪烁**：observation 合并 40ms；手牌/布局指纹相同则跳过销毁重建；点选仅改样式；宽度未变不二次 relayout
- **AI 窗确认按钮不显示**：`_rebuild_action_bar` 曾对 watch 提前 return，跳过 ready UI；改为先画确认再进只读提示
- **主窗左右家牌面朝向中心**：`TableView` 左侧手牌/副露/弃牌旋转 -90°、右侧 +90°，牌顶指向桌心；间距按旋转后尺寸推进
- **座位窗牌面显示不全**：源图 ~270px 缩放过松 + 未计控件边距导致单行溢出裁切；严格缩放到布局 `tw`、`cell_extra` 换行、中间区可滚动
- **座位窗按钮底色（macOS）**：Aqua 下 `tk.Button` 忽略 `bg`，确认开始/操作钮改为 Frame+Label 实心底色（绿底白字）
- **F0006 玩家视窗响应式布局**：共享 `players/view/responsive.py`；手牌/弃牌/副露/按钮随窗宽缩放并换行；Tk 座位窗 `<Configure>` 防抖重排；PlayerView 多行手牌与 hit-test 一致
- **F0005 Windows/macOS 兼容**：`detect_screen` 按平台分发（Win32 / CoreGraphics macOS / pygame）；HWND 布局 API 仅 win32；主窗非 Win 用 pygame Window 定位；子进程强制 `encoding=utf-8` 且 `creationflags` 仅 Windows；座位窗 Mac 以 Tk geometry 为准
- **macOS 中文显示**：`draw_text` 改为优先加载本机 CJK 字体文件（STHeiti / 冬青黑 / Arial Unicode 等）并用探针拒绝「假匹配」的 Windows 字体名；座位窗 Tk 字体按系统可用族回退（PingFang SC 等），不再写死微软雅黑
- **座位窗改 tkinter**：多进程 pygame 在 Windows 上常丢 S1/S3 → `seat_window` 改用原生 Tk 窗，实测 4 座均 `placed=True`
- **点击开始卡死**：座位启动改后台线程；hello 尽早发送；主界面保持可绘
- **座位启动加固**：清继承的 `SDL_VIDEO_WINDOW_POS`；按 PID 强制置位；`window_ready` 协议
- **F0004 座位确认开始**：每局发牌前人类+AI 座位窗需点「确认开始」；「自动开始」复选框会话内记忆；`ready_request`/`ready` 协议 + `SeatUIHub.wait_all_ready`
- **F0003 游戏封面 / 保窗 / 副露**：主程序 Lobby 可设模式、换三张、轮数，点击开始才开局；一局结束不杀座位窗，Hub 复用；`PlayerView` 绘制碰杠副露；`EngineConfig.enable_exchange`；`human`/`play` 默认进封面；全量 **135 passed**
- **多显示器**：启动时检测命令所在屏幕（控制台/前台窗/光标 → MonitorFrom*），用该屏 `rcWork` 分辨率与原点布局全部窗口
- **座位窗网格布局 + 统一启动**：网格保证全在当前屏工作区内；Hub 一次启动 S0–S3
- **DPI/坐标修复**：逻辑像素工作区，禁止 DPI 混用
- **窗口布局权威流程**：`detect_screen()` → `plan_for_screen()` 共用 `window_plan`
- **F0002 布局补丁**：分区不重叠窗口几何（修 1440×900 下 S0/S3 被主窗挡住）；Hub 单座失败不中止；人类窗优先于 AI 观战窗启动
- **F0002 座位完整 UI**：人类窗可操作渲染加固；AI 座位 `watch` 子窗 + `SeatUIHub` 广播；主程序观战；`seat_window` 统一入口
- **Human 完整 UI**：`human` / `play` 含 human 时同时开主程序观战 + 玩家子窗口（后台引擎线程）；`--headless` 才纯无界面
- **Human 握手**：子进程 stdout 被 pygame 横幅污染导致 `JSONDecodeError` — 隐藏 banner、hello 提前发送、父进程跳过非 JSON 行
- **pytest 路径**：新增 `pytest.ini`（`pythonpath = .`）与 `tests/conftest.py`，避免在非根目录收集测试时出现 `No module named 'display'`（2 errors）
- **F0001 UI 窗口几何**（规格见 `docs/features/F0001_window_geometry.md`）：主窗居中、玩家窗四向、可缩放、初始化 ≤2K 工作区；`window_geometry` + layout/app/human 联动。**补记**：实现一度早于正式规格，已回写 Docs-First 权威文档
- **M11 Done**：`ChengduMahjongEnv`（类 Gym 5-tuple）+ `training/spaces.py` + 根 `README.md` + `tests/test_env.py`；全量 **114 passed**；路线图 M01–M11 收尾
- **M10 Done**：存档/加载/回放 + crash policy + CLI resume/spectate
- **M09 Done**：Human 子进程 + NDJSON transport + HumanPlayerProxy + 本家 GUI
- **M08 Done**：analysis pipeline + inference/strategy HUD + RuleAI 接入
- **M07 Done**：AssetManager + Lobby/Table/Result + InteractiveRunner + `main.py`
- **M06 Done**：BasePlayer + random/rule_ai + PlayerGameRunner
- **M05 Done**：ScoreService + Reward + JSONL
- **M04 Done**：血战行牌状态机 + legal_actions + Session
- **M03 Done**：向听 / 胡形 / 成都番型 + `fan_cap`
- **M02 Done**：换三张 + 定缺开局状态机
- **M01 Done**：牌/牌墙/game_id/掷骰定庄/发牌/状态 JSON

### 文档

- 里程碑 **M11**：`Approved` → 实现 → **`Done`**（路线图闭环）
- 里程碑 **M10**：`Approved` → 实现 → **`Done`**
- 里程碑 **M09**：`Approved` → 实现 → **`Done`**
- 里程碑 **M08**：`Approved` → 实现 → **`Done`**
- 里程碑 **M07**：`Approved` → 实现 → **`Done`**
- 里程碑 **M06**：`Approved` → 实现 → **`Done`**
- 里程碑 **M05**：`Approved` → 实现 → **`Done`**
- 里程碑 **M04**：`Approved` → 实现 → **`Done`**
- 里程碑 **M03**：`Approved` → 实现 → **`Done`**
- 里程碑 **M02**：`Approved` → 实现 → **`Done`**
- 里程碑 **M01**：`Approved` → 实现 → **`Done`**
- 确立 **Docs-First** 开发规范：`docs/DEVELOPMENT.md`、`AGENTS.md`、收尾报告 §2.1
- 系统总设计基线：`PLAN.md`
