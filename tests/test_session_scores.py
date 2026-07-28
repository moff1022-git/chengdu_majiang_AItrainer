"""Multi-round session score carry-over."""

from __future__ import annotations

from engine.config import EngineConfig
from engine.orchestrator import PlayerGameRunner
from players.random_player import RandomPlayer


def test_starting_scores_applied_at_run_start() -> None:
    """PlayerGameRunner must inject cumulative scores right after deal."""
    seen: list[dict[int, int]] = []

    def on_state(st) -> None:
        if not seen:
            seen.append({p.seat: p.score for p in st.players})

    players = [RandomPlayer(i) for i in range(4)]
    start = {0: 10, 1: -5, 2: 0, 3: 3}
    runner = PlayerGameRunner(
        players,
        EngineConfig(num_players=4),
        game_id="session-score-run",
        starting_scores=start,
        max_steps=3,
        save_on_end=False,
        on_state_change=on_state,
        step_delay_ms=0,
    )
    result = runner.run()
    assert seen, "on_state_change should fire at least once"
    assert seen[0] == start
    # Final scores should still be defined for all seats
    assert set(result.scores.keys()) == {0, 1, 2, 3}


def test_second_hand_starts_from_previous_totals() -> None:
    """Simulate two hands: second hand starting_scores = first result.scores."""
    players1 = [RandomPlayer(i) for i in range(2)]
    r1 = PlayerGameRunner(
        players1,
        EngineConfig(num_players=2, enable_exchange=False),
        game_id="session-h1",
        starting_scores={0: 0, 1: 0},
        max_steps=200,
        save_on_end=False,
    )
    res1 = r1.run()
    assert res1.scores

    first_snap: list[dict[int, int]] = []

    def on_state(st) -> None:
        if not first_snap:
            first_snap.append({p.seat: p.score for p in st.players})

    players2 = [RandomPlayer(i) for i in range(2)]
    r2 = PlayerGameRunner(
        players2,
        EngineConfig(num_players=2, enable_exchange=False),
        game_id="session-h2",
        starting_scores=dict(res1.scores),
        max_steps=3,
        save_on_end=False,
        on_state_change=on_state,
    )
    r2.run()
    assert first_snap
    assert first_snap[0] == res1.scores
