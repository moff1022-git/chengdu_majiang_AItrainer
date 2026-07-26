# M10 — 存档 / 回放 / 崩溃策略

| 字段 | 值 |
|------|-----|
| **编号** | M10 |
| **标题** | Persistence, replay, crash policy |
| **状态** | `Done` |
| **依赖** | **M01–M09 Done**（GameState 序列化、orchestrator、Human 超时错误、JSONL） |
| **下一里程碑** | M11（training env + README） |
| **对应 PLAN** | `persistence.py`、crash policy、CLI spectate/save、§11 M10 |

---

## 1. 目标

完善对局的**可恢复性**与**容错**：

1. **存档 / 加载**：完整 `GameState`（+ 元数据）写入 `saves/{game_id}.json`；可断点续跑。  
2. **逐步快照（可选）**：按 turn 或每次 decision 追加快照目录，支持回放。  
3. **回放 / 观战**：从存档或 JSONL 驱动 `InteractiveRunner` 或只读逐步展示。  
4. **崩溃策略**：玩家 decide 超时/抛错/子进程死时，按配置执行  
   `abort_restart` | `replace_player` | `force_pass`（对齐 PLAN）。  
5. **配置**：`configs/crash_policy.json`；CLI 参数接入 `main.py`。

本步**不**实现：云存档、多人对战服务器、完整录像压缩格式（以 JSON 为主）。

---

## 2. 范围

### 2.1 In Scope

| 项 | 说明 |
|----|------|
| `engine/persistence.py` | `save_game` / `load_game` / 校验 schema |
| `engine/replay.py` | 从存档或 decision 日志逐步恢复 |
| `engine/crash.py` | `CrashPolicy` / `CrashConfig` / `handle_player_failure` |
| `configs/crash_policy.json` | 默认策略 |
| 编排接入 | `PlayerGameRunner` / `InteractiveRunner` 在 decide 外包 try/policy |
| `main.py` | `save` / `load` / `spectate` / `--crash-policy` / `--save-dir` |
| `.gitignore` | `saves/`、`logs/`（若尚未） |
| 测试 | 存读往返、续跑 phase 一致、crash replace/force_pass |

### 2.2 Out of Scope

- 加密存档、云同步  
- 跨版本无限兼容（明确支持 schema 3–4；写最新）  
- Human 崩溃后自动重开窗口的复杂 UX（replace 时换 random/rule_ai）  

---

## 3. 设计

### 3.1 存档格式

文件：`saves/{game_id}.json`（或用户指定路径）

```json
{
  "format": "cmj_save",
  "format_version": 1,
  "saved_at": "ISO-8601",
  "game_id": "...",
  "schema_version": 4,
  "engine_config": { ... },
  "players_meta": [
    {"seat": 0, "type": "rule_ai", "name": "..."}
  ],
  "state": { ... GameState.to_dict() ... },
  "rng_notes": "player rng not restored; engine state fully in state"
}
```

- **权威**：`state` 内含 wall、hands、phase、scores、pending 等。  
- 加载后可直接 `legal_actions` / `apply` 继续。  
- Human 座位：加载后需 **重新 spawn** proxy（不恢复子进程 pid）。

API：

```python
def save_game(
    path: Path,
    state: GameState,
    *,
    config: EngineConfig | None = None,
    players_meta: list[dict] | None = None,
) -> None: ...

def load_game(path: Path) -> tuple[GameState, dict]:
    """Returns (state, meta). Validates format/schema."""
```

### 3.2 逐步快照（回放源）

目录：`saves/{game_id}/` 或 `saves/{game_id}.steps.jsonl`

**推荐 JSONL 步骤文件**（与训练日志互补，更小）：

```text
saves/{game_id}.steps.jsonl
```

每行：

```json
{"i": 0, "kind": "snapshot", "state": {...}}
{"i": 1, "kind": "decision", "seat": 0, "action": {...}, "reason": "..."}
{"i": 2, "kind": "snapshot", "state": {...}}
```

配置：

| 选项 | 默认 |
|------|------|
| `save_mode` | `final`（仅终局/手动） / `every_decision` / `every_turn` |
| `save_dir` | `saves` |

M10 默认实现：

- **手动 / 终局** 完整 save  
- **`every_decision`** 可选写 steps.jsonl（状态可隔 N 步全量快照，中间只记 decision 以省空间）  

**回放策略 A（简单）**：只存全量 snapshot 列表，回放直接 load 第 i 帧。  
**回放策略 B**：初始 snapshot + decision 序列，用引擎 apply 重放（需玩家无关的确定性）。  

规格采用 **A 为主**：`every_decision` 时每步写完整 state（可接受体积；训练用 logs 已有 decision）。  
若体积过大，实现时用 **每步 decision + 每 10 步 snapshot**（文档允许）。

### 3.3 回放 API

```python
class ReplaySession:
    def __init__(self, path: Path): ...
    def __len__(self) -> int: ...
    def frame(self, i: int) -> GameState: ...
    def step_forward(self) -> GameState: ...
```

`main.py spectate --save PATH`：

- 若 GUI：TableView 显示，方向键切换帧  
- 若 headless：打印 phase / scores  

### 3.4 崩溃策略

#### 3.4.1 配置 `configs/crash_policy.json`

```json
{
  "policy": "replace_player",
  "timeout_ms": 120000,
  "max_crashes": 3,
  "fallback_player": "random",
  "log_stack": true,
  "restart_on_abort": false
}
```

| policy | 行为 |
|--------|------|
| `abort_restart` | 终止本局；`finished_reason=player_crash`；可选自动新开（`restart_on_abort`） |
| `replace_player` | 该座替换为 `fallback_player`（random/rule_ai），shutdown 旧 proxy，记 crash 计数 |
| `force_pass` | 响应阶段强制 PASS；弃牌阶段强制随机合法 DISCARD |

#### 3.4.2 触发源

- `HumanTimeoutError` / `HumanProcessError`  
- `decide` 抛任意 Exception  
- 非法 Decision（可选：计为 crash 或直接 force_pass；**默认 force 一次合法随机 + 计数**）  

#### 3.4.3 状态标记

```text
PlayerState.status 可增 "crashed" 瞬态；replace 后回到 active
state.crash_log: list[{seat, error, policy, turn_index}]
```

### 3.5 编排接入

```python
# PlayerGameRunner._play_seat_action
try:
    dec = player.decide(req)
    validate...
except Exception as e:
    dec = crash_handler.handle(state, seat, e, legal)
apply(dec)
```

`CrashHandler` 持有 `CrashConfig` + 工厂 `create_player(fallback)`。

Human 被 replace 后：调用 `shutdown()` 杀子进程。

### 3.6 CLI

```bash
# 存档
python main.py play --players rule_ai,... --save-dir saves --save-every-decision

# 加载续玩（AI only 或 replace human）
python main.py resume --save saves/xxx.json --players rule_ai,rule_ai,rule_ai,rule_ai

# 回放
python main.py spectate --save saves/xxx.json
python main.py spectate --steps saves/xxx.steps.jsonl

# 崩溃策略
python main.py play --players human,rule_ai,rule_ai,rule_ai --crash-policy replace_player
```

### 3.7 schema

- 存档 `format_version=1`  
- GameState 仍用现有 schema 4；可增 `crash_log` 字段 → **schema 5**（可选）  
- **决议：schema 升至 5** 若增加 crash_log；否则 crash_log 仅在 save meta  

推荐：`crash_log` 放在 save meta，**state schema 保持 4**，降低兼容成本。

---

## 4. 文件清单

| 路径 | 动作 |
|------|------|
| `engine/persistence.py` | 新增 |
| `engine/replay.py` | 新增 |
| `engine/crash.py` | 新增 |
| `configs/crash_policy.json` | 新增 |
| `engine/orchestrator.py` | 接入 crash + 可选 autosave |
| `main.py` | resume / spectate / 保存参数 |
| `tests/test_persistence.py` | 新增 |
| `tests/test_crash.py` | 新增 |
| `.gitignore` | saves/, logs/ |
| docs | 状态 |

---

## 5. 测试计划

| ID | 用例 | 期望 |
|----|------|------|
| S01 | save/load 往返 | phase、hands、wall 一致 |
| S02 | load 后续跑 random 至终局 | 无异常 |
| S03 | steps 回放帧数 | len>=1，frame 可取 |
| C01 | force_pass 超时模拟 | 产生 PASS/合法弃牌 |
| C02 | replace_player | 座位类型变为 fallback |
| C03 | abort | finished_reason 含 crash |
| R01 | 全量回归 | 通过 |

```bash
pytest tests/ -q
```

---

## 6. 验收标准

- [x] 可保存/加载牌局并续玩  
- [x] 可选逐步存档与回放 API  
- [x] 三种 crash policy 可配置且单测覆盖  
- [x] Human 超时走 crash 策略而非静默挂死  
- [x] CLI resume/spectate 可用  
- [x] M01–M09 回归通过  

---

## 7. 风险与开放问题

| 项 | 默认决议 |
|----|----------|
| 逐步存档 | 可选 `every_decision` 全量 snapshot |
| crash 默认 | **replace_player** + fallback **random** |
| schema | state 保持 **4**；crash_log 在 save meta |
| 非法 decision | 计 crash 并 **force 合法随机** |

**开放问题 — 已关闭（用户确认 M10，2026-07-10）：**

| # | 决议 |
|---|------|
| 1 | 默认 crash policy：**replace_player**（fallback=`random`） |
| 2 | 逐步存档默认 **关**（仅手动/终局；可选 every_decision） |
| 3 | 非法 Decision：**force 随机合法** 并计数（非直接 abort） |

---

## 8. 实现备注（编码后填写）

- 新增：`engine/persistence.py`、`replay.py`、`crash.py`、`configs/crash_policy.json`
- 编排接入 crash + 可选 `save_dir` / `save_every_decision`
- CLI：`resume` / `spectate` / `save-info`；play 支持 `--save-dir` / `--crash-policy`
- `.gitignore`：`saves/`、`logs/`
- 测试：`test_persistence.py`、`test_crash.py`；全量 **105 passed**

---

## 9. 状态历史

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-07-10 | `Review` | 首版规格，待用户确认 |
| 2026-07-10 | `Approved` | 用户确认 M10；开放问题按默认方案关闭 |
| 2026-07-10 | `Done` | 实现完成 |
