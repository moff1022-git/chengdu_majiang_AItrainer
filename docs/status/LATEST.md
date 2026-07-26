# 进度快照

> 2026-07-26 — **README 截图已重刷**

## 本轮

| 项 | 说明 |
|----|------|
| 目标 | 更新 README 截图 |
| 动作 | `tools/capture_readme_screenshots.py`（座位真抓因无屏幕录制权限回退 mockup） |
| 图片 | `docs/media/readme/01–05` + `MANIFEST.json`（`generated_at` 已更新） |
| 脚本 | 修复：`--prefer-seat-grab` 改子进程，避免 pygame/Tk 同进程崩溃 |
| 应用版本 | **0.2.1** |
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
