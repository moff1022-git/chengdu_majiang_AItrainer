"""Game id generation and deterministic seed derivation."""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timezone

_MASK_64 = 0xFFFFFFFFFFFFFFFF
_DICE_XOR = 0xA5A5A5A5A5A5A5A5
_EXCHANGE_XOR = 0x5A5A5A5A5A5A5A5A


@dataclass(frozen=True, slots=True)
class DerivedSeeds:
    master_seed: int
    shuffle_seed: int
    dice_seed: int
    exchange_seed: int  # reserved for M02; not consumed in M01


def normalize_game_id(game_id: str) -> str:
    if not isinstance(game_id, str):
        raise ValueError("game_id must be a string")
    gid = game_id.strip()
    if not gid:
        raise ValueError("game_id must be non-empty")
    return gid


def generate_game_id() -> str:
    """Create a new unique id: ``cmj-{utc_yyyymmdd_hhmmss}-{8hex}``."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    suffix = secrets.token_hex(4)
    return f"cmj-{ts}-{suffix}"


def master_seed_from_game_id(game_id: str) -> int:
    gid = normalize_game_id(game_id)
    digest = hashlib.blake2b(gid.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big")


def derive_seeds(game_id: str) -> DerivedSeeds:
    master = master_seed_from_game_id(game_id)
    shuffle = master & _MASK_64
    dice = (master ^ _DICE_XOR) & _MASK_64
    exchange = (master ^ _EXCHANGE_XOR) & _MASK_64
    return DerivedSeeds(
        master_seed=master,
        shuffle_seed=shuffle,
        dice_seed=dice,
        exchange_seed=exchange,
    )
