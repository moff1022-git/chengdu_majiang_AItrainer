# F0061 GitHub pytest CI

- 状态：Done
- 日期：2026-08-05

## 目标

为`main`、集成分支和pull request增加最小、可重复的pytest门禁，避免仅依赖本地测试。

## 方案

- GitHub Actions使用Ubuntu与Python 3.12。
- 安装Ubuntu `fonts-noto-cjk`、`requirements.txt`与pytest，运行`python -m pytest -q`；CJK字体属于UI测试必要环境依赖。
- 设置`PYTHONPYCACHEPREFIX`到runner临时目录；不上传data、复盘、虚拟环境或构建产物。
- 触发范围：push到`main`、`integration/**`、`codex/**`及所有pull request。
- 使用concurrency取消同一ref的过期运行。

## 验收

- workflow YAML可解析；
- 本地全仓测试通过；
- 推送后GitHub出现对应run并完成；失败时不得误报成功。

## 批准记录

用户“执行任务1-4”明确授权设计并实现GitHub pytest CI，据此Approved。

## 验收记录

- `.github/workflows/pytest.yml`已实现Python 3.12 pytest门禁、pip缓存、并发取消和20分钟超时。
- 首次远端运行显示`513 passed, 1 skipped`且仅因Ubuntu缺少CJK字体失败；补充`fonts-noto-cjk`后重跑结果见`LATEST.md`。
