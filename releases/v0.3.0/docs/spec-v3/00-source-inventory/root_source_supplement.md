# 根目录源码补充登记

> 原因：生成 `authoritative_file_manifest.md` 后发现根目录 `app_paths.py` 未被首轮显式范围纳入；因 Windows 沙箱暂时阻止读取型补丁，先以本补充清单登记，不修改原输入。

| 路径 | 版本 | 字节数 | SHA-256 |
|---|---|---:|---|
| `app_paths.py` | 未单独声明；随 APP 0.2.1 基线 | 5316 | `7868eb509056239e244b307d29d6181d2710590b011b47d276449c36e47eb44c` |

后续沙箱恢复时应将本行合并到 `authoritative_file_manifest.md`，并删除本补充文件。文件存在和哈希不构成实现证据。

