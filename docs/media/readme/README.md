# README 界面截图

固定文件名，供根目录 [`README.md`](../../../README.md) 功能章引用。

| 文件 | 场景 |
|------|------|
| `01_lobby.png` | 大厅 |
| `02_main_play.png` | 主窗口（游戏中） |
| `03_human_play.png` | 人类玩家（游戏中） |
| `04_ai_watch.png` | AI 玩家（游戏中） |
| `05_result.png` | 计分 / 结算窗口 |
| `MANIFEST.json` | 生成元数据（版本、时间、方法） |

## 刷新

```bash
.venv/bin/python tools/capture_readme_screenshots.py
# macOS 有「屏幕录制」权限时，座位窗可真抓：
.venv/bin/python tools/capture_readme_screenshots.py --prefer-seat-grab
```

规则见 [`docs/features/F0026_readme_screenshots.md`](../../features/F0026_readme_screenshots.md)。  
**发版或 UI 变更后必须重刷并提交本目录。**
