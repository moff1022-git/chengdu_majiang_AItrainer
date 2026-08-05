# F0060 worker内存模型校准

- 日期：2026-08-05
- 平台：macOS arm64 / Python 3.12

## 证据

|样本|执行器/workers|主进程RSS|子进程单体最大RSS|保守总峰值|
|---|---|---:|---:|---:|
|固定100局|serial/1|61.344 MiB|—|61.344 MiB|
|固定100局|process/2|34.578 MiB|51.250 MiB|137.078 MiB|

## 校准结论

- `DEFAULT_WORKER_MIB=96`相对实测单子进程51.25 MiB保留约1.87倍安全系数，当前无需下调。
- worker计算继续取用户请求、CPU、pending、`memory_budget_mib // 96`最小值。
- CI不运行100局性能门禁；Linux基线待独立采样，未有证据前沿用96 MiB保守值。
- 建议预算：workers 2至少256 MiB；workers 4至少512 MiB；完整trace另预留主进程和文件缓存空间。
