# MODEL-001最小模拟数据生成器

状态：Implemented（模拟数据生成能力；不代表MODEL-001审计状态改变）

生成器使用生产`PlayerGameRunner`和合法动作集合。四种程序化风格只接收`PlayerView`；当前时点标签在动作执行前从restricted truth提取，终局shape仅回填`labels.jsonl`。

```powershell
python -m training.model001.generate --samples 1000 --styles conservative,balanced,aggressive,legal-random --seed 20260730 --output data/model001/model001-sim-smoke-v1
```

输出严格为`features.jsonl`、`labels.jsonl`和`manifest.json`。进程退出码非0或`manifest.valid=false`时不得用于校准。

正式生成建议：

```powershell
python -m training.model001.generate --samples 10000 --styles conservative,balanced,aggressive,legal-random --seed 20260730 --output data/model001/model001-sim-v1
```

模拟范围训练与校准指标：

```powershell
python -m training.model001.train --dataset data/model001/model001-sim-v1 --output data/model001/model001-sim-v1-artifact
```

训练器不会把artifact自动接入生产策略；没有Approved指标阈值时，`metrics.json`只记录指标而不宣称校准通过。
