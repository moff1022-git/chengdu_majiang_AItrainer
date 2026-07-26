# 进度快照

> 2026-07-21 — **实测修复：MAIN 与人类窗「高出数个标题栏」**

## 本轮（自行运行测试）

| 项 | 结果 |
|----|------|
| Plan 高度 | MAIN == 人类（同 h、同 y） |
| Quartz 外框高度 | 同 client 时 outer **同为 +32 标题栏** |
| **真因** | SDL 主窗被 **Dock 上推** + POS 是内容顶；Tk 人类窗仍在 plan y → **顶边差约 110px** |
| 修复 | 工作区减 Dock；SDL Y + chrome；MAIN 再 pin 对齐 |
| 复测 outer 顶 | MAIN≈512 / 人类≈516（差 4px，原约 110px） |
| 测试 | `test_window_geometry` 16+ passed |

## 请验收

完全退出后重开 `main.py human`，底排 MAIN 与人类窗顶边/底边应对齐。

## 下一步

反馈「齐了」或「仍差 N px」
