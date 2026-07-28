"""Transport between orchestrator and players."""

from __future__ import annotations

from typing import Protocol

from players.base_player import BasePlayer
from protocols.messages import ActionRequest, Decision, Observation


class PlayerTransport(Protocol):
    def send_observation(self, player: BasePlayer, obs: Observation) -> None: ...
    def request_decision(
        self, player: BasePlayer, request: ActionRequest
    ) -> Decision: ...


class InProcessTransport:
    """Direct in-process calls (AI / headless)."""

    def send_observation(self, player: BasePlayer, obs: Observation) -> None:
        player.observe(obs)

    def request_decision(
        self, player: BasePlayer, request: ActionRequest
    ) -> Decision:
        return player.decide(request)
