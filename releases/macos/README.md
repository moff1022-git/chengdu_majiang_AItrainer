# macOS 发布产物（本机 · 不进 git）

应用版本以仓库根目录 [`version.py`](../../version.py) 为准（当前构建应对齐 **0.2.1**）。

| 文件 | 说明 |
|------|------|
| `ChengduMahjongAITrainer-PyInstaller.app` | PyInstaller 包（脚本或手动从 `dist/pyinstaller/` 同步） |
| `ChengduMahjongAITrainer-Nuitka.app` | Nuitka 包（`build_nuitka_macos.sh` 自动同步） |

## 构建

```bash
# 在仓库根目录
.venv/bin/python main.py --version    # 应为 0.2.1
bash tools/packaging/build_pyinstaller_macos.sh
bash tools/packaging/build_nuitka_macos.sh

# 可选：同步 PyInstaller 到本目录
rm -rf releases/macos/ChengduMahjongAITrainer-PyInstaller.app
cp -R dist/pyinstaller/ChengduMahjongAITrainer.app \
  releases/macos/ChengduMahjongAITrainer-PyInstaller.app
```

完整说明：[docs/packaging/MACOS_BUILD.md](../../docs/packaging/MACOS_BUILD.md)

## 运行注意

- **Nuitka**：若路径含中文（如 OneDrive「共享的库」），可能直接 abort。请：

```bash
cp -R releases/macos/ChengduMahjongAITrainer-Nuitka.app /Applications/
open /Applications/ChengduMahjongAITrainer.app
```

- **PyInstaller**：多数情况下可在中文路径下运行；若被拦截：`xattr -cr <app>`  
- 日志：`~/Library/Application Support/ChengduMahjongAITrainer/logs/`

## Git

`.app` 已被 `.gitignore`；本 README 可提交。远程仅代码与文档，不含二进制。
