# 功能变更规格目录

里程碑之外的功能增强、规则补丁、接口扩展，使用本目录。

命名：`Fxxxx_<slug>.md`（如 `F0001_window_geometry.md`）。

流程与必填章节见 [`../DEVELOPMENT.md`](../DEVELOPMENT.md) §4.2。

**强制**：状态未到 `Approved` 前**不得**编写对应业务代码（见 DEVELOPMENT Docs-First）。

| 编号 | 文档 | 摘要 | 状态 |
|------|------|------|------|
| F0001 | [F0001_window_geometry.md](F0001_window_geometry.md) | 主窗居中、玩家窗四向、可缩放、≤2K 工作区；**§13 多屏/Tk/线程安全（2026-07-11）** | **Done** |
| F0001-UAT | [F0001_user_test_plan.md](F0001_user_test_plan.md) | 用户测试方案（主 GUI + Human + 冒烟） | 方案 |
| F0002 | [F0002_seat_windows_full_ui.md](F0002_seat_windows_full_ui.md) | 人类窗可操作 + AI 座位观战窗 + 主程序；**§10 设置条（2026-07-11）** | **Done** |
| F0003 | [F0003_lobby_cover_keep_windows.md](F0003_lobby_cover_keep_windows.md) | 游戏封面/换三张/轮数；局后保窗；副露；**开始钮普通绿底（2026-07-11）** | **Done** |
| F0004 | [F0004_seat_ready_confirm.md](F0004_seat_ready_confirm.md) | 每局座位确认开始；**设置条/set_geometry/ready 顺序（2026-07-11）** | **Done** |
| F0005 | [F0005_win_mac_compat.md](F0005_win_mac_compat.md) | Win/Mac 兼容；**§10 禁用 _sdl2、后台不碰主窗（2026-07-11）** | **Done** |
| F0006 | [F0006_seat_responsive_layout.md](F0006_seat_responsive_layout.md) | 玩家视窗随窗缩放 + 牌面/按钮换行 | **Done** |
| F0007 | [F0007_main_table_ui_panel.md](F0007_main_table_ui_panel.md) | 主窗统一牌面/换行/防遮挡/控制面板 | **Done** |
| F0008 | [F0008_result_score_detail.md](F0008_result_score_detail.md) | 结算计分牌：各玩家积分明细 | **Done** |
| F0009 | [F0009_seat_select_current_discard.md](F0009_seat_select_current_discard.md) | 选中牌高亮放大 + 当前打出牌面板 | **Done** |
| F0010 | [F0010_seat_opponent_hand_predict.md](F0010_seat_opponent_hand_predict.md) | 座位窗对手牌形 **Top-5** 联合场景预测 + 连续性/策略/向听/互斥 + 准确度 + 开关 | **Done**（算法 v2） |
| F0010-ML | [F0010_mid_late_accuracy_plan.md](F0010_mid_late_accuracy_plan.md) | **中后期**准确度规则调整计划（M1→M2→L1→L2→L3） | **Approved** |
| F0010-L2 | [F0010_L2_shanten_structure_plan.md](F0010_L2_shanten_structure_plan.md) | L2 向听表/结构/G4 固化 | **Approved+Done** |
| F0010-L3 | [F0010_L3_ranking_plan.md](F0010_L3_ranking_plan.md) | L3 排序 T/MMR/blend/斩色合规 | **Approved+Done** |
| F0010-S | [F0010_S_shanten_quality_plan.md](F0010_S_shanten_quality_plan.md) | **向听/候选质量** S0–S2 | **Approved + S0–S2 Done** |
| F0010-DH | [F0010_discard_hand_assoc_plan.md](F0010_discard_hand_assoc_plan.md) | 出牌–手牌关联：前组合低相关 / 中后听牌低相关（排除定缺） | **Done** |
| F0011 | [F0011_integrated_discard_advisor.md](F0011_integrated_discard_advisor.md) | **综合出牌**：F0010×废张×remain×进张/番×防放炮（A1–A6） | **Done** |
| F0012 | [F0012_seat_discard_recommend_marks.md](F0012_seat_discard_recommend_marks.md) | 座位窗推荐出牌序号 + 听牌进张缩略图 | **Done** |
| F0013 | [F0013_seat_dirty_update.md](F0013_seat_dirty_update.md) | 座位窗脏更新/控件复用 + broadcast 节流（减闪） | **Done** |
| F0014 | [F0014_seat_layout_redesign.md](F0014_seat_layout_redesign.md) | 座位窗内容/视觉；多窗外框见 [UI_DESIGN_STANDARD](../design/UI_DESIGN_STANDARD.md) | **Draft** |
| F0015 | [F0015_main_window_interior_layout.md](F0015_main_window_interior_layout.md) | 主窗内部：左右 80/20、掷骰中心、四玩家扇区、侧栏三区 | **Done** |
| F0016 | [F0016_human_window_interior_layout.md](F0016_human_window_interior_layout.md) | 人类窗内部：67/33、操作区四段、扩展区可折叠 | **Done** |
| F0017 | [F0017_ai_window_interior_layout.md](F0017_ai_window_interior_layout.md) | AI 窗内部：67/33、只读手牌、扩展区日志+弃牌 | **Done** |
| F0018 | [F0018_ui_design_to_code_change_plan.md](F0018_ui_design_to_code_change_plan.md) | **四 UI 设计→程序修改计划**（文件清单 + P0–P8 切片） | **Done** |
| F0019 | [F0019_interior_element_scale.md](F0019_interior_element_scale.md) | **窗内元素等比缩放**（1080p 基准最小窗；布局比例不变） | **Done** |
| **F0020** | [F0020_multi_human_modes.md](F0020_multi_human_modes.md) | **2 人类 / 3 人类** 模式：布局 B/D、多 proxy、ready/decide | **Done** |
| **F0021** | [F0021_macos_packaging.md](F0021_macos_packaging.md) | **macOS 打包** PyInstaller + Nuitka；见 [MACOS_BUILD](../packaging/MACOS_BUILD.md) | **Done** |
| **F0022** | [F0022_lobby_result_human_chrome.md](F0022_lobby_result_human_chrome.md) | 大厅/结算与人类窗 UI 风格统一，分区防遮挡 | **Done** |
| **F0023** | [F0023_main_dice_roll_display.md](F0023_main_dice_roll_display.md) | 主窗每轮开局掷骰过程与结果（定庄） | **Done** |
| F0010-规则表 | [F0010_inference_rules_inventory.md](F0010_inference_rules_inventory.md) | 推理规则 ID 清单 + 可行性 | Review |

> **2026-07-11 交叉修订**：F0001 §13、F0002 §10、F0003 §3.3.1、F0004 全文补丁、F0005 §3.2/§10。日终复盘见 [`docs/status/2026-07-11.md`](../status/2026-07-11.md)。
