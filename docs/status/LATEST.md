# 进度快照

> 2026-07-26 — **MSI 安装程序问题已修复并重打**

## 本轮诊断与修复

| 问题 | 根因 | 修复 |
|------|------|------|
| 中文乱码 | UTF-8/65001 | GBK 代码页 936 |
| 安装失败 1925 | 无管理员 + 全机桌面快捷方式 | 去掉桌面快捷方式；要求 UAC elevated |
| 无向导 / 体验差 | 无 WixUI | WixUI_InstallDir + zh-CN |
| ARP 无安装路径 | 未写 ARPINSTALLLOCATION | 安装时写入 |

## 产物

- `dist\msi\ChengduMahjongAITrainer-0.2.1-windows-x64.msi`（约 31.7 MB）  
- 安装：**右键 → 以管理员身份运行**（或双击同意 UAC）  
- 目录：`%ProgramFiles%\ChengduMahjongAITrainer\`  
- 开始菜单：**成都麻将AI训练器**

## 下一步

| 序 | 动作 | 建议触发语 |
|----|------|------------|
| 1 | 卸载旧版后管理员安装新 MSI 目视 | （自行） |
| 2 | 提交并上传 Release | `提交并发布 MSI` |
