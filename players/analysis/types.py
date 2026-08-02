"""Shared analysis result types."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class DiscardAdvice:
    tile_id: str
    rank: int
    shanten_after: int
    ukeire_after: int
    danger: str
    score: float
    mark: str  # best|second|avoid|none
    ukeire_tiles: list[str] = field(default_factory=list)  # F0012 waits after discard

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class OpponentHint:
    seat: int
    tenpai_prob: float
    tenpai_level: str  # active|unknown
    likely_waits: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


# F0010 hand-shape prediction types live in hand_predict.py
# (OpponentHandHypothesis / OpponentHandForecast) to avoid circular imports.


@dataclass
class AnalysisSnapshot:
    seat: int
    shanten: int
    ukeire: list[str]
    ukeire_count: int
    remain: dict[str, int]
    danger: dict[str, str]
    discard_ranks: list[DiscardAdvice]
    opponents: list[OpponentHint]
    generated_ms: float

    def to_dict(self, *, verbose: bool = False) -> dict:
        d = {
            "seat": self.seat,
            "shanten": self.shanten,
            "ukeire_count": self.ukeire_count,
            "ukeire": self.ukeire[:12],
            "best": self.discard_ranks[0].tile_id if self.discard_ranks else None,
            "danger": {
                a.tile_id: a.danger for a in self.discard_ranks[:8]
            },
            "generated_ms": self.generated_ms,
        }
        if verbose:
            d["remain"] = self.remain
            d["discard_ranks"] = [a.to_dict() for a in self.discard_ranks]
            d["opponents"] = [o.to_dict() for o in self.opponents]
        return d
