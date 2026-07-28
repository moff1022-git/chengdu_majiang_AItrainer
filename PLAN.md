# 成都麻将 AI Trainer — 详细设计 Plan

> **状态**：**M01–M11 已 Done**；后续功能走 `docs/features/Fxxxx`（**Docs-First**）  
> **应用版本**：见根目录 [`version.py`](version.py)（发布线 **0.2.1+**）  
> **规则**：四川成都麻将 · 血战到底（含换三张、一炮多响、定缺）  
> **技术栈**：Python 3.11+ · Pygame（主窗）· Tk（座位窗）· NumPy（可选）· JSON/JSONL  
> **资源**：项目根目录 `assets/` + `assets/ASSETS.md`（双主题 green/blue）  
> **开发流程**：[`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) · 进度 [`docs/status/LATEST.md`](docs/status/LATEST.md) · 一致性 [`docs/status/DOC_CODE_BASELINE.md`](docs/status/DOC_CODE_BASELINE.md)
> **当前功能主线**：F0028-1–4 Done；F0028-5 决策审计与确定性回放子规格 Approved，进入实现。
---

## 0. 目标与非目标

### 0.1 目标

| 目标 | 说明 |
|------|------|
| 可复现牌局 | 相同 `game_id` → 相同洗牌与初始手牌（种子派生） |
| 完整规则引擎 | 定缺、碰/杠/胡、血战到底、流局、计分 |
| 主程序 / 玩家分离 | 主程序管规则与全局；`players/` 可插拔决策模块 |
| 多入口接入 | CLI 参数、图形大厅、主程序 API 调用 |
| 分析推理 | 向听、剩余牌概率、危险度、策略建议（UI 对齐 assets） |
| 训练友好 | headless、自定义 Reward、完整逐步日志 |
| 健壮性 | 玩家崩溃可配置：终止重开 / 替换玩家 |

### 0.2 非目标（首版不做）

- 网络多人实时对战服务器（可后续扩展 IPC/socket）
- 真实强化学习训练循环（只做 **环境 + 日志 + Reward 接口**，不内嵌 torch 训练）
- 音效资源（仅预留图标状态，无音频文件）

### 0.3 已确认的产品决策（Review 拍板）

| # | 议题 | 决议 |
|---|------|------|
| 1 | 定庄 | **骰子决定**（`assets/dice` 展示）；骰点由 `game_id` 派生 seed，**可复现**；整局以 **独立 `game_id`** 持久化（存档/日志/复盘键） |
| 2 | 一炮多响 | **默认开启**（可配置关闭） |
| 3 | 换三张 | **首版必须实现**（开局流程固定阶段） |
| 4 | 番型 / 封顶 | 按 **成都血战** 标准番型；**封顶番数可配置**（`fan_cap`，0=不封顶） |
| 5 | Human 进程 | **子进程隔离**（stdin/stdout JSON transport）；座位窗模块 `players.seat_window` |
| 6 | 2/3 人规则 | 与 4 人 **保持一致**（定缺/换三张/查叫/花猪等同逻辑，仅人数与付分对象变化） |
| 7 | NumPy | **允许**（向听、批模拟、概率计算） |
| 8 | 多 human（后增） | **1–3 人类 + AI**（F0020 布局 A/B/D）；非网络远程 |
| 9 | 定庄展示（后增） | 主窗每轮 ready 后掷骰动画（F0023）；骰点仍由 `game_id` 派生 |

---

## 1. 项目目录结构

```
chengdu_majiang_AItrainer/
├── assets/                      # 已有，432 PNG + ASSETS.md
│   └── ASSETS.md
├── PLAN.md                      # 系统总设计（本文档）
├── AGENTS.md                    # AI/助手：先文档后代码
├── docs/                        # 软件工程文档（流程权威 DEVELOPMENT.md）
│   ├── DEVELOPMENT.md
│   ├── VERSIONING.md
│   ├── changelog.md
│   ├── status/LATEST.md         # 跨机进度基线
│   ├── packaging/               # macOS 打包
│   ├── milestones/              # Mx（已全部 Done）
│   ├── features/                # Fxxxx 功能规格
│   ├── design/                  # UI 几何/内区
│   └── adr/
├── version.py                   # APP_VERSION 单一源
├── app_paths.py                 # 开发/冻结资源路径
├── packaging/macos/             # 打包入口
├── README.md
├── requirements.txt             # pygame, numpy, ...
├── pyproject.toml               # 可选
├── main.py                      # 主入口：CLI / GUI / headless 分发
│
├── engine/                      # ★ 主程序核心（权威状态）
│   ├── __init__.py
│   ├── tile.py                  # Tile 枚举、ID、花色
│   ├── deck.py                  # 108 张牌墙、洗牌（seed 绑定 game_id）
│   ├── game_id.py               # game_id 生成 / 解析 / seed 派生
│   ├── rules.py                 # 规则常量、合法动作判定
│   ├── hand.py                  # 手牌数据结构、定缺、副露
│   ├── shanten.py               # 向听数（万筒条 + 定缺）
│   ├── win_check.py             # 胡牌形判定
│   ├── fan.py                   # 番型与番数
│   ├── score.py                 # 计分结算（自摸/点炮/杠分）
│   ├── state.py                 # GameState 快照（可序列化）
│   ├── events.py                # 领域事件类型
│   ├── blood_battle.py          # 血战到底状态机
│   ├── action.py                # Action / LegalActions
│   ├── player_slot.py           # 座位槽：进程/对象封装、崩溃处理
│   ├── session.py               # 单局 Session 编排
│   ├── persistence.py           # 保存/加载牌局
│   ├── spectator.py             # 观战视图（全可见/延迟可见策略）
│   ├── reward.py                # RewardConfig + 计算
│   └── config.py                # 引擎配置
│
├── display/                     # ★ 主程序全局显示（可选开启）
│   ├── __init__.py
│   ├── asset_manager.py         # 统一资源加载（主程序与玩家共用契约）
│   ├── window_geometry.py       # F0018：85% 画布 + plan A/B/C；检测见 F0001
│   ├── layout.py / main_interior.py  # MAIN 80/20 + DICE + 四扇区条带（F0015）
│   ├── table_view.py            # 全局桌面渲染
│   ├── control_panel.py         # SIDE 中部开关
│   ├── side_scoreboard.py / play_log_panel.py / play_event_log.py
│   ├── result_view.py           # 结算
│   ├── lobby_view.py            # 大厅 / 配置
│   └── hud_common.py            # 分数数字拼接、特效横幅
│
├── players/                     # ★ 可插拔玩家模块
│   ├── __init__.py
│   ├── base_player.py           # 标准接口（抽象基类）
│   ├── human_player.py          # 人工：独立窗口交互
│   ├── rule_ai_player.py        # 规则 AI（可玩基线）
│   ├── random_player.py         # 随机合法动作（测试/自对弈基线）
│   ├── analysis/                # 分析推理（玩家侧共享）
│   │   ├── __init__.py
│   │   ├── remain.py            # 剩余牌统计/概率
│   │   ├── danger.py            # 放炮危险度
│   │   ├── opponent_model.py    # 对手听牌/手牌推测
│   │   └── strategy.py          # 弃牌建议、期望值
│   └── view/                    # 玩家视角渲染
│       ├── __init__.py
│       ├── player_view.py       # 本家视角桌面
│       ├── inference_hud.py     # assets/inference/*
│       └── strategy_hud.py      # assets/strategy/*
│
├── protocols/                   # ★ 主程序 ↔ 玩家通信契约
│   ├── __init__.py
│   ├── messages.py              # Observation / ActionRequest / Decision / Log
│   └── transport.py             # InProcess / Subprocess / (预留 Socket)
│
├── training/                    # ★ 训练支持（无显示）
│   ├── __init__.py
│   ├── env.py                   # 类 Gym 环境封装
│   ├── runner.py                # 批量自对弈
│   └── episode_log.py           # JSONL 轨迹写出
│
├── configs/                     # 默认配置
│   ├── default_game.yaml        # 或 .json
│   ├── reward_default.json
│   └── crash_policy.json
│
├── logs/                        # 运行时日志（gitignore）
├── saves/                       # 存档（gitignore）
└── tests/
    ├── test_tile_deck.py
    ├── test_shanten.py
    ├── test_win_fan.py
    ├── test_blood_battle.py
    ├── test_game_id_repro.py
    ├── test_reward.py
    └── test_persistence.py
```

### 1.1 职责边界（必须严格遵守）

| 模块 | 负责 | 禁止 |
|------|------|------|
| `main.py` + `engine/` | game_id、规则、血战流程、计分、座位管理、存档、观战、全局显示调度 | 替 AI 做策略决策 |
| `players/` | 决策、本家分析、本家窗口渲染、训练模式日志 | 直接改引擎私有状态；不得信任自己改 wall |
| `display/` | 主程序全局/观战渲染 | 不包含业务规则判定 |
| `protocols/` | 消息 schema 与传输 | 无规则逻辑 |
| `training/` | 批跑、env、轨迹 | 不复制一套规则 |

---

## 2. 四川血战到底 · 规则模型（引擎权威）

### 2.1 牌组

- 仅 **万 / 筒 / 条**，各 1–9，各 4 张 → **108 张**
- 无风牌、箭牌；**无吃（Chow）**

### 2.2 人数

- 默认 4 人；配置 `num_players ∈ {2,3,4}`（2/3 人时座位子集 + 初始分/墙不变逻辑需明确：仍用 108 张，庄家与轮转按在局人数）

### 2.3 开局流程

1. 生成/指定 **独立 `game_id`** → 派生 `shuffle_seed`、`dice_seed`
2. **掷骰定庄**（两枚骰子，点数由 `dice_seed` 决定，UI 用 `assets/dice`；同 `game_id` 结果固定）→ 庄家座位写入状态并随存档保存
3. 洗牌 → 各家发 **13 张**（庄家再摸 1 成 14，庄先打）
4. **换三张**（首版必做）：各家选 3 张交换；交换方向由规则配置（默认：按骰点/约定方向，可配置顺时针/逆时针/对家），全程可复现
5. **定缺**：每家选择缺一门（万/筒/条）；手牌中缺门未打完前 **不能胡**

### 2.4 行牌

- 摸打循环；动作：`DISCARD` / `PONG` / `GANG_MING` / `GANG_AN` / `GANG_JIA` / `HU` / `PASS`
- 响应优先级：**胡 > 杠/碰 > 过**；**一炮多响默认开启**（`rules.multi_ron = true`，可关）

### 2.5 血战到底

- 玩家胡牌后 **离桌（FINISHED）**，不再摸打；剩余未胡玩家继续
- 直到：仅剩 1 人未胡，或牌墙摸尽 → 结算未胡者（查叫/花猪等，见计分）
- 状态：`ACTIVE` / `FINISHED` / `BANKRUPT`（预留，首版可不做破产出局）

### 2.6 计分要点（可配置表）

| 项目 | 默认约定（可在 `fan.py`/`score.py` 调） |
|------|----------------------------------------|
| 底分 | 1 |
| 自摸 | 未胡各家付；血战按剩余活跃人数 |
| 点炮 | 点炮者付（一炮多响则分别付） |
| 杠 | 直杠/补杠/暗杠即时分，可入 `gang_score` |
| 定缺相关 | **花猪**（未打完缺门）：查花猪惩罚 |
| 叫 | 未叫付叫；大叫/退税按配置 |
| 番型 | **成都血战** 标准番型数据表（平胡、对对胡、清一色、七对、金钩钓、带幺九、断幺九、杠上花、杠上炮、抢杠胡、根、门清等） |
| 封顶 | **`fan_cap` 可配置**（例如 4/5/不封顶）；实际计番 `min(computed_fan, fan_cap)`，`fan_cap=0` 表示不封顶 |

> 实现时把番型做成 **数据驱动表**，便于训练 Reward 对齐真实番数；封顶只影响计分与 Reward，不改变胡牌合法性。

### 2.7 终局

- 写 `GameResult`：各家得分、排名、胡牌序列、是否流局、最终手牌（用于日志/RL）

---

## 3. 关键类 / 接口定义

### 3.1 牌与动作

```python
# engine/tile.py
class Suit(Enum):
    WAN = "wan"
    TONG = "tong"
    TIAO = "tiao"

@dataclass(frozen=True, order=True)
class Tile:
    suit: Suit
    rank: int  # 1-9

    @property
    def id(self) -> str: ...  # "wan_3"
    def to_asset_key(self) -> tuple[str, int]: ...

# engine/action.py
class ActionType(Enum):
    DISCARD = "discard"
    PASS = "pass"
    PONG = "pong"
    GANG_MING = "gang_ming"
    GANG_AN = "gang_an"
    GANG_JIA = "gang_jia"
    HU = "hu"
    DINGQUE = "dingque"  # 定缺

@dataclass(frozen=True)
class Action:
    type: ActionType
    tile: Tile | None = None
    # gang 目标等扩展字段
```

### 3.2 可序列化状态

```python
# engine/state.py
@dataclass
class Meld:
    kind: Literal["pong", "ming_gang", "an_gang", "jia_gang"]
    tile: Tile
    from_seat: int | None

@dataclass
class PlayerPublicState:
    seat: int
    name: str
    score: int
    status: Literal["active", "finished", "crashed"]
    dingque: Suit | None
    melds: list[Meld]
    discard_pile: list[Tile]
    hand_count: int          # 对手只见数量
    is_dealer: bool
    hu_order: int | None     # 第几个胡
    last_hu: dict | None

@dataclass
class PlayerPrivateState(PlayerPublicState):
    hand: list[Tile]         # 仅本家 / 观战全知

@dataclass
class GameState:
    game_id: str
    seed: int
    phase: str               # lobby|deal|dingque|playing|settling|finished
    wall_remaining: int
    current_seat: int
    last_discard: Tile | None
    last_discard_seat: int | None
    players: list[PlayerPublicState | PlayerPrivateState]
    legal_actions: list[Action]   # 对当前决策者
    turn_index: int
    config_snapshot: dict
```

### 3.3 玩家标准接口（`players/base_player.py`）

```python
class BasePlayer(ABC):
    player_id: str
    name: str
    seat: int | None

    @abstractmethod
    def on_join(self, seat: int, config: dict) -> None: ...

    @abstractmethod
    def observe(self, observation: Observation) -> None:
        """接收主程序下发的视角过滤状态。"""

    @abstractmethod
    def decide(self, request: ActionRequest) -> Decision:
        """
        必须返回合法 Action；超时/异常由主程序 crash 策略处理。
        Decision 含 action + reason(str) + analysis(optional dict)。
        """

    def on_event(self, event: GameEvent) -> None:
        """可选：广播事件（有人碰/胡等）。"""

    def on_game_end(self, result: GameResult) -> None: ...

    def shutdown(self) -> None: ...
```

### 3.4 通信消息（`protocols/messages.py`）

```python
@dataclass
class Observation:
    game_id: str
    self_seat: int
    state: GameState           # 已过滤：只含本家手牌
    analysis_hints: dict | None  # 主程序可不填；玩家可自算

@dataclass
class ActionRequest:
    request_id: str
    deadline_ms: int | None
    legal_actions: list[Action]
    phase: str

@dataclass
class Decision:
    request_id: str
    action: Action
    reason: str
    analysis: dict | None      # shanten, danger, candidates...
    think_ms: int | None

@dataclass
class GameEvent:
    type: str
    payload: dict
    turn_index: int
```

### 3.5 引擎会话

```python
# engine/session.py
class GameSession:
    def __init__(self, config: EngineConfig, players: list[PlayerSlot]): ...
    def new_game(self, game_id: str | None = None) -> str: ...
    def step(self) -> StepResult: ...          # 推进一步直到需决策或结束
    def apply_decision(self, seat: int, decision: Decision) -> None: ...
    def save(self, path: Path) -> None: ...
    def load(self, path: Path) -> None: ...
    def get_spectator_state(self) -> GameState: ...  # 全可见
```

### 3.6 Reward

```python
# engine/reward.py
@dataclass
class RewardConfig:
    hu_fan_scale: float = 1.0          # 胡牌得分 × 番
    deal_in_penalty: float = 1.0       # 放炮惩罚系数（按付出分）
    rank_bonus: list[float] = field(   # 名次奖励 [第1,第2,...]
        default_factory=lambda: [3.0, 1.0, -1.0, -3.0]
    )
    gang_scale: float = 0.1
    final_score_scale: float = 0.01    # 终局得分映射
    step_penalty: float = 0.0          # 步数惩罚（可选）
    liuju_penalty: float = 0.0
    # 自定义：从 JSON 加载任意键，callback 注册扩展

class RewardCalculator:
    def on_score_delta(self, seat: int, delta: int, reason: str) -> float: ...
    def on_game_end(self, result: GameResult) -> dict[int, float]: ...
```

### 3.7 崩溃策略

```python
class CrashPolicy(Enum):
    ABORT_RESTART = "abort_restart"   # 终止本局，可选自动新开
    REPLACE_PLAYER = "replace_player" # 用 RandomPlayer / 指定 fallback 替换
    FORCE_PASS = "force_pass"         # 仅响应阶段；摸打阶段强制随机合法弃牌

@dataclass
class CrashConfig:
    policy: CrashPolicy
    timeout_ms: int = 30_000
    max_crashes: int = 3
    fallback_player: str = "random"
    log_stack: bool = True
```

---

## 4. 资源加载方案

### 4.1 统一 AssetManager

路径锚定：**项目根 / `assets/`**（与 `ASSETS.md` 一致；忽略文档中的 `/src/assets` 别名）。

```python
# display/asset_manager.py
class AssetManager:
    def __init__(self, root: Path, theme: Literal["green", "blue"] = "green"): ...
    def set_theme(self, theme: str) -> None: ...
    def tile(self, suit: str, rank: int) -> Surface: ...
    def tile_back(self) -> Surface: ...
    def button(self, key: str) -> Surface: ...
    def bg(self, which: Literal["table","lobby","result"]) -> Surface: ...
    def avatar(self, seat_1based: int) -> Surface: ...
    def dice(self, n: int) -> Surface: ...
    def icon(self, key: str) -> Surface: ...
    def fx(self, key: str) -> Surface: ...
    def danger(self, level: str) -> Surface: ...
    def strategy(self, key: str) -> Surface: ...
    def digit(self, char: str, color: str, size: str) -> Surface: ...
    def char(self, key: str, size: str) -> Surface: ...
    def scale(self, surface: Surface, display_w: int) -> Surface: ...
```

### 4.2 加载策略

| 策略 | 说明 |
|------|------|
| 懒加载 + 缓存 | 首次访问读盘，dict 缓存 `key → Surface` |
| 主题切换 | 清空主题相关缓存，重载；`tile_placeholder` 无主题 |
| 缩放 | 原图高清（牌 270×378）；基准窗口 1280×720，牌显示宽约 48–64 px |
| headless | **不初始化 Pygame display**；玩家训练模式跳过 `AssetManager` |
| 共享 | `players/view` 与 `display/` **共用同一类**，禁止复制两套路径拼接逻辑 |

### 4.3 与 HUD 的映射

| 分析输出 | 资源 |
|----------|------|
| 弃牌危险度 | `inference/danger_{level}_{theme}.png` |
| 对手听牌估计 | `tenpai_active` / `tenpai_unknown` + `infer_panel` |
| 剩余牌 | `remain_bar` + 数字字体 |
| 最优/次优/避免弃牌 | `mark_best` / `mark_second` / `mark_avoid` |
| 向听 | `shanten_badge` + digit sm |
| 特效 | `fx_hu/pong/gang/liuju/coin` |

---

## 5. 通信流程

### 5.1 架构示意

```
                    ┌─────────────────────────────────────┐
                    │              main.py                 │
                    │  CLI / Lobby GUI / headless runner   │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │           GameSession                │
                    │  deck · rules · blood_battle · score │
                    │  reward · persistence · spectator    │
                    └──────────────┬──────────────────────┘
                                   │ Observation / ActionRequest
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
        PlayerSlot[0]        PlayerSlot[1]  ...   PlayerSlot[n]
        (InProcess |         (Subprocess              │
         Subprocess)          human 独立窗口)           │
              │                    │                    │
              ▼                    ▼                    ▼
         Decision             Decision              Decision
              │                    │                    │
              └────────────────────┴────────────────────┘
                                   │ validate legal
                                   ▼
                            apply → events → log
```

### 5.2 单步时序（摸打）

1. 引擎：若当前座需要摸牌 → 摸 → 检查暗杠/补杠/自摸胡 → 生成 `legal_actions`
2. 引擎：`ActionRequest` → 对应 `PlayerSlot.decide()`
3. 玩家：`observe` 更新内部；分析模块计算；返回 `Decision(reason=...)`
4. 引擎：校验合法性；非法视同崩溃策略
5. 若 `DISCARD` → 广播弃牌 → 其他活跃玩家按座次响应（胡/碰杠/过）
6. 结算即时分（杠/胡）→ `RewardCalculator` 记 step reward → 写日志
7. 血战：若胡 → 标记 FINISHED → 若不足 2 人活跃 → 终局

### 5.3 三种玩家加入方式

| 方式 | 机制 |
|------|------|
| **命令行** | `python main.py --players rule_ai,rule_ai,random,human --game-id xxx` |
| **图形大厅** | `lobby_view` 选择人数、座位模块、主题、是否观战 |
| **主程序 API** | `GameSession(players=[RuleAI(), ...]); session.run()` 供脚本/训练调用 |

玩家注册表：

```python
PLAYER_REGISTRY = {
    "human": HumanPlayer,
    "random": RandomPlayer,
    "rule_ai": RuleAIPlayer,
    # "rl_agent": 后续扩展
}
```

### 5.4 进程模型

| 模式 | 用途 |
|------|------|
| **InProcess** | AI / headless / 训练（函数调用，最快） |
| **Subprocess + stdin/stdout JSON** | **`human_player` 强制子进程隔离**（独立窗口 + 崩溃不拖垮主进程） |
| Socket（预留） | 远程 agent |

Human 独立程序（默认路径）：

```text
# 主程序拉起子进程，不与主进程共用 GUI 事件循环
python -m players.human_player --seat 0 --theme green
# transport: 一行一个 JSON（Observation/ActionRequest → Decision）
```

### 5.5 观战模式

- 主程序 `display/table_view`：`SpectatorMode.FULL` 可见所有手牌；`PUBLIC_ONLY` 仅公开信息
- 不占用座位；不接收 `ActionRequest`
- 可从存档 `load` 后逐步回放（`turn_index` 驱动）

---

## 6. 训练支持设计

### 6.1 Headless 快速模拟

```bash
python main.py train \
  --games 10000 \
  --players rule_ai,rule_ai,rule_ai,rule_ai \
  --reward configs/reward_default.json \
  --log-dir logs/run_001 \
  --num-workers 1
```

- 不创建 Pygame window（`SDL_VIDEODRIVER=dummy` 仅当误加载时兜底）
- 玩家 `training_mode=True`：不渲染，只 `decide` + 可选 debug 日志

### 6.2 类 Gym 环境（`training/env.py`）

```python
class ChengduMahjongEnv:
    """单座位学习接口；其余座位用固定 opponent 策略。"""
    def reset(self, game_id: str | None = None) -> Observation: ...
    def step(self, action: Action) -> tuple[Observation, float, bool, dict]: ...
    def legal_actions(self) -> list[Action]: ...
```

- `info` 含：`fan`, `score_delta`, `rank`, `raw_events`
- 多智能体并行：`training/runner.py` 4 个 agent 同时学习时用共享 `GameSession` 轮转 `step`

### 6.3 日志格式（RL / 策略分析）

**文件**：`logs/{run_id}/{game_id}.jsonl`

每行一类事件（完整、可回放）：

```json
{"t": 0, "type": "game_start", "game_id": "...", "seed": 123, "players": [...], "config": {...}}
{"t": 1, "type": "deal", "hands": {"0": ["wan_1", ...], ...}}
{"t": 2, "type": "dingque", "seat": 0, "suit": "wan"}
{"t": 10, "type": "request", "seat": 0, "legal": [...]}
{"t": 11, "type": "decision", "seat": 0, "action": {"type": "discard", "tile": "tiao_5"}, "reason": "...", "analysis": {"shanten": 2, "candidates": [...]}}
{"t": 12, "type": "state", "snapshot_ref": "..."} 
{"t": 50, "type": "score", "deltas": {"0": 8, "2": -8}, "reason": "hu_dianpao", "fan": 3}
{"t": 51, "type": "reward", "seat_rewards": {"0": 3.2, "2": -2.1}}
{"t": 99, "type": "game_end", "result": {...}, "final_rewards": {...}}
```

可选：`saves/{game_id}.json` 完整 `GameState` 树用于断点续跑。

### 6.4 game_id 与复现

```
game_id 格式（建议）：
  cmj-{timestamp}-{random8}  或用户指定任意字符串

seed = blake2b(game_id, digest_size=8) → int
洗牌、掷骰定庄、换三张方向 均由 game_id 派生，互不干扰：
  shuffle_seed = seed
  dice_seed    = seed ^ 0xA5A5A5A5   # 两枚骰子点数 → 庄家座位
  exchange_seed = seed ^ 0x5A5A5A5A  # 换三张方向（若规则需随机）
  player_rng 不进入引擎 seed（保证「同 game_id → 同骰点/同庄/同手牌」）
```

- 每局使用 **独立 `game_id`** 作为存档文件名、日志键、复盘入口  
- 单元测试：`test_game_id_repro.py` 断言同 `game_id` 下骰点、庄家、发牌、换三张结果一致

---

## 7. Reward 系统

### 7.1 信号来源

| 信号 | 计算 | 默认权重 |
|------|------|----------|
| 胡牌 | `fan * hu_fan_scale`（或实际得分） | 1.0 |
| 放炮 | `-|score_paid| * deal_in_penalty` | 1.0 |
| 杠 | `gang_points * gang_scale` | 0.1 |
| 终局排名 | `rank_bonus[rank]` | [3,1,-1,-3] |
| 终局得分 | `final_score * final_score_scale` | 0.01 |
| 花猪/未叫 | 与引擎扣分一致映射 | 1.0 |
| 步数 | `-step_penalty` | 0 |

### 7.2 配置示例 `configs/reward_default.json`

```json
{
  "hu_fan_scale": 1.0,
  "deal_in_penalty": 1.0,
  "rank_bonus": [3.0, 1.0, -1.0, -3.0],
  "gang_scale": 0.1,
  "final_score_scale": 0.01,
  "step_penalty": 0.0,
  "liuju_penalty": 0.0,
  "use_engine_score_as_reward": false
}
```

`use_engine_score_as_reward: true` 时，可直接用引擎分差作为稠密奖励（便于与真实麻将分对齐）。

### 7.3 与训练的接口

- 每个 `score` 事件 → 立即产生 dense reward（可选）
- `game_end` → sparse rank / final
- `env.step` 返回的 `reward` 仅针对 **学习座位**；完整 `seat_rewards` 写入 jsonl

---

## 8. 玩家分析模块设计

| 模块 | 输入 | 输出 |
|------|------|------|
| `shanten`（引擎或 players 复用） | 手牌+副露+定缺 | 向听数、有效进张集合 |
| `remain` | 可见弃牌/副露/本家手牌 | 每张牌剩余 0–4 概率 |
| `danger` | 对手弃牌、副露、听牌估计 | danger level → UI |
| `opponent_model` | 公开信息 | 听牌概率、可能伺胡牌 |
| `strategy` | 上述全部 | 弃牌排序、期望、reason 文本 |

规则 AI：用 `strategy` 贪心选分最高合法动作。  
Human：HUD 展示，最终由点击确认。

---

## 9. 主程序 CLI 草图

```bash
# 图形大厅
python main.py

# 指定自对弈 + 显示
python main.py play --players rule_ai,rule_ai,rule_ai,rule_ai --theme green

# 指定牌局 ID 复现
python main.py play --game-id demo-001 --players random,random,random,random

# 含人类（独立窗口）
python main.py play --players human,rule_ai,rule_ai,rule_ai

# 观战回放
python main.py spectate --save saves/demo-001.json

# 保存/加载
python main.py play --save-every-turn --save-dir saves/

# headless 训练模拟
python main.py train --games 1000 --headless --reward configs/reward_default.json

# 崩溃策略
python main.py play --crash-policy replace_player --timeout-ms 10000
```

---

## 10. 显示架构

### 10.1 主程序全局窗口

- Lobby → Table（四家公开布局）→ Result
- 用于观战 / 无 human 时的「上帝视角」演示
- **可缩放**（`pygame.RESIZABLE`）；初始位置在工作区**居中**

### 10.2 Human 独立窗口

- 仅本家手牌正面；对手牌背 + 副露 + 弃牌
- 底部：碰/杠/胡/过按钮（`assets/buttons`）
- 侧栏：推理 + 策略 HUD
- 与主程序 **进程隔离**，避免阻塞 AI 局
- **可缩放**；初始按座位分布在主窗四向（下/右/上/左）

### 10.3 布局基准与窗口几何（F0018 / F0020 / UI_DESIGN_STANDARD v1.4）

- **多窗外框**：布局有效画布 = 工作区面积 **85%** 居中；封顶 **2160p**；布局 **A**（1H3AI）/ **B**（2H2AI）/ **C**（0H4AI）/ **D**（3H1AI，F0020）
- **MAIN** 画布 **25% 左下**（D 为 body 四分）；人类/AI 尺寸见 `docs/design/UI_DESIGN_STANDARD.md` §8
- **主窗内部**：TABLE **80%** / SIDE **20%**；DICE 中心（含开局掷骰动画 F0023）；四扇区；SIDE 下为细化出牌日志（F0024）
- **座位窗内部**：play/watch **OP 67% + EXT 33%**（可折叠）；人类 EXT=对手 HUD+弃牌（多行）；AI EXT=日志+弃牌
- **资源**：运行时图形仅 **`assets/`**
- 规格：F0015–F0020；设计 `docs/design/UI_DESIGN_STANDARD.md` + MAIN/HUMAN/AI 内部布局

---

## 11. 实现里程碑（建议 Build 顺序）

确认 Plan 后按下列 PR/阶段推进，每阶段可独立测试：

| 阶段 | 内容 | 验收 |
|------|------|------|
| **M1** | `tile/deck/game_id/state` + 掷骰定庄 + 序列化 | 同 game_id → 同骰点/庄家/手牌 |
| **M2** | 换三张 + 定缺阶段状态机 | 开局四阶段：掷骰→发牌→换三张→定缺 |
| **M3** | `shanten/win_check/fan`（成都血战 + `fan_cap`） | 单元测试覆盖常见牌形与封顶 |
| **M4** | `blood_battle` + 一炮多响 + 合法动作 | 无 UI 随机 4 人可终局 |
| **M5** | `score` + `reward` + jsonl 日志 | 训练 runner 千局无崩溃 |
| **M6** | `BasePlayer` + random/rule_ai + session | 主程序 API 自对弈 |
| **M7** | `AssetManager` + 主程序 table/lobby/result/骰子 | 可视化观战 |
| **M8** | `analysis/*` + strategy HUD | rule_ai 决策带 reason |
| **M9** | `human` **子进程**座位窗 + transport | 首版 1H+3AI；**后由 F0020 扩至 ≤3H** |
| **M10** | 存档/加载/回放 + 崩溃策略 | 容错与复盘 |
| **M11** | `training/env` + numpy 加速路径 + README | 对外可训练接口 |

> **状态**：M01–M11 均已 **Done**（见 `docs/milestones/`）。  
> **M11 之后**：功能增量见 `docs/features/Fxxxx`（F0001–F0027 已实现；F0028 人类化 AI v2 的 F0028-1–4 已 Done；当前应用 **v0.2.1**）。
> M11 交付：`training/env.py`（Gymnasium 5-tuple，不强制 gymnasium/numpy）+ 根 `README.md`。

---

## 12. Key Decisions

| 决策 | 选择 | 理由 |
|------|------|------|
| 状态权威位置 | 仅 `engine/` | 防玩家篡改；可校验 Decision |
| 定庄 | **骰子**（seed 可复现）+ 独立 `game_id` 存档 | 符合开局仪式；同 ID 可复盘 |
| 玩家进程 | AI **InProcess**；Human **强制子进程** | 训练性能 vs GUI/崩溃隔离 |
| 无吃 | 硬编码规则 | 成都麻将；无 assets 按钮 |
| 一炮多响 | **默认开**，可配置 | 血战标准；训练需覆盖 |
| 换三张 | **首版必做** | 完整成都开局流程 |
| 番型 | 成都血战表 + **`fan_cap` 可配置** | 对齐本地规则；训练可调难度 |
| 资源 API | 单一 `AssetManager` | 与 ASSETS.md 一致，双主题 |
| 日志 | JSONL 逐步 | 利于 RL 与分析 |
| Reward | 配置文件 + 引擎分可选直通 | 实验可调，不改代码 |
| 向听 / 批模拟 | 可用 **NumPy** 加速 | 用户明确允许 |
| 2–4 人 | 规则逻辑一致，仅人数不同 | Review 确认 |
| **开发流程** | **Docs-First**：步骤与功能变更先文档后代码 | 可评审、可追溯、避免无规格实现 |
| **轮次收尾** | 每轮结束输出「已完成 + 下一步完整清单」 | 进度透明；见 `docs/DEVELOPMENT.md` §2.1 |

---

## 13. 开放问题 — 已关闭

| # | 决议摘要 |
|---|----------|
| 1 | 骰子定庄；骰点由 `game_id` 派生；局以独立 `game_id` 保存 |
| 2 | 默认一炮多响 |
| 3 | 需要换三张 |
| 4 | 成都血战番型；封顶可配置 |
| 5 | Human 子进程隔离 |
| 6 | 2/3/4 人规则保持一致 |
| 7 | 允许 numpy |

### 13.1 实现时仍可微调的技术细节（不阻塞 M1）

- 换三张默认方向：顺时针 / 逆时针 / 按骰点奇偶切换（实现时选一写入 `rules.exchange_dir`，默认 **按双骰点数惯例** 并写进配置）
- 成都番型细表：以常见血战清单为初值，可在 `configs/fan_table.json` 增删，无需改状态机
- 底分默认 1，与 `fan_cap` 分离配置

---

## 14. 验收标准（整项目）

- [x] 相同 `game_id` 两次运行：**骰点、庄家、初始手牌、换三张结果** 一致  
- [x] 开局含完整：**掷骰 → 发牌 → 换三张 → 定缺 → 行牌**（主窗另有掷骰动画 F0023）  
- [x] 一炮多响默认生效；可配置关闭  
- [x] 番型按成都血战；`fan_cap` 配置生效  
- [x] 4 AI headless 可连续跑（训练 runner / pytest 覆盖）  
- [x] 玩家崩溃时按配置策略（M10）  
- [x] Human **子进程**座位窗可完成换三张、定缺、出牌、碰杠胡（**1–3 human** F0020）  
- [x] 日志 / 存档 / 回放（M05/M10）  
- [x] Reward 配置可调（M05）  
- [x] 可见渲染使用 `assets/`，主题 green/blue  
- [x] 无「吃」动作与 UI  
- [x] 2/3/4 人共用同一规则代码路径  

---

## 15. 下一步

**M01–M11 已完成。F0028 已进入 In Progress，F0028-1–2 已 Done。** 当前有序队列：

1. 读 `docs/status/LATEST.md` + `docs/status/DOC_CODE_BASELINE.md`  
2. 本地 Git 与测试门禁已恢复；远端基线推送仍需单独授权
3. 编写并确认 F0028-5 决策审计与确定性回放子规格，随后继续逐切片实现和验收回写
4. 新需求 → `docs/features/Fxxxx_*.md`（Docs-First）→ Approved → 实现  
5. 发版 → 改 `version.py` + changelog + tag + 打包（`docs/VERSIONING.md`）

流程：[`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)、[`AGENTS.md`](AGENTS.md)。
