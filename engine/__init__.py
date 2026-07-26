"""Chengdu mahjong engine."""

from engine.action import Action, ActionType
from engine.blood_battle import GameResult, PlayError, apply_action, start_play
from engine.config import EngineConfig
from engine.deal import create_dealt_game
from engine.deck import Deck, build_full_wall, deal_hands, shuffle_wall
from engine.dice import DiceResult, roll_dice
from engine.exchange import (
    ExchangeError,
    pick_same_suit_triple,
    resolve_exchange_direction,
)
from engine.fan import FanError, FanResult, FanTable, WinContext, compute_fan
from engine.game_id import DerivedSeeds, derive_seeds, generate_game_id, normalize_game_id
from engine.hand_utils import MeldView
from engine.legal import legal_actions
from engine.opening import (
    OpeningError,
    begin_dingque_skip_exchange,
    begin_exchange,
    begin_opening,
    get_opening_status,
    run_opening_with_choices,
    submit_dingque,
    submit_exchange,
)
from engine.reward import RewardCalculator, RewardConfig
from engine.score import ScoreService, ScoreTransfer, ScoreTable
from engine.session import GameSession, build_ready_game, play_random_game
from engine.shanten import ShantenResult, shanten
from engine.state import (
    SCHEMA_VERSION,
    GameState,
    PlayerState,
    state_from_json,
    state_to_json,
)
from engine.tile import Suit, Tile, ids_to_tiles, parse_tile, tiles_to_ids
from engine.win_check import WinCheckResult, WinForm, is_winning_hand

__all__ = [
    "SCHEMA_VERSION",
    "Action",
    "ActionType",
    "Deck",
    "DerivedSeeds",
    "DiceResult",
    "EngineConfig",
    "ExchangeError",
    "FanError",
    "FanResult",
    "FanTable",
    "GameResult",
    "GameSession",
    "GameState",
    "MeldView",
    "OpeningError",
    "PlayError",
    "PlayerState",
    "RewardCalculator",
    "RewardConfig",
    "ScoreService",
    "ScoreTable",
    "ScoreTransfer",
    "ShantenResult",
    "Suit",
    "Tile",
    "WinCheckResult",
    "WinContext",
    "WinForm",
    "apply_action",
    "begin_dingque_skip_exchange",
    "begin_exchange",
    "begin_opening",
    "build_full_wall",
    "build_ready_game",
    "compute_fan",
    "create_dealt_game",
    "deal_hands",
    "derive_seeds",
    "generate_game_id",
    "get_opening_status",
    "ids_to_tiles",
    "is_winning_hand",
    "legal_actions",
    "normalize_game_id",
    "parse_tile",
    "pick_same_suit_triple",
    "play_random_game",
    "resolve_exchange_direction",
    "roll_dice",
    "run_opening_with_choices",
    "shanten",
    "shuffle_wall",
    "start_play",
    "state_from_json",
    "state_to_json",
    "submit_dingque",
    "submit_exchange",
    "tiles_to_ids",
]
