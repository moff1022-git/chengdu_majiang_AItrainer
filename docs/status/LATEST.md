# 进度快照

更新时间：`2026-08-03`

当前应用版本：`0.3.1`

## 本轮完成

- **F0038** 修订方案 C：**C1 为采集主路径**（用户认定 C0 整副手录无实操性）。
- 新增 **§4.4.11 C1 详细实现路径**（Layout Profile、截帧、检测/分类、河差分、副露、置信降级、M0–M6、工作量）。
- 文档：[`docs/features/F0038_online_platform_ai_bridge.md`](../features/F0038_online_platform_ai_bridge.md)
- **无业务代码**。

## 下一步队列

1. 指定首发目标客户端 + 分辨率 → `确认 F0038 C1` / `目标客户端：…`
2. Approved 后开实现规格 F0039 + 编码 C1-M0（schema/Policy/HUD）
3. C1-M1 标定工具 → M2 手牌识别 → M3 河 → M4 副露 → M5 串联
