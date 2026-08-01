# 00 Source Inventory

| 文档 ID | 用途 | 状态 |
|---|---|---|
| `source_inventory.md` | 来源、版本、缺失项、术语、ID、证据等级和依赖总览 | 权威 |
| `authoritative_file_manifest.md` | 锁定文档、审计/验收、源码、测试、配置与脚本的逐文件 SHA-256 | 权威 |
| `log_file_manifest.md` | 仓库内日志的单文件或目录 tree SHA-256 | 权威 |
| `source_file_manifest.md` | 首次生成时受工具输出截断影响的非完整清单 | **废弃，不得引用** |

在 Windows 沙箱恢复并允许安全删除前，保留废弃文件以避免使用非受控方式修改工作区。后续任务只能引用前三份权威文档。

