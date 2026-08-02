"""Configurable reward signals for RL / analysis (M05)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from engine.blood_battle import GameResult
from engine.score import ScoreTransfer
from engine.state import GameState

def _default_reward_path() -> Path:
    try:
        from app_paths import configs_dir

        return configs_dir() / "reward_default.json"
    except Exception:
        return (
            Path(__file__).resolve().parent.parent / "configs" / "reward_default.json"
        )


_DEFAULT_REWARD_PATH = _default_reward_path()


@dataclass
class RewardConfig:
    hu_fan_scale: float = 1.0
    deal_in_penalty: float = 1.0
    rank_bonus: list[float] = field(
        default_factory=lambda: [3.0, 1.0, -1.0, -3.0]
    )
    gang_scale: float = 0.1
    final_score_scale: float = 0.01
    step_penalty: float = 0.0
    liuju_penalty: float = 0.0
    use_engine_score_as_reward: bool = False
    hua_zhu_scale: float = 1.0
    cha_jiao_scale: float = 1.0

    @classmethod
    def load(cls, path: Path | str | None = None) -> RewardConfig:
        p = Path(path) if path else _DEFAULT_REWARD_PATH
        if not p.exists():
            return cls()
        with p.open(encoding="utf-8") as f:
            data = json.load(f)
        return cls(
            hu_fan_scale=float(data.get("hu_fan_scale", 1.0)),
            deal_in_penalty=float(data.get("deal_in_penalty", 1.0)),
            rank_bonus=list(data.get("rank_bonus") or [3.0, 1.0, -1.0, -3.0]),
            gang_scale=float(data.get("gang_scale", 0.1)),
            final_score_scale=float(data.get("final_score_scale", 0.01)),
            step_penalty=float(data.get("step_penalty", 0.0)),
            liuju_penalty=float(data.get("liuju_penalty", 0.0)),
            use_engine_score_as_reward=bool(
                data.get("use_engine_score_as_reward", False)
            ),
            hua_zhu_scale=float(data.get("hua_zhu_scale", 1.0)),
            cha_jiao_scale=float(data.get("cha_jiao_scale", 1.0)),
        )

    def to_dict(self) -> dict:
        return {
            "hu_fan_scale": self.hu_fan_scale,
            "deal_in_penalty": self.deal_in_penalty,
            "rank_bonus": list(self.rank_bonus),
            "gang_scale": self.gang_scale,
            "final_score_scale": self.final_score_scale,
            "step_penalty": self.step_penalty,
            "liuju_penalty": self.liuju_penalty,
            "use_engine_score_as_reward": self.use_engine_score_as_reward,
            "hua_zhu_scale": self.hua_zhu_scale,
            "cha_jiao_scale": self.cha_jiao_scale,
        }


class RewardCalculator:
    def __init__(self, config: RewardConfig | None = None) -> None:
        self.config = config or RewardConfig.load()
        self.episode_rewards: dict[int, float] = {}

    def reset(self) -> None:
        self.episode_rewards = {}

    def _acc(self, seat_rewards: dict[int, float]) -> dict[int, float]:
        for s, r in seat_rewards.items():
            self.episode_rewards[s] = self.episode_rewards.get(s, 0.0) + r
        return seat_rewards

    def on_transfers(self, transfers: list[ScoreTransfer]) -> dict[int, float]:
        rewards: dict[int, float] = {}
        cfg = self.config

        def add(seat: int, val: float) -> None:
            rewards[seat] = rewards.get(seat, 0.0) + val

        for t in transfers:
            if cfg.use_engine_score_as_reward:
                add(t.from_seat, -t.amount * cfg.final_score_scale)
                add(t.to_seat, t.amount * cfg.final_score_scale)
                continue

            reason = t.reason
            if reason in ("hu_zimo", "hu_dianpao"):
                fan = t.fan or 0
                add(t.to_seat, cfg.hu_fan_scale * (fan + 1))
                if reason == "hu_dianpao":
                    add(t.from_seat, -cfg.deal_in_penalty * (fan + 1))
                else:
                    add(t.from_seat, -cfg.hu_fan_scale * 0.5 * (fan + 1))
            elif reason.startswith("gang_"):
                add(t.to_seat, cfg.gang_scale * t.amount)
                add(t.from_seat, -cfg.gang_scale * t.amount)
            elif reason == "hua_zhu":
                add(t.from_seat, -cfg.hua_zhu_scale * t.amount)
                add(t.to_seat, cfg.hua_zhu_scale * t.amount)
            elif reason == "cha_jiao":
                add(t.from_seat, -cfg.cha_jiao_scale * t.amount)
                add(t.to_seat, cfg.cha_jiao_scale * t.amount)
            else:
                add(t.from_seat, -t.amount * cfg.final_score_scale)
                add(t.to_seat, t.amount * cfg.final_score_scale)

        if cfg.step_penalty:
            for s in list(rewards.keys()):
                add(s, -cfg.step_penalty)

        return self._acc(rewards)

    def on_game_end(
        self, result: GameResult, state: GameState
    ) -> dict[int, float]:
        cfg = self.config
        rewards: dict[int, float] = {}

        def add(seat: int, val: float) -> None:
            rewards[seat] = rewards.get(seat, 0.0) + val

        for rank_i, seat in enumerate(result.rankings):
            if rank_i < len(cfg.rank_bonus):
                add(seat, cfg.rank_bonus[rank_i])
            score = result.scores.get(seat, 0)
            add(seat, score * cfg.final_score_scale)

        if result.finished_reason == "wall_empty" and cfg.liuju_penalty:
            for seat in result.scores:
                add(seat, -cfg.liuju_penalty)

        return self._acc(rewards)
