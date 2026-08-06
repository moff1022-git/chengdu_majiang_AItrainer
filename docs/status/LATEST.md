# 进度快照

更新时间：`2026-08-06`
当前应用版本：`0.3.2`

## 本轮目标与进度

- 用户已确定0.3.2版本，F0067发布规格和F0068 F0057因果A/B预注册规格均为Approved。
- 已完成Nonhuman优化过程复核：确认正式能力提升来自HumanlikeV2Player参数栈中的杠偏好与speed/hand_value权重迁移；Engine保持规则权威，相关Engine改动属于合法性、胡牌/血战/定缺与复盘一致性修复，不作为调参收益来源。
- 0.3.2内容介绍已增加`docs/releases/V0.3.2_NONHUMAN_OPTIMIZATION.md`和`V0.3.2_PERSONALITY_PARAMETER_MATRIX.md`。
- `version.py`已升至0.3.2；存档schema 5、存档格式1、座位协议1均不改变。
- 新增手动Nonhuman防回退workflow：必须提供受控GitHub artifact run/name/SHA，校验后才运行门禁并上传诊断。
- F0068冻结单参数实验：只改变公开进张贡献倍率1.00→0.00；因当前是否存在独立倍率仍需代码核查，本轮不擅改评分公式、不启动伪A/B。

## 发布依据

- F0066两个独立盲测SHA共11000局：Nonhuman−Expert `+1036`，均分`+0.09418`，95% CI `[+0.04991,+0.13755]`。
- 胡牌`+154`、自摸`+74`、花猪`-16`、点炮`-28`，防回退门禁PASS。
- F0057公开trace审计：571,186次s0决策、1,151,998候选，三字段覆盖率100%。

## 当前状态

- F0060–F0066：Done。
- F0067：In Progress；530/1回归、双编译器构建、clean归档及主提交CI `31062994354`已完成，待最终修复CI、tag和GitHub Release。
- F0068：Approved，预注册完成；实验启动依赖独立公开进张倍率的实现规格。

## 风险与限制

- 发布构建依赖本机`.venv`；OneDrive非ASCII路径可能影响Nuitka，脚本已有ASCII路径smoke策略。
- 防回退workflow默认不在push触发，避免CI下载大数据；必须由受控artifact手动触发。
- 因果A/B尚未执行，不能把F0066观察关联表述为因果。

## 下一步完整任务清单

1. 完成定向和全仓回归。建议触发语：自动执行中。
2. 使用PyInstaller和Nuitka构建0.3.2，并生成clean source/evidence与SHA。建议触发语：自动执行中。
3. 提交推送双分支、等待CI、创建v0.3.2 tag和GitHub Release。建议触发语：自动执行中。
4. 后续另立公开进张倍率实现规格并执行F0068预注册10000局A/B。建议触发语：`实现并执行F0068`。
