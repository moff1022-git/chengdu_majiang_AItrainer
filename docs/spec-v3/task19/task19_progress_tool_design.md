# tools/task19_progress.py 设计（未授权实现）

命令：`validate`, `summary`, `apply-delta`, `show-unit`, `show-batch`, `show-wave`, `list-blocked`, `list-next`。只解析结构化 CSV/JSON 和固定 Markdown；完整校验表头/章节/96行/枚举/公式/转换/Task17；使用临时文件、fsync 与原子替换；以 delta 唯一摘要实现幂等；拒绝开发终端提交 AUDITED。

内部缓存 `.task19_progress_state.json` 可选且非权威，必须能从 Markdown 重建；不一致时报错并以 Markdown 为准。直接测试设计覆盖 Markdown 转义、重复 delta、非法转换、错误 writer、原子失败、稳定字节输出和摘要一致性。本 Task19 不创建工具代码，`progress_tool_implementation_authorized=false`。
