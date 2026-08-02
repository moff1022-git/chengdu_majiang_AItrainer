"""Stable fixed action codec for training contract v2."""

from __future__ import annotations

from itertools import combinations_with_replacement

from engine.action import Action, ActionType
from engine.tile import Suit, Tile

ACTION_CODEC_VERSION = 2
ACTION_SPACE_SIZE = 635
FACE_ACTIONS = (ActionType.PONG, ActionType.GANG_MING, ActionType.GANG_AN, ActionType.GANG_JIA, ActionType.DISCARD)
FACE_OFFSETS = dict(zip(FACE_ACTIONS, (2, 29, 56, 83, 110)))


class ActionCodecError(ValueError):
    code = "ACTION_CODEC_INVALID"

    def __init__(self, detail: str) -> None:
        super().__init__(f"{self.code}: {detail}")


def _face_index(tile: Tile) -> int:
    return tile.suit.sort_key * 9 + tile.rank - 1


EXCHANGE_TUPLES: tuple[tuple[Tile, Tile, Tile], ...] = tuple(
    tuple(Tile(suit, rank) for rank in ranks)  # type: ignore[arg-type]
    for suit in Suit
    for ranks in combinations_with_replacement(range(1, 10), 3)
)
_EXCHANGE_INDEX = {tuple(tile.id for tile in tiles): 137 + i for i, tiles in enumerate(EXCHANGE_TUPLES)}


def encode_action(action: Action) -> int:
    if action.type == ActionType.PASS and not action.tiles and action.suit is None:
        return 0
    if action.type == ActionType.HU and len(action.tiles) <= 1 and action.suit is None:
        return 1
    if action.type in FACE_OFFSETS and len(action.tiles) == 1 and action.suit is None:
        return FACE_OFFSETS[action.type] + _face_index(action.tiles[0])
    if action.type == ActionType.EXCHANGE and len(action.tiles) == 3 and action.suit is None:
        key = tuple(tile.id for tile in sorted(action.tiles))
        try:
            return _EXCHANGE_INDEX[key]
        except KeyError as exc:
            raise ActionCodecError("exchange must contain three same-suit tile faces") from exc
    if action.type == ActionType.DINGQUE and not action.tiles and action.suit is not None:
        return 632 + action.suit.sort_key
    raise ActionCodecError(f"unsupported action structure: {action}")


def decode_action(index: int) -> Action:
    if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < ACTION_SPACE_SIZE:
        raise ActionCodecError(f"action index out of range: {index!r}")
    if index == 0:
        return Action(ActionType.PASS)
    if index == 1:
        return Action(ActionType.HU)
    for action_type, offset in FACE_OFFSETS.items():
        if offset <= index < offset + 27:
            face = index - offset
            return Action(action_type, tiles=(Tile(tuple(Suit)[face // 9], face % 9 + 1),))
    if 137 <= index < 632:
        return Action(ActionType.EXCHANGE, tiles=EXCHANGE_TUPLES[index - 137])
    return Action(ActionType.DINGQUE, suit=tuple(Suit)[index - 632])


def legal_action_mask(actions: list[Action] | tuple[Action, ...]) -> tuple[int, ...]:
    mask = [0] * ACTION_SPACE_SIZE
    for action in actions:
        mask[encode_action(action)] = 1
    return tuple(mask)
