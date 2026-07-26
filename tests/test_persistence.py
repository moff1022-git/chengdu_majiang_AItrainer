"""M10 — save/load and resume tests."""

from __future__ import annotations

from pathlib import Path

from engine.blood_battle import start_play
from engine.config import EngineConfig
from engine.orchestrator import run_players_game
from engine.persistence import load_game, save_game
from engine.replay import ReplaySession, StepRecorder
from engine.session import build_ready_game
from engine.state import GameState


def test_s01_save_load_roundtrip(tmp_path: Path) -> None:
    state = build_ready_game("m10-save", num_players=2)
    start_play(state)
    path = tmp_path / "m10-save.json"
    save_game(path, state, config=EngineConfig(num_players=2))
    loaded, meta = load_game(path)
    assert loaded.game_id == state.game_id
    assert loaded.phase == state.phase
    assert loaded.dealer_seat == state.dealer_seat
    assert [t.id for t in loaded.wall] == [t.id for t in state.wall]
    for a, b in zip(loaded.players, state.players):
        assert [t.id for t in a.hand] == [t.id for t in b.hand]
    assert meta["game_id"] == "m10-save"


def test_s02_load_and_continue(tmp_path: Path) -> None:
    # play a bit via runner with save
    result = run_players_game(
        "random,random",
        game_id="m10-cont",
        base_seed=3,
        max_steps=5000,
        save_dir=tmp_path,
        save_on_end=True,
    )
    path = tmp_path / "m10-cont.json"
    assert path.exists()
    state, meta = load_game(path)
    assert state.phase == "finished"
    assert result.finished_reason


def test_s03_steps_replay(tmp_path: Path) -> None:
    state = build_ready_game("m10-steps", num_players=2)
    rec = StepRecorder(tmp_path / "m10-steps.steps.jsonl", snapshot_every=1)
    rec.record_snapshot(state)
    start_play(state)
    rec.record_snapshot(state)
    replay = ReplaySession(tmp_path / "m10-steps.steps.jsonl")
    assert len(replay) >= 2
    f0 = replay.frame(0)
    assert f0.phase == "ready"
    f1 = replay.step_forward()
    assert f1.phase == "discard"
