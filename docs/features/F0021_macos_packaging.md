# F0021 — macOS 打包（PyInstaller + Nuitka）

| 字段 | 值 |
|------|-----|
| **编号** | F0021 |
| **标题** | macOS packaging with PyInstaller and Nuitka |
| **状态** | **`Done`**（2026-07-26） |
| **类型** | 工程交付：分发产物 + 路径/子进程冻结支持 |
| **文档** | [`docs/packaging/MACOS_BUILD.md`](../packaging/MACOS_BUILD.md) |
| **关联代码** | `app_paths.py`、`packaging/macos/*`、`tools/packaging/*`、子进程/资源路径调用点 |

---

## 1. 目标

| ID | 目标 |
|----|------|
| G1 | 提供 **PyInstaller** macOS 构建脚本与说明，产出可运行 `.app` / onedir |
| G2 | 提供 **Nuitka** macOS 构建脚本与说明 |
| G3 | 冻结后多座位子进程可用（`--seat-window` 再入同一二进制） |
| G4 | `assets/` + `configs/` 正确加载；日志可写 |

### Out of Scope

- Apple 公证 / 公证自动化  
- Windows / Linux 打包（可复用 entry，另文）  
- 安装包 `.dmg` 美化（可后续）  

---

## 2. 设计

```text
用户启动 ChengduMahjongAITrainer.app
        │
        ▼
  packaging entry → main.gui / play
        │
        ├─ app_paths.resource_root() → assets, configs
        ├─ app_paths.logs_dir() → Application Support/.../logs
        │
        ▼
  SeatUIHub / SubprocessTransport
        │
        └─ seat_window_command() → [exe, --seat-window, --seat N, ...]
                    │
                    ▼
              同一二进制座位窗 (Tk)
```

---

## 3. 交付清单

| 路径 | 说明 |
|------|------|
| `app_paths.py` | 资源 / 运行时 / 座位命令 |
| `packaging/macos/pyinstaller_entry.py` | 统一入口 |
| `packaging/macos/ChengduMahjongAITrainer.spec` | PyInstaller spec |
| `tools/packaging/build_pyinstaller_macos.sh` | PyInstaller 构建 |
| `tools/packaging/build_nuitka_macos.sh` | Nuitka 构建 |
| `docs/packaging/MACOS_BUILD.md` | 用户向操作手册 |

---

## 4. 验收

见 `MACOS_BUILD.md` §4。单元：`tests/test_app_paths.py`。

---

## 5. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-26 | Done | 用户要求生成 mac 版 PyInstaller + Nuitka 打包与文档 |
