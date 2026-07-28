"""Legal action generation for blood-battle phases."""

from __future__ import annotations

from collections import Counter

from engine.action import Action, ActionType
from engine.hand_utils import melds_from_raw
from engine.rules import config_from_state, force_discard_dingque
from engine.state import GameState, PlayerState
from engine.tile import Tile
from engine.win_check import is_winning_hand


def _player(state: GameState, seat: int) -> PlayerState:
    for p in state.players:
        if p.seat == seat:
            return p
    raise ValueError(f"missing seat {seat}")


def _hand_counts(hand: list[Tile]) -> Counter:
    return Counter(t.id for t in hand)


def _can_hu_with(hand: list[Tile], melds, dingque, extra: Tile | None) -> bool:
    h = list(hand) if extra is None else list(hand) + [extra]
    return is_winning_hand(h, melds, dingque).ok


def legal_discards(state: GameState, seat: int) -> list[Action]:
    p = _player(state, seat)
    if p.status != "active":
        return []
    hand = p.hand
    force = force_discard_dingque(state)
    if force and p.dingque is not None:
        ding = [t for t in hand if t.suit == p.dingque]
        if ding:
            # unique faces
            seen: set[str] = set()
            out: list[Action] = []
            for t in ding:
                if t.id not in seen:
                    seen.add(t.id)
                    out.append(Action(ActionType.DISCARD, tiles=(t,)))
            return out
    seen = set()
    out = []
    for t in hand:
        if t.id not in seen:
            seen.add(t.id)
            out.append(Action(ActionType.DISCARD, tiles=(t,)))
    return out


def legal_actions(state: GameState, seat: int) -> list[Action]:
    """Return legal actions for seat in current phase."""
    if state.phase == "finished":
        return []
    if not 0 <= seat < state.num_players:
        return []

    p = _player(state, seat)
    if p.status != "active":
        return []

    if state.phase == "draw":
        return []  # engine auto-draws

    if state.phase == "discard":
        if state.current_seat != seat:
            return []
        actions: list[Action] = []
        actions.extend(legal_discards(state, seat))

        # Self HU
        melds = melds_from_raw(p.melds)
        if _can_hu_with(p.hand, melds, p.dingque, None):
            actions.append(Action(ActionType.HU))

        # An gang
        counts = _hand_counts(p.hand)
        for tid, n in counts.items():
            if n >= 4:
                tile = next(t for t in p.hand if t.id == tid)
                actions.append(Action(ActionType.GANG_AN, tiles=(tile,)))

        # Jia gang: pong meld + 1 in hand
        for m in melds_from_raw(p.melds):
            if m.kind == "pong" and counts[m.tile.id] >= 1:
                actions.append(Action(ActionType.GANG_JIA, tiles=(m.tile,)))

        return actions

    if state.phase == "response":
        if seat not in (state.response_seats or []):
            return []
        actions = [Action(ActionType.PASS)]
        # Qiang gang: only HU/PASS
        if state.qiang_gang_context:
            tile_id = state.qiang_gang_context.get("tile")
            from engine.tile import parse_tile

            tile = parse_tile(tile_id)
            melds = melds_from_raw(p.melds)
            if _can_hu_with(p.hand, melds, p.dingque, tile):
                actions.append(Action(ActionType.HU, tiles=(tile,)))
            return actions

        disc = state.last_discard
        if disc is None:
            return actions
        melds = melds_from_raw(p.melds)
        counts = _hand_counts(p.hand)
        if _can_hu_with(p.hand, melds, p.dingque, disc):
            actions.append(Action(ActionType.HU, tiles=(disc,)))
        if counts[disc.id] >= 2:
            actions.append(Action(ActionType.PONG, tiles=(disc,)))
        if counts[disc.id] >= 3:
            actions.append(Action(ActionType.GANG_MING, tiles=(disc,)))
        return actions

    return []


def action_in_legal(action: Action, legal: list[Action]) -> bool:
    """Compare by type and tile ids / suit."""
    for a in legal:
        if a.type != action.type:
            continue
        if a.suit != action.suit:
            continue
        if tuple(t.id for t in a.tiles) != tuple(t.id for t in action.tiles):
            continue
        return True
    return False
