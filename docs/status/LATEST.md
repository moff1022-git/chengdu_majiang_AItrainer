# 进度快照

> 2026-07-26 — **发布基线 v0.2.1：文档完善 + 双包重打 + GitHub 同步**

## 本轮目标

1. 完善跨机文档基线（版本 / 功能索引 / 打包 / 变更说明）  
2. 用 **v0.2.1** 重新构建 **PyInstaller** 与 **Nuitka** macOS 包  
3. 代码与文档 **push origin/main**


## 本轮打包结果（v0.2.1 · arm64）

| 包 | 路径 | 冒烟 |
|----|------|------|
| PyInstaller | `dist/pyinstaller/` · `releases/macos/…-PyInstaller.app` | `--version` → 0.2.1 |
| Nuitka | `dist/nuitka/` · `releases/macos/…-Nuitka.app` | `/tmp` 冒烟 0.2.1 |

## 应用版本

| 项 | 值 |
|----|-----|
| **APP_VERSION** | **0.2.1**（`version.py`） |
| 存档 schema | 4 |
| 存档 format | 1 |
| 座位协议 | 1 |

## 0.2.1 相对 0.2.0 摘要

| 编号 | 内容 | 状态 |
|------|------|------|
| F0020 | 2H/3H 模式布局 B/D | Done |
| F0021 | macOS PyInstaller + Nuitka 打包 | Done |
| F0022 | 大厅/结算 UI 对齐人类窗 | Done |
| F0023 | 主窗每轮掷骰定庄动画 | Done |
| F0024 | 主窗出牌日志细化 | Done |
| — | 弃牌多行 + 隐藏滚动条 | Done |
| — | 胡牌横幅 / 副露中文 / 选中金框 | Done |

## 文档入口（换机先读）

| 路径 | 用途 |
|------|------|
| **本文件** `docs/status/LATEST.md` | 当前基线 |
| `docs/changelog.md` | 变更倒序（含 **0.2.1** 节） |
| `docs/VERSIONING.md` | 版本规则 |
| `docs/packaging/MACOS_BUILD.md` | 打包手册 |
| `docs/features/README.md` | 功能索引 F00xx |
| `docs/DEVELOPMENT.md` | Docs-First 流程 |

## 本机产物（不进 git）

| 路径 | 说明 |
|------|------|
| `dist/pyinstaller/ChengduMahjongAITrainer.app` | PyInstaller |
| `dist/nuitka/ChengduMahjongAITrainer.app` | Nuitka 构建输出 |
| `releases/macos/ChengduMahjongAITrainer-Nuitka.app` | Nuitka 项目内副本 |
| `releases/macos/ChengduMahjongAITrainer-PyInstaller.app` | PyInstaller 项目内副本（若脚本同步） |

**Nuitka**：完整路径含中文时可能 abort → 请复制到 `/Applications` 或桌面再运行。

## 构建命令

```bash
bash tools/packaging/build_pyinstaller_macos.sh
bash tools/packaging/build_nuitka_macos.sh
.venv/bin/python main.py --version   # → 0.2.1
```

## 远程

- 仓库：https://github.com/moff1022-git/chengdu_majiang_AItrainer （private）  
- 分支：`main`  

## 下一步

| 序 | 动作 | 建议触发语 |
|----|------|------------|
| 1 | 双击 0.2.1 包开一局验收掷骰/日志/弃牌 | 目视打包版 |
| 2 | 可选 `git tag v0.2.1` | `打 tag v0.2.1` |
| 3 | 可选 GitHub Release 挂 .app | `上传 Release` |
