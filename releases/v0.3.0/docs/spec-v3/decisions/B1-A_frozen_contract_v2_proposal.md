# B1-A Frozen公共契约2.0变更提案

状态：**APPROVED**  
提案版本：`B1-A-FROZEN-V2 1.0.0`  
批准人：`project_owner_user`  
批准时间：`2026-07-30T04:43:40Z`

## 结论

本提案创建`CDMJ-CONTRACTS 2.0.0`与`CDMJ-AI-PARAMS 2.0.0`的新版本语义，不原地修改`CDMJ-CONTRACTS 1.0.0`。v1继续只读支持历史配置、存档、审计和回放；新配置和新录制必须显式使用v2。实施前规格门禁已满足，但代码、schema和迁移器仍须按本提案实现并通过测试。

## 1. 版本与判别字段

新写配置必须包含：

- `contract_version="CDMJ-CONTRACTS 2.0.0"`
- `parameter_version="CDMJ-AI-PARAMS 2.0.0"`
- `canonical_version="canonical-jcs-nfc-v2"`
- `rng_version=2`
- `algorithm_version=2`

历史对象缺少`canonical_version`时，仅当其contract/parameter/record格式属于批准前版本，读取器才映射为`legacy-json-v1`；新对象缺字段返回`SCHEMA_INVALID`。未知版本返回`VERSION_CONFLICT`或`RNG_VERSION_UNKNOWN`，不得采用当前最新版猜测。

## 2. Canonical JSON v2

处理顺序固定为：递归Unicode NFC → 检查正规化后键冲突 → RFC 8785 JCS键序、字符串转义和数字格式 → UTF-8无BOM、无额外空白 → SHA-256。

数字规则：

- int64整数使用无前导零十进制；零只能写`0`。
- 非整数使用RFC 8785引用的ECMAScript `NumberToString`最短round-trip格式。
- `-0`和`-0.0`写为ASCII字节`0`。
- NaN、正负Infinity返回`NON_FINITE`，不产生canonical bytes。
- Decimal先按字段scale以`ROUND_HALF_EVEN`量化，再移除无意义尾零并按同一number grammar输出。

Unicode规则：所有对象键和字符串值先NFC；NFC后键冲突返回`SCHEMA_INVALID`；键按RFC 8785的UTF-16 code units升序；控制字符、引号和反斜杠按JCS转义；其他字符直接UTF-8。

Hash统一定义：**SHA-256，32字节，序列化为64个小写十六进制字符。**

## 3. 配置v1/v2双轨

- v1配置只用`legacy-json-v1`复算历史hash，不允许用v2重新解释后声称hash相同。
- v2配置只用`canonical-jcs-nfc-v2`。
- v1→v2迁移是显式唯一边：先执行已批准1.0→1.1字段迁移（如适用），验证PARAMS 1.1完整字段，再添加v2判别字段并重新计算v2 hash。
- 迁移不改变业务参数值；GP-002/GP-004 `extensions`必须为`[]`；非空返回`PARAM_UNKNOWN`。
- 原文件只在全部迁移、验证和hash成功后原子替换；失败保留原文件和active config。

## 4. DecisionResult与SeedTrace可见性

v2删除策略边界上的完整`DecisionResult.seed_trace`，改为必填安全投影：

```json
{
  "seed_trace_ref": {
    "rng_used": true,
    "algorithm_version": 2,
    "rng_version": 2,
    "trace_ref": "<SHA-256 64 lowercase hex>"
  }
}
```

无随机行为时：`rng_used=false`，`algorithm_version=null`，`rng_version=null`，`trace_ref=null`。策略对象、序列化、异常、日志和缓存均不得包含`master_seed`、原始`stream_name`、原始index、原始逻辑坐标或`seed_hash`。

完整`SeedTraceV2Restricted`仅允许引擎、受限trainer controller和审计存储访问，字段为：

`game_id,algorithm_version,rng_version,master_seed,stream_name,consumer_kind,consumer_id,event_id,sample_index,seed_hash,coordinate_hash,created_at_utc`。

该载荷必须标记`sensitivity="restricted_rng"`，不得嵌入PlayerView、DecisionContext或策略DecisionResult。普通审计记录只保存`trace_ref`；受限存储以`trace_ref`关联完整记录。

## 5. RNG v2与legacy回放

- 缺少rng版本且record格式早于本提案的回放固定选择`legacy-v1`，调用现有`derive_seeds`；shuffle/dice/exchange/deal结果零变化。
- 新录制必须显式写`algorithm_version=2,rng_version=2`。
- v2随机派生使用已批准无状态逻辑坐标`stream_name,consumer_kind,consumer_id,event_id,sample_index`。
- 坐标禁止线程号、进程号、worker完成顺序、系统时间、容器位置、重试次数和共享可变index；重试复用原坐标。
- 未知流返回`STREAM_UNKNOWN`；未知版本返回`RNG_VERSION_UNKNOWN`；失败不产生部分流映射。

## 6. 配置失败与归档

- 首次启动无有效配置：不创建match或策略，返回失败。
- 热重载失败：保留active FrozenConfig、hash和目标文件；本次更新`accepted=false`并返回attempted/active hash和错误码。
- RP局末按座位归档RP-001..033不可变快照；新局不复制RP。仅RP-033可经公开信息受限学习适配器生成下一局profile输入。

## 7. 兼容、迁移与回滚

读取矩阵：v1 reader只读v1；v2 reader读v2并经显式adapter读v1；任何reader不得把v2降格成v1。历史文件不批量重写。

回滚时停止新v2写入，继续保留v2 reader；新录制切回明确legacy路径。已经写出的v2对象不得删除或用v1 hash覆盖。配置迁移前保留原文件及hash，失败直接恢复原active引用。

## 8. 验收门禁

实施必须通过：19条已批准R2 golden、v1 hash/legacy RNG零变化、v1→v2正反迁移、NFC/JCS跨进程字节golden、DecisionResult禁止字段schema测试、受限SeedTrace访问测试、100种worker调度排列、首次启动/热更原子性和真实生产链E4证据。

