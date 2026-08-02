"""Stable per-episode and aggregate training metrics."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from engine.blood_battle import GameResult


@dataclass(frozen=True, slots=True)
class EpisodeMetricsV2:
    game_id: str
    learner_seat: int
    illegal_action_count: int
    hidden_leak_count: int
    conservation_failure_count: int
    true_score: int
    rank: int
    first_hu: bool
    hu: bool
    hua_zhu: bool
    no_ting: bool
    fan_total: int
    fan_average: float
    pong_count: int
    gang_count: int
    pass_hu_count: int
    learner_steps: int
    base_reward: float
    shaping_reward: float
    combined_reward: float
    finished_reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_episode_metrics(result: GameResult, seat: int, *, action_counts: dict[str, int], illegal_count: int, learner_steps: int, base_reward: float, shaping_reward: float) -> EpisodeMetricsV2:
    wins = [event for event in result.hu_sequence if int(event.get("winner", event.get("seat", -1))) == seat]
    all_winners = [int(event.get("winner", event.get("seat", -1))) for event in result.hu_sequence]
    fans = [int(event.get("fan") or 0) for event in wins]
    reasons = [str(event.get("reason", "")) for event in result.score_events]
    tags = result.settle_tags or {}
    hua_tag = tags.get("hua_zhu", {}) if isinstance(tags, dict) else {}
    no_ting_tag = tags.get("no_ting", {}) if isinstance(tags, dict) else {}
    hua = (bool(hua_tag.get(str(seat), False)) if isinstance(hua_tag, dict) else seat in hua_tag) or "hua_zhu" in reasons
    no_ting = bool(no_ting_tag.get(str(seat), False)) if isinstance(no_ting_tag, dict) else seat in no_ting_tag
    base = float(base_reward)
    shaping = float(shaping_reward)
    return EpisodeMetricsV2(result.game_id, seat, illegal_count, 0, 0, int(result.scores.get(seat, 0)), result.rankings.index(seat) + 1, bool(all_winners and all_winners[0] == seat), bool(wins), hua, no_ting, sum(fans), sum(fans) / len(fans) if fans else 0.0, action_counts.get("pong", 0), sum(action_counts.get(k, 0) for k in ("gang_ming", "gang_an", "gang_jia")), action_counts.get("pass_hu", 0), learner_steps, base, shaping, base + shaping, result.finished_reason)


class TrainingMetricsAggregator:
    def __init__(self) -> None:
        self.episodes: list[EpisodeMetricsV2] = []

    def add(self, metric: EpisodeMetricsV2) -> None:
        self.episodes.append(metric)

    def extend(self, metrics: Iterable[EpisodeMetricsV2]) -> None:
        self.episodes.extend(metrics)

    def summary(self) -> dict[str, float | int]:
        n = len(self.episodes)
        if not n:
            return {"episodes": 0}
        rate = lambda name: sum(bool(getattr(m, name)) for m in self.episodes) / n
        total_steps = max(1, sum(m.learner_steps for m in self.episodes))
        return {
            "episodes": n, "first_hu_rate": rate("first_hu"), "hu_rate": rate("hu"),
            "hua_zhu_rate": rate("hua_zhu"), "no_ting_rate": rate("no_ting"),
            "average_fan": sum(m.fan_total for m in self.episodes) / max(1, sum(m.hu for m in self.episodes)),
            "pong_rate": sum(m.pong_count for m in self.episodes) / total_steps,
            "gang_rate": sum(m.gang_count for m in self.episodes) / total_steps,
            "pass_hu_rate": sum(m.pass_hu_count for m in self.episodes) / total_steps,
            "average_true_score": sum(m.true_score for m in self.episodes) / n,
            "illegal_action_rate": sum(m.illegal_action_count for m in self.episodes) / total_steps,
            "hidden_leak_rate": sum(m.hidden_leak_count for m in self.episodes) / n,
            "conservation_failure_rate": sum(m.conservation_failure_count for m in self.episodes) / n,
        }
