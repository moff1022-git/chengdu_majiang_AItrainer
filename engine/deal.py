"""One-shot dealt game creation from game_id."""

from __future__ import annotations

from engine.config import EngineConfig
from engine.deck import Deck, deal_hands
from engine.dice import roll_dice
from engine.game_id import derive_seeds, generate_game_id, normalize_game_id
from engine.state import GameState, PlayerState, config_snapshot
from engine.tile import sorted_tiles


def create_dealt_game(
    game_id: str | None = None,
    *,
    num_players: int = 4,
    initial_score: int = 0,
    config: EngineConfig | None = None,
) -> GameState:
    """
    Build a reproducible phase='dealt' GameState.

    If game_id is None, a new id is generated. Same game_id always yields
    the same dice, dealer, hands, and remaining wall.
    """
    if config is None:
        config = EngineConfig(num_players=num_players, initial_score=initial_score)
    else:
        # Explicit kwargs only apply when config is not passed; if both given,
        # prefer config object but allow validation.
        if num_players != 4 or initial_score != 0:
            # Keep simple: config object wins when provided.
            pass

    if game_id is None:
        gid = generate_game_id()
    else:
        gid = normalize_game_id(game_id)

    seeds = derive_seeds(gid)
    dice = roll_dice(seeds.dice_seed, config.num_players)
    deck = Deck.create_shuffled(seeds.shuffle_seed)
    hands = deal_hands(
        deck,
        num_players=config.num_players,
        dealer_seat=dice.dealer_seat,
    )

    players: list[PlayerState] = []
    for seat in range(config.num_players):
        players.append(
            PlayerState(
                seat=seat,
                # 万→筒→条，点数升序（展示与引擎一致）
                hand=sorted_tiles(hands[seat]),
                score=config.initial_score,
                is_dealer=(seat == dice.dealer_seat),
            )
        )

    state = GameState(
        game_id=gid,
        master_seed=seeds.master_seed,
        phase="dealt",
        num_players=config.num_players,
        dice=dice,
        dealer_seat=dice.dealer_seat,
        wall=deck.remaining_tiles(),
        players=players,
        turn_index=0,
        config=config_snapshot(config),
        current_seat=None,
        exchange_dir_resolved=None,
        pending_exchange={},
        exchange_log=[],
    )
    state.validate()
    return state
