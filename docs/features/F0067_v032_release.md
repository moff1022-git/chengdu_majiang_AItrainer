# F0067 v0.3.2 发布

- 状态：Approved
- 日期：2026-08-06
- 依赖：F0066

## 目标

将当前已通过跨种子防回退门禁的0.3.1开发基线发布为0.3.2。发布同时固化手动GitHub Nonhuman防回退workflow，生成PyInstaller、Nuitka和clean source/evidence产物，并保证版本、tag、Release、双分支与CI一致。

## 范围

### In Scope

- `version.py`唯一版本源升至`0.3.2`；schema、存档格式、座位协议不变。
- changelog增加正式`0.3.2 — 2026-08-06`版本节，LATEST与DOC_CODE_BASELINE同步。
- 新增仅`workflow_dispatch`触发的防回退workflow；证据通过GitHub artifact下载或显式URL/SHA提供，不把大数据提交Git。
- workflow先验证artifact SHA，再执行`tools/nonhuman_regression_gate.py`，上传诊断结果；无证据、SHA错误或门禁失败均不可绿灯。
- macOS分别用PyInstaller和Nuitka构建；生成clean source/evidence归档、SHA256SUMS。
- 提交并同步`main`、`integration/v0.3.1-humanlike`，等待CI后创建带注释tag`v0.3.2`和GitHub Release并上传产物。

### Out of Scope

- 不修改Nonhuman参数、规则、存档schema或协议。
- 不自动在普通push CI下载77GB trace或执行长牌局。
- 不重跑F0065/F0066固定牌局。
- 不宣称F0057观察关联为因果结论。

## 兼容性与发布内容

- 0.3.2为向后兼容PATCH；老配置和存档读取合同不变。
- README截图可跳过：本次无UI改动。
- GitHub Release正文必须列出F0066跨种子11000局结果、测试数、CI run、两个编译器产物和校验码。
- Release正文及仓库文档链接必须包含Nonhuman完整优化历程和13种人格+旧Nonhuman的7+12参数矩阵。
- 若本机编译器因环境缺失失败，应先修复构建环境；不得用source ZIP冒充应用包。

## 验收

- [x] `main.py --version`输出0.3.2，版本测试通过。
- [x] 手动workflow具备输入校验、SHA校验、门禁退出码传播和结果artifact。
- [x] 全仓pytest通过：530 passed、1 skipped。
- [x] PyInstaller与Nuitka产物均构建成功并有SHA-256。
- [x] clean source/evidence归档自校验通过。
- [ ] 双分支同步，最终CI成功（最终修复提交后回填）。
- [ ] tag `v0.3.2`与Release指向同一提交，Release资产完整。

## 回滚

发布前可撤销版本提交；发布后不移动tag，若发现缺陷按版本规则发布0.3.3。GitHub Release资产可补传但不可静默替换同名不同SHA资产。

## 构建验收记录

- PyInstaller macOS arm64：冻结程序与seat-window smoke通过，ZIP SHA-256 `768bc96a7cfb9fc03d81687629cb50d7d64ceb92ef40f3ec9928905d5ff6f6b8`。
- Nuitka macOS arm64：完整C编译、资源检查及ASCII路径smoke通过，ZIP SHA-256 `c1626970f64373372588af8265c0a68224592549b2582de6038de81be484f6cc`。
- Clean source ZIP：SHA-256 `9bfff482057a64a162abf861b24534db2b0a992bfa161a6415955485417d3c0d`。
- Evidence ZIP：SHA-256 `2d1ee3ae11fa57a5909f161044b536fcfb64e6e24cb93ba14d1446eee984a24d`。
- 版本主提交`4d131d46`的CI run `31062994354`成功。

## 批准记录

用户明确指定版本号0.3.2并要求执行任务1–4，据此Approved并自动实施。
