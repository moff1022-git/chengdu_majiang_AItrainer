# 进度快照

更新时间：`2026-08-03`
当前应用版本：`0.3.1`
发布基线：Git tag `v0.3.1` / commit `a0d5031f0b63fdbd831a6b39520f4e5752ad44b8`

## 本轮完成

- 在 Windows 11 x64、Python 3.12 x64 上完成 v0.3.1 Windows 兼容性测试。
- Windows 定向回归：`57 passed`。
- 全仓回归：`504 passed, 1 failed`；唯一失败为已记录的过期
  `tests/test_f0011_integrated.py::test_pipeline_f0011_flag` 合同断言，与 Windows
  兼容性和冻结构建无关。
- 修复 Windows PyInstaller/Nuitka 构建资源合同：冻结包现在包含
  `players/humanlike/parameter_registry_v2.json`；新增 3 项静态回归测试。
- PyInstaller 6.21.0 onedir 构建成功；冻结入口 `--version` 与
  `--seat-window --help` 均退出 0，PE machine 为 AMD64 (`0x8664`)。
- WiX 3.14.1 x64 MSI 构建成功；ProductName 中文正常、ProductVersion `0.3.1`、
  ProductLanguage `2052`。

## 发布资产

- `ChengduMahjongAITrainer-0.3.1-windows-x64-PyInstaller.zip`
  - SHA-256: `762C739EB1044562B07617F0728D8EDF8B836D3ED618FCB0CD53612648083B5C`
  - 大小：`40,295,251` bytes
- `ChengduMahjongAITrainer-0.3.1-windows-x64.msi`
  - SHA-256: `A0B82EF5349BB785CA45B4DAFF7D98E6E5173995A69FFBF92BDC8C57CC91E249`
  - 大小：`32,534,304` bytes
- `ChengduMahjongAITrainer-0.3.1-windows-x64-SHA256.txt`
- Release：`https://github.com/moff1022-git/chengdu_majiang_AItrainer/releases/tag/v0.3.1`

## 状态与风险

- Windows ZIP 与 MSI 自动验收通过；真实 MSI 安装/卸载未自动执行，以避免未经确认的
  per-machine/UAC 系统变更。
- Windows EXE/MSI 未做 Authenticode 签名，SmartScreen 可能提示“未知发布者”；符合
  F0025/F0027 的既定 Out of Scope。
- 0.3.1 tag 保持不变；本轮资源构建修复将作为 tag 后续提交推送到
  `release/v0.3.1` 分支，不重写已发布 tag。

## 下一步队列

1. 在干净 Windows 10/11 虚拟机中实际安装 MSI，验证开始菜单、启动、开局、日志目录和卸载。
2. 如需降低 SmartScreen 风险，配置 Authenticode 证书并对 EXE/MSI 签名后重新上传资产。
3. 将过期 F0011 合同测试迁移到当前推荐算法合同，使全仓回归恢复零失败。
4. 后续修复应发布为 `0.3.2`，不要重写 `v0.3.1` 源码 tag。
