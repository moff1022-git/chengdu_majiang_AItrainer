# B1-A Effective Spec Overlay

状态：**PENDING CANONICAL PROFILE APPROVAL**

本覆盖层不修改Locked源文件；批准后对B1-A开发提供版本化有效解释。历史读取使用PARAMS1.1/CONTRACTS1/legacy-json-v1，新写使用PARAMS2/CONTRACTS2/canonical profile/rng2。SHA-256统一表述为：SHA-256，32字节，序列化为64个小写十六进制字符。Locked中的“64小写hex/64位小写hex”列为待v2更正文案，不在本任务直接修改。

DecisionResult v2使用安全seed_trace_ref；完整SeedTrace为restricted audit payload。旧回放缺rng版本固定走legacy-v1；新record必须显式rng_version=2。迁移图只能使用B1-A_migration_edges.csv登记边。
