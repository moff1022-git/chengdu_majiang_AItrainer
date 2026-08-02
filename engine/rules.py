"""Rule helpers derived from EngineConfig / state.config."""

from __future__ import annotations

from engine.config import EngineConfig
from engine.state import GameState


def config_from_state(state: GameState, config: EngineConfig | None = None) -> EngineConfig:
    if config is not None:
        return config
    if state.config:
        try:
            return EngineConfig.from_dict(state.config)
        except ValueError:
            pass
    return EngineConfig(num_players=state.num_players)


def multi_ron_enabled(state: GameState, config: EngineConfig | None = None) -> bool:
    return config_from_state(state, config).multi_ron


def force_discard_dingque(state: GameState, config: EngineConfig | None = None) -> bool:
    return config_from_state(state, config).force_discard_dingque
