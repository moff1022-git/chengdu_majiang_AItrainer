"""F0020 — multi-human modes: layout B/D, hub human_seats, registry."""

from __future__ import annotations

from display.window_geometry import (
    GAP,
    compute_window_plan,
    layout_canvas,
    plan_mode_D,
    resolve_layout_mode,
    windows_overlap,
)
from players.human_proxy import HumanPlayerProxy
from players.registry import create_players
from players.rule_ai_player import RuleAIPlayer
from players.seat_ui_hub import SeatUIHub


def test_resolve_modes_f0020() -> None:
    assert resolve_layout_mode(1, 3) == "A"
    assert resolve_layout_mode(2, 2) == "B"
    assert resolve_layout_mode(3, 1) == "D"
    assert resolve_layout_mode(0, 4) == "C"
    assert resolve_layout_mode(4, 0) is None


def test_plan_b_two_humans() -> None:
    plan = compute_window_plan(
        4, desktop=(1920, 1080), origin=(0, 0), human_seats=[1, 2]
    )
    assert plan.layout_mode == "B"
    # H[0]=seat1 bottom-right, H[1]=seat2 top-right
    assert 1 in plan.players and 2 in plan.players
    assert plan.players[1].y >= plan.main.y - 2
    assert plan.players[2].y <= plan.main.y


def test_plan_d_three_humans_no_overlap() -> None:
    canvas = layout_canvas(1920, 1080)
    main, pl = plan_mode_D(canvas, human_seats=[0, 1, 2], ai_seats=[3])
    assert pl[3].h == 249  # Ha — must not grow
    body_top = canvas.y + pl[3].h + GAP
    assert pl[1].y == body_top
    assert pl[2].y == body_top
    assert main.y == body_top + pl[1].h
    assert pl[0].y == main.y
    # pairwise non-overlap
    rects = [main] + [pl[s] for s in sorted(pl)]
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            # main vs pl[0] share edge ok if no area overlap
            assert not windows_overlap(rects[i], rects[j]), (i, j)


def test_hub_human_seats_mode_for() -> None:
    hub = SeatUIHub(4, human_seats=[0, 2], theme="green")
    assert hub.human_seats == [0, 2]
    assert hub.human_seat == 0
    assert hub._mode_for(0) == "play"
    assert hub._mode_for(1) == "watch"
    assert hub._mode_for(2) == "play"
    assert hub._mode_for(3) == "watch"

    hub1 = SeatUIHub(4, human_seat=1, theme="green")
    assert hub1.human_seats == [1]
    assert hub1._mode_for(1) == "play"
    assert hub1._mode_for(0) == "watch"


def test_create_players_2h_3h() -> None:
    p = create_players("human,human,rule_ai,rule_ai", base_seed=9)
    assert isinstance(p[0], HumanPlayerProxy)
    assert isinstance(p[1], HumanPlayerProxy)
    assert isinstance(p[2], RuleAIPlayer)

    p3 = create_players("rule_ai,human,human,human", base_seed=3)
    humans = [i for i, x in enumerate(p3) if isinstance(x, HumanPlayerProxy)]
    assert humans == [1, 2, 3]
