"""M05 — JSONL logging and runner."""

from __future__ import annotations

import json
from pathlib import Path

from engine.reward import RewardConfig
from engine.session import play_random_game_logged
from training.episode_log import EpisodeLogger
from training.runner import run_random_batch


def test_lg01_jsonl_parseable(tmp_path: Path) -> None:
    result = play_random_game_logged(
        "m05-log-1",
        num_players=2,
        log_dir=tmp_path,
        reward_config=RewardConfig(),
        max_steps=2000,
    )
    path = tmp_path / "m05-log-1.jsonl"
    assert path.exists()
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) >= 2
    types = [json.loads(x)["type"] for x in lines]
    assert "game_start" in types
    assert "game_end" in types
    assert result.finished_reason


def test_lg02_runner_batch(tmp_path: Path) -> None:
    summary = run_random_batch(
        3,
        log_dir=tmp_path / "batch",
        num_players=2,
        seed=42,
        max_steps=3000,
    )
    assert summary["finished"] == 3
    files = list((tmp_path / "batch").glob("*.jsonl"))
    assert len(files) == 3


def test_episode_logger_basic(tmp_path: Path) -> None:
    with EpisodeLogger(tmp_path, "g1") as log:
        log.emit("game_start", game_id="g1")
        log.emit("game_end", ok=True)
    text = (tmp_path / "g1.jsonl").read_text(encoding="utf-8")
    assert "game_start" in text
