# Windows 发布产物（本机 · 不进 git）

应用版本以仓库根目录 [`version.py`](../../version.py) 为准（当前构建应对齐 **0.2.1**）。

| 目录 / 文件 | 说明 |
|-------------|------|
| `ChengduMahjongAITrainer-PyInstaller/` | PyInstaller onedir（`build_pyinstaller_windows.ps1`） |
| `ChengduMahjongAITrainer-Nuitka/` | Nuitka standalone（`build_nuitka_windows.ps1`） |
| `ChengduMahjongAITrainer-*-windows-x64.msi` | **MSI 安装包**（`build_msi_windows.ps1` · F0027） |

## 构建

在 **Windows** 上、仓库根目录：

```powershell
.\.venv\Scripts\python.exe -c "from version import APP_VERSION; print(APP_VERSION)"
.\tools\packaging\build_pyinstaller_windows.ps1
# 可选（需 MSVC / MinGW）:
.\tools\packaging\build_nuitka_windows.ps1
# MSI（需先有 PyInstaller onedir；首次下载 WiX 3.14）:
.\tools\packaging\build_msi_windows.ps1
```

或双击：`tools\packaging\build_pyinstaller_windows.bat`

完整说明：[docs/packaging/WINDOWS_BUILD.md](../../docs/packaging/WINDOWS_BUILD.md)

## 运行

```powershell
.\releases\windows\ChengduMahjongAITrainer-PyInstaller\ChengduMahjongAITrainer.exe
.\releases\windows\ChengduMahjongAITrainer-PyInstaller\ChengduMahjongAITrainer.exe --version
```

日志：`%APPDATA%\ChengduMahjongAITrainer\logs\`

## 注意

- **必须在 Windows 上构建**（不支持 macOS 交叉编译）
- 建议构建路径尽量 **ASCII**（中文 OneDrive 路径可能踩坑）
- 未签名 → SmartScreen 可能提示「未知发布者」
- `*.exe` 与 `releases/windows/**` 大目录已被 `.gitignore`；本 README 可提交
