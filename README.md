# 成都麻将 AI 训练器（血战到底）

基于 Python 的成都麻将（四川血战）模拟器：权威规则引擎、可插拔玩家、Pygame 界面、Human 子进程、存档/回放，以及面向强化学习的类 Gym 训练环境。

## 功能

- **引擎**：108 张（万筒条）、掷骰定庄、换三张、定缺、血战行牌、一炮多响、成都番型与可配置 `fan_cap`
- **计分 / Reward / JSONL**：可配置稠密与终局奖励，局级日志
- **玩家**：`random`、`rule_ai`、`human`（独立子进程窗口）
- **显示**：绿/蓝主题资产、牌桌 / HUD（策略与推理）
- **存档**：JSON 存档、逐步快照、崩溃策略
- **训练**：`ChengduMahjongEnv`（`reset` / `step` / `legal_actions`）+ 批跑 runner

## 环境要求

- Python **3.11+**
- **Windows** 与 **macOS** 双端支持（屏幕检测 / 座位窗 / 中文 UI，见 [`docs/features/F0005_win_mac_compat.md`](docs/features/F0005_win_mac_compat.md)）
- 依赖见 `requirements.txt`（运行时需要 `pygame`；训练 env **不**依赖 gymnasium）
- macOS 座位窗需要 **tkinter**（Homebrew：`brew install python-tk@3.12`）

## 安装（永久环境）

**权威解释器：项目根目录 `.venv`（Python 3.11+，推荐 3.12）。**  
完整说明见 [`docs/ENV.md`](docs/ENV.md)。

```bash
cd chengdu_majiang_AItrainer
bash tools/setup_venv.sh          # 创建/修复 .venv 并安装依赖
```

日常请始终用 venv，避免系统 Python 3.9：

```bash
.venv/bin/python main.py ...      # 推荐：不依赖 activate
# 或
source .venv/bin/activate
python main.py ...
```

可选：安装 [direnv](https://direnv.net/)，`direnv allow` 后进目录自动激活（见 `.envrc`）。  
编辑器：VS Code / Cursor 已配置 `.vscode/settings.json` → `.venv`。

可选依赖：`numpy`（观察向量）由 `setup_venv.sh` 尝试安装，或 ` .venv/bin/pip install numpy`。

## 快速开始

### 批跑 / 训练日志

```bash
.venv/bin/python main.py train --games 20 --players rule_ai,rule_ai,rule_ai,rule_ai --log-dir logs/demo --seed 0
# 或
.venv/bin/python -m training.runner --games 10 --players rule_ai,random,rule_ai,random --log-dir logs/demo
```

### GUI 观战 / 对局

```bash
.venv/bin/python main.py play --players rule_ai,rule_ai,rule_ai,rule_ai --theme green
```

- **多屏**：启动时检测**运行命令所在显示器**（控制台/光标），按该屏分辨率与工作区布局全部窗口  
- **主窗口 / 座位窗**：同一套 `plan`，落在当前屏工作区内（单屏区域 ≤2K），可拖拽缩放  
- 规格：[`docs/features/F0001_window_geometry.md`](docs/features/F0001_window_geometry.md)

### Human + 3 AI（主程序 + 玩家窗，完整 UI）

```bash
python main.py human --theme green
# 等价：
python main.py play --players human,rule_ai,rule_ai,rule_ai --theme green
```

会同时打开（F0002 完整 UI）：

1. **主程序窗口**：全局观战 / HUD  
2. **S0 人类窗**：操作换三张、定缺、出牌  
3. **S1–S3 AI 观战窗**：只读  

**S0 怎么操作：**

1. **换三张**：点 3 张同花色 →「确认换牌」；或 **「自动三张」**  
2. **定缺**：点 **万 / 筒 / 条**  
3. **出牌**：**双击**手牌直接打出（无确认按钮）；Enter 打出当前选中牌  
4. **碰/杠/胡**：有则点按钮；**仅能过时自动过**  

仅 headless 时加 `--headless`。

### 存档 / 观战

```bash
python main.py play --players rule_ai,rule_ai,rule_ai,rule_ai --save-dir saves
python main.py spectate --save saves/<game_id>.json
```

### 类 Gym 环境（Python API）

```python
from training.env import ChengduMahjongEnv

env = ChengduMahjongEnv(opponent_spec="rule_ai", num_players=4, seed=0)
obs = env.reset(game_id="train-demo-1")
done = False
while not done:
    legal = env.legal_actions()
    action = legal[0]  # 或策略选的 Action / dict / int 索引
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
print(env.episode_result.scores)
env.close()
```

随机策略压测：

```bash
python -c "from training.env import smoke_random_episode; print(smoke_random_episode())"
```

`step` 返回 **Gymnasium 风格 5 元组**：`(obs, reward, terminated, truncated, info)`。  
默认对手为 **`rule_ai`**；可用 `opponent_spec="random"` 或 `opponents="rule_ai,random,rule_ai"`（不含 learner 座位）。

观察字典键：`game_id`, `seat`, `phase`, `view`, `legal_actions`, `request_id`。  
可选扁平向量：`from training.env import encode_obs_vector`。

## 目录结构

```text
chengdu_majiang_AItrainer/
├── engine/           # 规则与状态机（权威）
├── players/          # BasePlayer / random / rule_ai / human
├── protocols/        # 消息、视角过滤、传输
├── display/          # Pygame UI
├── training/         # JSONL、runner、env
├── configs/          # reward / fan / crash 等
├── assets/           # 牌面与 UI 贴图
├── tests/
├── main.py
├── PLAN.md
└── docs/
```

## 规则与配置要点

| 项 | 说明 |
|----|------|
| 人数 | 2 / 3 / 4 |
| 换三张 | 必换同花色三张 |
| 定缺 | 每人一门 |
| 一炮多响 | 默认开（`multi_ron`） |
| 番封顶 | `fan_cap`（0 = 不封顶） |
| Reward | `configs/reward_default.json` |
| 崩溃策略 | `configs/crash_policy.json` |

`game_id` 决定洗牌与骰点（可复现）。详见 `PLAN.md` 与 `docs/milestones/`。

## 开发规范

- **Docs-First**：规格确认后再写业务代码（`docs/DEVELOPMENT.md`、`AGENTS.md`）
- 里程碑索引：[`docs/milestones/README.md`](docs/milestones/README.md)
- 进度快照：[`docs/status/LATEST.md`](docs/status/LATEST.md)

## 测试

在**仓库根目录**执行（不要先 `cd tests`）：

```bash
pytest tests/ -q
# 或冒烟
pytest tests/test_window_geometry.py tests/test_asset_manager.py -q
```

## 许可证

Internal / TBD
