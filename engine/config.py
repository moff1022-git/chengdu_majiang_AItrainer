"""Engine configuration."""

from __future__ import annotations

from dataclasses import asdict, dataclass

_EXCHANGE_DIRS = frozenset(
    {"clockwise", "counterclockwise", "across", "auto_dice"}
)


@dataclass(frozen=True, slots=True)
class EngineConfig:
    num_players: int = 4
    initial_score: int = 0
    exchange_dir: str = "auto_dice"
    fan_cap: int = 0  # 0 = no cap
    multi_ron: bool = True
    base_score: int = 1
    force_discard_dingque: bool = True
    enable_exchange: bool = True  # False → skip 换三张, go dingque

    def __post_init__(self) -> None:
        if self.num_players not in (2, 3, 4):
            raise ValueError(
                f"num_players must be 2, 3, or 4, got {self.num_players}"
            )
        if self.exchange_dir not in _EXCHANGE_DIRS:
            raise ValueError(
                f"exchange_dir must be one of {sorted(_EXCHANGE_DIRS)}, "
                f"got {self.exchange_dir!r}"
            )
        if self.fan_cap < 0:
            raise ValueError(f"fan_cap must be >= 0, got {self.fan_cap}")
        if self.base_score < 0:
            raise ValueError(f"base_score must be >= 0, got {self.base_score}")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> EngineConfig:
        if not isinstance(data, dict):
            raise ValueError("config must be a dict")
        return cls(
            num_players=int(data.get("num_players", 4)),
            initial_score=int(data.get("initial_score", 0)),
            exchange_dir=str(data.get("exchange_dir", "auto_dice")),
            fan_cap=int(data.get("fan_cap", 0)),
            multi_ron=bool(data.get("multi_ron", True)),
            base_score=int(data.get("base_score", 1)),
            force_discard_dingque=bool(data.get("force_discard_dingque", True)),
            enable_exchange=bool(data.get("enable_exchange", True)),
        )
