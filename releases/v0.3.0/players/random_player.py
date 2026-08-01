"""Random legal-action baseline player."""

from __future__ import annotations

from engine.action import Action, ActionType
from engine.exchange import pick_same_suit_triple
from engine.tile import Suit, parse_tile
from players.base_player import BasePlayer
from protocols.messages import ActionRequest, Decision


class RandomPlayer(BasePlayer):
    def on_join(self, seat: int, config: dict) -> None:
        self.seat = seat
        self.config = dict(config or {})
        if not self.name or self.name == "RandomPlayer":
            self.name = f"Random-{seat}"

    def decide(self, request: ActionRequest) -> Decision:
        if not request.legal_actions:
            raise RuntimeError(f"no legal actions for seat {request.seat}")
        action = self.rng.choice(list(request.legal_actions))
        return Decision(
            request_id=request.request_id,
            action=action,
            reason=f"random:{action.type.value}",
        )

    def decide_opening_exchange(self, hand_ids: list[str]) -> list:
        """Helper used if legal list empty — prefer pick_same_suit_triple path via legal."""
        from engine.tile import Tile

        hand = [parse_tile(i) for i in hand_ids]
        return pick_same_suit_triple(hand)
