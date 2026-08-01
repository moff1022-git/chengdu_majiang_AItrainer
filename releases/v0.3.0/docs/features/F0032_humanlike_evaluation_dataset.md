# F0032 Humanlike 评估数据集规划

| 字段 | 内容 |
|---|---|
| Feature ID | F0032 |
| 状态 | **Draft** |
| 类型 | 数据契约 / 评估基础设施规划 |
| 依赖 | F0028-2、F0028-5、F0028-6、F0031 |
| 目标 | 为 F0031 G2–G6 提供可复现、无泄漏、可分层的评估数据 |

## 1. 决策与目标

本数据集用于判定 Humanlike 策略的规则语义、风格可辨识度、策略强度、真人行为相似度和局间学习效果。它不是默认训练集；任何训练用途必须另行声明，并保持评估测试集永不参与训练、提示设计、规则调参或阈值选择。

数据集成功标准不是单纯“行数够多”，而是：

1. 决策时可见信息与 PlayerView v2 一致，隐藏真值物理隔离；
2. 每条动作标签均能映射到合法动作和固定 action codec；
3. 玩家、牌局和来源级切分避免同源泄漏；
4. 人数、房规、局阶段、动作类型和玩家水平有明确覆盖；
5. 来源授权、去标识化、版本和质量报告可审计。

## 2. 数据集组成

| 子集 | 来源 | 主要用途 | 是否含真人标签 | 是否可用于训练 |
|---|---|---|---|---|
| DS-Golden | 人工构造并双人复核的规则场景 | F0031 G2 语义正确性 | 否 | 否 |
| DS-Sim | 固定版本引擎生成、配对 seed 的完整对局 | G1/G3/G4/G6、回归和强度 | 否 | 可另行生成训练分片；评估分片禁止 |
| DS-Human-Pilot | 合规真人牌谱转换的试点集 | schema、映射和质量校准 | 是 | 否 |
| DS-Human-Eval | 冻结的真人评估集 | G5 正式验收 | 是 | **永不允许** |
| DS-Challenge | 低频动作、边界房规和困难上下文 | 分层失败分析 | 可选 | 否 |

各子集独立版本、独立 manifest，不把合成数据与真人数据合并计算“真人相似度”。

## 3. 权威粒度与实体关系

数据的最小分析粒度为“一名玩家在一个确定决策时点面对一个合法动作集合做出一次选择”。

```text
dataset_release
  └─ source_batch
      └─ player_pseudonym
          └─ session
              └─ game
                  └─ decision
                      ├─ policy_view       # 决策时可见
                      ├─ action_label      # 实际选择
                      └─ evaluation_truth  # 结果/隐藏真值，仅评估器可读
```

主键：

- release：`dataset_id + dataset_version`；
- game：`source_id + source_game_id_hash`；
- decision：`game_key + seat + decision_index`；
- 同一原始牌谱重复导入必须产生相同键和内容哈希，不得产生重复样本。

## 4. 文件布局与格式

建议使用可流式读取、可差异审计的 JSONL；规模达到 100 万决策后可增加 Parquet 镜像，但 JSONL 规范视图仍为权威交换格式。

```text
datasets/humanlike_eval/<dataset_id>/<version>/
  DATA_CARD.md
  manifest.json
  schema.json
  splits.json
  checksums.sha256
  public/games.jsonl
  public/decisions.jsonl
  restricted/evaluation_truth.jsonl
  reports/quality_report.md
  reports/coverage.json
```

真人原始文件不进入 Git。仓库只允许提交 schema、极小的合成/去隐私夹具、manifest 模板和质量报告；正式数据使用受控外部存储，并以内容哈希引用。

## 5. Manifest 与版本契约

`manifest.json` 必填：

| 字段组 | 必填内容 |
|---|---|
| 标识 | dataset_id、dataset_version、created_at、status、content_hash |
| 来源 | source_type、provider、license_or_consent_id、collection_period、jurisdiction |
| 兼容 | app_version、state_schema_version、player_view_version、action_codec_version、training_contract_version |
| 规则 | ruleset_id/version、人数、受支持房规及未知项 |
| 规模 | games、decisions、players、sessions、各 split 数量 |
| 转换 | importer_version、normalization_version、label_mapping_version、转换日志哈希 |
| 隔离 | split_policy、salt_id、restricted_truth_location、access_classification |
| 质量 | quality_status、failed_checks、waivers、reviewer、approved_at |

采用语义版本：schema 或标签语义不兼容升级 major；新增兼容字段升级 minor；只修元数据且不改变样本升级 patch。已发布版本只读，修复必须发新版本。

## 6. 决策记录 schema

### 6.1 公共标识与上下文

| 字段 | 类型 | 要求 |
|---|---|---|
| dataset_version | string | 非空 |
| decision_id | string | 全局唯一、稳定哈希 |
| game_key | string | 去标识化外键 |
| player_key | string | 带受控 salt 的稳定伪名；不可反推账号 |
| session_key | string/null | 同一连续场次稳定；来源无此概念时为空并注明 |
| seat | int | `[0, player_count)` |
| decision_index | int | 同一 seat/game 严格递增 |
| decision_type | enum | exchange、dingque、discard、pong_response、gang_response、hu_response、combined_response |
| player_count | int | 2、3、4 |
| ruleset_id | string | 必须能回连冻结房规 |
| event_time_bucket | string/null | 只保留批准粒度；默认月份，不保留精确时间 |

### 6.2 `policy_view`

- 权威结构为 PlayerView v2 的规范序列化；外部牌谱无法完整还原时，逐字段记录 `observed / inferred / unavailable`；
- `legal_action_ids` 使用 action codec v2；必须非空且无重复；
- `chosen_action_id` 必须属于 `legal_action_ids`；
- 手牌、公开弃牌/副露、牌墙计数、定缺、当前阶段等字段须通过引擎一致性校验；
- 禁止包含他家暗牌、未来摸牌顺序、最终结果、事后计算标签和原始玩家标识；
- 缺少任何计算 G5 所需的核心字段时，该决策不得进入正式 DS-Human-Eval，只能进入 quarantine。

### 6.3 `action_label`

| 字段 | 说明 |
|---|---|
| raw_action | 来源中的原始动作，仅受限转换区暂存 |
| normalized_action | 规范动作类型和牌面，不使用实体 copy ID 区分同牌动作 |
| action_id | action codec v2 ID |
| mapping_status | exact、deterministic_normalized、ambiguous、unsupported |
| response_window_complete | 是否能证明当时全部合法响应已知 |
| decision_time_ms | 可空；只有来源时间戳可信且定义明确时填写 |
| label_weight | 正式集固定为 1；探索性纠偏权重另表保存，不覆盖原标签 |

`ambiguous`、`unsupported` 或响应窗口不完整的记录不得进入相应动作的 NLL/Brier 正式指标。

### 6.4 `evaluation_truth`（受限层）

可保存完整终局结果、净分、番型、他家暗牌或后续事件，用于结果分层和离线诊断。该表必须独立文件、独立读取接口；策略评估调用链不得接收此对象。正式评测要记录“policy-only 输入字段快照哈希”，证明真值未进入决策。

## 7. 数据来源准入

真人来源按优先级：用户明确捐赠并授权的完整牌谱、拥有再利用授权的平台导出、经伦理/法务确认的研究数据。公开可访问不等于允许再分发或模型评测。

每个来源进入转换前必须确认：

- 授权覆盖离线评测、派生指标、保存期限和跨地区处理；
- 能否保留稳定但不可逆的玩家伪名，以支持玩家级切分；
- 规则、人数、动作顺序和合法响应是否可重建；
- 是否包含机器人、托管、断线或作弊样本的标识；
- 撤回机制能否定位并在下一版本删除相应数据。

无法证明授权或规则语义的来源一律不进入 DS-Human-Eval。

## 8. 切分与防泄漏

| 规则 | 要求 |
|---|---|
| 玩家隔离 | 同一 `player_key` 只能出现在 train/dev/test 之一 |
| 牌局隔离 | 同一 game 的所有座位和决策必须在同一 split |
| 会话隔离 | 可识别 session 时整段进入同一 split |
| 来源隔离审计 | 报告各来源在各 split 占比；单一来源不得只存在于 test 而无可比 dev 基线 |
| 时间外推 | 另建 future-test，时间晚于 train/dev；不替代玩家隔离 |
| 近重复隔离 | 对初始牌面、公开事件序列和结果构造指纹；近重复组不得跨 split |

建议比例 train/dev/test = 70/15/15，仅适用于未来获批的训练数据。DS-Human-Eval 本身是冻结 test；为阈值校准另建不重叠 DS-Human-Pilot，严禁从正式 test 回填 pilot。

## 9. 覆盖设计与规模路线

### 9.1 首期强制分层

- 人数：2/3/4 人分别报告；正式 L4 结论仅覆盖达到最低样本的组；
- 决策类型：discard 与 response 分开；pong、各类 gang、hu、pass 单列；
- 局阶段：早/中/晚，以剩余牌或事件序号的冻结定义分层；
- 状态：定缺花色是否清完、是否听牌、是否已有副露、是否面临多响应；
- 房规：规则版本和关键开关分层，不合并语义不同的房规；
- 玩家：来源允许时按稳定等级/分段分层，未知不得假定为“普通玩家”。

### 9.2 阶段规模

| 阶段 | 目标规模 | 出口条件 |
|---|---|---|
| P0 schema fixture | 20 局、≥300 决策，全部合成或明确授权 | round-trip、合法动作、隔离测试通过 |
| P1 Human Pilot | ≥200 局、10,000 决策、30 玩家 | 达到 F0031 G5 最低探索规模；完成盲审和质量基线 |
| P2 Frozen Eval v1 | 建议 ≥2,000 局、100,000 决策、200 玩家 | 核心层均达到有效样本；CI 满足 F0031 宽度要求 |
| P3 扩展 | 按缺口扩充房规、水平和低频动作 | 不以重复常见出牌替代稀有层覆盖 |

P2 是规划目标，不是无数据依据的硬性承诺。正式所需规模由 P1 的动作频率、方差和置信区间功效分析最终确定。

## 10. 数据质量门禁

| 维度 | 正式集门槛 | 严重级别 |
|---|---|---|
| 主键唯一 | decision_id、game_key+seat+decision_index 重复率 0 | Critical |
| 必填完整 | 核心标识、规则、policy_view、合法集、chosen action 完整率 100% | Critical |
| 标签合法 | chosen_action ∈ legal_action_ids =100% | Critical |
| PlayerView 泄漏 | 禁止字段出现次数 0 | Critical |
| 牌局一致性 | 守恒、阶段、动作序列和结果可重放通过率 100%；不可重放来源须用批准的等价校验并单列 | Critical |
| 切分泄漏 | 玩家、牌局、session、近重复跨 split 数 0 | Critical |
| 精确映射率 | exact + deterministic_normalized ≥98%；其余隔离，不强行填充 | High |
| 规则可识别率 | 正式样本 100% 绑定 ruleset；未知样本不进入正式集 | Critical |
| 来源集中度 | 最大来源占比报告；>60% 触发偏差审查，不自动判失败 | Medium |
| 覆盖 | F0031 所声明核心层均达到预注册最小有效样本 | High |
| 时间可信度 | 仅对启用思考时长指标的来源要求非负、时钟定义一致、异常率 <1% | High |

质量检查按来源、人数、房规、月份和 split 分层报告，不能只给总体比例。任何 Critical 失败使该 release 不可用于正式验收；豁免必须记录理由、影响范围、批准人和到期版本。

## 11. 标注、复核与争议处理

- 规则/动作转换器先自动标注，再对每个来源随机双人复核至少 200 个决策；
- 稀有动作、映射异常和所有 DS-Challenge 样本 100% 人工复核；
- 双人不一致交由第三人仲裁，保存原判断、理由和最终标签；
- P1 要报告动作映射一致率 Cohen's kappa，目标 ≥0.95；低于门槛先修规则手册和转换器；
- 修订已发布标签必须升级数据版本，不原地覆盖。

## 12. 隐私、安全与治理

- 原始账号、昵称、IP、设备、聊天、地理位置和精确时间默认删除；
- player_key 使用受控 salt 的不可逆 HMAC；salt 不进仓库，访问者不能跨数据集关联；
- restricted 层最小权限、访问日志、静态加密；导出只允许聚合指标或批准的去隐私样本；
- Data Card 记录目的、允许/禁止用途、已知偏差、保存期限、撤回和联系人；
- 每个版本指定 Data Owner、Rules Owner、Privacy Reviewer 和 Evaluation Owner；
- 删除请求通过受控映射定位，在下一 patch/minor 版本删除并更新 hash 与审计记录。

## 13. 产物与自动化检查

批准后建议新增：

- `docs/data/HUMANLIKE_EVAL_DATASET.md`：操作手册和数据卡模板；
- `schemas/humanlike_eval_dataset_v1.json`：机器可读 schema；
- `tools/datasets/import_humanlike_log.py`：来源适配器接口；
- `tools/datasets/validate_humanlike_dataset.py`：质量、泄漏、切分和覆盖检查；
- `tests/datasets/fixtures/`：极小合成夹具，不含真人数据；
- `tests/datasets/test_humanlike_dataset_contract.py`：schema/映射/隔离回归。

报告必须输出 Passed / Failed / Quarantined，以及每项分母、分子、比例、分层和样本 ID 清单；不得只输出一个 quality score。

## 14. 批准后的实施切片

| 切片 | 动作 | 产出 | 依赖 |
|---|---|---|---|
| F0032-1 | 冻结 schema、动作映射和 Data Card | schema v1、模板、20 局合成夹具 | F0032 Approved |
| F0032-2 | 实现验证器和 split builder | 自动质量报告、泄漏测试 | F0032-1 |
| F0032-3 | 构建 DS-Golden / DS-Sim manifest | G2/G3/G4 可消费的数据发布 | F0032-2 |
| F0032-4 | 接入一个已授权真人来源并建 P1 | DS-Human-Pilot、偏差/功效报告 | 数据授权、规则映射 |
| F0032-5 | 冻结 DS-Human-Eval v1 | 只读 test、hash、访问控制 | P1 达标、阈值复核批准 |

## 15. 当前边界与批准条件

- [ ] 确认 F0032 是评估数据契约，不默认授权模型训练；
- [ ] 指定成都麻将权威 ruleset 与房规矩阵；
- [ ] 指定首个候选真人数据来源及授权负责人；
- [ ] 确认 P1/P2 规模是最低探索量与规划量，不代表已获得数据；
- [ ] 确认哪些玩家水平、人群和房规允许进入对外结论；
- [ ] 确认 restricted truth 的存储位置、保留期和访问角色；
- [ ] 状态由 Draft 更新为 Approved 后，方可创建 schema、导入器或正式数据。

当前仓库没有经本规格验证的真人评估数据。因此本规划不能改变 F0031 G5 的 **Not Evaluated** 状态，也不构成对任何数据来源授权有效性的判断。
