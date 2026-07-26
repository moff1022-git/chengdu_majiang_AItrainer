# 进度快照

> 2026-07-26 — **文档↔程序一致性审计完成（v0.2.1）**

## 本轮

| 项 | 说明 |
|----|------|
| 目标 | 全面检查文档与程序一致性并修正文档 |
| 对照表 | [`DOC_CODE_BASELINE.md`](DOC_CODE_BASELINE.md)（权威） |
| 应用版本 | **0.2.1**（`version.py`） |
| 远程 | `main` + tag **`v0.2.1`** + [GitHub Release](https://github.com/moff1022-git/chengdu_majiang_AItrainer/releases/tag/v0.2.1) |

## 已修正的主要不一致（摘要）

| 问题 | 处理 |
|------|------|
| LATEST 下一步仍写「打 tag / 上传 Release」 | 已完成；改为当前基线 |
| F0009 写「选中放大」 | 改为 **实装不放大、金框高亮**（与代码一致） |
| F0014 长期 Draft | 改为 **Done（几何移交 UI 规范）** |
| F0012/F0019 等状态措辞不统一 | 索引统一为 **Done** |
| M09「最多 1 human」 | 标注 **被 F0020 扩展（≤3）** |
| README 功能列表偏旧 | 补 2H/3H、打包、掷骰、日志、Release |

## 当前产品能力（与代码一致）

- 引擎 M01–M11：血战、计分、AI、训练 env、存档  
- 座位窗：人类/AI 多窗、ready、推荐出牌、弃牌多行、胡牌横幅  
- 主窗：大厅/结算人类风、掷骰定庄动画、细化出牌日志  
- 布局 A/B/C/D；1–3 人类  
- macOS 双包（PyInstaller / Nuitka）见 Release  

## 版本线

| 线 | 值 |
|----|-----|
| APP | **0.2.1** |
| schema | 4 |
| format | 1 |
| wire | 1 |

## 打包 / 下载

| 位置 | 说明 |
|------|------|
| **GitHub Release v0.2.1** | zip 附件（不在 Code 文件树） |
| 本机 `releases/macos/` | PyInstaller / Nuitka `.app` 副本 |

## 下一步

| 序 | 动作 | 建议触发语 |
|----|------|------------|
| 1 | 目视验收 0.2.1 包（掷骰/日志/弃牌/2H） | 开局试玩 |
| 2 | 新功能按 Docs-First 开 F0025+ | `新功能 …` |
| 3 | 可选：Windows 打包文档 | `Windows 打包` |
