"""F0003: enable_exchange skip, meld draw, human proxy owns transport."""

from __future__ import annotations

import os

from engine.config import EngineConfig
from engine.deal import create_dealt_game
from engine.opening import begin_opening, begin_dingque_skip_exchange
from engine.tile import Suit


def test_enable_exchange_false_skips_to_dingque() -> None:
    cfg = EngineConfig(num_players=4, enable_exchange=False)
    state = create_dealt_game("f0003-no-ex", config=cfg)
    assert state.phase == "dealt"
    begin_opening(state, cfg)
    assert state.phase == "dingque"
    assert not state.exchange_log
    assert not (state.pending_exchange or {})


def test_enable_exchange_true_enters_exchange() -> None:
    cfg = EngineConfig(num_players=4, enable_exchange=True)
    state = create_dealt_game("f0003-ex", config=cfg)
    begin_opening(state, cfg)
    assert state.phase == "exchange"


def test_begin_dingque_skip_exchange_direct() -> None:
    state = create_dealt_game("f0003-skip", num_players=3)
    begin_dingque_skip_exchange(state, EngineConfig(num_players=3, enable_exchange=False))
    assert state.phase == "dingque"
    from engine.opening import submit_dingque

    suits = [Suit.WAN, Suit.TONG, Suit.TIAO]
    for s in range(3):
        submit_dingque(state, s, suits[s])
    assert state.phase == "ready"


def test_config_roundtrip_enable_exchange() -> None:
    c = EngineConfig(num_players=2, enable_exchange=False)
    d = c.to_dict()
    assert d["enable_exchange"] is False
    c2 = EngineConfig.from_dict(d)
    assert c2.enable_exchange is False


def test_player_view_draws_melds_without_raise() -> None:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    from display.asset_manager import AssetManager
    from players.view.player_view import PlayerView

    am = AssetManager(theme="green")
    pv = PlayerView(am, seat=0)
    pv.mode = "play"
    view = {
        "wall_remaining": 50,
        "players": [
            {
                "seat": 0,
                "hand": ["W1", "W2", "W3", "T4", "T5"],
                "score": 0,
                "status": "active",
                "melds": [
                    {"kind": "pong", "tile_id": "B5"},
                    {"kind": "ming_gang", "tile_id": "W9"},
                ],
                "discard_pile": ["T1", "T2"],
            },
            {
                "seat": 1,
                "hand_count": 10,
                "score": 0,
                "status": "active",
                "melds": [{"kind": "pong", "tile_id": "T3"}],
            },
        ],
    }
    pv.draw(screen, view, "discard", [], status_note="meld test")
    pygame.quit()


def test_human_proxy_attached_shutdown_does_not_clear_unowned() -> None:
    """Attached (hub-owned) transport must not be killed on shutdown."""
    from players.human_proxy import HumanPlayerProxy

    class FakeTr:
        def __init__(self) -> None:
            self.shutdown_calls = 0

        def shutdown(self) -> None:
            self.shutdown_calls += 1

        def send_game_end(self, _r: dict) -> None:
            pass

    proxy = HumanPlayerProxy()
    tr = FakeTr()
    proxy.attach_transport(tr, 0)  # type: ignore[arg-type]
    assert proxy._owns_transport is False
    proxy.shutdown()
    assert tr.shutdown_calls == 0
    assert proxy._transport is tr  # still attached for next hand
