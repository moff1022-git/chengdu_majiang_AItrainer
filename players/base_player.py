"""Standard player interface."""

from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import Any, Optional
from uuid import uuid4

from protocols.messages import ActionRequest, Decision, Observation


class BasePlayer(ABC):
    def __init__(
        self,
        name: str = "",
        player_id: str | None = None,
        *,
        seed: int | None = None,
        training_mode: bool = True,
    ) -> None:
        self.name = name or self.__class__.__name__
        self.player_id = player_id or uuid4().hex[:8]
        self.seat: int | None = None
        self.training_mode = training_mode
        self.config: dict = {}
        self.last_observation: Observation | None = None
        self.rng = random.Random(seed if seed is not None else random.randrange(1 << 30))

    @abstractmethod
    def on_join(self, seat: int, config: dict) -> None:
        ...

    def observe(self, observation: Observation) -> None:
        self.last_observation = observation

    @abstractmethod
    def decide(self, request: ActionRequest) -> Decision:
        ...

    def on_event(self, event: dict) -> None:
        return None

    def on_game_end(self, result: dict) -> None:
        return None

    def shutdown(self) -> None:
        return None
