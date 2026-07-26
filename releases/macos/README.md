# macOS 发布产物（本机）

| 文件 | 说明 |
|------|------|
| `ChengduMahjongAITrainer-Nuitka.app` | Nuitka 构建的应用包 |

- 构建命令：`bash tools/packaging/build_nuitka_macos.sh`（输出到 `dist/nuitka/`，并可同步到此目录）
- **运行注意**：若完整路径含中文（如 OneDrive「共享的库」），Nuitka 可能 abort。请复制到 `/Applications` 或桌面后再双击。
- 本目录默认不随 git 提交大体积 `.app`（见根目录 `.gitignore`）。
