"""F0002: seat window protocol + hub smoke (no real display required)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

from engine.deal import create_dealt_game
from protocols.view_filter import build_observation
from protocols.wire import encode_line, msg_observation


def test_s01_watch_hello_and_obs(tmp_path: Path) -> None:
    """Minimal fake watch client: hello then accept one observation."""
    script = tmp_path / "fake_watch.py"
    script.write_text(
        textwrap.dedent(
            """
            import json, sys, os
            def emit(o):
                sys.stdout.write(json.dumps(o)+\"\\n\")
                sys.stdout.flush()
            emit({\"type\":\"hello\",\"seat\":1,\"version\":1,\"pid\":os.getpid()})
            for line in sys.stdin:
                msg = json.loads(line)
                if msg.get(\"type\") == \"observation\":
                    assert \"view\" in msg or \"game_id\" in msg
                    emit({\"type\":\"ack\",\"ok\":True})
                    break
                if msg.get(\"type\") == \"shutdown\":
                    break
            """
        ),
        encoding="utf-8",
    )
    root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.Popen(
        [sys.executable, str(script)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(root),
        env=env,
    )
    assert proc.stdout and proc.stdin
    hello = json.loads(proc.stdout.readline())
    assert hello["type"] == "hello"
    assert hello["seat"] == 1
    state = create_dealt_game("f0002-obs", num_players=4)
    obs = build_observation(state, 1)
    proc.stdin.write(encode_line(msg_observation(obs)))
    proc.stdin.flush()
    ack = json.loads(proc.stdout.readline())
    assert ack.get("ok") is True
    proc.terminate()
    proc.wait(timeout=3)


def test_s03_player_view_empty_has_status_note() -> None:
    """PlayerView.draw with empty view should not raise (dummy display)."""
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((640, 400))
    from display.asset_manager import AssetManager
    from players.view.player_view import PlayerView

    am = AssetManager(theme="green")
    pv = PlayerView(am, seat=0)
    pv.mode = "play"
    # empty view — skeleton UI
    pv.draw(screen, {}, "wait", [], status_note="连接中")
    # with dealt-like view
    st = create_dealt_game("f0002-view", num_players=2)
    obs = build_observation(st, 0)
    pv.draw(screen, obs.view, "exchange", [], status_note="ok")
    pygame.quit()


def test_opponent_hud_helpers() -> None:
    """Seat window opponent HUD: dingque + finished labels."""
    from players.seat_window import _dingque_color, _dingque_label, _status_hud_label

    assert _dingque_label(None) == "未定缺"
    assert _dingque_label("wan") == "万"
    assert _dingque_label("tong") == "筒"
    assert _dingque_label("tiao") == "条"
    assert _dingque_color("wan") == "#ff8a80"
    assert _dingque_color("tong") == "#82b1ff"
    assert _dingque_color("tiao") == "#69f0ae"

    active, fg = _status_hud_label({"status": "active"})
    assert active == "行牌中"
    assert fg.startswith("#")

    hu, hu_fg = _status_hud_label(
        {"status": "finished", "hu_order": 1, "last_win": {"zimo": True}}
    )
    assert "已胡" in hu and "第1家" in hu and "自摸" in hu
    assert hu_fg.startswith("#")

    ron, _ = _status_hud_label(
        {"status": "finished", "hu_order": 2, "last_win": {"zimo": False, "loser": 0}}
    )
    assert "点炮S0" in ron


def test_selected_tile_tw_no_enlarge() -> None:
    """Selection must not enlarge (reflow flicker); same even width as base."""
    from players.seat_window import selected_tile_tw

    assert selected_tile_tw(36) == 36
    assert selected_tile_tw(35) == 34  # snap even
    assert selected_tile_tw(20) == 20
    assert selected_tile_tw(40) == 40
    assert selected_tile_tw(36) % 2 == 0


def test_hand_selection_face_style_gold_frame() -> None:
    """Selected compact hand tiles: gold border; outer size same as unselected."""
    from players.seat_window import TkSeatApp

    class _H:
        pass

    h = _H()
    style = TkSeatApp._tile_face_style.__get__(h, _H)
    on = style(selected=True, compact=True)
    off = style(selected=False, compact=True)
    assert on["border"] == "#ffeb3b"
    assert on["ht"] == off["ht"] == 2  # fixed chrome — no reflow
    assert on["bg"] != off["bg"]
    assert off["border"] == "#143528"  # blends into hand table when unselected


def test_meld_kind_label_zh() -> None:
    from players.seat_window import meld_kind_label

    assert meld_kind_label("pong") == "碰"
    assert meld_kind_label("ming_gang") == "明杠"
    assert meld_kind_label("an_gang") == "暗杠"
    assert meld_kind_label("jia_gang") == "加杠"
    assert meld_kind_label("chow") == "吃"
    assert meld_kind_label("") == "副露"


def test_msg_seat_settings_wire() -> None:
    from protocols.wire import decode_line, encode_line, msg_seat_settings

    m = msg_seat_settings(2, auto_start=True, ai_type="random")
    assert m["type"] == "seat_settings"
    assert m["seat"] == 2
    assert m["auto_start"] is True
    assert m["ai_type"] == "random"
    back = decode_line(encode_line(m))
    assert back["ai_type"] == "random"


def test_hub_compose_players_spec() -> None:
    from players.seat_ui_hub import SeatUIHub

    hub = SeatUIHub(4, human_seat=0)
    hub.seat_ai_types[1] = "random"
    hub.seat_ai_types[2] = "rule_ai"
    # human seat override ignored by compose for human key
    hub.seat_ai_types[0] = "random"
    out = hub.compose_players_spec("human,rule_ai,rule_ai,rule_ai")
    assert out == "human,random,rule_ai,rule_ai"
    hub2 = SeatUIHub(4, human_seat=None)
    hub2.seat_ai_types[0] = "random"
    hub2.seat_ai_types[3] = "random"
    assert hub2.compose_players_spec("rule_ai,rule_ai,rule_ai,rule_ai") == (
        "random,rule_ai,rule_ai,random"
    )


def test_format_round_and_scoreboard() -> None:
    from players.seat_window import format_round_line, format_scoreboard_line

    assert format_round_line(2, 4) == "当前局数: 第 2/4 局"
    assert format_round_line(1, None) == "当前局数: 第 1 局"
    board = format_scoreboard_line(
        [
            {"seat": 0, "score": 12},
            {"seat": 1, "score": -3},
            {"seat": 2, "score": 0},
            {"seat": 3, "score": -9},
        ],
        self_seat=0,
    )
    assert "得分情况" in board
    assert "★S0:+12" in board
    assert "S1:-3" in board
    assert "S2:0" in board
    multi = format_scoreboard_line(
        [{"seat": 0, "score": 1}, {"seat": 1, "score": 2}],
        self_seat=1,
        multiline=True,
    )
    assert "\n" in multi and "★S1:+2" in multi
    assert format_scoreboard_line([], self_seat=0).startswith("得分情况")


def test_format_discard_actor() -> None:
    from players.seat_window import format_discard_actor, format_discard_headline

    assert format_discard_actor(None, 0) == "暂无出牌"
    assert "本座" in format_discard_actor(1, 1)
    assert format_discard_actor(2, 0) == "S2 打出"
    assert format_discard_actor(0, 0) == "本座 S0 打出"
    # one-line actor + tile face
    assert format_discard_headline(2, 0, "wan_5") == "S2 打出 5万"
    assert format_discard_headline(0, 0, "tong_3") == "本座 S0 打出 3筒"
    assert format_discard_headline(None, 0, None) == "暂无出牌"


def test_remain_of_tile_from_view() -> None:
    from players.seat_window import (
        format_remain_badge,
        format_wall_remaining_line,
        remain_of_tile_from_view,
    )

    view = {
        "players": [
            {
                "seat": 0,
                "hand": ["wan_5", "wan_1"],
                "discard_pile": [],
                "melds": [],
            },
            {
                "seat": 1,
                "hand": None,
                "discard_pile": ["wan_5"],
                "melds": [{"kind": "pong", "tile_id": "tong_3"}],
            },
            {
                "seat": 2,
                "discard_pile": [],
                "melds": [{"kind": "gang_an", "tile_id": "wan_5"}],
            },
        ]
    }
    # wan_5: self 1 + disc 1 + gang 4 = 6 → remain max(0,4-6)=0
    assert remain_of_tile_from_view(view, 0, "wan_5") == 0
    # tong_3: pong 3 → remain 1
    assert remain_of_tile_from_view(view, 0, "tong_3") == 1
    # unknown face: remain 4
    assert remain_of_tile_from_view(view, 0, "tiao_9") == 4
    assert remain_of_tile_from_view(view, 0, None) is None
    # badge: digit only
    assert format_remain_badge(2) == "2"
    assert format_remain_badge(0) == "0"
    assert format_remain_badge(None) == ""

    assert format_wall_remaining_line(48) == "牌墙总剩余 48 张"
    assert format_wall_remaining_line(0) == "牌墙总剩余 0 张"
    assert "—" in format_wall_remaining_line(None)


def test_public_view_exposes_last_discard() -> None:
    from engine.session import build_ready_game
    from engine.tile import Tile, Suit
    from protocols.view_filter import filter_state_for_seat

    state = build_ready_game("disc-focus", num_players=4)
    state.last_discard = Tile(Suit.WAN, 5)
    state.last_discard_seat = 2
    view = filter_state_for_seat(state, 0)
    assert view.get("last_discard") == "wan_5"
    assert view.get("last_discard_seat") == 2


def test_public_view_exposes_dingque_and_status_for_opponents() -> None:
    """Opponent HUD needs public dingque/status/hu_order (not only hand_count)."""
    from engine.session import build_ready_game
    from protocols.view_filter import filter_state_for_seat

    state = build_ready_game("hud-opp", num_players=4)
    # mark seat 1 finished for HUD fields
    state.players[1].status = "finished"
    state.players[1].hu_order = 1
    view = filter_state_for_seat(state, 0)
    others = [p for p in view["players"] if p["seat"] != 0]
    assert len(others) == 3
    for p in others:
        assert "hand" not in p
        assert "dingque" in p
        assert "status" in p
        assert "hand_count" in p
    p1 = next(p for p in others if p["seat"] == 1)
    assert p1["status"] == "finished"
    assert p1["hu_order"] == 1
    # ready game always has dingque
    assert p1["dingque"] in ("wan", "tong", "tiao")
