# F0063复盘完整性、真实中断与Linux RSS

- 状态：Implemented（Linux RSS验收待CI）
- 日期：2026-08-05

## 目标

补齐F0060/F0062最后三项验收：报告证明每个成功局复盘完整；真实SIGINT不丢失已返回结果；Linux CI可独立采样RSS。

## 方案

- 成功game_id必须有独立目录内steps、audit和终局JSON；summary/report写完整/缺失数量，完成报告缺失则返回失败。
- SIGINT后停止新提交，但当前已返回结果先写games/checkpoint/report再退出130；resume按game_id补齐。
- batch增加`--humanlike-presets`四座无交互preset入口。
- GitHub Actions增加手动触发的Linux RSS smoke，不拖慢常规push pytest。

## 验收

- 真实process CLI收到SIGINT返回130，resume完成100/100且无重复game_id。
- 100个成功局trace完整100/100，报告门禁PASS。
- Linux RSS job手动运行并输出摘要。

## 批准记录

用户“执行任务1-4”明确授权真实SIGINT、Linux RSS、trace门禁和固定100局复盘，据此Approved。

## 实现与本机验收

- process真实SIGINT：14局完成后Ctrl-C，退出码130；checkpoint为14，games为14个唯一game_id；resume无交互补齐。
- 固定100局完整复盘：`fairness-20260802-fair-004`，SHA-256 `62196df40861fcfd8909246ed2f14ac4112250bdda9dbfa6563af21a2ffc9853`；100/100成功、100/100 trace完整、门禁PASS。
- 断点续跑过程中发现并修复worker `KeyboardInterrupt`向父进程逃逸，以及`--resume`错误进入交互选择的问题。
- JSON与Markdown报告均绑定测试编号、数据集SHA、复现模式、trace开关和四座人格参数快照。
- 定向测试25 passed；全仓回归522 passed、1 skipped。
