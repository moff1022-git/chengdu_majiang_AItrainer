"""Headless batch runner with JSONL logging (M05/M06)."""

from __future__ import annotations

import argparse
import random
import secrets
from datetime import datetime, timezone
from pathlib import Path

from engine.config import EngineConfig
from engine.reward import RewardConfig
from engine.rng_v2 import derive_coordinate_seed


def run_random_batch(
    n_games: int,
    *,
    log_dir: Path | str,
    reward_path: Path | str | None = None,
    num_players: int = 4,
    seed: int = 0,
    max_steps: int = 10_000,
    player_specs: str | None = None,
    rng_version: int = 1,
) -> dict:
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    reward_cfg = RewardConfig.load(reward_path)
    rng = random.Random(seed)
    summary = {
        "games": n_games,
        "finished": 0,
        "reasons": {},
        "log_dir": str(log_dir),
        "player_specs": player_specs,
    }

    for i in range(n_games):
        game_id = f"batch-{seed}-{i}"
        if rng_version == 2:
            game_seed = derive_coordinate_seed(game_id=game_id, stream_name="training_noise", consumer_kind="trainer", consumer_id="batch", event_id="game", sample_index=i).sample_seed
        elif rng_version == 1:
            game_seed = rng.randint(0, 2**30)
        else:
            raise ValueError("rng_version must be 1 or 2")
        if player_specs:
            from engine.orchestrator import run_players_game

            parts = [p.strip() for p in player_specs.split(",") if p.strip()]
            cfg = EngineConfig(num_players=len(parts))
            result = run_players_game(
                player_specs,
                game_id=game_id,
                config=cfg,
                base_seed=game_seed,
                log_dir=log_dir,
                reward_config=reward_cfg,
                max_steps=max_steps,
            )
        else:
            from engine.session import play_random_game_logged

            cfg = EngineConfig(num_players=num_players)
            result = play_random_game_logged(
                game_id,
                num_players=num_players,
                config=cfg,
                rng=random.Random(game_seed),
                max_steps=max_steps,
                log_dir=log_dir,
                reward_config=reward_cfg,
            )
        summary["finished"] += 1
        r = result.finished_reason
        summary["reasons"][r] = summary["reasons"].get(r, 0) + 1

    return summary


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Chengdu mahjong batch runner")
    parser.add_argument("--games", type=int, default=10)
    parser.add_argument("--log-dir", type=str, default=None)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--rng-version", type=int, choices=(1, 2), default=1)
    parser.add_argument(
        "--num-players",
        type=int,
        default=4,
        help="Used when --players is not set",
    )
    parser.add_argument(
        "--players",
        type=str,
        default=None,
        help="Comma-separated types, e.g. rule_ai,rule_ai,random,random",
    )
    parser.add_argument("--reward", type=str, default=None)
    args = parser.parse_args(argv)

    if args.log_dir is None:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        args.log_dir = f"logs/cmjrun-{ts}-{secrets.token_hex(3)}"

    summary = run_random_batch(
        args.games,
        log_dir=args.log_dir,
        reward_path=args.reward,
        num_players=args.num_players,
        seed=args.seed,
        player_specs=args.players,
        rng_version=args.rng_version,
    )
    print(summary)


if __name__ == "__main__":
    main()
