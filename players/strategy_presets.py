"""Load AI strategy presets for seat UI and player factory.

Presets live under ``configs/strategies/``:
  - presets.json — selectable list for seat window
  - current_s2.json — snapshot of hand_predict + F0011 flags
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
PRESETS_PATH = _ROOT / "configs" / "strategies" / "presets.json"
STRATEGIES_DIR = _ROOT / "configs" / "strategies"

# Built-in fallback if config missing
_FALLBACK: list[dict[str, Any]] = [
    {
        "id": "rule_ai",
        "label": "规则AI",
        "short_label": "规则",
        "player": "rule_ai",
        "use_f0011": False,
    },
    {
        "id": "random",
        "label": "随机AI",
        "short_label": "随机",
        "player": "random",
        "use_f0011": False,
    },
    {
        "id": "current_s2",
        "label": "当前策略·S2",
        "short_label": "当前S2",
        "player": "rule_ai",
        "use_f0011": True,
        "profile": "configs/strategies/current_s2.json",
    },
]


@lru_cache(maxsize=1)
def load_presets() -> list[dict[str, Any]]:
    if PRESETS_PATH.is_file():
        try:
            data = json.loads(PRESETS_PATH.read_text(encoding="utf-8"))
            items = list(data.get("strategies") or [])
            if items:
                return items
        except Exception:
            pass
    return list(_FALLBACK)


def list_strategy_ids() -> list[str]:
    return [str(s["id"]) for s in load_presets()]


def get_preset(strategy_id: str) -> dict[str, Any] | None:
    key = str(strategy_id or "").strip().lower().split(":")[0]
    for s in load_presets():
        if str(s.get("id", "")).lower() == key:
            return dict(s)
    # bare player keys
    if key in ("rule_ai", "random", "human"):
        return {
            "id": key,
            "label": key,
            "player": key,
            "use_f0011": False,
        }
    return None


def ui_choices() -> list[tuple[str, str]]:
    """Return (id, short_label) for seat window buttons."""
    out: list[tuple[str, str]] = []
    for s in load_presets():
        sid = str(s.get("id") or "")
        lab = str(s.get("short_label") or s.get("label") or sid)
        if sid:
            out.append((sid, lab))
    return out


def resolve_player_key(strategy_id: str) -> str:
    """Map strategy preset id → registry player type key."""
    p = get_preset(strategy_id)
    if not p:
        return "rule_ai"
    return str(p.get("player") or "rule_ai").lower()


def player_options_for_spec(spec: str) -> dict[str, Any]:
    """Extra kwargs / config for create_player from strategy id or player spec."""
    key = str(spec or "").strip().lower().split(":")[0]
    p = get_preset(key)
    if not p:
        return {}
    opts: dict[str, Any] = {
        "strategy_id": p.get("id"),
        "use_f0011": bool(p.get("use_f0011")),
    }
    profile = p.get("profile")
    if profile:
        opts["strategy_profile"] = str(profile)
    return opts


def load_profile(path: str | Path | None) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.is_file():
        p2 = _ROOT / path
        if p2.is_file():
            p = p2
        else:
            return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def apply_hand_predict_profile(profile: dict[str, Any] | None) -> list[str]:
    """Apply hand_predict constants from a strategy profile. Returns applied keys.

    Note: module-level constants affect the whole process (all seats share F0010).
    """
    if not profile:
        return []
    hp_params = profile.get("hand_predict") or {}
    if not isinstance(hp_params, dict):
        return []
    import players.analysis.hand_predict as hp

    applied: list[str] = []
    for k, v in hp_params.items():
        if not hasattr(hp, k):
            continue
        cur = getattr(hp, k)
        try:
            if isinstance(cur, tuple) and isinstance(v, list):
                setattr(hp, k, tuple(v))
            else:
                setattr(hp, k, type(cur)(v) if type(cur) in (int, float, bool) else v)
            applied.append(k)
        except Exception:
            continue
    return applied


def ensure_profile_applied(strategy_id: str) -> None:
    """Load and apply profile for current_s2-style presets (once per id)."""
    p = get_preset(strategy_id)
    if not p or not p.get("profile"):
        return
    path = p["profile"]
    cache_attr = "_applied_strategy_profiles"
    import players.strategy_presets as self_mod

    done: set[str] = getattr(self_mod, cache_attr, set())
    if str(path) in done:
        return
    prof = load_profile(path)
    apply_hand_predict_profile(prof)
    done = set(done)
    done.add(str(path))
    setattr(self_mod, cache_attr, done)
