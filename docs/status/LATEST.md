# 进度快照

> 2026-07-26 — **F0022 大厅/结算 UI 对齐人类窗 · 防遮挡**

## 本轮

| 项 | 说明 |
|----|------|
| 目标 | 开始窗、成绩汇总与人类座位窗风格统一；元素合理分布不遮挡 |
| 规格 | `docs/features/F0022_lobby_result_human_chrome.md` · Done |
| 代码 | `display/ui_chrome.py`、`lobby_view.py`、`result_view.py` |
| 测试 | `test_lobby_view`、`test_result_view`（含 640×400） |

## 布局约定

```text
HEADER（深绿 + 金线）→ BODY（卡片）→ FOOTER（固定高度按钮区）
```

## 基线

| 项 | 值 |
|----|-----|
| 应用版本 | 0.2.0 |
| F0020–F0021 | Done |

## 下一步

| 序 | 动作 | 建议触发语 |
|----|------|------------|
| 1 | 本机开大厅/打完一局看结算 | `play --players human,...` |
| 2 | 若要升版号记 UI 变更 | `bump 0.2.1` |
