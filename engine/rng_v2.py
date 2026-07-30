"""ALGO-011 stateless, versioned named random derivation."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path

RNG_VERSION = 2
ALGORITHM_VERSION = 2
STREAMS = frozenset({"shuffle", "dice", "exchange", "deal", "policy_noise", "training_noise"})


class RngV2Error(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _s(value: str) -> bytes:
    if not isinstance(value, str) or not value:
        raise RngV2Error("SCHEMA_INVALID", "coordinate strings must be non-empty")
    raw = value.encode("utf-8")
    if len(raw) > 256:
        raise RngV2Error("SCHEMA_INVALID", "coordinate string too long")
    return len(raw).to_bytes(2, "big") + raw


def _seed(data: bytes) -> int:
    return int.from_bytes(hashlib.blake2b(data, digest_size=8).digest(), "big")


def master_input(game_id: str, algorithm_version: int = 2, rng_version: int = 2) -> bytes:
    if (algorithm_version, rng_version) != (2, 2):
        raise RngV2Error("RNG_VERSION_UNKNOWN", "only algorithm/rng version 2 is supported")
    return b"CDMJ-RNG\x00master\x00" + _s(game_id) + algorithm_version.to_bytes(2, "big") + rng_version.to_bytes(2, "big")


def stream_input(master_seed: int, stream_name: str, rng_version: int = 2) -> bytes:
    if stream_name not in STREAMS:
        raise RngV2Error("STREAM_UNKNOWN", stream_name)
    return b"CDMJ-RNG\x00stream\x00" + master_seed.to_bytes(8, "big") + _s(stream_name) + rng_version.to_bytes(2, "big")


def coordinate_input(stream_seed: int, stream_name: str, consumer_kind: str, consumer_id: str, event_id: str, sample_index: int) -> bytes:
    if stream_name not in STREAMS or sample_index < 0 or sample_index > 2**64 - 1:
        raise RngV2Error("SCHEMA_INVALID", "invalid stream or sample index")
    return b"CDMJ-RNG\x00coord\x00" + stream_seed.to_bytes(8, "big") + _s(stream_name) + _s(consumer_kind) + _s(consumer_id) + _s(event_id) + sample_index.to_bytes(8, "big")


@dataclass(frozen=True, slots=True)
class SeedTraceRestricted:
    algorithm_version: int
    rng_version: int
    master_seed: int
    stream_name: str
    logical_consumer: str
    logical_event_id: str
    logical_index: int
    sample_seed: int

    def strategy_ref(self) -> dict[str, object]:
        opaque = hashlib.sha256(repr((self.algorithm_version, self.rng_version, self.master_seed, self.stream_name, self.logical_consumer, self.logical_event_id, self.logical_index)).encode()).hexdigest()
        return {"rng_used": True, "algorithm_version": self.algorithm_version, "rng_version": self.rng_version, "trace_ref": opaque}

    def audit_envelope(self) -> dict[str, object]:
        """Seven-field Frozen audit projection; sensitive values are hashed."""
        ref = self.strategy_ref()["trace_ref"]
        return {"algorithm_version": self.algorithm_version, "rng_version": self.rng_version, "master_hash": hashlib.sha256(self.master_seed.to_bytes(8, "big")).hexdigest(), "stream_names": [self.stream_name], "seed_hashes": [hashlib.sha256(self.sample_seed.to_bytes(8, "big")).hexdigest()], "coordinate_hash": hashlib.sha256(f"{self.logical_consumer}:{self.logical_event_id}:{self.logical_index}".encode()).hexdigest(), "trace_ref": ref}


def derive_coordinate_seed(*, game_id: str, stream_name: str, consumer_kind: str, consumer_id: str, event_id: str, sample_index: int) -> SeedTraceRestricted:
    master = _seed(master_input(game_id))
    stream = _seed(stream_input(master, stream_name))
    sample = _seed(coordinate_input(stream, stream_name, consumer_kind, consumer_id, event_id, sample_index))
    return SeedTraceRestricted(2, 2, master, stream_name, f"{consumer_kind}:{consumer_id}", event_id, sample_index, sample)


def select_rng_version(record: dict[str, object]) -> str:
    fmt = record.get("record_format")
    if fmt == "legacy-pre-rng-version" and "rng_version" not in record:
        return "legacy-v1"
    if fmt == "rng-v2-new-record" and record.get("rng_version") == 2:
        return "rng-v2"
    if fmt == "rng-v2-new-record" and record.get("rng_version") is not None:
        raise RngV2Error("RNG_VERSION_UNKNOWN", "unknown RNG version")
    raise RngV2Error("SCHEMA_INVALID", "record RNG version is missing or invalid")


class RestrictedSeedTraceStore:
    """Engine/audit-only append store; strategy projections contain only opaque refs."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, trace: SeedTraceRestricted) -> str:
        ref = str(trace.strategy_ref()["trace_ref"])
        row = {"trace_ref": ref, **{name: getattr(trace, name) for name in trace.__dataclass_fields__}}
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        return ref
