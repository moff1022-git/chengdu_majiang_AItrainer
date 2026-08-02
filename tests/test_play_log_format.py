"""Detailed main-window play log formatting."""

from __future__ import annotations

from display.play_log_format import (
    format_finish_summary,
    format_one_event,
    format_score_events_delta,
    tile_zh,
)
from engine.deal import create_dealt_game
from engine.state import GameState


def test_tile_zh() -> None:
    assert tile_zh("wan_3") == "3万"
    assert tile_zh("tong_9") == "9筒"
    assert tile_zh("tiao_1") == "1条"


def test_format_discard_draw_pong() -> None:
    rows = format_one_event(
        {"type": "discard", "turn_index": 3, "payload": {"seat": 1, "tile": "wan_5"}}
    )
    assert len(rows) == 1
    kind, text, seat, tid = rows[0]
    assert kind == "discard"
    assert "S1" in text and "5万" in text and "打出" in text
    assert seat == 1

    rows = format_one_event(
        {"type": "draw", "turn_index": 2, "payload": {"seat": 0, "tile": "tiao_2"}}
    )
    assert "摸" in rows[0][1] and "2条" in rows[0][1]

    rows = format_one_event(
        {"type": "pong", "turn_index": 4, "payload": {"seat": 2, "tile": "tong_7"}}
    )
    assert "碰" in rows[0][1] and "7筒" in rows[0][1]


def test_format_hu_and_score() -> None:
    rows = format_one_event(
        {
            "type": "hu",
            "turn_index": 10,
            "payload": {"seat": 0, "fan": 2, "zimo": True},
        }
    )
    assert "自摸" in rows[0][1] and "2番" in rows[0][1]

    rows = format_one_event(
        {
            "type": "score",
            "turn_index": 10,
            "transfers": [
                {
                    "reason": "hu_zimo",
                    "from_seat": 1,
                    "to_seat": 0,
                    "amount": 4,
                    "fan": 2,
                }
            ],
            "balances_after": {"0": 4, "1": -4, "2": 0, "3": 0},
        }
    )
    assert any("S0+4" in r[1] for r in rows)
    assert any("分后" in r[1] for r in rows)


def test_format_delta_batch() -> None:
    events = [
        {"type": "start_play", "turn_index": 0, "payload": {"dealer": 2}},
        {"type": "draw", "turn_index": 0, "payload": {"seat": 2, "tile": "wan_1"}},
        {"type": "discard", "turn_index": 1, "payload": {"seat": 2, "tile": "wan_9"}},
    ]
    rows = format_score_events_delta(events, 0)
    assert len(rows) == 3
    assert "行牌开始" in rows[0][1]
    rows2 = format_score_events_delta(events, 2)
    assert len(rows2) == 1
    assert "打出" in rows2[0][1]


def test_finish_summary() -> None:
    st = create_dealt_game("log-fin", num_players=4)
    st.phase = "finished"
    st.finished_reason = "last_one"
    st.hu_sequence = [{"seat": 0, "fan": 1, "zimo": True}]
    lines = format_finish_summary(st)
    assert any("本局结束" in x for x in lines)
    assert any("胡序" in x for x in lines)
