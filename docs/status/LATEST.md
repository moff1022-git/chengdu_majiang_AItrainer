# 进度快照

更新时间：`2026-08-03`

当前应用版本：`0.3.1`

## 本轮完成

- GitHub 首页 README 已按 v0.3.1 当前能力整体重写，移除过时的 v0.2.1 下载、玩家列表和命令说明。
- 首页提供 PyInstaller、Nuitka 两个 macOS arm64 发布包和 SHA-256 清单的直接下载入口。
- PyInstaller、Nuitka 构建脚本及可选 PyInstaller spec 永久补收 `players/humanlike/parameter_registry_v2.json`。
- 两个构建脚本增加强制门禁：App Bundle、`assets/`、`configs/`、参数注册表或 CLI 冒烟任一失败即终止构建。

## 验收锚点

- `tests/test_app_paths.py`：`7 passed`。
- PyInstaller App：`--version`、`--seat-window --help` 和三类资源检查通过。
- Nuitka App：`--version`、`--seat-window --help` 和三类资源检查通过。
- v0.3.1 clean-source 发布基线：`500 passed, 1 skipped, 0 failed`。
- Release：`https://github.com/moff1022-git/chengdu_majiang_AItrainer/releases/tag/v0.3.1`

## 状态与风险

- v0.3.1 macOS arm64 双构建已发布；未进行 Apple Developer ID 签名或公证。
- Nuitka 产物建议从 `/Applications` 等纯英文路径运行。
- Windows 最新预构建包未纳入本轮发布，README 未宣称存在 v0.3.1 Windows 包。

## 下一步队列

1. 在目标 arm64 Mac 上分别完成两个 App 的真实 GUI 验收。
2. 配置 Apple Developer ID 签名、公证和最低 macOS 兼容目标。
3. 如需 v0.3.1 Windows 包，在 Windows x64 主机分别构建、验证并追加 Release 资产。
