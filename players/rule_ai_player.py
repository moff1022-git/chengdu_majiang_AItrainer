"""Lightweight rule-based AI player."""

from __future__ import annotations

from collections import Counter
from typing import Optional

from engine.action import Action, ActionType
from engine.exchange import pick_same_suit_triple
from engine.shanten import shanten
from engine.tile import Suit, Tile, parse_tile
from players.base_player import BasePlayer
from protocols.messages import ActionRequest, Decision


class RuleAIPlayer(BasePlayer):
    """Prefer HU/GANG/PONG; discard to minimize shanten; aggressive claims."""

    def on_join(self, seat: int, config: dict) -> None:
        self.seat = seat
        self.config = dict(config or {})
        # Strategy preset may set use_f0011 / strategy_id on the instance or in config
        if "use_f0011" in self.config:
            self.use_f0011 = bool(self.config.get("use_f0011"))
        if "strategy_id" in self.config:
            self.strategy_id = str(self.config.get("strategy_id"))
        sid = getattr(self, "strategy_id", None) or "rule_ai"
        if not self.name or self.name in ("RuleAIPlayer", "rule_ai", "rule_ai_plus"):
            tag = sid if sid != "rule_ai" else "RuleAI"
            self.name = f"{tag}-{seat}"

    def decide(self, request: ActionRequest) -> Decision:
        legal = list(request.legal_actions)
        if not legal:
            raise RuntimeError(f"no legal actions for seat {request.seat}")

        phase = request.phase
        if phase in ("exchange",):
            return self._decide_exchange(request, legal)
        if phase in ("dingque",):
            return self._decide_dingque(request, legal)
        if phase == "response":
            return self._decide_response(request, legal)
        if phase == "discard":
            return self._decide_discard(request, legal)

        # fallback
        action = legal[0]
        return Decision(
            request_id=request.request_id,
            action=action,
            reason=f"rule:fallback:{action.type.value}",
        )

    def _decide_exchange(
        self, request: ActionRequest, legal: list[Action]
    ) -> Decision:
        # Prefer any EXCHANGE in legal; else first
        for a in legal:
            if a.type == ActionType.EXCHANGE and len(a.tiles) == 3:
                return Decision(
                    request_id=request.request_id,
                    action=a,
                    reason="rule:exchange_same_suit",
                )
        a = legal[0]
        return Decision(
            request_id=request.request_id,
            action=a,
            reason=f"rule:exchange:{a.type.value}",
        )

    def _decide_dingque(
        self, request: ActionRequest, legal: list[Action]
    ) -> Decision:
        # Prefer dingque the suit with fewest tiles in hand if we have view
        hand_ids: list[str] = []
        if self.last_observation:
            for p in self.last_observation.view.get("players") or []:
                if int(p.get("seat", -1)) == request.seat:
                    hand_ids = list(p.get("hand") or [])
                    break
        if hand_ids:
            counts = {Suit.WAN: 0, Suit.TONG: 0, Suit.TIAO: 0}
            for hid in hand_ids:
                t = parse_tile(hid)
                counts[t.suit] += 1
            best_suit = min(counts.keys(), key=lambda s: counts[s])
            for a in legal:
                if a.type == ActionType.DINGQUE and a.suit == best_suit:
                    return Decision(
                        request_id=request.request_id,
                        action=a,
                        reason=f"rule:dingque_min_count:{best_suit.value}",
                        analysis={"suit_counts": {k.value: v for k, v in counts.items()}},
                    )
        for a in legal:
            if a.type == ActionType.DINGQUE:
                return Decision(
                    request_id=request.request_id,
                    action=a,
                    reason=f"rule:dingque:{a.suit}",
                )
        a = legal[0]
        return Decision(request_id=request.request_id, action=a, reason="rule:dingque_fallback")

    def _decide_response(
        self, request: ActionRequest, legal: list[Action]
    ) -> Decision:
        order = [
            ActionType.HU,
            ActionType.GANG_MING,
            ActionType.PONG,
            ActionType.PASS,
        ]
        for typ in order:
            for a in legal:
                if a.type == typ:
                    return Decision(
                        request_id=request.request_id,
                        action=a,
                        reason=f"rule:{typ.value}",
                    )
        a = legal[0]
        return Decision(
            request_id=request.request_id, action=a, reason=f"rule:response:{a.type.value}"
        )

    def _decide_discard(
        self, request: ActionRequest, legal: list[Action]
    ) -> Decision:
        for typ in (ActionType.HU, ActionType.GANG_AN, ActionType.GANG_JIA):
            for a in legal:
                if a.type == typ:
                    return Decision(
                        request_id=request.request_id,
                        action=a,
                        reason=f"rule:{typ.value}",
                    )

        discards = [a for a in legal if a.type == ActionType.DISCARD]
        if not discards:
            a = legal[0]
            return Decision(
                request_id=request.request_id,
                action=a,
                reason=f"rule:discard_fallback:{a.type.value}",
            )

        # M08: force analysis pipeline when full state is available
        from players.analysis.pipeline import analyze_for_seat

        state = getattr(self, "_engine_state", None)
        if state is not None:
            use_f = getattr(self, "use_f0011", None)
            if use_f is None and isinstance(getattr(self, "config", None), dict):
                use_f = self.config.get("use_f0011")
            snap = analyze_for_seat(
                state,
                request.seat,
                legal_discards=discards,
                use_f0011=use_f,
            )
            if snap.discard_ranks:
                best_id = snap.discard_ranks[0].tile_id
                tag = getattr(self, "strategy_id", None) or "rule"
                for a in discards:
                    if a.tiles and a.tiles[0].id == best_id:
                        return Decision(
                            request_id=request.request_id,
                            action=a,
                            reason=f"{tag}:pipeline:{best_id}",
                            analysis=snap.to_dict(),
                        )

        hand, melds, dingque = self._read_private_hand(request.seat)
        if hand is None:
            a = self.rng.choice(discards)
            return Decision(
                request_id=request.request_id,
                action=a,
                reason=f"rule:discard_random:{a.tiles[0].id}",
            )

        # Fallback without engine state: shanten-min (still pipeline-like)
        from engine.state import GameState  # noqa: F401
        from players.analysis.types import AnalysisSnapshot  # local ranking

        best_action = discards[0]
        best_sh = 99
        candidates = []
        for a in discards:
            tile = a.tiles[0]
            trial_hand = []
            removed = False
            for t in hand:
                if not removed and t.id == tile.id:
                    removed = True
                    continue
                trial_hand.append(t)
            try:
                s = shanten(trial_hand, melds or [], dingque)
                sh_val = s.shanten
            except Exception:
                sh_val = 8
            candidates.append({"tile": tile.id, "shanten": sh_val})
            if sh_val < best_sh:
                best_sh = sh_val
                best_action = a

        return Decision(
            request_id=request.request_id,
            action=best_action,
            reason=f"rule:discard_min_shanten:{best_action.tiles[0].id}",
            analysis={"shanten": best_sh, "best": best_action.tiles[0].id, "candidates": candidates[:8]},
        )

    def _read_private_hand(
        self, seat: int
    ) -> tuple[Optional[list[Tile]], list, Optional[Suit]]:
        if not self.last_observation:
            return None, [], None
        for p in self.last_observation.view.get("players") or []:
            if int(p.get("seat", -1)) != seat:
                continue
            hand_ids = p.get("hand") or []
            hand = [parse_tile(i) for i in hand_ids]
            melds = p.get("melds") or []
            dq = p.get("dingque")
            dingque = Suit(dq) if dq else None
            return hand, melds, dingque
        return None, [], None
