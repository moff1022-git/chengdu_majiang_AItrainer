# Python 环境：永久有效配置方案

本仓库**权威解释器**为项目根目录 **`.venv`**（当前实测 **Python 3.12.x**）。  
**不要**用系统 `/usr/bin/python3`（macOS 常为 3.9，不满足 3.11+）。

---

## 1. 一键安装 / 修复（推荐）

```bash
cd "/path/to/chengdu_majiang_AItrainer"
bash tools/setup_venv.sh
```

脚本会：

1. 选择 PATH 上的 Python **≥3.11**（优先 3.12）  
2. 创建或复用 `.venv`  
3. `pip install -r requirements.txt`（+ 可选 numpy）  
4. 校验 pygame / pytest / tkinter  

---

## 2. 永久生效的三种方式（选一种即可）

### 方案 A — 始终写死路径（最稳，推荐 CI / 脚本）

```bash
.venv/bin/python main.py play --players rule_ai,rule_ai,rule_ai,rule_ai
.venv/bin/python -m pytest -q
.venv/bin/python tools/eval_hand_predict.py --set 20
```

不依赖 `activate`，换 shell、换会话都有效。

### 方案 B — direnv 自动激活（进目录即生效）

```bash
brew install direnv
# 写入 ~/.zshrc 一次：
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc

cd /path/to/chengdu_majiang_AItrainer
direnv allow
```

之后每次 `cd` 进仓库自动 `source .venv`（见根目录 `.envrc`）。

### 方案 C — 手动 activate（临时会话）

```bash
source .venv/bin/activate
python main.py ...
deactivate   # 离开时
```

可在 `~/.zshrc` 加别名（仅本机）：

```bash
alias cmj='cd "/path/to/chengdu_majiang_AItrainer" && source .venv/bin/activate'
```

---

## 3. 编辑器永久绑定

仓库已含 **`.vscode/settings.json`**：

- `python.defaultInterpreterPath` → `.venv/bin/python`  
- 集成终端自动激活 venv  

Cursor / VS Code：打开仓库根目录，选解释器为 `.venv`。

---

## 4. 版本钉死

| 文件 | 作用 |
|------|------|
| `.python-version` | `3.12`（pyenv / asdf 本地版本） |
| `requirements.txt` | 运行时依赖 |
| `.venv/` | 本机虚拟环境（**勿提交 git**；已在 `.gitignore`） |

安装 pyenv（可选）：

```bash
brew install pyenv
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
pyenv install 3.12
cd /path/to/repo   # 读取 .python-version
bash tools/setup_venv.sh
```

macOS 座位窗还需要：

```bash
brew install python-tk@3.12
```

---

## 5. 自检

```bash
.venv/bin/python -c "import sys; print(sys.executable); print(sys.version)"
# 应类似：.../chengdu_majiang_AItrainer/.venv/bin/python
#          3.12.x

.venv/bin/python -c "import pygame; print(pygame.version.ver)"
.venv/bin/python -m pytest -q --collect-only 2>/dev/null | tail -3
```

若 `which python` 仍是 `/usr/bin/python3` 且版本 3.9 → **未激活 venv**，改用方案 A 或 B。

---

## 6. 注意（OneDrive / 路径）

当前仓库在 **OneDrive 同步目录**下。虚拟环境偶发符号链接损坏时：

```bash
rm -rf .venv
bash tools/setup_venv.sh
```

更稳妥：把仓库克隆到本地非同步路径（如 `~/dev/...`），OneDrive 仅作备份。

---

## 7. Windows

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py play ...
```

---

## 8. 与本项目命令约定

| 场景 | 命令前缀 |
|------|----------|
| 日常 / 文档复现 | `.venv/bin/python` |
| 已 activate | `python` |
| Grok / CI 脚本 | 固定 `.venv/bin/python` |
