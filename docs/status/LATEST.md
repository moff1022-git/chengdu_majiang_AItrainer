# 进度快照

> 2026-07-26 — **F0027 Windows MSI 安装包已生成**

## 本轮

| 项 | 说明 |
|----|------|
| 规格 | F0027 WiX MSI · **Done** |
| 脚本 | `tools/packaging/build_msi_windows.ps1` |
| 模板 | `packaging/windows/msi/Product.wxs` |
| 产物 | `dist/msi/ChengduMahjongAITrainer-0.2.1-windows-x64.msi`（**31.4 MB**） |
| 安装 | 管理员 `msiexec /i …msi` → Program Files + 开始菜单 |

## 构建

```powershell
.\tools\packaging\build_msi_windows.ps1            # 可自动先打 PyInstaller
.\tools\packaging\build_msi_windows.ps1 -SkipPyInstaller
```

## 下一步

| 序 | 动作 | 建议触发语 |
|----|------|------------|
| 1 | 本机安装验收 M1–M5 | 双击 msi |
| 2 | 上传 MSI 到 Release v0.2.1 | `发布 MSI` |
| 3 | 提交 F0027 代码 | `提交 F0027` |
