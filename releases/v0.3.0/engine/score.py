"""Chengdu blood-battle scoring service (M05)."""

from __future__ import annotations

import json
from engine.audit import canonical_hash
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from engine.config import EngineConfig
from engine.hand_utils import melds_from_raw
from engine.shanten import shanten
from engine.state import GameState, PlayerState
from engine.tile import Suit

def _default_score_path() -> Path:
    try:
        from app_paths import configs_dir

        return configs_dir() / "score_default.json"
    except Exception:
        return (
            Path(__file__).resolve().parent.parent / "configs" / "score_default.json"
        )


_DEFAULT_SCORE_PATH = _default_score_path()


@dataclass(frozen=True, slots=True)
class ScoreTransfer:
    reason: str
    from_seat: int
    to_seat: int
    amount: int
    fan: int | None = None
    meta: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = {
            "reason": self.reason,
            "from_seat": self.from_seat,
            "to_seat": self.to_seat,
            "amount": self.amount,
        }
        if self.fan is not None:
            d["fan"] = self.fan
        if self.meta:
            d["meta"] = dict(self.meta)
        return d


@dataclass
class ScoreTable:
    base_score: int = 1
    gang_ming_mult: int = 2
    gang_jia_mult: int = 1
    gang_an_mult: int = 2
    hua_zhu_fan: int = 3
    cha_jiao_mult: int = 1

    @classmethod
    def load(cls, path: Path | str | None = None) -> ScoreTable:
        p = Path(path) if path else _DEFAULT_SCORE_PATH
        if not p.exists():
            return cls()
        with p.open(encoding="utf-8") as f:
            data = json.load(f)
        return cls(
            base_score=int(data.get("base_score", 1)),
            gang_ming_mult=int(data.get("gang_ming_mult", 2)),
            gang_jia_mult=int(data.get("gang_jia_mult", 1)),
            gang_an_mult=int(data.get("gang_an_mult", 2)),
            hua_zhu_fan=int(data.get("hua_zhu_fan", 3)),
            cha_jiao_mult=int(data.get("cha_jiao_mult", 1)),
        )

    @classmethod
    def from_config(cls, cfg: EngineConfig, table: ScoreTable | None = None) -> ScoreTable:
        base = table or cls.load()
        return cls(
            base_score=cfg.base_score if cfg.base_score else base.base_score,
            gang_ming_mult=base.gang_ming_mult,
            gang_jia_mult=base.gang_jia_mult,
            gang_an_mult=base.gang_an_mult,
            hua_zhu_fan=base.hua_zhu_fan,
            cha_jiao_mult=base.cha_jiao_mult,
        )


def hu_points(fan: int, base: int) -> int:
    return base * (2 ** max(fan, 0))


def _player(state: GameState, seat: int) -> PlayerState:
    for p in state.players:
        if p.seat == seat:
            return p
    raise ValueError(f"missing seat {seat}")


def _active_seats(state: GameState) -> list[int]:
    return [p.seat for p in state.players if p.status == "active"]


def _balances(state: GameState) -> dict[int, int]:
    return {p.seat: p.score for p in state.players}


def _is_hua_zhu(p: PlayerState) -> bool:
    if p.dingque is None:
        return False
    if any(t.suit == p.dingque for t in p.hand):
        return True
    for m in melds_from_raw(p.melds):
        if m.tile.suit == p.dingque:
            return True
    return False


def _is_ting(p: PlayerState) -> bool:
    if _is_hua_zhu(p):
        return False
    r = shanten(p.hand, p.melds, p.dingque)
    return r.shanten == 0


class ScoreService:
    def __init__(
        self,
        config: EngineConfig,
        score_table: ScoreTable | None = None,
    ) -> None:
        self.config = config
        self.table = ScoreTable.from_config(config, score_table)

    def apply_transfers(
        self, state: GameState, transfers: list[ScoreTransfer]
    ) -> None:
        if not transfers:
            return
        ordered = tuple(p.score for p in sorted(state.players, key=lambda item: item.seat))
        conserved = tuple(
            LedgerTransfer(t.from_seat, t.to_seat, t.amount)
            for t in transfers
            if t.amount != 0
        )
        expected_after, delta = apply_conserved_transfers(ordered, conserved)
        for t in transfers:
            if t.amount == 0:
                continue
            _player(state, t.from_seat).score -= t.amount
            _player(state, t.to_seat).score += t.amount
        actual_after = tuple(p.score for p in sorted(state.players, key=lambda item: item.seat))
        if actual_after != expected_after or sum(delta) != 0:
            raise LedgerInvariantError("SCORE_NOT_ZERO_SUM")
        if state.score_events is None:
            state.score_events = []
        state.score_events.append(
            {
                "type": "score",
                "turn_index": state.turn_index,
                "transfers": [t.to_dict() for t in transfers],
                "balances_after": _balances(state),
            }
        )

    def apply_hu_zimo(
        self, state: GameState, winner: int, fan: int
    ) -> list[ScoreTransfer]:
        pts = hu_points(fan, self.table.base_score)
        transfers: list[ScoreTransfer] = []
        for p in state.players:
            if p.seat == winner:
                continue
            if p.status != "active":
                continue
            transfers.append(
                ScoreTransfer(
                    reason="hu_zimo",
                    from_seat=p.seat,
                    to_seat=winner,
                    amount=pts,
                    fan=fan,
                )
            )
        self.apply_transfers(state, transfers)
        return transfers

    def apply_hu_dianpao(
        self,
        state: GameState,
        winners: list[int],
        loser: int,
        fans: dict[int, int],
    ) -> list[ScoreTransfer]:
        transfers: list[ScoreTransfer] = []
        for w in winners:
            fan = fans.get(w, 0)
            pts = hu_points(fan, self.table.base_score)
            transfers.append(
                ScoreTransfer(
                    reason="hu_dianpao",
                    from_seat=loser,
                    to_seat=w,
                    amount=pts,
                    fan=fan,
                )
            )
        self.apply_transfers(state, transfers)
        return transfers

    def apply_gang(
        self,
        state: GameState,
        kind: str,
        gang_seat: int,
        from_seat: int | None = None,
    ) -> list[ScoreTransfer]:
        """
        kind: gang_ming | gang_an | gang_jia
        from_seat: required for ming gang (the discarder)
        """
        base = self.table.base_score
        transfers: list[ScoreTransfer] = []
        if kind == "gang_ming":
            if from_seat is None:
                return []
            amt = base * self.table.gang_ming_mult
            transfers.append(
                ScoreTransfer(
                    reason="gang_ming",
                    from_seat=from_seat,
                    to_seat=gang_seat,
                    amount=amt,
                )
            )
        elif kind == "gang_an":
            amt = base * self.table.gang_an_mult
            for s in _active_seats(state):
                if s == gang_seat:
                    continue
                transfers.append(
                    ScoreTransfer(
                        reason="gang_an",
                        from_seat=s,
                        to_seat=gang_seat,
                        amount=amt,
                    )
                )
        elif kind == "gang_jia":
            amt = base * self.table.gang_jia_mult
            for s in _active_seats(state):
                if s == gang_seat:
                    continue
                transfers.append(
                    ScoreTransfer(
                        reason="gang_jia",
                        from_seat=s,
                        to_seat=gang_seat,
                        amount=amt,
                    )
                )
        else:
            return []
        self.apply_transfers(state, transfers)
        return transfers

    def settle_end(self, state: GameState) -> list[ScoreTransfer]:
        """Hua-zhu + simplified cha-jiao. Idempotent via state.end_settled flag."""
        if getattr(state, "end_settled", False):
            return []
        transfers: list[ScoreTransfer] = []
        base = self.table.base_score

        # Flower pig: active players still holding dingque suit
        pigs = [
            p.seat
            for p in state.players
            if p.status == "active" and _is_hua_zhu(p)
        ]
        non_pigs = [p.seat for p in state.players if p.seat not in pigs]
        hua_pts = hu_points(self.table.hua_zhu_fan, base)
        for pig in pigs:
            for other in non_pigs:
                transfers.append(
                    ScoreTransfer(
                        reason="hua_zhu",
                        from_seat=pig,
                        to_seat=other,
                        amount=hua_pts,
                        fan=self.table.hua_zhu_fan,
                    )
                )

        # Simplified cha jiao among remaining active non-pigs
        candidates = [
            p
            for p in state.players
            if p.status == "active" and p.seat not in pigs
        ]
        ting = [p.seat for p in candidates if _is_ting(p)]
        not_ting = [p.seat for p in candidates if p.seat not in ting]
        cha_pts = base * self.table.cha_jiao_mult
        for nt in not_ting:
            for t in ting:
                transfers.append(
                    ScoreTransfer(
                        reason="cha_jiao",
                        from_seat=nt,
                        to_seat=t,
                        amount=cha_pts,
                    )
                )

        self.apply_transfers(state, transfers)
        state.end_settled = True
        # tags for result
        state.settle_tags = {
            "hua_zhu": pigs,
            "ting": ting,
            "not_ting": not_ting,
        }
        return transfers


# ---------------------------------------------------------------------------
# Score ledger (per-seat breakdown for UI / logs) — F0008
# ---------------------------------------------------------------------------

REASON_LABELS: dict[str, str] = {
    "hu_zimo": "自摸",
    "hu_dianpao": "点炮胡",
    "gang_ming": "明杠",
    "gang_an": "暗杠",
    "gang_jia": "补杠",
    "hua_zhu": "花猪",
    "cha_jiao": "查叫",
    "tax": "税费",
}


def reason_label(reason: str) -> str:
    r = str(reason or "")
    return REASON_LABELS.get(r, r or "分变")


def format_score_line(
    *,
    delta: int,
    reason: str,
    counterparty: int,
    fan: int | None = None,
) -> str:
    """One human-readable ledger line, e.g. '+4 点炮胡(2番) ←S1'."""
    sign = f"+{delta}" if delta >= 0 else str(delta)
    label = reason_label(reason)
    fan_s = f"({fan}番)" if fan is not None else ""
    arrow = "←" if delta >= 0 else "→"
    return f"{sign} {label}{fan_s} {arrow}S{counterparty}"


def build_score_ledger(
    score_events: list[dict] | None,
) -> dict[int, list[dict[str, Any]]]:
    """
    Flatten score_events transfers into per-seat detail lines.

    Each line dict:
      delta, reason, label, counterparty, fan, text
    """
    ledger: dict[int, list[dict[str, Any]]] = {}
    for ev in score_events or []:
        if not isinstance(ev, dict):
            continue
        transfers = ev.get("transfers")
        if not transfers:
            continue
        for t in transfers:
            if not isinstance(t, dict):
                continue
            try:
                amount = int(t.get("amount") or 0)
                fr = int(t["from_seat"])
                to = int(t["to_seat"])
            except (KeyError, TypeError, ValueError):
                continue
            if amount == 0:
                continue
            reason = str(t.get("reason") or "")
            fan = t.get("fan")
            fan_i = int(fan) if fan is not None else None
            # receiver
            ledger.setdefault(to, []).append(
                {
                    "delta": amount,
                    "reason": reason,
                    "label": reason_label(reason),
                    "counterparty": fr,
                    "fan": fan_i,
                    "text": format_score_line(
                        delta=amount, reason=reason, counterparty=fr, fan=fan_i
                    ),
                }
            )
            # payer
            ledger.setdefault(fr, []).append(
                {
                    "delta": -amount,
                    "reason": reason,
                    "label": reason_label(reason),
                    "counterparty": to,
                    "fan": fan_i,
                    "text": format_score_line(
                        delta=-amount, reason=reason, counterparty=to, fan=fan_i
                    ),
                }
            )
    return ledger


def ledger_net(lines: list[dict[str, Any]]) -> int:
    return sum(int(x.get("delta") or 0) for x in lines)
@dataclass(frozen=True, slots=True)
class LedgerTransfer:
    payer: int
    receiver: int
    amount: int


class LedgerInvariantError(ValueError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def apply_conserved_transfers(balances: tuple[int, ...], transfers: tuple[LedgerTransfer, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """SCORE-001 atomic int64 transfer aggregation with zero-sum enforcement."""
    if not balances:
        raise LedgerInvariantError("TRANSFER_SCHEMA")
    delta = [0] * len(balances)
    for transfer in transfers:
        if not isinstance(transfer.amount, int) or isinstance(transfer.amount, bool) or transfer.amount <= 0:
            raise LedgerInvariantError("AMOUNT_RANGE")
        if not 0 <= transfer.payer < len(balances) or not 0 <= transfer.receiver < len(balances):
            raise LedgerInvariantError("SEAT_RANGE")
        if transfer.payer == transfer.receiver:
            raise LedgerInvariantError("SELF_TRANSFER")
        delta[transfer.payer] -= transfer.amount
        delta[transfer.receiver] += transfer.amount
    if sum(delta) != 0:
        raise LedgerInvariantError("SCORE_NOT_ZERO_SUM")
    after = tuple(value + change for value, change in zip(balances, delta))
    if any(not -(2**63) <= value <= 2**63 - 1 for value in (*delta, *after)):
        raise LedgerInvariantError("SCORE_OVERFLOW")
    return after, tuple(delta)


class ConservedScoreLedger:
    """SCORE-001 append-only idempotent event ledger."""
    def __init__(self, balances: tuple[int, ...]) -> None:
        self.balances=balances; self.events: dict[str, tuple[str, dict[str, Any]]] = {}; self.prev_hash: str|None=None
    def apply_event(self, *, event_id: str, layer: str, reason: str, transfers: tuple[LedgerTransfer,...]) -> dict[str,Any]:
        if not event_id: raise LedgerInvariantError("TRANSFER_SCHEMA")
        if layer not in {"atomic","round_settlement","match_total"}: raise LedgerInvariantError("TRANSFER_SCHEMA")
        payload={"event_id":event_id,"layer":layer,"reason":reason,"transfers":[{"from_seat":t.payer,"to_seat":t.receiver,"amount":t.amount} for t in transfers]}
        payload_hash=canonical_hash(payload)
        if event_id in self.events:
            old_hash,old=self.events[event_id]
            if old_hash != payload_hash: raise LedgerInvariantError("DUPLICATE_SCORE_EVENT")
            return {**old,"idempotent":True}
        after,delta=apply_conserved_transfers(self.balances,transfers)
        record={**payload,"before":self.balances,"delta":delta,"after":after,"sum_delta":sum(delta),"prev_hash":self.prev_hash}
        event_hash=canonical_hash(record); result={**record,"event_hash":event_hash,"idempotent":False}
        self.balances=after; self.prev_hash=event_hash; self.events[event_id]=(payload_hash,result)
        return result
