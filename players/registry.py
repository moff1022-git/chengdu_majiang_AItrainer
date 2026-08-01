"""Player type registry and factory."""

from __future__ import annotations

from typing import Type

from players.base_player import BasePlayer
from players.human_proxy import HumanPlayerProxy
from players.humanlike.player import HumanlikeV2Player
from players.random_player import RandomPlayer
from players.rule_ai_player import RuleAIPlayer
from players.strategy_presets import (
    ensure_profile_applied,
    get_preset,
    list_strategy_ids,
    player_options_for_spec,
    resolve_player_key,
)

PLAYER_REGISTRY: dict[str, Type[BasePlayer]] = {
    "random": RandomPlayer,
    "rule_ai": RuleAIPlayer,
    "human": HumanPlayerProxy,
    "humanlike_v2": HumanlikeV2Player,
}


def create_player(
    spec: str,
    *,
    seat: int | None = None,
    seed: int | None = None,
    training_mode: bool = True,
    theme: str = "green",
    human_timeout_ms: int = 120_000,
    humanlike_preset: str | None = None,
) -> BasePlayer:
    """
    spec: "random" | "rule_ai" | "rule_ai_plus" | "humanlike_v2" | "human" | "rule_ai:Bot1"

    Strategy preset ids from ``configs/strategies/presets.json`` resolve to a
    base player type plus options (e.g. use_f0011).
    """
    name = ""
    key = spec.strip()
    if ":" in key:
        key, name = key.split(":", 1)
        key, name = key.strip(), name.strip()
    key = key.lower()
    opts = player_options_for_spec(key)
    # Resolve preset → registry key
    if key not in PLAYER_REGISTRY:
        if get_preset(key) is not None:
            ensure_profile_applied(key)
            key = resolve_player_key(key)
        else:
            known = sorted(set(PLAYER_REGISTRY) | set(list_strategy_ids()))
            raise ValueError(f"unknown player type {key!r}; known: {known}")
    else:
        # still apply profile if bare rule_ai is also a preset with profile (no)
        pass
    cls = PLAYER_REGISTRY[key]
    join_cfg: dict = {"theme": theme, **opts}
    if cls is HumanPlayerProxy:
        player = HumanPlayerProxy(
            name=name or "Human",
            seed=seed,
            training_mode=False,
            theme=theme,
            timeout_ms=human_timeout_ms,
        )
        # Defer subprocess spawn until orchestrator on_join with full config
        if seat is not None:
            player.seat = seat
        if opts.get("use_f0011"):
            setattr(player, "use_f0011", True)
    else:
        display = name
        if not display and opts.get("strategy_id"):
            display = str(opts["strategy_id"])
        extra = {"preset_id": humanlike_preset} if cls is HumanlikeV2Player and humanlike_preset else {}
        player = cls(name=display or "", seed=seed, training_mode=training_mode, **extra)
        if opts.get("use_f0011"):
            setattr(player, "use_f0011", True)
        if opts.get("strategy_id"):
            setattr(player, "strategy_id", opts["strategy_id"])
        if seat is not None:
            player.on_join(seat, join_cfg)
    return player


def create_players(
    specs: str | list[str],
    *,
    base_seed: int = 0,
    training_mode: bool = True,
    theme: str = "green",
    human_timeout_ms: int = 120_000,
    humanlike_presets: list[str | None] | None = None,
) -> list[BasePlayer]:
    """
    specs: "human,rule_ai,rule_ai,rule_ai" or list of specs.

    F0020: multiple humans allowed (1–3 with remaining AI; see layout A/B/D).
    """
    if isinstance(specs, str):
        parts = [p.strip() for p in specs.split(",") if p.strip()]
    else:
        parts = list(specs)
    human_n = sum(1 for p in parts if p.split(":")[0].strip().lower() == "human")
    if human_n > 3:
        raise ValueError("F0020 supports at most 3 human players (use layout A/B/D)")
    players: list[BasePlayer] = []
    for i, spec in enumerate(parts):
        # Defer human spawn: on_join when seat assigned
        # create_player with seat spawns human immediately
        players.append(
            create_player(
                spec,
                seat=i,
                seed=base_seed + i * 9973,
                training_mode=training_mode,
                theme=theme,
                human_timeout_ms=human_timeout_ms,
                humanlike_preset=humanlike_presets[i] if humanlike_presets and i < len(humanlike_presets) else None,
            )
        )
    return players
