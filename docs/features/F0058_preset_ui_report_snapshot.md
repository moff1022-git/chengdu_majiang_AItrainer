# F0058 正式人格UI与报告参数快照

- 状态：Done
- 日期：2026-08-05

## 目标

确保F0056正式Nonhuman通过统一人格入口后，设置窗口雷达与能力测试报告展示同一组解析值。报告除preset ID外增加每座受控参数快照，避免名称正确而运行参数漂移。

## 方案

- `summarize`为每个humanlike_v2座位应用指定preset到默认玩家模板，输出profile六项、GP-025四项、GP-026容量/阈值和四项权重；其他AI为null。
- Markdown增加“humanlike_v2人格预设”和“人格参数快照”两行JSON。
- 设置窗口继续以`apply_personality_preset`后的player生成雷达；测试直接验证外层12项中gang与四权重位置及原始提示值。
- 不改变游戏策略或配置schema。

## 验收

- nonhuman报告含gang `.50`、权重`.40/.20/.25/.15`；
- UI雷达数据同值；13种下拉选项仍完整；
- 非Humanlike座位快照为null；
- 相关测试通过。

## 批准记录

用户“执行任务1-6”授权补充主程序、设置窗口与报告加载/快照测试，据此Approved。

## 验收记录

- 报告JSON/Markdown已记录逐座解析后参数快照，非Humanlike座位为`null`。
- 雷达外层权重改用显式`speed/hand_value/defense/flexibility`顺序；13种预设及Nonhuman值由无GUI测试锁定。
- 定向测试`38 passed`，Humanlike扩大回归`121 passed`。
- 正式preset入口固定100局`100/100`成功：s0总分`97`、胡`34`，与F0055证据一致。
