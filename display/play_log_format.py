"""Format engine score_events / public state into detailed play-log lines (F0024)."""

from __future__ import annotations

from typing import Any

from engine.score import reason_label

_SUIT_ZH = {"wan": "万", "tong": "筒", "tiao": "条"}

_EVENT_KIND_ZH = {
    "start_play": "行牌开始",
    "draw": "摸牌",
    "discard": "打出",
    "pong": "碰",
    "gang_ming": "明杠",
    "gang_an": "暗杠",
    "gang_jia": "补杠",
    "hu": "胡",
    "wall_empty": "流局",
    "score": "计分",
}

_REASON_ZH_EXTRA = {
    "hu_zimo": "自摸",
    "hu_dianpao": "点炮胡",
    "gang_ming": "明杠",
    "gang_an": "暗杠",
    "gang_jia": "补杠",
    "hua_zhu": "花猪",
    "cha_jiao": "查叫",
}


def tile_zh(tile_id: Any) -> str:
    """wan_3 → 3万."""
    if tile_id is None:
        return "?"
    if hasattr(tile_id, "id"):
        tile_id = tile_id.id
    s = str(tile_id)
    try:
        suit, rank = s.split("_", 1)
        return f"{rank}{_SUIT_ZH.get(suit, suit)}"
    except Exception:
        return s


def seat_s(seat: Any) -> str:
    if seat is None:
        return "S?"
    try:
        return f"S{int(seat)}"
    except (TypeError, ValueError):
        return f"S{seat}"


def _payload(ev: dict) -> dict:
    p = ev.get("payload")
    return p if isinstance(p, dict) else {}


def _turn_prefix(ev: dict) -> str:
    t = ev.get("turn_index")
    if t is None:
        return ""
    try:
        return f"T{int(t)} "
    except (TypeError, ValueError):
        return ""


def format_score_events_delta(
    events: list[dict],
    start_index: int = 0,
) -> list[tuple[str, str, int | None, str | None]]:
    """
    Format new score_events[start_index:] into play-log rows.

    Returns list of (kind, text, seat, tile_id).
    """
    out: list[tuple[str, str, int | None, str | None]] = []
    if not events:
        return out
    start = max(0, int(start_index))
    for ev in events[start:]:
        if not isinstance(ev, dict):
            continue
        out.extend(format_one_event(ev))
    return out


def format_one_event(ev: dict) -> list[tuple[str, str, int | None, str | None]]:
    et = str(ev.get("type") or "")
    pl = _payload(ev)
    tp = _turn_prefix(ev)
    rows: list[tuple[str, str, int | None, str | None]] = []

    if et == "start_play":
        dealer = pl.get("dealer", pl.get("dealer_seat"))
        rows.append(
            (
                "info",
                f"{tp}▶ 行牌开始 · 庄家 {seat_s(dealer)}",
                int(dealer) if dealer is not None else None,
                None,
            )
        )
        return rows

    if et == "draw":
        seat = pl.get("seat")
        tid = pl.get("tile")
        rows.append(
            (
                "draw",
                f"{tp}{seat_s(seat)} 摸 {tile_zh(tid)}",
                int(seat) if seat is not None else None,
                str(tid) if tid else None,
            )
        )
        return rows

    if et == "discard":
        seat = pl.get("seat")
        tid = pl.get("tile")
        rows.append(
            (
                "discard",
                f"{tp}{seat_s(seat)} 打出 {tile_zh(tid)}",
                int(seat) if seat is not None else None,
                str(tid) if tid else None,
            )
        )
        return rows

    if et == "pong":
        seat = pl.get("seat")
        tid = pl.get("tile")
        rows.append(
            (
                "pong",
                f"{tp}{seat_s(seat)} 碰 {tile_zh(tid)}",
                int(seat) if seat is not None else None,
                str(tid) if tid else None,
            )
        )
        return rows

    if et in ("gang_ming", "gang_an", "gang_jia"):
        seat = pl.get("seat")
        tid = pl.get("tile")
        label = {"gang_ming": "明杠", "gang_an": "暗杠", "gang_jia": "补杠"}.get(
            et, "杠"
        )
        rows.append(
            (
                "gang",
                f"{tp}{seat_s(seat)} {label} {tile_zh(tid)}",
                int(seat) if seat is not None else None,
                str(tid) if tid else None,
            )
        )
        return rows

    if et == "hu":
        seat = pl.get("seat")
        fan = pl.get("fan")
        zimo = bool(pl.get("zimo"))
        loser = pl.get("loser")
        fan_s = f" {fan}番" if fan is not None else ""
        if zimo:
            text = f"{tp}★ {seat_s(seat)} 自摸{fan_s}"
        else:
            text = f"{tp}★ {seat_s(seat)} 胡{fan_s}"
            if loser is not None:
                text += f" · 点炮 {seat_s(loser)}"
        rows.append(
            (
                "hu",
                text,
                int(seat) if seat is not None else None,
                None,
            )
        )
        return rows

    if et == "wall_empty":
        rows.append(("info", f"{tp}流局 · 牌墙摸尽", None, None))
        return rows

    if et == "score":
        transfers = ev.get("transfers") or []
        for t in transfers:
            if not isinstance(t, dict):
                continue
            try:
                amount = int(t.get("amount") or 0)
                fr = int(t.get("from_seat"))
                to = int(t.get("to_seat"))
            except (TypeError, ValueError):
                continue
            if amount == 0:
                continue
            reason = str(t.get("reason") or "")
            fan = t.get("fan")
            label = reason_label(reason)
            fan_s = f"({fan}番)" if fan is not None else ""
            # One summary for the money movement
            rows.append(
                (
                    "score",
                    f"{tp}分  {seat_s(to)}+{amount} {label}{fan_s} ←{seat_s(fr)}",
                    to,
                    None,
                )
            )
        bal = ev.get("balances_after")
        # Compact board after multi-seat score (zimo 3-way, end settle, etc.)
        if isinstance(bal, dict) and bal and len(transfers) >= 1:
            parts = []
            try:
                for k in sorted(bal.keys(), key=lambda x: int(x)):
                    v = int(bal[k])
                    parts.append(f"S{k}:{v:+d}" if v != 0 else f"S{k}:0")
            except Exception:
                parts = [f"S{k}:{bal[k]}" for k in bal]
            # Only add summary when useful (2+ seats changed or multi transfer)
            if parts and (len(transfers) >= 2 or len(parts) >= 3):
                rows.append(("info", f"{tp}分后 " + " ".join(parts), None, None))
        return rows

    # Unknown / generic
    if et:
        rows.append(("info", f"{tp}{et} {_payload_brief(pl)}".strip(), None, None))
    return rows


def _payload_brief(pl: dict) -> str:
    if not pl:
        return ""
    bits = []
    if "seat" in pl:
        bits.append(seat_s(pl.get("seat")))
    if "tile" in pl:
        bits.append(tile_zh(pl.get("tile")))
    if "dealer" in pl:
        bits.append(f"庄{seat_s(pl.get('dealer'))}")
    return " ".join(bits)


def format_phase_line(phase: str, state: Any) -> str | None:
    """One-shot phase banners (opening)."""
    ph = str(phase or "")
    if ph == "exchange":
        d = getattr(state, "exchange_dir_resolved", None)
        d_zh = {
            "clockwise": "顺时针",
            "counterclockwise": "逆时针",
            "across": "对家",
        }.get(str(d or ""), str(d or "—"))
        return f"◆ 换三张 · 方向 {d_zh}"
    if ph == "dingque":
        return "◆ 定缺阶段 · 各选一门"
    if ph == "ready":
        return "◆ 定缺完成 · 准备行牌"
    if ph == "dealt":
        return "◆ 发牌完成"
    return None


def format_dingque_done(state: Any) -> str | None:
    """When all seats have dingque, summarize suits."""
    players = getattr(state, "players", None) or []
    parts = []
    for p in players:
        seat = getattr(p, "seat", None)
        dq = getattr(p, "dingque", None)
        if dq is None:
            return None
        val = getattr(dq, "value", dq)
        zh = _SUIT_ZH.get(str(val).lower(), str(val))
        parts.append(f"{seat_s(seat)}缺{zh}")
    if not parts:
        return None
    return "定缺 " + " · ".join(parts)


def format_finish_summary(state: Any) -> list[str]:
    """End-of-hand multi-line summary."""
    lines: list[str] = []
    reason = getattr(state, "finished_reason", None) or "?"
    reason_zh = {
        "last_one": "血战末家",
        "wall_empty": "流局·墙尽",
        "max_steps": "步数上限",
        "error": "异常",
    }.get(str(reason), str(reason))
    lines.append(f"■ 本局结束 · {reason_zh}")
    seq = list(getattr(state, "hu_sequence", None) or [])
    if seq:
        bits = []
        for h in seq:
            if not isinstance(h, dict):
                continue
            seat = h.get("seat")
            fan = h.get("fan")
            zimo = h.get("zimo")
            loser = h.get("loser")
            fan_s = f"{fan}番" if fan is not None else ""
            if zimo:
                bits.append(f"{seat_s(seat)}自摸{fan_s}")
            else:
                s = f"{seat_s(seat)}胡{fan_s}"
                if loser is not None:
                    s += f"(点炮{seat_s(loser)})"
                bits.append(s)
        if bits:
            lines.append("胡序 " + " → ".join(bits))
    scores = []
    for p in getattr(state, "players", None) or []:
        try:
            sc = int(getattr(p, "score", 0))
            scores.append(f"{seat_s(p.seat)}:{sc:+d}" if sc else f"{seat_s(p.seat)}:0")
        except Exception:
            pass
    if scores:
        lines.append("得分 " + "  ".join(scores))
    tags = getattr(state, "settle_tags", None) or {}
    if tags:
        pigs = tags.get("hua_zhu") or []
        ting = tags.get("ting") or []
        not_ting = tags.get("not_ting") or []
        if pigs or not_ting:
            lines.append(
                f"查叫 花猪:{_seats(pigs)} 有叫:{_seats(ting)} 未叫:{_seats(not_ting)}"
            )
    return lines


def _seats(raw: Any) -> str:
    if not raw:
        return "—"
    if isinstance(raw, (list, tuple)):
        return ",".join(seat_s(x) for x in raw)
    return str(raw)
