"""Blood-battle play state machine (M04)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from engine.action import Action, ActionType
from engine.config import EngineConfig
from engine.fan import WinContext, compute_fan
from engine.hand_utils import melds_from_raw
from engine.legal import action_in_legal, legal_actions
from engine.rules import config_from_state
from engine.score import ScoreService
from engine.state import GameState, PlayerState
from engine.tile import Tile, parse_tile
from engine.win_check import is_winning_hand


class PlayError(ValueError):
    """Illegal play-phase transition or action."""


@dataclass
class GameResult:
    game_id: str
    rankings: list[int]
    scores: dict[int, int]
    hu_sequence: list[dict]
    finished_reason: str
    wall_remaining: int
    settle_tags: dict = field(default_factory=dict)
    # F0008: raw score events (type==score) for per-seat breakdown UI
    score_events: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "game_id": self.game_id,
            "rankings": list(self.rankings),
            "scores": {str(k): v for k, v in self.scores.items()},
            "hu_sequence": list(self.hu_sequence),
            "finished_reason": self.finished_reason,
            "wall_remaining": self.wall_remaining,
            "settle_tags": dict(self.settle_tags or {}),
            "score_events": list(self.score_events or []),
        }


def _score_svc(cfg: EngineConfig) -> ScoreService:
    return ScoreService(cfg)


def player_at(state: GameState, seat: int) -> PlayerState:
    for p in state.players:
        if p.seat == seat:
            return p
    raise PlayError(f"missing seat {seat}")


def active_seats(state: GameState) -> list[int]:
    return [p.seat for p in state.players if p.status == "active"]


def next_active(state: GameState, after_seat: int) -> int | None:
    n = state.num_players
    for k in range(1, n + 1):
        s = (after_seat + k) % n
        if player_at(state, s).status == "active":
            return s
    return None


def _remove_one(hand: list[Tile], tile: Tile) -> None:
    for i, t in enumerate(hand):
        if t.id == tile.id:
            del hand[i]
            return
    raise PlayError(f"tile {tile.id} not in hand")


def _remove_n(hand: list[Tile], tile: Tile, n: int) -> None:
    for _ in range(n):
        _remove_one(hand, tile)


def _meld_dict(kind: str, tile: Tile) -> dict:
    return {"kind": kind, "tile_id": tile.id}


def _append_event(state: GameState, etype: str, **payload: Any) -> None:
    if state.score_events is None:
        state.score_events = []
    state.score_events.append(
        {"type": etype, "turn_index": state.turn_index, "payload": payload}
    )


def finalize_game(state: GameState, cfg: EngineConfig | None = None) -> None:
    """Run end settlement once when phase is finished."""
    if state.phase != "finished":
        return
    config = config_from_state(state, cfg)
    _score_svc(config).settle_end(state)


def _mark_finished(
    state: GameState, reason: str, cfg: EngineConfig | None = None
) -> None:
    state.phase = "finished"
    state.finished_reason = reason
    finalize_game(state, cfg)


def _check_terminal(state: GameState, cfg: EngineConfig | None = None) -> bool:
    """
    Blood-battle (血战到底) terminal check.

    Game ends only when **≤1 active** players remain (others have hu'd/left)
    — **not** when the first player hus. Wall-empty is handled separately in
    do_draw / gang paths.
    """
    act = active_seats(state)
    if len(act) <= 1:
        _mark_finished(state, "last_one", cfg)
        return True
    return False


def _continue_after_hu(
    state: GameState, after_seat: int, cfg: EngineConfig
) -> None:
    """
    After one or more seats hu and leave the table, continue the hand from
    the next still-active seat (血战). Never end solely because someone hu'd.
    """
    if _check_terminal(state, cfg):
        return
    nxt = next_active(state, after_seat)
    if nxt is None:
        _mark_finished(state, "last_one", cfg)
        return
    state.current_seat = nxt
    state.phase = "draw"
    do_draw(state)


def force_complete_response(
    state: GameState, config: EngineConfig | None = None
) -> bool:
    """
    If response phase is stuck (missing claims), fill PASS for any seat that
    has not answered and resolve. Returns True if resolve ran.
    """
    if state.phase != "response":
        return False
    cfg = config_from_state(state, config)
    needed = list(state.response_seats or [])
    if not needed:
        # desynced: treat as all-pass from last discarder
        ds = state.last_discard_seat
        if ds is not None:
            _after_all_pass(state, ds, cfg)
            return True
        return False
    claims = dict(state.pending_claims or {})
    changed = False
    for s in needed:
        if s not in claims:
            claims[s] = Action(ActionType.PASS)
            changed = True
    if not changed and set(needed).issubset(claims.keys()):
        # already complete but not resolved — resolve now
        state.pending_claims = claims
        _resolve_response(state, cfg)
        return True
    if changed:
        state.pending_claims = claims
        if set(needed).issubset(state.pending_claims.keys()):
            _resolve_response(state, cfg)
            return True
    return False


def start_play(state: GameState, config: EngineConfig | None = None) -> GameState:
    if state.phase != "ready":
        raise PlayError(f"start_play requires ready, got {state.phase!r}")
    cfg = config_from_state(state, config)
    state.config = cfg.to_dict()
    state.phase = "discard"
    state.current_seat = state.dealer_seat
    state.schema_version = 4
    state.last_discard = None
    state.last_discard_seat = None
    state.response_seats = []
    state.pending_claims = {}
    state.last_draw_tile = None
    state.after_gang_draw = False
    state.qiang_gang_context = None
    state.finished_reason = None
    state.end_settled = False
    state.settle_tags = {}
    if state.score_events is None:
        state.score_events = []
    if state.hu_sequence is None:
        state.hu_sequence = []
    _append_event(state, "start_play", dealer=state.dealer_seat)
    return state


def do_draw(state: GameState) -> GameState:
    """Execute draw for current_seat; wall empty → finish."""
    if state.phase != "draw":
        raise PlayError(f"do_draw requires draw, got {state.phase!r}")
    seat = state.current_seat
    if seat is None:
        raise PlayError("current_seat is None")
    if player_at(state, seat).status != "active":
        nxt = next_active(state, seat)
        if nxt is None:
            _mark_finished(state, "last_one")
            return state
        state.current_seat = nxt
        seat = nxt

    if not state.wall:
        _append_event(state, "wall_empty")
        _mark_finished(state, "wall_empty")
        return state

    tile = state.wall.pop(0)
    p = player_at(state, seat)
    p.hand.append(tile)
    p.sort_hand_inplace()
    state.last_draw_tile = tile
    state.phase = "discard"
    _append_event(state, "draw", seat=seat, tile=tile.id)
    return state


def _enter_response(
    state: GameState, from_seat: int, cfg: EngineConfig | None = None
) -> None:
    others = [s for s in active_seats(state) if s != from_seat]
    # seats that might act — all others (PASS always legal)
    state.response_seats = others
    state.pending_claims = {}
    if not others:
        # no one to respond
        _after_all_pass(state, from_seat, cfg)
        return
    state.phase = "response"


def _after_all_pass(
    state: GameState, discard_seat: int, cfg: EngineConfig | None = None
) -> None:
    state.qiang_gang_context = None
    state.after_gang_draw = False
    nxt = next_active(state, discard_seat)
    if nxt is None:
        _mark_finished(state, "last_one", cfg)
        return
    state.current_seat = nxt
    state.phase = "draw"
    state.response_seats = []
    state.pending_claims = {}
    do_draw(state)


def _distance_from(discard_seat: int, seat: int, n: int) -> int:
    return (seat - discard_seat) % n


def _resolve_response(state: GameState, cfg: EngineConfig) -> None:
    claims: dict[int, Action] = dict(state.pending_claims or {})
    for s in state.response_seats or []:
        if s not in claims:
            claims[s] = Action(ActionType.PASS)

    discard_seat = state.last_discard_seat
    if discard_seat is None and state.qiang_gang_context:
        discard_seat = int(state.qiang_gang_context["seat"])
    if discard_seat is None:
        raise PlayError("no discard seat for response")

    n = state.num_players
    # HU claims
    hu_seats = [s for s, a in claims.items() if a.type == ActionType.HU]
    if hu_seats:
        hu_seats.sort(key=lambda s: _distance_from(discard_seat, s, n))
        if not cfg.multi_ron:
            hu_seats = hu_seats[:1]

        is_qiang = state.qiang_gang_context is not None
        disc = state.last_discard
        if is_qiang:
            disc = parse_tile(state.qiang_gang_context["tile"])
        if disc is None:
            raise PlayError("hu resolve missing discard tile")

        fans: dict[int, int] = {}
        for w in hu_seats:
            p = player_at(state, w)
            hand = list(p.hand) + [disc]
            melds = melds_from_raw(p.melds)
            ctx = WinContext(
                is_zimo=False,
                is_qiang_gang=is_qiang,
                is_gang_shang_pao=False,
            )
            try:
                fr = compute_fan(
                    hand, melds, p.dingque, disc, ctx, fan_cap=cfg.fan_cap
                )
                fan = fr.fan
            except Exception:
                fan = 0
            fans[w] = fan

        # score before marking finished
        loser = discard_seat
        svc = _score_svc(cfg)
        for w in hu_seats:
            p = player_at(state, w)
            p.hand.append(disc)
        svc.apply_hu_dianpao(state, hu_seats, loser, fans)
        for w in hu_seats:
            p = player_at(state, w)
            fan = fans[w]
            state.hu_count = (state.hu_count or 0) + 1
            p.status = "finished"
            p.hu_order = state.hu_count
            p.last_win = {
                "fan": fan,
                "zimo": False,
                "loser": loser,
                "qiang_gang": is_qiang,
            }
            state.hu_sequence.append(
                {"seat": w, "fan": fan, "zimo": False, "loser": loser}
            )
            _append_event(
                state, "hu", seat=w, fan=fan, zimo=False, loser=loser
            )

        state.qiang_gang_context = None
        state.pending_claims = {}
        state.response_seats = []
        state.turn_index += 1

        # 血战: winners leave table; continue from discarder's next active seat
        _continue_after_hu(state, discard_seat, cfg)
        return

    # PONG / GANG_MING — nearest to discarder
    claimers = [
        (s, a)
        for s, a in claims.items()
        if a.type in (ActionType.PONG, ActionType.GANG_MING)
    ]
    if claimers:
        claimers.sort(key=lambda x: _distance_from(discard_seat, x[0], n))
        seat, action = claimers[0]
        same_dist = [
            x
            for x in claimers
            if _distance_from(discard_seat, x[0], n)
            == _distance_from(discard_seat, seat, n)
        ]
        same_dist.sort(
            key=lambda x: 0 if x[1].type == ActionType.GANG_MING else 1
        )
        seat, action = same_dist[0]
        disc = state.last_discard
        assert disc is not None
        p = player_at(state, seat)
        svc = _score_svc(cfg)
        if action.type == ActionType.PONG:
            _remove_n(p.hand, disc, 2)
            p.sort_hand_inplace()
            p.melds.append(_meld_dict("pong", disc))
            state.current_seat = seat
            state.phase = "discard"
            state.after_gang_draw = False
            _append_event(state, "pong", seat=seat, tile=disc.id)
        else:
            _remove_n(p.hand, disc, 3)
            p.melds.append(_meld_dict("ming_gang", disc))
            state.current_seat = seat
            state.after_gang_draw = True
            _append_event(state, "gang_ming", seat=seat, tile=disc.id)
            svc.apply_gang(state, "gang_ming", seat, from_seat=discard_seat)
            if state.wall:
                t = state.wall.pop(0)
                p.hand.append(t)
                p.sort_hand_inplace()
                state.last_draw_tile = t
                state.phase = "discard"
            else:
                _mark_finished(state, "wall_empty", cfg)
        state.pending_claims = {}
        state.response_seats = []
        state.turn_index += 1
        return

    # all pass
    _after_all_pass(state, discard_seat, cfg)


def apply_action(
    state: GameState, seat: int, action: Action, config: EngineConfig | None = None
) -> GameState:
    cfg = config_from_state(state, config)
    legal = legal_actions(state, seat)
    if not action_in_legal(action, legal):
        raise PlayError(
            f"illegal action {action} for seat {seat} in phase {state.phase}; "
            f"legal={[str(a) for a in legal]}"
        )

    if state.phase == "discard":
        return _apply_discard_phase(state, seat, action, cfg)
    if state.phase == "response":
        return _apply_response_phase(state, seat, action, cfg)
    raise PlayError(f"no player actions in phase {state.phase}")


def _apply_discard_phase(
    state: GameState, seat: int, action: Action, cfg: EngineConfig
) -> GameState:
    p = player_at(state, seat)

    if action.type == ActionType.HU:
        melds = melds_from_raw(p.melds)
        if not is_winning_hand(p.hand, melds, p.dingque).ok:
            raise PlayError("cannot hu")
        ctx = WinContext(is_zimo=True, is_gang_shang_hua=bool(state.after_gang_draw))
        try:
            fr = compute_fan(
                p.hand, melds, p.dingque, None, ctx, fan_cap=cfg.fan_cap
            )
            fan = fr.fan
        except Exception:
            fan = 0
        _score_svc(cfg).apply_hu_zimo(state, seat, fan)
        state.hu_count = (state.hu_count or 0) + 1
        p.status = "finished"
        p.hu_order = state.hu_count
        p.last_win = {"fan": fan, "zimo": True, "loser": None}
        state.hu_sequence.append({"seat": seat, "fan": fan, "zimo": True})
        _append_event(state, "hu", seat=seat, fan=fan, zimo=True)
        state.after_gang_draw = False
        state.turn_index += 1
        # 血战: zimo winner leaves; continue from next active after winner
        _continue_after_hu(state, seat, cfg)
        return state

    if action.type == ActionType.DISCARD:
        if not action.tiles:
            raise PlayError("discard needs tile")
        tile = action.tiles[0]
        _remove_one(p.hand, tile)
        p.sort_hand_inplace()
        p.discard_pile.append(tile)
        state.last_discard = tile
        state.last_discard_seat = seat
        state.last_draw_tile = None
        state.after_gang_draw = False
        state.turn_index += 1
        _append_event(state, "discard", seat=seat, tile=tile.id)
        _enter_response(state, seat, cfg)
        return state

    if action.type == ActionType.GANG_AN:
        tile = action.tiles[0]
        _remove_n(p.hand, tile, 4)
        p.melds.append(_meld_dict("an_gang", tile))
        state.after_gang_draw = True
        _append_event(state, "gang_an", seat=seat, tile=tile.id)
        _score_svc(cfg).apply_gang(state, "gang_an", seat)
        if state.wall:
            t = state.wall.pop(0)
            p.hand.append(t)
            p.sort_hand_inplace()
            state.last_draw_tile = t
            state.phase = "discard"
        else:
            _mark_finished(state, "wall_empty", cfg)
        return state

    if action.type == ActionType.GANG_JIA:
        tile = action.tiles[0]
        # upgrade pong to jia_gang
        found = False
        for i, m in enumerate(p.melds):
            md = m if isinstance(m, dict) else {"kind": getattr(m, "kind"), "tile_id": m.tile.id}
            kind = md.get("kind")
            tid = md.get("tile_id") or md.get("tile")
            if kind == "pong" and tid == tile.id:
                p.melds[i] = _meld_dict("jia_gang", tile)
                found = True
                break
        if not found:
            raise PlayError("no pong for jia gang")
        _remove_one(p.hand, tile)
        # qiang gang opportunity
        state.qiang_gang_context = {"seat": seat, "tile": tile.id}
        state.last_discard = tile  # virtual
        state.last_discard_seat = seat
        others = [s for s in active_seats(state) if s != seat]
        can_any = False
        for s in others:
            op = player_at(state, s)
            if is_winning_hand(
                list(op.hand) + [tile], melds_from_raw(op.melds), op.dingque
            ).ok:
                can_any = True
                break
        if can_any:
            state.phase = "response"
            state.response_seats = others
            state.pending_claims = {}
            return state
        # no qiang — score jia gang and draw
        state.qiang_gang_context = None
        state.after_gang_draw = True
        _score_svc(cfg).apply_gang(state, "gang_jia", seat)
        if state.wall:
            t = state.wall.pop(0)
            p.hand.append(t)
            p.sort_hand_inplace()
            state.last_draw_tile = t
            state.phase = "discard"
        else:
            _mark_finished(state, "wall_empty", cfg)
        return state

    raise PlayError(f"unhandled action {action.type}")


def _apply_response_phase(
    state: GameState, seat: int, action: Action, cfg: EngineConfig
) -> GameState:
    if state.pending_claims is None:
        state.pending_claims = {}
    state.pending_claims[seat] = action
    # all submitted?
    needed = set(state.response_seats or [])
    if needed.issubset(state.pending_claims.keys()):
        _resolve_response(state, cfg)
    return state


def build_game_result(state: GameState) -> GameResult:
    if state.phase == "finished" and not getattr(state, "end_settled", False):
        finalize_game(state)
    scores = {p.seat: p.score for p in state.players}
    rankings = sorted(scores.keys(), key=lambda s: (-scores[s], s))
    score_events = [
        e
        for e in (state.score_events or [])
        if isinstance(e, dict) and (e.get("type") == "score" or e.get("transfers"))
    ]
    return GameResult(
        game_id=state.game_id,
        rankings=rankings,
        scores=scores,
        hu_sequence=list(state.hu_sequence or []),
        finished_reason=state.finished_reason or "unknown",
        wall_remaining=len(state.wall),
        settle_tags=dict(getattr(state, "settle_tags", None) or {}),
        score_events=score_events,
    )
