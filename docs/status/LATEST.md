# 进度快照

> 2026-07-26 — **F0026 README 功能五图 + 发版刷新流程**

## 本轮

| 项 | 说明 |
|----|------|
| 目标 | README 功能章增加五类界面图，并规定每次程序更新后重刷 |
| 规格 | [`docs/features/F0026_readme_screenshots.md`](../features/F0026_readme_screenshots.md) → **Done** |
| 图片 | `docs/media/readme/01_lobby.png` … `05_result.png` |
| 脚本 | `tools/capture_readme_screenshots.py` |
| 应用版本 | **0.2.1**（未升版） |
| 远程可见性 | **public** |

## 截图方法（当前）

| 图 | 方法 |
|----|------|
| 大厅 / 主桌 / 结算 | pygame 离屏真渲染 |
| 人类 / AI 座位 | 资源拼合 mockup（本机无屏幕录制权限；有权限时 `--prefer-seat-grab`） |

## 版本线

| 线 | 值 |
|----|-----|
| APP | **0.2.1** |
| schema | 4 |
| format | 1 |
| wire | 1 |
| GitHub | **public** |

## 下一步

| 序 | 动作 | 建议触发语 |
|----|------|------------|
| 1 | （可选）本机开屏幕录制后真抓座位窗 | `更新 README 截图 --prefer-seat-grab` |
| 2 | 确认 F0025 Windows 打包 | `确认 F0025` |
| 3 | 实现 Windows 打包脚本 | `实现 Windows 打包` |
