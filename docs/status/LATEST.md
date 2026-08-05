# 进度快照

更新时间：`2026-08-05`
当前应用版本：`0.3.1`

## 本轮已完成

- GitHub Actions检查：远端`codex/v0.3.1-humanlike-release`没有工作流运行记录；以本地全仓验收作为合并门禁。
- F0060受控多进程批跑设计已Approved并落盘，本轮未修改runner。
- 由于Humanlike分支与远端main历史断开，采用安全集成：从最新`origin/main@2198225d`创建`integration/v0.3.1-humanlike`，顺序cherry-pick功能提交；未使用无关历史合并。
- main已包含等效且更完整的macOS参数注册表打包修复，冲突提交判定为空并跳过。
- 集成分支全仓回归：`512 passed, 1 skipped`。
- 本地`default.json.bak`是设置保存恢复副本，`default.json.recommendation.json`是当前人类推荐算法旁车；均保留为运行状态并加入gitignore，不提交、不删除。
- 视觉采集C1数据仍不属于本仓，保持main现有清理结论。

## 当前功能基线

- F0040–F0056：Nonhuman联合验证栈Done；正式gang `.50`，权重`.40/.20/.25/.15`。
- F0057：候选shanten/dingque/ukeire/public count审计Done。
- F0058：报告人格快照和设置雷达轴合同Done。
- F0059：人类推荐F0011退役测试合同Done。
- F0060：Humanlike受控多进程批跑设计Approved，尚未实现。

## 状态与风险

- Humanlike线程并发无吞吐收益且提高RSS；正式批跑当前建议serial。
- GitHub Actions无该分支运行，因此远端CI证据缺失；本地全仓验收通过。
- 合并main只允许集成分支相对最新远端main快进，不强推。

## 下一步完整任务清单

1. 实现F0060多进程runner并验证serial/process逐局一致性。依赖：F0060 Approved。建议触发语：`实现F0060并测试`。
2. 为GitHub仓库补最小pytest Actions工作流，避免分支无CI记录。依赖：先写Approved CI规格。建议触发语：`设计GitHub pytest CI`。
3. 运行100局process workers 2性能验收，达不到吞吐门禁则保留serial默认。依赖：任务1完成。建议触发语：`执行F0060性能验收`。
