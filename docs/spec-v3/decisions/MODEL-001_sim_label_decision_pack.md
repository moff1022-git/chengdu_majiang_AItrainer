# MODEL-001最小模拟数据标签决策包

状态：**APPROVED**  
决策版本：`MODEL001-SIM-LABELS 1.0.0`  
批准人：`project_owner_user`  
批准日期：2026-07-30

范围仅为MODEL-001本地模拟数据的restricted labels；不改变线上模型、规则引擎或MODEL-001审计状态。

## SIM-LABEL-001 — APPROVED A（限定范围）

`cleared_dingque`和`dominant_suit`使用策略动作执行前、同一decision event冻结的权威隐藏状态。禁止使用该事件后的动作、摸牌、墙序或终局状态回填这两个标签。只为当时仍active的对手创建样本。

`shape`不适用上述当前时点限制，按SIM-LABEL-003 C在终局回填。

## SIM-LABEL-002 — APPROVED A

`dominant_suit`统计决策时点目标对手当前暗手加公开副露的万、筒、条实体牌数，每张计1；弃牌、牌墙、未来牌不计，定缺花色不排除。只有一个花色严格最大时输出`wan|tong|tiao`；最高计数并列或三门均为0时输出`mixed`。该标签表示当前实际牌张构成，不表示主观做牌意图。

`cleared_dingque=1`当且仅当目标对手已定缺，且当前暗手中定缺花色实体牌为0；否则为0。副露不参与清缺判断，因为合法流程不会把未清缺暗牌通过未来动作倒推回当前标签。

## SIM-LABEL-003 — APPROVED C

`shape`表示本局最终形成的牌型结果。policy features仍来自原decision event的PlayerView；牌局完整结束后，允许用同一玩家终局公开手牌或模拟器终局truth回填shape，但只能写入restricted labels。

互斥优先级：`seven_pairs > pure_suit > all_pongs > standard > other`。

- 七对类优先为`seven_pairs`；
- 否则全部终局牌张及副露同一花色为`pure_suit`；
- 否则满足碰碰胡为`all_pongs`；
- 否则满足普通胡牌为`standard`；
- 未胡、未形成完整牌型、不可确认或数据不完整为`other`。

不得因shape为`other`或决策时点尚未完成而跳过样本。

## 强制目标元数据

```json
{
  "cleared_target": "CURRENT_HIDDEN_STATE",
  "dominant_suit_target": "CURRENT_HIDDEN_STATE",
  "shape_target": "EVENTUAL_TERMINAL_OUTCOME"
}
```

同一`game_id`全部样本必须使用同一稳定hash split，禁止跨train/validation/test。policy feature文件不得包含任何当前/终局truth、标签或未来字段。

## 决议影响

生成器必须先暂存当前时点features、cleared和dominant结果，完整牌局结束后按opponent seat回填shape，再原子写出features/labels。异常或未完整结束的牌局不得写入有效数据集。
