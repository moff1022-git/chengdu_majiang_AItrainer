"""F0013: seat dirty-update helpers + broadcast signature throttle."""

from __future__ import annotations

import sys
import time
from types import SimpleNamespace

import pytest

from engine.deal import create_dealt_game


def test_broadcast_signature_stable_for_same_state() -> None:
    from players.seat_ui_hub import SeatUIHub

    hub = SeatUIHub(4, human_seat=0, theme="green")
    st = create_dealt_game("f0013-sig", num_players=4)
    a = hub._broadcast_signature(st)
    b = hub._broadcast_signature(st)
    assert a == b


def test_broadcast_signature_changes_on_hand_mutation() -> None:
    from players.seat_ui_hub import SeatUIHub

    hub = SeatUIHub(4, human_seat=0, theme="green")
    st = create_dealt_game("f0013-mut", num_players=4)
    a = hub._broadcast_signature(st)
    # mutate seat 0 hand order / content
    p0 = st.players[0]
    if len(p0.hand) >= 2:
        p0.hand[0], p0.hand[1] = p0.hand[1], p0.hand[0]
    b = hub._broadcast_signature(st)
    # sorted multiset may be equal if only swap — force real change
    if a == b and p0.hand:
        p0.hand.pop()
        b = hub._broadcast_signature(st)
    assert a != b


def test_broadcast_skips_identical_within_interval(monkeypatch) -> None:
    from players.seat_ui_hub import SeatUIHub

    hub = SeatUIHub(2, human_seat=0, theme="green")
    hub._broadcast_min_interval_s = 1.0
    st = create_dealt_game("f0013-skip", num_players=2)

    class FakeTr:
        def __init__(self) -> None:
            self.n = 0
            self._proc = SimpleNamespace(poll=lambda: None)

        def send_observation(self, obs) -> None:
            self.n += 1

    tr0, tr1 = FakeTr(), FakeTr()
    hub.transports = {0: tr0, 1: tr1}  # type: ignore[assignment]
    hub.broadcast(st)
    hub.broadcast(st)  # identical + within interval → skip
    assert tr0.n == 1
    assert tr1.n == 1
    # force time pass
    hub._last_broadcast_t = time.time() - 2.0
    hub.broadcast(st)
    assert tr0.n == 2


def test_hand_layout_key_stable() -> None:
    """layout_key is a pure tuple — no second Tk root (Windows Tcl is flaky)."""
    from players.seat_window import TkSeatApp

    k1 = TkSeatApp._hand_layout_key_of(None, 13, 40, 10, recommend_on=False)  # type: ignore[arg-type]
    k2 = TkSeatApp._hand_layout_key_of(None, 13, 40, 10, recommend_on=False)  # type: ignore[arg-type]
    k3 = TkSeatApp._hand_layout_key_of(None, 14, 40, 10, recommend_on=False)  # type: ignore[arg-type]
    assert k1 == k2
    assert k1 != k3


def _make_play_obs_view(
    *,
    seat: int = 0,
    hand: list[str] | None = None,
    discs: list[str] | None = None,
    opp_scores: dict[int, int] | None = None,
    opp_hand_counts: dict[int, int] | None = None,
) -> dict:
    hand = list(hand or [f"b_{i % 9 + 1}" for i in range(13)])
    discs = list(discs or [])
    scores = opp_scores or {1: 100, 2: -50, 3: 0}
    counts = opp_hand_counts or {1: 13, 2: 13, 3: 13}
    players = [
        {
            "seat": seat,
            "hand": hand,
            "melds": [],
            "discard_pile": discs,
            "score": 0,
            "status": "active",
            "dingque": "wan",
            "hand_count": len(hand),
        }
    ]
    for ps in range(4):
        if ps == seat:
            continue
        players.append(
            {
                "seat": ps,
                "hand": [],
                "melds": [],
                "discard_pile": [],
                "score": int(scores.get(ps, 0)),
                "status": "active",
                "dingque": "tiao",
                "hand_count": int(counts.get(ps, 13)),
            }
        )
    return {"players": players, "wall_remaining": 70, "phase": "discard"}


@pytest.mark.skipif(
    sys.platform == "darwin",
    reason=(
        "macOS Tk may abort the Python process during Tk() construction; "
        "covered by pure helper tests and manual/subprocess GUI acceptance"
    ),
)
def test_f0013_tk_inplace_paths_single_root() -> None:
    """Single Tk root covers face/hand/disc/opp dirty paths (Win Tcl flaky multi-root)."""
    import tkinter as tk

    from players.seat_window import TkSeatApp

    try:
        app = TkSeatApp(
            seat=0,
            mode="play",
            theme="green",
            title="f0013-smoke",
            x=20,
            y=20,
            w=520,
            h=420,
        )
    except tk.TclError as e:
        pytest.skip(f"Tk unavailable: {e}")

    app._photo = lambda tid, tw=36: None  # type: ignore[method-assign]

    # --- _update_tile_face identity ---
    parent = tk.Frame(app.root)
    parent.pack()
    b = app._tile_btn(parent, "x_1", selected=False, tw=32)
    id0 = id(b)
    app._update_tile_face(b, "x_2", selected=True, tw=32)
    assert id(b) == id0
    assert getattr(b, "_tid", None) == "x_2"

    # --- full _render_state dirty paths ---
    hand = [f"b_{i % 9 + 1}" for i in range(13)]
    discs = [f"t_{i % 9 + 1}" for i in range(8)]
    view = _make_play_obs_view(hand=hand, discs=discs)
    app.last_obs = SimpleNamespace(view=view, phase="discard")
    app.phase = "discard"
    app.root.update_idletasks()
    app._render_state(force=True)
    app.root.update_idletasks()

    # seat_id must remain int; cell key "seat" is the "S#" Label
    assert len(app._opp_cell_labels) == 3
    for refs in app._opp_cell_labels:
        assert isinstance(refs.get("seat_id"), int)
        assert 0 <= int(refs["seat_id"]) <= 3
        seat_lbl = refs.get("seat")
        assert seat_lbl is not None and hasattr(seat_lbl, "cget")
        assert str(seat_lbl.cget("text")).startswith("S")

    hand_ids_1 = [id(w[1]) for w in app._hand_tile_widgets]
    disc_ids_1 = [id(b2) for b2 in app._disc_tile_widgets]
    opp_score_ids_1 = [id(r["score"]) for r in app._opp_cell_labels]
    assert len(hand_ids_1) == 13
    assert len(disc_ids_1) == 8
    assert len(opp_score_ids_1) == 3

    # Opp score / hand_count only — must not rebuild opp or hand widgets
    view2 = _make_play_obs_view(
        hand=hand,
        discs=discs,
        opp_scores={1: 200, 2: -50, 3: 10},
        opp_hand_counts={1: 12, 2: 13, 3: 13},
    )
    app.last_obs = SimpleNamespace(view=view2, phase="discard")
    app._render_state(force=False)
    app.root.update_idletasks()
    assert [id(w[1]) for w in app._hand_tile_widgets] == hand_ids_1
    assert [id(b2) for b2 in app._disc_tile_widgets] == disc_ids_1
    assert [id(r["score"]) for r in app._opp_cell_labels] == opp_score_ids_1
    by_sid = {int(r["seat_id"]): r for r in app._opp_cell_labels}
    assert by_sid[1]["score"].cget("text") == "200"
    assert by_sid[1]["hand_count"].cget("text") == "12"

    # Same layout, different faces — hand/disc widgets reused
    hand2 = list(hand)
    hand2[0] = "b_9"
    discs2 = list(discs)
    discs2[0] = "t_9"
    view3 = _make_play_obs_view(
        hand=hand2,
        discs=discs2,
        opp_scores={1: 200, 2: -50, 3: 10},
        opp_hand_counts={1: 12, 2: 13, 3: 13},
    )
    app.last_obs = SimpleNamespace(view=view3, phase="discard")
    app._render_state(force=False)
    app.root.update_idletasks()
    assert [id(w[1]) for w in app._hand_tile_widgets] == hand_ids_1
    assert [id(b2) for b2 in app._disc_tile_widgets] == disc_ids_1

    try:
        app.root.destroy()
    except Exception:
        pass
